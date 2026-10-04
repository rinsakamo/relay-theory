#!/usr/bin/env python3
"""PLOS-in-archived-original supplementary identity investigation; archival copy never silently 'publisher-byte verified'."""
import hashlib, io, json, re, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
from urllib.request import Request,urlopen
from pypdf import PdfReader
from PIL import Image
from docx import Document
out=Path("g1-w4-public-archive-investigation");out.mkdir(exist_ok=True)
known={"pcbi.1009866.s001.pdf":"c45ab7072bfcbbe91e8e77c83091293cd43d3dc133c94dfb74be89f7de729ab4","pcbi.1009866.s002.pdf":"a82c34c729e533566c516ad95f08c9403be86dc837874aec85b00e338c958596"}
records=[]
for pmc,doi in [("PMC9744313","10.1371/journal.pcbi.1009866"),("PMC6420027","10.1371/journal.pcbi.1006676")]:
    rec={"pmc":pmc,"expected_original_doi":doi,"sources":[],"files":[]}
    try:
        xmlurl=f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/fullTextXML"
        response=urlopen(Request(xmlurl,headers={"User-Agent":"RelayTheory-original-provenance/1"}),timeout=90)
        raw=response.read();root=ET.fromstring(raw)
        actual={el.text for el in root.findall(".//article-id") if el.attrib.get("pub-id-type")=="doi"}
        if doi not in actual:raise ValueError("NLM-archived same article DOI mismatch "+repr(actual))
        rec["jats_xml_sha256"]=hashlib.sha256(raw).hexdigest()
        rec["same_article_doi_verified_in_public_archive"]=True
        rec["jats_supplement_href"]=[(a.attrib,a.findtext("label")) for a in root.findall(".//supplementary-material")]
        rec["sources"].append({"url":xmlurl,"status":"MATCHED_JATS_DOI"})
    except Exception as e:
        rec["sources"].append({"source":"JATS","error":repr(e)})
    try:
        url=f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/supplementaryFiles"
        resp=urlopen(Request(url,headers={"User-Agent":"RelayTheory-original-provenance/1"}),timeout=100)
        blob=resp.read();rec["archive_sha256"]=hashlib.sha256(blob).hexdigest();rec["archive_bytes"]=len(blob)
        if not zipfile.is_zipfile(io.BytesIO(blob)):raise ValueError("Europe PMC response not ZIP")
        archive=zipfile.ZipFile(io.BytesIO(blob))
        names=archive.namelist()
        rec["sources"].append({"url":url,"status":"ZIP_FETCHED","entries":len(names)})
        for name in names:
            if name.endswith("/"):continue
            raw=archive.read(name);low=Path(name).name.lower()
            ext=Path(low).suffix
            item={"archive_member":name,"bytes":len(raw),"raw_sha256":hashlib.sha256(raw).hexdigest(),"ext":ext}
            match=re.search(r"pcbi\.?(1009866|1006676)\.s(\d{3})",low)
            if not match:
                match=re.search(r"(1009866|1006676)\.s(\d{3})",low)
            item["looks_like_same_DOI_supplement"]=bool(match)
            exact=known.get(low)
            if exact:item["independently_existing_publisher_same_bytes"]=item["raw_sha256"]==exact
            if ext==".pdf":
                if raw.startswith(b"%PDF-"):
                    doc=PdfReader(io.BytesIO(raw))
                    item["pages"]=len(doc.pages)
                    item["text_start"]=" ".join((doc.pages[0].extract_text() or "").split())[:240]
            if ext in (".tif",".tiff"):
                im=Image.open(io.BytesIO(raw));item["img_type"]=im.format;item["size"]=list(im.size)
            if ext==".docx":
                doc=Document(io.BytesIO(raw));item["tables"]=len(doc.tables)
            if ext in (".pdf",".tif",".tiff",".docx") and (match or ("supp" in low and len(raw)<16000000)):
                nameout=pmc+"-"+Path(name).name
                (out/nameout).write_bytes(raw)
            rec["files"].append(item)
        (out/(pmc+"-archive.zip")).write_bytes(blob)
    except Exception as e:
        rec["sources"].append({"source":"EuropePMC_supplementaryFiles","error":repr(e)})
    records.append(rec)
    print(json.dumps({"pmc":pmc,"doi_ok":rec.get("same_article_doi_verified_in_public_archive",False),"sources":rec["sources"],"member_count":len(rec["files"]),"matching_publisher_bytes":[p for p in rec["files"] if "independently_existing_publisher_same_bytes" in p]},ensure_ascii=False),flush=True)
(out/"europepmc_archive_issuer_equivalence_investigation.json").write_text(json.dumps({"scope":"ARCHIVE_FALLBACK_INVESTIGATION_ONLY_NOT_ISSUER_SHA_CERTIFICATION","records":records},sort_keys=True,ensure_ascii=False,indent=2)+"\n")
if not all(x.get("same_article_doi_verified_in_public_archive") and x.get("archive_bytes") for x in records):
    raise SystemExit("ARCHIVE_FALLBACK_UNQUALIFIED")
