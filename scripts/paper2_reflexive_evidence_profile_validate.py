#!/usr/bin/env python3
"""Deterministic, evidence-only validation for Paper 2 #384 Stage C.

This is an audit of frozen annotations against author-reviewed IDs and
repository evidence. It is NOT independent human evidence coding, and it
does not inspect reflexive layered fit or calculate a reflexive verdict.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path("paper/validation/jgps-major-revision/reflexive-audit-v1")
P2 = Path("paper/validation/jgps-major-revision")
PAPER2 = Path("research/paper2")
CANDIDATES = ROOT / "reflexive-claimir-candidates-v1.json"
LEDGER = ROOT / "human-review-progress-v1.json"
RUBRIC = ROOT / "reflexive-evidence-rubric-v1.json"
PROFILE = ROOT / "reflexive-evidence-profile-v1.json"
STAGE = ROOT / "reflexive-stage-progress-v1.json"
MARKDOWN = ROOT / "reflexive-evidence-profile-v1.md"
RUBRIC_FREEZE_COMMIT = "11a011571b14b78d89eb094d67e2cf1233f1a39c"
CANDIDATE_FROZEN_SHA = "50fa50d24f2fbf9f3aef871cdeda08cdc97431a8"
AUTHOR_LEDGER_FROZEN_SHA = "8e3e9b56959838907ff2a2f825506711a615da8e"
PROFILE_FROZEN_SHA = "500621e62357e157c2c52935ff53d3c292b1547b"
RUBRIC_FROZEN_SHA = "fbd88d9d69f3f94c73fd8e5ccc56008839db641a"
PVS_RUBRIC_SHA = "712b0487ff5ae3d0adaa03e3180eed1eb9e9a2b5"
FROZEN_SOURCES: dict[str, str] = json.loads(r""""{\"paper/venues/jgps/main.tex\":\"89b094476137bae12e089e5a794a5e57300f4da1\",\"research/paper2/chatgpt_reference_claimir_v1/manifest.json\":\"597f487eef3e49aab440b24894cc5d25869b0d44\",\"research/paper2/claim_ir_reliability_boundary_v1.json\":\"85bbd562329fed34fd370f3c1fcbe672c2bb44fd\",\"research/paper2/paper2_result_v1.json\":\"a20d1ae31e1ccc905b891bfb7312285cdcce55b4\",\"research/paper2/reference_global_phi_freeze_v1.json\":\"2ff188b2f4d8b6038d95bc7b3467168b3776b80c\",\"research/paper2/reference_global_incomparability_diagnostic_v1.json\":\"00d027c0cec4bfea2b2d74db22f2bb68046d3b70\",\"research/paper2/global_archetype_reconstruction_v1.json\":\"4eda9d8ddbcd3bac02cd6657c427241c45729c98\",\"research/paper2/bounded_xlike_reconstruction_v1.json\":\"43066b6825b67e2a2e1726b08b7092016d0051de\",\"paper/validation/jgps-major-revision/basis-to-grammar-provenance-v1.json\":\"2618e1e2378063959daa638a7e1e2ce46bd0ad40\",\"research/paper2/grammar_v0_minimality_comparator_v1.json\":\"8d0588f2a7a5d53d1c7d32b3b48ea3d03db90fee\",\"research/paper2/grammar_v0_layered_architecture_v1.json\":\"150fbb166541ba52abbe07124924fab63a1ad575\",\"research/paper2/system_world_experiment_architecture_v1.json\":\"2047db910b097ecb3bc1e2ab568f6fe0d64168a1\",\"paper/validation/jgps-major-revision/pvs16-evidence-profile-v1.json\":\"f98b2faed1ccc04a2564d090e04513ca63a2efe4\",\"paper/validation/jgps-major-revision/pvs16-evidence-x-grammar-diagnostic-v1.json\":\"c087a85665891231069f33314681ca97e5f5a81b\",\"paper/validation/jgps-major-revision/pvs16-layered-architecture-projection-v1.json\":\"27ae511dba789a3e6049fdfe01b181573c69d913\",\"paper/validation/jgps-major-revision/ahv8-assertion-carrier-heldout-validation-v1.json\":\"873464a4a03f90e24a0e900882b6d5673047873c\",\"paper/validation/jgps-major-revision/ahv8-assertion-carrier-v2-retrospective-calibration-v1.json\":\"611b7521d6c16dbd3c8f85ed9adb7aa4c1d90b8d\"}"""")
EXPECTED_RELATION_GRADES: dict[str, dict[str, str]] = json.loads(r""""{\"RFX01A\":{\"r1\":\"E0\",\"r2\":\"E0\"},\"RFX01B1\":{\"r1\":\"E0\"},\"RFX01B2A\":{\"r1\":\"E0\"},\"RFX01B2B\":{\"r2\":\"E0\"},\"RFX01B2C\":{\"r3\":\"E0\"},\"RFX02A\":{\"r1\":\"E0\"},\"RFX02B\":{\"r1\":\"E0\"},\"RFX03\":{\"r1\":\"E1\",\"r2\":\"E1\",\"r3\":\"E1\"},\"RFX04\":{\"r1\":\"E1\",\"r2\":\"E1\"},\"RFX05A\":{\"r1\":\"E1\",\"r2\":\"E1\"},\"RFX05B\":{\"r2\":\"E1\",\"r3\":\"E1\",\"r4\":\"E1\"},\"RFX05C\":{\"r1\":\"E2\"},\"RFX06A\":{\"r1\":\"E1\",\"r2\":\"E1\",\"r3\":\"E1\",\"r4\":\"E1\"},\"RFX06B\":{\"r5\":\"E1\"},\"RFX07A\":{\"r1\":\"E1\",\"r2\":\"E1\",\"r3\":\"E1\"},\"RFX07B\":{\"r4\":\"E1\"},\"RFX08A\":{\"r1\":\"E0\",\"r3\":\"E1\"},\"RFX08B\":{\"r2\":\"E0\",\"r4\":\"E1\"},\"RFX08C\":{\"r5\":\"E0\"},\"RFX09A\":{\"r1\":\"E0\"},\"RFX09B\":{\"r2\":\"E1\",\"r3\":\"E0\"},\"RFX10A\":{\"r1\":\"E0\"},\"RFX10B\":{\"r2\":\"E0\"},\"RFX10C\":{\"r3\":\"E0\"},\"RFX10D\":{\"r4\":\"E0\"},\"RFX11A\":{\"r1\":\"E1\",\"r4\":\"E1\"},\"RFX11B\":{\"r3\":\"E1\",\"r4\":\"E1\"},\"RFX11C\":{\"r5\":\"E1\"},\"RFX12A\":{\"r1\":\"E1\",\"r2\":\"E1\",\"r3\":\"E1\"},\"RFX12B\":{\"r2\":\"E1\",\"r4\":\"E1\"},\"RFX12C\":{\"r5\":\"E1\",\"r6\":\"E0\"},\"RFX13A\":{\"r1\":\"E1\"},\"RFX13B\":{\"r4\":\"E1\"},\"RFX13C\":{\"r2\":\"E1\"},\"RFX13D\":{\"r3\":\"E1\"},\"RFX14A\":{\"r0\":\"E0\"},\"RFX14B\":{\"r1\":\"E0\"},\"RFX14C\":{\"r2\":\"E0\"},\"RFX14D\":{\"r3\":\"E0\"},\"RFX14E\":{\"r4\":\"E0\"},\"RFX14F\":{\"r5\":\"E0\"},\"RFX14G\":{\"r6\":\"E0\"},\"RFX15A\":{\"r1\":\"E1\"},\"RFX15B\":{\"r2\":\"E1\"},\"RFX15C\":{\"r3\":\"E1\"},\"RFX15D\":{\"r5\":\"E0\"},\"RFX15E\":{\"r4\":\"E0\"}}"""")
EXPECTED_LEVEL_COUNTS = {"E0": 27, "E1": 40, "E2": 1, "E3": 0}
LEVELS = {"E0": 0, "E1": 1, "E2": 2, "E3": 3}

class EvidenceValidationError(ValueError):
    pass

def j(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def blob(path: Path) -> str:
    return subprocess.run(["git", "hash-object", str(path)],
                          capture_output=True, text=True, check=True).stdout.strip()

def require(ok: bool, message: str) -> None:
    if not ok:
        raise EvidenceValidationError(message)

def frozen_source_audits() -> dict[str, Any]:
    for relpath, sha in FROZEN_SOURCES.items():
        path = Path(relpath)
        require(path.is_file(), f"frozen source file absent: {relpath}")
        require(blob(path) == sha, f"frozen authority blob drift: {relpath}")
    phi = j(PAPER2 / "reference_global_phi_freeze_v1.json")
    diag = j(PAPER2 / "reference_global_incomparability_diagnostic_v1.json")
    global_a = j(PAPER2 / "global_archetype_reconstruction_v1.json")
    bounded = j(PAPER2 / "bounded_xlike_reconstruction_v1.json")
    result = j(PAPER2 / "paper2_result_v1.json")
    provenance = j(P2 / "basis-to-grammar-provenance-v1.json")
    minimality = j(PAPER2 / "grammar_v0_minimality_comparator_v1.json")
    pvs_profile = j(P2 / "pvs16-evidence-profile-v1.json")
    pvs_map = j(P2 / "pvs16-evidence-x-grammar-diagnostic-v1.json")
    pvs_layer = j(P2 / "pvs16-layered-architecture-projection-v1.json")
    ahv = j(P2 / "ahv8-assertion-carrier-heldout-validation-v1.json")
    v2 = j(P2 / "ahv8-assertion-carrier-v2-retrospective-calibration-v1.json")
    reliability = j(PAPER2 / "claim_ir_reliability_boundary_v1.json")
    source_manifest = j(PAPER2 / "chatgpt_reference_claimir_v1" / "manifest.json")
    pvs_rubric_path = P2 / "pvs16-evidence-profile-rubric-v1.json"
    require(blob(pvs_rubric_path) == PVS_RUBRIC_SHA, "original PVS rubric blob drift")
    pvs_rubric = j(pvs_rubric_path)
    require("intervention" in pvs_rubric["levels"]["E2"]["rule"].lower(), "PVS E2 criterion drift")
    require("multiple" in pvs_rubric["levels"]["E3"]["rule"].lower(), "PVS E3 criterion drift")

    require(phi["claim_count"] == 60 and phi["pair_count"] == 1770 and
            phi["relation_counts"]["INCOMPARABLE"] == 1770 and
            not phi["equivalence_components"], "RFX03 Phi frozen values drift")
    require(diag["directed_pair_count"] == 3540 and
            diag["directed_stage_counts"]["scalar"] == 3518 and
            diag["directed_stage_counts"]["topology"] == 0 and
            diag["directed_stage_counts"]["embeds"] == 0,
            "RFX04 diagnosis frozen values drift")
    require(global_a["unique_global_archetype_count"] == 206 and
            global_a["cross_lane_refinement_closure_object_count"] == 99 and
            bounded["bounded_xlike_count"] == 206 and
            bounded["cross_lane_xlike_count"] == 99 and
            bounded["supported_claim_count"] == 59 and
            bounded["corpus_claim_count"] == 60,
            "RFX05 bounded reconstruction frozen values drift")
    controls = bounded["destructive_controls"]
    require(len(controls) == 8 and
            all(controls[k]["status"] == "PASS" for k in controls),
            "RFX05C eight declared controls drift")
    require(provenance["new_top_level_role_count"] == 0 and
            len(provenance["roles"]) == 9, "RFX06 provenance drift")
    require([result["reverse_projection"][k] for k in ("FULL", "PARTIAL", "RESIDUAL")] ==
            [21, 22, 17] and
            result["residual_adjudication"]["primary_class_counts"]["SOURCE_CONTEXT_PARAMETER"] == 13 and
            result["residual_adjudication"]["primary_class_counts"]["RELATION_LANGUAGE_GAP"] == 4 and
            result["residual_adjudication"]["primary_class_counts"]["ROLE_GAP"] == 0,
            "RFX07 frozen review verdict drift")
    require(result["strict_preservation_comparators"]["G_dyn"]["claims_requiring_role_beyond_XKT"] == 59 and
            result["strict_preservation_comparators"]["G_dyn"]["strict_full_direct_preservation_count"] == 0 and
            result["strict_preservation_comparators"]["G_pomdp_like"]["union_affected_by_missing_Pi_C_or_direction_split"] == 44 and
            "not a theorem" in minimality["test_semantics"]["limitation"].lower(),
            "RFX08 strict comparator boundary drift")
    pm = pvs_map["relation_level_matrix"]
    require(pvs_profile["summary"]["relation_level_counts"]["E2"] == 8 and
            pvs_profile["summary"]["relation_level_counts"]["E3"] == 4 and
            [pm["E2"][k] for k in ("PRESERVED", "PARTIAL", "UNMAPPED")] == [4, 2, 2] and
            [pm["E3"][k] for k in ("PRESERVED", "PARTIAL", "UNMAPPED")] == [3, 0, 1] and
            "ROLE_GAP" not in pvs_map["unmapped_residual_by_evidence"]["E2"]["primary_class_counts"] and
            "ROLE_GAP" not in pvs_map["unmapped_residual_by_evidence"]["E3"]["primary_class_counts"],
            "RFX11A PVS source-stratified outcome drift")
    ps = pvs_layer["summary"]
    require(ps["total_relations"] == 52 and
            ps["direct_l_sys_relations"] + ps["architecture_placeable_nonstrict_relations"] == 52 and
            ps["architecture_gaps"] == 0 and ps["role_gap_count"] == 0 and
            ps["claim_carrier_precision_pressure_count"] == 1 and
            ps["claim_carrier_pressure_relations"] == ["PVS-CNC-02.r2"],
            "RFX11B/C frozen layered result drift")
    ahs = ahv["summary"]
    require(ahs["relations"] == 28 and ahs["full_relations"] == 11 and
            ahs["gap_relations"] == 17 and ahs["full_claims"] == 1,
            "RFX12 AHV-8 v1 held-out outcome drift")
    require(reliability["source_grounded_reviewed_reference_corpus"]["reviewed_claims"] == 60 and
            reliability["source_grounded_reviewed_reference_corpus"]["total_claims"] == 60 and
            reliability["independent_extractor_structural_agreement"] == "NOT_ESTABLISHED" and
            reliability["local_automated_production_qualification"] == "NOT_ESTABLISHED" and
            reliability["historical_local_calibration"]["both_valid_agreement_denominator"] == 0 and
            len(source_manifest["entries"]) == 60,
            "RFX13 source review/reliability boundary drift")
    v2c = v2["calibration_boundary"]
    require(v2c["ahv8_relations"] == 28 and
            v2c["v1_full_carryover"] == 11 and
            v2c["v1_gaps_repaired"] == 17 and
            v2c["v2_retrospective_full"] == 28 and
            v2c["independent_v2_validation_claimed"] is False and
            v2["v1_heldout_source_blob_sha"] == FROZEN_SOURCES[
                str(P2 / "ahv8-assertion-carrier-heldout-validation-v1.json")
            ], "RFX15 in-sample retrospective calibration boundary drift")
    return {"frozen_source_blobs_verified": len(FROZEN_SOURCES),
            "pvs_reference_rubric_verified": True,
            "key_frozen_diagnostics_rechecked": True}

def validate() -> dict[str, Any]:
    c, h, rubric, p, stage = [j(path) for path in (CANDIDATES, LEDGER, RUBRIC, PROFILE, STAGE)]
    require(blob(CANDIDATES) == CANDIDATE_FROZEN_SHA and
            blob(LEDGER) == AUTHOR_LEDGER_FROZEN_SHA and
            blob(RUBRIC) == RUBRIC_FROZEN_SHA and
            blob(PROFILE) == PROFILE_FROZEN_SHA,
            "source packet, author ledger, prior rubric, or evidence profile SHA drift")
    require(rubric["status"] == "FROZEN_BEFORE_RELATION_ANNOTATION" and
            rubric["input_gate"]["author_review_accepted"] == 47 and
            rubric["input_gate"]["downstream_fit_read_for_new_annotations"] is False and
            rubric["lineage"]["reference_rubric_git_blob_sha"] == PVS_RUBRIC_SHA,
            "rubric preregistration boundary drift")
    require(p["pre_registered_rubric_commit"] == RUBRIC_FREEZE_COMMIT and
            p["rubric_git_blob_sha"] == RUBRIC_FROZEN_SHA and
            p["candidate_packet_git_blob_sha"] == CANDIDATE_FROZEN_SHA and
            p["author_review_completion_git_blob_sha"] == AUTHOR_LEDGER_FROZEN_SHA,
            "rubric/profile sequencing drift")
    require(h["status"] == "AUTHOR_REVIEW_COMPLETE" and
            h["accepted"] == h["reviewed"] == h["total"] == 47 and
            h["remaining"] == [] and h["review_gate_satisfied"] is True,
            "47/47 human-review gate not satisfied")
    require(c["candidate_count"] == 47 and len(c["candidates"]) == 47 and
            c["candidate_ids"] == list(EXPECTED_RELATION_GRADES),
            "47-target identity/order drift")
    require(len(h["decisions"]) == 47 and
            len({d["self_target_id"] for d in h["decisions"]}) == 47,
            "author decision uniqueness drift")
    cand_by_id = {x["self_target_id"]: x for x in c["candidates"]}
    for d in h["decisions"]:
        id_ = d["self_target_id"]
        require(id_ in cand_by_id and d["decision"] == "ACCEPT",
                f"human decision mismatch: {id_}")
        rec = j(ROOT / "human-reviewed" / f"{id_}.json")
        require(rec["self_target_id"] == id_ and
                rec["accepted_normalized_claim"] == cand_by_id[id_]["normalized_claim"] and
                rec["downstream_fit_inspected"] is False,
                f"accepted decision record mismatch: {id_}")

    require(p["status"] == "FROZEN_PRE_REFLEXIVE_MAPPING_EVIDENCE_PROFILE" and
            p["authorship"] == "RULE_GOVERNED_MODEL_ANNOTATION_NOT_INDEPENDENT_HUMAN_EVIDENCE_CODING" and
            len(p["evidence_catalog"]) == 17 and
            {v["path"]: v["git_blob_sha"] for v in p["evidence_catalog"].values()} == FROZEN_SOURCES,
            "profile scope or pinned evidence authority drift")
    require(p["flags"]["evidence_frozen_before_reflexive_mapping"] is True and
            p["flags"]["reflexive_grammar_fit_inspected"] is False and
            p["flags"]["reflexive_layered_mapping_inspected"] is False and
            p["flags"]["reflexive_verdict_produced"] is False and
            p["flags"]["original_PVS_source_grade_not_inherited_into_RFX11A"] is True and
            p["flags"]["retrospective_v2_not_independent_v2_validation"] is True,
            "profile cannot claim results from later stages")

    require(len(p["annotations"]) == 47 and
            [x["self_target_id"] for x in p["annotations"]] == c["candidate_ids"],
            "profile candidate coverage/order drift")
    level_counts: Counter[str] = Counter()
    warrants: Counter[str] = Counter()
    timings: Counter[str] = Counter()
    nrelations = 0
    for a in p["annotations"]:
        id_ = a["self_target_id"]
        original = cand_by_id[id_]
        require(a["claim_id"] == original["claimir"]["claim_id"] and
                a["accepted_normalized_claim"] == original["normalized_claim"] and
                a["author_review_status"] == "ACCEPT" and
                a["reflexive_mapping_inspected"] is False,
                f"{id_}: claim identity or annotation review drift")
        frozen_relations = original["claimir"]["claim_core"]["relations"]
        grade_mapping = EXPECTED_RELATION_GRADES[id_]
        require(len(a["relations"]) == len(frozen_relations) == len(grade_mapping) ==
                a["relation_count"], f"{id_}: relation count drift")
        require([r["relation_id"] for r in a["relations"]] ==
                [r["id"] for r in frozen_relations], f"{id_}: relation ID/order drift")
        grades = []
        for r, frozen_rel in zip(a["relations"], frozen_relations):
            grade = r["evidence_level"]
            require(grade in LEVELS and grade == grade_mapping[r["relation_id"]] and
                    r["graded_relation_description"] == frozen_rel["description"] and
                    r["source_span_ids"] == frozen_rel["source_span_ids"] and
                    r["rationale"] and r["locator"] and r["evidence_refs"],
                    f"{id_}.{r['relation_id']}: evidence annotation drift")
            for source in r["evidence_refs"]:
                key = source["authority_key"]
                require(key in p["evidence_catalog"] and
                        source["path"] == p["evidence_catalog"][key]["path"] and
                        source["git_blob_sha"] == p["evidence_catalog"][key]["git_blob_sha"],
                        f"{id_}.{r['relation_id']}: authority reference drift")
            if grade == "E0":
                require(r["support_directness"] == "DECLARED_OR_INFERRED" and
                        r["independent_replication_status"] == "NOT_APPLICABLE",
                        f"{id_}: E0 directness/replication drift")
            if grade == "E1":
                require(r["support_directness"] in ("FROZEN_ARTIFACT_DIRECT", "SOURCE_LOCAL_AUDIT")
                        and r["independent_replication_status"] == "NOT_CLAIMED" and
                        any(v["authority_key"] != "manuscript" for v in r["evidence_refs"]),
                        f"{id_}: E1 must have direct non-manuscript frozen support")
            if grade == "E2":
                require(id_ == "RFX05C" and r["relation_id"] == "r1" and
                        r["warrant_kind"] == "FROZEN_DESTRUCTIVE_CONTROL" and
                        r["validation_timing"] == "FROZEN_DECLARED_CONTROL" and
                        r["support_directness"] == "FROZEN_CONTROL_DIRECT",
                        f"{id_}: E2 misapplied beyond declared direct controls")
            if id_ == "RFX11A":
                require(grade == "E1", "RFX11A incorrectly inherited PVS source E2/E3")
            if id_.startswith("RFX15"):
                require(grade in ("E0", "E1") and
                        r["validation_timing"] in ("RETROSPECTIVE_POST_HOC_V2", "METHODOLOGICAL"),
                        "v2 calibration misrepresented as independent intervention")
            level_counts[grade] += 1
            warrants[r["warrant_kind"]] += 1
            timings[r["validation_timing"]] += 1
            grades.append(grade)
            nrelations += 1
        bounds = [min(grades, key=LEVELS.get), max(grades, key=LEVELS.get)]
        require(a["relation_level_range"] == bounds and
                a["relation_levels_not_aggregated"] is True,
                f"{id_}: relation range misaggregation")

    require(nrelations == 68 and dict(level_counts) == {k:v for k,v in EXPECTED_LEVEL_COUNTS.items() if v} and
            p["summary"]["relation_level_counts"] == EXPECTED_LEVEL_COUNTS and
            p["summary"]["claims"] == 47 and p["summary"]["relations"] == 68 and
            p["summary"]["warrant_counts"] == dict(warrants) and
            p["summary"]["validation_timing_counts"] == dict(timings),
            "evidence summary/level counts drift")
    require(stage["review_gate"]["status"] == "COMPLETE" and
            stage["evidence"]["profile_git_blob_sha"] == PROFILE_FROZEN_SHA and
            stage["evidence"]["relation_level_counts"] == EXPECTED_LEVEL_COUNTS and
            stage["stage_d"]["status"] == "NOT_STARTED" and
            stage["stage_e"]["status"] == "NOT_STARTED" and
            stage["stage_f"]["status"] == "NOT_STARTED" and
            all(v is False for v in stage["flags"].values()),
            "downstream stage accidentally started or declared")
    md = MARKDOWN.read_text(encoding="utf-8")
    require("68" in md and "47" in md and "E3" in md,
            "evidence summary markdown drift")
    source_check = frozen_source_audits()
    return {
      "schema": "relay-theory.paper2.reflexive_evidence_validation.v1",
      "status": "PASS",
      "authority_issue": 384,
      "author_accepted_claims": 47,
      "profiled_relations": nrelations,
      "relation_level_counts": EXPECTED_LEVEL_COUNTS,
      "review_record_checks": 47,
      **source_check,
      "no_reflexive_fit_or_verdict_inspected": True,
      "independent_v2_validation_claimed": False,
      "terminal": "RFX47_EVIDENCE_PROFILE_PRE_MAPPING_VALIDATION_PASS",
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate()
    duplicate = validate()
    require(result == duplicate, "nondeterministic evidence validation")
    payload = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    print("PAPER2_RFX47_EVIDENCE_PROFILE_PRE_MAPPING_GATE_PASS")

if __name__ == "__main__":
    main()
