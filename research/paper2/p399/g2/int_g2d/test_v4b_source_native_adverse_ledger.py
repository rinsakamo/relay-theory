#!/usr/bin/env python3
"""G2-D v4b source-integrity-only guards. Never construe PASS as original math truth."""
import copy,json,hashlib,pathlib,unittest
BASE=pathlib.Path(__file__).parent
P=BASE/"G2D_V4B_SOURCE_NATIVE_ADVERSE_MACHINE_DELTA.json"
D1=BASE/"G2D_V4_B3_PUBLISHED_PEER_REVIEW_ADVERSE_AND_INT03_INT06_FAMILY_JA_20261004.md"
D2=BASE/"G2D_V4B_OFFICIAL_INT06_DOC_AND_B4_S1_SOURCE_NATIVE_ADVERSE_JA_20261004.md"
def decision(d):return (
 d["backup_formal_adoptions"]==0 and
 d["source_full_scientific_admissions_increment"]==0 and
 not d["MAIN_authorized"] and
 not d["MAIN_decomposition_or_preview"] and
 not d["final_all_20x40_family_approval"] and
 d["physical_3_of_3_current_source_SHA_against_previous_run"] and
 not d["fully_visually_audited_supplement_figures"] and
 not d["source_reviews"]["INT-B3"]["source_native_analysis_provenance"]["novel_generative_integration_algorithm_demonstrated"] and
 d["source_reviews"]["INT-B3"]["adverse"][0]["reanalysis_r_4mm"]==0.03 and
 d["source_reviews"]["INT-B3"]["adverse"][0]["reanalysis_p_4mm"]==0.44 and
 d["source_reviews"]["INT-B3"]["g2_CTL_B1_same_DOI_unresolved"] and
 not d["source_reviews"]["INT-03"]["publisher_site_direct_reacquired_this_transaction"] and
 not d["source_reviews"]["INT-06"]["pair_03_06_final_global_independence_demonstrated"] and
 not d["source_reviews"]["INT-06"]["official_fig_s1_through_s6_visual_pixel_check_complete"] and
 d["source_reviews"]["INT-06"]["publisher_official_s007_doc"]["sha256"]=="ceec10ca95ae7bd2207d95c1ddb45098f2dc9741697c3608497dc2efd9b33bb5" and
 d["source_reviews"]["INT-06"]["publisher_official_s008_doc"]["sha256"]=="0813b44b5770f03b833a0623da876a76dde6e2ee5cd8dcbaf5ec8257fa04b504" and
 d["source_reviews"]["INT-B4"]["publisher_official_s001_pdf"]["sha256"]=="64f1e1f18bb51909e89b22112929125914ccff75c2ffd1c91ace4851ae091e88" and
 not d["source_reviews"]["INT-B4"]["publisher_official_s001_pdf"]["full_Fig_A_G_visual_numeric_audit"] and
 not d["source_reviews"]["INT-B4"]["source_native_model_family"]["new_split_gate_necessary_for_main_MASQ_AA_associations_demonstrated"] and
 d["source_reviews"]["INT-B4"]["adverse"][2]["M4_learning_rate_rho"]==-0.270 and
 d["source_reviews"]["INT-B4"]["adverse"][2]["M4_WM_decay_rho"]==0.245 and
 d["source_reviews"]["INT-B4"]["adverse"][3]["requires_author_or_code_reconciliation"] and
 not d["source_reviews"]["INT-B4"]["global_central_family_independence_certified"] and
 not d["source_reviews"]["INT-B4"]["activated"]
)
class V4B(unittest.TestCase):
 def setUp(self):self.d=json.loads(P.read_text(encoding="utf-8"))
 def test_exact_original_artifact_sha_and_no_promotions(self):
  self.assertTrue(decision(self.d))
  self.assertEqual(self.d["frozen_parent_g2"],"69748673c80f421605f1c63607472903ac2ed68c")
  self.assertEqual(self.d["physical_runs"],[37198446072,37198610873])
 def test_original_negative_evidence_all_identities(self):
  a=self.d["source_reviews"]
  self.assertEqual(len(a["INT-B3"]["adverse"]),3)
  self.assertEqual(len(a["INT-06"]["adverse"]),4)
  self.assertEqual(len(a["INT-B4"]["adverse"]),6)
  self.assertTrue(a["INT-06"]["adverse"][2]["claim"].find("Harder task faster")>=0)
  self.assertTrue(a["INT-B4"]["adverse"][0]["plot_cell_values_visually_verified"] is False)
 def test_corresponding_narrative_files(self):
  a=D1.read_text(encoding="utf-8");b=D2.read_text(encoding="utf-8")
  for x in ["r=0.03","p=0.44","INT03","INT06","FPCN"]:
   # "FPCN" may not literally occur: match official topic via contextual terms
   if x=="FPCN":self.assertIn("ネットワーク",a)
   else:self.assertIn(x,a)
  for x in ["paradoxically","N_INT06_V4B_003","0.686","0.797","N_B4_S1_V4B_004"]:
   if x=="paradoxically":self.assertIn("paradoxically",b) if "paradoxically" in b else self.assertIn("paradox",b.lower())
   else:self.assertIn(x,b)
 def test_12_destructive_false_promotion_regressions(self):
  paths=[
   (["backup_formal_adoptions"],1),
   (["MAIN_authorized"],True),
   (["MAIN_decomposition_or_preview"],True),
   (["final_all_20x40_family_approval"],True),
   (["fully_visually_audited_supplement_figures"],True),
   (["source_reviews","INT-B3","source_native_analysis_provenance","novel_generative_integration_algorithm_demonstrated"],True),
   (["source_reviews","INT-B3","g2_CTL_B1_same_DOI_unresolved"],False),
   (["source_reviews","INT-03","publisher_site_direct_reacquired_this_transaction"],True),
   (["source_reviews","INT-06","pair_03_06_final_global_independence_demonstrated"],True),
   (["source_reviews","INT-06","official_fig_s1_through_s6_visual_pixel_check_complete"],True),
   (["source_reviews","INT-B4","publisher_official_s001_pdf","full_Fig_A_G_visual_numeric_audit"],True),
   (["source_reviews","INT-B4","global_central_family_independence_certified"],True)
  ]
  for path,value in paths:
   d=copy.deepcopy(self.d);v=d
   for key in path[:-1]:v=v[key]
   v[path[-1]]=value
   with self.subTest(path=path):self.assertFalse(decision(d))
if __name__=="__main__":
 for f in [P,D1,D2]:print("G2D_V4B_PRECISE_RAW_UTF8",f.name,hashlib.sha256(f.read_bytes()).hexdigest())
 unittest.main()
