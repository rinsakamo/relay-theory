#!/usr/bin/env python3
"""Deterministic source receipt integrity only; not human semantic proof."""
import copy,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=Path.cwd()
def blob(p):
    return subprocess.check_output(["git","rev-parse","HEAD:"+p],cwd=ROOT,text=True).strip()
def checked(d):
    assert d["schema"]=="relaytheory.p399.g2.three_paper_supplement_source_and_science.v1"
    au=d["authority"];ev=d["physical_evidence"];so=d["sources"];v=d["verdict"]
    assert au["parent_g2_sha"]=="b9b238fe786cba2ae9df9efb26febc78ccd67486"
    assert au["existing_frozen_main40_manifest_blob"]=="b97b67a34ad9c2858745dfa6aa60444520eaab13"
    assert au["three_primary_freeze_receipt_blob"]=="021dd2856510a4ac04fbbb3221d93b103067bb17"
    assert set(so)=={"ATT-03","BLF-01","PRD-01"}
    assert [(so[k]["raw_sha256"],so[k]["raw_bytes"],so[k]["pages"]) for k in ["ATT-03","BLF-01","PRD-01"]]==[
        ("4d75c5cf6b2e896e45072edf7ef588101dae6a005d59b74d497fdf6e250acf5e",74000,5),
        ("dfe031097a03fa013aff88b1e1f5ddcfe41dc4d0bb231cc291b3dc1d92415d53",241964,2),
        ("10f5d55f971060fb325e3e5a0bb4be2df015407ecb1428af9ebd17a4bea6298c",1077373,17)]
    assert so["BLF-01"]["zip_member"]=="mmc1.pdf"
    assert (so["ATT-03"]["actually_model_visually_inspected_pdf_pages"],so["BLF-01"]["actually_model_visually_inspected_pdf_pages"],so["PRD-01"]["actually_model_visually_inspected_pdf_pages"])==([2,3,4],[2],[3,4,5,6])
    assert "S16" in so["ATT-03"]["verified_structure"]
    assert "Figure S1" in so["BLF-01"]["verified_structure"]
    assert "equations(1)-(7)" in so["PRD-01"]["verified_structure"]
    assert "MATERIAL_MULTISOURCE_CONTRADICTION_UNDERDETERMINED"==so["PRD-01"]["study2_numeric_edition_status"]
    assert so["PRD-01"]["supplementary_extraction_science_status"]=="CORE_FORMALISM_SOURCE_DIRECT_VERIFIED_AND_CRITICAL_FIGURE_CONFLICT_DISCOVERED"
    assert so["PRD-01"]["raw_sha256"]!="abb8287b752c4d53480ecc8daefe2802b26c2ed1b48c69067e61d8caea838e38"
    assert (ev["original_retrieval_success_run"],ev["exact_reacquisition_and_all_pages_render_run"],ev["expanded_prd_fig_s2_direct_image_run"])==(37251985672,37252175538,37252276259)
    assert ev["source_media_stored_in_public_git"] is False
    assert ev["human_eyeball_all_pages"] is False
    assert v["three_distinct_supplements_raw_physically_acquired"]==3
    assert v["three_distinct_supplements_hash_and_pages_physically_verified"]==3
    assert v["all_supplement_pages_machine_rasterized"]==24
    assert v["manually_model_visually_checked_page_count"]==8
    assert v["critical_supplement_mathematical_or_control_content_qualified_for_bounded_pre_a"]==3
    assert v["prd01_material_cross_version_numeric_conflict"] is True
    assert v["no_claim_human_visual_full24"] is True
    assert v["all_original_main40_final_source_scientific_admitted"]==0
    assert v["original_main40_roster_modified"] is False
    assert v["backups_activated"]==0
    assert v["g2_internal_780_final_family_independent_clearances"]==0
    assert v["g2_against_g1_800_final_family_independent_clearances"]==0
    assert v["g4_final_post_supplement_joint_audit"] is False
    assert v["main_scientific_grammar_run"] is False
    assert v["main_authorized"] is False
    assert v["state"]=="THREE_SUPPLEMENT_SOURCE_ACQUISITION_CLOSED / BOUNDED_SUPPLEMENT_REVIEWED / PRD_STUDY2_NUMERIC_HOLD / G2_PARTIAL / MAIN_NOT_AUTHORIZED"
d=json.loads((HERE/"THREE_SUPPLEMENT_EXACT_SOURCE_AND_SCIENCE_RECEIPT_v1.json").read_text())
checked(d)
assert blob("research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json")=="b97b67a34ad9c2858745dfa6aa60444520eaab13"
assert blob("research/paper2/p399/g2/three_primary_review_20261005/THREE_PRIMARY_SOURCE_FREEZE_AND_BOUNDED_SCIENCE_v1.json")=="021dd2856510a4ac04fbbb3221d93b103067bb17"
bad=[
 lambda x:x["sources"]["PRD-01"].update(study2_numeric_edition_status="RESOLVED"),
 lambda x:x["sources"]["PRD-01"].update(raw_sha256="0"*64),
 lambda x:x["sources"]["ATT-03"].update(raw_bytes=74001),
 lambda x:x["sources"]["BLF-01"].update(zip_member="publisher_original.pdf"),
 lambda x:x["physical_evidence"].update(human_eyeball_all_pages=True),
 lambda x:x["physical_evidence"].update(source_media_stored_in_public_git=True),
 lambda x:x["verdict"].update(all_supplement_pages_machine_rasterized=0),
 lambda x:x["verdict"].update(manually_model_visually_checked_page_count=24),
 lambda x:x["verdict"].update(prd01_material_cross_version_numeric_conflict=False),
 lambda x:x["verdict"].update(all_original_main40_final_source_scientific_admitted=40),
 lambda x:x["verdict"].update(g2_internal_780_final_family_independent_clearances=780),
 lambda x:x["verdict"].update(g2_against_g1_800_final_family_independent_clearances=800),
 lambda x:x["verdict"].update(backups_activated=1),
 lambda x:x["verdict"].update(main_authorized=True),
 lambda x:x["verdict"].update(main_scientific_grammar_run=True),
 lambda x:x["verdict"].update(g4_final_post_supplement_joint_audit=True),
]
for n,alter in enumerate(bad):
    x=copy.deepcopy(d); alter(x)
    try:checked(x)
    except AssertionError:continue
    raise AssertionError("false promotion slipped "+str(n))
print("PASS immutable original MAIN40 source and primary freeze blobs")
print("PASS publisher/archive supplement SHA/bytes/pages + bounded critical visual scope")
print(f"PASS {len(bad)}/{len(bad)} destructive false source/visual/math/science/MAIN promotions rejected")
print("NOTE this does not reproduce authors' behavioral numerical fits or resolve PRD supplemental numeric contradiction")
