#!/usr/bin/env python3
"""G2-D: strict first-party INT03/INT04 main official VOR firstparty-source rescue.
Each HTTP request 12s; failed direct publisher PDF+HTML -> bounded independent
Chromium publisher browser 18s navigation. Preserve per-route failures and never
elevate author manuscripts, PMC, metadata or thirdparty mirrors.
"""
import asyncio,hashlib,json,os,re,time,urllib.request,urllib.error
from io import BytesIO
from urllib.parse import urlparse
from pypdf import PdfReader
from playwright.async_api import async_playwright
SOURCE={
 "INT-03":{"doi":"10.1073/pnas.95.24.14529","title_words":["neuronal","model","global","workspace"],
  "pdf":["https://www.pnas.org/doi/pdf/10.1073/pnas.95.24.14529","https://www.pnas.org/doi/pdf/10.1073/pnas.95.24.14529?download=1"],
  "html":["https://www.pnas.org/doi/full/10.1073/pnas.95.24.14529"]},
 "INT-04":{"doi":"10.1038/s41562-023-01799-z","title_words":["generative","model","memory","consolidation"],
  "pdf":["https://www.nature.com/articles/s41562-023-01799-z.pdf","https://link.springer.com/content/pdf/10.1038/s41562-023-01799-z.pdf"],
  "html":["https://www.nature.com/articles/s41562-023-01799-z"]}}
PUBLISHERS={"INT-03":{"pnas.org"},"INT-04":{"nature.com","springer.com","springernature.com"}}
CAP=18*1024*1024
def trusted(slot,url):
 host=(urlparse(url).hostname or "").lower()
 return any(host==p or host.endswith("."+p) for p in PUBLISHERS[slot])
def classify(slot,url,status,raw,mode):
 d={"mode":mode,"final_url":url,"status":status,"bytes":len(raw),
    "raw_sha256":hashlib.sha256(raw).hexdigest(),"trusted_final_host":trusted(slot,url),
    "accepted_full_publisher_original":False,"independent_math_figure_science_qualified":False}
 if len(raw)>CAP: d["reason"]="18MB cap"; return d
 x=SOURCE[slot]
 if not d["trusted_final_host"]: d["reason"]="nonfirstparty final host"; return d
 if raw.startswith(b"%PDF-"):
  try:
   pdf=PdfReader(BytesIO(raw),strict=False);n=len(pdf.pages)
   title=" ".join((pdf.pages[i].extract_text() or "") for i in range(min(2,n))).lower()
   tokens={s:s in title for s in x["title_words"]}
   d.update(media="pdf",page_count=n,first_two_page_title_token_witnesses=tokens)
   if n>=5 and sum(tokens.values())>=3:
    d["accepted_full_publisher_original"]=True
   else:d["reason"]="source identity or complete main not proven"
  except Exception as e:d["reason"]="PDF_parse_"+type(e).__name__+":"+str(e)[:120]
 else:
  page=raw.decode("utf-8","replace").lower()
  token={s:s in page for s in x["title_words"]}
  sections={s:bool(re.search(r"\\b"+s+r"\\b",page)) for s in ("abstract","introduction","methods","results","references")}
  d.update(media="html",title_token_witnesses=token,section_indicators=sections)
  if len(page)>27000 and sum(token.values())>=3 and sum(sections.values())>=3 and (x["doi"].lower() in page):
   d["accepted_full_publisher_original"]=True
  else:d["reason"]="preview_or_captcha_metadata_short_OR_unidentified"
 return d
async def chromium_probe(p,slot,url):
 d={"method":"CHROMIUM_AFTER_DIRECT_FAILURE","requested":url}
 browser=None
 try:
  browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
  context=await browser.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",locale="en-US")
  page=await context.new_page()
  res=await page.goto(url,wait_until="domcontentloaded",timeout=18000)
  final=page.url
  data=(await page.content()).encode()
  cls=classify(slot,final,res.status if res else None,data,"browser_DOM_raw_rendered")
  cls["visible_body_length"]=len(await page.locator("body").inner_text(timeout=4000))
  d.update(cls)
 except Exception as e:d["error"]=type(e).__name__+":"+str(e)[:160]
 finally:
  if browser:await browser.close()
 return d
async def main():
 out={"schema":"p399_g2d_v6_selected_int03_04_official_only_timeout_chromium_rescue.v1",
 "runner_head":os.getenv("GITHUB_SHA"),"HTTP_TIMEOUT_SECONDS":12,"BROWSER_NAV_TIMEOUT_MS":18000,
 "full_scientific_original_qualified":0,"g2_main_roster_modified":False,"main_authorized":False,"records":[]}
 async with async_playwright() as p:
  for slot,x in SOURCE.items():
   record={"slot":slot,"doi":x["doi"],"raw_publisher_main_pdf":None,
           "publisher_full_html_candidate":None,"attempts":[],"no_manuscript_or_mirror_substitutions":True}
   for url in x["pdf"]+x["html"]:
    a={"method":"DIRECT_FIRSTPARTY_BOUND_12S","requested":url}
    try:
     req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36","Accept":"application/pdf,text/html;q=0.8,*/*;q=0.1"})
     with urllib.request.urlopen(req,timeout=12) as resp:
      raw=resp.read(CAP+1);cls=classify(slot,resp.geturl(),resp.status,raw,"firstparty_actual_http_response")
     a.update(cls)
    except Exception as e:a["error"]=type(e).__name__+":"+str(e)[:160]
    record["attempts"].append(a);print("INT_V6_DIRECT",slot,json.dumps(a,sort_keys=True),flush=True)
    if a.get("accepted_full_publisher_original"):
     if a.get("media")=="pdf" and not record["raw_publisher_main_pdf"]:record["raw_publisher_main_pdf"]=a.copy()
     if a.get("media")=="html" and not record["publisher_full_html_candidate"]:record["publisher_full_html_candidate"]=a.copy()
   if not record["raw_publisher_main_pdf"]:
    for url in x["html"][:1]:
     a=await chromium_probe(p,slot,url);record["attempts"].append(a)
     print("INT_V6_CHROMIUM",slot,json.dumps(a,sort_keys=True),flush=True)
     if a.get("accepted_full_publisher_original") and not record["publisher_full_html_candidate"]:
      record["publisher_full_html_candidate"]=a.copy()
     # Chromium must not claim a full PDF based only on a rendered article.
   out["records"].append(record)
 os.makedirs("g2d-v6-int03-04-rescue",exist_ok=True)
 with open("g2d-v6-int03-04-rescue/physical_verification.json","w") as f:json.dump(out,f,indent=2)
 print("INT_V6_FINAL",json.dumps([{"slot":r["slot"],"publisher_pdf":bool(r["raw_publisher_main_pdf"]),
 "publisher_html":bool(r["publisher_full_html_candidate"])} for r in out["records"]]),flush=True)
if __name__=="__main__":asyncio.run(main())
