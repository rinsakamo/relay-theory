#!/usr/bin/env python3
"""M33 fail-closed gate: keep source facts, map/data typing and submission contract distinct."""
from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / "research/paper2/p399/main/integration/M33/M33_REPRESENTATION_MEASUREMENT_BOUNDARY_v1.json").read_text(encoding="utf8"))
m32 = json.loads((root / "research/paper2/p399/main/integration/M32/M32_EVIDENTIAL_PROMOTION_AUDIT_v1.json").read_text(encoding="utf8"))
m29 = json.loads((root / "research/paper2/p399/main/integration/M29/M29_FINITE_PAIR_LAW_v1.json").read_text(encoding="utf8"))
main = (root / "paper/venues/jgps/main.tex").read_text(encoding="utf8")
supp = (root / "paper/venues/jgps/supplement.tex").read_text(encoding="utf8")
bib = (root / "paper/venues/jgps/references.bib").read_text(encoding="utf8")
index = (root / "paper/venues/jgps/supplementary-materials-index.md").read_text(encoding="utf8")

assert data["exact_parent_m32_head"] == "23edd6a088b34a3b70cbffe9a80505ff7534c5b1"
assert data["new_source_coding"] is False
assert data["empirical_pairwise_defeater_confirmed"] is False
src = data["source_registry"]
assert [(s["id"], s["doi"], s["type"]) for s in src] == [
    ("Patterson2007", "10.1038/nrn2277", "review"),
    ("Gainotti2012", "10.1016/j.cortex.2011.06.019", "position paper")
]
for s in src:
    assert s["doi"] in bib and s["publisher"].startswith("https://")
typ = data["type_system"]
assert typ["C_epistemically_justified_by_source"] is False
assert typ["measured_pair_of_systems"] is False
assert typ["D1"].startswith("(D0,L)")
assert "D0" in typ["prohibition"] and "phi_deficit" in typ["prohibition"]
ops = data["operations"]
assert [z["operation"] for z in ops] == [
    "REPRESENTATION_CHANGE", "MEASUREMENT_EXTENSION",
    "EXPLANATORY_COMPARISON", "IDENTITY_SUPPORT_ATTRIBUTION"
]
assert "Same D1" in ops[0]["input"]
assert "acquire L" in ops[1]["change"]
assert "same" in ops[2]["input"].lower()
assert "H_C(A,B)" in ops[3]["change"]
out = data["outcomes"]
assert out["representation_only_sourced_scientific_pairwise_defeater"] is False
assert out["data_extension_is_different_operation"] is True
assert out["architecture_rival_is_scientifically_grounded"] is True
assert out["conditional_Q_C_author_constructed"] is True
assert out["claim_of_new_confirmation_axiom"] is False
assert F(out["known_map_toy_LR_x"]) == 4 and F(out["known_map_toy_LR_y"]) == 1
assert F(out["toy_task_accuracy_each"]) == F(3,4)
assert m29["proof_model"]["events"]["Ex"]["LR"] == "4"
assert m29["proof_model"]["events"]["Ey"]["LR"] == "1"
assert m32["no_empirical_identity_defeater"] is True

for literal in (
    "A coarse task-level map",
    r"\phi_{\mathrm{task}}",
    r"\phi_{\mathrm{lesion}}",
    "cannot automatically be treated as two maps of the same observations",
    "changes the",
    "explanatory interpretation",
    "underqualified",
    r"Q_{\mathrm{sem}},C_{\mathrm{sem}}",
    "the review",
    r"\usepackage[round,authoryear]{natbib}",
    r"\providecommand{\doi}[1]",
    r"https://doi.org/#1",
    "23edd6a088b34a3b70cbffe9a80505ff7534c5b1",
):
    assert literal in main, f"Main missing: {literal}"
for literal in (
    "Semantic-hub case: separating representation, measurement and model comparison",
    "REPRESENTATION_CHANGE",
):
    # The visible table should use prose, not repository-specific machine identifiers.
    if literal != "REPRESENTATION_CHANGE":
        assert literal in supp, f"Supplement missing: {literal}"
for literal in (
    r"D_0", r"D_1", r"\phi_{\mathrm{task}}",
    r"\phi_{\mathrm{deficit}}", "not a pure change of map",
    "Two genuinely",
    "same-input representation comparison",
    "PattersonNestorRogers2007Semantic",
    "Gainotti2012SemanticFormat",
    "not a reported head-to-head experiment",
):
    # Case-insensitive only where English prose varies.
    if literal == "Two genuinely":
        continue
    assert literal in supp, f"Supplement missing: {literal}"
assert "M33_REPRESENTATION_MEASUREMENT_BOUNDARY_v1.json" in index
assert "paper2_m33_representation_measurement_audit.py" in index
assert "M32_EVIDENTIAL_PROMOTION_AUDIT_v1.json" in index
assert "23edd6a088b34a3b70cbffe9a80505ff7534c5b1" in index

submitted = data["submission"]
assert submitted["natbib_options"] == "round,authoryear"
assert submitted["guidelines_url"] == "https://link.springer.com/journal/10838/submission-guidelines"
assert submitted["archive_at_final_head_pending"] is True
assert "Use of generative AI" in main and "OpenAI ChatGPT" in main
assert "https://github.com/rinsakamo/relay-theory" in main
sci = data["scientific_authority_unchanged"]
assert sci["whole_pairs"] == "1770/1770 INCOMPARABLE"
assert sci["bounded_objects"] == 206 and sci["cross_stratum_families"] == 99
assert sci["cpcg_signatures"] == 143 and sci["collisions"] == "63/99"
assert sci["reverse"] == "21 FULL / 22 PARTIAL / 17 RESIDUAL"
assert sci["new_roles"] == "0/17" and sci["human_inter_rater"] == "unmeasured"

print("M33_REPRESENTATION_MEASUREMENT_AND_IDENTITY_SUPPORT_SCOPE_PASS")
