#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[5]
KICKOFF = "3c2761ac13b04203aa7dbd8f47a1d687d506bf7b"
A_FREEZE = "935c5c9b12949758148a32f16ce52cddb64661e3"
C_FREEZE = "e563741558c2ceb2e1b4017018a1a87901fbd6f4"
MANIFEST = "research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json"
MANIFEST_BLOB = "b97b67a34ad9c2858745dfa6aa60444520eaab13"
WORKFLOW = ".github/workflows/p399-main-m2-ctl-lrn.yml"
EXPECTED = {
    "CTL-01": "10.1371/journal.pcbi.1012228",
    "CTL-02": "10.7554/eLife.12029",
    "CTL-03": "10.7554/eLife.28040",
    "LRN-01": "10.1038/s41467-025-58848-6",
    "LRN-02": "10.1371/journal.pcbi.1007963",
    "LRN-03": "10.7554/eLife.21492",
}
PERMITTED = {"A0_FIDELITY","A1_FIDELITY","A2_FIDELITY","FAILURE_LOCALIZED","UNDERDETERMINED","SOURCE_INELIGIBLE"}
GRAMMAR_ROLES = {"Pi","X","C","Q","P_in","P_out","K","T","rho_O"}

checks = []
def check(name, cond):
    checks.append((name, bool(cond)))
    if not cond:
        raise AssertionError(name)

def load(path):
    return json.loads((ROOT / path).read_text())

def git(*args, check_rc=True):
    p = subprocess.run(["git", *args], cwd=REPO, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check_rc and p.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {p.stderr}")
    return p

intake = load("M2_SIX_PAPER_INTAKE_RECEIPT_v1.json")
registry = load("M2_SIX_PAPER_OUTCOME_REGISTRY_v1.json")
boundary = load("M2_CTL_LRN_BOUNDARY_AUDIT_v1.json")
consistency = load("M2_CROSS_PAPER_CONSISTENCY_AUDIT_v1.json")
negative = load("M2_NEGATIVE_AND_UNDERDETERMINED_REGISTER_v1.json")

assignment = {r["slot"]: r["doi"] for r in intake["lane"]["assignment"]}
check("01_exact_6_paper_assignment", len(assignment) == 6 and assignment == EXPECTED)
check("02_exact_doi_identity", all(EXPECTED[k] == v for k, v in assignment.items()))
check("03_no_non_m2_scientific_paper_in_assignment", set(assignment) == set(EXPECTED))
check("04_exact_kickoff_head_recorded", intake["authority"]["exact_kickoff_head"] == KICKOFF)
check("05_exact_kickoff_ancestry", git("merge-base", "--is-ancestor", KICKOFF, "HEAD", check_rc=False).returncode == 0)
check("06_exact_main40_manifest_blob", git("rev-parse", f"{KICKOFF}:{MANIFEST}").stdout.strip() == MANIFEST_BLOB)
check("07_no_duplicate_paper", len(set(assignment)) == 6 and len(set(assignment.values())) == 6)
check("08_no_roster_substitution", intake["lane"]["no_roster_substitution"] is True)
check("09_no_backup_activation", intake["lane"]["no_backup_activation"] is True)

check("10_stage_a_freeze_ancestor_of_c_freeze", git("merge-base", "--is-ancestor", A_FREEZE, C_FREEZE, check_rc=False).returncode == 0)
check("11_c_freeze_ancestor_of_final_head", git("merge-base", "--is-ancestor", C_FREEZE, "HEAD", check_rc=False).returncode == 0)

outcomes = {}
for slot, doi in EXPECTED.items():
    lock = load(f"{slot}/SOURCE_AUTHORITY_LOCK_v1.json")
    a = load(f"{slot}/PASS_A_SOURCE_FIRST_DECOMPOSITION_v1.json")
    b = load(f"{slot}/PASS_B_RESULT_INFORMED_REAUDIT_v1.json")
    c = load(f"{slot}/PASS_C_SOURCE_CLOSED_ADJUDICATION_v1.json")
    g = load(f"{slot}/GRAMMAR_V0_RECONSTRUCTION_v1.json")
    o = load(f"{slot}/ARCHITECTURAL_OUTCOME_v1.json")
    lim = load(f"{slot}/LIMITATIONS_AND_NEGATIVE_EVIDENCE_v1.json")
    outcomes[slot] = o

    check(f"12_source_lock_{slot}", lock["doi"] == doi and lock["source_native_profile_status"] == "SOURCE_NATIVE_PROFILE_COMPLETE")
    check(f"13_a_before_b_and_complete_{slot}", a["stage_a_complete"] and a["stage_a_frozen_before_b"] and b["stage_a_input"]["freeze_head"] == A_FREEZE and b["stage_a_input"]["complete_a_received"])
    b_commit = c["inputs"]["stage_b_commit"]
    check(f"14_b_after_a_{slot}", git("merge-base", "--is-ancestor", A_FREEZE, b_commit, check_rc=False).returncode == 0)
    check(f"15_c_objections_trace_source_{slot}", c["stage_c_complete"] and all(x.get("source_locus") for x in c["adjudications"]))
    check(f"16_c_safeguards_{slot}", c["safeguards"]["C1_original_a_coverage_and_overpatch"] and c["safeguards"]["C2_material_negative_limit_enumeration"])
    check(f"17_negative_evidence_retained_{slot}", c["negative_evidence_retained"] and bool(lim["negative_and_adverse_evidence"]))
    check(f"18_grammar_roles_unchanged_{slot}", g["roles_unchanged"] and set(g["role_mapping"]) == GRAMMAR_ROLES)
    check(f"19_no_hidden_procedural_logic_{slot}", g["arbitrary_procedural_logic_hidden_in_X_or_K"] is False)
    check(f"20_permitted_outcome_{slot}", o["final_architectural_state"] in PERMITTED)
    if o["final_architectural_state"] == "A2_FIDELITY":
        check(f"21_a2_requires_a0_a1_failure_{slot}", o["attempt_trace"]["A0"]["result"] == "FAIL" and o["attempt_trace"]["A1"]["result"] == "FAIL")
    else:
        check(f"21_no_illicit_a2_{slot}", o["attempt_trace"]["A2"]["attempted"] is False)
    if o["final_architectural_state"] == "FAILURE_LOCALIZED":
        check(f"22_failure_not_a2_{slot}", o["attempt_trace"]["A2"]["result"] != "PASS")
    else:
        check(f"22_failure_rule_vacuously_preserved_{slot}", True)
    check(f"23_no_genealogy_independence_{slot}", o["genealogy_annotation"]["global_genealogical_independence_assumed"] is False and lim["genealogy"]["global_independence_certified"] is False)
    check(f"24_no_replacement_from_outcome_{slot}", lim["outcome_replacement_triggered"] is False and lim["backup_activation"] is False)

check("25_exact_final_outcome_count", registry["exact_row_count"] == 6 and len(registry["rows"]) == 6)
check("26_registry_exact_roster", {r["slot"]: r["doi"] for r in registry["rows"]} == EXPECTED)
check("27_undertermined_preservation_rule", negative["underdetermined_outcomes_preserved"] is True)
check("28_source_ineligible_no_replacement_rule", negative["source_ineligible_would_not_trigger_replacement"] is True)
check("29_negative_evidence_cannot_disappear", negative["no_negative_evidence_dropped"] is True)
check("30_g1_pilot20_excluded", intake["frozen_main"]["g1_pilot20_excluded"] is True and intake["frozen_main"]["denominator"] == 40)
check("31_m2_no_overall_h_verdict", registry["overall_h0_h1_h2_conclusion"] is None and all(o["overall_h0_h1_h2_implication"].startswith("NONE") for o in outcomes.values()))
check("32_control_demand_proxy_boundary", any(x["boundary"] == "meta-control vs task instruction" and x["status"] == "PASS_SEPARATED" for x in boundary["findings"]))
check("33_neural_correlate_boundary", any(x["boundary"] == "controller state vs learned parameter" and x["status"] == "PASS_SEPARATED" for x in boundary["findings"]))
check("34_learned_parameter_not_coordinator", outcomes["LRN-01"]["added_stateful_mechanisms"]["count"] == 0 and outcomes["LRN-03"]["added_stateful_mechanisms"]["count"] == 0)
check("35_source_defined_ctl_not_new_a2", outcomes["CTL-02"]["final_architectural_state"] == "A0_FIDELITY" and outcomes["CTL-02"]["added_stateful_mechanisms"]["count"] == 0)
check("36_boundary_audit_all_six_classes", boundary["audit_count"] == 6 and len(boundary["findings"]) == 6)
check("37_cross_paper_terms_not_collapsed", all(x["same_mechanism_assumed"] is False for x in consistency["common_term_checks"]))
check("38_w9_intra_m2_pair_count_and_no_independence", len(consistency["w9_intra_m2_pair_annotations"]) == 15 and all(x["independence_inferred"] is False for x in consistency["w9_intra_m2_pair_annotations"]))
check("39_all_six_source_fidelity", all(r["source_fidelity"] == "SOURCE_CLOSED_ADJUDICATED" for r in registry["rows"]))
check("40_all_six_a0_trace_present", all(r["attempt_trace"]["A0"] == "ATTEMPTED_PASS" for r in registry["rows"]))

changed = [x for x in git("diff","--name-only",f"{KICKOFF}..HEAD").stdout.splitlines() if x]
allowed = [p.startswith("research/paper2/p399/main/parallel/M2_ctl_lrn/") or p == WORKFLOW for p in changed]
check("41_lane_isolation_changed_paths", bool(changed) and all(allowed))
check("42_no_shared_main_registry_modified", not any(p.startswith("research/paper2/p399/main/") and "/parallel/M2_ctl_lrn/" not in p for p in changed))
check("43_no_other_main_lane_modified", not any("/parallel/M1_" in p or "/parallel/M3_" in p or "/parallel/M4_" in p or "/parallel/M5_" in p or "/parallel/M6_" in p for p in changed))
check("44_standalone_supplement_scope_not_silently_expanded", intake["source_closed_rule"]["standalone_linked_supplements"].startswith("identity/profile-role retained"))
check("45_no_added_adapter_or_stateful_mechanism", registry["stateless_adapters_added"] == 0 and registry["stateful_mechanisms_added"] == 0)
check("46_exact_count_vector", registry["counts"] == {"A0_FIDELITY":6,"A1_FIDELITY":0,"A2_FIDELITY":0,"FAILURE_LOCALIZED":0,"UNDERDETERMINED":0,"SOURCE_INELIGIBLE":0})

print("\n".join(f"PASS {name}" for name, ok in checks if ok))
print(f"PASS {len(checks)}/{len(checks)} fail-closed checks")
