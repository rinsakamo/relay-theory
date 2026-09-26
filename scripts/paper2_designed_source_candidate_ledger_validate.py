#!/usr/bin/env python3
"""Validate Paper 2 designed-source candidate ledger v1.

Owner: #231. This validator binds the 180 ranked candidate positions to the
already-frozen #229 geometry and rejects any ClaimIR/Phi outcome dependence.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

LEDGER_VERSION = "paper2-designed-source-candidate-ledger-v1"
GEOMETRY_VERSION = "paper2-designed-corpus-geometry-v1"
BASIS_VERSION = "paper2-working-basis-v1"
PHI_VERSION = "paper2-phi-comparison-v1"

TEMPLATE_STATE = "CONTRACT_TEMPLATE_NO_REAL_SOURCES"
FROZEN_STATE = "CANDIDATE_LEDGER_FROZEN"

READ_BY_ACCESS = {
    "FULL_TEXT": {"FULL_TEXT_READ", "PARTIAL_TEXT_READ"},
    "PARTIAL_TEXT": {"PARTIAL_TEXT_READ"},
    "ABSTRACT_ONLY": {"ABSTRACT_ONLY_READ"},
    "INACCESS": {"NOT_READ"},
}

OUTCOME_TOKENS = {
    "equivalent",
    "right_strict_refinement_of_left",
    "left_strict_refinement_of_right",
    "mutual_embeddability_nonisomorphic",
    "incomparable",
    "phi residual",
    "verified_pass",
    "atlas cluster",
    "relay-self match",
    "relayself match",
}

ROOT_KEYS = {
    "schema_version", "geometry_version", "basis_version", "phi_version", "state",
    "selection_outcome_blind", "claim_ir_consumed", "structural_signature_consumed",
    "phi_consumed", "records",
}
BASE_RECORD_KEYS = {
    "slot_id", "surface", "sampling_stratum", "challenge_pressure",
    "candidate_rank", "candidate_state",
}
CANDIDATE_EXTRA_KEYS = {
    "stable_identity", "title", "year", "source_type", "canonical_locator",
    "source_access_class", "read_status", "candidate_rationale", "coverage_tags",
    "author_lineage_key", "registry_reference",
}


class ValidationError(ValueError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def load_geometry(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != GEOMETRY_VERSION:
        fail("geometry version mismatch")
    return data


def expected_slots(geometry: dict[str, Any]) -> list[dict[str, Any]]:
    expected: list[dict[str, Any]] = []
    for slot in geometry["primary"]["slots"]:
        for rank in (1, 2, 3):
            expected.append({
                "slot_id": slot["slot_id"],
                "surface": "primary",
                "sampling_stratum": slot["sampling_stratum"],
                "challenge_pressure": None,
                "candidate_rank": rank,
            })
    for slot in geometry["challenge"]["slots"]:
        for rank in (1, 2, 3):
            expected.append({
                "slot_id": slot["slot_id"],
                "surface": "challenge",
                "sampling_stratum": None,
                "challenge_pressure": slot["pressure"],
                "candidate_rank": rank,
            })
    return expected


def canonical_identity(identity: dict[str, Any]) -> tuple[str, str]:
    kind = identity["kind"]
    value = identity["value"].strip()
    if not value:
        fail("stable identity value must be nonempty")
    if kind == "DOI":
        value = value.casefold().removeprefix("https://doi.org/").removeprefix("doi:")
    elif kind in {"ARXIV", "PMID", "PMCID", "ISBN_CHAPTER"}:
        value = value.casefold()
    return kind, value


def validate_candidate(record: dict[str, Any], context: str, excluded_identities: set[tuple[str, str]]) -> tuple[str, str]:
    if set(record) != BASE_RECORD_KEYS | CANDIDATE_EXTRA_KEYS:
        fail(f"{context}: candidate keys mismatch")
    identity = record["stable_identity"]
    if not isinstance(identity, dict) or set(identity) != {"kind", "value"}:
        fail(f"{context}.stable_identity: malformed")
    if identity["kind"] not in {"DOI","ARXIV","PMID","PMCID","ISBN_CHAPTER","PUBLISHER_CANONICAL"}:
        fail(f"{context}.stable_identity.kind: unsupported")
    key = canonical_identity(identity)
    if key in excluded_identities:
        fail(f"{context}: forging/calibration source is excluded from the designed atlas: {key!r}")

    if not isinstance(record["title"], str) or not record["title"].strip():
        fail(f"{context}.title: required")
    if not isinstance(record["year"], int) or not 1900 <= record["year"] <= 2100:
        fail(f"{context}.year: invalid")
    if record["source_type"] not in {
        "journal_article","conference_paper","book_chapter","book","preprint","review","other"
    }:
        fail(f"{context}.source_type: invalid")
    if not isinstance(record["canonical_locator"], str) or not record["canonical_locator"].strip():
        fail(f"{context}.canonical_locator: required")
    if record["source_access_class"] not in READ_BY_ACCESS:
        fail(f"{context}.source_access_class: invalid")
    if record["read_status"] not in READ_BY_ACCESS[record["source_access_class"]]:
        fail(f"{context}: read_status incompatible with source_access_class")
    if record["source_access_class"] == "INACCESS":
        fail(f"{context}: inaccessible item cannot be frozen as a ranked candidate")

    rationale = record["candidate_rationale"]
    if not isinstance(rationale, str) or not rationale.strip():
        fail(f"{context}.candidate_rationale: required")
    tags = record["coverage_tags"]
    if not isinstance(tags, list) or not tags or len(tags) != len(set(tags)):
        fail(f"{context}.coverage_tags: nonempty unique list required")
    if not all(isinstance(x, str) and x.strip() for x in tags):
        fail(f"{context}.coverage_tags: nonempty strings required")
    if not isinstance(record["author_lineage_key"], str) or not record["author_lineage_key"].strip():
        fail(f"{context}.author_lineage_key: required")
    if not isinstance(record["registry_reference"], str) or not record["registry_reference"].startswith("#23:"):
        fail(f"{context}.registry_reference: #23 linkage required")

    outcome_surface = " ".join([rationale, *tags]).casefold()
    for token in OUTCOME_TOKENS:
        if token in outcome_surface:
            fail(f"{context}: outcome-dependent token forbidden: {token!r}")
    return key


def load_exclusions(path: Path) -> set[tuple[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "paper2-designed-atlas-forging-exclusion-v1":
        fail("forging exclusion version mismatch")
    rows = data.get("excluded")
    if not isinstance(rows, list) or len(rows) != 16:
        fail("forging exclusion must contain exactly F01-F16")
    expected = [f"F{i:02d}" for i in range(1, 17)]
    fixtures = [row.get("fixture") for row in rows]
    if fixtures != expected:
        fail("forging exclusion fixture order/identity mismatch")
    out: set[tuple[str, str]] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"fixture","kind","value","title","year"}:
            fail(f"forging exclusion row {index}: keys mismatch")
        key = canonical_identity({"kind": row["kind"], "value": row["value"]})
        if key in out:
            fail("forging exclusion contains duplicate stable identity")
        out.add(key)
    return out


def validate(data: Any, geometry: dict[str, Any], excluded_identities: set[tuple[str, str]]) -> dict[str, Any]:
    if not isinstance(data, dict):
        fail("root must be object")
    if set(data) != ROOT_KEYS:
        fail(f"root keys mismatch: {sorted(set(data) ^ ROOT_KEYS)}")
    if data["schema_version"] != LEDGER_VERSION:
        fail("ledger version mismatch")
    if data["geometry_version"] != GEOMETRY_VERSION:
        fail("geometry binding mismatch")
    if data["basis_version"] != BASIS_VERSION:
        fail("basis binding mismatch")
    if data["phi_version"] != PHI_VERSION:
        fail("Phi binding mismatch")
    if data["state"] not in {TEMPLATE_STATE, FROZEN_STATE}:
        fail("unexpected ledger state")
    for key in (
        "selection_outcome_blind", "claim_ir_consumed",
        "structural_signature_consumed", "phi_consumed",
    ):
        if not isinstance(data[key], bool):
            fail(f"{key}: boolean required")
    if data["selection_outcome_blind"] is not True:
        fail("selection_outcome_blind must be true")
    if data["claim_ir_consumed"] or data["structural_signature_consumed"] or data["phi_consumed"]:
        fail("candidate selection must precede ClaimIR/structural-signature/Phi consumption")

    records = data["records"]
    expected = expected_slots(geometry)
    if not isinstance(records, list) or len(records) != len(expected) or len(records) != 180:
        fail("records must contain exactly 180 ranked positions")

    identities: set[tuple[str, str]] = set()
    for index, (record, slot) in enumerate(zip(records, expected)):
        context = f"records[{index}]"
        if not isinstance(record, dict):
            fail(f"{context}: expected object")
        for key, value in slot.items():
            if record.get(key) != value:
                fail(f"{context}.{key}: geometry/rank mismatch")
        if record.get("candidate_state") not in {"UNASSIGNED","CANDIDATE"}:
            fail(f"{context}.candidate_state: invalid")

        if data["state"] == TEMPLATE_STATE:
            if set(record) != BASE_RECORD_KEYS or record["candidate_state"] != "UNASSIGNED":
                fail(f"{context}: template must contain only unassigned base records")
        else:
            if record["candidate_state"] != "CANDIDATE":
                fail(f"{context}: frozen ledger requires every position assigned")
            ident = validate_candidate(record, context, excluded_identities)
            if ident in identities:
                fail(f"{context}: duplicate stable identity across ranked ledger")
            identities.add(ident)

    if data["state"] == FROZEN_STATE and len(identities) != 180:
        fail("frozen ledger must contain 180 unique source identities")
    return data


def expect_invalid(data: dict[str, Any], geometry: dict[str, Any], excluded_identities: set[tuple[str, str]], label: str) -> None:
    try:
        validate(data, geometry, excluded_identities)
    except ValidationError:
        return
    raise AssertionError(f"{label}: unexpectedly validated")


def self_test(ledger_path: Path, geometry_path: Path, exclusion_path: Path) -> None:
    geometry = load_geometry(geometry_path)
    excluded_identities = load_exclusions(exclusion_path)
    base = json.loads(ledger_path.read_text(encoding="utf-8"))
    validate(base, geometry, excluded_identities)

    x = copy.deepcopy(base)
    x["records"].pop()
    expect_invalid(x, geometry, excluded_identities, "missing ranked position")

    x = copy.deepcopy(base)
    x["records"][0]["candidate_rank"] = 2
    expect_invalid(x, geometry, excluded_identities, "rank drift")

    x = copy.deepcopy(base)
    x["records"][0]["sampling_stratum"] = "Learning"
    expect_invalid(x, geometry, excluded_identities, "slot/stratum drift")

    x = copy.deepcopy(base)
    x["phi_consumed"] = True
    expect_invalid(x, geometry, excluded_identities, "Phi-before-ledger leak")

    x = copy.deepcopy(base)
    x["state"] = FROZEN_STATE
    expect_invalid(x, geometry, excluded_identities, "frozen ledger with unassigned candidates")

    # Build a synthetic fully assigned ledger to exercise uniqueness,
    # grounding/read-status, registry, and outcome-blindness constraints.
    full = copy.deepcopy(base)
    full["state"] = FROZEN_STATE
    for i, record in enumerate(full["records"]):
        record["candidate_state"] = "CANDIDATE"
        record.update({
            "stable_identity": {"kind": "PUBLISHER_CANONICAL", "value": f"synthetic:{i:03d}"},
            "title": f"Synthetic candidate {i:03d}",
            "year": 2026,
            "source_type": "journal_article",
            "canonical_locator": f"synthetic://candidate/{i:03d}",
            "source_access_class": "FULL_TEXT",
            "read_status": "FULL_TEXT_READ",
            "candidate_rationale": "Synthetic source-readable fit to the frozen slot geometry.",
            "coverage_tags": ["synthetic_grounded_fit"],
            "author_lineage_key": f"synthetic-lineage-{i:03d}",
            "registry_reference": f"#23:synthetic-{i:03d}",
        })
    validate(full, geometry, excluded_identities)

    x = copy.deepcopy(full)
    x["records"][1]["stable_identity"] = copy.deepcopy(x["records"][0]["stable_identity"])
    expect_invalid(x, geometry, excluded_identities, "duplicate source identity")

    x = copy.deepcopy(full)
    x["records"][0]["registry_reference"] = "missing"
    expect_invalid(x, geometry, excluded_identities, "missing registry linkage")

    x = copy.deepcopy(full)
    x["records"][0]["candidate_rationale"] = "Selected because Phi says EQUIVALENT."
    expect_invalid(x, geometry, excluded_identities, "outcome-dependent rationale")

    x = copy.deepcopy(full)
    x["records"][0]["source_access_class"] = "INACCESS"
    x["records"][0]["read_status"] = "NOT_READ"
    expect_invalid(x, geometry, excluded_identities, "inaccessible frozen candidate")

    x = copy.deepcopy(full)
    x["records"][0]["stable_identity"] = {
        "kind": "DOI",
        "value": "https://doi.org/10.1016/S0079-7421(08)60422-3",
    }
    expect_invalid(x, geometry, excluded_identities, "F01 forging source exclusion")

    print("PAPER2_DESIGNED_SOURCE_CANDIDATE_LEDGER_V1_SELFTEST_PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ledger",
        type=Path,
        default=Path("research/paper2/designed_source_candidate_ledger_v1.template.json"),
    )
    parser.add_argument(
        "--geometry",
        type=Path,
        default=Path("research/paper2/designed_corpus_geometry_v1.json"),
    )
    parser.add_argument(
        "--exclusions",
        type=Path,
        default=Path("research/paper2/designed_atlas_forging_exclusion_v1.json"),
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    geometry = load_geometry(args.geometry)
    excluded_identities = load_exclusions(args.exclusions)
    data = json.loads(args.ledger.read_text(encoding="utf-8"))
    validate(data, geometry, excluded_identities)
    if args.self_test:
        self_test(args.ledger, args.geometry, args.exclusions)
    else:
        print("PAPER2_DESIGNED_SOURCE_CANDIDATE_LEDGER_V1_VALID")


if __name__ == "__main__":
    main()
