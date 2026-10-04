#!/usr/bin/env python3
"""Isolated PRD-C official original pixel inspection helper. Source only, no admission."""
import base64, hashlib, io, json, os, re, urllib.request
from pathlib import Path
import fitz
DOI="10.1371/journal.pcbi.1010740"
URL="https://journals.plos.org/ploscompbiol/article/file?id="+DOI+"&type=printable"
EXPECTED="9c17c00fba0985f6f66b8520c6fc971ae5a2c6d3e1bac266d9fba2739c9792fe"
req=urllib.request.Request(URL,headers={"User-Agent":"RelayTheory-PRD-C-original-page-audit/1.0","Accept":"application/pdf"})
with urllib.request.urlopen(req,timeout=60) as handle:
 raw=handle.read(12000000); resolved=handle.geturl()
assert raw.startswith(b"%PDF-"),"fail closed: original response is not PDF"
doc=fitz.open(stream=raw,filetype="pdf")
receipt={"doi":DOI,"requested_first_party_original":URL,"resolved_url":resolved,"source_sha256":hashlib.sha256(raw).hexdigest(),"source_bytes":len(raw),"pages":len(doc),"prior_original_receipt_exact_match":hashlib.sha256(raw).hexdigest()==EXPECTED,"page_text":[],"science_qualified":False,"activated":False}
assert receipt["prior_original_receipt_exact_match"] and len(doc)==32 and len(raw)==3306881,"fail closed: publisher original changed from frozen receipt"
for i,p in enumerate(doc):
 t=p.get_text()
 receipt["page_text"].append({"page0":i,"sha256_extracted_text":hashlib.sha256(t.encode()).hexdigest(),"chars":len(t),"title_line":" ".join(t.splitlines()[:4])[:140],"ideal":bool(re.search("Ideal (Performance )?Model",t,re.I)),"retro":bool(re.search("Retrospective (Performance )?Model",t,re.I)),"prospective":bool(re.search("Prospective (Performance )?Model",t,re.I)),"table2":"Table 2" in t,"equation_cues":[x for x in ["(4)","(5)","(6)","(7)","(8)","(9)","(10)","(11)","(12)","(13)"] if x in t]})
print("PRD_C_FIRSTPARTY_SOURCE",json.dumps({k:v for k,v in receipt.items() if k!="page_text"},sort_keys=True))
for p in receipt["page_text"]: print("PRD_C_PAGE_MAP",json.dumps(p,sort_keys=True))
Path("prd-c-evidence").mkdir(exist_ok=True)
Path("prd-c-evidence/B1_OFFICIAL_SOURCE_PIXEL_READBACK.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
# Narrow bounded original publisher visuals: original p0 and source-critical equations/models/fit/adverse pages.
for idx in [0,10,11,12,13,14,15,17,18,19,20]:
 page=doc[idx]; pix=page.get_pixmap(matrix=fitz.Matrix(1.25,1.25),alpha=False,colorspace=fitz.csRGB)
 from PIL import Image
 im=Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
 buf=io.BytesIO();im.save(buf,format="JPEG",quality=57,optimize=True)
 print("PRD_C_ORIGINAL_VISUAL_BEGIN page0="+str(idx)+" format=jpeg sha256="+hashlib.sha256(buf.getvalue()).hexdigest())
 print("PRD_C_VISUAL_PAGE"+str(idx)+"_BASE64="+base64.b64encode(buf.getvalue()).decode("ascii"))
 print("PRD_C_ORIGINAL_VISUAL_END")
