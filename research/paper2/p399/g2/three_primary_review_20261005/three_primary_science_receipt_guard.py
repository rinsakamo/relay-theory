#!/usr/bin/env python3
"""Metadata/provenance anti-promotion guard. Optional separate physical local PDF checks.

Crucial: PASS without --raw-dir is NOT an independent source-PDF byte/pixel
audit and says nothing about correctness of human semantic mathematics.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[5]
SOURCE = Path(__file__).with_name("THREE_PRIMARY_SOURCE_FREEZE_AND_BOUNDED_SCIENCE_v1.json")
EXPECTED_ROSTER_BLOB = "b97b67a34ad9c2858745dfa6aa60444520eaab13"
EXPECTED_INTEGRATION_RECEIPT_BLOB = "17ca919493afe00e62adf4b8c896c0720c9cb1e9"
EXPECTED_PRD_OWNER_RECEIPT_BLOB = "c3b5a3d22035d454cdbec1083a10f3182e8eb755"

def checked(d):
    assert d["schema"] == "relaytheory.p399.g2.three_original_user_media_freeze.v1"
    a = d["authority"]
    assert (a["author_att03_review_permitted"], a["author_prd01_manuscript_plus_publisher_correction_permitted"]) == (True, True)
    assert d["source_access_class"].startswith("USER_UPLOADED_RAW_MEDIA_LOCALLY_PHYSICALLY_INSPECTED")
    assert d["frozen_scope"] == "THREE_SELECTED_SOURCE_MEDIA_AND_SOURCE_NATIVE_SCIENCE_PRE_A_ONLY"
    f = d["files"]
    assert set(f) == {"ATT03", "BLF01", "PRD01"}
    for k,doi in (("ATT03","10.1016/j.neuron.2009.01.002"),("BLF01","10.1016/j.isci.2025.112844"),("PRD01","10.1038/s41562-024-01930-8")):
        e=f[k]
        assert e["doi"] == doi
        assert e["main_source_native_result"].startswith("BOUNDED_")
        assert e["full_math_figure_and_adverse_qualification"] is False
        assert e["full_family_clear"] is False
        assert e["critical_supplement"].endswith("not physically frozen") or "not physically frozen" in e["critical_supplement"]
    assert f["ATT03"]["author_review_waiver"] is True
    assert f["ATT03"]["paper_first_page_type"] == "Review"
    assert (f["ATT03"]["pages"], f["ATT03"]["bytes"], f["ATT03"]["sha256"]) == (18,730088,"a4b4d5766ba20219a8f698cf0cbcc275916d5c06a7887bd877c309635804d5a0")
    assert (f["BLF01"]["pages"], f["BLF01"]["bytes"], f["BLF01"]["sha256"]) == (31,7976135,"5ba2b234ea4c6d3c3db119aa67e086ff1cf1732ab90b30b794ae6ac309f23807")
    assert f["PRD01"]["author_substitution_authorized"] is True
    assert f["PRD01"]["full_corrected_publisher_vor_acquired"] is False
    assert f["PRD01"]["original_publisher_initial_figure_pixels_obtained"] is False
    assert len(f["PRD01"]["source_bundle"])==2
    assert f["PRD01"]["source_bundle"][0]["sha256"] == "abb8287b752c4d53480ecc8daefe2802b26c2ed1b48c69067e61d8caea838e38"
    assert f["PRD01"]["source_bundle"][1]["sha256"] == "c05578f6ce33078a45ec97195405f0f8fcb2f1f8c4f9564447d6790ccf395302"
    c=f["PRD01"]["corrected_figures"]
    assert c["panels"] == ["2a","4a"]
    assert c["publisher_notice_corrected"]=={"trident":0.69,"planet":0.31}
    assert c["initial_publisher_notice"]=={"trident":0.33,"planet":0.67}
    assert c["uploaded_manuscript_figures_already_show_corrected_values"] is True
    assert c["double_patch_prohibited"] is True
    assert (c["uploaded_manuscript_fig2a_pdf_page"],c["uploaded_manuscript_fig4a_pdf_page"]) == (21,25)
    assert d["frozen_prior_manifest_git_blob"]==EXPECTED_ROSTER_BLOB
    s=d["formal_pre_a"]
    assert (s["source_media_locally_physically_hashed"],s["selected_original_slots_source_bundle_documented"]) == (4,3)
    assert (s["source_native_model_originality_present_with_disclosed_ancestry"],s["full_critical_source_science_qualifications"]) == (3,0)
    for field in ["complete_original_vs_G2_internal_family_pairwise_clearance","complete_original_vs_G1_family_pairwise_clearance","backup_activated"]:
        assert s[field] == 0
    for field in ["full_correction_chronology_certified","selected_roster_modified","main_science_executed","main_authorized"]:
        assert s[field] is False
    assert s["status"].endswith("G2_PARTIAL / MAIN_NOT_AUTHORIZED")

def blob(path):
    return subprocess.check_output(["git","rev-parse",f"HEAD:{path}"],text=True).strip()
def raw_verify(d,rawdir):
    try:
        import fitz
    except ImportError as e:
        raise RuntimeError("PyMuPDF needed for optional physical media page verification") from e
    files=d["files"]
    items=[
      (files["ATT03"]["local_original_filename"],files["ATT03"]),
      (files["BLF01"]["local_original_filename"],files["BLF01"]),
      *[(x["local_filename"],x) for x in files["PRD01"]["source_bundle"]],
    ]
    for name,x in items:
        b=(rawdir/name).read_bytes()
        assert hashlib.sha256(b).hexdigest()==x["sha256"],name
        assert len(b)==x["bytes"],name
        assert len(fitz.open(stream=b,filetype="pdf"))==x["pages"],name
        print("PASS local raw SHA/pages",name)
def destructive(d):
    edits=[
      lambda x:x["authority"].update(author_att03_review_permitted=False),
      lambda x:x["files"]["ATT03"].update(full_family_clear=True),
      lambda x:x["files"]["BLF01"].update(full_math_figure_and_adverse_qualification=True),
      lambda x:x["files"]["PRD01"].update(full_corrected_publisher_vor_acquired=True),
      lambda x:x["files"]["PRD01"].update(original_publisher_initial_figure_pixels_obtained=True),
      lambda x:x["files"]["PRD01"]["corrected_figures"].update(double_patch_prohibited=False),
      lambda x:x["files"]["PRD01"]["corrected_figures"].update(publisher_notice_corrected={"trident":0.33,"planet":0.67}),
      lambda x:x["files"]["PRD01"]["source_bundle"][0].update(sha256="0"*64),
      lambda x:x["formal_pre_a"].update(full_critical_source_science_qualifications=3),
      lambda x:x["formal_pre_a"].update(backup_activated=1),
      lambda x:x["formal_pre_a"].update(selected_roster_modified=True),
      lambda x:x["formal_pre_a"].update(main_science_executed=True),
      lambda x:x["formal_pre_a"].update(main_authorized=True),
      lambda x:x["formal_pre_a"].update(complete_original_vs_G1_family_pairwise_clearance=800),
      lambda x:x.update(source_access_class="INDEPENDENT_CLOUD_PUBLISHER_RECEIPT"),
      lambda x:x["files"]["ATT03"].update(paper_first_page_type="Research Article"),
    ]
    for i,edit in enumerate(edits):
        y=copy.deepcopy(d);edit(y)
        try:checked(y)
        except AssertionError: continue
        raise AssertionError(f"FALSE_PROMOTION_MUTATION_{i+1}_NOT_REJECTED")
    return len(edits)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--raw-dir",type=Path,help="OPTIONAL supplied user raw PDFs; without this CI tests metadata only")
    args=ap.parse_args()
    d=json.loads(SOURCE.read_text())
    checked(d)
    assert blob("research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json")==EXPECTED_ROSTER_BLOB, "Find current frozen roster path if renamed; no science promotion"
    assert blob("research/paper2/p399/g2/integration_20261005/G2_FOUR_LANE_INTEGRATION_RECEIPT_v1.json")==EXPECTED_INTEGRATION_RECEIPT_BLOB
    assert blob("research/paper2/p399/g2/integration_20261005/PRD01_AUTHOR_ADOPTED_MANUSCRIPT_CORRECTION_BUNDLE_v1.json")==EXPECTED_PRD_OWNER_RECEIPT_BLOB
    print("PASS frozen original manifest and unchanged prior original/history receipts")
    print("PASS 3 documented paper sources + 4 declared exact source hashes; bounded-science gating")
    print("PASS",destructive(d),"/16 destructive false-promotion and version-mislabel rejections")
    if args.raw_dir:raw_verify(d,args.raw_dir)
    else:print("SKIP independent publisher fetch / physical raw PDF CI; provide --raw-dir for actual local hash+page check")
if __name__=="__main__":main()
