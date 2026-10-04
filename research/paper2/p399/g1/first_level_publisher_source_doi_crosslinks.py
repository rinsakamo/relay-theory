#!/usr/bin/env python3
"""First-level DOI reference-mention triage across the exact 16 PLOS publisher article pages.

A DOI mention is NOT proof of direct mechanistic derivation or central-model duplicate.
An absent DOI mention is NOT proof of independent ancestry (undigitized/DOI-less references).
"""
import concurrent.futures,datetime,json,re,urllib.request
from bs4 import BeautifulSoup
from pathlib import Path
NEW={"P05":"10.1371/journal.pcbi.1010654","P06":"10.1371/journal.pcbi.1004375",
"P07":"10.1371/journal.pcbi.1000254","P08":"10.1371/journal.pcbi.1005418",
"P09":"10.1371/journal.pcbi.1006435","P10":"10.1371/journal.pcbi.1010699",
"P11":"10.1371/journal.pcbi.1008971","P12":"10.1371/journal.pcbi.1006043",
"P13":"10.1371/journal.pcbi.1006681","P14":"10.1371/journal.pcbi.1008969",
"P15":"10.1371/journal.pcbi.1010589","P16":"10.1371/journal.pcbi.1003648",
"P17":"10.1371/journal.pcbi.1009738","P18":"10.1371/journal.pcbi.1008552",
"P19":"10.1371/journal.pcbi.1009866","P20":"10.1371/journal.pcbi.1006676"}
PF={"PF01":"10.1371/journal.pcbi.1006928","PF02":"10.1371/journal.pcbi.1004331",
"PF03":"10.1371/journal.pcbi.1011801","PF04":"10.1371/journal.pcbi.1003364"}
MAIN={"ATT-01":"10.1007/s42113-024-00197-6","BLF-01":"10.1016/j.isci.2025.112844",
"CNC-01":"10.1038/s41562-023-01719-1","LRN-01":"10.1038/s41467-025-58848-6",
"MEM-01":"10.1007/s42113-023-00189-y","PRD-01":"10.1038/s41562-024-01930-8",
"INT-01":"10.1016/j.cognition.2024.105967","INT-02":"10.3390/e26060484",
"INT-03":"10.1073/pnas.95.24.14529","INT-04":"10.1038/s41562-023-01799-z"}
TARGETS={**NEW,**PF,**MAIN}
def scan(item):
 pid,doi=item;url="https://journals.plos.org/ploscompbiol/article?id="+doi
 row={"id":pid,"doi":doi,"official_html_url":url,"full_original_bibliography_reference_scope_verified":False,
      "central_family_decided_by_DOI_scan":False,"outgoing_DOI_mentions":[]}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (RelayTheory G1 neutral bibliographic triage)"})
  with urllib.request.urlopen(req,timeout=90) as resp: raw=resp.read()
  html=raw.decode("utf-8","replace")
  soup=BeautifulSoup(raw,"html.parser")
  headings=soup.find_all(["h2","h3"])
  refs=[x for x in headings if re.fullmatch("References",x.get_text(" ",strip=True),re.I)]
  row["publisher_article_has_references_heading"]=bool(refs)
  # Full publisher HTML may include surrounding navigation. Treat positives as
  # triage only until cited reference record is independently source-verified.
  normalized=html.lower().replace("&#x2f;","/").replace("&#47;","/")
  for other,otherdoi in TARGETS.items():
   if pid==other: continue
   if otherdoi.lower() in normalized:
    row["outgoing_DOI_mentions"].append({
     "target":other,"doi":otherdoi,
     "status":"SOURCE_HTML_DOI_STRING_HIT_NOT_YET_PROVEN_ACTUAL_REFERENCE_OR_DERIVATION"})
  row["official_html_request_success"]=True
 except Exception as e:
  row["official_html_request_success"]=False
  row["error"]=repr(e)
 return row
if __name__=="__main__":
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  rows=list(pool.map(scan,NEW.items()))
 d={"schema":"relaytheory.p399.g1.publisher-original-html-cross-DOI-mention-triage.v1",
    "timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "no_DOI_hit_does_not_establish_independence":True,
    "positive_DOI_hit_is_not_mechanistic_derivation":True,
    "historical_60_original_manifests_not_yet_loaded":True,
    "not_source_admission":True,"rows":rows}
 Path("g1-crossrefs").mkdir(exist_ok=True)
 Path("g1-crossrefs/crossrefs.json").write_text(json.dumps(d,indent=2)+"\n")
 for x in rows:
  print("G1CROSSREF",x["id"],"success",x["official_html_request_success"],
        "other_16_and_PF_and_known_MAIN_DOI_mentions",",".join(y["target"] for y in x["outgoing_DOI_mentions"]),
        "error",x.get("error"))
 print("G1CROSSREF_SUMMARY",sum(x["official_html_request_success"] for x in rows),
       "source-accessible",sum(len(x["outgoing_DOI_mentions"]) for x in rows),"nonqualifying DOI source-page mentions")
