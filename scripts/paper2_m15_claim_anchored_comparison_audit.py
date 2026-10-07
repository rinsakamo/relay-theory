#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M15 = ROOT / "research/paper2/p399/main/integration/M15"

def load(name: str):
    return json.loads((M15 / name).read_text(encoding="utf-8"))

spec = load("M15_SPEC_v1.json")
anchors = load("M15_CLAIM_ANCHORS_v1.json")
rules = load("M15_CLAIM_ANCHORED_COMPARISON_RULES_v1.json")
a = load("M15_A_EXTERNAL_FREEZE_RECEIPT_v1.json")
b = load("M15_B_EXTERNAL_FREEZE_RECEIPT_v1.json")
res = load("M15_COMPARISON_RESULTS_v1.json")
rec = load("M15_COMPARISON_RECEIPT_v1.json")
xm05 = load("M15_XM05_REFERENCE_CONFLICT_v1.json")
readme = (M15 / "README.md").read_text(encoding="utf-8")
frozen_readme = (M15 / "M15_PUBLIC_PACKET_README_FROZEN_v1.md").read_text(encoding="utf-8")

TERMINAL = "M15_CLAIM_ANCHORED_V2_COMPARISON_COMPLETE_XM05_REFERENCE_CORRECTION_REQUIRED"
ALLOWED = set(rules["classes"])

assert spec["relation_to_m14_v1"]["v2_is_independent_of_v1_results"] is False
assert spec["relation_to_m14_v1"]["v2_is_prospective_relative_to_its_own_outputs"] is True
assert len(anchors["rows"]) == 10

assert a["terminal_state"] == "M15_ASTRA_MEDIUM_CLAIM_ANCHORED_REPLAY_FROZEN_COMPARISON_NOT_PERFORMED"
assert b["terminal_state"] == "M15_GPT61_SOL_MEDIUM_CLAIM_ANCHORED_REPLAY_FROZEN_COMPARISON_NOT_PERFORMED"
assert a["freeze_receipt"]["comparison_performed"] is False
assert b["freeze_receipt"]["comparison_performed"] is False
assert a["freeze_receipt"]["complete"] == 10
assert b["freeze_receipt"]["complete"] == 10

assert b["independent_integrity_check"]["packaging_caveat"]["category"] == "NONSCIENTIFIC_GENERATED_PYTHON_BYTECODE"
assert b["independent_integrity_check"]["scientific_raw_files_present"] == 10
assert b["independent_integrity_check"]["scientific_record_files_present"] == 10
assert b["independent_integrity_check"]["present_entry_hash_mismatches"] == 0

assert res["status"] == "POSTFREEZE_COMPARISON_COMPLETE"
assert res["authority"]["input_packet_sha256"] == "edeb5aaae862dd240def175dddf87d112e6768517b33192b99e2688f8468d9c3"
assert res["authority"]["anchors_sha256"] == "989f5f7df87313e8669519d2e12af8ad9ef9d46ed4eb307a14a74a503a1e0c45"
assert res["authority"]["prompt_sha256"] == "b1100fed3a30c6e2487b6a6eb0197034980095038697617709161b2c8c8eb525"
assert res["authority"]["comparison_rules_sha256"] == "75c2e1f5d760875e72ad1f9dfc17ac421b3ba6d403bd8dcd3aebc24d3e4c605f"

assert len(res["cases"]) == 10
assert [x["case_id"] for x in res["cases"]] == [f"XM{i:02d}" for i in range(1,11)]
for c in res["cases"]:
    assert c["astra_vs_retained"] in ALLOWED
    assert c["sol_vs_retained"] in ALLOWED
    assert c["astra_vs_sol"] in ALLOWED

expected = {
    "EXACT_OR_NORMALIZED_RECOVERY": 0,
    "COMPATIBLE_ALTERNATIVE_DECOMPOSITION": 9,
    "SUBSTANTIVE_DISAGREEMENT": 1,
    "ABSTENTION_OR_UNDERDETERMINED": 0,
    "primary_compatible_fraction": "9/10",
}
assert res["aggregate"]["astra_vs_retained"] == expected
assert res["aggregate"]["sol_vs_retained"] == expected
assert res["aggregate"]["astra_vs_sol"] == {
    "EXACT_OR_NORMALIZED_RECOVERY": 0,
    "COMPATIBLE_ALTERNATIVE_DECOMPOSITION": 10,
    "SUBSTANTIVE_DISAGREEMENT": 0,
    "ABSTENTION_OR_UNDERDETERMINED": 0,
    "descriptive_compatible_fraction": "10/10",
}

sub_a=[x["case_id"] for x in res["cases"] if x["astra_vs_retained"]=="SUBSTANTIVE_DISAGREEMENT"]
sub_b=[x["case_id"] for x in res["cases"] if x["sol_vs_retained"]=="SUBSTANTIVE_DISAGREEMENT"]
assert sub_a == ["XM05"]
assert sub_b == ["XM05"]
xm05_case=[x for x in res["cases"] if x["case_id"]=="XM05"][0]
assert "ANCHOR_SOURCE_CONFLICT" in xm05_case["descriptive_flags"]
assert "RETAINED_REFERENCE_CORRECTION_REQUIRED" in xm05_case["descriptive_flags"]

assert xm05["status"] == "SOURCE_GROUNDED_REFERENCE_CONFLICT_IDENTIFIED_POSTFREEZE"
assert xm05["retained_commitment"]["node"] == "matched_initial_activity_time"
assert "20-min mapping = 25 min" in xm05["source_check"]["experiment_2"]
assert "7-min recall + 5-min reread + 7-min recall = 24 min" in xm05["source_check"]["experiment_2"]
assert xm05["frozen_comparison_effect"]["astra_vs_retained"] == "SUBSTANTIVE_DISAGREEMENT"
assert xm05["frozen_comparison_effect"]["sol_vs_retained"] == "SUBSTANTIVE_DISAGREEMENT"
assert xm05["independent_replay_behavior"]["pairwise_class"] == "COMPATIBLE_ALTERNATIVE_DECOMPOSITION"

assert rec["status"] == "COMPARISON_COMPLETE"
assert rec["terminal_state"] == TERMINAL
assert res["terminal_state"] == TERMINAL

assert res["v1_to_v2_descriptive_only"]["status"] == "NOT_AN_INDEPENDENT_CONFIRMATORY_COMPARISON_AND_NOT_A_HYPOTHESIS_TEST"
assert res["v1_to_v2_descriptive_only"]["astra_retained_compatible_or_exact"] == {"m14_v1":"1/10","m15_v2":"9/10"}
assert res["v1_to_v2_descriptive_only"]["sol_retained_compatible_or_exact"] == {"m14_v1":"3/10","m15_v2":"9/10"}

assert res["interpretation_boundary"]["independent_human_validation"] == "NOT_PERFORMED"
assert res["interpretation_boundary"]["human_inter_rater_reliability"] == "UNMEASURED"
assert res["interpretation_boundary"]["unseen_source_generalization"] == "NOT_ESTABLISHED"
assert res["interpretation_boundary"]["unique_decomposition"] == "NOT_ESTABLISHED"

assert TERMINAL in readme
assert "9/10" in readme and "10 compatible" in readme
assert "XM05 retained-reference conflict" in readme
assert "source-correction sensitivity lane" in readme

# The blind packet README remains pre-result and result-free.
assert "M15_CLAIM_ANCHORED_V2_PROTOCOL_FROZEN_REPLAYS_NOT_PERFORMED" in frozen_readme
assert "9/10" not in frozen_readme
assert "XM05 retained-reference conflict" not in frozen_readme
assert TERMINAL not in frozen_readme

print("M15_CLAIM_ANCHORED_COMPARISON_GUARDS_PASS")
