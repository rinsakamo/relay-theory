#!/usr/bin/env python3
"""G1 v5 selected raw scientific source receipt: 8/20 truly individual,
main/S1 dual-original P13 and all 8 sampling primaries; fail-closed.

Re-executes immutable earlier v4 audit, verifies 6 original P13 Git
introduction bytes/ancestor order and current append-only source status.
Selected raw Git metadata and source-critical cloud exact publisher receipts
do NOT prove full PILOT20, publisher diversity, biological mechanism truth,
blinded independent human rater, or original model code numeric replay.
"""
import json,hashlib,pathlib,subprocess,copy,sys
P=pathlib.Path(__file__).resolve().parent
subprocess.run([sys.executable,str(P/"g1_v4_source_science_evidence_check.py")],check=True)
read=lambda f:json.loads((P/f).read_text())
sha=lambda f:hashlib.sha256((P/f).read_bytes()).hexdigest()
V=read("G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v5.json")
R=read("G1_REMAINING_12_INDEPENDENT_SCIENCE_BLOCKERS_v5.json")
Q=read("p13/P13_SEPARATE_BOUNDED_SCIENTIFIC_QUALIFICATION_20261004.json")
H=read("G1_G2_P13_LRN_SOURCE_PLUS_MANDATORY_S1_FAMILY_HANDOFF_v5.json")
PHY=read("G1_ACTUAL_CLOUD_ORIGINAL_PDF_SHA_RECEIPTS_20261004.json")
prev=read("G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v4.json")
def check(v,r,q,h):
 n=v["counts"]
 assert n["historical_formally_source_qualified"]==4
 assert n["additional_original_publisher_pdf_bytes_acquired"]==16
 assert n["additional_publisher_original_html_fetched"]==16
 assert n["additional_scientifically_source_admitted"]==4
 assert n["additional_scientifically_attempted"]==4
 assert n["additional_all_A_E_completed"]==4
 assert n["additional_formal_bounded_qualified"]==4
 assert n["additional_not_yet_scientifically_attempted"]==12
 assert n["cohort_current_source_scoped_formally_qualified"]==8 and n["planned_cohort"]==20
 assert n["publication_selected_executed_PLOS"]==8 and n["publication_selected_executed_other"]==0
 assert n["all_eight_primary_sampling_lanes_source_calibrated"] is True
 assert sorted(n["scientifically_executed_primary_sampling_lanes"])==sorted(["ATT","BLF","CNC","CTL","LRN","MEM","PRD","SKL"])
 assert n["missing_primary_sampling_lanes"]==[]
 assert n["source_scientifically_executed_extra_mandatory_same_publisher_S1"]==1
 assert not n["full_final_PILOT20_gate"] and not v["main_authorized"] and v["decision"]=="G1_PARTIAL"
 rows={x["id"]:x for x in v["additional"]}
 assert len(rows)==16 and len(r["entries"])==12
 assert sorted(x["id"] for x in r["entries"])==sorted(i for i in rows if i not in ("P07","P09","P05","P13"))
 for id,row in rows.items():
  old=next(x for x in PHY["rows"] if x["id"]==id)
  assert row["publisher_pdf"]["raw_sha256"]==old["pdf_sha256"]
  assert row["publisher_pdf"]["bytes"]==old["pdf_original_bytes"] and row["publisher_pdf"]["pages"]==old["pdf_page_count"]
  if id in ("P07","P09","P05","P13"):
   assert row["science"]["scientific_A"]=="COMPLETED_IMMUTABLE"
   assert "FORMALLY_QUALIFIED" in row["science"]["formal_qualification"]
  else:
   assert row["science"]["scientific_A"]=="NOT_STARTED"
   assert row["science"]["source_admission"]=="NOT_SOURCE_ADMITTED"
   assert row["science"]["formal_qualification"]=="NOT_QUALIFIED"
 assert rows["P13"]["required_original_S1_publisher_pdf"]["raw_sha256"]=="198eb18de66cca150dd233184781923680831f6e59007fec83ab54b5ec36453c"
 assert rows["P13"]["required_original_S1_publisher_pdf"]["pages"]==32
 assert q["individual_decision"]=="FORMALLY_QUALIFIED_SOURCE_STRUCTURAL_PROCEDURAL_ONLY_WITH_MAIN_PLUS_MANDATORY_S1_DUAL_ORIGINAL_AND_FINAL_G2_CENTRAL_FAMILY_HOLD"
 assert q["independent_after_E_real_dual_original_source_ci"]["conclusion"]=="SUCCESS"
 assert q["independent_after_E_real_dual_original_source_ci"]["run_id"]==37186503655
 assert q["independent_after_E_real_dual_original_source_ci"]["canonical_original_evidence_sha256"]=="5c2f4580269203b8d4a8895cc5fe304fea9b3ecab1eec62926b664746256599b"
 assert q["independent_after_E_real_dual_original_source_ci"]["two_original_publisher_main_plus_S1_source_page_anchor_checks"]=="16/16"
 assert q["cohort_after_this_decision"]["total_bounded_individually_qualified"]==8
 assert len(q["source_stages"])==6
 assert q["no_MAIN_authorization"] is True
 assert q["original_required_math_supplement"]["all32_supplement_pages_pictorially_read"] is False
 assert any("statistically distinguish" in x for x in q["core_source_specific_outcomes"])
 assert h["source_scoped_qualified_before_new_P13"]==7 and h["current_individually_bounded_qualified_after_P13"]==8
 assert h["twenty_candidate_PILOT_vs_40_working_MAIN_unchanged_DOI_pairs"]==800 and h["exact_DOI_work_identical"]==0
 assert not h["all_original_central_family_800_pair_independence_done"]
 assert h["G2_source_progress"]["central_family_independence_formal"]==0
 assert h["new_qualified_work"]["mandatory_original_issuer_S1_math_pdf_sha256"]=="198eb18de66cca150dd233184781923680831f6e59007fec83ab54b5ec36453c"
 assert h["main_scientific_outcomes_not_inspected"] and not h["p13_main_sci_executed"]
 assert v["replacement_history"]["executed_replacements"]==[]
 return True
assert check(V,R,Q,H)
frozen={"PRE_A":"P13_PRE_A_PUBLISHED_MAIN_PLUS_REQUIRED_ORIGINAL_S1_FAMILY_FREEZE_v1.json","A":"P13_PASS_A_MAIN_AND_S1_SOURCE_FIRST_v1.json","B":"P13_PASS_B_FULL_ORIGINAL_MAIN_S1_A_INFORMED_v1.json","C":"P13_PASS_C_SOURCE_CLOSED_C1_C2_v1.json","D":"P13_PASS_D_UNCHANGED_GRAMMAR_V0_v1.json","E":"P13_PASS_E_REAL_ORIGINAL_MAIN_S1_FIDELITY_v1.json"}
stageRaw={};prevCommit=None
for stage in Q["source_stages"]:
 name=stage["label"];git=stage["commit"];path="p13/"+frozen[name]
 old=subprocess.check_output(["git","show",f"{git}:research/paper2/p399/g1/{path}"])
 assert old==(P/path).read_bytes(),"SILENT_FROZEN_SCIENTIFIC_STAGE_MUTATION "+name
 calc=hashlib.sha256(old).hexdigest()
 assert calc==stage["original_raw_sha256"],"STAGE_HISTORICAL_SHA_DRIFT "+name
 if prevCommit:subprocess.run(["git","merge-base","--is-ancestor",prevCommit,git],check=True)
 prevCommit=git;stageRaw[name]={"commit":git,"raw_sha256":calc}
 print("G1_V5_P13_REAL_FROZEN_STAGE_PASS",name,calc,flush=True)
A=read("p13/"+frozen["A"]);B=read("p13/"+frozen["B"]);C=read("p13/"+frozen["C"]);D=read("p13/"+frozen["D"]);E=read("p13/"+frozen["E"])
assert A["A_original_claim_count"]==len(A["A_claims"])==34
assert A["A_source_dependency_count"]==len(A["A_source_dependencies"])==50
assert B["entire_original_A_object_unmodified"]==A
assert C["C1_full_original_frozen_A_input_REOPENED_BEFORE_PATCH"]["complete_original_A_object"]==A
assert len(C["C2_all_unique_adverse_conditions_from_original_main_S1"])==18
assert len(C["append_only_C1_accepted_original_source_patches"])==3
assert len(D["source_claim_mapping"])==34 and len(D["source_dependency_mapping"])==50
assert len(E["original_source_fidelity_targets"])==10
def negative(tag,fn):
 v,r,q,h=map(copy.deepcopy,(V,R,Q,H));fn(v,r,q,h)
 try:check(v,r,q,h)
 except AssertionError:print("G1_V5_FALSE_PROMOTION_REJECTED",tag,flush=True);return
 raise RuntimeError("FAIL_CLOSED_BROKEN "+tag)
negative("FAKE_ALL_16_SCIENTIFICALLY_QUALIFIED",lambda v,r,q,h:v["counts"].update({"additional_all_A_E_completed":16}))
negative("FAKE_UNADMITTED_P14_QUALIFIED",lambda v,r,q,h:next(x for x in v["additional"] if x["id"]=="P14")["science"].update({"formal_qualification":"FORMALLY_QUALIFIED"}))
negative("FAKE_MISSING_MANDATORY_S1_MATH_SHA",lambda v,r,q,h:next(x for x in v["additional"] if x["id"]=="P13")["required_original_S1_publisher_pdf"].update({"raw_sha256":"0"*64}))
negative("FAKE_PUBLISHER_DIVERSITY_PASS",lambda v,r,q,h:v["counts"].update({"publication_selected_executed_other":1}))
negative("FAKE_800_ORIGINAL_CENTRAL_FAMILY_PASS",lambda v,r,q,h:h.update({"all_original_central_family_800_pair_independence_done":True}))
negative("FAKE_EXPBIAS_DISTINGUISHED_FLEX_BAYES",lambda v,r,q,h:q.update({"core_source_specific_outcomes":[]}))
negative("UNAUTHORIZED_ELIFE_REPLACEMENT",lambda v,r,q,h:v["replacement_history"]["executed_replacements"].append("G1_P12_ELIFE39497"))
files={"old_v4_source_science":"G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v4.json","old_v4_independent_selected_raw_receipt":"G1_INDEPENDENT_EVIDENCE_SHA256_RECEIPT_v4.json","old_real_16_original_publisher_receipts":"G1_ACTUAL_CLOUD_ORIGINAL_PDF_SHA_RECEIPTS_20261004.json","v5_science_and_denominators":"G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v5.json","v5_remain12":"G1_REMAINING_12_INDEPENDENT_SCIENCE_BLOCKERS_v5.json","v5_G2_LRN_native_handoff":"G1_G2_P13_LRN_SOURCE_PLUS_MANDATORY_S1_FAMILY_HANDOFF_v5.json","v5_P13_new_separate_qualification":"p13/P13_SEPARATE_BOUNDED_SCIENTIFIC_QUALIFICATION_20261004.json","v5_JA_report":"G1_P13_LRN_REAL_MAIN_S1_QUALIFICATION_AND_V5_DENOMINATORS_JA_20261004.md","p13_physically_justified_S1_acquisition_runner":"p13/p13_preA_mandatory_math_supplement_original_probe.py","p13_actual_critical_S1_publisher_visual_runner":"p13/p13_original_s1_math_visual_probe.py","p13_real_dual_publisher_afterE_runner":"p13/p13_postE_independent_two_original_pdfs_six_stages.py"}
for k,name in frozen.items():files["P13_frozen_"+k]="p13/"+name
digests={tag:sha(file) for tag,file in files.items()}
for tag,d in sorted(digests.items()):print("G1_V5_RAW_SHA256",tag,d,flush=True)
proj={"schema":"p399.g1.v5.source_scoped.eight_of_twenty.actual_immutable_source_git.v1","historical_v4_actual_selected_sha256":"e91bb65e33cc48e053cf001c04b86e00a04299406afbffa35ab66f733f2d9370","actual_P13_source_plus_S1_publisher_dual_afterE_run":37186503655,"actual_P13_afterE_dual_source_projection_sha256":"5c2f4580269203b8d4a8895cc5fe304fea9b3ecab1eec62926b664746256599b","raw_git_selected_file_sha256":digests,"six_P13_frozen_original_stage_git_SHA":stageRaw,"new_completed_P07_P09_P05_P13":4,"all_primary_scientific_lanes_source_sampled":8,"scoped_individually_qualified":8,"planned_total":20,"remaining_original_science_not_yet_attempted":12,"G1":"G1_PARTIAL","MAIN":False}
signature=hashlib.sha256(json.dumps(proj,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode()).hexdigest()
print("G1_V5_CANONICAL_SELECTED_PROJECTION_SHA256",signature,flush=True)
print("G1_V5_METADATA_AND_IMMUTABLE_ORIGINAL_SCIENCE_PASS 8/20 individual scoped only; 12 source science unattempted; main+mandatory publisher S1 physical independently certified run; 7/7 destructive false claims rejected",flush=True)
pathlib.Path("g1-v5").mkdir(exist_ok=True)
pathlib.Path("g1-v5/evidence.json").write_text(json.dumps({"projection":proj,"selected_SHA256":signature,"source_semantic_human_blind_proven":False,"global_source_diversity_or_20_completed":False},indent=2)+"\n")
