#!/usr/bin/env python3
"""Paper 2 JGPS #365: 48-primary-only ablation / sensitivity analysis.

This is an additive validation-extension analysis. It does not modify frozen
Paper-2 artifacts and MUST NOT be described as held-out validation.

The analysis has two layers:
1. recompute the global Archetype graph from the eight frozen primary lane
   reports only, excluding Challenge A/B before global merging/refinement;
2. summarize frozen Grammar-v0 role support after excluding challenge claims.

Layer (2) is explicitly a support-sensitivity check under the already-frozen
Grammar mapping, not an independent re-induction of Grammar v0.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import paper2_global_archetype_reconstruction as global_recon

PRIMARY_LANES = ("MEM", "SKL", "PRD", "ATT", "BLF", "CNC", "CTL", "LRN")
EXCLUDED_LANES = ("CHA", "CHB")
AGGREGATE_PATH = Path("research/paper2/grammar_v0_reverse_projection_aggregate_v1.json")

ROLE_ORDER = ("Pi", "X", "C", "Q", "P_in", "P_out", "K", "T", "rho/O")


class ValidationError(ValueError):
    pass


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _support_claims(obj: dict[str, Any]) -> tuple[str, ...]:
    return tuple(sorted({
        claim_id
        for ids in obj["derived_support_claim_ids_by_lane"].values()
        for claim_id in ids
    }))


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


def _primary_global_report() -> dict[str, Any]:
    original = global_recon.LANE_REPORTS
    primary = {k: v for k, v in original.items() if k in PRIMARY_LANES}
    if set(primary) != set(PRIMARY_LANES):
        raise ValidationError(
            f"primary lane set mismatch: {sorted(primary)}"
        )
    if any(k in primary for k in EXCLUDED_LANES):
        raise ValidationError("challenge lane leaked into primary-only input")
    try:
        global_recon.LANE_REPORTS = primary
        return global_recon.build_report()
    finally:
        global_recon.LANE_REPORTS = original


def _bounded_summary(global_report: dict[str, Any]) -> dict[str, Any]:
    objects = {
        row["global_archetype_id"]: row
        for row in global_report["global_archetype_objects"]
    }
    ids = sorted(objects)
    upward_adj = {x: set() for x in ids}
    for edge in global_report["direct_refinement_edges"]:
        a = edge["weaker_archetype_id"]
        b = edge["stronger_archetype_id"]
        upward_adj[a].add(b)
    upward = {x: _closure(x, upward_adj) for x in ids}

    groups: dict[tuple[str, ...], list[str]] = {}
    for object_id, row in objects.items():
        groups.setdefault(_support_claims(row), []).append(object_id)

    dominated: dict[str, list[str]] = {}
    survivors: list[str] = []
    for group_ids in groups.values():
        for object_id in sorted(group_ids):
            richer = sorted(
                other for other in group_ids
                if other != object_id and other in upward[object_id]
            )
            if richer:
                dominated[object_id] = richer
            else:
                survivors.append(object_id)
    survivors.sort()

    supported_claims = sorted({
        claim_id
        for object_id in survivors
        for claim_id in _support_claims(objects[object_id])
    })
    cross_lane = [
        x for x in survivors
        if len(objects[x]["derived_support_lanes"]) >= 2
    ]

    return {
        "support_signature_count": len(groups),
        "dominated_same_support_count": len(dominated),
        "bounded_survivor_count": len(survivors),
        "cross_lane_survivor_count": len(cross_lane),
        "lane_local_only_survivor_count": len(survivors) - len(cross_lane),
        "supported_claim_ids": supported_claims,
        "supported_claim_count": len(supported_claims),
    }


def _role_support() -> dict[str, Any]:
    aggregate = _load(AGGREGATE_PATH)
    rows = [
        row for row in aggregate["lane_sources"]
        if row["lane"] in PRIMARY_LANES
    ]
    if len(rows) != 8:
        raise ValidationError(f"expected 8 primary lane sources, got {len(rows)}")

    role_counts = {role: 0 for role in ROLE_ORDER}
    verdict_counts = {"FULL": 0, "PARTIAL": 0, "RESIDUAL": 0}
    both_p = 0
    claim_ids: list[str] = []
    lane_input_sha256: dict[str, str] = {}

    for row in rows:
        lane = row["lane"]
        path = Path(row["path"])
        lane_input_sha256[lane] = _sha(path)
        report = _load(path)
        claims = report["claims"]
        if len(claims) != 6:
            raise ValidationError(f"{lane}: expected 6 claims, got {len(claims)}")
        for claim in claims:
            cid = claim["claim_id"]
            claim_ids.append(cid)
            verdict = claim["verdict"]
            if verdict not in verdict_counts:
                raise ValidationError(f"{cid}: unexpected verdict {verdict}")
            verdict_counts[verdict] += 1

            roles = set(claim.get("grammar_roles_instantiated", []))
            unknown = roles - set(ROLE_ORDER)
            if unknown:
                raise ValidationError(f"{cid}: unknown Grammar roles {sorted(unknown)}")
            for role in roles:
                role_counts[role] += 1
            if {"P_in", "P_out"} <= roles:
                both_p += 1

    if len(claim_ids) != 48 or len(set(claim_ids)) != 48:
        raise ValidationError("primary reverse-projection surface is not 48 unique claims")

    return {
        "claim_count": 48,
        "claim_ids": sorted(claim_ids),
        "verdict_counts": verdict_counts,
        "role_support_counts": role_counts,
        "claims_with_both_P_directions": both_p,
        "all_nine_roles_have_primary_support": all(role_counts[r] > 0 for r in ROLE_ORDER),
        "lane_input_sha256": lane_input_sha256,
        "interpretation": (
            "Frozen-mapping support sensitivity only; this does not convert the "
            "48 claims into an independent Grammar-induction dataset."
        ),
    }


def build_report() -> dict[str, Any]:
    global_report = _primary_global_report()
    if set(global_report["lane_candidate_counts"]) != set(PRIMARY_LANES):
        raise ValidationError("global reconstruction includes non-primary lane")
    bounded = _bounded_summary(global_report)
    roles = _role_support()

    primary_claims = set(roles["claim_ids"])
    supported = set(bounded["supported_claim_ids"])
    foreign = supported - primary_claims
    if foreign:
        raise ValidationError(f"challenge/foreign claim support leaked in: {sorted(foreign)}")

    unsupported = sorted(primary_claims - supported)

    recurrence_survives = (
        global_report["exact_cross_lane_equivalence_component_count"] > 0
        or global_report["cross_lane_refinement_closure_object_count"] > 0
    )
    inventory_supported = roles["all_nine_roles_have_primary_support"]

    if recurrence_survives and inventory_supported:
        terminal = (
            "PRIMARY_ONLY_ABLATION_PRESERVES_CROSS_LANE_RECURRENCE_AND_"
            "FROZEN_GRAMMAR_ROLE_SUPPORT"
        )
    elif recurrence_survives:
        terminal = "PRIMARY_ONLY_ABLATION_PRESERVES_RECURRENCE_BUT_ROLE_SUPPORT_WEAKENS"
    else:
        terminal = "PRIMARY_ONLY_ABLATION_DESTABILIZES_CROSS_LANE_RECURRENCE"

    return {
        "schema": "relay-theory.paper2.primary_only_ablation.v1",
        "status": "VALIDATION_EXTENSION_RESULT",
        "authority_issue": 365,
        "analysis_semantics": {
            "historical_challenge_claims_excluded_before_global_reconstruction": True,
            "is_held_out_validation": False,
            "name": "challenge-set dependence / induction-set sensitivity test",
            "grammar_independently_reinduced": False,
            "frozen_core_modified": False,
        },
        "primary_lanes": list(PRIMARY_LANES),
        "excluded_global_lane_codes": list(EXCLUDED_LANES),
        "primary_only_archetype_reconstruction": {
            "lane_candidate_counts": global_report["lane_candidate_counts"],
            "lane_candidate_total": global_report["lane_candidate_total"],
            "unique_global_archetype_count": global_report["unique_global_archetype_count"],
            "exact_cross_lane_equivalence_component_count": global_report[
                "exact_cross_lane_equivalence_component_count"
            ],
            "strict_subobject_edge_count_transitive": global_report[
                "strict_subobject_edge_count_transitive"
            ],
            "direct_refinement_edge_count": global_report["direct_refinement_edge_count"],
            "cross_lane_exact_object_count": global_report["cross_lane_exact_object_count"],
            "cross_lane_refinement_closure_object_count": global_report[
                "cross_lane_refinement_closure_object_count"
            ],
            "decision": global_report["decision"],
            "input_report_sha256": global_report["input_report_sha256"],
        },
        "primary_only_bounded_recurrence": {
            **{k: v for k, v in bounded.items() if k != "supported_claim_ids"},
            "unsupported_primary_claim_ids": unsupported,
        },
        "frozen_grammar_mapping_sensitivity": {
            k: v for k, v in roles.items() if k != "claim_ids"
        },
        "conclusions": {
            "cross_lane_recurrence_survives_without_historical_challenge_lanes": recurrence_survives,
            "all_nine_frozen_grammar_roles_have_support_in_primary_claims": inventory_supported,
            "challenge_set_is_not_required_for_any_role_to_have_at_least_one_primary_support": inventory_supported,
            "independent_grammar_discovery_established": False,
            "prospective_validation_still_required": True,
        },
        "terminal": terminal,
    }


def render_markdown(report: dict[str, Any]) -> str:
    a = report["primary_only_archetype_reconstruction"]
    b = report["primary_only_bounded_recurrence"]
    g = report["frozen_grammar_mapping_sensitivity"]
    c = report["conclusions"]

    role_lines = "\n".join(
        f"- `{role}`: {g['role_support_counts'][role]}/48"
        for role in ROLE_ORDER
    )
    return f"""# 48-primary-only ablation v1

Status: **VALIDATION EXTENSION RESULT**

This is a challenge-set dependence / induction-set sensitivity test, **not**
held-out validation. The historical 12 challenge claims were excluded before
the primary-only global Archetype reconstruction.

## Primary-only structural reconstruction

- frozen lane-local candidates: {a['lane_candidate_total']}
- unique global Archetypes: {a['unique_global_archetype_count']}
- exact cross-lane equivalence components: {a['exact_cross_lane_equivalence_component_count']}
- transitive strict-subobject relations: {a['strict_subobject_edge_count_transitive']}
- direct refinement edges: {a['direct_refinement_edge_count']}
- cross-lane objects by refinement closure: {a['cross_lane_refinement_closure_object_count']}
- bounded survivors after same-support maximality: {b['bounded_survivor_count']}
- cross-lane bounded survivors: {b['cross_lane_survivor_count']}
- supported primary claims: {b['supported_claim_count']}/48
- unsupported primary claim IDs: {', '.join(b['unsupported_primary_claim_ids']) if b['unsupported_primary_claim_ids'] else 'none'}

## Frozen Grammar mapping support after challenge exclusion

{role_lines}

- claims instantiating both `P_in` and `P_out`: {g['claims_with_both_P_directions']}/48
- verdicts: {g['verdict_counts']}
- all nine roles retain at least one primary-claim witness: {g['all_nine_roles_have_primary_support']}

## Interpretation

Cross-lane recurrence survives challenge exclusion: **{c['cross_lane_recurrence_survives_without_historical_challenge_lanes']}**.

All nine already-frozen Grammar roles retain primary-claim support:
**{c['all_nine_frozen_grammar_roles_have_support_in_primary_claims']}**.

This does **not** establish independent Grammar discovery or turn the 48
primary claims into an independent induction surface. Grammar v0 remains a
data-constrained refinement/factorization of the declared basis. This result
only tests whether the historical challenge set is necessary for the observed
cross-lane recurrence and for role support under the frozen mapping.

Prospective validation remains required.

Terminal:

`{report['terminal']}`
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--md-output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    first = build_report()
    second = build_report()
    if first != second:
        raise ValidationError("non-deterministic primary-only ablation")

    if args.self_test:
        assert first["analysis_semantics"]["is_held_out_validation"] is False
        assert first["frozen_grammar_mapping_sensitivity"]["claim_count"] == 48
        assert sum(first["frozen_grammar_mapping_sensitivity"]["verdict_counts"].values()) == 48
        print("PAPER2_JGPS_PRIMARY_ONLY_ABLATION_V1_SELFTEST_PASS")
        return

    payload = json.dumps(first, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    md = render_markdown(first)

    if args.json_output:
        args.json_output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    if args.md_output:
        args.md_output.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
