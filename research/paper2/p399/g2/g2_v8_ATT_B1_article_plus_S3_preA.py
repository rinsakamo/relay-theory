#!/usr/bin/env python3
"""Prospective PRE_A first-priority backup source bundle ATT-B1: original publisher
article (sole primary medium) plus publisher-linked *defining* S3 appendix.
No MAIN science, grammar or backup activation. No claim PDF visual review from pypdf.
"""
import datetime,hashlib,io,json,os,re,urllib.request
from pathlib import Path
from pypdf import PdfReader
DOI="10.1371/journal.pcbi.1011283"
SOURCES=[
 dict(role="SINGLE_PRIMARY_PUBLISHED_ARTICLE",url=f"https://journals.plos.org/ploscompbiol/article/file?id={DOI}&type=printable",sha="8c190f4d6e981061e4ccd67f4797b83ccdeb8f1d47d8368fdafe137f1ef44209",bytes=1760491,pages=20),
 dict(role="MODEL_DEFINING_PUBLISHER_LINKED_S3_APPENDIX_NOT_ANOTHER_PAPER",url=f"https://journals.plos.org/ploscompbiol/article/file?id={DOI}.s003&type=supplementary",sha="c71313033e52ccbbe5b0b3e8579959dfb7ac75c52ca254a36abca89ac8fcb72f",bytes=210828,pages=6)
]
def firstparty(url):
 from urllib.parse import urlparse
 return urlparse(url).hostname=="journals.plos.org" or urlparse(url).hostname=="storage.googleapis.com" and urlparse(url).path.startswith("/plos-corpus-prod/")
def get(u,limit=7*1024*1024):
 h={"User-Agent":"RelayTheory Paper2 source-only exact-prereg ATT pre-A verification","Accept":"application/pdf,text/html;q=0.9,*/*"}
 with urllib.request.urlopen(urllib.request.Request(u,headers=h),timeout=40) as r:return r.read(limit),r.geturl(),r.headers.get("Content-Type",""),r.status
def anchor_report(page):
 txt=page.extract_text() or ""
 clean=re.sub(r"\s+"," ",txt)
 # Match equation identifiers with no overly strong requirement that PDF text is semantic LaTex.
 eq=sorted({int(x) for x in re.findall(r"(?:Eq\.?|Equation|\()\s*\(?S\s*(1\d|[1-9])\b",clean,re.I)})
 raw=sorted({int(x) for x in re.findall(r"\bS\s*(1\d|[1-9])\b",clean)})
 negs=sorted({w for w in ("inhibition","facilitation","simultaneous","sequential","performance","fit","noise","control","baseline","model") if w in clean.lower()})
 return dict(text_chars=len(txt),extract_sha256=hashlib.sha256(txt.encode()).hexdigest(),explicit_equation_ref_digits=eq,all_S_digits=raw,method_scope_keyword_flags=negs)
def main():
 out={"schema":"p399.g2.att_b1.prospective_PRE_A_publisher_article_plus_defining_S3_v8",
 "utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"github_sha":os.getenv("GITHUB_SHA"),"publication_doi":DOI,
 "source_mode_policy":"ONE published original main PDF as sole primary and its explicitly referenced defining firstparty publisher S3 mathematics as a mandatory companion artifact fixed before A; S3 is NOT a second paper, NOT a replacement primary, nor permission to include every standalone supplemental document.",
 "prospective_freeze_is_technical_source_scope_not_semantic_scientific_qualification":True,
 "only_source_native_pre_A":True,"backup_activation":False,"main_40_unchanged":True,
 "all_semantic_math_figure_variant_negative_inspection_complete":False,"firstparty_raw_exact_receipt_repeated":False,"sources":[]}
 alltext=[]
 try:
  for s in SOURCES:
   raw,url,ct,status=get(s["url"])
   assert firstparty(url) and raw.startswith(b"%PDF-")
   pdf=PdfReader(io.BytesIO(raw),strict=False)
   digest=hashlib.sha256(raw).hexdigest()
   assert digest==s["sha"] and len(raw)==s["bytes"] and len(pdf.pages)==s["pages"],"published source identity differs from frozen raw!"
   docs=[anchor_report(p) for p in pdf.pages];text="\n".join(p.extract_text() or "" for p in pdf.pages)
   out["sources"].append(dict(role=s["role"],canonical_publisher_url=s["url"],effective_host=url.split("/")[2],
     pdf_exact_raw_sha256=digest,bytes=len(raw),pages=len(pdf.pages),pypdf_page_text_digests=docs,
     all_extractable_chars=len(text),external_original_pdf_not_stored_in_git=True))
   alltext.append(text)
  primary,s3=alltext
  source_urls=[f"https://journals.plos.org/ploscompbiol/article?id={DOI}"]
  html,h_url,h_ct,h_status=get(source_urls[0])
  h=html.decode("utf-8","replace")
  assert DOI in h and ".s003" in h and len(h)>100000 and h_status==200 and firstparty(h_url),"original main publisher does not link defining appendix"
  out["publisher_original_html_corroboration"]={"url":h_url,"response_sha256":hashlib.sha256(html).hexdigest(),
     "html_response_bytes":len(html),"doi_literal":True,"explicit_S3_document_link_present":True,
     "phrases_confirmed":{k:k in h for k in ("Eq. S1","Eq. S2","Eq. S3","Eq. S4","Eq. S6","Eq. S19","five models","S3 Text")},
     "source_link_consistency":True}
  out["S3_math_reference_surface"]={"unique_pypdf_S_digits":sorted(set(z for d in out["sources"][1]["pypdf_page_text_digests"] for z in d["all_S_digits"])),
     "main_published_model_reference":{k:k.lower() in primary.lower() for k in ("CoRLEGO","Target Selection","Movement Production","sequential","simultaneous","noise","fit")},
     "appendix_five_parameter_tables":{k:("Table "+k).lower() in s3.lower() for k in ("A","B","C","D")},
     "appendix_method_sections":{k:k.lower() in s3.lower() for k in ("Target Selection","Selection History","Movement Production","goodness of fit","best parameters")}}
  out["firstparty_raw_exact_receipt_repeated"]=True
 except Exception as e:out["failure_or_changed_publisher_original"]=repr(e)[:240]
 Path("g2-v8-att").mkdir(exist_ok=True)
 raw=(json.dumps(out,sort_keys=True,ensure_ascii=False,separators=(",",":"))+"\n").encode()
 Path("g2-v8-att/ATT_B1_PROSPECTIVE_PRIMARY_PLUS_DEFINING_S3_PRE_A.json").write_bytes(raw)
 print("G2_V8_ATT_METADATA_SHA256",hashlib.sha256(raw).hexdigest())
 print("G2_V8_ATT_STATUS",out["firstparty_raw_exact_receipt_repeated"],out.get("failure_or_changed_publisher_original"))
 for ss in out["sources"]:
  print("G2_V8_ATT_SOURCE",ss["role"],ss["pdf_exact_raw_sha256"],ss["pages"],ss["bytes"])
  for i,d in enumerate(ss["pypdf_page_text_digests"]):print("G2_V8_ATT_PAGE_MAP",ss["role"],i,"EQS",d["explicit_equation_ref_digits"],"ALLS",d["all_S_digits"],"MODELFLAGS",d["method_scope_keyword_flags"])
 print("G2_V8_ATT_CORROBORATION",out.get("publisher_original_html_corroboration"),out.get("S3_math_reference_surface"))
 if not out["firstparty_raw_exact_receipt_repeated"]:raise RuntimeError("Prospective backup pre-A exact source pair not reproducible")
if __name__=="__main__":main()
