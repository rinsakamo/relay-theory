#!/usr/bin/env python3
"""Paper 2 #300: BLF six-object Archetype reconstruction.

This lane reuses the frozen #293 / merged #295 MEM-pilot machinery without
changing U_claim, F_R, B_P2, Phi, ClaimIR, or structural adjudication.

Pipeline:
    reviewed ClaimIR + adjudication
      -> structural signature
      -> Phi
      -> U_claim basis skeleton
      -> F_R common basis subobjects
      -> maximal non-trivial lane-local Archetype candidates

Candidate generation uses structural objects only. It does not inspect source
prose, construct labels, authors, venues, lexical similarity, embeddings,
clustering, MEM candidates, or other lane results.
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
from paper2_basis_structural_skeleton import project_basis_skeleton, skeleton_equivalent, validate_skeleton
from paper2_basis_subobject_forgetting import image_equivalent, restrict_skeleton, validate_image
from paper2_archetype_mem_pilot import (
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

BLF_IDS = [f"BLF0{i}" for i in range(1, 7)]
CLAIM_DIR = Path("research/paper2/chatgpt_reference_claimir_v1")
ADJ_DIR = Path("research/paper2/reference_structural_adjudication_v1")


class LaneError(ValueError):
    pass


def _canon(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha(value: Any) -> str:
    return hashlib.sha256(_canon(value).encode("utf-8")).hexdigest()


def load_blf_objects() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, str]]]:
    skeletons: dict[str, dict[str, Any]] = {}
    fingerprints: dict[str, dict[str, str]] = {}
    for claim_id in BLF_IDS:
        claim_path = CLAIM_DIR / f"{claim_id}.json"
        adj_path = ADJ_DIR / f"{claim_id}.json"
        claim = json.loads(claim_path.read_text(encoding="utf-8"))
        adjudication = json.loads(adj_path.read_text(encoding="utf-8"))

        if claim["extraction"]["manual_review_status"] != "reviewed":
            raise LaneError(f"{claim_id}: ClaimIR is not reviewed")
        if adjudication["decision"]["status"] not in {"PASS", "RESIDUAL"}:
            raise LaneError(f"{claim_id}: structural adjudication is not terminal")
        if adjudication["decision"]["status"] != "PASS":
            raise LaneError(f"{claim_id}: frozen structural input is RESIDUAL")

        structural = compile_record(claim, adjudication)
        phi = project_first(structural)
        skeleton = project_basis_skeleton(phi)
        validate_skeleton(skeleton)

        skeletons[claim_id] = skeleton
        fingerprints[claim_id] = {
            "claim_ir_sha256": hashlib.sha256(claim_path.read_bytes()).hexdigest(),
            "adjudication_sha256": hashlib.sha256(adj_path.read_bytes()).hexdigest(),
            "phi_sha256": _sha(phi),
            "u_claim_skeleton_sha256": _sha(skeleton),
        }
    return skeletons, fingerprints


def member_forgetting_witness(image: dict[str, Any], skeleton: dict[str, Any]) -> dict[str, Any]:
    """Return one deterministic explicit F_R witness from skeleton to image."""
    validate_image(image)
    validate_skeleton(skeleton)

    for key, value in image["temporal"].items():
        if skeleton["temporal"].get(key) != value:
            raise LaneError(f"temporal feature {key!r} not preserved in member")
    for key, value in image["controls"].items():
        if skeleton["controls"].get(key) != value:
            raise LaneError(f"control feature {key!r} not preserved in member")

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
    target_edge_signatures = [
        _edge_under_mapping(edge, identity)
        for edge in skeleton["edges"]
    ]

    def choose_edges(mapping: dict[str, str]) -> list[int] | None:
        used: set[int] = set()
        chosen: list[int] = []
        for edge in image["edges"]:
            sig = _edge_under_mapping(edge, mapping)
            found = None
            for idx, target_sig in enumerate(target_edge_signatures):
                if idx in used or target_sig != sig:
                    continue
                found = idx
                break
            if found is None:
                return None
            used.add(found)
            chosen.append(found)
        return chosen

    def partial_ok(mapping: dict[str, str]) -> bool:
        needed: Counter[str] = Counter()
        for edge in image["edges"]:
            refs = edge["arguments"] + edge["conditional_on"]
            if all(ref in mapping for ref in refs):
                needed[_edge_under_mapping(edge, mapping)] += 1
        available = Counter(target_edge_signatures)
        return all(available[k] >= v for k, v in needed.items())

    def rec(i: int, mapping: dict[str, str], used: set[str]):
        if i == len(order):
            edge_indices = choose_edges(mapping)
            if edge_indices is None:
                return None
            return dict(mapping), edge_indices

        iid = order[i]
        label = _node_label(image["nodes"][iid])
        for sid in target_by_label.get(label, []):
            if sid in used:
                continue
            mapping[iid] = sid
            used.add(sid)
            if partial_ok(mapping):
                result = rec(i + 1, mapping, used)
                if result is not None:
                    return result
            used.remove(sid)
            del mapping[iid]
        return None

    result = rec(0, {}, set())
    if result is None:
        raise LaneError("candidate support lacked explicit F_R embedding witness")
    mapping, retained_edge_indices = result

    retained_node_ids = sorted(mapping.values())
    retained_edge_indices = sorted(retained_edge_indices)
    retained_temporal_keys = sorted(image["temporal"])
    retained_control_keys = sorted(image["controls"])

    reconstructed = restrict_skeleton(
        skeleton,
        retained_node_ids=retained_node_ids,
        retained_edge_indices=retained_edge_indices,
        retained_temporal_keys=retained_temporal_keys,
        retained_control_keys=retained_control_keys,
    )
    if not image_equivalent(image, reconstructed):
        raise LaneError("explicit F_R witness does not reconstruct candidate image")

    positive_temporal = set(_positive_temporal_keys(skeleton))
    positive_controls = set(_positive_control_keys(skeleton))
    return {
        "image_to_member_node_mapping": dict(sorted(mapping.items())),
        "retained_node_ids": retained_node_ids,
        "retained_edge_indices": retained_edge_indices,
        "retained_temporal_keys": retained_temporal_keys,
        "retained_control_keys": retained_control_keys,
        "forgotten_node_ids": sorted(set(skeleton["nodes"]) - set(retained_node_ids)),
        "forgotten_edge_indices": sorted(set(range(len(skeleton["edges"]))) - set(retained_edge_indices)),
        "forgotten_positive_temporal_keys": sorted(positive_temporal - set(retained_temporal_keys)),
        "forgotten_positive_control_keys": sorted(positive_controls - set(retained_control_keys)),
        "witness_check": "F_R_RESTRICTION_EQUIVALENT",
    }


def retained_structure(image: dict[str, Any]) -> dict[str, Any]:
    """Canonical anonymous summary of exactly retained positive structure."""
    summary = summarize_image(image)
    return {
        "active_axes": summary["active_axes"],
        "node_count": summary["node_count"],
        "edge_count": summary["edge_count"],
        "nodes": summary["node_profile"],
        "edges": summary["edge_profile"],
        "temporal_features": summary["temporal_features"],
        "controls": summary["control_features"],
    }


def run_lane() -> dict[str, Any]:
    skeletons, fingerprints = load_blf_objects()

    exact_equivalence_pairs: list[list[str]] = []
    all_candidates: dict[str, dict[str, Any]] = {}
    pair_candidate_counts: dict[str, int] = {}

    for i, left_id in enumerate(BLF_IDS):
        for right_id in BLF_IDS[i + 1:]:
            left = skeletons[left_id]
            right = skeletons[right_id]

            if skeleton_equivalent(left, right):
                exact_equivalence_pairs.append([left_id, right_id])

            candidates = pair_common_candidates(left, right)
            pair_key = f"{left_id}::{right_id}"
            pair_candidate_counts[pair_key] = len(candidates)
            for key, payload in candidates.items():
                item = all_candidates.setdefault(key, {
                    "image": payload["image"],
                    "pair_forgetting_witnesses": {},
                })
                item["pair_forgetting_witnesses"][pair_key] = {
                    left_id: payload["left_witness"],
                    right_id: payload["right_witness"],
                }

    support_groups: dict[tuple[str, ...], list[tuple[str, dict[str, Any]]]] = {}
    for key, payload in all_candidates.items():
        image = payload["image"]
        support = tuple(
            claim_id
            for claim_id in BLF_IDS
            if image_embeds_in_skeleton(image, skeletons[claim_id])
        )
        if len(support) < 2:
            continue
        support_groups.setdefault(support, []).append((key, payload))

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
            summary["retained_structure"] = retained_structure(image)
            summary["member_forgetting_witnesses"] = {
                claim_id: member_forgetting_witness(image, skeletons[claim_id])
                for claim_id in support
            }
            summary["generating_pair_forgetting_witnesses"] = dict(
                sorted(payload["pair_forgetting_witnesses"].items())
            )
            maximal.append(summary)

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

    relation_pairs = []
    relation_counts = {
        "incomparable_pairs": 0,
        "comparable_pairs": 0,
        "equivalent_pairs": 0,
    }
    for i, left in enumerate(maximal):
        for right in maximal[i + 1:]:
            a = image_by_id[left["archetype_id"]]
            b = image_by_id[right["archetype_id"]]
            ab = image_embeds_in_image(a, b)
            ba = image_embeds_in_image(b, a)
            if ab and ba:
                relation = "EQUIVALENT"
                relation_counts["equivalent_pairs"] += 1
                relation_counts["comparable_pairs"] += 1
            elif ab:
                relation = "LEFT_SUBOBJECT_OF_RIGHT"
                relation_counts["comparable_pairs"] += 1
            elif ba:
                relation = "RIGHT_SUBOBJECT_OF_LEFT"
                relation_counts["comparable_pairs"] += 1
            else:
                relation = "INCOMPARABLE"
                relation_counts["incomparable_pairs"] += 1
            relation_pairs.append({
                "left_archetype_id": left["archetype_id"],
                "right_archetype_id": right["archetype_id"],
                "relation": relation,
            })

    support_sets = [
        {
            "member_claim_ids": list(support),
            "candidate_count_before_maximality": len(items),
            "maximal_archetype_ids": sorted(
                candidate["archetype_id"]
                for candidate in maximal
                if tuple(candidate["member_claim_ids"]) == support
            ),
        }
        for support, items in sorted(support_groups.items())
    ]

    if not maximal:
        decision = "BLF_ONLY_TRIVIAL_COMMON_STRUCTURE"
    elif len(maximal) == 1:
        decision = "BLF_ARCHETYPE_RECONSTRUCTION_SUPPORTED"
    elif relation_counts["incomparable_pairs"] > 0:
        decision = "BLF_MULTIPLE_INCOMPARABLE_ARCHETYPES"
    else:
        decision = "BLF_ARCHETYPE_RECONSTRUCTION_SUPPORTED"

    return {
        "schema_version": "paper2-blf-archetype-reconstruction-v1",
        "owner_issue": 300,
        "parent_issue": 283,
        "reference_pilot_issue": 295,
        "input_claim_ids": BLF_IDS,
        "input_policy": "frozen reviewed ClaimIR + frozen structural adjudication only",
        "input_fingerprints": fingerprints,
        "abstraction_contract": {
            "stage1": "U_claim",
            "stage2": "F_R",
            "common_absence_as_positive_structure": False,
            "grammar_source": "merged #293 / #295 machinery",
        },
        "exact_basis_skeleton_equivalence_pairs": exact_equivalence_pairs,
        "pair_candidate_counts": pair_candidate_counts,
        "unique_nontrivial_pair_generated_candidate_count": len(all_candidates),
        "support_set_count": len(support_groups),
        "support_sets": support_sets,
        "maximal_archetype_candidate_count": len(maximal),
        "maximal_candidate_relation_summary": relation_counts,
        "maximal_candidate_relations": relation_pairs,
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
    assert first["input_claim_ids"] == BLF_IDS
    assert first["abstraction_contract"]["stage1"] == "U_claim"
    assert first["abstraction_contract"]["stage2"] == "F_R"
    assert first["abstraction_contract"]["common_absence_as_positive_structure"] is False
    assert first["construct_specificity_claim"] is False
    assert first["cross_lane_comparison"] == "NOT_RUN"
    assert first["architecture_tuning"] == "NONE"

    for candidate in first["archetype_candidates"]:
        assert candidate["support_size"] >= 2
        assert set(candidate["member_forgetting_witnesses"]) == set(candidate["member_claim_ids"])
        for witness in candidate["member_forgetting_witnesses"].values():
            assert witness["witness_check"] == "F_R_RESTRICTION_EQUIVALENT"

    print("PAPER2_BLF_ARCHETYPE_RECONSTRUCTION_V1_SELFTEST_PASS")


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
