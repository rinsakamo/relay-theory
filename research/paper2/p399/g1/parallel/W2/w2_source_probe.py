#!/usr/bin/env python3
"""W2 issuer-original physical acquisition. No science/semantic-qualification claims.
Keep copyrighted PDF/DOCX/TIFF raw sources in ephemeral runner only; upload metadata
and sample-page rendered previews for independent human visual assessment.
Usage: python w2_source_probe.py P11 [--phase preflight|postE].
"""
import hashlib, io, json, os, pathlib, re, subprocess, sys, time
from urllib.parse import quote
import requests
import fitz

BASE = "https://journals.plos.org/ploscompbiol/article/file"
SPECS = {
  "P11": dict(doi="10.1371/journal.pcbi.1008971",
     sha="9291d8bca264a2216467e2254dede69dda71232708d94d10619f6d253458d022",
     pages=24, title="Analogous computations in working memory input, output and motor gating",
     critical_pages=[1,3,5,8,10,14,16,19,22],
     supplements={"s001":"TIF","s002":"TIF","s003":"TIF","s004":"TIF","s005":"DOCX"}),
  "P12": dict(doi="10.1371/journal.pcbi.1006043",
     sha="17368c69624bc5e968ccd2f3cc5eeb349070801e3b240cbc50a66d770bae2370",
     pages=27, title="Rational metareasoning and the plasticity of cognitive control",
     critical_pages=[1,3,5,6,7,9,11,14,18,21],
     supplements={"s001":"DOCX","s002":"DOCX","s003":"DOCX"}),
  "P17": dict(doi="10.1371/journal.pcbi.1009738",
     sha="e2d28aea56a31501db49aa791158f18771ae3054748d331df2ec26817f16f305",
     pages=16, title="An initial", critical_pages=[1,3,4,5,6,8,10,12,15],
     supplements={f"s{i:03d}":"PDF" for i in range(1,7)}),
  "ELIFE39497": dict(doi="10.7554/eLife.39497",
     sha="c2adddf8d232d851d9decbb304fb02107686cf55a5dad4cbbfd8b0fd7ac7d64a",
     pages=23, title="Integrated externally and internally generated task predictions",
     critical_pages=[1,3,5,7,9,11,15,19], supplements={})
}
# Historical frozen stage-PRE_A issuer-original supplement SHA receipts. Exact raw bytes, not MIME labels, are mandatory.
EXPECTED_SUP = {
  "P11": {
    "s001": "153c857ccf12eacc05a5eaee0dffb45d8bc156a2205f41ea9e22c16a8a90b34f",
    "s002": "6abb4dee4a92c1f94a28ef993c802e03dde53af15ef6216198df7c5c566b8643",
    "s003": "d5b928e563b43919f4d91f4c53deab4987112570c7079906fbcb36fcdaed0cca",
    "s004": "43bf600b853a77a07011201ad935464c2aadc390a18a4be1cd5dfd5dddf99fc4",
    "s005": "9c1961a7f032f32805c95d958562912abb814673ffc1657cca56d908e18335b5"
  },
  "P12": {
    "s001": "6870d9344bcbecc77aabe9a32335ed9c9820e4d1aefef03f6f59fe64d23c6fb5",
    "s002": "8ea0198c46a4b78bc6af1bcd4a0fdbb5859a96b76ee0335ba92156ed25931432",
    "s003": "7fac52d9c530d7627d3065413818e75581f2e02a14dddbf84fd797aef715d9a4"
  },
  "P17": {
    "s001": "5ca2de3cbd46d3c00571c2ae79ab2fe3bdd03d0a30353da4231cdff7b8aebc16",
    "s002": "f9bcdf77670fb0e2aa155156955512695379547068f03d33904371433eafe5e4",
    "s003": "8c72ee49d7955b9e388b0a6a8f8a15a0a634d80d53f0d017a1a540eedaf9d5de",
    "s004": "310264d18535e4f1b1cbb2d2d8fdde104227954883b8b71c1f7acbd35f3858b8",
    "s005": "8d51d8313d955221fe00be587901397aaa0b5b5573d1ea328e59f80c43aa917b",
    "s006": "4994dc5c0f5e40e12fac2a42113cb2c3da4a7c5598ac24fa38a84ccdee12f153"
  }
}
def hash_data(data): return hashlib.sha256(data).hexdigest()
def get(session,url):
    last=None
    for attempt in range(3):
        try:
            resp=session.get(url, timeout=65, headers={"Accept":"application/pdf,application/octet-stream,text/html,*/*"})
            resp.raise_for_status()
            return resp
        except Exception as exc:
            last=str(exc)
            time.sleep(2*(attempt+1))
    raise RuntimeError(f"GET failed: {url}: {last}")
def physical_pdf(data, spec, output, label):
    if not data.startswith(b"%PDF"): raise ValueError("not PDF signature")
    doc=fitz.open(stream=data,filetype="pdf")
    source_title=(doc[0].get_text() or "")[:12000]
    matched = all(x.lower() in source_title.lower() for x in [spec["title"][:16]])
    receipt=dict(media=label,sha256=hash_data(data),bytes=len(data),pages=len(doc),
      expected_raw_sha256=spec["sha"],expected_pages=spec["pages"],
      exact_raw_sha_match=hash_data(data)==spec["sha"],
      page_match=len(doc)==spec["pages"],title_first_page_match=matched,
      first_page_text_prefix=source_title[:500])
    if spec["doi"]=="10.1371/journal.pcbi.1009738":
        # Specific, visually selected anchors for the actual publisher original edition.
        critical={0:["An initial","changes of mind"],
                  5:["Fig 3","100,000","drift"],
                  12:["Computational modeling","externalVar","firstFrame"]}
        receipt["actual_original_specific_page_text_anchors"]={}
        for page_idx,words in critical.items():
            pg_text=doc[page_idx].get_text().lower()
            observations={w:w.lower() in pg_text for w in words}
            receipt["actual_original_specific_page_text_anchors"][str(page_idx+1)]=observations
        receipt["critical_page_anchors_all_present"]=all(
            all(v.values()) for v in receipt["actual_original_specific_page_text_anchors"].values())
    p=output/"previews"
    p.mkdir(parents=True,exist_ok=True)
    for one_based in spec["critical_pages"]:
        if one_based<=len(doc):
            page=doc[one_based-1]; pix=page.get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False)
            pix.save(str(p/f"{label}_p{one_based:02d}.png"))
    doc.close()
    return receipt
def do_paper(paper,phase):
    spec=SPECS[paper]
    root=pathlib.Path("w2-source-output")/paper/phase
    root.mkdir(parents=True,exist_ok=True)
    sess=requests.Session()
    sess.headers.update({"User-Agent":"Mozilla/5.0 (compatible; RelayTheory-W2-original-issuer-source-audit/1.0)"})
    doi=spec["doi"]
    url=(f"https://cdn.elifesciences.org/articles/39497/elife-39497-v3.pdf"
        if paper=="ELIFE39497" else BASE+f"?id={doi}&type=printable")
    record={"paper":paper,"phase":phase,"doi":doi,"url":url,"issuer_original":True,
       "scientific_qualification":False,"proof_kind":"raw-physical-source-only",
       "preexisting_sha_from_frozen_receipt":spec["sha"],"source_errors":[],
       "supplementary":{}}
    try:
        resp=get(sess,url)
        record["download_final_url"]=resp.url
        record["primary"]=physical_pdf(resp.content,spec,root,"original")
    except Exception as exc:
        record["source_errors"].append("PRIMARY: "+repr(exc))
    if paper!="ELIFE39497":
        for sid,extension in spec["supplements"].items():
            # PLOS official DOI file endpoint; never silently replace with mirrored reprint.
            supdoi=f"{doi}.{sid}"
            u=BASE+f"?id={supdoi}&type=supplementary"
            try:
                response=get(sess,u)
                b=response.content
                if extension=="PDF": valid=b.startswith(b"%PDF")
                elif extension=="TIF": valid=(b[:4] in (bytes.fromhex("49492a00"),bytes.fromhex("4d4d002a"),bytes.fromhex("49492b00"),bytes.fromhex("4d4d002b")))
                else: valid=b.startswith(b"PK")
                source_specific_supplement_pdf=None
                if paper=="P17" and valid:
                    expected_pages={"s001":2,"s002":3,"s003":2,"s004":1,"s005":1,"s006":1}
                    src=fitz.open(stream=b,filetype="pdf")
                    source_specific_supplement_pdf={"actual_pages":len(src),
                       "expected_pages":expected_pages[sid],
                       "pages_match":len(src)==expected_pages[sid],
                       "first_page_has_extracted_original_text":len(src[0].get_text())>100}
                    src.close()
                    if not source_specific_supplement_pdf["pages_match"] or not source_specific_supplement_pdf["first_page_has_extracted_original_text"]:
                        record["source_errors"].append(sid+" exact P17 original supplement page/text source anchor mismatch")
                record["supplementary"][sid]={"source_specific_supplement_pdf":source_specific_supplement_pdf,"url":u,"final_url":response.url,
                   "bytes":len(b),"sha256":hash_data(b),"format_expected":extension,
                   "signature_match":valid}
                if not valid:record["source_errors"].append(sid+" publisher-format-signature mismatch")
                if hash_data(b)!=EXPECTED_SUP[paper][sid]:record["source_errors"].append(sid+" historical frozen issuer raw SHA mismatch")
            except Exception as exc:record["source_errors"].append(sid+": "+repr(exc))
    else:
        record["additional_critical_supplement_status"]="NOT_YET_EXHAUSTIVELY_CLASSIFIED"
        record["source_errors"].append("eLife v3 issuer supplementary and amendment/negative-source full audit pending")
    if "primary" in record:
        p=record["primary"]
        if paper=="P17" and not p.get("critical_page_anchors_all_present",False):
            record["source_errors"].append("P17 publisher original visually-selected page-specific textual anchors mismatch")
        if not all([p["exact_raw_sha_match"],p["page_match"],p["title_first_page_match"]]):
            record["source_errors"].append("official raw primary SHA/pages/title mismatch")
    else:record["source_errors"].append("no physical verified original primary")
    record["source_physical_pass"]=not record["source_errors"]
    (root/"source_receipt.json").write_text(json.dumps(record,sort_keys=True,indent=2)+"\\n")
    print(json.dumps(record,sort_keys=True), flush=True)
    if record["source_errors"]:sys.exit(1)
if __name__=="__main__":
    paper = sys.argv[1]
    phase = sys.argv[2] if len(sys.argv)>2 else "preflight"
    assert phase in ("preflight","postE")
    do_paper(paper,phase)
