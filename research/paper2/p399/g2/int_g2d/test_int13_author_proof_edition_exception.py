#!/usr/bin/env python3
"""INT13 author-source exception: exact baseline and strict non-promotion safety guards."""
import copy,json,unittest
from pathlib import Path
P=Path(__file__).parent
def read(n): return json.loads((P/n).read_text(encoding="utf8"))
V1=read("G2D_INT13_20261005_TIMED_FIRSTPARTY_AND_CHROMIUM_APPEND_ONLY_RECEIPT_v1.json")
V2=read("G2D_INT13_AUTHOR_ADOPTED_UNCORRECTED_PROOF_STUDY_EDITION_DELTA_v2.json")
OLD=read("G2D_INT_BOUNDED_DECISIONS_v1.json")
PDF="5f313f8690f377faaea6b9a3610013c71b880af86634c97dbd4a5344bede9258"
HTML="057e12d6c60605f3f5344b3411e6038397c3f823e09274c4929da9af1afaaca0"
def check(d):
 a=d["authority"];s=d["selected_source"];st=d["state_delta"];f=d["prospective_version_policy"];p=s["physical_receipt"]
 return (
 a["type"]=="EXPLICIT_AUTHOR_DECISION_IN_CURRENT_CONVERSATION"
 and a["scope"].startswith("INT-13 only;")
 and a["exact_directive_japanese"]=="未校正稿を正式採用とする"
 and a["historic_edition_hold"].startswith("retained true")
 and s["slot"]=="INT-13" and s["doi"]=="10.1371/journal.pcbi.1014796"
 and s["selection"]=="KEEP_ORIGINAL_SELECTED_SLOT_NOT_BACKUP"
 and s["source_type"]=="ACTUAL_FIRSTPARTY_PUBLISHER_UNCORRECTED_PROOF"
 and s["publisher_published_original_final_vor"] is False
 and s["publisher_proof_notice_explicit"] is True
 and s["canonical_main_reference"]=={"medium":"publisher-hosted printable PDF","bytes":2581474,"pages":31,"sha256":PDF}
 and s["matched_publisher_html_crosscheck"]["sha256"]==HTML
 and s["matched_publisher_html_crosscheck"]["bytes"]==356026
 and s["matched_publisher_html_crosscheck"]["raw_pdf_html_content_equivalence_proven"] is False
 and p["run_id"]==37211673439 and p["result"]=="SUCCESS"
 and p["direct_and_chromium_pdf_raw_equal"] is True
 and p["both_live_raw_responses_match_prior_proof_baseline"] is True
 and p["browser_rendered_dom_not_primary_hash"] is True
 and st["previous_study_edition_admissibility"]=="HOLD_FINAL_VOR"
 and st["new_study_edition_admissibility"]=="AUTHOR_APPROVED_FROZEN_PUBLISHER_PROOF"
 and st["edition_wait_blocker_for_study_selection"]=="WAIVED_FOR_INT13_PROOF_ONLY"
 and st["published_final_vor_gate"].startswith("NOT_CLAIMED")
 and st["source_scientific_math_figures_variants_negative_and_corrections_review"]=="PENDING"
 and st["independent_all_G1_MAIN_central_model_family_qualification"]=="PENDING"
 and st["full_int13_scientific_qualification"]=="NOT_GRANTED"
 and all(st[x] is False for x in ("formal_backup_activation","g2_common_manifest_mutated","main_authorized"))
 and f["immutable_primary_media_for_original_int13_pre_a"].startswith("canonical_main_reference exact SHA")
 and d["preservation"]["global_design_and_grammar_unchanged"] is True
 )
class EditionTest(unittest.TestCase):
 def test_actual_prior_publisher_receipts(self):
  s=V1["live_publisher_bounded_sources"]
  self.assertEqual((s["pdf"]["actual_sha256"],s["pdf"]["actual_response_bytes"],s["pdf"]["pages"]),(PDF,2581474,31))
  self.assertEqual((s["html"]["actual_sha256"],s["html"]["actual_response_bytes"]),(HTML,356026))
  self.assertTrue(s["html"]["explicit_proof_banner"])
  self.assertEqual(s["chromium"]["chromium_context_pdf_raw_sha256"],PDF)
  self.assertTrue(s["chromium"]["renderer_DOM_is_NOT_raw_publisher_HTML"])
 def test_historical_hold_immutable(self):
  self.assertEqual(V1["edition_decision"],"HOLD_FINAL_VOR")
  self.assertFalse(V1["no_scientific_promotion"]["final_vor_verified"])
  prior=[s for s in OLD["selected"] if s["slot"]=="INT-13"]
  self.assertEqual(len(prior),1)
  self.assertEqual(prior[0]["decision"],"HOLD_FINAL_VOR")
  self.assertFalse(prior[0]["final_vor_physically_verified"])
 def test_policy_adoption_and_separate_remaining_gates(self): self.assertTrue(check(V2))
 def test_destructive_false_promotion_rejected(self):
  mutations=[
   (["selected_source","publisher_published_original_final_vor"],True),
   (["selected_source","canonical_main_reference","sha256"],"0"*64),
   (["selected_source","matched_publisher_html_crosscheck","raw_pdf_html_content_equivalence_proven"],True),
   (["state_delta","full_int13_scientific_qualification"],"PASS"),
   (["state_delta","independent_all_G1_MAIN_central_model_family_qualification"],"PASS"),
   (["state_delta","main_authorized"],True),
   (["state_delta","formal_backup_activation"],True),
   (["state_delta","g2_common_manifest_mutated"],True),
   (["selected_source","source_type"],"FINAL_VOR"),
   (["state_delta","new_study_edition_admissibility"],"FINAL_PUBLISHER_VOR"),
   (["authority","scope"],"All MAIN works use proof editions"),
   (["selected_source","physical_receipt","browser_rendered_dom_not_primary_hash"],False)
  ]
  for keys,value in mutations:
   with self.subTest(keys=keys):
    d=copy.deepcopy(V2);x=d
    for k in keys[:-1]:x=x[k]
    x[keys[-1]]=value
    self.assertFalse(check(d))
  print("12/12 destructive invalid-promotion guards PASS")
if __name__=="__main__":unittest.main(verbosity=2)
