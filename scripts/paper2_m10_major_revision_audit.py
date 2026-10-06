#!/usr/bin/env python3
"""Deterministic M10 guards: rival-basis sensitivity and real-source perturbations."""
from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path("research/paper2")
M10=ROOT/"p399/main/integration/M10"

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def canon(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def sha(x):
    return hashlib.sha256(canon(x).encode("utf-8")).hexdigest()

def main():
    rs=load(M10/"M10_RIVAL_BASIS_SPEC_v1.json")
    ps=load(M10/"M10_REAL_SOURCE_PERTURBATION_SPEC_v1.json")
    rr=load(M10/"M10_RIVAL_BASIS_SENSITIVITY_v1.json")
    pr=load(M10/"M10_REAL_SOURCE_PERTURBATION_RESULTS_v1.json")
    wx=load(M10/"M10_WORKED_EXAMPLES_v1.json")
    glob=load(ROOT/"global_archetype_reconstruction_v1.json")
    agg=load(ROOT/"grammar_v0_reverse_projection_aggregate_v1.json")
    diag=load(ROOT/"reference_global_incomparability_diagnostic_v1.json")
    m9b=load(ROOT/"p399/main/integration/M9B/M9B_MAIN40_PAPER_LEVEL_EVIDENCE_v1.json")

    gm=rs["lossless_index_map"]["grammar_v0"]
    bm=rs["lossless_index_map"]["working_basis"]
    assert len(gm)==9 and len(set(gm.values()))==9
    assert len(bm)==8 and len(set(bm.values()))==8
    assert {v:k for k,v in gm.items()} | {} == {v:k for k,v in gm.items()}
    invg={v:k for k,v in gm.items()}
    invb={v:k for k,v in bm.items()}
    for k,v in gm.items(): assert invg[v]==k
    for k,v in bm.items(): assert invb[v]==k

    claim_count=0
    for src in agg["lane_sources"]:
        lane=load(src["path"])
        for row in lane["claims"]:
            roles=row.get("grammar_roles_instantiated",[])
            assert [invg[gm[r]] for r in roles]==roles
            claim_count += 1
    assert claim_count==60

    transformed=[]
    for obj in glob["global_archetype_objects"]:
        co=json.loads(json.dumps(obj["canonical_structural_object"]))
        co["active_axes"]=sorted(bm[a] for a in co["active_axes"])
        for node in co["nodes"].values():
            if node.get("axis") is not None:
                node["axis"]=bm[node["axis"]]
        transformed.append(sha(co))
    assert len(transformed)==206
    assert len(set(transformed))==206
    assert glob["cross_lane_refinement_closure_object_count"]==99
    assert diag["frozen_global_relation_counts"]=={"INCOMPARABLE":1770}

    arch=next(x for x in glob["global_archetype_objects"] if x["global_archetype_id"]=="A-3b814de4da04")
    lanes=set(arch["derived_support_lanes"])
    assert {"ATT","BLF"} <= lanes
    att=load(ROOT/"chatgpt_reference_claimir_v1/ATT01.json")
    blf=load(ROOT/"chatgpt_reference_claimir_v1/BLF01.json")
    assert set(att["provenance"]["construct_labels"]).isdisjoint(blf["provenance"]["construct_labels"])

    rows=m9b["rows"]
    assert len(rows)==40
    assert sum(r["final_state"]=="A0_FIDELITY" for r in rows)==40
    assert sum(r["corpus_arm"]=="component" and r["final_state"]=="A0_FIDELITY" for r in rows)==24
    assert sum(r["corpus_arm"]=="integrated" and r["final_state"]=="A0_FIDELITY" for r in rows)==16
    assert m9b["independent_human_readjudication"]=="NOT_PERFORMED"

    i10=load(M10/"frozen_inputs/INT10_PASS_A.json")
    i10o=load(M10/"frozen_inputs/INT10_ARCHITECTURAL_OUTCOME.json")
    assert i10o["final_architectural_state"]=="A0_FIDELITY"
    assert "BG-selected action/CPG parameter interface" in i10o["source_defined_mediator"]
    assert i10["integration_questions"]["coupling_removal_failure"]=="cerebellar fine-tuning cannot consume BG-selected action results"
    c10=next(c for c in pr["controls"] if c["paper_id"]=="INT-10")
    assert c10["counterfactual_state"]=="A1_FIDELITY_CONTROL"
    assert c10["added_stateless_adapter_count"]==1 and c10["added_persistent_state_count"]==0

    i16=load(M10/"frozen_inputs/INT16_PASS_A.json")
    i16o=load(M10/"frozen_inputs/INT16_ARCHITECTURAL_OUTCOME.json")
    assert i16o["final_architectural_state"]=="A0_FIDELITY"
    assert "traces/tags bridge delay" in i16["decomposition"]["temporal_order"]
    assert "tags" in i16["decomposition"]["source_defined_shared_state"]
    c16=next(c for c in pr["controls"] if c["paper_id"]=="INT-16")
    assert c16["counterfactual_state"]=="A2_FIDELITY_CONTROL"
    assert c16["stateless_repair_sufficient"] is False
    assert c16["added_persistent_state_count"]==1

    assert rr["higher_level_conclusions"]["labels_alone_do_not_individuate"] is True
    assert rr["higher_level_conclusions"]["whole_claim_failure_remains_informative"] is True
    assert rr["higher_level_conclusions"]["reuse_requires_explicit_preservation_criterion"] is True
    assert rr["higher_level_conclusions"]["representation_choice_changes_first_class_distinctions"] is True
    assert rr["higher_level_conclusions"]["representation_relative_conclusion_required"] is True
    assert wx["boundary"]["new_scientific_adjudication"] is False

    # Scientific invariants must remain exact.
    assert rr["scientific_invariants"]["whole_claim_incomparable"]==1770
    assert rr["scientific_invariants"]["reusable_structural_subobjects"]==206
    assert rr["scientific_invariants"]["cross_stratum_families"]==99
    assert rr["scientific_invariants"]["reverse_projection"]=={"full":21,"partial":22,"residual":17}
    assert rr["scientific_invariants"]["residual_new_top_level_role"]=="0/17"
    assert rr["scientific_invariants"]["prospective"]=={"A0":40,"A1":0,"A2":0}
    print("M10_MAJOR_REVISION_GUARDS_PASS")

if __name__=="__main__":
    main()
