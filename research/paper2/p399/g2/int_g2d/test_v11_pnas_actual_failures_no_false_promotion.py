#!/usr/bin/env python3
"""Negative publisher-source classification only; no science admission from CI."""
import hashlib,copy,json,pathlib,unittest
HERE=pathlib.Path(__file__).parent
P=HERE/"G2D_V11_ACTUAL_FIRSTPARTY_PNAS_LEGACY_NEGATIVE_MACHINE_RECEIPTS.json"
D=HERE/"G2D_V11_ACTUAL_PNAS_LEGACY_FIRSTPARTY_TIMEOUT_BROWSER_SOURCE_HOLD_JA_20261004.md"
def check(x):
 assert x["starting_parent_G2_sha256"]=="69748673c80f421605f1c63607472903ac2ed68c"
 assert x["historical_v6_ordinary_pnas_browser_failure_run"]==37199967871
 assert x["new_distinct_legacy_run_id"]==37206599277
 assert x["new_distinct_legacy_run_conclusion"]=="success_procedural_only"
 assert x["direct_request_timeout_seconds"]==10 and x["legacy_chromium_nav_timeout_seconds"]==16
 assert len(x["legacy_direct_firstparty_attempts"])==5
 assert all(r["status"]==403 and r["url"].startswith("https://www.pnas.org/") for r in x["legacy_direct_firstparty_attempts"])
 a=x["fallback_chromium"]
 assert a["http_status"]==403 and a["response_bytes"]==6200
 assert a["raw_challenge_sha256"]=="7134cbd21ccb5c2a428229463e8331eec7665457c443606a2ff5cfc8e974a66f"
 assert not a["publisher_full_scientific_original_acquired"]
 for k in ("any_PNAS_original_new_raw_VOR_acquired","PMC_mirror_elevated_to_PNAS_publisher_original","any_nonpublisher_article_elevated","selected_INT03_independently_scientific_source_qualified","global_INT03_INT06_family_proven_independent","selected_INT13_final_corrected_VOR_verified","selected_INT01_official_publisher_raw_complete_full_original_acquired","all_G1_20_G2_40_global_family_independence_qualified","MAIN_scientific_reconstruction_performed","MAIN_preliminary_scientific_outcomes_inspected","author_MAIN_authorized"):
  assert x[k] is False,k
 assert x["formal_backup_activated"]==0
 assert x["selected_INT04_original_main_science_fig1_to7_bounded_reviewed"]
 assert x["selected_INT04_original_supp_science_fig1_to3_bounded_reviewed"]
 assert x["selected_INT08_elife_official_original_exact_sha_locked"] and x["selected_INT08_human_task_hand_fixed_encoding_page6_verified"]
class Test(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.x=json.loads(P.read_text())
 def test_negative_source_receipt_boundary(self):check(self.x)
 def test_japanese_prose_unaltered(self):
  text=D.read_text()
  for phrase in ["37206599277","37199967871","10s","16s","MAIN_NOT_AUTHORIZED"]:
   self.assertIn(phrase.lower(),text.lower())
 def test_destructive_10_false_promotions(self):
  mutations=[
    (("legacy_direct_firstparty_attempts",0,"status"),200),
    (("legacy_direct_firstparty_attempts",1,"url"),"https://pmc.ncbi.nlm.nih.gov/"),
    (("fallback_chromium","http_status"),200),
    (("fallback_chromium","publisher_full_scientific_original_acquired"),True),
    (("any_PNAS_original_new_raw_VOR_acquired",),True),
    (("PMC_mirror_elevated_to_PNAS_publisher_original",),True),
    (("selected_INT03_independently_scientific_source_qualified",),True),
    (("global_INT03_INT06_family_proven_independent",),True),
    (("formal_backup_activated",),1),
    (("author_MAIN_authorized",),True)]
  for path,value in mutations:
   d=copy.deepcopy(self.x);node=d
   for seg in path[:-1]:node=node[seg]
   node[path[-1]]=value
   with self.subTest(path=path),self.assertRaises(AssertionError):check(d)
if __name__=="__main__":
 print("V11_ACTUAL_PROSE_JSON_SHA",[(z.name,hashlib.sha256(z.read_bytes()).hexdigest()) for z in (P,D)])
 unittest.main()
