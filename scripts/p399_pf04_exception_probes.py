"""PF04 post-E EX2 author-corroboration algebra probes.

Explicitly independent, researcher-authored algebra examples: NOT original 2013
MATLAB/IPOPT or fitted-likelihood replication; author 2015 thesis is secondary.
Run as python scripts/p399_pf04_exception_probes.py on GitHub Actions.
"""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1] / "research/paper2/p399/pf04"

def load(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))

def author_corrob_second_stage(q_single, q_seq_first, q_seq_second, p_fresh_first):
    """Correct intended Eq13 using original Eq11/12: first a' fixed, second a varies."""
    assert all(x >= 0 for x in (q_single,q_seq_first,q_seq_second))
    assert abs(sum((q_single,q_seq_first,q_seq_second))-1.) < 1e-12
    assert 0 <= p_fresh_first <= 1.
    return (q_single*p_fresh_first+q_seq_first,
            q_single*(1.-p_fresh_first)+q_seq_second)

def naive_literal_extension(q_single,q_seq_first,q_seq_second,p_fresh_first):
    """Illustrates a literal reading's breakdown: second candidate a != observed a'.

    Under original Eq12, first-step single action different from observed a'
    cannot explain that observation. Treat that incompatible origin as 0 to
    demonstrate the mass deficit; NOT asserted as authors' original algorithm.
    """
    return (q_single*p_fresh_first+q_seq_first,q_seq_second)

class Author2015SecondaryCorroboration(unittest.TestCase):
    def test_2015_source_is_distinct_secondary(self):
        r=load("EXCEPTIONS_EX1_EX2_SOURCE_RECHECK_v1.json")
        self.assertIn("March 2015",r["independent_followup_source"]["work"])
        self.assertIn("DIFFERENT 2015",r["independent_followup_source"]["authority_status"])
        self.assertEqual(r["authority"]["original_publisher_pdf_sha256"],
                         "bc84d4827df202cf5051cf10aa64cc09673b718af2acd31441a3712bcd376df9")
        self.assertIn("EX2_ANALYTIC_STRUCTURE_RESOLVED",r["EX2"]["scope_decision"])
        self.assertTrue(r["EX1"]["state"].startswith("UNDERDETERMINED"))
        self.assertEqual(r["current_scientific_boundary"]["official_qualified_pilot_count_increment"],0)
        self.assertFalse(r["current_scientific_boundary"]["main_authorized"])

    def test_exact_nonnormalized_literal_example(self):
        corrected=author_corrob_second_stage(.2,.3,.5,.4)
        printed_extension=naive_literal_extension(.2,.3,.5,.4)
        self.assertAlmostEqual(corrected[0],.38)
        self.assertAlmostEqual(corrected[1],.62)
        self.assertAlmostEqual(sum(corrected),1.)
        self.assertAlmostEqual(sum(printed_extension),.88)
        # This proves the printed first coefficient cannot be directly used as
        # a different second-stage candidate's single-action first-stage origin.

    def test_conditional_total_probability_grid(self):
        for qsingle in (0.,.05,.2,.7,1.):
            for qfirst_frac in (0.,.25,.75,1.):
                qfirst=(1.-qsingle)*qfirst_frac
                qsecond=1.-qsingle-qfirst
                for fresh in (0.,.15,.4,.89,1.):
                    p1,p2=author_corrob_second_stage(qsingle,qfirst,qsecond,fresh)
                    self.assertAlmostEqual(p1+p2,1.,places=12)
                    self.assertTrue(-1e-12 <= p1 <=1+1e-12)
                    self.assertTrue(-1e-12 <= p2 <=1+1e-12)

    def test_singleton_only_is_fresh_choice(self):
        self.assertEqual(author_corrob_second_stage(1.,0.,0.,.4),(.4,.6))

    def test_sequence_only_is_precommitted_choice(self):
        self.assertEqual(author_corrob_second_stage(0.,.3,.7,.4),(.3,.7))
        self.assertEqual(author_corrob_second_stage(0.,.3,.7,.8),(.3,.7))

    def test_selected_option_dependency_survives(self):
        pA=author_corrob_second_stage(.2,.3,.5,.4)
        pB=author_corrob_second_stage(.2,.5,.3,.4)
        self.assertAlmostEqual(pA[0],.38)
        self.assertAlmostEqual(pB[0],.58)
        self.assertNotEqual(pA,pB)

    def test_no_import_of_2015_rat_only_interruption_parameter(self):
        A=load("PASS_A_original.json")
        E=load("PASS_E_fidelity.json")
        self.assertEqual(A["compared_variants"]["total_displayed"],16)
        self.assertEqual(len(A["compared_variants"]["hierarchy"]),8)
        self.assertEqual(len(A["compared_variants"]["flat"]),8)
        for model in A["compared_variants"]["hierarchy"]:
            self.assertNotIn("I",model["free"])
        self.assertEqual(E["formal_pilot_status"][:32],
                         "NOT_FULLY_SCIENTIFICALLY_QUALIFI")

    def test_original_implementation_not_certified(self):
        r=load("EXCEPTIONS_EX1_EX2_SOURCE_RECHECK_v1.json")
        self.assertIn("NOT_VERIFIED",r["EX2"]["scope_decision"].replace("UNVERIFIED","NOT_VERIFIED"))
        self.assertTrue(r["EX1"]["state"].startswith("UNDERDETERMINED"))
        self.assertNotIn("AUTHENTICATED",r["EX1"]["state"])
        self.assertEqual(r["current_scientific_boundary"]["new_grammar_primitives"],0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
