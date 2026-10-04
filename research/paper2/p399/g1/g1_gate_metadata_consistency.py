#!/usr/bin/env python3
"""G1 metadata consistency / negative controls; cannot adjudicate source semantics."""
import copy,hashlib,json,re,sys
from pathlib import Path
DIR=Path(__file__).resolve().parent
def load(filename):
 return json.loads((DIR/filename).read_text(encoding="utf-8"))
def check(ledger,physical,ancestry,alternates):
 names={f"P{x:02d}" for x in range(5,21)}
 assert len(ledger["candidates"])==16 and {r["id"] for r in ledger["candidates"]}==names
 assert len(physical["rows"])==16 and {r["id"] for r in physical["rows"]}==names
 assert all(not r["original_primary_frozen_for_A"] and r["scientific_attempt"]=="NOT_STARTED" for r in ledger["candidates"])
 assert all(r["scientific_qualification"]=="NOT_QUALIFIED" for r in ledger["candidates"])
 assert ledger["baseline_original_four"]["qualified_count"]==4
 original_sha={x["id"]:x["original_pdf_sha256"] for x in ledger["baseline_original_four"]["refs"]}
 assert len(original_sha)==4
 assert original_sha["PF01"]=="8531103d577a3249c7edffa06ef2a8a7e85eb01b0a2f02cee2145e187581fbc3"
 assert original_sha["PF02"]=="bef58465c56cec93f1cbb0f689c8fcd48cd656f3520d70a6032aaac9caa63655"
 assert original_sha["PF03"]=="62d744125034ce834692cdb210065d34e2bbd0f58c9eb3387ed2d75dfb7f77ae"
 assert original_sha["PF04"]=="bc84d4827df202cf5051cf10aa64cc09673b718af2acd31441a3712bcd376df9"
 assert physical["run_id"]==37178895352
 assert physical["actual_workflow_conclusion"]=="success"
 assert physical["new_formal_source_admissions"]==0 and physical["new_scientific_qualifications"]==0
 sha=set()
 for rec in physical["rows"]:
  assert rec["pdf_original_bytes"]>100000 and rec["pdf_page_count"]>=8
  assert re.fullmatch("[0-9a-f]{64}",rec["pdf_sha256"])
  assert rec["pdf_sha256"] not in sha
  sha.add(rec["pdf_sha256"])
  assert rec["official_article_html_request_success"] and rec["network_errors"]==0
  candidate=next(x for x in ledger["candidates"] if x["id"]==rec["id"])
  assert candidate["doi"] in rec["publisher_original_pdf_url"]
  if rec["id"] in ("P08","P10"): assert rec["correction_request_success"] is True
 pf=ancestry["all_remaining_pairs_by_review_scope"]["pilot_vs_pf"]
 inter=ancestry["all_remaining_pairs_by_review_scope"]["additional_pilot_interpairs"]
 main=ancestry["all_remaining_pairs_by_review_scope"]["against_known_main_seeds"]
 assert len(pf["pairs"])+sum(1 for x in ancestry["named_source_grounded_relations"] if x["a"] in names and x["b"].startswith("PF"))==16*4
 assert len(inter["pairs"])+sum(1 for x in ancestry["named_source_grounded_relations"] if x["a"] in names and x["b"] in names)==16*15//2
 assert len(main["pairs"])==16*10 and main["default_classification"]=="UNDERDETERMINED"
 assert alternates["actual"]["P12_eLife39497"]["real_raw_bytes_acquired"] is True
 assert alternates["actual"]["P12_eLife39497"]["pdf_pages"]==23
 assert len([x for x in alternates["actual"].values() if x.get("real_raw_bytes_acquired",False)])==1
 assert all(x["prospective_replacement"]=="NOT_ADOPTED" for x in alternates["actual"].values())
 return True

if __name__=="__main__":
 l=load("G1_PILOT20_RECONCILED_SOURCE_AND_FAMILY_LEDGER_v1.json")
 r=load("G1_ACTUAL_CLOUD_ORIGINAL_PDF_SHA_RECEIPTS_20261004.json")
 f=load("G1_MODEL_FAMILY_AND_ANCESTRY_MATRIX_v1.json")
 a=load("G1_CROSS_PUBLISHER_PROBE_RESULTS_20261004.json")
 check(l,r,f,a)
 print("PASS G1 manifest exact count, original-PF boundaries, 16 original PDF metadata, 2 corrections, 160 MAIN seed unknowns, single acquired eLife alternative")
 def reject(name,lm,pm,fm,am):
  try:check(lm,pm,fm,am)
  except AssertionError:print("PASS negative control (rejected):",name)
  else:raise RuntimeError("FAIL negative control unexpectedly ACCEPTED: "+name)
 tam=copy.deepcopy(r);tam["rows"][0]["pdf_sha256"]="unknown"
 reject("invalid source SHA",l,tam,f,a)
 tam=copy.deepcopy(l);tam["candidates"][0]["original_primary_frozen_for_A"]=True
 reject("faked source admission",tam,r,f,a)
 tam=copy.deepcopy(r);next(x for x in tam["rows"] if x["id"]=="P08")["correction_request_success"]=False
 reject("suppressed correction",l,tam,f,a)
 tam=copy.deepcopy(r);tam["rows"][1]["pdf_sha256"]=tam["rows"][0]["pdf_sha256"]
 reject("duplicate source raw bytes",l,tam,f,a)
 digest_input={"candidate_ids":[x["id"] for x in l["candidates"]],
  "pf_sha256":{x["id"]:x["original_pdf_sha256"] for x in l["baseline_original_four"]["refs"]},
  "new_source_sha256":{x["id"]:x["pdf_sha256"] for x in r["rows"]},
  "new_source_pdf_pages":{x["id"]:x["pdf_page_count"] for x in r["rows"]},
  "corrections":["P08:10.1371/journal.pcbi.1005908","P10:10.1371/journal.pcbi.1010775"],
  "alt_pdf_sha256":a["actual"]["P12_eLife39497"]["publisher_original_pdf_sha256"],
  "added_qualified":0,"G1":"G1_PARTIAL"}
 canonical=json.dumps(digest_input,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
 print("G1 source receipt projection SHA256",hashlib.sha256(canonical).hexdigest())
 print("G1 status G1_PARTIAL; original 4 qualified; 16 new raw-PDF physically accessible; ZERO new scientific qualifications; no scientific validation claimed")
