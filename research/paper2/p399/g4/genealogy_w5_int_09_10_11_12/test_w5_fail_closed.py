#!/usr/bin/env python3
import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
PARENT = "ae044a8f475fb0dc9140a91e360e1ff26a0b5e3a"
EXPECTED = {
    "INT-09": "10.1371/journal.pcbi.1005190",
    "INT-10": "10.1371/journal.pcbi.1011024",
    "INT-11": "10.1371/journal.pcbi.1014093",
    "INT-12": "10.1371/journal.pcbi.1006116",
}
ALLOWED_RESULTS = {
    "DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY",
    "SHARED_CONSTITUENT_ONLY",
    "BOUNDED_SOURCE_NATIVE_DIFFERENCE",
    "UNDERDETERMINED",
}
ALLOWED_STATUS = {
    "PROFILE_FRAGMENT_READY",
    "SOURCE_BLOCKED",
    "SCIENTIFIC_ANCESTRY_UNDERDETERMINED",
}
GITSHA = re.compile(r"^[0-9a-f]{40}$")


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def git_blob(path):
    return subprocess.check_output(
        ["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True
    ).strip()


class W5FailClosed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profiles = load("W5_SOURCE_NATIVE_PROFILE_FRAGMENTS_v1.json")
        cls.pairs = load("W5_BOUNDED_PAIR_ADJUDICATIONS_v1.json")
        cls.gaps = load("W5_SOURCE_GAPS_AND_BLOCKERS_v1.json")
        cls.freeze = load("W5_SOURCE_EVIDENCE_FREEZE_v1.json")

    def test_exact_four_doi_identities_no_comparison_profiles_promoted(self):
        rows = self.profiles["profiles"]
        self.assertEqual(len(rows), 4)
        got = {r["id"]: r["doi"] for r in rows}
        self.assertEqual(got, EXPECTED)
        self.assertEqual(len(got), len(rows))
        self.assertTrue({"INT-01", "INT-04", "INT-08"}.isdisjoint(got))

    def test_source_freeze_exact_four_and_correction_cannot_disappear(self):
        rows = self.freeze["source_records"]
        self.assertEqual({r["slot"]: r["doi"] for r in rows}, EXPECTED)
        int09 = next(r for r in rows if r["slot"] == "INT-09")
        ed = int09["adopted_scientific_edition"]
        self.assertEqual(ed["correction_doi"], "10.1371/journal.pcbi.1005370")
        self.assertFalse(ed["correction_changes_central_model"])
        p09 = next(r for r in self.profiles["profiles"] if r["id"] == "INT-09")
        corr = [x for x in p09["correction_supplement_bundle"]
                if x.get("doi") == "10.1371/journal.pcbi.1005370"]
        self.assertEqual(len(corr), 1)
        self.assertTrue(corr[0]["provenance_preserved"])

    def test_exact_git_blob_and_ref_provenance(self):
        expected_freeze_blob = "4e453eb63c662f167735ed929aa14d3cff88ddf6"
        self.assertEqual(
            git_blob("research/paper2/p399/g4/genealogy_w5_int_09_10_11_12/W5_SOURCE_EVIDENCE_FREEZE_v1.json"),
            expected_freeze_blob,
        )
        for p in self.profiles["profiles"]:
            for ev in p["original_source_evidence"]:
                self.assertTrue(GITSHA.fullmatch(ev["repository_git_blob_sha1"]))
                self.assertTrue(GITSHA.fullmatch(ev["source_repository_ref"]))
                self.assertEqual(ev["repository_git_blob_sha1"], expected_freeze_blob)
        self.assertEqual(
            git_blob("research/paper2/p399/g4/genealogy_accelerator_v1/ORIGINAL_NATIVE_PROFILES_v1.json"),
            "903f8db6e1569ed27507cf47e668f7599a08cd98",
        )
        self.assertEqual(
            git_blob("research/paper2/p399/g4/genealogy_accelerator_v1/build_pair_matrix.py"),
            "4d9443d43ac911fbc3731c6f110c51abb8a0ed1c",
        )

    def test_no_global_independence_or_ancestry_exhaustiveness_promotion(self):
        for p in self.profiles["profiles"]:
            self.assertIs(p["global_family_independence_certified"], False)
            self.assertEqual(p["ancestry_exhaustiveness"], "NOT_ATTESTED")
        for r in self.pairs["pairs"]:
            self.assertIs(r["global_family_independence_certified"], False)
            self.assertEqual(r["ancestry_exhaustiveness"], "NOT_ATTESTED")
            self.assertFalse(r["main_authorization_promoted"])
        self.assertFalse(self.profiles["lane_gates"]["global_family_independence_certified"])
        self.assertFalse(self.pairs["lane_gates"]["global_family_independence_certified"])

    def test_pair_domain_counts_and_bounded_difference_never_promotes(self):
        rows = self.pairs["pairs"]
        self.assertEqual(len(rows), 110)
        self.assertEqual(len({r["pair_id"] for r in rows}), 110)
        self.assertTrue(all(r["result"] in ALLOWED_RESULTS for r in rows))
        for r in rows:
            if r["result"] == "BOUNDED_SOURCE_NATIVE_DIFFERENCE":
                self.assertIs(r["global_family_independence_certified"], False)
                self.assertFalse(r["main_authorization_promoted"])
        self.assertEqual(sum(bool(r["reused_existing_bounded_pair"]) for r in rows), 1)
        self.assertEqual(self.pairs["scope"]["newly_added_bounded_pair_count"], 109)

    def test_unverified_variant_never_canonical(self):
        for p in self.profiles["profiles"]:
            for v in p.get("model_variants", []):
                if not str(v.get("verification", "")).startswith("VERIFIED_IN_MAIN_SOURCE"):
                    self.assertIs(v.get("canonical"), False)

    def test_completion_statuses_and_main_no_go(self):
        statuses = {r["slot"]: r["status"] for r in self.gaps["status_by_paper"]}
        self.assertEqual(set(statuses), set(EXPECTED))
        self.assertTrue(all(v in ALLOWED_STATUS for v in statuses.values()))
        self.assertEqual(sum(v == "PROFILE_FRAGMENT_READY" for v in statuses.values()), 4)
        self.assertEqual(self.gaps["lane_blockers"]["source_blocked_count"], 0)
        self.assertEqual(self.gaps["lane_blockers"]["scientific_ancestry_underdetermined_count"], 0)
        self.assertFalse(self.gaps["fail_closed_gates"]["main_authorized"])
        self.assertFalse(self.freeze["lane_gates"]["main_authorized"])

    def test_isolation_only_w5_directory_changed_from_parent(self):
        changed = subprocess.check_output(
            ["git", "diff", "--name-only", f"{PARENT}..HEAD"], cwd=ROOT, text=True
        ).splitlines()
        prefix = "research/paper2/p399/g4/genealogy_w5_int_09_10_11_12/"
        self.assertTrue(changed)
        self.assertTrue(all(p.startswith(prefix) for p in changed), changed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
