#!/usr/bin/env python3
"""Source-native diagnostic excerpts for already-acquired official PLOS supplementary
files. B4 S1 and INT06 S7/S8 only. No source redistribution, no silent
manuscript substitution, no automatic model science admission.
"""
import datetime,hashlib,json,os,re,shutil,subprocess,urllib.request,urllib.parse
from io import BytesIO
from pypdf import PdfReader
FILES=[
 ("INT06_S7_NOTES","10.1371/journal.pcbi.1000765.s007","doc","ceec10ca95ae7bd2207d95c1ddb45098f2dc9741697c3608497dc2efd9b33bb5"),
 ("INT06_S8_ANOVA","10.1371/journal.pcbi.1000765.s008","doc","0813b44b5770f03b833a0623da876a76dde6e2ee5cd8dcbaf5ec8257fa04b504"),
 ("B4_S1_RECOVERY","10.1371/journal.pcbi.1012872.s001","pdf","64f1e1f18bb51909e89b22112929125914ccff75c2ffd1c91ace4851ae091e88")]
BASE="https://journals.plos.org/ploscompbiol/article/file?id="
KEYS=("figure a","figure b","figure c","figure d","figure e","figure f","figure g",
      "model recovery","parameter recovery","exclusion","anxiety","capacity","sensitivity",
      "anova","statistically","significant","inhibition","mapping","router","control","experimental",
      "simulation","neuronal","slope","selection")
out={"schema":"relaytheory.p399.g2d.v4.publisher_supplement_bounded_native_readout.v1",
     "source_only":True,"supplements_scientifically_fully_qualified":False,
     "supplement_images_visually_inspected_in_this_runner":False,
     "runner_head":os.environ.get("GITHUB_SHA"),"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"items":[]}
def text_windows(text):
 ls=[re.sub(r"\\s+"," ",line).strip() for line in text.splitlines()]
 ls=[x for x in ls if x]
 hits=[(i,l) for i,l in enumerate(ls) if len(l)>20 and any(k in l.lower() for k in KEYS)]
 return [{"line_number_in_extractor":i+1,"excerpt":v[:280]} for i,v in hits[:65]]
for slot,doi,kind,sha in FILES:
 url=BASE+doi+"&type=supplementary"
 row={"slot":slot,"doi":doi,"expected_sha256":sha,"published_original_resolved":False}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (G2-D bounded source native academic provenance)","Accept":"*/*"})
  with urllib.request.urlopen(req,timeout=12) as resp:
   data=resp.read(9*1024*1024+1)
   final=resp.geturl();row.update(response_status=resp.status,final_url_no_query=final.split("?")[0],bytes=len(data))
  orig=urllib.parse.urlparse(url);dst=urllib.parse.urlparse(final)
  if orig.hostname!="journals.plos.org":raise ValueError("not publisher-origin request")
  publisher_delegate=dst.hostname=="storage.googleapis.com" and dst.path.startswith("/plos-corpus-prod/"+doi.rsplit(".",1)[0] if False else "/plos-corpus-prod/10.1371/")
  if dst.hostname not in ("journals.plos.org","content.plos.org") and not publisher_delegate:raise ValueError("non-publisher non-delegated redirect")
  row.update(actual_sha256=hashlib.sha256(data).hexdigest(),publisher_gateway=True,publisher_delegated_storage=bool(publisher_delegate))
  if len(data)>9*1024*1024 or row["actual_sha256"]!=sha:raise ValueError("publisher original raw SHA changed or size cap")
  if kind=="pdf":
   if not data.startswith(b"%PDF-"):raise ValueError("not source PDF")
   p=PdfReader(BytesIO(data),strict=False)
   row.update(source_page_count=len(p.pages),page_readouts=[])
   for i,page in enumerate(p.pages):
    text=page.extract_text() or ""
    w=text_windows(text)
    row["page_readouts"].append({"page":i+1,"native_text_sha256":hashlib.sha256(text.encode()).hexdigest(),
                                "native_text_chars":len(text),"bounded_key_windows":w[:15]})
    print("SOURCE_NATIVE_B4_SUPP_PAGE",i+1,json.dumps({"text_chars":len(text),"key_windows":w[:11]},ensure_ascii=False),flush=True)
  else:
   if not data.startswith(bytes.fromhex("d0cf11e0a1b11ae1")):raise ValueError("not authentic original DOC")
   binary=shutil.which("antiword")
   row["antiword_available"]=bool(binary)
   if not binary:raise RuntimeError("no antiword; DOC content UNREAD while raw SHA is verified")
   p=subprocess.run([binary,"-w","120","-"],input=data,capture_output=True,timeout=12)
   if p.returncode:raise RuntimeError("antiword exit "+str(p.returncode)+":"+p.stderr.decode(errors="replace")[:90])
   decoded=p.stdout.decode("utf-8",errors="replace")
   row.update(doc_extracted_native_utf8_sha256=hashlib.sha256(decoded.encode()).hexdigest(),
              extracted_native_text_chars=len(decoded),bounded_key_windows=text_windows(decoded))
   print("SOURCE_NATIVE_DOC",slot,json.dumps({"text_chars":len(decoded),"key_windows":row["bounded_key_windows"][:60]},ensure_ascii=False),flush=True)
  row["published_original_resolved"]=True
 except Exception as e:
  row["source_or_extraction_failure"]=type(e).__name__+":"+str(e)[:190]
 out["items"].append(row)
 print("SOURCE_RESULT",slot,json.dumps({k:v for k,v in row.items() if k not in ("page_readouts","bounded_key_windows")},ensure_ascii=False),flush=True)
os.makedirs("g2d-v4-supplement-readout",exist_ok=True)
with open("g2d-v4-supplement-readout/metadata.json","w",encoding="utf-8") as f:json.dump(out,f,ensure_ascii=False,indent=2)
print("V4_SUPPLEMENT_INDEPENDENT_NATIVE_READOUT",sum(x["published_original_resolved"] for x in out["items"]),"OF",len(FILES),"SCIENTIFIC_FULL_ADMITTED",0)
