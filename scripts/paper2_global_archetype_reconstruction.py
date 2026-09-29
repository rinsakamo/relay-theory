#!/usr/bin/env python3
"""Paper 2 #315: global Archetype reconstruction.

Inputs are independently frozen lane-local Archetype reports only.
Candidate generation is NOT rerun jointly across lanes.

For each frozen lane-local candidate:
- recover the exact F_R image from a frozen structural object or membership
  witness;
- MEM candidates are recovered by exact frozen archetype_id from the frozen
  reference-pilot pair enumeration;
- verify recovered image_id;
- merge exact/isomorphic images by canonical archetype_id;
- compute strict basis-subobject relations among unique global objects;
- compute a transitive reduction when the strict relation is acyclic;
- derive cross-lane support by refinement composition.

Owner: #315. Parent: #283.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

from paper2_reference_structural_adjudication import compile_record
from paper2_phi_compare import project_first
from paper2_basis_structural_skeleton import project_basis_skeleton
from paper2_basis_subobject_forgetting import (
    image_equivalent,
    restrict_skeleton,
    validate_image,
)
from paper2_archetype_mem_pilot import (
    canonical_image_key,
    image_embeds_in_image,
    image_id,
    pair_common_candidates,
)

CLAIM_DIR = Path("research/paper2/chatgpt_reference_claimir_v1")
ADJ_DIR = Path("research/paper2/reference_structural_adjudication_v1")

LANE_REPORTS = {
    "MEM": Path("research/paper2/mem_archetype_pilot_v1.json"),
    "ATT": Path("research/paper2/att_archetype_lane_v1.json"),
    "CTL": Path("research/paper2/ctl_archetype_lane_v1.json"),
    "CNC": Path("research/paper2/cnc_archetype_lane_v1.json"),
    "BLF": Path("research/paper2/blf_archetype_reconstruction_v1.json"),
    "LRN": Path("research/paper2/lrn_archetype_reconstruction_v1.json"),
    "PRD": Path("research/paper2/prd_archetype_lane_v1.json"),
    "SKL": Path("research/paper2/skl_archetype_reconstruction_v1.json"),
    "CHA": Path("research/paper2/challenge_a_archetype_v1.json"),
    "CHB": Path("research/paper2/challenge_b_archetype_lane_v1.json"),
}

DIRECT_WITNESS_KEYS = (
    "membership_witnesses",
    "membership_forgetting_witnesses",
    "forgetting_witnesses",
    "member_forgetting_witnesses",
)

FULL_OBJECT_KEYS = (
    "archetype_structural_object",
    "structural_image",
    "retained_basis_subobject",
)


class GlobalArchetypeError(ValueError):
    pass


def _canon(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _claim_skeleton(claim_id: str, cache: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if claim_id in cache:
        return cache[claim_id]
    claim_path = CLAIM_DIR / f"{claim_id}.json"
    adj_path = ADJ_DIR / f"{claim_id}.json"
    if not claim_path.exists() or not adj_path.exists():
        raise GlobalArchetypeError(f"missing frozen input for {claim_id}")
    claim = _load_json(claim_path)
    adjudication = _load_json(adj_path)
    record = compile_record(claim, adjudication)
    phi = project_first(record)
    skeleton = project_basis_skeleton(phi)
    cache[claim_id] = skeleton
    return skeleton


def _normalize_explicit_object(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize report-embedded candidate objects to basis-subobject-v1."""
    if raw.get("schema_version") == "paper2-basis-subobject-v1":
        out = copy.deepcopy(raw)
        validate_image(out)
        return out
    raise GlobalArchetypeError(
        f"unsupported explicit candidate object schema {raw.get('schema_version')!r}"
    )


def _witness_map(candidate: dict[str, Any]) -> dict[str, dict[str, Any]] | None:
    for key in DIRECT_WITNESS_KEYS:
        value = candidate.get(key)
        if isinstance(value, dict) and value:
            return value
    return None


def _image_from_witness(
    claim_id: str,
    witness: dict[str, Any],
    skeleton_cache: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    needed = {
        "retained_node_ids",
        "retained_edge_indices",
        "retained_temporal_keys",
        "retained_control_keys",
    }
    if not needed <= set(witness):
        raise GlobalArchetypeError(
            f"{claim_id}: witness missing {sorted(needed - set(witness))}"
        )
    skeleton = _claim_skeleton(claim_id, skeleton_cache)
    return restrict_skeleton(
        skeleton,
        retained_node_ids=list(witness["retained_node_ids"]),
        retained_edge_indices=list(witness["retained_edge_indices"]),
        retained_temporal_keys=list(witness["retained_temporal_keys"]),
        retained_control_keys=list(witness["retained_control_keys"]),
    )


def _recover_mem_candidate(
    candidate: dict[str, Any],
    skeleton_cache: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    target = candidate["archetype_id"]
    members = list(candidate["member_claim_ids"])
    for left_id, right_id in itertools.combinations(members, 2):
        left = _claim_skeleton(left_id, skeleton_cache)
        right = _claim_skeleton(right_id, skeleton_cache)
        for payload in pair_common_candidates(left, right).values():
            image = payload["image"]
            if image_id(image) == target:
                return image
    raise GlobalArchetypeError(f"MEM candidate {target}: exact image not recovered")


def _recover_candidate(
    lane: str,
    candidate: dict[str, Any],
    skeleton_cache: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], str]:
    target = candidate["archetype_id"]

    for key in FULL_OBJECT_KEYS:
        raw = candidate.get(key)
        if isinstance(raw, dict) and raw:
            try:
                image = _normalize_explicit_object(raw)
            except Exception:
                continue
            if image_id(image) == target:
                return image, f"report:{key}"

    # CHB stores the same structural content under decomposed retained_* fields.
    if (
        isinstance(candidate.get("retained_nodes"), dict)
        and isinstance(candidate.get("retained_edges"), list)
    ):
        temporal_keys = list(candidate.get("retained_temporal_features", []))
        temporal = {key: {"state": "present"} for key in temporal_keys}
        controls = copy.deepcopy(candidate.get("retained_controls", {}))
        image = {
            "schema_version": "paper2-basis-subobject-v1",
            "source_skeleton_version": "paper2-basis-structural-skeleton-v1",
            "basis_version": "paper2-working-basis-v1",
            "nodes": copy.deepcopy(candidate["retained_nodes"]),
            "edges": copy.deepcopy(candidate["retained_edges"]),
            "temporal": temporal,
            "controls": controls,
            "active_axes": list(candidate["active_axes"]),
        }
        try:
            validate_image(image)
        except Exception:
            pass
        else:
            if image_id(image) == target:
                return image, "report:retained_*"

    witnesses = _witness_map(candidate)
    if witnesses:
        errors = []
        for claim_id in sorted(witnesses):
            witness = witnesses[claim_id]
            try:
                image = _image_from_witness(claim_id, witness, skeleton_cache)
            except Exception as exc:
                errors.append(f"{claim_id}:{exc}")
                continue
            if image_id(image) == target:
                return image, f"witness:{claim_id}"
        raise GlobalArchetypeError(
            f"{lane} candidate {target}: no direct witness reproduced ID; "
            + "; ".join(errors[:3])
        )

    if lane == "MEM":
        return _recover_mem_candidate(candidate, skeleton_cache), "mem:frozen-id-recovery"

    raise GlobalArchetypeError(f"{lane} candidate {target}: no recovery route")


def _canonicalize_image(image: dict[str, Any]) -> dict[str, Any]:
    """Return an actual canonical image object, not only its canonical string key."""
    validate_image(image)

    # Reuse the canonical key as the identity authority, then search node
    # permutations for the lexicographically minimal actual object.
    target_key = canonical_image_key(image)

    by_label: dict[str, list[str]] = {}
    for node_id, node in image["nodes"].items():
        by_label.setdefault(_canon(node), []).append(node_id)

    label_groups = sorted(by_label)
    slots: dict[str, list[str]] = {}
    offset = 0
    for label in label_groups:
        size = len(by_label[label])
        slots[label] = [f"n{i}" for i in range(offset, offset + size)]
        offset += size

    group_maps = []
    for label in label_groups:
        ids = sorted(by_label[label])
        group_maps.append([
            dict(zip(ids, perm))
            for perm in itertools.permutations(slots[label])
        ])

    best_key = None
    best_obj = None
    for pieces in itertools.product(*group_maps):
        mapping: dict[str, str] = {}
        for piece in pieces:
            mapping.update(piece)

        nodes = {
            mapping[node_id]: copy.deepcopy(image["nodes"][node_id])
            for node_id in image["nodes"]
        }
        edges = []
        for edge in image["edges"]:
            args = [mapping[x] for x in edge["arguments"]]
            if not edge["ordered_arguments"]:
                args = sorted(args)
            edges.append({
                "family": edge["family"],
                "kind": edge["kind"],
                "ordered_arguments": edge["ordered_arguments"],
                "arguments": args,
                "conditional_on": sorted(mapping[x] for x in edge["conditional_on"]),
                "temporal_direction": edge["temporal_direction"],
            })
        edges.sort(key=_canon)

        obj = {
            "schema_version": "paper2-basis-subobject-v1",
            "source_skeleton_version": "paper2-basis-structural-skeleton-v1",
            "basis_version": image["basis_version"],
            "nodes": dict(sorted(nodes.items())),
            "edges": edges,
            "temporal": copy.deepcopy(image["temporal"]),
            "controls": copy.deepcopy(image["controls"]),
            "active_axes": list(image["active_axes"]),
        }
        key = _canon({
            "active_axes": obj["active_axes"],
            "nodes": obj["nodes"],
            "edges": [_canon(e) for e in obj["edges"]],
            "temporal": obj["temporal"],
            "controls": obj["controls"],
        })
        if best_key is None or key < best_key:
            best_key = key
            best_obj = obj

    if best_obj is None:
        raise GlobalArchetypeError("empty candidate image cannot be canonicalized")
    if best_key != target_key:
        raise GlobalArchetypeError("canonicalization disagrees with frozen image key")
    validate_image(best_obj)
    return best_obj


def _summary(image: dict[str, Any]) -> dict[str, Any]:
    return {
        "active_axes": list(image["active_axes"]),
        "node_count": len(image["nodes"]),
        "edge_count": len(image["edges"]),
        "temporal_features": sorted(image["temporal"]),
        "control_features": sorted(image["controls"]),
    }


def _strict_relation(
    left: dict[str, Any],
    right: dict[str, Any],
) -> str:
    lr = image_embeds_in_image(left, right)
    rl = image_embeds_in_image(right, left)
    if lr and rl:
        if image_equivalent(left, right):
            return "EQUIVALENT"
        return "MUTUAL_EMBEDDABILITY_NONISOMORPHIC"
    if lr:
        return "LEFT_STRICT_SUBOBJECT_OF_RIGHT"
    if rl:
        return "RIGHT_STRICT_SUBOBJECT_OF_LEFT"
    return "INCOMPARABLE"


def _transitive_reduction(
    object_ids: list[str],
    strict_edges: set[tuple[str, str]],
) -> tuple[list[tuple[str, str]], bool]:
    # Detect cycles first.
    adj = {x: set() for x in object_ids}
    for a, b in strict_edges:
        adj[a].add(b)

    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs_cycle(x: str) -> bool:
        if x in visiting:
            return True
        if x in visited:
            return False
        visiting.add(x)
        for y in adj[x]:
            if dfs_cycle(y):
                return True
        visiting.remove(x)
        visited.add(x)
        return False

    cyclic = any(dfs_cycle(x) for x in object_ids if x not in visited)
    if cyclic:
        return sorted(strict_edges), False

    # For a transitive strict-subobject relation, (a,b) is a cover iff there
    # is no c with a<c and c<b.
    reduced = []
    for a, b in sorted(strict_edges):
        mediated = any(
            c != a and c != b
            and (a, c) in strict_edges
            and (c, b) in strict_edges
            for c in object_ids
        )
        if not mediated:
            reduced.append((a, b))
    return reduced, True


def build_report() -> dict[str, Any]:
    skeleton_cache: dict[str, dict[str, Any]] = {}
    recovered_by_id: dict[str, dict[str, Any]] = {}
    origins_by_id: dict[str, list[dict[str, Any]]] = {}
    lane_counts: dict[str, int] = {}
    recovery_counts: dict[str, int] = {}
    input_sha256 = {}

    for lane, path in LANE_REPORTS.items():
        input_sha256[lane] = _sha256_path(path)
        report = _load_json(path)
        candidates = report["archetype_candidates"]
        lane_counts[lane] = len(candidates)

        for candidate in candidates:
            target = candidate["archetype_id"]
            image, recovery = _recover_candidate(lane, candidate, skeleton_cache)
            if image_id(image) != target:
                raise GlobalArchetypeError(f"{lane}:{target}: recovered ID mismatch")
            canonical = _canonicalize_image(image)

            if target in recovered_by_id:
                if not image_equivalent(recovered_by_id[target], canonical):
                    raise GlobalArchetypeError(
                        f"{target}: repeated canonical ID is not structurally equivalent"
                    )
            else:
                recovered_by_id[target] = canonical

            recovery_counts[recovery.split(":", 1)[0]] = (
                recovery_counts.get(recovery.split(":", 1)[0], 0) + 1
            )
            origins_by_id.setdefault(target, []).append({
                "lane": lane,
                "lane_candidate_id": target,
                "member_claim_ids": list(candidate["member_claim_ids"]),
                "support_size": int(candidate.get("support_size", len(candidate["member_claim_ids"]))),
                "recovery": recovery,
            })

    object_ids = sorted(recovered_by_id)

    equivalence_components = []
    for object_id in object_ids:
        lanes = sorted({x["lane"] for x in origins_by_id[object_id]})
        if len(lanes) >= 2:
            equivalence_components.append({
                "global_archetype_id": object_id,
                "lanes": lanes,
                "origins": sorted(
                    origins_by_id[object_id],
                    key=lambda x: (x["lane"], x["member_claim_ids"]),
                ),
            })

    strict_edges: set[tuple[str, str]] = set()
    relation_counts = {
        "EQUIVALENT": 0,
        "LEFT_STRICT_SUBOBJECT_OF_RIGHT": 0,
        "RIGHT_STRICT_SUBOBJECT_OF_LEFT": 0,
        "MUTUAL_EMBEDDABILITY_NONISOMORPHIC": 0,
        "INCOMPARABLE": 0,
    }
    mutual_noniso = []

    for i, left_id in enumerate(object_ids):
        left = recovered_by_id[left_id]
        for right_id in object_ids[i + 1:]:
            right = recovered_by_id[right_id]
            relation = _strict_relation(left, right)
            relation_counts[relation] += 1
            if relation == "LEFT_STRICT_SUBOBJECT_OF_RIGHT":
                strict_edges.add((left_id, right_id))
            elif relation == "RIGHT_STRICT_SUBOBJECT_OF_LEFT":
                strict_edges.add((right_id, left_id))
            elif relation == "MUTUAL_EMBEDDABILITY_NONISOMORPHIC":
                mutual_noniso.append([left_id, right_id])

    reduced_edges, reduction_valid = _transitive_reduction(object_ids, strict_edges)

    # Refinement closure support: if A <= B and B is independently supported
    # in a lane, A inherits that support by composition.
    strict_out = {x: set() for x in object_ids}
    for a, b in strict_edges:
        strict_out[a].add(b)

    def upward(start: str) -> set[str]:
        seen = {start}
        stack = [start]
        while stack:
            x = stack.pop()
            for y in strict_out[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        return seen

    global_objects = []
    cross_lane_by_exact = 0
    cross_lane_by_closure = 0

    for object_id in object_ids:
        image = recovered_by_id[object_id]
        direct_lanes = sorted({x["lane"] for x in origins_by_id[object_id]})
        closure_ids = sorted(upward(object_id))
        derived_lanes = sorted({
            origin["lane"]
            for upper_id in closure_ids
            for origin in origins_by_id[upper_id]
        })
        derived_claims_by_lane: dict[str, set[str]] = {}
        for upper_id in closure_ids:
            for origin in origins_by_id[upper_id]:
                derived_claims_by_lane.setdefault(origin["lane"], set()).update(
                    origin["member_claim_ids"]
                )

        if len(direct_lanes) >= 2:
            cross_lane_by_exact += 1
        if len(derived_lanes) >= 2:
            cross_lane_by_closure += 1

        global_objects.append({
            "global_archetype_id": object_id,
            **_summary(image),
            "canonical_structural_object": image,
            "direct_origin_lanes": direct_lanes,
            "direct_origins": sorted(
                origins_by_id[object_id],
                key=lambda x: (x["lane"], x["member_claim_ids"]),
            ),
            "upward_refinement_object_count": len(closure_ids),
            "derived_support_lanes": derived_lanes,
            "derived_support_claim_ids_by_lane": {
                lane: sorted(ids)
                for lane, ids in sorted(derived_claims_by_lane.items())
            },
        })

    direct_refinement_edges = []
    for a, b in reduced_edges:
        a_lanes = sorted({x["lane"] for x in origins_by_id[a]})
        b_lanes = sorted({x["lane"] for x in origins_by_id[b]})
        direct_refinement_edges.append({
            "weaker_archetype_id": a,
            "stronger_archetype_id": b,
            "weaker_origin_lanes": a_lanes,
            "stronger_origin_lanes": b_lanes,
            "disjoint_lane_provenance": set(a_lanes).isdisjoint(b_lanes),
        })

    pair_count = len(object_ids) * (len(object_ids) - 1) // 2
    if sum(relation_counts.values()) != pair_count:
        raise GlobalArchetypeError("relation count does not exhaust unique object pairs")

    decision = (
        "GLOBAL_ARCHETYPE_PREORDER_WITH_CROSS_LANE_RECURRENCE_SUPPORTED"
        if equivalence_components or cross_lane_by_closure
        else "NO_CROSS_LANE_ARCHETYPE_STRUCTURE_ON_FROZEN_SURFACE"
    )

    return {
        "schema_version": "paper2-global-archetype-reconstruction-v1",
        "owner_issue": 315,
        "parent_issue": 283,
        "input_policy": "independently frozen lane-local Archetype reports only",
        "input_report_sha256": input_sha256,
        "lane_candidate_counts": lane_counts,
        "lane_candidate_total": sum(lane_counts.values()),
        "unique_global_archetype_count": len(object_ids),
        "exact_cross_lane_equivalence_component_count": len(equivalence_components),
        "exact_cross_lane_equivalence_components": equivalence_components,
        "unique_object_pair_count": pair_count,
        "global_relation_counts": relation_counts,
        "strict_subobject_edge_count_transitive": len(strict_edges),
        "direct_refinement_edge_count": len(direct_refinement_edges),
        "transitive_reduction_valid": reduction_valid,
        "mutual_embeddability_nonisomorphic_pairs": mutual_noniso,
        "direct_refinement_edges": direct_refinement_edges,
        "cross_lane_exact_object_count": cross_lane_by_exact,
        "cross_lane_refinement_closure_object_count": cross_lane_by_closure,
        "global_archetype_objects": global_objects,
        "recovery_route_counts": recovery_counts,
        "historical_construct_labels_used": False,
        "joint_cross_lane_candidate_generation_performed": False,
        "architecture_tuning": "NONE",
        "decision": decision,
    }


def self_test() -> None:
    first = build_report()
    second = build_report()
    assert first == second
    assert first["lane_candidate_total"] == 213
    assert first["unique_global_archetype_count"] == 206
    assert first["exact_cross_lane_equivalence_component_count"] == 7
    assert first["historical_construct_labels_used"] is False
    assert first["joint_cross_lane_candidate_generation_performed"] is False
    assert first["architecture_tuning"] == "NONE"
    print("PAPER2_GLOBAL_ARCHETYPE_RECONSTRUCTION_V1_SELFTEST_PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--emit-report", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return
    if not args.emit_report:
        parser.error("--emit-report or --self-test is required")

    report = build_report()
    payload = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
