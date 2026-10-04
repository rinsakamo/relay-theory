#!/usr/bin/env python3
"""v8 bounded source metadata integrity/false scientific promotion guards.
Passing confirms exact authored receipts, NOT publisher PDF scientific truth.
"""
import copy,hashlib,json,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parent
J=ROOT/"G2D_V8_INT04_EXACT_ORIGINAL_RAW_AND_BOUNDED_FIGURES_MACHINE_GATES.json"
R=ROOT/"G2D_V8_INT04_ALL_PUBLISHER_MEDIA_RAW_REPRO_AND_SOURCE_FIG1_FIG2_JA_20261004.md"
MEDIA=[
 ("b78a62b28775ec55610aeeca2252bc43b1ba782486c083a5065a3419ed3cde31",20,2666492),
 ("6f9baebc2f95492b4ce275c64ed0cb640105cd480d401b78dee09c5abbb03612",9,2912573),
 ("a9b713fbc8d39e24534ecaceb9c6deb53f13d36b0ec21843130bb69f67ad93bf",2,47812)
]
def assert_provenance(d):
 assert d["starting_parent_G2_head"]=="69748673c80f421605f1c63607472903ac2ed68c"
 assert d["independent_draft_pr"]==430
 assert d["source_runner"]["id"]==37200273167 and d["source_runner"]["result"]=="success"
 assert d["source_runner"]["originals_exact_reacquired"]==3 and d["source_runner"]["source_pages_indexed"]==31
 assert d["source_runner"]["publisher_HTML_origin_required"] and d["source_runner"]["publisher_page_actual_links_required"]
 assert d["source_runner"]["precommitted_exact_previous_v7_raw_SHA_every_media_required"]
 assert not d["source_runner"]["all_source_math_semantically_qualified"]
 assert len(d["source_media"])==3
 for r,(sha,pages,bytes_) in zip(d["source_media"],MEDIA):
  assert (r["sha256"],r["pages"],r["bytes"])==(sha,pages,bytes_)
  assert r["independent_second_raw_SHA_exact_match"]
 assert d["source_media"][2]["reporting_summary_is_not_main_scientific_supplement"]
 vis=d["pixel_visual_audit_bounded"]
 assert vis["true_SHA_locked_Nature_main_original_rendered_as_JPEG_through_GHA_logs"]
 assert [x["Nature_main_pdf_page_1based"] for x in vis["real_images_inspected_by_reviewer"]]==[3,4]
 assert [x["original_figure"] for x in vis["real_images_inspected_by_reviewer"]]==["Fig1 basic a–g","Fig2 extended a–d"]
 assert not vis["other_main_article_figures_visually_checked"] and not vis["supplement_all_figures_pixels_checked"] and not vis["all_math_formula_rendered_verified"]
 bad=d["adverse_original_evidence"]
 assert bad["source_printed_text_confirms_not_simulated_capacity"]
 assert not bad["basic_autoassociative_module_decay_deletion_capacity_limits_actually_simulated"]
 assert not bad["basic_event_level_prediction_error_selective_encoding_explicitly_simulated"]
 assert bad["extended_fig2_sensory_error_selective_component_depicted"]
 assert not bad["component_MHN_initially_invented_in_this_article"] and not bad["component_VAE_initially_invented_in_this_article"]
 p=d["selected_INT04_INT08_pair"]
 assert p["observed_distinct_local_core_operations_source_native"]
 assert not p["full_global_independence_qualified"] and not p["all_original_main_and_supplemental_figure_comparison_completed"]
 assert d["INT04_full_physical_official_original_main_and_scientific_supplement_succeeded"]
 for flag in ("INT03_new_PNAS_original_reacquisition_succeeded","INT04_full_scientific_source_semantic_qualification","G2_original_40_shared_registry_changed","global_G1_pilot20_central_family_qualified","global_MAIN40_family_qualified","MAIN_scientific_reconstruction_performed","MAIN_results_inspected","MAIN_authorized"):
  assert d[flag] is False,flag
 assert d["authorized_backup_adoption_count"]==0
class Exact(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=json.loads(J.read_text())
 def test_v8_immutable_actual_source_receipts(self):assert_provenance(self.d)
 def test_original_visual_prose_trace(self):
  txt=R.read_text()
  for t in ("37200273167","31","20","9","b78a62b28775ec","6f9baebc2f954","a9b713fbc8d39","Fig1","Fig2","not simulated","MAIN_NOT_AUTHORIZED"):
   self.assertIn(t.lower(),txt.lower())
 def test_16_false_promotions_rejected(self):
  edits=[
   (("source_runner","originals_exact_reacquired"),2),
   (("source_runner","source_pages_indexed"),29),
   (("source_runner","publisher_page_actual_links_required"),False),
   (("source_media",0,"sha256"),"fake"),
   (("source_media",1,"independent_second_raw_SHA_exact_match"),False),
   (("source_media",2,"reporting_summary_is_not_main_scientific_supplement"),False),
   (("pixel_visual_audit_bounded","other_main_article_figures_visually_checked"),True),
   (("pixel_visual_audit_bounded","supplement_all_figures_pixels_checked"),True),
   (("pixel_visual_audit_bounded","all_math_formula_rendered_verified"),True),
   (("adverse_original_evidence","basic_autoassociative_module_decay_deletion_capacity_limits_actually_simulated"),True),
   (("adverse_original_evidence","component_VAE_initially_invented_in_this_article"),True),
   (("selected_INT04_INT08_pair","full_global_independence_qualified"),True),
   (("INT03_new_PNAS_original_reacquisition_succeeded",),True),
   (("INT04_full_scientific_source_semantic_qualification",),True),
   (("authorized_backup_adoption_count",),1),
   (("MAIN_authorized",),True)]
  for path,wrong in edits:
   m=copy.deepcopy(self.d);x=m
   for k in path[:-1]:x=x[k]
   x[path[-1]]=wrong
   with self.subTest(path=path),self.assertRaises(AssertionError):assert_provenance(m)
if __name__=="__main__":
 print("V8_RAW_UTF8_SHA256",[(x.name,hashlib.sha256(x.read_bytes()).hexdigest()) for x in (J,R)])
 unittest.main()
