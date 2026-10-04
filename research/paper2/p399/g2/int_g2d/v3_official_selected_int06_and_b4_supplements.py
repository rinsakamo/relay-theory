#!/usr/bin/env python3
"""INT G2-D selected INT06 original+source-native DOC supplements and B4 formal S1.
First-party original raw bytes, bounded timeout and digest; no full source distribution.
Scientific truth, rendered supplementary figures, complete model lineage remain separate.
"""
import hashlib,json,os,re,urllib.request,urllib.error,zipfile
from io import BytesIO
from datetime import datetime,timezone
from pypdf import PdfReader
PREFIX="https://journals.plos.org/ploscompbiol/article/file?id="
URLS=[
("INT06_PLOS_PUBLISHED_MAIN_PDF","10.1371/journal.pcbi.1000765","pdf","10.1371/journal.pcbi.1000765","c276294fa7a111e5df98f35aa0da933af28d45a1e1347940a1b57753c0980706"),
("INT06_PLOS_SUPPORTING_S7_TEXT","10.1371/journal.pcbi.1000765.s007","doc","10.1371/journal.pcbi.1000765.s007",None),
("INT06_PLOS_SUPPORTING_S8_TABLE","10.1371/journal.pcbi.1000765.s008","doc","10.1371/journal.pcbi.1000765.s008",None),
("INTB4_PLOS_PUBLISHED_SUPPLEMENT_S1","10.1371/journal.pcbi.1012872.s001","pdf","10.1371/journal.pcbi.1012872.s001",None)
]
TARGETS={
 "INT06_PLOS_PUBLISHED_MAIN_PDF":"https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1000765&type=printable",
 "INT06_PLOS_SUPPORTING_S7_TEXT":"https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1000765.s007&type=supplementary",
 "INT06_PLOS_SUPPORTING_S8_TABLE":"https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1000765.s008&type=supplementary",
 "INTB4_PLOS_PUBLISHED_SUPPLEMENT_S1":"https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1012872.s001&type=supplementary"
}
out={"schema":"p399.g2d.v3_firstparty_int06_and_B4_supplement_reacquisition.v1","runner_head":os.getenv("GITHUB_SHA"),
"historical_int06_original_sha_expected":"c276294fa7a111e5df98f35aa0da933af28d45a1e1347940a1b57753c0980706",
"scope":"PHYSICAL_FIRSTPARTY_SOURCE_ONLY_PLUS_SUPPLEMENT_NATIVE_TEXT_LOCATORS",
"no_source_scientific_full_admissions":True,"no_backup_activation":True,"records":[]}
for name,doi,kind,identity,expected_sha in URLS:
 url=TARGETS[name]
 x={"slot":name,"doi":doi,"requested_url":url,"kind":kind,"firstparty_binary_verified":False,
    "independent_full_visual_supplement_audit":False,"utc":datetime.now(timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36","Accept":"application/pdf,application/msword,*/*;q=0.8"})
  with urllib.request.urlopen(req,timeout=12) as resp:
   data=resp.read(12*1024*1024+1)
   x.update(status=resp.status,final_url=resp.geturl(),media_type=resp.headers.get("Content-Type"),raw_bytes=len(data))
  x["firstparty_url_verified"]=x["final_url"].split("/")[2] in ("journals.plos.org","content.plos.org","plos.org")
  if len(data)>12*1024*1024:raise ValueError("12M cap exceeded")
  x["sha256"]=hashlib.sha256(data).hexdigest()
  x["prefix_hex"]=data[:8].hex()
  if not x["firstparty_url_verified"]:raise ValueError("nonfirstparty redirect")
  if kind=="pdf":
   if data[:5]!=b"%PDF-":raise ValueError("not pdf despite endpoint")
   reader=PdfReader(BytesIO(data),strict=False)
   x["pdf_pages"]=len(reader.pages)
   texts=[p.extract_text() or "" for p in reader.pages]
   x["each_page_native_text_sha256"]=[hashlib.sha256(t.encode()).hexdigest() for t in texts]
   x["firsttwo_title_identity_anchor"]=all(t in (" ".join(texts[:2])).lower() for t in ("brain","router")) if name.startswith("INT06") else None
   if name.startswith("INT06"):
    if x["sha256"]!=expected_sha:raise ValueError("original INT06 main SHA differs from frozen G2")
   else:
    full=" ".join(texts)
    x["supplemental_figure_letter_page_locator"]={a:[i+1 for i,t in enumerate(texts) if re.search(r"(?im)\bfig(?:ure)?\s+"+a+r"\b",t)] for a in "ABCDEFG"}
    x["supplement_terms_page_locator"]={w:[i+1 for i,t in enumerate(texts) if w.lower() in t.lower()] for w in ("model recovery","parameter recovery","bias","depression","exclusion")}
    x["figure_letter_all_A_through_G_candidate_coverage"]=all(bool(v) for v in x["supplemental_figure_letter_page_locator"].values())
   x["firstparty_binary_verified"]=True
  else:
   x["is_compound_doc_ole"]=data.startswith(bytes.fromhex("d0cf11e0a1b11ae1"))
   x["is_docx_zip"]=zipfile.is_zipfile(BytesIO(data))
   if not (x["is_compound_doc_ole"] or x["is_docx_zip"]):raise ValueError("not MS DOC/DOCX; preserve bytes receipt not promote")
   x["firstparty_binary_verified"]=True
 except Exception as e:x["failure"]=type(e).__name__+":"+str(e)[:210]
 out["records"].append(x)
 print("G2D_V3_SOURCE",json.dumps(x,sort_keys=True),flush=True)
os.makedirs("g2d-v3-original-supplement",exist_ok=True)
with open("g2d-v3-original-supplement/actual_sources.json","w",encoding="utf-8") as f:json.dump(out,f,indent=2)
print("INT_G2D_V3_REAL_FIRSTPARTY_BYTES",sum(x["firstparty_binary_verified"] for x in out["records"]),"OF",len(URLS),"NO_SCIENCE_PROMOTION")
