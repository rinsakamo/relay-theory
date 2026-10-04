#!/usr/bin/env python3
"""G2 publisher-original bytes and publisher HTML metadata: NOT scientific source admission."""
import concurrent.futures, datetime, hashlib, html, io, json, os, re, urllib.request, urllib.parse
from pathlib import Path
from pypdf import PdfReader

HEAD={"User-Agent":"Mozilla/5.0 (RelayTheory independent scholarly source provenance/eligibility verification)"}
BASE=Path("research/paper2/p399/g2")
MANIFEST=json.loads((BASE/"MAIN40_G2_SOURCE_ADMISSION_WORKING_v1.json").read_text())
def get(url, timeout=35):
    r=urllib.request.Request(url,headers=HEAD)
    with urllib.request.urlopen(r,timeout=timeout) as f:return f.read(), f.geturl(),f.headers.get("Content-Type","")
def pdf_urls(e,html_data):
    doi=e["stable_identity"]["value"]
    p=e["publisher"]
    u=e["official_candidate_url"]
    out=[]
    if p=="PLOS":out=["https://journals.plos.org/ploscompbiol/article/file?id="+doi+"&type=printable"]
    elif p=="Springer":out=["https://link.springer.com/content/pdf/"+doi+".pdf"]
    elif p=="Nature":out=["https://www.nature.com/articles/"+doi.split("/")[-1]+".pdf"]
    elif p=="eLife":
        n=doi.split(".")[-1]
        out=["https://elifesciences.org/articles/"+n+".pdf"]+["https://cdn.elifesciences.org/articles/"+n+"/elife-"+n+"-v"+v+".pdf" for v in ("3","2","1")]
    elif p=="PNAS":out=["https://www.pnas.org/doi/pdf/"+doi]
    elif p=="MDPI":out=["https://www.mdpi.com/1099-4300/26/6/484/pdf"]
    elif p=="Elsevier":
        out=["https://www.cell.com/iscience/pdf/S2542-4650(25)00844-7.pdf"] if doi.startswith("10.1016/j.isci") else []
    if html_data:
        for m in re.findall(r'<meta[^>]*name=["\\\']citation_pdf_url["\\\'][^>]*>',html_data,re.I):
            found=re.search(r'content=["\\\']([^"\\\']+)',m)
            if found:out.insert(0,html.unescape(found.group(1)))
    return list(dict.fromkeys(out))
def process(e):
    pid=e["slot_id"]; doi=e["stable_identity"]["value"]; url=e["official_candidate_url"]
    res=dict(id=pid,doi=doi,requested_html_url=url,publisher=e["publisher"],
             source_qualification=False, edition_qualification=False, lineage_qualification=False,
             html_open=False, html_final_url=None,html_response_bytes=None,html_sha256=None,
             html_headings=[],html_math_tags=None,html_figure_tags=None,html_publication_meta=[],
             html_correction_link_hints=[],pdf_bytes_acquired=False,pdf_sha256=None,pdf_bytes=None,
             pdf_pages=None,pdf_final_url=None,pdf_text_nonempty_pages=None,errors=[])
    content=""
    try:
        raw,final,ctype=get(url)
        content=raw.decode("utf-8","replace")
        # An HTTP 200 on doi resolver or abstract is not complete publisher original
        res["html_open"]=len(content)>1500 and (doi.split("/")[-1].lower() in content.lower() or pid=="INT-03")
        res["html_final_url"]=final;res["html_response_bytes"]=len(raw)
        res["html_sha256"]=hashlib.sha256(raw).hexdigest() if res["html_open"] else None
        res["html_headings"]=[re.sub(r"<[^>]+>"," ",x)[:95].strip() for x in re.findall(r"<h[1-4][^>]*>.*?</h[1-4]>",content,re.S|re.I)][:55]
        res["html_math_tags"]=len(re.findall(r'<(?:math|span[^>]+class=["\\\'][^"\\\']*(?:equation|math))',content,re.I))
        res["html_figure_tags"]=len(re.findall(r"<figure\\b",content,re.I))
        res["html_publication_meta"]=[re.sub(r"<[^>]+>"," ",x)[:160] for x in re.findall(r'<meta[^>]*(?:citation_date|citation_title|citation_doi|citation_pdf_url)[^>]*>',content,re.I)][:9]
        res["html_correction_link_hints"]=list(dict.fromkeys(re.findall(r'href=["\\\']([^"\\\']+(?:correction|Correction)[^"\\\']*)',content,re.I)))[:7]
    except Exception as exc:res["errors"].append("HTML "+repr(exc)[:250])
    for pu in pdf_urls(e,content):
        try:
            raw,final,ctype=get(pu)
            if not raw.startswith(b"%PDF-"):raise ValueError("Non-PDF response "+ctype)
            pdf=PdfReader(io.BytesIO(raw),strict=False); pages=len(pdf.pages)
            if pages<2:raise ValueError("Implausible page count")
            probes=sorted(set([0,pages//2,pages-1]))
            res.update(pdf_bytes_acquired=True,pdf_sha256=hashlib.sha256(raw).hexdigest(),pdf_bytes=len(raw),
                pdf_pages=pages,pdf_final_url=final,pdf_text_nonempty_pages=[int(bool((pdf.pages[i].extract_text() or "").strip())) for i in probes])
            break
        except Exception as exc:res["errors"].append("PDF "+pu+" : "+repr(exc)[:180])
    # Publisher correction determination and exact math-figure equivalence require manual review.
    return res
if __name__=="__main__":
    rows=MANIFEST["entries"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results=list(pool.map(process,rows))
    packet=dict(schema="p399.g2.github_actions_actual_source_acquisition.working.v1",
       timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
       git_sha=os.environ.get("GITHUB_SHA"),scope="PHYSICAL_PROVENANCE_ONLY_NO_SCIENTIFIC_ADMISSION",
       publisher_original_copyrighted_bytes_uploaded=False,rows=results)
    out=Path("g2-receipts");out.mkdir(exist_ok=True)
    raw=(json.dumps(packet,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\\n").encode("utf-8")
    (out/"publisher-original-provenance.json").write_bytes(raw)
    print("SOURCE_RECEIPT_CANONICAL_SHA256 "+hashlib.sha256(raw).hexdigest())
    for r in results:
        print("G2_RAW",r["id"],"PDF",str(r["pdf_bytes"] or "FAILED"),"PAGES",r["pdf_pages"] or "-","PDF_SHA256",r["pdf_sha256"] or "-",
        "HTML",int(r["html_open"]),"HTML_SHA256",r["html_sha256"] or "-","ERROR_COUNT",len(r["errors"]))
    print("COUNTS physical-original-pdf",sum(x["pdf_bytes_acquired"] for x in results),
          "publisher-html-pages-accessed",sum(x["html_open"] for x in results),
          "independently-scientifically-source-admitted",0)
