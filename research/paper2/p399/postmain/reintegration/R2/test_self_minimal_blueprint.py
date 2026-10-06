import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MATRIX = json.loads((ROOT / "SELF_CAPABILITY_COMPOSITION_MATRIX_v1.json").read_text(encoding="utf-8"))
MAPPING = json.loads((ROOT / "SELF_RELAYSELF_MAPPING_v1.json").read_text(encoding="utf-8"))

assert MATRIX["authority"]["main40_A0"] == 40
assert MATRIX["authority"]["main40_A1"] == 0
assert MATRIX["authority"]["main40_A2"] == 0

interfaces = MATRIX["execution_interfaces"]
assert interfaces["state_access"]["semantic_owner"] is False
assert interfaces["state_access"]["universal_mutable_dictionary"] is False
assert interfaces["operator"]["hidden_persistent_state_allowed"] is False
assert interfaces["criterion"]["semantic_owner"] is False
assert interfaces["scheduler"]["persistent_coordinator"] is False
assert interfaces["scheduler"]["owns_goal"] is False
assert interfaces["scheduler"]["owns_belief"] is False
assert interfaces["scheduler"]["owns_intent"] is False
assert interfaces["scheduler"]["owns_world_model"] is False

capabilities = MATRIX["capabilities"]
required = {"ATT", "BLF", "CNC", "CTL", "LRN", "MEM", "PRD", "SKL", "PLAN", "HABIT", "TALK"}
assert set(capabilities) == required

for capability_id, capability in capabilities.items():
    for key in ["reads", "writes", "operators", "criteria", "ports", "triggers", "dependencies", "disable_semantics", "relayself_status"]:
        assert key in capability, (capability_id, key)
    assert capability_id not in capability["dependencies"]

profiles = MATRIX["profiles"]
assert profiles["CONVERSATIONAL_SELF"]["TALK"] is True
assert profiles["CONVERSATIONAL_SELF"]["MEM"] is True
assert profiles["REACTIVE_EMBODIED_SELF"]["CTL"] is True
assert profiles["REACTIVE_EMBODIED_SELF"]["SKL"] is True
assert profiles["REACTIVE_EMBODIED_SELF"]["LRN"] is False
assert profiles["DELIBERATIVE_EMBODIED_SELF"]["PLAN"] is True
assert profiles["ADAPTIVE_EMBODIED_SELF"]["LRN"] is True
assert profiles["ADAPTIVE_EMBODIED_SELF"]["HABIT"] is True

for profile_name, profile in profiles.items():
    assert set(profile) == required, profile_name
    for value in profile.values():
        assert isinstance(value, bool)

assert MAPPING["first_code_target"]["recommended_slice"] == "S1"
slices = MAPPING["implementation_slices"]
assert [item["id"] for item in slices] == ["S1", "S2", "S3", "S4", "S5"]
assert slices[0]["new_semantic_owner"] is False
assert slices[0]["runtime_behavior_change"] is False
assert "LRN" in slices[-1]["order"]
assert "HABIT" in slices[-1]["order"]

print("SELF_MINIMAL_BLUEPRINT_PASS")
