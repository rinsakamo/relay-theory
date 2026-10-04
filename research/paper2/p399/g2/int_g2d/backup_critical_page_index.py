#!/usr/bin/env python3
"""Source-native page-index-only audit of actual official original backup PDFs.
No MAIN science, no full scientific qualification; index all page text of backup originals.
Does NOT assert pixel-perfect equations or that every negative is captured.
"""
import hashlib,json,os,re,urllib.request
from io import BytesIO
from datetime import datetime,timezone
from pypdf import PdfReader
items=[
("INT-B1","https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1007720&type=printable","0a79da7e5504e1e970332a65401d3da2c6282bb48ad640f760c17f4bc06a3fcf",["meta-generalization","joint clustering","independent clustering","Chinese Restaurant Process","Q-learning","UCB","limitation","figure"]),
("INT-B2","https://cdn.elifesciences.org/articles/39497/elife-39497-v3.pdf","c2adddf8d232d851d9decbb304fb02107686cf55a5dad4cbbfd8b0fd7ac7d64a",["external","internal","predict","model","fit","control","limitation","figure"]),
("INT-B3","https://cdn.elifesciences.org/articles/57244/elife-57244-v2.pdf","9e13535592ff1cf36c9eb4a9a1daae23cb6dfa8a916a40586a6cc5c651b80d35",["spectral","causal","frontal","parietal","integrat","segregat","Nee","limitation","figure"]),
("INT-B4","https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1012872&type=printable","67fe0d5aaed06474e53344716de73050f08e1e900420fb078712921312fb5ef6",["working memory","reinforcement learning","prediction error","negative feedback","Model #5","Model #4","AIC","limitation","figure"])]
results=[]
for slot,url,sha,patterns in items:
 rec={"slot":slot,"publisher_pdf_url":url,"sha_expected":sha,"time_utc":datetime.now(timezone.utc).isoformat(),
      "source_math_image_pixel_visual_audited":False,"complete_negative_sweep_qualified":False,
      "semantic_full_model_qualification":False}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
  with urllib.request.urlopen(req,timeout=12) as f: data=f.read(13*1024*1024);rec["http_status"]=f.status;rec["final_url"]=f.geturl()
  rec.update(actual_pdf_sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),pdf_signature=data.startswith(b"%PDF-"))
  if not rec["pdf_signature"] or rec["actual_pdf_sha256"]!=sha:
   rec["error"]="FAIL_CLOSED_OFFICIAL_PDF_SOURCE_SHA_OR_SIGNATURE_MISMATCH";results.append(rec);continue
  rd=PdfReader(BytesIO(data));pages=[re.sub(r"\s+"," ",x.extract_text() or "").lower() for x in rd.pages]
  rec["pages"]=len(pages)
  rec["page_index_1_based_by_term"]={p:[i+1 for i,t in enumerate(pages) if p.lower() in t][:20] for p in patterns}
  rec["candidate_fig_caption_page_indices"]=[i+1 for i,t in enumerate(pages) if re.search(r"(?:fig\.?|figure)\s*\d",t)][:45]
  rec["candidate_table_page_indices"]=[i+1 for i,t in enumerate(pages) if re.search(r"table\s*\d",t)][:30]
  rec["page_text_sha256"]=[hashlib.sha256(s.encode()).hexdigest() for s in pages]
  rec["pages_examined_by_text_extraction"]=len(pages)
  rec["page_index_ONLY_not_semantics"]=True
 except Exception as e:rec["error"]=type(e).__name__+":"+str(e)[:160]
 results.append(rec)
 print(slot,json.dumps({k:v for k,v in rec.items() if k!="page_text_sha256"},sort_keys=True),flush=True)
os.makedirs("g2d-int-critical-pages",exist_ok=True)
with open("g2d-int-critical-pages/source_native_text_index.json","w") as f:
 json.dump({"schema":"p399.g2d.backup_official_pdf_page_locator_only.v1",
            "not_scientific_semantic_or_visual_qualification":True,
            "models_are_original_publisher_backup_candidates_only":True,
            "records":results},f,indent=2)
if not all(r.get("page_index_ONLY_not_semantics") for r in results):
 raise SystemExit("Fail closed: some original publisher SHA/page texts inaccessible; no science qualification")
