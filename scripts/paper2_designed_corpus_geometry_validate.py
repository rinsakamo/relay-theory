#!/usr/bin/env python3
"""Validate Paper 2 designed-corpus geometry v1.

Owner: #229. Geometry only: no real source identity or Phi outcome belongs here.
"""

from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from pathlib import Path
from typing import Any

VERSION = "paper2-designed-corpus-geometry-v1"
BASIS = "paper2-working-basis-v1"
PHI = "paper2-phi-comparison-v1"

STRATA = {
    "Memory": "MEM",
    "Learning": "LRN",
    "Skill": "SKL",
    "Attention": "ATT",
    "Prediction": "PRD",
    "Control": "CTL",
    "Belief": "BLF",
    "Concept": "CNC",
}
CHALLENGE_PRESSURES = {
    "CH01": "multi_timescale",
    "CH02": "stochastic_or_approximate",
    "CH03": "constitutive_boundary",
    "CH04": "compositional_or_systematic",
    "CH05": "embodied_or_world_coupled",
    "CH06": "normative_or_value_criterion",
    "CH07": "hybrid_construct_labels",
    "CH08": "label_coordinate_mismatch_pressure",
    "CH09": "multi_condition_structure",
    "CH10": "same_inventory_different_topology_pressure",
    "CH11": "strict_refinement_pressure",
    "CH12": "high_structural_heterogeneity",
}
EXPECTED_MINIMA = {
    "temporal_persistence_explicit": 8,
    "temporal_persistence_not_required": 8,
    "acquisition_update_explicit": 6,
    "acquisition_update_not_required": 6,
    "resource_boundedness_explicit": 6,
    "resource_boundedness_not_required": 6,
    "criterion_explicit": 8,
    "criterion_not_required": 8,
    "probe_or_intervention_explicit": 8,
    "structured_probe_transform": 4,
    "partition_subsystem_explicit": 6,
    "alternative_partition_material": 4,
    "stochastic_probabilistic_approximate": 6,
    "deterministic_exact": 6,
    "same_inventory_different_wiring_pairs": 6,
    "cross_label_overlap_pressure_pairs": 6,
}
RELATIONS = {
    "causal_or_counterfactual",
    "correlational_or_dependence",
    "constitutive_or_definitional",
    "constraint_or_optimization",
    "mapping_or_representation",
    "intervention_sensitive_interaction",
}
EXECUTION_ORDER = [
    "freeze_geometry",
    "freeze_ranked_source_candidates",
    "freeze_primary_and_challenge_manifests",
    "restore_registry_links",
    "only_then_claim_ir",
    "only_then_structural_signature",
    "only_then_phi",
    "only_then_atlas_analysis",
]


class ValidationError(ValueError):
    pass


def fail(msg: str) -> None:
    raise ValidationError(msg)


def validate(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        fail("root must be object")
    required = {
        "schema_version", "paper", "basis_version", "phi_version", "design_status",
        "primary", "challenge", "coverage_minima", "required_relation_families",
        "max_primary_fraction_single_relation_family", "within_stratum",
        "predeclared_pressure_pairs", "source_manifest_rules", "replacement_rules",
        "execution_order",
    }
    if set(data) != required:
        fail(f"root keys mismatch: {sorted(set(data) ^ required)}")
    if data["schema_version"] != VERSION:
        fail("unexpected schema version")
    if data["paper"] != "Paper 2":
        fail("paper must be Paper 2")
    if data["basis_version"] != BASIS or data["phi_version"] != PHI:
        fail("basis/Phi version mismatch")
    if data["design_status"] != "geometry_only_no_real_sources":
        fail("design_status must remain geometry-only")

    primary = data["primary"]
    if primary["target_claims"] != 48:
        fail("primary target must be 48")
    if primary["strata"] != {name: 6 for name in STRATA}:
        fail("primary stratum quotas must be exactly 6 each")
    slots = primary["slots"]
    if len(slots) != 48:
        fail("expected 48 primary slots")
    slot_ids = [s["slot_id"] for s in slots]
    if len(set(slot_ids)) != 48:
        fail("duplicate primary slot")
    expected_ids = []
    for label, prefix in STRATA.items():
        for i in range(1, 7):
            expected_ids.append(f"{prefix}{i:02d}")
    if slot_ids != expected_ids:
        fail("primary slot identity/order mismatch")
    for slot in slots:
        if set(slot) != {"slot_id", "sampling_stratum", "source_work_uniqueness", "phi_visible_label"}:
            fail(f"{slot['slot_id']}: slot keys mismatch")
        prefix = slot["slot_id"][:3]
        expected_label = next((label for label,p in STRATA.items() if p == prefix), None)
        if slot["sampling_stratum"] != expected_label:
            fail(f"{slot['slot_id']}: stratum mismatch")
        if slot["source_work_uniqueness"] != "one_primary_claim_per_work":
            fail(f"{slot['slot_id']}: uniqueness rule mismatch")
        if slot["phi_visible_label"] is not False:
            fail(f"{slot['slot_id']}: sampling label leaked to Phi")

    challenge = data["challenge"]
    if challenge["target_claims"] != 12 or challenge["tuning_surface"] is not False:
        fail("challenge contract mismatch")
    if len(challenge["slots"]) != 12:
        fail("expected 12 challenge slots")
    for slot in challenge["slots"]:
        sid = slot["slot_id"]
        if CHALLENGE_PRESSURES.get(sid) != slot["pressure"]:
            fail(f"{sid}: challenge pressure mismatch")
        if slot["phi_tuning_forbidden"] is not True:
            fail(f"{sid}: challenge tuning must be forbidden")

    if data["coverage_minima"] != EXPECTED_MINIMA:
        fail("coverage minima drifted")
    if set(data["required_relation_families"]) != RELATIONS or len(data["required_relation_families"]) != len(RELATIONS):
        fail("relation-family coverage mismatch")
    if data["max_primary_fraction_single_relation_family"] != 0.5:
        fail("single relation-family cap must be 0.5")

    within = data["within_stratum"]
    if within != {
        "minimum_distinct_operational_traditions": 3,
        "maximum_slots_one_author_group_or_close_lineage": 2,
        "exception_requires_prefreeze_documented_availability_reason": True,
    }:
        fail("within-stratum diversity contract drifted")

    pairs = data["predeclared_pressure_pairs"]
    if set(pairs) != {"same_inventory_different_wiring", "cross_label_overlap"}:
        fail("pressure-pair keys mismatch")
    for key, expected_n in (
        ("same_inventory_different_wiring", 6),
        ("cross_label_overlap", 6),
    ):
        values = pairs[key]
        if len(values) != expected_n:
            fail(f"{key}: expected {expected_n} pairs")
        seen = set()
        for pair in values:
            if not isinstance(pair, list) or len(pair) != 2:
                fail(f"{key}: malformed pair")
            a, b = pair
            if a not in slot_ids or b not in slot_ids or a == b:
                fail(f"{key}: invalid slot reference")
            if (a,b) in seen:
                fail(f"{key}: duplicate pair")
            seen.add((a,b))
            # Every pressure pair is intentionally cross-stratum.
            sa = next(s["sampling_stratum"] for s in slots if s["slot_id"] == a)
            sb = next(s["sampling_stratum"] for s in slots if s["slot_id"] == b)
            if sa == sb:
                fail(f"{key}: pair must cross sampling strata")

    manifest = data["source_manifest_rules"]
    if manifest != {
        "candidates_per_slot_before_mapping": 3,
        "candidate_rank_frozen_before_claim_ir": True,
        "stable_bibliographic_identity_required": True,
        "source_access_and_claim_grounding_required_before_slot_activation": True,
        "construct_labels_allowed_for_sampling_only": True,
        "author_venue_citation_not_analysis_features": True,
        "primary_source_reuse_forbidden": True,
        "challenge_sources_do_not_tune_basis_or_phi": True,
    }:
        fail("source-manifest rules drifted")

    replacement = data["replacement_rules"]
    allowed = replacement["replacement_allowed_only_before_claim_ir_for"]
    if set(allowed) != {
        "source_inaccessible",
        "bibliographic_identity_mismatch",
        "no_source_grounded_claim_matching_frozen_slot",
        "duplicate_primary_work_detected",
    }:
        fail("replacement reasons drifted")
    for key in (
        "replacement_uses_next_prefrozen_candidate",
        "replacement_for_phi_residual_forbidden",
        "replacement_for_unexpected_equivalence_forbidden",
        "replacement_for_extraction_failure_after_claim_ir_start_forbidden",
    ):
        if replacement[key] is not True:
            fail(f"{key}: must be true")

    if data["execution_order"] != EXECUTION_ORDER:
        fail("execution order drifted")

    # Geometry must not contain real-source identity or any outcome.
    text = json.dumps(data, ensure_ascii=False).casefold()
    for forbidden in (
        "doi.org/", "arxiv.org/", "openalex.org/", "pmid:", "verified_pass",
        "right_strict_refinement_of_left", "left_strict_refinement_of_right",
        "mutual_embeddability_nonisomorphic",
    ):
        if forbidden in text:
            fail(f"geometry contains forbidden source/outcome token {forbidden!r}")

    return data


def expect_invalid(data: dict[str, Any], label: str) -> None:
    try:
        validate(data)
    except ValidationError:
        return
    raise AssertionError(f"{label}: unexpectedly validated")


def self_test(path: Path) -> None:
    base = json.loads(path.read_text(encoding="utf-8"))
    validate(base)

    x = copy.deepcopy(base)
    x["primary"]["target_claims"] = 47
    expect_invalid(x, "wrong primary size")

    x = copy.deepcopy(base)
    x["primary"]["slots"][0]["phi_visible_label"] = True
    expect_invalid(x, "sampling-label leakage")

    x = copy.deepcopy(base)
    x["predeclared_pressure_pairs"]["cross_label_overlap"][0] = ["MEM01", "MEM02"]
    expect_invalid(x, "within-stratum pressure pair")

    x = copy.deepcopy(base)
    x["source_manifest_rules"]["candidates_per_slot_before_mapping"] = 1
    expect_invalid(x, "no prefrozen reserve")

    x = copy.deepcopy(base)
    x["replacement_rules"]["replacement_for_phi_residual_forbidden"] = False
    expect_invalid(x, "result-dependent replacement")

    x = copy.deepcopy(base)
    x["challenge"]["slots"][0]["phi_tuning_forbidden"] = False
    expect_invalid(x, "challenge tuning")

    x = copy.deepcopy(base)
    x["execution_order"][-2:] = list(reversed(x["execution_order"][-2:]))
    expect_invalid(x, "atlas before Phi")

    print("PAPER2_DESIGNED_CORPUS_GEOMETRY_V1_SELFTEST_PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("research/paper2/designed_corpus_geometry_v1.json"),
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    validate(data)
    if args.self_test:
        self_test(args.input)
    else:
        print("PAPER2_DESIGNED_CORPUS_GEOMETRY_V1_VALID")


if __name__ == "__main__":
    main()
