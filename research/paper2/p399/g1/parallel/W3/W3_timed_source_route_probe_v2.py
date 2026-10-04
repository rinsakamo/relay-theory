#!/usr/bin/env python3
"""Timed issuer, PMC, Europe PMC transport probes. Neither PRE_A nor post-E scientific qualification."""
import concurrent.futures,hashlib,io,json,pathlib,time,urllib.request,zipfile
from urllib.parse import urlencode
def plos(doi):
    return "https://journals.plos.org/ploscompbiol/article/file?"+urlencode({"id":doi,"type":"supplementary" if ".s00" in doi else "printable"})
data={"P15":("10.1371/journal.pcbi.1010589","PMC9586412","591339de97a02abc1faeb276b48b8dfc73b518aca2d8ad1c36a10ba96038e002",1546007),
"P16":("10.1371/journal.pcbi.1003648","PMC4046921","93428304dccfa6828e0f355d8b4c5875fb441fb939098519e78fbedf6405bdc5",1121696),
"P18":("10.1371/journal.pcbi.1008552","PMC7817042","cb75481590c34686eeeb8635dcb8a381283bcbe3e7f8ed9f0ee246fa95e419d1",1872932)}
jobs=[]
for paper,(doi,pmc,sha,sz) in data.items():
    suffix=doi.rsplit(".",1)[-1]
    jobs.extend([(paper+"_official_main",plos(doi)),(paper+"_PMC_main",f"https://pmc.ncbi.nlm.nih.gov/articles/{pmc}/pdf/pcbi.{suffix}.pdf"),
    (paper+"_EuropePMC_supplements",f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/supplementaryFiles")])
for paper,supps in [("P15",["s001","s003","s004"]),("P18",["s005","s006","s007"])]:
    doi,pmc,_,_=data[paper]
    suffix=doi.rsplit(".",1)[-1]
    ext={"s005":"tif","s006":"tif","s007":"pdf","s001":"pdf","s003":"pdf","s004":"pdf"}
    for item in supps:
        jobs.extend([(paper+"_"+item+"_official",plos(doi+"."+item)),
           (paper+"_"+item+"_PMC",f"https://pmc.ncbi.nlm.nih.gov/articles/{pmc}/bin/pcbi.{suffix}.{item}.{ext[item]}")])
jobs += [("P16_GCS_unsigned","https://storage.googleapis.com/plos-corpus-prod/10.1371/journal.pcbi.1003648/1/pcbi.1003648.pdf")]
def probe(row):
    name,url=row
    rec={"name":name,"url":url,"trials":[],"transport_success":False}
    for idx in range(1,3):
        start=time.monotonic()
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (W3 bounded-original-source-qualification-probe)","Accept":"application/pdf,application/zip,image/tiff,*/*"})
            with urllib.request.urlopen(req,timeout=18) as response:
                raw=response.read(75*1024*1024+1)
                final=response.geturl().split("?")[0]
                mime=response.headers.get("Content-Type","")
            if len(raw)>75*1024*1024: raise ValueError("response exceeds maximum 75MB")
            entry={"trial":idx,"seconds":round(time.monotonic()-start,2),"mime":mime,"final_url_without_tokens":final,
                   "bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"magic_hex":raw[:6].hex()}
            paper=name[:3]
            if name.endswith("_official_main"):
                entry["exact_previously_acquired_issuer_main_sha_and_bytes"]=entry["sha256"]==data[paper][2] and len(raw)==data[paper][3]
            if raw[:4]==b"PK\x03\x04":
                with zipfile.ZipFile(io.BytesIO(raw)) as zipfile_obj:
                    entry["relevant_files"]=[{"path":m.filename,"size":m.file_size,"sha256":hashlib.sha256(zipfile_obj.read(m)).hexdigest()}
                    for m in zipfile_obj.infolist() if m.filename.lower().endswith((".pdf",".tif",".tiff",".eps")) and m.file_size<20*1024*1024][:60]
            rec["trials"].append(entry);rec["transport_success"]=True;break
        except Exception as err:
            rec["trials"].append({"trial":idx,"seconds":round(time.monotonic()-start,2),"error":str(err)[:250]})
    print(json.dumps(rec,sort_keys=True),flush=True)
    return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=11) as executor:
    result=list(executor.map(probe,jobs))
rec={"scope":"W3_BOUNDED_TRANSPORT_DISCOVERY_ONLY_NOT_PREA_OR_POSTE","attempts_per_route_max":2,
"timeout_per_attempt_seconds":18,"results":result,"new_science_qualifications":0,
"issuer_main_exact_recovery":[x["name"] for x in result if any(y.get("exact_previously_acquired_issuer_main_sha_and_bytes") for y in x["trials"])]}
out=pathlib.Path("w3-source-route-probe-v2");out.mkdir(exist_ok=True)
(out/"receipt.json").write_text(json.dumps(rec,indent=2,sort_keys=True)+"\n")
print("W3_ROUTE_DISCOVERY_SUMMARY",json.dumps({"transport_ok":[x["name"] for x in result if x["transport_success"]],
"issuer_main_exact_recovery":rec["issuer_main_exact_recovery"],"new_qualifications":0}),flush=True)
