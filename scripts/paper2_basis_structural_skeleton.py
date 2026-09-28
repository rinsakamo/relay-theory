#!/usr/bin/env python3
"""Paper 2 #293: U_claim projection for Archetype reconstruction.

U_claim forgets concrete claim realization while retaining anonymous
basis-structural meaning.  It does not alter the frozen #225 Phi atlas.

Input:  paper2-phi-object-v1
Output: paper2-basis-structural-skeleton-v1
"""

from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from pathlib import Path
from typing import Any

from paper2_phi_compare import validate_phi_object

SKELETON_VERSION = "paper2-basis-structural-skeleton-v1"
PHI_VERSION = "paper2-phi-object-v1"
BASIS_VERSION = "paper2-working-basis-v1"
AXES = {"S", "Pi", "K", "O", "T", "C", "Q", "P"}
STRUCTURAL_EDGE_FAMILIES = {"basis_relation", "temporal_order"}
TEMPORAL_KEYS = ("time_index", "history_window", "future_horizon", "recurrence", "persistence")
CONTROL_KEYS = ("probe_P", "criterion_Q", "partition_Pi", "resource_C")
MAX_SEARCH_STATES = 100_000


class SkeletonError(ValueError):
    pass


def _canon(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def validate_skeleton(obj: dict[str, Any]) -> dict[str, Any]:
    required = {
        "schema_version", "source_phi_version", "basis_version",
        "active_axes", "nodes", "edges", "temporal", "controls",
    }
    if set(obj) != required:
        raise SkeletonError(f"skeleton keys differ: {sorted(set(obj) ^ required)}")
    if obj["schema_version"] != SKELETON_VERSION:
        raise SkeletonError("unexpected skeleton schema version")
    if obj["source_phi_version"] != PHI_VERSION:
        raise SkeletonError("unexpected source Phi version")
    if obj["basis_version"] != BASIS_VERSION:
        raise SkeletonError("unexpected basis version")

    axes = obj["active_axes"]
    if axes != sorted(set(axes)) or not set(axes) <= AXES:
        raise SkeletonError("active_axes must be sorted unique Paper 2 axes")

    if not isinstance(obj["nodes"], dict):
        raise SkeletonError("nodes must be an object")
    for node in obj["nodes"].values():
        if set(node) != {"space", "role", "required", "axis"}:
            raise SkeletonError("basis node keys mismatch")
        if node["space"] != "basis_coordinate":
            raise SkeletonError("skeleton contains non-basis node")
        if node["axis"] is not None and node["axis"] not in AXES:
            raise SkeletonError("unknown basis axis")

    node_ids = set(obj["nodes"])
    for edge in obj["edges"]:
        if set(edge) != {
            "family", "kind", "ordered_arguments", "arguments",
            "conditional_on", "temporal_direction",
        }:
            raise SkeletonError("edge keys mismatch")
        if edge["family"] not in STRUCTURAL_EDGE_FAMILIES:
            raise SkeletonError("non-structural edge family entered skeleton")
        if not edge["arguments"]:
            raise SkeletonError("edge arguments must not be empty")
        if not set(edge["arguments"] + edge["conditional_on"]) <= node_ids:
            raise SkeletonError("edge references non-basis node")

    if set(obj["temporal"]) != set(TEMPORAL_KEYS):
        raise SkeletonError("temporal keys mismatch")
    if set(obj["controls"]) != set(CONTROL_KEYS):
        raise SkeletonError("control keys mismatch")
    for value in obj["controls"].values():
        if set(value) != {"state"}:
            raise SkeletonError("control detail beyond structural state leaked")
    return obj


def project_basis_skeleton(phi: dict[str, Any]) -> dict[str, Any]:
    """Apply generic U_claim to one frozen Phi object."""
    validate_phi_object(phi)

    nodes = {
        node_id: {
            "space": "basis_coordinate",
            "role": node["role"],
            "required": bool(node["required"]),
            "axis": node.get("axis"),
        }
        for node_id, node in phi["nodes"].items()
        if node.get("space") == "basis_coordinate"
    }

    edges = []
    for edge in phi["edges"]:
        if edge["family"] not in STRUCTURAL_EDGE_FAMILIES:
            continue
        refs = edge["arguments"] + edge["conditional_on"]
        if not set(refs) <= set(nodes):
            raise SkeletonError(
                f"structural edge {edge['family']!r} references non-basis node"
            )
        edges.append({
            "family": edge["family"],
            "kind": edge["kind"],
            "ordered_arguments": edge["ordered_arguments"],
            "arguments": list(edge["arguments"]),
            "conditional_on": list(edge["conditional_on"]),
            "temporal_direction": edge["temporal_direction"],
        })

    result = {
        "schema_version": SKELETON_VERSION,
        "source_phi_version": PHI_VERSION,
        "basis_version": BASIS_VERSION,
        "active_axes": list(phi["active_axes"]),
        "nodes": nodes,
        "edges": edges,
        "temporal": copy.deepcopy(phi["temporal"]),
        "controls": {
            key: {"state": phi["controls"][key]["state"]}
            for key in CONTROL_KEYS
        },
    }
    return validate_skeleton(result)


def _node_label(node: dict[str, Any]) -> str:
    return _canon(node)


def _edge_under_mapping(edge: dict[str, Any], mapping: dict[str, str]) -> str:
    args = [mapping[x] for x in edge["arguments"]]
    if not edge["ordered_arguments"]:
        args = sorted(args)
    cond = sorted(mapping[x] for x in edge["conditional_on"])
    return _canon({
        "family": edge["family"],
        "kind": edge["kind"],
        "ordered_arguments": edge["ordered_arguments"],
        "arguments": args,
        "conditional_on": cond,
        "temporal_direction": edge["temporal_direction"],
    })


def skeleton_equivalent(a: dict[str, Any], b: dict[str, Any]) -> bool:
    """Exact basis-skeleton isomorphism modulo anonymous node identifiers."""
    validate_skeleton(a)
    validate_skeleton(b)

    for key in ("active_axes", "temporal", "controls"):
        if a[key] != b[key]:
            return False
    if len(a["nodes"]) != len(b["nodes"]) or len(a["edges"]) != len(b["edges"]):
        return False

    b_by_label: dict[str, list[str]] = {}
    for bid, bnode in b["nodes"].items():
        b_by_label.setdefault(_node_label(bnode), []).append(bid)

    candidates: dict[str, list[str]] = {}
    for aid, anode in a["nodes"].items():
        opts = list(b_by_label.get(_node_label(anode), []))
        if not opts:
            return False
        candidates[aid] = opts

    b_identity = {x: x for x in b["nodes"]}
    b_edges = Counter(_edge_under_mapping(e, b_identity) for e in b["edges"])
    order = sorted(a["nodes"], key=lambda x: (len(candidates[x]), _node_label(a["nodes"][x]), x))
    search_states = 0

    def partial_ok(mapping: dict[str, str]) -> bool:
        c: Counter[str] = Counter()
        for edge in a["edges"]:
            refs = edge["arguments"] + edge["conditional_on"]
            if all(ref in mapping for ref in refs):
                c[_edge_under_mapping(edge, mapping)] += 1
        return all(b_edges[k] >= v for k, v in c.items())

    def rec(i: int, mapping: dict[str, str], used: set[str]) -> bool:
        nonlocal search_states
        search_states += 1
        if search_states > MAX_SEARCH_STATES:
            raise SkeletonError("skeleton isomorphism search limit exceeded")
        if i == len(order):
            mapped = Counter(_edge_under_mapping(e, mapping) for e in a["edges"])
            return mapped == b_edges

        aid = order[i]
        for bid in sorted(candidates[aid]):
            if bid in used:
                continue
            mapping[aid] = bid
            used.add(bid)
            if partial_ok(mapping) and rec(i + 1, mapping, used):
                return True
            used.remove(bid)
            del mapping[aid]
        return False

    return rec(0, {}, set())


def _base_fixture() -> dict[str, Any]:
    return {
        "schema_version": PHI_VERSION,
        "basis_version": BASIS_VERSION,
        "claim_type": "comparison",
        "modality": "comparative",
        "scope_shape": {
            "conditions": True,
            "population": True,
            "substrate": False,
            "task": True,
            "temporal_scope": True,
        },
        "active_axes": ["K", "O", "P", "S", "T"],
        "nodes": {
            "claim_node:probe": {
                "space": "claim_ir_node",
                "role": "probe",
                "grounding": "explicit",
            },
            "claim_node:outcome": {
                "space": "claim_ir_node",
                "role": "response_or_outcome",
                "grounding": "explicit",
            },
            "claim_relation:r": {
                "space": "claim_ir_relation",
                "kind": "maps_to",
                "grounding": "normalized",
            },
            "basis:p": {
                "space": "basis_coordinate",
                "role": "probe",
                "required": True,
                "provenance_origin": "claim_ir_node",
                "axis": "P",
            },
            "basis:o": {
                "space": "basis_coordinate",
                "role": "response_or_outcome",
                "required": True,
                "provenance_origin": "claim_ir_node",
                "axis": "O",
            },
        },
        "edges": [
            {
                "family": "claim_ir_relation",
                "kind": "maps_to",
                "ordered_arguments": True,
                "arguments": ["claim_node:probe", "claim_node:outcome"],
                "conditional_on": [],
                "temporal_direction": "unspecified",
                "grounding": "normalized",
            },
            {
                "family": "coordinate_grounding",
                "kind": "claim_ir_node",
                "ordered_arguments": True,
                "arguments": ["basis:p", "claim_node:probe"],
                "conditional_on": [],
                "temporal_direction": "atemporal",
                "grounding": "claim_ir_node",
            },
            {
                "family": "coordinate_grounding",
                "kind": "claim_ir_node",
                "ordered_arguments": True,
                "arguments": ["basis:o", "claim_node:outcome"],
                "conditional_on": [],
                "temporal_direction": "atemporal",
                "grounding": "claim_ir_node",
            },
            {
                "family": "basis_relation",
                "kind": "maps_to",
                "ordered_arguments": True,
                "arguments": ["basis:p", "basis:o"],
                "conditional_on": [],
                "temporal_direction": "unspecified",
                "grounding": "normalized",
            },
            {
                "family": "temporal_order",
                "kind": "precedes",
                "ordered_arguments": True,
                "arguments": ["basis:p", "basis:o"],
                "conditional_on": [],
                "temporal_direction": "forward",
                "grounding": "structural_signature",
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
            "probe_P": {"state": "present", "provenance_kind": "source_declared"},
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


def _rename_basis_ids(phi: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(phi)
    mapping = {"basis:p": "basis:x", "basis:o": "basis:y"}
    renamed_nodes = {}
    for key, value in out["nodes"].items():
        renamed_nodes[mapping.get(key, key)] = value
    out["nodes"] = renamed_nodes
    for edge in out["edges"]:
        edge["arguments"] = [mapping.get(x, x) for x in edge["arguments"]]
        edge["conditional_on"] = [mapping.get(x, x) for x in edge["conditional_on"]]
    return out


def self_test() -> None:
    base = _base_fixture()
    validate_phi_object(base)
    s0 = project_basis_skeleton(base)

    # U1: paper-specific claim envelope / provenance / approximation disappears.
    variant = copy.deepcopy(base)
    variant["claim_type"] = "effect"
    variant["modality"] = "asserted"
    variant["scope_shape"] = {
        "conditions": False,
        "population": False,
        "substrate": True,
        "task": False,
        "temporal_scope": False,
    }
    variant["controls"]["probe_P"]["provenance_kind"] = "experimental_contract"
    variant["approximation"]["mode"] = "stochastic"
    variant["bridges"] = ["some-claim-specific-audit-bridge"]
    variant["nodes"]["claim_node:probe"]["grounding"] = "normalized"
    assert skeleton_equivalent(s0, project_basis_skeleton(variant))

    # U2: basis topology remains discriminating.
    topo = copy.deepcopy(base)
    topo["edges"][3]["arguments"] = ["basis:o", "basis:p"]
    assert not skeleton_equivalent(s0, project_basis_skeleton(topo))

    # U3: basis control state remains discriminating.
    criterion = copy.deepcopy(base)
    criterion["controls"]["criterion_Q"] = {
        "state": "present",
        "provenance_kind": "source_declared",
    }
    criterion["active_axes"] = sorted(set(criterion["active_axes"]) | {"Q"})
    assert not skeleton_equivalent(s0, project_basis_skeleton(criterion))

    # U4: temporal basis meaning remains discriminating.
    temporal = copy.deepcopy(base)
    temporal["temporal"]["persistence"] = {"state": "not_required"}
    assert not skeleton_equivalent(s0, project_basis_skeleton(temporal))

    # U5: anonymous basis IDs are presentation only.
    renamed = _rename_basis_ids(base)
    assert skeleton_equivalent(s0, project_basis_skeleton(renamed))

    # U6: same 8-axis inventory is insufficient when topology differs.
    same_axes_diff_topology = copy.deepcopy(base)
    same_axes_diff_topology["edges"][3]["kind"] = "depends_on"
    assert same_axes_diff_topology["active_axes"] == base["active_axes"]
    assert not skeleton_equivalent(
        s0, project_basis_skeleton(same_axes_diff_topology)
    )

    # U7: no ClaimIR wrapper or audit edge survives.
    assert all(n["space"] == "basis_coordinate" for n in s0["nodes"].values())
    assert all(e["family"] in STRUCTURAL_EDGE_FAMILIES for e in s0["edges"])

    print("PAPER2_BASIS_STRUCTURAL_SKELETON_V1_SELFTEST_PASS")


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

    phi = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(
        project_basis_skeleton(phi),
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
    ))


if __name__ == "__main__":
    main()
