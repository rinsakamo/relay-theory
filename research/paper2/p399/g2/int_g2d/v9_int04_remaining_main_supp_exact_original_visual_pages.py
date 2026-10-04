#!/usr/bin/env python3
"""G2-D v9 targeted original Nature 20+9+2 pages and remaining Fig3-7/Supp
limited render. The official browser page anchors source each PDF; no mirroring.
Each PDF request 12 sec; browser 18s. Raw SHA mandatory. Text pages indexed
for followup, not independent all math/fig science or secondary model fitness.
"""
import asyncio,base64,hashlib,json,os,re
from io import BytesIO
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from pypdf import PdfReader
import fitz
START="https://www.nature.com/articles/s41562-023-01799-z"
DOI="10.1038/s41562-023-01799-z"
MEDIA=[
("MAIN_PUBLISHED_VOR","https://www.nature.com/articles/s41562-023-01799-z.pdf",20,2666492,"b78a62b28775ec55610aeeca2252bc43b1ba782486c083a5065a3419ed3cde31"),
("PUBLISHER_SCIENTIFIC_SUPPLEMENT","https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41562-023-01799-z/MediaObjects/41562_2023_1799_MOESM1_ESM.pdf",9,2912573,"6f9baebc2f95492b4ce275c64ed0cb640105cd480d401b78dee09c5abbb03612"),
("PUBLISHER_REPORTING_SUMMARY","https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41562-023-01799-z/MediaObjects/41562_2023_1799_MOESM2_ESM.pdf",2,47812,"a9b713fbc8d39e24534ecaceb9c6deb53f13d36b0ec21843130bb69f67ad93bf")]
TERMS=("Fig. 1","Fig. 2","Fig. 3","Supplementary Fig.","not simulated","not modelled","not modeled","prediction error","replay","teacher","Hopfield","VAE","schema","limitations","lesion")
def allowed(url):
 h=(urlparse(url).hostname or "").lower()
 return any(h==d or h.endswith("."+d) for d in ("nature.com","springernature.com","springer.com"))
async def main():
 out={"schema":"relaytheory.p399.g2d.v9_INT04_Nature_targeted_remaining_original_figure_visual.v1",
 "runner_head":os.getenv("GITHUB_SHA"),"review_mode":os.getenv("INT04_REVIEW_MODE","main"),"timeout_seconds_each_pdf":12,"chromium_navigate_timeout_seconds":18,
 "base_g2_head":"69748673c80f421605f1c63607472903ac2ed68c",
 "no_pdf_original_binary_redistributed":True,"source_math_all_visually_qualified":False,
 "global_family_qualified":False,"backup_activated":0,"records":[]}
 async with async_playwright() as pl:
  b=await pl.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
  c=await b.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36")
  page=await c.new_page()
  resp=await page.goto(START,wait_until="domcontentloaded",timeout=18000)
  body=await page.locator("body").inner_text(timeout=5000)
  if not resp or resp.status!=200 or DOI not in body or len(body)<25000:raise ValueError("Nature official full browser original not physically exposed")
  official_links=await page.locator("a[href]").evaluate_all("""els=>els.map(a=>a.href)""")
  out["full_official_html_browser_pass"]=True
  for label,url,expected_pages,expected_bytes,expected_sha in MEDIA:
   a={"source":label,"expected_raw_sha256":expected_sha,"firstparty_article_anchor_confirmed":url in official_links,
      "raw_bytes":None,"exact_original_reacquired":False,"all_original_pixels_visually_audited":False}
   try:
    if url not in official_links:raise ValueError("Nature official article did not link exact firstparty published original")
    response=await c.request.get(url,timeout=12000)
    data=await response.body()
    a.update(status=response.status,actual_final_origin=urlparse(response.url).netloc,
      raw_bytes=len(data),actual_raw_sha256=hashlib.sha256(data).hexdigest(),
      pdf_signature=data[:5]==b"%PDF-")
    if not allowed(response.url) or not a["pdf_signature"] or len(data)!=expected_bytes or a["actual_raw_sha256"]!=expected_sha:
     raise ValueError("firstparty linked original raw byte signature, SHA or media mismatch")
    pdf=PdfReader(BytesIO(data),strict=False)
    texts=[(pg.extract_text() or "") for pg in pdf.pages]
    a["page_count"]=len(texts)
    if len(texts)!=expected_pages:raise ValueError("firstparty PDF unexpected page count")
    a["per_page_native_extractor_text_sha256"]=[hashlib.sha256(t.encode()).hexdigest() for t in texts]
    a["candidate_text_anchor_1based"]={term:[i+1 for i,t in enumerate(texts) if term.lower() in t.lower()] for term in TERMS}
    a["exact_original_reacquired"]=True
    mode=out["review_mode"]
    if (label=="MAIN_PUBLISHED_VOR" and mode=="main") or (label=="PUBLISHER_SCIENTIFIC_SUPPLEMENT" and mode=="supp"):
     target=([4,5,6,7,8,9,10,11,12,13] if mode=="main" else list(range(9)))
     for index in target:
      doc=fitz.open(stream=data,filetype="pdf");pg=doc.load_page(index)
      px=pg.get_pixmap(matrix=fitz.Matrix(1.48,1.48),alpha=False)
      jpeg=px.tobytes(output="jpeg",jpg_quality=41)
      out.setdefault("bounded_original_page_render_sha256",{})[label+"_P"+str(index+1)]=hashlib.sha256(jpeg).hexdigest()
      print("NATURE_V9_"+mode.upper()+"_P"+str(index+1)+"_JPEG",base64.b64encode(jpeg).decode(),flush=True)
      doc.close()
   except Exception as e:a["acquisition_or_verification_failure"]=type(e).__name__+":"+str(e)[:170]
   out["records"].append(a)
   print("NATURE_V9_RAW_SOURCE",json.dumps({k:v for k,v in a.items() if k!="per_page_native_extractor_text_sha256"},sort_keys=True),flush=True)
  await b.close()
 os.makedirs("g2d-v9-int04-figure-review",exist_ok=True)
 with open("g2d-v9-int04-figure-review/executed.json","w") as f:json.dump(out,f,indent=2)
 print("NATURE_V9_FINAL",json.dumps({"exact_publisher_media_reacquired":sum(a["exact_original_reacquired"] for a in out["records"]),"expected":3,"entire_21_media_main_supp_reporting_pages":sum(a.get("page_count",0) for a in out["records"]),"science_semantic_full_qualified":False}),flush=True)
if __name__=="__main__":asyncio.run(main())
