#!/usr/bin/env python3
import json
import re
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROFILES = HERE / "W3_SOURCE_NATIVE_PROFILE_FRAGMENTS_v1.json"
PAIRS = HERE / "W3_BOUNDED_PAIR_ADJUDICATIONS_v1.json"
GAPS = HERE / "W3_SOURCE_GAPS_AND_BLOCKERS_v1.json"

EXPECTED = {
    "MEM-01": "10.1007/s42113-023-00189-y",
    "MEM-02": "10.1371/journal.pcbi.1008367",
    "MEM-03": "10.1371/journal.pcbi.1004003",
    "PRD-02": "10.1371/journal.pcbi.1001003",
    "PRD-03": "10.1371/journal.pcbi.1007093",
    "SKL-01": "10.1371/journal.pcbi.1012455",
    "SKL-02": "10.1371/journal.pcbi.1005632",
    "SKL-03": "10.1371/journal.pcbi.1006839",
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
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(ref, path):
    return subprocess.run(
        ["git", "rev-parse", f"{ref}:{path}"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()


class W3FailClosed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = load(PROFILES)
        cls.r = load(PAIRS)
        cls.g = load(GAPS)
        cls.profiles = cls.p["profiles"]

    def test_exact_eight_identity_and_no_prd01_profile(self):
        self.assertEqual(len(self.profiles), 8)
        ids = [p["id"] for p in self.profiles]
        dois = [p["doi"].lower() for p in self.profiles]
        self.assertEqual(set(ids), set(EXPECTED))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(dois), len(set(dois)))
        self.assertNotIn("PRD-01", ids)
        self.assertEqual({p["id"]: p["doi"].lower() for p in self.profiles},
                         {k: v.lower() for k, v in EXPECTED.items()})

    def test_status_and_ancestry_fail_closed(self):
        for p in self.profiles:
            self.assertIn(p["status"], ALLOWED_STATUS)
            self.assertEqual(p["ancestry_exhaustiveness"], "NOT_ATTESTED")
            self.assertIs(p["global_family_independence_certified"], False)
            for op in p["native_core_operators"]:
                self.assertTrue(op.startswith(p["id"] + ":"), op)
        self.assertIs(self.p["global_family_independence_certified"], False)
        self.assertIs(self.p["main_scientific_authorization"], False)
        self.assertEqual(self.p["ancestry_exhaustiveness"], "NOT_ATTESTED")

    def test_source_provenance_refs_and_hash_shapes(self):
        seen = set()
        for p in self.profiles:
            edition_sha = p["adopted_source_edition"].get("raw_sha256")
            if edition_sha is not None:
                self.assertRegex(edition_sha, HEX64)
            for ev in p["original_source_evidence"]:
                path = ev["repository_path"]
                ref = ev["source_repository_ref"]
                blob = ev["repository_git_blob_sha1"]
                self.assertRegex(blob, HEX40)
                self.assertRegex(ref, HEX40)
                actual = git_blob(ref, path)
                self.assertEqual(actual, blob, (p["id"], ref, path))
                raw = ev.get("original_primary_sha256")
                if raw is not None:
                    self.assertRegex(raw, HEX64)
                seen.add((ref, path, blob))
        self.assertGreaterEqual(len(seen), 2)

    def test_mandatory_supplements_cannot_disappear_or_promote(self):
        blockers = {x["id"]: x for x in self.g["blocking_gaps"]}
        required_blocked = {"MEM-03", "SKL-01", "SKL-03"}
        self.assertEqual(set(blockers), required_blocked)
        by_id = {p["id"]: p for p in self.profiles}
        for ident in required_blocked:
            self.assertEqual(by_id[ident]["status"], "SOURCE_BLOCKED")
            mandatory = [
                x for x in by_id[ident].get("additional_edition_bundle", [])
                if x.get("mandatory_for_profile_closure")
            ]
            self.assertTrue(mandatory)
            blocker_dois = {
                m["doi"].lower()
                for m in blockers[ident]["required_material"]
                if m.get("doi")
            }
            self.assertEqual(
                {m["doi"].lower() for m in mandatory if m.get("doi")},
                blocker_dois,
            )
            for m in mandatory:
                if m.get("sha256") is None:
                    self.assertTrue(m.get("blocker"))

    def test_gap_statuses_exactly_match_profiles(self):
        statuses = {p["id"]: p["status"] for p in self.profiles}
        self.assertEqual(self.g["exact_statuses"], statuses)
        self.assertIs(self.g["fail_closed_rules"]["global_family_independence_certified"], False)
        self.assertIs(self.g["fail_closed_rules"]["main_scientific_authorization"], False)
        self.assertIs(self.g["fail_closed_rules"]["blocked_source_cannot_become_ready"], True)
        self.assertIs(self.g["fail_closed_rules"]["bounded_pair_difference_is_not_global_independence"], True)

    def test_pair_coverage_and_no_global_promotion(self):
        rows = self.r["pair_adjudications"]
        self.assertEqual(len(rows), 236)
        self.assertEqual(self.r["inspection_coverage"]["w3_internal_pairs"], 28)
        self.assertEqual(self.r["inspection_coverage"]["w3_x_g1_pairs"], 160)
        self.assertEqual(self.r["inspection_coverage"]["w3_x_current_profiled_g2_pairs"], 48)
        self.assertEqual(self.r["inspection_coverage"]["total_pairs"], 236)
        keys = []
        for row in rows:
            self.assertIn(row["judgment"], ALLOWED_JUDGMENT)
            self.assertIs(row["global_independence_conclusion"], False)
            self.assertIs(row["may_be_counted_independent"], False)
            if row["judgment"] == "BOUNDED_SOURCE_NATIVE_DIFFERENCE":
                self.assertIs(row["global_independence_conclusion"], False)
            keys.append(tuple(sorted((row["a"], row["b"]))))
        self.assertEqual(len(keys), len(set(keys)))
        self.assertIs(self.r["global_family_independence_certified"], False)
        self.assertIs(self.r["main_scientific_authorization"], False)

    def test_pair_judgment_counts_are_derived(self):
        counts = {}
        for row in self.r["pair_adjudications"]:
            counts[row["judgment"]] = counts.get(row["judgment"], 0) + 1
        self.assertEqual(counts, self.r["judgment_counts"])
        self.assertEqual(sum(counts.values()), 236)

    def test_prd01_only_comparison_target_not_new_profile(self):
        self.assertNotIn("PRD-01", {p["id"] for p in self.profiles})
        self.assertTrue(any(
            "PRD-01" in {row["a"], row["b"]}
            for row in self.r["pair_adjudications"]
        ))

    def test_main_never_authorized(self):
        self.assertIs(self.p["main_scientific_authorization"], False)
        self.assertIs(self.r["main_scientific_authorization"], False)
        self.assertIs(self.g["fail_closed_rules"]["main_scientific_authorization"], False)


if __name__ == "__main__":
    unittest.main()
