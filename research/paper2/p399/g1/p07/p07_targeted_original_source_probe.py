#!/usr/bin/env python3
"""P07 targeted pre-A original-source exact byte/page/negative evidence verification.

Actual source-only mechanical CI. This neither reconstructs/validates the original
scientific interpretation nor performs exact numeric reanalysis.
Reacquisition is specifically justified to bind the separately completed full
14-page visual inspection to prior G1 physically obtained source SHA before A.
"""
import hashlib,io,json,re,urllib.request,datetime
from pypdf import PdfReader
from pathlib import Path
url="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1000254&type=printable"
expected="2b6cb16c821e937f712586ef52ac8edb895bf4f019d2c86b181aae805eb31959"
req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (RelayTheory scientific original pre-A P07)"})
with urllib.request.urlopen(req,timeout=120) as f: raw=f.read();final=f.geturl()
if not raw.startswith(b"%PDF-"):raise RuntimeError("Non original PDF response")
sha=hashlib.sha256(raw).hexdigest()
if sha!=expected:raise RuntimeError("PRE_A FAIL_CLOSED original publisher PDF checksum mismatch "+sha)
if len(raw)!=613841:raise RuntimeError("PRE_A FAIL_CLOSED original publisher PDF size changed")
reader=PdfReader(io.BytesIO(raw),strict=False)
if len(reader.pages)!=14:raise RuntimeError("PRE_A FAIL_CLOSED original publisher original page count changed")
tests=[
 ("ORIGINAL_ID",0,["Game Theory of Mind","Yoshida","Dolan","Friston"]),
 ("VALUE_FUNCTION_AND_POLICY",1,["Policies and Value Functions","Todorov","Bellman"]),
 ("STATE_SPACE_STAG",2,["A Toy Example","one-dimensional","uncontrolled"]),
 ("JOINT_RECURSION",3,["Sequential Games","Stag-Hunt","Inferring an Agent"]),
 ("VISUAL_MODEL_CONTRAST",4,["Figure 2","Stag-hunt","equilibrium"]),
 ("FIXED_STRATEGY_LIKELIHOOD",5,["Bounded Rationality","strategy"]),
 ("ADAPTIVE_STRATEGY_AND_INFERENCE",6,["Representing the Goals","Inferring Theory of Mind"]),
 ("SIMULATED_VS_EMPIRICAL",7,["Figure 5","Results","Theory of Mind"]),
 ("ACTUAL_TASK_AND_PROCEDURE",8,["Experimental Procedures","computer"]),
 ("THREE_AGENT_GENERALIZATION",9,["Modelling Strategy","three"]),
 ("HUMAN_TO_M_COMPARISON",10,["Figure 8","Discussion"]),
 ("NON_EQUIVALENCE_OF_MECHANISM",11,["Prosocial Utility","Bellman"]),
 ("EQUILIBRIUM_NEGATIVE_CONTROL",12,["prosocial","equilibrium","pure"]),
 ("REFERENCES_NOT_STANDALONE_SUPPLEMENTS",13,["References","Supporting Information"])
]
receipts=[]
for ident,idx,needles in tests:
 text=reader.pages[idx].extract_text() or ""
 normalized=re.sub(r"\s+"," ",text).lower()
 found=[q for q in needles if q.lower() in normalized]
 receipts.append({"id":ident,"page_index":idx,"paper_page":idx+1,
  "expected_text_markers":needles,"actual_found":found,
  "all_markers":len(found)==len(needles),
  "text_length":len(text)})
for x in receipts:
 print("P07_SOURCE_ANCHOR",x["paper_page"],x["id"],"FOUND",x["actual_found"],"FULL",x["all_markers"])
# Technical fail-closed for a bounded subset of essential identity/core/negative
required={"ORIGINAL_ID","VALUE_FUNCTION_AND_POLICY","SIMULATED_VS_EMPIRICAL","HUMAN_TO_M_COMPARISON","EQUILIBRIUM_NEGATIVE_CONTROL"}
for x in receipts:
 if x["id"] in required and not x["all_markers"]:
  raise RuntimeError("P07 essential source page anchor mismatch: "+x["id"]+" "+str(x["actual_found"]))
packet={"schema":"p399.g1.p07.original-publisher-pdf.pre-a.exact-byte-identity-page-anchors.v1",
 "timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"original_pdf_url":url,
 "actual_final_url":final,"expected_original_sha256":expected,"actual_original_sha256":sha,
 "original_bytes":len(raw),"original_pages":len(reader.pages),
 "page_specific_text_anchor_receipts":receipts,
 "original_visual_review":"SEPARATE_HUMAN_AI_VISUAL_INSPECTION_OF_ALL_PDF_PAGES_IN_G1_LANE_NOT_THIS_SCRIPT",
 "original_decisive_source_interpretation_certified_by_ci":False,
 "original_numeric_model_replay":False}
Path("g1-p07").mkdir(exist_ok=True)
Path("g1-p07/source-pre-a-check.json").write_text(json.dumps(packet,indent=2)+"\n")
print("P07_SOURCE_SHA",sha,"PAGES",len(reader.pages),"BYTES",len(raw))
print("P07_PRE_A_PHYSICAL_RECEIPT_ONLY_PASS semantic qualification NOT_PROVEN")
