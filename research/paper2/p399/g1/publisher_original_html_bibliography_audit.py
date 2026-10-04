#!/usr/bin/env python3
"""Extract ORIGINAL publisher PLOS bibliographic metadata and linked corrections, no science.

Publisher landing/full article HTML is not a surrogate for primary PDF's mathematical
visual audit. This script does not certify correction *absence* merely from no link.
"""
import concurrent.futures,datetime,json,re,urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
DOI_SUFFIX={"P05":"1010654","P06":"1004375","P07":"1000254","P08":"1005418",
"P09":"1006435","P10":"1010699","P11":"1008971","P12":"1006043",
"P13":"1006681","P14":"1008969","P15":"1010589","P16":"1003648",
"P17":"1009738","P18":"1008552","P19":"1009866","P20":"1006676"}
KNOWN_CORRECTIONS={"P08":"10.1371/journal.pcbi.1005908","P10":"10.1371/journal.pcbi.1010775"}
def check(item):
 id,suffix=item;doi="10.1371/journal.pcbi."+suffix
 url="https://journals.plos.org/ploscompbiol/article?id="+doi
 row={"id":id,"registered_doi":doi,"publisher_url":url,
 "original_publisher_html_actual_bytes_acquired":False,
 "correction_absence_established":False,"source_fully_qualified":False,
 "scientific_source_primary_selected":False}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (RelayTheory G1 bibliographic audit)"}),timeout=90) as res:
   raw=res.read()
   row["redirect_resolved_url"]=res.geturl()
  soup=BeautifulSoup(raw,"html.parser")
  def meta(key):
   el=soup.find("meta",attrs={"name":key}) or soup.find("meta",attrs={"property":key})
   return el.get("content") if el else None
  row.update(original_publisher_html_actual_bytes_acquired=True,
     raw_publisher_html_sha256=__import__("hashlib").sha256(raw).hexdigest(),
     raw_publisher_html_byte_count=len(raw),
     publisher_citation_doi=meta("citation_doi"),
     publisher_citation_title=meta("citation_title"),
     publisher_citation_date=meta("citation_date"),
     publisher_citation_publication_date=meta("citation_publication_date"),
     publisher_dc_date=meta("dc.date"),
     publisher_journal=meta("citation_journal_title"),
     publisher_citation_pdf_url=meta("citation_pdf_url"),
     source_heading_count=len(soup.find_all(["h2","h3"])),
     publisher_html_has_expected_doi=doi.lower() in raw.decode("utf-8","replace").lower())
  headings=[x.get_text(" ",strip=True) for x in soup.find_all(["h2","h3"])]
  row["section_heading_inventory"]=headings[:90]
  correction_headings=[x for x in headings if re.fullmatch(r"corrections?",x.strip(),re.I)]
  row["publisher_explicit_correction_section_seen"]=bool(correction_headings)
  row["publisher_correction_doi_urls"]=sorted(set(re.findall(r"10[.]1371/journal[.]pcbi[.][0-9]{7}",raw.decode("utf-8","replace")))&set(KNOWN_CORRECTIONS.values()))
  row["registered_known_correction"]=KNOWN_CORRECTIONS.get(id)
  row["known_correction_doi_present_in_original_html"]=KNOWN_CORRECTIONS[id] in raw.decode("utf-8","replace") if id in KNOWN_CORRECTIONS else None
  row["has_textual_body_equations_or_figures_hint"]=bool(soup.find_all("figure") or "equation" in soup.get_text(" ",strip=True).lower())
  if row["publisher_citation_doi"] and row["publisher_citation_doi"].lower().replace("https://doi.org/","")!=doi:
   row["audit_exception"]="PUBLISHER_CITATION_DOI_MISMATCH"
  del raw,soup
 except Exception as e:row["failure"]=repr(e)
 return row
if __name__=="__main__":
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  rows=list(pool.map(check,DOI_SUFFIX.items()))
 packet={"schema":"p399.g1.official-publisher-original-html-citation-metadata-and-correction-link-screen.v1",
  "timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "correction_absence_for_unflagged_papers_NOT_ESTABLISHED":True,
  "all_other_corrections_still_need_version_status_review":True,
  "no_source_scientifically_qualified_by_metadata":True,"rows":rows}
 Path("g1-pubmeta").mkdir(exist_ok=True)
 Path("g1-pubmeta/html-original-metadata.json").write_text(json.dumps(packet,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 for r in rows:
  print("G1PUBMETA",r["id"],"DOI",r.get("publisher_citation_doi"),"date",r.get("publisher_citation_date") or r.get("publisher_citation_publication_date"),"sha",r.get("raw_publisher_html_sha256"),"correction_section",r.get("publisher_explicit_correction_section_seen"),"known_correction_link",r.get("known_correction_doi_present_in_original_html"),"error",r.get("failure"))
 print("G1PUBMETA_COUNTS",sum(x["original_publisher_html_actual_bytes_acquired"] for x in rows),
  "known_published_corrections",sum(x.get("known_correction_doi_present_in_original_html") is True for x in rows),
  "scientifically_admitted",0)
