#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M23 = ROOT / "research/paper2/p399/main/integration/M23"
MAIN = (ROOT / "paper/venues/jgps/main.tex").read_text(encoding="utf-8")
SUPP = (ROOT / "paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
INDEX = (ROOT / "paper/venues/jgps/supplementary-materials-index.md").read_text(encoding="utf-8")

SPEC = json.loads((M23 / "M23_SPEC_v1.json").read_text(encoding="utf-8"))
BT = json.loads((M23 / "M23_BT_SOURCE_COMPATIBILITY_AUDIT_v1.json").read_text(encoding="utf-8"))
NORTH = json.loads((M23 / "M23_NORTH_RESISTANT_COUNTEREXAMPLE_v1.json").read_text(encoding="utf-8"))

assert SPEC["status"] == "COMPLETE"
assert SPEC["exact_parent_m22_head"] == "a25339a42306c134fcda159a7b6d80fb858c19bd"
assert all(v["status"] == "CLOSED" for v in SPEC["gates"].values())
assert SPEC["terminal_state"] == "M23_HOSTILE_REJECT_GATES_CLOSED_LIVE_RIVAL_SOURCE_COMPATIBILITY_EXPLICIT"

assert BT["status"] == "SOURCE_LOCAL_LIVE_RIVAL_AUDIT_COMPLETE"
assert BT["treur_role"]["licensed_role"] == "INDEPENDENT_SCIENTIFIC_MOTIVATION_ONLY"
assert BT["live_alternative_test"]["independently_scientifically_motivated"] is True
assert BT["live_alternative_test"]["source_compatible_at_disputed_weak_granularity"] is True
assert BT["live_alternative_test"]["changes_identity_relevant_overlap_verdict"] is True
assert BT["live_alternative_test"]["unique_or_globally_best_representation_claimed"] is False
assert [c["source_compatibility_verdict"] for c in BT["cases"]] == [
    "PASS_AT_WEAK_TEMPORAL_GRANULARITY",
    "PASS_AT_WEAK_TEMPORAL_GRANULARITY",
]

assert NORTH["status"] == "COUNTEREXAMPLE_FROZEN"
assert "superior for the predictive target" in NORTH["construction"]["granted_scientific_superiority"]
assert "suppressed update mechanism" in NORTH["construction"]["missing_identity_warrant"]

M27_PATH=ROOT/"research/paper2/p399/main/integration/M27/M27_SPEC_v1.json"
if M27_PATH.exists():
    M27=json.loads(M27_PATH.read_text(encoding="utf-8"))
    MATCH=json.loads((ROOT/"research/paper2/p399/main/integration/M27/M27_MATCHED_CASES_v1.json").read_text(encoding="utf-8"))
    assert M27["terminal_state"]=="M27_REPRESENTATION_PROVENANCE_AND_MATCHED_DISCRIMINATION_CLARIFIED"
    assert MATCH["missing_data"] is False
    assert MATCH["unperformed_intervention"] is False
    assert MATCH["maps"]["phi_cross"]["C_crossing"] is True
    for phrase in [
        "matched comparison",
        "same identity question",
        "Behrens--Friston",
        "past-directed subjective time",
        "Activated Representational-Defeater Trigger",
    ]:
        assert phrase in MAIN, phrase
    assert "Botvinick--Tulving: a same-question boundary case" in SUPP
    print("M23_HOSTILE_REJECT_CLOSURE_GUARDS_PASS_VIA_M27_SUCCESSOR")
    raise SystemExit(0)

M26_PATH=ROOT/"research/paper2/p399/main/integration/M26/M26_SPEC_v1.json"
if M26_PATH.exists():
    M26=json.loads(M26_PATH.read_text(encoding="utf-8"))
    CEX=json.loads((ROOT/"research/paper2/p399/main/integration/M26/M26_UNDERCUTTING_COUNTEREXAMPLE_v1.json").read_text(encoding="utf-8"))
    assert M26["terminal_state"]=="M26_ACTIVATED_UNDERCUTTING_AND_GENERAL_PROVENANCE_SEPARATED"
    assert CEX["intervention_family_J"]["performed"] is False
    assert CEX["inferential_status"]["H_id"]=="OPEN"
    for phrase in [
        "same identity question",
        "substantial role",
        "externally manipulable binary channel",
        "has not been performed",
        "Behrens--Friston",
        "past-directed subjective time",
    ]:
        assert phrase in MAIN, phrase
    assert "Botvinick--Tulving: a same-question boundary case" in SUPP
    print("M23_HOSTILE_REJECT_CLOSURE_GUARDS_PASS_VIA_M26_SUCCESSOR")
    raise SystemExit(0)

M25_PATH=ROOT/"research/paper2/p399/main/integration/M25/M25_SPEC_v1.json"
if M25_PATH.exists():
    M25=json.loads(M25_PATH.read_text(encoding="utf-8"))
    PROC=json.loads((ROOT/"research/paper2/p399/main/integration/M25/M25_PROCESS_WITNESS_AUDIT_v1.json").read_text(encoding="utf-8"))
    assert M25["terminal_state"]=="M25_QUESTION_RELATIVE_DEFEATER_AND_PROCESS_WITNESS_CLARIFIED"
    assert PROC["botvinick_tulving_m25_role"]=="SAME_QUESTION_BOUNDARY_CASE_NOT_TRIGGER_EVIDENCE"
    for phrase in [
        "same identity question",
        "substantial role",
        "System A has one internal bit",
        "System B has two internal bits",
        "Behrens--Friston",
        "past-directed subjective time",
    ]:
        assert phrase in MAIN, phrase
    assert "Botvinick--Tulving: a same-question boundary case" in SUPP
    print("M23_HOSTILE_REJECT_CLOSURE_GUARDS_PASS_VIA_M25_SUCCESSOR")
    raise SystemExit(0)

required_main = [
    "structurally supported capacity-individuation inferences",
    "same predictive-state dynamics",
    "superiority with respect to some other genuine target does not automatically transfer that warrant",
    "source-compatibility part of the live-alternative test is separate and local to the two claims",
    "exponentially weighted history",
    "source-compatible at the disputed granularity",
    "constructed calibration cases reach direct, stateless-repair, and history-bearing-repair classes",
    "Mechanistic or other routes to capacity identity that do not rely on this structural promotion are not claimed to satisfy the requirement",
]
for phrase in required_main:
    assert phrase in MAIN, phrase

for forbidden in [
    "The paper offers a necessary evidential condition on capacity individuation,",
    "It establishes something weaker but sufficient for a live alternative",
]:
    assert forbidden not in MAIN, forbidden

required_supp = [
    "A Discrimination Requirement for Structural Approaches to Cognitive-Capacity Individuation",
    "Source-local provenance of the temporal rival",
    "The central pair is not licensed by Treur alone",
    "does each reviewed claim contain cross-time state dependence?",
    "faithful quotient of the reviewed representations",
]
for phrase in required_supp:
    assert phrase in SUPP, phrase

assert "M23_BT_SOURCE_COMPATIBILITY_AUDIT_v1.json" in INDEX

# Freeze referenced source records and reconstruction authorities as existing files.
for case in BT["cases"]:
    assert (ROOT / case["claim_ir"]).is_file()
    assert (ROOT / case["structural_adjudication"]).is_file()
    assert (ROOT / case["bounded_membership_authority"]).is_file()

print("M23_HOSTILE_REJECT_CLOSURE_GUARDS_PASS")
