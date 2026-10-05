#!/usr/bin/env python3
"""Read exact physical original supplementary PDF bytes from approved source URLs.

Emit hash+per-page text anchor inventory and limited critical page images to
separate actual human/model visual inspection. Log B64 images are NOT the
full original material and rendered-but-unviewed files are not human approved.
"""
import base64, hashlib, io, json, re, subprocess, tempfile, textwrap, urllib.request, zipfile
from pathlib import Path
EXPECTED={
"ATT03":("https://ars.els-cdn.com/content/image/1-s2.0-S0896627309000038-mmc1.pdf","4d75c5cf6b2e896e45072edf7ef588101dae6a005d59b74d497fdf6e250acf5e",74000,5),
"BLF01":("https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12221758/supplementaryFiles","dfe031097a03fa013aff88b1e1f5ddcfe41dc4d0bb231cc291b3dc1d92415d53",241964,2),
"PRD01":("https://static-content.springer.com/esm/art%3A10.1038%2Fs41562-024-01930-8/MediaObjects/41562_2024_1930_MOESM1_ESM.pdf","10f5d55f971060fb325e3e5a0bb4be2df015407ecb1428af9ebd17a4bea6298c",1077373,17)}
CRITICAL={"ATT03":[2,3,4],"BLF01":[2],"PRD01":[3,4,5]}
ROOT=Path(tempfile.mkdtemp(prefix="supp_exact_"))
def run(cmd):
    p=subprocess.run(cmd,text=True,capture_output=True,timeout=40)
    if p.returncode:raise RuntimeError(cmd[0]+": "+p.stderr[:1000])
    return p.stdout
receipts={}
for lane,(url,sha,raw_n,pages) in EXPECTED.items():
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=15) as r: b=r.read(4500000)
    if lane=="BLF01":
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            assert "mmc1.pdf" in z.namelist(),z.namelist()
            b=z.read("mmc1.pdf")
    assert b[:5]==b"%PDF-"
    assert len(b)==raw_n,(lane,len(b),raw_n)
    assert hashlib.sha256(b).hexdigest()==sha,(lane,hashlib.sha256(b).hexdigest(),sha)
    pdf=ROOT/(lane+".pdf");pdf.write_bytes(b)
    info=run(["pdfinfo",str(pdf)])
    assert re.search(r"^Pages:\s+"+str(pages)+r"$",info,re.M),lane
    txt=ROOT/(lane+".txt")
    run(["pdftotext","-layout",str(pdf),str(txt)])
    t=txt.read_text(errors="replace")
    ptxt=t.split("\f")
    meta={"url":url,"sha256":sha,"size":raw_n,"pages":pages,"page_text_sha256":[],"page_bitmap_sha256":[],"required_source_anchors_found":[],"critical_page_images_encoded_in_action_logs":CRITICAL[lane],"human_visual_status":"PENDING_INDEPENDENT_IMAGE_OPEN"}
    phrase_patterns={
      "ATT03":[r"Figure 4C",r"Figure 4E",r"Figure 6C",r"equation",r"contrast gain"],
      "BLF01":[r"Figure S1",r"inter-trial interval",r"2 s",r"8 s"],
      "PRD01":[r"forward and backward planning",r"SR",r"PR",r"Table S6",r"Note S3"]
    }[lane]
    for q in phrase_patterns:
        found=bool(re.search(q,t,re.I))
        meta["required_source_anchors_found"].append({"phrase":q,"found":found})
    assert all(x["found"] for x in meta["required_source_anchors_found"]),meta["required_source_anchors_found"]
    for n in range(1,pages+1):
        page=(ptxt[n-1] if n<=len(ptxt) else "")
        ph=hashlib.sha256(page.encode()).hexdigest()
        meta["page_text_sha256"].append({"page":n,"sha256":ph,"chars":len(page)})
        pre=ROOT/f"{lane}_p{n}"
        run(["pdftoppm","-f",str(n),"-l",str(n),"-singlefile","-scale-to","900","-jpeg","-jpegopt","quality=50",str(pdf),str(pre)])
        img=(pre.with_suffix(".jpg")).read_bytes()
        ih=hashlib.sha256(img).hexdigest()
        meta["page_bitmap_sha256"].append({"page":n,"sha256":ih,"bytes":len(img)})
        if n in CRITICAL[lane]:
            print("=== TEXT_PAGE_EXTRACT",lane,n,"chars",len(page),flush=True)
            # Page-specific key source phrases only, not unlicensed full supplementary republication.
            lines=[" ".join(s.split()) for s in page.splitlines()]
            terms={"ATT03":r"Derivation|Figure|equation|contrast|gain|S[0-9]|suppression|σ|γ",
                   "BLF01":r"ITI|Figure|granularity|short|long|regression|hysteresis|duration",
                   "PRD01":r"SR|PR|forward|backward|successor|predecessor|equation|Figure|ratio|trident|planet"}[lane]
            for line in lines:
                if re.search(terms,line,re.I) and len(line)>6:
                    print("SCI_ANCHOR",lane,n,line[:165],flush=True)
            print("BEGIN_PAGE_B64",lane,n,ih,len(img),flush=True)
            for row in textwrap.wrap(base64.b64encode(img).decode(),96):print(row,flush=True)
            print("END_PAGE_B64",lane,n,flush=True)
    receipts[lane]=meta
    print("REVIEW_SOURCE",lane,"SHA",sha,"BYTES",len(b),"PAGES",pages,"ALL_RASTERS_SHA_LOCKED",len(meta["page_bitmap_sha256"]),flush=True)
out=ROOT/"supplement_pixel_and_math_receipt.json"
out.write_text(json.dumps(receipts,indent=2,ensure_ascii=False))
print("REVIEW_JSON",out.read_text()[:14000],flush=True)
print("ALL_EXACT_SUPPLEMENTS_AND_PAGE_RASTERS_SUCCESS",flush=True)
