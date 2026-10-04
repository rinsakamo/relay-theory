#!/usr/bin/env python3
"""Synthetic and exposed-development protocol regression tests; no MAIN science."""
import copy
import json
import sys
import unittest
from pathlib import Path
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P))
from evaluate_g3 import (G3Error, METRICS, check_packet, check_reference,
                         check_source_reference_alignment, destructive_control,
                         score, coordination, verify_receipt_chain, freeze_gate,
                         score_locked, check_role_bridge, coordination_locked,
                         schema_check, canonical_sha)

FIXTURE = json.loads((P / "fixtures/synthetic.v1.json").read_text(encoding="utf-8"))
def fresh():
    return copy.deepcopy(FIXTURE["baseline_evaluation"])
def ref():
    return copy.deepcopy(FIXTURE["reference"])
def packet():
    return copy.deepcopy(FIXTURE["packet"])
def missing(r, metric):
    entry = r["variants"][0]["metrics"][metric]
    item = entry["matched_ids"].pop()
    entry["evidence_witnesses"].pop(item)
    return item
def receipt(stage, prior=None):
    return dict(schema_version="G3_STAGE_RECEIPT_V1", paper_token="SYNTHETIC-ONLY-01",
                stage=stage, protocol_sha256="a"*64, primary_source_id="SYNTHETIC",
                prior_raw_sha256=prior, artifact_raw_sha256=stage.encode().hex().ljust(64,"a"),
                git_commit="SYNTHETIC", actor="FIXTURE_ONLY", runtime="unittest",
                real_execution=False, signed_freeze=True, main_authorized=False,
                independence_claim="NONE")


class G3SyntheticTests(unittest.TestCase):
    def test_baseline_source_conditional_full_no_false_independence(self):
        s=score(fresh())
        self.assertEqual(s["paper"],"FULL")
        self.assertEqual(s["reference_independence"],"SINGLE_REFERENCE_UNVALIDATED")
        self.assertFalse(s["variant_outcomes"]["V_SYNTH"]["semantic_audit_independent"])
        self.assertEqual(s["excluded_count"],1)
        self.assertEqual(s["micro_counts"]["nodes"],{"numerator":2,"denominator":2})

    def test_schemas_and_actual_fixture(self):
        schema_check("evaluation",fresh())
        self.assertTrue(check_reference(ref()))
        self.assertTrue(check_packet(packet()))
        self.assertTrue(check_source_reference_alignment(ref(),fresh()))

    def test_schema_undocumented_additional_field_blocked(self):
        r=fresh();r["undisclosed"]={"role":"unknown"}
        with self.assertRaises(G3Error):score(r)

    def test_source_unknown_failclosed(self):
        r=fresh();r["source_state"]="UNKNOWN"
        self.assertEqual(score(r)["paper"],"INPUT_UNDERSPECIFIED")

    def test_source_ineligible_failclosed(self):
        r=fresh();r["source_state"]="INELIGIBLE"
        self.assertEqual(score(r)["paper"],"INPUT_UNDERSPECIFIED")

    def test_invalid_packet_failclosed(self):
        r=fresh();r["packet_state"]="INVALID"
        self.assertEqual(score(r)["paper"],"INPUT_UNDERSPECIFIED")

    def test_missing_reference_failclosed(self):
        r=fresh();r["reference_state"]="MISSING"
        self.assertEqual(score(r)["paper"],"INPUT_UNDERSPECIFIED")

    def test_conflicting_reference_stays_underdetermined(self):
        r=fresh();r["reference_state"]="CONFLICT_UNRESOLVED"
        self.assertEqual(score(r)["paper"],"UNDERDETERMINED")

    def test_unresolved_source_variant_stays_underdetermined(self):
        r=fresh();r["variants"][0]["unresolved_material"]=["SYNTH_UNRESOLVED_GLYPH"]
        self.assertEqual(score(r)["paper"],"UNDERDETERMINED")

    def test_unresolved_metric(self):
        r=fresh();entry=r["variants"][0]["metrics"]["temporal"]
        entry["unresolved_ids"]=["t1"];entry["matched_ids"]=[]
        self.assertEqual(score(r)["paper"],"UNDERDETERMINED")

    def test_edge_deletion_critical_failure(self):
        r=fresh();missing(r,"edges")
        self.assertEqual(score(r)["paper"],"FAILED")

    def test_edge_deletion_noncritical_partial(self):
        r=fresh();missing(r,"edges")
        r["variants"][0]["metrics"]["edges"]["critical_ids"]=[]
        self.assertEqual(score(r)["paper"],"PARTIAL")

    def test_role_loss_not_syntactic_success(self):
        r=fresh();missing(r,"roles")
        self.assertEqual(score(r)["paper"],"FAILED")

    def test_temporal_inversion(self):
        r=fresh();r["variants"][0]["contradictions"]=["t1_reversed"]
        self.assertEqual(score(r)["paper"],"FAILED")

    def test_wrong_world_boundary(self):
        r=fresh();missing(r,"boundary")
        self.assertEqual(score(r)["paper"],"FAILED")

    def test_negative_finding_suppression(self):
        r=fresh();missing(r,"restrictions")
        self.assertEqual(score(r)["paper"],"FAILED")

    def test_mechanistic_distinction_loss(self):
        r=fresh();missing(r,"distinctions")
        self.assertEqual(score(r)["paper"],"FAILED")

    def test_unnecessary_assumption_prevents_full(self):
        r=fresh();r["assumptions"]=[dict(id="h",level="A1",source_grounded=False,necessity_test="UNTESTED")]
        self.assertEqual(score(r)["paper"],"PARTIAL")

    def test_excluded_quantitative_cannot_be_promoted(self):
        r=fresh();m=r["variants"][0]["metrics"]["nodes"]
        m["required_ids"].append("q_exact");m["matched_ids"].append("q_exact")
        m["evidence_witnesses"]["q_exact"]="claim made from no actual math"
        with self.assertRaisesRegex(G3Error,"EXCLUDED_QUANTITATIVE"):
            score(r)

    def test_reference_denominator_check_catches_self_reporting(self):
        r=fresh();e=r["variants"][0]["metrics"]["edges"]
        e["matched_ids"].clear();e["required_ids"].clear();e["critical_ids"].clear()
        self.assertEqual(score(r)["paper"],"FULL")  # Self-report alone is NOT source truth.
        with self.assertRaisesRegex(G3Error,"SOURCE_NATIVE_DENOMINATOR"):
            check_source_reference_alignment(ref(),r)

    def test_reference_variant_omission_blocked(self):
        r=fresh();r["declared_variant_ids"].append("V_OMITTED")
        with self.assertRaisesRegex(G3Error,"MISSING_DUPLICATE"):
            score(r)

    def test_reference_variant_merger_vs_separate_source(self):
        native=ref();v=copy.deepcopy(native["variants"][0]);v["variant_id"]="V_DISTINCT"
        native["variants"].append(v)
        with self.assertRaisesRegex(G3Error,"SOURCE_VARIANTS"):
            check_source_reference_alignment(native,fresh())

    def test_source_native_reference_dangling_dependency(self):
        native=ref();native["variants"][0]["edges"][0]["to"]="nonexistent"
        with self.assertRaisesRegex(G3Error,"DANGLING"):
            check_reference(native)

    def test_excluded_target_erasure_from_reference(self):
        r=fresh();r["excluded_quantitative_targets"]=[]
        with self.assertRaisesRegex(G3Error,"EXCLUDED_SOURCE_TARGET"):
            check_source_reference_alignment(ref(),r)

    def test_reference_role_contamination_schema(self):
        native=ref();native["variants"][0]["nodes"][0]["grammar_role"]="X"
        with self.assertRaises(G3Error):check_reference(native)

    def test_packet_no_grammar_output_leakage(self):
        pkt=packet();pkt["reference_object"]=ref()
        with self.assertRaises(G3Error):check_packet(pkt)

    def test_packet_must_keep_original_negative(self):
        pkt=packet();pkt["scope_integrity"]["negative_outcomes_kept"]=False
        with self.assertRaisesRegex(G3Error,"INCOMPLETE"):
            check_packet(pkt)

    def test_packet_direct_recognition_cannot_claim_fully_masked(self):
        pkt=packet();pkt["masking"]["leakage_flags"]=["FULLY_MASKED","DIRECTLY_RECOGNIZABLE"]
        with self.assertRaisesRegex(G3Error,"CONTRADICTORY"):
            check_packet(pkt)

    def test_prior_recognition_cannot_claim_fully_blind(self):
        pkt=packet();pkt["masking"]["leakage_flags"]=["FULLY_MASKED"]
        pkt["masking"]["recognition_pre_D"]="YES"
        with self.assertRaisesRegex(G3Error,"KNOWN_RECOGNITION"):
            check_packet(pkt)

    def test_h0_is_source_only_not_general_proof(self):
        r=fresh();r["coordination"]["discrimination"]="H0_SOURCE_CONDITIONAL"
        self.assertEqual(coordination(r),"H0_SOURCE_CONDITIONAL")

    def test_h1_without_necessity_rejected(self):
        r=fresh();h=r["coordination"];h.update(a0="FAILED",a1="SUPPORTED",discrimination="H1_SOURCE_CONDITIONAL")
        r["assumptions"]=[dict(id="a1",level="A1",source_grounded=True,necessity_test="UNTESTED")]
        self.assertEqual(coordination(r),"UNSUPPORTED_COORDINATION_INFERENCE")

    def test_h1_with_exhaustive_source_conditional_countercheck(self):
        r=fresh();h=r["coordination"];h.update(a0="FAILED",a1="SUPPORTED",discrimination="H1_SOURCE_CONDITIONAL")
        r["assumptions"]=[dict(id="a1",level="A1",source_grounded=True,necessity_test="PASS")]
        self.assertEqual(coordination(r),"H1_SOURCE_CONDITIONAL")

    def test_h2_unjustified_source_defined_state_not_exhausted(self):
        r=fresh();h=r["coordination"]
        h.update(a0="FAILED",a1="FAILED",a2="SUPPORTED",discrimination="H2_SOURCE_CONDITIONAL",
                 source_defined_functions_exhausted=False,additional_state_source_grounded=True)
        r["assumptions"]=[dict(id="a2",level="A2",source_grounded=True,necessity_test="PASS")]
        self.assertEqual(coordination(r),"UNSUPPORTED_COORDINATION_INFERENCE")

    def test_h2_possible_only_with_all_strict_flags(self):
        r=fresh();h=r["coordination"]
        h.update(a0="FAILED",a1="FAILED",a2="SUPPORTED",discrimination="H2_SOURCE_CONDITIONAL",
                 source_defined_functions_exhausted=True,additional_state_source_grounded=True)
        r["assumptions"]=[dict(id="a2",level="A2",source_grounded=True,necessity_test="PASS")]
        self.assertEqual(coordination(r),"H2_SOURCE_CONDITIONAL")
        # Structural feasibility in a fake fixture is NOT actual scientific H2 evidence.

    def test_a2_failure_alone_never_h2(self):
        r=fresh();h=r["coordination"];h.update(a0="FAILED",a1="FAILED",a2="FAILED",
                                                discrimination="H2_SOURCE_CONDITIONAL")
        self.assertEqual(coordination(r),"UNSUPPORTED_COORDINATION_INFERENCE")

    def test_destructive_controls_seven_source_semantic_losses(self):
        for kind,metric in [("REMOVE_EDGE","edges"),("REVERSE_TEMPORAL","temporal"),
                            ("SWAP_BOUNDARY","boundary"),("REMOVE_NATIVE_COORDINATOR","edges"),
                            ("MERGE_VARIANTS","distinctions"),("STATEFUL_TO_STATELESS","temporal"),
                            ("REMOVE_NEGATIVE","restrictions"),("G_DYN","boundary")]:
            with self.subTest(kind=kind):
                changed=fresh();missing(changed,metric)
                self.assertEqual(destructive_control(fresh(),changed,kind,True,True),"INFORMATIVE")

    def test_undetected_mutation_is_false_positive_not_automatic_success(self):
        self.assertEqual(destructive_control(fresh(),fresh(),"REMOVE_EDGE",True,True),
                         "FALSE_POSITIVE_RECONSTRUCTION")

    def test_invalid_mutation_does_not_count_as_power(self):
        self.assertEqual(destructive_control(fresh(),fresh(),"REMOVE_EDGE",False,True),"INVALID")

    def test_nondiscriminating_faithfully_reported(self):
        self.assertEqual(destructive_control(fresh(),fresh(),"REMOVE_EDGE",True,False),
                         "NON_DISCRIMINATING")

    def test_destructive_control_with_missing_base_not_informative(self):
        r=fresh();r["source_state"]="UNKNOWN"
        self.assertEqual(destructive_control(r,fresh(),"REMOVE_EDGE",True,True),"INVALID")

    def test_invalid_receipt_chain_prevents_stage_jump(self):
        with self.assertRaisesRegex(G3Error,"MISSING_SOURCE"):
            verify_receipt_chain([receipt("C")])

    def test_receipt_chain_prospective_stage_sequencing(self):
        a=receipt("S0");b=receipt("R0",a["artifact_raw_sha256"]);c=receipt("P0",b["artifact_raw_sha256"])
        self.assertTrue(verify_receipt_chain([a,b,c]))

    def test_receipt_chain_sha_tampering(self):
        a=receipt("S0");b=receipt("R0","f"*64)
        with self.assertRaisesRegex(G3Error,"BROKEN_SHA"):
            verify_receipt_chain([a,b])

    def test_receipt_unmask_requires_anonymous_atlas(self):
        a=receipt("S0");b=receipt("UNMASK",a["artifact_raw_sha256"])
        with self.assertRaisesRegex(G3Error,"PREMATURE_LABEL"):
            verify_receipt_chain([a,b])

    def test_no_main_authorization_from_g3_success_alone(self):
        self.assertEqual(freeze_gate(False,False,True,True,False),"PRE_FREEZE_NO_MAIN")
        self.assertEqual(freeze_gate(True,True,True,True,True),"READY_FOR_JOINT_REVIEW")

    def test_pf_procedural_compatibility_nonpromotion(self):
        cases=json.loads((P/"fixtures/frozen_pf_boundaries.v1.json").read_text(encoding="utf-8"))
        self.assertEqual(len(cases["pilots"]),4)
        self.assertTrue(all(p["scope_only"] and not p["numeric_replay_certified"]
                            and not p["universal_h2_claim"] for p in cases["pilots"]))
        self.assertEqual({p["id"] for p in cases["pilots"]},{"PF01","PF02","PF03","PF04"})
        self.assertTrue(any("omega(a')" in x for x in cases["pilots"][3]["conditions"]))
        self.assertEqual(cases["status"],"EXPOSED_COMPATIBILITY_REGRESSION_ONLY")


    def locked_fixture(self):
        native=ref()
        pkt=packet()
        bridge=json.loads((P/"fixtures/synthetic_role_bridge_template.v1.json").read_text(encoding="utf-8"))["bridge"]
        bridge["source_reference_canonical_sha256"]=canonical_sha(native)
        pkt["reference_digest_private"]=canonical_sha(native)
        pkt["primary_source_digest"]=native["source"]["source_fingerprint"]
        return native,pkt,bridge,fresh()

    def test_formal_source_locked_only_entry(self):
        native,pkt,bridge,r=self.locked_fixture()
        report=score_locked(native,pkt,bridge,r)
        self.assertEqual(report["paper"],"FULL")
        self.assertTrue(report["source_reference_alignment_checked"])
        self.assertTrue(report["role_bridge_pre_D_checked"])
        self.assertTrue(report["packet_digest_checked"])

    def test_formal_scoring_blocks_self_serving_edge_denominator(self):
        native,pkt,bridge,r=self.locked_fixture()
        edge=r["variants"][0]["metrics"]["edges"]
        edge["required_ids"]=[];edge["matched_ids"]=[];edge["critical_ids"]=[]
        self.assertEqual(score(r)["paper"],"FULL")
        with self.assertRaisesRegex(G3Error,"SOURCE_NATIVE_DENOMINATOR"):
            score_locked(native,pkt,bridge,r)

    def test_formal_scoring_blocks_hidden_negative_denominator(self):
        native,pkt,bridge,r=self.locked_fixture()
        negative=r["variants"][0]["metrics"]["restrictions"]
        negative["required_ids"]=[];negative["matched_ids"]=[];negative["critical_ids"]=[]
        with self.assertRaisesRegex(G3Error,"SOURCE_NATIVE_DENOMINATOR"):
            score_locked(native,pkt,bridge,r)

    def test_formal_scoring_blocks_unfrozen_grammar_role_denominator(self):
        native,pkt,bridge,r=self.locked_fixture()
        roles=r["variants"][0]["metrics"]["roles"]
        roles["required_ids"]=[];roles["matched_ids"]=[];roles["critical_ids"]=[]
        with self.assertRaisesRegex(G3Error,"ROLE_DENOMINATOR"):
            score_locked(native,pkt,bridge,r)

    def test_formal_scoring_prevents_oracle_packet_swap(self):
        native,pkt,bridge,r=self.locked_fixture()
        pkt["reference_digest_private"]="incorrect"
        with self.assertRaisesRegex(G3Error,"SOURCE_OR_REFERENCE_PACKET_DIGEST"):
            score_locked(native,pkt,bridge,r)

    def test_formal_scoring_prevents_source_medium_swap(self):
        native,pkt,bridge,r=self.locked_fixture()
        native["source"]["primary_kind"]="PUBLISHER_COMPLETE_ORIGINAL_HTML"
        bridge["source_reference_canonical_sha256"]=canonical_sha(native)
        pkt["reference_digest_private"]=canonical_sha(native)
        with self.assertRaisesRegex(G3Error,"ORIGINAL_PRIMARY_MEDIUM"):
            score_locked(native,pkt,bridge,r)
        r["source_state"]="VERIFIED_HTML"
        self.assertEqual(score_locked(native,pkt,bridge,r)["paper"],"FULL")

    def test_role_bridge_cannot_be_post_grammar(self):
        native,pkt,bridge,r=self.locked_fixture()
        bridge["bridge_frozen_before_D"]=False
        with self.assertRaises(G3Error):check_role_bridge(native,bridge)

    def test_role_bridge_must_be_source_grounded(self):
        native,pkt,bridge,r=self.locked_fixture()
        bridge["variants"][0]["role_obligations"][0]["source_atom_ids"]=["invented_source_n"]
        with self.assertRaisesRegex(G3Error,"ROLE_OBLIGATION_WITHOUT_NATIVE_SOURCE"):
            check_role_bridge(native,bridge)

    def test_role_bridge_reference_digest_change_detected(self):
        native,pkt,bridge,r=self.locked_fixture()
        bridge["source_reference_canonical_sha256"]="f"*64
        with self.assertRaisesRegex(G3Error,"ROLE_BRIDGE_REFERENCE_SWAP"):
            check_role_bridge(native,bridge)

    def test_reference_limit_unallocated_blocks_source_freeze(self):
        native,pkt,bridge,r=self.locked_fixture()
        native["original_limitations"].append(dict(id="neg_unallocated",source_locator="synthetic",
                                                   witness="not actually allocated",critical=True))
        with self.assertRaisesRegex(G3Error,"UNALLOCATED_NATIVE_SOURCE_LIMITATION"):
            check_reference(native)

    def test_locked_scoring_invalid_packet_is_not_allowed(self):
        native,pkt,bridge,r=self.locked_fixture()
        pkt["scope_integrity"]["variant_boundaries_kept"]=False
        with self.assertRaisesRegex(G3Error,"INCOMPLETE_OR_UNAPPROVED"):
            score_locked(native,pkt,bridge,r)


    def test_fake_R2_independence_without_actual_receipt_rejected(self):
        native=ref()
        native["assessor"]["independence_disclosure"]="INDEPENDENT_R2_COMPLETED"
        with self.assertRaises(G3Error):check_reference(native)

    def test_same_actor_fake_R2_independence_rejected(self):
        native=ref()
        actor=native["assessor"]
        actor["independence_disclosure"]="INDEPENDENT_R2_COMPLETED"
        actor["r2_attestation"]=dict(assessor_token=actor["assessor_token"],
                                     full_original_read=True,blind_to_D_E=True,
                                     separate_actor_receipt_sha256="a"*64)
        with self.assertRaisesRegex(G3Error,"R2_NOT_ACTUALLY_SEPARATE"):
            check_reference(native)

    def test_R2_bounded_structural_record_not_automatic_source_truth(self):
        native=ref()
        actor=native["assessor"]
        actor["independence_disclosure"]="INDEPENDENT_R2_COMPLETED"
        actor["r2_attestation"]=dict(assessor_token="DIFFERENT_SYNTHETIC_ACTOR",
                                     full_original_read=True,blind_to_D_E=True,
                                     separate_actor_receipt_sha256="b"*64)
        self.assertTrue(check_reference(native))
        # This constructed test cannot establish a genuine separate real-world reader.


    def test_h2_raw_claim_cannot_bypass_locked_missing_source_comparison(self):
        native,pkt,bridge,r=self.locked_fixture()
        h=r["coordination"]
        h.update(a0="FAILED",a1="FAILED",a2="SUPPORTED",discrimination="H2_SOURCE_CONDITIONAL",
                 source_defined_functions_exhausted=True,additional_state_source_grounded=True)
        r["assumptions"]=[dict(id="a2",level="A2",source_grounded=True,necessity_test="PASS")]
        self.assertEqual(coordination(r),"H2_SOURCE_CONDITIONAL")  # Untrusted self-report.
        self.assertEqual(coordination_locked(native,pkt,bridge,r),"NON_DISCRIMINATING")

    def test_h2_source_native_history_comparison_is_necessary_not_proof(self):
        native,pkt,bridge,r=self.locked_fixture()
        native["variants"][0]["source_comparisons"]=[dict(
            id="native_history_difference",source_locator="SYNTHETIC:fictional-test",
            witness="synthetic same input, distinct histories",critical=True,
            contrast_kind="HISTORY_DEPENDENCE_CONTRAST")]
        pkt["reference_digest_private"]=canonical_sha(native)
        bridge["source_reference_canonical_sha256"]=canonical_sha(native)
        h=r["coordination"]
        h.update(a0="FAILED",a1="FAILED",a2="SUPPORTED",discrimination="H2_SOURCE_CONDITIONAL",
                 source_defined_functions_exhausted=True,additional_state_source_grounded=True)
        r["assumptions"]=[dict(id="a2",level="A2",source_grounded=True,necessity_test="PASS")]
        self.assertEqual(coordination_locked(native,pkt,bridge,r),"H2_SOURCE_CONDITIONAL")
        # Only checks structured predeclared SOURCE witness; no real scientific H2 proof.

    def test_h1_incompatible_source_history_only_contrast_is_nondiscriminating(self):
        native,pkt,bridge,r=self.locked_fixture()
        native["variants"][0]["source_comparisons"]=[dict(
            id="native_history_difference",source_locator="SYNTHETIC:fictional-test",
            witness="synthetic history comparison",critical=True,
            contrast_kind="HISTORY_DEPENDENCE_CONTRAST")]
        pkt["reference_digest_private"]=canonical_sha(native)
        bridge["source_reference_canonical_sha256"]=canonical_sha(native)
        h=r["coordination"]
        h.update(a0="FAILED",a1="SUPPORTED",discrimination="H1_SOURCE_CONDITIONAL")
        r["assumptions"]=[dict(id="a1",level="A1",source_grounded=True,necessity_test="PASS")]
        self.assertEqual(coordination_locked(native,pkt,bridge,r),"NON_DISCRIMINATING")

if __name__ == "__main__":
    unittest.main(verbosity=2)
