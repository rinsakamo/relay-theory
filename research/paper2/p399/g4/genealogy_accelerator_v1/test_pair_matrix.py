#!/usr/bin/env python3
"""Destructive/fail-closed tests; synthetic fixtures are NOT scientific sources."""
import copy
import itertools
import unittest
from build_pair_matrix import InputMismatch, generate


def fixture():
    g2 = [{"slot": f"MAIN-{i:02}", "doi": f"10.1000/main{i}"} for i in range(40)]
    g1 = [{"id": f"P{i:02}", "doi": f"10.1000/pilot{i}"} for i in range(20)]
    m = [{"a": x["slot"], "b": y["slot"], "doi_a": x["doi"], "doi_b": y["doi"],
          "source_citation": None, "prior_logged_risk": None}
         for x, y in itertools.combinations(g2, 2)]
    e = [{"main_id": x["slot"], "g1_id": y["id"], "main_doi": x["doi"],
          "g1_doi": y["doi"], "source_citation": None, "prior_risk": None}
         for x, y in itertools.product(g2, g1)]
    return {"selected_working_roster": g2}, {"roster_snapshot": g1}, {
        "main_main_pairs": m, "main_g1_pairs": e
    }, {"schema": "blank", "profiles": []}


class MatrixTests(unittest.TestCase):
    def setUp(self):
        self.args = fixture()

    def test_full_1580_complete_no_invented_independence(self):
        rows, summary = generate(*self.args)
        self.assertEqual((len(rows), summary["g2_internal_pairs_checked"],
                          summary["g2_g1_pairs_checked"]), (1580, 780, 800))
        self.assertEqual(summary["global_final_independent_pairs"], 0)
        self.assertTrue(all(not r["global_independence_certified"] and
                            r["scientific_family_decision"] == "UNDERDETERMINED"
                            for r in rows))

    def test_existing_risks_citations_prioritized_without_clearance(self):
        self.args[2]["main_main_pairs"][0]["prior_logged_risk"] = {"kind": "SHARED_CORE"}
        self.args[2]["main_g1_pairs"][0]["source_citation"] = "archived original"
        rows, _ = generate(*self.args)
        self.assertEqual(sum(r["priority"] == 1 for r in rows), 1)
        self.assertEqual(sum(r["priority"] == 2 for r in rows), 1)
        self.assertEqual(sum(r["global_independence_certified"] for r in rows), 0)

    def test_known_exact_doi_collision_is_not_silently_admitted(self):
        # Synthetic same DOI across cohorts is detected rather than lost.
        self.args[1]["roster_snapshot"][0]["doi"] = self.args[0]["selected_working_roster"][0]["doi"]
        for row in self.args[2]["main_g1_pairs"]:
            if row["g1_id"] == "P00":
                row["g1_doi"] = self.args[1]["roster_snapshot"][0]["doi"]
        rows, _ = generate(*self.args)
        self.assertEqual(sum(r["triage"] == "EXACT_DOI_CONFLICT" for r in rows), 1)

    def test_missing_one_pair_is_a_hard_error(self):
        self.args[2]["main_main_pairs"].pop()
        with self.assertRaises(InputMismatch):
            generate(*self.args)

    def test_duplicate_pair_is_a_hard_error(self):
        self.args[2]["main_g1_pairs"][1] = copy.deepcopy(self.args[2]["main_g1_pairs"][0])
        with self.assertRaises(InputMismatch):
            generate(*self.args)

    def test_roster_drift_is_a_hard_error(self):
        self.args[1]["roster_snapshot"][0]["doi"] = "10.1000/changed"
        with self.assertRaises(InputMismatch):
            generate(*self.args)

    def test_unverified_profile_is_rejected(self):
        self.args[3]["profiles"] = [{"id": "MAIN-00", "native_core_operators": ["RL"]}]
        with self.assertRaises(InputMismatch):
            generate(*self.args)

    def test_grounded_common_operator_still_not_independence_or_collision(self):
        common = dict(native_core_operators=["SOURCE_DEFINED_OPERATOR_X"],
                      direct_model_ancestors=[], edition_sha256="a"*64,
                      original_source_evidence=[{"locator": "source page", "claim": "bounded"}])
        self.args[3]["profiles"] = [
            dict({"id": "MAIN-00"}, **common),
            dict({"id": "MAIN-01"}, **common),
        ]
        rows, summary = generate(*self.args)
        pair = next(r for r in rows if {r["a"], r["b"]} == {"MAIN-00", "MAIN-01"})
        self.assertEqual(pair["triage"], "PROFILE_STRUCTURAL_CANDIDATE_REVIEW")
        self.assertEqual(pair["scientific_family_decision"], "UNDERDETERMINED")
        self.assertEqual(summary["global_final_independent_pairs"], 0)


if __name__ == "__main__":
    unittest.main()
