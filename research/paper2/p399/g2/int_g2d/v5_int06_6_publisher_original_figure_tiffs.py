#!/usr/bin/env python3
"""INT06 all six original PLOS publisher figure TIFFs: exact DOI signed-delegate
binding, content hash, Pillow structural check. Scientific pixel interpretation
is a separate gate; never promote first-party media to scientific consensus.
"""
import hashlib,json,os,re,urllib.request
from urllib.parse import urlparse,parse_qs
from datetime import datetime,timezone
from io import BytesIO
from PIL import Image
BASE="10.1371/journal.pcbi.1000765"
items=[]
for i in range(1,7):
 suffix=f"s{i:03d}";doi=BASE+"."+suffix
 url=f"https://journals.plos.org/ploscompbiol/article/file?id={doi}&type=supplementary"
 o={"id":"INT06_FIG_"+suffix.upper(),"publisher_doi":doi,"publisher_article_origin":url,
    "raw_original_verified":False,"full_scientific_pixel_meaning_verified":False}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (G2D original source audit)","Accept":"image/tiff,*/*"})
  with urllib.request.urlopen(req,timeout=12) as res:
   data=res.read(6*1024*1024+1);final=res.geturl()
   o.update(status=res.status,raw_bytes=len(data),media_type=res.headers.get("Content-Type",""))
  parsed=urlparse(final);params=parse_qs(parsed.query)
  o["redacted_final_url"]=parsed.scheme+"://"+parsed.netloc+parsed.path
  expected=r"^/plos-corpus-prod/"+re.escape(BASE)+r"/[1-9][0-9]*/pcbi\.1000765\."+suffix+r"\.tif$"
  delegate=parsed.hostname=="storage.googleapis.com" and bool(re.fullmatch(expected,parsed.path)) and params.get("X-Goog-Algorithm")==["GOOG4-RSA-SHA256"] and params.get("X-Goog-Credential",[""])[0].startswith("wombat-sa@plos-prod.iam.gserviceaccount.com/") and bool(params.get("X-Goog-Signature",[""])[0])
  o["publisher_exact_signed_delegation"]=bool(delegate)
  if not delegate:raise ValueError("unexpected non-PLOS delegated host, bad DOI path or unsigned bucket")
  if len(data)>6*1024*1024:raise ValueError("6MiB original cap exceeded")
  o["raw_sha256"]=hashlib.sha256(data).hexdigest()
  o["tiff_prefix_hex"]=data[:4].hex()
  with Image.open(BytesIO(data)) as im:
   o.update(image_format=im.format,pixel_dimensions=list(im.size),frames=getattr(im,"n_frames",1),mode=im.mode)
   if im.format!="TIFF":raise ValueError("not original TIFF")
   im.verify()
  o["raw_original_verified"]=True
 except Exception as exc:o["error"]=type(exc).__name__+":"+str(exc)[:190]
 items.append(o)
 print("G2D_INT06_V5_PUBLISHER_FIG",json.dumps(o,sort_keys=True),flush=True)
res={"schema":"p399.g2d.int06_firstparty_supplement_s1_s6_original_tiff_physical_v1",
     "time_utc":datetime.now(timezone.utc).isoformat(),"runner_head":os.getenv("GITHUB_SHA"),
     "fig_s1_s6_original_physical_receipts_only":True,"pixel_semantics_audited":False,
     "no_main_or_family_science_authorized":True,"records":items,"verified_total":sum(x["raw_original_verified"] for x in items)}
os.makedirs("g2d-v5-int06-all-six-original-figures",exist_ok=True)
with open("g2d-v5-int06-all-six-original-figures/receipts.json","w") as f:json.dump(res,f,indent=2)
print("G2D_V5_INT06_OFFICIAL_TIF_ORIGINALS",res["verified_total"],"/6; scientific_whole_qualified=0")
