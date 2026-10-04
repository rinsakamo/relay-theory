#!/usr/bin/env python3
"""Justified publisher official original S1 exact SHA check + actual rendered maths."""
import io,base64,urllib.request,hashlib
import fitz
from PIL import Image
url="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1006681.s001&type=supplementary"
with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (RelayTheory model critical publisher S1 visual maths review)"}),timeout=120) as f:b=f.read()
assert hashlib.sha256(b).hexdigest()=="198eb18de66cca150dd233184781923680831f6e59007fec83ab54b5ec36453c"
src=fitz.open(stream=b,filetype="pdf");assert len(src)==32
print("P13_MANDATORY_S1_ORIGINAL_VISUAL_SOURCE_IDENTITY_PASS",len(src),len(b),flush=True)
for p in [3,4,5,6,7,8,10,11,15]:
 pg=src[p-1]; pix=pg.get_pixmap(matrix=fitz.Matrix(1.0,1.0),colorspace=fitz.csRGB,alpha=False)
 im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples);d=io.BytesIO();im.save(d,"JPEG",quality=67,optimize=True)
 enc=base64.b64encode(d.getvalue()).decode()
 print("P13_S1_VISUAL_BEGIN",p,"jpegbytes",len(d.getvalue()),flush=True)
 for j in range(0,len(enc),2500):print("P13_S1_VISUAL_CHUNK",p,j//2500,enc[j:j+2500],flush=True)
 print("P13_S1_VISUAL_END",p,flush=True)
