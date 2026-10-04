#!/usr/bin/env python3
"""Publisher vs independent archive source-format verification, only four G2 blocks.
Archive bytes are NEVER promoted into publisher-original eligibility by this probe.
INT13 formal PLOS proof banner check is edition metadata only, not MAIN science.
"""
import concurrent.futures,datetime,hashlib,io,json,os,re,urllib.request,urllib.error,xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader
UA={"User-Agent":"RelayTheory-G2-original-source-metadata-audit/1.2 (research, public first-party sources)","Accept":"application/pdf,application/xml,text/html,*/*"}
S={
"BLF-01":{"doi":"10.1016/j.isci.2025.112844","pmcid":"PMC12221758","pubmed":40612506,"pii":"S2589004225011058",
 "first_party_urls":["https://www.cell.com/iscience/pdf/S2589-0042(25)01105-8.pdf","https://www.cell.com/iscience/fulltext/S2589-0042(25)01105-8","https://api.elsevier.com/content/article/pii/S2589004225011058?httpAccept=text/xml","https://ars.els-cdn.com/content/image/1-s2.0-S2589004225011058-main.pdf"]},
"INT-01":{"doi":"10.1016/j.cognition.2024.105967","pmcid":"PMC12052257","pubmed":39368350,"pii":"S0010027724002531",
 "first_party_urls":["https://api.elsevier.com/content/article/pii/S0010027724002531?httpAccept=text/xml","https://www.sciencedirect.com/science/article/pii/S0010027724002531/pdfft?isDTMRedir=true&download=true"]},
"ATT-03":{"doi":"10.1016/j.neuron.2009.01.002","pmcid":"PMC2752446","pubmed":19186161,"pii":"S0896627309000038",
 "first_party_urls":["https://api.elsevier.com/content/article/pii/S0896627309000038?httpAccept=text/xml","https://www.cell.com/neuron/pdf/S0896-6273(09)00003-8.pdf"]},
"PRD-01":{"doi":"10.1038/s41562-024-01930-8",
 "first_party_urls":["https://www.nature.com/articles/s41562-024-01930-8.pdf","https://link.springer.com/content/pdf/10.1038/s41562-024-01930-8.pdf"]}
}
def req(url,max_bytes=14*1024*1024):
 request=urllib.request.Request(url,headers=UA)
 with urllib.request.urlopen(request,timeout=15) as f:return f.read(max_bytes),f.geturl(),f.headers.get("Content-Type",""),f.status
def site(url):
 from urllib.parse import urlparse
 return urlparse(url).netloc
def fingerprint(buf,expected_doi):
 raw=buf[:3500000]
 r={"byte_size":len(buf),"sha256":hashlib.sha256(buf).hexdigest(),"pdf":buf.startswith(b"%PDF-"),"doi_found_raw":expected_doi.lower().encode() in raw.lower()}
 if r["pdf"]:
  try:
   pdf=PdfReader(io.BytesIO(buf),strict=False);txt=" ".join((z.extract_text() or "") for z in pdf.pages[:2]).lower()
   r.update(pages=len(pdf.pages),doi_found_first_2_pdf_pages=expected_doi.lower() in txt,first_2_text_chars=len(txt),
    iScience_published_journal_header="iscience" in txt,
    elsevier_typeset_footer="published by elsevier" in txt,
    first_2_page_title_words=sorted(set(re.findall(r"\b(?:belief|updating|decision|hierarchically|normalization|attention)\b",txt))))
  except Exception as e:r["parse_error"]=str(e)[:110]
 return r
def scan_one(item):
 name,obj=item;doi=obj["doi"];out={"slot":name,"doi":doi,"first_party":[],
  "source_authorized_original_verified":False,"archived_candidate_only":None,"pmc_published_version_verified":False}
 for u in obj["first_party_urls"]:
  entry={"requested_url":u,"host":site(u)}
  try:
   b,real,ct,stat=req(u)
   entry.update(actual_url=real,status=stat,content_type=ct,raw=fingerprint(b,doi))
   if entry["raw"]["pdf"] and entry["raw"].get("doi_found_first_2_pdf_pages"):
    entry["publisher_first_party_original_pdf_candidate"]=True
    # DOI and PDF signature alone do not certify corrected edition.
    out["first_party_publisher_pdf_candidate"]=entry.copy()
   else:entry["publisher_first_party_original_pdf_candidate"]=False
  except Exception as exc:entry["error"]=str(exc)[:160]
  out["first_party"].append(entry)
 if "pmcid" in obj:
  # NLM is independently labeled archival source, not first-party publication. We
  # only extract structured edition/PII metadata, then fingerprint archived PDFs.
  full="https://www.ebi.ac.uk/europepmc/webservices/rest/"+obj["pmcid"]+"/fullTextXML"
  try:
   b,real,ct,s=req(full,7*1024*1024)
   root=ET.fromstring(b)
   ids=[(el.attrib.get("pub-id-type"),(el.text or "").strip()) for el in root.findall(".//front/article-meta/article-id")]
   labels={x.attrib.get("article-type") for x in root.findall(".")}
   out["archival_metadata"]={"url":real,"status":s,"article_ids":ids,"archive_xml_sha256":hashlib.sha256(b).hexdigest(),
     "front_copyright_text":" ".join((e.text or "") for e in root.findall(".//front/article-meta/permissions/copyright-statement"))[:180],
     "pmcid_has_expected_doi":any(k=="doi" and v.lower()==doi.lower() for k,v in ids),
     "pmc_piis":[v for k,v in ids if k=="pii"],
     "archive_publisher_typeset_possible":b"Published by Elsevier" in b,
     "full_archived_xml_chars":len(b)}
  except Exception as e:out["archival_metadata"]={"url":full,"error":str(e)[:120]}
  for url in [f"https://pmc.ncbi.nlm.nih.gov/articles/{obj['pmcid']}/pdf/",f"https://www.ebi.ac.uk/europepmc/webservices/rest/{obj['pmcid']}/fullTextXML"]:
   if "fullTextXML" in url:continue
   try:
    b,real,ct,stat=req(url)
    info={"archival_url":url,"effective_url":real,"status":stat,"content_type":ct,
     "fingerprint":fingerprint(b,doi)}
    out["archived_candidate_only"]=info
   except Exception as e:out["archived_pdf_error"]=str(e)[:160]
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as exe:rows=list(exe.map(scan_one,S.items()))
plos="https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014796"
try:
 b,real,ct,s=req(plos,4*1024*1024)
 txt=re.sub(r"<[^>]*>"," ",b.decode("utf-8","replace"))
 edition={"url":real,"http_status":s,"source_raw_sha256":hashlib.sha256(b).hexdigest(),
          "still_explicit_uncorrected_proof":"This is an uncorrected proof." in txt}
except Exception as e:edition={"url":plos,"error":str(e)}
receipt={"schema":"relaytheory.g2.four_primary_publishers_vs_archive_edition_discrimination.v6",
 "utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"runner_sha":os.environ.get("GITHUB_SHA"),
 "source_replay_no_public_copyrighted_original_bytes":True,"archive_copies_are_NOT_authorized_as_publisher_original":True,
 "plos_int13_edition":edition,"records":rows}
Path("g2-v6").mkdir(exist_ok=True)
raw=(json.dumps(receipt,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
Path("g2-v6/restricted_origin_and_edition_metadata.json").write_bytes(raw)
print("G2_V6_METADATA_SHA256",hashlib.sha256(raw).hexdigest())
print("G2_V6_INT13_PLOS",edition)
for x in rows:print("G2_V6_SLOT",x["slot"],"FIRSTPARTY",x.get("first_party_publisher_pdf_candidate"),"ARCHIVE",x.get("archival_metadata"),"ARCHIVEPDF",x.get("archived_candidate_only"),"FIRSTPARTYFAILS",[(y["requested_url"],y.get("error"),y.get("raw",{}).get("pdf")) for y in x["first_party"]])
print("G2_V6_REAL_NEW_PUBLISHER_PDF_CANDIDATE",sum(bool(x.get("first_party_publisher_pdf_candidate")) for x in rows),"SCIENCE_ADMITTED",0)
