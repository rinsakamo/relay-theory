#!/usr/bin/env python3
"""Second-family publisher-first media rescue: Nature first-party & Elsevier first-party only.

Pre-A technical provenance only. No third-party author manuscript, PMC reprint,
preprint or abstract promoted to published original. No scientific reconstruction.
"""
import concurrent.futures,hashlib,io,json,os,re,urllib.error,urllib.request
from pathlib import Path
from pypdf import PdfReader
target={
"LRN-01":("10.1038/s41467-025-58848-6","Humans learn generalizable representations through efficient coding",[
"https://www.nature.com/articles/s41467-025-58848-6.pdf?download=1",
"https://static-content.springer.com/pdf/10.1038/s41467-025-58848-6.pdf",
"https://link.springer.com/article/10.1038/s41467-025-58848-6",
"https://www.nature.com/articles/s41467-025-58848-6?error=cookies_not_supported"]),
"ATT-03":("10.1016/j.neuron.2009.01.002","The Normalization Model of Attention",[
"https://ars.els-cdn.com/content/image/1-s2.0-S0896627309000038-main.pdf",
"https://www.cell.com/action/showPdf?pii=S0896-6273%2809%2900003-8",
"https://linkinghub.elsevier.com/retrieve/pii/S0896627309000038"]),
"BLF-01":("10.1016/j.isci.2025.112844","Belief updating in decision-variable space",[
"https://ars.els-cdn.com/content/image/1-s2.0-S2589004225011058-main.pdf",
"https://www.cell.com/action/showPdf?pii=S2589-0042%2825%2901105-8",
"https://linkinghub.elsevier.com/retrieve/pii/S2589004225011058"]),
"INT-01":("10.1016/j.cognition.2024.105967","An algorithmic account for how humans efficiently learn",[
"https://ars.els-cdn.com/content/image/1-s2.0-S0010027724002531-main.pdf",
"https://ars.els-cdn.com/content/image/1-s2.0-S0010027724002531-main.pdf?download=true",
"https://linkinghub.elsevier.com/retrieve/pii/S0010027724002531",
"https://www.sciencedirect.com/science/article/pii/S0010027724002531/pdfft"])
}
h={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/127.0.0.0 Safari/537.36","Accept":"application/pdf,text/html;q=0.9,*/*;q=0.8"}
def one(k):
 doi,title,urls=target[k];out={"slot":k,"doi":doi,"attempts":[],"raw_original_success":None,"full_official_html_success":None}
 for url in urls:
  d=dict(requested_url=url,kind="UNKNOWN",raw_original_hash=None,identity_ok=False,reason=None)
  try:
   request=urllib.request.Request(url,headers=h)
   with urllib.request.urlopen(request,timeout=18) as f:
    ct=f.headers.get("Content-Type","");effective=f.geturl();raw=f.read(18*1024*1024)
   d["effective_url"]=effective;d["http_content_type"]=ct;d["raw_bytes"]=len(raw)
   if not any(x in effective for x in ("nature.com","springer.com","els-cdn.com","cell.com","sciencedirect.com","elsevier.com")):
    raise ValueError("effective host not first-party")
   if raw.startswith(b"%PDF-"):
    reader=PdfReader(io.BytesIO(raw),strict=False);t=" ".join((p.extract_text() or "") for p in reader.pages[:2]).lower()
    major=len([x for x in re.findall("[a-z]{5,}",title.lower())[:10] if x in t])
    if doi.lower() not in t and major<3:raise ValueError("PDF title/DOI fingerprint mismatch")
    d.update(kind="FIRST_PARTY_PDF",identity_ok=True,pages=len(reader.pages),title_word_hits=major,
        raw_original_hash=hashlib.sha256(raw).hexdigest())
    if out["raw_original_success"] is None:out["raw_original_success"]={k:v for k,v in d.items() if k not in ("reason",)}
   else:
    s=raw.decode("utf-8","replace").lower()
    if doi.lower() not in s or "references" not in s or "methods" not in s or "<html" not in s:
     raise ValueError("HTML not DOI-identical complete publisher original")
    d.update(kind="FIRST_PARTY_FULL_HTML_CANDIDATE",identity_ok=True,raw_original_hash=hashlib.sha256(raw).hexdigest())
    if out["full_official_html_success"] is None:out["full_official_html_success"]={k:v for k,v in d.items() if k not in ("reason",)}
  except Exception as e:d["reason"]=str(e)[:145]
  out["attempts"].append(d)
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:r=list(ex.map(one,target))
p={"schema":"p399.g2.first_party_rescue_of_remaining_four.v1","original_media_redistributed":False,"model_scientific_review_complete":False,"g2_final_admission":False,"runner_sha":os.getenv("GITHUB_SHA"),"rows":r}
raw=(json.dumps(p,sort_keys=True,separators=(",",":"))+"\n").encode();Path("g2-second-rescue").mkdir(exist_ok=True)
Path("g2-second-rescue/metadata.json").write_bytes(raw)
print("G2_SECOND_RESCUE_RECEIPT_SHA256",hashlib.sha256(raw).hexdigest())
for x in r:
 print("G2_SECOND_RESCUE",x["slot"],"PDF",x["raw_original_success"],"HTML",x["full_official_html_success"])
 for a in x["attempts"]:
  if a["reason"]:print("G2_SECOND_FAIL",x["slot"],a["requested_url"],a["reason"])
print("G2_SECOND_RESCUE_COUNTS",sum(bool(x["raw_original_success"]) for x in r),sum(bool(x["full_official_html_success"]) for x in r))
