#!/usr/bin/env python3
"""G2-D: INT08 source-native firstparty comparator for bounded INT04 pair ancestry.
12s direct official eLife v3 original expected legacy G2 SHA. Chromium fallback
only if first-party original raw fails; never auto-admit all math / global family.
"""
import asyncio,hashlib,json,os,re,urllib.request,urllib.error
from io import BytesIO
from pypdf import PdfReader
from playwright.async_api import async_playwright
DOI="10.7554/eLife.74445"
EXPECTED="89f8846ab34dbc5af0d4079423ff51e00c1873b6149c48217b547b1bdcb678da"
PDF="https://cdn.elifesciences.org/articles/74445/elife-74445-v3.pdf"
PAGE="https://elifesciences.org/articles/74445"
KEYS=["episodic memory","LSTM","actor critic","actor-critic","leaky competing accumulator","LCA","memory gate","gate","policy","A2C","retrieval","encoding","limitation","ablation"]
r={"schema":"relaytheory.p399.g2d.v10_INT08_elife_original_12s_firstparty_and_fallback.v1","runner_head":os.getenv("GITHUB_SHA"),"original_expected_frozen_g2_SHA256":EXPECTED,"individual_pdf_timeout_s":12,"browser_nav_timeout_s":18,
"physical_original_reacquired_exact_G2_sha":False,"full_original_independent_science_qualified":False,"pairwise_independence_qualified":False,"MAIN_authorized":False,"attempts":[]}
try:
 req=urllib.request.Request(PDF,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36","Accept":"application/pdf"})
 with urllib.request.urlopen(req,timeout=12) as resp:
  raw=resp.read(15*1024*1024+1)
  final=resp.geturl();status=resp.status
 a={"url":PDF,"final_noquery":final.split("?")[0],"status":status,"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"signature_pdf":raw.startswith(b"%PDF-")}
 if not final.startswith("https://cdn.elifesciences.org/articles/74445/") or len(raw)>15*1024*1024 or not a["signature_pdf"]:raise ValueError("firstparty original URL/pdf authenticity failed")
 doc=PdfReader(BytesIO(raw),strict=False);a["pdf_pages"]=len(doc.pages)
 text=[pg.extract_text() or "" for pg in doc.pages]
 a["source_native_page_sha256"]=[hashlib.sha256(t.encode()).hexdigest() for t in text]
 a["terms_1based"]={q:[i+1 for i,t in enumerate(text) if q.lower() in t.lower()] for q in KEYS}
 a["title_on_first_page"]=all(q in text[0].lower() for q in ("episodic","memory"))
 a["matched_G2_frozen_SHA256"]=a["sha256"]==EXPECTED
 r["physical_original_reacquired_exact_G2_sha"]=a["matched_G2_frozen_SHA256"] and a["title_on_first_page"] and len(text)>=8
 a["firstparty_verified"]=r["physical_original_reacquired_exact_G2_sha"]
 # v10b strict contiguous-string false negative: publisher PDF extraction splits lines/punctuation. Preserve original run as failed phrase detection.
 def witnessed_manual_policy(t):
  norm=" ".join(t.lower().replace("\\xad","").split())
  return bool(re.search(r"imposed.{0,45}by\\s+hand.{0,90}encoding\\s+policy",norm))
 a["human_comparison_hand_fixed_end_of_event_encoding_condition"] = any(witnessed_manual_policy(t) for t in text)
 a["manual_policy_text_witness_1based_pages"]=[i+1 for i,t in enumerate(text) if witnessed_manual_policy(t)]
 print("V10_INT08_ACTUAL_RAW_PDF",json.dumps({k:a.get(k) for k in ("status","bytes","sha256","pdf_pages","title_on_first_page","matched_G2_frozen_SHA256","human_comparison_hand_fixed_end_of_event_encoding_condition","manual_policy_text_witness_1based_pages")},sort_keys=True),flush=True)
 for page_no in sorted({1,2,3,4,5,6,7,8,min(len(text),12),min(len(text),16),min(len(text),20)}):
  t=text[page_no-1]
  matches=[]
  for q in KEYS:
   m=re.search(re.escape(q),t,re.I)
   if m:matches.append({"term":q,"window":" ".join(t[max(0,m.start()-80):min(len(t),m.end()+180)].split())[:250]})
  if matches:print("V10_INT08_BOUNDED_NATIVE_PAGE",json.dumps({"page":page_no,"witnesses":matches[:5]},sort_keys=True),flush=True)
 r["attempts"].append(a)
except Exception as e:r["attempts"].append({"url":PDF,"error":type(e).__name__+":"+str(e)[:170]})
async def backup_browser():
 async with async_playwright() as p:
  b=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
  page=await b.new_page()
  a={"requested":PAGE}
  try:
   res=await page.goto(PAGE,wait_until="domcontentloaded",timeout=18000)
   html=await page.content();body=await page.locator("body").inner_text(timeout=4500)
   a.update(http=res.status if res else None,final_url=page.url.split("?")[0],rendered_dom_sha256=hashlib.sha256(html.encode()).hexdigest(),visible_body_chars=len(body),
    official_complete_html_candidate=bool(res and res.status==200 and len(body)>18000 and DOI.lower() in html.lower() and all(x in body.lower() for x in ("episodic","memory","methods","results"))))
  except Exception as e:a["error"]=type(e).__name__+":"+str(e)[:170]
  await b.close();return a
if not r["physical_original_reacquired_exact_G2_sha"]:
 r["attempts"].append(asyncio.run(backup_browser()))
os.makedirs("g2d-v10-elife-int08-firstparty",exist_ok=True)
with open("g2d-v10-elife-int08-firstparty/executed.json","w") as f:json.dump(r,f,indent=2)
print("V10_INT08_INDEPENDENT_SOURCE_RECEIPT",json.dumps({k:v for k,v in r.items() if k!="attempts"},sort_keys=True),flush=True)
if not r["physical_original_reacquired_exact_G2_sha"]:print("V10_INT08_HOLD_NOT_EXACT_RAW_ORIGINAL",flush=True)
