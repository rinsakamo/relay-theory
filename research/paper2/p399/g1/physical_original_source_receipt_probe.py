#!/usr/bin/env python3
"""G1 source acquisition receipts only. NOT scientific, semantic, full-math or correction qualification.

Runner network is used because conversation runtime has no outbound DNS. Never commit or
upload publisher PDF bytes. Every access failure remains visible and is not replaced by HTML
without an explicit edition/source-mode adjudication.
"""
import concurrent.futures
import datetime
import hashlib
import io
import json
import os
import re
import urllib.request
from pathlib import Path
from pypdf import PdfReader

DOIS = {
    "P05":"10.1371/journal.pcbi.1010654",
    "P06":"10.1371/journal.pcbi.1004375",
    "P07":"10.1371/journal.pcbi.1000254",
    "P08":"10.1371/journal.pcbi.1005418",
    "P09":"10.1371/journal.pcbi.1006435",
    "P10":"10.1371/journal.pcbi.1010699",
    "P11":"10.1371/journal.pcbi.1008971",
    "P12":"10.1371/journal.pcbi.1006043",
    "P13":"10.1371/journal.pcbi.1006681",
    "P14":"10.1371/journal.pcbi.1008969",
    "P15":"10.1371/journal.pcbi.1010589",
    "P16":"10.1371/journal.pcbi.1003648",
    "P17":"10.1371/journal.pcbi.1009738",
    "P18":"10.1371/journal.pcbi.1008552",
    "P19":"10.1371/journal.pcbi.1009866",
    "P20":"10.1371/journal.pcbi.1006676",
}
CORRECTIONS = {
    "P08":"10.1371/journal.pcbi.1005908",
    "P10":"10.1371/journal.pcbi.1010775",
}
HEADERS={"User-Agent":"Mozilla/5.0 (RelayTheory G1 source provenance audit; research-use)"}
def fetch(url):
    request=urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read(),response.geturl(),response.headers.get("Content-Type","")
def check(row):
    pid,doi=row
    pdfurl="https://journals.plos.org/ploscompbiol/article/file?id="+doi+"&type=printable"
    htmlurl="https://journals.plos.org/ploscompbiol/article?id="+doi
    rec={"id":pid,"doi":doi,"publisher_pdf_url":pdfurl,"publisher_html_url":htmlurl,
         "pdf_bytes_acquired":False,"raw_sha256":None,"raw_bytes":None,
         "page_count":None,"first_mid_last_text_pages":None,
         "html_page_accessed":False,"html_section_heading_hint":None,
         "correction_url":None,"correction_accessed":None,"errors":[],
         "status":"METADATA_PROVENANCE_ONLY_NOT_FORMAL_SOURCE_ADMISSION"}
    try:
        raw,final,ctype=fetch(pdfurl)
        if not raw.startswith(b"%PDF-"):
            raise ValueError("PDF signature absent: response content type="+ctype)
        r=PdfReader(io.BytesIO(raw), strict=False)
        count=len(r.pages)
        if count<2: raise ValueError("implausible PDF page count")
        selected=sorted(set([0,count//2,count-1]))
        texts=[(i+1,bool((r.pages[i].extract_text() or "").strip())) for i in selected]
        rec.update(pdf_bytes_acquired=True,raw_sha256=hashlib.sha256(raw).hexdigest(),
                   raw_bytes=len(raw),page_count=count,
                   first_mid_last_text_pages=texts,publisher_pdf_final_url=final)
        del raw
    except Exception as e:
        rec["errors"].append("PDF: "+repr(e))
    try:
        page,final,ctype=fetch(htmlurl)
        body=page.decode("utf-8","replace")
        rec["html_page_accessed"]="journal.pcbi" in body and ("Article" in body or "article" in body)
        rec["html_response_bytes"]=len(page)
        rec["html_final_url"]=final
        rec["html_section_heading_hint"]=sorted(set(re.findall(r'<h[23][^>]*>(.{2,95}?)</h[23]>',body,flags=re.S|re.I)))[:25]
    except Exception as e:
        rec["errors"].append("HTML: "+repr(e))
    if pid in CORRECTIONS:
        cu="https://journals.plos.org/ploscompbiol/article?id="+CORRECTIONS[pid]
        rec["correction_url"]=cu
        try:
            correction,final,ct=fetch(cu)
            rec["correction_accessed"]=CORRECTIONS[pid].split(".")[-1].encode() in correction
            rec["correction_response_bytes"]=len(correction)
        except Exception as e:
            rec["correction_accessed"]=False
            rec["errors"].append("CORRECTION: "+repr(e))
    return rec
if __name__=="__main__":
    Path("g1-receipts").mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        rows=list(pool.map(check,DOIS.items()))
    packet={"schema":"p399.g1.physical_remote_acquisition_attempt.v1",
      "recorded_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "runner_commit":os.environ.get("GITHUB_SHA"),"automatic_semantic_qualification":False,
      "auto_selected_primary_source":False,
      "publisher_originals_retained_in_git":False,
      "rows":rows}
    path=Path("g1-receipts/source-receipts.json")
    path.write_text(json.dumps(packet,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("G1 machine source acquisition: ATTEMPT ONLY")
    for rec in rows:
        print(rec["id"],"PDF",rec["raw_bytes"] or "FAILED","pages",rec["page_count"] or "-",
              "sha256",rec["raw_sha256"] or "-", "HTML",rec["html_page_accessed"],
              "correction",rec["correction_accessed"],"errors",len(rec["errors"]))
    print("Counts: PDF byte-acquired",sum(bool(x["pdf_bytes_acquired"]) for x in rows),
          "HTML fetched",sum(bool(x["html_page_accessed"]) for x in rows),
          "scientifically admitted",0,"scientifically qualified",0)
