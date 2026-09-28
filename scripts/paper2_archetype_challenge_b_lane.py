#!/usr/bin/env python3
"""Paper 2 #308: Challenge-B six-object Archetype reconstruction lane.

Uses only frozen reviewed ClaimIR + reference structural adjudication inputs,
then the qualified #293 machinery:

    ClaimIR + adjudication
      -> compiled structural signature
      -> frozen Phi
      -> U_claim basis skeleton
      -> explicit F_R common basis subobjects
      -> maximal non-trivial common images

Candidate generation does not inspect source construct labels, authors, venues,
historical taxonomy, lexical similarity, embeddings, clustering, MEM Archetype
outcomes, or challenge-pressure labels.
"""

from __future__ import annotations

import argparse
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
    image_equivalent,
    is_nontrivial,
    restrict_skeleton,
    validate_image,
)

CLAIM_IDS = ["CH02", "CH04", "CH06", "CH08", "CH10", "CH12"]
CLAIM_DIR = Path("research/paper2/chatgpt_reference_claimir_v1")
ADJ_DIR = Path("research/paper2/reference_structural_adjudication_v1")
POSITIVE_STATE = "present"


class LaneError(ValueError):
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


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_skeletons() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, str]]]:
    skeletons: dict[str, dict[str, Any]] = {}
    fingerprints: dict[str, dict[str, str]] = {}
    for claim_id in CLAIM_IDS:
        claim_path = CLAIM_DIR / f"{claim_id}.json"
        adj_path = ADJ_DIR / f"{claim_id}.json"
        claim = json.loads(claim_path.read_text(encoding="utf-8"))
        adjudication = json.loads(adj_path.read_text(encoding="utf-8"))
        record = compile_record(claim, adjudication)
        phi = project_first(record)
        skeleton = project_basis_skeleton(phi)
        validate_skeleton(skeleton)
        skeletons[claim_id] = skeleton
        fingerprints[claim_id] = {
            "claim_ir_sha256": _sha256_file(claim_path),
            "structural_adjudication_sha256": _sha256_file(adj_path),
        }
    return skeletons, fingerprints


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
        best = _canon({
            "active_axes": image["active_axes"],
            "nodes": {},
            "edges": [],
            "temporal": image["temporal"],
            "controls": image["controls"],
        })
    return best


def canonical_image_object(image: dict[str, Any]) -> dict[str, Any]:
    obj = json.loads(canonical_image_key(image))
    obj["edges"] = [json.loads(x) for x in obj["edges"]]
    return obj


def image_id(image: dict[str, Any]) -> str:
    return "A-" + hashlib.sha256(canonical_image_key(image).encode("utf-8")).hexdigest()[:12]


def image_embeds_in_image(weak: dict[str, Any], strong: dict[str, Any]) -> bool:
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


def image_forgetting_witness_in_skeleton(
    image: dict[str, Any],
    skeleton: dict[str, Any],
) -> dict[str, Any] | None:
    """Return an explicit F_R witness if image embeds in skeleton."""
    validate_image(image)
    validate_skeleton(skeleton)

    for key, value in image["temporal"].items():
        if skeleton["temporal"].get(key) != value:
            return None
    for key, value in image["controls"].items():
        if skeleton["controls"].get(key) != value:
            return None

    target_by_label: dict[str, list[str]] = {}
    for sid, node in skeleton["nodes"].items():
        target_by_label.setdefault(_node_label(node), []).append(sid)
    for values in target_by_label.values():
        values.sort()

    order = sorted(
        image["nodes"],
        key=lambda x: (len(target_by_label.get(_node_label(image["nodes"][x]), [])), x),
    )
    identity = {x: x for x in skeleton["nodes"]}
    target_by_signature: dict[str, list[int]] = {}
    for i, edge in enumerate(skeleton["edges"]):
        target_by_signature.setdefault(_edge_under_mapping(edge, identity), []).append(i)

    def finalize(mapping: dict[str, str]) -> dict[str, Any] | None:
        cursors: Counter[str] = Counter()
        indices: list[int] = []
        for edge in image["edges"]:
            sig = _edge_under_mapping(edge, mapping)
            options = target_by_signature.get(sig, [])
            cursor = cursors[sig]
            if cursor >= len(options):
                return None
            indices.append(options[cursor])
            cursors[sig] += 1

        witness = {
            "retained_node_ids": sorted(mapping.values()),
            "retained_edge_indices": sorted(indices),
            "retained_temporal_keys": sorted(image["temporal"]),
            "retained_control_keys": sorted(image["controls"]),
        }
        rebuilt = restrict_skeleton(
            skeleton,
            retained_node_ids=witness["retained_node_ids"],
            retained_edge_indices=witness["retained_edge_indices"],
            retained_temporal_keys=witness["retained_temporal_keys"],
            retained_control_keys=witness["retained_control_keys"],
        )
        if not image_equivalent(image, rebuilt):
            return None
        return witness

    def partial_ok(mapping: dict[str, str]) -> bool:
        counts: Counter[str] = Counter()
        for edge in image["edges"]:
            refs = edge["arguments"] + edge["conditional_on"]
            if all(ref in mapping for ref in refs):
                counts[_edge_under_mapping(edge, mapping)] += 1
        return all(len(target_by_signature.get(sig, [])) >= count for sig, count in counts.items())

    def rec(i: int, mapping: dict[str, str], used: set[str]) -> dict[str, Any] | None:
        if i == len(order):
            return finalize(mapping)
        source_id = order[i]
        label = _node_label(image["nodes"][source_id])
        for target_id in target_by_label.get(label, []):
            if target_id in used:
                continue
            mapping[source_id] = target_id
            used.add(target_id)
            if partial_ok(mapping):
                witness = rec(i + 1, mapping, used)
                if witness is not None:
                    return witness
            used.remove(target_id)
            del mapping[source_id]
        return None

    return rec(0, {}, set())


def pair_common_candidates(
    left: dict[str, Any],
    right: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    temporal, controls = common_positive_features(left, right)
    out: dict[str, dict[str, Any]] = {}

    for mapping in partial_node_mappings(left, right):
        left_edges, right_edges = matched_edge_indices(left, right, mapping)
        left_nodes = sorted(mapping)
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
            raise LaneError("pair candidate witness failed equivalence check")

        key = canonical_image_key(left_image)
        if key not in out:
            out[key] = {"image": left_image}
    return out


def summarize_image(image: dict[str, Any]) -> dict[str, Any]:
    canonical = canonical_image_object(image)
    return {
        "archetype_id": image_id(image),
        "active_axes": canonical["active_axes"],
        "node_count": len(canonical["nodes"]),
        "edge_count": len(canonical["edges"]),
        "retained_nodes": canonical["nodes"],
        "retained_edges": canonical["edges"],
        "retained_temporal_features": canonical["temporal"],
        "retained_controls": canonical["controls"],
    }


def run_lane() -> dict[str, Any]:
    skeletons, fingerprints = load_skeletons()

    exact_equivalence_pairs: list[list[str]] = []
    all_candidates: dict[str, dict[str, Any]] = {}
    pair_candidate_counts: dict[str, int] = {}

    for i, left_id in enumerate(CLAIM_IDS):
        for right_id in CLAIM_IDS[i + 1:]:
            left = skeletons[left_id]
            right = skeletons[right_id]
            if skeleton_equivalent(left, right):
                exact_equivalence_pairs.append([left_id, right_id])

            candidates = pair_common_candidates(left, right)
            pair_candidate_counts[f"{left_id}::{right_id}"] = len(candidates)
            for key, payload in candidates.items():
                all_candidates.setdefault(key, {"image": payload["image"]})

    support_groups: dict[tuple[str, ...], list[tuple[str, dict[str, Any]]]] = {}
    for key, payload in all_candidates.items():
        image = payload["image"]
        member_witnesses: dict[str, dict[str, Any]] = {}
        for claim_id in CLAIM_IDS:
            witness = image_forgetting_witness_in_skeleton(image, skeletons[claim_id])
            if witness is not None:
                member_witnesses[claim_id] = witness
        support = tuple(claim_id for claim_id in CLAIM_IDS if claim_id in member_witnesses)
        if len(support) < 2:
            continue
        payload["member_witnesses"] = member_witnesses
        support_groups.setdefault(support, []).append((key, payload))

    maximal: list[dict[str, Any]] = []
    maximal_ids_by_support: dict[tuple[str, ...], list[str]] = {}
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
            summary["member_forgetting_witnesses"] = {
                claim_id: payload["member_witnesses"][claim_id]
                for claim_id in support
            }
            maximal.append(summary)
            maximal_ids_by_support.setdefault(support, []).append(summary["archetype_id"])

    maximal.sort(key=lambda x: (
        -x["support_size"],
        -x["node_count"],
        -x["edge_count"],
        x["archetype_id"],
    ))

    image_by_id = {
        image_id(payload["image"]): payload["image"]
        for payload in all_candidates.values()
    }
    relation_counts = Counter()
    pair_relations: list[dict[str, str]] = []
    for i, a in enumerate(maximal):
        for b in maximal[i + 1:]:
            ia = image_by_id[a["archetype_id"]]
            ib = image_by_id[b["archetype_id"]]
            ab = image_embeds_in_image(ia, ib)
            ba = image_embeds_in_image(ib, ia)
            if ab and ba:
                relation = "EQUIVALENT"
            elif ab:
                relation = "LEFT_EMBEDS_IN_RIGHT"
            elif ba:
                relation = "RIGHT_EMBEDS_IN_LEFT"
            else:
                relation = "INCOMPARABLE"
            relation_counts[relation] += 1
            pair_relations.append({
                "left_archetype_id": a["archetype_id"],
                "right_archetype_id": b["archetype_id"],
                "relation": relation,
            })

    support_sets = []
    for support, items in sorted(support_groups.items()):
        support_sets.append({
            "member_claim_ids": list(support),
            "candidate_count": len(items),
            "maximal_archetype_ids": sorted(maximal_ids_by_support.get(support, [])),
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
        "schema_version": "paper2-challenge-b-archetype-lane-v1",
        "owner_issue": 308,
        "parent_issue": 283,
        "input_claim_ids": CLAIM_IDS,
        "input_policy": "frozen reviewed ClaimIR + frozen reference structural adjudication only",
        "input_fingerprints": fingerprints,
        "abstraction_contract": {
            "stage1": "U_claim",
            "stage2": "F_R",
            "common_absence_as_positive_structure": False,
            "candidate_generation_logic": "same_as_merged_mem_reference_pilot",
            "historical_construct_labels_used": False,
            "cross_lane_archetypes_used": False,
        },
        "exact_basis_skeleton_equivalence_pairs": exact_equivalence_pairs,
        "pair_candidate_counts": pair_candidate_counts,
        "unique_nontrivial_pair_generated_candidate_count": len(all_candidates),
        "support_set_count": len(support_groups),
        "support_sets": support_sets,
        "maximal_archetype_candidate_count": len(maximal),
        "maximal_candidate_relation_summary": {
            "incomparable_pairs": relation_counts["INCOMPARABLE"],
            "comparable_pairs": (
                relation_counts["LEFT_EMBEDS_IN_RIGHT"]
                + relation_counts["RIGHT_EMBEDS_IN_LEFT"]
                + relation_counts["EQUIVALENT"]
            ),
            "equivalent_pairs": relation_counts["EQUIVALENT"],
            "left_embeds_in_right_pairs": relation_counts["LEFT_EMBEDS_IN_RIGHT"],
            "right_embeds_in_left_pairs": relation_counts["RIGHT_EMBEDS_IN_LEFT"],
        },
        "maximal_candidate_pair_relations": pair_relations,
        "archetype_candidates": maximal,
        "decision": decision,
        "historical_construct_naming_applied": False,
        "cross_lane_comparison": "NOT_RUN",
        "architecture_tuning": "NONE",
    }


def self_test() -> None:
    first = run_lane()
    second = run_lane()
    assert first == second
    assert first["input_claim_ids"] == CLAIM_IDS
    assert first["abstraction_contract"]["common_absence_as_positive_structure"] is False
    assert first["abstraction_contract"]["historical_construct_labels_used"] is False
    assert first["abstraction_contract"]["cross_lane_archetypes_used"] is False
    assert first["historical_construct_naming_applied"] is False
    assert first["cross_lane_comparison"] == "NOT_RUN"
    assert first["architecture_tuning"] == "NONE"
    for candidate in first["archetype_candidates"]:
        assert candidate["archetype_id"].startswith("A-")
        assert set(candidate["member_claim_ids"]) == set(candidate["member_forgetting_witnesses"])
    print("PAPER2_CHALLENGE_B_ARCHETYPE_LANE_V1_SELFTEST_PASS")


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
