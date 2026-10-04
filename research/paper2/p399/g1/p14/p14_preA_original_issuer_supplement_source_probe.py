#!/usr/bin/env python3
"""P14 pre-A targeted issuer-original source package admission receipt ONLY.

Old acquisition already confirms main PLOS 34 page SHA. Critical supplementary
math/proof/noise S3,S4,S5 are linked by published original itself: do not
reconstruct or certify those before independent original content is acquired.
This CI physically checks publisher primary plus required supplements, raw
SHA/bytes/pages, all source page text headings, and saves no scientific
conclusion. PDF critical figures/equations must still be visually reviewed.
"""
import urllib.request,hashlib,io,re,json,pathlib
from pypdf import PdfReader
DOI="10.1371/journal.pcbi.1008969"
SPEC=[
 ("MAIN",f"https://journals.plos.org/ploscompbiol/article/file?id={DOI}&type=printable","cca218ddff9764422316f99fe2cf8cf6a5519462a0b38ac25b45999080b79ec0",2551032,34),
 ("S2",f"https://journals.plos.org/ploscompbiol/article/file?id={DOI}.s002&type=supplementary",None,None,None),
 ("S3",f"https://journals.plos.org/ploscompbiol/article/file?id={DOI}.s003&type=supplementary",None,None,None),
 ("S4",f"https://journals.plos.org/ploscompbiol/article/file?id={DOI}.s004&type=supplementary",None,None,None),
 ("S5",f"https://journals.plos.org/ploscompbiol/article/file?id={DOI}.s005&type=supplementary",None,None,None)]
allrec={}
for name,url,knownsha,knownsize,knownpg in SPEC:
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (RelayTheory only justified official P14 model critical supplementary evidence audit)"})
 with urllib.request.urlopen(req,timeout=110) as f:b=f.read();issuer=f.geturl()
 assert b.startswith(b"%PDF"),"not original publisher PDF "+name
 dig=hashlib.sha256(b).hexdigest()
 rdr=PdfReader(io.BytesIO(b),strict=False)
 if knownsha:
  assert dig==knownsha and len(b)==knownsize and len(rdr.pages)==knownpg,"previous physically locked main changed"
 pages=[]
 for i,page in enumerate(rdr.pages):
  t=re.sub(r"\s+"," ",page.extract_text() or "")
  pages.append({"page_pdf_1_based":i+1,"characters":len(t),"opening_source_text":t[:250]})
  print("P14_ORIGINAL_PAGE",name,i+1,"CHARS",len(t),"OPEN",t[:135],flush=True)
 allrec[name]={"issuer_original_url":url,"redirect":issuer,"raw_sha256":dig,"bytes":len(b),"pages":len(rdr.pages),"physical_publisher_original_verified":True,"page_text_map":pages}
 print("P14_PHYSICAL_ORIGINAL_SUCCESS",name,dig,len(b),len(rdr.pages),flush=True)
p=pathlib.Path("g1-p14-source");p.mkdir(exist_ok=True)
(p/"mandatory-original-math-and-negative-supplements.json").write_text(json.dumps({"schema":"p399.g1.p14.original_edition_original_s2_5_before_preA.v1","old_original_main_receipt_run":37178895352,"sources":allrec,"PRE_A_scientifically_qualified_automatically":False,"all_pages_visually_inspected":False,"full_S1_observer_individual_data_primary_admitted":False},indent=2)+"\n")
