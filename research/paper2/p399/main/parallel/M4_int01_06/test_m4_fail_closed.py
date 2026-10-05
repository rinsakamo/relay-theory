#!/usr/bin/env python3
import json, pathlib, subprocess, sys

ROOT=pathlib.Path(__file__).resolve().parent
REPO=ROOT.parents[5]
KICKOFF="3c2761ac13b04203aa7dbd8f47a1d687d506bf7b"
MANIFEST_BLOB="b97b67a34ad9c2858745dfa6aa60444520eaab13"
SOURCE_LOCK="a4ef8fbdafc3870ef100bafbfaed20f46adbe87f"
STAGE_A="0992a46f38f4beefb4bf6f29a69a4b9637390e12"
STAGE_B="cc1228ff16a612165e0d35caaa7d89c86ad556ae"
STAGE_C="873031d8d45e7b41e6c89fb3c73c879d42e05900"
EXPECTED={
"INT-01":"10.1016/j.cognition.2024.105967",
"INT-02":"10.3390/e26060484",
"INT-03":"10.1073/pnas.95.24.14529",
"INT-04":"10.1038/s41562-023-01799-z",
"INT-05":"10.1371/journal.pcbi.1004110",
"INT-06":"10.1371/journal.pcbi.1000765"}
ROLES=["Pi","X","C","Q","P_in","P_out","K","T","rho/O"]
ALLOWED={"A0_FIDELITY","A1_FIDELITY","A2_FIDELITY","FAILURE_LOCALIZED","UNDERDETERMINED","SOURCE_INELIGIBLE"}
ARTS=[
"SOURCE_AUTHORITY_LOCK_v1.json","PASS_A_SOURCE_FIRST_DECOMPOSITION_v1.json",
"PASS_B_RESULT_INFORMED_REAUDIT_v1.json","PASS_C_SOURCE_CLOSED_ADJUDICATION_v1.json",
"GRAMMAR_V0_RECONSTRUCTION_v1.json","ARCHITECTURAL_OUTCOME_v1.json",
"INTEGRATION_MECHANISM_AUDIT_v1.json","LIMITATIONS_AND_NEGATIVE_EVIDENCE_v1.json"]

def load(p): return json.loads((ROOT/p).read_text())
def git(*args): return subprocess.run(["git",*args],cwd=REPO,text=True,capture_output=True)
def ok(cond,msg):
    if not cond: raise AssertionError(msg)

intake=load("M4_SIX_PAPER_INTAKE_RECEIPT_v1.json")
registry=load("M4_SIX_PAPER_OUTCOME_REGISTRY_v1.json")
boundary=load("M4_INTEGRATION_BOUNDARY_AUDIT_v1.json")
consistency=load("M4_CROSS_PAPER_CONSISTENCY_AUDIT_v1.json")
negative=load("M4_NEGATIVE_AND_UNDERDETERMINED_REGISTER_v1.json")
rows={r["slot"]:r for r in registry["rows"]}

tests=[]
def T(name,fn): tests.append((name,fn))

T("01_exact_6_paper_assignment",lambda: ok([x["slot"] for x in intake["exact_assignment"]]==list(EXPECTED),"slot assignment mismatch"))
T("02_exact_doi_identity",lambda: ok({x["slot"]:x["doi"] for x in intake["exact_assignment"]}==EXPECTED,"DOI mismatch"))
def t03():
    d=git("diff","--name-only",KICKOFF,"HEAD"); ok(d.returncode==0,d.stderr)
    bad=[p for p in d.stdout.splitlines() if p and not (p.startswith("research/paper2/p399/main/parallel/M4_int01_06/") or p==".github/workflows/p399-main-m4-int01-06.yml")]
    ok(not bad,f"outside M4 scope: {bad}")
T("03_no_INT07_16_or_other_lane_substantive_work",t03)
def t04():
    ok(git("merge-base","--is-ancestor",KICKOFF,"HEAD").returncode==0,"kickoff not ancestor")
    ok(intake["kickoff_head"]==KICKOFF,"intake kickoff mismatch")
T("04_exact_kickoff_head_ancestry",t04)
def t05():
    r=git("rev-parse",f"{KICKOFF}:research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json")
    ok(r.returncode==0 and r.stdout.strip()==MANIFEST_BLOB,"manifest blob mismatch")
    ok(intake["manifest_blob"]==MANIFEST_BLOB,"intake manifest mismatch")
T("05_exact_frozen_manifest_blob",t05)
T("06_no_duplicate_paper",lambda: ok(len(set(EXPECTED))==6 and len(set(EXPECTED.values()))==6,"duplicate slot/DOI"))
T("07_no_roster_substitution",lambda: ok(not intake["roster_replacement"] and registry["roster_replacement_count"]==0,"roster substitution"))
T("08_no_backup_activation",lambda: ok(not intake["backup_activation"] and registry["backup_activation_count"]==0,"backup activation"))
def t09():
    ok(git("merge-base","--is-ancestor",SOURCE_LOCK,STAGE_A).returncode==0,"source lock not before A")
    ok(git("merge-base","--is-ancestor",STAGE_A,STAGE_B).returncode==0,"A not before B")
T("09_stage_A_after_lock_and_before_B",t09)
def t10():
    for s in EXPECTED:
        b=load(f"{s}/PASS_B_RESULT_INFORMED_REAUDIT_v1.json")
        ok(b["frozen_stage_a"]["commit"]==STAGE_A and b["stage_b_received_frozen_a"] and not b["stage_a_mutated"],s)
T("10_B_receives_frozen_A",t10)
def t11():
    for s in EXPECTED:
        c=load(f"{s}/PASS_C_SOURCE_CLOSED_ADJUDICATION_v1.json")
        ok(c["inputs"]["frozen_A_commit"]==STAGE_A and c["inputs"]["frozen_B_commit"]==STAGE_B,s)
        for a in c["adjudications"]: ok(bool(a["decisive_source_locus"]),f"{s}:{a['objection_id']}")
T("11_C_objections_source_traced",t11)
def t12():
    for s in EXPECTED:
        a=load(f"{s}/PASS_A_SOURCE_FIRST_DECOMPOSITION_v1.json")
        c=load(f"{s}/PASS_C_SOURCE_CLOSED_ADJUDICATION_v1.json")
        l=load(f"{s}/LIMITATIONS_AND_NEGATIVE_EVIDENCE_v1.json")
        ok(bool(a["adverse_null_results"]) and c["negative_evidence_preserved"] and bool(l["retained_negative_adverse_evidence"]),s)
T("12_negative_evidence_cannot_disappear",t12)
def t13():
    for s in EXPECTED:
        g=load(f"{s}/GRAMMAR_V0_RECONSTRUCTION_v1.json")
        ok(g["authority"]["grammar_role_set"]==ROLES,s); ok(not g["new_grammar_role_added"],s)
T("13_grammar_roles_unchanged",t13)
T("14_integrated_label_cannot_auto_create_coordinator",lambda: ok(not boundary["generic_universal_coordinator_added"],"generic coordinator"))
def t15():
    for s in EXPECTED:
        o=load(f"{s}/ARCHITECTURAL_OUTCOME_v1.json")
        ok(o["added_stateful_mechanism_count"]==0,s)
T("15_shared_variable_cannot_auto_create_added_state",t15)
T("16_temporal_order_cannot_auto_create_coordinator",lambda: ok(all(rows[s]["added_stateful_mechanism_type_count"]["count"]==0 for s in EXPECTED),"temporal order promoted"))
def t17():
    for s in ["INT-03","INT-06"]:
        o=load(f"{s}/ARCHITECTURAL_OUTCOME_v1.json")
        ok(o["final_per_paper_outcome"]!="A2_FIDELITY" and o["recurrent_dynamics_alone_does_not_license_A2"],s)
T("17_recurrent_dynamics_cannot_auto_create_A2",t17)
def t18():
    for s in ["INT-03","INT-06"]:
        o=load(f"{s}/ARCHITECTURAL_OUTCOME_v1.json")
        ok(o["workspace_label_alone_does_not_license_A2"],s)
T("18_workspace_cannot_auto_create_added_A2",t18)
def t19():
    for s in EXPECTED:
        i=load(f"{s}/INTEGRATION_MECHANISM_AUDIT_v1.json")
        ok(not i["source_defined_coordination_double_counted_as_added_mechanism"],s)
T("19_source_defined_coordination_not_double_counted",t19)
def t20():
    for s,r in rows.items():
        if r["final_architectural_state"]=="A2_FIDELITY":
            tr={x["attempt"]:x["result"] for x in r["A0_A1_A2_trace"]}
            ok(tr.get("A0")=="FAIL" and tr.get("A1")=="FAIL",s)
T("20_A2_requires_documented_A0_A1_failure",t20)
def t21():
    for s in EXPECTED:
        o=load(f"{s}/ARCHITECTURAL_OUTCOME_v1.json")
        ok(o["reconstruction_failure_alone_does_not_license_A2"],s)
T("21_fit_difficulty_alone_cannot_imply_A2",t21)
def t22():
    lock=load("INT-01/SOURCE_AUTHORITY_LOCK_v1.json"); c=load("INT-01/PASS_C_SOURCE_CLOSED_ADJUDICATION_v1.json")
    txt=json.dumps(lock)+json.dumps(c)
    ok("SOFTMAX_PREPUBLICATION" in txt and "publisher corrigendum" in txt.lower() and "likelihood" in txt.lower(),"INT01 ambiguity lost")
T("22_INT01_published_code_ambiguity_preserved",t22)
def t23():
    lock=load("INT-03/SOURCE_AUTHORITY_LOCK_v1.json"); o=load("INT-03/ARCHITECTURAL_OUTCOME_v1.json")
    ok(lock["source"]["genealogy"]["status"]=="ANCESTRY_RESOLVED_DIRECT_EDGE","INT03 ancestry missing")
    ok("provenance" in o["genealogy_annotation"].lower() and o["final_per_paper_outcome"]=="A0_FIDELITY","ancestry determined architecture")
T("23_INT03_ancestry_cannot_determine_architecture",t23)
def t24():
    lock=load("INT-06/SOURCE_AUTHORITY_LOCK_v1.json")
    ok(lock["source"]["genealogy"]["int03_relation"]=="SHARED_FRAMEWORK_ONLY_NO_DIRECT_DESCENT","INT03->INT06 direct descent promoted")
T("24_INT06_shared_framework_not_direct_descent",t24)
T("25_UNDERDETERMINED_preserved_as_permitted_state",lambda: ok(all(r["final_architectural_state"] in ALLOWED for r in rows.values()),"invalid forced state"))
T("26_SOURCE_INELIGIBLE_cannot_trigger_replacement",lambda: ok(registry["roster_replacement_count"]==0 and set(rows)==set(EXPECTED),"replacement"))
T("27_genealogy_cannot_alter_roster",lambda: ok(set(rows)==set(EXPECTED) and all(r["genealogy_annotation"] for r in rows.values()),"genealogy roster change"))
def t28():
    for s in EXPECTED:
        o=load(f"{s}/ARCHITECTURAL_OUTCOME_v1.json"); l=load(f"{s}/LIMITATIONS_AND_NEGATIVE_EVIDENCE_v1.json")
        ok(not o["genealogical_independence_assumed"] and not l["global_genealogical_independence_claimed"],s)
    ok(registry["genealogy_independence_promotions"]==0,"registry promotion")
T("28_no_genealogy_independence_promotion",t28)
T("29_G1_PILOT20_excluded",lambda: ok(not intake["g1_pilot20_counts_as_main_evidence"] and not intake["g1_pilot20_counts_in_main_denominator"] and registry["g1_pilot20_in_main_evidence_count"]==0,"G1 leaked"))
T("30_exact_outcome_count_6",lambda: ok(len(registry["rows"])==6 and len(rows)==6 and sum(registry["outcome_counts"].values())==6,"outcome count"))
def t31():
    ok(registry["aggregate_H_claim"]=="PROHIBITED_IN_M4","registry H verdict")
    for s in EXPECTED:
        o=load(f"{s}/ARCHITECTURAL_OUTCOME_v1.json")
        ok(not o["overall_H_verdict_issued"] and o["no_universal_H_claim"],s)
T("31_M4_cannot_issue_overall_H_verdict",t31)
def t32():
    for s in EXPECTED:
        lock=load(f"{s}/SOURCE_AUTHORITY_LOCK_v1.json")
        ok(lock["kickoff_head"]==KICKOFF and lock["manifest_blob"]==MANIFEST_BLOB and lock["w9_profile_status"]=="SOURCE_NATIVE_PROFILE_COMPLETE",s)
T("32_exact_source_authority_lock_per_paper",t32)
def t33():
    for s in EXPECTED:
        c=load(f"{s}/PASS_C_SOURCE_CLOSED_ADJUDICATION_v1.json")
        ok(c["safeguards"]["C1_entire_original_A_reopened_before_patch"] and c["safeguards"]["C2_source_local_negative_limit_enumeration"],s)
        ok(c["condition_ledger_reconciled_exactly_once"] and not c["duplicate_patching"],s)
T("33_RIR_v231_C1_C2_and_no_duplicate_patch",t33)
def t34():
    for s in EXPECTED:
        missing=[f for f in ARTS if not (ROOT/s/f).is_file()]
        ok(not missing,f"{s} missing {missing}")
T("34_eight_required_per_paper_artifacts",t34)
T("35_integration_boundary_added_counts_zero",lambda: ok(boundary["totals"]["papers"]==6 and boundary["totals"]["reconstruction_added_stateless_interface_count"]==0 and boundary["totals"]["reconstruction_added_stateful_mechanism_count"]==0,"boundary totals"))
T("36_cross_paper_templates_not_forced",lambda: ok(not consistency["forced_single_integration_template"] and consistency["overall_H_conclusion_forbidden"],"forced template/H"))

passed=0
for name,fn in tests:
    try:
        fn(); print("PASS",name); passed+=1
    except Exception as e:
        print("FAIL",name,repr(e)); sys.exit(1)
print(f"PASS {passed}/{len(tests)}")
ok(passed==36 and len(tests)==36,"test count")
