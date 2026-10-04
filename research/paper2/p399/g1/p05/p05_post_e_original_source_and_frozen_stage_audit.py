#!/usr/bin/env python3
"""P05 bounded original publisher PDF exact source after E + immutable-stage audit.

Web original critical PDF pages independently visually inspected before PRE_A.
This physically re-fetches published PDF to prove raw exact identity after E,
checks source-page textual anchor coverage and original historical git bytes.
These anchors are NOT independent full semantic reading, original supplementary
visual proof, parameter simulation or independent blinded human source rating.
"""
import hashlib,json,io,re,pathlib,subprocess,urllib.request
from pypdf import PdfReader
P=pathlib.Path(__file__).resolve().parent;ROOT="research/paper2/p399/g1/p05/"
URL="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1010654&type=printable"
SHA="80900fab574c1bf17c0bb65f81c87c1bdb6ba0dbbbbadfa31dcd2c8522735c7c"
with urllib.request.urlopen(urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0 (RelayTheory original publisher P05 after E exact source verification)"}),timeout=110) as fh:buf=fh.read()
assert buf.startswith(b"%PDF") and len(buf)==4726900 and hashlib.sha256(buf).hexdigest()==SHA,"P05 ORIGINAL PUBLISHED SOURCE FAIL-CLOSE"
pdf=PdfReader(io.BytesIO(buf));assert len(pdf.pages)==38
print("P05_ORIGINAL_EXACT_SOURCE_PASS",SHA,len(buf),len(pdf.pages),flush=True)
targets=[
("SOURCE_ORIGINAL_MODEL_BASE",14,["IVSN","VGG"]),
("SOURCE_FIVE_MODEL_COMPONENTS",15,["Fig 7","memory","saccade"]),
("SOURCE_SIX_STATIC_MODEL_RESULTS",17,["Fig 8","return"]),
("SOURCE_QUALITATIVE_DIVERGENCE",18,["Fig 9","preceding"]),
("SOURCE_ABLATION_TABLE1",19,["Table 1","0.75","memory"]),
("SOURCE_NO_UNIVERSAL_TRAINING",21,["Visual Search 2","quantitative"]),
("SOURCE_SIX_NOT_EIGHT_MODEL",26,["video","first six"]),
("SOURCE_EXACT_CLIPPED_MEMORY",27,["0.92","0.5","0.08","0.02"]),
("SOURCE_WEIGHT_AND_STOP",28,["0.2346","0.93","0.5","0.3"]),
("SOURCE_MEMORYLESS_NULL",29,["null model","saccade"])
]
checked=[]
for label,page,words in targets:
 t=re.sub(r"\\s+"," ",pdf.pages[page-1].extract_text() or "").lower()
 hit=[s for s in words if s.lower() in t]
 ok=len(hit)==len(words)
 print("P05_ORIGINAL_PAGE",page,label,"PASS" if ok else "FAIL","matches",hit,flush=True)
 assert ok,"P05 bounded original publisher textual page source anchor failed "+label
 checked.append({"id":label,"source_pdf_page_1_based":page,"matched":words})
stages=[
("PRE_A","bc08fc4714f4658600e8f74ef2e0af80fd9bc111","P05_PRE_A_ORIGINAL_SOURCE_EDITION_AND_ANCESTRY_v1.json"),
("A","bb92bec572afe080dc1467ea836c41dda1199e62","P05_PASS_A_SOURCE_FIRST_v1.json"),
("B","556b7d43f106ac7724deed7711b0046d8e4df257","P05_PASS_B_RESULT_INFORMED_FULL_A_v1.json"),
("C","431b21411677f7e7d6d44dd1bde8dab27cecc55f","P05_PASS_C_SOURCE_CLOSED_C1_C2_v1.json"),
("D","899b062ebc4c244e7badc4a724bdbae2c9018a3a","P05_PASS_D_UNCHANGED_GRAMMAR_v0_v1.json"),
("E","dc85b2c56cebf5f3e29462036dc5eac2b4e86aed","P05_PASS_E_ORIGINAL_SOURCE_FIDELITY_v1.json")
]
r={};prev=None
for label,git,path in stages:
 old=subprocess.check_output(["git","show",f"{git}:{ROOT}{path}"])
 now=(P/path).read_bytes()
 assert old==now,"P05 IMMUTABLE ORIGINAL HISTORIC SCIENCE MUTATED "+label
 if prev:subprocess.run(["git","merge-base","--is-ancestor",prev,git],check=True)
 r[label]={"commit":git,"file":ROOT+path,"original_raw_utf8_sha256":hashlib.sha256(old).hexdigest()}
 print("P05_FROZEN_STAGE_PASS",label,r[label]["original_raw_utf8_sha256"],flush=True)
 prev=git
A=json.loads((P/stages[1][2]).read_text())
B=json.loads((P/stages[2][2]).read_text())
C=json.loads((P/stages[3][2]).read_text())
D=json.loads((P/stages[4][2]).read_text())
E=json.loads((P/stages[5][2]).read_text())
assert len(A["source_first_claims"])==A["original_claim_count"]==30
assert len(A["original_source_relations"])==A["original_source_relation_count"]==42
assert B["entire_immutable_A_original_input"]==A and len(B["original_A_claim_independent_reread"])==30 and len(B["original_A_all_source_edges_review"])==42
assert C["C1_full_entire_frozen_A_reopened_BEFORE_patches"]["A_original_object_in_full"]==A
assert C["C2_unique_negative_count"]==17 and len(C["append_only_C1_and_source_negative_C2_patches"])==3
assert len(D["source_typed_grammar_claims"])==30 and len(D["source_relation_coverage"])==42
assert E["original_A_claims_covered"]==30 and E["original_A_dependencies_covered"]==42 and E["original_C_conditions_covered"]==17
assert E["source"]["full38_publisher_pdf_pixel_reviewed"] is False
assert not E["quantitative_original_training_replay_done"] and not E["qualified_automatically_by_this_E"]
proof={"original_publisher_P05_pdf_raw_sha256":SHA,"exact_original_bytes":len(buf),"exact_pdf_pages":len(pdf.pages),"source_page_anchor_checks":checked,"six_frozen_scientific_stage_raw_git_provenance":r,"A_B_C_D_E_counts":{"claims":30,"edges":42,"negative":17,"source_target_E":8},"script_limit":"Source anchors and Git identity only; original critical mathematical PDF visually reviewed independently earlier by same G1 researcher."}
digest=hashlib.sha256(json.dumps(proof,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
print("P05_POSTE_SOURCE_EVIDENCE_PROJECTION_SHA256",digest,flush=True)
print("P05_POSTE_ALL_PASS ten original source page anchors, six chronological unchanged raw Git stage files; no human/quantitative replay",flush=True)
pathlib.Path("g1-p05-poste").mkdir(exist_ok=True)
pathlib.Path("g1-p05-poste/source-receipt.json").write_text(json.dumps({"schema":"p399.g1.p05.after_E_independent_actual_original_source_check_v1","proof":proof,"canonical_projection_sha256":digest,"scientific_semantic_blind_human_proven":False,"final_global_G1":False},indent=2)+"\n")
