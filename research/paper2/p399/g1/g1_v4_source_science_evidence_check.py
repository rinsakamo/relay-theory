#!/usr/bin/env python3
"""G1 v4 append-only source-scoped 7/20 evidence audit.

Runs actual prior v3 audit unchanged. Then verifies new P05 historical stage
bytes/Git ancestry, original raw physical metadata from completed real run and
v4 7/20 denominators. No new 16-original network downloads for JSON edits.
A physical independently repeated new P05 post-E original-source test passed
in dedicated run 37185342303 and is referenced by this consistency check.
"""
import json,hashlib,pathlib,subprocess,copy,sys
P=pathlib.Path(__file__).resolve().parent
subprocess.run([sys.executable,str(P/"g1_v3_scientific_evidence_check.py")],check=True)
load=lambda f:json.loads((P/f).read_text())
sha=lambda f:hashlib.sha256((P/f).read_bytes()).hexdigest()
V=load("G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v4.json")
R=load("G1_REMAINING_13_SCIENCE_BLOCKERS_v4.json")
Q=load("p05/P05_SEPARATE_BOUNDED_SCIENTIFIC_QUALIFICATION_20261004.json")
H=load("G1_G2_P05_ATT_FAMILY_HANDOFF_v4.json")
phys=load("G1_ACTUAL_CLOUD_ORIGINAL_PDF_SHA_RECEIPTS_20261004.json")
v3=load("G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v3.json")
def check(v,r,q,h):
 n=v["counts"]
 assert n["historical_formally_source_qualified"]==4
 assert len(v["additional"])==16 and len(r["entries"])==13
 assert n["additional_original_publisher_pdf_bytes_acquired"]==16
 assert n["additional_publisher_original_html_fetched"]==16
 assert n["additional_scientifically_source_admitted"]==3
 assert n["additional_scientifically_attempted"]==3
 assert n["additional_all_A_E_completed"]==3
 assert n["additional_formal_bounded_qualified"]==3
 assert n["additional_not_yet_scientifically_attempted"]==13
 assert n["cohort_current_source_scoped_formally_qualified"]==7
 assert n["publication_selected_executed_PLOS"]==7
 assert sorted(n["missing_primary_sampling_lanes"])==["LRN"]
 assert not n["full_final_PILOT20_gate"] and not v["main_authorized"]
 rows={x["id"]:x for x in v["additional"]}
 assert sorted(x["id"] for x in r["entries"])==sorted(x for x in rows if x not in ("P07","P09","P05"))
 for id,x in rows.items():
  source=next(z for z in phys["rows"] if z["id"]==id)
  assert x["publisher_pdf"]["raw_sha256"]==source["pdf_sha256"]
  assert x["publisher_pdf"]["bytes"]==source["pdf_original_bytes"]
  assert x["publisher_pdf"]["pages"]==source["pdf_page_count"]
  if id in ("P05","P07","P09"):
   assert x["science"]["scientific_A"]=="COMPLETED_IMMUTABLE"
   assert "FORMALLY_QUALIFIED" in x["science"]["formal_qualification"]
  else:
   assert x["science"]["scientific_A"]=="NOT_STARTED"
   assert x["science"]["source_admission"]=="NOT_SOURCE_ADMITTED"
   assert x["science"]["formal_qualification"]=="NOT_QUALIFIED"
 assert q["formal_bounded_decision"]=="FORMALLY_QUALIFIED_SOURCE_STRUCTURAL_PROCEDURAL_ONLY_WITH_DIRECT_2018_IVSN_ANCESTRY_AND_FINAL_G1_G2_FAMILY_HOLD"
 assert q["postE_real_independent_source_and_frozen_history"]["run"]==37185342303
 assert q["postE_real_independent_source_and_frozen_history"]["conclusion"]=="SUCCESS"
 assert q["postE_real_independent_source_and_frozen_history"]["evidence_projection_raw_sha256"]=="9c07192e68a8f64dc4a1ad1154f58a548aed3ac202f6ed4c1a0204d7046da4d5"
 assert len(q["frozen_stages"])==6
 assert not q["MAIN_authorized"]
 assert h["identical_pilot20_main40_DOI_pairs"]==0
 assert h["DOI_pairs_screened"]==800
 assert not h["full_family_800_completed"]
 assert not h["G2_known_counts"]["central_family_independence"]
 assert h["latest_G2_original_working_selected_slot_and_DOI_unchanged"]
 assert h["G2_known_counts"]["original_40_working_identifications"]==40
 assert h["G2_known_counts"]["publisher_PDF_original_bytes"]==30
 assert h["G1_only_no_G2_mutations"]
 assert v["replacement_history"]["executed_replacements"]==[]
 return True
assert check(V,R,Q,H)
frozen={"PRE_A":"P05_PRE_A_ORIGINAL_SOURCE_EDITION_AND_ANCESTRY_v1.json","A":"P05_PASS_A_SOURCE_FIRST_v1.json","B":"P05_PASS_B_RESULT_INFORMED_FULL_A_v1.json","C":"P05_PASS_C_SOURCE_CLOSED_C1_C2_v1.json","D":"P05_PASS_D_UNCHANGED_GRAMMAR_v0_v1.json","E":"P05_PASS_E_ORIGINAL_SOURCE_FIDELITY_v1.json"}
stageHashes={}
prev=None
for stage in Q["frozen_stages"]:
 key=stage["stage"];git=stage["original_introduction_commit"];name=frozen[key]
 old=subprocess.check_output(["git","show",f"{git}:research/paper2/p399/g1/p05/{name}"])
 assert old==(P/"p05"/name).read_bytes(),"P05 SOURCE STAGE MUTATION "+key
 got=hashlib.sha256(old).hexdigest()
 assert got==stage["raw_git_file_sha256"],"P05 STAGE FROZEN RAW SHA MISMATCH "+key
 if prev:subprocess.run(["git","merge-base","--is-ancestor",prev,git],check=True)
 prev=git
 stageHashes[key]={"git":git,"original_stage_sha256":got}
 print("G1_V4_P05_SCIENCE_RAW_GIT_HISTORY_PASS",key,got,flush=True)
A=load("p05/"+frozen["A"]);B=load("p05/"+frozen["B"]);C=load("p05/"+frozen["C"]);D=load("p05/"+frozen["D"]);E=load("p05/"+frozen["E"])
assert len(A["source_first_claims"])==30 and len(A["original_source_relations"])==42
assert B["entire_immutable_A_original_input"]==A
assert C["C1_full_entire_frozen_A_reopened_BEFORE_patches"]["A_original_object_in_full"]==A
assert len(C["C2_full_local_nearest_source_negatives_and_all_prior"])==17
assert len(C["append_only_C1_and_source_negative_C2_patches"])==3
assert len(D["source_typed_grammar_claims"])==30 and len(D["source_relation_coverage"])==42
assert len(E["original_source_fidelity_targets"])==8
def rejected(tag,mutate):
 v,r,q,h=map(copy.deepcopy,(V,R,Q,H));mutate(v,r,q,h)
 try:check(v,r,q,h)
 except AssertionError:print("G1_V4_NEGATIVE_REJECTED",tag,flush=True);return
 raise RuntimeError("FAILED_FAIL_CLOSED "+tag)
rejected("FAKE_ALL_SIXTEEN_DONE",lambda v,r,q,h:v["counts"].update({"additional_all_A_E_completed":16}))
rejected("FAKE_P06_QUALIFIED",lambda v,r,q,h:next(x for x in v["additional"] if x["id"]=="P06")["science"].update({"formal_qualification":"FORMALLY_QUALIFIED"}))
rejected("FAKE_P05_SOURCE_SHA",lambda v,r,q,h:next(x for x in v["additional"] if x["id"]=="P05")["publisher_pdf"].update({"raw_sha256":"0"*64}))
rejected("FALSE_800_FULL_FAMILY_CLEAR",lambda v,r,q,h:h.update({"full_family_800_completed":True}))
rejected("UNAUTHORIZED_ELIFE_REPLACEMENT",lambda v,r,q,h:v["replacement_history"]["executed_replacements"].append("P12_ELIFE.39497"))
files={
 "prior_source_science_v3":"G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v3.json",
 "prior_verified_v3_meta_receipt":"G1_INDEPENDENT_EVIDENCE_SHA256_RECEIPT_v3.json",
 "v4_science":"G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v4.json",
 "v4_13_remaining":"G1_REMAINING_13_SCIENCE_BLOCKERS_v4.json",
 "v4_G2_handoff":"G1_G2_P05_ATT_FAMILY_HANDOFF_v4.json",
 "v4_P05_qualification":"p05/P05_SEPARATE_BOUNDED_SCIENTIFIC_QUALIFICATION_20261004.json",
 "v4_P05_report_JA":"G1_P05_ATT_COMPLETION_AND_V4_DENOMINATORS_JA_20261004.md",
 "physical_source16_original":"G1_ACTUAL_CLOUD_ORIGINAL_PDF_SHA_RECEIPTS_20261004.json",
}
for stage,name in frozen.items():files["P05_"+stage]="p05/"+name
dig={tag:sha(file) for tag,file in files.items()}
for tag,hashvalue in sorted(dig.items()):print("G1_V4_FILE_SHA256",tag,hashvalue,flush=True)
proj={"schema":"p399.g1.v4.source_scoped.seven_of_twenty.actual_git_evidence_projection.v1","prior_v3_selected_sha256":"30ea4442eb643b15dc6727fbe0d8182383df8f004cfbf8b3f1d52f7efddd5562","real_postE_P05_original_source_run":37185342303,"postE_original_source_projection_sha256":"9c07192e68a8f64dc4a1ad1154f58a548aed3ac202f6ed4c1a0204d7046da4d5","files_exact_raw_sha":dig,"P05_frozen_git_historical_SHA":stageHashes,"new_qualified_3":["P07","P09","P05"],"qualified_7":7,"not_attempted_13":13,"G1":"G1_PARTIAL","MAIN":False}
digest=hashlib.sha256(json.dumps(proj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
print("G1_V4_CANONICAL_PROJECTION_SHA256",digest,flush=True)
print("G1_V4_ALL_PASS 7/20 scoped source structure; P05 six immutable original git stages; original physical receipt; 5/5 false-promotions rejected; LRN still unexecuted",flush=True)
pathlib.Path("g1-v4").mkdir(exist_ok=True)
pathlib.Path("g1-v4/receipt.json").write_text(json.dumps({"projection":proj,"canonical_sha256":digest,"not_final_20_semantic_freeze":True,"not_scientific_blinded_semantic_assessor":True},indent=2)+"\n")
