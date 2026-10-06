#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M14 = ROOT / "research/paper2/p399/main/integration/M14"
M15 = ROOT / "research/paper2/p399/main/integration/M15"

def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

spec = load(M15 / "M15_SPEC_v1.json")
anchors = load(M15 / "M15_CLAIM_ANCHORS_v1.json")
protocol = load(M15 / "M15_CLAIM_ANCHORED_REPLAY_PROTOCOL_v1.json")
blank = load(M15 / "M15_CLAIM_ANCHORED_BLANK_RECORD_v1.json")
rules = load(M15 / "M15_CLAIM_ANCHORED_COMPARISON_RULES_v1.json")
runplan = load(M15 / "M15_RUN_PLAN_v1.json")
pref = load(M15 / "M15_PREFREEZE_RECEIPT_v1.json")
m14_manifest = load(M14 / "M14_CROSS_MODEL_INPUT_MANIFEST_v1.json")
frozen_readme = (M15 / "M15_PUBLIC_PACKET_README_FROZEN_v1.md").read_text(encoding="utf-8")
prompt = (M15 / "M15_CLAIM_ANCHORED_PROMPT_v1.md").read_text(encoding="utf-8")

PARENT = "6662e2760fff259f55455d17a225fd5527921f8f"
TERMINAL = "M15_CLAIM_ANCHORED_V2_PROTOCOL_FROZEN_REPLAYS_NOT_PERFORMED"

assert spec["status"] == "PREFROZEN_BEFORE_ANY_M15_REPLAY_OUTPUT"
assert spec["authority"]["exact_parent_head"] == PARENT
assert pref["exact_parent_head"] == PARENT
assert pref["m15_results_at_freeze"] == "NOT_PERFORMED"
assert spec["target_state"] == TERMINAL
assert spec["relation_to_m14_v1"]["v2_is_repair_followup"] is True
assert spec["relation_to_m14_v1"]["v2_is_independent_of_v1_results"] is False
assert spec["relation_to_m14_v1"]["v2_is_prospective_relative_to_its_own_outputs"] is True
assert spec["relation_to_m14_v1"]["same_sources"] is True

rows = anchors["rows"]
assert anchors["status"] == "FROZEN_BEFORE_ANY_M15_REPLAY_OUTPUT"
assert len(rows) == 10
assert [r["case_id"] for r in rows] == [f"XM{i:02d}" for i in range(1,11)]
assert [(r["slot_id"], r["doi"]) for r in rows] == [
    (r["slot_id"], r["doi"]) for r in m14_manifest["rows"]
]

for r in rows:
    assert set(r) == {"case_id","slot_id","doi","source_locators","anchor_proposition"}
    assert r["source_locators"]
    assert len(r["anchor_proposition"].split()) >= 12
    text = json.dumps(r, ensure_ascii=False)
    for forbidden in [
        "retained_claim_id", "claim_id", "coordinate_map", "bounded_object",
        "A0", "A1", "A2", "EXACT_OR_NORMALIZED_RECOVERY",
        "COMPATIBLE_ALTERNATIVE_DECOMPOSITION", "SUBSTANTIVE_DISAGREEMENT",
        "ABSTENTION_OR_UNDERDETERMINED", "M14_REPLAY_COMPARISON"
    ]:
        assert forbidden not in text, (r["case_id"], forbidden)
    assert re.search(r"\bA-[0-9a-f]{8,}\b", text) is None
    for role_token in ["P_in","P_out","rho/O","resource_C"]:
        assert role_token not in text, (r["case_id"], role_token)

assert protocol["status"] == "PROTOCOL_FROZEN_M15_REPLAYS_NOT_PERFORMED"
assert protocol["result"] == "NOT_PERFORMED"
assert "Treat the supplied anchor as the target claim" in protocol["execution_rules"]
assert "Execute the two named-model runs in separate fresh conversations and do not pass run A outputs to run B." in protocol["execution_rules"]

assert blank["uncertainty"]["status"] == "COMPLETE|ABSTAIN|UNDERDETERMINED"
assert blank["anchor"]["target_status"] == "USED_AS_GIVEN|ABSTAIN|UNDERDETERMINED"

assert rules["status"] == "FROZEN_BEFORE_ANY_M15_REPLAY_OUTPUT"
assert list(rules["classes"]) == [
    "EXACT_OR_NORMALIZED_RECOVERY",
    "COMPATIBLE_ALTERNATIVE_DECOMPOSITION",
    "SUBSTANTIVE_DISAGREEMENT",
    "ABSTENTION_OR_UNDERDETERMINED",
]
assert rules["summaries"]["primary"] == "(EXACT_OR_NORMALIZED_RECOVERY + COMPATIBLE_ALTERNATIVE_DECOMPOSITION) / 10"
assert rules["summaries"]["pairwise_replay_A_vs_B"].startswith("apply the same four classes")

assert [x["product_level_configuration"] for x in runplan["order"]] == [
    "GPT-6 Astra / Medium",
    "GPT-6.1 Sol / Medium",
]
assert runplan["comparison_authorization"].startswith("Only after both M15-A and M15-B are frozen")

for phrase in [
    "The focal claim has already been fixed",
    "Do not replace it with another interesting, nearby, broader, or narrower claim",
    "The anchor identifies **which scientific claim** to reconstruct",
    "ABSTAIN",
    "UNDERDETERMINED",
    "Complete and freeze all ten cases for this model configuration",
]:
    assert phrase in prompt, phrase

assert TERMINAL in frozen_readme
assert "No M15 replay or comparison result exists at this freeze." in frozen_readme
for forbidden in [
    "M15_ASTRA_MEDIUM_CLAIM_ANCHORED_REPLAY_FROZEN",
    "M15_GPT61_SOL_MEDIUM_CLAIM_ANCHORED_REPLAY_FROZEN",
    "comparison result:",
    "EXACT 0",
    "SUBSTANTIVE 8",
]:
    assert forbidden not in frozen_readme

# No result-bearing M15 files are allowed at prefreeze.
for p in M15.iterdir():
    upper = p.name.upper()
    assert "RESULT" not in upper
    assert "OUTPUT" not in upper
    assert "COMPARISON_RECEIPT" not in upper

print("M15_CLAIM_ANCHORED_PREFREEZE_GUARDS_PASS")
