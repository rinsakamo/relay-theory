#!/usr/bin/env python3
"""G2 original predeclared first-priority standby physical provenance; no replacement.
Inspect only publisher-original source/edition identity, not anticipated MAIN outcomes.
"""
import concurrent.futures,datetime,hashlib,io,json,os,re,urllib.request,urllib.error
from pathlib import Path
from pypdf import PdfReader
ROOT=Path("research/paper2/p399/g2")
backups=json.loads((ROOT/"MAIN40_G2_OBJECTIVE_BACKUPS_v1.json").read_text())
roster=json.loads((ROOT/"MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json").read_text())
targets={"ATT-03":"ATT-B1","BLF-01":"BLF-B1","PRD-01":"PRD-B1"}
by_id={x["id"]:x for x in backups["backups"]}
bydoi={x["doi"].lower():x["slot"] for x in roster["selected_working_roster"]}
assert len(bydoi)==40
H={"User-Agent":"RelayTheory-G2-publisher-original-objective-standby/1.0","Accept":"application/pdf,text/html,*/*"}
def fetch(url):
 request=urllib.request.Request(url,headers=H)
 with urllib.request.urlopen(request,timeout=28) as f:
  return f.read(30*1024*1024),f.geturl(),f.headers.get("Content-Type","")
def one(pair):
 slot,cand=pair;item=by_id[cand];doi=item["doi"].lower()
 out={"affected_slot":slot,"backup_slot":cand,"doi":doi,"predeclared_backup_title_v1":item["title"],
  "predeclared_backup_gate":item["gate"],"initial_40_doi_collision":bydoi.get(doi),
  "prospective_only":True,"actual_replacement_activated":False,"source_scientific_admission":False,
  "model_family_independence_certified":False,"final_edition_certified":False}
 first="https://journals.plos.org/ploscompbiol/article?id="+doi
 try:
  b,actual,ct=fetch(first);t=b.decode("utf-8","replace")
  out["original_publisher_html"]={"url":actual,"raw_sha256":hashlib.sha256(b).hexdigest(),
      "raw_bytes":len(b),"doi_exact_present":doi in t.lower(),
      "publisher_proof_banner":"this is an uncorrected proof" in t.lower(),
      "correction_banner_tagged":bool(re.search(r"(correction|updated)",re.sub(r"<[^>]*>"," ",t.lower())[:20000])),
      "publisher_original_complete_article_tags":all(x in t.lower() for x in (">abstract",">introduction",">references")),
      "note":"Correction banner detection is coarse and does not demonstrate correction absence"}
 except Exception as e:out["html_error"]=str(e)[:160]
 pdf="https://journals.plos.org/ploscompbiol/article/file?id="+doi+"&type=printable"
 try:
  b,actual,ct=fetch(pdf)
  assert b.startswith(b"%PDF-"),"not_pdf"
  p=PdfReader(io.BytesIO(b),strict=False);firstpages=" ".join((p.pages[i].extract_text() or "") for i in range(min(2,len(p.pages)))).lower()
  out["official_original_pdf"]={"url":actual,"sha256":hashlib.sha256(b).hexdigest(),"raw_bytes":len(b),
      "pages":len(p.pages),"doi_on_original_first_two_pages":doi in firstpages,
      "publisher_pdf_identity_not_title_equivalence":doi in firstpages}
 except Exception as e:out["pdf_error"]=str(e)[:160]
 out["model_central_family_preregistered_not_adjudicated"]=True
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:r=list(pool.map(one,targets.items()))
result={"schema":"relaytheory.p399.g2.v6.preregistered_primary_backup_original_media_PRE_A_only",
   "runner_sha":os.environ.get("GITHUB_SHA"),"time_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
   "initial_selected_40_dois_unchanged":True,"backups_activated":0,
   "owner_go_required_prior_to_any_backup_placement":True,
   "source_version_and_family_final_admission":False,"no_original_publisher_bytes_redistributed":True,"rows":r}
Path("g2-v6-backup").mkdir(exist_ok=True)
b=(json.dumps(result,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
Path("g2-v6-backup/predeclared_first_standby_source_metadata.json").write_bytes(b)
print("G2_V6_BACKUP_RESEARCH_METADATA_SHA256",hashlib.sha256(b).hexdigest())
for x in r:print("G2_V6_BACKUP",x["backup_slot"],x["doi"],"PDF",x.get("official_original_pdf"),"HTML",x.get("original_publisher_html"),"ERRORS",x.get("pdf_error"),x.get("html_error"),"ACTIVATED",False)
print("G2_V6_BACKUP_COUNTS",sum("official_original_pdf" in x for x in r),sum("original_publisher_html" in x for x in r),"NEW_MAIN_SCIENCE",0,"ACTUAL_BACKUP_ACTIVATIONS",0)
