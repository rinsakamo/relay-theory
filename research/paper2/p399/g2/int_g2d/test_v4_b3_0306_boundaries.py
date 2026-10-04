#!/usr/bin/env python3
"""Non-semantic fail-closed regression tests; source science interpreted in v4 report, not by tests."""
import unittest,json,copy,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent
P=D/"G2D_V4_B3_ADVERSE_0306_SELECTED_PAIR_SOURCE_BOUNDARIES.json"
R=D/"G2D_V4_B3_REPRODUCIBILITY_AND_SELECTED_0306_FAMILY_JA_20261004.md"
class Gates(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.d=json.loads(P.read_text())
 def test_parent_no_main(self):
  d=self.d
  self.assertEqual(d["frozen_g2_base"],"69748673c80f421605f1c63607472903ac2ed68c")
  self.assertFalse(d["joint_freeze"]["any_backup_activated"])
  self.assertFalse(d["joint_freeze"]["MAIN_authorization"])
  self.assertFalse(d["joint_freeze"]["all_global_main_model_families_cleared"])
 def test_actual_b3_pub_source(self):
  b=self.d["item_B3"]
  self.assertEqual(b["original_pdf_expected_sha256"],"9e13535592ff1cf36c9eb4a9a1daae23cb6dfa8a916a40586a6cc5c651b80d35")
  self.assertEqual(b["pdf_pages_expected"],35)
  self.assertTrue(b["model_core_existing_spectral_DCM_SPM12"])
  self.assertTrue(b["model_core_existing_PPI"])
  self.assertFalse(b["new_independent_generative_cognitive_control_algorithm_proven"])
  self.assertTrue(b["new_indices_distinguishable_from_new_generative_algorithm"])
  self.assertFalse(b["activation"])
 def test_preserve_adverse_and_positive(self):
  b=self.d["item_B3"]
  self.assertEqual(b["smoothing8mm_ability_joint_prediction_r"],.32)
  self.assertEqual((b["smoothing4mm_ability_joint_prediction_r"],b["smoothing4mm_ability_joint_prediction_p"]),(.03,.44))
  self.assertTrue(b["retained_tms_effect_prediction"])
  self.assertEqual(b["domain_specific_TMS_prediction_r"],.03)
  self.assertEqual(len(b["source_native_negative_ids"]),5)
 def test_03_06_not_same_and_not_clear(self):
  q=self.d["selected_pair_03_06"]
  self.assertTrue(q["abstract_ancestry_related"])
  self.assertTrue(q["mechanistic_delta_present"])
  self.assertFalse(q["exact_same_central_model_proven"])
  self.assertFalse(q["fully_independent_central_family_proven"])
  self.assertIsNone(q["INT03"]["publisher_raw_original_pdf_sha256"])
  self.assertFalse(q["INT06"]["formal_text_S1_all_math_verified"])
 def test_13_version_hold(self):
  q=self.d["INT13"]
  self.assertTrue(q["publisher_text_uncorrected_proof"])
  self.assertFalse(q["final_corrected_version_physically_confirmed"])
  self.assertEqual(q["formal_qualification"],"HOLD_FINAL_EDITION")
 def test_report_critical_negatives_present(self):
  s=R.read_text()
  for v in ("r=0.03","p=0.44","r=0.56","r=0.03,p>0.3","1998","2010","uncorrected proof","SHARED_BROAD_WORKSPACE_ANCESTRY"):
   self.assertIn(v,s)
 def test_10_destructive_false_promotions_blocked(self):
  tests=[
   (("joint_freeze","any_backup_activated"),True),
   (("joint_freeze","MAIN_authorization"),True),
   (("joint_freeze","all_global_main_model_families_cleared"),True),
   (("item_B3","new_independent_generative_cognitive_control_algorithm_proven"),True),
   (("item_B3","activation"),True),
   (("item_B3","retained_tms_effect_prediction"),False),
   (("selected_pair_03_06","exact_same_central_model_proven"),True),
   (("selected_pair_03_06","fully_independent_central_family_proven"),True),
   (("INT13","final_corrected_version_physically_confirmed"),True),
   (("joint_freeze","g1_parallel_W2_eLife_39497_reservation_released"),True),
  ]
  for path,new in tests:
   original=copy.deepcopy(self.d); mutant=copy.deepcopy(self.d)
   a,b=original,mutant
   for item in path[:-1]:a,b=a[item],b[item]
   b[path[-1]]=new
   with self.subTest(path=path),self.assertRaises(AssertionError):self.assertEqual(a[path[-1]],b[path[-1]])
if __name__=="__main__":
 print("G2D_V4_INTERNAL_UTF8_HASHES",[(x.name,hashlib.sha256(x.read_bytes()).hexdigest()) for x in [P,R]])
 unittest.main()
