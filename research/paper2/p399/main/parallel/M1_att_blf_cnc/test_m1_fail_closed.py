#!/usr/bin/env python3
import json, pathlib, subprocess, sys

ROOT=pathlib.Path(__file__).resolve().parent
REPO=ROOT.parents[5]
KICKOFF="3c2761ac13b04203aa7dbd8f47a1d687d506bf7b"
MANIFEST_BLOB="b97b67a34ad9c2858745dfa6aa60444520eaab13"
STAGE_A="541b9a269b31b21dbea595b172dda4f37be19f78"
STAGE_B="ea298e106fe2dd800ffdc8f26479d1f09be5864a"
STAGE_C="9e597539244d161a7f20320ecf22ece1bf32b400"
EXPECTED={
"ATT-01":"10.1007/s42113-024-00197-6","ATT-02":"10.1371/journal.pcbi.1004770","ATT-03":"10.1016/j.neuron.2009.01.002",
"BLF-01":"10.1016/j.isci.2025.112844","BLF-02":"10.1371/journal.pcbi.1006972","BLF-03":"10.7554/eLife.08825",
"CNC-01":"10.1038/s41562-023-01719-1","CNC-02":"10.1371/journal.pcbi.1011954","CNC-03":"10.7554/eLife.77185"}
ROLES=["Pi","X","C","Q","P","K","T","rho/O"]
ALLOWED={"A0_FIDELITY","A1_FIDELITY","A2_FIDELITY","FAILURE_LOCALIZED","UNDERDETERMINED","SOURCE_INELIGIBLE"}

def load(p): return json.loads((ROOT/p).read_text())
def git(*args):
    return subprocess.run(["git",*args],cwd=REPO,text=True,capture_output=True)
def ok(cond,msg):
    if not cond: raise AssertionError(msg)

intake=load("M1_NINE_PAPER_INTAKE_RECEIPT_v1.json")
registry=load("M1_NINE_PAPER_OUTCOME_REGISTRY_v1.json")
rows={r["slot"]:r for r in registry["rows"]}

tests=[]
def T(name,fn): tests.append((name,fn))

T("01_exact_9_paper_assignment",lambda: ok([x["slot"] for x in intake["exact_assignment"]]==list(EXPECTED),"slot assignment mismatch"))
T("02_exact_doi_identity",lambda: ok({x["slot"]:x["doi"] for x in intake["exact_assignment"]}==EXPECTED,"DOI mismatch"))
def t03():
    d=git("diff","--name-only",KICKOFF,"HEAD"); ok(d.returncode==0,d.stderr)
    bad=[p for p in d.stdout.splitlines() if p and not (p.startswith("research/paper2/p399/main/parallel/M1_att_blf_cnc/") or p==".github/workflows/p399-main-m1-att-blf-cnc.yml")]
    ok(not bad,f"outside M1 substantive scope: {bad}")
T("03_no_paper_or_substantive_work_outside_M1",t03)
def t04():
    r=git("merge-base","--is-ancestor",KICKOFF,"HEAD"); ok(r.returncode==0,"kickoff is not ancestor")
    ok(intake["authority"]["kickoff_head"]==KICKOFF,"intake kickoff mismatch")
T("04_exact_kickoff_head_ancestry",t04)
def t05():
    r=git("rev-parse",f"{KICKOFF}:research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json")
    ok(r.returncode==0 and r.stdout.strip()==MANIFEST_BLOB,"manifest blob mismatch")
T("05_exact_frozen_MAIN40_manifest_blob",t05)
T("06_no_duplicate_paper",lambda: ok(len(set(EXPECTED))==9 and len({v for v in EXPECTED.values()})==9,"duplicate slot/DOI"))
T("07_no_roster_substitution",lambda: ok(not intake["roster_substitution"] and registry["roster_replacement_count"]==0,"roster substitution"))
T("08_no_backup_activation",lambda: ok(not intake["backup_activation"] and registry["backup_activation_count"]==0,"backup activation"))
def t09():
    ok(git("merge-base","--is-ancestor",STAGE_A,STAGE_B).returncode==0,"A not before B")
    for s in EXPECTED:
        b=load(f"{s}/PASS_B_RESULT_INFORMED_REAUDIT_v1.json"); ok(b["chronology"]["stage_a_exact_commit"]==STAGE_A and b["chronology"]["stage_a_was_frozen_before_b"],s)
T("09_stage_A_frozen_before_stage_B",t09)
def t10():
    for s in EXPECTED:
        b=load(f"{s}/PASS_B_RESULT_INFORMED_REAUDIT_v1.json"); ok(b["chronology"]["received_complete_frozen_stage_a"],s)
T("10_stage_B_receives_complete_stage_A",t10)
def t11():
    for s in EXPECTED:
        c=load(f"{s}/PASS_C_SOURCE_CLOSED_ADJUDICATION_v1.json")
        ok(c["chronology"]["stage_a_exact_commit"]==STAGE_A and c["chronology"]["stage_b_exact_commit"]==STAGE_B,s)
        for a in c["adjudications"]: ok(bool(a["decisive_original_source_loci"]),f"{s}:{a['objection_id']}")
T("11_stage_C_objections_trace_to_source_loci",t11)
def t12():
    for s in EXPECTED:
        c=load(f"{s}/PASS_C_SOURCE_CLOSED_ADJUDICATION_v1.json")
        ok(c["duplicate_patch_count"]==0,s)
        ids=[a["objection_id"] for a in c["adjudications"]]; ok(len(ids)==len(set(ids)),s)
T("12_no_double_patch_of_already_qualified_A",t12)
def t13():
    for s in EXPECTED:
        a=load(f"{s}/PASS_A_SOURCE_FIRST_DECOMPOSITION_v1.json")
        l=load(f"{s}/LIMITATIONS_AND_NEGATIVE_EVIDENCE_v1.json")
        ok(a["source_native_decomposition"]["negative_adverse_findings"],s)
        ok(l["retained_negative_adverse_evidence"],s)
T("13_material_negative_conditions_retained",t13)
def t14():
    for s in EXPECTED:
        g=load(f"{s}/GRAMMAR_V0_RECONSTRUCTION_v1.json")
        ok(g["authority"]["grammar_role_set"]==ROLES,s); ok(not g["new_grammar_role_added"],s)
T("14_grammar_v0_role_set_unchanged",t14)
def t15():
    for s,r in rows.items():
        if r["final_per_paper_outcome"]=="A2_FIDELITY":
            tr={x["attempt"]:x["result"] for x in r["A0_A1_A2_attempt_trace"]}
            ok(tr.get("A0")=="FAIL" and tr.get("A1")=="FAIL",s)
T("15_A2_requires_documented_A0_A1_failures",t15)
def t16():
    for s in EXPECTED:
        o=load(f"{s}/ARCHITECTURAL_OUTCOME_v1.json"); ok(o["reconstruction_failure_alone_does_not_license_A2"],s)
T("16_reconstruction_failure_alone_not_A2",t16)
def t17():
    for s in EXPECTED:
        o=load(f"{s}/ARCHITECTURAL_OUTCOME_v1.json"); ok(o["source_defined_ctl_or_state_does_not_count_as_new_coordinator"],s)
T("17_source_defined_CTL_or_state_not_new_coordinator",t17)
T("18_UNDERDETERMINED_not_auto_promoted",lambda: ok(all(r["final_per_paper_outcome"] in ALLOWED for r in rows.values()) and not any(r["final_per_paper_outcome"]=="A2_FIDELITY" and r["unresolved_state"] for r in rows.values()),"promotion"))
T("19_SOURCE_INELIGIBLE_not_replaced",lambda: ok(registry["roster_replacement_count"]==0 and set(rows)==set(EXPECTED),"replacement"))
T("20_genealogy_cannot_alter_roster",lambda: ok(set(rows)==set(EXPECTED) and all(r["genealogy_annotation"] for r in rows.values()),"genealogy roster change"))
def t21():
    for s in EXPECTED:
        o=load(f"{s}/ARCHITECTURAL_OUTCOME_v1.json"); l=load(f"{s}/LIMITATIONS_AND_NEGATIVE_EVIDENCE_v1.json")
        ok(not o["genealogical_independence_assumed"] and not l["global_genealogical_independence_claimed"],s)
T("21_no_genealogy_independence_promotion",t21)
T("22_G1_PILOT20_excluded_from_MAIN",lambda: ok(not intake["g1_pilot20_main_evidence"] and registry["g1_pilot20_in_main_evidence_count"]==0,"G1 leaked"))
T("23_per_paper_outcome_count_9",lambda: ok(len(registry["rows"])==9 and len(rows)==9,"outcome count"))
T("24_no_aggregate_H_majority_claim",lambda: ok(registry["aggregate_H_claim"]=="PROHIBITED_IN_M1" and all(r["no_universal_H_claim"] for r in rows.values()),"aggregate H claim"))
def t25():
    for s in EXPECTED:
        lock=load(f"{s}/SOURCE_AUTHORITY_LOCK_v1.json"); lim=load(f"{s}/LIMITATIONS_AND_NEGATIVE_EVIDENCE_v1.json")
        ok(not lock["edition_substitution_performed"],s); ok(lim["source_edition_exceptions_remain_explicit"],s)
T("25_all_source_edition_exceptions_explicit",t25)

passed=0
for name,fn in tests:
    try: fn(); print("PASS",name); passed+=1
    except Exception as e: print("FAIL",name,repr(e)); sys.exit(1)
print(f"PASS {passed}/{len(tests)}")
ok(passed==25 and len(tests)==25,"test count")
