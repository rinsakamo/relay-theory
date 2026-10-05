import json
from pathlib import Path
from collections import Counter
from datetime import datetime

ROOT = Path(__file__).resolve().parents[6]
M9B = ROOT / "research/paper2/p399/main/integration/M9B"

checks = []
def check(name, cond):
    if not cond:
        raise AssertionError(name)
    checks.append(name)

evidence = json.loads((M9B / "M9B_MAIN40_PAPER_LEVEL_EVIDENCE_v1.json").read_text())
decision = json.loads((M9B / "M9B_A012_OPERATIONAL_DECISION_TREE_v1.json").read_text())
chronology = json.loads((M9B / "M9B_FREEZE_CHRONOLOGY_v1.json").read_text())
boundary = (M9B / "M9B_SINGLE_ADJUDICATOR_BOUNDARY_v1.md").read_text()
manuscript = (ROOT / "paper/venues/jgps/main.tex").read_text()
m7 = json.loads((ROOT / "research/paper2/p399/main/integration/M7/M7_40_PAPER_ARCHITECTURAL_MATRIX_v1.json").read_text())

check("evidence_schema", evidence["schema"] == "relaytheory.p399.main.m9b.paper_level_adjudication_evidence.v1")
check("denominator_40", evidence["denominator"] == 40)
check("rows_40", len(evidence["rows"]) == 40)
check("unique_papers", len({r["paper_id"] for r in evidence["rows"]}) == 40)
check("unique_doi", len({r["doi"] for r in evidence["rows"]}) == 40)

counts = Counter(r["final_state"] for r in evidence["rows"])
check("m9b_40_0_0", counts == Counter({"A0_FIDELITY": 40}))
check("m7_40_0_0", Counter(r["m7_adjudicated_final_A_state"] for r in m7["rows"]) == Counter({"A0_FIDELITY": 40}))
check("same_roster", {(r["paper_id"], r["doi"]) for r in evidence["rows"]} == {(r["slot"], r["doi"]) for r in m7["rows"]})

for r in evidence["rows"]:
    check(f"{r['paper_id']}_no_a1_addition", r["added_stateless_adapter_count"] == 0)
    check(f"{r['paper_id']}_no_a2_addition", r["added_stateful_mechanism_count"] == 0)
    check(f"{r['paper_id']}_no_persistent_added", r["reconstruction_added_persistent_state"] is False)
    check(f"{r['paper_id']}_outcome_path", r["evidence"]["architectural_outcome_path"].endswith("/ARCHITECTURAL_OUTCOME_v1.json"))
    check(f"{r['paper_id']}_source_loci_path", r["evidence"]["source_loci_artifact_path"].endswith("/PASS_A_SOURCE_FIRST_DECOMPOSITION_v1.json"))
    check(f"{r['paper_id']}_single_adjudicator", r["independent_human_readjudication"] == "NOT_PERFORMED")
    check(f"{r['paper_id']}_no_independence_assumption", "independence" in r["genealogy_risk_annotation"].lower() or "genealogy" in r["genealogy_risk_annotation"].lower())

ih = evidence["independent_human_readjudication"]
check("human_not_performed", ih["performed"] is False)
check("human_not_claimed", ih["claim"] == "NOT_CLAIMED")

nodes = {n["id"]: n for n in decision["nodes"]}
check("decision_nodes", set(nodes) == {"E0", "E1", "A0", "A1", "A2", "NL"})
check("a0_yes", nodes["A0"]["yes"] == "A0_FIDELITY")
check("a1_yes", nodes["A1"]["yes"] == "A1_FIDELITY")
check("a2_yes", nodes["A2"]["yes"] == "A2_FIDELITY")
check("failure_branch", nodes["NL"]["yes"] == "FAILURE_LOCALIZED")
check("ud_branch", nodes["NL"]["no"] == "UNDERDETERMINED")
check("guard_source_defined", any("source-defined state" in g for g in decision["guardrails"]))
check("guard_failure_not_a2", any("failure alone" in g for g in decision["guardrails"]))

events = {x["event"]: x for x in chronology["commits"]}
def dt(event):
    return datetime.fromisoformat(events[event]["timestamp_utc"].replace("Z", "+00:00"))

check("method_before_kickoff", dt("RIR_v2_3_1_method_reference") < dt("MAIN_kickoff_and_A_state_boundary"))
check("criterion_before_kickoff", dt("genealogy_criterion_freeze") < dt("MAIN_kickoff_and_A_state_boundary"))
check("w9_before_kickoff", dt("W9_final_closure") < dt("MAIN_kickoff_and_A_state_boundary"))
for lane in ["M1_final","M2_final","M3_final","M4_final","M5_final","M6_final"]:
    check(f"{lane}_after_kickoff", dt("MAIN_kickoff_and_A_state_boundary") < dt(lane))
check("m7_after_all_lanes", max(dt(x) for x in ["M1_final","M2_final","M3_final","M4_final","M5_final","M6_final"]) < dt("M7_integration"))
check("m8_after_m7", dt("M7_integration") < dt("M8_manuscript_integration"))
check("m9a_after_m8", dt("M8_manuscript_integration") < dt("M9A_posthoc_falsifiability_calibration"))
check("m9a_posthoc_flag", chronology["prospective_boundary"]["m9a_is_posthoc_review_repair"] is True)
check("m9a_no_readjudication", chronology["prospective_boundary"]["m9a_does_not_redefine_main40_outcomes"] is True)

for phrase in [
    "procedural auditability rather than inter-rater reliability",
    "not substitutes for independent human adjudication",
    "single-adjudicator, source-identity-separated prospective compatibility test",
]:
    check(f"boundary_{phrase}", phrase in boundary)

for phrase in [
    "single-adjudicator prospective compatibility test",
    "Independent human re-adjudication was not performed",
    "Post-hoc falsifiability calibration of the A-state rule",
    "uniform descriptive compatibility with direct composition under the frozen source-faithful reconstruction contract",
    "A1=E_1\\setminus E_0",
]:
    check(f"manuscript_{phrase}", phrase in manuscript)

for forbidden in [
    "40 independent replications",
    "independent human re-adjudication was performed",
    "POMDPs cannot encode",
]:
    check(f"forbidden_{forbidden}", forbidden not in manuscript)

print(f"M9B_AUDITABILITY_PASS {len(checks)}/{len(checks)}")
