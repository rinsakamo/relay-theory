#!/usr/bin/env python3
"""Pre-A P14 original issuer ONLY critical-model visual images.
Physical SHA list from two issuer provenance-only Actions. Real rendered
PDF equation pixels / chart bars are human-reviewed separately from logs.
Rasterizing alone never auto-certifies scientific semantic content.
"""
import fitz,hashlib,urllib.request,base64,io
from PIL import Image
srcs=[
 ("MAIN","https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1008969&type=printable","cca218ddff9764422316f99fe2cf8cf6a5519462a0b38ac25b45999080b79ec0",[4,5,7,8,11,17,18,19,20,21,22,23,24,25]),
 ("S2","https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1008969.s002&type=supplementary","80ff7cca0501b3989fd8ba0867b4dea411f1243b5ca094cc2cecd1c34dd0575b",[1]),
 ("S3","https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1008969.s003&type=supplementary","82f2a03519e5718428303158c27caf21b39937b9841a7581a40eb15901eb2be2",[1,2]),
 ("S4","https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1008969.s004&type=supplementary","044423d324d62b4231f056e704e41582c6bb1e1ab950d196c636322c10046f43",[1]),
 ("S5","https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1008969.s005&type=supplementary","3aee815baf0f50dcaf4e53f8a3563469ed3d2a89e73038b5e6429ac1aaca51c2",[1,2])
]
for name,url,sha,pages in srcs:
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (RelayTheory exact published original P14 math/negative pixel review)"}),timeout=130) as f:raw=f.read()
 assert hashlib.sha256(raw).hexdigest()==sha,name+" ORIGINAL FILE CHANGED"
 pdf=fitz.open(stream=raw,filetype="pdf")
 print("P14_VISUAL_SOURCE_RAW_SHA_SUCCESS",name,sha,len(pdf),flush=True)
 for page in pages:
  pix=pdf[page-1].get_pixmap(matrix=fitz.Matrix(1.0,1.0),colorspace=fitz.csRGB,alpha=False)
  im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
  out=io.BytesIO();im.save(out,"JPEG",quality=62,optimize=True)
  enc=base64.b64encode(out.getvalue()).decode()
  print("P14_CRITICAL_ORIGINAL_VISUAL_BEGIN",name,page,"bytes",len(out.getvalue()),flush=True)
  for i in range(0,len(enc),2400):print("P14_CRITICAL_ORIGINAL_VISUAL_CHUNK",name,page,i//2400,enc[i:i+2400],flush=True)
  print("P14_CRITICAL_ORIGINAL_VISUAL_END",name,page,flush=True)
