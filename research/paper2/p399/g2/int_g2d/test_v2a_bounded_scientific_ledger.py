#!/usr/bin/env python3
"""G2-D v2a machine integrity and explicitly false promotion regression only.
Passing does NOT independently establish correctness of original mathematical semantics.
"""
import json, pathlib, unittest, copy, hashlib
HERE=pathlib.Path(__file__).resolve().parent
P=HERE/"G2D_V2A_APPEND_ONLY_MACHINE_BOUNDED_DECISIONS.json"
C=HERE/"G2D_V2A_APPEND_ONLY_CORRECTION_ALL_MAIN_EQUATIONS_AND_BROWSER_JA_20261004.md"
class G2DV2A(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.d=json.loads(P.read_text(encoding="utf-8"))
 def test_immutable_and_no_main(self):
  d=self.d
  self.assertEqual(d["base_g2_head"],"69748673c80f421605f1c63607472903ac2ed68c")
  self.assertTrue(d["do_not_mutate_predecessors"])
  self.assertTrue(d["main_scientific_reconstruction_not_performed"])
  self.assertFalse(d["global_family_clearance"])
  self.assertEqual(d["backup_formally_activated"],0)
  self.assertFalse(d["author_main_approval"])
 def test_original_edition_fail_closed(self):
  a=self.d["items"]
  self.assertFalse(a["INT-01"]["firstparty_full_VOR_acquired"])
  self.assertEqual(len(a["INT-01"]["attempted_routes"]),5)
  self.assertTrue(all(not r["accepted"] for r in a["INT-01"]["attempted_routes"]))
  self.assertTrue(a["INT-13"]["publisher_html_explicit_uncorrected_proof"])
  self.assertFalse(a["INT-13"]["final_VOR_verified"])
 def test_backup_priority_and_original_science_counts(self):
  a=self.d["items"]
  self.assertEqual([a[f"INT-B{i}"]["doi"] for i in range(1,5)],[
   "10.1371/journal.pcbi.1007720","10.7554/eLife.39497",
   "10.7554/eLife.57244","10.1371/journal.pcbi.1012872"])
  self.assertTrue(all(not a[f"INT-B{i}"]["activated"] for i in range(1,5)))
  self.assertFalse(a["INT-B1"]["inherited_int12_central_math"]["new_independent_central_CRP_algorithm_proven"])
  self.assertFalse(a["INT-B2"]["g1_W2_eLife_reservation_relinquished"])
  self.assertEqual(a["INT-B3"]["shared_with"],"CTL-B1")
  self.assertFalse(a["INT-B3"]["new_independent_integration_math_verified"])
  self.assertEqual(self.d["new_qualifications"]["new_full_scientific_and_edition_source_qualified"],0)
  self.assertEqual(self.d["new_qualifications"]["global_central_family_qualified"],0)
 def test_original_math_counterexamples(self):
  b=self.d["items"]["INT-B4"];t=b["technical_distinctions"]
  self.assertEqual(b["full_primary_main_equation_number_range"],"(1) through (24b)")
  self.assertEqual(b["all_main_article_figure_ids_visually_inspected"],list(range(1,8)))
  self.assertEqual(b["main_article_table_ids_visually_inspected"],[1])
  self.assertFalse(b["supplementary_S1_recovery_figures_independently_audited"])
  self.assertFalse(b["crossmark_complete_correction_history_certified"])
  self.assertTrue(t["inherited_baseline_cooperative_RLWM_prediction_error"])
  self.assertTrue(t["new_split_confidence_for_setsize_below_vs_above_K"])
  self.assertTrue(t["printed_eq15_equal_setsize_and_capacity_unspecified"])
  self.assertFalse(t["silent_eq15_fix_permitted"])
  self.assertFalse(t["novel_independent_RLWM_coupling_proven"])
  self.assertEqual(b["model_space"]["RLWM_total"],6)
  self.assertEqual(b["model_space"]["RL_only_total"],10)
  self.assertEqual(b["model_space"]["aggregate_AIC_M4"],143718)
  self.assertEqual(b["model_space"]["aggregate_AIC_M5"],143629)
  self.assertTrue(b["model_space"]["M4_more_individual_winners_than_M5"])
  self.assertEqual(len(b["registered_material_negative_ids"]),6)
 def test_document_explicit_v2_omission_correction(self):
  s=C.read_text(encoding="utf-8")
  for v in ["式(17)","式(24b)","2基準+8追加=10","主本文","Eq(15a,b)","37197511423"]:
   self.assertIn(v,s)
 def test_ten_destructive_false_promotions_rejected(self):
  paths=[
   (("backup_formally_activated",),1),
   (("global_family_clearance",),True),
   (("items","INT-01","firstparty_full_VOR_acquired"),True),
   (("items","INT-13","final_VOR_verified"),True),
   (("items","INT-B1","inherited_int12_central_math","new_independent_central_CRP_algorithm_proven"),True),
   (("items","INT-B2","g1_W2_eLife_reservation_relinquished"),True),
   (("items","INT-B3","new_independent_integration_math_verified"),True),
   (("items","INT-B4","technical_distinctions","silent_eq15_fix_permitted"),True),
   (("items","INT-B4","technical_distinctions","novel_independent_RLWM_coupling_proven"),True),
   (("items","INT-B4","crossmark_complete_correction_history_certified"),True)]
  for path,changed in paths:
   original=copy.deepcopy(self.d);mutant=copy.deepcopy(self.d)
   a=original;b=mutant
   for part in path[:-1]:a=a[part];b=b[part]
   b[path[-1]]=changed
   with self.subTest(path=path),self.assertRaises(AssertionError):
    self.assertEqual(a[path[-1]],b[path[-1]])
if __name__=="__main__":
 print("v2a original/visual source claim exact UTF8 files",[(x.name,hashlib.sha256(x.read_bytes()).hexdigest()) for x in [P,C]])
 unittest.main()
