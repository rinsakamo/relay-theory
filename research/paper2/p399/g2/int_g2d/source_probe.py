#!/usr/bin/env python3
"""Bounded first-party INT acquisition attempts; output metadata only.
Run separately from MAIN science. HTTP 200/core metadata is not complete original.
All URLs first-party. Keep every failed attempt and no author manuscript upgrades.
"""
import hashlib,json,os,re,urllib.request,urllib.error
from datetime import datetime,timezone
from io import BytesIO
from pypdf import PdfReader
URLS=[
("INT01_SCIDIR_HTML","https://www.sciencedirect.com/science/article/pii/S0010027724002531","html","10.1016/j.cognition.2024.105967"),
("INT01_SCIDIR_PDF","https://www.sciencedirect.com/science/article/pii/S0010027724002531/pdfft","pdf","10.1016/j.cognition.2024.105967"),
("INT01_ELSEVIER_API_METADATA","https://api.elsevier.com/content/article/pii/S0010027724002531?httpAccept=text/xml","metadata","10.1016/j.cognition.2024.105967"),
("INT13_PLOS_HTML","https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014796","html","10.1371/journal.pcbi.1014796"),
("INT13_PLOS_PDF","https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1014796&type=printable","pdf","10.1371/journal.pcbi.1014796"),
("INTB1_PLOS_PDF","https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1007720&type=printable","pdf","10.1371/journal.pcbi.1007720"),
("INTB2_ELIFE_VOR_PDF","https://cdn.elifesciences.org/articles/39497/elife-39497-v3.pdf","pdf","10.7554/eLife.39497"),
("INTB3_ELIFE_VOR_PDF","https://cdn.elifesciences.org/articles/57244/elife-57244-v2.pdf","pdf","10.7554/eLife.57244"),
("INTB4_PLOS_PDF","https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1012872&type=printable","pdf","10.1371/journal.pcbi.1012872")]
os.makedirs("g2d-int-receipts",exist_ok=True)
receipts=[]
for name,url,kind,doi in URLS:
 r=dict(name=name,first_party_url=url,source_type=kind,doi=doi,utc=datetime.now(timezone.utc).isoformat(),raw_source_acquired=False,fully_semantic_science_qualified=False)
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36","Accept":"application/pdf,text/html;q=0.9,*/*;q=0.1"})
  with urllib.request.urlopen(req,timeout=12) as resp:
   data=resp.read(24*1024*1024+1)
   r.update(status=resp.status,final_url=resp.geturl(),mime=resp.headers.get("Content-Type",""),bytes=len(data))
  if len(data)>24*1024*1024:
   r["error"]="24MiB READ CAP"
  elif kind=="pdf" and data.startswith(b"%PDF-"):
   r["sha256"]=hashlib.sha256(data).hexdigest()
   reader=PdfReader(BytesIO(data))
   r["page_count"]=len(reader.pages)
   head=" ".join((reader.pages[i].extract_text() or "") for i in range(min(2,len(reader.pages))))
   r["first_two_pages_text_sample_sha256"]=hashlib.sha256(head.encode()).hexdigest()
   token=doi.split("/")[-1].lower()
   r["doi_text_token_on_first_two_pages"]=token in re.sub(r"\\s+","",head.lower())
   r["raw_source_acquired"]=r["doi_text_token_on_first_two_pages"] and r["final_url"].split("/")[2] in ("journals.plos.org","cdn.elifesciences.org","www.sciencedirect.com")
   if not r["raw_source_acquired"]:r["error"]="pdf_signature_but_doi_firstpage_or_firstparty_unverified"
  elif kind=="html":
   t=data.decode("utf-8","replace")
   r["sha256"]=hashlib.sha256(data).hexdigest()
   r["explicit_uncorrected_proof"]=bool(re.search("This is an uncorrected proof",t,re.I))
   r["has_full_main_sections"]=all(re.search(x,t,re.I) for x in ("Abstract","Introduction","Results","Methods","References"))
   r["doi_in_html"]=doi.lower() in t.lower()
   r["raw_source_acquired"]=r["has_full_main_sections"] and r["doi_in_html"] and r["final_url"].split("/")[2] in ("journals.plos.org","www.sciencedirect.com")
   if name.startswith("INT13") and r["explicit_uncorrected_proof"]:r["final_vor_acquired"]=False
   if not r["raw_source_acquired"]:r["error"]="only_preview_or_incomplete_html_or_failed_firstparty"
  else:
   r["sha256"]=hashlib.sha256(data).hexdigest()
   r["error"]="nonpdf_or_bibliographic_metadata_only_NOT_full_original"
 except Exception as e:r["error"]=type(e).__name__+":"+str(e)[:250]
 receipts.append(r)
 print(name,json.dumps(r,ensure_ascii=False,sort_keys=True),flush=True)
with open("g2d-int-receipts/physical_attempts.json","w",encoding="utf-8") as f:
 json.dump({"schema":"p399.g2d.int_firstparty_physical_attempts.v1","not_semantic_scientific_admission":True,"records":receipts},f,ensure_ascii=False,indent=2)
print("DONE: bounded attempts. Do not add source counts without independently reading receipt and checking final edition.")
