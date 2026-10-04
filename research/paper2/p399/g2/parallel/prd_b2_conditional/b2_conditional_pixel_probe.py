#!/usr/bin/env python3
"""Conditionally verify predeclared PRD-B2 firstparty original only; zero promotion."""
import base64,hashlib,io,json,re,urllib.request
from pathlib import Path
import fitz
from PIL import Image
doi="10.1371/journal.pcbi.1009557"
url=f"https://journals.plos.org/ploscompbiol/article/file?id={doi}&type=printable"
expected="7b6e4192bfe1b60d794d197e14822997b77d22e437db89850fc4cddcb79482db"
request=urllib.request.Request(url,headers={"User-Agent":"RelayTheory-PRD-C-B2-conditional-original-pixel-audit","Accept":"application/pdf"})
with urllib.request.urlopen(request,timeout=55) as response: raw=response.read(12000000)
assert raw.startswith(b"%PDF-"),"publisher response is not an original PDF"
doc=fitz.open(stream=raw,filetype="pdf")
sha=hashlib.sha256(raw).hexdigest()
assert (sha,len(raw),len(doc))==(expected,2306402,39),"publisher original failed independent old-byte readback"
r={"doi":doi,"url":url,"sha256":sha,"bytes":len(raw),"pages":len(doc),"old_receipt_exact_match":True,"conditional_only":True,"activated":False,"source_math_qualified":False,"page_map":[]}
for i,p in enumerate(doc):
 t=p.get_text()
 r["page_map"].append({"page0":i,"sha256_extracted_text":hashlib.sha256(t.encode()).hexdigest(),"head":t[:130].replace("\n"," "),"posterior":bool(re.search("posterior",t,re.I)),"covariance":bool(re.search("covari",t,re.I)),"mathematical":bool(re.search("Methods|proportional|choice correlation",t,re.I))})
print("PRD_C_B2_FIRSTPARTY_SOURCE",json.dumps({k:v for k,v in r.items() if k!="page_map"},sort_keys=True))
for p in r["page_map"]:print("PRD_C_B2_PAGE_MAP",json.dumps(p,sort_keys=True))
Path("prd-c-b2-evidence").mkdir(exist_ok=True)
Path("prd-c-b2-evidence/B2_CONDITIONAL_PUBLISHER_SOURCE_PIXEL_READBACK.json").write_text(json.dumps(r,sort_keys=True,indent=2)+"\n")
for idx in [0,4,8,9,11,12,15,18,23]:
 p=doc[idx];pix=p.get_pixmap(matrix=fitz.Matrix(1.15,1.15),alpha=False);im=Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB");bio=io.BytesIO();im.save(bio,format="JPEG",quality=56,optimize=True)
 print("PRD_C_B2_VISUAL_PAGE"+str(idx)+"_BASE64="+base64.b64encode(bio.getvalue()).decode("ascii"))
