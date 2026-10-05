#!/usr/bin/env python3
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KICKOFF = "3c2761ac13b04203aa7dbd8f47a1d687d506bf7b"
MANIFEST_BLOB = "b97b67a34ad9c2858745dfa6aa60444520eaab13"
GRAMMAR_ROLES = {"Pi","X","C","Q","P_in","P_out","K","T","rho_O"}
ROSTER = {
 "MEM-01":"10.1007/s42113-023-00189-y",
 "MEM-02":"10.1371/journal.pcbi.1008367",
 "MEM-03":"10.1371/journal.pcbi.1004003",
 "PRD-01":"10.1038/s41562-024-01930-8",
 "PRD-02":"10.1371/journal.pcbi.1001003",
 "PRD-03":"10.1371/journal.pcbi.1007093",
 "SKL-01":"10.1371/journal.pcbi.1012455",
 "SKL-02":"10.1371/journal.pcbi.1005632",
 "SKL-03":"10.1371/journal.pcbi.1006839",
}
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def git(*args):
    return subprocess.run(["git",*args],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
def addition_commit(path):
    r=git("log","--diff-filter=A","--format=%H","--",str(ROOT/path))
    lines=[x for x in r.stdout.splitlines() if x.strip()]
    return lines[-1] if lines else None

class M3FailClosed(unittest.TestCase):
    def setUp(self):
        self.intake=load("M3_NINE_PAPER_INTAKE_RECEIPT_v1.json")
        self.reg=load("M3_NINE_PAPER_OUTCOME_REGISTRY_v1.json")
        self.boundary=load("M3_MEM_PRD_SKL_BOUNDARY_AUDIT_v1.json")
        self.neg=load("M3_NEGATIVE_AND_UNDERDETERMINED_REGISTER_v1.json")

    def test_01_exact_9_assignment(self):
        self.assertEqual({x["slot"] for x in self.intake["assignment"]},set(ROSTER))
    def test_02_exact_doi_identity(self):
        self.assertEqual({x["slot"]:x["doi"] for x in self.intake["assignment"]},ROSTER)
        for s,d in ROSTER.items(): self.assertEqual(load(f"{s}/SOURCE_AUTHORITY_LOCK_v1.json")["doi"],d)
    def test_03_no_foreign_main_paper(self):
        paper_dirs={p.name for p in ROOT.iterdir() if p.is_dir()}
        self.assertEqual(paper_dirs,set(ROSTER))
    def test_04_exact_kickoff_head_ancestry(self):
        self.assertEqual(self.intake["kickoff"]["exact_head"],KICKOFF)
        self.assertEqual(git("merge-base","--is-ancestor",KICKOFF,"HEAD").returncode,0)
    def test_05_exact_manifest_blob(self):
        self.assertEqual(self.intake["main_denominator"]["manifest_git_blob"],MANIFEST_BLOB)
        r=git("rev-parse",f"{KICKOFF}:research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json")
        self.assertEqual(r.returncode,0); self.assertEqual(r.stdout.strip(),MANIFEST_BLOB)
    def test_06_no_duplicate_paper(self):
        vals=[x["doi"] for x in self.intake["assignment"]]; self.assertEqual(len(vals),len(set(vals)))
    def test_07_no_roster_substitution(self):
        self.assertFalse(self.intake["main_denominator"]["roster_substitution"])
    def test_08_no_backup_activation(self):
        self.assertFalse(self.intake["main_denominator"]["backup_activation"])
    def test_09_stage_a_before_b(self):
        for s in ROSTER:
            a=addition_commit(f"{s}/PASS_A_SOURCE_FIRST_DECOMPOSITION_v1.json")
            b=addition_commit(f"{s}/PASS_B_RESULT_INFORMED_REAUDIT_v1.json")
            self.assertTrue(a and b); self.assertEqual(git("merge-base","--is-ancestor",a,b).returncode,0)
    def test_10_b_receives_frozen_a(self):
        for s in ROSTER:
            b=load(f"{s}/PASS_B_RESULT_INFORMED_REAUDIT_v1.json")
            self.assertTrue(b["chronology"]["stage_a_frozen_input"])
            self.assertEqual(b["chronology"]["input_stage_a"],"PASS_A_SOURCE_FIRST_DECOMPOSITION_v1.json")
    def test_11_c_traces_objections_to_source_loci(self):
        for s in ROSTER:
            c=load(f"{s}/PASS_C_SOURCE_CLOSED_ADJUDICATION_v1.json")
            self.assertTrue(c["c1_original_a_gap_test"])
            self.assertTrue(all(x.get("source_locus") for x in c["c1_original_a_gap_test"]))
    def test_12_negative_evidence_cannot_disappear(self):
        for s in ROSTER:
            a=set(load(f"{s}/PASS_A_SOURCE_FIRST_DECOMPOSITION_v1.json")["negative_adverse_results"])
            n=set(load(f"{s}/LIMITATIONS_AND_NEGATIVE_EVIDENCE_v1.json")["negative_evidence"])
            self.assertTrue(a.issubset(n))
    def test_13_grammar_roles_cannot_change(self):
        for s in ROSTER:
            g=load(f"{s}/GRAMMAR_V0_RECONSTRUCTION_v1.json")
            self.assertFalse(g["frozen_grammar_authority"]["roles_modified"])
            self.assertEqual(set(g["mapping"]),GRAMMAR_ROLES)
    def test_14_external_history_not_auto_memory(self):
        self.assertTrue(self.boundary["fail_closed_guards"]["external_history_cannot_auto_become_memory_state"])
    def test_15_fitted_latent_not_auto_stored_memory(self):
        self.assertTrue(self.boundary["fail_closed_guards"]["fitted_latent_cannot_auto_become_stored_memory"])
    def test_16_prediction_error_not_auto_coordinator(self):
        self.assertTrue(self.boundary["fail_closed_guards"]["prediction_error_cannot_auto_become_coordinator_state"])
    def test_17_learned_parameter_not_auto_active_controller(self):
        self.assertTrue(self.boundary["fail_closed_guards"]["learned_parameter_cannot_auto_become_active_controller"])
    def test_18_motor_target_not_auto_internal_skill(self):
        self.assertTrue(self.boundary["fail_closed_guards"]["motor_target_cannot_auto_become_internal_skill_state"])
    def test_19_offline_replay_not_auto_online_coordination(self):
        self.assertTrue(self.boundary["fail_closed_guards"]["offline_replay_cannot_auto_become_online_coordination"])
    def test_20_a2_requires_a0_and_a1_failure(self):
        for s in ROSTER:
            o=load(f"{s}/ARCHITECTURAL_OUTCOME_v1.json")
            if o["attempts"]["A2"]["attempted"]:
                self.assertEqual(o["attempts"]["A0"]["result"],"FAIL")
                self.assertEqual(o["attempts"]["A1"]["result"],"FAIL")
    def test_21_fit_failure_alone_cannot_imply_a2(self):
        self.assertTrue(self.boundary["fail_closed_guards"]["fit_failure_alone_cannot_imply_A2"])
    def test_22_source_state_not_double_counted(self):
        self.assertTrue(self.boundary["fail_closed_guards"]["source_defined_state_cannot_be_double_counted_as_new_coordinator"])
        for s in ROSTER:
            guard=load(f"{s}/ARCHITECTURAL_OUTCOME_v1.json")["double_count_guard"]
            self.assertIn("re-counted",guard)
            self.assertTrue(guard.startswith("No "))
    def test_23_prd01_bundle_and_exclusions_preserved(self):
        p=load("PRD-01/SOURCE_AUTHORITY_LOCK_v1.json")["source"]
        comps={x["role"]:x for x in p["components"]}
        self.assertEqual(comps["official_publisher_supplement"]["sha256"],"10f5d55f971060fb325e3e5a0bb4be2df015407ecb1428af9ebd17a4bea6298c")
        self.assertTrue(any("Fig S2" in x for x in p["permanent_exclusions"]))
        self.assertIn("NOT relabeled",p["edition"])
    def test_24_skl01_convergence_conditions_preserved(self):
        n=" ".join(load("SKL-01/PASS_A_SOURCE_FIRST_DECOMPOSITION_v1.json")["negative_adverse_results"])
        for token in ["gamma^2","Omega_c","O(|sigma_u|)","persistently exciting","no inverse exploration noise"]: self.assertIn(token,n)
    def test_25_underdetermined_preserved(self):
        self.assertTrue(self.neg["policies"]["preserve_underdetermined"])
    def test_26_source_ineligible_no_replacement(self):
        self.assertTrue(self.neg["policies"]["source_ineligible_cannot_trigger_replacement"])
    def test_27_genealogy_cannot_alter_roster(self):
        self.assertTrue(self.neg["policies"]["genealogy_cannot_alter_roster"])
    def test_28_no_genealogy_independence_promotion(self):
        self.assertFalse(self.intake["genealogy"]["global_genealogical_independence_claimed"])
        for s in ROSTER: self.assertFalse(load(f"{s}/SOURCE_AUTHORITY_LOCK_v1.json")["genealogy"]["global_independence_certified"])
    def test_29_g1_pilot20_excluded(self):
        self.assertFalse(self.intake["main_denominator"]["g1_pilot20_is_main_evidence"])
    def test_30_final_outcome_count_9(self):
        self.assertEqual(self.reg["denominator"],9); self.assertEqual(len(self.reg["rows"]),9)
    def test_31_m3_no_overall_h_verdict(self):
        self.assertTrue(self.reg["no_overall_h0_h1_h2_conclusion"])
        for s in ROSTER: self.assertEqual(load(f"{s}/ARCHITECTURAL_OUTCOME_v1.json")["overall_h0_h1_h2_verdict"],"NOT_ISSUED_BY_M3")

if __name__ == "__main__":
    unittest.main(verbosity=2)
