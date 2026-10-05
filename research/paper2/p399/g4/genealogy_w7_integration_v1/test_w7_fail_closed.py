#!/usr/bin/env python3
import copy
import importlib.util
import pathlib
import unittest
from unittest.mock import patch

HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("w7", HERE / "w7_integrate.py")
w7 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(w7)


class W7FailClosedTests(unittest.TestCase):
    def setUp(self):
        self.roster = {"X-01": "10.1000/x1", "X-02": "10.1000/x2"}
        self.ready = {
            "id": "X-01",
            "doi": "10.1000/x1",
            "status": "PROFILE_FRAGMENT_READY",
            "ancestry_exhaustiveness": "NOT_ATTESTED",
            "global_family_independence_certified": False,
            "main_scientific_authorization": False,
            "adopted_edition": {"raw_sha256": "a" * 64},
            "source_provenance": [{
                "repository_path": "research/paper2/p399/f.json",
                "repository_git_blob_sha1": "b" * 40,
                "source_repository_ref": "c" * 40,
            }],
            "source_native_structure": {
                "paper_specific_operators": ["X-01:op"],
                "decisive_equations_or_updates": [
                    "A source-grounded operator description long enough for validation."
                ],
                "direct_model_ancestor_dois": [],
            },
            "required_bundle_ids": [],
            "supplement_bundle": [],
        }

    def validate(self, p=None, returned_blob=None):
        with patch.object(w7, "git_blob", return_value=returned_blob or "b" * 40):
            return w7.validate_profile(p or self.ready, self.roster, "T")

    def test_01_ready_profile_passes(self):
        self.assertEqual(self.validate(), "PROFILE_FRAGMENT_READY")

    def test_02_doi_mismatch_fails(self):
        p = copy.deepcopy(self.ready); p["doi"] = "10.1000/wrong"
        with self.assertRaises(w7.W7Error): self.validate(p)

    def test_03_global_independence_true_fails(self):
        p = copy.deepcopy(self.ready); p["global_family_independence_certified"] = True
        with self.assertRaises(w7.W7Error): self.validate(p)

    def test_04_main_authorization_true_fails(self):
        p = copy.deepcopy(self.ready); p["main_scientific_authorization"] = True
        with self.assertRaises(w7.W7Error): self.validate(p)

    def test_05_ancestry_exhaustiveness_promotion_fails(self):
        p = copy.deepcopy(self.ready); p["ancestry_exhaustiveness"] = "ATTESTED"
        with self.assertRaises(w7.W7Error): self.validate(p)

    def test_06_nonlocal_operator_id_fails(self):
        p = copy.deepcopy(self.ready)
        p["source_native_structure"]["paper_specific_operators"] = ["OTHER:op"]
        with self.assertRaises(w7.W7Error): self.validate(p)

    def test_07_malformed_git_blob_fails(self):
        p = copy.deepcopy(self.ready)
        p["source_provenance"][0]["repository_git_blob_sha1"] = "not-a-sha"
        with self.assertRaises(w7.W7Error): self.validate(p)

    def test_08_source_blob_drift_fails(self):
        with self.assertRaises(w7.W7Error): self.validate(returned_blob="d" * 40)

    def test_09_required_supplement_disappearance_fails(self):
        p = copy.deepcopy(self.ready)
        p["required_bundle_ids"] = ["S1"]
        p["supplement_bundle"] = []
        with self.assertRaises(w7.W7Error): self.validate(p)

    def test_10_source_blocked_is_not_ready(self):
        p = copy.deepcopy(self.ready); p["status"] = "SOURCE_BLOCKED"
        self.assertEqual(self.validate(p), "SOURCE_BLOCKED")

    def test_11_ancestry_underdetermined_is_not_ready(self):
        p = copy.deepcopy(self.ready); p["status"] = "SCIENTIFIC_ANCESTRY_UNDERDETERMINED"
        self.assertEqual(self.validate(p), "SCIENTIFIC_ANCESTRY_UNDERDETERMINED")

    def test_12_bounded_difference_never_means_global_independence(self):
        ws = [{"category": "BOUNDED_SOURCE_NATIVE_DIFFERENCE", "global_independence_certified": False}]
        self.assertEqual(w7.strongest(ws), "BOUNDED_SOURCE_NATIVE_DIFFERENCE")
        self.assertFalse(ws[0]["global_independence_certified"])

    def test_13_shared_constituent_never_means_global_independence(self):
        ws = [{"category": "SHARED_CONSTITUENT_ONLY", "global_independence_certified": False}]
        self.assertEqual(w7.strongest(ws), "SHARED_CONSTITUENT_ONLY")
        self.assertFalse(ws[0]["global_independence_certified"])

    def test_14_direct_ancestry_is_risk_not_independence(self):
        ws = [{"category": "DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY", "global_independence_certified": False}]
        self.assertEqual(w7.strongest(ws), "DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY")
        self.assertFalse(ws[0]["global_independence_certified"])

    def test_15_absence_of_positive_evidence_remains_underdetermined(self):
        self.assertEqual(w7.strongest([]), "UNDERDETERMINED")

    def test_16_lane_partition_is_exactly_34_unique_ids(self):
        ids = [x for m in w7.LANES.values() for x in m["ids"]]
        self.assertEqual(len(ids), 34)
        self.assertEqual(len(set(ids)), 34)

    def test_17_allowed_scientific_vocabulary_is_exact(self):
        self.assertEqual(w7.ALLOWED_DECISIONS, {
            "DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY",
            "SHARED_CONSTITUENT_ONLY",
            "BOUNDED_SOURCE_NATIVE_DIFFERENCE",
            "UNDERDETERMINED",
        })

    def test_18_w1_legacy_category_normalization_is_bounded(self):
        self.assertEqual(w7.normalize_category("BOUNDED_SOURCE_NATIVE_CENTRAL_OPERATION_DIFFERENCE"), "BOUNDED_SOURCE_NATIVE_DIFFERENCE")
        self.assertEqual(w7.normalize_category("SHARED_CONSTITUENT_TECHNIQUE_ONLY"), "SHARED_CONSTITUENT_ONLY")
        self.assertEqual(w7.normalize_category("SHARED_MODEL_LINEAGE_ANCESTOR_SUPPORTED"), "DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY")

    def test_19_unknown_independence_category_is_rejected(self):
        with self.assertRaises(w7.W7Error):
            w7.normalize_category("GLOBAL_FAMILY_INDEPENDENT")

    def test_20_int13_uncorrected_proof_identity_is_preservable(self):
        p = copy.deepcopy(self.ready)
        p["adopted_edition"] = {
            "status": "AUTHOR_APPROVED_FROZEN_PUBLISHER_UNCORRECTED_PROOF",
            "sha256": "e" * 64,
            "final_corrected_vor": False,
        }
        self.assertEqual(w7.edition_sha_of(p), "e" * 64)
        self.assertIn("UNCORRECTED_PROOF", str(p["adopted_edition"]))


if __name__ == "__main__":
    unittest.main()
