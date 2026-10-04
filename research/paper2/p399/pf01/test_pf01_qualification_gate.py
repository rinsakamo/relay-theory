#!/usr/bin/env python3
"""PF01 *additional* post-E scoped admission tests (not original #401 validator).
Tests report/source-manifest consistency and mutation guards. Cannot prove source semantics.
"""
import copy
import hashlib
import json
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REVIEW = "PF01_POST_E_TARGETED_SOURCE_REVIEW_20261004.json"
REVIEW_SHA256 = "ffb085f7a2a66e7db3d9e2409418f5b35d8d6af368b0ad324b29a3fb7d58be1b"
ORIGINAL_PDF_SHA256 = "8531103d577a3249c7edffa06ef2a8a7e85eb01b0a2f02cee2145e187581fbc3"
STAGE_FILES = {
    "PRE_A": ("PF01_PRE_A_REQUALIFIED_20261004.json","9a9e72d7d0174af1fe9623c15874fbe6fe1a91ba2836312bbad652ab9c294f7b"),
    "A": ("PF01_A_ORIGINAL_SOURCE_20261004.json","79e308cd97ec01bc2456d636422fd66b6279681ff631948959d294f1482c6383"),
    "B": ("PF01_B_RESULT_INFORMED_20261004.json","8baa554cefc97bd773fff78dffb903275e96943a6a9af645f0d81783f6b4f128"),
    "C": ("PF01_C_V231_SOURCE_CLOSED_20261004.json","051fa6128cb384338a1767a9a78f6c64ea29eeb63eea9e26e8572368601d6d60"),
    "D": ("PF01_D_GRAMMAR_V0_RECONSTRUCTION_20261004.json","db0e4652e8fb19900908dce7b48b70a3275e8872d98ff21599c21bdaaec2e8b8"),
    "E": ("PF01_E_STRUCTURAL_FIDELITY_20261004.json","e2bffee3d9103d5688354bb7bfcced6fa22b7649c492902882f61da041045ba2"),
}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def load(name):
    return json.loads((HERE / name).read_bytes())

def gate(v):
    """Fail-closed admission *record* invariants, independent of reviewer confidence."""
    ex=v["targeted_exception_closure"]
    q=v["admission_decision"]
    return (
        v["source_primary"]["raw_sha256"] == ORIGINAL_PDF_SHA256
        and ex["source_internal_numeric_issues"] == ["U01", "U02"]
        and ex["material_for_reconstructed_core"] is False
        and ex["material_for_excluded_exact_figure_and_1000_trial_replication"] is True
        and q["status"] == "READY_FOR_FORMAL_PF01_QUALIFICATION_DECISION_ONLY"
        and q["formal_qualified"] is False
        and q["qualified_pilot_count_delta"] == 0
        and q["MAIN_authorized"] is False
        and v["scientific_boundary"]["exact_original_PLOS_numeric_replication"] == "NOT_EXECUTED_AND_NOT_CLAIMED"
        and v["scientific_boundary"]["exact_original_v231_validator_import"].startswith("UNAVAILABLE")
    )

class PostETargetedReviewTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review=load(REVIEW)
        cls.A=load(STAGE_FILES["A"][0])
        cls.B=load(STAGE_FILES["B"][0])
        cls.C=load(STAGE_FILES["C"][0])
        cls.D=load(STAGE_FILES["D"][0])

    def test_targeted_review_pin_and_stage_hashes(self):
        self.assertEqual(sha((HERE/REVIEW).read_bytes()),REVIEW_SHA256)
        for stage,(filename,expected) in STAGE_FILES.items():
            with self.subTest(stage=stage):
                self.assertEqual(sha((HERE/filename).read_bytes()),expected)
                self.assertEqual(self.review["frozen_stages"][stage],expected)

    def test_historic_manifests_actually_have_no_exact_original_identity(self):
        fields=("Seeholzer","Deger","1006928")
        for item in self.review["historic_exact_identity_rescreen"]:
            with self.subTest(path=item["git_path"]):
                blob=(ROOT/item["git_path"]).read_text(encoding="utf-8")
                self.assertFalse(any(s.lower() in blob.lower() for s in fields))
                self.assertIs(item["exact_title_author_doi_match"],False)

    def test_all_four_C_patches_have_reinspected_in_primary_source(self):
        decisions={x["id"]:x for x in self.review["original_pdf_targeted_reinspection"]}
        for key,patch in (("RV_DISTRACTOR_WIDTH","P01"),("RV_NUMERIC_ORDER","P02"),
                          ("RV_EQ11","P03"),("RV_NUMERIC_ORDER","P04")):
            with self.subTest(key=key):
                self.assertEqual(decisions[key]["decision"],"PASS_IN_SCOPE")
                self.assertIn(patch,{x["id"] for x in self.C["append_only_delta"]})
        self.assertEqual({x["id"] for x in self.C["append_only_delta"]},{"P01","P02","P03","P04"})

    def test_fig2_and_diffusion_conflicts_not_silently_resolved(self):
        items={x["id"]:x for x in self.review["original_pdf_targeted_reinspection"]}
        self.assertEqual(items["RV_FIG2_U"]["exception_id"],"U01")
        self.assertEqual(items["RV_DIFFUSION_N"]["exception_id"],"U02")
        self.assertEqual(items["RV_FIG2_U"]["decision"],"RETAIN_UNDERDETERMINED_NO_A_B_C_PATCH")
        self.assertEqual(items["RV_DIFFUSION_N"]["decision"],"RETAIN_UNDERDETERMINED_NO_A_B_C_PATCH")
        self.assertEqual(len(self.review["targeted_exception_closure"]["source_internal_numeric_issues"]),2)

    def test_c1_no_false_duplicate_patches(self):
        b={x["id"] for x in self.B["findings"]}
        c=self.C["c1_source_vs_entire_original_A_objection_adjudication"]
        self.assertEqual(b,{x["id"] for x in c})
        self.assertEqual({x["id"] for x in c if x["patch"]},{"B01","B02","B03","B12"})
        self.assertTrue(all(x["patch"] is None for x in c if x["id"] not in {"B01","B02","B03","B12"}))

    def test_c2_existing_material_negatives_are_referenced_once(self):
        self.assertEqual(len(self.C["c2_material_conditions_once_each"]),16)
        self.assertEqual({x["id"] for x in self.C["c2_material_conditions_once_each"]},
                         {x["id"] for x in self.A["material_limits"]})
        self.assertTrue(all(x["treatment"] == "ALREADY_IN_A" for x in self.C["c2_material_conditions_once_each"]))

    def test_eq11_not_RSS_and_external_numeric_order_is_not_neural_state(self):
        patch={x["id"]:x for x in self.C["append_only_delta"]}["P03"]
        self.assertIn("separate roots added",patch["appended_nodes"][0]["meaning"])
        d=self.D["layers"]["L_formal"]
        self.assertIn("ADDED",d["source_derived_measure"])
        self.assertIn("then",d["numerical_order"])
        self.assertIn("full_spiking",d)

    def test_code_corrob_does_not_override_primary_source(self):
        x=self.review["secondary_author_code"]
        self.assertTrue(x["not_primary_scientific_source"])
        self.assertEqual(x["pinned_commit"],"6d8824235af3a345d33a6cff6c1ede9ea0d4b66f")
        self.assertIn("SECONDARY_CORROBORATION_ONLY",x["adjudication"])

    def test_required_qualification_scope_invariants(self):
        self.assertTrue(gate(self.review))

    def test_mutations_fail_closed(self):
        for path,newvalue in (
            (("admission_decision","formal_qualified"),True),
            (("admission_decision","qualified_pilot_count_delta"),1),
            (("admission_decision","MAIN_authorized"),True),
            (("targeted_exception_closure","material_for_reconstructed_core"),True),
            (("targeted_exception_closure","source_internal_numeric_issues"),[]),
            (("scientific_boundary","exact_original_PLOS_numeric_replication"),"PASS"),
            (("source_primary","raw_sha256"),"0"*64),
            (("scientific_boundary","exact_original_v231_validator_import"),"GITHUB_DEPLOYED_PASS"),
        ):
            with self.subTest(path=path):
                v=copy.deepcopy(self.review)
                v[path[0]][path[1]]=newvalue
                self.assertFalse(gate(v))

if __name__=="__main__":
    unittest.main(verbosity=2)
