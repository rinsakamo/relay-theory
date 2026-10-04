#!/usr/bin/env python3
"""Fail-closed P19 separately issued remaining original sources; v1 original A/B remain retired."""
import hashlib, io, json
from pathlib import Path
from urllib.request import Request,urlopen
from pypdf import PdfReader
from PIL import Image
out=Path("g1-w4-p19-additional")
out.mkdir(exist_ok=True)
rows=[]; errors=[]
for i,kind in [(3,"TIFF"),(4,"TIFF"),(5,"TIFF"),(6,"TIFF"),(7,"PDF"),(8,"PDF")]:
    name=f"P19_S{i-2}_Fig" if i<=6 else f"P19_S{i-6}_Table"
    id=f"10.1371/journal.pcbi.1009866.s{i:03}"
    url=f"https://journals.plos.org/ploscompbiol/article/file?id={id}&type=supplementary"
    rec={"name":name,"issuer_id":id,"request_url":url}
    try:
        res=urlopen(Request(url,headers={"User-Agent":"RelayTheory-W4-original-source-qualifier/1"}),timeout=65)
        raw=res.read(); sha=hashlib.sha256(raw).hexdigest()
        rec.update(sha256=sha,bytes=len(raw),content_type=res.headers.get("Content-Type"),source_status="FETCHED")
        if kind=="PDF":
            if not raw.startswith(b"%PDF-"): raise ValueError("no PDF signature")
            reader=PdfReader(io.BytesIO(raw))
            rec["pages"]=len(reader.pages)
            rec["page_text_excerpts"]=[{"page":j+1,"first_250_text":" ".join((page.extract_text() or "").split())[:250]} for j,page in enumerate(reader.pages)]
            (out/(name+".pdf")).write_bytes(raw)
        else:
            img=Image.open(io.BytesIO(raw))
            if img.format not in ("TIFF","TIF"): raise ValueError("not actual TIFF "+str(img.format))
            rec["tiff_size"]=list(img.size);rec["mode"]=img.mode
            (out/(name+".tif")).write_bytes(raw)
    except Exception as ex:
        rec.update(source_status="FAIL",error=repr(ex));errors.append(name+": "+repr(ex))
    rows.append(rec)
    print(json.dumps(rec,ensure_ascii=False),flush=True)
(out/"publisher_remaining_original_receipts.json").write_text(json.dumps({"rows":rows,"errors":errors,"scope":"preA source only; no semantic qualification"},indent=2,ensure_ascii=False,sort_keys=True)+"\n")
if errors:raise SystemExit("One or more defining issuer originals missing: "+repr(errors))
