#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M26 = ROOT / "research/paper2/p399/main/integration/M26"
MAIN = (ROOT / "paper/venues/jgps/main.tex").read_text(encoding="utf-8")
SUPP = (ROOT / "paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
INDEX = (ROOT / "paper/venues/jgps/supplementary-materials-index.md").read_text(encoding="utf-8")

SPEC = json.loads((M26 / "M26_SPEC_v1.json").read_text(encoding="utf-8"))
DR = json.loads((M26 / "M26_ACTIVATED_DR_v1.json").read_text(encoding="utf-8"))
CEX = json.loads((M26 / "M26_UNDERCUTTING_COUNTEREXAMPLE_v1.json").read_text(encoding="utf-8"))

assert SPEC["status"] == "COMPLETE"
assert SPEC["exact_parent_m25_head"] == "275f1cd8bd22e44d416d833e77d45afcc3712470"
assert all(v["status"] == "CLOSED" for v in SPEC["gates"].values())
assert SPEC["new_empirical_corpus_execution"] is False
assert SPEC["new_human_coding"] is False
assert SPEC["terminal_state"] == "M26_ACTIVATED_UNDERCUTTING_AND_GENERAL_PROVENANCE_SEPARATED"

assert DR["status"] == "FROZEN"
assert DR["general_provenance_condition"]["actual_rival_required"] is False
assert DR["general_provenance_condition"]["exhaustive_elimination_of_possible_representations_required"] is False
assert DR["activated_condition"]["requires_specific_rival"] is True
assert DR["activated_condition"]["rival_must_remain_compatible_with_current_evidence"] is True
assert DR["activated_condition"]["same_Q_required"] is True
assert DR["activated_condition"]["same_C_required"] is True
assert DR["activated_condition"]["rival_must_preserve_C_relevant_distinction"] is True
assert DR["activated_condition"]["unresolved_required"] is True
assert DR["rebutting_boundary"]["H_id_must_remain_open_for_pure_undercutting_example"] is True
assert DR["terminal_state"] == "M26_GENERAL_AND_ACTIVATED_DR_SCOPE_FROZEN"

assert CEX["status"] == "CONCEPTUAL_COUNTEREXAMPLE_FROZEN"
assert CEX["observed_evidence_E"]["baseline_constraint"] == "p[t] = 0 for every observed trial"
assert CEX["live_completions"]["both_compatible_with_E"] is True
assert CEX["intervention_family_J"]["P_star"] == "Apply the same external operation p[t] <- 1 to either system under the matched test condition."
assert CEX["intervention_family_J"]["performed"] is False
assert CEX["inferential_status"]["H_id"] == "OPEN"
assert "does not establish theta_A != theta_B" in CEX["inferential_status"]["not_rebutting_reason"]
assert "equally compatible with E" in CEX["inferential_status"]["undercutting_reason"]
assert CEX["empirical_claim"] is False
assert CEX["terminal_state"] == "M26_PURE_UNDERCUTTING_COUNTEREXAMPLE_FROZEN"

M27_PATH=ROOT/"research/paper2/p399/main/integration/M27/M27_SPEC_v1.json"
if M27_PATH.exists():
    M27=json.loads(M27_PATH.read_text(encoding="utf-8"))
    PROV=json.loads((ROOT/"research/paper2/p399/main/integration/M27/M27_PROVENANCE_QUALIFICATION_v1.json").read_text(encoding="utf-8"))
    MATCH=json.loads((ROOT/"research/paper2/p399/main/integration/M27/M27_MATCHED_CASES_v1.json").read_text(encoding="utf-8"))
    assert M27["terminal_state"]=="M27_REPRESENTATION_PROVENANCE_AND_MATCHED_DISCRIMINATION_CLARIFIED"
    assert PROV["minimal_normative_premise"]["claimed_novel"] is False
    assert PROV["activated_defeater"]["logical_possibility_alone_sufficient"] is False
    assert MATCH["missing_data"] is False
    assert MATCH["unknown_parameter"] is False
    assert MATCH["unperformed_intervention"] is False
    assert MATCH["ordinary_underdetermination_required"] is False
    for phrase in [
        "minimal contrastive norm for evidential support",
        "C-homogeneous",
        "C-crossing fiber",
        "matched comparison",
        "Nothing is unobserved in this toy construction",
        "methodological corollary",
        "Support-changing.",
    ]:
        assert phrase in MAIN, phrase
    for forbidden in [
        "externally manipulable binary channel",
        "same-profile completion",
        "different-profile completion",
        "p_t\\leftarrow 1",
    ]:
        assert forbidden not in MAIN, forbidden
    print("M26_ACTIVATED_UNDERCUTTING_GUARDS_PASS_VIA_M27_SUCCESSOR")
    raise SystemExit(0)

for phrase in [
    "general provenance condition",
    "stronger \\emph{activated condition}",
    "Activated Representational-Defeater Trigger",
    "A rival that already establishes \\(\\neg H_{\\mathrm{id}}\\)",
    "externally manipulable binary channel \\(p_t\\)",
    "p_t\\leftarrow 1",
    "has not been performed",
    "same-profile completion",
    "different-profile completion",
    "identity hypothesis remains open",
    "genuinely undercutting rather than rebutting",
    "do A and B instantiate the same capacity type?",
    "stable counterfactual organization over a declared intervention family \\(J\\)",
    "does not diagnose a standing defect in Beni's framework",
    "prior provenance question specific to representation-mediated individuation",
    "corpus-anchored demonstration of representation sensitivity",
]:
    assert phrase in MAIN, phrase

for forbidden in [
    "System A has one internal bit",
    "System B has two internal bits",
    "v_{t+1}=u_t\\oplus v_t",
    "let A continue to report",
    "criterion \\(C\\) that includes the relevant update and intervention profile",
]:
    assert forbidden not in MAIN, forbidden

for phrase in [
    "Activated Representational-Defeater Trigger",
    "corpus-anchored demonstration",
]:
    assert phrase in SUPP, phrase

assert "Activated Activated" not in SUPP

for name in [
    "M26_ACTIVATED_DR_v1.json",
    "M26_UNDERCUTTING_COUNTEREXAMPLE_v1.json",
]:
    assert name in INDEX, name

for name, text in [("main", MAIN), ("supplement", SUPP)]:
    assert re.search(r"\bM26\b", text) is None, name
    assert "ClaimIR" not in text, name

assert SPEC["scientific_authority_unchanged"]["whole_claim_pairs_incomparable"] == "1770/1770"
assert SPEC["scientific_authority_unchanged"]["bounded_objects"] == 206
assert SPEC["scientific_authority_unchanged"]["cross_stratum_families"] == 99
assert SPEC["scientific_authority_unchanged"]["reverse_projection"] == "21 FULL / 22 PARTIAL / 17 RESIDUAL"
assert SPEC["scientific_authority_unchanged"]["residual_new_top_level_role"] == "0/17"

print("M26_ACTIVATED_UNDERCUTTING_GUARDS_PASS")
