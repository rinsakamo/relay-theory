#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"paper/venues/jgps/main.tex").read_text(encoding="utf-8")
SUPP=(ROOT/"paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
BIB=(ROOT/"paper/venues/jgps/references.bib").read_text(encoding="utf-8")
M17=json.loads((ROOT/"research/paper2/p399/main/integration/M17/M17_SPEC_v1.json").read_text(encoding="utf-8"))
M16=json.loads((ROOT/"research/paper2/p399/main/integration/M16/M16_LRN03_SENSITIVITY_RESULT_v1.json").read_text(encoding="utf-8"))
MAP=json.loads((ROOT/"paper/venues/jgps/reader-facing-source-map.json").read_text(encoding="utf-8"))
INDEX=(ROOT/"paper/venues/jgps/supplementary-materials-index.md").read_text(encoding="utf-8")

assert M17["exact_parent_head"]=="8ccdcc73ed578386e5e003254a1f7bec82c0f86e"
assert M17["status"]=="COMPLETE"
assert M17["terminal_state"]=="M17_JGPS_PHILOSOPHY_FIRST_READER_FACING_CONSOLIDATION_COMPLETE"
assert M16["terminal_state"]=="M16_LRN03_CORRECTION_STRUCTURALLY_INVARIANT"
assert M16["headline_results"]["material_change"] is False
assert M16["whole_claim_recalculation"]["matrix_relation_change_count"]==0

M25_PATH=ROOT/"research/paper2/p399/main/integration/M25/M25_SPEC_v1.json"
if M25_PATH.exists():
    M25=json.loads(M25_PATH.read_text(encoding="utf-8"))
    assert M25["terminal_state"]=="M25_QUESTION_RELATIVE_DEFEATER_AND_PROCESS_WITNESS_CLARIFIED"
    for phrase in [
        "The Discrimination Requirement",
        "Structural invariance as a live target",
        "What corpus representation sensitivity does---and does not---show",
        "Capacity-level consequences",
        "target alignment",
        "capacity-relevant bridge warrant",
        "representational discrimination",
        "Procedural auditability is established; inter-rater reliability remains unmeasured.",
    ]:
        assert phrase in MAIN, phrase
    for name,text in [("main",MAIN),("supplement",SUPP)]:
        assert re.search(r"\bM(?:2[0-9]|1[0-9]|[0-9])\b",text) is None, name
        assert re.search(r"\bfrozen\b",text,re.I) is None, name
    print("M17_JGPS_READER_FACING_GUARDS_PASS_VIA_M25_SUCCESSOR")
    raise SystemExit(0)

# Journal-facing PDFs must not expose repository workflow codes or analysis slot IDs.
for name,text in [("main",MAIN),("supplement",SUPP)]:
    assert re.search(r"\bM(?:1[0-9]|[0-9])\b",text) is None, name
    assert "ClaimIR" not in text, name
    assert re.search(r"\bA[012]\b",text) is None, name
    assert re.search(r"\bINT-\d+\b",text) is None, name
    assert re.search(r"\b(?:ATT|BLF|CNC|CTL|LRN|MEM|PRD|SKL|CH)\d{2}\b",text) is None, name
    assert re.search(r"\bfrozen\b",text,re.I) is None, name

# Philosophy-first argumentative surface. Successor M19 may sharpen the
# named thesis while preserving the reader-facing boundary.
m19=(ROOT/"research/paper2/p399/main/integration/M19/M19_SPEC_v1.json").exists()
if m19:
    for phrase in [
        "The Discrimination Requirement",
        "Structural invariance as a live target",
        "clearest contemporary application of the Discrimination Requirement",
        "Critical representation-sensitivity tests",
        "Capacity-level consequences",
        "target alignment",
        "capacity-relevant bridge warrant",
        "representational discrimination",
        "Procedural auditability is established; inter-rater reliability remains unmeasured.",
    ]:
        assert phrase in MAIN, phrase
else:
    for phrase in [
        "From reconstruction success to licensed identity inference",
        "The argument can be stated directly",
        "Structural invariance as a live target",
        "Beni's structural-realist proposal",
        "This is not an attribution of a simple fallacy to Beni",
        "North's defense of objective or non-pragmatic perspicuity",
        "The present claim adds a non-circularity constraint",
        "Critical representation-sensitivity tests",
        "Botvinick et al.--Tulving comparison",
        "The corpus is purposive and diagnostic",
    ]:
        assert phrase in MAIN, phrase

assert "Decisive representation tests" not in MAIN
assert "GPT-6 Astra" not in MAIN
assert "GPT-6.1 Sol" not in MAIN
if m19:
    assert "Secondary procedural robustness diagnostics" in MAIN
    for forbidden in ["40/40","9/10","10/10","nine of ten","mutually compatible in all ten"]:
        assert forbidden not in MAIN
else:
    assert "named-model configurations" in MAIN
    assert "nine of ten" in MAIN
    assert "mutually compatible in all ten" in MAIN

# Corpus is not sold as prevalence evidence.
assert "not a probability sample" in MAIN
if m19:
    assert "supporting diagnostics rather than the philosophical contribution" in MAIN
else:
    assert "witnesses and stress tests, not prevalence estimates" in MAIN
assert "population prevalence" in MAIN

# Supplement state is current and reader-facing.
assert "protocol frozen, not yet performed" not in SUPP.lower()
assert ("named-model procedural robustness diagnostics: both the unanchored and claim-anchored replay analyses have been completed" in SUPP if m19 else "named-model validation: both the unanchored and claim-anchored replay analyses have been completed" in SUPP)
assert "Versioned study materials" in SUPP
assert "reader-facing supplementary-materials index" in SUPP
assert ("Named-model procedural robustness diagnostics" in SUPP if m19 else "Named-model reconstruction validation" in SUPP)
assert "Source correction and sensitivity analysis" in SUPP
assert "The index connects each reported analysis to its versioned supporting records" in SUPP
assert re.search(r"\b[0-9a-f]{40,64}\b",SUPP) is None

# Reader-facing indexes are complete.
assert len(MAP["original_60"])==60
assert len(MAP["prospective_40"])==40
assert [x["reader_id"] for x in MAP["original_60"]]==[f"S{i:02d}" for i in range(1,61)]
assert [x["reader_id"] for x in MAP["prospective_40"]]==[f"P{i:02d}" for i in range(1,41)]
assert "Internal workflow and milestone identifiers are repository provenance only" in INDEX

# Central analyzed scientific sources are ordinary bibliography entries.
for key in [
    "Duncan1984SelectiveAttention",
    "BehrensEtAl2007ValueInformation",
    "BotvinickEtAl2001ConflictMonitoring",
    "Tulving2002EpisodicMemory",
    "PattersonNestorRogers2007Semantic",
    "KarpickeBlunt2011RetrievalPractice",
]:
    assert "{"+key+"," in BIB, key

# Core result boundaries remain explicit.
assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in MAIN
assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in SUPP

print("M17_JGPS_READER_FACING_GUARDS_PASS")
