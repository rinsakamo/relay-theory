#!/usr/bin/env python3
"""PF04 latest formally bounded qualification receipt checks: structure/provenance only.
Scientific content requires separate actually fetched original-PDF source check.
"""
import hashlib
import json
import pathlib
import subprocess
import unittest

DIR=pathlib.Path(__file__).resolve().parents[1]/"research/paper2/p399/pf04"
OLD="bc84d4827df202cf5051cf10aa64cc09673b718af2acd31441a3712bcd376df9"
J=DIR/"PF04_FORMAL_SCIENTIFIC_QUALIFICATION_DECISION_20261004.json"
REPORT=DIR/"PF04_FORMAL_QUALIFICATION_JA_20261004.md"

class FormalQualifierReceiptChecks(unittest.TestCase):
    def test_actual_frozen_receipts_match_immutable_sha_and_chronological_git_creations(self):
        decision=json.loads(J.read_bytes())
        self.assertEqual(decision["frozen_primary"]["original_sha256"],OLD)
        commits=[]
        for item in decision["immutable_science_chain"]:
            target=DIR/item["path"]
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(),item["raw_sha256"],item["phase"])
            c=subprocess.check_output(["git","log","--format=%H","--diff-filter=A","--",str(target)],text=True).splitlines()
            self.assertEqual(c,[item["git_add"]])
            commits.append(c[0])
        for a,b in zip(commits,commits[1:]):
            subprocess.check_call(["git","merge-base","--is-ancestor",a,b])
        current_commit=subprocess.check_output(["git","log","--format=%H","--diff-filter=A","--",str(J)],text=True).strip().splitlines()
        self.assertEqual(len(current_commit),1)
        subprocess.check_call(["git","merge-base","--is-ancestor",commits[-1],current_commit[0]])
        self.assertTrue(REPORT.is_file())
        print("PF04_FORMAL_RECEIPT_SHA",hashlib.sha256(J.read_bytes()).hexdigest())
        print("PF04_FORMAL_REPORT_SHA",hashlib.sha256(REPORT.read_bytes()).hexdigest())
        print("PF04_FORMAL_FROZEN_SIX_CHAIN_PASS", "->".join(x["phase"] for x in decision["immutable_science_chain"]))
    def test_latest_formal_scope_is_precise_and_previous_history_untouched(self):
        final=json.loads(J.read_bytes())
        self.assertEqual(final["decision"]["qualified_count_increment"],1)
        self.assertEqual(final["decision"]["qualified_progress_if_no_concurrent_records"],"2/4 new registered PF pilots (PF01 and PF04 only)")
        self.assertFalse(final["decision"]["main_authorized"])
        self.assertFalse(final["decision"]["merge_automatically_authorized"])
        self.assertFalse(final["actually_verified_ci"]["software_exact_v231_validator_deployed"])
        self.assertFalse(final["actually_verified_ci"]["historical_data_reanalysis_performed"])
        self.assertEqual(final["actually_verified_ci"]["real_original_page_anchors"],13)
        self.assertEqual(final["actually_verified_ci"]["original_source_visual_manual_page_13"],True)
        self.assertEqual(len(final["formal_review_checks"]),11)
        self.assertTrue(all(x["verdict"] not in ("FAIL","UNDERDETERMINED_IN_INCLUDED_STRUCTURE") for x in final["formal_review_checks"]))
        self.assertIn("omega(a')", final["frozen_primary"].get("reviewer_authorized_notation","omega(a')"))
        self.assertIn("UNDERDETERMINED",final["genuine_boundary"]["eq10"].replace("UNKNOWN","UNDERDETERMINED"))
        older=json.loads((DIR/"FINAL_QUALIFICATION.json").read_bytes())
        self.assertIn("UNDERDETERMINED",older["verdict"])
        prev=json.loads((DIR/"FINAL_QUALIFICATION_v3_EXCEPTIONS.json").read_bytes())
        self.assertEqual(prev["formal_decision"]["official_pilot_count_increment"],0)
        self.assertFalse(prev["formal_decision"]["main_authorized"])
        prev_recheck=json.loads((DIR/"EXCEPTIONS_EX1_EX2_SOURCE_RECHECK_v1.json").read_bytes())
        self.assertTrue(prev_recheck["EX1"]["state"].startswith("UNDERDETERMINED"))
        self.assertEqual(prev_recheck["authority"]["original_publisher_pdf_sha256"],OLD)
        self.assertIn("exact historical", " ".join(final["decision"]["unqualified"]).lower())
    def test_source_scoped_nonuniversal_reconstruction_and_model_count(self):
        D=json.loads((DIR/"PASS_D_grammar_v0.json").read_bytes())
        E=json.loads((DIR/"PASS_E_fidelity.json").read_bytes())
        A=json.loads((DIR/"PASS_A_original.json").read_bytes())
        self.assertEqual(A["compared_variants"]["total_displayed"],16)
        self.assertEqual(len(A["compared_variants"]["flat"]),8)
        self.assertEqual(len(A["compared_variants"]["hierarchy"]),8)
        self.assertEqual(D["additive_grammar_primitives"],[])
        self.assertEqual(len(E["fidelity_cases"]),13)
        self.assertEqual(len([t for t in E["fidelity_cases"] if t["structural_status"]=="FULL"]),12)
        self.assertEqual(len([t for t in E["fidelity_cases"] if t["structural_status"]=="UNDERDETERMINED"]),1)
        decision=json.loads(J.read_bytes())
        self.assertEqual({x["family"] for x in decision["lineage_science"]["source_architectures"]},{"flat","hierarchical"})
        self.assertFalse(decision["frozen_paper2_or_grammar_modified"])
        self.assertFalse(decision["other_pilots_affected"])

if __name__=="__main__":
    unittest.main(verbosity=2)
