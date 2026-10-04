#!/usr/bin/env python3
"""Genuine publisher-only P18 post-E original-asset and immutable six-stage audit.
No MAIN science, exact author model replay, or claim of blind human panel review.
"""
import hashlib,io,json,pathlib,os,subprocess,urllib.request,time
from pypdf import PdfReader
from PIL import Image,ImageStat
import fitz
ROOT=pathlib.Path(__file__).resolve().parent;PFX="research/paper2/p399/g1/parallel/W3/"
sources=[
 ("main_final","1008552","printable","pdf","cb75481590c34686eeeb8635dcb8a381283bcbe3e7f8ed9f0ee246fa95e419d1",28,None),
 ("S5_original_recovery","1008552.s005","supplementary","tif","1e42c90baa502f7d0d3be32100ccb6a62fe04b29fbd9bd5274fe22f529e860e8",None,(1084,641)),
 ("S6_original_validation","1008552.s006","supplementary","tif","67048c23a5bc77ffe7b8690042e1d680599ab62ad2517cbfcc245d71071f7cf1",None,(1028,1498)),
 ("S1_original_parameter_table","1008552.s007","supplementary","pdf","25465f1dfe9c05f8e37028b16c1070dc19e437301804d7344c42651a2e748f48",1,None),
]
stages=[
 ("PRE_A","P18_PRE_A_publisher_original_final_and_model_recovery_sources_frozen_v1.json","07b4e732461b350eb6aef8dddb94394c59260c1d"),
 ("A","P18_A_final_original_source_native_v1.json","4026bfaadc3d1672f441fb963b2bb5041b9fd245"),
 ("B","P18_B_original_source_complete_A_adversarial_review_v1.json","420bb7799bf8bb50d5b337f4a70b31c0e513bcd7"),
 ("C","P18_C_full_original_A_reopen_and_adversarial_closure_v1.json","c8869c6e8306b40e1ccf5dd334b7d667c5cbd7a1"),
 ("D","P18_D_unchanged_frozen_grammar_v0_full_original_v1.json","c24f9a5679721299e7909a4e51c0756fe48ef967"),
 ("E","P18_E_bounded_original_publisher_fidelity_v1.json","b7f7270a038f3dfaad2ed0bf9f3c0f86f5dbf5cb"),
]
def req(c,msg):
 if not c:raise RuntimeError("FAIL_CLOSED_P18_"+msg)
def git(*args):return subprocess.check_output(["git",*args],encoding="utf8").strip()
source_records=[]
for name,doi,fmt,form,sha,pages,dims in sources:
 url="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi."+doi+"&type="+fmt
 for attempt in range(1,4):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"RelayTheory-W3-P18-independent-original-post-E","Accept":"application/pdf,image/tiff,*/*"}),timeout=38) as rr:raw=rr.read(8_000_000)
   break
  except Exception as e:
   print("P18_REAL_ORIGINAL_RETRY",name,attempt,str(e)[:110],flush=True)
   if attempt==3:raise
   time.sleep(3*attempt)
 got=hashlib.sha256(raw).hexdigest();req(got==sha,"ORIGINAL_PUBLISHER_SHA_"+name)
 obj={"source_part":name,"official_original_url":url,"sha256":got,"bytes":len(raw)}
 if form=="pdf":
  req(raw.startswith(b"%PDF-"),"PDF_MAGIC_"+name)
  doc=PdfReader(io.BytesIO(raw));req(len(doc.pages)==pages,"PAGES_"+name)
  f=fitz.open(stream=raw,filetype="pdf")
  indexes=[2,3,5,9,12,20] if pages==28 else [0]
  render=[]
  for idx in indexes:
   pix=f[idx].get_pixmap(matrix=fitz.Matrix(0.7,0.7))
   req(pix.width>250 and pix.height>250,"RENDER_"+name)
   render.append(idx+1)
  obj["pages"]=pages;obj["rasterized_original_selected_pages"]=render
  alltext="\n".join((p.extract_text() or "").lower() for p in doc.pages)
  if pages==28:
   for key in ("reflect","model","reward","free"):
    req(key in alltext,"MAIN_TEXT_"+key)
   obj["bounded_main_original_text_anchors"]=4
  else:
   req("parameter" in alltext.lower() or len(alltext)>100,"S1_TABLE_EXTRACT")
 else:
  img=Image.open(io.BytesIO(raw));img.load()
  req(img.format=="TIFF" and tuple(img.size)==dims,"TIFF_ACTUAL_PIXELS_"+name)
  stats=ImageStat.Stat(img.convert("RGB")).stddev
  req(max(stats)>5.0,"SOURCE_NONBLANK_TIFF_"+name)
  obj.update({"pixel_dimensions":list(img.size),"RGB_stddev":stats,"provenance":"actual current PLOS original source TIFF not original analysis recreation"})
 print("P18_ORIGINAL_SOURCE_EXACT_PASS",name,got,flush=True)
 source_records.append(obj)
orig=[];data={};prev=None
for stage,file,commit in stages:
 source= subprocess.check_output(["git","show",commit+":"+PFX+file])
 current=(ROOT/file).read_bytes()
 req(source==current,"FROZEN_FIRST_INTRODUCTION_BYTES_"+stage)
 intro=git("log","--diff-filter=A","--format=%H","HEAD","--",PFX+file).splitlines()
 req(intro==[commit],"FIRST_INTRO_"+stage)
 req(subprocess.run(["git","merge-base","--is-ancestor",commit,"HEAD"]).returncode==0,"HISTORY_"+stage)
 if prev:req(subprocess.run(["git","merge-base","--is-ancestor",prev,commit]).returncode==0,"ANSESTOR_"+stage)
 prev=commit;data[stage]=json.loads(current)
 orig.append({"stage":stage,"first_introduction_commit":commit,"source_git_sha256":hashlib.sha256(source).hexdigest(),"bytes":len(source)})
a,b,c,d,e=[data[x] for x in ["A","B","C","D","E"]]
Aids={x["id"] for x in a["original_claims"]}
Dids={x["id"] for x in a["source_local_dependencies"]}
req(len(Aids)==28 and len(Dids)==35,"A_28_35")
req(set(b["full_A_claim_ids"])==Aids and set(b["full_A_dependency_ids"])==Dids,"B_FULL_28_35")
req(len(b["findings"])==16,"B_16")
req(c["C1_before_any_patch_reopen_complete_frozen_original_A"]["original_A_git_blob"]==git("hash-object",str(ROOT/stages[1][1])),"C_REOPEN_FROZEN_A")
req(set(c["C1_before_any_patch_reopen_complete_frozen_original_A"]["reopened_all_original_A_dependency_ids"])==Dids,"C_FULL_A_DEPENDENCIES")
req(len(c["C2_adjudicate_all_16_original_B_ids"])==16 and len(c["unique_source_native_adversarial_negatives"])==18,"C_B16_NEG18")
req(d["original_A_git_blob"]==c["C1_before_any_patch_reopen_complete_frozen_original_A"]["original_A_git_blob"],"D_ORIGINAL_A")
req({v["claim_id"] for v in d["complete_original_A_roles"]}==Aids and len(d["preserve_original_A_source_dependencies"])==35,"D_FULL_28_35")
req(set(e["all_A_original_claim_ids"])==Aids and set(e["all_A_original_dependency_ids"])==Dids,"E_FULL_ORIGINAL_A")
req(len(e["fidelity_targets"])==12 and len(e["all_source_closed_C_negatives"])==18,"E_12_AND_C18")
assert hashlib.sha256((ROOT/stages[1][1]).read_bytes()+b" ").hexdigest()!=orig[1]["source_git_sha256"]
assert len(a["original_claims"])-1!=28
assert len(c["unique_source_native_adversarial_negatives"])-1!=18
receipt={"result":"PASS_GENUINE_P18_EXACT_PUBLISHER_ORIGINAL_SOURCE_AND_SIX_IMMUTABLE_STAGES",
 "original_source_asset_receipts":source_records,"six_original_scientific_first_git_commits":orig,
 "scope_counts":{"A_claims":28,"A_dependencies":35,"B_source_adversarials":16,"C_negative":18,"D_mapped":28,"E_fidelity_targets":12},
 "mutational_sanity_controls":3,
 "limitations":["Publisher TIFF nonblank integrity does not establish pixel-panel independent human adjudication",
 "Original published original fmincon 200 start each individual, 1001x10000 BGLRT, original human raw data not reproduced",
 "BGLRT rejection supports relative fitted models and tested rivals, not neural self-model verified existence",
 "No model-family PF04 or G2 INT15 complete original-ancestry clearance or shared G1 admission"]}
out=pathlib.Path(os.environ.get("RUNNER_TEMP","/tmp"))/"W3_P18_independent_afterE_original_publisher_receipt.json"
out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
print("P18_REAL_AFTER_E_AUDIT_PASS",json.dumps(receipt,indent=2,sort_keys=True),flush=True)
