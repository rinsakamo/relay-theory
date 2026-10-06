import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads(
    (ROOT / "SELF_S3_EPOCH_PLAN_HANDOFF_v1.json").read_text(
        encoding="utf-8"
    )
)

assert DATA["relayself"]["s3_pr"] == 339
assert DATA["relayself"]["s3_exact_head"] == "303dbc7f6fb6e7ea8edb3ce60636079b909ac048"

scope = DATA["s3_scope"]
assert scope["new_semantic_owner_added"] is False
assert scope["persistent_scheduler_added"] is False
assert scope["dynamic_descriptor_import_added"] is False
assert scope["automatic_trigger_detection_added"] is False
assert scope["llm_per_tick_added"] is False
assert scope["capability_toggle_changes_runtime_route_availability"] is True
assert scope["disabled_due_work_is_explicitly_suppressed"] is True
assert scope["action_supervision_deadline_first_preserved"] is True
assert scope["max_cognition_calls_per_epoch"] == 1
assert scope["cognition_must_be_final_inner_step"] is True

ci = DATA["ci"]
assert ci["exact_head"] == DATA["relayself"]["s3_exact_head"]
for key in (
    "repository_contracts",
    "pytest",
    "lint",
    "mineflayer_adapter",
):
    assert ci[key] == "SUCCESS"

next_slice = DATA["next_slice_constraints"]
assert next_slice["slice"] == "S4"
assert "MEM+CTL+SKL" in next_slice["priority_profiles"]
assert "MEM+TALK" in next_slice["priority_profiles"]
assert "no persistent scheduler state" in next_slice["must_preserve"]
assert "no universal central executive" in next_slice["must_preserve"]

print("SELF_S3_HANDOFF_PASS")
