#!/usr/bin/env python3
"""P09 justified independent critical-render source review of ALREADY ACQUIRED publisher original.

Prior run 37178895352 physically acquired this PLOS original. This repeat is
ONLY to validate exact equality and make decisive mathematical and figure pages
available for actual independent visual review, rather than pretending pypdf
text/page metadata equals original scientific source fidelity.
"""
import urllib.request,io,hashlib,json,re,base64,os
from pypdf import PdfReader
import fitz
from PIL import Image
URL="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1006435&type=printable"
SHA="9d5f8df792c19e88749311dc2f9688705fe3aeaea4eb7bfad7e761ca90e5e6b2"
req=urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0 (RelayTheory P09 visual scientific source inspection)"})
with urllib.request.urlopen(req,timeout=100) as f:b=f.read();url=f.geturl()
assert b.startswith(b"%PDF"),"not source pdf"
assert hashlib.sha256(b).hexdigest()==SHA,"published original byte identity MISMATCH stop all review"
assert len(b)==3283055,"publisher original size changed"
pdf=PdfReader(io.BytesIO(b))
assert len(pdf.pages)==21,"publisher original pages changed"
print("P09_VERIFIED_SOURCE",SHA,len(b),len(pdf.pages),flush=True)
page_meta=[]
patterns=["Fig 1","Fig 2","Fig 3","Fig 4","Table 1","Table 2","Reduced model","Full model","Model parameter selection","Delayed Match to Sample","sufficiency","Discussion","References","Supplemental"]
for idx,p in enumerate(pdf.pages):
 t=p.extract_text() or ""
 located=[s for s in patterns if s.lower() in t.lower()]
 page_meta.append({"pdf_page":idx+1,"text_chars":len(t),"locators":located})
 print("P09_PAGE_MAP",idx+1,"|".join(located),flush=True)
# JPG reduced visual pages are printed to Actions job logs in 2800char
# chunks; the researcher will inspect actual source pixels with the model's
# vision capabilities, independent from the text extraction above.
f=fitz.open(stream=b,filetype="pdf")
for page in [2,4,6,8,10,12,14,16]:
 p=f[page-1]
 pix=p.get_pixmap(matrix=fitz.Matrix(0.85,0.85),colorspace=fitz.csRGB,alpha=False)
 im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
 dest=io.BytesIO(); im.save(dest,format="JPEG",quality=62,optimize=True)
 enc=base64.b64encode(dest.getvalue()).decode()
 print("P09_IMAGE_BEGIN",page,"JPEG",len(dest.getvalue()),flush=True)
 for i in range(0,len(enc),2800):print("P09_IMG_CHUNK",page,i//2800,enc[i:i+2800],flush=True)
 print("P09_IMAGE_END",page,flush=True)
os.makedirs("g1-p09",exist_ok=True)
with open("g1-p09/p09-pdf-visual-targets-metadata.json","w") as out:
 json.dump({"schema":"p399.g1.p09.original_pdf_exact_physical_and_critical_visual_delivery.v1","prior_source_run":37178895352,"reason_to_reacquire":"visual critical math/fig pre-A qualification only","original_sha256":SHA,"original_bytes":len(b),"original_pages":len(pdf.pages),"page_map":page_meta,"visually_delivered_pages":[2,4,6,8,10,12,14,16],"original_math_figure_semantics_pass_ci":False,"formal_source_admission_automatically_granted":False},out,indent=2)
