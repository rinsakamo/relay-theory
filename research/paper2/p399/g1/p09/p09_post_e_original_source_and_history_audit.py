#!/usr/bin/env python3
"""P09 independently executed post-E exact original-source and frozen stage audit.

Checks original real publisher-pdf raw SHA/bytes/pages, source-specific negative
page anchors and frozen PRE_A/A/B/C/D/E git-original byte/ancestor chronology.
Machine text anchors are a bounded source receipt, NOT independent semantic,
visual or human reliability proof. Visual PDF checks were run and reviewed
separately BEFORE PRE_A: 37183422420 and 37183471486.
"""
import urllib.request,hashlib,io,json,pathlib,subprocess,re,datetime
from pypdf import PdfReader
P=pathlib.Path(__file__).resolve().parent
ROOT="research/paper2/p399/g1/p09/"
u="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1006435&type=printable"
sha="9d5f8df792c19e88749311dc2f9688705fe3aeaea4eb7bfad7e761ca90e5e6b2"
req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0 (RelayTheory exact P09 postE original source audit)"})
with urllib.request.urlopen(req,timeout=120) as f:raw=f.read();final=f.geturl()
assert raw.startswith(b"%PDF"),"NOT_PUBLISHER_PDF"
assert len(raw)==3283055,"WRONG_ORIGINAL_RAW_BYTES_LENGTH"
assert hashlib.sha256(raw).hexdigest()==sha,"DIFFERENT_ORIGINAL_EDITION_OR_BYTE_INTEGRITY"
pdf=PdfReader(io.BytesIO(raw),strict=False)
assert len(pdf.pages)==21,"P09_DIFFERENT_ORIGINAL_PAGE_COUNT"
targets=[
 ("S01_ARCHITECTURE_AND_NEGATIVE_TABLE",4,["fig 1","table 1","pct"]),
 ("S02_KC_UNDERLYING_MECHANISM",5,["phenomenologically","pct","kenyon"]),
 ("S03_PCT_ABLATION_SIMULATION_DENOM",6,["fig 2","338","360","pct"]),
 ("S04_MODEL_PCT_NECESSITY_SCOPE",8,["pct","transfer","associative"]),
 ("S05_OLDER_BEE_VALIDATION",9,["fig 3","per"]),
 ("S06_TRANSIENT_LIMITS",10,["transient","limitation","capuchins"]),
 ("S07_TUNED_PARAMETERS",11,["table 2","2:1","model parameter selection"]),
 ("S08_REDUCED_LOGIT_ATTENUATION",12,["reduced model","0.7"]),
 ("S09_FULL_SPARSE",13,["full model","0.02","kenyon"]),
 ("S10_PCT_10STEP_DELAY",14,["10 iteration","pct","learning"]),
 ("S11_360_SEEDS_60_TRIALS",15,["360","60","transfer test"]),
 ("S12_EXTERNAL_WORLD_MAZE",16,["fig 4","nogo","maze"]),
 ("S13_DISTINCT_OTHER_CONDITIONING",17,["positive","negative","software"])
]
checks=[]
for ident,pg,markers in targets:
 t=re.sub(r"\s+"," ",pdf.pages[pg-1].extract_text() or "").lower()
 hits=[m for m in markers if m.lower() in t]
 checks.append({"id":ident,"one_based_original_pdf_page":pg,"expected_anchor":markers,"matched":hits,"pass":len(hits)==len(markers)})
 print("P09_POSTE_PAGE",pg,ident,"PASS",len(hits)==len(markers),"found",hits,flush=True)
 if len(hits)!=len(markers):raise AssertionError("P09_POSTE_ORIGINAL_SOURCE_ANCHOR_FAILED "+ident)
stages=[
 ("PRE_A","d8daabe86c03cf02c8a88fbe897b8b0b3c8f5615","P09_PRE_A_SOURCE_EDITION_VARIANT_LINEAGE_v1.json"),
 ("A","69c443902e59a5bb11882721ca0230919f370375","P09_PASS_A_SOURCE_FIRST_v1.json"),
 ("B","df633e25ee235cd34eca34f0b95ae32a63f16e21","P09_PASS_B_RESULT_INFORMED_FULL_A_v1.json"),
 ("C","ac58188798295f19f05bf55d27291e7788d65687","P09_PASS_C_SOURCE_CLOSED_C1_C2_v1.json"),
 ("D","8d11eabcf8bdf026284aeab5e38f1b8bbe24dc25","P09_PASS_D_UNCHANGED_GRAMMAR_v0_v1.json"),
 ("E","801aeb99e6fe0ea3319b557d17f481ad29810690","P09_PASS_E_ORIGINAL_SOURCE_FIDELITY_v1.json")
]
receipts={}; prev=None
for label,commit,name in stages:
 old=subprocess.check_output(["git","show",f"{commit}:{ROOT}{name}"],stderr=subprocess.STDOUT)
 now=(P/name).read_bytes()
 assert old==now,"FROZEN_P09_SCIENTIFIC_HISTORY_MUTATED "+label
 if prev:subprocess.run(["git","merge-base","--is-ancestor",prev,commit],check=True)
 prev=commit
 digest=hashlib.sha256(old).hexdigest()
 receipts[label]={"git_introduction_sha":commit,"raw_utf8_sha256":digest,"bytes":len(old),"file":ROOT+name}
 print("P09_FROZEN_STAGE",label,digest,flush=True)
A=json.loads((P/stages[1][2]).read_text())
B=json.loads((P/stages[2][2]).read_text())
C=json.loads((P/stages[3][2]).read_text())
D=json.loads((P/stages[4][2]).read_text())
E=json.loads((P/stages[5][2]).read_text())
assert A["original_claim_count"]==len(A["complete_A_source_claims"])==28
assert A["original_edge_count"]==len(A["complete_A_source_dependencies"])==36
assert B["inputs"]["full_original_A_object"]==A
assert len(B["entire_original_A_claim_by_claim_independent_reread"])==28
assert len(B["all_original_A_dependencies_reread"])==36
assert len(C["C1_actual_full_entire_original_A_reopened_before_ANY_patch"]["original_A_unchanged"]["complete_A_source_claims"])==28
assert len(C["C1_actual_full_entire_original_A_reopened_before_ANY_patch"]["original_A_unchanged"]["complete_A_source_dependencies"])==36
assert C["all_important_material_original_source_negatives_count_once"]
assert C["C2_unique_condition_count"]==13 and len(C["append_only_accepted_patches"])==3
assert len(D["complete_corrected_original_claim_mapping"])==28
assert len(D["all_original_source_dependencies"])==36
assert len(E["original_fidelity_targets"])==8
assert E["counts"]["unique_adverse_conditions_covered"]==13
assert E["H_discrimination"]=="NO_GENERAL_H0_H1_H2_RESULT"
assert E["source"]["all_21_pages_pictorially_reviewed"] is False
assert E["source"]["original_source_physical_verified_runs"]==[37178895352,37183422420,37183471486]
print("P09_POSTE_ALL_PASS 13/13 source page anchors, six immutable stage bytes and git ancestry, 28/36 source inventory and 13 negatives; historical RED 37183751964 harness wrong C JSON key fixed",flush=True)
project={"P09_original_published_pdf_sha256":sha,"frozen_stage_git_and_raw_sha256":receipts,"bounded_original_page_anchors":checks,"negative_count":13,"qualified_automatically":False,"no_MAIN":True}
enc=json.dumps(project,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
digest=hashlib.sha256(enc).hexdigest()
print("P09_POSTE_REPRODUCIBLE_PROJECTION_SHA256",digest,flush=True)
pathlib.Path("g1-p09-poste").mkdir(exist_ok=True)
pathlib.Path("g1-p09-poste/exact-raw-publisher-poste.json").write_text(json.dumps({"schema":"p399.g1.p09.post_E.reproducible_source_provenance.v1","runtime_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"original_final_publisher_url":final,"real_raw_sha256":sha,"real_pdf_bytes":len(raw),"real_pdf_pages":len(pdf.pages),"project":project,"digest":digest,"semantic_qualification_ci_proven":False,"numeric_replay_performed":False},indent=2)+"\n")
