#!/usr/bin/env python3
"""G2-D selected INT02 publisher original only; 12s/request, Chromium 18s fallback.
Freeze exact previously verified G2 PDF raw SHA. Never promote mirror/manuscript.
Extract only bounded native figure/math/negative page locators; no copyrighted PDF.
"""
import asyncio,hashlib,json,os,re,urllib.request,urllib.error
from urllib.parse import urlparse
from io import BytesIO
from datetime import datetime,timezone
from playwright.async_api import async_playwright
from pypdf import PdfReader
BASE="https://www.mdpi.com/1099-4300/26/6/484"
DOI="10.3390/e26060484"
SHA="a1e644c826bf1b356187bc556d5947eb23638f3f9bc6c61835d46850b4f1cc37"
URLS=[BASE+"/pdf",BASE, "https://mdpi-res.com/d_attachment/entropy/entropy-26-00484/article_deploy/entropy-26-00484.pdf"]
TERMS=("planning","learning","counterfactual","mixed","complexity","reward","grid","Figure 1","Figure 2","Figure 3","Figure 4","Figure 5","Figure 6","Table 1","limitation","simulation","policy")
def trusted(url):
 host=(urlparse(url).hostname or "").lower()
 return host in ("mdpi.com","www.mdpi.com","mdpi-res.com","www.mdpi-res.com")
def examine(url,status,data,mode):
 item={"mode":mode,"final_url":url,"http_status":status,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"pdf_magic":data[:5]==b"%PDF-","firstparty_publisher_host":trusted(url),"original_full_qualified":False}
 if not trusted(url):item["error"]="unexpected final host";return item
 if data[:5]==b"%PDF-":
  try:
   p=PdfReader(BytesIO(data),strict=False)
   text=[x.extract_text() or "" for x in p.pages]
   front=" ".join(text[:2]).lower()
   item["pages"]=len(p.pages)
   item["firsttwo_identity_title_tokens"]={t:t in front for t in ("predictive","planning","counterfactual","inference")}
   item["same_frozen_g2_original_sha"]=item["sha256"]==SHA
   item["page_native_text_sha256"]=[hashlib.sha256(t.encode()).hexdigest() for t in text]
   item["term_pages_1_based"]={term:[i+1 for i,t in enumerate(text) if term.lower() in t.lower()] for term in TERMS}
   item["original_full_qualified"]=item["same_frozen_g2_original_sha"] and len(text)>=10 and sum(item["firsttwo_identity_title_tokens"].values())>=3
   if not item["original_full_qualified"]:item["error"]="publisher PDF identity or exact G2 hash mismatch"
  except Exception as e:item["error"]="PDF_"+type(e).__name__+":"+str(e)[:125]
 else:
  t=data.decode("utf-8","replace").lower()
  item["html_doi_present"]=DOI in t
  item["html_title_terms_present"]={x:x in t for x in ("predictive","planning","counterfactual","inference")}
  item["html_section_witnesses"]={x:bool(re.search(r"\b"+x+r"\b",t)) for x in ("abstract","introduction","methods","results","discussion","references")}
  item["publisher_full_html_heuristic"]=DOI in t and len(t)>35000 and sum(item["html_section_witnesses"].values())>=4 and sum(item["html_title_terms_present"].values())>=3
 return item
async def main():
 out={"schema":"p399_g2d_v12_selected_INT02_exact_original_timeout_chromium_v1","doi":DOI,"expected_g2_raw_sha":SHA,"runner_head":os.getenv("GITHUB_SHA"),
 "max_http_timeout_s":12,"fallback_chromium_nav_timeout_s":18,"copyright_pdf_binaries_redistributed":False,
 "source_exact_original_found":False,"all_math_fig_semantically_audited":False,"main_authorized":False,"attempts":[]}
 for url in URLS:
  r={"method":"12s_HTTP_DIRECT","requested":url}
  try:
   req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125 Safari/537.36","Accept":"application/pdf,text/html;q=0.9,*/*;q=0.8"})
   with urllib.request.urlopen(req,timeout=12) as resp:
    data=resp.read(20*1024*1024+1)
    if len(data)>20*1024*1024:raise ValueError("20 MiB source cap")
    r.update(examine(resp.geturl(),resp.status,data,"12s_HTTP_DIRECT"))
  except Exception as e:r["error"]=type(e).__name__+":"+str(e)[:160]
  out["attempts"].append(r)
  print("INT02_V12_DIRECT",json.dumps({k:v for k,v in r.items() if k!="page_native_text_sha256"},ensure_ascii=False),flush=True)
  if r.get("original_full_qualified"):out["source_exact_original_found"]=True
 if not out["source_exact_original_found"]:
  async with async_playwright() as p:
   browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
   context=await browser.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36")
   page=await context.new_page()
   r={"method":"CHROMIUM_FALLBACK","requested":BASE}
   try:
    resp=await page.goto(BASE,wait_until="domcontentloaded",timeout=18000)
    body=await page.locator("body").inner_text(timeout=4000)
    html=(await page.content()).encode()
    r.update(examine(page.url,resp.status if resp else None,html,"CHROMIUM_RENDERED_DOM"))
    r["rendered_visible_chars"]=len(body)
    links=await page.locator("a[href]").evaluate_all("""els=>els.map(a=>a.href).filter(s=>s.includes('pdf'))""")
    r["official_page_pdf_link_candidates"]=[x for x in links if trusted(x) and ("484" in x or "00484" in x)][:8]
    for u in r["official_page_pdf_link_candidates"][:3]:
     attempt={"method":"CHROMIUM_SESSION_PUBLISHER_PDF_12S","requested":u}
     try:
      pres=await context.request.get(u,timeout=12000)
      raw=await pres.body()
      attempt.update(examine(pres.url,pres.status,raw,"CHROMIUM_SESSION_PUBLISHER_PDF_12S"))
      if attempt["original_full_qualified"]:out["source_exact_original_found"]=True
     except Exception as e:attempt["error"]=type(e).__name__+":"+str(e)[:170]
     out["attempts"].append(attempt)
     print("INT02_V12_BROWSER_PDF",json.dumps({k:v for k,v in attempt.items() if k!="page_native_text_sha256"},ensure_ascii=False),flush=True)
   except Exception as e:r["error"]=type(e).__name__+":"+str(e)[:140]
   out["attempts"].append(r)
   print("INT02_V12_BROWSER",json.dumps({k:v for k,v in r.items() if k!="page_native_text_sha256"},ensure_ascii=False),flush=True)
   await browser.close()
 os.makedirs("g2d-v12-int02-original",exist_ok=True)
 with open("g2d-v12-int02-original/receipt.json","w") as f:json.dump(out,f,indent=2)
 print("INT02_V12_FINAL",json.dumps({"source_exact_original_found":out["source_exact_original_found"],"all_math_fig_semantically_audited":False,"route_count":len(out["attempts"])}),flush=True)
if __name__=="__main__":asyncio.run(main())
