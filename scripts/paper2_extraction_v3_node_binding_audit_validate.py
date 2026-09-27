#!/usr/bin/env python3
"""Synthetic/static audit for Paper 2 #257.

Proves whether the frozen SystemOne-v3 Stage-1 node-binding surface admits
duplicate node referent handles that are only rejected after a wire-valid answer
map has been accepted. No real source text, model, server, or #210 replay.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import paper2_extraction_two_pass_systemone_v3 as v3

BASE = Path(__file__).resolve().parent.parent
ARTIFACT_PATH = BASE / "research/paper2/extraction_v3_node_binding_audit_v1.json"
ARTIFACT_VERSION = "paper2-v3-node-binding-audit-v1"
EXPECTED_STATUS = "V3_NODE_BINDING_DEPENDENCY_DEFECT_CONFIRMED"

BOUND = {
    "scripts/paper2_extraction_two_pass_systemone_v3.py":
        "9e2fdff07fd6b860d9dfe686c384b00d6c66b23f",
    "research/paper2/extraction_two_pass_systemone_v3.json":
        "cbb579742f7f16cbbe51f7db9603eaa8639d841e",
    "research/paper2/extraction_systemone_decision_v3.schema.json":
        "22c1b6dce32f71d70dcc30d3c6879c18845b4c3f",
    "scripts/paper2_extraction_two_pass_llama_cpp_transaction_v3.py":
        "75f8436758bb5c93c5ca3a834e7c807155d5ce05",
    "research/paper2/extraction_v3_real_calibration_transaction_v1.json":
        "1abb318ff1f4160b38301169032c4924b58b3338",
    "research/paper2/claim_ir_v1.schema.json":
        "963f54bd61c3112daa046fa191e3194d47db0768",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def load_artifact() -> dict[str, Any]:
    value = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    if value.get("schema_version") != ARTIFACT_VERSION:
        fail("artifact schema drift")
    if value.get("owner_issue") != 257:
        fail("artifact owner drift")
    if value.get("status") != EXPECTED_STATUS:
        fail("artifact terminal classification drift")
    if value.get("architecture_consequence") != "NONE":
        fail("architecture consequence drift")
    if value.get("bound_repository_blobs") != BOUND:
        fail("bound repository identities drift")
    for rel, expected in BOUND.items():
        raw = (BASE / rel).read_bytes()
        actual = git_blob_sha(raw)
        if actual != expected:
            fail(f"bound blob changed: {rel}: {actual} != {expected}")
    accounting = value.get("scientific_accounting", {})
    if any(accounting.get(k) != 0 for k in (
        "real_model_calls",
        "real_server_launches",
        "real_literature_extraction",
        "paper210_replay",
        "paper193_replay",
        "heldout_execution",
        "basis_decomposition",
    )):
        fail("scientific accounting must remain zero")
    parent = value.get("parent_terminal", {})
    if parent.get("issue") != 210 or parent.get("terminal_comment_id") != 5855526067:
        fail("#210 terminal provenance drift")
    if parent.get("outcomes") != {
        "VALID_CLAIM_IR": 0,
        "EXTRACTION_ABSTAIN": 2,
        "EXTRACTION_FAILURE": 8,
    }:
        fail("#210 outcome provenance drift")
    return value


def default_stage1_answers(source: dict[str, Any]) -> dict[str, str]:
    questions = v3.stage1(source)
    answers = v3.answer_defaults(questions)
    answers["claim_type"] = "relation"
    answers["modality"] = "descriptive"
    for name in questions:
        if name.startswith("scope__"):
            answers[name] = "no"
    return answers


def duplicate_handle_witness() -> dict[str, Any]:
    source = v3.v2.synthetic_source(
        ["Synthetic evidence unit A.", "Synthetic evidence unit B."],
        bundle_id="B9257",
    )
    questions = v3.stage1(source)

    handle = "s1::condition"
    for slot in ("n1", "n2", "n3"):
        if handle not in questions[f"{slot}__seed"]["criteria"]:
            fail(f"A1: common handle absent from {slot}")

    if questions["n1__seed"]["criteria"] != questions["n2__seed"]["criteria"]:
        fail("A1: n1/n2 seed criteria unexpectedly differ")
    if questions["n2__seed"]["criteria"] != questions["n3__seed"]["criteria"]:
        fail("A1: n2/n3 seed criteria unexpectedly differ")

    answers = default_stage1_answers(source)
    answers["n1__seed"] = handle
    answers["n2__seed"] = handle
    answers["n3__seed"] = "NONE"

    # This is the key witness: the duplicate tuple is locally wire-admissible.
    v3.check_answers(questions, answers)

    error = None
    try:
        v3.bindings(source, answers)
    except v3.v2.TwoPassV2Error as exc:
        error = str(exc)
    if error != "duplicate or unknown node referent handle":
        fail(f"A6: expected duplicate-handle rejection, got {error!r}")

    # The same rejection is the earliest dependency barrier to Stage 2.
    stage2_error = None
    try:
        v3.stage2(source, answers)
    except v3.v2.TwoPassV2Error as exc:
        stage2_error = str(exc)
    if stage2_error != error:
        fail("A2: stage2 did not reject at bindings with the same error")

    return {
        "handle": handle,
        "stage1_wire_valid": True,
        "bindings_error": error,
        "stage2_error": stage2_error,
    }


def unknown_handle_witness() -> None:
    source = v3.v2.synthetic_source(
        ["Synthetic evidence unit A.", "Synthetic evidence unit B."],
        bundle_id="B9258",
    )
    questions = v3.stage1(source)
    answers = default_stage1_answers(source)
    answers["n1__seed"] = "s999::condition"
    answers["n2__seed"] = "NONE"
    answers["n3__seed"] = "NONE"

    error = None
    try:
        v3.check_answers(questions, answers)
    except v3.v2.TwoPassV2Error as exc:
        error = str(exc)
    if error != "answer outside finite surface: n1__seed":
        fail(f"A5: unknown handle did not fail at finite-surface validation: {error!r}")

    bindings_error = None
    try:
        v3.bindings(source, answers)
    except v3.v2.TwoPassV2Error as exc:
        bindings_error = str(exc)
    if bindings_error != error:
        fail("A5: bindings did not fail first at finite-surface validation")


def audit_203_coverage_gap() -> None:
    text = (BASE / "scripts/paper2_extraction_two_pass_systemone_v3.py").read_text(
        encoding="utf-8"
    )
    required = (
        'checks["R3"] = "n1::n1" not in q2["r1__tuple"]["criteria"]',
        'same["n2__seed"] = "s1::response_or_outcome"',
        'collision_first["n1__seed"] = U',
    )
    for token in required:
        if token not in text:
            fail(f"A7: expected #203 witness missing: {token}")
    # The existing same-anchor test deliberately changes role, so it is not the
    # exact cross-slot duplicate full-handle witness established above.
    if 'same["n2__seed"] = "s1::state_or_structure"' in text:
        fail("A7: historical v3 self-test unexpectedly contains exact duplicate-handle probe")


def self_test() -> None:
    artifact = load_artifact()
    witness = duplicate_handle_witness()
    unknown_handle_witness()
    audit_203_coverage_gap()

    findings = artifact["findings"]
    expected = {
        "A1_exact_stage1_admissibility": "DEFECT_WITNESS",
        "A2_dependency_timing": "POST_RESPONSE_REJECTION",
        "A3_contract_consistency": "VIOLATES_DECLARED_AUDIT_CRITERION",
        "A4_bounded_210_linkage": "#210_DUPLICATE_HANDLE_FAILURES_REPRODUCE_CONFIRMED_INTERFACE_DEFECT",
        "A5_unknown_handle_branch": "WIRE_INVALID_UNDER_CANONICAL_FLOW",
        "A6_synthetic_destructive_witness": "REPRODUCED",
        "A7_203_coverage_gap": "MISSED_CROSS_SLOT_NODE_UNIQUENESS",
    }
    for key, result in expected.items():
        if findings.get(key, {}).get("result") != result:
            fail(f"{key}: artifact result drift")

    # Current v3 manifest explicitly says node handles are anchor::role and that
    # impossible finite choices should be pruned rather than semantically repaired.
    manifest = json.loads(
        (BASE / "research/paper2/extraction_two_pass_systemone_v3.json").read_text()
    )
    if manifest["bounded_surface"]["node_referent_handle"] != (
        "anchor_span_id::role; NONE is inactive; __unresolved__ is applicable but insufficiently distinguished"
    ):
        fail("A3: node handle semantics drift")
    if "prune impossible choices" not in manifest["bounded_surface"]["compiler_policy"]:
        fail("A3: impossible-choice pruning authority drift")

    print(f"A1=PASS common_handle={witness['handle']}")
    print("A2=PASS duplicate uniqueness enforced only after Stage-1 answer validation")
    print("A3=PASS declared finite-dependency criterion violated by duplicate seed tuple")
    print("A4=PASS #210 combined exception localized to duplicate branch under canonical wire flow")
    print("A5=PASS unknown handle cannot reach bindings as a wire-valid answer")
    print("A6=PASS source-free duplicate-handle failure reproduced")
    print("A7=PASS #203 R1-R17 missed exact cross-slot full-handle uniqueness")
    print(EXPECTED_STATUS)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if not args.self_test:
        p.error("only --self-test is supported")
    self_test()


if __name__ == "__main__":
    main()
