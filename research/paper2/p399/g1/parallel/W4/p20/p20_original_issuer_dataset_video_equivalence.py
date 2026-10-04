#!/usr/bin/env python3
"""P20 targeted same-article original dataset and demonstration video source identity (not human replay)."""
import hashlib,json,io,zipfile
from pathlib import Path
from urllib.request import urlopen,Request
d=Path("g1-w4-p20-data-video");d.mkdir(exist_ok=True)
known={"s001":("zip",2326772,"06caca17f908fa58dff9ae2fe19bbf07e16092e333b38342287d2429f9b89103"),"s010":("mp4",3002196,"2fb702c0f629f8f9e2288adbdf96a17a1db6b68b97cea21006f2298673b5c7f0")}
res=[];bad=[]
for key,(ext,n,sha) in known.items():
 id="10.1371/journal.pcbi.1006676."+key
 link="https://journals.plos.org/ploscompbiol/article/file?id="+id+"&type=supplementary"
 item={"publisher_id":id,"link":link,"archive_original_sha256":sha}
 try:
  raw=urlopen(Request(link,headers={"User-Agent":"RelayTheory-G1-W4-original-companion-probe"}),timeout=70).read()
  item.update(raw_sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),exact_archived_original_match=(len(raw)==n and hashlib.sha256(raw).hexdigest()==sha))
  if ext=="zip":
   z=zipfile.ZipFile(io.BytesIO(raw))
   item["dataset_archive_members"]=len(z.namelist())
   item["original_file_types"]={i.filename.split(".")[-1] for i in z.infolist()}
   item["original_file_types"]=list(item["original_file_types"])
  else:
   item["mp4_signature"]="ftyp" in str(raw[:16])
  if not item["exact_archived_original_match"]:raise ValueError("publisher vs archived original raw identity mismatch")
  (d/(key+"."+ext)).write_bytes(raw)
 except Exception as e:item["failure"]=repr(e);bad.append(key)
 res.append(item);print(json.dumps(item,ensure_ascii=False),flush=True)
(d/"source_receipts.json").write_text(json.dumps({"sources":res,"failed":bad},indent=2,ensure_ascii=False,sort_keys=True)+"\n")
if bad:raise SystemExit("P20 original separate source incomplete "+str(bad))
