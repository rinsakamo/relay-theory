import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[6]
M9A = ROOT / "research/paper2/p399/main/integration/M9A"
BENCH = json.loads((M9A / "M9A_MATCHED_LIFT_BENCHMARK_v1.json").read_text())

checks = []
def check(name, cond):
    if not cond:
        raise AssertionError(name)
    checks.append(name)

check("schema", BENCH["schema"] == "relaytheory.p399.main.m9a.matched_lift_benchmark.v1")
check("base_head", BENCH["base_head"] == "3e0c82fb090bc0fc2f66ed3c4e65df282779f4eb")
check("tower_order", list(BENCH["reconstruction_tower"]["least_lift_rule"]) == ["A0", "A1", "A2"])

cases = BENCH["matched_cases"]
check("six_cases", len(cases) == 6)
ids = [c["case_id"] for c in cases]
check("case_ids_unique", len(ids) == len(set(ids)))
expected = Counter(c["expected"] for c in cases)
families = Counter(c["family"] for c in cases)
check("balanced_A_states", expected == Counter({"A0": 2, "A1": 2, "A2": 2}))
check("balanced_families", families == Counter({"DYNAMIC": 3, "POMDP_LIKE": 3}))

for c in cases:
    if c["expected"] == "A0":
        check(f"{c['case_id']}_a0_no_added",
              not c["reconstruction_added_stateless"] and
              not c["reconstruction_added_persistent"])
    elif c["expected"] == "A1":
        check(f"{c['case_id']}_a1_stateless_only",
              c["reconstruction_added_stateless"] and
              not c["reconstruction_added_persistent"])
        check(f"{c['case_id']}_a1_failure_witness", bool(c.get("A0_failure_witness")))
    elif c["expected"] == "A2":
        check(f"{c['case_id']}_a2_persistent",
              not c["reconstruction_added_stateless"] and
              c["reconstruction_added_persistent"])
        check(f"{c['case_id']}_a2_failure_witness", bool(c.get("A1_failure_witness")))

comp = BENCH["frozen_comparator_constraints"]
check("gdyn_59", comp["G_dyn"]["claims_requiring_at_least_one_role_beyond"] == 59)
check("gdyn_zero_full", comp["G_dyn"]["strict_full_direct_preservation_count"] == 0)
check("gpom_44", comp["G_pomdp_like"]["claims_hit_by_missing_Pi_or_C_or_collapsed_P_direction"] == 44)
check("gpom_missing_pi_c", comp["G_pomdp_like"]["missing_first_class_roles"] == ["Pi", "C"])

# Cross-check copied receipts against frozen source artifacts.
COMP_SRC = json.loads((ROOT / "research/paper2/grammar_v0_minimality_comparator_v1.json").read_text())
check("source_gdyn_59",
      COMP_SRC["comparator_G_dyn"]["claims_requiring_at_least_one_role_beyond_G_dyn"] == 59)
check("source_gdyn_zero_full",
      COMP_SRC["comparator_G_dyn"]["strict_full_direct_preservation_count"] == 0)
check("source_gpom_44",
      COMP_SRC["comparator_G_pomdp_like"]["union_claims_affected_by_missing_Pi_or_C_or_collapsed_P_direction"] == 44)
check("source_gpom_missing_pi_c",
      COMP_SRC["comparator_G_pomdp_like"]["missing_first_class_roles"] == ["Pi", "C"])

M7_SCI = json.loads((ROOT / "research/paper2/p399/main/integration/M7/M7_MAIN_SCIENTIFIC_ADJUDICATION_v1.json").read_text())
m7c = M7_SCI["m7_accepted_state_counts"]
check("source_m7_40_0_0",
      (m7c["A0_FIDELITY"], m7c["A1_FIDELITY"], m7c["A2_FIDELITY"]) == (40, 0, 0))
check("source_m7_denominator_40", M7_SCI["exact_main_denominator"] == 40)

M7_A1 = json.loads((ROOT / "research/paper2/p399/main/integration/M7/M7_A1_INTERFACE_ADVERSE_AUDIT_v1.json").read_text())
M7_A2 = json.loads((ROOT / "research/paper2/p399/main/integration/M7/M7_A2_STATEFUL_MECHANISM_ADVERSE_AUDIT_v1.json").read_text())
check("source_m7_a1_zero", M7_A1["case_count"] == 0 and M7_A1["H1_positive_evidence_count"] == 0)
check("source_m7_a2_zero", M7_A2["case_count"] == 0 and M7_A2["H2_positive_evidence_count"] == 0)

m7 = BENCH["m7_result_preserved"]
check("m7_counts_preserved",
      (m7["MAIN40_A0"], m7["MAIN40_A1"], m7["MAIN40_A2"]) == (40, 0, 0))
check("m9a_no_readjudication", m7["re_adjudicated_by_m9a"] is False)

formal = (ROOT / "formal/relay_theory/RelayTheory/ReconstructionLiftHierarchy.lean").read_text()
for theorem in [
    "least_lift_exhaustive",
    "six_case_reachability",
    "a1_port_not_direct",
    "a1_port_stateless_adapter_exists",
    "no_stateless_history_realizer",
    "stateful_history_realizer_exists",
    "toDynView_viaPomdp_transition_iff",
]:
    check(f"formal_{theorem}", f"theorem {theorem}" in formal)

report = (M9A / "M9A_CATEGORICAL_LIFT_FOUNDATION_v1.md").read_text()
for phrase in [
    "least-lift well-definedness",
    "source-defined persistent state is compatible with A0",
    "too forgetful",
    "not a non-encodability theorem",
    "independent human re-adjudication",
]:
    check(f"report_{phrase}", phrase in report)

print(f"M9A_CATEGORICAL_LIFT_PASS {len(checks)}/{len(checks)}")
