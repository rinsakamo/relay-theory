#!/usr/bin/env python3
"""W4 source-only independent cloud acquisition. Does NOT certify scientific fidelity."""
import hashlib
import io
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen
from pypdf import PdfReader

OUT = Path("g1-w4-source")
OUT.mkdir(exist_ok=True)
SOURCE = [
    ("P19_main", "https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1009866&type=printable", "4ee1e89bb1d0bc0961c86185cee7bb851a25033c2f8f71270212fd6b313deee4", 2080943, 28),
    ("P19_S1_algorithm", "https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1009866.s001&type=supplementary", None, None, None),
    ("P19_S2_results", "https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1009866.s002&type=supplementary", None, None, None),
    ("P20_main", "https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1006676&type=printable", "5b6c3347eda5fc1509db0867e2c75fe94e90f1fe85385abf61f8738b2f16f097", 3073632, 27),
]
ANCHORS = {
    "P19_main": {
        5:["Modeling strategy"], 6:["internal sequence model","Dirichlet process"],
        8:["distance-dependent","hierarchical"], 9:["Parameter fitting"],
        10:["seating arrangement"], 11:["Fitted parameter"],
        16:["interference"], 17:["interference"]
    },
    "P20_main": {
        1:["Goal-related feedback"], 2:["Goal Babbling"],
    }
}
results = []
errors = []
for name,url,expect_sha,expect_bytes,expect_pages in SOURCE:
    rec = {"id":name,"requested":url}
    try:
        response=urlopen(Request(url,headers={"User-Agent":"RelayTheory-G1-W4-academic-source-verifier/1.0"}),timeout=70)
        data=response.read()
        sha=hashlib.sha256(data).hexdigest()
        if not data.startswith(b"%PDF-"): raise ValueError("not PDF signature")
        pdf=PdfReader(io.BytesIO(data))
        page_count=len(pdf.pages)
        rec.update(raw_sha256=sha,bytes=len(data),pages=page_count,final_url=response.url,status="FETCHED")
        if expect_sha and sha!=expect_sha: raise ValueError("RAW_SHA_MISMATCH "+sha)
        if expect_bytes and len(data)!=expect_bytes: raise ValueError("BYTE_SIZE_MISMATCH")
        if expect_pages and page_count!=expect_pages: raise ValueError("PAGE_COUNT_MISMATCH")
        anchors=[]
        for page,terms in ANCHORS.get(name,{}).items():
            t=pdf.pages[page-1].extract_text() or ""
            for term in terms:
                ok=term.lower() in " ".join(t.split()).lower()
                anchors.append({"publisher_page_1_based":page,"term":term,"extraction_found":ok,"not_semantic_visual_review":True})
        rec["text_probes"]=anchors
        if name.endswith("_S1_algorithm") or name.endswith("_S2_results"):
            rec["supplement_page_headers"]=[
              {"p":k+1,"text_start":" ".join((pdf.pages[k].extract_text() or "").split())[:170]}
              for k in range(page_count)
            ]
        rec["expected_raw_receipt_matched"]=bool(expect_sha)
        (OUT/(name+".pdf")).write_bytes(data)
    except Exception as exc:
        rec["status"]="FAIL"; rec["error"]=repr(exc)
        errors.append(name+": "+repr(exc))
    results.append(rec)
    print(json.dumps({k:v for k,v in rec.items() if k!="supplement_page_headers"},ensure_ascii=False,sort_keys=True),flush=True)
(OUT/"raw_source_receipt.json").write_text(json.dumps({"purpose":"PRE_A_ONLY_not_semantic_admission","sources":results,"errors":errors},sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("W4_SOURCE_INTEGRITY_ERRORS", errors,flush=True)
if errors: raise SystemExit(1)
