#!/usr/bin/env python3
"""Actual first-party browser media check (one fail-closed receipt per G2 missing work).
Do not use author manuscripts, third-party mirrors, search snippets or publisher preview
as proof of the COMPLETE published original; preserve previous working DOI roster.
"""
import asyncio,hashlib,json,os,re,time,urllib.parse
from pathlib import Path
from playwright.async_api import async_playwright
from pypdf import PdfReader
from io import BytesIO
WORKS={
"LRN-01":{"doi":"10.1038/s41467-025-58848-6","title":"Humans learn generalizable representations through efficient coding","pages":[("Nature VOR HTML","https://www.nature.com/articles/s41467-025-58848-6"),("Springer VOR HTML","https://link.springer.com/article/10.1038/s41467-025-58848-6")],"pdf":"https://www.nature.com/articles/s41467-025-58848-6.pdf"},
"PRD-01":{"doi":"10.1038/s41562-024-01930-8","title":"Humans adaptively deploy forward and backward prediction","pages":[("Nature updated original","https://www.nature.com/articles/s41562-024-01930-8")],"pdf":"https://www.nature.com/articles/s41562-024-01930-8.pdf","correction":"10.1038/s41562-024-01978-6"},
"ATT-03":{"doi":"10.1016/j.neuron.2009.01.002","title":"The Normalization Model of Attention","pages":[("Cell Neuron fulltext","https://www.cell.com/neuron/fulltext/S0896-6273(09)00003-8"),("ScienceDirect publisher","https://www.sciencedirect.com/science/article/pii/S0896627309000038")],"pdf":"https://www.cell.com/neuron/pdf/S0896-6273(09)00003-8.pdf"},
"BLF-01":{"doi":"10.1016/j.isci.2025.112844","title":"Belief updating in decision-variable space","pages":[("Cell iScience fulltext","https://www.cell.com/iscience/fulltext/S2589-0042(25)01105-8"),("ScienceDirect publisher","https://www.sciencedirect.com/science/article/pii/S2589004225011058")],"pdf":"https://www.cell.com/iscience/pdf/S2589-0042(25)01105-8.pdf"},
"INT-01":{"doi":"10.1016/j.cognition.2024.105967","title":"An algorithmic account for how humans efficiently learn","pages":[("ScienceDirect publisher fulltext","https://www.sciencedirect.com/science/article/pii/S0010027724002531")],"pdf":"https://www.sciencedirect.com/science/article/pii/S0010027724002531/pdfft?isDTMRedir=true&download=true"}
}
ALLOWED=("nature.com","springer.com","cell.com","sciencedirect.com","els-cdn.com")
def first_party(url):
 host=(urllib.parse.urlparse(url).hostname or "").lower()
 return any(host==d or host.endswith("."+d) for d in ALLOWED)
def fingerprint(doc,doi,title):
 lower=doc.lower()
 # Reject text extracted from short publisher paywall abstract, index, cookies or references
 words=set(re.findall(r"[a-z]{6,}",title.lower()))
 matches=sum(w in lower for w in words)
 full_anchors=[s for s in ("introduction","methods","results","discussion","references") if s in lower]
 suspicious=any(s in lower[:1000] for s in ("sign in to access","subscribe to journal","please enable cookies","captcha","access denied"))
 return dict(doi_literal=doi.lower() in lower,title_long_words_found=matches,word_count=len(re.findall(r"\b[a-z]{2,}\b",lower)),section_heading_tokens=full_anchors,
     missing_fullness=not (doi.lower() in lower and matches>=3 and len(full_anchors)>=4 and len(doc)>20000 and not suspicious))
async def run_one(p,slot,obj,sem):
 async with sem:
  out=dict(slot=slot,doi=obj["doi"],kind="BROWSER_FIRST_PARTY_DIAGNOSTIC",raw_published_original_pdf=None,verified_complete_original_html=None,attempts=[],source_eligible=False,full_math_figures_variants_verified=False)
  browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
  context=await browser.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",locale="en-US",accept_downloads=False)
  for label,url in obj["pages"]:
   row=dict(label=label,requested=url,first_party_response_complete=False)
   try:
    page=await context.new_page()
    r=await page.goto(url,wait_until="domcontentloaded",timeout=23000)
    await page.wait_for_timeout(1500)
    final=page.url
    body=await page.locator("body").inner_text(timeout=5000)
    html=await page.content()
    row.update(final_url=final,http_status=r.status if r else None,title=await page.title(),body_chars=len(body))
    if not first_party(final):raise ValueError("redirect_to_non_first_party_idp_or_other")
    detail=fingerprint(html+"\n"+body,obj["doi"],obj["title"])
    row["identity_and_fullness"]=detail
    if detail["missing_fullness"]:raise ValueError("publisher_response_does_not_expose_full_original")
    # publisher-owned complete live DOM confirmed, record both HTML snapshot & publisher response hash
    raw=await r.body()
    if len(raw)<20000:raise ValueError("publisher_original_response_raw_too_small")
    row.update(first_party_response_complete=True,html_response_sha256=hashlib.sha256(raw).hexdigest(),response_bytes=len(raw),rendered_dom_sha256=hashlib.sha256(html.encode()).hexdigest())
    if out["verified_complete_original_html"] is None:out["verified_complete_original_html"]={k:v for k,v in row.items() if k not in ("reason",)}
   except Exception as exc:row["reason"]=str(exc)[:150]
   finally:
    if 'page' in locals() and not page.is_closed():await page.close()
   out["attempts"].append(row)
  pdf=dict(requested=obj["pdf"],kind="FIRST_PARTY_ACTUAL_PDF")
  try:
   raw_resp=await context.request.get(obj["pdf"],timeout=20000)
   data=await raw_resp.body();url=raw_resp.url
   pdf.update(status=raw_resp.status,final_url=url,bytes=len(data),has_pdf_signature=data[:5]==b"%PDF-")
   if not first_party(url) or not data.startswith(b"%PDF-"):raise ValueError("publisher_pdf_not_obtained")
   rd=PdfReader(BytesIO(data),strict=False)
   first=" ".join((rd.pages[i].extract_text() or "") for i in range(min(2,len(rd.pages)))).lower()
   details=fingerprint(first,obj["doi"],obj["title"])
   if not details["doi_literal"] and details["title_long_words_found"]<3:raise ValueError("PDF_original_identity_unverified")
   pdf.update(actual_raw_sha256=hashlib.sha256(data).hexdigest(),page_count=len(rd.pages),page0_identity=details)
   out["raw_published_original_pdf"]=pdf.copy()
  except Exception as exc:pdf["reason"]=str(exc)[:150]
  out["attempts"].append(pdf)
  await browser.close()
  return out
async def main():
 async with async_playwright() as p:
  sem=asyncio.Semaphore(2)
  rows=await asyncio.gather(*(run_one(p,k,v,sem) for k,v in WORKS.items()))
  result={"schema":"p399.g2.v5.browser_owned_publisher_diagnostics","runner_sha":os.environ.get("GITHUB_SHA"),"source_fullness_heuristic_only":True,
         "requires_independent_human_visual_math_figure_negative_variant_review":True,"original_media_redistributed":False,"rows":rows,
         "raw_primary_pdfs_confirmed":sum(bool(z["raw_published_original_pdf"]) for z in rows),
         "complete_full_publisher_html_candidates_confirmed":sum(bool(z["verified_complete_original_html"]) for z in rows),
         "source_scientifically_admitted":0}
  Path("g2-v5-browser").mkdir(exist_ok=True)
  raw=(json.dumps(result,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
  Path("g2-v5-browser/diagnostic.json").write_bytes(raw)
  print("G2_V5_BROWSER_RAW_METADATA_SHA256",hashlib.sha256(raw).hexdigest())
  for row in rows:
   print("G2_V5",row["slot"],"PDF",row["raw_published_original_pdf"],"HTML",row["verified_complete_original_html"])
   for x in row["attempts"]:
    if x.get("reason"):print("G2_V5_FAIL",row["slot"],x["requested"],x["reason"],x.get("http_status") or x.get("status"))
  print("G2_V5_REAL_MEDIA_ACQUISITION",result["raw_primary_pdfs_confirmed"],result["complete_full_publisher_html_candidates_confirmed"],"SCIENCE_ADMITS",0)
if __name__=="__main__":asyncio.run(main())
