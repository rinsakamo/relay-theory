#!/usr/bin/env python3
"""G1 v2 reproducible source-scoped evidence verifier, not scientific semantic judge.

All stages have explicit historical immutable Git bytes and git chronology.
Only P07 added science; sixteen original physical acquisitions are inherited
from exact previous cloud source receipts (not silently re-downloaded here).
"""
import copy,hashlib,json,pathlib,subprocess
P=pathlib.Path(__file__).resolve().parent
def raw(n):return (P/n).read_bytes()
def j(n):return json.loads(raw(n))
def sha(n):return hashlib.sha256(raw(n)).hexdigest()
e=j("G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v2.json")
pdf=j("G1_ACTUAL_CLOUD_ORIGINAL_PDF_SHA_RECEIPTS_20261004.json")
html=j("G1_ACTUAL_PUBLISHER_HTML_BIBLIOGRAPHY_AND_CORRECTION_RECEIPT_20261004.json")
g2=j("G1_TO_G2_G4_WORKING_20X40_COLLISION_HANDOFF_v2.json")
qual=j("p07/P07_SEPARATE_BOUNDED_SCIENTIFIC_QUALIFICATION_20261004.json")
evidence={
 "v2_overlay":"G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v2.json",
 "physical_original_16":"G1_ACTUAL_CLOUD_ORIGINAL_PDF_SHA_RECEIPTS_20261004.json",
 "publisher_original_16":"G1_ACTUAL_PUBLISHER_HTML_BIBLIOGRAPHY_AND_CORRECTION_RECEIPT_20261004.json",
 "main_g2_handoff":"G1_TO_G2_G4_WORKING_20X40_COLLISION_HANDOFF_v2.json",
 "direct_ancestry":"G1_SOURCE_SUPPORTED_ANCESTRY_AND_G2_RISKS_v2.json",
 "p07_prea":"p07/P07_PRE_A_ORIGINAL_SOURCE_AND_LINEAGE_FREEZE_v1.json",
 "p07_A":"p07/P07_PASS_A_SOURCE_FIRST_v1.json",
 "p07_B":"p07/P07_PASS_B_RESULT_INFORMED_v1.json",
 "p07_C":"p07/P07_PASS_C_SOURCE_CLOSED_C1_C2_v1.json",
 "p07_D":"p07/P07_PASS_D_UNCHANGED_GRAMMAR_V0_v1.json",
 "p07_E":"p07/P07_PASS_E_ORIGINAL_SOURCE_FIDELITY_v1.json",
 "p07_qualification":"p07/P07_SEPARATE_BOUNDED_SCIENTIFIC_QUALIFICATION_20261004.json"
}
def verify(ov,pdf,html,g2,qual):
 c=ov["counts"]
 assert [c[k] for k in ["historical_formally_source_qualified","additional_original_publisher_pdf_bytes_acquired","additional_publisher_original_html_fetched","additional_scientifically_source_admitted","additional_scientifically_attempted","additional_all_A_E_completed","additional_formal_bounded_qualified","cohort_current_source_scoped_formally_qualified"]]==[4,16,16,1,1,1,1,5]
 assert len(ov["additional"])==16 and len({x["doi"] for x in ov["additional"]})==16
 assert len(pdf["rows"])==len(html["rows"])==16
 assert all(x["publisher_pdf"]["physical_bytes_acquired"] for x in ov["additional"])
 for x in ov["additional"]:
  pid=x["id"];rawrow=next(z for z in pdf["rows"] if z["id"]==pid)
  assert x["publisher_pdf"]["raw_sha256"]==rawrow["pdf_sha256"]
  assert x["publisher_pdf"]["bytes"]==rawrow["pdf_original_bytes"]
  assert x["publisher_pdf"]["pages"]==rawrow["pdf_page_count"]
  if pid!="P07":
   assert x["science"]["source_admission"]=="NOT_SOURCE_ADMITTED"
   assert x["science"]["scientific_A"]=="NOT_STARTED"
   assert x["science"]["formal_qualification"]=="NOT_QUALIFIED"
 assert qual["candidate"]["id"]=="P07"
 assert qual["disposition"]=="FORMALLY_QUALIFIED_SOURCE_STRUCTURAL_PROCEDURAL_WITH_G1_G2_FINAL_FAMILY_COLLISION_HOLD"
 assert qual["actual_separate_post_E_independent_original_publisher_pdf_review"]["conclusion"]=="SUCCESS"
 assert pdf["rows"][2]["id"]=="P07" and pdf["rows"][2]["pdf_sha256"]==qual["source"]["sha256"]
 assert g2["doi_pair_check_count"]==800 and g2["exact_same_work_doi_hits"]==0
 assert not g2["all_800_central_family_independent"]
 assert any(x["state"]=="EXACT_DOI_DOUBLE_RESERVED" for x in g2["additional_g1_handoff"])
 assert ov["replacement_history"]["executed_replacements"]==[]
 assert not ov["main_authorized"] and not c["full_final_PILOT20_gate"]
 assert not qual["cohort_reconciliation"]["main_authorized"]
 return True
verify(e,pdf,html,g2,qual)
stages=["PRE_A","A","B","C","D","E"]
files={}
previous=None
for phase in stages:
 ref=qual["frozen_stage_provenance"][phase]
 filename=evidence["p07_"+("prea" if phase=="PRE_A" else phase)]
 historical=subprocess.check_output(["git","show",ref["commit"]+":research/paper2/p399/g1/"+filename])
 actual=raw(filename)
 assert historical==actual, "Original frozen stage changed: "+phase
 actual_sha=hashlib.sha256(actual).hexdigest()
 assert actual_sha==ref["raw_sha256"],"G1 receipt SHA mismatch "+phase
 if previous:subprocess.check_call(["git","merge-base","--is-ancestor",previous,ref["commit"]])
 previous=ref["commit"]
 files[phase]={"git_commit":ref["commit"],"raw_file_sha256":actual_sha}
 print("G1_VERIFIED_STAGE",phase,actual_sha)
def rejected(kind,fn):
 try:fn()
 except AssertionError: print("G1_NEGATIVE_REJECTED",kind)
 else:raise RuntimeError("Negative incorrectly accepted "+kind)
bad=copy.deepcopy(e);bad["counts"]["additional_scientifically_attempted"]=16
rejected("FALSE_16_COMPLETED",lambda:verify(bad,pdf,html,g2,qual))
bad=copy.deepcopy(e);next(x for x in bad["additional"] if x["id"]=="P08")["science"]["formal_qualification"]="QUALIFIED"
rejected("FAKE_P08_ADMISSION",lambda:verify(bad,pdf,html,g2,qual))
bad=copy.deepcopy(g2);bad["all_800_central_family_independent"]=True
rejected("DOI_ONLY_FALSE_GENEALOGY",lambda:verify(e,pdf,html,bad,qual))
bad=copy.deepcopy(e);bad["replacement_history"]["executed_replacements"]=["P12_ALT_ELIFE"]
rejected("UNAUTHORIZED_ELIFE_BACKUP_REPLACEMENT",lambda:verify(bad,pdf,html,g2,qual))
checksums={alias:sha(filename) for alias,filename in evidence.items()}
for alias,h in sorted(checksums.items()):print("G1_V2_RAW_FILE_SHA256",alias,h)
projection={"schema":"relaytheory.p399.g1.scientific_receipt_projection.v2","raw_git_file_sha256":checksums,
 "p07_immutable_stage_proofs":files,"original_P07_pdf_sha256":qual["source"]["sha256"],
 "new_qualified":1,"old_qualified":4,"G1":"G1_PARTIAL","MAIN_authorized":False}
canonical=json.dumps(projection,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
digest=hashlib.sha256(canonical).hexdigest()
print("G1_V2_EVIDENCE_PROJECTION_SHA256",digest)
print("G1_V2_LEDGER_CONSISTENCY_PASS 16 physical, 1 new source admitted+qualified, 5/20 total; 4/4 negative controls rejected; MAIN_NO_GO")
pathlib.Path("g1-evidence-v2").mkdir(exist_ok=True)
pathlib.Path("g1-evidence-v2/receipt.json").write_text(json.dumps({"projection":projection,"canonical_projection_sha256":digest},ensure_ascii=False,indent=2)+"\n")
