#!/usr/bin/env python3
"""G1 v7 source-integrity + never auto-promote MAIN evidence-only audit."""
import pathlib,json,subprocess,re,sys,copy
P=pathlib.Path(__file__).resolve().parents[1]
x=json.loads((P/"G1_FOUR_LANE_SOURCE_EVIDENCE_INTEGRATED_GLOBAL_ADMISSION_HOLDS_v7.json").read_text())
z=subprocess.run([sys.executable,str(P/"integration/g1_fourlane_actual_postmerge_exact_source_171_verifier.py")],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
if z.returncode:
 print(z.stdout[-9000:],flush=True)
 raise AssertionError("source provenance independent postmerge failed")
m=re.search(r"G1_POSTMERGE_171_ORIGINAL_RAW_PROJECTION_SHA256 ([a-f0-9]{64})",z.stdout)
assert m and m.group(1)==x["actual_source_evidence_integrity"]["actual_postmerge_provenance_projection_SHA256"]
assert x["actual_source_evidence_integrity"]["all_actual_squash_transport_commits_in_common_history"]
assert x["actual_source_evidence_integrity"]["original_171_git_file_raw_blobs_match_all_original_stage_branch_heads"]=="171/171"
assert x["actual_source_evidence_integrity"]["eleven_exact_distinct_new_limited_source_scoped_individual_qualification_files"]=="11/11"
assert x["actual_source_evidence_integrity"]["W3_exact_original_genuine_scoped_complete"]=="3/3"
assert x["actual_source_evidence_integrity"]["W3_original_native_family_risk_pair_records"]=="7/7 FAMILY_UNDERDETERMINED"
assert x["reconciled_provenance_numbers"]["already_historically_source_scoped_individual_qualified"]==9
assert x["reconciled_provenance_numbers"]["additional_eleven_exact_individual_limited_science_evidence_present"]==11
assert x["reconciled_provenance_numbers"]["all_20_individual_SOURCE_SCOPED_qualification_files_in_shared_G1_evidence"]==20
assert len(x["individual_source_limited_evidence_imported_11"])==11
assert len(x["actual_shared_common_four_squash_science_evidence_transport_commits"])==4
assert sorted(y["paper"] for y in x["individual_source_limited_evidence_imported_11"])==sorted(["P06","P08","P10","P11","P12","P17","P15","P16","P18","P19","P20"])
assert x["reconciled_provenance_numbers"]["source_original_primary_PLOS_present"]==20
assert x["reconciled_provenance_numbers"]["scientifically_admitted_nonPLOS_primary"]==0
assert x["formal_scientific_admission_status"]["original_primary_source_20_full_all_model_variants_eligibility"]=="HOLD_P10_SCOPE"
assert x["formal_scientific_admission_status"]["native_model_family_unique_independence_for_selected_20"]=="UNDERDETERMINED"
assert x["formal_scientific_admission_status"]["original_all_20_published_primary_publisher_diversity"].startswith("FAIL")
assert x["formal_scientific_admission_status"]["G4_independent_new_joint_audit"].startswith("NOT_COMPLETED")
assert x["global_G1_status"]=="G1_SCIENCE_EVIDENCE_INTEGRATED_BUT_FINAL_QUALIFICATION_HOLD"
assert x["G1_PARTIAL"] is True and x["MAIN_authorized"] is False
negative=[
 ("FAKE_W3_FULL_MODEL_FAMILY_CLEAR",lambda v:v["formal_scientific_admission_status"].update({"W3_family_7_pairs":"ALL_CLEARED"})),
 ("FAKE_NONPLOS_SOURCE_DIVERSITY",lambda v:v["reconciled_provenance_numbers"].update({"scientifically_admitted_nonPLOS_primary":1})),
 ("FAKE_20_FULL_VARIANTS",lambda v:v["formal_scientific_admission_status"].update({"original_primary_source_20_full_all_model_variants_eligibility":"PASS"})),
 ("FAKE_AUTHOR_MAIN_GO",lambda v:v.update({"MAIN_authorized":True})),
]
def invariant(v):
 assert v["formal_scientific_admission_status"]["W3_family_7_pairs"]=="ALL_FAMILY_UNDERDETERMINED"
 assert v["reconciled_provenance_numbers"]["scientifically_admitted_nonPLOS_primary"]==0
 assert v["formal_scientific_admission_status"]["original_primary_source_20_full_all_model_variants_eligibility"]=="HOLD_P10_SCOPE"
 assert v["MAIN_authorized"] is False
for name,mut in negative:
 test=copy.deepcopy(x);mut(test)
 try:invariant(test)
 except AssertionError:print("G1_POSTMERGE_V7_FALSE_PROMOTION_REJECTED",name,flush=True);continue
 raise RuntimeError("false claim accepted "+name)
print("G1_POSTMERGE_V7_REAL_171_ORIGINALS_AND_SCOPED_20_SOURCE_FILES_PASS",m.group(1),flush=True)
print("G1_POSTMERGE_V7_GLOBAL_ADMISSION_AND_MAIN_STILL_BLOCKED",flush=True)
