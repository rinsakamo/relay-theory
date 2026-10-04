#!/usr/bin/env python3
"""P13 narrowly justified supplemental acquisition BEFORE scientific PRE_A.

The 26pp published main original has already been raw-hash checked in
prior 16/16 provenance run 37178895352. HOWEVER its Bayesian
change-point *exact iterative posterior* lives in separate publisher S1
Appendix. Do not silently certify full scientific math from main alone.
This probe fetches publisher-hosted appendix, raw-hashes/pages/anchors,
and prints a bounded source-text page map plus relevant derivation spans.
Nothing in this probe alone grants source-science PRE_A eligibility.
"""
import urllib.request,hashlib,io,json,re,pathlib
from pypdf import PdfReader
main_sha="8e4aef9af81827f0bf5b6a82cd78b3ff9d6f60aa436b3e54156e6143e0c5af07"
sources=[
("MAIN","https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1006681&type=printable"),
("S1","https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1006681.s001&type=supplementary")]
results={}
for id,url in sources:
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (RelayTheory P13 targeted pre-A publisher original and necessary supplementary source review)"})
 with urllib.request.urlopen(req,timeout=130) as f:b=f.read();final=f.geturl()
 assert b.startswith(b"%PDF"),f"{id} NOT A REAL OFFICIAL SOURCE PDF"
 pdf=PdfReader(io.BytesIO(b),strict=False)
 sha=hashlib.sha256(b).hexdigest()
 if id=="MAIN":
  assert sha==main_sha and len(b)==2109160 and len(pdf.pages)==26,"ORIGINAL_MAIN_SOURCE_NOT_SAME_FAIL_CLOSE"
 print("P13_PUBLISHER_ORIGINAL",id,sha,len(b),len(pdf.pages),flush=True)
 refs=[]
 for i,page in enumerate(pdf.pages):
  txt=re.sub(r"\\s+"," ",page.extract_text() or "")
  words=["Bayesian","observer","recursive","recursion","change-point","run length","Model recovery","parameter recovery","ideal observer","Beta","Exp","criterion","Bayes","Wilson"]
  matches=[s for s in words if s.lower() in txt.lower()]
  refs.append({"page":i+1,"chars":len(txt),"terms":matches})
  print("P13_PAGE_MAP",id,i+1,"chars",len(txt),"topics",",".join(matches),flush=True)
  if id=="S1" and i<10:
   # Real original supplemental text only; exact mathematical typesetting
   # requires separate source PDF pixel review before final qualification.
   print("P13_SUPPLEMENT_PAGE_TEXT",i+1,txt[:3600].replace("\\n"," "),flush=True)
 results[id]={"sha256":sha,"byte_count":len(b),"page_count":len(pdf.pages),"source_url":url,"final_issuer_url":final,"page_map":refs}
 assert id!="S1" or any("Bayes" in w for rec in refs for w in rec["terms"])
pathlib.Path("g1-p13-original").mkdir(exist_ok=True)
pathlib.Path("g1-p13-original/publisher-original-and-source-mandatory-supplement-metadata.json").write_text(json.dumps({"schema":"p399.g1.p13.bound_publication_original_plus_math_necessary_S1_provenance.v1","main_prior_raw_receipt":37178895352,"S1_why_fetched":"Original published main 26pp expressly delegates exact iterative Bayesian joint-state recursion, other model variants and fit identifiability to separate published S1 PDF","source":results,"model_critical_S1_visual_semantic_acceptance_Auto":False,"main_science_started":False},indent=2)+"\n")
