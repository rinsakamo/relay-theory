#!/usr/bin/env python3
"""Paper 2 #304: independent Challenge A Archetype reconstruction.

Uses only frozen reviewed ClaimIR + merged reference structural adjudication
inputs and the same frozen #293 U_claim / F_R procedure used by the merged MEM
reference pilot. MEM Archetype outputs are never loaded.

    ClaimIR + adjudication
      -> compiled structural signature
      -> frozen Phi
      -> U_claim basis skeleton
      -> explicit F_R common basis subobjects
      -> maximal non-trivial common images

No source rereading, construct labels, lexical similarity, embeddings,
clustering, authors, venues, or other-lane outcomes enter candidate generation.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from paper2_reference_structural_adjudication import compile_record
from paper2_phi_compare import project_first
from paper2_basis_structural_skeleton import project_basis_skeleton, skeleton_equivalent, validate_skeleton
from paper2_basis_subobject_forgetting import image_equivalent, restrict_skeleton, validate_image
from paper2_archetype_mem_pilot import (
    _canon,
    _edge_under_mapping,
    _node_label,
    canonical_image_key,
    image_embeds_in_image,
    image_embeds_in_skeleton,
    image_id,
    pair_common_candidates,
    summarize_image,
)

LANE_IDS = ["CH01", "CH03", "CH05", "CH07", "CH09", "CH11"]
CLAIM_DIR = Path("research/paper2/chatgpt_reference_claimir_v1")
ADJ_DIR = Path("research/paper2/reference_structural_adjudication_v1")


class LaneError(ValueError):
    pass


def load_lane_skeletons() -> dict[str, dict[str, Any]]:
    out = {}
    for claim_id in LANE_IDS:
        claim = json.loads((CLAIM_DIR / f"{claim_id}.json").read_text(encoding="utf-8"))
        adjudication = json.loads((ADJ_DIR / f"{claim_id}.json").read_text(encoding="utf-8"))
        if claim["extraction"]["manual_review_status"] != "reviewed":
            raise LaneError(f"{claim_id}: ClaimIR is not reviewed")
        if adjudication["decision"]["status"] not in {"PASS", "RESIDUAL"}:
            raise LaneError(f"{claim_id}: structural adjudication is not terminal")
        record = compile_record(claim, adjudication)
        phi = project_first(record)
        skeleton = project_basis_skeleton(phi)
        validate_skeleton(skeleton)
        out[claim_id] = skeleton
    return out


def forgetting_witness(
    image: dict[str, Any],
    skeleton: dict[str, Any],
) -> dict[str, Any] | None:
    """Return the lexicographically first explicit F_R witness for image <= skeleton."""
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

    source_ids = sorted(
        image["nodes"],
        key=lambda x: (len(target_by_label.get(_node_label(image["nodes"][x]), [])), _node_label(image["nodes"][x]), x),
    )

    target_identity = {x: x for x in skeleton["nodes"]}
    target_edge_slots: dict[str, list[int]] = {}
    for idx, edge in enumerate(skeleton["edges"]):
        sig = _edge_under_mapping(edge, target_identity)
        target_edge_slots.setdefault(sig, []).append(idx)

    def complete_witness(mapping: dict[str, str]) -> dict[str, Any] | None:
        used_by_sig: Counter[str] = Counter()
        edge_indices: list[int] = []
        for edge in image["edges"]:
            sig = _edge_under_mapping(edge, mapping)
            slots = target_edge_slots.get(sig, [])
            cursor = used_by_sig[sig]
            if cursor >= len(slots):
                return None
            edge_indices.append(slots[cursor])
            used_by_sig[sig] += 1

        witness = {
            "retained_node_ids": sorted(mapping.values()),
            "retained_edge_indices": sorted(edge_indices),
            "retained_temporal_keys": sorted(image["temporal"]),
            "retained_control_keys": sorted(image["controls"]),
        }
        projected = restrict_skeleton(skeleton, **witness)
        if not image_equivalent(image, projected):
            return None
        return witness

    def rec(i: int, mapping: dict[str, str], used: set[str]) -> dict[str, Any] | None:
        if i == len(source_ids):
            return complete_witness(mapping)

        iid = source_ids[i]
        label = _node_label(image["nodes"][iid])
        for sid in target_by_label.get(label, []):
            if sid in used:
                continue
            mapping[iid] = sid
            used.add(sid)
            result = rec(i + 1, mapping, used)
            if result is not None:
                return result
            used.remove(sid)
            del mapping[iid]
        return None

    return rec(0, {}, set())


def run_lane() -> dict[str, Any]:
    skeletons = load_lane_skeletons()

    exact_equivalence_pairs: list[list[str]] = []
    all_candidates: dict[str, dict[str, Any]] = {}
    pair_candidate_counts: dict[str, int] = {}

    for i, left_id in enumerate(LANE_IDS):
        for right_id in LANE_IDS[i + 1:]:
            left = skeletons[left_id]
            right = skeletons[right_id]

            if skeleton_equivalent(left, right):
                exact_equivalence_pairs.append([left_id, right_id])

            candidates = pair_common_candidates(left, right)
            pair_candidate_counts[f"{left_id}::{right_id}"] = len(candidates)
            for key, payload in candidates.items():
                item = all_candidates.setdefault(key, {
                    "image": payload["image"],
                    "pair_witnesses": {},
                })
                item["pair_witnesses"][f"{left_id}::{right_id}"] = {
                    left_id: payload["left_witness"],
                    right_id: payload["right_witness"],
                }

    support_groups: dict[tuple[str, ...], list[tuple[str, dict[str, Any]]]] = {}
    for key, payload in all_candidates.items():
        image = payload["image"]
        support = tuple(
            claim_id for claim_id in LANE_IDS
            if image_embeds_in_skeleton(image, skeletons[claim_id])
        )
        if len(support) < 2:
            continue
        support_groups.setdefault(support, []).append((key, payload))

    maximal: list[dict[str, Any]] = []
    maximal_images: dict[str, dict[str, Any]] = {}
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
            witnesses = {}
            for claim_id in support:
                witness = forgetting_witness(image, skeletons[claim_id])
                if witness is None:
                    raise LaneError(
                        f"{summary['archetype_id']}: missing F_R witness for {claim_id}"
                    )
                witnesses[claim_id] = witness

            summary["member_claim_ids"] = list(support)
            summary["support_size"] = len(support)
            summary["member_forgetting_witnesses"] = witnesses
            summary["witness_pair_count"] = len(payload["pair_witnesses"])
            maximal.append(summary)
            maximal_images[summary["archetype_id"]] = image

    maximal.sort(key=lambda x: (
        -x["support_size"],
        -x["node_count"],
        -x["edge_count"],
        x["archetype_id"],
    ))

    pair_relations = []
    relation_counts = {
        "INCOMPARABLE": 0,
        "LEFT_SUBOBJECT_OF_RIGHT": 0,
        "RIGHT_SUBOBJECT_OF_LEFT": 0,
        "EQUIVALENT": 0,
    }
    for i, left in enumerate(maximal):
        for right in maximal[i + 1:]:
            a = maximal_images[left["archetype_id"]]
            b = maximal_images[right["archetype_id"]]
            ab = image_embeds_in_image(a, b)
            ba = image_embeds_in_image(b, a)
            if ab and ba:
                relation = "EQUIVALENT"
            elif ab:
                relation = "LEFT_SUBOBJECT_OF_RIGHT"
            elif ba:
                relation = "RIGHT_SUBOBJECT_OF_LEFT"
            else:
                relation = "INCOMPARABLE"
            relation_counts[relation] += 1
            pair_relations.append({
                "left_archetype_id": left["archetype_id"],
                "right_archetype_id": right["archetype_id"],
                "relation": relation,
            })

    if not maximal:
        decision = "CHALLENGE_A_ONLY_TRIVIAL_COMMON_STRUCTURE"
    elif len(maximal) == 1:
        decision = "CHALLENGE_A_ARCHETYPE_RECONSTRUCTION_SUPPORTED"
    elif relation_counts["INCOMPARABLE"] > 0:
        decision = "CHALLENGE_A_MULTIPLE_INCOMPARABLE_ARCHETYPES"
    else:
        decision = "CHALLENGE_A_ARCHETYPE_RECONSTRUCTION_SUPPORTED"

    support_sets = [
        list(support)
        for support in sorted(support_groups)
    ]

    return {
        "schema_version": "paper2-challenge-a-archetype-v1",
        "owner_issue": 304,
        "parent_issue": 283,
        "input_claim_ids": LANE_IDS,
        "input_policy": "frozen reviewed ClaimIR + merged reference structural adjudication only",
        "abstraction_contract": {
            "stage1": "U_claim",
            "stage2": "F_R",
            "reference_procedure": "merged MEM pilot machinery",
            "common_absence_as_positive_structure": False,
        },
        "exact_basis_skeleton_equivalence_pairs": exact_equivalence_pairs,
        "pair_candidate_counts": pair_candidate_counts,
        "unique_nontrivial_pair_generated_candidate_count": len(all_candidates),
        "support_set_count": len(support_groups),
        "support_sets": support_sets,
        "maximal_archetype_candidate_count": len(maximal),
        "maximal_candidate_relation_summary": relation_counts,
        "candidate_pair_relations": pair_relations,
        "archetype_candidates": maximal,
        "decision": decision,
        "construct_specificity_claim": False,
        "cross_lane_comparison": "NOT_RUN",
        "architecture_tuning": "NONE",
    }


def self_test() -> None:
    first = run_lane()
    second = run_lane()
    assert first == second
    assert first["input_claim_ids"] == LANE_IDS
    assert first["abstraction_contract"]["common_absence_as_positive_structure"] is False
    assert first["construct_specificity_claim"] is False
    assert first["cross_lane_comparison"] == "NOT_RUN"
    assert first["architecture_tuning"] == "NONE"
    for candidate in first["archetype_candidates"]:
        assert set(candidate["member_forgetting_witnesses"]) == set(candidate["member_claim_ids"])
        assert candidate["archetype_id"].startswith("A-")
    print("PAPER2_CHALLENGE_A_ARCHETYPE_V1_SELFTEST_PASS")


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
