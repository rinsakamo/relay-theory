import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads(
    (ROOT / "SELF_S4_PROFILE_QUALIFICATION_HANDOFF_v1.json").read_text(
        encoding="utf-8"
    )
)

assert DATA["relayself"]["s4_pr"] == 340
assert DATA["relayself"]["s4_exact_head"] == "5cc6b1b3cdcbafe3ccdc86d96d4de54e1cc8a302"
assert DATA["qualified_profiles"] == [
    "MEM",
    "CTL",
    "CTL+SKL",
    "TALK",
    "MEM+CTL+SKL",
    "MEM+TALK",
]

positive = DATA["positive_qualification"]
assert all(value == "PASS" for value in positive.values())

negative = DATA["negative_authority_qualification"]
assert all(value == "PASS" for value in negative.values())

toggle = DATA["toggle_isolation"]
assert toggle["mem_off_talk_on"]["mem_due_work"] == "SUPPRESSED"
assert toggle["mem_off_talk_on"]["talk_due_work"] == "EXECUTED"
assert toggle["mem_off_talk_on"]["existing_memory"] == "PRESERVED"
assert toggle["mem_off_talk_on"]["open_provider_calls"] == 1
assert toggle["mem_on_talk_off"]["mem_due_work"] == "EXECUTED"
assert toggle["mem_on_talk_off"]["talk_due_work"] == "SUPPRESSED"
assert toggle["mem_on_talk_off"]["provider_calls"] == 0

ci = DATA["ci"]
assert ci["exact_head"] == DATA["relayself"]["s4_exact_head"]
for key in (
    "repository_contracts",
    "pytest",
    "lint",
    "mineflayer_adapter",
):
    assert ci[key] == "SUCCESS"

next_slice = DATA["next_slice_constraints"]
assert next_slice["slice"] == "S5"
assert next_slice["first_candidate"] == "ATT"
assert next_slice["recommended_order"][0] == "ATT"
assert next_slice["recommended_order"][-1] == "HABIT"

print("SELF_S4_HANDOFF_PASS")
