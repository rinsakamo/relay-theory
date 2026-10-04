#!/usr/bin/env python3
"""G2-D INT02 v14 exact SOURCE evidence metadata consistency and false promotion guards.
Neither passing tests nor SHA receipts prove the mathematical scientific hypothesis.
"""
import copy,hashlib,json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parent
M=HERE/"G2D_V14_INT02_PUBLISHER_ALL_MATH_FIGURES_AND_CODE_TYPED_DECISIONS.json"
R=HERE/"G2D_V14_INT02_ORIGINAL_FULL_MAIN_MATH_FIG8_AUTHOR_CODE_ADVERSE_JA_20261004.md"
SHA="a1e644c826bf1b356187bc556d5947eb23638f3f9bc6c61835d46850b4f1cc37"
def check(d):
 assert d["frozen_g2_head"]=="69748673c80f421605f1c63607472903ac2ed68c"
 assert d["g2_original_roster_unchanged"]
 assert d["grammar_decomposition_performed"] is False
 assert d["main_results_previews_inspected"] is False
 assert d["main_authorized"] is False and d["backup_actively_adopted"]==0
 src=d["published_original"]
 assert src["raw_sha256"]==SHA and src["raw_bytes"]==2814783 and src["pages"]==14
 assert src["exact_frozen_original_g2_v5_sha_match"] and src["real_original_firstparty_acquisition_run"]==37209569351
 assert src["firstparty_MDPI_article_HTML_direct_HTTP"]==403 and src["firstparty_MDPI_article_PDF_direct_HTTP"]==403
 assert src["firstparty_MDPI_official_media_HTTP"]==200 and not src["third_party_full_VOR_substitution"]
 v=d["full_original_main_page_visual_review"]
 assert v["actual_run"]==37209720541 and v["successful_jobs"]==v["raw_SHA_check_independent_jobs"]==5
 assert v["total_source_pdf_pages_image_rendered_and_inspected"]==14
 assert v["main_figure_number_ids_image_examined"]==[1,2,3,4,5,6,7,8]
 assert v["main_published_equation_printed_number_range"]=="(1) through (17)"
 assert v["original_first_locator_figure_lists_falsely_empty_due_regex"] and v["initial_locator_failure_history_preserved"]
 assert v["corrected_locator_run"]==37209913343 and v["corrected_all_eight_figure_labels_detected"]
 assert all(v["corrected_fig_caption_candidate_1based"][str(i)] for i in range(1,9))
 assert not v["automatic_all_scientific_truth_verification"]
 s=d["scientific_source_native_model"]
 assert s["prior_work_DPEFE_planning_explicitly_inherited"] and s["prior_work_CL_counterfactual_risk_explicitly_inherited"]
 assert not s["independent_invention_of_prior_DPEFE_or_CL_claimed"]
 assert s["paper_eq9_prints_unnormalized_geometric_action_pool"]
 assert not s["paper_eq9_printed_Z_normalization_symbol_explicit"]
 assert s["paper_eq8_local_linear_approx_to_eq16_under_small_entropy_difference"]
 assert not s["entropy_bias_is_explicit_measured_runtime_or_training_data_count_controller"]
 a=d["author_linked_original_code"]
 assert a["github_original_historical_commit"]=="9922288952a4f999d0e272e6ab7416ba433b1923"
 assert a["historical_raw_blob_sha"]=="e50c062847dd779e17077d6bda20ceb7dec92395"
 assert a["historical_code_lines"]["softmax_normalization"]==149
 assert a["historical_code_lines"]["logweighted_product_unnormalized"]==148
 assert a["historical_code_lines"]["beta_clipped_to_0_1"]==144
 assert a["historical_code_includes_softmax_normalization"]
 assert not a["source_original_eq9_omission_equals_implementation_probabilities_invalid"]
 assert not a["historical_specific_code_has_separate_exposed_alpha_parameter_for_beta_update"]
 assert not a["independent_reexecute_author_code_and_numeric_seeds_performed"]
 assert len(d["material_original_negatives"])==9
 assert all(n["preserved"] for n in d["material_original_negatives"])
 assert d["original_science_decision"]=="PUBLISHER_FULL_MAIN14P_ALL_EQUATIONS1_17_AND_FIGURES1_8_BOUNDED_SOURCE_NATIVE_VISUAL_REVIEW_COMPLETE"
 for k in ("official_edition_correction_global_absence_proven","independent_author_model_numeric_reproducibility_verified","selected_INT02_vs_all_G1_MAIN40_global_family_independent","selected_INT02_full_final_global_scientific_freeze"):
  assert d[k] is False
 assert d["g2d_overall"]=="G2_D_PARTIAL_MAIN_NOT_AUTHORIZED"
class TestSourceOnly(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=json.loads(M.read_text(encoding="utf-8"))
 def test_original_main_publisher_math_figures_receipts(self):check(self.d)
 def test_append_only_text_source_witness(self):
  s=R.read_text(encoding="utf-8")
  for witness in ("37209569351","37209720541","37209913343",SHA,"Eq9","Eq16","Fig1","Fig8","9922288952a4f999d0e272e6ab7416ba433b1923","MAIN_NOT_AUTHORIZED"):
   self.assertIn(witness,s)
 def test_seventeen_destructive_false_promotions_rejected(self):
  mutations=[
   (("g2_original_roster_unchanged",),False),
   (("main_authorized",),True),
   (("backup_actively_adopted",),1),
   (("published_original","raw_sha256"),"falseSHA"),
   (("published_original","pages"),13),
   (("published_original","third_party_full_VOR_substitution"),True),
   (("full_original_main_page_visual_review","successful_jobs"),4),
   (("full_original_main_page_visual_review","original_first_locator_figure_lists_falsely_empty_due_regex"),False),
   (("full_original_main_page_visual_review","corrected_all_eight_figure_labels_detected"),False),
   (("full_original_main_page_visual_review","automatic_all_scientific_truth_verification"),True),
   (("scientific_source_native_model","independent_invention_of_prior_DPEFE_or_CL_claimed"),True),
   (("scientific_source_native_model","paper_eq9_printed_Z_normalization_symbol_explicit"),True),
   (("author_linked_original_code","historical_code_includes_softmax_normalization"),False),
   (("author_linked_original_code","independent_reexecute_author_code_and_numeric_seeds_performed"),True),
   (("official_edition_correction_global_absence_proven",),True),
   (("selected_INT02_vs_all_G1_MAIN40_global_family_independent",),True),
   (("selected_INT02_full_final_global_scientific_freeze",),True)]
  for path,invalid in mutations:
   copy_d=copy.deepcopy(self.d);v=copy_d
   for key in path[:-1]:v=v[key]
   v[path[-1]]=invalid
   with self.subTest(path=path),self.assertRaises(AssertionError):check(copy_d)
if __name__=="__main__":
 print("G2D_V14_RAW_UTF8_SHA256",[(f.name,hashlib.sha256(f.read_bytes()).hexdigest()) for f in (M,R)])
 unittest.main()
