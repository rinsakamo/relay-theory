#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M27 = ROOT / "research/paper2/p399/main/integration/M27"
MAIN = (ROOT / "paper/venues/jgps/main.tex").read_text(encoding="utf-8")
SUPP = (ROOT / "paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
BIB = (ROOT / "paper/venues/jgps/references.bib").read_text(encoding="utf-8")
INDEX = (ROOT / "paper/venues/jgps/supplementary-materials-index.md").read_text(encoding="utf-8")

SPEC = json.loads((M27 / "M27_SPEC_v1.json").read_text(encoding="utf-8"))
PROV = json.loads((M27 / "M27_PROVENANCE_QUALIFICATION_v1.json").read_text(encoding="utf-8"))
MATCH = json.loads((M27 / "M27_MATCHED_CASES_v1.json").read_text(encoding="utf-8"))
PRIOR = json.loads((M27 / "M27_PRIOR_ART_DELTA_v1.json").read_text(encoding="utf-8"))

assert SPEC["status"] == "COMPLETE"
assert SPEC["exact_parent_m26_head"] == "b91766d8717ebe2bf504ce5eb8acaea5cb3e33c8"
assert all(v["status"] == "CLOSED" for v in SPEC["gates"].values())
assert SPEC["new_empirical_corpus_execution"] is False
assert SPEC["new_human_coding"] is False
assert SPEC["terminal_state"] == "M27_REPRESENTATION_PROVENANCE_AND_MATCHED_DISCRIMINATION_CLARIFIED"

assert PROV["status"] == "FROZEN"
assert PROV["minimal_normative_premise"]["name"] == "MINIMAL_CONTRASTIVE_SUPPORT_NORM"
assert PROV["minimal_normative_premise"]["claimed_novel"] is False
assert PROV["representation_mediation"]["representation_map"] == "phi_R: F -> S_R"
assert PROV["discrimination_requirement"]["argumentative_indispensability_required"] is False
assert PROV["discrimination_requirement"]["evidential_strength_threshold_required"] is False
assert PROV["activated_defeater"]["logical_possibility_alone_sufficient"] is False
assert PROV["novelty_scope"] == "METHODOLOGICAL_SPECIALIZATION_NOT_FOUNDATIONAL_CONFIRMATION_THEORY"
assert PROV["terminal_state"] == "M27_FIBER_BASED_PROVENANCE_QUALIFICATION_FROZEN"

assert MATCH["status"] == "CONCEPTUAL_MATCHED_CASE_FROZEN"
assert MATCH["criterion_C"]["independently_declared"] is True
assert MATCH["ordinary_scientific_adequacy"]["held_fixed"] is True
assert MATCH["maps"]["phi_align"]["C_homogeneous"] is True
assert MATCH["maps"]["phi_cross"]["C_crossing"] is True
assert MATCH["missing_data"] is False
assert MATCH["unknown_parameter"] is False
assert MATCH["unperformed_intervention"] is False
assert MATCH["ordinary_underdetermination_required"] is False
assert MATCH["empirical_claim"] is False
assert MATCH["terminal_state"] == "M27_MATCHED_PROVENANCE_CASES_FROZEN"

assert PRIOR["beni_2024"]["doi"] == "10.1007/s10838-024-09673-w"
assert PRIOR["beni_2026"]["doi"] == "10.1007/s10838-025-09759-z"
assert PRIOR["north_2026"]["doi"] == "10.1007/s10838-025-09753-5"
assert PRIOR["brousalis_2026"]["doi"] == "10.1007/s10838-026-09773-9"
assert PRIOR["terminal_state"] == "M27_PRIOR_ART_DELTAS_PINNED"

for phrase in [
    "minimal contrastive norm for evidential support",
    r"\phi_R:\mathcal F\rightarrow\mathcal S_R",
    r"I_R(f_A,f_B)=1",
    r"\(C\)-homogeneous",
    r"\(C\)-crossing fiber",
    "methodological corollary",
    "not itself the novelty claim",
    "not reducible to ordinary missing-data underdetermination",
    r"\phi_{\mathrm{align}}",
    r"\phi_{\mathrm{cross}}",
    "Nothing is unobserved in this toy construction",
    "ordinary scientific adequacy of the two representations is held fixed",
    "logical possibility is insufficient",
    "Support-changing.",
    "input-qualification rule",
    "provenance qualification",
    "Beni's two JGPS papers",
    "2024 paper argues for a modest structural realism",
    "Formal continuity can warrant structural realism without every continuity class being a natural-kind class",
    "206 bounded objects; 99 cross-stratum families",
    "206 objects map to 143 coarse CPCG signatures; 63/99 cross-stratum families collide",
    r"where \(N\) denotes the coarse carrier/component family and \(T\) records temporal presence",
    "The procedures and supporting artifacts are documented for audit; independent inter-rater reliability remains unmeasured.",
]:
    assert phrase in MAIN, phrase

for forbidden in [
    r"\theta_A",
    r"\theta_B",
    r"p_t\leftarrow 1",
    "same-profile completion",
    "different-profile completion",
    "common intervention remains unperformed",
    "conceptual intervention example",
    "concrete two-system counterexample",
]:
    assert forbidden not in MAIN, forbidden

assert "@article{Beni2024StructuralRealismFEP," in BIB
assert "10.1007/s10838-024-09673-w" in BIB
assert "The procedures and supporting artifacts are documented for audit; independent inter-rater reliability remains unmeasured." in SUPP
assert r"Here \(N\) is the coarse carrier/component family and \(T\) records temporal presence." in SUPP

for name in [
    "M27_PROVENANCE_QUALIFICATION_v1.json",
    "M27_MATCHED_CASES_v1.json",
    "M27_PRIOR_ART_DELTA_v1.json",
]:
    assert name in INDEX, name

assert SPEC["scientific_authority_unchanged"]["whole_claim_pairs_incomparable"] == "1770/1770"
assert SPEC["scientific_authority_unchanged"]["bounded_objects"] == 206
assert SPEC["scientific_authority_unchanged"]["cross_stratum_families"] == 99
assert SPEC["scientific_authority_unchanged"]["cpcg_distinct_signatures"] == 143
assert SPEC["scientific_authority_unchanged"]["cpcg_collapsed_cross_stratum_families"] == "63/99"
assert SPEC["scientific_authority_unchanged"]["reverse_projection"] == "21 FULL / 22 PARTIAL / 17 RESIDUAL"
assert SPEC["scientific_authority_unchanged"]["residual_new_top_level_role"] == "0/17"

for name, text in [("main", MAIN), ("supplement", SUPP)]:
    assert re.search(r"\bM27\b", text) is None, name
    assert "ClaimIR" not in text, name

print("M27_REPRESENTATION_PROVENANCE_GUARDS_PASS")
