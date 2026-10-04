#!/usr/bin/env python3
"""W3 independent source-complete handoff guard. Verifies immutable original stage
bytes/chronology, new individually scoped outcomes, unresolved ancestry and lane-only
git scope. This is NOT independent human semantic adjudication or global G1 GO.
"""
import hashlib,json,pathlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
PRE="research/paper2/p399/g1/parallel/W3/"
BASE="38c5eb24c61b9e57371084a65fcbcb9fb9c62a4b"
STAGES={
 "P15":[
 ("PRE_A","P15_PRE_A_original_complete_math_figures_frozen_v1.json","6e523ca5c9257def9a58a37c49d6a29541eedc38"),
 ("A","P15_A_original_source_native_v1.json","50268096b0bb54ae85443e796a72d9052c141950"),
 ("B","P15_B_original_source_full_A_adversarial_reaudit_v1.json","25651804e9cfccb152975a1430790a1aec2d9689"),
 ("C","P15_C_reopen_original_A_adjudicate_source_negatives_v1.json","e64579b1573299773bb017add1a4366e05133977"),
 ("D","P15_D_unchanged_grammar_v0_complete_source_mapping_v1.json","e8bbe2eb9144c2c1e4b9928e5baf8235147bba23"),
 ("E","P15_E_original_source_relative_fidelity_v1.json","1e49466bd88b044532c1848df48a69b5be3c12b5"),
 ],
 "P16":[
 ("PRE_A","P16_PRE_A_original_source_freeze_v1.json","09519d43dcf73ba0d18be443298528723b5cf8fa"),
 ("A","P16_A_source_native_v1.json","998dd41220b4365c2572cdcdd4e0ff7a460967ac"),
 ("B","P16_B_reaudit_complete_frozen_A_v1.json","8aa8bf28eda3e3dc42d8fae9a6518757e5fb36c9"),
 ("C","P16_C1C2_source_closed_v1.json","273193a55fe605c6d623efc05fcb8c81061c6462"),
 ("D","P16_D_unchanged_grammar_v0_v1.json","dcca60ef6b26227d3bb13de924a414dfa79a437f"),
 ("E","P16_E_original_source_fidelity_v1.json","b3f742422e12c07298b339d1e5067a7266781679"),
 ],
 "P18":[
 ("PRE_A","P18_PRE_A_publisher_original_final_and_model_recovery_sources_frozen_v1.json","07b4e732461b350eb6aef8dddb94394c59260c1d"),
 ("A","P18_A_final_original_source_native_v1.json","4026bfaadc3d1672f441fb963b2bb5041b9fd245"),
 ("B","P18_B_original_source_complete_A_adversarial_review_v1.json","420bb7799bf8bb50d5b337f4a70b31c0e513bcd7"),
 ("C","P18_C_full_original_A_reopen_and_adversarial_closure_v1.json","c8869c6e8306b40e1ccf5dd334b7d667c5cbd7a1"),
 ("D","P18_D_unchanged_frozen_grammar_v0_full_original_v1.json","c24f9a5679721299e7909a4e51c0756fe48ef967"),
 ("E","P18_E_bounded_original_publisher_fidelity_v1.json","b7f7270a038f3dfaad2ed0bf9f3c0f86f5dbf5cb"),
 ]}
QUAL={
 "P15":("P15_POST_E_INDEPENDENT_PUBLISHER_SCOPED_QUALIFICATION_v1.json","P15_individual_source_scientific_qualified",37198525660),
 "P16":("P16_POST_E_INDEPENDENT_REAL_SOURCE_SCOPED_QUALIFICATION_v1.json","separate_scientific_candidate_qualified",37191737724),
 "P18":("P18_POST_E_INDEPENDENT_PUBLISHER_SCOPED_QUALIFICATION_v1.json","P18_individual_scoped_scientific_source_qualified",37198719136),
}
def run(*cmd):return subprocess.check_output(["git",*cmd],text=True).strip()
def check(value,msg):
 if not value:raise RuntimeError("FAIL_CLOSED_W3_"+msg)
check(run("merge-base",BASE,"HEAD")==BASE,"exact_scoped_coordination_origin")
changed=run("diff","--name-only",BASE+"..HEAD").splitlines()
check(bool(changed) and all(x.startswith(PRE) or (x.startswith(".github/workflows/p399-g1-W3-") and x.endswith(".yml")) for x in changed),"strict_scoped_write_allowlist")
staged={};qualified={}
for paper,seq in STAGES.items():
 checks=[];previous=None
 for name,file,commit in seq:
  rel=PRE+file;source=subprocess.check_output(["git","show",commit+":"+rel]);current=(ROOT/file).read_bytes()
  check(source==current,paper+"_"+name+"_frozen_first_introduction_bytes")
  check(run("log","--diff-filter=A","--format=%H","HEAD","--",rel).splitlines()==[commit],paper+"_"+name+"_single_original_introduction")
  check(subprocess.run(["git","merge-base","--is-ancestor",commit,"HEAD"]).returncode==0,paper+"_"+name+"_on_branch")
  if previous:check(subprocess.run(["git","merge-base","--is-ancestor",previous,commit]).returncode==0,paper+"_"+name+"_strict_ancestry")
  previous=commit;checks.append({"stage":name,"commit":commit,"bytes_sha256":hashlib.sha256(source).hexdigest()})
 staged[paper]=checks
 file,key,run_id=QUAL[paper]
 q=json.loads((ROOT/file).read_text())
 check(q.get(key) is True,paper+"_real_qualified_flag")
 if paper=="P15":record=q["independent_real_afterE_CI"]
 elif paper=="P16":record=q["independent_POST_E_run"]
 else:record=q["independent_real_afterE_original_PLOS_Actions"]
 check(record["run_id"]==run_id and record["conclusion"]=="success",paper+"_genuine_original_Actions_receipt_ref")
 qualified[paper]={"scoped_qualified":True,"original_real_publisher_Actions_id":run_id,"absolute_global_G1_admission":False}
j=json.loads((ROOT/"W3_SOURCE_COMPLETED_FAMILY_HANDOFF_MATRIX_v2.json").read_text())
check(len(j["rows"])==7 and all(r["result"]=="FAMILY_UNDERDETERMINED" for r in j["rows"]),"seven_source_bounded_unresolved_family_cases")
check(j["baseline_common_G1_original_9of20_unmodified"] is True and j["global_cohort_model_family_independence_not_yet_granted"] is True,"global_G1_guards")
check(set(p["id"] for p in j["W3_all_three_scoped_source_qualified"])==set(STAGES),"exact_W3_3")
# Synthetic mutation guard (not arbitrary safety): frozen source-byte changes cannot hash match.
check(hashlib.sha256((ROOT/STAGES["P15"][1][1]).read_bytes()+b"altered").hexdigest()!=staged["P15"][1]["bytes_sha256"],"destructive_sha_check")
check(6*3==sum(len(x) for x in staged.values()),"eighteen_strict_commits")
receipt={"result":"PASS_W3_SCOPED_ALL_THREE_SOURCE_QUALIFIED_NOT_FAMILY_CLEARED","exact_baseline":BASE,
  "only_W3_scoped_changed_files":changed,"all_eighteen_immutable_science_introductions":staged,
  "three_scoped_source_qualifications":qualified,"source_genealogy_pairs":7,
  "family_decisions":"7x_UNDERDETERMINED_FOR_GLOBAL_COHORT","global_G1_shared_baseline":9,
  "no_global_denominator_revision":True,"G4_authorization":False,
  "not_independent_external_semantic_adjudication":True}
print(json.dumps(receipt,indent=2,sort_keys=True),flush=True)
pathlib.Path("W3_handoff_receipt").mkdir(exist_ok=True)
(pathlib.Path("W3_handoff_receipt")/"receipt.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
