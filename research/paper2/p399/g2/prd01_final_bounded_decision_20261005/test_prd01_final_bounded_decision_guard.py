#!/usr/bin/env python3
"""Fail-closed permanent PRD01 bounded-qualification scope/edition guards.

This tests committed decisions and historic receipts, NOT independent paper
math truth or trial-log participant-level numeric reproduction.
"""
import copy,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
D=json.loads((HERE/"PRD01_FINAL_BOUNDED_SOURCE_SCIENCE_QUALIFICATION_AND_FIGS2_EXCEPTION_v1.json").read_text())
def blob(p):
    return subprocess.check_output(["git","rev-parse",f"HEAD:{p}"],text=True).strip()
EXPECTED={
"research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json":"b97b67a34ad9c2858745dfa6aa60444520eaab13",
"research/paper2/p399/g2/integration_20261005/PRD01_AUTHOR_ADOPTED_MANUSCRIPT_CORRECTION_BUNDLE_v1.json":"c3b5a3d22035d454cdbec1083a10f3182e8eb755",
"research/paper2/p399/g2/three_primary_review_20261005/THREE_PRIMARY_SOURCE_FREEZE_AND_BOUNDED_SCIENCE_v1.json":"021dd2856510a4ac04fbbb3221d93b103067bb17",
"research/paper2/p399/g2/supplement_20261005/THREE_SUPPLEMENT_EXACT_SOURCE_AND_SCIENCE_RECEIPT_v1.json":"29fb9f96d5990c1b06e562eaf5e5dd370d1a34f9",
"research/paper2/p399/g2/supplement_20261005/PRD01_PREPUBLICATION_TASK_CODE_NUMERIC_RECONCILIATION_DELTA_v1.json":"096605d752e23854e5dcf36575f35c41ae915813"
}
def check(d):
    assert d["schema"]=="relaytheory.paper2.p399.g2.prd01.author_directed_final_bounded_source_science_decision.v1"
    assert d["final_verdict"]=="QUALIFIED_WITH_REGISTERED_EXCLUSIONS"
    assert d["qualification_axis"]=="SELECTED_PRD01_PRE_A_SOURCE_NATIVE_STRUCTURAL_PROCEDURAL_MODEL_SCIENCE_ONLY"
    a=d["authority"];f=d["frozen_source_bundle"];p=d["permitted_reconstruction"];exc=d["permanent_exclusions"];e=d["eligibility"]
    assert a["exact_starting_g2_commit"]=="9444238465cfbabca9bac653b6e54fa313eacc2d"
    assert a["original_working_main40_manifest_git_blob"]==EXPECTED["research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json"]
    assert f["study"]["raw_sha256"]=="abb8287b752c4d53480ecc8daefe2802b26c2ed1b48c69067e61d8caea838e38"
    assert f["study"]["origin"].startswith("user-supplied PMC")
    assert f["publisher_correction"]["raw_sha256"]=="c05578f6ce33078a45ec97195405f0f8fcb2f1f8c4f9564447d6790ccf395302"
    assert f["publisher_supplement"]["raw_sha256"]=="10f5d55f971060fb325e3e5a0bb4be2df015407ecb1428af9ebd17a4bea6298c"
    assert f["publisher_supplement"]["critical_math_and_figure_pages_visually_inspected"]==[3,4,5,6]
    assert f["publisher_supplement"]["all_17_machine_rasterized"] is True
    assert f["source_original_first_vor_and_corrected_full_vor_direct_bytes_obtained"] is False
    assert f["author_permitted_substitution_applied"] is True
    assert f["user_supplied_pdf_binaries_committed_publicly"] is False
    for k,name in [("prior_author_bundle_receipt_git_blob","PRD01_AUTHOR_ADOPTED_MANUSCRIPT_CORRECTION_BUNDLE_v1.json"),("prior_three_primary_bundle_receipt_git_blob","THREE_PRIMARY_SOURCE_FREEZE_AND_BOUNDED_SCIENCE_v1.json"),("prior_three_supplement_receipt_git_blob","THREE_SUPPLEMENT_EXACT_SOURCE_AND_SCIENCE_RECEIPT_v1.json"),("prior_prepublication_code_delta_git_blob","PRD01_PREPUBLICATION_TASK_CODE_NUMERIC_RECONCILIATION_DELTA_v1.json")]:
        assert f[k] in EXPECTED.values(),(k,name)
    assert len(p["structural_and_procedural_claims"])==7
    assert p["official_corrected_main_Fig2a_Fig4a_study2_study4"]=={"trident":0.69,"planet":0.31}
    assert p["published_supplement_FigS1_study1_not_affected"]=={"trident":0.33,"planet":0.67}
    code=p["publicly_released_prepublication_source_code"]
    assert code["git_commit"]=="ab131a9d0366df00ac2dc79438fe9a89e30f5767"
    assert code["commit_date_utc"]=="2024-05-04T15:49:57Z"
    assert code["study2_task_csv_git_blob"]=="6e6e016a53dea8b02e8f4d8fed7de0dc8b4da0b3"
    assert code["study4_task_csv_git_blob"]=="5e9bffe4697f8c469758c6fe93df5705c406c261"
    assert code["study2_trial_counts"]=={"total":520,"trident":360,"planet":160}
    assert code["study4_trial_counts"]=={"total":520,"trident":360,"planet":160}
    assert code["qualifies"]=="INTENDED_PUBLIC_RELEASED_TASK_FREQUENCIES_ONLY"
    assert code["not_proven"]=="ALL_HISTORICAL_PARTICIPANTS_RECEIVED_IDENTICAL_TRIAL_FILES"
    c=exc["publication_unresolved_figS2"]
    assert c["study"]=="Study 2" and c["pdf_page"]==6 and c["preserve_original_publisher_supplement"] is True
    assert c["figure_diagram"]=={"trident":0.33,"planet":0.67}
    assert c["figure_caption"]=={"trident":0.67,"planet":0.33}
    assert c["formal_publisher_main_fig_corrected"]=={"trident":0.69,"planet":0.31}
    assert c["publisher_supplement_figS2_official_correction_issued"] is False
    assert "DO_NOT_USE_UNCORRECTED_FIGS2_NUMERIC_LABELS" in c["source_disposition"]
    assert c["repair_action"]=="NONE_NO_SILENT_PUBLISHER_FIGURE_MODIFICATION"
    assert len(exc["author_manuscript_internal_discrepancies"])==3
    assert all(z["preserve_source"] for z in exc["author_manuscript_internal_discrepancies"])
    assert len(exc["not_rescued_by_task_design_counts"])==4
    assert e["paper_has_own_empirically_tested_original_mechanistic_scope"] is True
    assert e["selected_prd01_pre_A_final_source_science"]=="QUALIFIED_WITH_REGISTERED_EXCLUSIONS"
    assert e["unresolved_published_figS2_blocker_under_scoped_admission"]=="WAIVED_AS_NUMERIC_EVIDENCE_IF_EXCLUDED_AND_RETAINED_AS_VERSION_ADVERSARIAL_CASE"
    assert e["mandatory_critical_structural_learning_supplement_missing"] is False
    assert e["all_original_publication_text_stats_and_pixels_fully_reconciled"] is False
    assert e["exact_participant_level_statistical_replication"] is False
    assert e["global_family_independence"]=="HOLD_ALL_780_PLUS_800"
    assert e["final_MAIN40_global_g2_admission"] is False
    assert e["main40_roster_edited"] is False and e["backup_activated"] is False
    assert e["g4_independent_second_assessor_approval"] is False and e["main_authorized"] is False
    assert "MAIN_NOT_AUTHORIZED" in e["status"]
    for denied in ["UNCONDITIONAL_ALL_PUBLISHED_EDITION_PIXEL_EQUIVALENCE","REPLAYED_AUTHOR_EMPIRICAL_FIT_OR_BAYES_FACTORS","GLOBAL_MODEL_FAMILY_INDEPENDENCE","G2_WHOLE_MAIN40_FINAL_ADMISSION","MAIN_GRAMMAR_ANALYSIS"]:
        assert denied in d["not_granted"]
check(D)
for path,wanted in EXPECTED.items():
    actual=blob(path)
    assert actual==wanted,(path,actual,wanted)
print("PASS 5/5 immutable original manifest/prior-source/supplement/task-code evidence Git blobs")
print("PASS PRD01 bounded admission, authorized three-original edition bundle, authentic supplement, official correction and pre-publication code source")
alter=[
 lambda x:x.update(final_verdict="UNCONDITIONAL_QUALIFIED"),
 lambda x:x.update(qualification_axis="G2_GLOBAL_SOURCE_PLUS_FAMILY"),
 lambda x:x["frozen_source_bundle"].update(source_original_first_vor_and_corrected_full_vor_direct_bytes_obtained=True),
 lambda x:x["frozen_source_bundle"]["study"].update(raw_sha256="0"*64),
 lambda x:x["frozen_source_bundle"]["publisher_supplement"].update(raw_sha256="0"*64),
 lambda x:x["permitted_reconstruction"].update(official_corrected_main_Fig2a_Fig4a_study2_study4={"trident":.33,"planet":.67}),
 lambda x:x["permitted_reconstruction"].update(published_supplement_FigS1_study1_not_affected={"trident":.69,"planet":.31}),
 lambda x:x["permitted_reconstruction"]["publicly_released_prepublication_source_code"].update(study2_trial_counts={"total":520,"trident":160,"planet":360}),
 lambda x:x["permitted_reconstruction"]["publicly_released_prepublication_source_code"].update(qualifies="ACTUAL_PARTICIPANT_LOGS"),
 lambda x:x["permanent_exclusions"]["publication_unresolved_figS2"].update(figure_diagram={"trident":.69,"planet":.31}),
 lambda x:x["permanent_exclusions"]["publication_unresolved_figS2"].update(publisher_supplement_figS2_official_correction_issued=True),
 lambda x:x["permanent_exclusions"].update(author_manuscript_internal_discrepancies=[]),
 lambda x:x["eligibility"].update(all_original_publication_text_stats_and_pixels_fully_reconciled=True),
 lambda x:x["eligibility"].update(exact_participant_level_statistical_replication=True),
 lambda x:x["eligibility"].update(global_family_independence="QUALIFIED"),
 lambda x:x["eligibility"].update(final_MAIN40_global_g2_admission=True),
 lambda x:x["eligibility"].update(main40_roster_edited=True),
 lambda x:x["eligibility"].update(backup_activated=True),
 lambda x:x["eligibility"].update(g4_independent_second_assessor_approval=True),
 lambda x:x["eligibility"].update(main_authorized=True),
]
for i,modify in enumerate(alter):
    m=copy.deepcopy(D);modify(m)
    try:check(m)
    except AssertionError:continue
    raise AssertionError("FAIL_MUTATION_NOT_REJECTED_"+str(i+1))
print(f"PASS {len(alter)}/{len(alter)} destructive false original-edition/S2/task-code/full-family/MAIN promotion rejects")
print("NOT a participant level replay, independent full source-pixel audit, G4 joint science approval, or MAIN license")
