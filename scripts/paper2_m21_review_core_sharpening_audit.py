#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "paper/venues/jgps/main.tex").read_text(encoding="utf-8")
SUPP = (ROOT / "paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
BIB = (ROOT / "paper/venues/jgps/references.bib").read_text(encoding="utf-8")
INDEX = (ROOT / "paper/venues/jgps/supplementary-materials-index.md").read_text(encoding="utf-8")
M21 = json.loads((ROOT / "research/paper2/p399/main/integration/M21/M21_SPEC_v1.json").read_text(encoding="utf-8"))
PIN = json.loads((ROOT / "research/paper2/p399/main/integration/M21/M21_TEMPORAL_ABSTRACTION_SOURCE_PIN_v1.json").read_text(encoding="utf-8"))
M20 = json.loads((ROOT / "research/paper2/p399/main/integration/M20/M20_SPEC_v1.json").read_text(encoding="utf-8"))
WIT = json.loads((ROOT / "research/paper2/p399/main/integration/M20/M20_CENTRAL_WITNESS_AUDIT_v1.json").read_text(encoding="utf-8"))
CPCG = json.loads((ROOT / "research/paper2/p399/main/integration/M11/M11_LOSSY_RIVAL_RESULTS_v1.json").read_text(encoding="utf-8"))

assert M21["exact_parent_head"] == "0592a9ee2d34c993739d48a79003bb229122553f"
assert M21["status"] == "COMPLETE"
assert M21["terminal_state"] == "M21_REVIEW_CORE_SHARPENED_TEMPORAL_RIVAL_INDEPENDENTLY_MOTIVATED"
assert M21["scientific_authority_unchanged"] is True
assert M20["terminal_state"] == "M20_REPRESENTATIONAL_DEFEATER_PINNED_CENTRAL_WITNESSES_AUDITABLE"

assert r"\title{A Discrimination Requirement for Structural Approaches to Cognitive-Capacity Individuation}" in MAIN
assert "When Does Structural Comparison Support Cognitive-Capacity Individuation?" not in MAIN

for phrase in [
    "scientific warrant for }R",
    "individuative warrant for invariant }I",
    "representation justification is not yet identity-relevance justification",
    "The Discrimination Requirement adds a provenance constraint",
    "North's objective perspicuity",
    "Brousalis makes epistemically relevant similarities and differences",
]:
    assert phrase in MAIN, phrase

for phrase in [
    "Scientifically motivated.",
    "Live alternative.",
    "Discrimination.",
    "independently articulable modeling, explanatory, measurement, or abstraction aim",
    "change an identity-relevant verdict",
    "live, scientifically motivated alternative",
    "This is not a global skeptical defeater.",
]:
    assert phrase in MAIN, phrase

for phrase in [
    "using PP--FEP to articulate candidate structural invariants",
    "assigning those invariants objective force for kind individuation",
    "it does not challenge the legitimacy of PP--FEP simply as a scientific scaffold",
    "Beni provides an important application rather than the sole target",
]:
    assert phrase in MAIN, phrase

assert PIN["status"] == "SOURCE_METADATA_VERIFIED"
assert PIN["source"]["doi"] == "10.1016/j.cogsys.2006.08.002"
assert PIN["source"]["verified_date"] == "2026-10-08"
assert "Treur2007TemporalFactorisation" in MAIN
assert "{Treur2007TemporalFactorisation," in BIB
assert "10.1016/j.cogsys.2006.08.002" in BIB
assert "10.1016/j.cogsys.2006.08.002" in SUPP
for phrase in [
    "scientifically intelligible rather than arbitrary string deletion",
    "prima facie reason to ask the coarser question",
    "The projection itself does not decide which possibility is correct.",
]:
    assert phrase in MAIN, phrase

bot = [c for c in WIT["cases"] if c["reader_facing_case"] == "Botvinick--Tulving"][0]
assert bot["fine_overlap_positive"] is False
assert bot["cpcg_overlap_positive"] is True
assert bot["cpcg_shared_signature"]["original_archetype_ids"] == ["A-53b16535e1c2", "A-af97ed649c6f"]
assert CPCG["projection"]["distinct_CPCG_signatures"] == 143
assert CPCG["projection"]["original_99_cross_lane_families_collapsed_with_another_original_family"] == 63
for phrase in [
    "206 fine-grained reusable objects to 143 coarse signatures",
    "63 of the 99 fine cross-stratum families",
    "Neither result establishes equal adequacy of the rivals.",
    "not presented as the uniquely correct representation",
    "nor that the coarse representation is correct",
]:
    assert phrase in MAIN, phrase

assert r"\caption{Designed corpus." not in MAIN
assert r"\caption{Epistemic status of the principal analyses." not in MAIN
assert r"\begin{tikzpicture}" not in MAIN
assert "Lossless and lossy representation controls" in SUPP
assert "supporting diagnostics rather than the philosophical contribution" in MAIN
assert "Secondary procedural robustness diagnostics" in MAIN
assert "the pattern is partly built into the contrast between those criteria" in MAIN
assert "procedural robustness diagnostic" in MAIN

for forbidden in ["40/40", "9/10", "10/10", "nine of ten", "mutually compatible in all ten"]:
    assert forbidden not in MAIN, forbidden
for name, text in [("main", MAIN), ("supplement", SUPP)]:
    assert re.search(r"\bM(?:2[0-9]|1[0-9]|[0-9])\b", text) is None, name
    assert "ClaimIR" not in text, name
    assert re.search(r"\b(?:ATT|BLF|CNC|CTL|LRN|MEM|PRD|SKL|CH)\d{2}\b", text) is None, name
assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in MAIN
assert "independent coding reliability" in MAIN
assert "population prevalence" in MAIN
assert "M21_TEMPORAL_ABSTRACTION_SOURCE_PIN_v1.json" in INDEX

print("M21_REVIEW_CORE_SHARPENING_GUARDS_PASS")
