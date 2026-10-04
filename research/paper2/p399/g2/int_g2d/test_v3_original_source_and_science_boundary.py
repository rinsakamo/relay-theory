#!/usr/bin/env python3
"""G2-D v3 check receipts and invalid SCIENCE promotion claims only.
NOT an automated scientific model truth, full edition or global family proof.
"""
import copy, hashlib, json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parent
JSON=ROOT/"G2D_V3_APPEND_ONLY_SELECTED_INT_AND_SUPPLEMENT_MACHINE_DECISIONS.json"
MD=ROOT/"G2D_V3_INT06_B3_AND_B4_OFFICIAL_SUPPLEMENT_REVIEW_JA_20261004.md"
EXPECTED={
"INT-06":"c276294fa7a111e5df98f35aa0da933af28d45a1e1347940a1b57753c0980706",
"INT-06-S7":"ceec10ca95ae7bd2207d95c1ddb45098f2dc9741697c3608497dc2efd9b33bb5",
"INT-06-S8":"0813b44b5770f03b833a0623da876a76dde6e2ee5cd8dcbaf5ec8257fa04b504",
"INT-B4-S1":"64f1e1f18bb51909e89b22112929125914ccff75c2ffd1c91ace4851ae091e88"
}
def check(d):
 assert d["frozen_parent_g2_head"]=="69748673c80f421605f1c63607472903ac2ed68c"
 assert d["g2_shared_roster_mutated"] is False
 assert d["original_failures_retained"] and not d["main_scientific_results_not_inspected"] is False
 assert d["main_grammar_decomposition_performed"] is False
 assert d["global_family_qualified"] is False
 assert d["author_main_authorized"] is False
 assert d["backup_activated_count"]==0
 r=d["real_physical_run"]
 assert r["run_id"]==37198446072 and r["run_result"]=="success"
 assert r["physical_true_count"]==r["physical_target_count"]==4
 assert not r["first_attempt"] and not r["generic_gcs_host_permitted"]
 assert r["first_invalid_rejection_runs"]==[37198377401,37198431676]
 assert set(e["slot"] for e in d["new_original_sources"])==set(EXPECTED)
 for e in d["new_original_sources"]:
  assert e["raw_sha256"]==EXPECTED[e["slot"]]
  assert e["scientific_whole_original_qualified"] is False
 assert d["original_central_decisions"]["INT-06"]["shares_global_workspace_abstract_architecture_with_INT03"]
 assert d["original_central_decisions"]["INT-06"]["new_concrete_spiking_router_dual_task_order_circuit_differential"]
 assert d["original_central_decisions"]["INT-06"]["pairwise_distinct_original_mathematical_family_final"] is False
 b3=d["backup_decisions"]["INT-B3"]
 assert b3["original_vor_pdf_sha256"]=="9e13535592ff1cf36c9eb4a9a1daae23cb6dfa8a916a40586a6cc5c651b80d35"
 assert b3["novel_emprical_network_topology_beyond_prior_six_PFC"]
 assert not b3["novel_independent_spDCM_PPI_learning_algorithm_demonstrated"]
 assert b3["important_original_negatives"]["PPI_sensory_motor_r"]==-0.06
 assert b3["important_original_negatives"]["reduced_smoothing_integration_predicts_cognitive_ability_failed_replication"]
 assert b3["g2_cross_lane_exact_shared_backup"]=="CTL-B1" and not b3["activated"]
 b4=d["backup_decisions"]["INT-B4"]
 assert b4["publisher_S1_source_physically_acquired_now"]
 assert b4["main_printed_equation_15_equal_K_case_unresolved"]
 assert not b4["all_S1_figure_pixels_visually_audited"]
 assert not b4["published_code_K_equality_branch_matched"]
 assert not b4["final_global_model_family_independence"]
 assert b4["source_native_supplement_text_negatives"]["BIC_overpenalizes_complex_models_in_recovery"]
 assert b4["source_native_supplement_text_negatives"]["fig_D_n_per_generating_model"]==492
 assert set(b4["supplement_main_figure_letter_page_1based"])==set("ABCDEFG")
 assert not b4["activated"]
 assert all(x is False for x in d["still_pending"].values())
class TestG2DV3(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.doc=json.loads(JSON.read_text())
 def test_full_machine_ledger_gates(self):check(self.doc)
 def test_append_only_prose_matches_primary_official_source(self):
  t=MD.read_text()
  for s in ("37198446072","37198377401","37198431676","ceec10ca95","64f1e1f18","r=-0.06","0.004","0.001","INT03/06","Eq(15a,b)"):
   self.assertIn(s,t)
 def test_destructive_16_false_promotions_rejected(self):
  edits=[
   (("g2_shared_roster_mutated",),True),
   (("main_scientific_results_not_inspected",),False),
   (("main_grammar_decomposition_performed",),True),
   (("global_family_qualified",),True),
   (("backup_activated_count",),1),
   (("real_physical_run","generic_gcs_host_permitted"),True),
   (("real_physical_run","physical_true_count"),1),
   (("new_original_sources",0,"raw_sha256"),"fake"),
   (("new_original_sources",1,"scientific_whole_original_qualified"),True),
   (("original_central_decisions","INT-06","pairwise_distinct_original_mathematical_family_final"),True),
   (("backup_decisions","INT-B3","novel_independent_spDCM_PPI_learning_algorithm_demonstrated"),True),
   (("backup_decisions","INT-B3","activated"),True),
   (("backup_decisions","INT-B3","important_original_negatives","reduced_smoothing_integration_predicts_cognitive_ability_failed_replication"),False),
   (("backup_decisions","INT-B4","main_printed_equation_15_equal_K_case_unresolved"),False),
   (("backup_decisions","INT-B4","all_S1_figure_pixels_visually_audited"),True),
   (("backup_decisions","INT-B4","activated"),True)
  ]
  for path,change in edits:
   m=copy.deepcopy(self.doc);target=m
   for key in path[:-1]:target=target[key]
   target[path[-1]]=change
   with self.subTest(path=path),self.assertRaises(AssertionError):check(m)
if __name__=="__main__":
 print("G2D_V3_RAW_BYTES",[(p.name,hashlib.sha256(p.read_bytes()).hexdigest()) for p in (JSON,MD)])
 unittest.main()
