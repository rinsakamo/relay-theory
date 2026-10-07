#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"paper/venues/jgps/main.tex").read_text(encoding="utf-8")
SUPP=(ROOT/"paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
M19=json.loads((ROOT/"research/paper2/p399/main/integration/M19/M19_SPEC_v1.json").read_text(encoding="utf-8"))
M18=json.loads((ROOT/"research/paper2/p399/main/integration/M18/M18_SPEC_v1.json").read_text(encoding="utf-8"))
M16=json.loads((ROOT/"research/paper2/p399/main/integration/M16/M16_LRN03_SENSITIVITY_RESULT_v1.json").read_text(encoding="utf-8"))

assert M19["exact_parent_head"]=="5a6c8b9a26c58367bf80a79e05d35c335bad2bc3"
assert M19["terminal_state"]=="M19_DISCRIMINATION_REQUIREMENT_CONSOLIDATED_CLAIM_TO_CAPACITY_BRIDGE_EXPLICIT"
assert M18["terminal_state"]=="M18_BENI_ABDUCTIVE_EVIDENCE_AND_SOURCE_FIRST_TRIANGULATION_COMPLETE"
assert M16["terminal_state"]=="M16_LRN03_CORRECTION_STRUCTURALLY_INVARIANT"
assert M16["headline_results"]["material_change"] is False
assert M16["whole_claim_recalculation"]["matrix_relation_change_count"]==0

dr=M19["central_contribution"]["statement"]
assert dr in MAIN
assert MAIN.count("Discrimination Requirement") >= 10

# Named novelty claim is visible early and remains the conclusion.
abstract=MAIN.split("\\begin{abstract}",1)[1].split("\\end{abstract}",1)[0]
intro=MAIN.split("\\section{Introduction}",1)[1].split("\\section{The Discrimination Requirement}",1)[0]
discussion=MAIN.split("\\section{Discussion}",1)[1].split("\\section{Conclusion}",1)[0]
conclusion=MAIN.split("\\section{Conclusion}",1)[1].split("\\section*{Reproducibility",1)[0]
for part in [abstract,intro,discussion,conclusion]:
    assert "Discrimination Requirement" in part

# Claim -> capacity bridge is explicit and explicitly non-sufficient.
for phrase in [
    "claim-level recurrent structure",
    "target alignment",
    "capacity-relevant bridge warrant",
    "representational discrimination",
    "defeasible evidence for capacity identity",
    "This is an evidential schema, not a sufficient definition of capacity identity.",
]:
    assert phrase in MAIN, phrase

assert "The paper therefore does not offer a positive theory of capacity identity." in MAIN
assert "necessary condition on when claim-level structural evidence may be promoted" in MAIN

# Beni is a central application, not an empirical premise.
for phrase in [
    "clearest contemporary application of the Discrimination Requirement",
    "does not depend on completing a PP--FEP-specific empirical comparison",
    "not a premise of the general argument",
    "not reported as a completed result here",
    "Beni provides an important application rather than the sole target",
]:
    assert phrase in MAIN, phrase

# Explanatory success remains evidential.
assert "genuine abductive evidence" in MAIN
for forbidden in [
    "explanatory success is not evidence",
    "reconstruction success is not evidence",
    "successful unification is epistemically inert",
]:
    assert forbidden not in MAIN.lower()

# CPCG is a live alternative, not a declared true/privileged representation.
for phrase in [
    "scientifically intelligible rather than arbitrary string deletion",
    "prima facie reason to ask the coarser question",
    "The projection itself does not decide which possibility is correct.",
    "Neither result establishes equal adequacy of the rivals.",
]:
    assert phrase in MAIN, phrase
assert "uniquely correct representation" not in MAIN

# Large diagnostics are subordinate in the journal-facing main text.
assert "Secondary procedural robustness diagnostics" in MAIN
assert "procedural robustness diagnostic" in MAIN
assert "the pattern is partly built into the contrast between those criteria" in MAIN
for forbidden in ["40/40","9/10","10/10","nine of ten","mutually compatible in all ten"]:
    assert forbidden not in MAIN, forbidden
assert "Named-model procedural robustness diagnostics" in SUPP
assert "GPT-6 Astra / Medium" in SUPP
assert "GPT-6.1 Sol / Medium" in SUPP

# Preserve JGPS-facing terminology boundary.
for name,text in [("main",MAIN),("supplement",SUPP)]:
    assert re.search(r"\bM(?:1[0-9]|[0-9])\b",text) is None, name
    assert "ClaimIR" not in text, name
    assert re.search(r"\bA[012]\b",text) is None, name
    assert re.search(r"\bINT-\d+\b",text) is None, name
    assert re.search(r"\b(?:ATT|BLF|CNC|CTL|LRN|MEM|PRD|SKL|CH)\d{2}\b",text) is None, name
    assert re.search(r"\bfrozen\b",text,re.I) is None, name

# Reliability boundary remains exact.
assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in MAIN
assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in SUPP
assert "independent coding reliability" in MAIN
assert "population prevalence" in MAIN

print("M19_DISCRIMINATION_REQUIREMENT_GUARDS_PASS")
