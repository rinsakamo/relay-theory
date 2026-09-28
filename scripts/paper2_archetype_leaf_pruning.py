#!/usr/bin/env python3
"""Paper 2 #293 leaf-pruning projection for Archetype reconstruction.

Stage 1 only.

This projection removes representation/provenance/audit-only detail from a
frozen paper2-phi-object-v1 while preserving the scientific structural surface
that #283 may later weaken through separately qualified forgetting operators.

Owner: #293. Parent: #283.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from paper2_phi_compare import compare_phi, validate_phi_object

NORMALIZED = "paper2-archetype-leaf-pruned-v1"
AUDIT_EDGE_FAMILIES = {"coordinate_grounding"}
AUDIT_WRAPPER_SPACES = {"claim_ir_relation", "basis_coordinate"}
ALWAYS_RETAIN_SPACES = {"claim_ir_node"}


class LeafPruningError(ValueError):
    pass


def _prune_node(node: dict[str, Any]) -> dict[str, Any]:
    space = node.get("space")
    if space == "claim_ir_node":
        return {
            "space": space,
            "role": node.get("role"),
        }
    if space == "claim_ir_relation":
        return {
            "space": space,
            "kind": node.get("kind"),
        }
    if space == "basis_coordinate":
        return {
            "space": space,
            "role": node.get("role"),
            "required": node.get("required"),
            "axis": node.get("axis"),
        }
    raise LeafPruningError(f"unsupported node space {space!r}")


def _prune_edge(edge: dict[str, Any]) -> dict[str, Any]:
    return {
        "family": edge["family"],
        "kind": edge["kind"],
        "ordered_arguments": edge["ordered_arguments"],
        "arguments": list(edge["arguments"]),
        "conditional_on": list(edge["conditional_on"]),
        "temporal_direction": edge["temporal_direction"],
        "grounding": NORMALIZED,
    }


def _prune_control(value: dict[str, Any]) -> dict[str, Any]:
    return {"state": value["state"]}


def leaf_prune_phi(obj: dict[str, Any]) -> dict[str, Any]:
    """Return a valid Phi v1 image with audit-only detail normalized away."""
    validate_phi_object(obj)
    out = copy.deepcopy(obj)

    # Stage 1 does NOT forget claim envelope, scope, temporal state,
    # approximation, bridges, axes, or scientific topology.
    out["edges"] = [
        _prune_edge(edge)
        for edge in obj["edges"]
        if edge["family"] not in AUDIT_EDGE_FAMILIES
    ]

    referenced: set[str] = set()
    for edge in out["edges"]:
        referenced.update(edge["arguments"])
        referenced.update(edge["conditional_on"])

    nodes: dict[str, dict[str, Any]] = {}
    for node_id, node in obj["nodes"].items():
        space = node.get("space")
        if (
            space in AUDIT_WRAPPER_SPACES
            and node_id not in referenced
            and space not in ALWAYS_RETAIN_SPACES
        ):
            continue
        nodes[node_id] = _prune_node(node)
    out["nodes"] = nodes

    out["controls"] = {
        key: _prune_control(value)
        for key, value in obj["controls"].items()
    }

    return validate_phi_object(out)


def _base_fixture() -> dict[str, Any]:
    return {
        "schema_version": "paper2-phi-object-v1",
        "basis_version": "paper2-working-basis-v1",
        "claim_type": "effect",
        "modality": "asserted",
        "scope_shape": {
            "conditions": True,
            "population": True,
            "substrate": False,
            "task": True,
            "temporal_scope": True,
        },
        "active_axes": ["K", "O", "P", "S", "T"],
        "nodes": {
            "claim_node:s": {
                "space": "claim_ir_node",
                "role": "state_or_structure",
                "grounding": "explicit",
            },
            "claim_node:p": {
                "space": "claim_ir_node",
                "role": "probe",
                "grounding": "normalized",
            },
            "claim_node:o": {
                "space": "claim_ir_node",
                "role": "response_or_outcome",
                "grounding": "explicit",
            },
            "claim_relation:r": {
                "space": "claim_ir_relation",
                "kind": "maps_to",
                "grounding": "normalized",
            },
            "basis:s": {
                "space": "basis_coordinate",
                "role": "state_or_structure",
                "required": True,
                "provenance_origin": "claim_ir_node",
                "axis": "S",
            },
        },
        "edges": [
            {
                "family": "claim_ir_relation",
                "kind": "maps_to",
                "ordered_arguments": True,
                "arguments": ["claim_node:p", "claim_node:o"],
                "conditional_on": ["claim_node:s"],
                "temporal_direction": "forward",
                "grounding": "normalized",
            },
            {
                "family": "coordinate_grounding",
                "kind": "claim_ir_node",
                "ordered_arguments": True,
                "arguments": ["basis:s", "claim_node:s"],
                "conditional_on": [],
                "temporal_direction": "atemporal",
                "grounding": "claim_ir_node",
            },
        ],
        "temporal": {
            "time_index": {"state": "present"},
            "history_window": {"state": "not_required"},
            "future_horizon": {"state": "present"},
            "recurrence": {"state": "not_required"},
            "persistence": {"state": "present"},
        },
        "controls": {
            "probe_P": {
                "state": "present",
                "provenance_kind": "source_declared",
            },
            "criterion_Q": {"state": "not_required"},
            "partition_Pi": {"state": "not_required"},
            "resource_C": {"state": "not_required"},
        },
        "approximation": {
            "mode": "deterministic",
            "threshold": {"state": "not_required"},
            "tolerance": {"state": "not_required"},
            "confidence": {"state": "not_applicable"},
            "loss": {"state": "not_required"},
            "comparison_criterion": {"state": "not_required"},
        },
        "bridges": [],
    }


def _rename_nodes(obj: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(obj)
    mapping = {
        "claim_node:s": "claim_node:x",
        "claim_node:p": "claim_node:y",
        "claim_node:o": "claim_node:z",
        "claim_relation:r": "claim_relation:q",
        "basis:s": "basis:t",
    }
    out["nodes"] = {mapping[k]: v for k, v in out["nodes"].items()}
    for edge in out["edges"]:
        edge["arguments"] = [mapping[x] for x in edge["arguments"]]
        edge["conditional_on"] = [mapping[x] for x in edge["conditional_on"]]
    return out


def self_test() -> None:
    base = _base_fixture()
    validate_phi_object(base)

    # L1: audit/provenance-only differences disappear.
    audit_variant = copy.deepcopy(base)
    audit_variant["nodes"]["claim_node:s"]["grounding"] = "normalized"
    audit_variant["nodes"]["basis:s"]["provenance_origin"] = "formal_contract"
    audit_variant["controls"]["probe_P"]["provenance_kind"] = "experimental_contract"
    audit_variant["edges"][0]["grounding"] = "explicit"
    p0 = leaf_prune_phi(base)
    p1 = leaf_prune_phi(audit_variant)
    assert compare_phi(p0, p1)["relation"] == "EQUIVALENT"
    assert all(edge["family"] != "coordinate_grounding" for edge in p0["edges"])
    assert "basis:s" not in p0["nodes"]
    assert "claim_relation:r" not in p0["nodes"]

    # L2: temporal scientific differences are not leaf-pruned.
    delayed = copy.deepcopy(base)
    delayed["temporal"]["persistence"] = {"state": "not_required"}
    delayed["active_axes"] = ["K", "O", "P", "S", "T"]
    assert compare_phi(
        leaf_prune_phi(base), leaf_prune_phi(delayed)
    )["relation"] != "EQUIVALENT"

    # L3: target/topology differences survive pruning.
    target_variant = copy.deepcopy(base)
    target_variant["edges"][0]["arguments"] = ["claim_node:p", "claim_node:s"]
    assert compare_phi(
        leaf_prune_phi(base), leaf_prune_phi(target_variant)
    )["relation"] != "EQUIVALENT"

    # L4: pruning is idempotent.
    twice = leaf_prune_phi(leaf_prune_phi(base))
    assert twice == leaf_prune_phi(base)

    # L5: presentation renaming remains structurally equivalent.
    renamed = _rename_nodes(base)
    assert compare_phi(
        leaf_prune_phi(base), leaf_prune_phi(renamed)
    )["relation"] == "EQUIVALENT"

    # Boundary: Stage 1 preserves claim envelope / approximation.
    envelope = copy.deepcopy(base)
    envelope["claim_type"] = "comparison"
    assert compare_phi(
        leaf_prune_phi(base), leaf_prune_phi(envelope)
    )["relation"] != "EQUIVALENT"

    approx = copy.deepcopy(base)
    approx["approximation"]["mode"] = "stochastic"
    assert compare_phi(
        leaf_prune_phi(base), leaf_prune_phi(approx)
    )["relation"] != "EQUIVALENT"

    print("PAPER2_ARCHETYPE_LEAF_PRUNING_V1_SELFTEST_PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    if not args.input:
        parser.error("--input is required unless --self-test is used")
    obj = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(
        leaf_prune_phi(obj),
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
    ))


if __name__ == "__main__":
    main()
