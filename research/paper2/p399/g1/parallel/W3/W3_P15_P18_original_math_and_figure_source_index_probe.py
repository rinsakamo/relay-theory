#!/usr/bin/env python3
"""Source-only primary math and figure locator witness for P15/P18 W3.
NOT PRE_A freeze, not an A scientific transaction, and not independent blinded source audit.
"""
import io, hashlib, json, os, pathlib, urllib.request
from pypdf import PdfReader
import fitz
from PIL import Image
BASE="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi."
q=[
("P15_MAIN","1010589","printable","591339de97a02abc1faeb276b48b8dfc73b518aca2d8ad1c36a10ba96038e002",27),
("P15_S1_APPENDIX","1010589.s001","supplementary","cc407ed073633a3aff3719ef4ceb0d97446026b771fd15f5bb6cd74d99dff074",5),
("P15_S1_TABLE","1010589.s003","supplementary","a1d5cb779afd0a918f7c1102720e03aadd2ef1bed57327aafec60ef4d3975a3a",1),
("P15_S2_TABLE","1010589.s004","supplementary","58c1963db4a3770c65fc9dc5d9973f7a397fd61401c350a4a20537eaabc646b3",1),
("P18_MAIN","1008552","printable","cb75481590c34686eeeb8635dcb8a381283bcbe3e7f8ed9f0ee246fa95e419d1",28),
("P18_S1_TABLE","1008552.s007","supplementary","25465f1dfe9c05f8e37028b16c1070dc19e437301804d7344c42651a2e748f48",1),
]
f=[]
for label,doi,t,expected,pages in q:
 url=BASE+doi+"&type="+t
 req=urllib.request.Request(url,headers={"User-Agent":"RelayTheory-W3-original-source-math-visual-inspection","Accept":"application/pdf"})
 with urllib.request.urlopen(req,timeout=32) as r: raw=r.read()
 got=hashlib.sha256(raw).hexdigest()
 assert got==expected, f"{label} exact pinned published PDF changed or wrong version: {got}"
 assert raw[:5]==b"%PDF-"
 reader=PdfReader(io.BytesIO(raw))
 assert len(reader.pages)==pages,(label,len(reader.pages))
 fit=fitz.open(stream=raw,filetype="pdf")
 rec={"label":label,"doi":doi,"official_url":url,"sha256":got,"pages":pages,"pages_inspected":[]}
 if label=="P15_MAIN": indexes=[1,2,3,4,5,6,7,8,14,16,21]
 elif label=="P18_MAIN": indexes=[2,3,4,5,9,10,11,12,13,14,17,18,20,22]
 else: indexes=list(range(pages))
 for p in indexes:
  pg=fit[p]
  w=pg.get_pixmap(matrix=fitz.Matrix(0.55,0.55))
  assert w.width>180 and w.height>180
  full=(reader.pages[p].extract_text() or "").replace("\u0000","").strip()
  rec["pages_inspected"].append({"page_1based":p+1,"render_dims":[w.width,w.height],"text_sha256":hashlib.sha256(full.encode()).hexdigest(),
    "extract_len":len(full)})
  limit=3700 if label=="P15_S1_APPENDIX" else (2500 if "TABLE" in label else 500)
  print("\n===== SOURCE_EXCERPT",label,"page",p+1,"chars",len(full),"=====\n",full[:limit].replace("\n"," "),flush=True)
 print("SOURCE_VALIDATED",label,pages,got,flush=True)
 f.append(rec)
out=pathlib.Path(os.environ.get("RUNNER_TEMP","/tmp"))/"W3_P15_P18_original_math_and_figure_source_index.json"
out.write_text(json.dumps({"kind":"ORIGINAL_PUBLISHER_SOURCE_MATH_AND_RENDERABILITY_INDEX_ONLY","not_visual_semantic_proof":True,"not_science_stage":True,"sources":f},indent=2)+"\n")
