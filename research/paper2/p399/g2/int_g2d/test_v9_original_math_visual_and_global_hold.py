#!/usr/bin/env python3
"""v9 exact first-party INT04 source-level visual/printed-math claim integrity.
All assertions guard AUTHORED ORIGINAL RECEIPT, not automated mathematics truth.
"""
import json,pathlib,copy,hashlib,unittest
P=pathlib.Path(__file__).parent
J=P/"G2D_V9_INT04_ALL_MAIN_SUPP_VISUAL_MATH_BOUNDED_DECISIONS.json"
M=P/"G2D_V9_INT04_FULL_MAIN_FIGS_SUPP_ALL_PAGES_MATH_AND_ADVERSE_JA_20261004.md"
SHAS=["b78a62b28775ec55610aeeca2252bc43b1ba782486c083a5065a3419ed3cde31","6f9baebc2f95492b4ce275c64ed0cb640105cd480d401b78dee09c5abbb03612","a9b713fbc8d39e24534ecaceb9c6deb53f13d36b0ec21843130bb69f67ad93bf"]
def guard(o):
 assert o["frozen_g2_parent_sha"]=="69748673c80f421605f1c63607472903ac2ed68c"
 r=o["git_actions_run_37205772232"]
 assert r["run_id"]==37205772232 and r["matrix_job_results"]=={"main":"success","supp":"success"}
 assert r["per_job_three_firstparty_media_original_raw_exact_reacquired"]
 assert r["main_extra_pages_true_original_visual_reviewed"]==[5,6,7,8,9,10,11,12,13,14]
 assert r["main_prior_v8_original_fig1_fig2_reviewed_page_nums"]==[3,4]
 assert r["supp_all_publisher_science_original_pages_visually_reviewed"]==list(range(1,10))
 assert [s["raw_sha256"] for s in o["publisher_sources"]]==SHAS
 assert [s["original_pages"] for s in o["publisher_sources"]]==[20,9,2]
 assert [s["bytes"] for s in o["publisher_sources"]]==[2666492,2912573,47812]
 t=o["local_original_visual_science"]
 assert t["main_printed_figure_ids_all_reviewed"]==list(range(1,8))
 assert t["supp_printed_figure_ids_all_reviewed"]==[1,2,3]
 assert t["supp_printed_equations_original_source_checked"]==[1,2,3]
 assert t["supp_Eq1_classical_Hopfield_existing"] and t["supp_Eq2_dense_polynomial_energy_existing"] and t["supp_Eq3_modern_Hopfield_softmax_X_beta_Xt_xi_existing"]
 assert not t["claimed_first_invention_of_prior_mhn_or_vae"]
 assert not t["code_executed_and_independently_result_reproduced"] and not t["full_global_scientific_independence_clearance"]
 assert t["individual_original_main_and_supp_figures_math_source_native_bounded_review_completed"]
 assert t["fig5_threshold_up_fewer_hippocampal_sensory_stored_and_higher_reconstruction_error"]
 assert t["fig7_drm_400_simulated_trials_not_400_human_subjects"]
 assert len(o["negative_evidence_ids"])==8
 bad=o["bad_claim_guard"]
 for k in ["basic_autoassociative_MHN_capacity_constraint_simulated","basic_decay_deletion_simulated","basic_prediction_error_event_only_storage_simulated","standard_backprop_biological_validity_proven","all_lifelong_sequential_catastrophic_forgetting_solved","multiple_modalities_one_training_simultaneously_modelled","claimed_400_new_human_DRM_subjects","claimed_supp_prior_Fig3_face_transforms_new_dataset"]:
  assert bad[k] is False,k
 assert bad["extended_pixel_wise_prediction_error_threshold_really_applied"]
 pair=o["INT04_vs_INT08"]
 assert pair["source_native_local_difference_bounded"] and pair["broad_memory_neocortical_hpc_ancestry_shared"]
 assert not pair["pairwise_exact_complete_math_and_figures_independence_proven"]
 for k in ["INT01_full_Elsevier_publisher_original_acquired","INT03_new_exact_PNAS_publisher_source_reacquired","INT13_final_corrected_publisher_edition_verified","INTB1_distinct_from_INT12_crp_parent","INTB2_G1_P12_release","INTB3_CTL_B1_duplicate_cleared","INTB4_global_RLWM_parent_math_cleared","all_selected_INT_original_full_science_qualified","all_G1_PILOT20_final_roster_frozen","full_global_central_model_family_all_qualified","MAIN_scientific_reconstruction_performed","MAIN_results_inspected","MAIN_authorized"]:
  assert o["current_global_gates"][k] is False,k
 assert o["current_global_gates"]["backup_formally_activated_count"]==0
class Checks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.o=json.loads(J.read_text(encoding="utf-8"))
 def test_all_actual_source_bounds(self):guard(self.o)
 def test_prose_signals(self):
  t=M.read_text()
  for x in ["37205772232","supp Fig1","supp Fig2","supp Fig3","数式(1)","数式(3)","Fig5","Fig7","未実装","MAIN_NOT_AUTHORIZED"]:
   self.assertIn(x.lower(),t.lower())
 def test_17_destructive_fake_promotions(self):
  edits=[
   (("git_actions_run_37205772232","matrix_job_results","supp"),"failure"),
   (("git_actions_run_37205772232","supp_all_publisher_science_original_pages_visually_reviewed"),[1,2]),
   (("publisher_sources",0,"raw_sha256"),"fake"),
   (("publisher_sources",1,"raw_sha256"),"fake"),
   (("publisher_sources",2,"original_pages"),9),
   (("local_original_visual_science","main_printed_figure_ids_all_reviewed"),[1,2]),
   (("local_original_visual_science","supp_printed_equations_original_source_checked"),[1]),
   (("local_original_visual_science","claimed_first_invention_of_prior_mhn_or_vae"),True),
   (("local_original_visual_science","code_executed_and_independently_result_reproduced"),True),
   (("local_original_visual_science","full_global_scientific_independence_clearance"),True),
   (("bad_claim_guard","basic_decay_deletion_simulated"),True),
   (("bad_claim_guard","basic_prediction_error_event_only_storage_simulated"),True),
   (("bad_claim_guard","claimed_400_new_human_DRM_subjects"),True),
   (("INT04_vs_INT08","pairwise_exact_complete_math_and_figures_independence_proven"),True),
   (("current_global_gates","INT13_final_corrected_publisher_edition_verified"),True),
   (("current_global_gates","backup_formally_activated_count"),1),
   (("current_global_gates","MAIN_authorized"),True)
  ]
  for path,wrong in edits:
   o=copy.deepcopy(self.o);x=o
   for k in path[:-1]:x=x[k]
   x[path[-1]]=wrong
   with self.subTest(path=path),self.assertRaises(AssertionError):guard(o)
if __name__=="__main__":
 print("V9_ACTUAL_RECORD_BYTES",[(p.name,hashlib.sha256(p.read_bytes()).hexdigest()) for p in (J,M)])
 unittest.main()
