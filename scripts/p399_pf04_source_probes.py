#!/usr/bin/env python3
"""PF04 illustrative/source-structure probes only; NOT original 2013 numerical replication
and NOT the byte-locked v2.3.1 scientific structural validator.
All formula examples are intentionally researcher-declared, not re-fitted participant traces.
"""
import json
import math
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1] / "research/paper2/p399/pf04"

def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

def omega(index, w):
    return w if index < 2 else 1 - w

def scores(values, *, w, beta=1.0, kappas=None):
    assert len(values) == 6
    if kappas is None: kappas = [0.0] * 6
    return [math.exp(beta*omega(i,w)*v + kappas[i]) for i,v in enumerate(values)]

def normalized_s0(values, w, beta=1.0, kappas=None):
    exps=scores(values,w=w,beta=beta,kappas=kappas)
    denom=sum(exps)
    return [v/denom for v in exps]

def as_printed_eq10(values, w, beta=1.0, kappas=None):
    if kappas is None: kappas = [0.0] * 6
    numerator=scores(values,w=w,beta=beta,kappas=kappas)
    # Prints omega(a) even as a' is varied in the denominator.
    return [num / sum(math.exp(beta*omega(i,w)*v + k)
                      for v,k in zip(values,kappas))
            for i,num in enumerate(numerator)]

def second_stage_conditional(first_options, fresh_second_a2_probability):
    # first_options = P(A1 single), P(A1A1), P(A1A2) conditional on observed first A1;
    # the original's concept-level eq11-13 establishes this latent option mixture.
    one,seq_a1,seq_a2=first_options
    assert abs(sum(first_options)-1)<1e-12
    assert 0<=fresh_second_a2_probability<=1
    return seq_a2 + one*fresh_second_a2_probability

def fitted_source_stage2_disabled(first_options, fresh_second_a2_probability):
    # Implements illustrative qualitative effect of SOURCE eq15:
    # no first-stage sequence influence on stage-two choice;
    # original fitting code and likelihoods are NOT represented.
    return fresh_second_a2_probability

def source_option_next(active_option, observed_expected_trigger, gd_override=False):
    # Source-defined option progress; NOT a newly invented coordinator.
    if gd_override: return None
    if active_option is None or not observed_expected_trigger: return None
    return active_option[1]

def terminal_transition_update(old_p, eta, observed_reward, terminal_observed):
    if not terminal_observed: return old_p
    return (1-eta)*old_p + eta*(1.0 if observed_reward else 0.0)

class PF04SourceProbes(unittest.TestCase):
    def test_paper_and_frozen_procedure(self):
        P=load("PRE_A_v3_author_scoped_normalization.json")
        A=load("PASS_A_original.json")
        B=load("PASS_B_reaudit.json")
        C=load("PASS_C_adjudication.json")
        D=load("PASS_D_grammar_v0.json")
        src=P["source"]["sha256"]
        self.assertTrue(all(x==src for x in [
            A["frozen_source"]["sha256"],
            B["input"]["original_pdf_sha256"],
            C["input"]["sha256"],
            D["original_pdf_sha256"]]))
        self.assertEqual(len(A["nodes"]),30)
        self.assertEqual(len(A["edges"]),30)
        self.assertEqual(len(B["item_coverage"]),60)
        self.assertEqual(len(B["objections"]),8)
        self.assertEqual(len(C["adjudications"]),8)
        self.assertEqual(len(C["append_only_delta"]),7)
        self.assertEqual(len(C["material_source_local_conditions"]),23)
        self.assertEqual(len(C["additional_original_order_full_sweep"]),len(A["sections"]))
        self.assertEqual({r["role"] for r in D["role_mapping"]},
            {"Pi","X","C","Q","P_in","P_out","K","T","rho/O"})
        self.assertFalse(D["additive_grammar_primitives"])
        self.assertEqual({e["id"] for e in D["source_exceptions"]},{"EX1","EX2"})

    def test_full_and_reduced_original_variant_inventory(self):
        A=load("PASS_A_original.json")
        H=A["compared_variants"]["hierarchy"]
        F=A["compared_variants"]["flat"]
        self.assertEqual((len(H),len(F)),(8,8))
        self.assertEqual(len(H[-1]["free"]),6)
        self.assertEqual(len(F[-1]["free"]),7)
        self.assertEqual([x["original_table1_row"] for x in H], list(range(1,9)))
        self.assertEqual([x["original_table1_row"] for x in F], list(range(9,17)))

    def test_author_normalization_original_nonprobability_witness(self):
        vals=[1,0,0,0,0,0]
        raw=as_printed_eq10(vals,.25)
        fixed=normalized_s0(vals,.25)
        self.assertAlmostEqual(sum(raw), .9254999009562278, places=12)
        self.assertAlmostEqual(sum(fixed), 1.0, places=14)
        self.assertGreater(abs(sum(raw)-1), .07)
        self.assertTrue(all(0<p<1 for p in fixed))

    def test_corrected_policy_normalizes_across_parameter_ranges(self):
        for w in (.1,.25,.46,.5,.9):
            for beta in (.1,1.,5.8):
                p=normalized_s0([.1,.6,-.2,.4,.8,.05],w,beta,[0,.3,-.1,.2,0,-.2])
                self.assertAlmostEqual(sum(p),1,places=12)

    def test_flat_second_step_remains_fresh_conditional_on_same_current_state(self):
        # Fixed current World second-state and learned flat values: no active option dependency.
        fresh_second_a2=.3
        self.assertEqual(fitted_source_stage2_disabled([.1,.2,.7],fresh_second_a2),.3)
        self.assertEqual(fitted_source_stage2_disabled([.1,.7,.2],fresh_second_a2),.3)

    def test_hierarchy_preserves_initiated_sequence_dependency(self):
        p=second_stage_conditional([.1,.2,.7],.3)
        self.assertAlmostEqual(p,.73)
        self.assertGreater(p,fitted_source_stage2_disabled([.1,.2,.7],.3))

    def test_break_sequence_level_dependency_destructive_illustration(self):
        original=second_stage_conditional([.1,.2,.7],.3)
        scrambled=second_stage_conditional([.1,.7,.2],.3)
        self.assertAlmostEqual(original,.73)
        self.assertAlmostEqual(scrambled,.23)
        self.assertAlmostEqual(original-scrambled,.5)
        # Invented computational perturbation, not an actual published experiment.

    def test_sequence_disabled_original_comparator_eq15(self):
        seq=[.1,.2,.7]
        self.assertAlmostEqual(second_stage_conditional(seq,.3),.73)
        self.assertAlmostEqual(fitted_source_stage2_disabled(seq,.3),.3)
        self.assertEqual(seq,[.1,.2,.7])  # comparator does not destroy S0 option family

    def test_open_loop_is_distinct_from_world_feedback_and_trigger(self):
        active=("A1","A2")
        for second_state in ("S1","S2"):
            self.assertEqual(source_option_next(active,True),"A2")
        self.assertIsNone(source_option_next(active,False))  # no go stimulus
        self.assertIsNone(source_option_next(active,True,gd_override=True))
        # Inhibition is source-discussion possibility, NOT fitted hazard replication.

    def test_terminal_learning_depends_on_observed_outcome(self):
        self.assertAlmostEqual(terminal_transition_update(.2,.25,True,False),.2)
        self.assertAlmostEqual(terminal_transition_update(.2,.25,True,True),.4)
        self.assertAlmostEqual(terminal_transition_update(.2,.25,False,True),.15)

    def test_rt_proxy_not_full_three_option_posterior(self):
        first_probs={"single_A1":.1, "seq_A1A1":.2, "seq_A1A2":.7}
        rt_pair=first_probs["seq_A1A2"]/(first_probs["single_A1"]+first_probs["seq_A1A2"])
        full=first_probs["seq_A1A2"]/sum(first_probs.values())
        self.assertAlmostEqual(rt_pair,.875)
        self.assertAlmostEqual(full,.7)
        self.assertNotAlmostEqual(rt_pair,full)

    def test_A0_uses_separate_source_defined_mechanisms(self):
        D=load("PASS_D_grammar_v0.json")
        f,h=D["architectures"]
        self.assertEqual(f["family"],"FLAT_SOURCE_FAMILY_8")
        self.assertEqual(h["family"],"HIERARCHICAL_SOURCE_FAMILY_8")
        self.assertIn("eq8",f["original_control"])
        self.assertIn("source-defined",h["original_control"])
        self.assertIn("NOT_REQUIRED",f["coordination"]["A2"])
        self.assertIn("NOT_REQUIRED",h["coordination"]["A2"])
        self.assertIn("NOT_NECESSARY",f["coordination"]["A1"])
        self.assertIn("NOT_NECESSARY",h["coordination"]["A1"])

if __name__=="__main__":
    unittest.main(verbosity=2)
