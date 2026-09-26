#!/usr/bin/env python3
"""Validate, self-test, canonicalize, and replay Paper 2 structural-signature v1.

Owner: #142. Infrastructure only; architecture consequence: NONE.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from paper2_claim_ir_validate import ValidationError as ClaimIRValidationError
from paper2_structural_signature_contract import (
    CLAIM_IR_VERSION, RESIDUAL_TAXONOMY_VERSION, ValidationError, validate,
)
from paper2_structural_signature_canonical import canonical_artifact_bytes, structural_digest
from paper2_structural_signature_constants import WORKING_BASIS_VERSION
from paper2_structural_signature_replay import replay_summary

def expect_invalid(data: dict[str, Any], label: str) -> None:
    try:
        validate(data)
    except (ValidationError, ClaimIRValidationError):
        return
    raise AssertionError(f"{label}: adversarial fixture unexpectedly validated")


def self_test(example_path: Path) -> None:
    base = json.loads(example_path.read_text(encoding="utf-8"))
    validate(base)
    claim = base["paper"]["claims"][0]
    ir = claim["claim_ir_records"][0]
    attempt = ir["decomposition_attempts"][0]
    assert attempt["outcome"]["status"] == "PASS"

    # P1 minimal valid PASS record.
    p1_digest = structural_digest(attempt, ir["claim_ir"])
    assert len(p1_digest) == 64

    # #226: the working measurement basis is an admitted version tuple, while
    # basis-version bookkeeping itself does not alter structural identity.
    p1_working = copy.deepcopy(base)
    p1w_ir = p1_working["paper"]["claims"][0]["claim_ir_records"][0]
    p1w_attempt = p1w_ir["decomposition_attempts"][0]
    p1_working["contract_versions"]["basis"] = WORKING_BASIS_VERSION
    validate(p1_working)
    assert structural_digest(p1w_attempt, p1w_ir["claim_ir"]) == p1_digest

    # P2 minimal valid RESIDUAL record with machine-readable localization.
    p2 = copy.deepcopy(base)
    p2_attempt = p2["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
    witness = p2_attempt["outcome"]["witness"]
    witness["verification"]["status"] = "failed"
    p2_attempt["outcome"] = {
        "status": "RESIDUAL",
        "residual": {
            "taxonomy_version": RESIDUAL_TAXONOMY_VERSION,
            "residual_kind": "witness_failure",
            "failure_layer": "witness",
            "unmet_obligations": ["synthetic witness obligation did not verify"],
            "details": "synthetic residual fixture",
        },
        "witness_attempts": [witness],
    }
    validate(p2)

    # P3 same basis-coordinate multiset, different relation topology => identity differs.
    p3 = copy.deepcopy(base)
    p3_attempt = p3["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
    p3_attempt["relation_topology"][0]["kind"] = "maps_to"
    validate(p3)
    assert structural_digest(p3_attempt, p3["paper"]["claims"][0]["claim_ir_records"][0]["claim_ir"]) != p1_digest

    # P4 explicit absence semantics are serially distinct.
    p4a = copy.deepcopy(base)
    p4b = copy.deepcopy(base)
    p4c = copy.deepcopy(base)
    for doc, state in ((p4a, "not_required"), (p4b, "unknown"), (p4c, "explicitly_absent")):
        doc["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]["control_surface"]["criterion_Q"] = {"state": state}
        validate(doc)
    assert len({canonical_artifact_bytes(p4a), canonical_artifact_bytes(p4b), canonical_artifact_bytes(p4c)}) == 3

    # N1 macro-only artifact.
    n1 = copy.deepcopy(base)
    n1_attempt = n1["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
    n1_attempt["basis_instantiation"]["coordinates"] = []
    n1_attempt["relation_topology"] = []
    expect_invalid(n1, "N1 macro-only")

    # N2 PASS without witness.
    n2 = copy.deepcopy(base)
    n2_attempt = n2["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
    del n2_attempt["outcome"]["witness"]
    expect_invalid(n2, "N2 PASS without witness")

    # N3 source-facing label leakage into blinded analysis surface.
    n3 = copy.deepcopy(base)
    n3_attempt = n3["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
    n3_attempt["analysis_identity"]["analysis_labels"] = ["working memory"]
    expect_invalid(n3, "N3 provenance leakage")

    # N4 opaque residual without failure localization.
    n4 = copy.deepcopy(p2)
    del n4["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]["outcome"]["residual"]["failure_layer"]
    expect_invalid(n4, "N4 residual without failure localization")

    # N5 malformed relation reference.
    n5 = copy.deepcopy(base)
    n5_attempt = n5["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
    n5_attempt["relation_topology"][0]["arguments"][0]["ref"] = "missing.coordinate"
    expect_invalid(n5, "N5 malformed relation reference")

    # N6 illegal null collapse.
    n6 = copy.deepcopy(base)
    n6["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]["control_surface"]["criterion_Q"] = None
    expect_invalid(n6, "N6 ambiguous null")

    # N7 unsupported version tuple.
    n7 = copy.deepcopy(base)
    n7["contract_versions"]["basis"] = "paper2-unknown-basis-v999"
    expect_invalid(n7, "N7 unsupported version")

    # P5 canonical structural identity survives key/list reorder and declared
    # presentation-only attempt/relation IDs, but preserves ordered relation args.
    p5 = copy.deepcopy(base)
    p5_ir = p5["paper"]["claims"][0]["claim_ir_records"][0]
    p5_attempt = p5_ir["decomposition_attempts"][0]
    p5_attempt["attempt_id"] = "presentation.changed"
    p5_attempt["relation_topology"][0]["relation_id"] = "presentation_relation_changed"
    p5_attempt["derived_macros"][0]["expansion"]["relation_ids"] = ["presentation_relation_changed"]
    p5_attempt["basis_instantiation"]["coordinates"].reverse()
    validate(p5)
    assert structural_digest(p5_attempt, p5_ir["claim_ir"]) == p1_digest

    p5_ordered = copy.deepcopy(base)
    p5o_ir = p5_ordered["paper"]["claims"][0]["claim_ir_records"][0]
    p5o_attempt = p5o_ir["decomposition_attempts"][0]
    p5o_attempt["relation_topology"][0]["arguments"].reverse()
    validate(p5_ordered)
    assert structural_digest(p5o_attempt, p5o_ir["claim_ir"]) != p1_digest

    # H4 macro witness reference must resolve to the recorded outcome witness.
    n8 = copy.deepcopy(base)
    n8_attempt = n8["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
    n8_attempt["derived_macros"][0]["expansion"]["witness_schema_id"] = "fixture:unrecorded-witness:v1"
    expect_invalid(n8, "H4 untraceable macro witness")

    # P5b ClaimIR node/relation IDs are presentation tokens under #147 semantics.
    p5_rename = copy.deepcopy(base)
    p5r_ir = p5_rename["paper"]["claims"][0]["claim_ir_records"][0]
    p5r_claim_ir = p5r_ir["claim_ir"]
    p5r_attempt = p5r_ir["decomposition_attempts"][0]
    node_renames = {"earlier_information": "node_a", "later_response": "node_b"}
    for node in p5r_claim_ir["claim_core"]["nodes"]:
        node["id"] = node_renames[node["id"]]
    p5r_claim_ir["claim_core"]["relations"][0]["id"] = "relation_a"
    p5r_claim_ir["claim_core"]["relations"][0]["arguments"] = [
        node_renames[arg] for arg in p5r_claim_ir["claim_core"]["relations"][0]["arguments"]
    ]
    for coord in p5r_attempt["basis_instantiation"]["coordinates"]:
        if coord["provenance"]["origin"] == "claim_ir_node":
            coord["provenance"]["ref"] = node_renames[coord["provenance"]["ref"]]
    validate(p5_rename)
    assert structural_digest(p5r_attempt, p5r_claim_ir) == p1_digest

    # Replay requirement.
    replay = replay_summary(base)
    row = replay["rows"][0]
    assert row["claim_ir_version"] == CLAIM_IR_VERSION
    assert {c["coordinate_id"] for c in row["basis_expansion"]} == {
        c["coordinate_id"] for c in attempt["basis_instantiation"]["coordinates"]
    }
    assert row["relation_graph"] == attempt["relation_topology"]
    assert tuple(row["control_surface"][key]["state"] for key in (
        "probe_P", "criterion_Q", "partition_Pi", "resource_C"
    )) == ("present", "present", "not_required", "not_required")
    assert row["temporal_structure"] == attempt["temporal_structure"]
    assert row["bridge_assumptions"] == attempt["bridge_assumptions"]
    assert row["outcome"] == "PASS"
    assert row["failure_localization"] == {"state": "not_applicable"}
    assert row["witnesses"][0]["generic_schema_id"] == attempt["outcome"]["witness"]["generic_schema_id"]
    assert row["witnesses"][0]["verification"] == attempt["outcome"]["witness"]["verification"]

    artifact_digest = hashlib.sha256(canonical_artifact_bytes(base)).hexdigest()
    print(
        "PAPER2_STRUCTURAL_SIGNATURE_V1_SELFTEST_PASS "
        f"structural_sha256={p1_digest} artifact_sha256={artifact_digest}"
    )
