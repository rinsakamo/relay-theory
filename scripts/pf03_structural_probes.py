#!/usr/bin/env python3
"""PF03 independent synthetic structural/provenance probes. NOT original numeric replication
and NOT the #401 exact v2.3.1 historical scientific validator.
All generated numbers and micro-models are illustrative, not source-simulation outputs.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
P = ROOT / "research/paper2/p399/pf03"
def get(name):
    return json.loads((P / name).read_text(encoding="utf-8"))
def digest(name):
    return hashlib.sha256((P / name).read_bytes()).hexdigest()
def relu(v):
    return [max(0., x) for x in v]
def matvec(A, x):
    return [sum(a*b for a,b in zip(row,x)) for row in A]
def combine(mats, w):
    return [[sum(w[k]*mats[k][i][j] for k in range(len(w)))
             for j in range(len(mats[0][0]))] for i in range(len(mats[0]))]
def two_level_pred(previous, higher_modulation, bases):
    return relu(matvec(combine(bases, higher_modulation), previous))
def l3(image_e, lower_e, upper_e, mask, var_image=1., var_low=1., var_up=1., sparsity=0.):
    assert mask in (0,1)
    return (image_e**2 / (2*var_image)
            + lower_e**2 / (2*var_low)
            + mask*upper_e**2 / (2*var_up)
            + sparsity)
def model_early_late(initial=1., observation=-1., rate=.2, steps=9):
    x=initial
    vals=[]
    for _ in range(steps):
        x-=rate*(x-observation)
        vals.append(x)
    return vals
def masked_memory_read(content_cue, G_lower, G_upper, mask_higher=False, higher_cue=0.):
    # Scalar source-inspired least-square memory read; not authors' learned neural net.
    m=(G_lower*content_cue + (G_upper*higher_cue if mask_higher else 0.)) / (
        G_lower*G_lower + (G_upper*G_upper if mask_higher else 0.))
    return m,G_upper*m
class PF03FrozenStructuralProbes(unittest.TestCase):
    def test_01_original_primary_and_freezes(self):
        p,a,b,c,delta,d=map(get,["PRE_A.json","A.json","B.json","C.json","C_DELTA.json","D.json"])
        source="62d744125034ce834692cdb210065d34e2bbd0f58c9eb3387ed2d75dfb7f77ae"
        self.assertEqual(p["frozen_primary"]["sha256"],source)
        self.assertTrue(all(g["decision"]=="PASS" for g in p["gates"]))
        for v in (a["frozen_authority"]["primary"]["sha256"],
                  b["primary_source"]["sha256"],c["primary_source"]["sha256"],
                  delta["source_pdf_sha256"],d["frozen_inputs"]["pdf"]):
            self.assertEqual(v,source)
        self.assertEqual(len(a["source_defined_nodes"]),35)
        self.assertEqual(len(a["source_defined_edges"]),23)
        self.assertEqual(len(a["limits"]),12)
        self.assertEqual(len(b["objections"]),4)
        self.assertEqual(len(c["decisions"]),4)
        self.assertEqual(len(c["C2_source_local_conditions_unique"]),18)
        for name,slot in [("PRE_A.json","PRE_A"),("A.json","A"),("B.json","B"),
                          ("C.json","C"),("C_DELTA.json","C_DELTA")]:
            self.assertEqual(d["frozen_inputs"][slot], digest(name))
    def test_02_complete_coverage_and_no_duplicate_c(self):
        a,b,c=map(get,["A.json","B.json","C.json"])
        for original,review in [("source_defined_nodes","all_node_review"),
                                ("source_defined_edges","all_edge_review"),
                                ("limits","all_limits_review"),
                                ("variant_catalog","all_variants_review")]:
            self.assertEqual({z["id"] for z in a[original]},
                             {z["id"] for z in b[review]})
        self.assertEqual({x["id"] for x in b["objections"]},
                         {x["B_id"] for x in c["decisions"]})
        for objection in c["decisions"]:
            self.assertTrue(objection["original_a"]["nodes"])
            self.assertTrue(objection["original_a"]["edges"])
            self.assertTrue(objection["material_adjacent_condition_ids"])
        ids=[x["id"] for x in c["C2_source_local_conditions_unique"]]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertTrue(all(x["disposition"] for x in c["C2_source_local_conditions_unique"]))
        self.assertTrue(c["C1_entire_original_A_reopened"]["actually_fetched_from_git"])
        self.assertTrue(any(s["zero_B"] for s in c["full_original_source_order_independent_c_sweep"]))
    def test_03_no_duplicate_or_source_invented_gate(self):
        delta,d=get("C_DELTA.json"),get("D.json")
        self.assertEqual({x["id"] for x in delta["patches"]},
                         {"C-L13","C-N01","C-E01","C-N02","C-E02"})
        self.assertEqual(next(x for x in delta["patches"] if x["id"]=="C-E01")["supersedes"],"A-E21")
        self.assertIn("A-E21",d["grammar_v0_roles"]["K"]["disabled_historical_edges"])
        self.assertEqual(d["D_uncertainties"][0]["id"],"D-U01")
    def test_04_grammar_v0_original_file_exists_unchanged(self):
        source=(ROOT/"formal/relay_theory/RelayTheory/UnifiedCognitiveStructuralGrammar.lean").read_text()
        for required in ["structure Grammar where","succession :", "transition :", "transitionAdmissible :",
                         "observe :", "observationAdmissible :", "qLe :"]:
            self.assertIn(required,source)
        d=get("D.json")
        self.assertEqual(set(d["grammar_v0_roles"]),
                         {"Pi","X","C","Q","P_in","P_out","K","T","rho_O"})
    def test_05_topdown_weighted_basis_and_destructive_ablation(self):
        # Two distinct pretrained lower transition matrices; upper state is modulator not matrix.
        v1=[[1.,0.],[0.,0.]]
        v2=[[0.,0.],[0.,1.]]
        bases=[v1,v2]
        before=[1.,1.]
        top_a=two_level_pred(before,[1.,0.],bases)
        top_b=two_level_pred(before,[0.,1.],bases)
        self.assertNotEqual(top_a,top_b)
        ablated_a=two_level_pred(before,[.5,.5],bases)
        ablated_b=two_level_pred(before,[.5,.5],bases)
        self.assertEqual(ablated_a,ablated_b)
        self.assertEqual(top_a,[1.,0.])
    def test_06_inference_versus_parameter_learning(self):
        original_params=[1.,.5]
        inference_state=0.
        observed=2.
        for _ in range(8):
            inference_state+=.1*(observed-original_params[0]*inference_state)
        self.assertEqual(original_params,[1.,.5])
        new_params=original_params.copy()
        new_params[0]+=.05*(observed-new_params[0]*inference_state)*inference_state
        self.assertNotEqual(new_params,original_params)
    def test_07_event_gated_three_level_objective(self):
        self.assertEqual(l3(2.,2.,3.,0),4.)
        self.assertEqual(l3(2.,2.,3.,1),8.5)
        self.assertNotEqual(l3(2.,2.,3.,0),l3(2.,2.,3.,1))
        # No source-derived specific spatial-only threshold scalar is asserted here.
    def test_08_higher_level_modulation_of_intermediate_dynamics(self):
        upper_bases=[[[1.,0.],[0.,0.]],[[0.,0.],[0.,1.]]]
        intermediate_prev=[1.,1.]
        type_straight=matvec(combine(upper_bases,[1.,0.]),intermediate_prev)
        type_clockwise=matvec(combine(upper_bases,[0.,1.]),intermediate_prev)
        self.assertNotEqual(type_straight,type_clockwise)
        disabled_top=matvec(combine(upper_bases,[.5,.5]),intermediate_prev)
        self.assertEqual(disabled_top,[.5,.5])
        self.assertNotEqual(disabled_top,type_straight)
    def test_09_temporal_hierarchy_and_internal_not_world_recurrence(self):
        # Illustrative stable sequence-global higher mode over changing lower frames.
        h=[1.,0.]
        bases=[[[1.,0.],[0.,0.]],[[0.,0.],[0.,1.]]]
        x=[2.,1.]
        traces=[]
        for _ in range(3):
            x=two_level_pred(x,h,bases)
            traces.append(x)
        self.assertTrue(all(x[0]==2. for x in traces))
        self.assertEqual(h,[1.,0.])
        d=get("D.json")
        self.assertIn("NOT INSTANTIATED_AS_CLOSED_LOOP",
                      d["system_world_experiment"]["derived_system_world_recurrence"])
        self.assertNotEqual(d["system_world_experiment"]["W"],
                            d["system_world_experiment"]["system_boundary"])
    def test_10_predictive_to_postdictive_toy_iterates(self):
        estimates=model_early_late()
        self.assertGreater(estimates[0],0.)
        self.assertLess(estimates[-1],0.)
        self.assertEqual(model_early_late(1.,1.)[-1],1.)
    def test_11_source_defined_optional_memory_mask_vs_disconnect(self):
        m,rh=masked_memory_read(content_cue=1.,G_lower=1.,G_upper=2.,mask_higher=False)
        self.assertAlmostEqual(m,1.)
        self.assertAlmostEqual(rh,2.)
        _,bad=masked_memory_read(content_cue=1.,G_lower=1.,G_upper=2.,mask_higher=True,higher_cue=0.)
        self.assertNotEqual(rh,bad)
        _,disconnected=masked_memory_read(content_cue=1.,G_lower=1.,G_upper=0.,mask_higher=False)
        self.assertEqual(disconnected,0.)
        a=get("A.json")
        self.assertIn("VM",{x["id"] for x in a["variant_catalog"]})
        self.assertIn("A-N25",{x["id"] for x in a["source_defined_nodes"]})
    def test_12_baseline_without_memory_cannot_earn_recall(self):
        a,d=get("A.json"),get("D.json")
        v2=next(v for v in a["variant_catalog"] if v["id"]=="V2")
        vm=next(v for v in a["variant_catalog"] if v["id"]=="VM")
        self.assertNotIn("m",v2["parts"])
        self.assertIn("m",vm["parts"])
        # The A V2 catalog's abbreviated 'G' is a generic generative-graph
        # label, NOT memory synaptic matrix G. Check typed original-A nodes.
        typed_g=next(n for n in a["source_defined_nodes"] if n["id"]=="A-N26")
        self.assertEqual(typed_g["variant"],"VM")
        self.assertIn("G",vm["parts"])
        self.assertTrue(all(x["A2"]=="NOT REQUIRED" or x["A2"].startswith("NOT REQUIRED")
                            for x in d["A0_A1_A2_by_variant"]))
if __name__=="__main__":
    unittest.main(verbosity=2)
