#!/usr/bin/env python3
"""Independent bounded visually inspected original S1 negative and S6 stimuli."""
import fitz,io,urllib.request,hashlib,base64
from PIL import Image
for name,n,expected,pages in [("S1",1,"f2e9bef0fd311132078f8de1e1ef261649c9d540ab93cba541c7d25534322385",[1,2]),("S6",6,"25eddff2e76155d34bd394f97644a6b438154095d72f369830aba239e4cda6d9",[1])]:
 url=f"https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1008969.s{n:03d}&type=supplementary"
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (RelayTheory P14 targeted published negative/scenario source pixel audit)"}),timeout=90) as f:b=f.read()
 assert hashlib.sha256(b).hexdigest()==expected
 d=fitz.open(stream=b,filetype="pdf")
 print("P14_COMPLEMENT_VISUAL_ORIGINAL_IDENTITY_PASS",name,expected,len(d),flush=True)
 for k in pages:
  pix=d[k-1].get_pixmap(matrix=fitz.Matrix(1.1,1.1),colorspace=fitz.csRGB,alpha=False)
  im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
  o=io.BytesIO();im.save(o,"JPEG",quality=67,optimize=True);e=base64.b64encode(o.getvalue()).decode()
  print("P14_COMPLEMENT_VISUAL_BEGIN",name,k,flush=True)
  for j in range(0,len(e),2400):print("P14_COMPLEMENT_VISUAL_CHUNK",name,k,j//2400,e[j:j+2400],flush=True)
  print("P14_COMPLEMENT_VISUAL_END",name,k,flush=True)
