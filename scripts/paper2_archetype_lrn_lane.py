#!/usr/bin/env python3
"""Paper 2 #301: LRN six-object Archetype reconstruction.

Uses only frozen reviewed ClaimIR + reference structural adjudication inputs
already present on main, followed by the frozen #293 abstraction grammar:

    ClaimIR + adjudication
      -> compiled structural signature
      -> Phi
      -> U_claim basis skeleton
      -> explicit F_R common basis subobjects
      -> maximal non-trivial common images

Candidate generation never consumes construct labels, lexical similarity,
embeddings, clustering output, or MEM Archetype results.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

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
    pair_common_candidates,
    summarize_image,
)

LRN_IDS = [f"LRN0{i}" for i in range(1, 7)]
CLAIM_DIR = Path("research/paper2/chatgpt_reference_claimir_v1")
ADJ_DIR = Path("research/paper2/reference_structural_adjudication_v1")


class LaneError(ValueError):
    pass


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_lrn_skeletons() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, str]]]:
    skeletons: dict[str, dict[str, Any]] = {}
    fingerprints: dict[str, dict[str, str]] = {}

    for lane_id in LRN_IDS:
        claim_path = CLAIM_DIR / f"{lane_id}.json"
        adj_path = ADJ_DIR / f"{lane_id}.json"
        claim = json.loads(claim_path.read_text(encoding="utf-8"))
        adjudication = json.loads(adj_path.read_text(encoding="utf-8"))

        if claim["extraction"]["manual_review_status"] != "reviewed":
            raise LaneError(f"{lane_id}: ClaimIR is not reviewed")
        if adjudication["decision"]["status"] != "PASS":
            raise LaneError(f"{lane_id}: structural adjudication is not PASS")

        record = compile_record(claim, adjudication)
        phi = project_first(record)
        skeleton = project_basis_skeleton(phi)
        validate_skeleton(skeleton)

        skeletons[lane_id] = skeleton
        fingerprints[lane_id] = {
            "claimir_sha256": _sha256(claim_path),
            "structural_adjudication_sha256": _sha256(adj_path),
        }

    return skeletons, fingerprints


def canonical_structural_object(image: dict[str, Any]) -> dict[str, Any]:
    """Return the anonymous-ID canonical F_R image as a normal JSON object."""
    validate_image(image)
    core = json.loads(canonical_image_key(image))
    core["edges"] = [json.loads(edge) for edge in core["edges"]]
    return {
        "schema_version": image["schema_version"],
        "source_skeleton_version": image["source_skeleton_version"],
        "basis_version": image["basis_version"],
        "active_axes": core["active_axes"],
        "nodes": core["nodes"],
        "edges": core["edges"],
        "temporal": core["temporal"],
        "controls": core["controls"],
    }


def _target_edge_indices_for_mapping(
    image: dict[str, Any],
    skeleton: dict[str, Any],
    mapping: dict[str, str],
) -> list[int] | None:
    target_identity = {node_id: node_id for node_id in skeleton["nodes"]}
    target_by_sig: dict[str, list[int]] = {}
    for index, edge in enumerate(skeleton["edges"]):
        sig = _edge_under_mapping(edge, target_identity)
        target_by_sig.setdefault(sig, []).append(index)

    cursors: Counter[str] = Counter()
    retained: list[int] = []
    for edge in image["edges"]:
        sig = _edge_under_mapping(edge, mapping)
        options = target_by_sig.get(sig, [])
        cursor = cursors[sig]
        if cursor >= len(options):
            return None
        retained.append(options[cursor])
        cursors[sig] += 1
    return sorted(retained)


def explicit_f_r_witness(
    image: dict[str, Any],
    skeleton: dict[str, Any],
) -> dict[str, Any]:
    """Find one deterministic exact F_R restriction witness for image <= skeleton."""
    validate_image(image)
    validate_skeleton(skeleton)

    for key, value in image["temporal"].items():
        if skeleton["temporal"].get(key) != value:
            raise LaneError("temporal feature is not preserved")
    for key, value in image["controls"].items():
        if skeleton["controls"].get(key) != value:
            raise LaneError("control feature is not preserved")

    target_by_label: dict[str, list[str]] = {}
    for target_id, node in skeleton["nodes"].items():
        target_by_label.setdefault(_node_label(node), []).append(target_id)
    for values in target_by_label.values():
        values.sort()

    order = sorted(
        image["nodes"],
        key=lambda node_id: (
            len(target_by_label.get(_node_label(image["nodes"][node_id]), [])),
            _node_label(image["nodes"][node_id]),
            node_id,
        ),
    )
    target_identity = {node_id: node_id for node_id in skeleton["nodes"]}
    target_edges = Counter(
        _edge_under_mapping(edge, target_identity)
        for edge in skeleton["edges"]
    )

    def partial_ok(mapping: dict[str, str]) -> bool:
        seen: Counter[str] = Counter()
        for edge in image["edges"]:
            refs = edge["arguments"] + edge["conditional_on"]
            if all(ref in mapping for ref in refs):
                seen[_edge_under_mapping(edge, mapping)] += 1
        return all(target_edges[sig] >= count for sig, count in seen.items())

    chosen_mapping: dict[str, str] | None = None
    chosen_edges: list[int] | None = None

    def rec(i: int, mapping: dict[str, str], used: set[str]) -> bool:
        nonlocal chosen_mapping, chosen_edges
        if i == len(order):
            edges = _target_edge_indices_for_mapping(image, skeleton, mapping)
            if edges is None:
                return False
            chosen_mapping = dict(mapping)
            chosen_edges = edges
            return True

        source_id = order[i]
        label = _node_label(image["nodes"][source_id])
        for target_id in target_by_label.get(label, []):
            if target_id in used:
                continue
            mapping[source_id] = target_id
            used.add(target_id)
            if partial_ok(mapping) and rec(i + 1, mapping, used):
                return True
            used.remove(target_id)
            del mapping[source_id]
        return False

    if not rec(0, {}, set()) or chosen_mapping is None or chosen_edges is None:
        raise LaneError("failed to construct explicit F_R witness")

    retained_nodes = sorted(chosen_mapping.values())
    retained_temporal = sorted(image["temporal"])
    retained_controls = sorted(image["controls"])

    projected = restrict_skeleton(
        skeleton,
        retained_node_ids=retained_nodes,
        retained_edge_indices=chosen_edges,
        retained_temporal_keys=retained_temporal,
        retained_control_keys=retained_controls,
    )
    if not image_equivalent(image, projected):
        raise LaneError("explicit F_R witness does not reproduce candidate image")

    return {
        "retained_node_ids": retained_nodes,
        "retained_edge_indices": chosen_edges,
        "retained_temporal_keys": retained_temporal,
        "retained_control_keys": retained_controls,
        "forgotten_node_ids": sorted(set(skeleton["nodes"]) - set(retained_nodes)),
        "forgotten_edge_indices": [
            i for i in range(len(skeleton["edges"])) if i not in set(chosen_edges)
        ],
        "forgotten_temporal_keys": sorted(set(TEMPORAL_KEYS) - set(retained_temporal)),
        "forgotten_control_keys": sorted(set(CONTROL_KEYS) - set(retained_controls)),
    }


def run_lane() -> dict[str, Any]:
    skeletons, fingerprints = load_lrn_skeletons()

    exact_equivalence_pairs: list[list[str]] = []
    all_candidates: dict[str, dict[str, Any]] = {}
    pair_candidate_counts: dict[str, int] = {}

    for i, left_id in enumerate(LRN_IDS):
        for right_id in LRN_IDS[i + 1:]:
            left = skeletons[left_id]
            right = skeletons[right_id]

            if skeleton_equivalent(left, right):
                exact_equivalence_pairs.append([left_id, right_id])

            candidates = pair_common_candidates(left, right)
            pair_key = f"{left_id}::{right_id}"
            pair_candidate_counts[pair_key] = len(candidates)
            for key, payload in candidates.items():
                item = all_candidates.setdefault(
                    key,
                    {
                        "image": payload["image"],
                        "pair_witnesses": {},
                    },
                )
                item["pair_witnesses"][pair_key] = {
                    left_id: payload["left_witness"],
                    right_id: payload["right_witness"],
                }

    support_groups: dict[tuple[str, ...], list[tuple[str, dict[str, Any]]]] = {}
    for key, payload in all_candidates.items():
        image = payload["image"]
        support = tuple(
            lane_id
            for lane_id in LRN_IDS
            if image_embeds_in_skeleton(image, skeletons[lane_id])
        )
        if len(support) < 2:
            continue
        support_groups.setdefault(support, []).append((key, payload))

    maximal: list[dict[str, Any]] = []
    image_by_id = {
        image_id(payload["image"]): payload["image"]
        for payload in all_candidates.values()
    }

    for support, items in sorted(support_groups.items()):
        for key, payload in items:
            image = payload["image"]
            dominated = False
            for other_key, other_payload in items:
                if other_key == key:
                    continue
                other = other_payload["image"]
                if (
                    image_embeds_in_image(image, other)
                    and not image_equivalent(image, other)
                ):
                    dominated = True
                    break
            if dominated:
                continue

            summary = summarize_image(image)
            summary["archetype_structural_object"] = canonical_structural_object(image)
            summary["member_claim_ids"] = list(support)
            summary["support_size"] = len(support)
            summary["witness_pair_count"] = len(payload["pair_witnesses"])
            summary["membership_witnesses"] = {
                lane_id: explicit_f_r_witness(image, skeletons[lane_id])
                for lane_id in support
            }
            maximal.append(summary)

    maximal.sort(
        key=lambda x: (
            -x["support_size"],
            -x["node_count"],
            -x["edge_count"],
            x["archetype_id"],
        )
    )

    maximal_ids_by_support: dict[tuple[str, ...], list[str]] = {}
    for candidate in maximal:
        support = tuple(candidate["member_claim_ids"])
        maximal_ids_by_support.setdefault(support, []).append(candidate["archetype_id"])
    for ids in maximal_ids_by_support.values():
        ids.sort()

    support_sets = []
    for support, items in sorted(
        support_groups.items(),
        key=lambda item: (-len(item[0]), item[0]),
    ):
        support_sets.append({
            "member_claim_ids": list(support),
            "support_size": len(support),
            "nontrivial_common_image_count": len(items),
            "maximal_archetype_candidate_ids": maximal_ids_by_support.get(support, []),
        })

    candidate_relations = []
    incomparable_pairs = 0
    comparable_pairs = 0
    for i, left in enumerate(maximal):
        for right in maximal[i + 1:]:
            left_image = image_by_id[left["archetype_id"]]
            right_image = image_by_id[right["archetype_id"]]
            left_in_right = image_embeds_in_image(left_image, right_image)
            right_in_left = image_embeds_in_image(right_image, left_image)

            if left_in_right and right_in_left:
                relation = "EQUIVALENT"
                comparable_pairs += 1
            elif left_in_right:
                relation = "LEFT_EMBEDS_IN_RIGHT"
                comparable_pairs += 1
            elif right_in_left:
                relation = "RIGHT_EMBEDS_IN_LEFT"
                comparable_pairs += 1
            else:
                relation = "INCOMPARABLE"
                incomparable_pairs += 1

            candidate_relations.append({
                "left_archetype_id": left["archetype_id"],
                "right_archetype_id": right["archetype_id"],
                "relation": relation,
            })

    if not maximal:
        decision = "LRN_ONLY_TRIVIAL_COMMON_STRUCTURE"
    elif len(maximal) == 1:
        decision = "LRN_ARCHETYPE_RECONSTRUCTION_SUPPORTED"
    elif incomparable_pairs > 0:
        decision = "LRN_MULTIPLE_INCOMPARABLE_ARCHETYPES"
    else:
        decision = "LRN_ARCHETYPE_RECONSTRUCTION_SUPPORTED"

    return {
        "schema_version": "paper2-lrn-archetype-reconstruction-v1",
        "owner_issue": 301,
        "parent_issue": 283,
        "grammar_issue": 293,
        "reference_pilot_issue": 295,
        "input_claim_ids": LRN_IDS,
        "input_policy": "frozen reviewed ClaimIR + reference structural adjudication only",
        "input_fingerprints": fingerprints,
        "input_validation": {
            "all_claimir_reviewed": True,
            "all_structural_adjudications_pass": True,
        },
        "abstraction_contract": {
            "stage1": "U_claim",
            "stage2": "F_R",
            "common_absence_as_positive_structure": False,
            "candidate_generation_uses_construct_labels": False,
            "candidate_generation_uses_lexical_similarity": False,
            "candidate_generation_uses_embeddings_or_clustering": False,
            "candidate_generation_uses_mem_archetypes": False,
        },
        "exact_basis_skeleton_equivalence_pairs": exact_equivalence_pairs,
        "pair_candidate_counts": pair_candidate_counts,
        "unique_nontrivial_pair_generated_candidate_count": len(all_candidates),
        "support_set_count": len(support_groups),
        "support_sets": support_sets,
        "maximal_archetype_candidate_count": len(maximal),
        "maximal_candidate_relation_summary": {
            "incomparable_pairs": incomparable_pairs,
            "comparable_pairs": comparable_pairs,
        },
        "maximal_candidate_relations": candidate_relations,
        "archetype_candidates": maximal,
        "decision": decision,
        "historical_labels_restored_post_hoc": False,
        "cross_lane_comparison_performed": False,
        "construct_specificity_claim": False,
        "architecture_tuning": "NONE",
    }


def self_test() -> None:
    first = run_lane()
    second = run_lane()
    assert first == second
    assert first["input_claim_ids"] == LRN_IDS
    assert first["historical_labels_restored_post_hoc"] is False
    assert first["cross_lane_comparison_performed"] is False
    assert first["construct_specificity_claim"] is False
    assert first["architecture_tuning"] == "NONE"

    skeletons, _ = load_lrn_skeletons()
    for candidate in first["archetype_candidates"]:
        image = candidate["archetype_structural_object"]
        validate_image(image)
        for lane_id, witness in candidate["membership_witnesses"].items():
            projected = restrict_skeleton(
                skeletons[lane_id],
                retained_node_ids=witness["retained_node_ids"],
                retained_edge_indices=witness["retained_edge_indices"],
                retained_temporal_keys=witness["retained_temporal_keys"],
                retained_control_keys=witness["retained_control_keys"],
            )
            assert image_equivalent(image, projected)

    print("PAPER2_LRN_ARCHETYPE_RECONSTRUCTION_V1_SELFTEST_PASS")


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
