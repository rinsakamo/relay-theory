#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M22 = ROOT / "research/paper2/p399/main/integration/M22"
SPEC = json.loads((M22 / "M22_SPEC_v1.json").read_text(encoding="utf-8"))
MATRIX = json.loads((M22 / "M22_REJECT_CASE_MATRIX_v1.json").read_text(encoding="utf-8"))
REVIEW = (M22 / "M22_HOSTILE_REVIEW_JA_v1.md").read_text(encoding="utf-8")

assert SPEC["status"] == "COMPLETE"
assert SPEC["mode"] == "HOSTILE_REVIEW_ONLY_NO_MANUSCRIPT_OR_SCIENTIFIC_AUTHORITY_EDIT"
assert SPEC["exact_parent_head"] == "23ffc91c4be057d6564bf7f92944a3ea96335b61"
assert SPEC["terminal_state"] == "M22_HOSTILE_REVIEW_REJECT_CASES_FROZEN_M23_GATES_IDENTIFIED"

assert MATRIX["status"] == "FROZEN"
assert MATRIX["exact_parent_head"] == SPEC["exact_parent_head"]
assert MATRIX["editor_modal_recommendation"] == "REJECT_AND_RESUBMIT_AS_A_HIGH-POTENTIAL_REVISION"
assert MATRIX["terminal_state"] == "M22_REJECT_CASE_MATRIX_FROZEN"
assert [x["rank"] for x in MATRIX["ranking"]] == [1, 2, 3]
assert MATRIX["ranking"][0]["id"] == "R2_LIVE_RIVAL_NOT_ESTABLISHED"
assert MATRIX["ranking"][0]["severity"] == 5
assert MATRIX["ranking"][0]["fatal_if_unanswered"] is True
assert MATRIX["ranking"][1]["id"] == "R1_NOVELTY_COLLAPSE_INTO_PERSPICUITY_ROBUSTNESS"
assert MATRIX["ranking"][1]["fatal_if_unanswered"] is True
assert MATRIX["ranking"][2]["id"] == "R3_SCOPE_COMPLEXITY_AND_PROMOTION_NOT_IDENTITY"
assert MATRIX["editor_synthesis"]["no_new_large_scale_analysis_required"] is True

for phrase in [
    "live alternative",
    "source-compatible",
    "ATT03",
    "MEM04",
    "North",
    "robustness",
    "identity-evidence",
    "Reject and Resubmit",
]:
    assert phrase in REVIEW, phrase

# M22 is review-only. The journal-facing paper remains the M21 object.
assert (ROOT / "paper/venues/jgps/main.tex").exists()
assert (ROOT / "paper/venues/jgps/supplement.tex").exists()

print("M22_HOSTILE_REVIEW_GUARDS_PASS")
