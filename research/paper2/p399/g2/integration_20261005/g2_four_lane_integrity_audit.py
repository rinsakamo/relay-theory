#!/usr/bin/env python3
"""Fail-closed evidence-integrity audit. Not semantic scientific qualification."""
import copy
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[5]  # replaced below by git rev-parse
ROOT = pathlib.Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
D = ROOT / "research/paper2/p399/g2"
I = D / "integration_20261005"
def load(path):
    return json.loads(path.read_text(encoding="utf-8"))
def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()
def eq(actual, expected, name):
    if actual != expected:
        raise AssertionError(f"{name}: {actual!r} != {expected!r}")
def yes(cond, name):
    if not cond: raise AssertionError(name)
def policy(m, f, r, v20, softmax, proof):
    roster=m["selected_working_roster"]
    eq(len(roster), 40, "40 slots")
    eq(len(set(x["doi"].lower() for x in roster)), 40, "40 unique DOI")
    eq(sum(x["primary"] != "INTEGRATION" for x in roster), 24, "component count")
    eq(sum(x["primary"] == "INTEGRATION" for x in roster), 16, "INT count")
    eq(m["count"]["current_publisher_pdf_byte_receipts"], 31, "historical raw PDF")
    yes(all(x.get("central_family_independent_certified") is False and x.get("source_eligible") is False for x in roster), "no upstream science admission")
    eq(len(f["main_main_pairs"]), 780, "MAIN internal complete pair enumeration")
    eq(len(f["main_vs_g1_pairs"]), 800, "G1 20 x MAIN 40 complete enumeration")
    yes(not any(x.get("may_be_counted_independent", False) for x in f["main_main_pairs"] + f["main_vs_g1_pairs"]), "no final family clearances")
    eq(r["state"], "G2_PARTIAL / MAIN_NOT_AUTHORIZED", "explicit final stop")
    eq(r["source"]["minimum_distinct_publisher_raw_selected_pdfs_after_unique_increment"],32,"new unique INT04 main raw PDF")
    eq(r["source"]["baseline_publisher_raw_selected_pdfs"],31,"base PDF census")
    eq(r["source"]["study_readable_original_with_user_private_INT01_MHT"],37,"private source separate")
    yes(r["source"]["publisher_firstparty_access_not_automatically_incremented_by_private_MHT"],"MHT must not imply publisher HTTP")
    eq(r["source"]["three_remaining_primary_edition_acquisition_blockers"],["ATT-03","BLF-01","PRD-01"],"unobtained selected originals")
    eq(r["source"]["all40_complete_mathematics_figures_variants_negative_and_correction_qualified"],0,"source is not science")
    eq(r["decisions"]["backups_preregistered_but_activated"],0,"no backup")
    eq(r["formal"]["full_selected_main40_scientific_admissions"],0,"no complete science promotion")
    eq(r["formal"]["fully_independent_central_family_qualified_global"],0,"no global independence")
    eq(r["formal"]["formally_activated_backups"],0,"no adoption")
    eq(r["formal"]["final_joint_scientific_manifest_sha"],None,"no final roster sha")
    eq(r["formal"]["final_G3_joint_protocol_sha"],None,"no joint protocol sha")
    yes(not r["formal"]["MAIN_authorized"] and not r["formal"]["author_MAIN_GO"] and not r["formal"]["G4_latest_joint_postintegration_audit_pass"],"no MAIN GO")
    yes(r["no_main_science_executed"] and r["grammar_v0_untouched"] and r["old_398_untouched"] and r["private_int01_mht_not_published"],"protected scopes")
    eq(r["family"]["G2_internal_exact_pairs"],780,"internal pair denominator")
    eq(r["family"]["G2_vs_G1_working20_pairs"],800,"G1 pair denominator")
    eq(r["family"]["complete_central_family_independent_G2_pairs"],0,"internal full family hold")
    eq(r["family"]["complete_central_family_independent_G1_pairs"],0,"G1 full family hold")
    yes(not r["family"]["G1_cohort_final_diversity_accepted"],"G1 20 individual != cohort acceptance")
    q=v20["updated_original35_matrix"]["quantitative_scope"]
    eq(q["prospective_pair_queue"],35,"INT01 total prospective original peers")
    eq(q["source_native_bounded_checked_pairs"],12,"INT01 bounded checks")
    eq(q["untested_original_native_math_pairs"],23,"INT01 unreviewed math")
    eq(q["full_family_final_global_qualifications"],0,"no final from scoped witnesses")
    eq(r["family"]["int01_scoped_native_original_pairs_checked"],12,"scoped pair transfer")
    eq(r["family"]["int01_original_native_mathematics_not_yet_checked"],23,"unreviewed transfer")
    yes(not r["family"]["global_overlay_all_1580_scoped_examined_exhaustively_reconciled"],"do not invent all-pair examined count")
    yes(softmax["adopted_model_operator"]["status"].startswith("AUTHOR_APPROVED"),"INT01 code softmax author decision")
    yes(softmax["printed_publisher_record"]["retained_as_source_variant"] and not softmax["printed_publisher_record"]["proven_publisher_erratum"],"preserve printed discrepancy")
    yes(not softmax["independent_status"]["whole_selected_INT01_formal_full_scientific_admission"],"INT01 no false full admission")
    yes(r["decisions"]["INT01"]["adopted"].find("softmax")>=0 and not r["decisions"]["INT01"]["full_science_qualified"],"INT01 exception bounded")
    eq(proof["selected_source"]["canonical_main_reference"]["sha256"],r["decisions"]["INT13"]["publisher_pdf_raw_sha256"],"INT13 exact approved proof")
    yes(proof["selected_source"]["publisher_proof_notice_explicit"] and not proof["selected_source"]["publisher_published_original_final_vor"],"uncorrected stays uncorrected")
    eq(proof["state_delta"]["full_int13_scientific_qualification"],"NOT_GRANTED","INT13 no false full science")
    eq(proof["state_delta"]["formal_backup_activation"],False,"INT13 not a backup")
    yes(not r["decisions"]["INT13"]["publisher_corrected_final_vor"] and not r["decisions"]["INT13"]["full_science_qualified"],"INT13 bounded edition waiver")
    yes(v20["published_INT09_correction"]["source_native_correction_read"] and not v20["published_INT09_correction"]["full_INT09_scientific_qualification"],"INT09 source correction not science")
    return True

def main():
    r=load(I/"G2_FOUR_LANE_INTEGRATION_RECEIPT_v1.json")
    m=load(D/"MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json")
    f=load(D/"MAIN40_G2_780_MAIN_AND_800_G1_FAMILY_RECONCILIATION_v2.json")
    v20=load(D/"int_g2d/G2D_V20_INT01_THREE_ADDITIONAL_PAIRS_INT09_OFFICIAL_FIG9_CORRIGENDUM_AND_35_QUEUE.json")
    softmax=load(D/"int_g2d/G2D_V17_INT01_AUTHOR_ADOPTED_SOFTMAX_PROBABILITY_OPERATOR_v1.json")
    proof=load(D/"int_g2d/G2D_INT13_AUTHOR_ADOPTED_UNCORRECTED_PROOF_STUDY_EDITION_DELTA_v2.json")
    base=r["frozen_start"]
    exact={
        "research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json":base["main40_manifest_v5_git_blob"],
        "research/paper2/p399/g2/MAIN40_G2_780_MAIN_AND_800_G1_FAMILY_RECONCILIATION_v2.json":base["family_v2_git_blob"],
        "research/paper2/p399/g2/int_g2d/G2D_V17_INT01_AUTHOR_ADOPTED_SOFTMAX_PROBABILITY_OPERATOR_v1.json":"1b54c0ce7d464f9086b39ac67310c07dd11e5915",
        "research/paper2/p399/g2/int_g2d/G2D_INT13_AUTHOR_ADOPTED_UNCORRECTED_PROOF_STUDY_EDITION_DELTA_v2.json":"8bf8c411dcd3c4d314265be56d85276bb1451fb6",
        "research/paper2/p399/g2/int_g2d/G2D_V20_INT01_THREE_ADDITIONAL_PAIRS_INT09_OFFICIAL_FIG9_CORRIGENDUM_AND_35_QUEUE.json":"886bed52531abec3457f3b9976f39236b8899007"
    }
    for path,sha in exact.items(): eq(git("rev-parse","HEAD:"+path),sha,"pinned blob "+path)
    for key,item in r["input_prs"].items():
        eq(git("rev-parse","HEAD:"+item["path"]),item["evidence_tree"],key+" original whole evidence tree")
        subprocess.run(["git","merge-base","--is-ancestor",item["head"],"HEAD"],cwd=ROOT,check=True)
        print(f"PASS provenance {key} {item['head']} evidence tree {item['evidence_tree']}")
    subprocess.run(["git","merge-base","--is-ancestor",base["commit"],"HEAD"],cwd=ROOT,check=True)
    yes(not list((D/"int_g2d").rglob("*.mht")),"private MHT not deposited")
    eq(sum(x["file_count"] for x in r["input_prs"].values()),151,"source files disjoint total")
    eq(r["provenance"]["file_path_overlap_four_prs"],[],"nonoverlapping paths")
    policy(m,f,r,v20,softmax,proof)
    print("PASS positive fixed-source roster/editions/35/780/800/promotion boundaries")
    mutations=[
      lambda x:x["source"].update(all40_complete_mathematics_figures_variants_negative_and_correction_qualified=40),
      lambda x:x["formal"].update(full_selected_main40_scientific_admissions=1),
      lambda x:x["formal"].update(fully_independent_central_family_qualified_global=1580),
      lambda x:x["formal"].update(formally_activated_backups=1),
      lambda x:x["formal"].update(MAIN_authorized=True),
      lambda x:x["formal"].update(author_MAIN_GO=True),
      lambda x:x["formal"].update(G4_latest_joint_postintegration_audit_pass=True),
      lambda x:x["formal"].update(final_joint_scientific_manifest_sha="fabricated"),
      lambda x:x["family"].update(complete_central_family_independent_G2_pairs=1),
      lambda x:x["family"].update(int01_scoped_native_original_pairs_checked=35),
      lambda x:x["family"].update(global_overlay_all_1580_scoped_examined_exhaustively_reconciled=True),
      lambda x:x["decisions"]["INT01"].update(full_science_qualified=True),
      lambda x:x["decisions"]["INT13"].update(publisher_corrected_final_vor=True),
      lambda x:x["decisions"].update(backups_preregistered_but_activated=1),
      lambda x:x["source"].update(publisher_firstparty_access_not_automatically_incremented_by_private_MHT=False),
      lambda x:x["family"].update(G1_cohort_final_diversity_accepted=True)
    ]
    for i,mutation in enumerate(mutations,1):
        bad=copy.deepcopy(r)
        mutation(bad)
        try:policy(m,f,bad,v20,softmax,proof)
        except AssertionError:pass
        else:raise AssertionError(f"FALSE PROMOTION ACCEPTED {i}")
    print(f"PASS {len(mutations)}/{len(mutations)} destructive false-promotion rejects")
    print("PASS original four branch histories, exact trees, pinned upstream records, main manifest and policy guards")
if __name__=="__main__":main()
