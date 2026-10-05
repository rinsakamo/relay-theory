#!/usr/bin/env python3
"""G2 bibliographic direct-citation screening; missing citations never imply independence."""
import concurrent.futures, datetime,hashlib,html,json,os,re,urllib.request
from pathlib import Path
P=Path("research/paper2/p399/g2")
main=json.loads((P/"MAIN40_G2_SOURCE_ADMISSION_WORKING_v1.json").read_text())["entries"]
pilot=json.loads((P/"MAIN40_G2_COLLISION_LEDGER_v1.json").read_text())["all_current_or_proposed_g1_pilots"]
allworks=[dict(id=e["slot_id"],doi=e["stable_identity"]["value"]) for e in main]+[dict(id="G1_"+p["id"],doi=p["doi"]) for p in pilot]
def fetch(e):
    url=e["official_candidate_url"]; pid=e["slot_id"]
    out=dict(id=pid,doi=e["stable_identity"]["value"],url=url,publisher=e["publisher"],html_received=False,html_sha256=None,cited_doi_edges=[],error=None)
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (RelayTheory source bibliography DOI citation-only audit)"})
        with urllib.request.urlopen(req,timeout=28) as r:raw=r.read()
        rawtext=html.unescape(raw.decode("utf8","replace")).lower()
        out["html_received"]=len(raw)>1500 and (out["doi"].split("/")[-1].lower() in rawtext)
        if not out["html_received"]:return out
        out["html_sha256"]=hashlib.sha256(raw).hexdigest()
        # This checks DOI appearances in publisher ORIGINAL full HTML only; remove self.
        for x in allworks:
            if x["doi"].lower()==out["doi"].lower():continue
            needle=x["doi"].lower()
            if needle in rawtext:
                at=rawtext.find(needle);out["cited_doi_edges"].append(dict(target=x["id"],target_doi=x["doi"],doi_literal_present=True,
                    context=rawtext[max(0,at-90):at+len(needle)+80].replace("\\n"," ")[:220]))
    except Exception as exc:out["error"]=repr(exc)[:170]
    return out
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:r=list(pool.map(fetch,main))
packet=dict(schema="g2.p399.source_publisher_html_direct_doi_literature_edges.v1",timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),git_sha=os.environ.get("GITHUB_SHA"),interpretation="DOI literal in obtained HTML only: could be citation, inline DOI, or unrelated; NOT central model-family equivalence, zero links NOT independence",rows=r)
raw=(json.dumps(packet,sort_keys=True,separators=(",",":"),ensure_ascii=False)+chr(10)).encode("utf8")
d=Path("g2-lineage");d.mkdir(exist_ok=True)
(d/"doi_literal_reference_probe.json").write_bytes(raw)
print("G2_LINEAGE_RECEIPT_SHA256",hashlib.sha256(raw).hexdigest())
for x in r:
    for e in x["cited_doi_edges"]:print("G2_CITATION",x["id"],e["target"],e["target_doi"])
print("G2_COUNTS_OPENED",sum(x["html_received"] for x in r),"DIRECT_LITERAL_EDGES",sum(len(x["cited_doi_edges"]) for x in r))
