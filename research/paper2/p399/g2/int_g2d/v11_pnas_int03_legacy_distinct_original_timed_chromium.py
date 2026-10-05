#!/usr/bin/env python3
"""Last bounded DISTINCT legacy original PNAS first-party routes for INT03.
This is deliberately not PMC/author manuscript or search mirror substitute.
Each firstparty URL 10s. Legacy HTML Chromium fallback 16s. A 403, cookies,
metadata PDF or full webpage challenge always preserves HOLD; not QUALIFIED.
"""
import asyncio,hashlib,json,os,re,urllib.request,urllib.error
from io import BytesIO
from urllib.parse import urlparse
from datetime import datetime,timezone
from pypdf import PdfReader
from playwright.async_api import async_playwright
DOI="10.1073/pnas.95.24.14529"
URLS=[
 ("PNAS_LEGACY_FULL_PDF","https://www.pnas.org/content/95/24/14529.full.pdf"),
 ("PNAS_LEGACY_CANONICAL_PATH_PDF","https://www.pnas.org/content/pnas/95/24/14529.full.pdf"),
 ("PNAS_DOI_EPUB_PDF","https://www.pnas.org/doi/epdf/10.1073/pnas.95.24.14529"),
 ("PNAS_LEGACY_FULL_HTML","https://www.pnas.org/content/95/24/14529.full"),
 ("PNAS_DOI_FULL_JOURNAL_PARAM","https://www.pnas.org/doi/full/10.1073/pnas.95.24.14529?journalCode=pnas")]
def check(url,status,raw):
 h=(urlparse(url).hostname or "").lower()
 good=h=="pnas.org" or h.endswith(".pnas.org")
 r={"final_redacted_url":url.split("?")[0],"HTTP":status,"bytes":len(raw),
     "sha256":hashlib.sha256(raw).hexdigest(),"firstparty_host":good,
     "publisher_full_original_physically_qualified":False}
 if not good or status!=200:r["reason"]="firstparty host or 200 requirement fail";return r
 if raw.startswith(b"%PDF-"):
  try:
   pdf=PdfReader(BytesIO(raw),strict=False)
   title=" ".join((pdf.pages[i].extract_text() or "") for i in range(min(3,len(pdf.pages)))).lower()
   x={k:k in title for k in ("neuronal","model","global","workspace","effortful","tasks")}
   r.update(kind="PUBLISHED_PDF",pages=len(pdf.pages),title_tokens=x,source_identity_detected=sum(x.values())>=4)
   if len(pdf.pages)>=4 and r["source_identity_detected"]:r["publisher_full_original_physically_qualified"]=True
   else:r["reason"]="not complete PDF or not PNAS article identity"
  except Exception as e:r["reason"]="PDF parsing failed "+str(e)[:140]
 else:
  t=raw.decode("utf-8","replace").lower()
  anchors={k:bool(re.search(r"\b"+k+r"\b",t)) for k in ("abstract","workspace","stroop","introduction","model","discussion","references")}
  r.update(kind="HTML_OR_CHALLENGE",title_token_count=sum(k in t for k in ("neuronal","model","global","workspace")),required_sections=anchors)
  if len(t)>30000 and DOI.lower() in t and r["title_token_count"]>=4 and sum(anchors.values())>=5 and ("stroop" in t):
   r["publisher_full_original_physically_qualified"]=True
  else:r["reason"]="challenge/cookieAbsent/metadata without full article"
 return r
async def browser(url):
 bdata={"browser_path":url,"official_publisher_full_original":False}
 async with async_playwright() as p:
  b=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
  pg=await b.new_page()
  try:
   resp=await pg.goto(url,wait_until="domcontentloaded",timeout=16000)
   raw=await resp.body() if resp else b""
   probe=check(pg.url,resp.status if resp else 0,raw);probe["browser_dom_chars"]=len(await pg.content())
   bdata.update(probe);bdata["official_publisher_full_original"]=probe["publisher_full_original_physically_qualified"]
  except Exception as e:bdata["error"]=type(e).__name__+":"+str(e)[:190]
  await b.close()
 return bdata
out={"schema":"relaytheory.p399.g2d.v11_INT03_PNAS_distinct_publisher_legacy_routes.v1","utc":datetime.now(timezone.utc).isoformat(),
"runner_head":os.getenv("GITHUB_SHA"),"direct_per_request_timeout_seconds":10,"chromium_navigation_timeout_seconds":16,
"historical_v6_failed_original_run":37199967871,"all_attempts_are_firstparty_pnas_only":True,
"new_full_pnas_original_acquired":False,"full_original_source_semantically_qualified":False,
"PMC_mirror_or_author_manuscript_upgraded":False,"MAIN_authorized":False,"attempts":[]}
for label,url in URLS:
 a={"name":label,"url":url}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36","Accept":"application/pdf,text/html;q=0.7,*/*;q=0.2"})
  with urllib.request.urlopen(req,timeout=10) as r:
   data=r.read(12*1024*1024+1);status=r.status;final=r.geturl()
  if len(data)>12*1024*1024:raise ValueError("12MB cap")
  a.update(check(final,status,data))
  if a["publisher_full_original_physically_qualified"]:
   out["new_full_pnas_original_acquired"]=True
 except Exception as e:a["error"]=type(e).__name__+":"+str(e)[:150]
 out["attempts"].append(a);print("V11_PNAS_DISTINCT_DIRECT",json.dumps(a,sort_keys=True),flush=True)
if not out["new_full_pnas_original_acquired"]:
 x=asyncio.run(browser(URLS[3][1]));out["attempts"].append(x)
 out["new_full_pnas_original_acquired"]=x.get("official_publisher_full_original",False)
 print("V11_PNAS_LEGACY_CHROMIUM",json.dumps(x,sort_keys=True),flush=True)
os.makedirs("g2d-v11-legacy-pnas",exist_ok=True)
with open("g2d-v11-legacy-pnas/actual.json","w") as f:json.dump(out,f,indent=2)
print("V11_PNAS_FINAL",json.dumps({"publisher_full_original_physically_acquired":out["new_full_pnas_original_acquired"],"scientific_original_semantically_qualified":False,"main_authorized":False}),flush=True)
