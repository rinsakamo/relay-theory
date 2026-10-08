#!/usr/bin/env python3
"""M33 exact source-vs-author semantic cohort and data-mapping qualification."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/"research/paper2/p399/main/integration/M33/M33_MATCHED_SEMANTIC_PRIMARY_CASE_v1.json").read_text(encoding="utf-8"))
main=(root/"paper/venues/jgps/main.tex").read_text(encoding="utf-8")
supp=(root/"paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
bib=(root/"paper/venues/jgps/references.bib").read_text(encoding="utf-8")
idx=(root/"paper/venues/jgps/supplementary-materials-index.md").read_text(encoding="utf-8")
assert d["exact_parent_m32_head"]=="23edd6a088b34a3b70cbffe9a80505ff7534c5b1"
assert d["status"]=="IMPLEMENTED_PENDING_EXACT_HEAD_CI"
assert len(d["source_registry"])==2
assert {x["doi"] for x in d["source_registry"]}=={"10.1093/brain/awl153","10.1093/brain/awp146"}
for x in d["source_registry"]:
    assert x["doi"] in bib
    assert x["cite_key"] in bib
    assert x["type"]=="original comparative case-series"
    assert x["reported_results"]
assert d["fixed_identity_frame"]["independently_validated_capacity_type_criterion"] is False
assert d["fixed_identity_frame"]["actually_measured_capacity_type_identity"] is False
ops=d["evidence_ops"]
assert [x["op"] for x in ops]==["phi_aggregate","phi_profile","corbett2009_object_use","patient_lesion_anatomy"]
assert ops[0]["data"]==ops[1]["data"]=="Omega06"
assert ops[0]["kind"]==ops[1]["kind"]=="representation after measurement"
assert ops[2]["data"]=="Omega09"
assert ops[2]["kind"]=="new sample or measurement"
assert ops[3]["kind"]=="different measurement"
for key,val in d["scientific_vs_philosophical_boundary"].items():
    assert isinstance(val,bool),key
for key in ("actual_direct_patient_group_comparison","same_test_battery_observations","coarse_vs_detailed_maps_counterfactual_analyst_representations","source_justifies_different_impairment_mechanisms_not_nec_capacity_kinds"):
    assert d["scientific_vs_philosophical_boundary"][key] is True
for key in ("exact_numerical_equality_observed","item_level_data_independently_analyzed","mapping_audit_implemented_on_patient_dataset","observed_activated_same_QC_capacity_defeater","independent_journal_referee_review","clinical_data_do_not_identify_pairwise_capacity_LR"):
    value=d["scientific_vs_philosophical_boundary"][key]
    if key=="clinical_data_do_not_identify_pairwise_capacity_LR":
        assert value is True
    else:
        assert value is False,key
assert d["corpus_rerun"] is False and d["recoded_claims"] is False
assert d["frozen_science"]["whole_pairs"]=="1770/1770 INCOMPARABLE"
assert d["frozen_science"]["bounded_objects"]==206
assert d["frozen_science"]["cross_stratum_families"]==99
assert d["frozen_science"]["cpcg_signatures"]==143
assert d["frozen_science"]["collision_families"]=="63/99"
assert d["frozen_science"]["reverse_projection"]=="21 FULL / 22 PARTIAL / 17 RESIDUAL"
assert d["frozen_science"]["residual_new_roles"]=="0/17"
assert d["frozen_science"]["human_inter_rater"]=="unmeasured"
for phrase in (
    "Jefferies and Lambon Ralph compared patients",
    r"\citep{JefferiesLambonRalph2006Semantic}",
    r"\citep{JefferiesEtAl2009Nonverbal}",
    r"\phi_{\mathrm{aggregate}}",
    r"\phi_{\mathrm{profile}}",
    "same existing observations",
    "not a sampled pair of systems",
):
    assert phrase in main, f"main missing {phrase}"
for phrase in (
    "Direct patient-group evidence",
    "seven",
    "eight",
    "the same battery",
    "post-measurement",
    r"\phi_{\rm aggregate}",
    r"\phi_{\rm profile}",
    "not an observed instance",
):
    assert phrase in supp, f"supplement missing {phrase}"
assert "M33_MATCHED_SEMANTIC_PRIMARY_CASE_v1.json" in idx
assert "paper2_m33_matched_semantic_case_audit.py" in idx
print("M33_MATCHED_PRIMARY_CASE_AND_DATA_MAP_SCOPE_GUARDS_PASS")
