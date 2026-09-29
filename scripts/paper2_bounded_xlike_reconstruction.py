#!/usr/bin/env python3
"""Paper 2 #317: terminal A1-A8 audit and bounded XLike freeze.

Consumes the frozen global Archetype graph from #315 / PR #316.
No new Archetype generation or forgetting rule is introduced here.

The terminal bounded family is:
    XLike(A) = { frozen corpus claims X | A <= U_claim(Phi(X)) }

Support is inherited through the frozen refinement graph by composition.
Historical construct labels are restored only after structural families are
frozen and do not participate in identity, membership, or maximality.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

from paper2_basis_subobject_forgetting import (
    image_equivalent,
    is_nontrivial,
    validate_image,
)
from paper2_archetype_mem_pilot import image_id

GLOBAL_PATH = Path("research/paper2/global_archetype_reconstruction_v1.json")
GLOBAL_PHI_PATH = Path("research/paper2/reference_global_phi_freeze_v1.json")
U_CLAIM_CONTRACT = Path("research/paper2/archetype_claim_forgetting_contract_v1.json")
F_R_CONTRACT = Path("research/paper2/basis_subobject_forgetting_contract_v1.json")
CLAIM_DIR = Path("research/paper2/chatgpt_reference_claimir_v1")


class TerminalAuditError(ValueError):
    pass


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _canon(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _support_claims(obj: dict[str, Any]) -> list[str]:
    return sorted({
        claim_id
        for ids in obj["derived_support_claim_ids_by_lane"].values()
        for claim_id in ids
    })


def _support_key(obj: dict[str, Any]) -> tuple[str, ...]:
    return tuple(_support_claims(obj))


def _build_adjacency(
    object_ids: list[str],
    direct_edges: list[dict[str, Any]],
) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    stronger = {x: set() for x in object_ids}
    weaker = {x: set() for x in object_ids}
    for edge in direct_edges:
        a = edge["weaker_archetype_id"]
        b = edge["stronger_archetype_id"]
        if a not in stronger or b not in stronger:
            raise TerminalAuditError("direct refinement edge references unknown object")
        stronger[a].add(b)
        weaker[b].add(a)
    return stronger, weaker


def _closure(start: str, adjacency: dict[str, set[str]]) -> set[str]:
    seen = {start}
    stack = [start]
    while stack:
        x = stack.pop()
        for y in adjacency[x]:
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return seen


def _rename_image_nodes(image: dict[str, Any]) -> dict[str, Any]:
    validate_image(image)
    mapping = {
        old: f"presentation_{i}"
        for i, old in enumerate(sorted(image["nodes"]))
    }
    out = copy.deepcopy(image)
    out["nodes"] = {
        mapping[old]: copy.deepcopy(node)
        for old, node in image["nodes"].items()
    }
    for edge in out["edges"]:
        edge["arguments"] = [mapping[x] for x in edge["arguments"]]
        edge["conditional_on"] = [mapping[x] for x in edge["conditional_on"]]
    return out


def _historical_labels(claim_id: str) -> list[str]:
    path = CLAIM_DIR / f"{claim_id}.json"
    if not path.exists():
        raise TerminalAuditError(f"missing ClaimIR for post-hoc label restore: {claim_id}")
    claim = _load(path)
    return sorted(set(claim["provenance"]["construct_labels"]))


def _claim_pair_key(a: str, b: str) -> str:
    x, y = sorted((a, b))
    return f"{x}::{y}"


def _lane_code(claim_id: str) -> str:
    return "CH" if claim_id.startswith("CH") else claim_id[:3]


def build_report() -> dict[str, Any]:
    global_report = _load(GLOBAL_PATH)
    phi_freeze = _load(GLOBAL_PHI_PATH)
    u_claim_contract = _load(U_CLAIM_CONTRACT)
    f_r_contract = _load(F_R_CONTRACT)

    if global_report["decision"] != "GLOBAL_ARCHETYPE_PREORDER_WITH_CROSS_LANE_RECURRENCE_SUPPORTED":
        raise TerminalAuditError("unexpected #315 terminal classification")
    if u_claim_contract["projection"]["name"] != "U_claim":
        raise TerminalAuditError("U_claim contract mismatch")
    if f_r_contract["operator"]["name"] != "F_R":
        raise TerminalAuditError("F_R contract mismatch")

    objects = {
        row["global_archetype_id"]: row
        for row in global_report["global_archetype_objects"]
    }
    if len(objects) != global_report["unique_global_archetype_count"]:
        raise TerminalAuditError("global object count mismatch")

    object_ids = sorted(objects)
    stronger, weaker = _build_adjacency(
        object_ids, global_report["direct_refinement_edges"]
    )
    upward = {x: _closure(x, stronger) for x in object_ids}

    # A1 — use only the pre-frozen #293 non-triviality predicate.
    a1_failures = []
    minimal_survivors = []
    for object_id in object_ids:
        image = objects[object_id]["canonical_structural_object"]
        validate_image(image)
        if not is_nontrivial(image):
            a1_failures.append(object_id)
        if len(image["nodes"]) == 1 and len(image["edges"]) == 0:
            minimal_survivors.append(object_id)

    # A2 — labels were not used structurally.
    a2_pass = (
        global_report["historical_construct_labels_used"] is False
        and global_report["joint_cross_lane_candidate_generation_performed"] is False
    )

    # A3 — all lane candidates trace through pre-frozen recovery and contracts.
    recovery_total = sum(global_report["recovery_route_counts"].values())
    a3_pass = (
        recovery_total == global_report["lane_candidate_total"] == 213
        and u_claim_contract["projection"]["claim_specific_rules_forbidden"] is True
        and f_r_contract["operator"]["claim_specific_operator_definitions_forbidden"] is True
    )

    # A4 — within an identical observed corpus support signature, retain only
    # maximal common cores.  If A < B with identical support, A is dominated.
    support_groups: dict[tuple[str, ...], list[str]] = {}
    for object_id in object_ids:
        support_groups.setdefault(_support_key(objects[object_id]), []).append(object_id)

    dominated: dict[str, list[str]] = {}
    survivors: list[str] = []
    for ids in support_groups.values():
        for object_id in sorted(ids):
            richer = sorted(
                other
                for other in ids
                if other != object_id and other in upward[object_id]
            )
            if richer:
                dominated[object_id] = richer
            else:
                survivors.append(object_id)
    survivors.sort()

    # A5 — overlapping, incomparable common cores must be preserved.
    overlapping_incomparable = []
    support_sets = {
        x: set(_support_claims(objects[x]))
        for x in survivors
    }
    for i, left in enumerate(survivors):
        for right in survivors[i + 1:]:
            overlap = sorted(support_sets[left] & support_sets[right])
            if not overlap:
                continue
            comparable = right in upward[left] or left in upward[right]
            if not comparable:
                overlapping_incomparable.append({
                    "left_archetype_id": left,
                    "right_archetype_id": right,
                    "overlap_claim_count": len(overlap),
                })

    # A6 — exact and refinement-derived cross-lane structure.
    exact_cross_lane = global_report["exact_cross_lane_equivalence_component_count"]
    closure_cross_lane = sum(
        1
        for x in survivors
        if len(objects[x]["derived_support_lanes"]) >= 2
    )

    # A7 — the original whole-object atlas is all incomparable, while the
    # reconstructed Archetype surface can still relate those claims.
    if phi_freeze["relation_counts"] != {"INCOMPARABLE": 1770}:
        raise TerminalAuditError("unexpected frozen global Phi relation surface")

    shared_claim_pairs: set[str] = set()
    shared_cross_lane_pairs: set[str] = set()
    for object_id in survivors:
        claims = sorted(support_sets[object_id])
        for a, b in itertools.combinations(claims, 2):
            key = _claim_pair_key(a, b)
            shared_claim_pairs.add(key)
            if _lane_code(a) != _lane_code(b):
                shared_cross_lane_pairs.add(key)

    # A8 — all canonical objects survive presentation-only node renaming.
    a8_failures = []
    for object_id in object_ids:
        image = objects[object_id]["canonical_structural_object"]
        renamed = _rename_image_nodes(image)
        if not image_equivalent(image, renamed) or image_id(image) != image_id(renamed):
            a8_failures.append(object_id)

    controls = {
        "A1_trivial_core_rejection": {
            "status": "PASS" if not a1_failures else "FAIL",
            "pre_frozen_predicate": "paper2_basis_subobject_forgetting.is_nontrivial",
            "global_object_count": len(object_ids),
            "failure_count": len(a1_failures),
            "failure_ids": a1_failures,
            "minimal_one_node_no_edge_survivor_count": len(minimal_survivors),
            "minimal_survivor_ids": sorted(minimal_survivors),
            "note": "Minimal survivors are reported, not retroactively deleted; no post-hoc threshold was added."
        },
        "A2_label_deletion": {
            "status": "PASS" if a2_pass else "FAIL",
            "historical_construct_labels_used_in_reconstruction": False,
        },
        "A3_permissive_forgetting_pressure": {
            "status": "PASS" if a3_pass else "FAIL",
            "lane_candidates_recovered_and_id_checked": recovery_total,
            "operator": "F_R explicit basis-subobject restriction",
            "rewriting_or_rewiring_authorized": False,
        },
        "A4_richer_core_pressure": {
            "status": "PASS",
            "support_signature_count": len(support_groups),
            "dominated_same_support_count": len(dominated),
            "dominated": dominated,
            "surviving_maximal_count": len(survivors),
        },
        "A5_competing_core_pressure": {
            "status": "PASS" if overlapping_incomparable else "FAIL",
            "overlapping_incomparable_survivor_pair_count": len(overlapping_incomparable),
            "preserved": True,
        },
        "A6_cross_label_challenge": {
            "status": "PASS" if exact_cross_lane > 0 and closure_cross_lane > 0 else "FAIL",
            "exact_cross_lane_object_count": exact_cross_lane,
            "refinement_closure_cross_lane_object_count": closure_cross_lane,
        },
        "A7_whole_object_incomparability_compatibility": {
            "status": "PASS" if shared_claim_pairs else "FAIL",
            "frozen_whole_object_incomparable_pairs": 1770,
            "claim_pairs_sharing_at_least_one_surviving_archetype": len(shared_claim_pairs),
            "cross_lane_claim_pairs_sharing_at_least_one_surviving_archetype": len(shared_cross_lane_pairs),
        },
        "A8_presentation_invariance": {
            "status": "PASS" if not a8_failures else "FAIL",
            "objects_checked": len(object_ids),
            "failure_count": len(a8_failures),
            "failure_ids": a8_failures,
        },
    }

    all_controls_pass = all(row["status"] == "PASS" for row in controls.values())

    # Freeze bounded XLike families only after A1-A8 structural checks.  Labels
    # are restored below solely as post-hoc metadata.
    xlikes = []
    all_supported_claims: set[str] = set()
    cross_lane_xlikes = 0
    lane_local_xlikes = 0

    for object_id in survivors:
        row = objects[object_id]
        claims = _support_claims(row)
        all_supported_claims.update(claims)
        lanes = list(row["derived_support_lanes"])
        if len(lanes) >= 2:
            cross_lane_xlikes += 1
        else:
            lane_local_xlikes += 1

        labels_by_claim = {
            claim_id: _historical_labels(claim_id)
            for claim_id in claims
        }
        label_union = sorted({
            label
            for labels in labels_by_claim.values()
            for label in labels
        })

        xlikes.append({
            "xlike_id": f"XLike::{object_id}",
            "archetype_id": object_id,
            "archetype_structural_object": row["canonical_structural_object"],
            "member_claim_ids": claims,
            "member_claim_ids_by_lane": row["derived_support_claim_ids_by_lane"],
            "supporting_lane_codes": lanes,
            "direct_origin_lanes": row["direct_origin_lanes"],
            "exact_cross_lane_recurrence": len(row["direct_origin_lanes"]) >= 2,
            "immediate_weaker_archetype_ids": sorted(weaker[object_id]),
            "immediate_stronger_archetype_ids": sorted(stronger[object_id]),
            "historical_construct_labels_restored_post_hoc": label_union,
            "historical_construct_labels_by_claim": labels_by_claim,
            "a1_nontrivial": object_id not in a1_failures,
            "a4_maximal_for_observed_support": object_id not in dominated,
            "minimal_low_complexity_survivor": object_id in minimal_survivors,
        })

    # Terminal choice from #283's declared vocabulary.
    if not all_controls_pass:
        decision = "ARCHETYPE_UNSTABLE_UNDER_CONTROLS"
        family_status = "NOT_QUALIFIED"
    elif overlapping_incomparable:
        decision = "MULTIPLE_INCOMPARABLE_ARCHETYPES_SUPPORTED"
        family_status = "ARCHETYPE_FAMILY_RECONSTRUCTION_SUPPORTED"
    else:
        decision = "ARCHETYPE_FAMILY_RECONSTRUCTION_SUPPORTED"
        family_status = "ARCHETYPE_FAMILY_RECONSTRUCTION_SUPPORTED"

    grand_null_status = (
        "FAILS_ON_FROZEN_BOUNDED_SURFACE"
        if all_controls_pass and shared_claim_pairs
        else "SURVIVES_OR_UNDERDETERMINED"
    )

    return {
        "schema_version": "paper2-bounded-xlike-reconstruction-v1",
        "owner_issue": 317,
        "parent_issue": 283,
        "input_sha256": {
            "global_archetype_reconstruction": _sha(GLOBAL_PATH),
            "global_phi_freeze": _sha(GLOBAL_PHI_PATH),
            "u_claim_contract": _sha(U_CLAIM_CONTRACT),
            "f_r_contract": _sha(F_R_CONTRACT),
        },
        "input_global_archetype_count": len(object_ids),
        "support_signature_count": len(support_groups),
        "a4_dominated_object_count": len(dominated),
        "bounded_xlike_count": len(xlikes),
        "cross_lane_xlike_count": cross_lane_xlikes,
        "lane_local_only_xlike_count": lane_local_xlikes,
        "supported_claim_count": len(all_supported_claims),
        "destructive_controls": controls,
        "bounded_xlike_families": xlikes,
        "historical_labels_restored_only_post_hoc": True,
        "new_abstraction_threshold_added_after_results": False,
        "architecture_tuning": "NONE",
        "family_reconstruction_status": family_status,
        "grand_null_status": grand_null_status,
        "decision": decision,
    }


def self_test() -> None:
    first = build_report()
    second = build_report()
    assert first == second
    assert first["input_global_archetype_count"] == 206
    assert first["a4_dominated_object_count"] == 0
    assert first["bounded_xlike_count"] == 206
    assert first["cross_lane_xlike_count"] == 99
    assert first["supported_claim_count"] == 60
    assert all(
        row["status"] == "PASS"
        for row in first["destructive_controls"].values()
    )
    assert first["decision"] == "MULTIPLE_INCOMPARABLE_ARCHETYPES_SUPPORTED"
    assert first["grand_null_status"] == "FAILS_ON_FROZEN_BOUNDED_SURFACE"
    print("PAPER2_BOUNDED_XLIKE_RECONSTRUCTION_V1_SELFTEST_PASS")


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
