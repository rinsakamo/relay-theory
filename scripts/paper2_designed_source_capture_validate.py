#!/usr/bin/env python3
"""Validate Paper 2 #239 designed source-capture descriptors.

This is a repository-side, zero-model-call contract. It binds the terminal #231
activated source manifest to opaque extraction bundle identifiers while keeping
source-facing metadata out of extraction-visible bundle bytes.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

CAPTURE_VERSION = "paper2-designed-source-capture-manifest-v1"
DESIGNED_MANIFEST_VERSION = "paper2-designed-source-manifest-v1"
PRETEXT_STATE = "CAPTURE_DESCRIPTOR_FROZEN_PRE_TEXT"
BLINDED_VERSION = "paper2-designed-blinded-source-bundle-v1"

ROOT_KEYS = {
    "schema_version", "owner_issue", "designed_manifest_sha256", "state",
    "source_text_captured", "claim_ir_consumed", "phi_consumed",
    "atlas_outcome_consumed", "records",
}
RECORD_KEYS = {
    "slot_id", "opaque_bundle_id", "stable_identity", "canonical_locator",
    "activated_rank", "registry_reference", "capture_state",
    "source_language", "source_version", "retrieval_date", "access_class",
    "exact_span_locators", "masked_source_surface_sha256",
    "local_evidence_descriptor_sha256", "mask_authority_sha256",
    "capture_limitation",
}
BLINDED_ROOT_PROPERTIES = {
    "schema_version", "bundle_id", "source_language", "source_spans"
}
FORBIDDEN_BLINDED_FIELDS = {
    "slot_id", "sampling_stratum", "challenge_pressure", "stable_identity",
    "doi", "pmid", "arxiv", "title", "authors", "institutions", "venue",
    "citation_count", "registry_reference", "construct_labels",
    "candidate_rank", "activated_rank", "coverage_claims", "relation_family",
    "phi", "claim_ir", "atlas_outcome",
}


class ValidationError(ValueError):
    pass


def fail(msg: str) -> None:
    raise ValidationError(msg)


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pseudo_key(manifest_digest: str, slot_id: str) -> int:
    h = 2166136261
    for byte in (manifest_digest + ":" + slot_id).encode("utf-8"):
        h ^= byte
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def expected_bundle_map(manifest_digest: str, entries: list[dict[str, Any]]) -> dict[str, str]:
    ordered = sorted(entries, key=lambda e: (pseudo_key(manifest_digest, e["slot_id"]), e["slot_id"]))
    return {
        entry["slot_id"]: f"B{i:04d}"
        for i, entry in enumerate(ordered, start=1)
    }


def canon_identity(x: dict[str, Any]) -> tuple[str, str]:
    kind = x["kind"]
    raw = x["value"].strip()
    if kind == "DOI":
        raw = raw.casefold().removeprefix("https://doi.org/").removeprefix("doi:")
    else:
        raw = raw.casefold()
    return kind, raw


def validate_blinded_schema(schema: dict[str, Any]) -> None:
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        fail("blinded bundle root must be closed object")
    props = set(schema.get("properties", {}))
    required = set(schema.get("required", []))
    if props != BLINDED_ROOT_PROPERTIES or required != BLINDED_ROOT_PROPERTIES:
        fail("blinded bundle root property surface drift")
    if props & FORBIDDEN_BLINDED_FIELDS:
        fail("source-facing field leaked into blinded bundle schema")
    if schema["properties"]["schema_version"].get("const") != BLINDED_VERSION:
        fail("blinded bundle schema version mismatch")
    span_props = set(
        schema["properties"]["source_spans"]["items"]["properties"]
    )
    if span_props != {"span_id", "text"}:
        fail("blinded source span schema must expose only span_id and text")


def validate(
    capture: Any,
    designed: dict[str, Any],
    designed_bytes: bytes,
    blinded_schema: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(capture, dict) or set(capture) != ROOT_KEYS:
        fail("capture root keys mismatch")
    if capture["schema_version"] != CAPTURE_VERSION:
        fail("capture schema version mismatch")
    if capture["owner_issue"] != 239:
        fail("owner issue mismatch")
    if designed.get("schema_version") != DESIGNED_MANIFEST_VERSION:
        fail("unexpected designed manifest version")
    designed_digest = digest_bytes(designed_bytes)
    if capture["designed_manifest_sha256"] != designed_digest:
        fail("designed manifest digest mismatch")
    if capture["claim_ir_consumed"] or capture["phi_consumed"] or capture["atlas_outcome_consumed"]:
        fail("downstream outcome consumed before source capture freeze")
    if capture["state"] != PRETEXT_STATE:
        fail("this validator release certifies pre-text descriptor state only")
    if capture["source_text_captured"] is not False:
        fail("pre-text descriptor must not claim source text capture")

    validate_blinded_schema(blinded_schema)

    entries = designed["entries"]
    records = capture["records"]
    if len(entries) != 60 or len(records) != 60:
        fail("designed/capture records must both contain exactly 60 entries")

    expected_map = expected_bundle_map(designed_digest, entries)
    designed_by_slot = {e["slot_id"]: e for e in entries}
    if len(designed_by_slot) != 60:
        fail("designed manifest slot identities not unique")

    seen_slots: set[str] = set()
    seen_bundles: set[str] = set()
    seen_ids: set[tuple[str, str]] = set()

    for i, rec in enumerate(records):
        ctx = f"records[{i}]"
        if not isinstance(rec, dict) or set(rec) != RECORD_KEYS:
            fail(f"{ctx}: keys mismatch")
        slot = rec["slot_id"]
        if slot in seen_slots:
            fail(f"{ctx}: duplicate slot")
        seen_slots.add(slot)
        if slot not in designed_by_slot:
            fail(f"{ctx}: slot not activated by #231")

        source = designed_by_slot[slot]
        for key in (
            "stable_identity", "canonical_locator", "activated_rank",
            "registry_reference", "source_access_class"
        ):
            capture_key = "access_class" if key == "source_access_class" else key
            if rec[capture_key] != source[key]:
                fail(f"{ctx}.{capture_key}: drift from activated #231 source")

        bundle = rec["opaque_bundle_id"]
        if bundle in seen_bundles:
            fail(f"{ctx}: duplicate opaque bundle id")
        seen_bundles.add(bundle)
        if bundle != expected_map[slot]:
            fail(f"{ctx}: opaque bundle assignment drift")

        ident = canon_identity(rec["stable_identity"])
        if ident in seen_ids:
            fail(f"{ctx}: duplicate source identity")
        seen_ids.add(ident)

        if rec["capture_state"] != "PENDING_SOURCE_CAPTURE":
            fail(f"{ctx}: pre-text descriptor must remain pending")
        if rec["source_language"] != "en":
            fail(f"{ctx}: v1 source language freeze expects English")
        if rec["source_version"] is not None or rec["retrieval_date"] is not None:
            fail(f"{ctx}: source retrieval metadata populated before capture")
        if rec["exact_span_locators"]:
            fail(f"{ctx}: span locators populated before capture")
        for key in (
            "masked_source_surface_sha256", "local_evidence_descriptor_sha256",
            "mask_authority_sha256", "capture_limitation",
        ):
            if rec[key] is not None:
                fail(f"{ctx}.{key}: populated before capture")

    if seen_slots != set(designed_by_slot):
        fail("capture slots do not exactly equal activated #231 slots")
    if seen_bundles != {f"B{i:04d}" for i in range(1, 61)}:
        fail("opaque bundle set must be exactly B0001..B0060")
    return capture


def expect_invalid(
    capture: dict[str, Any],
    designed: dict[str, Any],
    designed_bytes: bytes,
    blinded_schema: dict[str, Any],
    label: str,
) -> None:
    try:
        validate(capture, designed, designed_bytes, blinded_schema)
    except ValidationError:
        return
    raise AssertionError(f"{label}: unexpectedly validated")


def self_test(
    capture_path: Path,
    designed_path: Path,
    blinded_schema_path: Path,
) -> None:
    designed_bytes = designed_path.read_bytes()
    designed = json.loads(designed_bytes)
    capture = json.loads(capture_path.read_text(encoding="utf-8"))
    blinded = json.loads(blinded_schema_path.read_text(encoding="utf-8"))
    validate(capture, designed, designed_bytes, blinded)

    x = copy.deepcopy(capture)
    x["records"][0]["stable_identity"]["value"] = "10.0000/wrong"
    expect_invalid(x, designed, designed_bytes, blinded, "identity drift")

    x = copy.deepcopy(capture)
    x["records"][1]["opaque_bundle_id"] = x["records"][0]["opaque_bundle_id"]
    expect_invalid(x, designed, designed_bytes, blinded, "duplicate opaque id")

    x = copy.deepcopy(capture)
    x["records"][0]["activated_rank"] = 2
    expect_invalid(x, designed, designed_bytes, blinded, "reserve substitution")

    x = copy.deepcopy(capture)
    x["phi_consumed"] = True
    expect_invalid(x, designed, designed_bytes, blinded, "Phi-before-capture")

    x = copy.deepcopy(capture)
    x["records"][0]["masked_source_surface_sha256"] = "0" * 64
    expect_invalid(x, designed, designed_bytes, blinded, "premature source bytes")

    b = copy.deepcopy(blinded)
    b["properties"]["slot_id"] = {"type": "string"}
    b["required"].append("slot_id")
    expect_invalid(capture, designed, designed_bytes, b, "slot leakage into blinded bundle")

    b = copy.deepcopy(blinded)
    b["properties"]["source_spans"]["items"]["properties"]["title"] = {"type": "string"}
    expect_invalid(capture, designed, designed_bytes, b, "title leakage inside source span")

    print("PAPER2_DESIGNED_SOURCE_CAPTURE_DESCRIPTOR_V1_SELFTEST_PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--capture",
        type=Path,
        default=Path("research/paper2/designed_source_capture_manifest_v1.json"),
    )
    parser.add_argument(
        "--designed",
        type=Path,
        default=Path("research/paper2/designed_source_manifest_v1.json"),
    )
    parser.add_argument(
        "--blinded-schema",
        type=Path,
        default=Path("research/paper2/designed_blinded_source_bundle_v1.schema.json"),
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    designed_bytes = args.designed.read_bytes()
    designed = json.loads(designed_bytes)
    capture = json.loads(args.capture.read_text(encoding="utf-8"))
    blinded = json.loads(args.blinded_schema.read_text(encoding="utf-8"))
    validate(capture, designed, designed_bytes, blinded)
    if args.self_test:
        self_test(args.capture, args.designed, args.blinded_schema)
    else:
        print("PAPER2_DESIGNED_SOURCE_CAPTURE_DESCRIPTOR_V1_VALID")


if __name__ == "__main__":
    main()
