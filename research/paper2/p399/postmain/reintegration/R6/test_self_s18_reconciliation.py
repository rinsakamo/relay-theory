import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads(
    (ROOT / "S18_RELAYSELF_IMPLEMENTATION_RECONCILIATION_v1.json").read_text(
        encoding="utf-8"
    )
)

EXPECTED_STATUSES = {
    "DIRECTLY_INSTANTIATED",
    "INSTANTIATED_WITH_REFINEMENT",
    "IMPLEMENTATION_SPECIFIC_ADDITION",
    "NOT_YET_INSTANTIATED",
    "NOT_TESTED",
    "APPARENT_TENSION",
}

assert DATA["schema"] == "relaytheory.p399.postmain.relayself_s18_reconciliation.v1"

# Exact RelayTheory parent authority.
assert DATA["theory_base"]["exact_head"] == (
    "826ad01fd2caa8a6a783a1670b4255888f262c0d"
)

# Exact RelaySelf S18 subject and frozen artifacts.
s18 = DATA["relayself_s18"]
assert s18["pr"] == 354
assert s18["exact_head"] == "b5eb5d3416a9c303b855250adea4323e7611f350"
assert s18["exact_base"] == "64868337510a960c140e96d5d3d20949ad53fb8e"
assert s18["manifest_sha256"] == (
    "762e575572c2ccb70cf073006b7e18d9617fd3939d0f9f72665d41901958eec9"
)
assert s18["architecture_doc_sha256"] == (
    "33218278d69d16764db890ff4e1dde2c5eaee39213873e7438c47fbe12d56fbb"
)
assert s18["terminal_interpretation"] == (
    "S18_FROZEN_AS_SINGLE_TRANSACTION_COGNITIVE_ACTION_LEARNING_"
    "ARCHITECTURE_WITH_EXPLICIT_OWNERSHIP_AND_AUTHORITY_BOUNDARIES"
)

# MAIN40 is imported as frozen authority and cannot be rewritten by reconciliation.
main = DATA["frozen_main_result"]
assert main["main40"] == 40
assert main["component_arm"] == {"count": 24, "A0": 24}
assert main["integrated_arm"] == {"count": 16, "A0": 16}
assert (main["A0"], main["A1"], main["A2"]) == (40, 0, 0)
assert main["reconstruction_added_stateless_adapters"] == 0
assert main["reconstruction_added_persistent_stateful_coordinators"] == 0
assert main["modified_by_this_reconciliation"] is False

# A0/A1/A2 interpretation must not retroactively convert software interfaces
# into MAIN scientific A1 cases.
a_state = DATA["a0_a1_a2_interpretation"]
assert a_state["main_result_remains"] == (
    "A0=40, A1=0, A2=0; integrated arm 16/16 A0."
)
assert a_state["retroactive_reclassification"] is False
assert "not MAIN A1 cases" in a_state["engineering_interpretation"]

# Declared reconciliation status vocabulary is closed.
assert set(DATA["declared_status_enum"]) == EXPECTED_STATUSES
rows = DATA["correspondence_table"]
assert len(rows) == 22
assert all(row["status"] in EXPECTED_STATUSES for row in rows)

counts = DATA["correspondence_counts"]
assert counts == {
    "DIRECTLY_INSTANTIATED": 8,
    "INSTANTIATED_WITH_REFINEMENT": 6,
    "IMPLEMENTATION_SPECIFIC_ADDITION": 4,
    "NOT_YET_INSTANTIATED": 3,
    "NOT_TESTED": 1,
    "APPARENT_TENSION": 0,
}

# Exact implementation-specific refinements are kept out of MAIN empirical status.
by_id = {row["id"]: row for row in rows}
for row_id in ("R13", "R14", "R17", "R18"):
    assert by_id[row_id]["status"] == "IMPLEMENTATION_SPECIFIC_ADDITION"

assert "Do not attribute the exact ladder to MAIN40 empirical adjudication." == by_id["R13"]["limitation"]
assert "MAIN remains 40/0/0" in by_id["R14"]["limitation"]
assert "not all corpus measurements" in by_id["R17"]["limitation"]
assert "RelaySelf as a whole is not model-free" in by_id["R18"]["limitation"]

# Bounded central-executive conclusion.
coord = DATA["coordinator_conclusion"]
assert coord["statement"] == (
    "The RelaySelf S1-S18 implementation demonstrates that the frozen "
    "single-transaction cognitive-action-learning architecture can be "
    "constructed without introducing a persistent central executive or a "
    "persistent cognitive scheduler."
)
assert coord["bound"] == (
    "This is an implementation existence result for the present architecture, "
    "not a universal impossibility result for centralized coordination."
)

# Live field remains blocked/not-run exactly.
live = DATA["live_field_limitation"]
assert live["status"] == "BLOCKED_NOT_RUN"
assert live["blocker"] == "genuine Minecraft endpoint unavailable"
assert live["allowed_wording"] == "deterministic implementation-apparatus qualification"
assert "empirical field validation" in live["forbidden_claims"]

# Autonomous reentry remains absent.
autonomy = DATA["autonomy_limitation"]
assert autonomy["autonomous_reentry"] == "NOT_IMPLEMENTED"
assert autonomy["continuous_multi_epoch_operation"] == "NOT_QUALIFIED"
assert autonomy["demonstrated_scope"] == "one bounded transaction"

# No automatic LRN -> ATT edge.
graph = DATA["canonical_correspondence_graph"]
assert graph["forbidden_reentry"] == {
    "from": "LearningPreferenceState",
    "to": "ATT",
    "kind": "NO_AUTOMATIC_EDGE",
}

# Negative-edge classifications are closed to the three intended categories.
negative_classes = {
    item["classification"] for item in DATA["negative_edge_assessment"]
}
assert negative_classes <= {
    "DIRECTLY_IMPLIED_BY_POSTMAIN_STRUCTURAL_SEPARATION",
    "ENGINEERING_REFINEMENT",
    "FUTURE_EMPIRICAL_OR_RUNTIME_QUESTION",
}
assert len(DATA["negative_edge_assessment"]) == 17

# Paper3 observations remain hypotheses rather than results.
for item in DATA["paper3_implications"]:
    assert item["epistemic_status"] == "IMPLEMENTATION_GENERATED_HYPOTHESIS"

assert DATA["unresolved_tensions"] == []
assert DATA["terminal_interpretation"] == (
    "POSTMAIN_SELF_S18_RECONCILED_WITH_PAPER2_STRUCTURAL_ARCHITECTURE_"
    "WITH_IMPLEMENTATION_SPECIFIC_AUTHORITY_REFINEMENTS"
)

print("SELF_S18_RECONCILIATION_PASS")
