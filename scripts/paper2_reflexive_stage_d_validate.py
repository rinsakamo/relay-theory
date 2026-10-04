#!/usr/bin/env python3
"""Validate Paper 2 #384 Stage D typed placement WITHOUT importing Evidence Profile."""
from __future__ import annotations
import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path("paper/validation/jgps-major-revision/reflexive-audit-v1")
CANDIDATE_SHA = "50fa50d24f2fbf9f3aef871cdeda08cdc97431a8"
CONTRACT_SHA = "38f06d98f70f29490efe7360750eb907ac1a3f15"
INDEX_SHA = "7a4a9bb1df15aa1b12de51e9ca048565601964a0"
PRECISION_SHA = "daa3081a74428c77bad158ef6ccffe90d0ddad54"
ALLOWED = {"L_claim", "L_ctx", "L_sys", "L_formal"}
REFS = {"G_cog", "W", "Gamma", "E_exp", "R",
        "Pi", "X", "C", "Q", "P_in", "P_out", "K", "T", "rho/O"}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha(path):
    return subprocess.run(["git", "hash-object", str(path)],
                          capture_output=True, check=True, text=True).stdout.strip()

def need(x, note):
    if not x:
        raise AssertionError(note)

def run():
    cfile = ROOT / "reflexive-claimir-candidates-v1.json"
    contract_file = ROOT / "reflexive-layer-placement-contract-v1.json"
    index_file = ROOT / "reflexive-stage-d-index-v1.json"
    precision_file = ROOT / "stage-d-binding-precision-audit-v1.json"
    need(sha(cfile) == CANDIDATE_SHA and sha(contract_file) == CONTRACT_SHA
         and sha(index_file) == INDEX_SHA and sha(precision_file) == PRECISION_SHA,
         "frozen packet, contract, index, or precision audit blob drift")
    c, contract, ix, precision = map(load, [cfile, contract_file, index_file, precision_file])
    need(c["candidate_count"] == 47 and ix["status"] == "STAGE_D_TYPING_FROZEN_BEFORE_EVIDENCE_JOIN"
         and contract["status"] == "FROZEN_BEFORE_STAGE_D_PLACEMENT"
         and ix["contract"]["blob_sha"] == CONTRACT_SHA, "preplacement freeze drift")
    for path, expected in [
      ("research/paper2/grammar_v0_layered_architecture_v1.json",
       contract["inputs"]["layered_architecture_sha"]),
      ("research/paper2/system_world_experiment_architecture_v1.json",
       contract["inputs"]["system_world_experiment_sha"])
    ]:
        need(sha(Path(path)) == expected, "architecture blob drift " + path)
    s1file = ROOT / "stage-d-semantics-spec-1-v1.json"
    s2file = ROOT / "stage-d-semantics-spec-2-v1.json"
    bfile = ROOT / "stage-d-typed-binding-spec-v1.json"
    need([sha(s1file), sha(s2file)] ==
         [x["blob_sha"] for x in ix["semantic_spec_blobs"]]
         and sha(bfile) == ix["typed_binding_spec_blob"], "frozen type/spec identity drift")
    s1, s2, bindings = map(load, [s1file, s2file, bfile])
    sem = {**s1["relation_operators"], **s2["relation_operators"]}
    need(list(sem) == c["candidate_ids"]
         and list(bindings["context_by_id"]) == c["candidate_ids"],
         "full 47-target semantic spec coverage/order drift")
    byid = {x["self_target_id"]: x for x in c["candidates"]}
    for id_, sets in bindings["node_layer_overrides"].items():
        need(id_ in byid, "unknown override target")
        ids = {n["id"] for n in byid[id_]["claimir"]["claim_core"]["nodes"]}
        all_ids = [v for a in sets.values() for v in a]
        need(set(all_ids) <= ids and len(all_ids) == len(set(all_ids))
             and all(k in ALLOWED for k in sets), "bad frozen node override " + id_)
    for id_, refs in bindings["node_architecture_refs"].items():
        need(id_ in byid, "unknown architectural-reference target")
        ids = {n["id"] for n in byid[id_]["claimir"]["claim_core"]["nodes"]}
        need(set(refs) <= ids and all(set(v) <= REFS for v in refs.values()),
             "bad architecture object refs " + id_)
    all_rows = []
    layer_count = Counter()
    operators = set()
    contexts = set()
    known_referent_pressure = []
    for i, link in enumerate(ix["batches"], 1):
        f = ROOT / f"stage-d-placement-batch-{i}-v1.json"
        need(f.as_posix() == link["path"] and sha(f) == link["git_blob_sha"],
             "batch order/sha drift")
        batch = load(f)
        need(batch["batch"] == i and batch["evidence_profile_used"] is False
             and batch["contract_sha"] == CONTRACT_SHA
             and batch["contract_format"] == "PREREGISTERED_MANDATORY_FIELDS"
             and batch["binding_spec_sha"] == sha(bfile)
             and batch["semantic_spec_shas"] == [sha(s1file), sha(s2file)],
             "batch input identity or evidence blindness drift")
        want = c["candidates"][(i - 1) * 8:i * 8]
        need([e["id"] for e in batch["entries"]] == [x["self_target_id"] for x in want],
             "candidate batch identity drift")
        nrel = 0
        for placed, original in zip(batch["entries"], want):
            id_ = placed["id"]
            originals = original["claimir"]["claim_core"]["relations"]
            node_ids = {n["id"] for n in original["claimir"]["claim_core"]["nodes"]}
            need(placed["claim_id"] == original["claimir"]["claim_id"]
                 and placed["relations"] and len(placed["relations"]) == len(originals)
                 and len(sem[id_]) == len(originals), "relation coverage " + id_)
            for j, (r, source) in enumerate(zip(placed["relations"], originals)):
                need(r["relation_id"] == source["id"]
                     and r["original_kind"] == source["kind"]
                     and r["original_arguments"] == source["arguments"]
                     and r["assertion_operator"] == sem[id_][j]
                     and r["context_type"] == bindings["context_by_id"][id_]
                     and r["assertion_layer"] == "L_claim"
                     and r["reason"], "relation semantic/source drift " + id_)
                expected = []
                for node in source["arguments"]:
                    need(node in node_ids, "source argument missing " + id_)
                    sets = bindings["node_layer_overrides"].get(id_, {})
                    matches = [k for k, ns in sets.items() if node in ns]
                    need(len(matches) <= 1, "ambiguous layer rule " + id_)
                    layer = matches[0] if matches else "L_claim"
                    expected.append({"node": node, "layer": layer,
                                     "architecture_refs":
                                     bindings["node_architecture_refs"].get(id_, {}).get(node, [])})
                need(r["argument_bindings"] == expected, "node binding drift " + id_)
                exp_layers = sorted({"L_claim", *(n["layer"] for n in expected)})
                exp_objs = sorted({a for n in expected for a in n["architecture_refs"]})
                need(r["referenced_layers"] == exp_layers
                     and r["referenced_objects"] == exp_objs
                     and set(exp_layers) <= ALLOWED
                     and r["placement_status"] == "TYPED_LAYER_PLACEMENT_CARRIER_UNTESTED"
                     and r["system_role_projection_status"] == "NOT_STARTED"
                     and r["direct_system_relation"] is False,
                     "layer/role verdict scope drift " + id_)
                expected_carrier = ("FROZEN_REFERENT_PRECISION_ISSUE_UNREPAIRED"
                                    if id_ == "RFX11C" else "EXACT_CARRIER_NOT_TESTED")
                need(r["carrier_status"] == expected_carrier,
                     "carrier fidelity improperly inferred " + id_)
                if id_ == "RFX11C":
                    known_referent_pressure.append(id_ + "." + source["id"])
                all_rows.append((id_, source["id"]))
                layer_count.update(exp_layers)
                operators.add(r["assertion_operator"])
                contexts.add(r["context_type"])
                nrel += 1
        need(nrel == batch["relation_count"] == link["relations"]
             and len(batch["entries"]) == batch["claim_count"] == link["claims"],
             "batch count drift")
    need(len(all_rows) == len(set(all_rows)) == 68
         and [x[0] for x in all_rows] == [
             x["self_target_id"] for x in c["candidates"]
             for _ in x["claimir"]["claim_core"]["relations"]],
         "47/68 total coverage drift")
    layer_totals = {"L_claim": 68, "L_ctx": 33, "L_formal": 22, "L_sys": 16}
    need(dict(layer_count) == layer_totals and
         ix["summary"]["referenced_layer_occurrences"] == layer_totals
         and len(operators) == ix["summary"]["distinct_semantic_description_tags"] == 63
         and len(contexts) == ix["summary"]["distinct_context_types"] == 18,
         "typed aggregate drift")
    need(known_referent_pressure == ["RFX11C.r5"]
         and ix["summary"]["exact_AssertionCarrier_v2_encodings_tested"] == 0
         and ix["summary"]["source_direct_cognitive_system_relations_evaluated"] == 0
         and ix["summary"]["architecture_completeness_conclusion"] == "NOT_ASSESSED",
         "trivial meta-layer fit must not become exact carrier/role success")
    actual = {}
    for item in c["candidates"]:
        used = {v for rel in item["claimir"]["claim_core"]["relations"] for v in rel["arguments"]}
        absent = [n["id"] for n in item["claimir"]["claim_core"]["nodes"] if n["id"] not in used]
        if absent:
            actual[item["self_target_id"]] = absent
    declared = {v["self_target_id"]: [n["node_id"] for n in v["unbound_nodes"]]
                for v in precision["watches"]}
    need(actual == declared and sum(map(len, actual.values())) == 7
         and len(actual) == 5 and precision["summary"]["confirmed_semantic_gaps"] == 0,
         "binding precision audit drift")
    need(ix["binding_precision_audit"]["blob_sha"] == PRECISION_SHA
         and ix["summary"]["self_target_claimir_binding_precision_watches"]["unbound_nodes"] == 7,
         "unbound precision witness provenance drift")
    state = load(ROOT / "reflexive-stage-progress-v2.json")
    need(state["stages"]["D"]["status"] == "FROZEN_PRE_EVIDENCE_JOIN"
         and state["stages"]["D"]["index_git_blob_sha"] == INDEX_SHA
         and state["stages"]["D"]["binding_precision_audit_git_blob_sha"] == PRECISION_SHA
         and state["stages"]["E"]["status"] == state["stages"]["F"]["status"] == "NOT_STARTED"
         and state["flags"]["stage_d_used_reflexive_evidence_grades"] is False,
         "stage sequencing drift")
    report = (ROOT / "reflexive-stage-d-report-v1.md").read_text(encoding="utf-8")
    need("5/47" in report and "68" in report and "NOT_STARTED" in report,
         "stage D report missing fixed limitations")
    return {"status": "PASS", "authority_issue": 384, "claims": 47, "relations": 68,
            "typed_reference_layer_occurrences": layer_totals,
            "descriptive_semantic_tags": 63, "unbound_claims": 5,
            "unbound_nodes": 7, "confirmed_semantic_gaps": 0,
            "exact_v2_encoding_tested": 0, "direct_system_role_tested": 0,
            "evidence_profile_read_for_fit": False, "stage_e_started": False,
            "stage_f_started": False,
            "terminal": "RFX47_STAGE_D_EVIDENCE_BLIND_PREJOIN_VALIDATION_PASS"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    a = run()
    need(run() == a, "nondeterministic validation")
    text = json.dumps(a, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    print("PAPER2_RFX47_STAGE_D_PREJOIN_GATE_PASS")

if __name__ == "__main__":
    main()
