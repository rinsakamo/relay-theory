#!/usr/bin/env python3
"""W1 P08 sole official original S1 .docx text and embedded media inventory.
Raw original .docx is NOT rewritten or committed. Text extraction != pixel review.
"""
import hashlib,json,pathlib,urllib.request,zipfile,re
from io import BytesIO
from xml.etree import ElementTree as ET
OUT=pathlib.Path("w1-p08-s1-original");OUT.mkdir(exist_ok=True)
url="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1005418.s001&type=supplementary"
raw=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"RelayTheory-W1-S1-original/1.0"}),timeout=80).read()
assert hashlib.sha256(raw).hexdigest()=="59162cf3338a8677d58328d382ede402bf0fd0ff5dfa7e9b2f6bfd58c44b7372"
N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(BytesIO(raw)) as z:
    doc=ET.fromstring(z.read('word/document.xml'))
    paragraphs=[]
    for p in doc.findall('.//w:p',N):
        val=''.join(x.text or '' for x in p.findall('.//w:t',N))
        if val.strip():paragraphs.append(val)
    extras=[{'name':n,'size':z.getinfo(n).file_size} for n in z.namelist() if n.startswith('word/media/')]
text='\n'.join(paragraphs)
receipt={'name':'P08 original publisher S1 Text', 'url':url,'raw_sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'paragraph_count':len(paragraphs),'extracted_chars':len(text),'embedded_images_not_pixel_certified':extras,'complete_supplement_semantic_visual_certified':False}
(OUT/'supplement_original_metadata.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
(OUT/'source_extracted_paragraphs.txt').write_text(text+'\n')
print(json.dumps(receipt))
