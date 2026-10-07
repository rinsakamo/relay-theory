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

required_main = [
    "structurally supported capacity-individuation inferences",
    "same predictive-state dynamics",
    "superiority with respect to some other genuine target does not automatically transfer that warrant",
    "source-compatibility part of the live-alternative test is separate and local to the two claims",
    "exponentially weighted history",
    "source-compatible at the disputed granularity",
    "constructed calibration cases reach direct, stateless-repair, and history-bearing-repair classes",
    "mechanistic or other routes to capacity identity that do not rely on this structural promotion are not claimed to satisfy the requirement",
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
