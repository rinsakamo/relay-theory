#!/usr/bin/env python3
"""G1 chronological v6 limited 9/20 real original source evidence audit.

Run previous v5 actual independent selected raw scientific proof. Recompute
v6 current source counts only after P14 full original PRE_A-E source-qualified
7-publisher-original afterE physical CI. Independently verify exact P14
six original immutable Git stage bytes and their ancestor order, original
source identities, selected 20 raw evidence files and destructive checks.
This verifies provenance/selected anchors, NOT model-semantic human blinded
validity nor 20-paper scientific diversity/final joint authorization.
"""
import pathlib,hashlib,json,subprocess,copy,sys
P=pathlib.Path(__file__).resolve().parent
subprocess.run([sys.executable,str(P/"g1_v5_actual_original_scientific_evidence_check.py")],check=True)
read=lambda p:json.loads((P/p).read_text())
sha=lambda p:hashlib.sha256((P/p).read_bytes()).hexdigest()
V=read("G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v6.json")
R=read("G1_REMAINING_11_INDEPENDENT_SCIENCE_BLOCKERS_v6.json")
Q=read("p14/P14_SEPARATE_BOUNDED_ORIGINAL_SCIENCE_QUALIFICATION_20261004.json")
H=read("G1_G2_V6_P14_SECOND_LRN_ORIGINAL_FAMILY_HANDOFF.json")
PHY=read("G1_ACTUAL_CLOUD_ORIGINAL_PDF_SHA_RECEIPTS_20261004.json")
def check(v,r,q,h):
 n=v["counts"]
 assert n["historical_formally_source_qualified"]==4
 assert n["additional_original_publisher_pdf_bytes_acquired"]==16 and n["additional_publisher_original_html_fetched"]==16
 assert n["additional_scientifically_source_admitted"]==5 and n["additional_scientifically_attempted"]==5
 assert n["additional_all_A_E_completed"]==5 and n["additional_formal_bounded_qualified"]==5
 assert n["additional_not_yet_scientifically_attempted"]==11 and n["cohort_current_source_scoped_formally_qualified"]==9
 assert n["planned_cohort"]==20 and n["publication_selected_executed_PLOS"]==9 and n["publication_selected_executed_other"]==0
 assert n["original_extra_same_publisher_required_P14_supplements"]==6
 assert n["all_eight_primary_sampling_lanes_source_calibrated"] is True
 assert sorted(n["scientifically_executed_primary_sampling_lanes"])==sorted(["ATT","BLF","CNC","CTL","LRN","MEM","PRD","SKL"])
 assert n["missing_primary_sampling_lanes"]==[]
 assert not n["full_final_PILOT20_gate"] and not v["main_authorized"] and v["decision"]=="G1_PARTIAL"
 rows={x["id"]:x for x in v["additional"]}
 assert len(rows)==16 and len(r["entries"])==11
 assert sorted(x["id"] for x in r["entries"])==sorted(i for i in rows if i not in ("P05","P07","P09","P13","P14"))
 for name,row in rows.items():
  orig=next(x for x in PHY["rows"] if x["id"]==name)
  assert row["publisher_pdf"]["raw_sha256"]==orig["pdf_sha256"]
  assert row["publisher_pdf"]["bytes"]==orig["pdf_original_bytes"]
  assert row["publisher_pdf"]["pages"]==orig["pdf_page_count"]
  if name in ("P05","P07","P09","P13","P14"):
   assert row["science"]["scientific_A"]=="COMPLETED_IMMUTABLE"
   assert "FORMALLY_QUALIFIED" in row["science"]["formal_qualification"]
  else:
   assert row["science"]["scientific_A"]=="NOT_STARTED"
   assert row["science"]["source_admission"]=="NOT_SOURCE_ADMITTED"
   assert row["science"]["formal_qualification"]=="NOT_QUALIFIED"
 supp=rows["P14"]["mandatory_issuer_original_supplements_p14"]
 assert len(supp)==6 and {x["id"] for x in supp}=={"S1","S2","S3","S4","S5","S6"}
 assert next(x for x in supp if x["id"]=="S3")["raw_sha256"]=="82f2a03519e5718428303158c27caf21b39937b9841a7581a40eb15901eb2be2"
 assert q["decision"]=="FORMALLY_QUALIFIED_SOURCE_STRUCTURAL_PROCEDURAL_ONLY_WITH_ORIGINAL_PUBLISHED_MAIN_S1_S6_AND_FINAL_FAMILY_DIVERSITY_HOLD"
 assert q["actual_real_independent_after_E_source_and_procedure"]["cloud_run"]==37188868874
 assert q["actual_real_independent_after_E_source_and_procedure"]["conclusion"]=="SUCCESS"
 assert q["actual_real_independent_after_E_source_and_procedure"]["actual_same_published_publisher_original_pdf_SHA_bytes_pages"]=="7/7"
 assert q["actual_real_independent_after_E_source_and_procedure"]["original_source_narrow_paper_and_supplement_text_anchors"]=="21/21"
 assert q["actual_real_independent_after_E_source_and_procedure"]["selected_nonrecursive_sha256"]=="eb21084eca2f417e61dfc12100c8c2f05212dacb5d8034a23486d36db8a35fec"
 assert q["cohort_at_time"]["total_source_scoped_qualified"]==9
 assert len(q["frozen_actual_stage_provenance"])==6
 assert q["MAIN_authorized"] is False
 assert q["adopted_original_sources"]["not_adopted_anatomical_S1_Fig_original_s007"]
 assert any("22/25" in s for s in q["source_scoped_scientific_findings"])
 assert h["new_additional_scientific_A_E_done"]==5 and h["new_remaining_scientifically_unattempted"]==11
 assert h["G2_actual_source_progress"]["source_native_central_family_scientifically_qualified"]==0
 assert h["current_working_20x40_identical_DOI_identity_pairs_screened"]==800
 assert h["current_identical_DOI_pairs"]==0 and not h["full_native_800_independence_proven"]
 assert not h["G2_branch_writes"] and not h["G2_MAIN_Grammar_scientific_reconstruction_read"]
 assert v["replacement_history"]["executed_replacements"]==[]
 return True
assert check(V,R,Q,H)
frozen={
 "PRE_A":"P14_PRE_A_PUBLISHED_MAIN_AND_ISSUER_S1_S6_SOURCE_FAMILY_FREEZE_v1.json",
 "A":"P14_PASS_A_SOURCE_FIRST_MAIN_S1_S6_v1.json",
 "B":"P14_PASS_B_RESULT_INFORMED_FULL_A_ALL_ORIGINALS_v1.json",
 "C":"P14_PASS_C1_C2_ORIGINAL_SOURCE_CLOSED_v1.json",
 "D":"P14_PASS_D_UNCHANGED_GRAMMAR_v0_39_56_v1.json",
 "E":"P14_PASS_E_ORIGINAL_MAIN_AND_S1_S6_FIDELITY_v1.json"}
stageproof={};prev=None
for stage in Q["frozen_actual_stage_provenance"]:
 n=stage["stage"];git=stage["original_git_introduction"];name=frozen[n];p="p14/"+name
 original=subprocess.check_output(["git","show",f"{git}:research/paper2/p399/g1/{p}"])
 assert original==(P/p).read_bytes(),"P14_FROZEN_SCIENCE_STAGE_MUTATED "+n
 calc=hashlib.sha256(original).hexdigest()
 assert calc==stage["original_raw_git_utf8_sha256"],"P14_FROZEN_GIT_STAGE_SHA_DRIFT "+n
 if prev:subprocess.run(["git","merge-base","--is-ancestor",prev,git],check=True)
 prev=git;stageproof[n]={"git":git,"raw_sha256":calc}
 print("G1_V6_P14_REAL_IMMUTABLE_ORIGINAL_STAGE_PASS",n,calc,flush=True)
A=read("p14/"+frozen["A"]);B=read("p14/"+frozen["B"]);C=read("p14/"+frozen["C"]);D=read("p14/"+frozen["D"]);E=read("p14/"+frozen["E"])
assert len(A["source_first_claims"])==39 and len(A["source_conditional_dependencies"])==56
assert B["complete_original_immutable_A_embedded_before_reviews"]==A
assert C["C1_original_FROZEN_complete_A_reopened_BEFORE_ANY_PATCH"]["complete_entire_original_A"]==A
assert len(C["accepted_append_only_material_source_clarifications"])==3
assert len(C["C2_full_unfavorable_source_local_conditions_one_canonical_each"])==19
assert len(D["full_source_claim_39_mapping"])==39 and len(D["original_56_source_dependencies"])==56
assert E["full_source_claim_coverage"]==39 and E["all_C_material_source_negatives_unique_covered"]==19
assert len(E["original_source_specific_fidelity_targets"])==9
def negative(name,mutator):
 v,r,q,h=map(copy.deepcopy,(V,R,Q,H));mutator(v,r,q,h)
 try:check(v,r,q,h)
 except AssertionError:print("G1_V6_FALSE_SOURCE_OR_COMPLETION_REJECTED",name,flush=True);return
 raise RuntimeError("FALSE_ACCEPT "+name)
negative("FAKE_16_NEW_SCIENCE_DONE",lambda v,r,q,h:v["counts"].update({"additional_all_A_E_completed":16}))
negative("FAKE_P06_SCIENCE_QUALIFIED",lambda v,r,q,h:next(x for x in v["additional"] if x["id"]=="P06")["science"].update({"formal_qualification":"FORMALLY_QUALIFIED"}))
negative("FAKE_P14_ISSUER_ORIGINAL_S3_SHA",lambda v,r,q,h:next(x for x in v["additional"] if x["id"]=="P14")["mandatory_issuer_original_supplements_p14"][2].update({"raw_sha256":"0"*64}))
negative("FAKE_ALL_P14_ANATOMICAL_SOURCE_COVERED",lambda v,r,q,h:q["adopted_original_sources"].update({"not_adopted_anatomical_S1_Fig_original_s007":""}))
negative("FAKE_P14_25_SCANNED_SOURCE_POPULATION",lambda v,r,q,h:q.update({"source_scoped_scientific_findings":[]}))
negative("FAKE_PUBLISHER_DIVERSITY",lambda v,r,q,h:v["counts"].update({"publication_selected_executed_other":1}))
negative("FAKE_800_G2_ORIGINAL_CENTRAL_FAMILY_PASS",lambda v,r,q,h:h.update({"full_native_800_independence_proven":True}))
negative("UNAUTHORIZED_P12_ELIFE_BACKUP",lambda v,r,q,h:v["replacement_history"]["executed_replacements"].append("G1_P12_ELIFE39497"))
files={
 "prior_v5_original_source_science":"G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v5.json",
 "prior_v5_raw_evidence_receipt":"G1_INDEPENDENT_EVIDENCE_SHA256_RECEIPT_v5.json",
 "prior_sixteen_actual_original_pdf_acquisition":"G1_ACTUAL_CLOUD_ORIGINAL_PDF_SHA_RECEIPTS_20261004.json",
 "v6_source_science":"G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v6.json",
 "v6_eleven_remaining":"G1_REMAINING_11_INDEPENDENT_SCIENCE_BLOCKERS_v6.json",
 "v6_G2_source_family_handoff":"G1_G2_V6_P14_SECOND_LRN_ORIGINAL_FAMILY_HANDOFF.json",
 "v6_P14_separate_bounded_qualification":"p14/P14_SEPARATE_BOUNDED_ORIGINAL_SCIENCE_QUALIFICATION_20261004.json",
 "v6_P14_complete_Japanese_report":"G1_P14_SECOND_LRN_COMPLETION_V6_DENOMINATORS_JA_20261004.md",
 "P14_original_issuer_S2_S5_physical_probe":"p14/p14_preA_original_issuer_supplement_source_probe.py",
 "P14_original_issuer_S1_S6_physical_probe":"p14/p14_preA_publisher_original_S1_S6_probe.py",
 "P14_original_math_main_S2_S5_visual_runner":"p14/p14_main_and_S2_S5_visual_critical_math_probe.py",
 "P14_original_negative_S1_S6_visual_runner":"p14/p14_original_negative_S1_and_stimulus_S6_visual.py",
 "P14_after_E_seven_real_issuer_source_runner":"p14/p14_after_E_seven_exact_original_sources_six_git_stages.py"
}
for n,filename in frozen.items():files["P14_frozen_"+n]="p14/"+filename
raw={k:sha(p) for k,p in files.items()}
for k,v in sorted(raw.items()):print("G1_V6_SELECTED_RAW_GIT_FILE_SHA",k,v,flush=True)
projection={"schema":"p399.g1.v6.selected_source_scoped.nine_of_twenty.current_raw_and_original_immutable_P14","prior_v5_evidence_sha":"9f9fa58c135d7054a7eb8284bec608054ec6996b3c0e34d91c0cd1411fa33687","P14_afterE_actual_7_genuine_issuer_pdf_run":37188868874,"P14_actual_7_issuer_afterE_source_projection_sha":"eb21084eca2f417e61dfc12100c8c2f05212dacb5d8034a23486d36db8a35fec","current_selected_git_file_raw_sha":raw,"original_P14_six_science_stage_provenance":stageproof,"source_scoped_qualified":9,"original_total":20,"unattempted_new":11,"complete_science_primary_lanes":8,"full_joint_PILOT20":False,"MAIN":False}
digest=hashlib.sha256(json.dumps(projection,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
print("G1_V6_ACTUAL_SELECTED_SOURCE_EVIDENCE_SHA256",digest,flush=True)
print("G1_V6_ALL_PASS 9/20 real individually source-scoped only; afterE publisher7 original/21 content anchors historical; all P14 6 frozen real Git stage original raw provenance, false source/family/publisher promotions 8/8 rejected",flush=True)
pathlib.Path("g1-v6").mkdir(exist_ok=True)
pathlib.Path("g1-v6/projection.json").write_text(json.dumps({"projection":projection,"selected_actual_sha":digest,"blinded_independent_human_semantic_or_model_numeric_replay_proven":False,"full_PILOT20_main_authorization":False},indent=2)+"\n")
