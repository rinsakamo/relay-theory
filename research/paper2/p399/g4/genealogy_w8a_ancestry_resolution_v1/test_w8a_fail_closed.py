#!/usr/bin/env python3
import copy, json, pathlib, re, unittest

HERE=pathlib.Path(__file__).resolve().parent
SCHEMA=json.loads((HERE/"W8A_ANCESTRY_NODE_SCHEMA_PROPOSAL_v1.json").read_text())
RES=json.loads((HERE/"W8A_FOUR_PAPER_ANCESTRY_RESOLUTION_v1.json").read_text())
EDGE=json.loads((HERE/"W8A_ANCESTRY_EDGE_RECEIPTS_v1.json").read_text())
W9=json.loads((HERE/"W8A_W9_IMPORT_FRAGMENT_v1.json").read_text())

DOI_RE=re.compile(r"^10\.\d{4,9}/\S+$", re.I)
DIRECT={"DIRECT_ADAPTATION","DIRECT_EXTENSION","DIRECT_IMPLEMENTATION_DESCENT"}
ALL=set(SCHEMA["edge_vocabulary"])
REQ_NONDOI={"node_type","local_node_id","doi","doi_status","title","authors","year","venue","bibliographic_locator","publisher_or_proceedings_authority","stable_locators","descendant_citation_locus","identity_basis"}

def validate_non_doi(n):
    missing=REQ_NONDOI-set(n)
    if missing: raise ValueError(f"missing {sorted(missing)}")
    if n["node_type"]!="NON_DOI_BIBLIOGRAPHIC_WORK": raise ValueError("wrong node type")
    if n["doi"] is not None: raise ValueError("fabricated DOI")
    if not n["local_node_id"].startswith("rt-biblio-"): raise ValueError("unsafe local id")
    if DOI_RE.match(n["local_node_id"]): raise ValueError("local id resembles DOI")
    if not n["title"] or not n["authors"] or not n["year"] or not n["venue"]: raise ValueError("title-only/partial identity")
    if not n["stable_locators"]: raise ValueError("missing stable locator")
    if not all(x.get("url") and x.get("value") for x in n["stable_locators"]): raise ValueError("incomplete stable locator")
    if "DO NOT INVENT" not in n["doi_status"]: raise ValueError("non-DOI status not fail-closed")
    return True

def validate_edge(r):
    if r["edge_type"] not in ALL: raise ValueError("unknown edge type")
    if r["direct_ancestry_candidate"] != (r["edge_type"] in DIRECT):
        raise ValueError("direct flag disagrees with controlled vocabulary")
    if r["edge_type"] in {"RELATED_CITATION_ONLY","SHARED_FRAMEWORK","SHARED_CONSTITUENT","HISTORICAL_INSPIRATION","UNDERDETERMINED"} and r["direct_ancestry_candidate"]:
        raise ValueError("non-direct relation promoted")
    if r.get("global_independence_evidence") is not False:
        raise ValueError("ancestry receipt promoted to independence")
    return True

class W8AFailClosed(unittest.TestCase):
    def test_01_no_fabricated_doi_in_real_non_doi_nodes(self):
        for n in EDGE["non_doi_nodes"]: self.assertTrue(validate_non_doi(n))

    def test_02_non_doi_requires_complete_identity(self):
        n=copy.deepcopy(EDGE["non_doi_nodes"][0]); del n["authors"]
        with self.assertRaises(ValueError): validate_non_doi(n)

    def test_03_title_only_node_rejected(self):
        n={"node_type":"NON_DOI_BIBLIOGRAPHIC_WORK","title":"Only a title"}
        with self.assertRaises(ValueError): validate_non_doi(n)

    def test_04_local_synthetic_id_cannot_resemble_doi(self):
        n=copy.deepcopy(EDGE["non_doi_nodes"][0]); n["local_node_id"]="10.9999/fake"
        with self.assertRaises(ValueError): validate_non_doi(n)

    def test_05_non_doi_node_cannot_carry_doi(self):
        n=copy.deepcopy(EDGE["non_doi_nodes"][0]); n["doi"]="10.9999/invented"
        with self.assertRaises(ValueError): validate_non_doi(n)

    def test_06_citation_alone_cannot_be_direct(self):
        r={"edge_type":"RELATED_CITATION_ONLY","direct_ancestry_candidate":True,"global_independence_evidence":False}
        with self.assertRaises(ValueError): validate_edge(r)

    def test_07_shared_authorship_cannot_be_direct(self):
        # Shared authorship is not an allowed edge type and cannot enter the direct set.
        self.assertNotIn("SHARED_AUTHORSHIP", ALL)
        self.assertFalse("SHARED_AUTHORSHIP" in DIRECT)

    def test_08_broad_framework_cannot_be_exact_descent(self):
        r={"edge_type":"SHARED_FRAMEWORK","direct_ancestry_candidate":True,"global_independence_evidence":False}
        with self.assertRaises(ValueError): validate_edge(r)

    def test_09_unresolved_edge_cannot_be_independence_evidence(self):
        r={"edge_type":"UNDERDETERMINED","direct_ancestry_candidate":False,"global_independence_evidence":True}
        with self.assertRaises(ValueError): validate_edge(r)

    def test_10_all_real_receipts_validate(self):
        for r in EDGE["receipts"]: self.assertTrue(validate_edge(r))

    def test_11_four_statuses_are_exact_and_resolved(self):
        got={p["id"]:p["status"] for p in RES["papers"]}
        self.assertEqual(got,{
            "CNC-01":"ANCESTRY_RESOLVED_NON_DOI_NODE_REQUIRED",
            "MEM-01":"ANCESTRY_RESOLVED_NON_DOI_NODE_REQUIRED",
            "INT-03":"ANCESTRY_RESOLVED_DIRECT_EDGE",
            "INT-06":"ANCESTRY_RESOLVED_DIRECT_EDGE",
        })

    def test_12_direct_edge_count(self):
        self.assertEqual(EDGE["counts"]["direct_candidate_edges"],11)
        self.assertEqual(RES["summary"]["direct_ancestry_edges_resolved"],11)

    def test_13_exact_two_non_doi_nodes(self):
        self.assertEqual(EDGE["counts"]["non_doi_nodes"],2)
        self.assertEqual(RES["summary"]["non_doi_nodes_required"],2)

    def test_14_int03_int06_not_direct(self):
        rs=[r for r in EDGE["receipts"] if r["descendant"]=="INT-06" and r["ancestor"]=="doi:10.1073/pnas.95.24.14529"]
        self.assertEqual(len(rs),1); self.assertEqual(rs[0]["edge_type"],"SHARED_FRAMEWORK"); self.assertFalse(rs[0]["direct_ancestry_candidate"])

    def test_15_w7_matrix_not_rewritten(self):
        self.assertFalse(W9["isolation"]["modifies_w7_original_native_profiles"])
        self.assertFalse(W9["isolation"]["modifies_w7_pair_triage_matrix"])
        self.assertFalse(W9["isolation"]["rewrites_1580_pair_results"])

    def test_16_no_global_independence_true(self):
        self.assertFalse(RES["summary"]["global_independent_count_promoted"])
        self.assertEqual(W9["isolation"]["global_independence_fields_promoted"],0)
        self.assertTrue(all(r["global_independence_evidence"] is False for r in EDGE["receipts"]))

    def test_17_main_authorization_false(self):
        self.assertFalse(SCHEMA["w9_isolation_contract"]["main_scientific_authorization"])
        self.assertFalse(RES["summary"]["main_scientific_authorization"])
        self.assertFalse(EDGE["main_scientific_authorization"])
        self.assertFalse(W9["isolation"]["main_scientific_authorization"])

    def test_18_no_source_blocked_claimed_resolved(self):
        self.assertEqual(W9["isolation"]["source_blocked_profiles_resolved_here"],0)

    def test_19_no_g1_190_pair_audit(self):
        self.assertFalse(W9["isolation"]["g1_190_pair_audit_performed"])

    def test_20_w9_is_proposal_only(self):
        self.assertEqual(W9["import_status"],"PROPOSED_ONLY_REQUIRES_W9_INDEPENDENT_VALIDATION")

if __name__=="__main__":
    unittest.main()
