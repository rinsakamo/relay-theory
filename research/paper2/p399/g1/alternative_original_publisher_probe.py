#!/usr/bin/env python3
"""Attempt exact original publisher VOR PDF alternatives; NO automatic replacement/admission.

This is a *pre-A source accessibility* screen only. The copyright originals are kept
in memory and never copied into public Git or uploaded as Actions artifacts.
"""
import concurrent.futures,datetime,hashlib,io,json,urllib.request
from pathlib import Path
from pypdf import PdfReader
LEADS={
 "ALT_P08_ELIFE101157_VOR3":{"publisher":"eLife","doi":"10.7554/eLife.101157.3","source_urls":["https://cdn.elifesciences.org/articles/101157/elife-101157-v3.pdf","https://elifesciences.org/articles/101157.pdf"],"version":"published VOR 3, confirm header/metadata"},
 "ALT_P12_ELIFE39497_VOR_UPDATED":{"publisher":"eLife","doi":"10.7554/eLife.39497","source_urls":["https://cdn.elifesciences.org/articles/39497/elife-39497-v3.pdf","https://cdn.elifesciences.org/articles/39497/elife-39497-v2.pdf","https://elifesciences.org/articles/39497.pdf"],"version":"2018-10-19 updated VOR, do not treat unverified older PDF as latest"},
 "ALT_P16_ELIFE97894_VOR3":{"publisher":"eLife","doi":"10.7554/eLife.97894.3","source_urls":["https://cdn.elifesciences.org/articles/97894/elife-97894-v3.pdf","https://elifesciences.org/articles/97894.pdf"],"version":"2025-02-28 VOR3 verify"},
 "ALT_P20_NATURE2023":{"publisher":"Nature Communications","doi":"10.1038/s41467-023-38626-y","source_urls":["https://www.nature.com/articles/s41467-023-38626-y.pdf"],"version":"2023-05-23 VOR"}
}
def check(item):
 key,x=item
 row={"id":key,**x,"attempts":[],"actual_full_publisher_pdf_acquired":False,
      "primary_source_frozen":False,"replacement_accepted":False,"not_a_scientific_eligibility_decision":True}
 for url in x["source_urls"]:
  out={"url":url}
  try:
   req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (RelayTheory G1 original source audit)"})
   with urllib.request.urlopen(req,timeout=70) as resp:
    raw=resp.read()
    out["final_url"]=resp.geturl()
    out["content_type"]=resp.headers.get("Content-Type")
   if not raw.startswith(b"%PDF-"): raise ValueError("not raw PDF")
   rd=PdfReader(io.BytesIO(raw),strict=False)
   cnt=len(rd.pages)
   first=(rd.pages[0].extract_text() or "")+" "+(rd.pages[1].extract_text() if cnt>1 else "")
   out.update(raw_sha256=hashlib.sha256(raw).hexdigest(),byte_count=len(raw),
      pages=cnt,title_doi_first_two_pages_sample=first[:550],pdf_signature_ok=True)
   row["actual_full_publisher_pdf_acquired"]=True
   row["publisher_pdf_result"]=out
   row["attempts"].append(out)
   del raw
   break
  except Exception as e:
   out["error"]=repr(e)
   row["attempts"].append(out)
 return row
if __name__=="__main__":
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: 
  rows=list(pool.map(check,LEADS.items()))
 out={"schema":"p399.g1.non-plos.publisher-pdf-original-preA-audit.v1",
      "recorded_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "alternatives_only_no_replace":True,"originals_uploaded":False,"rows":rows}
 Path("g1-alt-receipts").mkdir(exist_ok=True)
 Path("g1-alt-receipts/alternatives.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
 for x in rows:
  print(x["id"],"acquired",x["actual_full_publisher_pdf_acquired"],
        "sha",x.get("publisher_pdf_result",{}).get("raw_sha256"),"pages",
        x.get("publisher_pdf_result",{}).get("pages"),"attempts",len(x["attempts"]))
