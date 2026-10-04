#!/usr/bin/env python3
"""G2-D v4: publisher-owned B3 VOR raw exact recheck, no full-article redistribution.
Failures are source-acquisition failures; metadata anchors are NOT science qualification.
"""
import hashlib,json,re,urllib.request,urllib.parse,datetime,sys,os
from io import BytesIO
from pathlib import Path
from pypdf import PdfReader
URL="https://cdn.elifesciences.org/articles/57244/elife-57244-v2.pdf"
SHA="9e13535592ff1cf36c9eb4a9a1daae23cb6dfa8a916a40586a6cc5c651b80d35"
OUT=Path("g2d-v4-b3-evidence");OUT.mkdir(exist_ok=True)
r={"schema":"g2d.v4.b3.publisher_source_original_nonsemantic.v1","source_url":URL,"expected_sha256":SHA,"run_commit":os.getenv("GITHUB_SHA"),"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"full_original_source_reproduced":False,"new_mechanistic_independence_proven":False,"main_authorized":False}
def out():
 (OUT/"actual_source_receipt.json").write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print("B3_V4_ACTUAL_SOURCE",json.dumps(r,sort_keys=True),flush=True)
def norm(s):return re.sub(r"[^a-z0-9]+","",s.lower())
try:
 req=urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0","Accept":"application/pdf"})
 with urllib.request.urlopen(req,timeout=12) as response:
  data=response.read(7*1024*1024+1);final=response.geturl()
  h=urllib.parse.urlparse(final).hostname
  r.update(status=response.status,final_url=final,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),first5_pdf=data[:5]==b"%PDF-",resolved_host=h)
  if h not in ("cdn.elifesciences.org","elifesciences.org"):raise ValueError("publisher_host_mismatch")
  if len(data)>7*1024*1024 or data[:5]!=b"%PDF-":raise ValueError("not_bounded_pdf")
  if r["sha256"]!=SHA:raise ValueError("raw_exact_original_sha_mismatch")
  pdf=PdfReader(BytesIO(data),strict=False)
  r["pages"]=len(pdf.pages)
  if r["pages"]!=35:raise ValueError("expected_vor_35_pages_mismatch")
  texts=[p.extract_text() or "" for p in pdf.pages]
  r["per_page_extracted_utf8_sha256"]=[hashlib.sha256(t.encode()).hexdigest() for t in texts]
  whole=norm(" ".join(texts))
  r["title_identity"]=all(norm(x) in norm(" ".join(texts[:2])) for x in ["integrative","frontal","parietal","cognitive","control"])
  if not r["title_identity"]:raise ValueError("pdf_title_publisher_identity_unmatched")
  anchors={"spectral_dcm":"spectraldynamiccausalmodeling","reduced_smoothing":"reducedsmoothing","cognitive_ability":"cognitiveability","TMS":"transcranialmagneticstimulation","spm12":"spm12"}
  r["source_text_anchor_present"]={k:v in whole for k,v in anchors.items()}
  # Ambiguous numeric format is recorded as candidate and never used to assert semantic proof.
  r["candidate_reduced_smoothing_page_numbers"]=[i+1 for i,t in enumerate(texts) if "smoothing" in t.lower() and ("reduced" in t.lower() or "4 mm" in t.lower())]
  r["candidate_figure8_page_numbers"]=[i+1 for i,t in enumerate(texts) if re.search(r"figure\s*8",t,re.I)]
  r["full_original_source_reproduced"]=True
except Exception as e:
 r["failure"]=type(e).__name__+":"+str(e)[:180]
 out()
 sys.exit(1)
out()
