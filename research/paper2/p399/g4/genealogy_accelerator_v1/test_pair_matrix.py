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
        "main_main_pairs": m, "main_vs_g1_pairs": e
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
        self.args[2]["main_vs_g1_pairs"][0]["source_citation"] = "archived original"
        rows, _ = generate(*self.args)
        self.assertEqual(sum(r["priority"] == 1 for r in rows), 1)
        self.assertEqual(sum(r["priority"] == 2 for r in rows), 1)
        self.assertEqual(sum(r["global_independence_certified"] for r in rows), 0)

    def test_known_exact_doi_collision_is_not_silently_admitted(self):
        # Synthetic same DOI across cohorts is detected rather than lost.
        self.args[1]["roster_snapshot"][0]["doi"] = self.args[0]["selected_working_roster"][0]["doi"]
        for row in self.args[2]["main_vs_g1_pairs"]:
            if row["g1_id"] == "P00":
                row["g1_doi"] = self.args[1]["roster_snapshot"][0]["doi"]
        rows, _ = generate(*self.args)
        self.assertEqual(sum(r["triage"] == "EXACT_DOI_CONFLICT" for r in rows), 1)

    def test_missing_one_pair_is_a_hard_error(self):
        self.args[2]["main_main_pairs"].pop()
        with self.assertRaises(InputMismatch):
            generate(*self.args)

    def test_duplicate_pair_is_a_hard_error(self):
        self.args[2]["main_vs_g1_pairs"][1] = copy.deepcopy(self.args[2]["main_vs_g1_pairs"][0])
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

    def bounded_profile(self, ident, doi, ancestors=None):
        return {
            "id": ident, "doi": doi,
            "profile_state": "LEDGER_DERIVED_BOUNDED_NO_NEW_SOURCE_QUALIFICATION",
            "global_family_independence_certified": False,
            "ancestry_exhaustiveness": "NOT_ATTESTED",
            "native_core_operators": [ident + ":local-core"],
            "operator_source_descriptions": {
                ident + ":local-core": "Source-recorded narrow operator description, not a general-family label"
            },
            "direct_model_ancestors": ancestors or [],
            "edition_sha256": "a" * 64,
            "original_source_evidence": [{
                "source_audit_kind": "PREEXISTING_FROZEN_BOUNDED_LEDGER_NOT_NEW_INDEPENDENT_READING",
                "original_primary_sha256": "a" * 64,
                "repository_git_blob_sha1": "b" * 40,
                "source_repository_ref": "c" * 40,
                "repository_path": "research/paper2/p399/synthetic_source.json",
                "source_loci": ["synthetic test page"]
            }]
        }

    def test_local_operator_strings_do_not_auto_match(self):
        self.args[3]["profiles"] = [
            self.bounded_profile("MAIN-00", "10.1000/main0"),
            self.bounded_profile("MAIN-01", "10.1000/main1")
        ]
        rows, summary = generate(*self.args)
        pair = next(r for r in rows if {r["a"], r["b"]} == {"MAIN-00", "MAIN-01"})
        self.assertEqual(pair["priority"], 4)
        self.assertEqual(summary["global_final_independent_pairs"], 0)

    def test_direct_declared_doi_ancestor_is_priority_only(self):
        self.args[3]["profiles"] = [
            self.bounded_profile("MAIN-00", "10.1000/main0", ["10.1000/main1"]),
            self.bounded_profile("MAIN-01", "10.1000/main1")
        ]
        rows, _ = generate(*self.args)
        pair = next(r for r in rows if {r["a"], r["b"]} == {"MAIN-00", "MAIN-01"})
        self.assertEqual(pair["triage"], "PROFILE_STRUCTURAL_CANDIDATE_REVIEW")
        self.assertFalse(pair["global_independence_certified"])

    def test_profile_roster_doi_drift_hard_error(self):
        self.args[3]["profiles"] = [self.bounded_profile("MAIN-00", "10.1000/other")]
        with self.assertRaises(InputMismatch):
            generate(*self.args)

    def test_source_ledger_reference_sha_validation_hard_error(self):
        p = self.bounded_profile("MAIN-00", "10.1000/main0")
        p["original_source_evidence"][0]["repository_git_blob_sha1"] = "not_sha"
        self.args[3]["profiles"] = [p]
        with self.assertRaises(InputMismatch):
            generate(*self.args)

    def test_unattested_scientific_qualification_hard_error(self):
        p = self.bounded_profile("MAIN-00", "10.1000/main0")
        p["global_family_independence_certified"] = True
        self.args[3]["profiles"] = [p]
        with self.assertRaises(InputMismatch):
            generate(*self.args)


    def native_fixture(self):
        g2_data, g1_data, legacy, profiles = fixture()
        id_map = {}
        for i in range(16):
            old = g2_data["selected_working_roster"][i]["slot"]
            new = f"INT-{i+1:02d}"
            g2_data["selected_working_roster"][i]["slot"] = new
            id_map[old] = new
        for row in legacy["main_main_pairs"]:
            row["a"] = id_map.get(row["a"], row["a"])
            row["b"] = id_map.get(row["b"], row["b"])
        for row in legacy["main_vs_g1_pairs"]:
            row["main_id"] = id_map.get(row["main_id"], row["main_id"])
        subject_doi = g2_data["selected_working_roster"][0]["doi"]
        pairs = []
        for item in g2_data["selected_working_roster"][1:16]:
            pairs.append({"other_lane": "G2_INT", "other_slot": item["slot"],
                          "doi": item["doi"], "source_scoped_only": False,
                          "final_central_family_independent_certified": False,
                          "original_family_analysis": "NOT_YET_EXECUTED"})
        for item in g1_data["roster_snapshot"]:
            pairs.append({"other_lane": "G1", "other_slot": item["id"], "doi": item["doi"],
                          "final_central_family_independent_certified": False,
                          "original_family_analysis": "NOT_YET_EXECUTED"})
        for row in (pairs[0], pairs[15]):
            row["source_scoped_evidence_id"] = "SOURCE_TEST_PIN"
            row["source_scoped_only"] = True
            row["original_family_analysis"] = "BOUNDED_DIFFERENT_TEST"
        native = {"updated_original35_matrix": {
            "subject": {"slot": "INT-01", "doi": subject_doi}, "pairs": pairs
        }}
        return (g2_data, g1_data, legacy, profiles, native)

    def test_bounded_native_reuse_without_global_clearance(self):
        rows, summary = generate(*self.native_fixture())
        self.assertEqual(summary["prior_indexed_native_scoped_pairs_reused"], 2)
        self.assertEqual(sum(r.get("prior_source_scoped_comparison") is not None for r in rows), 2)
        self.assertEqual(summary["global_final_independent_pairs"], 0)

    def test_native_peer_doi_drift_hard_error(self):
        args = list(self.native_fixture())
        args[4]["updated_original35_matrix"]["pairs"][0]["doi"] = "10.1000/WRONG"
        with self.assertRaises(InputMismatch):
            generate(*args)

    def test_native_false_global_promotion_hard_error(self):
        args = list(self.native_fixture())
        args[4]["updated_original35_matrix"]["pairs"][0]["final_central_family_independent_certified"] = True
        with self.assertRaises(InputMismatch):
            generate(*args)


    def test_pair_local_int04_int08_source_reuse_only(self):
        args = list(self.native_fixture())
        g2 = {x["slot"]: x["doi"] for x in args[0]["selected_working_roster"]}
        limited = {
            "official_sources": {
                "INT-04": {"doi": g2["INT-04"], "raw_main20_sha256": "a"*64},
                "INT-08": {"doi": g2["INT-08"], "exact_G2_inherited_raw_sha256": "b"*64,
                           "manual_policy_hand_imposed_detected_on_corrected_run": True}
            },
            "source_native_pairwise_delta": {
                "distinct_local_primary_learning_target_and_operations_source_confirmed": True,
                "pairwise_all_figures_math_complete_qualified": False,
                "full_G1_20_G2_40_independent_family_cleared": False
            },
            "MAIN_authorized": False
        }
        rows, summary = generate(*args, limited)
        self.assertEqual(summary["prior_indexed_native_scoped_pairs_reused"], 3)
        pair = next(r for r in rows if {r["a"], r["b"]} == {"INT-04", "INT-08"})
        self.assertEqual(pair["triage"], "BOUNDED_SOURCE_COMPARISON_GLOBAL_REVIEW_PENDING")
        self.assertFalse(pair["global_independence_certified"])

    def test_pair_local_native_false_full_family_promotion_rejected(self):
        args = list(self.native_fixture())
        g2 = {x["slot"]: x["doi"] for x in args[0]["selected_working_roster"]}
        limited = {
            "official_sources": {
                "INT-04": {"doi": g2["INT-04"], "raw_main20_sha256": "a"*64},
                "INT-08": {"doi": g2["INT-08"], "exact_G2_inherited_raw_sha256": "b"*64,
                           "manual_policy_hand_imposed_detected_on_corrected_run": True}
            },
            "source_native_pairwise_delta": {
                "distinct_local_primary_learning_target_and_operations_source_confirmed": True,
                "pairwise_all_figures_math_complete_qualified": False,
                "full_G1_20_G2_40_independent_family_cleared": True
            },
            "MAIN_authorized": False
        }
        with self.assertRaises(InputMismatch):
            generate(*args, limited)


if __name__ == "__main__":
    unittest.main()
