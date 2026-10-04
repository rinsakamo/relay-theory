#!/usr/bin/env python3
"""W1 P06 independent AFTER-E official publisher source and frozen Git stage bytes audit.
This checks source/procedural integrity, NOT blind semantic assessment/numerical reproduction.
"""
import hashlib, json, pathlib, subprocess, sys, urllib.request
from io import BytesIO
from pypdf import PdfReader

D = pathlib.Path("w1-p06-after-E")
D.mkdir(exist_ok=True)
ROOT = "research/paper2/p399/g1/parallel/W1/p06/"
SHA = "50a8e9fb16bbb00eab02a934a629fe43a7142456206df7b6e5331d33c561da15"
STAGES = [
("PRE_A","e9677b5a44e40996bf4dcc9c8a93f3ec98ac1d4d","P06_PRE_A_ORIGINAL_PUBLISHED_SOURCE_FREEZE_v1.json"),
("A","13f46bfe82c9c06729904dcd7f6a583a1d9ae0de","P06_PASS_A_SOURCE_FIRST_FROZEN_v1.json"),
("B","dd68116bc75f735182edf9faac1aa2bb47ff881e","P06_PASS_B_FULL_A_ORIGINAL_ADVERSARIAL_FROZEN_v1.json"),
("C","ea0060dd6898314dfa04a9d4d1c637221705f987","P06_PASS_C_SOURCE_CLOSED_FROZEN_v1.json"),
("D","f1bbb464315bf50b2075a1857501e37980f2c5e3","P06_PASS_D_ORIGINAL_STRUCTURE_UNCHANGED_GRAMMAR_v0_v1.json"),
("E","2c57e8a4b09e0ec26e534d208058c475add89586","P06_PASS_E_SOURCE_RELATIVE_FIDELITY_FROZEN_v1.json"),
]
def git(*xs):
    return subprocess.check_output(["git",*xs]).decode().strip()
def check(cond, message):
    if not cond: raise RuntimeError(message)
r={"scope":"AFTER E independent exact primary issuer raw PDF and original chronological frozen stages, no numeric replay","source":{},"stages":[],"scientific_qualification_implied":False}
try:
    url="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1004375&type=printable"
    req=urllib.request.Request(url,headers={"User-Agent":"RelayTheory-W1-original-science-source-qualification/1.0"})
    raw=None
    source_http_failures=[]
    for attempt in range(1,5):
        try:
            raw=urllib.request.urlopen(req, timeout=85).read()
            if not raw.startswith(b"%PDF"): raise ValueError("NOT_ORIGINAL_PDF")
            break
        except Exception as e:
            source_http_failures.append({"attempt":attempt,"error":repr(e)})
            if attempt<4:
                import time
                time.sleep(attempt*3)
    check(raw is not None,"REPEATED_PUBLISHER_HTTP_UNAVAILABLE_"+repr(source_http_failures))
    r["source_prior_http_attempts"]=source_http_failures
    reader=PdfReader(BytesIO(raw))
    r["source"]={"url":url,"raw_sha256":hashlib.sha256(raw).hexdigest(),"raw_bytes":len(raw),"pages":len(reader.pages),"publisher_pdf_signature":raw[:4].decode(errors="replace")}
    check(r["source"]["raw_sha256"]==SHA,"RAW_PUBLISHED_SHA_MISMATCH")
    check(len(raw)==6901523 and len(reader.pages)==39,"RAW_PUBLISHED_LENGTH_OR_PAGES_MISMATCH")
    # Anchors derived from actual original PDF page text, used only as bounded page pointers.
    probes={0:["Saliency","Zhaoping"],5:["reaction","salien"],10:["salien"]}
    for ix,terms in probes.items():
        t=reader.pages[ix].extract_text() or ""
        h={z:z.lower() in t.lower() for z in terms}
        check(any(h.values()),f"ZERO_TERMS_ON_ORIGINAL_PAGE_{ix+1}")
        r["source"].setdefault("source_page_anchors",[]).append({"one_based_page":ix+1,"terms":h})
    previous=None
    doc={}
    for label,commit,name in STAGES:
        path=ROOT+name
        check(git("cat-file","-t",commit)=="commit","UNKNOWN_STAGE_COMMIT_"+label)
        if previous: subprocess.run(["git","merge-base","--is-ancestor",previous,commit],check=True)
        head=git("rev-parse","HEAD")
        subprocess.run(["git","merge-base","--is-ancestor",commit,head],check=True)
        parent=git("rev-parse",commit+"^")
        old=subprocess.run(["git","cat-file","-e",parent+":"+path],capture_output=True)
        check(old.returncode!=0,"STAGE_FILE_ALREADY_IN_PARENT_"+label)
        introduced=git("rev-parse",commit+":"+path)
        athead=git("rev-parse","HEAD:"+path)
        check(introduced==athead,"STAGE_FILE_MUTATED_AFTER_FREEZE_"+label)
        checked=pathlib.Path(path).read_bytes()
        check(git("hash-object",path)==introduced,"CHECKED_WORKTREE_DIFFERS_"+label)
        doc[label]=json.loads(checked)
        r["stages"].append({"stage":label,"first_git_introduction":commit,"git_blob":introduced,"raw_utf8_sha256":hashlib.sha256(checked).hexdigest(),"immutable_through_HEAD":True})
        previous=commit
    A,B,C,E=(doc[x] for x in ["A","B","C","E"])
    check(A["count_claims"]==28 and A["count_dependencies"]==40,"A_COUNT_DRIFT")
    check(B["entire_exact_immutable_A_original_input"]==A,"B_LOST_ORIGINAL_FROZEN_A")
    check(C["C1_original_full_A_reopened_before_patch"]==A,"C_DID_NOT_REOPEN_COMPLETE_A")
    check(C["C1_confirm_exact_B_embedded_original_A"],"C_B_NOT_FROZEN_A")
    check(len(C["C2_all_material_source_negative_conditions"])==18,"C_NEGATIVE_MISSING")
    cids={x["condition_id"] for x in C["C2_all_material_source_negative_conditions"]}
    eids={v for t in E["fidelity_targets"] for v in t["covered_C_condition_ids"]}
    aids={v for t in E["fidelity_targets"] for v in t["covered_original_A_claim_ids"]}
    check(cids<=eids and {x["id"] for x in A["source_first_claims"]}<=aids,"SOURCE_FIDELITY_COVERAGE_INCOMPLETE")
    check(len(doc["D"]["source_claim_role_mapping"])==28 and len(doc["D"]["all_original_source_dependencies"])==40,"D_CLAIM_DEPENDENCY_DRIFT")
    check(not E["qualification_granted_by_E_alone"],"E_FALSE_PREMATURE_QUALIFICATION")
    r.update({"stage_ancestry_pass":True,"source_page_anchor_count":len(probes),"full39_visually_reread_by_runner":False,"fidelity_source_replay_numerical":False,"status":"SOURCE_AND_IMMUTABLE_STAGE_INTEGRITY_SUCCESS_NOT_HUMAN_SEMANTIC_SCIENCE_CERT"})
except Exception as exc:
    r.update({"status":"FAIL","error":repr(exc)})
(D/"source_and_stage_receipt.json").write_text(json.dumps(r,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(r,ensure_ascii=False))
if r["status"]=="FAIL":sys.exit(1)
