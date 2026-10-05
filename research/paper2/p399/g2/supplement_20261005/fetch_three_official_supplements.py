#!/usr/bin/env python3
"""Fetch source-linked three original supplements in a networked GitHub runner.

No PDF binaries, extracted copyrighted full text, or user private inputs are
committed. Exact complete source SHA/pages and bounded original-text anchors
are recorded in Actions logs and generated private runner artifact.
Source acquisition is not a scientific proof or an independent visual read.
"""
import hashlib,json,os,re,subprocess,sys,urllib.request,urllib.error,xml.etree.ElementTree as ET
from pathlib import Path
SPECS={
"ATT03":{"pmc":"PMC2752446","name":"NIHMS107478-supplement.pdf","min":18000,"max":400000,
  "extra":["https://www.cell.com/neuron/supplemental/S0896-6273(09)00003-8",
   "https://www.cns.nyu.edu/heegerlab/content/publications/Reynolds-Neuron2009-Supplement.pdf"]},
"BLF01":{"pmc":"PMC12221758","name":"mmc1.pdf","min":35000,"max":1200000,
 "extra":["https://www.cell.com/cms/10.1016/j.isci.2025.112844/attachment/","https://www.cell.com/cms/10.1016/j.isci.2025.112844/mmc1.pdf"]},
"PRD01":{"pmc":"PMC11878374","name":"NIHMS2053848-supplement-Supplementary.pdf","min":100000,"max":4000000,
 "extra":["https://static-content.springer.com/esm/art%3A10.1038%2Fs41562-024-01930-8/MediaObjects/41562_2024_1930_MOESM1_ESM.pdf",
          "https://static-content.springer.com/esm/art%3A10.1038%2Fs41562-024-01930-8/MediaObjects/41562_2024_1930_MOESM1_ESM.docx"]}}
BASE=Path("/tmp/p399_supplement_sci_20261005")
BASE.mkdir(exist_ok=True)
HEAD={"User-Agent":"Mozilla/5.0 (compatible; ResearchSupplementVerifier/1.0; scholarly research)","Accept":"application/pdf,*/*"}
def retrieve(url):
    req=urllib.request.Request(url,headers=HEAD)
    with urllib.request.urlopen(req,timeout=12) as r:
        body=r.read(6000000)
        return body,r.headers.get("content-type",""),r.url
def candidate_urls(spec):
    name=spec["name"]; pmc=spec["pmc"]; n=pmc[3:]
    hosts=[
      f"https://pmc.ncbi.nlm.nih.gov/articles/instance/{n}/bin/{name}",
      f"https://pmc.ncbi.nlm.nih.gov/articles/{pmc}/bin/{name}",
      f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc}/bin/{name}",
      f"https://europepmc.org/articles/{pmc}/bin/{name}",
      f"https://europepmc.org/articles/{pmc}/bin/{name}?page=1",
      f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/supplementaryFiles",
    ]
    return [*hosts,*spec["extra"]]
def ispdf(b):
    return b.startswith(b"%PDF-") and b"%%EOF" in b[-20000:]
def inspect_pdf(k,b,s,origin,attempts):
    p=BASE/f"{k}_original_supplement.pdf";p.write_bytes(b)
    meta=subprocess.run(["pdfinfo",str(p)],capture_output=True,text=True,timeout=10,check=True).stdout
    pages=int(re.search(r"^Pages:\s+(\d+)",meta,re.M).group(1))
    txt=(BASE/f"{k}_original_supplement.txt")
    subprocess.run(["pdftotext","-layout",str(p),str(txt)],capture_output=True,text=True,timeout=15,check=True)
    t=txt.read_text(errors="replace")
    if len(t.strip()) < 150: raise ValueError("PDF text too short: could be image-only, do not falsely admit")
    sections=re.split(r"\f",t)
    info={"selected_source":k,"source_pmc":s["pmc"],"source_file":s["name"],"download_url":origin,"source_sha256":hashlib.sha256(b).hexdigest(),"raw_bytes":len(b),"pdf_pages":pages,"text_chars":len(t),"extracted_text_sha256":hashlib.sha256(t.encode()).hexdigest(),"complete_original_pdf_in_runner":True,"all_pdf_pages_rasterized":False,"human_pixel_vision_certified":False,"semantic_sci_certified":False,"source_attempts":attempts}
    hits={}
    filters={"ATT03":r"contrast|response|preferred|nonpreferred|attention|suppres|deriv|limit|gain|Fig|Table",
       "BLF01":r"ITI|hysteresis|Figure|Exp|delay|accuracy|trial|supplement",
       "PRD01":r"Supplemental|Supplementary|Text S1|Figure S|Fig. S|Table S|backward|forward|predecessor|convergen|divergen|base.rate|PR|SR"}[k]
    for i,pg in enumerate(sections):
        l=[re.sub(r"\s+"," ",line).strip() for line in pg.splitlines()]
        matches=[line[:360] for line in l if re.search(filters,line,re.I) and len(line)>6][:27]
        hits[str(i+1)]={"page_first_line":next((ln for ln in l if ln),"")[:180],"matched_original_text_excerpt":matches}
    info["pagewise_anchors"]=hits
    # Export the full original extracted text only in ephemeral runner workspace;
    # bounded excerpts in CI logs for non-infringing independent verification.
    (BASE/f"{k}_receipt.json").write_text(json.dumps(info,ensure_ascii=False,indent=2))
    print("==== ACQUIRED",k,json.dumps({key:info[key] for key in ("download_url","source_sha256","raw_bytes","pdf_pages","text_chars","extracted_text_sha256")}),flush=True)
    for page, datum in hits.items():
        print("PAGE",k,page,":",datum["page_first_line"],flush=True)
        for text in datum["matched_original_text_excerpt"][:9]:
            print("  ANCHOR",text[:300],flush=True)
    return info

all_info={}
for k,s in SPECS.items():
    print("=== START",k,s["pmc"],s["name"],flush=True)
    attempts=[]
    found=None
    for url in candidate_urls(s):
        try:
            b,ctype,actual=retrieve(url)
            if ispdf(b) and s["min"]<=len(b)<=s["max"]:
                found=inspect_pdf(k,b,s,actual,attempts)
                break
            reason=f"non-PDF/invalid size:{len(b)} mime:{ctype[:55]} start:{b[:20]!r}"
            attempts.append({"url":url,"result":reason})
            print("TRY",k,url,reason,flush=True)
        except Exception as e:
            err=str(e)[:110]
            attempts.append({"url":url,"result":err})
            print("TRY",k,url,err,flush=True)
    if not found:
        print("=== FAIL_CLOSED_NO_ORIGINAL_RAW_SUPPLEMENT",k,flush=True)
        all_info[k]={"source_pmc":s["pmc"],"requested_original_supplement":s["name"],"complete_original_pdf_in_runner":False,"source_attempts":attempts,"scientific_qualified":False}
    else: all_info[k]=found
(BASE/"all_three_acquisition_result.json").write_text(json.dumps(all_info,indent=2,ensure_ascii=False))
print("FINAL",json.dumps({k:("SOURCE_RAW_ACQUIRED" if d.get("complete_original_pdf_in_runner") else "SOURCE_RAW_BLOCKED") for k,d in all_info.items()}),flush=True)
# fail closed if any source missing; Actions artifact still uploaded via if always()
if not all(z.get("complete_original_pdf_in_runner") for z in all_info.values()):
    sys.exit(4)
