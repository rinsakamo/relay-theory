#!/usr/bin/env python3
"""P13 AFTER E independent publisher exact dual-original and frozen Git audit.

Both source PDFs are actually re-acquired from ORIGINAL official issuer
because S1 32pp has complete ideal-Bayesian recurrence that the 26pp
main itself expressly delegates. Mechanical anchors scoped ONLY and
cannot substitute independent blinded scientific semantic review.
"""
import urllib.request,io,hashlib,json,pathlib,subprocess,re
from pypdf import PdfReader
ROOT="research/paper2/p399/g1/p13/"
P=pathlib.Path(__file__).resolve().parent
orig=[
 ("MAIN","https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1006681&type=printable","8e4aef9af81827f0bf5b6a82cd78b3ff9d6f60aa436b3e54156e6143e0c5af07",2109160,26,[
  (4,["0.2","0.35","0.8"]),
  (5,["Bayesian","run length","previous"]),
  (6,["Bayes","hyperprior","probability"]),
  (7,["Exp","criterion","Wilson"]),
  (8,["RL","Wilson","change"]),
  (9,["volatility","criterion"]),
  (12,["model comparison","Exp"]),
  (15,["Table 1","Table 2","Exp"])
 ]),
 ("S1","https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1006681.s001&type=supplementary","198eb18de66cca150dd233184781923680831f6e59007fec83ab54b5ec36453c",2738609,32,[
  (3,["run","previous","recursive"]),
  (4,["posterior","predictive","Conditional"]),
  (5,["hazard","posterior","change"]),
  (6,["boundary","posterior","Covert"]),
  (7,["Overt","criterion"]),
  (10,["Additional models","Bayesian"]),
  (11,["probability","incorrect","Reinforcement"]),
  (15,["Model recovery","datasets","observer"])
 ])
]
all_orig={}; anchorTotal=0
for name,url,sha,byt,pages,anchors in orig:
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (RelayTheory independent P13 after-E original dual publisher exact byte provenance)"}),timeout=150) as f:data=f.read()
 assert data.startswith(b"%PDF") and len(data)==byt and hashlib.sha256(data).hexdigest()==sha,"FAIL_CLOSED_ORIGINAL_"+name+"_CHANGED"
 reader=PdfReader(io.BytesIO(data));assert len(reader.pages)==pages
 print("P13_AFTER_E_PUBLISHER_ORIGINAL_EXACT_PASS",name,sha,byt,pages,flush=True)
 results=[]
 for pg,keys in anchors:
  t=re.sub(r"\\s+"," ",reader.pages[pg-1].extract_text() or "").lower()
  found=[key for key in keys if key.lower() in t]
  ok=len(found)==len(keys)
  print("P13_AFTER_E_ORIGINAL_PAGE",name,pg,"PASS" if ok else "FAIL",found,flush=True)
  assert ok,"SCOPE_ORIGINAL_ANCHOR_FAIL "+name+" "+str(pg)
  anchorTotal+=1
  results.append({"source_page_1based":pg,"matches":found})
 all_orig[name]={"original_pdf_sha256":sha,"original_raw_bytes":byt,"original_pdf_pages":pages,"actual_source_anchor_tests":results}
stage=[
("PRE_A","6b123ce85488b05bbd486fb22b5f8dc7251c22af","P13_PRE_A_PUBLISHED_MAIN_PLUS_REQUIRED_ORIGINAL_S1_FAMILY_FREEZE_v1.json"),
("A","6413c646841fd7912a22af0f5cb4e7e2266df419","P13_PASS_A_MAIN_AND_S1_SOURCE_FIRST_v1.json"),
("B","141c3dda8feeade76dcb0215efe41564374ad18f","P13_PASS_B_FULL_ORIGINAL_MAIN_S1_A_INFORMED_v1.json"),
("C","22803a9ae65fbb56dea321bab08c9f3dad8a993f","P13_PASS_C_SOURCE_CLOSED_C1_C2_v1.json"),
("D","af4992665a012e0bda24de7015e06f1a0b16c775","P13_PASS_D_UNCHANGED_GRAMMAR_V0_v1.json"),
("E","0940a51c03852e4ee74c457d0d6336b668774b4b","P13_PASS_E_REAL_ORIGINAL_MAIN_S1_FIDELITY_v1.json")
]
rawHist={};prev=None
for label,git,f in stage:
 stored=(P/f).read_bytes();original=subprocess.check_output(["git","show",f"{git}:{ROOT}{f}"])
 assert original==stored,"STAGE_SILENT_MUTATION_"+label
 if prev:subprocess.run(["git","merge-base","--is-ancestor",prev,git],check=True)
 prev=git
 digest=hashlib.sha256(original).hexdigest()
 rawHist[label]={"stage_git_commit":git,"raw_source_utf8_sha256":digest,"relative_path":ROOT+f}
 print("P13_AFTER_E_GIT_ORIGINAL_FROZEN",label,digest,flush=True)
A=json.loads((P/stage[1][2]).read_text());B=json.loads((P/stage[2][2]).read_text())
C=json.loads((P/stage[3][2]).read_text());D=json.loads((P/stage[4][2]).read_text());E=json.loads((P/stage[5][2]).read_text())
assert len(A["A_claims"])==34 and len(A["A_source_dependencies"])==50
assert B["entire_original_A_object_unmodified"]==A
assert len(B["review_all_source_claims"])==34 and len(B["review_all_A_source_edges"])==50
assert C["C1_full_original_frozen_A_input_REOPENED_BEFORE_PATCH"]["complete_original_A_object"]==A
assert C["counts"]["distinct_original_negative_conditions"]==18
assert len(C["append_only_C1_accepted_original_source_patches"])==3
assert len(D["source_claim_mapping"])==34 and len(D["source_dependency_mapping"])==50
assert len(E["original_source_fidelity_targets"])==10
assert E["all_18_original_material_negative_conditions_covered"]==18
assert E["raw_edition"]["original_all_pages_visually_read"] is False
assert E["original_scientific_result"].startswith("Source-native possible mechanisms")
assert E["formal_qualification_not_autogranted"] is True
print("P13_AFTER_E_FULL_PASS original both published raw sources 26+32 pages, 16/16 bounded text anchors, all6 exact historical source stages Git order and 34/50/18 source evidence",flush=True)
rec={"official_original_2_pdfs":all_orig,"six_historical_source_science_git_sha":rawHist,"after_E_actual_original_page_anchors":anchorTotal,"source_A_nodes":34,"source_A_edges":50,"C2_material_adverse":18,"qualified_automatically":False,"human_blinded_assessor":False,"numerical_original_model_replay":False,"MAIN_performed":False}
canon=hashlib.sha256(json.dumps(rec,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
print("P13_AFTER_E_SELECTED_SOURCE_PROJECTION_SHA256",canon,flush=True)
pathlib.Path("g1-p13-poste").mkdir(exist_ok=True)
pathlib.Path("g1-p13-poste/real-dual-original-and-six-git-history.json").write_text(json.dumps({"schema":"p399.g1.p13.after_E_dual_issuer_original_exact_audit.v1","selected_evidence_sha256":canon,"evidence":rec},indent=2)+"\n")
