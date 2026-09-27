#!/usr/bin/env python3
"""Validate Paper 2 #239 designed source-capture descriptors after #243.

This zero-model repository contract preserves the original opaque bundle mapping,
but rebinds source identity to the frozen public-web-full-text manifest from #243.
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
WEB_MANIFEST_VERSION = "paper2-web-fulltext-reconciliation-v1"
LEDGER_VERSION = "paper2-designed-source-candidate-ledger-v1"
PRETEXT_STATE = "CAPTURE_DESCRIPTOR_WEB_FULLTEXT_RECONCILED_PRE_TEXT"
BLINDED_VERSION = "paper2-designed-blinded-source-bundle-v1"
WEB_MANIFEST_SHA256 = "49e97c31655a3a325346327aaeb7ca00e6ab6475984d2cffe7a9b16a26c3cd57"

ROOT_KEYS = {
    "schema_version", "owner_issue", "designed_manifest_sha256",
    "web_fulltext_manifest_sha256", "state", "source_text_captured",
    "claim_ir_consumed", "phi_consumed", "atlas_outcome_consumed", "records",
}
RECORD_KEYS = {
    "slot_id", "opaque_bundle_id", "stable_identity", "canonical_locator",
    "public_fulltext_locator", "public_fulltext_verdict", "activated_rank",
    "registry_reference", "capture_state", "source_language",
    "source_version", "retrieval_date", "selection_inspection_access_class",
    "capture_access_class", "exact_span_locators", "masked_source_surface_sha256",
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
    "phi", "claim_ir", "atlas_outcome", "public_fulltext_locator",
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
    return {entry["slot_id"]: f"B{i:04d}" for i, entry in enumerate(ordered, start=1)}

def canon_identity(x: dict[str, Any]) -> tuple[str, str]:
    if not isinstance(x, dict) or set(x) != {"kind", "value"}:
        fail("malformed stable identity")
    kind = x["kind"]
    raw = x["value"]
    if kind not in {"DOI", "ARXIV", "PMID"} or not isinstance(raw, str) or not raw.strip():
        fail("invalid stable identity")
    raw = raw.strip()
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
    span_props = set(schema["properties"]["source_spans"]["items"]["properties"])
    if span_props != {"span_id", "text"}:
        fail("blinded source span schema must expose only span_id and text")

def ledger_index(ledger: dict[str, Any]) -> dict[tuple[str, int], dict[str, Any]]:
    if ledger.get("schema_version") != LEDGER_VERSION:
        fail("candidate ledger version drift")
    rows = ledger.get("records")
    if not isinstance(rows, list) or len(rows) != 180:
        fail("candidate ledger must contain 180 rows")
    out: dict[tuple[str, int], dict[str, Any]] = {}
    for row in rows:
        key = (row["slot_id"], row["candidate_rank"])
        if key in out:
            fail(f"duplicate ledger position: {key}")
        out[key] = row
    return out

def validate(
    capture: Any,
    designed: dict[str, Any],
    designed_bytes: bytes,
    web: dict[str, Any],
    web_bytes: bytes,
    ledger: dict[str, Any],
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
    if web.get("schema_version") != WEB_MANIFEST_VERSION:
        fail("unexpected web-fulltext manifest version")
    if web.get("state") != "WEB_FULLTEXT_60_SOURCE_MANIFEST_FROZEN":
        fail("web-fulltext manifest not terminally frozen")
    web_digest = digest_bytes(web_bytes)
    if web_digest != WEB_MANIFEST_SHA256 or capture["web_fulltext_manifest_sha256"] != web_digest:
        fail("web-fulltext manifest digest mismatch")
    if capture["claim_ir_consumed"] or capture["phi_consumed"] or capture["atlas_outcome_consumed"]:
        fail("downstream outcome consumed before source capture freeze")
    if capture["state"] != PRETEXT_STATE:
        fail("validator certifies reconciled pre-text descriptor state only")
    if capture["source_text_captured"] is not False:
        fail("pre-text descriptor must not claim source text capture")

    validate_blinded_schema(blinded_schema)
    lidx = ledger_index(ledger)

    designed_entries = designed["entries"]
    web_entries = web["entries"]
    records = capture["records"]
    if len(designed_entries) != 60 or len(web_entries) != 60 or len(records) != 60:
        fail("designed/web/capture records must all contain exactly 60 entries")

    expected_map = expected_bundle_map(designed_digest, designed_entries)
    original_by_slot = {e["slot_id"]: e for e in designed_entries}
    web_by_slot = {e["slot_id"]: e for e in web_entries}
    if len(original_by_slot) != 60 or len(web_by_slot) != 60:
        fail("slot identities not unique")
    if set(original_by_slot) != set(web_by_slot):
        fail("web-fulltext manifest changed slot membership")

    seen_slots: set[str] = set()
    seen_bundles: set[str] = set()
    seen_ids: set[tuple[str, str]] = set()
    rank_counts = {1: 0, 2: 0, 3: 0}
    substitutions = 0

    for i, rec in enumerate(records):
        ctx = f"records[{i}]"
        if not isinstance(rec, dict) or set(rec) != RECORD_KEYS:
            fail(f"{ctx}: keys mismatch")
        slot = rec["slot_id"]
        if slot in seen_slots or slot not in web_by_slot:
            fail(f"{ctx}: duplicate or unknown slot")
        seen_slots.add(slot)

        web_source = web_by_slot[slot]
        rank = web_source["activated_rank"]
        if rank not in {1, 2, 3}:
            fail(f"{ctx}: invalid reconciled rank")
        candidate = lidx.get((slot, rank))
        if candidate is None:
            fail(f"{ctx}: reconciled candidate absent from frozen ledger")

        for key in ("stable_identity", "activated_rank"):
            if rec[key] != web_source[key]:
                fail(f"{ctx}.{key}: drift from #243 web-fulltext manifest")
        if rec["public_fulltext_locator"] != web_source["public_fulltext_locator"]:
            fail(f"{ctx}.public_fulltext_locator: drift from #243")
        if rec["public_fulltext_verdict"] != web_source["public_fulltext_verdict"]:
            fail(f"{ctx}.public_fulltext_verdict: drift from #243")
        if rec["public_fulltext_verdict"] not in {"PASS_FULL_TEXT", "PASS_FULL_TEXT_PDF"}:
            fail(f"{ctx}: reconciled source lacks full-text PASS")

        for key in ("stable_identity", "canonical_locator", "activated_rank", "registry_reference"):
            if rec[key] != candidate[key if key != "activated_rank" else "candidate_rank"]:
                fail(f"{ctx}.{key}: drift from frozen ranked candidate")
        if rec["selection_inspection_access_class"] != candidate["source_access_class"]:
            fail(f"{ctx}.selection_inspection_access_class: ledger drift")

        bundle = rec["opaque_bundle_id"]
        if bundle in seen_bundles:
            fail(f"{ctx}: duplicate opaque bundle id")
        seen_bundles.add(bundle)
        if bundle != expected_map[slot]:
            fail(f"{ctx}: original pre-outcome opaque bundle assignment drift")

        ident = canon_identity(rec["stable_identity"])
        if ident in seen_ids:
            fail(f"{ctx}: duplicate selected source identity")
        seen_ids.add(ident)

        if rec["capture_state"] != "PENDING_SOURCE_CAPTURE":
            fail(f"{ctx}: reconciled pre-text descriptor must remain pending")
        if rec["source_language"] != "en":
            fail(f"{ctx}: v1 source language freeze expects English")
        if rec["source_version"] is not None or rec["retrieval_date"] is not None:
            fail(f"{ctx}: retrieval metadata populated before capture")
        if rec["capture_access_class"] is not None:
            fail(f"{ctx}: capture access class populated before capture")
        if rec["exact_span_locators"]:
            fail(f"{ctx}: span locators populated before capture")
        for key in (
            "masked_source_surface_sha256", "local_evidence_descriptor_sha256",
            "mask_authority_sha256", "capture_limitation",
        ):
            if rec[key] is not None:
                fail(f"{ctx}.{key}: populated before capture")

        rank_counts[rank] += 1
        if rank > 1:
            substitutions += 1

    if seen_slots != set(web_by_slot):
        fail("capture slots do not exactly equal reconciled source slots")
    if seen_bundles != {f"B{i:04d}" for i in range(1, 61)}:
        fail("opaque bundle set must be exactly B0001..B0060")
    if len(seen_ids) != 60:
        fail("reconciled source identities must be unique")
    if rank_counts != {1: 55, 2: 4, 3: 1} or substitutions != 5:
        fail("reconciled rank/substitution counts drift")
    return capture

def expect_invalid(
    capture: dict[str, Any],
    designed: dict[str, Any],
    designed_bytes: bytes,
    web: dict[str, Any],
    web_bytes: bytes,
    ledger: dict[str, Any],
    blinded_schema: dict[str, Any],
    label: str,
) -> None:
    try:
        validate(capture, designed, designed_bytes, web, web_bytes, ledger, blinded_schema)
    except ValidationError:
        return
    raise AssertionError(f"{label}: unexpectedly validated")

def self_test(
    capture_path: Path,
    designed_path: Path,
    web_path: Path,
    ledger_path: Path,
    blinded_schema_path: Path,
) -> None:
    designed_bytes = designed_path.read_bytes()
    web_bytes = web_path.read_bytes()
    designed = json.loads(designed_bytes)
    web = json.loads(web_bytes)
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    capture = json.loads(capture_path.read_text(encoding="utf-8"))
    blinded = json.loads(blinded_schema_path.read_text(encoding="utf-8"))
    validate(capture, designed, designed_bytes, web, web_bytes, ledger, blinded)

    def bad(mutator, label: str) -> None:
        x = copy.deepcopy(capture)
        mutator(x)
        expect_invalid(x, designed, designed_bytes, web, web_bytes, ledger, blinded, label)

    bad(lambda x: x["records"][0]["stable_identity"].__setitem__("value", "10.0000/wrong"), "identity drift")
    bad(lambda x: x["records"][0].__setitem__("public_fulltext_locator", "https://example.invalid/wrong"), "public locator drift")
    bad(lambda x: x["records"][0].__setitem__("activated_rank", 2), "rank drift")
    bad(lambda x: x["records"][1].__setitem__("opaque_bundle_id", x["records"][0]["opaque_bundle_id"]), "duplicate opaque id")
    bad(lambda x: x.__setitem__("phi_consumed", True), "Phi-before-capture")
    bad(lambda x: x["records"][0].__setitem__("masked_source_surface_sha256", "0" * 64), "premature source bytes")

    b = copy.deepcopy(blinded)
    b["properties"]["slot_id"] = {"type": "string"}
    b["required"].append("slot_id")
    expect_invalid(capture, designed, designed_bytes, web, web_bytes, ledger, b, "slot leakage into blinded bundle")

    print("PAPER2_DESIGNED_SOURCE_CAPTURE_RECONCILED_DESCRIPTOR_V1_SELFTEST_PASS")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", type=Path, default=Path("research/paper2/designed_source_capture_manifest_v1.json"))
    parser.add_argument("--designed", type=Path, default=Path("research/paper2/designed_source_manifest_v1.json"))
    parser.add_argument("--web-manifest", type=Path, default=Path("research/paper2/designed_source_web_fulltext_manifest_v1.json"))
    parser.add_argument("--ledger", type=Path, default=Path("research/paper2/designed_source_candidate_ledger_v1.json"))
    parser.add_argument("--blinded-schema", type=Path, default=Path("research/paper2/designed_blinded_source_bundle_v1.schema.json"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    designed_bytes = args.designed.read_bytes()
    web_bytes = args.web_manifest.read_bytes()
    designed = json.loads(designed_bytes)
    web = json.loads(web_bytes)
    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    capture = json.loads(args.capture.read_text(encoding="utf-8"))
    blinded = json.loads(args.blinded_schema.read_text(encoding="utf-8"))
    validate(capture, designed, designed_bytes, web, web_bytes, ledger, blinded)
    if args.self_test:
        self_test(args.capture, args.designed, args.web_manifest, args.ledger, args.blinded_schema)
    else:
        print("PAPER2_DESIGNED_SOURCE_CAPTURE_RECONCILED_DESCRIPTOR_V1_VALID")

if __name__ == "__main__":
    main()
