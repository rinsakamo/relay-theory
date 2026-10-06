import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads(
    (ROOT / "SELF_S2_EXECUTION_DESCRIPTOR_HANDOFF_v1.json").read_text(
        encoding="utf-8"
    )
)

assert DATA["relayself"]["s2_pr"] == 338
assert DATA["relayself"]["s2_exact_head"] == "40b83d9012dc1bcc8e1dc2c74664a7d0e0ffb172"

scope = DATA["s2_scope"]
assert scope["capabilities"] == ["MEM", "CTL", "SKL", "TALK"]
assert scope["runtime_dispatch_added"] is False
assert scope["new_semantic_owner_added"] is False
assert scope["hidden_persistent_operator_state_allowed"] is False
assert scope["criterion_state_mutation_allowed"] is False
assert scope["all_current_criteria_kind"] == "CONTRACT_GUARD"

ci = DATA["ci"]
assert ci["exact_head"] == DATA["relayself"]["s2_exact_head"]
assert ci["repository_contracts"] == "SUCCESS"
assert ci["pytest"] == "SUCCESS"
assert ci["lint"] == "SUCCESS"

constraints = DATA["next_slice_constraints"]
assert constraints["slice"] == "S3"
assert "no persistent scheduler state" in constraints["must_preserve"]
assert "no LLM-per-tick loop" in constraints["must_preserve"]

print("SELF_S2_HANDOFF_PASS")
