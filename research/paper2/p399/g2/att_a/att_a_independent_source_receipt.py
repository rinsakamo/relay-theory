#!/usr/bin/env python3
"""Independent ATT-only original-media source integrity check, NOT semantic mathematical qualification.

Each network request has a strict timeout. Failed official downloads produce explicit HOLD;
a publisher PDF browser opening is an independent manual route, never silently a SHA receipt.
"""
import argparse
import hashlib
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
HANDOFF = HERE / "ATT_A_BOUNDED_SOURCE_GENEALOGY_HANDOFF_v1.json"
FILES = {
    "ATT_B1_MAIN": {
        "url": "https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1011283&type=printable",
        "sha": "8c190f4d6e981061e4ccd67f4797b83ccdeb8f1d47d8368fdafe137f1ef44209",
        "bytes": 1760491, "pages": 20,
    },
    "ATT_B1_S3": {
        "url": "https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1011283.s003&type=supplementary",
        "sha": "c71313033e52ccbbe5b0b3e8579959dfb7ac75c52ca254a36abca89ac8fcb72f",
        "bytes": 210828, "pages": 6,
    },
}

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def validate_ledger(ledger):
    assert ledger["baseline_g2_head"] == "69748673c80f421605f1c63607472903ac2ed68c"
    b = ledger["ATT_B1"]
    assert b["source_bundle"]["single_primary"]["prior_raw_sha256"] == FILES["ATT_B1_MAIN"]["sha"]
    assert b["source_bundle"]["mandatory_same_article_s3"]["prior_raw_sha256"] == FILES["ATT_B1_S3"]["sha"]
    assert len(b["published_models"]) == 5
    assert len(b["negative_conditions_upstream_v8_immutable"]) == 7
    assert b["new_unresolved_upstream_v8a_preserved"] == "N_ATT_B1_008"
    assert abs(b["published_error"]["M3a"]["se"] - 0.05) < 1e-10
    assert b["published_error"]["M3c"]["mean"] < b["published_error"]["M3a"]["mean"] < b["published_error"]["M3b"]["mean"]
    assert ledger["bounded_decision"]["backups_activated"] == 0
    assert ledger["bounded_decision"]["main_authorized"] is False
    assert b["full_S3_math_eq_S1_to_S19_visual"] == "HOLD"
    assert ledger["ATT_03"]["admission"] == "HOLD_OFFICIAL_SOURCE_UNACQUIRED"
    return True

def fetch_with_timeout(url, attempts=2, timeout=12):
    errors=[]
    for idx in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "RelayTheory-source-audit/1.0", "Accept": "application/pdf"})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content = response.read(12_000_000)
                return content, {"attempt":idx + 1,"status":response.status,"final_url":response.geturl()}
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            errors.append({"attempt":idx + 1, "error":str(exc)[:300],"timeout_seconds":timeout})
            if idx + 1 < attempts: time.sleep(0.5)
    return None, {"attempts":errors,"fallback":"MANUAL_BROWSER_DIRECT_OFFICIAL_URL_NO_BYTE_CLAIM"}

def check_pdf(item, spec, outdir, timeout):
    data, transfer = fetch_with_timeout(spec["url"], timeout=timeout)
    result={"role":item,"url":spec["url"],"transfer":transfer,"expected_sha256":spec["sha"],
            "verified":False,"original_images_semantically_eyeballed":False}
    if data is None:
        result["disposition"]="OFFICIAL_TIMEOUT_OR_ACCESS_FAILURE_BROWSER_INSPECTION_REQUIRED"
        return result
    result["observed_sha256"]=sha256(data)
    result["observed_bytes"]=len(data)
    if not data.startswith(b"%PDF"):
        result["disposition"]="NOT_ACTUAL_PDF"
        return result
    if result["observed_sha256"] != spec["sha"] or len(data)!=spec["bytes"]:
        result["disposition"]="SOURCE_BYTES_MISMATCH_FAIL_CLOSED"
        return result
    try:
        import fitz
        doc=fitz.open(stream=data,filetype="pdf")
        result["observed_pages"]=len(doc)
        if len(doc)!=spec["pages"]:
            result["disposition"]="SOURCE_PAGE_COUNT_MISMATCH"
            return result
        for n in (range(len(doc)) if item.endswith("S3") else (2,3,5,8,9,10)):
            # Explicit per-page rendering receipt; a render is NOT visual human equation validation.
            pix=doc[n].get_pixmap(matrix=fitz.Matrix(1.75,1.75),alpha=False)
            raw=pix.tobytes("png")
            sub=outdir / "rendered_original_pages"
            sub.mkdir(parents=True,exist_ok=True)
            file=sub / f"{item}_p{n + 1:02d}.png"
            file.write_bytes(raw)
            result.setdefault("rendered_image_receipts",[]).append({
                "page_number_1_based":n+1,"render_png_sha256":sha256(raw),
                "width":pix.width,"height":pix.height})
        if item.endswith("S3"):
            full="\\n".join(page.get_text() for page in doc)
            result["s3_equation_text_identifiers_detected"]=[n for n in range(1,20) if
                re.search(rf"\\bS{n}\\b",full)]
            result["s3_equation_pixel_semantics_pass"]=False
        result["verified"]=True
        result["disposition"]="EXACT_ORIGINAL_BYTES_AND_PAGES_AND_PIXELS_RENDERED_NO_AUTOMATIC_SEMANTIC_QUALIFICATION"
    except Exception as exc:
        result["disposition"]="RENDER_ERROR"
        result["render_error"]=repr(exc)[:500]
    return result

def run(out,offline=False,timeout=12,fixture=None):
    data=json.loads(HANDOFF.read_text(encoding="utf-8") if fixture is None else pathlib.Path(fixture).read_text(encoding="utf-8"))
    validate_ledger(data)
    out=pathlib.Path(out)
    out.mkdir(parents=True,exist_ok=True)
    report={"schema":"relaytheory.p399.g2a.actual_runtime_receipt.v1",
            "starting_head":data["baseline_g2_head"],"ledger_static_guard":"PASS",
            "mode":"OFFLINE_GUARD_ONLY" if offline else "ACTUAL_FIRST_PARTY_PDF_NETWORK_ATTEMPTS",
            "not_a_visual_math_claim":True,"not_final_admission":True,"records":[]}
    if not offline:
        for name,spec in FILES.items():
            report["records"].append(check_pdf(name,spec,out,timeout))
    (out / "ATT_A_ACTUAL_RUNTIME_RECEIPT.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="records"},sort_keys=True))
    for result in report["records"]:
        print(result["role"],result["disposition"],result.get("observed_sha256","NO_BYTES"),result.get("observed_pages","NO_PAGES"))
    return report

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="att-a-run")
    ap.add_argument("--offline",action="store_true")
    ap.add_argument("--timeout",type=int,default=12)
    ap.add_argument("--fixture")
    a=ap.parse_args()
    run(a.out,a.offline,a.timeout,a.fixture)
