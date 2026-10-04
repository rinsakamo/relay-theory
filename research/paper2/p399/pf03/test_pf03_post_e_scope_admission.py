#!/usr/bin/env python3
"""PF03 post-E qualification *record* invariants; original-source semantics
are separately reviewed and bounded in the real-PDF anchor workflow.
NOT original #401 full structural checker and NOT source semantics proof.
"""
from __future__ import annotations
import copy
import hashlib
import json
import subprocess
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
STAGES={
 "PRE_A":("PRE_A.json","1c499d46dd545ed2508a8bebb73f0617e620b1846e475719948200eeca70f91e","9298f5c6e9a528c8f44daf5530d40aa4b3c0df47"),
 "A":("A.json","ef1ce05d8b05d6d9d489b052ec2a5941d8a569975560c12a6b4c9d00e0b1e633","dd5dce774780a9a6df854b14fb2943e324734ad0"),
 "B":("B.json","8a1b21c7825ca4617af9b17e28ddd11bc71726d6780097ddd4750ad5f648111b","3784da529f317e28798038f8a41ba8e98805ab61"),
 "C":("C.json","4507bce2b8fc240f5598ffb9c451b09da867a0d3053d3fdc6041e370b6fe9c69","72834ee3e0d7c3a03439b09dfd73b8ebafe4b419"),
 "C_DELTA":("C_DELTA.json","b434715e3b318e70181ca69d8c2633971dc6c2096e7ecdf75d39e3429344c2fa","216336fc0d811fc294cf27abee913fd3d1c15b2e"),
 "D":("D.json","17992b06e6ce2897d4af8ac093028061ec9eefe402e126d59d0603c020586bb7","242fc5f286d062a523e2246ea4377f0bf6c94605"),
 "E":("E.json","49d0d0dfcfb9f02397ae4b9a2d59fc1a1846f132809b3630a140ca2b736b85b2","ad3a05d2ae94401caf2a3081fc5a297073f8795e"),
 "FINAL":("FINAL.json","29fb0ade9c4c89e02f4a1b3f42c7ec22b4ef1670086dbc8fb264294fd1163bdf","a9666a9708337d2b27ec8f70aa19e3312441c565")
}
ORIGINAL="62d744125034ce834692cdb210065d34e2bbd0f58c9eb3387ed2d75dfb7f77ae"
def load(name):
    return json.loads((HERE/name).read_bytes())
def hash_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def required_scope(v):
    a=v["pre_formal_scientific_disposition"]
    ex=v["primary_original_ambiguities"]
    return (v["source"]["raw_sha256"]==ORIGINAL and
      a["scientific_core_reconstruction"]=="SOURCE_GROUNDED_BOUNDED_A0_FIDELITY" and
      a["original_full_quantitative_behavior"]=="EXCLUDED_NOT_REPRODUCED" and
      a["exact_source_contradiction_in_included_core"] is False and
      a["targeted_exception_human_review_required_for_included_core"] is False and
      a["qualified_pilot_count_delta_from_this_post_e_review"]==0 and
      a["main_status"]=="NOT_AUTHORIZED" and
      len(ex)==3 and ex[0]["retained_status"]=="UNDERDETERMINED_IN_PRIMARY_ONLY" and
      ex[0]["material_to_included_scope"] is False and
      ex[0]["material_to_excluded_exact_numeric_three_level_replay"] is True and
      ex[1]["retained_status"]=="ORIGINAL_NUMERICAL_REPLICATION_NOT_EXECUTED" and
      len(v["bounded_original_post_e_checks"])==8 and
      all(c["decision"].startswith("PASS_") for c in v["bounded_original_post_e_checks"])
    )
class PF03ScopeAdmissionRecords(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review=load("PF03_POST_E_TARGETED_SOURCE_REVIEW_20261004.json")
        cls.C=load("C.json")
        cls.D=load("D.json")
        cls.E=load("E.json")
        cls.secondary=load("SECONDARY_IMPLEMENTATION_RESULT.json")
    def test_01_stage_bytes_pinned_and_never_rewritten(self):
        for label,(p,expected,commit) in STAGES.items():
            with self.subTest(stage=label):
                path=HERE/p
                self.assertEqual(hash_of(path),expected)
                historical=subprocess.check_output(
                  ["git","show",f"{commit}:research/paper2/p399/pf03/{p}"],cwd=ROOT
                )
                self.assertEqual(hashlib.sha256(historical).hexdigest(),expected)
                self.assertEqual(historical,path.read_bytes())
                if label != "FINAL":
                    self.assertEqual(self.review["historic_frozen_stages"][label],expected)
    def test_02_actual_full_chronology_git_ancestors(self):
        seq=[v[2] for v in STAGES.values()]
        for left,right in zip(seq,seq[1:]):
            with self.subTest(before=left[:7],after=right[:7]):
                x=subprocess.run(["git","merge-base","--is-ancestor",left,right],cwd=ROOT,check=False)
                self.assertEqual(x.returncode,0)
    def test_03_frozen_original_source_scope_only(self):
        self.assertTrue(required_scope(self.review))
        self.assertEqual(self.C["primary_source"]["sha256"],ORIGINAL)
        self.assertEqual(self.D["frozen_inputs"]["pdf"],ORIGINAL)
        self.assertEqual(self.review["source"]["size_bytes"],3333319)
    def test_04_result_informed_B_and_source_closed_C1_C2_procedural_receipt(self):
        self.assertTrue(self.C["C1_entire_original_A_reopened"]["actually_fetched_from_git"])
        self.assertEqual(self.C["C1_entire_original_A_reopened"]["nodes_checked"],"A-N01..A-N35 all 35")
        self.assertEqual(len(self.C["decisions"]),4)
        self.assertEqual({x["B_id"] for x in self.C["decisions"]},{"B-O01","B-O02","B-O03","B-O04"})
        self.assertEqual(len(self.C["C2_source_local_conditions_unique"]),18)
        self.assertEqual(len({x["id"] for x in self.C["C2_source_local_conditions_unique"]}),18)
        self.assertTrue(self.C["checks"]["independent_source_order_sweep"])
    def test_05_original_model_variants_and_disabled_unsupported_narrow_edge(self):
        self.assertEqual(len(self.D["A0_A1_A2_by_variant"]),5)
        self.assertEqual(set(self.D["grammar_v0_roles"]),{"Pi","X","C","Q","P_in","P_out","K","T","rho_O"})
        self.assertIn("A-E21",self.D["grammar_v0_roles"]["K"]["disabled_historical_edges"])
        self.assertTrue(all("NOT REQUIRED" in x["A2"] or "NOT_REQUIRED" in x["A2"]
                        for x in self.D["A0_A1_A2_by_variant"]))
    def test_06_original_E_partial_quantitative_not_silently_promoted(self):
        scores={x["id"]:x["source_fidelity"] for x in self.E["evidence"]}
        self.assertEqual(set(scores),{f"E-0{i}" for i in range(1,9)})
        for k in ["E-04","E-05","E-06","E-07"]:
            self.assertEqual(scores[k],"PARTIAL")
        self.assertEqual(self.E["summary"]["exact_original_numeric_replications"],0)
    def test_07_post_E_publisher_reinspection_covers_each_source_specific_exception(self):
        ids=[x["id"] for x in self.review["bounded_original_post_e_checks"]]
        self.assertEqual(ids,[f"RV{i:02}" for i in range(1,9)])
        self.assertTrue(all(x["pages"] and x["actual_source"] and x["stage_trace"] for x in self.review["bounded_original_post_e_checks"]))
        self.assertEqual(self.review["independent_source_byte_ci"]["corrected_result"],"SUCCESS_ALL_15_OF_15")
    def test_08_secondary_author_code_not_backported_to_primary(self):
        self.assertEqual(self.secondary["source_to_code_reconciliation"]["scope_decision"].split(";")[0],
           "AUTHOR_IMPLEMENTATION_EXACT_SCALAR_RESOLVED_FOR_PINNED_CODE")
        self.assertIn("SECONDARY_IMPLEMENTATION_NOT_ORIGINAL_PRIMARY",self.review["secondary_evidence_isolation"]["source_kind"])
        self.assertEqual(self.review["primary_original_ambiguities"][0]["retained_status"],
             "UNDERDETERMINED_IN_PRIMARY_ONLY")
    def test_09_scope_admission_mutations_fail_closed(self):
        for p,new in (
          (("source","raw_sha256"),"0"*64),
          (("pre_formal_scientific_disposition","original_full_quantitative_behavior"),"COMPLETE"),
          (("pre_formal_scientific_disposition","qualified_pilot_count_delta_from_this_post_e_review"),1),
          (("pre_formal_scientific_disposition","main_status"),"AUTHORIZED"),
          (("pre_formal_scientific_disposition","exact_source_contradiction_in_included_core"),True)
        ):
          with self.subTest(changed=p):
            fake=copy.deepcopy(self.review)
            fake[p[0]][p[1]]=new
            self.assertFalse(required_scope(fake))
if __name__=="__main__":
    unittest.main(verbosity=2)
