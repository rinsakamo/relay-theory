#!/usr/bin/env python3
"""Validate the frozen Paper 2 activated 48+12 source manifest.

Owner: #231. This is a pre-ClaimIR/source-selection contract. It does not
consume structural-signature or Phi outcomes.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from paper2_designed_source_candidate_ledger_validate import (
    load_exclusions,
    load_geometry,
    validate as validate_ledger,
)

MANIFEST_VERSION = "paper2-designed-source-manifest-v1"
LEDGER_VERSION = "paper2-designed-source-candidate-ledger-v1"
GEOMETRY_VERSION = "paper2-designed-corpus-geometry-v1"
STATE = "ACTIVATED_MANIFEST_FROZEN"

COVERAGE_TAGS = {
    "temporal_persistence_explicit",
    "temporal_persistence_not_required",
    "acquisition_update_explicit",
    "acquisition_update_not_required",
    "resource_boundedness_explicit",
    "resource_boundedness_not_required",
    "criterion_explicit",
    "criterion_not_required",
    "probe_or_intervention_explicit",
    "structured_probe_transform",
    "partition_subsystem_explicit",
    "alternative_partition_material",
    "stochastic_probabilistic_approximate",
    "deterministic_exact",
}
RELATION_FAMILIES = {
    "causal_or_counterfactual",
    "correlational_or_dependence",
    "constitutive_or_definitional",
    "constraint_or_optimization",
    "mapping_or_representation",
    "intervention_sensitive_interaction",
}
ROOT_KEYS = {
    "schema_version", "geometry_version", "ledger_version", "ledger_sha256",
    "state", "activation_policy", "selection_outcome_blind",
    "claim_ir_consumed", "structural_signature_consumed", "phi_consumed",
    "entries",
}
ENTRY_KEYS = {
    "slot_id", "surface", "sampling_stratum", "challenge_pressure",
    "activated_rank", "activation_outcome", "replacement_reason",
    "stable_identity", "title", "year", "canonical_locator",
    "registry_reference", "source_access_class", "read_status",
    "grounding_receipt", "author_lineage_key", "operational_tradition",
    "relation_family", "coverage_claims",
}
POLICY = {
    "start_rank": 1,
    "reserve_use_only_after_prefrozen_pre_claim_ir_failure": True,
    "coverage_driven_substitution_forbidden": True,
    "post_claim_ir_replacement_forbidden": True,
}
GROUNDING_BY_READ = {
    "ABSTRACT_ONLY_READ": "ABSTRACT_LEVEL_GROUNDING",
    "PARTIAL_TEXT_READ": "PARTIAL_PRIMARY_TEXT_GROUNDING",
    "FULL_TEXT_READ": "FULL_TEXT_GROUNDING",
}


class ValidationError(ValueError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def canon_identity(value: dict[str, Any]) -> tuple[str, str]:
    kind = value["kind"]
    raw = value["value"].strip()
    if kind == "DOI":
        raw = raw.casefold().removeprefix("https://doi.org/").removeprefix("doi:")
    else:
        raw = raw.casefold()
    return kind, raw


def expected_slot_rows(geometry: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for row in geometry["primary"]["slots"]:
        out.append({
            "slot_id": row["slot_id"],
            "surface": "primary",
            "sampling_stratum": row["sampling_stratum"],
            "challenge_pressure": None,
        })
    for row in geometry["challenge"]["slots"]:
        out.append({
            "slot_id": row["slot_id"],
            "surface": "challenge",
            "sampling_stratum": None,
            "challenge_pressure": row["pressure"],
        })
    return out


def validate(
    manifest: Any,
    geometry: dict[str, Any],
    ledger: dict[str, Any],
    ledger_bytes: bytes,
) -> dict[str, Any]:
    if not isinstance(manifest, dict) or set(manifest) != ROOT_KEYS:
        fail("manifest root keys mismatch")
    if manifest["schema_version"] != MANIFEST_VERSION:
        fail("manifest version mismatch")
    if manifest["geometry_version"] != GEOMETRY_VERSION:
        fail("geometry version mismatch")
    if manifest["ledger_version"] != LEDGER_VERSION:
        fail("ledger version mismatch")
    if manifest["state"] != STATE:
        fail("manifest state mismatch")
    if manifest["activation_policy"] != POLICY:
        fail("activation policy drift")
    if manifest["selection_outcome_blind"] is not True:
        fail("selection_outcome_blind must be true")
    if manifest["claim_ir_consumed"] or manifest["structural_signature_consumed"] or manifest["phi_consumed"]:
        fail("downstream analysis consumed before manifest freeze")

    actual_ledger_digest = hashlib.sha256(ledger_bytes).hexdigest()
    if manifest["ledger_sha256"] != actual_ledger_digest:
        fail("ledger digest mismatch")

    expected = expected_slot_rows(geometry)
    entries = manifest["entries"]
    if not isinstance(entries, list) or len(entries) != 60 or len(entries) != len(expected):
        fail("manifest must contain exactly 60 activated entries")

    ledger_by_position = {
        (r["slot_id"], r["candidate_rank"]): r for r in ledger["records"]
    }
    seen_ids: set[tuple[str, str]] = set()

    for i, (entry, slot) in enumerate(zip(entries, expected)):
        ctx = f"entries[{i}]"
        if not isinstance(entry, dict) or set(entry) != ENTRY_KEYS:
            fail(f"{ctx}: keys mismatch")
        for key, value in slot.items():
            if entry[key] != value:
                fail(f"{ctx}.{key}: frozen geometry mismatch")

        if entry["activated_rank"] != 1:
            fail(f"{ctx}: reserve activation is not authorized in this frozen manifest")
        if entry["activation_outcome"] != "ACTIVATED_RANK_1":
            fail(f"{ctx}: activation outcome mismatch")
        if entry["replacement_reason"] is not None:
            fail(f"{ctx}: no replacement reason is allowed for rank-1 activation")

        candidate = ledger_by_position.get((entry["slot_id"], 1))
        if candidate is None:
            fail(f"{ctx}: rank-1 ledger candidate missing")
        for key in (
            "stable_identity", "title", "year", "canonical_locator",
            "registry_reference", "source_access_class", "read_status",
            "author_lineage_key",
        ):
            if entry[key] != candidate[key]:
                fail(f"{ctx}.{key}: does not match frozen rank-1 ledger")

        ident = canon_identity(entry["stable_identity"])
        if ident in seen_ids:
            fail(f"{ctx}: duplicate activated stable identity")
        seen_ids.add(ident)

        receipt = entry["grounding_receipt"]
        if not isinstance(receipt, dict) or set(receipt) != {"central_claim_supported", "limitation"}:
            fail(f"{ctx}.grounding_receipt: malformed")
        if receipt["central_claim_supported"] is not True:
            fail(f"{ctx}: central claim must be source-grounded before activation")
        expected_limit = GROUNDING_BY_READ.get(entry["read_status"])
        if receipt["limitation"] != expected_limit:
            fail(f"{ctx}: grounding limitation/read-status mismatch")

        claims = entry["coverage_claims"]
        if not isinstance(claims, list) or len(claims) != len(set(claims)):
            fail(f"{ctx}.coverage_claims: unique list required")
        if not set(claims) <= COVERAGE_TAGS:
            fail(f"{ctx}.coverage_claims: unknown tag")

        if entry["surface"] == "primary":
            if entry["relation_family"] not in RELATION_FAMILIES:
                fail(f"{ctx}.relation_family: required for primary")
            if not entry["operational_tradition"]:
                fail(f"{ctx}.operational_tradition: required")
        else:
            if entry["relation_family"] is not None:
                fail(f"{ctx}: challenge relation family must remain unclassified pre-Phi")
            if claims:
                fail(f"{ctx}: challenge entries do not contribute primary coverage claims")
            if entry["operational_tradition"] != f"challenge_{entry['challenge_pressure']}":
                fail(f"{ctx}: challenge tradition/pressure mismatch")

    primary = [x for x in entries if x["surface"] == "primary"]
    challenge = [x for x in entries if x["surface"] == "challenge"]
    if len(primary) != 48 or len(challenge) != 12:
        fail("primary/challenge activation counts mismatch")

    # Exact six-per-stratum and diversity constraints.
    by_stratum: dict[str, list[dict[str, Any]]] = {}
    for row in primary:
        by_stratum.setdefault(row["sampling_stratum"], []).append(row)
    if set(by_stratum) != set(geometry["primary"]["strata"]):
        fail("primary strata mismatch")
    min_trad = geometry["within_stratum"]["minimum_distinct_operational_traditions"]
    max_lineage = geometry["within_stratum"]["maximum_slots_one_author_group_or_close_lineage"]
    for stratum, quota in geometry["primary"]["strata"].items():
        rows = by_stratum[stratum]
        if len(rows) != quota:
            fail(f"{stratum}: activated quota mismatch")
        if len({x["operational_tradition"] for x in rows}) < min_trad:
            fail(f"{stratum}: insufficient operational-tradition diversity")
        lineage_counts = Counter(x["author_lineage_key"] for x in rows)
        if lineage_counts and max(lineage_counts.values()) > max_lineage:
            fail(f"{stratum}: author/lineage concentration exceeds frozen cap")

    # Source-readable primary coverage minima.
    coverage_counts = Counter(
        tag for row in primary for tag in row["coverage_claims"]
    )
    for key, minimum in geometry["coverage_minima"].items():
        if key in {"same_inventory_different_wiring_pairs", "cross_label_overlap_pressure_pairs"}:
            continue
        if coverage_counts[key] < minimum:
            fail(f"coverage minimum not met: {key}={coverage_counts[key]} < {minimum}")

    active_slots = {x["slot_id"] for x in entries}
    for pair_key, geometry_key in (
        ("same_inventory_different_wiring", "same_inventory_different_wiring_pairs"),
        ("cross_label_overlap", "cross_label_overlap_pressure_pairs"),
    ):
        pairs = geometry["predeclared_pressure_pairs"][pair_key]
        count = sum(1 for a, b in pairs if a in active_slots and b in active_slots)
        if count < geometry["coverage_minima"][geometry_key]:
            fail(f"{pair_key}: insufficient activated predeclared pairs")

    # All six source-level relation families must appear; none may dominate > 50%.
    rel_counts = Counter(x["relation_family"] for x in primary)
    required_rel = set(geometry["required_relation_families"])
    if set(rel_counts) != required_rel:
        fail(f"relation-family coverage mismatch: {sorted(set(rel_counts) ^ required_rel)}")
    cap = geometry["max_primary_fraction_single_relation_family"] * len(primary)
    if max(rel_counts.values()) > cap:
        fail("single relation family exceeds frozen primary fraction cap")

    # Challenge pressure surface must be exact and complete.
    expected_pressures = [x["pressure"] for x in geometry["challenge"]["slots"]]
    if [x["challenge_pressure"] for x in challenge] != expected_pressures:
        fail("challenge pressure sequence mismatch")

    return manifest


def expect_invalid(
    manifest: dict[str, Any],
    geometry: dict[str, Any],
    ledger: dict[str, Any],
    ledger_bytes: bytes,
    label: str,
) -> None:
    try:
        validate(manifest, geometry, ledger, ledger_bytes)
    except ValidationError:
        return
    raise AssertionError(f"{label}: unexpectedly validated")


def self_test(
    manifest_path: Path,
    geometry_path: Path,
    ledger_path: Path,
    exclusions_path: Path,
) -> None:
    geometry = load_geometry(geometry_path)
    exclusions = load_exclusions(exclusions_path)
    ledger_bytes = ledger_path.read_bytes()
    ledger = json.loads(ledger_bytes)
    validate_ledger(ledger, geometry, exclusions)
    base = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate(base, geometry, ledger, ledger_bytes)

    x = copy.deepcopy(base)
    x["phi_consumed"] = True
    expect_invalid(x, geometry, ledger, ledger_bytes, "Phi-before-freeze leak")

    x = copy.deepcopy(base)
    x["entries"][0]["activated_rank"] = 2
    expect_invalid(x, geometry, ledger, ledger_bytes, "coverage-driven reserve substitution")

    x = copy.deepcopy(base)
    # Exactly six resource-explicit entries are frozen; deleting one must fail.
    for entry in x["entries"]:
        if "resource_boundedness_explicit" in entry["coverage_claims"]:
            entry["coverage_claims"].remove("resource_boundedness_explicit")
            break
    expect_invalid(x, geometry, ledger, ledger_bytes, "resource coverage erosion")

    x = copy.deepcopy(base)
    for entry in x["entries"]:
        if entry["surface"] == "primary":
            entry["relation_family"] = "causal_or_counterfactual"
    expect_invalid(x, geometry, ledger, ledger_bytes, "relation-family collapse")

    x = copy.deepcopy(base)
    memories = [e for e in x["entries"] if e["sampling_stratum"] == "Memory"]
    for e in memories[:5]:
        e["operational_tradition"] = "collapsed_tradition"
    expect_invalid(x, geometry, ledger, ledger_bytes, "tradition diversity collapse")

    x = copy.deepcopy(base)
    challenges = [e for e in x["entries"] if e["surface"] == "challenge"]
    challenges[0]["challenge_pressure"] = challenges[1]["challenge_pressure"]
    expect_invalid(x, geometry, ledger, ledger_bytes, "challenge pressure drift")

    print("PAPER2_DESIGNED_SOURCE_MANIFEST_V1_SELFTEST_PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path("research/paper2/designed_source_manifest_v1.json"))
    parser.add_argument("--geometry", type=Path, default=Path("research/paper2/designed_corpus_geometry_v1.json"))
    parser.add_argument("--ledger", type=Path, default=Path("research/paper2/designed_source_candidate_ledger_v1.json"))
    parser.add_argument("--exclusions", type=Path, default=Path("research/paper2/designed_atlas_forging_exclusion_v1.json"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    geometry = load_geometry(args.geometry)
    exclusions = load_exclusions(args.exclusions)
    ledger_bytes = args.ledger.read_bytes()
    ledger = json.loads(ledger_bytes)
    validate_ledger(ledger, geometry, exclusions)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    validate(manifest, geometry, ledger, ledger_bytes)
    if args.self_test:
        self_test(args.manifest, args.geometry, args.ledger, args.exclusions)
    else:
        print("PAPER2_DESIGNED_SOURCE_MANIFEST_V1_VALID")


if __name__ == "__main__":
    main()
