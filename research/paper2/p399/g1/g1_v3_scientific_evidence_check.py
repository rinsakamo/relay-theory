#!/usr/bin/env python3
"""G1 chronological v3: actual limited P09 scientific completion and fail-closed checks.

This validates raw frozen P09 stage files/Git ancestry and metadata-only
already executed publisher exact bytes receipts; does not pretend that
metadata SHA certifies source semantics, blind human reliability or FULL
PILOT20 scientific freeze.
"""
import hashlib,json,pathlib,subprocess,copy
P=pathlib.Path(__file__).resolve().parent
def raw(p):return (P/p).read_bytes()
def load(p):return json.loads(raw(p))
def sha(p):return hashlib.sha256(raw(p)).hexdigest()
old=load("G1_INDEPENDENT_EVIDENCE_SHA256_RECEIPT_v2.json")
physical=load("G1_ACTUAL_CLOUD_ORIGINAL_PDF_SHA_RECEIPTS_20261004.json")
v3=load("G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v3.json")
rem=load("G1_REMAINING_14_SCIENCE_BLOCKERS_v3.json")
handoff=load("G1_G2_LATEST_V3_P09_CNC_CROSS_LANE_DELTA.json")
p09=load("p09/P09_SEPARATE_BOUNDED_SCIENTIFIC_QUALIFICATION_20261004.json")
p07=load("p07/P07_SEPARATE_BOUNDED_SCIENTIFIC_QUALIFICATION_20261004.json")
assert old["evidence_projection_sha256"]=="1f111b38695e3925b20b30fed004d6522952c01761311b26b2dad9d98819f830"
assert sha("G1_ACTUAL_CLOUD_ORIGINAL_PDF_SHA_RECEIPTS_20261004.json")=="ba1e916d597a73ee9817903d6fabd91e4d13bd9c0b580f84bc334de9d90579ca"
def check(v3,rem,handoff,phy,p09):
 n=v3["counts"]
 assert n["historical_formally_source_qualified"]==4
 assert len(phy["rows"])==len(v3["additional"])==16 and len(rem["entries"])==14
 assert n["additional_original_publisher_pdf_bytes_acquired"]==16 and n["additional_publisher_original_html_fetched"]==16
 assert n["additional_scientifically_source_admitted"]==2
 assert n["additional_scientifically_attempted"]==2
 assert n["additional_all_A_E_completed"]==2
 assert n["additional_formal_bounded_qualified"]==2
 assert n["additional_not_yet_scientifically_attempted"]==14
 assert n["cohort_current_source_scoped_formally_qualified"]==6
 assert sorted(n["missing_primary_sampling_lanes"])==["ATT","LRN"]
 assert n["publication_selected_executed_PLOS"]==6
 assert not n["full_final_PILOT20_gate"] and not v3["main_authorized"]
 rows={x["id"]:x for x in v3["additional"]}
 assert len(rows)==16
 assert sorted(x["id"] for x in rem["entries"])==sorted(x for x in rows if x not in ("P07","P09"))
 for id,row in rows.items():
  p=next(x for x in phy["rows"] if x["id"]==id)
  assert p["pdf_sha256"]==row["publisher_pdf"]["raw_sha256"]
  assert p["pdf_original_bytes"]==row["publisher_pdf"]["bytes"]
  assert p["pdf_page_count"]==row["publisher_pdf"]["pages"]
  if id in ("P07","P09"):
   assert row["science"]["scientific_A"]=="COMPLETED_IMMUTABLE"
   assert "FORMALLY_QUALIFIED" in row["science"]["formal_qualification"]
  else:
   assert row["science"]["source_admission"]=="NOT_SOURCE_ADMITTED"
   assert row["science"]["scientific_A"]=="NOT_STARTED"
   assert row["science"]["formal_qualification"]=="NOT_QUALIFIED"
 assert p09["decision"]=="FORMALLY_QUALIFIED_SOURCE_STRUCTURAL_PROCEDURAL_ONLY_WITH_FINAL_PILOT20_G2_GENEALOGY_HOLD"
 assert p09["actual_after_E_independent_original_source_runner"]["run_id"]==37183782398
 assert p09["actual_after_E_independent_original_source_runner"]["conclusion"]=="SUCCESS"
 assert p09["actual_after_E_independent_original_source_runner"]["frozen_evidence_projection_sha256"]=="2a914a9660bd337c8921d034239496e99e8928a31af5b72e67dfd6115b6b5db6"
 assert p09["source_scientific_boundaries"] and p09["no_main_authorization"]
 assert handoff["G2_latest_working_40_slot_doi_order_unchanged_from_prior_v2"]
 assert handoff["current_20_pilot_vs_40_working_main_exact_doi_identity_pairs_checked"]==800
 assert handoff["current_exact_work_identity_collisions"]==0
 assert handoff["G2_latest_publisher_original_pdf_raw_byte_receipts"]==30
 assert handoff["G2_latest_final_original_full_semantic_admissions"]==0
 assert handoff["G2_latest_qualified_central_model_family_independent"]==0
 assert handoff["g1_did_not_edit_g2"]
 assert v3["replacement_history"]["executed_replacements"]==[]
 return True
check(v3,rem,handoff,physical,p09)
assert p07["disposition"]=="FORMALLY_QUALIFIED_SOURCE_STRUCTURAL_PROCEDURAL_WITH_G1_G2_FINAL_FAMILY_COLLISION_HOLD"
frozen_paths={"PRE_A":"p09/P09_PRE_A_SOURCE_EDITION_VARIANT_LINEAGE_v1.json","A":"p09/P09_PASS_A_SOURCE_FIRST_v1.json","B":"p09/P09_PASS_B_RESULT_INFORMED_FULL_A_v1.json","C":"p09/P09_PASS_C_SOURCE_CLOSED_C1_C2_v1.json","D":"p09/P09_PASS_D_UNCHANGED_GRAMMAR_v0_v1.json","E":"p09/P09_PASS_E_ORIGINAL_SOURCE_FIDELITY_v1.json"}
receipts={};prev=None
for x in p09["immutable_science_stages"]:
 label=x["stage"];path=frozen_paths[label];git=x["introduction_git_commit"];expected=x["raw_utf8_sha256"]
 original=subprocess.check_output(["git","show",f"{git}:research/paper2/p399/g1/{path}"],stderr=subprocess.STDOUT)
 assert original==raw(path),"SILENT_P09_STAGE_MUTATION "+label
 calc=hashlib.sha256(original).hexdigest()
 assert calc==expected, "P09_HISTORIC_STAGE_SHA_DRIFT "+label
 if prev:subprocess.run(["git","merge-base","--is-ancestor",prev,git],check=True)
 prev=git
 receipts[label]={"commit":git,"raw_utf8_sha256":calc}
 print("G1_V3_REVERIFIED_P09_STAGE",label,calc,flush=True)
A=load(frozen_paths["A"]);B=load(frozen_paths["B"]);C=load(frozen_paths["C"]);D=load(frozen_paths["D"]);E=load(frozen_paths["E"])
assert len(A["complete_A_source_claims"])==28 and len(A["complete_A_source_dependencies"])==36
assert B["inputs"]["full_original_A_object"]==A
assert C["C1_actual_full_entire_original_A_reopened_before_ANY_patch"]["original_A_unchanged"]==A
assert len(C["C2_source_local_negatives_all_reopened_and_exclusively_once"])==13
assert len(C["append_only_accepted_patches"])==3
assert len(D["complete_corrected_original_claim_mapping"])==28
assert len(D["all_original_source_dependencies"])==36
assert len(E["original_fidelity_targets"])==8
def reject(name,mutator):
 badv=copy.deepcopy(v3);badrem=copy.deepcopy(rem);badhand=copy.deepcopy(handoff);badphy=copy.deepcopy(physical);badp09=copy.deepcopy(p09)
 mutator(badv,badrem,badhand,badphy,badp09)
 try:check(badv,badrem,badhand,badphy,badp09)
 except AssertionError:print("G1_V3_NEGATIVE_REJECTED",name,flush=True);return
 raise RuntimeError("FALSELY_ACCEPTED "+name)
reject("FAKE_SIXTEEN_SCIENTIFICALLY_COMPLETED",lambda v,r,h,p,q:v["counts"].update({"additional_all_A_E_completed":16}))
reject("FAKE_P08_QUALIFICATION",lambda v,r,h,p,q:next(x for x in v["additional"] if x["id"]=="P08")["science"].update({"formal_qualification":"FORMALLY_QUALIFIED"}))
reject("TAMPER_P09_PUBLISHER_RAW_SHA",lambda v,r,h,p,q:next(x for x in p["rows"] if x["id"]=="P09").update({"pdf_sha256":"0"*64}))
reject("DOI_ONLY_FAKE_G2_CENTRAL_FAMILY_PASS",lambda v,r,h,p,q:h.update({"G2_latest_qualified_central_model_family_independent":40}))
reject("UNAUTHORIZED_P12_ELIFE_REPLACEMENT",lambda v,r,h,p,q:v["replacement_history"]["executed_replacements"].append("P12_ELIFE39497"))
files={
 "historical_v2_receipt":"G1_INDEPENDENT_EVIDENCE_SHA256_RECEIPT_v2.json",
 "original_16_real_physical_publisher_pdf_receipts":"G1_ACTUAL_CLOUD_ORIGINAL_PDF_SHA_RECEIPTS_20261004.json",
 "source_and_science_v3":"G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v3.json",
 "remaining_14":"G1_REMAINING_14_SCIENCE_BLOCKERS_v3.json",
 "g2_latest_v3_cnc_handoff":"G1_G2_LATEST_V3_P09_CNC_CROSS_LANE_DELTA.json",
 "p07_frozen_prior_qualified":"p07/P07_SEPARATE_BOUNDED_SCIENTIFIC_QUALIFICATION_20261004.json",
 "p09_new_frozen_formal_qualification":"p09/P09_SEPARATE_BOUNDED_SCIENTIFIC_QUALIFICATION_20261004.json",
 "p09_JA_science_report":"G1_P09_CNC_EXECUTED_AND_CURRENT_DENOMINATORS_JA_20261004.md",
}
files.update({"p09_"+k:p for k,p in frozen_paths.items()})
dig={k:sha(p) for k,p in files.items()}
for k,v in sorted(dig.items()):print("G1_V3_RAW_FILE_SHA256",k,v,flush=True)
proj={"schema":"p399.g1.six_of_twenty.scoped_raw_scientific_evidence_projection.v3","previous_actual_v2_projection_sha256":old["evidence_projection_sha256"],"current_raw_git_file_sha256":dig,"P09_six_immutable_stage_commits_and_sha":receipts,"original_P09_pdf_raw_sha256":p09["primary_original"]["sha256"],"verified_real_P09_postE_runner":37183782398,"old_four":4,"additional_new":2,"qualified_total":6,"G1":"G1_PARTIAL","main_authorized":False}
enc=json.dumps(proj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
proof=hashlib.sha256(enc).hexdigest()
print("G1_V3_EVIDENCE_PROJECTION_SHA256",proof,flush=True)
print("G1_V3_FINAL_METADATA_CHECK_SUCCESS actual originals16, scoped scientific new2, total6/20, fourteen unattempted, 5/5 destructive controls rejected",flush=True)
pathlib.Path("g1-v3-receipt").mkdir(exist_ok=True)
pathlib.Path("g1-v3-receipt/science-projection.json").write_text(json.dumps({"projection":proj,"canonical_sha256":proof,"semantic_science_ci_proven":False,"final20_frozen":False},ensure_ascii=False,indent=2)+"\n")
