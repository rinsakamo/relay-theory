#!/usr/bin/env python3
import copy
import importlib.util
import json
import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("w8g", HERE / "w8g_audit.py")
w8g = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(w8g)

def context():
    g1 = w8g.git_json(w8g.G1_REF, w8g.G1_ROSTER_PATH)["roster_snapshot"]
    g2 = w8g.load(w8g.G2_ROSTER_PATH)["selected_working_roster"]
    g1_ids = [x["id"] for x in g1]
    g2_ids = [x["slot"] for x in g2]
    g1_dois = {x["id"]: w8g.normdoi(x["doi"]) for x in g1}
    g2_dois = {x["slot"]: w8g.normdoi(x["doi"]) for x in g2}
    profiles = {p["id"]: p for p in w8g.load(w8g.PROFILES_PATH)["profiles"]}
    recon = w8g.load(w8g.RECON_PATH)
    unresolved = {x["id"]: x["status"] for x in recon["blocked"] + recon["scientific_ancestry_underdetermined"]}
    order = {x: i for i, x in enumerate(g1_ids)}
    rules = w8g.pair_rules(profiles, order)
    registry = w8g.build_registry(g1_ids, g1_dois, profiles, rules, order)
    graph = w8g.build_graph({**g1_dois, **g2_dois}, profiles, unresolved, rules, order)
    signals = w8g.derive_signals(registry, graph)
    return g1_ids, g2_ids, g1_dois, profiles, unresolved, order, rules, registry, graph, signals

class W8GDestructiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (cls.g1_ids, cls.g2_ids, cls.g1_dois, cls.profiles, cls.unresolved,
         cls.order, cls.rules, cls.registry, cls.graph, cls.signals) = context()

    def row(self, a, b):
        a, b = w8g.canonical_pair(a, b, self.order)
        return next(x for x in self.registry if x["a"] == a and x["b"] == b)

    def signal(self, a, b):
        a, b = w8g.canonical_pair(a, b, self.order)
        pid = f"G1G1::{a}::{b}"
        return next(x for x in self.signals["signals"] if x["pair_id"] == pid)

    def test_01_exact_190_g1_pairs(self):
        self.assertEqual(len(self.registry), 190)
        self.assertEqual(len({x["pair_id"] for x in self.registry}), 190)

    def test_02_duplicate_pair_rejection(self):
        with self.assertRaises(w8g.W8GError):
            w8g.enumerate_pairs(["P05", "P05"])

    def test_03_reversed_pair_canonicalization(self):
        self.assertEqual(
            w8g.canonical_pair("P17", "P11", self.order),
            w8g.canonical_pair("P11", "P17", self.order),
        )

    def test_04_self_pair_rejection(self):
        with self.assertRaises(w8g.W8GError):
            w8g.canonical_pair("P11", "P11", self.order)

    def test_05_missing_profile_fail_closed(self):
        broken = dict(self.profiles)
        broken.pop("P11")
        with self.assertRaises(w8g.W8GError):
            w8g.build_registry(self.g1_ids, self.g1_dois, broken, {}, self.order)

    def test_06_fabricated_ancestry_edge_rejection(self):
        bad = copy.deepcopy(self.graph)
        bad["edges"].append({
            "edge_id": "FABRICATED",
            "source": "paper:P11",
            "target": "paper:P17",
            "relation_type": "DIRECT_EXTENSION",
            "directed": True,
            "attested": False,
            "provenance": [],
            "global_independence_implication": False,
        })
        with self.assertRaises(w8g.W8GError):
            w8g.validate_graph_edges(bad)

    def test_07_citation_absence_not_independence(self):
        row = self.row("P05", "P20")
        self.assertEqual(row["normalized_scientific_category"], "UNDERDETERMINED")
        self.assertFalse(row["global_independence_certified"])

    def test_08_no_graph_path_not_independence(self):
        s = self.signal("P05", "P20")
        self.assertIn("NO_PATH_FOUND", s["signals"])
        self.assertFalse(s["independence_judgment"])

    def test_09_shared_constituent_not_whole_family_identity(self):
        row = self.row("P11", "P17")
        self.assertEqual(row["normalized_scientific_category"], "SHARED_CONSTITUENT_ONLY")
        self.assertFalse(row["global_independence_certified"])

    def test_10_bounded_difference_not_independence(self):
        row = self.row("P11", "P12")
        self.assertEqual(row["normalized_scientific_category"], "BOUNDED_SOURCE_NATIVE_DIFFERENCE")
        self.assertFalse(row["global_independence_certified"])

    def test_11_direct_common_ancestor_generates_risk_signal(self):
        row = self.row("P18", "PF04")
        sig = self.signal("P18", "PF04")
        self.assertEqual(row["normalized_scientific_category"], "DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY")
        self.assertIn("COMMON_EXPLICIT_ANCESTOR", sig["signals"])
        self.assertFalse(sig["independence_judgment"])

    def test_12_source_edition_mismatch_blocks_inference(self):
        key = w8g.canonical_pair("P11", "P17", self.order)
        prov = copy.deepcopy(self.rules[key]["provenance"])
        prov[0]["edition_sha256"] = "0" * 64
        with self.assertRaises(w8g.W8GError):
            w8g.validate_provenance(prov, self.profiles)

    def test_13_p08_substantive_scientific_correction_survives(self):
        text = json.dumps(self.profiles["P08"], ensure_ascii=False)
        self.assertIn("mandatory_official_normative_correction", text)
        self.assertIn("original normative optimal distinct claim superseded", text)
        self.assertIn("corrected-sequential-recursion", text)

    def test_14_p10_funding_only_correction_not_scientific_model_change(self):
        text = json.dumps(self.profiles["P10"], ensure_ascii=False)
        self.assertIn("funding_only_official_correction", text)
        self.assertIn("Correction changes funding only", text)

    def test_15_p20_source_conflict_not_silently_resolved(self):
        text = json.dumps(self.profiles["P20"], ensure_ascii=False)
        self.assertIn("p=.944", text)
        self.assertIn("p=.44", text)
        self.assertIn("no corrected numeric winner", text)

    def test_16_pf04_author_exception_not_publisher_corrigendum(self):
        text = json.dumps(self.profiles["PF04"], ensure_ascii=False)
        self.assertIn("author-approved Eq10", text)
        self.assertIn("NOT publisher corrected equation", text)

    def test_17_unresolved_non_doi_ancestor_remains_opaque(self):
        node = next(x for x in self.graph["nodes"] if x["node_id"] == "opaque:w8a:daw_niv_dayan_2005_mb_mf")
        self.assertEqual(node["identity_status"], "OPAQUE_PENDING_W8A")
        self.assertIsNone(node["doi"])
        self.assertTrue(node["incomplete"])

    def test_18_all_scientific_global_independence_flags_false(self):
        self.assertTrue(all(x["global_independence_certified"] is False for x in self.registry))
        self.assertFalse(self.graph["global_independence_certified"])

    def test_19_main_authorization_remains_false(self):
        self.assertTrue(all(x["main_authorized"] is False for x in self.registry))
        self.assertFalse(self.graph["main_authorized"])

    def test_20_future_1770_enumeration(self):
        plan = w8g.build_w9_plan(self.g1_ids, self.g2_ids)
        self.assertEqual(plan["g1_g1"], 190)
        self.assertEqual(plan["g2_g2"], 780)
        self.assertEqual(plan["g2_g1"], 800)
        self.assertEqual(plan["total"], 1770)

    def test_21_normalized_scientific_vocabulary_exact(self):
        self.assertEqual(w8g.ALLOWED, {
            "DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY",
            "SHARED_CONSTITUENT_ONLY",
            "BOUNDED_SOURCE_NATIVE_DIFFERENCE",
            "UNDERDETERMINED",
        })

    def test_22_duplicate_graph_edge_rejected(self):
        bad = copy.deepcopy(self.graph)
        bad["edges"].append(copy.deepcopy(bad["edges"][0]))
        with self.assertRaises(w8g.W8GError):
            w8g.validate_graph_edges(bad)

    def test_23_g1_authority_is_exactly_20(self):
        self.assertEqual(len(self.g1_ids), 20)
        self.assertTrue(all(x in self.profiles for x in self.g1_ids))

    def test_24_w7_incomplete_graph_nodes_are_marked(self):
        incomplete_papers = [n for n in self.graph["nodes"] if n["node_class"] == "SELECTED_PAPER" and n["incomplete"]]
        self.assertEqual(len(incomplete_papers), 9)
        self.assertEqual({n["paper_id"] for n in incomplete_papers}, set(self.unresolved))

if __name__ == "__main__":
    unittest.main()
