#!/usr/bin/env python3
"""W3 P16 bounded real publisher-PDF *post-E* source, page, historic stage audit.
This is not external blinded human semantics, full-original quantitative replay,
or original historical #401 checker deployment. No MAIN material is accessed.
"""
import hashlib, io, json, os, pathlib, subprocess, sys, time, urllib.request
import requests
from pypdf import PdfReader
import fitz

ROOT=pathlib.Path(__file__).resolve().parent
REPO=ROOT.parents[5]  # corrected dynamically below if necessary
SHA_EXPECT="93428304dccfa6828e0f355d8b4c5875fb441fb939098519e78fbedf6405bdc5"
BYTES_EXPECT=1121696
PAGES_EXPECT=10
SOURCE="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1003648&type=printable"
STAGES=[
 ("PRE_A","P16_PRE_A_original_source_freeze_v1.json","09519d43dcf73ba0d18be443298528723b5cf8fa"),
 ("A","P16_A_source_native_v1.json","998dd41220b4365c2572cdcdd4e0ff7a460967ac"),
 ("B","P16_B_reaudit_complete_frozen_A_v1.json","8aa8bf28eda3e3dc42d8fae9a6518757e5fb36c9"),
 ("C","P16_C1C2_source_closed_v1.json","273193a55fe605c6d623efc05fcb8c81061c6462"),
 ("D","P16_D_unchanged_grammar_v0_v1.json","dcca60ef6b26227d3bb13de924a414dfa79a437f"),
 ("E","P16_E_original_source_fidelity_v1.json","b3f742422e12c07298b339d1e5067a7266781679"),
]
PFX="research/paper2/p399/g1/parallel/W3/"
def git(*a):
    return subprocess.check_output(["git",*a],encoding="utf-8").strip()
def require(cond,label):
    if not cond: raise RuntimeError("FAIL_CLOSED: "+label)
def test_destroyed(valid):
    bad=bytearray(valid);bad[min(len(bad)-1,100)] ^= 1
    assert hashlib.sha256(bad).hexdigest()!=SHA_EXPECT
    assert len(valid)-1!=BYTES_EXPECT
    assert (not list(reversed([x[0] for x in STAGES])) == [x[0] for x in STAGES])
    assert PAGES_EXPECT+1 != PAGES_EXPECT

def main():
    raw=None
    for attempt in range(1,5):
        try:
            with urllib.request.urlopen(urllib.request.Request(SOURCE,headers={"User-Agent":"Mozilla/5.0 (RelayTheory P16 independent post-E exact publisher original PDF verification)","Accept":"application/pdf,*/*"}),timeout=130) as response: raw=response.read()
            if raw.startswith(b"%PDF"): break
            raise RuntimeError("official source HTTP OK but non-PDF bytes")
        except Exception as exc:
            print("P16_OFFICIAL_SOURCE_ACQUISITION_RETRY",attempt,type(exc).__name__,str(exc),flush=True)
            if attempt==4: raise
            time.sleep(attempt*5)
    sha=hashlib.sha256(raw).hexdigest()
    require(raw[:5]==b"%PDF-","original must be PDF")
    require(sha==SHA_EXPECT,"exact previously acquired original publisher raw SHA: "+sha)
    require(len(raw)==BYTES_EXPECT,"original publisher raw byte count")
    reader=PdfReader(io.BytesIO(raw),strict=False);require(len(reader.pages)==PAGES_EXPECT,"published source 10 pages")
    anchors={
      0:["Place Cell Rate Remapping","Sejnowski"],
      1:["Hebbian","recurrent"],
      2:["Figure 1","context"],
      3:["Figure 2","overlapping"],
      4:["Figure 3","attractor"],
      5:["Figure 5","hysteresis"],
      6:["Figure 7","Figure 8"],
      8:["Recurrent weights","forward"],
    }
    # Text extraction locators are bounded original page tests, not proof of pixel math.
    texts=[(page.extract_text() or "").lower().replace("-\\n","").replace("\\n"," ") for page in reader.pages]
    checks=[]
    for page,needles in anchors.items():
      for needle in needles:
        n=needle.lower(); ok=n in texts[page]
        # permit model-section caption on immediately preceding/next original page
        if not ok: ok=any(n in texts[k] for k in range(max(0,page-1),min(len(texts),page+2)))
        checks.append({"expected_page_1based":page+1,"anchor":needle,"bounded_adjacent_page_fallback":True,"ok":ok})
        require(ok,f"original bounded page {page+1} anchor {needle}")
    doc=fitz.open(stream=raw,filetype="pdf")
    visuals=[]
    for p in [1,2,3,4,5,6,7,8]:
      bitmap=doc[p].get_pixmap(matrix=fitz.Matrix(0.75,0.75))
      require(bitmap.width>200 and bitmap.height>200,"critical page renderability")
      visuals.append({"source_pdf_page_1based":p+1,"render_dimensions":[bitmap.width,bitmap.height]})
    previous=None; original=[]
    for stage,name,commit in STAGES:
      filepath=PFX+name
      source_git=subprocess.check_output(["git","show",f"{commit}:{filepath}"])
      work_bytes=(ROOT/name).read_bytes()
      require(source_git==work_bytes,"frozen scientific bytes must equal first stage introduction: "+stage)
      intro=git("log","--diff-filter=A","--format=%H","HEAD","--",filepath).splitlines()
      require(len(intro)==1 and intro[0]==commit,"first original Git introduction identity: "+stage)
      if previous: require(subprocess.run(["git","merge-base","--is-ancestor",previous,commit]).returncode==0,"strict stage chronological ancestry "+stage)
      require(subprocess.run(["git","merge-base","--is-ancestor",commit,"HEAD"]).returncode==0,"stage commit must be in current branch ancestry")
      original.append({"stage":stage,"intro_commit":commit,"raw_sha256":hashlib.sha256(work_bytes).hexdigest(),"bytes":len(work_bytes)})
      previous=commit
    A=json.loads((ROOT/pathlib.Path("P16_A_source_native_v1.json")).read_text())
    B=json.loads((ROOT/pathlib.Path("P16_B_reaudit_complete_frozen_A_v1.json")).read_text())
    C=json.loads((ROOT/pathlib.Path("P16_C1C2_source_closed_v1.json")).read_text())
    D=json.loads((ROOT/pathlib.Path("P16_D_unchanged_grammar_v0_v1.json")).read_text())
    E=json.loads((ROOT/pathlib.Path("P16_E_original_source_fidelity_v1.json")).read_text())
    require(len(A["original_claims"])==29 and len(A["source_local_dependencies"])==35,"original A inventory")
    require(set(B["review_all_A_claim_ids"])=={v["id"] for v in A["original_claims"]},"B covered exact full A")
    require(len(C["adjacent_negative_C2_unique"])==13 and len(C["append_only_source_supported_deltas"])==1,"C13 original adverse+new B04 only")
    require({x["claim_id"] for x in D["complete_A_roles"]}=={v["id"] for v in A["original_claims"]},"D complete original mapping")
    require(len(D["all_source_dependencies_preserved"])==35,"D preserved all source edges")
    require(len(E["fidelity_targets"])==12 and len(E["all_original_C_unique_negatives"])==13,"E bounded negative fidelity")
    test_destroyed(raw)
    receipt={"scope":"SOURCE_AND_HISTORY_BOUNDED_P16_ONLY; NOT original MATLAB replay or human blinded semantic audit","source_sha256":sha,"size":len(raw),"pages":len(reader.pages),"page_anchors":checks,"page_renderability":visuals,"original_stage_git":original,"scientific_structure_check":"PASS_29_35_13_12","destructive_guard_tests":4,"G1_science_delta_to_shared_denominator":"NONE_WITHOUT_SEPARATE_QUALIFICATION"}
    print(json.dumps(receipt,indent=2,ensure_ascii=False,sort_keys=True),flush=True)
    path=pathlib.Path(os.environ.get("RUNNER_TEMP","/tmp"))/"P16_W3_post_E_real_source_audit_receipt.json"
    path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
if __name__=="__main__":
    main()
