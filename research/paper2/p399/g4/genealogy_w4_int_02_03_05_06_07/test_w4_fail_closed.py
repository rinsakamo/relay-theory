#!/usr/bin/env python3
import json
import re
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
BASE = "ae044a8f475fb0dc9140a91e360e1ff26a0b5e3a"
SHARED = "research/paper2/p399/g4/genealogy_accelerator_v1/ORIGINAL_NATIVE_PROFILES_v1.json"
SHARED_BLOB = "903f8db6e1569ed27507cf47e668f7599a08cd98"
PREFIX = "research/paper2/p399/g4/genealogy_w4_int_02_03_05_06_07/"
EXPECTED = {
    "INT-02": "10.3390/e26060484",
    "INT-03": "10.1073/pnas.95.24.14529",
    "INT-05": "10.1371/journal.pcbi.1004110",
    "INT-06": "10.1371/journal.pcbi.1000765",
    "INT-07": "10.1371/journal.pcbi.1003383",
}
EXPECTED_SHA = {
    "INT-02": "a1e644c826bf1b356187bc556d5947eb23638f3f9bc6c61835d46850b4f1cc37",
    "INT-03": None,
    "INT-05": "6a0445b1569b98af90615f5d78664e4935fea4a9e0a8a14799c22da8bf5fbb95",
    "INT-06": "c276294fa7a111e5df98f35aa0da933af28d45a1e1347940a1b57753c0980706",
    "INT-07": "a22b6e5ff2822a62b471cb8141529b7ed3350cb2f5b3f2be61ea45b464b56698",
}
ALLOWED = {"PROFILE_FRAGMENT_READY", "SOURCE_BLOCKED", "SCIENTIFIC_ANCESTRY_UNDERDETERMINED"}

def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))

def rev(spec):
    return subprocess.check_output(["git", "rev-parse", spec], cwd=ROOT, text=True).strip()

class W4FailClosed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = load("W4_SOURCE_NATIVE_PROFILE_FRAGMENTS_v1.json")
        cls.q = load("W4_BOUNDED_PAIR_ADJUDICATIONS_v1.json")
        cls.b = load("W4_SOURCE_GAPS_AND_BLOCKERS_v1.json")
        cls.rows = cls.p["profiles"]

    def test_exact_five_doi_identities_and_comparison_only_slots_absent(self):
        self.assertEqual({x["id"]: x["doi"] for x in self.rows}, EXPECTED)
        self.assertEqual(len(self.rows), 5)
        self.assertTrue({"INT-01", "INT-04", "INT-08"}.isdisjoint({x["id"] for x in self.rows}))

    def test_no_duplicate_or_nonlocal_operator_ids(self):
        ops = [o for x in self.rows for o in x["native_core_operators"]]
        self.assertEqual(len(ops), len(set(ops)))
        for x in self.rows:
            self.assertEqual(len(x["native_core_operators"]), len(set(x["native_core_operators"])))
            self.assertTrue(all(o.startswith(x["id"] + ":") for o in x["native_core_operators"]))

    def test_exact_source_git_blob_ref_validation(self):
        for x in self.rows:
            for e in x["original_source_evidence"]:
                self.assertEqual(e["source_repository_ref"], BASE)
                self.assertEqual(rev(BASE + ":" + e["repository_path"]), e["repository_git_blob_sha1"])
        self.assertEqual(rev(BASE + ":" + SHARED), SHARED_BLOB)
        self.assertEqual(rev("HEAD:" + SHARED), SHARED_BLOB)

    def test_mandatory_source_hashes_cannot_disappear(self):
        for x in self.rows:
            self.assertEqual(x["edition_sha256"], EXPECTED_SHA[x["id"]])
            if x["source_hash_required"]:
                self.assertRegex(x["edition_sha256"], r"^[0-9a-f]{64}$")
            else:
                self.assertEqual(x["id"], "INT-03")
                self.assertIsNone(x["edition_sha256"])
                self.assertIn("NO HASH INVENTED", x["source_hash_status"])

    def test_no_global_independence_or_ancestry_exhaustiveness_promotion(self):
        for x in self.rows:
            self.assertFalse(x["global_family_independence_certified"])
            self.assertEqual(x["ancestry_exhaustiveness"], "NOT_ATTESTED")
            self.assertIn(x["completion_status"], ALLOWED)

    def test_int06_all_eight_supplement_hashes_frozen(self):
        x = next(x for x in self.rows if x["id"] == "INT-06")
        supp = x["required_supplements_or_corrections"]
        self.assertEqual(len(supp), 8)
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{64}", s["sha256"]) for s in supp))

    def test_int07_missing_required_supplements_forces_source_blocked(self):
        x = next(x for x in self.rows if x["id"] == "INT-07")
        self.assertEqual(x["completion_status"], "SOURCE_BLOCKED")
        self.assertEqual(
            [s["doi"] for s in x["required_supplements_or_corrections"]],
            [f"10.1371/journal.pcbi.1003383.s00{i}" for i in range(1, 5)],
        )
        self.assertTrue(all(s["sha256"] is None and s["status"] == "REQUIRED_RAW_NOT_FROZEN"
                            for s in x["required_supplements_or_corrections"]))

    def test_broad_workspace_relationship_cannot_promote_exact_family(self):
        row = next(r for r in self.q["adjudications"] if {r["a"], r["b"]} == {"INT-03", "INT-06"})
        self.assertEqual(row["judgment"], "SHARED_CONSTITUENT_ONLY")
        self.assertFalse(row["exact_same_central_mathematical_model_proven"])
        self.assertFalse(row["global_family_independence_promoted"])

    def test_bounded_operator_difference_cannot_promote_independence(self):
        rows = [r for r in self.q["adjudications"] if r["judgment"] == "BOUNDED_SOURCE_NATIVE_DIFFERENCE"]
        self.assertEqual(len(rows), 9)
        self.assertTrue(all(not r["global_family_independence_promoted"] for r in rows))

    def test_pair_registry_exact_scope_and_unique_pairs(self):
        self.assertEqual(len(self.q["adjudications"]), 140)
        keys = [tuple(sorted((r["a"], r["b"]))) for r in self.q["adjudications"]]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(self.q["reused_bounded_pair_count"], 1)
        self.assertEqual(self.q["new_bounded_pair_count"], 9)

    def test_main_authorization_remains_false(self):
        self.assertFalse(self.p["scope"]["main_authorized"])
        self.assertFalse(self.q["policies"]["main_authorized"])
        self.assertFalse(self.b["main_authorized"])

    def test_only_w4_directory_changed_from_pr438_head(self):
        changed = subprocess.check_output(["git", "diff", "--name-only", BASE + "..HEAD"], cwd=ROOT, text=True).splitlines()
        self.assertTrue(changed)
        self.assertTrue(all(p.startswith(PREFIX) for p in changed), changed)

if __name__ == "__main__":
    unittest.main()
