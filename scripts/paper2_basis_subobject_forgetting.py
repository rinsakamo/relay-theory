#!/usr/bin/env python3
"""Paper 2 #293: admissible basis-subobject forgetting.

F_R restricts a paper2-basis-structural-skeleton-v1 to an explicitly
witnessed basis subobject.  It may delete structure but may not rewrite,
rewire, strengthen, or invent retained structure.

This is the Stage-2 grammar for #283 Archetype common-image search.
"""

from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from pathlib import Path
from typing import Any

from paper2_basis_structural_skeleton import (
    CONTROL_KEYS,
    SKELETON_VERSION,
    TEMPORAL_KEYS,
    SkeletonError,
    skeleton_equivalent,
    validate_skeleton,
)

IMAGE_VERSION = "paper2-basis-subobject-v1"
CONTROL_AXIS = {
    "probe_P": "P",
    "criterion_Q": "Q",
    "partition_Pi": "Pi",
    "resource_C": "C",
}


def _canon(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def validate_image(obj: dict[str, Any]) -> dict[str, Any]:
    required = {
        "schema_version", "source_skeleton_version", "basis_version",
        "nodes", "edges", "temporal", "controls", "active_axes",
    }
    if set(obj) != required:
        raise SkeletonError(f"subobject keys differ: {sorted(set(obj) ^ required)}")
    if obj["schema_version"] != IMAGE_VERSION:
        raise SkeletonError("unexpected subobject schema version")
    if obj["source_skeleton_version"] != SKELETON_VERSION:
        raise SkeletonError("unexpected source skeleton version")
    if not isinstance(obj["nodes"], dict):
        raise SkeletonError("nodes must be object")
    node_ids = set(obj["nodes"])
    for node in obj["nodes"].values():
        if set(node) != {"space", "role", "required", "axis"}:
            raise SkeletonError("node keys mismatch")
        if node["space"] != "basis_coordinate":
            raise SkeletonError("non-basis node in subobject")
    if not isinstance(obj["edges"], list):
        raise SkeletonError("edges must be array")
    for edge in obj["edges"]:
        if set(edge) != {
            "family", "kind", "ordered_arguments", "arguments",
            "conditional_on", "temporal_direction",
        }:
            raise SkeletonError("edge keys mismatch")
        if not set(edge["arguments"] + edge["conditional_on"]) <= node_ids:
            raise SkeletonError("edge references forgotten node")
    if not set(obj["temporal"]) <= set(TEMPORAL_KEYS):
        raise SkeletonError("unknown temporal key")
    if not set(obj["controls"]) <= set(CONTROL_KEYS):
        raise SkeletonError("unknown control key")
    return obj


def _derived_axes(
    nodes: dict[str, dict[str, Any]],
    edges: list[dict[str, Any]],
    temporal: dict[str, Any],
    controls: dict[str, Any],
) -> list[str]:
    axes = {node["axis"] for node in nodes.values() if node.get("axis")}
    if edges:
        axes.add("K")
    if temporal or any(e["family"] == "temporal_order" for e in edges):
        axes.add("T")
    for key, value in controls.items():
        if value["state"] == "present":
            axes.add(CONTROL_AXIS[key])
    return sorted(axes)


def restrict_skeleton(
    skeleton: dict[str, Any],
    *,
    retained_node_ids: list[str],
    retained_edge_indices: list[int],
    retained_temporal_keys: list[str],
    retained_control_keys: list[str],
) -> dict[str, Any]:
    """Apply one explicit F_R forgetting witness."""
    validate_skeleton(skeleton)

    node_ids = set(retained_node_ids)
    if len(node_ids) != len(retained_node_ids):
        raise SkeletonError("duplicate retained node id")
    if not node_ids <= set(skeleton["nodes"]):
        raise SkeletonError("retained_node_ids contains unknown node")

    edge_indices = set(retained_edge_indices)
    if len(edge_indices) != len(retained_edge_indices):
        raise SkeletonError("duplicate retained edge index")
    if any(i < 0 or i >= len(skeleton["edges"]) for i in edge_indices):
        raise SkeletonError("retained_edge_indices contains unknown edge")

    temporal_keys = set(retained_temporal_keys)
    if len(temporal_keys) != len(retained_temporal_keys):
        raise SkeletonError("duplicate retained temporal key")
    if not temporal_keys <= set(TEMPORAL_KEYS):
        raise SkeletonError("unknown retained temporal key")

    control_keys = set(retained_control_keys)
    if len(control_keys) != len(retained_control_keys):
        raise SkeletonError("duplicate retained control key")
    if not control_keys <= set(CONTROL_KEYS):
        raise SkeletonError("unknown retained control key")

    nodes = {
        key: copy.deepcopy(value)
        for key, value in skeleton["nodes"].items()
        if key in node_ids
    }

    edges = []
    for i, edge in enumerate(skeleton["edges"]):
        if i not in edge_indices:
            continue
        refs = set(edge["arguments"] + edge["conditional_on"])
        if not refs <= node_ids:
            raise SkeletonError(
                "retained edge references forgotten node; forgetting witness is not closed"
            )
        edges.append(copy.deepcopy(edge))

    temporal = {
        key: copy.deepcopy(skeleton["temporal"][key])
        for key in TEMPORAL_KEYS
        if key in temporal_keys
    }
    controls = {
        key: copy.deepcopy(skeleton["controls"][key])
        for key in CONTROL_KEYS
        if key in control_keys
    }

    out = {
        "schema_version": IMAGE_VERSION,
        "source_skeleton_version": SKELETON_VERSION,
        "basis_version": skeleton["basis_version"],
        "nodes": nodes,
        "edges": edges,
        "temporal": temporal,
        "controls": controls,
        "active_axes": _derived_axes(nodes, edges, temporal, controls),
    }
    return validate_image(out)


def is_nontrivial(image: dict[str, Any]) -> bool:
    """Minimal anti-collapse predicate for synthetic qualification."""
    validate_image(image)
    # Generic State-like singletons and disconnected bags are not Archetypes.
    if image["edges"]:
        return len(image["nodes"]) >= 2
    # A single structural position with one retained typed basis feature can
    # still be informative enough to keep as a candidate for later pressure.
    typed_features = len(image["temporal"]) + len(image["controls"])
    return len(image["nodes"]) >= 1 and typed_features >= 1 and len(image["active_axes"]) >= 2


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


def image_equivalent(a: dict[str, Any], b: dict[str, Any]) -> bool:
    validate_image(a)
    validate_image(b)
    if a["active_axes"] != b["active_axes"]:
        return False
    if a["temporal"] != b["temporal"] or a["controls"] != b["controls"]:
        return False
    if len(a["nodes"]) != len(b["nodes"]) or len(a["edges"]) != len(b["edges"]):
        return False

    b_by_label: dict[str, list[str]] = {}
    for bid, node in b["nodes"].items():
        b_by_label.setdefault(_node_label(node), []).append(bid)
    candidates = {}
    for aid, node in a["nodes"].items():
        opts = b_by_label.get(_node_label(node), [])
        if not opts:
            return False
        candidates[aid] = list(opts)

    b_identity = {x: x for x in b["nodes"]}
    b_edges = Counter(_edge_under_mapping(e, b_identity) for e in b["edges"])
    order = sorted(a["nodes"], key=lambda x: (len(candidates[x]), _node_label(a["nodes"][x]), x))

    def rec(i: int, mapping: dict[str, str], used: set[str]) -> bool:
        if i == len(order):
            c = Counter(_edge_under_mapping(e, mapping) for e in a["edges"])
            return c == b_edges
        aid = order[i]
        for bid in sorted(candidates[aid]):
            if bid in used:
                continue
            mapping[aid] = bid
            used.add(bid)
            if rec(i + 1, mapping, used):
                return True
            used.remove(bid)
            del mapping[aid]
        return False

    return rec(0, {}, set())


def _fixture(extra_left: bool = False, extra_right: bool = False) -> dict[str, Any]:
    nodes = {
        "basis:s": {"space": "basis_coordinate", "role": "state_or_structure", "required": True, "axis": "S"},
        "basis:o": {"space": "basis_coordinate", "role": "response_or_outcome", "required": True, "axis": "O"},
    }
    edges = [{
        "family": "basis_relation",
        "kind": "depends_on",
        "ordered_arguments": True,
        "arguments": ["basis:o", "basis:s"],
        "conditional_on": [],
        "temporal_direction": "forward",
    }]
    controls = {
        "probe_P": {"state": "not_required"},
        "criterion_Q": {"state": "not_required"},
        "partition_Pi": {"state": "not_required"},
        "resource_C": {"state": "not_required"},
    }
    if extra_left:
        nodes["basis:p"] = {"space": "basis_coordinate", "role": "probe", "required": True, "axis": "P"}
        edges.append({
            "family": "basis_relation",
            "kind": "maps_to",
            "ordered_arguments": True,
            "arguments": ["basis:p", "basis:o"],
            "conditional_on": [],
            "temporal_direction": "unspecified",
        })
        controls["probe_P"] = {"state": "present"}
    if extra_right:
        nodes["basis:q"] = {"space": "basis_coordinate", "role": "criterion", "required": True, "axis": "Q"}
        edges.append({
            "family": "basis_relation",
            "kind": "satisfies",
            "ordered_arguments": True,
            "arguments": ["basis:o", "basis:q"],
            "conditional_on": [],
            "temporal_direction": "unspecified",
        })
        controls["criterion_Q"] = {"state": "present"}
    axes = {v["axis"] for v in nodes.values() if v["axis"]}
    if edges:
        axes.add("K")
    return {
        "schema_version": SKELETON_VERSION,
        "source_phi_version": "paper2-phi-object-v1",
        "basis_version": "paper2-working-basis-v1",
        "active_axes": sorted(axes | ({"P"} if extra_left else set()) | ({"Q"} if extra_right else set())),
        "nodes": nodes,
        "edges": edges,
        "temporal": {
            "time_index": {"state": "present"},
            "history_window": {"state": "not_required"},
            "future_horizon": {"state": "present"},
            "recurrence": {"state": "not_required"},
            "persistence": {"state": "present"},
        },
        "controls": controls,
    }


def self_test() -> None:
    left = _fixture(extra_left=True)
    right = _fixture(extra_right=True)
    validate_skeleton(left)
    validate_skeleton(right)
    assert not skeleton_equivalent(left, right)

    # F1: distinct richer skeletons can share an explicit common basis image.
    keep_temporal = ["time_index", "future_horizon", "persistence"]
    common_controls: list[str] = []
    a = restrict_skeleton(
        left,
        retained_node_ids=["basis:s", "basis:o"],
        retained_edge_indices=[0],
        retained_temporal_keys=keep_temporal,
        retained_control_keys=common_controls,
    )
    b = restrict_skeleton(
        right,
        retained_node_ids=["basis:s", "basis:o"],
        retained_edge_indices=[0],
        retained_temporal_keys=keep_temporal,
        retained_control_keys=common_controls,
    )
    assert image_equivalent(a, b)
    assert is_nontrivial(a)

    # F2: over-forgetting to one untyped node is rejected as trivial.
    trivial = restrict_skeleton(
        left,
        retained_node_ids=["basis:s"],
        retained_edge_indices=[],
        retained_temporal_keys=[],
        retained_control_keys=[],
    )
    assert not is_nontrivial(trivial)

    # F3: richer common image defeats a poorer candidate.
    poor = restrict_skeleton(
        left,
        retained_node_ids=["basis:s"],
        retained_edge_indices=[],
        retained_temporal_keys=["persistence"],
        retained_control_keys=[],
    )
    assert is_nontrivial(poor)
    assert len(a["nodes"]) > len(poor["nodes"]) and len(a["edges"]) > len(poor["edges"])

    # F4: forgetting witnesses may be incomparable; no scalar depth is implied.
    left_branch = restrict_skeleton(
        left,
        retained_node_ids=["basis:s", "basis:p"],
        retained_edge_indices=[],
        retained_temporal_keys=["persistence"],
        retained_control_keys=["probe_P"],
    )
    right_branch = restrict_skeleton(
        right,
        retained_node_ids=["basis:o", "basis:q"],
        retained_edge_indices=[1],
        retained_temporal_keys=[],
        retained_control_keys=["criterion_Q"],
    )
    assert is_nontrivial(left_branch)
    assert is_nontrivial(right_branch)
    assert not image_equivalent(left_branch, right_branch)

    # F5: composition is auditable. Restricting left to A through an
    # intermediate object preserves the same retained structure as direct F_R.
    mid = restrict_skeleton(
        left,
        retained_node_ids=["basis:s", "basis:o", "basis:p"],
        retained_edge_indices=[0, 1],
        retained_temporal_keys=keep_temporal,
        retained_control_keys=[],
    )
    # Lift mid into skeleton syntax solely for the second synthetic restriction.
    mid_skel = {
        "schema_version": SKELETON_VERSION,
        "source_phi_version": "paper2-phi-object-v1",
        "basis_version": mid["basis_version"],
        "active_axes": mid["active_axes"],
        "nodes": mid["nodes"],
        "edges": mid["edges"],
        "temporal": {
            key: mid["temporal"].get(key, {"state": "not_required"})
            for key in TEMPORAL_KEYS
        },
        "controls": {
            key: mid["controls"].get(key, {"state": "not_required"})
            for key in CONTROL_KEYS
        },
    }
    validate_skeleton(mid_skel)
    composed = restrict_skeleton(
        mid_skel,
        retained_node_ids=["basis:s", "basis:o"],
        retained_edge_indices=[0],
        retained_temporal_keys=keep_temporal,
        retained_control_keys=[],
    )
    assert image_equivalent(a, composed)

    # Closure: retaining an edge after forgetting one of its endpoints fails.
    try:
        restrict_skeleton(
            left,
            retained_node_ids=["basis:s"],
            retained_edge_indices=[0],
            retained_temporal_keys=[],
            retained_control_keys=[],
        )
    except SkeletonError:
        pass
    else:
        raise AssertionError("non-closed forgetting witness unexpectedly accepted")

    print("PAPER2_BASIS_SUBOBJECT_FORGETTING_V1_SELFTEST_PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    parser.error("only --self-test is qualified in v1")


if __name__ == "__main__":
    main()
