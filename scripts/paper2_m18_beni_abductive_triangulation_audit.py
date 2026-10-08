#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"paper/venues/jgps/main.tex").read_text(encoding="utf-8")
SUPP=(ROOT/"paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
M18=json.loads((ROOT/"research/paper2/p399/main/integration/M18/M18_SPEC_v1.json").read_text(encoding="utf-8"))
M16=json.loads((ROOT/"research/paper2/p399/main/integration/M16/M16_LRN03_SENSITIVITY_RESULT_v1.json").read_text(encoding="utf-8"))

assert M18["exact_parent_head"]=="907ceadccc4daeb71888aecdf9582bf5cf4e1b63"
assert M18["terminal_state"]=="M18_BENI_ABDUCTIVE_EVIDENCE_AND_SOURCE_FIRST_TRIANGULATION_COMPLETE"
assert M16["terminal_state"]=="M16_LRN03_CORRECTION_STRUCTURALLY_INVARIANT"
assert M16["headline_results"]["material_change"] is False
assert M16["whole_claim_recalculation"]["matrix_relation_change_count"] == 0

M27_PATH=ROOT/"research/paper2/p399/main/integration/M27/M27_SPEC_v1.json"
if M27_PATH.exists():
    M27=json.loads(M27_PATH.read_text(encoding="utf-8"))
    PRIOR=json.loads((ROOT/"research/paper2/p399/main/integration/M27/M27_PRIOR_ART_DELTA_v1.json").read_text(encoding="utf-8"))
    assert M27["terminal_state"]=="M27_REPRESENTATION_PROVENANCE_AND_MATCHED_DISCRIMINATION_CLARIFIED"
    assert PRIOR["beni_2024"]["doi"]=="10.1007/s10838-024-09673-w"
    assert PRIOR["beni_2026"]["doi"]=="10.1007/s10838-025-09759-z"
    for phrase in [
        "Beni's two JGPS papers",
        "Formal continuity can warrant structural realism",
        "The Discrimination Requirement",
        "source-first",
        "not framework-free or representation-neutral",
        "input-qualification rule",
        "objective perspicuity",
    ]:
        assert phrase in MAIN, phrase
    assert "The procedures and supporting artifacts are documented for audit; independent inter-rater reliability remains unmeasured." in MAIN
    print("M18_BENI_ABDUCTIVE_TRIANGULATION_GUARDS_PASS_VIA_M27_SUCCESSOR")
    raise SystemExit(0)

M25_PATH=ROOT/"research/paper2/p399/main/integration/M25/M25_SPEC_v1.json"
if M25_PATH.exists():
    M25=json.loads(M25_PATH.read_text(encoding="utf-8"))
    assert M25["terminal_state"]=="M25_QUESTION_RELATIVE_DEFEATER_AND_PROCESS_WITNESS_CLARIFIED"
    for phrase in [
        "genuine abductive evidence",
        "The Discrimination Requirement",
        "target organization",
        "comparison framework",
        "source-first",
        "not framework-free or representation-neutral",
        "objective perspicuity",
    ]:
        assert phrase in MAIN, phrase
    print("M18_BENI_ABDUCTIVE_TRIANGULATION_GUARDS_PASS_VIA_M25_SUCCESSOR")
    raise SystemExit(0)

# Preserve the abductive-evidence interpretation while allowing successor M19
# to name the more precise Discrimination Requirement.
m19=(ROOT/"research/paper2/p399/main/integration/M19/M19_SPEC_v1.json").exists()
if m19:
    for phrase in [
        "genuine abductive evidence",
        "The Discrimination Requirement",
        "source-side recurrence",
        "framework-enabled commonality",
        "source-first",
        "not framework-free or representation-neutral",
        "A systematic alignment with PP--FEP would be an especially probative application",
        "not a premise of the general argument",
        "objective perspicuity",
    ]:
        assert phrase in MAIN, phrase
else:
    thesis=(
        "An inference from structural comparison to cognitive-capacity identity is "
        "epistemically licensed only if the comparison representation, preservation "
        "criterion, and granularity are specified and warranted for that inferential use."
    )
    assert thesis in MAIN
    for phrase in [
        "explanatory or unificatory success is genuine abductive evidence",
        "source-of-invariance",
        "The central claim is not that reconstruction success is epistemically inert.",
        "successful unification is compatible with at least three possibilities",
        "The success of \\(R\\) alone cannot discriminate among those possibilities.",
        "This is not an attribution of a simple fallacy to Beni",
        "The present reconstruction supplies a complementary route.",
        "source-first",
        "the method is not framework-free or representation-neutral",
        "This yields a triangulation strategy",
        "Convergence between the two routes",
        "a systematic alignment with PP--FEP is a further comparative test, not a result presupposed here",
        "The present claim adds a non-circularity constraint",
        "The contribution is thus a method for epistemic triangulation around structural invariance.",
        "The paper therefore rejects neither inference to the best explanation nor explanatory evidence",
    ]:
        assert phrase in MAIN, phrase

# Do not slip into a stronger neutrality claim than the method supports.
assert "concept-neutral" not in MAIN
assert "framework-neutral" not in MAIN
assert "representation-neutral cognitive ontology" not in MAIN
assert ("systematic alignment with PP--FEP" in MAIN or "systematic alignment with PP--FEP would be an especially probative application" in MAIN)

# The article should not state that explanatory success is evidence-free.
for forbidden in [
    "explanatory success is not evidence",
    "reconstruction success is not evidence",
    "successful unification is epistemically inert",
]:
    assert forbidden not in MAIN.lower()

# Journal-facing internal-code boundary remains intact.
for name,text in [("main",MAIN),("supplement",SUPP)]:
    assert re.search(r"\bM(?:1[0-9]|[0-9])\b",text) is None, name
    assert "ClaimIR" not in text, name
    assert re.search(r"\bA[012]\b",text) is None, name
    assert re.search(r"\bINT-\d+\b",text) is None, name
    assert re.search(r"\b(?:ATT|BLF|CNC|CTL|LRN|MEM|PRD|SKL|CH)\d{2}\b",text) is None, name
    assert re.search(r"\bfrozen\b",text,re.I) is None, name

# Scientific/validation boundaries remain unchanged.
assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in MAIN
assert "population prevalence" in MAIN
assert "independent coding reliability" in MAIN
if m19:
    assert "Secondary procedural robustness diagnostics" in MAIN
    assert "nine of ten" not in MAIN
    assert "mutually compatible in all ten" not in MAIN
else:
    assert "nine of ten" in MAIN
    assert "mutually compatible in all ten" in MAIN

print("M18_BENI_ABDUCTIVE_TRIANGULATION_GUARDS_PASS")
