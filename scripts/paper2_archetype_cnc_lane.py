#!/usr/bin/env python3
"""Paper 2 #299: CNC lane-local Archetype reconstruction.

Uses only frozen reviewed CNC ClaimIR + reference structural adjudication inputs
and the already-frozen #293 / #295 machinery:

    ClaimIR + adjudication
      -> compiled structural signature
      -> Phi
      -> U_claim basis skeleton
      -> F_R common basis subobjects
      -> maximal non-trivial common images

Candidate generation does not inspect construct labels, source prose, authors,
venues, embeddings, clusters, MEM Archetypes, or any other lane result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from paper2_reference_structural_adjudication import compile_record
from paper2_phi_compare import project_first
from paper2_basis_structural_skeleton import (
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
    canonical_image_key,
    image_embeds_in_image,
    image_embeds_in_skeleton,
    image_id,
    matched_edge_indices,
    pair_common_candidates,
    partial_node_mappings,
    summarize_image,
)

CNC_IDS = [f"CNC0{i}" for i in range(1, 7)]
CLAIM_DIR = Path("research/paper2/chatgpt_reference_claimir_v1")
ADJ_DIR = Path("research/paper2/reference_structural_adjudication_v1")


class LaneError(ValueError):
    pass


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_cnc_skeletons() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, str]]]:
    skeletons: dict[str, dict[str, Any]] = {}
    frozen_inputs: dict[str, dict[str, str]] = {}
    for claim_id in CNC_IDS:
        claim_path = CLAIM_DIR / f"{claim_id}.json"
        adj_path = ADJ_DIR / f"{claim_id}.json"
        claim = json.loads(claim_path.read_text(encoding="utf-8"))
        adjudication = json.loads(adj_path.read_text(encoding="utf-8"))

        if claim["extraction"]["manual_review_status"] != "reviewed":
            raise LaneError(f"{claim_id}: ClaimIR is not reviewed")
        if adjudication["decision"]["status"] not in {"PASS", "RESIDUAL"}:
            raise LaneError(f"{claim_id}: unexpected adjudication decision")

        record = compile_record(claim, adjudication)
        phi = project_first(record)
        skeleton = project_basis_skeleton(phi)
        validate_skeleton(skeleton)
        skeletons[claim_id] = skeleton
        frozen_inputs[claim_id] = {
            "claim_ir_sha256": _file_sha256(claim_path),
            "structural_adjudication_sha256": _file_sha256(adj_path),
        }
    return skeletons, frozen_inputs


def forgetting_witness(image: dict[str, Any], skeleton: dict[str, Any]) -> dict[str, Any]:
    """Return the first deterministic explicit F_R witness for image <= skeleton."""
    validate_image(image)
    validate_skeleton(skeleton)

    temporal_keys = sorted(image["temporal"])
    control_keys = sorted(image["controls"])

    for mapping in partial_node_mappings(image, skeleton):
        if set(mapping) != set(image["nodes"]):
            continue
        if any(skeleton["temporal"][key] != image["temporal"][key] for key in temporal_keys):
            continue
        if any(skeleton["controls"][key] != image["controls"][key] for key in control_keys):
            continue

        image_edge_indices, skeleton_edge_indices = matched_edge_indices(image, skeleton, mapping)
        if image_edge_indices != list(range(len(image["edges"]))):
            continue

        witness = {
            "retained_node_ids": sorted(mapping.values()),
            "retained_edge_indices": skeleton_edge_indices,
            "retained_temporal_keys": temporal_keys,
            "retained_control_keys": control_keys,
        }
        reconstructed = restrict_skeleton(
            skeleton,
            retained_node_ids=witness["retained_node_ids"],
            retained_edge_indices=witness["retained_edge_indices"],
            retained_temporal_keys=witness["retained_temporal_keys"],
            retained_control_keys=witness["retained_control_keys"],
        )
        if image_equivalent(image, reconstructed):
            return witness

    raise LaneError("no explicit F_R witness for claimed member")


def _candidate_relation(left: dict[str, Any], right: dict[str, Any]) -> str:
    lr = image_embeds_in_image(left, right)
    rl = image_embeds_in_image(right, left)
    if lr and rl:
        return "EQUIVALENT"
    if lr:
        return "LEFT_EMBEDS_IN_RIGHT"
    if rl:
        return "RIGHT_EMBEDS_IN_LEFT"
    return "INCOMPARABLE"


def run_lane() -> dict[str, Any]:
    skeletons, frozen_inputs = load_cnc_skeletons()

    exact_equivalence_pairs: list[list[str]] = []
    all_candidates: dict[str, dict[str, Any]] = {}
    pair_candidate_counts: dict[str, int] = {}

    for i, left_id in enumerate(CNC_IDS):
        for right_id in CNC_IDS[i + 1:]:
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
                    {"image": payload["image"], "pair_witnesses": {}},
                )
                item["pair_witnesses"][pair_key] = {
                    left_id: payload["left_witness"],
                    right_id: payload["right_witness"],
                }

    support_groups: dict[tuple[str, ...], list[tuple[str, dict[str, Any]]]] = {}
    for key, payload in all_candidates.items():
        image = payload["image"]
        support = tuple(
            claim_id
            for claim_id in CNC_IDS
            if image_embeds_in_skeleton(image, skeletons[claim_id])
        )
        if len(support) < 2:
            continue
        support_groups.setdefault(support, []).append((key, payload))

    maximal_payloads: list[dict[str, Any]] = []
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
            summary["generation_witness_pairs"] = sorted(payload["pair_witnesses"])
            summary["forgetting_witnesses"] = {
                claim_id: forgetting_witness(image, skeletons[claim_id])
                for claim_id in support
            }
            maximal_payloads.append({"summary": summary, "image": image})
            maximal_ids_by_support.setdefault(support, []).append(summary["archetype_id"])

    maximal_payloads.sort(
        key=lambda x: (
            -x["summary"]["support_size"],
            -x["summary"]["node_count"],
            -x["summary"]["edge_count"],
            x["summary"]["archetype_id"],
        )
    )
    maximal = [item["summary"] for item in maximal_payloads]

    relation_pairs = []
    incomparable_pairs = 0
    comparable_pairs = 0
    for i, left in enumerate(maximal_payloads):
        for right in maximal_payloads[i + 1:]:
            relation = _candidate_relation(left["image"], right["image"])
            if relation == "INCOMPARABLE":
                incomparable_pairs += 1
            else:
                comparable_pairs += 1
            relation_pairs.append({
                "left_archetype_id": left["summary"]["archetype_id"],
                "right_archetype_id": right["summary"]["archetype_id"],
                "relation": relation,
            })

    support_sets = []
    for support, items in sorted(support_groups.items()):
        support_sets.append({
            "member_claim_ids": list(support),
            "unique_common_image_count": len(items),
            "maximal_archetype_ids": sorted(maximal_ids_by_support.get(support, [])),
        })

    if not maximal:
        decision = "ONLY_TRIVIAL_COMMON_STRUCTURE"
    elif len(maximal) == 1:
        decision = "ARCHETYPE_FAMILY_RECONSTRUCTION_SUPPORTED"
    elif incomparable_pairs > 0:
        decision = "MULTIPLE_INCOMPARABLE_ARCHETYPES_SUPPORTED"
    else:
        decision = "ARCHETYPE_FAMILY_RECONSTRUCTION_SUPPORTED"

    return {
        "schema_version": "paper2-cnc-archetype-lane-v1",
        "owner_issue": 299,
        "parent_issue": 283,
        "grammar_issue": 293,
        "reference_pilot_pr": 296,
        "input_claim_ids": CNC_IDS,
        "frozen_input_sha256": frozen_inputs,
        "input_policy": "frozen reviewed ClaimIR + reference structural adjudication only",
        "abstraction_contract": {
            "stage1": "U_claim",
            "stage2": "F_R",
            "grammar_reused_from_reference_pilot": True,
            "common_absence_as_positive_structure": False,
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
        "maximal_candidate_relations": relation_pairs,
        "archetype_candidates": maximal,
        "decision": decision,
        "construct_specificity_claim": False,
        "cross_lane_comparison": "NOT_RUN",
        "pairwise_phi_comparison": "NOT_RUN",
        "atlas": "NOT_RUN",
        "architecture_tuning": "NONE",
    }


def self_test() -> None:
    first = run_lane()
    second = run_lane()
    assert first == second
    assert first["input_claim_ids"] == CNC_IDS
    assert first["abstraction_contract"]["common_absence_as_positive_structure"] is False
    assert first["construct_specificity_claim"] is False
    assert first["cross_lane_comparison"] == "NOT_RUN"
    assert first["architecture_tuning"] == "NONE"

    skeletons, _ = load_cnc_skeletons()
    for candidate in first["archetype_candidates"]:
        # Recover the canonical image from a generating pair candidate.
        target_id = candidate["archetype_id"]
        recovered = None
        for i, left_id in enumerate(CNC_IDS):
            for right_id in CNC_IDS[i + 1:]:
                for payload in pair_common_candidates(
                    skeletons[left_id], skeletons[right_id]
                ).values():
                    if image_id(payload["image"]) == target_id:
                        recovered = payload["image"]
                        break
                if recovered is not None:
                    break
            if recovered is not None:
                break
        if recovered is None:
            raise LaneError(f"cannot recover {target_id}")
        for claim_id, witness in candidate["forgetting_witnesses"].items():
            image = restrict_skeleton(
                skeletons[claim_id],
                retained_node_ids=witness["retained_node_ids"],
                retained_edge_indices=witness["retained_edge_indices"],
                retained_temporal_keys=witness["retained_temporal_keys"],
                retained_control_keys=witness["retained_control_keys"],
            )
            assert image_equivalent(recovered, image)

    print("PAPER2_CNC_ARCHETYPE_LANE_V1_SELFTEST_PASS")


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
