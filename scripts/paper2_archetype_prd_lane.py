#!/usr/bin/env python3
"""Paper 2 #302: PRD lane-local Archetype reconstruction.

Uses only frozen reviewed PRD ClaimIR + structural adjudication inputs and the
already-qualified #293 abstraction grammar:

    ClaimIR + adjudication -> structural signature -> Phi
    -> U_claim basis skeleton -> F_R common basis subobjects
    -> maximal non-trivial common images

Candidate semantics are identical to the frozen MEM pilot.  The enumeration
engine only removes permutations of nodes that cannot possibly participate in
a shared structural edge; a synthetic self-test checks candidate-key identity
against the frozen MEM-pilot helper on the same fixtures.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
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
from paper2_archetype_mem_pilot import (
    _canon,
    _edge_under_mapping,
    _node_label,
    _positive_control_keys,
    _positive_temporal_keys,
    canonical_image_key,
    image_embeds_in_image,
    image_embeds_in_skeleton,
    image_id,
    matched_edge_indices,
    pair_common_candidates,
    summarize_image,
)

LANE_IDS = [f"PRD0{i}" for i in range(1, 7)]
CLAIM_DIR = Path("research/paper2/chatgpt_reference_claimir_v1")
ADJ_DIR = Path("research/paper2/reference_structural_adjudication_v1")
OWNER_ISSUE = 302
PARENT_ISSUE = 283
GRAMMAR_ISSUE = 293
REFERENCE_PILOT_ISSUE = 295
REFERENCE_PILOT_PR = 296
INPUT_MAIN = "d45982a4174ce7efb44a0ce12fa1171d6095773d"
POSITIVE_STATE = "present"


class LaneError(ValueError):
    pass


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_lane_skeletons() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    skeletons: dict[str, dict[str, Any]] = {}
    inputs: list[dict[str, Any]] = []
    for slot in LANE_IDS:
        claim_path = CLAIM_DIR / f"{slot}.json"
        adj_path = ADJ_DIR / f"{slot}.json"
        claim = json.loads(claim_path.read_text(encoding="utf-8"))
        adjudication = json.loads(adj_path.read_text(encoding="utf-8"))
        if claim["extraction"]["manual_review_status"] != "reviewed":
            raise LaneError(f"{slot}: ClaimIR is not reviewed")
        if adjudication["decision"]["status"] not in {"PASS", "RESIDUAL"}:
            raise LaneError(f"{slot}: structural adjudication is not terminal")
        record = compile_record(claim, adjudication)
        phi = project_first(record)
        skeleton = project_basis_skeleton(phi)
        validate_skeleton(skeleton)
        skeletons[slot] = skeleton
        inputs.append({
            "slot": slot,
            "claim_id": claim["claim_id"],
            "claim_ir_sha256": file_sha256(claim_path),
            "structural_adjudication_sha256": file_sha256(adj_path),
            "structural_decision": adjudication["decision"]["status"],
        })
    return skeletons, inputs


def edge_coarse_signature(skeleton: dict[str, Any], edge: dict[str, Any]) -> str:
    args = [_node_label(skeleton["nodes"][x]) for x in edge["arguments"]]
    if not edge["ordered_arguments"]:
        args = sorted(args)
    cond = sorted(_node_label(skeleton["nodes"][x]) for x in edge["conditional_on"])
    return _canon({
        "family": edge["family"],
        "kind": edge["kind"],
        "ordered_arguments": edge["ordered_arguments"],
        "argument_node_labels": args,
        "conditional_node_labels": cond,
        "temporal_direction": edge["temporal_direction"],
    })


def relevant_left_nodes(left: dict[str, Any], right: dict[str, Any]) -> set[str]:
    right_signatures = {edge_coarse_signature(right, e) for e in right["edges"]}
    out: set[str] = set()
    for edge in left["edges"]:
        if edge_coarse_signature(left, edge) not in right_signatures:
            continue
        out.update(edge["arguments"])
        out.update(edge["conditional_on"])
    return out


def partial_relevant_mappings(
    left: dict[str, Any],
    right: dict[str, Any],
    relevant: set[str],
) -> Iterator[dict[str, str]]:
    left_ids = sorted(relevant)
    right_by_label: dict[str, list[str]] = {}
    for rid, node in right["nodes"].items():
        right_by_label.setdefault(_node_label(node), []).append(rid)
    for values in right_by_label.values():
        values.sort()

    mapping: dict[str, str] = {}
    used: set[str] = set()

    def rec(i: int):
        if i == len(left_ids):
            yield dict(mapping)
            return
        lid = left_ids[i]
        label = _node_label(left["nodes"][lid])

        yield from rec(i + 1)

        for rid in right_by_label.get(label, []):
            if rid in used:
                continue
            mapping[lid] = rid
            used.add(rid)
            yield from rec(i + 1)
            used.remove(rid)
            del mapping[lid]

    yield from rec(0)


def isolated_extra_mappings(
    left: dict[str, Any],
    right: dict[str, Any],
    relevant: set[str],
    base_mapping: dict[str, str],
) -> Iterator[dict[str, str]]:
    """Enumerate one canonical representative for each isolated-node count vector.

    Nodes outside 'relevant' cannot participate in a matched edge under any
    label-preserving mapping, because every incident left edge has a coarse
    signature absent from the right skeleton.  Their identities therefore
    affect a common image only through typed multiplicity.
    """
    left_by_label: dict[str, list[str]] = {}
    for lid, node in left["nodes"].items():
        if lid in relevant:
            continue
        left_by_label.setdefault(_node_label(node), []).append(lid)
    for values in left_by_label.values():
        values.sort()

    used = set(base_mapping.values())
    right_by_label: dict[str, list[str]] = {}
    for rid, node in right["nodes"].items():
        if rid in used:
            continue
        right_by_label.setdefault(_node_label(node), []).append(rid)
    for values in right_by_label.values():
        values.sort()

    labels = sorted(set(left_by_label) & set(right_by_label))
    choices = [
        range(0, min(len(left_by_label[label]), len(right_by_label[label])) + 1)
        for label in labels
    ]
    if not labels:
        yield {}
        return

    for counts in itertools.product(*choices):
        extra: dict[str, str] = {}
        for label, count in zip(labels, counts):
            for lid, rid in zip(left_by_label[label][:count], right_by_label[label][:count]):
                extra[lid] = rid
        yield extra


def image_fingerprint(image: dict[str, Any]) -> str:
    """Cheap isomorphism invariant; exact equivalence is still checked in-bucket."""
    validate_image(image)
    node_counts = Counter(_node_label(node) for node in image["nodes"].values())
    labels = {node_id: _node_label(node) for node_id, node in image["nodes"].items()}
    edge_profiles = []
    for edge in image["edges"]:
        args = [labels[x] for x in edge["arguments"]]
        if not edge["ordered_arguments"]:
            args = sorted(args)
        edge_profiles.append(_canon({
            "family": edge["family"],
            "kind": edge["kind"],
            "ordered_arguments": edge["ordered_arguments"],
            "arguments": args,
            "conditional_on": sorted(labels[x] for x in edge["conditional_on"]),
            "temporal_direction": edge["temporal_direction"],
        }))
    return _canon({
        "active_axes": image["active_axes"],
        "node_counts": sorted(node_counts.items()),
        "edge_profiles": sorted(Counter(edge_profiles).items()),
        "temporal": image["temporal"],
        "controls": image["controls"],
    })


def append_if_new_equivalent_class(
    entries: list[dict[str, Any]],
    buckets: dict[str, list[int]],
    payload: dict[str, Any],
) -> tuple[int, bool]:
    fp = image_fingerprint(payload["image"])
    for index in buckets.get(fp, []):
        if image_equivalent(entries[index]["image"], payload["image"]):
            return index, False
    index = len(entries)
    entries.append(payload)
    buckets.setdefault(fp, []).append(index)
    return index, True


def possible_subobject(weak: dict[str, Any], strong: dict[str, Any]) -> bool:
    if not set(weak["active_axes"]) <= set(strong["active_axes"]):
        return False
    if len(weak["nodes"]) > len(strong["nodes"]) or len(weak["edges"]) > len(strong["edges"]):
        return False
    for key, value in weak["temporal"].items():
        if strong["temporal"].get(key) != value:
            return False
    for key, value in weak["controls"].items():
        if strong["controls"].get(key) != value:
            return False
    wc = Counter(_node_label(node) for node in weak["nodes"].values())
    sc = Counter(_node_label(node) for node in strong["nodes"].values())
    return all(sc[k] >= v for k, v in wc.items())


def optimized_pair_common_candidates(
    left: dict[str, Any],
    right: dict[str, Any],
) -> list[dict[str, Any]]:
    """Exact frozen-pilot candidate set with permutation-equivalent search pruning."""
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

    relevant = relevant_left_nodes(left, right)
    out: list[dict[str, Any]] = []
    buckets: dict[str, list[int]] = {}
    seen_core_outcomes: set[tuple[tuple[str, ...], tuple[int, ...]]] = set()
    seen_left_images: set[tuple[tuple[str, ...], tuple[int, ...]]] = set()

    for core_mapping in partial_relevant_mappings(left, right, relevant):
        left_edges, right_edges = matched_edge_indices(left, right, core_mapping)
        core_key = (tuple(sorted(core_mapping)), tuple(left_edges))
        if core_key in seen_core_outcomes:
            continue
        seen_core_outcomes.add(core_key)

        for extra in isolated_extra_mappings(left, right, relevant, core_mapping):
            mapping = dict(core_mapping)
            mapping.update(extra)
            if not mapping:
                continue

            left_nodes = sorted(mapping)
            right_nodes = sorted(mapping.values())
            raw_key = (tuple(left_nodes), tuple(left_edges))
            if raw_key in seen_left_images:
                continue
            seen_left_images.add(raw_key)

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
                raise LaneError("optimized pair witness failed equivalence check")

            append_if_new_equivalent_class(
                out,
                buckets,
                {
                    "image": left_image,
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
    return out


def canonical_image_object(image: dict[str, Any]) -> dict[str, Any]:
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
            dict(zip(ids, perm)) for perm in itertools.permutations(slots)
        ])

    best: str | None = None
    best_mapping: dict[str, str] | None = None
    for parts in itertools.product(*group_permutations):
        mapping: dict[str, str] = {}
        for part in parts:
            mapping.update(part)
        nodes = {mapping[nid]: image["nodes"][nid] for nid in image["nodes"]}
        edges = sorted(_edge_under_mapping(edge, mapping) for edge in image["edges"])
        candidate = _canon({
            "active_axes": image["active_axes"],
            "nodes": nodes,
            "edges": edges,
            "temporal": image["temporal"],
            "controls": image["controls"],
        })
        if best is None or candidate < best:
            best = candidate
            best_mapping = dict(mapping)

    if best_mapping is None:
        raise LaneError("empty candidate cannot be a retained Archetype image")

    out = {
        "schema_version": IMAGE_VERSION,
        "source_skeleton_version": image["source_skeleton_version"],
        "basis_version": image["basis_version"],
        "nodes": {
            best_mapping[nid]: copy.deepcopy(image["nodes"][nid])
            for nid in image["nodes"]
        },
        "edges": sorted(
            [json.loads(_edge_under_mapping(edge, best_mapping)) for edge in image["edges"]],
            key=_canon,
        ),
        "temporal": copy.deepcopy(image["temporal"]),
        "controls": copy.deepcopy(image["controls"]),
        "active_axes": list(image["active_axes"]),
    }
    return validate_image(out)


def embedding_mapping(image: dict[str, Any], strong: dict[str, Any]) -> dict[str, str] | None:
    if not set(image["active_axes"]) <= set(strong["active_axes"]):
        return None
    for key, value in image["temporal"].items():
        if strong["temporal"].get(key) != value:
            return None
    for key, value in image["controls"].items():
        if strong["controls"].get(key) != value:
            return None

    strong_by_label: dict[str, list[str]] = {}
    for sid, node in strong["nodes"].items():
        strong_by_label.setdefault(_node_label(node), []).append(sid)
    for values in strong_by_label.values():
        values.sort()

    order = sorted(
        image["nodes"],
        key=lambda x: (len(strong_by_label.get(_node_label(image["nodes"][x]), [])), x),
    )
    strong_identity = {x: x for x in strong["nodes"]}
    strong_edges = Counter(_edge_under_mapping(e, strong_identity) for e in strong["edges"])

    def partial_ok(mapping: dict[str, str]) -> bool:
        c: Counter[str] = Counter()
        for edge in image["edges"]:
            refs = edge["arguments"] + edge["conditional_on"]
            if all(ref in mapping for ref in refs):
                c[_edge_under_mapping(edge, mapping)] += 1
        return all(strong_edges[k] >= v for k, v in c.items())

    def rec(i: int, mapping: dict[str, str], used: set[str]) -> dict[str, str] | None:
        if i == len(order):
            c = Counter(_edge_under_mapping(e, mapping) for e in image["edges"])
            if all(strong_edges[k] >= v for k, v in c.items()):
                return dict(mapping)
            return None
        wid = order[i]
        label = _node_label(image["nodes"][wid])
        for sid in strong_by_label.get(label, []):
            if sid in used:
                continue
            mapping[wid] = sid
            used.add(sid)
            if partial_ok(mapping):
                found = rec(i + 1, mapping, used)
                if found is not None:
                    return found
            used.remove(sid)
            del mapping[wid]
        return None

    return rec(0, {}, set())


def membership_witness(image: dict[str, Any], skeleton: dict[str, Any]) -> dict[str, Any]:
    full = restrict_skeleton(
        skeleton,
        retained_node_ids=sorted(skeleton["nodes"]),
        retained_edge_indices=list(range(len(skeleton["edges"]))),
        retained_temporal_keys=_positive_temporal_keys(skeleton),
        retained_control_keys=_positive_control_keys(skeleton),
    )
    mapping = embedding_mapping(image, full)
    if mapping is None:
        raise LaneError("candidate support lacks an explicit embedding witness")

    identity = {x: x for x in skeleton["nodes"]}
    target_by_signature: dict[str, list[int]] = {}
    for i, edge in enumerate(skeleton["edges"]):
        target_by_signature.setdefault(_edge_under_mapping(edge, identity), []).append(i)

    cursors: Counter[str] = Counter()
    retained_edges: list[int] = []
    for edge in image["edges"]:
        sig = _edge_under_mapping(edge, mapping)
        options = target_by_signature.get(sig, [])
        cursor = cursors[sig]
        if cursor >= len(options):
            raise LaneError("witness edge multiplicity mismatch")
        retained_edges.append(options[cursor])
        cursors[sig] += 1

    witness = {
        "retained_node_ids": sorted(mapping.values()),
        "retained_edge_indices": sorted(retained_edges),
        "retained_temporal_keys": sorted(image["temporal"]),
        "retained_control_keys": sorted(image["controls"]),
    }
    restricted = restrict_skeleton(skeleton, **witness)
    if not image_equivalent(image, restricted):
        raise LaneError("explicit forgetting witness failed F_R equivalence")

    witness["forgotten_node_count"] = len(skeleton["nodes"]) - len(witness["retained_node_ids"])
    witness["forgotten_edge_count"] = len(skeleton["edges"]) - len(witness["retained_edge_indices"])
    witness["forgotten_temporal_keys"] = sorted(set(TEMPORAL_KEYS) - set(witness["retained_temporal_keys"]))
    witness["forgotten_control_keys"] = sorted(set(CONTROL_KEYS) - set(witness["retained_control_keys"]))
    return witness


def _compute_pair_job(
    payload: tuple[str, str, dict[str, Any], dict[str, Any]],
) -> tuple[str, str, bool, list[dict[str, Any]]]:
    left_id, right_id, left, right = payload
    return (
        left_id,
        right_id,
        skeleton_equivalent(left, right),
        optimized_pair_common_candidates(left, right),
    )


def run_lane() -> dict[str, Any]:
    skeletons, inputs = load_lane_skeletons()

    exact_equivalence_pairs: list[list[str]] = []
    all_candidates: list[dict[str, Any]] = []
    global_buckets: dict[str, list[int]] = {}
    pair_candidate_counts: dict[str, int] = {}

    pair_jobs = [
        (left_id, right_id, skeletons[left_id], skeletons[right_id])
        for i, left_id in enumerate(LANE_IDS)
        for right_id in LANE_IDS[i + 1:]
    ]
    with ProcessPoolExecutor(max_workers=min(4, len(pair_jobs))) as executor:
        pair_results = list(executor.map(_compute_pair_job, pair_jobs))

    for left_id, right_id, is_equivalent, candidates in pair_results:
        if is_equivalent:
            exact_equivalence_pairs.append([left_id, right_id])
        pair_key = f"{left_id}::{right_id}"
        pair_candidate_counts[pair_key] = len(candidates)
        for payload in candidates:
            index, is_new = append_if_new_equivalent_class(
                all_candidates,
                global_buckets,
                {"image": payload["image"], "pair_witnesses": {}},
            )
            all_candidates[index]["pair_witnesses"][pair_key] = {
                left_id: payload["left_witness"],
                right_id: payload["right_witness"],
            }

    support_groups: dict[tuple[str, ...], list[int]] = {}
    for index, payload in enumerate(all_candidates):
        image = payload["image"]
        support = tuple(
            claim_id for claim_id in LANE_IDS
            if image_embeds_in_skeleton(image, skeletons[claim_id])
        )
        if len(support) < 2:
            continue
        payload["support"] = support
        support_groups.setdefault(support, []).append(index)

    maximal: list[dict[str, Any]] = []
    maximal_image_by_id: dict[str, dict[str, Any]] = {}
    maximal_ids_by_support: dict[tuple[str, ...], list[str]] = {}

    for support, indices in sorted(support_groups.items()):
        ordered = sorted(
            indices,
            key=lambda k: (
                -len(all_candidates[k]["image"]["nodes"]),
                -len(all_candidates[k]["image"]["edges"]),
                image_fingerprint(all_candidates[k]["image"]),
                k,
            ),
        )
        for index in ordered:
            image = all_candidates[index]["image"]
            dominated = False
            for other_index in ordered:
                if other_index == index:
                    continue
                other = all_candidates[other_index]["image"]
                if len(other["nodes"]) < len(image["nodes"]):
                    break
                if not possible_subobject(image, other):
                    continue
                if image_embeds_in_image(image, other) and not image_equivalent(image, other):
                    dominated = True
                    break
            if dominated:
                continue

            summary = summarize_image(image)
            summary["member_claim_ids"] = list(support)
            summary["support_size"] = len(support)
            summary["witness_pair_count"] = len(all_candidates[index]["pair_witnesses"])
            summary["structural_image"] = canonical_image_object(image)
            summary["membership_witnesses"] = {
                claim_id: membership_witness(image, skeletons[claim_id])
                for claim_id in support
            }
            maximal.append(summary)
            maximal_image_by_id[summary["archetype_id"]] = image
            maximal_ids_by_support.setdefault(support, []).append(summary["archetype_id"])

    maximal.sort(key=lambda x: (
        -x["support_size"],
        -x["node_count"],
        -x["edge_count"],
        x["archetype_id"],
    ))
    for values in maximal_ids_by_support.values():
        values.sort()

    relation_counts = Counter()
    candidate_relations: list[dict[str, str]] = []
    for i, a in enumerate(maximal):
        for b in maximal[i + 1:]:
            ia = maximal_image_by_id[a["archetype_id"]]
            ib = maximal_image_by_id[b["archetype_id"]]
            ab = possible_subobject(ia, ib) and image_embeds_in_image(ia, ib)
            ba = possible_subobject(ib, ia) and image_embeds_in_image(ib, ia)
            if ab and ba:
                relation = "EQUIVALENT"
            elif ab:
                relation = "LEFT_SUBOBJECT_OF_RIGHT"
            elif ba:
                relation = "RIGHT_SUBOBJECT_OF_LEFT"
            else:
                relation = "INCOMPARABLE"
            relation_counts[relation] += 1
            candidate_relations.append({
                "left_archetype_id": a["archetype_id"],
                "right_archetype_id": b["archetype_id"],
                "relation": relation,
            })

    support_sets = []
    for support, indices in sorted(support_groups.items()):
        support_sets.append({
            "member_claim_ids": list(support),
            "unique_common_image_count": len(indices),
            "maximal_archetype_ids": maximal_ids_by_support.get(support, []),
        })

    if not maximal:
        decision = "ONLY_TRIVIAL_COMMON_STRUCTURE"
    elif len(maximal) == 1:
        decision = "ARCHETYPE_FAMILY_RECONSTRUCTION_SUPPORTED"
    elif relation_counts["INCOMPARABLE"] > 0:
        decision = "MULTIPLE_INCOMPARABLE_ARCHETYPES_SUPPORTED"
    else:
        decision = "ARCHETYPE_FAMILY_RECONSTRUCTION_SUPPORTED"

    return {
        "schema_version": "paper2-prd-archetype-lane-v1",
        "owner_issue": OWNER_ISSUE,
        "parent_issue": PARENT_ISSUE,
        "grammar_issue": GRAMMAR_ISSUE,
        "reference_pilot_issue": REFERENCE_PILOT_ISSUE,
        "reference_pilot_pr": REFERENCE_PILOT_PR,
        "input_main_commit": INPUT_MAIN,
        "input_claim_ids": LANE_IDS,
        "input_policy": "frozen reviewed ClaimIR + frozen structural adjudication only",
        "input_records": inputs,
        "abstraction_contract": {
            "stage1": "U_claim",
            "stage2": "F_R",
            "common_absence_as_positive_structure": False,
            "candidate_semantics": "frozen MEM pilot pair-common-image semantics",
            "enumeration_optimization": "exact isomorphism-bucket and permutation-equivalent search pruning; no candidate weakening",
        },
        "exact_basis_skeleton_equivalence_pairs": exact_equivalence_pairs,
        "pair_candidate_counts": pair_candidate_counts,
        "unique_nontrivial_common_image_count": len(all_candidates),
        "support_set_count": len(support_groups),
        "support_sets": support_sets,
        "maximal_archetype_candidate_count": len(maximal),
        "maximal_candidate_relation_summary": {
            "equivalent_pairs": relation_counts["EQUIVALENT"],
            "left_subobject_of_right_pairs": relation_counts["LEFT_SUBOBJECT_OF_RIGHT"],
            "right_subobject_of_left_pairs": relation_counts["RIGHT_SUBOBJECT_OF_LEFT"],
            "incomparable_pairs": relation_counts["INCOMPARABLE"],
            "comparable_pairs": (
                relation_counts["EQUIVALENT"]
                + relation_counts["LEFT_SUBOBJECT_OF_RIGHT"]
                + relation_counts["RIGHT_SUBOBJECT_OF_LEFT"]
            ),
        },
        "candidate_relations": candidate_relations,
        "archetype_candidates": maximal,
        "decision": decision,
        "construct_specificity_claim": False,
        "historical_labels_restored": False,
        "cross_lane_comparison": "NOT_RUN",
        "architecture_tuning": "NONE",
    }


def synthetic_equivalence_self_test() -> None:
    from paper2_basis_subobject_forgetting import _fixture

    left = _fixture(extra_left=True)
    right = _fixture(extra_right=True)

    # Add same-typed nodes that cannot participate in any shared edge.  This
    # exercises the exact permutation pruning used for larger PRD skeletons.
    left = copy.deepcopy(left)
    right = copy.deepcopy(right)
    left["nodes"]["basis:s_extra_left"] = copy.deepcopy(left["nodes"]["basis:s"])
    right["nodes"]["basis:s_extra_right"] = copy.deepcopy(right["nodes"]["basis:s"])
    validate_skeleton(left)
    validate_skeleton(right)

    frozen = list(pair_common_candidates(left, right).values())
    optimized = optimized_pair_common_candidates(left, right)
    if len(frozen) != len(optimized):
        raise AssertionError("optimized candidate count differs from frozen helper")
    for item in frozen:
        matches = [x for x in optimized if image_equivalent(item["image"], x["image"])]
        if len(matches) != 1:
            raise AssertionError("frozen candidate lacks unique optimized equivalent")
    for item in optimized:
        matches = [x for x in frozen if image_equivalent(item["image"], x["image"])]
        if len(matches) != 1:
            raise AssertionError("optimized candidate lacks unique frozen equivalent")


def self_test() -> None:
    synthetic_equivalence_self_test()
    skeletons, inputs = load_lane_skeletons()
    assert list(skeletons) == LANE_IDS
    assert [row["slot"] for row in inputs] == LANE_IDS
    assert all(row["structural_decision"] in {"PASS", "RESIDUAL"} for row in inputs)
    print("PAPER2_PRD_ARCHETYPE_LANE_V1_SELFTEST_PASS")


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

    report = run_lane()
    payload = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
