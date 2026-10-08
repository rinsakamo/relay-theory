#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
M24=ROOT/"research/paper2/p399/main/integration/M24"
MAIN=(ROOT/"paper/venues/jgps/main.tex").read_text(encoding="utf-8")
SUPP=(ROOT/"paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
INDEX=(ROOT/"paper/venues/jgps/supplementary-materials-index.md").read_text(encoding="utf-8")

SPEC=json.loads((M24/"M24_SPEC_v1.json").read_text(encoding="utf-8"))
SCOPE=json.loads((M24/"M24_DEFEATER_SCOPE_v1.json").read_text(encoding="utf-8"))
BT=json.loads((M24/"M24_BT_TRIGGER_RECLASSIFICATION_v1.json").read_text(encoding="utf-8"))
TUL=json.loads((M24/"M24_TULVING_ENCODING_BOUNDARY_v1.json").read_text(encoding="utf-8"))
BENI=json.loads((M24/"M24_BENI_STRONG_REPLY_v1.json").read_text(encoding="utf-8"))

assert SPEC["status"]=="COMPLETE"
assert SPEC["exact_parent_m23_head"]=="08366e1171710cf4e363510016a503f64f6b6419"
assert all(v["status"]=="CLOSED" for v in SPEC["gates"].values())
assert SPEC["no_new_large_scale_analysis"] is True
assert SPEC["no_new_human_coding"] is True
assert SPEC["terminal_state"]=="M24_DEFEATER_SCOPE_EVIDENTIAL_WEIGHT_AND_TRIGGER_ROLE_CLARIFIED"

assert SCOPE["status"]=="FROZEN"
assert SCOPE["central_distinctions"]["defeater_type"]=="UNDERCUTTING_NOT_REBUTTING"
assert SCOPE["terminal_state"]=="M24_DEFEATER_TRIGGER_AND_UNDERCUTTING_SCOPE_FROZEN"

assert BT["status"]=="FROZEN"
assert BT["m24_role"]=="EMPIRICAL_REPRESENTATIONAL_DEFEATER_TRIGGER_WITNESS"
assert BT["scientific_overlap_result_unchanged"]["fine_overlap_positive"] is False
assert BT["scientific_overlap_result_unchanged"]["coarse_overlap_positive"] is True
assert BT["terminal_state"]=="M24_BT_RECLASSIFIED_AS_TRIGGER_NOT_FULL_DEFEATER"

assert TUL["status"]=="FROZEN"
assert TUL["representation_level_encoding"]["status"]=="ANALYTIC_ENCODING_IN_WORKING_COMPARISON_REPRESENTATION"
assert "literal computational history buffer" in TUL["representation_level_encoding"]["not_attributed_to_source"]

assert BENI["status"]=="PUBLISHER_HTML_REVERIFIED"
assert BENI["verified_date"]=="2026-10-08"
assert BENI["source"]["doi"]=="10.1007/s10838-025-09759-z"

M25_PATH=ROOT/"research/paper2/p399/main/integration/M25/M25_SPEC_v1.json"
if M25_PATH.exists():
    M25=json.loads(M25_PATH.read_text(encoding="utf-8"))
    QREL=json.loads((ROOT/"research/paper2/p399/main/integration/M25/M25_QUESTION_RELATIVE_DEFEATER_v1.json").read_text(encoding="utf-8"))
    PROC=json.loads((ROOT/"research/paper2/p399/main/integration/M25/M25_PROCESS_WITNESS_AUDIT_v1.json").read_text(encoding="utf-8"))
    assert M25["terminal_state"]=="M25_QUESTION_RELATIVE_DEFEATER_AND_PROCESS_WITNESS_CLARIFIED"
    assert QREL["defeater_type"]=="UNDERCUTTING_NOT_REBUTTING"
    assert QREL["trigger"]["same_Q_required"] is True
    assert QREL["trigger"]["same_C_required"] is True
    assert PROC["botvinick_tulving_m25_role"]=="SAME_QUESTION_BOUNDARY_CASE_NOT_TRIGGER_EVIDENCE"
    for phrase in [
        "substantial evidential role",
        "Representational-Defeater Trigger",
        "Same question and criterion.",
        "Behrens--Friston",
        "analyst-imposed representation of past-directedness",
    ]:
        assert phrase in MAIN, phrase
    print("M24_DEFEATER_SCOPE_EVIDENTIAL_WEIGHT_GUARDS_PASS_VIA_M25_SUCCESSOR")
    raise SystemExit(0)

for phrase in [
    "material evidential weight",
    "individuative evidential weight",
    "not evidential relevance simpliciter",
    "Representational-Defeater Trigger",
    "The defeater is therefore \\emph{undercutting}, not rebutting",
    "does not entitle that invariant to carry the identity inference",
    "weak support can remain weak support".capitalize(),
    "R_{\\mathrm{pred}}",
    "R_{\\mathrm{mech}}",
    "empirical natural-kind constraints can themselves discharge the Discrimination Requirement",
    "natural-kind reasoning the empirical criteria and clustered content",
    "inferential rather than ontological",
    "working reconstruction encodes that source-grounded commitment as a history-window plus time-index witness",
    "not a claim that Tulving literally posits a computational history buffer",
    "Here \\(S\\) marks state-like carriers",
    "\\phi_{\\mathrm{coarse}}",
    "not itself presented as a fully instantiated Representational Defeater",
]:
    assert phrase in MAIN, phrase

for phrase in [
    "trigger condition",
    "does not itself defeat a Botvinick--Tulving identity inference",
    "analysis-level encoding choice",
    "not presented as Tulving's own computational primitive",
    "history window",
]:
    assert phrase in SUPP, phrase

for forbidden in [
    "the pair instantiates the Representational Defeater",
    "The changed verdict instantiates the Representational Defeater",
]:
    assert forbidden not in MAIN
    assert forbidden not in SUPP

for name in [
    "M24_DEFEATER_SCOPE_v1.json",
    "M24_BT_TRIGGER_RECLASSIFICATION_v1.json",
    "M24_TULVING_ENCODING_BOUNDARY_v1.json",
    "M24_BENI_STRONG_REPLY_v1.json",
]:
    assert name in INDEX, name

# Frozen scientific headline values remain unchanged.
assert SPEC["scientific_authority_unchanged"]["whole_claim_pairs_incomparable"]=="1770/1770"
assert SPEC["scientific_authority_unchanged"]["bounded_objects"]==206
assert SPEC["scientific_authority_unchanged"]["cross_stratum_families"]==99
assert SPEC["scientific_authority_unchanged"]["residual_new_top_level_role"]=="0/17"

print("M24_DEFEATER_SCOPE_EVIDENTIAL_WEIGHT_GUARDS_PASS")
