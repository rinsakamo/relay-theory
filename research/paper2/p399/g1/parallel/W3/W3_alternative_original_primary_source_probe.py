#!/usr/bin/env python3
"""W3 acquisition-only alternative original/supplement probe. No science stage or qualification.
All source payloads are independently downloaded at runtime; SHA/page equality is explicit.
Alternate archive provenance is never silently treated as publisher-original equality.
"""
import hashlib, io, json, os, pathlib, urllib.request, urllib.error, time
from pypdf import PdfReader
D="https://journals.plos.org/ploscompbiol/article/file?id="
ALT="https://pmc.ncbi.nlm.nih.gov/articles/"
UCL="https://discovery.ucl.ac.uk/id/eprint/10119020/1/Dolan_journal.pcbi.1008552.pdf"
out=pathlib.Path(os.environ.get("RUNNER_TEMP","/tmp"))/"W3_alternative_original_source_probe_v1.json"
sources=[
 ("P16_MAIN", "pdf", "93428304dccfa6828e0f355d8b4c5875fb441fb939098519e78fbedf6405bdc5", 10, [
     ("PLOS_ORIGINAL", D+"10.1371/journal.pcbi.1003648&type=printable"),
     ("PMC_ARCHIVED_COPY", ALT+"PMC4046921/pdf/pcbi.1003648.pdf"),
     ("PMC_LEGACY_ARCHIVED_COPY", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4046921/pdf/pcbi.1003648.pdf")
 ]),
 ("P18_MAIN", "pdf", "cb75481590c34686eeeb8635dcb8a381283bcbe3e7f8ed9f0ee246fa95e419d1", 28, [
     ("UCL_AUTHOR_INSTITUTIONAL_PUBLICATION",UCL),
     ("PMC_ARCHIVED_COPY",ALT+"PMC7817042/pdf/pcbi.1008552.pdf"),
     ("PLOS_ORIGINAL",D+"10.1371/journal.pcbi.1008552&type=printable")
 ]),
]
for label,ext in [
 ("P15_S1_APPENDIX","s001.pdf"),("P15_S1_TABLE","s003.pdf"),("P15_S2_TABLE","s004.pdf")
]:
 suffix=ext.split(".")[0]
 doi="10.1371/journal.pcbi.1010589."+suffix
 sources.append((label,"pdf",None,None,[
  ("PMC_ARCHIVED_PUBLISHER_SUPPLEMENT",ALT+"PMC9586412/bin/pcbi.1010589."+ext),
  ("PMC_LEGACY_PUBLISHER_SUPPLEMENT","https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9586412/bin/pcbi.1010589."+ext),
  ("PLOS_PUBLISHER_SUPPLEMENT",D+doi+"&type=supplementary")
 ]))
for label,ext in [
 ("P18_S5_RECOVERY","s005.tif"),("P18_S6_VALIDATION","s006.tif"),("P18_S1_PARAMETER_TABLE","s007.pdf")
]:
 suffix=ext.split(".")[0]
 doi="10.1371/journal.pcbi.1008552."+suffix
 sources.append((label,"pdf" if ext.endswith("pdf") else "tif",None,None,[
   ("PMC_ARCHIVED_PUBLISHER_SUPPLEMENT",ALT+"PMC7817042/bin/pcbi.1008552."+ext),
   ("PMC_LEGACY_PUBLISHER_SUPPLEMENT","https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7817042/bin/pcbi.1008552."+ext),
   ("PLOS_PUBLISHER_SUPPLEMENT",D+doi+"&type=supplementary")
 ]))
def fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":"RelayTheory-W3/1.0 independent scholarly-original verification; public open-access","Accept":"application/pdf,image/tiff,application/octet-stream,*/*"})
 with urllib.request.urlopen(req,timeout=18) as r:
  raw=r.read(15_000_001)
  return raw, r.url, r.headers.get("content-type","")
receipts=[]
for key,ext,expected,pages,locations in sources:
 rec={"id":key,"type":ext,"prior_original_sha256_if_known":expected,
      "prior_original_pages_if_known":pages,"source_variants":[],"scope":"SOURCE_ONLY_NOT_SCIENCE_QUALIFICATION"}
 for provenance,url in locations:
  source={"repository_type":provenance,"url":url}
  try:
   raw,final,ctype=fetch(url)
   source.update(final_url=final,content_type=ctype,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
   if len(raw)>15_000_000: raise ValueError("oversize")
   if ext=="pdf":
    if raw[:5]!=b"%PDF-":raise ValueError("not_pdf_magic")
    source["pages"]=len(PdfReader(io.BytesIO(raw),strict=False).pages)
   if ext=="tif":
    if raw[:4] not in [b"II*\\x00",b"MM\\x00*"]:raise ValueError("not_tiff_magic")
   source["validated_file_type"]=True
   source["exact_prior_original_sha_match"]=None if not expected else source["sha256"]==expected
   source["exact_prior_page_count_match"]=None if not pages else source.get("pages")==pages
   source["publisher_provenance_verified"]=provenance.startswith("PLOS")
   print("SUCCESS",key,provenance,source["sha256"],source.get("pages"),"EXACT",source["exact_prior_original_sha_match"],flush=True)
  except Exception as e:
   source.update(validated_file_type=False,error=type(e).__name__+":"+str(e)[:240])
   print("BLOCK",key,provenance,source["error"],flush=True)
  rec["source_variants"].append(source)
 receipts.append(rec)
 out.write_text(json.dumps({"schema":"W3.alternate_original_primary_source_probe.v1",
   "do_not_mutate_original_science_stages":True,"not_a_qualification_decision":True,
   "probes":receipts},indent=2,sort_keys=True)+"\n")
print("RECEIPT",out,flush=True)
