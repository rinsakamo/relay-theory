#!/usr/bin/env python3
"""Bounded P18 original PLOS supplementary figure image integrity. Not semantic model recovery."""
import urllib.request,hashlib,json,io,pathlib,os
from PIL import Image,ImageStat
g=[("P18_S5_model_comparison","s005","1e42c90baa502f7d0d3be32100ccb6a62fe04b29fbd9bd5274fe22f529e860e8"),
("P18_S6_model_validation","s006","67048c23a5bc77ffe7b8690042e1d680599ab62ad2517cbfcc245d71071f7cf1")]
out=[]
for key,suffix,expected in g:
 u="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1008552."+suffix+"&type=supplementary"
 with urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"RelayTheory-W3-source-viz-publisher-original"}),timeout=45) as r: raw=r.read()
 sha=hashlib.sha256(raw).hexdigest()
 assert sha==expected
 img=Image.open(io.BytesIO(raw));img.load()
 assert img.format=="TIFF" and img.width>300 and img.height>300
 st=ImageStat.Stat(img.convert("RGB"))
 assert any(q>5 for q in st.stddev),"Nontrivial figure content expected"
 rec={"key":key,"url":u,"exact_raw_sha256":sha,"bytes":len(raw),"type":"TIFF","pixel_dimensions":img.size,
 "rgb_channel_sd":st.stddev,"visual_integrity":"original publisher TIFF decoded, nonblank color/grey metrics; image semantic content not automatically adjudicated"}
 out.append(rec);print("VERIFIED_ORIGINAL_TIFF",json.dumps(rec),flush=True)
p=pathlib.Path(os.environ.get("RUNNER_TEMP","/tmp"))/"W3_P18_original_S5_S6_image_pixel_receipt.json"
p.write_text(json.dumps({"scope":"ORIGINAL_VISUAL_INTEGRITY_ONLY_NOT_MODEL_FIDELITY","items":out},indent=2)+"\n")
