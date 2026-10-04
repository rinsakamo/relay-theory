#!/usr/bin/env python3
"""Actual firstparty source receipt and two false-negative histories.
Tests reject false scientific promotion; passing does not compute model truth.
"""
import json,pathlib,copy,hashlib,unittest
ROOT=pathlib.Path(__file__).parent
P=ROOT/"G2D_V10D_CORRECTED_PAIR_SOURCE_NATIVE_MACHINE_GATES.json"
D=ROOT/"G2D_V10D_INT08_CORRECTED_SOURCE_NATIVE_WITNESS_APPEND_ONLY_JA_20261004.md"
def guard(x):
 assert x["frozen_parent_g2_head"]=="69748673c80f421605f1c63607472903ac2ed68c" and not x["g2_shared_original_40_mutated"]
 a=x["official_sources"]["INT-04"];b=x["official_sources"]["INT-08"]
 assert a["actual_v9_reread_run"]==37205772232 and a["v9_two_independent_same_sha_jobs_both_success"]
 assert a["publisher_main_figure_ids_visually_reviewed"]==list(range(1,8))
 assert a["publisher_science_supp_figure_ids_visually_reviewed"]==[1,2,3]
 assert a["publisher_supp_printed_eqs_visually_reviewed"]==[1,2,3]
 assert not a["code_independent_training_reproduced"] and not a["science_full_global_family_qualified"]
 assert b["first_raw_independent_source_verified_run"]==37206108178
 assert b["publisher_original_pages"]==43 and b["publisher_original_bytes"]==4476771
 assert b["exact_G2_inherited_raw_sha256"]=="89f8846ab34dbc5af0d4079423ff51e00c1873b6149c48217b547b1bdcb678da"
 assert [b[k] for k in ("strict_false_negative_literal_run","strict_false_negative_regexp_double_escape_run","corrected_exact_same_original_run")]==[37206213517,37206294340,37206404322]
 assert b["source_reacquired_on_corrected_run"]
 assert b["manual_policy_hand_imposed_detected_on_corrected_run"] and b["manual_policy_source_page_1based"]==[6]
 assert b["human_RM_DM_NM_task_manual_end_event_encoding"] and b["learned_LSTM_neocortical_LCA_gated_episodic_retrieval"]
 assert not b["all_43_pages_figure_and_appendix_math_pixel_audited"] and not b["full_global_family_science_qualified"]
 pair=x["source_native_pairwise_delta"]
 assert pair["distinct_local_primary_learning_target_and_operations_source_confirmed"]
 assert pair["INT08_human_scenarios_end_of_event_encoding_hand_set"] and not pair["INT08_all_encoding_policies_joint_end_to_end_free_learned"]
 assert not pair["pairwise_all_figures_math_complete_qualified"] and not pair["full_G1_20_G2_40_independent_family_cleared"]
 assert len(x["negative_claims"])==7 and not x["all_selected_INT_global_full_scientific_qualified"]
 assert not x["any_backup_formally_activated"] and not x["MAIN_scientific_decomposition_performed"] and not x["MAIN_preliminary_scientific_results_read"] and not x["MAIN_authorized"]
class T(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.x=json.loads(P.read_text())
 def test_authoritative_limited_original_provenance(self):guard(self.x)
 def test_source_correction_note(self):
  s=D.read_text()
  for x in ("37206213517","37206294340","37206404322","4,476,771","[6]","false"):
   self.assertIn(x.lower(),s.lower())
 def test_thirteen_destructive_false_promotions(self):
  cases=[
   (("g2_shared_original_40_mutated",),True),
   (("official_sources","INT-04","publisher_main_figure_ids_visually_reviewed"),[1,2]),
   (("official_sources","INT-04","code_independent_training_reproduced"),True),
   (("official_sources","INT-08","exact_G2_inherited_raw_sha256"),"FAKE"),
   (("official_sources","INT-08","publisher_original_pages"),2),
   (("official_sources","INT-08","manual_policy_hand_imposed_detected_on_corrected_run"),False),
   (("official_sources","INT-08","manual_policy_source_page_1based"),[]),
   (("official_sources","INT-08","all_43_pages_figure_and_appendix_math_pixel_audited"),True),
   (("source_native_pairwise_delta","INT08_all_encoding_policies_joint_end_to_end_free_learned"),True),
   (("source_native_pairwise_delta","pairwise_all_figures_math_complete_qualified"),True),
   (("source_native_pairwise_delta","full_G1_20_G2_40_independent_family_cleared"),True),
   (("any_backup_formally_activated",),True),
   (("MAIN_authorized",),True)]
  for path,v in cases:
   m=copy.deepcopy(self.x);q=m
   for k in path[:-1]:q=q[k]
   q[path[-1]]=v
   with self.subTest(path=path),self.assertRaises(AssertionError):guard(m)
if __name__=="__main__":
 print("V10D_RAW_UTF8_SHA256",[(f.name,hashlib.sha256(f.read_bytes()).hexdigest()) for f in (P,D)])
 unittest.main()
