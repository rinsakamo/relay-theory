#!/usr/bin/env python3
"""Independent physical re-acquisition of the exact Nature published original LRN-01.
Source media admission technical only, no MAIN science, no publisher PDF redistribution.
"""
import asyncio,hashlib,io,json,os,re
from pathlib import Path
from pypdf import PdfReader
from playwright.async_api import async_playwright
URL="https://www.nature.com/articles/s41467-025-58848-6"
DOI="10.1038/s41467-025-58848-6"
TITLE="Humans learn generalizable representations through efficient coding"
BASE="638c40d95b03e9ed076949c1c17f469bed4e1c3c9959ca8a84dc65c8a0744718"
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
  c=await browser.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",locale="en-US")
  row={"schema":"p399.g2.lrn01.independent_source_reacquisition.v1","first_experiment_run":37185492865,"first_raw_original_sha256":BASE,
       "first_pages":20,"second_run_sha":os.getenv("GITHUB_SHA"),"doi":DOI,"published_original_raw_byte_verified":False,
       "full_source_semantic_eligible":False,"scientific_source_reconstruction_executed":False,"attempts":[]}
  try:
   page=await c.new_page();resp=await page.goto(URL,wait_until="domcontentloaded",timeout=40000)
   await page.wait_for_timeout(1400)
   body=await page.locator("body").inner_text(timeout=10000)
   raw=await resp.body()
   row["html_original"]={"status":resp.status,"url":page.url,"raw_sha256":hashlib.sha256(raw).hexdigest(),"raw_bytes":len(raw),
     "rendered_full_body_chars":len(body),"doi_found":DOI.lower() in body.lower(),
     "full_original_sections_presence":{k:k in body.lower() for k in ("introduction","methods","results","discussion","references")}}
   row["attempts"].append("official html browser original returned")
   pdf=await c.request.get(URL+".pdf",timeout=55000)
   data=await pdf.body();reader=PdfReader(io.BytesIO(data),strict=False) if data.startswith(b"%PDF-") else None
   text0=" ".join((p.extract_text() or "") for p in reader.pages[:2]).lower() if reader else ""
   filesha=hashlib.sha256(data).hexdigest()
   meta={"status":pdf.status,"url":pdf.url,"raw_sha256":filesha,"raw_bytes":len(data),
     "pages":len(reader.pages) if reader else 0,"doi_found":DOI.lower() in text0,
     "title_found":all(word in text0 for word in ("humans","representations","efficient","coding")),
     "cross_run_sha256_equal":filesha==BASE,"contains_full_pdf_signature":data.startswith(b"%PDF-")}
   row["pdf_publisher"]=meta
   row["published_original_raw_byte_verified"]=all([
      pdf.status==200,meta["contains_full_pdf_signature"],meta["doi_found"],meta["title_found"],
      meta["pages"]==20,meta["cross_run_sha256_equal"],row["html_original"]["doi_found"],
      row["html_original"]["rendered_full_body_chars"]>20000,
      all(row["html_original"]["full_original_sections_presence"].values())
   ])
   if row["published_original_raw_byte_verified"]:
    # No PDF committed. Page text hashes verify 20-page extracted content without releasing source text.
    row["source_page_extracted_text_sha256"]=[hashlib.sha256((p.extract_text() or "").encode()).hexdigest() for p in reader.pages]
    row["full_20_page_extractable"] = all(len(p.extract_text() or "")>200 for p in reader.pages[:19])
    row["publisher_original_version_record"]={"venue":"Nature Communications 16 article 3989","published_online":"2025-04-29","source_document_DOI":DOI}
  except Exception as e:row["error"]=repr(e)[:200]
  finally:await browser.close()
  Path("g2-lrn01").mkdir(exist_ok=True)
  raw=(json.dumps(row,sort_keys=True,ensure_ascii=False,separators=(",",":"))+"\n").encode()
  Path("g2-lrn01/independent_original_receipt.json").write_bytes(raw)
  print("G2_LRN01_INDEPENDENT_RECEIPT_SHA256",hashlib.sha256(raw).hexdigest())
  print("G2_LRN01_SECOND_PUBLISHER_PDF",row.get("pdf_publisher"))
  print("G2_LRN01_HTML_FULL_ORIGINAL",row.get("html_original"))
  print("G2_LRN01_REPRODUCED_RAW_ORIGINAL",row["published_original_raw_byte_verified"])
  print("G2_LRN01_NO_SCIENCE_ADMISSION",not row["full_source_semantic_eligible"])
  if not row["published_original_raw_byte_verified"]:raise RuntimeError("LRN01 original physical repeat acquisition not independently verified")
if __name__=="__main__":asyncio.run(main())
