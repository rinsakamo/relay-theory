#!/usr/bin/env python3
"""Exact nine original PLOS physical receipt metadata guards; NOT source science proof."""
import copy,hashlib,json,pathlib,unittest
P=pathlib.Path(__file__).resolve().parent
J=P/"G2D_V5_INT06_ALL_EIGHT_PUBLISHER_SUPPLEMENTS_AND_STOP_GATES.json"
R=P/"G2D_V5_INT06_ALL_8_OFFICIAL_SUPPLEMENTS_SOURCE_AND_NEGATIVE_JA_20261004.md"
S=["7923010b6449f00ff37807358af1a2ae46927dbeed142821a7225cec3b494bdb","d01181c75eb525c713935ffe6aad1229e0c0307af20398d2af2c7088159b411c","6f102a9de2ecd3aae3c8de0fbe3fa9ca947a65002156d7252cddeb427c108524","5b6be0840536fd9e21c0082e1dae0393258a32bcac942411b127285d0b5fa3ad","498c5cdfefb764ad8d3eb11d378d12a3179d3dcd7ceecdf6a606580703f5bc66","e3e2247e2676d97bedfe7cc83da3ab8b081e81a93dc26434516d771fc0d39049"]
def check(d):
 assert d["base_g2_head"]=="69748673c80f421605f1c63607472903ac2ed68c" and d["previous_int_documents_remain_unmodified"]
 assert d["main_original"]["raw_sha256"]=="c276294fa7a111e5df98f35aa0da933af28d45a1e1347940a1b57753c0980706"
 f=d["source_supplements"]["original_figure_TIFFs"]
 assert len(f)==6 and [x["raw_sha256"] for x in f]==S
 assert [x["doi"] for x in f]==[f"10.1371/journal.pcbi.1000765.s{i:03d}" for i in range(1,7)]
 assert all(x["original_mime"]=="TIFF" and x["firstparty_exact_source_signed_origin_verified"] and not x["semantic_all_pixel_figure_audit"] for x in f)
 assert d["source_supplements"]["official_doc_s007"]["sha256"]=="ceec10ca95ae7bd2207d95c1ddb45098f2dc9741697c3608497dc2efd9b33bb5"
 assert d["source_supplements"]["official_doc_s008"]["sha256"]=="0813b44b5770f03b833a0623da876a76dde6e2ee5cd8dcbaf5ec8257fa04b504"
 assert d["source_supplements"]["official_doc_s008"]["raw_table_multi_tier_visual_numbers_audited"] is False
 r=d["firstparty_real_ci_receipts"]
 assert r["main_plus_two_doc_run"]==37198446072 and r["all_six_tiff_run"]==37198751884 and r["all_six_tiff_actual_result"]=="success"
 assert r["media_count_official_9_verified"]==9 and r["formal_supplement_count_verified"]==8
 assert not r["arbitrary_nonpublisher_google_storage_permitted"]
 assert r["first_party_initial_PLOS_endpoint_required"] and r["signed_PLOS_delegated_bucket_exact_DOI_filename_required"]
 n=d["bounded_science_adverse"]
 assert len(n["negative_ids"])==5 and n["published_doc_note_order_network_not_necessary_for_serial_bottleneck"]
 assert n["Dehaene_coauthor_and_broad_workspace_ancestry_shared_with_INT03"] and n["router_task_setting_spiking_model_specific_mechanistic_delta_vs_INT03"]
 assert n["S1_S6_original_pixels_structurally_verified"] and not n["S1_S6_original_pixel_semantics_all_qualified"]
 assert not n["supplement_full_formal_math_scientifically_qualified"] and not n["INT03_INT06_independent_global_central_family_proven"]
 assert d["selected_INT06_new_raw_media_full_set"] and not d["selected_INT06_full_source_semantic_admission"]
 assert not d["all_SELECTED_INT_global_model_families_cleared"] and d["formal_backup_activation_count"]==0
 assert not d["main_scientific_reconstruction_performed"] and not d["main_scientific_results_inspected"] and not d["author_main_GO"]
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=json.loads(J.read_text())
 def test_real_source_receipts_and_science_boundaries(self):check(self.d)
 def test_append_only_report(self):
  t=R.read_text()
  for s in ("37198751884","37198446072","7923010b6449","d01181c75eb5","e3e2247e2676","s008","order network","MAIN"):
   self.assertIn(s.lower(),t.lower())
 def test_thirteen_destructive_false_promotions(self):
  edits=[
   (("base_g2_head",),"false"),(("main_original","raw_sha256"),"wrong"),(("source_supplements","original_figure_TIFFs",0,"raw_sha256"),"wrong"),
   (("source_supplements","original_figure_TIFFs",1,"semantic_all_pixel_figure_audit"),True),
   (("source_supplements","official_doc_s008","raw_table_multi_tier_visual_numbers_audited"),True),
   (("firstparty_real_ci_receipts","media_count_official_9_verified"),8),
   (("firstparty_real_ci_receipts","arbitrary_nonpublisher_google_storage_permitted"),True),
   (("bounded_science_adverse","published_doc_note_order_network_not_necessary_for_serial_bottleneck"),False),
   (("bounded_science_adverse","INT03_INT06_independent_global_central_family_proven"),True),
   (("bounded_science_adverse","S1_S6_original_pixel_semantics_all_qualified"),True),
   (("selected_INT06_full_source_semantic_admission",),True),
   (("formal_backup_activation_count",),1),
   (("author_main_GO",),True)]
  for p,v in edits:
   m=copy.deepcopy(self.d);x=m
   for k in p[:-1]:x=x[k]
   x[p[-1]]=v
   with self.subTest(p=p),self.assertRaises(AssertionError):check(m)
if __name__=="__main__":
 print("G2D_V5_UTF8_FILES_RAW_SHA256",[(f.name,hashlib.sha256(f.read_bytes()).hexdigest()) for f in [J,R]])
 unittest.main()
