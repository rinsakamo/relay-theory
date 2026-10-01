#!/usr/bin/env python3
"""Post-fit-only join of separately frozen Paper2 #384 Stage C and D.
No layer re-fitting, grading, carrier reconstruction, or role verdict.
"""
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path("paper/validation/jgps-major-revision/reflexive-audit-v1")
J = ROOT / "stage-d-postfit-evidence-join-v1.json"
EXPECTED_JOIN_SHA = "4c5f1e53a1cbe5ecbf9d167fdc8a0cea6c230143"
EXPECTED_INDEX_SHA = "7a4a9bb1df15aa1b12de51e9ca048565601964a0"
EXPECTED_PROFILE_SHA = "500621e62357e157c2c52935ff53d3c292b1547b"
LEVELS = ("E0", "E1", "E2", "E3")
LAYERS = ("L_claim", "L_ctx", "L_sys", "L_formal")

def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def sha(p):
    return subprocess.run(["git", "hash-object", str(p)],check=True,
                          capture_output=True,text=True).stdout.strip()

def check(ok, msg):
    if not ok:
        raise AssertionError(msg)

def audit():
    j = read(J)
    index = read(ROOT / "reflexive-stage-d-index-v1.json")
    p = read(ROOT / "reflexive-evidence-profile-v1.json")
    check(sha(J) == EXPECTED_JOIN_SHA and
          sha(ROOT / "reflexive-stage-d-index-v1.json") == EXPECTED_INDEX_SHA and
          sha(ROOT / "reflexive-evidence-profile-v1.json") == EXPECTED_PROFILE_SHA,
          "postfit join or source freeze drift")
    check(j["status"] == "FROZEN_POST_LAYER_PLACEMENT_JOIN"
          and j["sequencing"]["join_only_after_stage_d_ci"]
          and j["sequencing"]["stage_d_layer_placement_frozen_without_grade"]
          and j["sequencing"]["evidence_profile_used_to_change_fit"] is False,
          "fit/evidence sequencing drift")
    check(j["authorities"]["evidence"]["blob_sha"] == EXPECTED_PROFILE_SHA and
          j["authorities"]["placement_index"]["blob_sha"] == EXPECTED_INDEX_SHA,
          "source reference drift")
    grade_by_id = {a["self_target_id"] + "." + r["relation_id"]:r
                   for a in p["annotations"] for r in a["relations"]}
    check(len(grade_by_id) == 68 and len(j["joins"]) == 68,
          "grade/join identity count drift")
    typed = []
    for i, pin in enumerate(j["authorities"]["placement_batches"]):
        path = ROOT / ("stage-d-placement-batch-" + str(i+1) + "-v1.json")
        check(pin["path"] == path.as_posix() and sha(path) == pin["blob_sha"]
              and index["batches"][i]["git_blob_sha"] == pin["blob_sha"],
              "postfit batch pin drift")
        b = read(path)
        for claim in b["entries"]:
            for rel in claim["relations"]:
                typed.append((claim["id"] + "." + rel["relation_id"],rel))
    check(len(typed) == 68 and len(set(k for k,r in typed)) == 68,
          "stage D identity drift")
    counts = Counter()
    x = {grade:{layer:0 for layer in LAYERS} for grade in LEVELS}
    high = []
    for (id_, rel), joined in zip(typed, j["joins"]):
        profile = grade_by_id.get(id_)
        check(profile is not None and joined["id"] == id_
              and joined["evidence_grade"] == profile["evidence_level"]
              and joined["warrant_kind"] == profile["warrant_kind"]
              and joined["timing"] == profile["validation_timing"],
              "profile relation join drift " + id_)
        check(joined["layers"] == rel["referenced_layers"]
              and joined["operator_tag"] == rel["assertion_operator"]
              and joined["carrier_status"] == rel["carrier_status"]
              and joined["context"] == rel["context_type"]
              and joined["system_role_fit"] == "NOT_STARTED",
              "typed layer/role status drift " + id_)
        grade = joined["evidence_grade"]
        counts[grade] += 1
        for layer in joined["layers"]:
            check(layer in LAYERS, "unexpected layer")
            x[grade][layer] += 1
        if grade in ("E2", "E3"):
            high.append((id_,grade))
    check({k:counts.get(k,0) for k in LEVELS} ==
          {"E0":27,"E1":40,"E2":1,"E3":0},
          "frozen evidence counts drift")
    check(j["counts"]["evidence_grade_by_typed_reference_layer"] == x and
          j["counts"]["level_counts"] ==
          {k:counts.get(k,0) for k in LEVELS},
          "postfit cross-tabulation drift")
    check(high == [("RFX05C.r1","E2")] and x["E2"]["L_sys"] == 0,
          "interventional evidence misattributed to direct system role fit")
    check(all(g["carrier_exact_validated"] == 0 and
              g["source_direct_cognitive_system_role_fit_tested"] == 0
              for g in j["stage_d_fidelity_by_grade"].values()),
          "unsupported exact-carrier or role success")
    check(j["flagged_relations"]["retained_referent_precision_issue"]
          == "RFX11C.r5 / PVS-CNC-02.r2"
          and j["flagged_relations"]["explicit_source_argument_binding_watches"]
          == {"claims":5,"nodes":7,"confirmed_semantic_losses":0},
          "known carrier/binding watch drift")
    return {"status":"PASS","claims":47,"relations":68,
            "grade_counts":{k:counts.get(k,0) for k in LEVELS},
            "grade_by_layer":x,"higher_grade_meta_controls":high,
            "carrier_exact_validated":0,"object_level_role_fit_validated":0,
            "upstream_fit_unchanged":True,
            "terminal":"RFX47_POSTFIT_EVIDENCE_JOIN_CI_PASS"}

if __name__ == "__main__":
    a = audit()
    assert audit() == a, "nondeterministic evidence join"
    print(json.dumps(a,ensure_ascii=False,sort_keys=True,indent=2))
