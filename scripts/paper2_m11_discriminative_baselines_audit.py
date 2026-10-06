#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M11 = ROOT / "research/paper2/p399/main/integration/M11"
M7 = ROOT / "research/paper2/p399/main/integration/M7/M7_40_PAPER_ARCHITECTURAL_MATRIX_v1.json"
M10_RIVAL = ROOT / "research/paper2/p399/main/integration/M10/M10_RIVAL_BASIS_SENSITIVITY_v1.json"
MAIN = ROOT / "paper/venues/jgps/main.tex"
SUPP = ROOT / "paper/venues/jgps/supplement.tex"

def load(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)

prefreeze = load(M11 / "M11_PREFREEZE_RECEIPT_v1.json")
comp_spec = load(M11 / "M11_PROSPECTIVE_COMPARATOR_SPEC_v1.json")
comp = load(M11 / "M11_PROSPECTIVE_COMPARATOR_RESULTS_v1.json")
enc_spec = load(M11 / "M11_ENCODING_PERMISSIVE_COMPOSITION_BASELINE_SPEC_v1.json")
enc = load(M11 / "M11_ENCODING_PERMISSIVE_COMPOSITION_BASELINE_RESULTS_v1.json")
loss_spec = load(M11 / "M11_LOSSY_RIVAL_SPEC_v1.json")
loss = load(M11 / "M11_LOSSY_RIVAL_RESULTS_v1.json")
same = load(M11 / "M11_SAME_LABEL_WORKED_EXAMPLE_v1.json")
m7 = load(M7)
m10 = load(M10_RIVAL)
main = MAIN.read_text(encoding="utf-8")
supp = SUPP.read_text(encoding="utf-8")

# Immutable pre-M11 science.
assert prefreeze["immutable_scientific_results"]["whole_claim_incomparable"] == "1770/1770"
assert prefreeze["immutable_scientific_results"]["bounded_objects"] == 206
assert prefreeze["immutable_scientific_results"]["cross_stratum_families"] == 99
assert prefreeze["immutable_scientific_results"]["reverse_projection"] == "21 full / 22 partial / 17 residual"
assert prefreeze["immutable_scientific_results"]["residual_new_top_level_role"] == "0/17"
assert prefreeze["immutable_scientific_results"]["main40"] == {"A0": 40, "A1": 0, "A2": 0}
assert prefreeze["immutable_scientific_results"]["component"] == "24/24 A0"
assert prefreeze["immutable_scientific_results"]["integrated"] == "16/16 A0"
assert prefreeze["immutable_scientific_results"]["independent_human_readjudication"] == "NOT_PERFORMED"
assert prefreeze["immutable_scientific_results"]["global_genealogical_independence"] == "NOT_CLAIMED"

assert m10["scientific_invariants"]["whole_claim_incomparable"] == 1770
assert m10["scientific_invariants"]["reusable_structural_subobjects"] == 206
assert m10["scientific_invariants"]["cross_stratum_families"] == 99
assert m10["scientific_invariants"]["reverse_projection"] == {"full": 21, "partial": 22, "residual": 17}
assert m10["scientific_invariants"]["residual_new_top_level_role"] == "0/17"
assert m10["scientific_invariants"]["prospective"] == {"A0": 40, "A1": 0, "A2": 0}

rows = m7["rows"]
assert len(rows) == 40
assert sum(r["corpus_arm"] == "component" for r in rows) == 24
assert sum(r["corpus_arm"] == "integrated" for r in rows) == 16
assert all(r["m7_adjudicated_final_A_state"] == "A0_FIDELITY" for r in rows)
expected_roles = {"Pi", "X", "C", "Q", "P", "K", "T", "rho/O"}
assert all(set(r["Grammar_roles_used"]) == expected_roles for r in rows)

# Prefreeze chronology / transparency.
assert prefreeze["status"] == "PREFREEZE"
assert prefreeze["exact_parent_head"] == "095c6f41bc7ca6a08bf423137bbf3b8f7bc068e5"
assert comp_spec["status"] == "FROZEN_BEFORE_M11_COMPARATOR_RESULT_MATERIALIZATION"
assert comp_spec["prefreeze_disclosure"]["main40_all_eight_roles_usage_known_before_freeze"] is True
assert comp_spec["prefreeze_disclosure"]["result_artifact_materialized_before_freeze"] is False
assert loss_spec["status"] == "FROZEN_BEFORE_LOSSY_RIVAL_RESULT_MATERIALIZATION"
assert loss_spec["prefreeze_disclosure"]["lossy_projection_result_computed_before_freeze"] is False
assert loss_spec["predeclared_outputs"]
assert loss_spec["no_pass_threshold"] == "No retention threshold is declared. The result is descriptive sensitivity: survival, collapse, or failure are all reportable outcomes."

# Prospective comparator exact results.
assert comp["status"] == "DETERMINISTIC_CONTROL_COMPLETE"
assert comp["source_re_adjudication"] is False
assert comp["certified_MAIN40_unchanged"] == {
    "A0": 40, "A1": 0, "A2": 0,
    "component_A0": "24/24", "integrated_A0": "16/16"
}
summary = comp["comparator_summary"]
expected = {
    "G_FULL": (40, 0, 0),
    "G_DYN": (0, 40, 0),
    "G_POMDP_LIKE": (0, 40, 0),
    "G_MINUS_PI": (0, 40, 0),
    "G_MINUS_C": (0, 40, 0),
    "G_MINUS_P": (0, 40, 0),
    "G_MINUS_T": (0, 40, 0),
}
for arm, (a0, a1, a2) in expected.items():
    counts = summary[arm]["counts"]
    assert counts["A0"] == a0, (arm, counts)
    assert counts["A1"] == a1, (arm, counts)
    assert counts["A2"] == a2, (arm, counts)
    assert counts["NONLIFT_OR_UNDERDETERMINED"] == 0, (arm, counts)
assert comp["any_weaker_comparator_40_of_40_A0"] is False
assert comp["full_anchor_matches_certified_MAIN40"] is True
assert comp["basis_sensitive_under_direct_preservation"] is True
assert len(comp["row_results"]) == 40 * 7
assert comp["human_boundary"] == "Independent human re-adjudication remains NOT PERFORMED."

# Encoding-permissive composition baseline: original A-state semantics do not select the basis.
assert enc_spec["status"] == "FROZEN_BEFORE_ENCODING_PERMISSIVE_RESULT_MATERIALIZATION"
assert enc_spec["result_not_materialized_here"] is True
assert enc["status"] == "DETERMINISTIC_ENCODING_PERMISSIVE_BASELINE_COMPLETE"
assert enc["source_re_adjudication"] is False
assert enc["source_defined_mechanisms_changed"] is False
assert enc["all_tested_arms_40_of_40_A0"] is True
assert enc["weaker_arms_40_of_40_A0"] is True
for arm in expected:
    counts = enc["comparator_summary"][arm]["counts"]
    assert counts["A0"] == 40, (arm, counts)
    assert counts["A1"] == 0, (arm, counts)
    assert counts["A2"] == 0, (arm, counts)
    assert counts["UNDERDETERMINED"] == 0, (arm, counts)
assert len(enc["row_results"]) == 40 * 7
assert enc["independent_human_readjudication"] == "NOT_PERFORMED"
assert "does not by itself discriminate" in enc["constructive_encoding_boundary"]["consequence"]

# Lossy CPCG exact results.
assert loss["status"] == "DETERMINISTIC_LOSSY_SENSITIVITY_COMPLETE"
assert loss["rival_name"] == "Coarse Process-Constraint Graph (CPCG)"
assert loss["input"] == {"bounded_objects": 206, "cross_lane_families": 99, "corpus_claims": 60}
assert loss["non_injectivity"]["original_archetype_collision_group_count"] == 37
proj = loss["projection"]
assert proj["distinct_CPCG_signatures"] == 143
assert proj["cross_lane_CPCG_signatures"] == 62
assert proj["corpus_claims_supported_by_cross_lane_CPCG_signature"] == 58
assert proj["original_99_cross_lane_families_collapsed_with_another_original_family"] == 63
assert proj["original_99_cross_lane_families_not_collapsed_with_another_original_family"] == 36
assert abs(proj["collapsed_fraction"] - 0.636364) < 1e-12
assert loss["cross_label_witness"]["survives_shared_under_CPCG"] is True
assert loss["forbidden_promotions_preserved"] is True

# Same-label witness is explicitly post hoc and structurally disjoint.
assert same["status"] == "POST_HOC_EXPOSITORY_WITNESS_FROM_FROZEN_EVIDENCE"
assert same["inferential_status"] == "NOT_A_PREDECLARED_TEST"
assert same["shared_historical_label"] == "semantic memory"
assert same["claim_a"]["id"] == "MEM04"
assert same["claim_b"]["id"] == "CNC05"
assert same["frozen_bounded_overlap"]["count"] == 0
assert same["cpcg_sensitivity"]["projected_signature_intersection_count"] == 0
assert same["cpcg_sensitivity"]["remains_disjoint_under_CPCG"] is True

# Manuscript philosophical and editorial boundary.
thesis = (
    "Construct-based individuation is evidentially incomplete unless the comparison "
    "representation, preservation criterion, and granularity are independently stated; "
    "neither terminology nor successful reconstruction licenses representation-independent identity."
)
assert thesis in main
assert (
    "A Pre-Individuation Structural Comparison Procedure for Cognitive-Capacity Claims" in main
    or "When Does Structural Comparison Support Cognitive-Capacity Individuation?" in main
)
assert "claim-level structural comparison" in main
assert "evidential constraint on capacity comparison" in main
assert "capacity individuation" in main
assert "Coarse Process--Constraint Graph (CPCG)" in main
assert "206 bounded structural objects collapse to 143 distinct CPCG signatures" in main
assert "Sixty-two CPCG signatures" in main
assert "58 of the 60 source claims" in main
assert "Under the encoding-permissive baseline" in main
assert "every tested weaker representation also remains 40/40 A0" in main
assert "Under direct preservation" in main
assert "0 A0/40 A1" in main
assert "Prospective A0 therefore supports the absence of reconstruction-added coordination" in main
assert "semantic memory" in main and "MEM04" in main and "CNC05" in main
assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in main
assert "Independent human re-adjudication was not performed." in main
assert "Paper 2" not in main
assert "construct-label-neutral" not in main.lower()
assert "M11" not in main
assert "\\paragraph{" not in main

# Supplement keeps the audit material and exact limitations.
assert "a212820d225050bbc10d395685e74cd2fb0d9912" in supp
assert "b31f670f31d2f015b65d8bbf2e4fb12178b46694" in supp
assert "1c22fcb177c434d2900ffb3af9ef6baee2af73ff" in supp
assert "206 bounded objects" in supp
assert "143 CPCG signatures" in supp
assert "63/99" in supp
assert "62 CPCG signatures" in supp
assert "58/60 claims" in supp
assert "Encoding-permissive A-state closure" in supp
assert "Dynamic & 40 & 0 & 0" in supp
assert "Direct-preservation closure result" in supp
assert "Dynamic & 0 & 40 & 0" in supp
assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in supp
assert "\\paragraph{" not in supp

print("M11_DISCRIMINATIVE_BASELINES_GUARDS_PASS")
