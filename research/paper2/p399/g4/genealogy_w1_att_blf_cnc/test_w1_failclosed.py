#!/usr/bin/env python3
import copy
import unittest

import verify_w1_failclosed as v


class TestW1FailClosed(unittest.TestCase):
    def setUp(self):
        self.p = v.load_json(v.PROFILE_PATH)
        self.q = v.load_json(v.PAIR_PATH)
        self.g = v.load_json(v.GAPS_PATH)

    def test_current_bundle_passes(self):
        self.assertTrue(v.validate(self.p, self.q, self.g))

    def test_exact_seven_doi_identities(self):
        bad = copy.deepcopy(self.p)
        bad["profiles"][0]["doi"] = "10.invalid/example"
        with self.assertRaises(AssertionError):
            v.validate(bad, self.q, self.g)

    def test_duplicate_profile_fails(self):
        bad = copy.deepcopy(self.p)
        bad["profiles"][1]["id"] = bad["profiles"][0]["id"]
        with self.assertRaises(AssertionError):
            v.validate(bad, self.q, self.g)

    def test_malformed_sha_or_ref_fails(self):
        bad = copy.deepcopy(self.p)
        bad["profiles"][0]["original_source_evidence"][0]["repository_git_blob_sha1"] = "bad"
        with self.assertRaises(AssertionError):
            v.validate(bad, self.q, self.g)

    def test_global_independence_true_fails(self):
        bad = copy.deepcopy(self.p)
        bad["profiles"][0]["global_family_independence_certified"] = True
        with self.assertRaises(AssertionError):
            v.validate(bad, self.q, self.g)

    def test_ancestry_promotion_fails(self):
        bad = copy.deepcopy(self.p)
        bad["profiles"][0]["ancestry_exhaustiveness"] = "ATTESTED"
        with self.assertRaises(AssertionError):
            v.validate(bad, self.q, self.g)

    def test_required_supplement_disappearance_fails(self):
        bad = copy.deepcopy(self.p)
        target = next(x for x in bad["profiles"] if x["id"] == "BLF-02")
        target["additional_edition_bundle"] = []
        with self.assertRaises(AssertionError):
            v.validate(bad, self.q, self.g)

    def test_missing_evidence_fails_closed(self):
        bad = copy.deepcopy(self.p)
        target = next(x for x in bad["profiles"] if x["id"] == "ATT-01")
        target["original_source_evidence"] = []
        with self.assertRaises(AssertionError):
            v.validate(bad, self.q, self.g)

    def test_missing_required_supplement_cannot_be_ready(self):
        bad = copy.deepcopy(self.p)
        target = next(x for x in bad["profiles"] if x["id"] == "BLF-02")
        target["completion_status"] = "PROFILE_FRAGMENT_READY"
        with self.assertRaises(AssertionError):
            v.validate(bad, self.q, self.g)

    def test_pair_cannot_promote_global_independence(self):
        bad = copy.deepcopy(self.q)
        bad["pairs"][0]["global_independence_promoted"] = True
        with self.assertRaises(AssertionError):
            v.validate(self.p, bad, self.g)


if __name__ == "__main__":
    unittest.main(verbosity=2)
