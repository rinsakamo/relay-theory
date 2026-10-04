#!/usr/bin/env python3
"""Last distinct official-browser routes for G2-D INT01 only. No manuscript substitution.
Version metadata, publisher body and raw PDF access are independently recorded.
Never output original full text/PDF or auto-promote science.
"""
import asyncio, hashlib, json, os, re
from urllib.parse import urlparse
from io import BytesIO
from playwright.async_api import async_playwright
from pypdf import PdfReader

PII="S0010027724002531"
DOI="10.1016/j.cognition.2024.105967"
TITLE="An algorithmic account for how humans efficiently learn"
PAGES=[
 ("SD_DIRECT_DOM","https://www.sciencedirect.com/science/article/pii/"+PII),
 ("SD_VIA_IHUB_DOM","https://www.sciencedirect.com/science/article/pii/"+PII+"?via%3Dihub"),
 ("ELSEVIER_LINKING_HUB_DOM","https://linkinghub.elsevier.com/retrieve/pii/"+PII)
]
PDFS=[
 ("SCIENCEDIRECT_REDIRECTED_PDF","https://www.sciencedirect.com/science/article/pii/"+PII+"/pdfft?isDTMRedir=true&download=true"),
 ("ELSEVIER_ARTICLE_CDN_PDF","https://ars.els-cdn.com/content/image/1-s2.0-"+PII+"-main.pdf")
]
def publisher(url):
 h=(urlparse(url).hostname or "").lower()
 return any(h==x or h.endswith("."+x) for x in ("sciencedirect.com","elsevier.com","els-cdn.com"))
def fullness(s):
 t=s.lower()
 refs={x:bool(re.search(r"\b"+x+r"\b",t)) for x in ("abstract","introduction","methods","results","discussion","references")}
 return dict(doi_literal=DOI.lower() in t,pii_literal=PII.lower() in t,
             title_identifiers={x:x in t for x in ("algorithmic","efficiently","learn")},
             structural_sections=refs,body_chars=len(s),
             candidate_fullness=len(s)>22000 and sum(refs.values())>=4
             and sum(x in t for x in ("algorithmic","efficiently","learn"))>=2
             and (DOI.lower() in t or PII.lower() in t))
async def main():
 out={"schema":"relaytheory.p399.g2d.int01_distinct_chromium_official_paths.v1",
      "scope":"SOURCE_RESCUE_ONLY_NOT_SCIENTIFIC_ADMISSION","runner_head":os.getenv("GITHUB_SHA"),
      "official_complete_html_obtained":False,"official_pdf_obtained":False,
      "full_published_math_figures_variants_negatives_audited":False,
      "attempts":[]}
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
  context=await browser.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                                  locale="en-US")
  for label,url in PAGES:
   r={"item":label,"requested":url,"obtained_candidate_full_HTML":False}
   pg=None
   try:
    pg=await context.new_page()
    res=await pg.goto(url,wait_until="domcontentloaded",timeout=14500)
    await pg.wait_for_timeout(1000)
    final=pg.url; dom=await pg.content(); body=await pg.locator("body").inner_text(timeout=2500)
    r.update(final_url=final,status=res.status if res else None,dom_sha256=hashlib.sha256(dom.encode()).hexdigest(),fingerprint=fullness(body))
    if not publisher(final):raise ValueError("redirect_nonpublisher")
    if not r["fingerprint"]["candidate_fullness"]:raise ValueError("publisher_response_preview_or_challenge")
    raw=await res.body()
    if len(raw)<20000:raise ValueError("raw_html_short")
    r.update(raw_html_sha256=hashlib.sha256(raw).hexdigest(),raw_bytes=len(raw),obtained_candidate_full_HTML=True)
    out["official_complete_html_obtained"]=True
   except Exception as e:r["error"]=type(e).__name__+":"+str(e)[:180]
   finally:
    if pg:await pg.close()
   out["attempts"].append(r)
   print("BROWSER_HTML",json.dumps(r,sort_keys=True),flush=True)
  for label,url in PDFS:
   r={"item":label,"requested":url,"obtained_published_pdf":False}
   try:
    resp=await context.request.get(url,timeout=13000)
    data=await resp.body();r.update(status=resp.status,final_url=resp.url,bytes=len(data),pdf_signature=data[:5]==b"%PDF-")
    if not publisher(resp.url) or not data.startswith(b"%PDF-"):raise ValueError("not_publisher_original_pdf")
    rd=PdfReader(BytesIO(data));first=" ".join((rd.pages[i].extract_text() or "") for i in range(min(2,len(rd.pages)))).lower()
    if not (PII.lower() in first.replace(" ","") or ("algorithmic" in first and "learn" in first)):raise ValueError("publisher_pdf_identity_unresolved")
    r.update(pages=len(rd.pages),sha256=hashlib.sha256(data).hexdigest(),obtained_published_pdf=True)
    out["official_pdf_obtained"]=True
   except Exception as e:r["error"]=type(e).__name__+":"+str(e)[:180]
   out["attempts"].append(r)
   print("BROWSER_PDF",json.dumps(r,sort_keys=True),flush=True)
  await browser.close()
 os.makedirs("g2d-int01-browser",exist_ok=True)
 with open("g2d-int01-browser/source_paths.json","w") as f:json.dump(out,f,indent=2)
 print("INT01_PUBLISHER_PHYSICAL",out["official_complete_html_obtained"],out["official_pdf_obtained"],
       "SCIENTIFIC_QUALIFIED",False,flush=True)
if __name__=="__main__":asyncio.run(main())
