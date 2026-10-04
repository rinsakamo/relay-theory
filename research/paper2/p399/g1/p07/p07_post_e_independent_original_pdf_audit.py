#!/usr/bin/env python3
"""Independent-after-E targeted primary-publisher P07 adverse source audit.

Actually reacquires original PLOS publisher bytes and checks exact SHA/size/pages.
Machine text anchors are BOUNDED and do not independently establish full semantic
correctness of mathematics, figures, original data/likelihood or human-blind rating.
All frozen historical stage JSON bytes AND actual Git ancestor order are tested.
"""
import hashlib,io,json,pathlib,re,subprocess,urllib.request
from pypdf import PdfReader
ROOT=pathlib.Path(__file__).resolve().parent
BASE="research/paper2/p399/g1/p07/"
SOURCE="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1000254&type=printable"
SHA="2b6cb16c821e937f712586ef52ac8edb895bf4f019d2c86b181aae805eb31959"
STAGES=[
 ("PRE_A","5ecf5893f09e3d10ca0b791bda3d0a2cfb25bacc","P07_PRE_A_ORIGINAL_SOURCE_AND_LINEAGE_FREEZE_v1.json"),
 ("A","ed01ae9a231db362a2aad372a16a9ae451a8cab1","P07_PASS_A_SOURCE_FIRST_v1.json"),
 ("B","7de912b5084fd9d68fe4b977ca25a496ad90df57","P07_PASS_B_RESULT_INFORMED_v1.json"),
 ("C","f2b5c4cced5bdc17675ca95db2ed4959b19b540b","P07_PASS_C_SOURCE_CLOSED_C1_C2_v1.json"),
 ("D","0a8144525976c2bb91bfa7ee319576033e9a211a","P07_PASS_D_UNCHANGED_GRAMMAR_V0_v1.json"),
 ("E","40ec6c3d8cf96fb9cd2697b8382f39a989be6910","P07_PASS_E_ORIGINAL_SOURCE_FIDELITY_v1.json")
]
def run(*args):return subprocess.check_output(args,stderr=subprocess.STDOUT)
def norm(x):return re.sub(r"\s+"," ",x).lower()
req=urllib.request.Request(SOURCE,headers={"User-Agent":"Mozilla/5.0 (RelayTheory P07 source-specific postE)"})
with urllib.request.urlopen(req,timeout=120) as f:raw=f.read();final_url=f.geturl()
assert raw[:5]==b"%PDF-", "not actual publisher PDF"
assert hashlib.sha256(raw).hexdigest()==SHA,"POST_E_ORIGINAL_SOURCE_SHA_MISMATCH"
assert len(raw)==613841,"POST_E_BYTES_CHANGED"
rd=PdfReader(io.BytesIO(raw),strict=False)
assert len(rd.pages)==14,"POST_E_PAGE_COUNT_CHANGED"
specific=[
 ("E01_CONDITIONAL_OPTIMUM",1,["divergence","controlled","uncontrolled","equation 3","optimum"]),
 ("E02_ACTUAL_TASK_FORM",8,["experimental procedures","two","computer","stag"]),
 ("E03_SEX_SPLIT",8,["six","three males","subjects"]),
 ("E04_NEGATIVE_TIMEOUT",8,["time out","four","240","1.7"]),
 ("E05_EXPERIMENT_FITTING",9,["model","subjects","equation"]),
 ("E06_SOURCE_HUMAN_MODEL",10,["85.8","fixed","figure 8"]),
 ("E07_PROSOCIAL_SOURCE",12,["equilibrium","sophisticated","unsophisticated","prosocial"])
]
checks=[]
for ident,page,markers in specific:
 t=norm(rd.pages[page].extract_text() or "")
 hits=[m for m in markers if m in t]
 ok=len(hits)==len(markers)
 checks.append({"id":ident,"physical_pdf_page_1based":page+1,"markers":markers,"matched":hits,"pass":ok})
 print("POST_E_SOURCE",ident,"PASS",ok,"hits",hits)
 assert ok, "POST_E_PDF_TARGET_FAILED "+ident
files={}
for i,(phase,sha,path) in enumerate(STAGES):
 # Git SHOW exact historical bytes, not current branch's possibly modified file.
 orig=run("git","show",f"{sha}:{BASE}{path}")
 cur=(ROOT/path).read_bytes()
 assert orig==cur, "FROZEN_HISTORICAL_STAGE_BYTES_CHANGED "+phase
 canonical=hashlib.sha256(orig).hexdigest()
 files[phase]={"git_introduction_commit":sha,"original_raw_sha256":canonical,"original_byte_count":len(orig),"path":BASE+path}
 print("FROZEN_STAGE",phase,"SHA",canonical,"BYTES",len(orig))
 if i:run("git","merge-base","--is-ancestor",STAGES[i-1][1],sha)
a=json.loads((ROOT/STAGES[1][2]).read_text())
b=json.loads((ROOT/STAGES[2][2]).read_text())
c=json.loads((ROOT/STAGES[3][2]).read_text())
d=json.loads((ROOT/STAGES[4][2]).read_text())
e=json.loads((ROOT/STAGES[5][2]).read_text())
assert len(a["A_claims"])==27 and len(a["A_source_edges"])==30
assert len(b["full_A_review"])==27 and len(b["edge_review"])==30 and len(b["source_order_independent_sweep"])==14
assert b["input_full_frozen_A"]["complete_original_A_object"]==a
assert len(c["C1_source_versus_entire_original_A_gap_test_before_any_patch"])==5
assert len(c["patches_append_only"])==3 and len(c["C2_unique_source_local_material_condition_ledger"])==12
assert c["all_conditions_accounted_once"]
assert len(d["complete_corrected_claim_mapping"])==27 and len(d["all_original_source_edge_relations"])==30
assert e["original_claim_coverage_count"]==27 and e["material_condition_coverage_count"]==12
assert e["post_E_source_specific_original_PDF_adverse_independent_CI"]=="PENDING_NOT_CLAIMED"
assert c["C_exceptions"]["novel_H1_H2_assertions"]==0
assert d["system_world_experiment"]["World_W"] and d["system_world_experiment"]["E_exp"]
print("PASS source specific original bytes 7/7 adverse targets and 6 immutable sequential stages and 27/30/12 counts")
packet={"schema":"p399.g1.p07.post_e.physical_original_targeted_source_scope.v1",
 "original_publisher_pdf_url":final_url,"publisher_source_raw_sha256":SHA,"publisher_bytes":len(raw),
 "original_publisher_page_count":len(rd.pages),"source_specific_checks":checks,
 "historical_stage_raw_sha256_and_chronology":files,
 "checks_all_pass":True,"new_formal_qualification_automatically_granted":False,
 "source_semantics_or_independent_rater_proven":False,
 "exact_original_numeric_replay_performed":False,
 "main_science_performed":False}
pathlib.Path("g1-p07-poste").mkdir(exist_ok=True)
pathlib.Path("g1-p07-poste/source-post-e.json").write_text(json.dumps(packet,indent=2)+"\n")
