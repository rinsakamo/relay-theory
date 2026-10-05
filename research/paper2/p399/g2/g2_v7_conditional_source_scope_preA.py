#!/usr/bin/env python3
"""G2: two specific conditional firstparty PLOS media scope checks.
ATT-B1 S3 is separate publisher-owned supplement referred to as DEFINING,
NOT retroactively inserted into source unless preregistered eligibility resolved.
PRD-B2 is PREDECLARED second-priority backup only; NOT automatically selected.
"""
import concurrent.futures,datetime,hashlib,io,json,os,re,urllib.request
from pathlib import Path
from pypdf import PdfReader
H={"User-Agent":"RelayTheory-G2-exact-source-scope-preA (university research, no content redistribution)","Accept":"application/pdf,text/html,*/*"}
TARGET={
"ATT-B1-OFFICIAL-DEFINING-S3":{"doi":"10.1371/journal.pcbi.1011283","target":"https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1011283.s003&type=supplementary","expected_origin":"PLOS separate linked SH-CoR model-defining S3 EqS1–S19, outside primary article","backup":"ATT-B1","secondary_publisher_source":True},
"PRD-B2-SECOND-PREDECLARED":{"doi":"10.1371/journal.pcbi.1009557","target":"https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1009557&type=printable","expected_origin":"Official PLOS whole published original PDF, 2nd-ranked shared PRD/BLF/LRN candidate","backup":"PRD-B2","secondary_publisher_source":False}
}
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=35) as f:
  return f.read(28*1024*1024),f.geturl(),f.headers.get("Content-Type"),f.status
def one(it):
 sid,d=it;v={"slot":sid,"parent_backup":d["backup"],"doi":d["doi"],"official_request":d["target"],"is_separately_linked_original_supplement":d["secondary_publisher_source"],"original_raw_pdf_verified":False,"full_math_figures_variants_scientifically_reviewed":False,"backup_scientifically_eligible":False,"backup_activated":False}
 try:
  blob,url,ct,status=get(d["target"])
  assert blob.startswith(b"%PDF-"),"PLOS official delivery not PDF"
  rd=PdfReader(io.BytesIO(blob),strict=False);part=" ".join((p.extract_text() or "") for p in rd.pages[:2]).lower()
  alltext=" ".join((p.extract_text() or "") for p in rd.pages).lower()
  v.update(real_url=url,http_status=status,content_type=ct,source_sha256=hashlib.sha256(blob).hexdigest(),source_bytes=len(blob),pages=len(rd.pages),
    first_2_page_extracted_text_sha256=hashlib.sha256(part.encode()).hexdigest(),
    first2_doi_direct_extracted=d["doi"] in part,
    first2_title_tokens={word:word in part for word in (["computational","modelling","modeling","selection","history"] if d["secondary_publisher_source"] else ["task-induced","neural","covariability","learning","bayesian"])},
    contains_any_eq_s1="s1" in alltext,contains_any_eq_s19="s19" in alltext,
    firstpage_text_chars=len(part),full_pdf_extractable_chars=len(alltext),original_raw_pdf_verified=True)
 except Exception as e:v["failure_reason"]=repr(e)[:240]
 return v
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:out=list(ex.map(one,TARGET.items()))
r={"schema":"relaytheory.p399.g2.v7.conditional_publisher_source_original_supplement_PREA_only","runner_sha":os.getenv("GITHUB_SHA"),"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "source_acquisition_only":True,"no_original_bytes_publicly_distributed":True,"no_activation_or_science":True,"rows":out}
Path("g2-v7").mkdir(exist_ok=True);b=(json.dumps(r,sort_keys=True,ensure_ascii=False,separators=(",",":"))+"\n").encode();Path("g2-v7/firstparty_conditional_media.json").write_bytes(b)
print("G2_V7_MEDIA_RECEIPT_SHA256",hashlib.sha256(b).hexdigest())
for x in out:print("G2_V7_MEDIA",x)
