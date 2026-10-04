#!/usr/bin/env python3
"""P14 bounded additional issuer original: negative control S1 and stimuli S6.
S1 tests regional novel codes, S6 supplies original exact 14 sequences for
task generation; source original main and S2-5 independently already acquired.
"""
import urllib.request,hashlib,io,json,pathlib,re
from pypdf import PdfReader
out={}
for name,i in [("S1",1),("S6",6)]:
 url=f"https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1008969.s{i:03d}&type=supplementary"
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (RelayTheory P14 original negative and stimulus supplement qualification)"}),timeout=90) as f:b=f.read()
 assert b.startswith(b"%PDF")
 src=PdfReader(io.BytesIO(b))
 per=[]
 for k,p in enumerate(src.pages):
  t=re.sub(r"\s+"," ",p.extract_text() or "")
  per.append({"page":k+1,"characters":len(t),"text_head":t[:170]})
 out[name]={"url":url,"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b),"pages":len(src.pages),"page_map":per}
 print("P14_ORIGINAL_ISSUER_SUPPLEMENT",name,out[name]["sha256"],len(b),len(src.pages),flush=True)
 print("P14_ISSUER_TEXT_HEAD",name,per[:2],flush=True)
pathlib.Path("g1-p14-s1s6").mkdir(exist_ok=True)
pathlib.Path("g1-p14-s1s6/real-source.json").write_text(json.dumps(out,indent=2)+"\n")
