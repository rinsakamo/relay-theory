#!/usr/bin/env python3
"""Exact publisher-owned alternative URL probes for the eight G2 unavailable originals.

No scientific paper analysis, no manuscript substitutions, no copyrighted file retention.
A PDF's identity must match target original DOI/title in publisher-authored contents. Source
reachability NEVER constitutes full source/edition/figure/variant admission.
"""
import concurrent.futures, datetime, hashlib, io, json, os, re, urllib.request, urllib.error
from pathlib import Path
from pypdf import PdfReader

BASE=Path("research/paper2/p399/g2")
orig=json.loads((BASE/"MAIN40_G2_SOURCE_ADMISSION_WORKING_v1.json").read_text())
by_id={x["slot_id"]:x for x in orig["entries"]}
PROBES={
 "ATT-03":[
 ("Elsevier Cell Neuron publisher PDF","https://www.cell.com/neuron/pdf/S0896-6273(09)00003-8.pdf","PDF"),
 ("Elsevier official Neuron fulltext","https://www.cell.com/neuron/fulltext/S0896-6273(09)00003-8","HTML"),
 ("Elsevier official ScienceDirect fulltext","https://www.sciencedirect.com/science/article/pii/S0896627309000038","HTML")],
 "BLF-01":[
 ("Elsevier Cell iScience publisher PDF","https://www.cell.com/iscience/pdf/S2589-0042(25)01105-8.pdf","PDF"),
 ("Elsevier Cell iScience publisher fulltext","https://www.cell.com/iscience/fulltext/S2589-0042(25)01105-8","HTML"),
 ("Elsevier publisher ScienceDirect fulltext","https://www.sciencedirect.com/science/article/pii/S2589004225011058","HTML")],
 "CNC-01":[
 ("Springer Nature original alternative PDF","https://link.springer.com/content/pdf/10.1038/s41562-023-01719-1.pdf","PDF"),
 ("Nature article PDF direct","https://www.nature.com/articles/s41562-023-01719-1.pdf","PDF"),
 ("Nature publisher complete original","https://www.nature.com/articles/s41562-023-01719-1","HTML")],
 "LRN-01":[
 ("Springer Nature alternative published PDF","https://link.springer.com/content/pdf/10.1038/s41467-025-58848-6.pdf","PDF"),
 ("Nature Communications PDF direct","https://www.nature.com/articles/s41467-025-58848-6.pdf","PDF"),
 ("Nature publisher complete original","https://www.nature.com/articles/s41467-025-58848-6","HTML")],
 "PRD-01":[
 ("Springer Nature corrected original PDF","https://link.springer.com/content/pdf/10.1038/s41562-024-01930-8.pdf","PDF"),
 ("Nature corrected-original PDF direct","https://www.nature.com/articles/s41562-024-01930-8.pdf","PDF"),
 ("Nature corrected-original publisher HTML","https://www.nature.com/articles/s41562-024-01930-8","HTML"),
 ("Nature official correction article","https://www.nature.com/articles/s41562-024-01978-6","HTML")],
 "INT-01":[
 ("Elsevier ScienceDirect publisher PDF","https://www.sciencedirect.com/science/article/pii/S0010027724002531/pdfft?isDTMRedir=true&download=true","PDF"),
 ("Elsevier ScienceDirect publisher full-length HTML","https://www.sciencedirect.com/science/article/pii/S0010027724002531","HTML")],
 "INT-02":[
 ("MDPI publisher first-party media PDF","https://mdpi-res.com/d_attachment/entropy/entropy-26-00484/article_deploy/entropy-26-00484.pdf","PDF"),
 ("MDPI publisher full text HTML","https://www.mdpi.com/1099-4300/26/6/484/htm","HTML"),
 ("MDPI publisher first-party raw XML","https://www.mdpi.com/1099-4300/26/6/484/xml","XML")],
 "INT-04":[
 ("Springer Nature publisher alternative PDF","https://link.springer.com/content/pdf/10.1038/s41562-023-01799-z.pdf","PDF"),
 ("Nature original publisher direct PDF","https://www.nature.com/articles/s41562-023-01799-z.pdf","PDF"),
 ("Nature publisher complete original HTML","https://www.nature.com/articles/s41562-023-01799-z","HTML")]
}
assert set(PROBES)=={x["slot"] for x in json.loads((BASE/"MAIN40_G2_ELEVEN_PDF_FAILURE_HTML_FALLBACK_REVIEW_v1.json").read_text())["rows"] if not x["html_verified"]}
H={"User-Agent":"RelayTheory-G2-original-provenance-research/1.1 (publisher-primary audit; no original redistribution)","Accept":"application/pdf,text/html,application/xhtml+xml,application/xml,*/*"}
def fetch(url):
 req=urllib.request.Request(url,headers=H)
 with urllib.request.urlopen(req,timeout=20) as f:
  return f.read(50*1024*1024),f.geturl(),f.headers.get("Content-Type","")
def probe(k):
 e=by_id[k];doi=e["stable_identity"]["value"];title=e["title_identity"]
 out=dict(slot=k,doi=doi,attempts=[],publisher_original_byte_acquisition_candidate=None,
      publisher_complete_html_candidate=None,source_eligible=False,edition_frozen=False,
      model_critical_visual_and_variants_verified=False)
 for origin,url,mode in PROBES[k]:
  attempt=dict(origin=origin,requested_url=url,mode=mode,downloaded=False,publisher_identity_verified=False,actual_url=None,sha256=None,raw_bytes=None,original_pdf_pages=None,errors=[])
  try:
   raw,final,ctype=fetch(url)
   attempt["actual_url"]=final;attempt["content_type"]=ctype
   if mode=="PDF":
    if not raw.startswith(b"%PDF-"):raise ValueError("non_pdf_response")
    reader=PdfReader(io.BytesIO(raw),strict=False)
    if len(reader.pages)<2:raise ValueError("implausible_page_count")
    text=" ".join((reader.pages[i].extract_text() or "") for i in range(min(2,len(reader.pages)))).lower()
    # Need positive publisher-original identity, not just a PDF signature.
    from_title=sum(1 for word in re.findall(r"[a-z]{5,}",title.lower())[:12] if word in text)
    attempt["identity_evidence"]=dict(doi_found=doi.lower() in text,title_keyword_matches=from_title)
    attempt["publisher_identity_verified"]=doi.lower() in text or from_title>=3
    if not attempt["publisher_identity_verified"]:raise ValueError("PDF_identity_not_verified")
    attempt["original_pdf_pages"]=len(reader.pages)
   else:
    s=raw.decode("utf-8","replace")
    t=re.sub(r"<[^>]+>"," ",s).lower()
    attempt["identity_evidence"]=dict(doi_found=doi.lower() in s.lower(),full_article_marker=bool(re.search(r"(full length article|research article|article|introduction|methods)",t)))
    attempt["publisher_identity_verified"]=attempt["identity_evidence"]["doi_found"] and attempt["identity_evidence"]["full_article_marker"]
    if not attempt["publisher_identity_verified"]:raise ValueError("not_verified_complete_publisher_original_page")
   attempt["downloaded"]=True
   attempt["sha256"]=hashlib.sha256(raw).hexdigest()
   attempt["raw_bytes"]=len(raw)
   if mode=="PDF" and out["publisher_original_byte_acquisition_candidate"] is None:
    out["publisher_original_byte_acquisition_candidate"]={p:attempt[p] for p in ("requested_url","actual_url","sha256","raw_bytes","original_pdf_pages","identity_evidence")}
   if mode=="HTML" and out["publisher_complete_html_candidate"] is None:
    out["publisher_complete_html_candidate"]={p:attempt[p] for p in ("requested_url","actual_url","sha256","raw_bytes","identity_evidence")}
  except Exception as err:attempt["errors"].append(type(err).__name__+": "+str(err)[:110])
  out["attempts"].append(attempt)
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:rows=list(pool.map(probe,PROBES))
payload=dict(schema="p399.g2.only-publisher-primary-eight-retry.v1",time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),runner_commit=os.getenv("GITHUB_SHA"),context="Technical acquisition only; no semantic qualification",source_files_committed_or_redistributed=False,rows=rows)
dir=Path("g2-primary-retry");dir.mkdir(exist_ok=True)
raw=(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
(dir/"eight-source-retry-metadata.json").write_bytes(raw)
print("G2_RETRY_RECEIPT_SHA256",hashlib.sha256(raw).hexdigest())
for row in rows:
 print("G2_RETRY",row["slot"],"PDF",row["publisher_original_byte_acquisition_candidate"],"HTML",row["publisher_complete_html_candidate"])
 for a in row["attempts"]:
  if a["errors"]:print("G2_RETRY_FAIL",row["slot"],a["origin"],a["errors"][0])
print("G2_RETRY_COUNTS",sum(bool(r["publisher_original_byte_acquisition_candidate"]) for r in rows),sum(bool(r["publisher_complete_html_candidate"]) for r in rows), "scientifically_source_admitted",0)
