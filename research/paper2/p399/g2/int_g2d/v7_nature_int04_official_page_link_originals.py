#!/usr/bin/env python3
"""G2-D v7 publisher navigation source chase for INT04 (no mirror/manuscript).
Browser navigation 18s, each firstparty PDF URL 12s; never equate metadata,
rendered full HTML, or linked-only supplements with a raw published VOR PDF.
"""
import asyncio,hashlib,json,os,re,urllib.parse
from io import BytesIO
from playwright.async_api import async_playwright
from pypdf import PdfReader
DOI="10.1038/s41562-023-01799-z"
START="https://www.nature.com/articles/s41562-023-01799-z"
TITLE=("generative","memory","consolidation")
def allowed(url):
 h=(urllib.parse.urlparse(url).hostname or "").lower()
 return any(h==d or h.endswith("."+d) for d in ("nature.com","springer.com","springernature.com"))
def redacted(url):return url.split("?")[0]
def fingerprint(body):
 low=body.lower(); headings=("abstract","introduction","methods","results","discussion","references","supplementary information","data availability","code availability")
 return {"DOI_on_page":DOI in low,"title_terms":{v:v in low for v in TITLE},
   "scientific_section_witnesses":{v:v in low for v in headings},
   "visible_character_count":len(body),
   "fullness_heuristic_only":DOI in low and len(body)>22000 and all(v in low for v in TITLE)
   and sum(v in low for v in headings)>=5}
async def main():
 out={"schema":"p399.g2d.v7_nature_original_article_authoritative_link_chase.v1",
 "G2_exact_frozen_head":"69748673c80f421605f1c63607472903ac2ed68c",
 "runner_head":os.getenv("GITHUB_SHA"),"publisher_only":True,"browser_nav_timeout_s":18,
 "each_asset_request_timeout_s":12,"publisher_full_html_response_confirmed":False,
 "publisher_main_pdf_confirmed":False,"publisher_supplementary_pdf_confirmed":False,
 "all_math_figures_variants_independently_qualified":False,"main_authorized":False,
 "link_candidates":[],"attempts":[]}
 async with async_playwright() as pl:
  b=await pl.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
  c=await b.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",locale="en-US")
  pg=await c.new_page()
  try:
   res=await pg.goto(START,wait_until="domcontentloaded",timeout=18000)
   body=await pg.locator("body").inner_text(timeout=5000)
   html=await pg.content()
   raw=await res.body() if res else b""
   f=fingerprint(body)
   out["publisher_full_html_response_confirmed"]=res.status==200 and allowed(pg.url) and f["fullness_heuristic_only"] and len(raw)>20000
   out["publisher_page"]={"HTTP":res.status if res else None,"final_url":redacted(pg.url),
      "original_HTTP_body_bytes":len(raw),"publisher_original_HTTP_response_sha256":hashlib.sha256(raw).hexdigest(),
      "browser_DOM_sha256":hashlib.sha256(html.encode()).hexdigest(),"rendered_body_sha256":hashlib.sha256(body.encode()).hexdigest(),
      "fingerprint":f,"browser_DOM_is_not_same_thing_as_original_raw_pdf":True}
   print("V7_NATURE_ORIGINAL_PAGE",json.dumps(out["publisher_page"],sort_keys=True),flush=True)
   links=await pg.locator("a[href]").evaluate_all("""els=>els.map(a=>({title:(a.innerText||a.title||'').trim().slice(0,120),href:a.href})).filter(x=>x.href&&(/pdf/i.test(x.title)||/\\.pdf/i.test(x.href)))""")
   out["link_candidates"]=[{"label":x["title"],"url":redacted(x["href"]),"official_host":allowed(x["href"])} for x in links[:25]]
   # follow the actual page links; prioritize canonical article PDF and supplementary information, not unrelated reference PDFs
   cand=[];seen=set()
   for l in links:
    url=l["href"];low=(l["title"]+" "+url).lower()
    if not allowed(url) or url in seen or not ("pdf" in low):continue
    if DOI in low or "s41562-023-01799-z" in low or "41562_2023_1799_moesm" in low:
     kind="main" if "s41562-023-01799-z.pdf" in low or "10.1038/s41562-023-01799-z.pdf" in low else ("supplementary" if ("supp" in low or "moesm" in low) else "unresolved")
     cand.append((kind,url,l["title"]));seen.add(url)
   # include canonical official publisher PDF independently; if not linked, record it as candidate and verify, not assume
   canonical=START+".pdf"
   if canonical not in seen:cand.insert(0,("main",canonical,"publisher DOI PDF canonical"))
   out["candidate_count"]=len(cand)
   for kind,url,title in cand[:8]:
    a={"kind":kind,"page_anchor_title":title,"requested_url":redacted(url),"publisher_page_anchor":any(l["href"]==url for l in links),
      "official_original_pdf_accepted":False}
    try:
     resp=await c.request.get(url,timeout=12000)
     data=await resp.body()
     a.update(status=resp.status,final_url=redacted(resp.url),raw_bytes=len(data),
      response_sha256=hashlib.sha256(data).hexdigest(),pdf_magic=data[:5]==b"%PDF-",trusted_final_host=allowed(resp.url))
     if len(data)>18*1024*1024:raise ValueError("over18MB")
     if not a["trusted_final_host"] or not data.startswith(b"%PDF-"):raise ValueError("not genuine firstparty raw PDF")
     pdf=PdfReader(BytesIO(data),strict=False)
     first=" ".join((pdf.pages[i].extract_text() or "") for i in range(min(2,len(pdf.pages)))).lower()
     a["page_count"]=len(pdf.pages)
     a["publisher_article_DOI_in_first_two"]=DOI in first
     a["publisher_article_title_first_two"]=all(w in first for w in TITLE)
     if kind=="main" and len(pdf.pages)>=15 and a["publisher_article_title_first_two"]:
      a["official_original_pdf_accepted"]=True;out["publisher_main_pdf_confirmed"]=True
     if kind=="supplementary" and a["publisher_page_anchor"] and len(pdf.pages)>=2:
      a["official_original_pdf_accepted"]=True;out["publisher_supplementary_pdf_confirmed"]=True
     if not a["official_original_pdf_accepted"]:a["reason"]="pdf but source supplement/main classification unproven"
    except Exception as e:a["error"]=type(e).__name__+":"+str(e)[:160]
    out["attempts"].append(a)
    print("V7_NATURE_LINKED_PDF",json.dumps(a,sort_keys=True),flush=True)
  except Exception as e:out["article_or_browser_error"]=type(e).__name__+":"+str(e)[:180]
  await b.close()
 os.makedirs("g2d-v7-nature-official-links",exist_ok=True)
 with open("g2d-v7-nature-official-links/receipt.json","w") as f:json.dump(out,f,indent=2)
 print("V7_FINAL_REAL",json.dumps({k:out[k] for k in ("publisher_full_html_response_confirmed","publisher_main_pdf_confirmed","publisher_supplementary_pdf_confirmed","all_math_figures_variants_independently_qualified")}),flush=True)
if __name__=="__main__":asyncio.run(main())
