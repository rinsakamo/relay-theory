#!/usr/bin/env python3
"""Synthetic adverse G4-B06/B08 tests; no MAIN identities, originals or scientific results."""
import copy
import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from qualify_g3_v11 import (G3Error, SEQUENCE, schema, check_authorization,
    check_role_isolation, check_completeness, raw_sha, verify_exact_freeze_chain,
    verify_anonymous_atlas, guarded_score)
from nonmain_dryrun import assemble_constructed_packet
from evaluate_g3 import canonical_sha

ROOT = Path(__file__).resolve().parent
H = lambda text: hashlib.sha256(text.encode()).hexdigest()

def envelope(purpose="DRYRUN_NON_MAIN", source_class="CONSTRUCTED_NONMAIN"):
    return dict(schema_version="G3_QUALIFICATION_ENVELOPE_V1_1",purpose=purpose,
        source_class=source_class,paper_token="NONMAIN_TEST_ONLY",real_execution=False,
        stage="PREPARED",
        actors=[],source=dict(primary_medium="CONSTRUCTED_SYNTHETIC",
            edition_id="CONSTRUCTED_ONLY",primary_fingerprint=H("test"),
            source_access_state="CONSTRUCTED_FIXTURE",
            source_locator="CONSTRUCTED_NOT_A_REAL_DOI",correction_review="NONE"),
        protocol_sha256=H("protocol_synthetic"),
        authorization=dict(preflight_scope_receipt=None,g4_reaudit_receipt=None,
            joint_manifest_sha256=None,joint_protocol_sha256=None,
            author_main_go_receipt=None,first_paper_go_receipt=None,
            external_verification="NOT_PERFORMED"),
        roster_binding=dict(g1_final_sha256=None,g2_final_sha256=None,slot_id=None,
            locked_before_science=False),
        role_access=dict(r_seen_analyst_result=False,rb_seen_analyst_result=False,
            analyst_received_reference=False,analyst_received_bridge=False,
            analyst_received_anticipated_H=False,
            b_receives_complete_A_and_original=True,
            c_receives_complete_A_B_and_original=True),
        recognition=dict(before_D="UNKNOWN",after_D="UNKNOWN",leakage_events=[],
            prior_exposure="UNKNOWN"),
        packet_integrity=dict(source_completeness_sha256=None,
            packet_raw_sha256=None,curator_assessment="PENDING",
            independent_completeness="NOT_PERFORMED"),
        freeze_artifacts=dict(reference_sha256=None,bridge_sha256=None,
            anonymous_atlas_sha256=None,label_vault_release_receipt=None))

def fake_main(authority=False):
    e=envelope("MAIN_SCIENTIFIC","FINAL_MAIN_ROSTER")
    e["stage"]="S0"
    e["source"]["primary_medium"]="PUBLISHER_ORIGINAL_PDF"
    e["source"]["source_access_state"]="ORIGINAL_ACTUALLY_READ"
    e["roster_binding"].update(g1_final_sha256=H("fictional_g1"),
        g2_final_sha256=H("fictional_g2"),slot_id="FICTIONAL-ONLY",
        locked_before_science=True)
    if authority:
        a=e["authorization"]
        a.update(g4_reaudit_receipt="FICTIONAL_TEST_G4",
            joint_manifest_sha256=H("fictional_joint_manifest"),
            joint_protocol_sha256=H("fictional_protocol"),
            author_main_go_receipt="FICTIONAL_TEST_AUTHOR",
            first_paper_go_receipt="FICTIONAL_TEST_FIRST_PAPER",
            external_verification="EXTERNAL_VERIFIED")
    return e

def actor(role, who, execution, status="PROCEDURAL_SEPARATION_ONLY",sha=None):
    return dict(role=role,actor_id=who,execution_id=execution,actual_separate_from=[],
        independence_status=status,prior_exposure="UNKNOWN",attestation_raw_sha256=sha)

def stage_events():
    stages=SEQUENCE
    shas={st:H("FAKE_TEST_"+st) for st in stages}
    out=[]
    for idx,st in enumerate(stages):
        e=dict(stage=st,paper_token="NONMAIN_ONLY",primary_source_sha256=H("original_nonmain"),
            original_edition="CONSTRUCTED",protocol_sha256=H("protocol"),
            g1_final_sha256=None,g2_final_sha256=None,packet_sha256=shas["P0"],
            authorization_receipt_sha256=None,
            artifact_raw_sha256=shas[st],
            prior_raw_sha256=shas[stages[idx-1]] if idx else None,
            reference_sha256=shas["R0"],bridge_sha256=shas["RB0"],
            actual_scientific_authorized=False)
        if st=="B":
            e.update(complete_original_A_sha256=shas["A"],
                     b_source_sha256=H("original_nonmain"))
        if st=="C":
            e.update(c_A_sha256=shas["A"],c_B_sha256=shas["B"],
                C1_entire_original_A=True,C2_adjacent_negative_and_zero_resweep=True)
        if st=="ATLAS0":e["anonymous_atlas_frozen"]=True
        if st=="UNMASK":
            e["atlas_sha256"]=shas["ATLAS0"]
            e["label_vault_release_authorized"]=True
        out.append(e)
    return out

class G3CompletionTests(unittest.TestCase):
    def test_v11_schemas_are_valid(self):
        for filename in ("qualification-envelope.v1.schema.json",
                         "source-completeness.v1.schema.json"):
            o=json.loads((ROOT/filename).read_text(encoding="utf-8"))
            from jsonschema import Draft202012Validator
            Draft202012Validator.check_schema(o)

    def test_dryrun_only_constructed_scope(self):
        self.assertEqual(check_authorization(envelope()),"NON_MAIN_DRYRUN_ONLY")
        e=envelope();e["source_class"]="FINAL_MAIN_ROSTER"
        with self.assertRaisesRegex(G3Error,"DRYRUN_MAIN"):check_authorization(e)

    def test_dryrun_cannot_claim_metadata_preflight(self):
        e=envelope();e["stage"]="METADATA_ONLY"
        with self.assertRaisesRegex(G3Error,"DRYRUN_MAIN"):check_authorization(e)

    def test_unapproved_main_preflight_blocked(self):
        e=envelope("MAIN_METADATA_PREFLIGHT","FINAL_MAIN_ROSTER")
        e["stage"]="METADATA_ONLY";e["source"]["source_access_state"]="METADATA_ONLY"
        with self.assertRaisesRegex(G3Error,"PREFLIGHT_SEPARATE_AUTHORIZATION"):
            check_authorization(e)

    def test_preflight_scope_cannot_be_r0(self):
        e=envelope("MAIN_METADATA_PREFLIGHT","FINAL_MAIN_ROSTER")
        e["authorization"]["preflight_scope_receipt"]="TEST_ONLY"
        e["stage"]="R0"
        with self.assertRaisesRegex(G3Error,"PREFLIGHT_CANNOT_RUN"):
            check_authorization(e, lambda *_:True)

    def test_preflight_scope_rejects_scientific_reference(self):
        e=envelope("MAIN_METADATA_PREFLIGHT","FINAL_MAIN_ROSTER")
        e["authorization"]["preflight_scope_receipt"]="TEST_ONLY"
        e["stage"]="METADATA_ONLY";e["source"]["source_access_state"]="METADATA_ONLY"
        e["freeze_artifacts"]["reference_sha256"]=H("NO_PREMAIN_REFERENCE")
        with self.assertRaisesRegex(G3Error,"PREFLIGHT_MUST_NOT_GENERATE"):
            check_authorization(e,lambda *_:True)

    def test_preflight_separate_authority_only_not_main_go(self):
        e=envelope("MAIN_METADATA_PREFLIGHT","FINAL_MAIN_ROSTER")
        e["authorization"]["preflight_scope_receipt"]="FICTIONAL_AUTH_FOR_NEGATIVE_TEST"
        e["stage"]="METADATA_ONLY";e["source"]["source_access_state"]="METADATA_ONLY"
        self.assertEqual(check_authorization(e,lambda kind,*_:kind=="PREFLIGHT"),
                         "AUTHORIZED_METADATA_ONLY_NOT_R0_P0")
        e["purpose"]="MAIN_SCIENTIFIC";e["stage"]="S0"
        with self.assertRaises(G3Error):check_authorization(e,lambda *_:True)

    def test_fake_main_all_gates_missing(self):
        with self.assertRaisesRegex(G3Error,"MAIN_JOINT"):
            check_authorization(fake_main())

    def test_fake_main_structured_claim_without_actual_verifier_denied(self):
        with self.assertRaisesRegex(G3Error,"TRUSTED_EXTERNAL"):
            check_authorization(fake_main(True))

    def test_external_verifier_explicitly_rejects_fake_test_token(self):
        with self.assertRaisesRegex(G3Error,"MAIN_AUTHORITY_REJECTED"):
            check_authorization(fake_main(True),lambda *_:False)

    def test_structurally_authorized_test_is_not_real_signature_verification(self):
        e=fake_main(True)
        self.assertEqual(check_authorization(e,lambda *_:True),
                         "EXTERNAL_AUTHORITY_STRUCTURALLY_VERIFIED_FOR_NAMED_PAPER")
        # An artificial lambda cannot verify GitHub author authority; no real token issued.

    def test_fake_main_missing_final_roster_gate(self):
        e=fake_main(True);e["roster_binding"]["g2_final_sha256"]=None
        with self.assertRaisesRegex(G3Error,"FINAL_ROSTER_NOT_LOCKED"):
            check_authorization(e,lambda *_:True)

    def test_fake_main_cannot_skip_b_result_informed(self):
        e=fake_main(True)
        e["role_access"]["b_receives_complete_A_and_original"]=False
        e["actors"]=[actor("REFERENCE_R","r","e1"),actor("ROLE_BRIDGE_RB","rb","e2"),
                     actor("CURATOR_P","p","e3"),actor("GRAMMAR_D","d","e4")]
        with self.assertRaisesRegex(G3Error,"V231_B"):
            check_role_isolation(e)

    def test_reference_analyst_leakage_flag(self):
        e=envelope();e["role_access"]["analyst_received_reference"]=True
        with self.assertRaisesRegex(G3Error,"REFERENCE_OR_ROLE_BRIDGE_LEAKED"):
            check_role_isolation(e)

    def test_source_recognition_known_requires_prior_leakage_log(self):
        e=envelope();e["recognition"]["prior_exposure"]="KNOWN"
        with self.assertRaisesRegex(G3Error,"KNOWN_EXPOSURE"):
            check_role_isolation(e)
        e["recognition"]["leakage_events"]=[dict(type="PRIOR_EXPOSURE",
            source_locator="synthetic_exposure_only",disposition="STRATIFY_NOT_EXCLUDE")]
        self.assertIn("DECLARED_ROLE_ACCESS",check_role_isolation(e))

    def test_false_independent_attestation_rejected(self):
        e=envelope();e["actors"]=[actor("ADJUDICATOR_R2","r2","session",
                                    "ACTUAL_SEPARATE_ASSESSOR",None)]
        with self.assertRaisesRegex(G3Error,"FALSE_INDEPENDENCE"):
            check_role_isolation(e)

    def test_same_person_r2_rejected(self):
        e=envelope();e["actors"]=[actor("REFERENCE_R","one","s1"),
            actor("ADJUDICATOR_R2","one","s2","ACTUAL_SEPARATE_ASSESSOR",H("fake"))]
        with self.assertRaisesRegex(G3Error,"FAKE_INDEPENDENT_R2"):
            check_role_isolation(e)

    def test_separate_roles_required_even_when_main_flags_are_fake(self):
        e=fake_main(True);e["actors"]=[actor("REFERENCE_R","r","s1"),
            actor("ROLE_BRIDGE_RB","r","s2"),actor("CURATOR_P","p","s3"),
            actor("GRAMMAR_D","d","s4")]
        with self.assertRaisesRegex(G3Error,"UNSEPARATED_MAIN"):
            check_role_isolation(e)

    def test_main_pre_D_recognition_mandatory(self):
        e=fake_main(True);e["actors"]=[actor("REFERENCE_R","r","s1"),
            actor("ROLE_BRIDGE_RB","rb","s2"),actor("CURATOR_P","p","s3"),
            actor("GRAMMAR_D","d","s4")]
        e["recognition"]["before_D"]="NOT_COLLECTED"
        with self.assertRaisesRegex(G3Error,"PRE_D_RECOGNITION"):
            check_role_isolation(e)

    def test_real_nonmain_packet_transport_preserves_math_and_limits(self):
        source,packet,doc,f=assemble_constructed_packet()
        self.assertNotEqual(f["source_raw_sha256"],f["packet_raw_sha256"])
        self.assertIn(b"x[t+1] = 0.5*x[t] + u[t]",packet)
        self.assertIn(b"NEGATIVE neg-1:",packet)
        self.assertIn(b"VARIANT variant-2:",packet)
        self.assertNotIn(b"Mock State-Coupling Demonstration",packet)
        self.assertEqual(doc["reference_status"],"SINGLE_REFERENCE_UNVALIDATED")
        self.assertEqual(doc["second_review"]["status"],"CURATOR_ONLY_UNVALIDATED")
        self.assertEqual(len(doc["evidence_audit"]),12)

    def test_packet_negative_clause_not_optional(self):
        _,_,doc,_=assemble_constructed_packet()
        doc["preserved"]["negative"]=[]
        with self.assertRaisesRegex(G3Error,"DECISIVE_SOURCE_PACKET_OMISSION"):
            check_completeness(doc)

    def test_packet_critical_redaction_denied(self):
        _,_,doc,_=assemble_constructed_packet()
        doc["redactions"][0]["scientific_load_bearing"]=True
        with self.assertRaisesRegex(G3Error,"MASK_DESTROYS"):
            check_completeness(doc)

    def test_packet_forged_second_review_denied(self):
        _,_,doc,_=assemble_constructed_packet()
        doc["second_review"]=dict(status="ACTUAL_SEPARATE_ATTESTED",
            actor_id=doc["curator"]["actor_id"],execution_id="other",
            attestation_raw_sha256=H("fake"))
        with self.assertRaisesRegex(G3Error,"CURATOR_SELF_REVIEW"):
            check_completeness(doc)

    def test_packet_unaudited_required_witness_denied(self):
        _,_,doc,_=assemble_constructed_packet()
        doc["evidence_audit"]=[a for a in doc["evidence_audit"] if a["source_atom_id"]!="neg-1"]
        with self.assertRaisesRegex(G3Error,"UNREVIEWED_DECISIVE"):
            check_completeness(doc)

    def test_stage_exact_full_synthetic_order(self):
        self.assertEqual(verify_exact_freeze_chain(stage_events())["verified_prefix"],13)

    def test_stage_exact_authorized_partial_prefix(self):
        self.assertEqual(verify_exact_freeze_chain(stage_events()[:2])["next"],"RB0")

    def test_stage_skipped_RB0_cannot_enter_P0(self):
        e=stage_events();e.pop(2)
        with self.assertRaisesRegex(G3Error,"MISSING_SKIPPED"):
            verify_exact_freeze_chain(e)

    def test_stage_swapped_D1_D2_fails(self):
        e=stage_events();e[8],e[9]=e[9],e[8]
        with self.assertRaisesRegex(G3Error,"MISSING_SKIPPED"):
            verify_exact_freeze_chain(e)

    def test_stage_rewrite_source_fails(self):
        e=stage_events();e[5]["primary_source_sha256"]=H("swapped")
        with self.assertRaisesRegex(G3Error,"SOURCE_PROTOCOL"):
            verify_exact_freeze_chain(e)

    def test_stage_rewrite_packet_fails(self):
        e=stage_events();e[5]["packet_sha256"]=H("swapped")
        with self.assertRaisesRegex(G3Error,"SOURCE_PROTOCOL"):
            verify_exact_freeze_chain(e)

    def test_stage_b_must_see_whole_A(self):
        e=stage_events();e[5]["complete_original_A_sha256"]=H("A_truncated")
        with self.assertRaisesRegex(G3Error,"B_MUST_SEE"):
            verify_exact_freeze_chain(e)

    def test_stage_c_both_safeguards_mandatory(self):
        for key in ("C1_entire_original_A","C2_adjacent_negative_and_zero_resweep"):
            with self.subTest(key=key):
                e=stage_events();e[6][key]=False
                with self.assertRaisesRegex(G3Error,"V231"):
                    verify_exact_freeze_chain(e)

    def test_stage_role_bridge_bad_native_sha(self):
        e=stage_events();e[2]["reference_sha256"]=H("wrong_ref")
        with self.assertRaisesRegex(G3Error,"ROLE_BRIDGE_NOT_BOUND"):
            verify_exact_freeze_chain(e)

    def test_stage_unmask_denied_without_atlas_reference(self):
        e=stage_events();e[-1]["atlas_sha256"]=H("bad_atlas")
        with self.assertRaisesRegex(G3Error,"LABEL_UNMASK"):
            verify_exact_freeze_chain(e)

    def test_stage_missing_git_actual_authority_fails(self):
        e=stage_events()
        with self.assertRaisesRegex(G3Error,"MISSING_FINAL_SCIENTIFIC_BINDING"):
            verify_exact_freeze_chain(e[:2],scientific=True)

    def test_actual_temp_git_stage_bytes_and_ancestor_success(self):
        events=stage_events()[:2]
        for x in events:
            for key in ("g1_final_sha256","g2_final_sha256","authorization_receipt_sha256"):
                x[key]=H("test_only_"+key)
            x["actual_scientific_authorized"]=True # git plumbing test only!
        with tempfile.TemporaryDirectory() as d:
            git=["git","-C",d]
            def run(*args):
                return subprocess.check_output([*git,*args],stderr=subprocess.PIPE).strip().decode()
            run("init","-q");run("config","user.email","test@example.invalid")
            run("config","user.name","SYNTHETIC-NOT-A-READER")
            for e in events:
                path=Path(d)/(e["stage"]+".dat")
                data=("SYNTHETIC_RAW_GIT_BYTES_"+e["stage"]).encode()
                path.write_bytes(data);e["artifact_raw_sha256"]=raw_sha(data)
                if e["stage"]=="R0":e["prior_raw_sha256"]=events[0]["artifact_raw_sha256"]
                receipt_path=Path(d)/(e["stage"]+".receipt.json")
                recorded={k:e[k] for k in ("stage","artifact_raw_sha256","prior_raw_sha256",
                          "primary_source_sha256","protocol_sha256","paper_token",
                          "authorization_receipt_sha256")}
                receipt_data=(json.dumps(recorded,sort_keys=True)+"\n").encode()
                receipt_path.write_bytes(receipt_data)
                e["receipt_raw_sha256"]=raw_sha(receipt_data)
                e["receipt_signed_freeze"]=True # constructed signed-flag, no true signatory
                run("add",path.name,receipt_path.name)
                run("commit","-q","-m","synthetic_"+e["stage"])
                e["git_commit"]=run("rev-parse","HEAD")
                e["git_artifact_path"]=path.name
                e["git_receipt_path"]=receipt_path.name
            self.assertTrue(verify_exact_freeze_chain(events,repo_path=d,
                    scientific=True)["scientific_git_verification"])
            events[1]["artifact_raw_sha256"]=H("forged")
            with self.assertRaisesRegex(G3Error,"GIT_BLOB_RAW_BYTES"):
                verify_exact_freeze_chain(events,repo_path=d,scientific=True)

    def test_anonymous_atlas_multimaxima_preserved(self):
        atlas=dict(anonymized=True,atlas_raw_sha256=H("fake"),
          maximal_common_images=[["anon-e1","anon-n1"],["anon-e1","anon-n2"]],
          comparator_semantics="FROZEN_NO_REDEFINITION",
          forgetful_map_contract_sha256=H("known_frozen_digest"),
          identity_release=None)
        self.assertIn("ANONYMOUS_ATLAS",
                      verify_anonymous_atlas(atlas,["famous_construct"]))
        atlas["maximal_common_images"][0].append("famous_construct")
        with self.assertRaisesRegex(G3Error,"LABEL_LEAKED"):
            verify_anonymous_atlas(atlas,["famous_construct"])

    def test_guarded_scientific_score_always_blocks_without_external_go(self):
        e=fake_main(True)
        with self.assertRaisesRegex(G3Error,"TRUSTED_EXTERNAL"):
            guarded_score(None,None,None,None,e,None)


    def test_metadata_preflight_cannot_create_hidden_packet(self):
        e=envelope("MAIN_METADATA_PREFLIGHT","FINAL_MAIN_ROSTER")
        e["authorization"]["preflight_scope_receipt"]="FICTIONAL_TEST"
        e["stage"]="METADATA_ONLY"
        e["source"]["source_access_state"]="METADATA_ONLY"
        e["packet_integrity"]["packet_raw_sha256"]=H("surreptitious_packet")
        with self.assertRaisesRegex(G3Error,"PREFLIGHT_MUST_NOT_GENERATE"):
            check_authorization(e,lambda *_:True)

    def test_metadata_preflight_cannot_start_silent_reference_assessor(self):
        e=envelope("MAIN_METADATA_PREFLIGHT","FINAL_MAIN_ROSTER")
        e["authorization"]["preflight_scope_receipt"]="FICTIONAL_TEST"
        e["stage"]="METADATA_ONLY"
        e["source"]["source_access_state"]="METADATA_ONLY"
        e["actors"]=[actor("REFERENCE_R","fake_r","fake_execution")]
        with self.assertRaisesRegex(G3Error,"PREFLIGHT_MUST_NOT_GENERATE"):
            check_authorization(e,lambda *_:True)

    def test_scientific_stage_receipt_hash_tamper_is_caught(self):
        e=stage_events()[:1]
        for key in ("g1_final_sha256","g2_final_sha256","authorization_receipt_sha256"):
            e[0][key]=H("fictional_"+key)
        e[0]["actual_scientific_authorized"]=True
        with tempfile.TemporaryDirectory() as d:
            git=["git","-C",d]
            def run(*args):
                return subprocess.check_output([*git,*args],stderr=subprocess.PIPE).strip().decode()
            run("init","-q");run("config","user.email","fixture@example.invalid")
            run("config","user.name","FICTIONAL")
            data=b"synthetic_stage_artifact";Path(d,"S0.dat").write_bytes(data)
            e[0]["artifact_raw_sha256"]=raw_sha(data)
            meta={k:e[0][k] for k in ("stage","artifact_raw_sha256","prior_raw_sha256",
                "primary_source_sha256","protocol_sha256","paper_token","authorization_receipt_sha256")}
            record=(json.dumps(meta,sort_keys=True)+"\n").encode()
            Path(d,"S0.receipt.json").write_bytes(record)
            run("add","S0.dat","S0.receipt.json")
            run("commit","-q","-m","fixture")
            e[0].update(git_commit=run("rev-parse","HEAD"),
                git_artifact_path="S0.dat",git_receipt_path="S0.receipt.json",
                receipt_raw_sha256=raw_sha(record),receipt_signed_freeze=True)
            self.assertTrue(verify_exact_freeze_chain(e,repo_path=d,scientific=True)["scientific_git_verification"])
            e[0]["receipt_raw_sha256"]=H("mutated_receipt")
            with self.assertRaisesRegex(G3Error,"IMMUTABLE_STAGE_RECEIPT_RAW_BYTES"):
                verify_exact_freeze_chain(e,repo_path=d,scientific=True)


    def test_locked_v11_rubric_preserves_all_controls_and_null_joint_freeze(self):
        r=json.loads((ROOT/"G3_MEASUREMENT_CONTROL_COMPARISON_RUBRIC_v1.1.json").read_text(encoding="utf-8"))
        self.assertEqual(set(r["negative_controls"]),{"REMOVE_EDGE","REVERSE_TEMPORAL",
            "SWAP_BOUNDARY","REMOVE_NATIVE_COORDINATOR","MERGE_VARIANTS",
            "STATEFUL_TO_STATELESS","REMOVE_NEGATIVE","G_DYN"})
        self.assertEqual(len(r["negative_controls"]),8)
        self.assertEqual(len(r["reporting"]["evidence_classes"]),6)
        self.assertIsNone(r["roster_bindings"]["g1_final_sha256"])
        self.assertIsNone(r["roster_bindings"]["g2_final_sha256"])
        self.assertFalse(r["roster_bindings"]["first_main_authorized"])

if __name__=="__main__":
    unittest.main(verbosity=2)
