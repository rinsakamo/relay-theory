#!/usr/bin/env python3
"""Paper 2 #303: SKL six-object Archetype pilot.

Uses only frozen reviewed ClaimIR + reference structural adjudication inputs,
then the qualified #293 machinery:

    ClaimIR + adjudication
      -> compiled structural signature
      -> frozen Phi
      -> U_claim basis skeleton
      -> explicit F_R common basis subobjects

No source rereading, lexical similarity, historical construct labels, or
clustering enters candidate generation.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

from paper2_reference_structural_adjudication import compile_record
from paper2_phi_compare import project_first
from paper2_basis_structural_skeleton import (
    CONTROL_KEYS,
    TEMPORAL_KEYS,
    project_basis_skeleton,
    skeleton_equivalent,
    validate_skeleton,
)
from paper2_basis_subobject_forgetting import (
    IMAGE_VERSION,
    image_equivalent,
    is_nontrivial,
    restrict_skeleton,
    validate_image,
)

SKL_IDS = [f"SKL0{i}" for i in range(1, 7)]
CLAIM_DIR = Path("research/paper2/chatgpt_reference_claimir_v1")
ADJ_DIR = Path("research/paper2/reference_structural_adjudication_v1")

POSITIVE_STATE = "present"


class PilotError(ValueError):
    pass


def _canon(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


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


def _positive_temporal_keys(skeleton: dict[str, Any]) -> list[str]:
    return [
        key for key in TEMPORAL_KEYS
        if skeleton["temporal"][key]["state"] == POSITIVE_STATE
    ]


def _positive_control_keys(skeleton: dict[str, Any]) -> list[str]:
    return [
        key for key in CONTROL_KEYS
        if skeleton["controls"][key]["state"] == POSITIVE_STATE
    ]


def load_skl_skeletons() -> dict[str, dict[str, Any]]:
    out = {}
    for claim_id in SKL_IDS:
        claim = json.loads((CLAIM_DIR / f"{claim_id}.json").read_text(encoding="utf-8"))
        adjudication = json.loads((ADJ_DIR / f"{claim_id}.json").read_text(encoding="utf-8"))
        record = compile_record(claim, adjudication)
        phi = project_first(record)
        skeleton = project_basis_skeleton(phi)
        validate_skeleton(skeleton)
        out[claim_id] = skeleton
    return out


def partial_node_mappings(
    left: dict[str, Any],
    right: dict[str, Any],
) -> Iterator[dict[str, str]]:
    """Enumerate all nonempty injective partial mappings preserving node labels."""
    left_ids = sorted(left["nodes"])
    right_by_label: dict[str, list[str]] = {}
    for rid, node in right["nodes"].items():
        right_by_label.setdefault(_node_label(node), []).append(rid)
    for values in right_by_label.values():
        values.sort()

    mapping: dict[str, str] = {}
    used: set[str] = set()

    def rec(i: int):
        if i == len(left_ids):
            if mapping:
                yield dict(mapping)
            return

        lid = left_ids[i]
        label = _node_label(left["nodes"][lid])

        # Forget this left node.
        yield from rec(i + 1)

        # Retain/map it.
        for rid in right_by_label.get(label, []):
            if rid in used:
                continue
            mapping[lid] = rid
            used.add(rid)
            yield from rec(i + 1)
            used.remove(rid)
            del mapping[lid]

    yield from rec(0)


def matched_edge_indices(
    left: dict[str, Any],
    right: dict[str, Any],
    mapping: dict[str, str],
) -> tuple[list[int], list[int]]:
    """Retain the full common edge multiset induced by one node mapping."""
    right_identity = {x: x for x in right["nodes"]}
    right_by_signature: dict[str, list[int]] = {}
    for i, edge in enumerate(right["edges"]):
        sig = _edge_under_mapping(edge, right_identity)
        right_by_signature.setdefault(sig, []).append(i)

    cursors: dict[str, int] = Counter()
    left_indices: list[int] = []
    right_indices: list[int] = []

    mapped_left = set(mapping)
    for i, edge in enumerate(left["edges"]):
        refs = set(edge["arguments"] + edge["conditional_on"])
        if not refs <= mapped_left:
            continue
        sig = _edge_under_mapping(edge, mapping)
        options = right_by_signature.get(sig, [])
        cursor = cursors[sig]
        if cursor >= len(options):
            continue
        left_indices.append(i)
        right_indices.append(options[cursor])
        cursors[sig] += 1

    return left_indices, right_indices


def common_positive_features(
    left: dict[str, Any],
    right: dict[str, Any],
) -> tuple[list[str], list[str]]:
    temporal = [
        key for key in TEMPORAL_KEYS
        if left["temporal"][key] == right["temporal"][key]
        and left["temporal"][key]["state"] == POSITIVE_STATE
    ]
    controls = [
        key for key in CONTROL_KEYS
        if left["controls"][key] == right["controls"][key]
        and left["controls"][key]["state"] == POSITIVE_STATE
    ]
    return temporal, controls


def canonical_image_key(image: dict[str, Any]) -> str:
    """Canonical image identity modulo anonymous basis-coordinate IDs."""
    validate_image(image)
    by_label: dict[str, list[str]] = {}
    for node_id, node in image["nodes"].items():
        by_label.setdefault(_node_label(node), []).append(node_id)

    label_groups = sorted(by_label)
    canonical_slots: dict[str, list[str]] = {}
    offset = 0
    for label in label_groups:
        size = len(by_label[label])
        canonical_slots[label] = [f"n{i}" for i in range(offset, offset + size)]
        offset += size

    group_permutations = []
    for label in label_groups:
        ids = sorted(by_label[label])
        slots = canonical_slots[label]
        group_permutations.append([
            dict(zip(ids, perm))
            for perm in itertools.permutations(slots)
        ])

    best: str | None = None
    for parts in itertools.product(*group_permutations):
        mapping: dict[str, str] = {}
        for part in parts:
            mapping.update(part)

        nodes = {
            mapping[node_id]: image["nodes"][node_id]
            for node_id in image["nodes"]
        }
        edges = sorted(
            _edge_under_mapping(edge, mapping)
            for edge in image["edges"]
        )
        candidate = _canon({
            "active_axes": image["active_axes"],
            "nodes": nodes,
            "edges": edges,
            "temporal": image["temporal"],
            "controls": image["controls"],
        })
        if best is None or candidate < best:
            best = candidate

    if best is None:
        # Empty-node objects are not valid Archetype candidates, but keep a
        # deterministic identity for defensive use.
        best = _canon({
            "active_axes": image["active_axes"],
            "nodes": {},
            "edges": [],
            "temporal": image["temporal"],
            "controls": image["controls"],
        })
    return best


def image_id(image: dict[str, Any]) -> str:
    return "A-" + hashlib.sha256(canonical_image_key(image).encode("utf-8")).hexdigest()[:12]


def image_embeds_in_image(weak: dict[str, Any], strong: dict[str, Any]) -> bool:
    """Whether weak is a basis subobject of strong modulo anonymous IDs."""
    validate_image(weak)
    validate_image(strong)

    if not set(weak["active_axes"]) <= set(strong["active_axes"]):
        return False
    for key, value in weak["temporal"].items():
        if strong["temporal"].get(key) != value:
            return False
    for key, value in weak["controls"].items():
        if strong["controls"].get(key) != value:
            return False
    if len(weak["nodes"]) > len(strong["nodes"]):
        return False

    strong_by_label: dict[str, list[str]] = {}
    for sid, node in strong["nodes"].items():
        strong_by_label.setdefault(_node_label(node), []).append(sid)
    for values in strong_by_label.values():
        values.sort()

    order = sorted(
        weak["nodes"],
        key=lambda x: (len(strong_by_label.get(_node_label(weak["nodes"][x]), [])), x),
    )
    strong_identity = {x: x for x in strong["nodes"]}
    strong_edges = Counter(_edge_under_mapping(e, strong_identity) for e in strong["edges"])

    def partial_ok(mapping: dict[str, str]) -> bool:
        c: Counter[str] = Counter()
        for edge in weak["edges"]:
            refs = edge["arguments"] + edge["conditional_on"]
            if all(ref in mapping for ref in refs):
                c[_edge_under_mapping(edge, mapping)] += 1
        return all(strong_edges[k] >= v for k, v in c.items())

    def rec(i: int, mapping: dict[str, str], used: set[str]) -> bool:
        if i == len(order):
            c = Counter(_edge_under_mapping(e, mapping) for e in weak["edges"])
            return all(strong_edges[k] >= v for k, v in c.items())
        wid = order[i]
        label = _node_label(weak["nodes"][wid])
        for sid in strong_by_label.get(label, []):
            if sid in used:
                continue
            mapping[wid] = sid
            used.add(sid)
            if partial_ok(mapping) and rec(i + 1, mapping, used):
                return True
            used.remove(sid)
            del mapping[wid]
        return False

    return rec(0, {}, set())


def image_embeds_in_skeleton(image: dict[str, Any], skeleton: dict[str, Any]) -> bool:
    validate_image(image)
    validate_skeleton(skeleton)

    # Convert the target skeleton into a maximal positive-feature image.
    full = restrict_skeleton(
        skeleton,
        retained_node_ids=sorted(skeleton["nodes"]),
        retained_edge_indices=list(range(len(skeleton["edges"]))),
        retained_temporal_keys=_positive_temporal_keys(skeleton),
        retained_control_keys=_positive_control_keys(skeleton),
    )
    return image_embeds_in_image(image, full)



def find_image_witness(
    image: dict[str, Any],
    skeleton: dict[str, Any],
) -> dict[str, Any] | None:
    """Return one deterministic explicit F_R witness if image embeds in skeleton."""
    validate_image(image)
    validate_skeleton(skeleton)

    retained_temporal_keys = sorted(image["temporal"])
    retained_control_keys = sorted(image["controls"])

    for key, value in image["temporal"].items():
        if skeleton["temporal"].get(key) != value:
            return None
    for key, value in image["controls"].items():
        if skeleton["controls"].get(key) != value:
            return None
    if len(image["nodes"]) > len(skeleton["nodes"]):
        return None

    skeleton_by_label: dict[str, list[str]] = {}
    for sid, node in skeleton["nodes"].items():
        skeleton_by_label.setdefault(_node_label(node), []).append(sid)
    for values in skeleton_by_label.values():
        values.sort()

    order = sorted(
        image["nodes"],
        key=lambda x: (len(skeleton_by_label.get(_node_label(image["nodes"][x]), [])), x),
    )
    identity = {x: x for x in skeleton["nodes"]}
    skeleton_edges = Counter(_edge_under_mapping(e, identity) for e in skeleton["edges"])

    def partial_ok(mapping: dict[str, str]) -> bool:
        counts: Counter[str] = Counter()
        for edge in image["edges"]:
            refs = edge["arguments"] + edge["conditional_on"]
            if all(ref in mapping for ref in refs):
                counts[_edge_under_mapping(edge, mapping)] += 1
        return all(skeleton_edges[k] >= v for k, v in counts.items())

    def matched_indices(mapping: dict[str, str]) -> list[int] | None:
        buckets: dict[str, list[int]] = {}
        for i, edge in enumerate(skeleton["edges"]):
            sig = _edge_under_mapping(edge, identity)
            buckets.setdefault(sig, []).append(i)
        cursors: Counter[str] = Counter()
        indices: list[int] = []
        for edge in image["edges"]:
            sig = _edge_under_mapping(edge, mapping)
            options = buckets.get(sig, [])
            cursor = cursors[sig]
            if cursor >= len(options):
                return None
            indices.append(options[cursor])
            cursors[sig] += 1
        return sorted(indices)

    def rec(i: int, mapping: dict[str, str], used: set[str]) -> dict[str, Any] | None:
        if i == len(order):
            edge_indices = matched_indices(mapping)
            if edge_indices is None:
                return None
            retained_nodes = sorted(mapping.values())
            reconstructed = restrict_skeleton(
                skeleton,
                retained_node_ids=retained_nodes,
                retained_edge_indices=edge_indices,
                retained_temporal_keys=retained_temporal_keys,
                retained_control_keys=retained_control_keys,
            )
            if not image_equivalent(image, reconstructed):
                return None
            positive_temporal = set(_positive_temporal_keys(skeleton))
            positive_controls = set(_positive_control_keys(skeleton))
            retained_edges = set(edge_indices)
            return {
                "image_node_to_member_node": dict(sorted(mapping.items())),
                "retained_node_ids": retained_nodes,
                "forgotten_node_ids": sorted(set(skeleton["nodes"]) - set(retained_nodes)),
                "retained_edge_indices": edge_indices,
                "forgotten_edge_indices": [
                    idx for idx in range(len(skeleton["edges"])) if idx not in retained_edges
                ],
                "retained_temporal_keys": retained_temporal_keys,
                "forgotten_temporal_keys": sorted(
                    positive_temporal - set(retained_temporal_keys)
                ),
                "retained_control_keys": retained_control_keys,
                "forgotten_control_keys": sorted(
                    positive_controls - set(retained_control_keys)
                ),
                "resulting_image_equivalence_verified": True,
            }

        iid = order[i]
        label = _node_label(image["nodes"][iid])
        for sid in skeleton_by_label.get(label, []):
            if sid in used:
                continue
            mapping[iid] = sid
            used.add(sid)
            if partial_ok(mapping):
                witness = rec(i + 1, mapping, used)
                if witness is not None:
                    return witness
            used.remove(sid)
            del mapping[iid]
        return None

    return rec(0, {}, set())



def coarse_image_invariant(image: dict[str, Any]) -> str:
    """Cheap isomorphism invariant; collisions are resolved by image_equivalent."""
    validate_image(image)
    node_labels = {node_id: _node_label(node) for node_id, node in image["nodes"].items()}
    node_multiset = sorted(node_labels.values())
    edge_profile = []
    for edge in image["edges"]:
        args = [node_labels[x] for x in edge["arguments"]]
        if not edge["ordered_arguments"]:
            args = sorted(args)
        cond = sorted(node_labels[x] for x in edge["conditional_on"])
        edge_profile.append(_canon({
            "family": edge["family"],
            "kind": edge["kind"],
            "ordered_arguments": edge["ordered_arguments"],
            "arguments": args,
            "conditional_on": cond,
            "temporal_direction": edge["temporal_direction"],
        }))
    edge_profile.sort()
    return _canon({
        "active_axes": image["active_axes"],
        "node_multiset": node_multiset,
        "edge_profile": edge_profile,
        "temporal": image["temporal"],
        "controls": image["controls"],
    })


def _register_equivalence_class(
    buckets: dict[str, list[dict[str, Any]]],
    image: dict[str, Any],
    payload: dict[str, Any],
) -> tuple[dict[str, Any], bool]:
    inv = coarse_image_invariant(image)
    bucket = buckets.setdefault(inv, [])
    for item in bucket:
        if image_equivalent(image, item["image"]):
            return item, False
    item = {"image": image, **payload}
    bucket.append(item)
    return item, True


def pair_common_candidates(
    left: dict[str, Any],
    right: dict[str, Any],
) -> list[dict[str, Any]]:
    """Enumerate exact common-image classes, deduplicating before canonical labeling."""
    temporal, controls = common_positive_features(left, right)
    buckets: dict[str, list[dict[str, Any]]] = {}
    raw_seen: set[tuple[tuple[str, ...], tuple[int, ...]]] = set()

    right_identity = {x: x for x in right["nodes"]}
    right_by_signature: dict[str, list[int]] = {}
    for i, edge in enumerate(right["edges"]):
        sig = _edge_under_mapping(edge, right_identity)
        right_by_signature.setdefault(sig, []).append(i)

    for mapping in partial_node_mappings(left, right):
        cursors: Counter[str] = Counter()
        left_edges: list[int] = []
        right_edges: list[int] = []
        mapped_left = set(mapping)
        for i, edge in enumerate(left["edges"]):
            refs = set(edge["arguments"] + edge["conditional_on"])
            if not refs <= mapped_left:
                continue
            sig = _edge_under_mapping(edge, mapping)
            options = right_by_signature.get(sig, [])
            cursor = cursors[sig]
            if cursor >= len(options):
                continue
            left_edges.append(i)
            right_edges.append(options[cursor])
            cursors[sig] += 1

        left_nodes = sorted(mapping)
        raw_key = (tuple(left_nodes), tuple(left_edges))
        if raw_key in raw_seen:
            continue
        raw_seen.add(raw_key)

        right_nodes = sorted(mapping.values())
        left_image = restrict_skeleton(
            left,
            retained_node_ids=left_nodes,
            retained_edge_indices=left_edges,
            retained_temporal_keys=temporal,
            retained_control_keys=controls,
        )
        if not is_nontrivial(left_image):
            continue
        right_image = restrict_skeleton(
            right,
            retained_node_ids=right_nodes,
            retained_edge_indices=right_edges,
            retained_temporal_keys=temporal,
            retained_control_keys=controls,
        )
        if not image_equivalent(left_image, right_image):
            raise PilotError("pair candidate witness failed equivalence check")

        _register_equivalence_class(
            buckets,
            left_image,
            {
                "left_witness": {
                    "retained_node_ids": left_nodes,
                    "retained_edge_indices": left_edges,
                    "retained_temporal_keys": temporal,
                    "retained_control_keys": controls,
                },
                "right_witness": {
                    "retained_node_ids": right_nodes,
                    "retained_edge_indices": right_edges,
                    "retained_temporal_keys": temporal,
                    "retained_control_keys": controls,
                },
            },
        )

    classes: list[dict[str, Any]] = []
    for inv in sorted(buckets):
        classes.extend(buckets[inv])
    return classes


def summarize_image(image: dict[str, Any]) -> dict[str, Any]:
    node_profile = sorted(
        [
            {
                "role": node["role"],
                "axis": node["axis"],
                "required": node["required"],
            }
            for node in image["nodes"].values()
        ],
        key=lambda x: _canon(x),
    )

    edge_profile = []
    labels = {node_id: _node_label(node) for node_id, node in image["nodes"].items()}
    for edge in image["edges"]:
        edge_profile.append({
            "family": edge["family"],
            "kind": edge["kind"],
            "ordered_arguments": edge["ordered_arguments"],
            "argument_node_labels": [labels[x] for x in edge["arguments"]],
            "conditional_node_labels": [labels[x] for x in edge["conditional_on"]],
            "temporal_direction": edge["temporal_direction"],
        })
    edge_profile.sort(key=_canon)

    return {
        "archetype_id": image_id(image),
        "active_axes": image["active_axes"],
        "node_count": len(image["nodes"]),
        "edge_count": len(image["edges"]),
        "node_profile": node_profile,
        "edge_profile": edge_profile,
        "temporal_features": sorted(image["temporal"]),
        "control_features": sorted(image["controls"]),
    }


def _compute_pair_task(
    task: tuple[str, str, dict[str, Any], dict[str, Any]],
) -> tuple[str, str, bool, list[dict[str, Any]]]:
    """Run one exact pair search; pair tasks are scientifically independent."""
    left_id, right_id, left, right = task
    return (
        left_id,
        right_id,
        skeleton_equivalent(left, right),
        pair_common_candidates(left, right),
    )


def run_pilot() -> dict[str, Any]:
    skeletons = load_skl_skeletons()

    exact_equivalence_pairs = []
    all_candidate_buckets: dict[str, list[dict[str, Any]]] = {}
    pair_candidate_counts = {}

    pair_tasks = [
        (left_id, right_id, skeletons[left_id], skeletons[right_id])
        for i, left_id in enumerate(SKL_IDS)
        for right_id in SKL_IDS[i + 1:]
    ]

    # Same exact pair search as the merged MEM pilot, parallelized only across
    # scientifically independent unordered claim pairs. pool.map preserves
    # the frozen pair order, so aggregation and report bytes remain deterministic.
    with ProcessPoolExecutor(max_workers=min(4, len(pair_tasks))) as pool:
        pair_results = list(pool.map(_compute_pair_task, pair_tasks))

    for left_id, right_id, equivalent, candidates in pair_results:
        if equivalent:
            exact_equivalence_pairs.append([left_id, right_id])

        pair_candidate_counts[f"{left_id}::{right_id}"] = len(candidates)
        for payload in candidates:
            item, created = _register_equivalence_class(
                all_candidate_buckets,
                payload["image"],
                {"pair_witnesses": {}},
            )
            item["pair_witnesses"][f"{left_id}::{right_id}"] = {
                left_id: payload["left_witness"],
                right_id: payload["right_witness"],
            }

    all_candidates: list[dict[str, Any]] = []
    for inv in sorted(all_candidate_buckets):
        all_candidates.extend(all_candidate_buckets[inv])

    # Determine full SKL support for every unique non-trivial candidate.
    support_groups: dict[tuple[str, ...], list[tuple[int, dict[str, Any]]]] = {}
    for key, payload in enumerate(all_candidates):
        image = payload["image"]
        support = tuple(
            claim_id for claim_id in SKL_IDS
            if image_embeds_in_skeleton(image, skeletons[claim_id])
        )
        if len(support) < 2:
            continue
        support_groups.setdefault(support, []).append((key, payload))

    # Within an identical support set, retain only structurally maximal candidates.
    maximal: list[dict[str, Any]] = []
    for support, items in sorted(support_groups.items()):
        for key, payload in items:
            image = payload["image"]
            dominated = False
            for other_key, other_payload in items:
                if other_key == key:
                    continue
                other = other_payload["image"]
                if image_embeds_in_image(image, other) and not image_equivalent(image, other):
                    dominated = True
                    break
            if dominated:
                continue

            summary = summarize_image(image)
            summary["member_claim_ids"] = list(support)
            summary["support_size"] = len(support)
            summary["witness_pair_count"] = len(payload["pair_witnesses"])
            summary["retained_basis_subobject"] = image
            member_witnesses = {}
            for claim_id in support:
                witness = find_image_witness(image, skeletons[claim_id])
                if witness is None:
                    raise PilotError(
                        f"terminal candidate lacks explicit forgetting witness for {claim_id}"
                    )
                member_witnesses[claim_id] = witness
            summary["member_forgetting_witnesses"] = member_witnesses
            maximal.append(summary)

    maximal.sort(key=lambda x: (
        -x["support_size"],
        -x["node_count"],
        -x["edge_count"],
        x["archetype_id"],
    ))

    # Count pairwise incomparability among terminal maximal candidates using
    # their canonical images recovered from all_candidates.
    image_by_id = {
        image_id(payload["image"]): payload["image"]
        for payload in all_candidates
    }
    incomparable_pairs = 0
    comparable_pairs = 0
    candidate_relations = []
    for i, a in enumerate(maximal):
        for b in maximal[i + 1:]:
            ia = image_by_id[a["archetype_id"]]
            ib = image_by_id[b["archetype_id"]]
            ab = image_embeds_in_image(ia, ib)
            ba = image_embeds_in_image(ib, ia)
            if not ab and not ba:
                relation = "INCOMPARABLE"
                incomparable_pairs += 1
            elif ab and ba:
                relation = "EQUIVALENT"
                comparable_pairs += 1
            elif ab:
                relation = "LEFT_EMBEDS_IN_RIGHT"
                comparable_pairs += 1
            else:
                relation = "RIGHT_EMBEDS_IN_LEFT"
                comparable_pairs += 1
            candidate_relations.append({
                "left_archetype_id": a["archetype_id"],
                "right_archetype_id": b["archetype_id"],
                "relation": relation,
            })

    if not maximal:
        decision = "SKL_ONLY_TRIVIAL_COMMON_STRUCTURE"
    elif len(maximal) == 1:
        decision = "SKL_ARCHETYPE_RECONSTRUCTION_SUPPORTED"
    elif incomparable_pairs > 0:
        decision = "SKL_MULTIPLE_INCOMPARABLE_ARCHETYPES"
    else:
        decision = "SKL_ARCHETYPE_RECONSTRUCTION_SUPPORTED"

    return {
        "schema_version": "paper2-skl-archetype-reconstruction-v1",
        "owner_issue": 303,
        "parent_issue": 283,
        "input_claim_ids": SKL_IDS,
        "input_policy": "frozen reviewed ClaimIR + reference structural adjudication only",
        "abstraction_contract": {
            "stage1": "U_claim",
            "stage2": "F_R",
            "common_absence_as_positive_structure": False,
        },
        "exact_basis_skeleton_equivalence_pairs": exact_equivalence_pairs,
        "pair_candidate_counts": pair_candidate_counts,
        "unique_nontrivial_pair_generated_candidate_count": len(all_candidates),
        "support_set_count": len(support_groups),
        "support_sets": [
            {
                "member_claim_ids": list(support),
                "pair_generated_candidate_count": len(items),
            }
            for support, items in sorted(support_groups.items())
        ],
        "maximal_archetype_candidate_count": len(maximal),
        "maximal_candidate_relation_summary": {
            "incomparable_pairs": incomparable_pairs,
            "comparable_pairs": comparable_pairs,
        },
        "maximal_candidate_relations": candidate_relations,
        "archetype_candidates": maximal,
        "decision": decision,
        "construct_specificity_claim": False,
        "architecture_tuning": "NONE",
    }


def self_test() -> None:
    # One exact real-input reconstruction here plus the separate CI report
    # regeneration/byte-identity step provide two independent deterministic runs.
    first = run_pilot()
    assert first["input_claim_ids"] == SKL_IDS
    assert first["construct_specificity_claim"] is False
    assert first["architecture_tuning"] == "NONE"
    for candidate in first["archetype_candidates"]:
        assert set(candidate["member_forgetting_witnesses"]) == set(candidate["member_claim_ids"])
        assert all(
            witness["resulting_image_equivalence_verified"]
            for witness in candidate["member_forgetting_witnesses"].values()
        )
    print("PAPER2_SKL_ARCHETYPE_RECONSTRUCTION_V1_SELFTEST_PASS")


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

    report = run_pilot()
    payload = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
