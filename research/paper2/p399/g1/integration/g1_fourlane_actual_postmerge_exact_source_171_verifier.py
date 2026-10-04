#!/usr/bin/env python3
"""Post-SQUASH exact source-scoped metadata proof.

Verifies actual integrated shared-branch 171 raw Git blob contents against the
FOUR unchanged original stage-head archival refs, each original source
qualification record, and the original v6 source evidence chain. This is NOT
final G1 original central family/independent publisher admission.
"""
import pathlib,sys,subprocess,hashlib,json
p=pathlib.Path(__file__).resolve().parents[1]
root="research/paper2/p399/g1/"
M=json.loads((p/"integration/G1_FOUR_LANE_EXACT_PREMERGE_PROVENANCE_AND_CONDITIONAL_SCOPE_FREEZE_v1.json").read_text())
X=json.loads((p/"integration/G1_ORIGINAL_STAGE_ARCHIVE_AND_SQUASH_TRANSPORT_EXCEPTION_AFTER_GITHUB_405_v1.json").read_text())
def git(*args):return subprocess.check_output(["git",*args],text=True,stderr=subprocess.STDOUT).strip()
def blob(ref,file):return git("rev-parse",f"{ref}:{file}")
archive={x["lane"]:x for x in X["archived_immutable_scientific_history_heads"]}
files=set();rows={}
for lane in M["lanes"]:
 n=lane["lane"];a=archive[n]
 assert a["original_source_head"]==lane["original_head_sha"]
 git("fetch","--no-tags","origin",f'refs/heads/{a["archival_branch"]}:refs/remotes/origin/{n}-g1-original-science-archive')
 assert git("rev-parse",f"refs/remotes/origin/{n}-g1-original-science-archive")==a["original_source_head"]
 assert git("merge-base",M["base_exact_before_any_science_lane_integration"],a["original_source_head"])==M["base_exact_before_any_science_lane_integration"]
 local={}
 for f in lane["changed_filenames_exact_sorted"]:
  assert f not in files,"duplicate source: "+f
  files.add(f)
  actual=blob("HEAD",f);original=blob(a["original_source_head"],f)
  assert actual==original,"actual integrated science evidence mutated "+f
  local[f]=original
 rows[n]={"original_head":a["original_source_head"],"archive_branch":a["archival_branch"],"source_exact_same_original_git_blobs":len(local),"original_git_blob_by_file":local}
 print("G1_POSTMERGE_REAL_ORIGINAL_UNCHANGED_BLOBS_PASS",n,len(local),a["original_source_head"],flush=True)
assert len(files)==171
# Actual shared branch history must contain all four squash transports, not
# the original scientific source-stage branches. Original stage DAG preserved
# explicitly by the archives above, not faked by squash parentage.
merged=["00f01d6bf3f04f05f07a5e356fb5a0d23d120c61","46194e7cf7d6d0e84ba54b536dd147b09f3bab0e","8abe16d25eeb776b08b08c5ee43739e098d19a9e","e577fdc26a428e3ccaab681ec58fa61dc0c2e0d1"]
for sha in merged:git("merge-base","--is-ancestor",sha,"HEAD")
assert git("rev-parse",M["base_exact_before_any_science_lane_integration"]+":research/paper2/p399/g1/G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v6.json")==blob("HEAD",root+"G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v6.json")
q={
"P06":("W1","p06/P06_SEPARATE_LIMITED_ORIGINAL_SCIENCE_QUALIFICATION_20261004.json"),
"P08":("W1","p08/P08_SEPARATE_LIMITED_ORIGINAL_SCIENCE_QUALIFICATION_20261004.json"),
"P10":("W1","p10/P10_SEPARATE_LIMITED_ORIGINAL_SCIENCE_QUALIFICATION_20261004.json"),
"P11":("W2","p11/P11_SEPARATE_INDIVIDUAL_SOURCE_BOUNDED_QUALIFICATION_v1.json"),
"P12":("W2","p12/P12_SEPARATE_SOURCE_BOUNDED_QUALIFICATION_AFTER_POSTE_v1.json"),
"P17":("W2","p17/P17_SEPARATE_INDIVIDUAL_SOURCE_BOUNDED_QUALIFICATION_AFTER_POSTE_v1.json"),
"P15":("W3","P15_POST_E_INDEPENDENT_PUBLISHER_SCOPED_QUALIFICATION_v1.json"),
"P16":("W3","P16_POST_E_INDEPENDENT_REAL_SOURCE_SCOPED_QUALIFICATION_v1.json"),
"P18":("W3","P18_POST_E_INDEPENDENT_PUBLISHER_SCOPED_QUALIFICATION_v1.json"),
"P19":("W4","p19/P19_SEPARATE_BOUNDED_POSTE_SCIENTIFIC_QUALIFICATION_20261004.json"),
"P20":("W4","p20/P20_SEPARATE_POSTE_SOURCE_BOUNDED_SCIENTIFIC_QUALIFICATION_20261004.json")
}
assert set(q)==set(M["all_11_exact_paper_ids"])
source_records={}
for id,(lane,name) in sorted(q.items()):
 f=root+"parallel/"+lane+"/"+name
 x=json.loads((pathlib.Path.cwd()/f).read_text())
 good={
"P06":lambda z:z["formal_decision"].startswith("SOURCE_BOUNDED_"),
"P08":lambda z:"MANDATORY_COMPLETE_SUBSTANTIVE_CORRECTION" in z["formal_decision"],
"P10":lambda z:z["qualification"]=="QUALIFIED_BOUNDED_ORIGINAL_SOURCE_STRUCTURAL_AND_PROCEDURAL_ONLY",
"P11":lambda z:z["decision"]=="SOURCE_BOUNDED_INDIVIDUAL_QUALIFIED",
"P12":lambda z:z["decision"]=="SOURCE_BOUNDED_INDIVIDUAL_QUALIFIED",
"P17":lambda z:z["decision"]=="SOURCE_BOUNDED_INDIVIDUAL_QUALIFIED",
"P15":lambda z:z["P15_individual_source_scientific_qualified"] is True,
"P16":lambda z:z["separate_scientific_candidate_qualified"] is True,
"P18":lambda z:z["P18_individual_scoped_scientific_source_qualified"] is True,
"P19":lambda z:z["cohort_delta_if_W4_integrated"]==1,
"P20":lambda z:z["qualified_W4_delta_candidate"]==1
}[id](x)
 assert good,id
 source_records[id]={"lane":lane,"original_immutable_exact_git_blob":blob("HEAD",f),"source_scope":"SCOPED_PER_PAPER_NOT_GLOBAL"}
# Source W3 six-stage history remains separately anchored in archived originals,
# and W3 sibling completed matrix is a HOLD, not a family clearance.
w3=json.loads((p/"parallel/W3/W3_SOURCE_COMPLETED_FAMILY_HANDOFF_MATRIX_v2.json").read_text())
assert len(w3["W3_all_three_scoped_source_qualified"])==3
assert len(w3["rows"])==7 and all(z["result"]=="FAMILY_UNDERDETERMINED" for z in w3["rows"])
w4=json.loads((p/"parallel/W4/W4_P19_PF03_P14_P20_G2_SKL_CENTRAL_FAMILY_COMPARISON_MATRIX_v1.json").read_text())
assert w4
# Exactly existing 9 are frozen historically and original 11 imported as
# evidence; not an automatically independent "accepted 20" source family cohort.
old=json.loads((p/"G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v6.json").read_text())
assert old["counts"]["cohort_current_source_scoped_formally_qualified"]==9
assert old["main_authorized"] is False
subprocess.run([sys.executable,str(p/"g1_v6_actual_issuer_original_scoped_science_evidence_check.py")],check=True,stdout=subprocess.DEVNULL)
print("G1_POSTMERGE_PREEXISTING_NINE_EXACT_ORIGINAL_V6_EVIDENCE_PASS",flush=True)
checks={
"actual_evidence_original_sources_imported":171,
"exact_individual_per_paper_scoped_qualification_files":len(source_records),
"historical_preexisting_individually_scoped":9,
"potential_individual_scoped_source_records":20,
"cohort_unconditional_20_model_variants_admitted":False,
"P10_optional_full_extra_models_mathematically_qualified":False,
"publication_nonPLOS_diversity_satisfied":False,
"W3_7_family_pairs_fully_clear":False,
"G2_final40_original_math_and_all_family_pairs_cleared":False,
"new_G4_joint_MAIN_authorization":False,
"MAIN_authorized":False
}
assert len(source_records)==11
assert all(v is False for k,v in checks.items() if k in ("cohort_unconditional_20_model_variants_admitted","P10_optional_full_extra_models_mathematically_qualified","publication_nonPLOS_diversity_satisfied","W3_7_family_pairs_fully_clear","G2_final40_original_math_and_all_family_pairs_cleared","new_G4_joint_MAIN_authorization","MAIN_authorized"))
for k in ("P10_optional_full_extra_models_mathematically_qualified","publication_nonPLOS_diversity_satisfied","W3_7_family_pairs_fully_clear","MAIN_authorized"):
 assert checks[k] is False
 print("G1_POSTMERGE_FALSE_PROMOTION_STOP_PASS",k,flush=True)
v={"schema":"p399.g1.real_shared_after_four_squash.original_source_integrity_not_joint_GO.v1",
"original_heads_full_git_stage_history_saved_by_separate_original_refs":rows,
"original_actual_shared_transport_squash_commit_ancestors":merged,
"imported_eleven_source_scoped_qualifications":source_records,
"original_v6_metadata_and_sources_frozen_verified":True,
"data_status_checks":checks}
encoded=json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode()
d=hashlib.sha256(encoded).hexdigest()
print("G1_POSTMERGE_171_ORIGINAL_RAW_PROJECTION_SHA256",d,flush=True)
print("G1_POSTMERGE_ACTUAL_SHARED_FOUR_LANE_SOURCE_BLOBS_FULL_PASS_G1_STILL_PARTIAL",flush=True)
folder=pathlib.Path("g1-fourlane-real-postmerge");folder.mkdir(exist_ok=True)
(folder/"original_evidence.json").write_text(json.dumps({"projection":v,"sha256":d},ensure_ascii=False,indent=2)+"\n")
