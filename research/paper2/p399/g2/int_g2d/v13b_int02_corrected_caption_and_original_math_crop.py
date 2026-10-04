#!/usr/bin/env python3
"""Correct v13 fig regex extraction; high-res crop around original eq8-17 only.
Fail closed original SHA; 12s issuer-owned CDN. Unmodified older locator's
empty figure candidates remain as a historical false-negative receipt.
"""
import hashlib,json,os,re,urllib.request,base64
from io import BytesIO
from pypdf import PdfReader
import fitz
URL="https://mdpi-res.com/d_attachment/entropy/entropy-26-00484/article_deploy/entropy-26-00484.pdf"
SHA="a1e644c826bf1b356187bc556d5947eb23638f3f9bc6c61835d46850b4f1cc37"
with urllib.request.urlopen(urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0 (originally SHA-bound academic page-review)"}),timeout=12) as r:
 b=r.read(12*1024*1024+1)
 actual=hashlib.sha256(b).hexdigest()
 if actual!=SHA or not b.startswith(b"%PDF-") or r.status!=200:raise RuntimeError("original mismatch/non-publisher source")
rd=PdfReader(BytesIO(b),strict=False)
assert len(rd.pages)==14
texts=[p.extract_text() or "" for p in rd.pages]
figure_pages={str(i):[n+1 for n,t in enumerate(texts) if re.search(r"(?im)\bFigure\s*"+str(i)+r"\b",t)] for i in range(1,9)}
print("V13B_REAL_ORIGINAL_CAPTION_LOCATORS",json.dumps(figure_pages),flush=True)
if not all(figure_pages.values()):
 raise RuntimeError("corrected caption coverage unexpectedly absent; do not falsify locator PASS")
pdf=fitz.open(stream=b,filetype="pdf")
# Native original p8/p9/p10 each math-critical, rendered 2.5x cropped.
REGIONS={8:(140,390,545,760),9:(100,375,545,775),10:(90,75,550,430)}
highres={}
for page,coords in REGIONS.items():
 pix=pdf.load_page(page-1).get_pixmap(matrix=fitz.Matrix(2.1,2.1),clip=fitz.Rect(coords),alpha=False)
 jpg=pix.tobytes(output="jpeg",jpg_quality=55)
 highres[str(page)]={"raw_original_highres_crop_sha256":hashlib.sha256(jpg).hexdigest(),"clip_points":coords}
 print("INT02_V13B_HIGHRES_EQUATIONS_PAGE_"+str(page),base64.b64encode(jpg).decode(),flush=True)
pdf.close()
o={"schema":"p399.g2d.int02.v13b.corrected_source_figures_and_highres_exact_equation_locator",
 "publisher_original_url":URL,"publisher_original_sha":SHA,
 "original_pdf_pages":14,"prior_v13_historical_all_figures_empty_regex_false_negative":True,
 "corrected_figure_caption_page_indices_1based":figure_pages,
 "highres_original_math_crop_receipts":highres,
 "complete_scientific_math_semantics_automatically_verified":False,
 "global_lineage_and_any_MAIN_approval":False}
os.makedirs("g2d-int02-v13b",exist_ok=True)
with open("g2d-int02-v13b/receipt.json","w") as f:json.dump(o,f,indent=2)
print("V13B_BOUNDED_DONE corrected 8/8 FIG source locator labels; math must be independently visually checked")
