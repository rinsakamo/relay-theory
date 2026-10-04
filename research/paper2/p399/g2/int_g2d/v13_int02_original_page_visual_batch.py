#!/usr/bin/env python3
"""INT02 official MDPI 14-page VOR exact SHA, separate batches for visual science.
Firstparty CDN exact previously G2-frozen original. 12s request; no mirror.
Render source pages as temporary CI review-only JPEG, not repo source redistribution.
Do not auto-promote figures or equations from mere raw source/index success.
"""
import hashlib,json,os,re,urllib.request,base64
from io import BytesIO
from datetime import datetime,timezone
from pypdf import PdfReader
import fitz
URL="https://mdpi-res.com/d_attachment/entropy/entropy-26-00484/article_deploy/entropy-26-00484.pdf"
SHA="a1e644c826bf1b356187bc556d5947eb23638f3f9bc6c61835d46850b4f1cc37"
BATCHES=[[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14]]
batch=int(os.getenv("BATCH","0"))
assert 0<=batch<len(BATCHES)
req=urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0 (G2D selected published source exact review)","Accept":"application/pdf"})
with urllib.request.urlopen(req,timeout=12) as resp:
 data=resp.read(12*1024*1024+1);final=resp.geturl();status=resp.status
actual=hashlib.sha256(data).hexdigest()
if status!=200 or not final.startswith("https://mdpi-res.com/d_attachment/entropy/entropy-26-00484/") or actual!=SHA or not data.startswith(b"%PDF-"):
 raise RuntimeError("failclosed INT02 exact previously frozen firstparty source identity")
reader=PdfReader(BytesIO(data),strict=False)
assert len(reader.pages)==14
texts=[page.extract_text() or "" for page in reader.pages]
fig={str(i):[n+1 for n,t in enumerate(texts) if re.search(r"(?i)\\bFig(?:ure)?\\s*"+str(i)+r"\\b",t)] for i in range(1,10)}
terms=("planning","counterfactual","mixed model","model bias","beta","risk","precision","baseline","limitations","trade-off")
out={"schema":"relaytheory.g2d.INT02.actual_publisher_exact_all_page_source_batch.v1","utc":datetime.now(timezone.utc).isoformat(),"runner_head":os.environ.get("GITHUB_SHA"),"batch":batch,"firstparty_url":URL,
"original_raw_sha256":actual,"raw_bytes":len(data),"main_pages":len(texts),"page_text_sha":[hashlib.sha256(t.encode()).hexdigest() for t in texts],
"figure_caption_candidate_pages_native":fig,"selected_rendered_pages":BATCHES[batch],
"full_figure_visual_semantics_automatically_qualified":False,"global_lineage_clearance":False,"main_authorized":False,"rendered_jpeg_hashes":{}}
print("INT02_V13_SOURCE",json.dumps({"batch":batch,"sha":actual,"bytes":len(data),"pages":len(texts),"figure_pages":fig},sort_keys=True),flush=True)
pdf=fitz.open(stream=data,filetype="pdf")
for page1 in BATCHES[batch]:
 txt=texts[page1-1]
 findings=[]
 for term in terms:
  i=txt.lower().find(term.lower())
  if i>=0:findings.append({"key":term,"context_normalized":re.sub(r"\\s+"," ",txt[max(0,i-70):i+200])[:260]})
 print("INT02_V13_TEXT_PAGE",json.dumps({"page":page1,"native_characters":len(txt),"witnesses":findings[:7]},ensure_ascii=False),flush=True)
 pg=pdf.load_page(page1-1)
 pix=pg.get_pixmap(matrix=fitz.Matrix(1.1,1.1),alpha=False)
 jpg=pix.tobytes(output="jpeg",jpg_quality=25)
 out["rendered_jpeg_hashes"][str(page1)]=hashlib.sha256(jpg).hexdigest()
 print("INT02_V13_RENDER_PAGE_"+str(page1),base64.b64encode(jpg).decode(),flush=True)
pdf.close()
os.makedirs("g2d-v13-int02-source-index",exist_ok=True)
with open(f"g2d-v13-int02-source-index/batch-{batch}.json","w") as f:json.dump(out,f,indent=2)
print("INT02_V13_BATCH_COMPLETE",batch,len(BATCHES[batch]),"exact_origin_SHA_MATCH",True,"SCIENCE_FULL",False,flush=True)
