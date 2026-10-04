#!/usr/bin/env python3
"""G3 v1.1 permission/completeness/staging tests. NOT historic #401 or scientific truth validator.
No real MAIN transaction may proceed without a separate *trusted* external authority verifier.
"""
import hashlib
import json
import subprocess
from pathlib import Path
from jsonschema import Draft202012Validator
from evaluate_g3 import G3Error, check_reference, check_packet, check_role_bridge, score_locked, coordination_locked, canonical_sha

ROOT = Path(__file__).resolve().parent
MAIN = ("S0", "R0", "P0", "A", "B", "C", "D0", "D1", "D2", "E0", "ATLAS0", "UNMASK")
SEQUENCE = ("S0", "R0", "RB0", "P0", "A", "B", "C", "D0", "D1", "D2", "E0", "ATLAS0", "UNMASK")
CATEGORIES = ("sections", "equations", "figures", "states", "dependencies",
              "temporal", "variants", "negative", "boundaries")
LEAKAGE = ("MATH_DIRECT", "FIGURE_DIRECT", "PRIOR_EXPOSURE", "PRETRAINED_POSSIBLE",
           "CURATOR_RELEASE", "UNEXPECTED_LABEL")

def raw_sha(raw):
    return hashlib.sha256(raw).hexdigest()

def schema(name, obj):
    specification = json.loads((ROOT / name).read_bytes().decode("utf-8"))
    Draft202012Validator.check_schema(specification)
    errors = sorted(Draft202012Validator(specification).iter_errors(obj), key=lambda e: str(e.path))
    if errors:
        e = errors[0]
        raise G3Error("SCHEMA_" + name + ":" + str(list(e.path)) + ":" + e.message)
    return True

def check_authorization(envelope, trusted_authority_verifier=None):
    """Structural gate, not an author signature service. None = main activities blocked."""
    schema("qualification-envelope.v1.schema.json", envelope)
    mode, source = envelope["purpose"], envelope["source_class"]
    authorization = envelope["authorization"]
    if mode == "DRYRUN_NON_MAIN":
        if source not in ("CONSTRUCTED_NONMAIN", "EXPOSED_PILOT") or envelope["stage"] == "METADATA_ONLY":
            raise G3Error("DRYRUN_MAIN_OR_UNAUTHORIZED_SCOPE")
        # Dry runs are never independent prospective scientific calibration.
        return "NON_MAIN_DRYRUN_ONLY"
    if source != "FINAL_MAIN_ROSTER":
        raise G3Error("MAIN_REQUIRES_EXACT_FINAL_ROSTER_SOURCE")
    if mode == "MAIN_METADATA_PREFLIGHT":
        if envelope["stage"] != "METADATA_ONLY":
            raise G3Error("PREFLIGHT_CANNOT_RUN_MAIN_SCIENTIFIC_STAGE")
        if (any(v is not None for v in envelope["freeze_artifacts"].values()) or
                envelope["packet_integrity"]["packet_raw_sha256"] is not None or
                envelope["packet_integrity"]["source_completeness_sha256"] is not None or
                envelope["packet_integrity"]["curator_assessment"] != "PENDING" or
                any(a["role"] in ("REFERENCE_R", "ROLE_BRIDGE_RB", "CURATOR_P",
                                  "GRAMMAR_D", "ADJUDICATOR_R2")
                    for a in envelope["actors"])):
            raise G3Error("PREFLIGHT_MUST_NOT_GENERATE_SCIENTIFIC_R_P")
        if envelope["source"]["source_access_state"] not in ("METADATA_ONLY", "UNKNOWN"):
            raise G3Error("PREFLIGHT_SOURCE_ANALYSIS_PROHIBITED")
        if not authorization["preflight_scope_receipt"] or not callable(trusted_authority_verifier):
            raise G3Error("PREFLIGHT_SEPARATE_AUTHORIZATION_REQUIRED")
        if not trusted_authority_verifier("PREFLIGHT", authorization, envelope):
            raise G3Error("PREFLIGHT_AUTHORITY_REJECTED")
        return "AUTHORIZED_METADATA_ONLY_NOT_R0_P0"
    if envelope["stage"] in ("PREPARED", "METADATA_ONLY"):
        raise G3Error("MAIN_SCIENCE_STAGE_NOT_SPECIFIED")
    fields = ("g4_reaudit_receipt", "joint_manifest_sha256", "joint_protocol_sha256",
              "author_main_go_receipt", "first_paper_go_receipt")
    if any(not authorization[x] for x in fields):
        raise G3Error("MAIN_JOINT_AND_FIRST_PAPER_AUTHORITY_INCOMPLETE")
    binding = envelope["roster_binding"]
    if not binding["locked_before_science"] or not binding["g1_final_sha256"] or (
            not binding["g2_final_sha256"] or not binding["slot_id"]):
        raise G3Error("MAIN_FINAL_ROSTER_NOT_LOCKED")
    if not callable(trusted_authority_verifier) or (
            authorization["external_verification"] != "EXTERNAL_VERIFIED"):
        raise G3Error("MAIN_REQUIRES_TRUSTED_EXTERNAL_AUTHORITY_VERIFICATION")
    if not trusted_authority_verifier("MAIN_JOINT_AND_FIRST_PAPER", authorization, envelope):
        raise G3Error("MAIN_AUTHORITY_REJECTED")
    # This result is only a checked structure; external verifier must certify true
    # GitHub issue/author identities, signatures, scope, hashes and antecedent dates.
    return "EXTERNAL_AUTHORITY_STRUCTURALLY_VERIFIED_FOR_NAMED_PAPER"

def check_role_isolation(envelope, reference=None, bridge=None):
    schema("qualification-envelope.v1.schema.json", envelope)
    r = envelope["role_access"]
    if any(r[k] for k in ("r_seen_analyst_result", "rb_seen_analyst_result",
                          "analyst_received_reference", "analyst_received_bridge",
                          "analyst_received_anticipated_H")):
        raise G3Error("REFERENCE_OR_ROLE_BRIDGE_LEAKED")
    if envelope["purpose"] == "MAIN_SCIENTIFIC" and not (
            r["b_receives_complete_A_and_original"] and r["c_receives_complete_A_B_and_original"]):
        raise G3Error("V231_B_IS_RESULT_INFORMED_C_IS_SOURCE_CLOSED")
    actors = envelope["actors"]
    keyed = {}
    for actor in actors:
        role = actor["role"]
        if role in keyed:
            raise G3Error("MULTIPLE_UNDECLARED_ROLE_ACTORS")
        keyed[role] = actor
        if actor["independence_status"] == "ACTUAL_SEPARATE_ASSESSOR" and (
                not actor.get("attestation_raw_sha256")):
            raise G3Error("FALSE_INDEPENDENCE_WITHOUT_REAL_RECEIPT")
    if envelope["purpose"] == "MAIN_SCIENTIFIC":
        if not all(k in keyed for k in ("REFERENCE_R", "ROLE_BRIDGE_RB", "CURATOR_P", "GRAMMAR_D")):
            raise G3Error("MISSING_OPERATIONAL_ROLE_ASSIGNMENT")
        if reference is not None and (
                reference["assessor"]["independence_disclosure"] == "INDEPENDENT_R2_COMPLETED"):
            if "ADJUDICATOR_R2" not in keyed:
                raise G3Error("FALSE_R2_WITHOUT_DISTINCT_ACTOR")
            att = reference["assessor"]["r2_attestation"]
            if att["assessor_token"] != keyed["ADJUDICATOR_R2"]["actor_id"] or (
                    att["separate_actor_receipt_sha256"] !=
                    keyed["ADJUDICATOR_R2"].get("attestation_raw_sha256")):
                raise G3Error("R2_ATTESTATION_ACTOR_OR_HASH_MISMATCH")
        distinct_roles = ("REFERENCE_R", "ROLE_BRIDGE_RB", "CURATOR_P", "GRAMMAR_D")
        if len({keyed[k]["actor_id"] for k in distinct_roles}) != 4 or (
                len({keyed[k]["execution_id"] for k in distinct_roles}) != 4):
            raise G3Error("UNSEPARATED_MAIN_REFERENCE_BRIDGE_CURATOR_ANALYST")
        if reference is not None and (
                reference["assessor"]["assessor_token"] != keyed["REFERENCE_R"]["actor_id"]):
            raise G3Error("REFERENCE_ASSESSOR_ID_MISMATCH")
        if envelope["recognition"]["before_D"] == "NOT_COLLECTED":
            raise G3Error("PRE_D_RECOGNITION_NOT_RECORDED")
    if "ADJUDICATOR_R2" in keyed and "REFERENCE_R" in keyed:
        left, right = keyed["REFERENCE_R"], keyed["ADJUDICATOR_R2"]
        if left["actor_id"] == right["actor_id"] or (
                left["execution_id"] == right["execution_id"]):
            raise G3Error("FAKE_INDEPENDENT_R2")
        if right["independence_status"] != "ACTUAL_SEPARATE_ASSESSOR":
            raise G3Error("R2_NOT_INDEPENDENTLY_ATTESTED")
    flags = set(envelope["recognition"]["leakage_events"][i]["type"]
                for i in range(len(envelope["recognition"]["leakage_events"])))
    if envelope["recognition"]["prior_exposure"] == "KNOWN" and (
            "PRIOR_EXPOSURE" not in flags):
        raise G3Error("KNOWN_EXPOSURE_NOT_LOGGED")
    if reference is not None:
        check_reference(reference)
    if bridge is not None:
        if reference is None:
            raise G3Error("ROLE_BRIDGE_REQUIRES_NATIVE_REFERENCE")
        check_role_bridge(reference, bridge)
    return "DECLARED_ROLE_ACCESS_CHECKED_NOT_SEMANTIC_INDEPENDENCE_CERTIFIED"

def check_completeness(doc, packet=None):
    schema("source-completeness.v1.schema.json", doc)
    if doc["second_review"]["status"] == "ACTUAL_SEPARATE_ATTESTED":
        peer = doc["second_review"]
        curator = doc["curator"]
        if not peer["attestation_raw_sha256"] or peer["actor_id"] == curator["actor_id"] or (
                peer["execution_id"] == curator["execution_id"]):
            raise G3Error("CURATOR_SELF_REVIEW_MISREPRESENTED")
    if doc["reference_status"] == "INDEPENDENT_R2_COMPLETED" and (
            doc["second_review"]["status"] == "NOT_PERFORMED"):
        # Distinct R2 and packet reviewer are different duties; no implication.
        pass
    required_union = set()
    for category in CATEGORIES:
        required, seen = set(doc["required"][category]), set(doc["preserved"][category])
        if required != seen:
            raise G3Error("DECISIVE_SOURCE_PACKET_OMISSION_OR_ADDITION:" + category)
        for witness in required:
            required_union.add((category, witness))
    if any(red["scientific_load_bearing"] for red in doc["redactions"]):
        raise G3Error("MASK_DESTROYS_LOAD_BEARING_SOURCE_INFORMATION")
    proofs = {(p["source_atom_id"], p["original_locator"], p["preserved_packet_locator"])
              for p in doc["evidence_audit"]}
    if any(not x[1].strip() or not x[2].strip() for x in proofs):
        raise G3Error("EMPTY_PRIMARY_OR_PACKET_EVIDENCE_LOCATOR")
    audited_ids = {x["source_atom_id"] for x in doc["evidence_audit"]}
    if not set().union(*[set(doc["required"][c]) for c in CATEGORIES]) <= audited_ids:
        raise G3Error("UNREVIEWED_DECISIVE_SOURCE_WITNESS")
    if packet is not None:
        check_packet(packet)
        if packet["paper_token"] != doc["paper_token"] or (
                packet["primary_source_digest"] != doc["source_fingerprint"]):
            raise G3Error("PACKET_SOURCE_IDENTITY_MISMATCH")
        integrity = packet["scope_integrity"]
        if not all(integrity[k] for k in (
                "equations_kept", "figures_kept", "negative_outcomes_kept",
                "variant_boundaries_kept", "source_order_kept")):
            raise G3Error("PACKET_INTEGRITY_DECLARATION_FALSE")
    return "BOUNDED_RECORDED_SOURCE_COMPLETENESS_CHECK_ONLY"

def guarded_score(reference, packet, bridge, record, envelope, completeness,
                  trusted_authority_verifier=None):
    if envelope["purpose"] != "MAIN_SCIENTIFIC":
        raise G3Error("SYNTHETIC_OR_PREFLIGHT_CANNOT_ISSUE_MAIN_SCIENTIFIC_FIDELITY")
    check_authorization(envelope, trusted_authority_verifier)
    check_role_isolation(envelope, reference, bridge)
    check_completeness(completeness, packet)
    if completeness["native_reference_digest"] != canonical_sha(reference):
        raise G3Error("SOURCE_COMPLETENESS_NOT_TIED_TO_LOCKED_NATIVE_REFERENCE")
    if envelope["packet_integrity"]["independent_completeness"] != completeness["second_review"]["status"]:
        raise G3Error("FALSE_INDEPENDENT_PACKET_COMPLETENESS")
    if len({envelope["source"]["primary_fingerprint"], completeness["source_fingerprint"],
            reference["source"]["source_fingerprint"], packet["primary_source_digest"]}) != 1:
        raise G3Error("QUALIFICATION_ORIGINAL_SOURCE_IDENTITY_MISMATCH")
    if envelope["freeze_artifacts"]["reference_sha256"] != canonical_sha(reference) or (
            envelope["freeze_artifacts"]["bridge_sha256"] != canonical_sha(bridge)):
        raise G3Error("QUALIFICATION_REFERENCE_OR_BRIDGE_NOT_LOCKED")
    if envelope["packet_integrity"]["packet_raw_sha256"] != packet["packet_digest"]:
        raise G3Error("QUALIFICATION_PACKET_BYTES_NOT_LOCKED")
    if envelope["packet_integrity"]["source_completeness_sha256"] != canonical_sha(completeness):
        raise G3Error("SOURCE_COMPLETENESS_NOT_LOCKED")
    if record["reference_state"] == "LOCKED_INDEPENDENT" and (
            reference["assessor"]["independence_disclosure"] != "INDEPENDENT_R2_COMPLETED"):
        raise G3Error("FAKE_INDEPENDENT_REFERENCE_VERDICT")
    return score_locked(reference, packet, bridge, record)

def guarded_coordination(reference, packet, bridge, record, envelope, completeness,
                         trusted_authority_verifier=None):
    guarded_score(reference, packet, bridge, record, envelope, completeness,
                  trusted_authority_verifier=trusted_authority_verifier)
    return coordination_locked(reference, packet, bridge, record)

def git_run(repo_path, *args):
    res = subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True,
                         text=False, check=False)
    if res.returncode:
        raise G3Error("GIT_PROVENANCE_UNAVAILABLE:" + " ".join(args))
    return res.stdout.strip().decode("utf-8")

def verify_exact_freeze_chain(events, repo_path=None, scientific=False,
                              mandatory_protocol_sha=None, mandatory_source_sha=None):
    """Ordered prefix only; RB0 sidecar strictly between R0 and P0; exact raw Git bytes
    and actual full Git ancestry REQUIRED for scientific runs.
    """
    if not events or len(events) > len(SEQUENCE):
        raise G3Error("MISSING_OR_EXCESS_STAGE_RECEIPTS")
    observed = [e["stage"] for e in events]
    if observed != list(SEQUENCE[:len(events)]):
        raise G3Error("MISSING_SKIPPED_DUPLICATED_OR_REORDERED_STAGE")
    keys = ("paper_token", "primary_source_sha256", "original_edition", "protocol_sha256",
            "g1_final_sha256", "g2_final_sha256", "packet_sha256",
            "authorization_receipt_sha256")
    base = events[0]
    if scientific:
        for name in ("g1_final_sha256", "g2_final_sha256", "packet_sha256",
                     "authorization_receipt_sha256", "primary_source_sha256"):
            value = base.get(name)
            if not isinstance(value, str) or len(value) != 64:
                raise G3Error("MISSING_FINAL_SCIENTIFIC_BINDING:" + name)
        if repo_path is None:
            raise G3Error("REAL_GIT_ANCESTRY_NOT_AVAILABLE")
        if git_run(repo_path, "rev-parse", "--is-shallow-repository") != "false":
            raise G3Error("SHALLOW_GIT_HISTORY_CANNOT_VERIFY_ANCESTRY")
    prev = None
    for e in events:
        if any(e.get(k) != base.get(k) for k in keys):
            raise G3Error("SOURCE_PROTOCOL_ROSTER_PACKET_OR_AUTHORITY_CHANGED")
        if mandatory_protocol_sha and e["protocol_sha256"] != mandatory_protocol_sha:
            raise G3Error("WRONG_FROZEN_PROTOCOL")
        if mandatory_source_sha and e["primary_source_sha256"] != mandatory_source_sha:
            raise G3Error("WRONG_PRIMARY_SOURCE")
        if e.get("artifact_raw_sha256") is None or len(e["artifact_raw_sha256"]) != 64:
            raise G3Error("UNHASHED_ARTIFACT")
        if e.get("prior_raw_sha256") != (prev["artifact_raw_sha256"] if prev else None):
            raise G3Error("BROKEN_IMMUTABLE_STAGE_HASH_CHAIN")
        if e["stage"] == "RB0" and e["reference_sha256"] != events[1]["artifact_raw_sha256"]:
            raise G3Error("ROLE_BRIDGE_NOT_BOUND_TO_R0")
        if e["stage"] == "P0" and (
                e["reference_sha256"] != events[1]["artifact_raw_sha256"] or
                e["bridge_sha256"] != events[2]["artifact_raw_sha256"] or
                e["artifact_raw_sha256"] != base["packet_sha256"]):
            raise G3Error("P0_NOT_BOUND_TO_LOCKED_R_AND_RB_AND_PACKET")
        if e["stage"] == "B" and (
                e.get("complete_original_A_sha256") != events[4]["artifact_raw_sha256"] or
                e.get("b_source_sha256") != base["primary_source_sha256"]):
            raise G3Error("B_MUST_SEE_FULL_FROZEN_A_AND_SAME_ORIGINAL")
        if e["stage"] == "C" and (e.get("c_A_sha256") != events[4]["artifact_raw_sha256"] or
                                   e.get("c_B_sha256") != events[5]["artifact_raw_sha256"] or
                                   not e.get("C1_entire_original_A") or
                                   not e.get("C2_adjacent_negative_and_zero_resweep")):
            raise G3Error("C_MUST_BE_V231_C1_C2_SOURCE_CLOSED")
        if e["stage"] in ("D0", "D1", "D2") and (e.get("reference_sha256") != events[1]["artifact_raw_sha256"] or
                                                     e.get("bridge_sha256") != events[2]["artifact_raw_sha256"]):
            raise G3Error("D_USING_UNFROZEN_ROLE_OR_REFERENCE")
        if e["stage"] == "ATLAS0" and not e.get("anonymous_atlas_frozen"):
            raise G3Error("ANONYMOUS_ATLAS_NOT_FROZEN")
        if e["stage"] == "UNMASK" and (e.get("atlas_sha256") != events[11]["artifact_raw_sha256"] or
                                       not e.get("label_vault_release_authorized")):
            raise G3Error("LABEL_UNMASK_BEFORE_FROZEN_ATLAS")
        if scientific:
            if not e.get("actual_scientific_authorized") or not e.get("git_commit") or (
                    not e.get("git_artifact_path")) or not e.get("git_receipt_path") or (
                    not e.get("receipt_raw_sha256")) or not e.get("receipt_signed_freeze"):
                raise G3Error("SCIENTIFIC_STAGE_MISSING_REAL_AUTHORITY_OR_GIT_ARTIFACT")
            if repo_path is None:
                raise G3Error("REAL_GIT_ANCESTRY_NOT_AVAILABLE")
            sha = e["git_commit"]
            path = e["git_artifact_path"]
            if sha != git_run(repo_path, "rev-parse", sha + "^{commit}"):
                raise G3Error("INVALID_GIT_COMMIT_ID")
            raw = subprocess.run(["git", "-C", str(repo_path), "show", sha + ":" + path],
                                 capture_output=True, check=False)
            if raw.returncode or raw_sha(raw.stdout) != e["artifact_raw_sha256"]:
                raise G3Error("GIT_BLOB_RAW_BYTES_DO_NOT_MATCH")
            receipt = subprocess.run(["git", "-C", str(repo_path), "show",
                                      sha + ":" + e["git_receipt_path"]],
                                     capture_output=True, check=False)
            if receipt.returncode or raw_sha(receipt.stdout) != e["receipt_raw_sha256"]:
                raise G3Error("IMMUTABLE_STAGE_RECEIPT_RAW_BYTES_DO_NOT_MATCH")
            try:
                recorded = json.loads(receipt.stdout.decode("utf-8"))
            except (UnicodeDecodeError, ValueError):
                raise G3Error("INVALID_IMMUTABLE_STAGE_RECEIPT_JSON")
            bound = ("stage", "artifact_raw_sha256", "prior_raw_sha256",
                     "primary_source_sha256", "protocol_sha256", "paper_token",
                     "authorization_receipt_sha256")
            if any(recorded.get(k) != e.get(k) for k in bound):
                raise G3Error("IMMUTABLE_RECEIPT_DOES_NOT_BIND_STAGE_OR_AUTHORITY")
            if prev is not None:
                if sha == prev["git_commit"]:
                    raise G3Error("SCIENTIFIC_STAGES_NOT_IN_DISTINCT_COMMITS")
                git_run(repo_path, "merge-base", "--is-ancestor", prev["git_commit"], sha)
        prev = e
    return {"verified_prefix": len(events), "next": SEQUENCE[len(events)] if len(events) < len(SEQUENCE) else None,
            "scientific_git_verification": scientific}

def verify_anonymous_atlas(atlas, known_source_label_tokens):
    required = ("anonymized", "atlas_raw_sha256", "maximal_common_images",
                "comparator_semantics", "forgetful_map_contract_sha256", "identity_release")
    if not all(k in atlas for k in required):
        raise G3Error("ATLAS_MISSING_LOCKED_COMPARATOR_DATA")
    if not atlas["anonymized"] or atlas["identity_release"] is not None or (
            atlas["comparator_semantics"] != "FROZEN_NO_REDEFINITION"):
        raise G3Error("ATLAS_UNMASKED_OR_COMPARATOR_CHANGED")
    canonical = json.dumps(atlas["maximal_common_images"], ensure_ascii=False, sort_keys=True)
    if any(t.lower() in canonical.lower() for t in known_source_label_tokens if t):
        raise G3Error("ORIGINAL_LABEL_LEAKED_BEFORE_ATLAS_FREEZE")
    images = [tuple(sorted(image)) for image in atlas["maximal_common_images"]]
    if len(images) != len(set(images)):
        raise G3Error("MAXIMAL_COMMON_IMAGE_TIES_COLLAPSED_OR_DUPLICATED")
    # No forced count or fabricated new maximality proof: external frozen comparator required.
    return "ANONYMOUS_ATLAS_STRUCTURE_RECORDED_NOT_SCIENTIFIC_EQUIVALENCE_PROVEN"
