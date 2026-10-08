#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
M25=ROOT/"research/paper2/p399/main/integration/M25"
MAIN=(ROOT/"paper/venues/jgps/main.tex").read_text(encoding="utf-8")
SUPP=(ROOT/"paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
BIB=(ROOT/"paper/venues/jgps/references.bib").read_text(encoding="utf-8")
INDEX=(ROOT/"paper/venues/jgps/supplementary-materials-index.md").read_text(encoding="utf-8")
BOUNDED=json.loads((ROOT/"research/paper2/bounded_xlike_reconstruction_v1.json").read_text(encoding="utf-8"))
CPCG=json.loads((ROOT/"research/paper2/p399/main/integration/M11/M11_LOSSY_RIVAL_RESULTS_v1.json").read_text(encoding="utf-8"))

SPEC=json.loads((M25/"M25_SPEC_v1.json").read_text(encoding="utf-8"))
SCOPE=json.loads((M25/"M25_QUESTION_RELATIVE_DEFEATER_v1.json").read_text(encoding="utf-8"))
PROC=json.loads((M25/"M25_PROCESS_WITNESS_AUDIT_v1.json").read_text(encoding="utf-8"))
CEX=json.loads((M25/"M25_COUNTEREXAMPLE_v1.json").read_text(encoding="utf-8"))

assert SPEC["status"]=="COMPLETE"
assert SPEC["exact_parent_m24_head"]=="11f9d2cb0cf34d3ac3263562bd84b19999b8c9c3"
assert all(v["status"]=="CLOSED" for v in SPEC["gates"].values())
assert SPEC["new_empirical_corpus_execution"] is False
assert SPEC["new_human_coding"] is False
assert SPEC["terminal_state"]=="M25_QUESTION_RELATIVE_DEFEATER_AND_PROCESS_WITNESS_CLARIFIED"

assert SCOPE["status"]=="FROZEN"
assert SCOPE["trigger"]["same_Q_required"] is True
assert SCOPE["trigger"]["same_C_required"] is True
assert SCOPE["trigger"]["different_legitimate_questions_alone_are_insufficient"] is True
assert SCOPE["substantial_evidential_role"]["type"]=="ARGUMENTATIVE_COUNTERFACTUAL_DEPENDENCE_NOT_NUMERICAL_THRESHOLD"
assert SCOPE["bridge_relation"]["separate_independent_evidence_type_required"] is False
assert SCOPE["defeater_type"]=="UNDERCUTTING_NOT_REBUTTING"
assert SCOPE["corpus_representation_sensitivity_is_automatically_trigger"] is False

assert PROC["status"]=="PREEXISTING_RESULT_RECLASSIFIED_FOR_EXPOSITION"
assert PROC["witness"]=="Behrens--Friston"
assert PROC["scientific_result"]["fine_exact_shared_bounded_object_count"]==0
assert PROC["scientific_result"]["coarse_overlap_positive"] is True
assert PROC["licensed_role"]=="PROCESS_LEVEL_SOURCE_CLAIM_REPRESENTATION_SENSITIVITY_DIAGNOSTIC_NOT_DEFEATER_TRIGGER"
assert PROC["botvinick_tulving_m25_role"]=="SAME_QUESTION_BOUNDARY_CASE_NOT_TRIGGER_EVIDENCE"
assert PROC["new_corpus_run"] is False
assert PROC["new_recoding"] is False

def fine_overlap(a,b):
    return [
        fam["archetype_id"] for fam in BOUNDED["bounded_xlike_families"]
        if a in fam["member_claim_ids"] and b in fam["member_claim_ids"]
    ]

assert fine_overlap("BLF01","PRD05")==[]
group=[
    g for g in CPCG["all_groups"]
    if "A-53b16535e1c2" in g["original_archetype_ids"]
    and "A-af97ed649c6f" in g["original_archetype_ids"]
]
assert len(group)==1
assert "BLF01" in group[0]["member_claim_ids"]
assert "PRD05" in group[0]["member_claim_ids"]
assert group[0]["signature"]["active_families"]==["N","T"]
assert group[0]["signature"]["temporal_present"] is True

assert CEX["status"]=="CONCEPTUAL_COUNTEREXAMPLE_FROZEN"
assert CEX["empirical_claim"] is False
assert CEX["systems"]["A"]["ordinary_response"]=="r[t+1] = x[t+1]"
assert CEX["systems"]["B"]["ordinary_response"]=="r[t+1] = u[t+1]"
assert CEX["criterion_C"]=="Includes the relevant update and intervention profile."

for phrase in [
    r"\title{Structural Similarity and Cognitive-Capacity Identity: A Discrimination Requirement}",
    "substantial evidential role",
    "holding the rest of the stated evidential package fixed",
    "Same question and criterion.",
    "Source-compatible.",
    "representation sensitivity is not yet a defeater trigger",
    "different legitimate questions and both be correct",
    "System A has one internal bit",
    "System B has two internal bits",
    "v_{t+1}=u_t\oplus v_t",
    "diagnostic perturbation \(P^\star\)",
    "Behrens--Friston",
    "process-level witness",
    "corpus-based evidence of representation sensitivity at the source-claim level",
    "not a Representational-Defeater Trigger",
    "past-directed subjective time",
    "analyst-imposed representation of past-directedness",
    "These aggregate collisions establish neither scientific importance nor capacity identity",
    "type-level scientific claims, not token identity claims",
]:
    assert phrase in MAIN, phrase

for phrase in [
    "Behrens--Friston: process-level representation sensitivity",
    "Source locator: Friston",
    "history window plus a time index",
    "persistence plus a time index",
    "not, by itself, a Representational-Defeater Trigger",
    "Botvinick--Tulving: a same-question boundary case",
    "representation sensitivity before the defeater-trigger stage",
]:
    assert phrase in SUPP, phrase

assert "{Friston2005CorticalResponses," in BIB
assert "10.1098/rstb.2005.1622" in BIB

for name in [
    "M25_QUESTION_RELATIVE_DEFEATER_v1.json",
    "M25_PROCESS_WITNESS_AUDIT_v1.json",
    "M25_COUNTEREXAMPLE_v1.json",
]:
    assert name in INDEX, name

for name,text in [("main",MAIN),("supplement",SUPP)]:
    assert re.search(r"\bM(?:2[0-9]|1[0-9]|[0-9])\b",text) is None, name
    assert "ClaimIR" not in text, name
    assert re.search(r"\b(?:ATT|BLF|CNC|CTL|LRN|MEM|PRD|SKL|CH)\d{2}\b",text) is None, name
    assert re.search(r"\bfrozen\b",text,re.I) is None, name

for forbidden in [
    "The pair therefore instantiates the empirical \emph{trigger condition}",
    "The changed verdict instantiates the \emph{trigger condition}",
]:
    assert forbidden not in MAIN
    assert forbidden not in SUPP

assert SPEC["scientific_authority_unchanged"]["whole_claim_pairs_incomparable"]=="1770/1770"
assert SPEC["scientific_authority_unchanged"]["bounded_objects"]==206
assert SPEC["scientific_authority_unchanged"]["cross_stratum_families"]==99
assert SPEC["scientific_authority_unchanged"]["residual_new_top_level_role"]=="0/17"

print("M25_QUESTION_RELATIVE_DEFEATER_GUARDS_PASS")
