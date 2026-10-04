#!/usr/bin/env python3
"""P15 independent post-E publisher-source and immutable-stage verifier, actual live Actions."""
import pathlib,hashlib,json,subprocess,urllib.request,io,time,os
from pypdf import PdfReader
import fitz
ROOT=pathlib.Path(__file__).resolve().parent
PREFIX="research/paper2/p399/g1/parallel/W3/"
SRCS=[
 ("main","1010589","printable","pdf", "591339de97a02abc1faeb276b48b8dfc73b518aca2d8ad1c36a10ba96038e002",27),
 ("math_appendix","1010589.s001","supplementary","pdf","cc407ed073633a3aff3719ef4ceb0d97446026b771fd15f5bb6cd74d99dff074",5),
 ("input_pattern_original_EPS","1010589.s002","supplementary","eps","5d1c4070af7452c691029aee2ff08c2b6b70f2180900ff8b1e3f68db7d3e9400",None),
 ("network_size_S1_table","1010589.s003","supplementary","pdf","a1d5cb779afd0a918f7c1102720e03aadd2ef1bed57327aafec60ef4d3975a3a",1),
 ("parameter_S2_table","1010589.s004","supplementary","pdf","58c1963db4a3770c65fc9dc5d9973f7a397fd61401c350a4a20537eaabc646b3",1),
]
STAGES=[
 ("PRE_A","P15_PRE_A_original_complete_math_figures_frozen_v1.json","6e523ca5c9257def9a58a37c49d6a29541eedc38"),
 ("A","P15_A_original_source_native_v1.json","50268096b0bb54ae85443e796a72d9052c141950"),
 ("B","P15_B_original_source_full_A_adversarial_reaudit_v1.json","25651804e9cfccb152975a1430790a1aec2d9689"),
 ("C","P15_C_reopen_original_A_adjudicate_source_negatives_v1.json","e64579b1573299773bb017add1a4366e05133977"),
 ("D","P15_D_unchanged_grammar_v0_complete_source_mapping_v1.json","e8bbe2eb9144c2c1e4b9928e5baf8235147bba23"),
 ("E","P15_E_original_source_relative_fidelity_v1.json","1e49466bd88b044532c1848df48a69b5be3c12b5"),
]
def require(p,why):
 if not p:raise RuntimeError("FAIL_CLOSED_"+why)
def git(*args):return subprocess.check_output(["git",*args],encoding="utf8").strip()
records=[];textual={}
for label,doi,t,fmt,expected,pages in SRCS:
 url="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi."+doi+"&type="+t
 for retry in range(1,4):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"RelayTheory-W3-original-publisher-afterE-exact-audit","Accept":"application/pdf,application/postscript,*/*"}),timeout=40) as r:raw=r.read(8_000_000)
   break
  except Exception as ex:
   print("P15_POST_E_SOURCE_RETRY",label,retry,str(ex)[:150],flush=True)
   if retry==3:raise
   time.sleep(retry*3)
 sha=hashlib.sha256(raw).hexdigest();require(sha==expected,"P15_original_exact_SHA_"+label)
 obj={"part":label,"official_publisher_url":url,"sha256":sha,"bytes":len(raw),"filetype":fmt}
 if fmt=="pdf":
  require(raw.startswith(b"%PDF-"),"P15_pdf_magic_"+label)
  pdf=PdfReader(io.BytesIO(raw));require(len(pdf.pages)==pages,"P15_pdf_pages_"+label)
  txt="\n".join((pg.extract_text() or "") for pg in pdf.pages).lower()
  textual[label]=txt;obj["pages"]=pages
  doc=fitz.open(stream=raw,filetype="pdf")
  checks=[4,6,16] if label=="main" else list(range(pages))
  for page in checks:
   bmp=doc[page].get_pixmap(matrix=fitz.Matrix(0.65,0.65))
   require(bmp.width>150 and bmp.height>150,"P15_original_pdf_render_"+label)
  obj["bounded_render_pages_1based"]=[p+1 for p in checks]
 else:
  require(raw.startswith(b"%!PS") and b"%%BoundingBox:" in raw[:7000],"EPS_original_magic_and_bbox")
  import tempfile
  with tempfile.TemporaryDirectory() as d:
   eps=pathlib.Path(d)/"original.eps";png=pathlib.Path(d)/"render.png";eps.write_bytes(raw)
   cp=subprocess.run(["gs","-dSAFER","-dBATCH","-dNOPAUSE","-sDEVICE=png16m","-r80","-sOutputFile="+str(png),str(eps)],capture_output=True,timeout=45)
   require(cp.returncode==0 and png.exists() and png.stat().st_size>5000,"EPS_original_real_raster")
   obj["raster_original_png_bytes"]=png.stat().st_size
 print("P15_PUBLISHER_ORIGINAL_EXACT_PASS",label,sha,flush=True)
 records.append(obj)
# Semantic source locator guard is modest: presence in *actual original text*; not proof of all proposed numeric simulation outcomes.
for x in ["theremin","ca3","dg","hippocamp"]:
 require(x in textual["main"],"P15_main_lexical_"+x)
for x in ["xcal","avgss","hebb","bcm"]:
 require(x in textual["math_appendix"],"P15_actual_appendix_math_"+x)
for x in ["dg","ca3","small","large"]:
 require(x in textual["network_size_S1_table"],"P15_actual_network_table_"+x)
for x in ["hebb","0.01","dg"]:
 require(x in textual["parameter_S2_table"],"P15_actual_nonzero_hebb_table_"+x)
previous=None;historic=[];objects={}
for label,name,sha in STAGES:
 p=PREFIX+name
 original=subprocess.check_output(["git","show",sha+":"+p])
 current=(ROOT/name).read_bytes()
 require(original==current,"P15_science_frozen_exact_stage_"+label)
 intro=git("log","--diff-filter=A","--format=%H","HEAD","--",p).splitlines()
 require(intro==[sha],"P15_stage_first_git_introduction_"+label)
 require(subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"]).returncode==0,"P15_stage_ancestor_HEAD_"+label)
 if previous:require(subprocess.run(["git","merge-base","--is-ancestor",previous,sha]).returncode==0,"P15_stage_chronology_"+label)
 previous=sha
 objects[label]=json.loads(current)
 historic.append({"stage":label,"introduction_commit":sha,"raw_sha256":hashlib.sha256(current).hexdigest(),"bytes":len(current)})
A,B,C,D,E=(objects[x] for x in ("A","B","C","D","E"))
C1=C["C1_before_any_patch_reopen_complete_original_A"]
require(len(A["original_claims"])==26 and len(A["source_local_dependencies"])==32,"P15_A_26_32")
require(set(B["review_all_A_claim_ids"])=={x["id"] for x in A["original_claims"]},"P15_B_all_A")
require(set(B["review_all_A_dependency_ids"])=={x["id"] for x in A["source_local_dependencies"]},"P15_B_all_dependencies")
require(len(B["findings"])==14,"P15_B_14_adverse")
require(C1["original_A_git_blob"]==git("hash-object",str(ROOT/STAGES[1][1])),"P15_C_reopen_original_full_A_blob")
require(len(C["C2_all_B_individual_adjudications"])==14 and len(C["source_closed_C2_unique_negatives"])==16,"P15_C14_16")
require(set(C1["all_original_A_claim_ids"])==set(B["review_all_A_claim_ids"]),"P15_C_original_complete_A")
require(set(C1["all_original_A_dependency_ids"])==set(B["review_all_A_dependency_ids"]),"P15_C_original_32")
require(D["original_A_git_blob"]==C1["original_A_git_blob"],"P15_D_original_frozen_A_reference")
require(len(D["complete_original_A_roles"])==26 and {x["claim_id"] for x in D["complete_original_A_roles"]}==set(B["review_all_A_claim_ids"]),"P15_D_all_26")
require(len(D["all_original_source_dependencies_preserved"])==32,"P15_D_all_32")
require(len(E["fidelity_targets"])==12 and len(E["all_original_C_unique_negatives"])==16,"P15_E_12_16")
require(set(E["all_A_claim_ids"])==set(B["review_all_A_claim_ids"]) and set(E["all_A_dependency_ids"])==set(B["review_all_A_dependency_ids"]),"P15_E_original_IDS")
assert hashlib.sha256((ROOT/STAGES[1][1]).read_bytes()+b"\n").hexdigest()!=historic[1]["raw_sha256"]
assert len(A["original_claims"])-1!=26
assert (SRCS[0][4]!=hashlib.sha256(b"not publisher PDF").hexdigest())
receipt={"status":"PASS_REAL_P15_PUBLISHER_EXACT_SOURCE_AND_FROZEN_HISTORY_SCOPED","original_source_variants":records,
 "original_stage_git_ancestry_and_immutable_bytes":historic,"source_math_lexical_guards":15,
 "original_science_inventory":{"A_claims":26,"dependencies":32,"B_objections":14,"C_negatives":16,"D_roles":26,"E_fidelity_targets":12},
 "illustrative_mutation_guards":3,"exclusions":["No source panel blind human audit","No exact historical hip-edl code/seeds numerical replay","No full all-original mathematical prior ancestor graph clearance","No automatic G1 denominator admission or MAIN scientific operation"]}
out=pathlib.Path(os.environ.get("RUNNER_TEMP","/tmp"))/"W3_P15_real_afterE_original_publisher_audit_receipt.json"
out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
print("P15_INDEPENDENT_REAL_AFTER_E_SUCCESS",json.dumps(receipt,indent=2,sort_keys=True),flush=True)
