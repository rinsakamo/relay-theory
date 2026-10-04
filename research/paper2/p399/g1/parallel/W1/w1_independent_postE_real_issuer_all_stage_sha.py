#!/usr/bin/env python3
"""W1 P08/P10 independent after-E official-original bytes + exact historical Git freeze.
Run one paper per distinct real GitHub Actions workflow. Structural/provenance ONLY.
"""
import hashlib,json,pathlib,sys,subprocess,time,zipfile,urllib.request,re
from io import BytesIO
from pypdf import PdfReader
PAPER=sys.argv[1] if len(sys.argv)>1 else ""
CONFIG={
"P08":{
 "stages":[
 ("PRE_A","74b6310d8af50f5e126ee50e01d1cf59834be65b","P08_PRE_A_CORRECTED_PUBLISHED_MAIN_SOURCE_BOUNDED_v1.json"),
 ("A","43db0f246ceeffbb5335e846bbd8bdd2185d516a","P08_PASS_A_CORRECTED_SOURCE_FIRST_FROZEN_v1.json"),
 ("B","2efac266c981e3d0e79fdd2c4fa599f738384bbb","P08_PASS_B_FULL_CORRECTED_A_ADVERSARIAL_FROZEN_v1.json"),
 ("C","db2e06d495273f7659e652cd4e1eeb99da636084","P08_PASS_C_FULL_CORRECTED_SOURCE_CLOSED_FROZEN_v1.json"),
 ("D","1c84b7b44e529839d171b8660dfce04562932eb5","P08_PASS_D_CORRECTED_UNCHANGED_GRAMMAR_v0_FROZEN_v1.json"),
 ("E","7eb5b2df6df90c186ae5140806752ac62d544f94","P08_PASS_E_CORRECTED_ORIGINAL_FIDELITY_FROZEN_v1.json")],
 "sources":[
 ("published_20pp_main","10.1371/journal.pcbi.1005418","printable","58ab19b12c6bf637329645f67889d11914a701e511744a784091d52958f1cd08",4199384,20,{0:["Sequential"],13:["model"]},True),
 ("scientific_3pp_correction","10.1371/journal.pcbi.1005908","printable","3df4dd0df0395fc14b2fb4a00e8f452db8abfeb42b4fa83fcfde36ed20528b5c",536685,3,{0:["Sequential"],1:["filtering","optimal"]},True),
 ("physically_verified_S1_not_semantically_certified","10.1371/journal.pcbi.1005418.s001","supplementary","59162cf3338a8677d58328d382ede402bf0fd0ff5dfa7e9b2f6bfd58c44b7372",4723646,None,{},True)]
},
"P10":{
 "stages":[
 ("PRE_A","339c7d87e04903148322e51a959c58d2b906d33a","P10_PRE_A_MAIN_FUNDING_CORRECTION_SUPPLEMENTS_v1.json"),
 ("A","f06a31987d9261e7a2c2682280c89136d7df4d5c","P10_PASS_A_ORIGINAL_SOURCE_FIRST_FROZEN_v1.json"),
 ("B","43c1ad0bc898a136e239b7ea836293c0149da771","P10_PASS_B_FULL_ORIGINAL_A_SOURCE_ADVERSARIAL_FROZEN_v1.json"),
 ("C","98e52fca82821d84f7fbf88cb264b62383023259","P10_PASS_C_SOURCE_CLOSED_FULL_A_NEGATIVE_FROZEN_v1.json"),
 ("D","c3bcec6fca2b463e64ed314e052aec72a42e79d2","P10_PASS_D_FROZEN_UNCHANGED_GRAMMAR_v0_v1.json"),
 ("E","dcfe66ff8c526ded46a262791d29c8bf6f1e35ee","P10_PASS_E_SOURCE_RELATIVE_FULL_MAIN_SUPPLEMENT_FIDELITY_FROZEN_v1.json")],
 "sources":[
 ("published_22pp_main","10.1371/journal.pcbi.1010699","printable","36839ae5557a296d73903089523328d75b5e0300fc3e6fca3be18d53a2c9c5d4",1543382,22,{14:["reward","Feature"],15:["Bayesian","hypothesis"],16:["switch","hypothesis"]},True),
 ("funding_only_1pp_correction","10.1371/journal.pcbi.1010775","printable","eb4c593d9c4c43e6f2dc33d80ed393bf9cc5b79f191d076afbfb5f9fc3771daa",202516,1,{0:["Funding"]},True),
 ("original_math_S1_Text","10.1371/journal.pcbi.1010699.s005","supplementary","fb5526948449edc4535550f6c0ca9faa31bc5920e36fa2a41812b1920dd6d2a5",155753,2,{0:["hypothesis"]},True),
 ("original_alternative_S4_Fig","10.1371/journal.pcbi.1010699.s004","supplementary","d427f7dedf601214a0f6acdd9c0f0be23d92023056e234e6d432006d9a26950e",146146,1,{},True)]
}}
if PAPER not in CONFIG:raise SystemExit("EXACT_PAPER_REQUIRED")
cfg=CONFIG[PAPER]
output=pathlib.Path("w1-"+PAPER.lower()+"-after-E")
output.mkdir(exist_ok=True)
ROOT="research/paper2/p399/g1/parallel/W1/"+PAPER.lower()+"/"
receipt={"paper":PAPER,"scope":"independent actual official publisher SHA/page + Git original chronological frozen stage receipt only","source_numeric_replay":False,"independent_blinded_human_semantic_review":False,"stages":[],"original_issuer_sources":[],"scope_dependent_complete":False}
def git(*args):return subprocess.check_output(["git",*args],stderr=subprocess.DEVNULL).decode().strip()
try:
    docs={}
    previous=None
    for stage,commit,name in cfg["stages"]:
        path=ROOT+name
        assert git("cat-file","-t",commit)=="commit","UNKNOWN_ORIGINAL_STAGE_COMMIT_"+stage
        assert subprocess.run(["git","merge-base","--is-ancestor",commit,"HEAD"]).returncode==0,"INTRO_COMMIT_NOT_HEAD_ANCESTOR_"+stage
        if previous:assert subprocess.run(["git","merge-base","--is-ancestor",previous,commit]).returncode==0,"STAGE_CHRONOLOGY_BROKEN_"+stage
        parent=git("rev-parse",commit+"^")
        assert subprocess.run(["git","cat-file","-e",parent+":"+path],capture_output=True).returncode!=0,"ORIGINAL_INTRO_FILE_EXISTED_IN_PARENT_"+stage
        blob=git("rev-parse",commit+":"+path)
        assert blob==git("rev-parse","HEAD:"+path),"ORIGINAL_STAGE_FILE_MUTATED_"+stage
        raw=pathlib.Path(path).read_bytes()
        assert blob==git("hash-object",path),"WORKTREE_UNFROZEN_"+stage
        docs[stage]=json.loads(raw)
        receipt["stages"].append({"stage":stage,"actual_introduction_commit":commit,"first_git_blob":blob,"raw_utf8_sha256":hashlib.sha256(raw).hexdigest(),"unchanged_on_head":True})
        previous=commit
    A,B,C,D,E=(docs[x] for x in ["A","B","C","D","E"])
    aa=A["source_first_claims"] if PAPER=="P08" else A["original_source_first_claims"]
    cc=C["C2_full_negative_register"] if PAPER=="P08" else C["C2_original_full_unfavorable_conditions"]
    ae=B["exact_complete_immutable_A_reopened"] if PAPER=="P08" else B["exact_entire_immutable_A_input"]
    cr=C["full_frozen_original_A_reopened_BEFORE_any_corrections"] if PAPER=="P08" else C["complete_original_frozen_A_reopened_before_any_patch"]
    assert A==ae==cr,"ORIGINAL_A_NOT_EXACT_FULL_IN_B_C"
    assert len(aa)==28 if PAPER=="P08" else len(aa)==27,"A_COUNT_INCONSISTENT"
    assert len(cc)==17 if PAPER=="P08" else len(cc)==18,"NEGATIVE_C2_COUNT_DRIFT"
    claims={x["id"] for x in aa}
    negative={x["id"] for x in cc}
    evidence=E["fidelity_groups"] if PAPER=="P08" else E["fidelity_targets"]
    ec={v for z in evidence for v in (z["covered_original_A_ids"] if PAPER=="P08" else z["all_original_A_claim_ids"])}
    en={v for z in evidence for v in (z["covered_original_C_negative_ids"] if PAPER=="P08" else z["material_original_C2_negative_ids"])}
    assert claims<=ec and negative<=en,"E_COVERAGE_INCOMPLETE"
    if PAPER=="P08":
        assert len(D["per_original_A_claim_v0_roles"])==28 and len(D["all_frozen_original_A_dependencies"])==40,"D_GRAMMAR_COVERAGE_MISMATCH"
    else:
        assert len(D["exact_source_claim_roles"])==27 and len(D["original_dependencies_roles"])==43,"D_GRAMMAR_COVERAGE_MISMATCH"
    receipt["git_provenance_outcome"]="SUCCESS_EXACT_SIX_ORIGINAL_STAGE_INTRODUCTION_BYTES_AND_ORDER"
except Exception as e:
    receipt["git_provenance_outcome"]="FAIL"
    receipt["git_blocker"]=repr(e)
    (output/"real_after_E_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt),flush=True)
    raise
for name,doi,typ,sha,size,pages,anchors,required in cfg["sources"]:
    url="https://journals.plos.org/ploscompbiol/article/file?id="+doi+"&type="+typ
    r={"name":name,"doi":doi,"url":url,"required":required,"success":False,"http_errors":[]}
    for attempt in range(1,5):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"RelayTheory-W1-original-science-source-qualification/1.0"})
            raw=urllib.request.urlopen(req,timeout=90).read()
            assert hashlib.sha256(raw).hexdigest()==sha,"NOT_IDENTICAL_ORIGINAL_SOURCE_RAW_SHA"
            assert len(raw)==size,"ORIGINAL_BYTES_CHANGED"
            r.update({"raw_sha256":sha,"bytes":len(raw)})
            if pages:
                assert raw.startswith(b"%PDF"),"NOT_PUBLISHED_PDF"
                pdf=PdfReader(BytesIO(raw))
                assert len(pdf.pages)==pages,"ORIGINAL_PUBLISHER_PAGE_COUNT_DIFFERS"
                r["pages"]=len(pdf.pages)
                r["anchors"]=[]
                for i,terms in anchors.items():
                    t=pdf.pages[i].extract_text() or ""
                    hits=[term for term in terms if term.lower() in t.lower()]
                    assert hits,"SOURCE_PAGE_ANCHOR_MISSING_PAGE_"+str(i+1)
                    r["anchors"].append({"page_1based":i+1,"matched_terms":hits,"bounded_text_only":True})
            else:
                assert raw.startswith(b"PK"),"NOT_ORIGINAL_DOCX"
                with zipfile.ZipFile(BytesIO(raw)) as z:
                    assert "word/document.xml" in z.namelist(),"OFFICIAL_S1_DOCX_INCOMPLETE"
                r["supplement_content_scope"]="DOCX_FORMAT_CHECK_ONLY_NO_EXACT_TABLE_SEMANTIC_QUALIFICATION"
            r["success"]=True
            break
        except Exception as exc:
            r["http_errors"].append({"attempt":attempt,"reason":repr(exc)})
            if attempt<4:time.sleep(attempt*2)
    receipt["original_issuer_sources"].append(r)
    print(json.dumps(r),flush=True)
receipt["source_provenance_outcome"]="SUCCESS" if all(x["success"] for x in receipt["original_issuer_sources"] if x["required"]) else "FAIL_CANNOT_ISSUE_SCIENTIFIC_QUALIFICATION"
receipt["scope_dependent_complete"]=receipt["git_provenance_outcome"].startswith("SUCCESS") and receipt["source_provenance_outcome"]=="SUCCESS"
receipt["conclusion"]="AFTER_E_BOUNDED_PHYSICAL_AND_CHRONOLOGY_PASS_NOT_INDEPENDENT_SEMANTIC" if receipt["scope_dependent_complete"] else "AFTER_E_NO_PASS_OFFICIAL_SOURCE_OR_HISTORICAL_GIT_BLOCK"
(output/"real_after_E_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"paper":PAPER,"outcome":receipt["conclusion"],"git":receipt["git_provenance_outcome"],"source":receipt["source_provenance_outcome"]}),flush=True)
if not receipt["scope_dependent_complete"]:sys.exit(1)
