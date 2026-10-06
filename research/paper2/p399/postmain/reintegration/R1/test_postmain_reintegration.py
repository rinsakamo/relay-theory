import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARCH = ROOT / "POSTMAIN_REINTEGRATED_ARCHITECTURE_v1.json"

data = json.loads(ARCH.read_text(encoding="utf-8"))

auth = data["authority"]
assert auth["m7_exact_head"] == "48b2cf3c627e030e7131af485206b0013d7e02f1"
assert auth["main40_count"] == 40
assert auth["component_arm"] == 24
assert auth["integrated_arm"] == 16
assert auth["m7_A0"] == 40
assert auth["m7_A1"] == 0
assert auth["m7_A2"] == 0
assert auth["reconstruction_added_stateless_adapters"] == 0
assert auth["reconstruction_added_persistent_stateful_coordinators"] == 0
assert auth["global_genealogical_independence_claimed"] is False

substrate = data["common_execution_substrate"]
for key in [
    "typed_individuation",
    "configuration_carrier",
    "typed_transformation",
    "criterion_orientation",
    "interface",
    "succession",
    "observation_trace",
]:
    assert key in substrate

assert substrate["configuration_carrier"]["persistent_substructure_optional"] is True
assert substrate["typed_transformation"]["universal_hidden_interpreter"] is False
assert substrate["succession"]["persistent_scheduler_state_required"] is False

domains = data["domain_projections"]
assert set(domains) == {"ATT", "BLF", "CNC", "CTL", "LRN", "MEM", "PRD", "SKL"}

integrated = data["integrated_arm_result"]
assert integrated["new_common_persistent_coordinator_required"] is False
assert integrated["new_common_stateless_adapter_required"] is False
assert integrated["new_ninth_cognitive_module_supported"] is False

minimal = data["minimal_reintegrated_architecture"]
assert minimal["central_executive_required"] is False

print("POSTMAIN_REINTEGRATION_PASS 40/40")
