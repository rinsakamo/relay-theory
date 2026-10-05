import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent
PROFILES = json.loads((ROOT / "W2_SOURCE_NATIVE_PROFILE_FRAGMENTS_v1.json").read_text())
PAIRS = json.loads((ROOT / "W2_BOUNDED_PAIR_ADJUDICATIONS_v1.json").read_text())
GAPS = json.loads((ROOT / "W2_SOURCE_GAPS_AND_BLOCKERS_v1.json").read_text())

EXPECTED = {
    "CTL-01": "10.1371/journal.pcbi.1012228",
    "CTL-02": "10.7554/eLife.12029",
    "CTL-03": "10.7554/eLife.28040",
    "LRN-01": "10.1038/s41467-025-58848-6",
    "LRN-02": "10.1371/journal.pcbi.1007963",
    "LRN-03": "10.7554/eLife.21492",
}
ALLOWED_STATUS = {
    "PROFILE_FRAGMENT_READY",
    "SOURCE_BLOCKED",
    "SCIENTIFIC_ANCESTRY_UNDERDETERMINED",
}
ALLOWED_JUDGMENT = {
    "DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY",
    "SHARED_CONSTITUENT_ONLY",
    "BOUNDED_SOURCE_NATIVE_DIFFERENCE",
    "UNDERDETERMINED",
}
SHA1 = re.compile(r"^[0-9a-f]{40}$")


class W2FailClosed(unittest.TestCase):
    def test_exact_six_doi_identities_and_no_duplicates(self):
        ps = PROFILES["profiles"]
        self.assertEqual(len(ps), 6)
        self.assertEqual({p["id"]: p["doi"] for p in ps}, EXPECTED)
        self.assertEqual(len({p["doi"] for p in ps}), 6)

    def test_only_ctl_lrn_and_local_operator_ids(self):
        for p in PROFILES["profiles"]:
            self.assertTrue(p["id"].startswith(("CTL-", "LRN-")))
            for op in p["source_native_structure"]["paper_specific_operators"]:
                self.assertTrue(op.startswith(p["id"] + ":"), (p["id"], op))

    def test_status_and_global_promotion_fail_closed(self):
        self.assertFalse(PROFILES["main_scientific_authorization"])
        self.assertFalse(PROFILES["shared_profile_file_modified"])
        for p in PROFILES["profiles"]:
            self.assertIn(p["status"], ALLOWED_STATUS)
            self.assertFalse(p["global_family_independence_certified"])
            self.assertFalse(p["main_scientific_authorization"])
            self.assertEqual(p["ancestry_exhaustiveness"], "NOT_ATTESTED")

    def test_git_provenance_is_exactly_pinned(self):
        for p in PROFILES["profiles"]:
            self.assertTrue(p["source_provenance"])
            for src in p["source_provenance"]:
                self.assertTrue(src["repository_path"].startswith("research/paper2/p399/"))
                self.assertRegex(src["repository_git_blob_sha1"], SHA1)
                self.assertRegex(src["source_repository_ref"], SHA1)

    def test_required_supplements_cannot_disappear(self):
        gap_by_paper = {}
        for g in GAPS["gaps"]:
            gap_by_paper.setdefault(g["paper_id"], []).append(g)
        for p in PROFILES["profiles"]:
            bundle = {x["id"]: x for x in p["supplement_bundle"]}
            for required in p["required_bundle_ids"]:
                self.assertIn(required, bundle)
                self.assertTrue(bundle[required]["required_for_profile"])
            for g in gap_by_paper.get(p["id"], []):
                for required in g.get("must_preserve_bundle_ids", []):
                    self.assertIn(required, p["required_bundle_ids"])

    def test_source_blocked_paper_cannot_be_ready(self):
        status = {p["id"]: p["status"] for p in PROFILES["profiles"]}
        calculated = sum(bool(g["blocking"]) for g in GAPS["gaps"])
        self.assertEqual(GAPS["blocking_count"], calculated)
        for g in GAPS["gaps"]:
            if g["blocking"]:
                self.assertNotEqual(status[g["paper_id"]], "PROFILE_FRAGMENT_READY")
                self.assertEqual(status[g["paper_id"]], "SOURCE_BLOCKED")

    def test_pair_judgment_vocabulary_and_no_main_promotion(self):
        self.assertFalse(PAIRS["main_scientific_authorization"])
        self.assertFalse(PAIRS["global_family_independence_certified"])
        self.assertTrue(PAIRS["no_automatic_family_clearance"])
        self.assertEqual(PAIRS["bounded_pair_judgment_count"], len(PAIRS["pairs"]))
        for pair in PAIRS["pairs"]:
            self.assertIn(pair["judgment"], ALLOWED_JUDGMENT)
            self.assertFalse(pair["main_promotion_allowed"])
            self.assertFalse(pair["global_independence_inferred"])

    def test_all_fifteen_internal_w2_pairs_present(self):
        ids = sorted(EXPECTED)
        wanted = {
            "__".join(sorted((ids[i], ids[j])))
            for i in range(len(ids))
            for j in range(i + 1, len(ids))
        }
        actual = {
            p["pair_id"]
            for p in PAIRS["pairs"]
            if p["left"] in EXPECTED and p["right"] in EXPECTED
        }
        self.assertEqual(actual, wanted)
        self.assertEqual(len(actual), 15)

    def test_no_shared_accelerator_mutation_contract(self):
        forbidden = "research/paper2/p399/g4/genealogy_accelerator_v1/ORIGINAL_NATIVE_PROFILES_v1.json"
        self.assertFalse(PROFILES["shared_profile_file_modified"])
        for p in ROOT.iterdir():
            self.assertNotEqual(p.as_posix(), forbidden)


if __name__ == "__main__":
    unittest.main()
