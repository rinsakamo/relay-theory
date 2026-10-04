#!/usr/bin/env python3
"""Targeted B1 first-page identity witness after run 37196467277 DOI-token false-negative.
Publisher PDF and publisher complete HTML are paired only to verify paper identity;
not assumed byte-equivalent and not source-semantic scientific qualification.
"""
import hashlib,json,re,urllib.request,os
from datetime import datetime,timezone
from io import BytesIO
from pypdf import PdfReader
doi="10.1371/journal.pcbi.1007720"
pdfurl="https://journals.plos.org/ploscompbiol/article/file?id="+doi+"&type=printable"
htmlurl="https://journals.plos.org/ploscompbiol/article?id="+doi
def read(url):
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36"})
 with urllib.request.urlopen(req,timeout=12) as f:
  return f.read(12000000),f.geturl(),f.headers.get("Content-Type")
result={"observed_utc":datetime.now(timezone.utc).isoformat(),"doi":doi,"previous_first_probe_run":37196467277,
        "previous_pdf_sha256":"0a79da7e5504e1e970332a65401d3da2c6282bb48ad640f760c17f4bc06a3fcf",
        "source_identity_qualified":False,"source_semantic_math_figures_qualified":False}
try:
 pdf,purl,pmime=read(pdfurl); html,hurl,hmime=read(htmlurl)
 R=PdfReader(BytesIO(pdf)); page=" ".join((R.pages[i].extract_text() or "") for i in range(min(3,len(R.pages))))
 norm=re.sub(r"\\s+"," ",page.lower()); h=html.decode("utf-8","replace")
 tokens=("generalizing","conjunctive","franklin")
 result.update(publisher_pdf_bytes=len(pdf),publisher_pdf_sha256=hashlib.sha256(pdf).hexdigest(),
               pdf_signature=pdf.startswith(b"%PDF-"),pdf_pages=len(R.pages),
               pdf_title_unique_tokens={x:x in norm for x in tokens},
               official_html_raw_sha256=hashlib.sha256(html).hexdigest(),
               official_html_doi_present=doi in h,official_html_title_present="Generalizing to generalize" in h,
               firstpage_contiguous_DOI_legacy=False,official_pdf_url=purl,official_html_url=hurl)
 result["source_identity_qualified"]=(result["pdf_signature"] and result["publisher_pdf_sha256"]==result["previous_pdf_sha256"]
 and all(result["pdf_title_unique_tokens"].values()) and result["official_html_doi_present"]
 and result["official_html_title_present"] and purl.startswith("https://journals.plos.org/")
 and hurl.startswith("https://journals.plos.org/"))
except Exception as e: result["error"]=type(e).__name__+":"+str(e)[:300]
os.makedirs("g2d-int-b1",exist_ok=True)
with open("g2d-int-b1/publisher_identity.json","w") as f: json.dump(result,f,indent=2)
print(json.dumps(result,sort_keys=True))
if not result["source_identity_qualified"]:
 raise SystemExit("FAIL CLOSED: B1 identity not established; preserve original 37196467277 false DOI detector")
