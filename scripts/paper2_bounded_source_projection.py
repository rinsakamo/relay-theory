#!/usr/bin/env python3
"""Freeze/test Paper 2 #250 full-text-access -> bounded-source projection.

The surviving v1 projection is intentionally narrow:

    frozen public-web full-text identity/access authority
      -> complete source-native abstract only
      -> inherited #162 normalization + sentence-like segmentation
      -> <=32-unit local pre-mask surface

No body excerpt, semantic search, summarization, paraphrase, or truncation is
permitted.  If a source has no verified source-native abstract, or that complete
abstract exceeds the inherited 32-unit bound, projection terminates explicitly.

This program performs zero model calls and produces local-only source-bearing
artifacts.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any

from paper2_extraction_two_pass_prepare import (
    MAX_SEGMENTS,
    SEGMENT_RE,
    normalize_text,
)

BASE = Path(__file__).resolve().parent.parent
CONTRACT_PATH = BASE / "research/paper2/bounded_source_projection_v1.json"
INPUT_SCHEMA_PATH = BASE / "research/paper2/bounded_source_projection_input_v1.schema.json"
SURFACE_SCHEMA_PATH = BASE / "research/paper2/bounded_source_surface_v1.schema.json"
RECEIPT_SCHEMA_PATH = BASE / "research/paper2/bounded_source_projection_receipt_v1.schema.json"
WEB_MANIFEST_PATH = BASE / "research/paper2/designed_source_web_fulltext_manifest_v1.json"
CAPTURE_DESCRIPTOR_PATH = BASE / "research/paper2/designed_source_capture_manifest_v1.json"

CONTRACT_VERSION = "paper2-bounded-source-projection-contract-v1"
INPUT_VERSION = "paper2-bounded-source-projection-input-v1"
SURFACE_VERSION = "paper2-bounded-source-surface-v1"
RECEIPT_VERSION = "paper2-bounded-source-projection-receipt-v1"
PROJECTION_MODE = "SOURCE_NATIVE_COMPLETE_ABSTRACT_ONLY"

PARENT_BLOBS = {
    "research/paper2/designed_source_manifest_v1.json":
        "dd34e2048020124561477ba8fe53f1e4e1452bb7",
    "research/paper2/designed_source_web_fulltext_manifest_v1.json":
        "be44887a8024bbf13c3a746452291e330349889a",
    "research/paper2/designed_source_capture_manifest_v1.json":
        "b406776e866ea938531da32ae5b2cc35b081ba42",
    "research/paper2/extraction_label_mask_v1.json":
        "26f52c2f49c15c559b42c527d1b918c56d935785",
    "scripts/paper2_extraction_two_pass_prepare.py":
        "bbabb1f910459c64a340bb70c2e05dd88fd6f1df",
    "research/paper2/extraction_normal_prompt_v1.md":
        "a9918f5e51f38f6307057ffc207c1a2b1d73c885",
    "research/paper2/extraction_two_pass_real_protocol_v1.json":
        "98cacc90e405486b6ae6cd4acb7f8b31289ccdef",
}

CONTENT_DIGESTS = {
    "designed_source_manifest_sha256":
        "e37ef0bf9d8a7499daddac5112b31e8fd52fb9ab727c468faa1ad337bbcd2409",
    "web_fulltext_manifest_sha256":
        "49e97c31655a3a325346327aaeb7ca00e6ab6475984d2cffe7a9b16a26c3cd57",
    "reconciled_capture_descriptor_sha256":
        "ca335a00c60f8817c9e703231137decacfe1a59c4ee41fba7daa7d3d8f3228ab",
}

INPUT_KEYS = {
    "schema_version",
    "bundle_id",
    "stable_identity",
    "public_fulltext_locator",
    "retrieved_at",
    "source_language",
    "fulltext_sha256",
    "abstract_state",
    "abstract_locator",
    "abstract_text",
    "abstract_boundary_attestation",
}

HEX64 = re.compile(r"^[0-9a-f]{64}$")


class ProjectionError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ProjectionError(message)


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProjectionError(f"JSON_LOAD_FAILED:{path}:{exc}") from exc


def canon_identity(value: dict[str, Any]) -> tuple[str, str]:
    if not isinstance(value, dict) or set(value) != {"kind", "value"}:
        fail("STABLE_IDENTITY_FIELD_SET_INVALID")
    kind = value["kind"]
    raw = value["value"]
    if kind not in {"DOI", "ARXIV", "PMID"}:
        fail("STABLE_IDENTITY_KIND_INVALID")
    if not isinstance(raw, str) or not raw.strip():
        fail("STABLE_IDENTITY_VALUE_INVALID")
    raw = raw.strip()
    if kind == "DOI":
        raw = raw.casefold().removeprefix("https://doi.org/").removeprefix("doi:")
    else:
        raw = raw.casefold()
    return kind, raw


def validate_schema_documents() -> None:
    inp = load_json(INPUT_SCHEMA_PATH)
    surf = load_json(SURFACE_SCHEMA_PATH)
    rec = load_json(RECEIPT_SCHEMA_PATH)
    if inp.get("$id") != INPUT_VERSION or inp.get("additionalProperties") is not False:
        fail("INPUT_SCHEMA_DRIFT")
    if surf.get("$id") != SURFACE_VERSION or surf.get("additionalProperties") is not False:
        fail("SURFACE_SCHEMA_DRIFT")
    if rec.get("$id") != RECEIPT_VERSION or rec.get("additionalProperties") is not False:
        fail("RECEIPT_SCHEMA_DRIFT")
    if surf["properties"]["source_spans"].get("maxItems") != MAX_SEGMENTS:
        fail("SURFACE_UNIT_BOUND_DRIFT")


def validate_contract() -> dict[str, Any]:
    contract = load_json(CONTRACT_PATH)
    if contract.get("schema_version") != CONTRACT_VERSION:
        fail("CONTRACT_VERSION_DRIFT")
    if contract.get("owner_issue") != 250 or contract.get("parent_issue") != 239:
        fail("CONTRACT_OWNER_DRIFT")
    if contract.get("status") != "SOURCE_NATIVE_ABSTRACT_PROJECTION_FROZEN":
        fail("CONTRACT_STATUS_DRIFT")
    if contract.get("bound_parent_blobs") != PARENT_BLOBS:
        fail("CONTRACT_PARENT_BLOB_MAP_DRIFT")
    for rel, expected in PARENT_BLOBS.items():
        path = BASE / rel
        if not path.is_file():
            fail(f"PARENT_FILE_MISSING:{rel}")
        actual = git_blob_sha(path.read_bytes())
        if actual != expected:
            fail(f"PARENT_BLOB_DRIFT:{rel}:{actual}")
    if contract.get("bound_content_digests") != CONTENT_DIGESTS:
        fail("CONTRACT_CONTENT_DIGEST_MAP_DRIFT")
    designed = (BASE / "research/paper2/designed_source_manifest_v1.json").read_bytes()
    web = WEB_MANIFEST_PATH.read_bytes()
    capture = CAPTURE_DESCRIPTOR_PATH.read_bytes()
    actual_digests = {
        "designed_source_manifest_sha256": sha256_bytes(designed),
        "web_fulltext_manifest_sha256": sha256_bytes(web),
        "reconciled_capture_descriptor_sha256": sha256_bytes(capture),
    }
    if actual_digests != CONTENT_DIGESTS:
        fail(f"BOUND_CONTENT_DIGEST_DRIFT:{actual_digests}")

    projection = contract.get("projection", {})
    expected_false = (
        "body_fallback_allowed",
        "body_excerpt_allowed",
        "semantic_search_or_selection_allowed",
        "summarization_allowed",
        "paraphrase_allowed",
        "manual_claim_window_allowed",
        "post_projection_truncation_allowed",
    )
    if projection.get("mode") != PROJECTION_MODE:
        fail("PROJECTION_MODE_DRIFT")
    if projection.get("source_native_abstract_boundary_must_be_verified") is not True:
        fail("ABSTRACT_BOUNDARY_AUTHORITY_DRIFT")
    for key in expected_false:
        if projection.get(key) is not False:
            fail(f"FORBIDDEN_PROJECTION_FREEDOM_DRIFT:{key}")
    if projection.get("maximum_units") != MAX_SEGMENTS:
        fail("PROJECTION_UNIT_BOUND_DRIFT")
    if projection.get("no_abstract_action") != "terminal projection failure; do not use body fallback":
        fail("NO_ABSTRACT_POLICY_DRIFT")
    if projection.get("over_bound_action") != "terminal projection failure; do not truncate":
        fail("OVER_BOUND_POLICY_DRIFT")

    boundary = contract.get("scientific_boundary", {})
    if any(boundary.values()):
        fail("SCIENTIFIC_AUTHORITY_MUST_REMAIN_FALSE")
    if contract.get("architecture_consequence") != "NONE":
        fail("ARCHITECTURE_CONSEQUENCE_DRIFT")

    validate_schema_documents()
    return contract


def descriptor_map() -> dict[str, dict[str, Any]]:
    descriptor = load_json(CAPTURE_DESCRIPTOR_PATH)
    if descriptor.get("state") != "CAPTURE_DESCRIPTOR_WEB_FULLTEXT_RECONCILED_PRE_TEXT":
        fail("CAPTURE_DESCRIPTOR_STATE_DRIFT")
    records = descriptor.get("records")
    if not isinstance(records, list) or len(records) != 60:
        fail("CAPTURE_DESCRIPTOR_COUNT_DRIFT")
    out: dict[str, dict[str, Any]] = {}
    for row in records:
        bundle = row.get("opaque_bundle_id")
        if not isinstance(bundle, str) or bundle in out:
            fail("CAPTURE_DESCRIPTOR_BUNDLE_DRIFT")
        out[bundle] = row
    if set(out) != {f"B{i:04d}" for i in range(1, 61)}:
        fail("CAPTURE_DESCRIPTOR_OPAQUE_SET_DRIFT")
    return out


def validate_input(
    value: Any,
    *,
    descriptor: dict[str, Any],
    fulltext_bytes: bytes,
) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != INPUT_KEYS:
        fail("PROJECTION_INPUT_FIELD_SET_INVALID")
    if value["schema_version"] != INPUT_VERSION:
        fail("PROJECTION_INPUT_VERSION_INVALID")
    if value["bundle_id"] != descriptor["opaque_bundle_id"]:
        fail("FROZEN_BUNDLE_BINDING_MISMATCH")
    if canon_identity(value["stable_identity"]) != canon_identity(descriptor["stable_identity"]):
        fail("FROZEN_SOURCE_BINDING_MISMATCH")
    if value["public_fulltext_locator"] != descriptor["public_fulltext_locator"]:
        fail("FROZEN_FULLTEXT_LOCATOR_MISMATCH")
    if value["source_language"] != "en":
        fail("SOURCE_LANGUAGE_INVALID")
    if not isinstance(value["retrieved_at"], str) or not value["retrieved_at"].strip():
        fail("RETRIEVED_AT_INVALID")
    if not isinstance(value["fulltext_sha256"], str) or not HEX64.fullmatch(value["fulltext_sha256"]):
        fail("FULLTEXT_SHA256_INVALID")
    actual_fulltext = sha256_bytes(fulltext_bytes)
    if value["fulltext_sha256"] != actual_fulltext:
        fail(f"FULLTEXT_DIGEST_MISMATCH:{value['fulltext_sha256']}!={actual_fulltext}")

    state = value["abstract_state"]
    attestation = value["abstract_boundary_attestation"]
    locator = value["abstract_locator"]
    text = value["abstract_text"]
    if state == "PRESENT":
        if attestation != "SOURCE_NATIVE_COMPLETE_ABSTRACT_VERIFIED":
            fail("ABSTRACT_BOUNDARY_ATTESTATION_INVALID")
        if not isinstance(locator, str) or not locator.strip():
            fail("ABSTRACT_LOCATOR_REQUIRED")
        if not isinstance(text, str) or not text.strip():
            fail("COMPLETE_ABSTRACT_TEXT_REQUIRED")
    elif state == "ABSENT":
        if attestation != "NO_SOURCE_NATIVE_ABSTRACT_VERIFIED":
            fail("ABSTRACT_ABSENCE_ATTESTATION_INVALID")
        if locator is not None or text is not None:
            fail("ABSENT_ABSTRACT_MUST_NOT_CARRY_TEXT_OR_LOCATOR")
    else:
        fail("ABSTRACT_STATE_INVALID")
    return value


def split_complete_abstract(text: str) -> tuple[str, list[str]]:
    normalized = normalize_text(text)
    segments = [part.strip() for part in SEGMENT_RE.split(normalized) if part.strip()]
    if not segments:
        fail("ABSTRACT_SEGMENTATION_EMPTY")
    return normalized, segments


def make_receipt(
    value: dict[str, Any],
    *,
    classification: str,
    normalized_abstract_sha256: str | None,
    segment_count: int,
    projected_surface_sha256: str | None,
) -> dict[str, Any]:
    return {
        "schema_version": RECEIPT_VERSION,
        "owner_issue": 250,
        "bundle_id": value["bundle_id"],
        "stable_identity": copy.deepcopy(value["stable_identity"]),
        "public_fulltext_locator": value["public_fulltext_locator"],
        "retrieved_at": value["retrieved_at"],
        "fulltext_sha256": value["fulltext_sha256"],
        "abstract_state": value["abstract_state"],
        "abstract_locator": value["abstract_locator"],
        "abstract_boundary_attestation": value["abstract_boundary_attestation"],
        "projection_mode": PROJECTION_MODE,
        "normalized_abstract_sha256": normalized_abstract_sha256,
        "segment_count": segment_count,
        "projected_surface_sha256": projected_surface_sha256,
        "classification": classification,
        "model_calls": 0,
        "claim_ir_consumed": False,
        "structural_signature_consumed": False,
        "phi_consumed": False,
        "atlas_outcome_consumed": False,
    }


def project(
    value: dict[str, Any],
    *,
    descriptor: dict[str, Any],
    fulltext_bytes: bytes,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    validate_input(value, descriptor=descriptor, fulltext_bytes=fulltext_bytes)

    if value["abstract_state"] == "ABSENT":
        return None, make_receipt(
            value,
            classification="SOURCE_NATIVE_ABSTRACT_ABSENT",
            normalized_abstract_sha256=None,
            segment_count=0,
            projected_surface_sha256=None,
        )

    normalized, segments = split_complete_abstract(value["abstract_text"])
    normalized_digest = sha256_bytes(normalized.encode("utf-8"))
    if len(segments) > MAX_SEGMENTS:
        return None, make_receipt(
            value,
            classification="SOURCE_NATIVE_ABSTRACT_UNIT_BOUND_EXCEEDED",
            normalized_abstract_sha256=normalized_digest,
            segment_count=len(segments),
            projected_surface_sha256=None,
        )

    surface = {
        "schema_version": SURFACE_VERSION,
        "bundle_id": value["bundle_id"],
        "source_language": "en",
        "source_spans": [
            {"span_id": f"s{i}", "text": text}
            for i, text in enumerate(segments, start=1)
        ],
    }
    surface_sha = sha256_bytes(canonical_json_bytes(surface))
    receipt = make_receipt(
        value,
        classification="PROJECTED_SOURCE_NATIVE_ABSTRACT",
        normalized_abstract_sha256=normalized_digest,
        segment_count=len(segments),
        projected_surface_sha256=surface_sha,
    )
    return surface, receipt


def write_exclusive(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise ProjectionError(f"OUTPUT_ALREADY_EXISTS:{path}") from exc


def execute(input_path: Path, fulltext_path: Path, output_dir: Path) -> dict[str, Any]:
    validate_contract()
    if output_dir.exists():
        fail(f"OUTPUT_DIRECTORY_ALREADY_EXISTS:{output_dir}")
    value = load_json(input_path)
    if not isinstance(value, dict):
        fail("PROJECTION_INPUT_MUST_BE_OBJECT")
    descriptors = descriptor_map()
    bundle = value.get("bundle_id")
    if bundle not in descriptors:
        fail("UNKNOWN_FROZEN_BUNDLE")
    try:
        fulltext_bytes = fulltext_path.read_bytes()
    except OSError as exc:
        raise ProjectionError(f"FULLTEXT_READ_FAILED:{fulltext_path}:{exc}") from exc

    surface, receipt = project(
        value,
        descriptor=descriptors[bundle],
        fulltext_bytes=fulltext_bytes,
    )
    output_dir.mkdir(parents=True, exist_ok=False)
    write_exclusive(
        output_dir / "projection-receipt.json",
        canonical_json_bytes(receipt),
    )
    if surface is not None:
        write_exclusive(
            output_dir / "bounded-source-surface.json",
            canonical_json_bytes(surface),
        )
    return receipt


def make_input(
    descriptor: dict[str, Any],
    *,
    fulltext_bytes: bytes,
    abstract_state: str = "PRESENT",
    abstract_text: str | None = (
        "Synthetic claim states that one variable constrains another. "
        "A second sentence records the declared condition."
    ),
) -> dict[str, Any]:
    present = abstract_state == "PRESENT"
    return {
        "schema_version": INPUT_VERSION,
        "bundle_id": descriptor["opaque_bundle_id"],
        "stable_identity": copy.deepcopy(descriptor["stable_identity"]),
        "public_fulltext_locator": descriptor["public_fulltext_locator"],
        "retrieved_at": "2026-09-27T00:00:00Z",
        "source_language": "en",
        "fulltext_sha256": sha256_bytes(fulltext_bytes),
        "abstract_state": abstract_state,
        "abstract_locator": "synthetic://source#abstract" if present else None,
        "abstract_text": abstract_text if present else None,
        "abstract_boundary_attestation": (
            "SOURCE_NATIVE_COMPLETE_ABSTRACT_VERIFIED"
            if present
            else "NO_SOURCE_NATIVE_ABSTRACT_VERIFIED"
        ),
    }


def expect_failure(call, label: str, contains: str | None = None) -> None:
    try:
        call()
    except (ProjectionError, OSError, json.JSONDecodeError) as exc:
        if contains and contains not in str(exc):
            raise AssertionError(f"{label}: wrong failure {exc}") from exc
        return
    raise AssertionError(f"{label}: unexpectedly succeeded")


def self_test() -> None:
    validate_contract()
    descriptors = descriptor_map()
    descriptor = descriptors[sorted(descriptors)[0]]
    fulltext = (
        b"Synthetic complete public-web full-text artifact. "
        b"It deliberately contains body material that must never be selected by the projection."
    )

    with tempfile.TemporaryDirectory(prefix="relaytheory-250-") as td:
        root = Path(td)
        fulltext_path = root / "fulltext.bin"
        fulltext_path.write_bytes(fulltext)

        # Happy path: only the complete source-native abstract survives.
        good = make_input(descriptor, fulltext_bytes=fulltext)
        good_path = root / "good.json"
        good_path.write_bytes(canonical_json_bytes(good))
        out = root / "good-out"
        receipt = execute(good_path, fulltext_path, out)
        if receipt["classification"] != "PROJECTED_SOURCE_NATIVE_ABSTRACT":
            raise AssertionError("valid native abstract did not project")
        if receipt["segment_count"] != 2 or receipt["model_calls"] != 0:
            raise AssertionError("valid projection metrics drift")
        surface = load_json(out / "bounded-source-surface.json")
        if set(surface) != {"schema_version", "bundle_id", "source_language", "source_spans"}:
            raise AssertionError("projection surface leaked source-facing metadata")
        if [x["span_id"] for x in surface["source_spans"]] != ["s1", "s2"]:
            raise AssertionError("projection span order drift")

        # Body excerpts cannot be smuggled in as an extra input field.
        body = copy.deepcopy(good)
        body["body_excerpt"] = "An attractive later-body claim."
        expect_failure(
            lambda: project(body, descriptor=descriptor, fulltext_bytes=fulltext),
            "body excerpt field",
            "FIELD_SET",
        )

        # Frozen identity and public full-text locator are immutable.
        wrong_identity = copy.deepcopy(good)
        wrong_identity["stable_identity"]["value"] = "10.0000/wrong"
        expect_failure(
            lambda: project(wrong_identity, descriptor=descriptor, fulltext_bytes=fulltext),
            "identity drift",
            "FROZEN_SOURCE_BINDING_MISMATCH",
        )
        wrong_locator = copy.deepcopy(good)
        wrong_locator["public_fulltext_locator"] = "https://example.invalid/not-frozen"
        expect_failure(
            lambda: project(wrong_locator, descriptor=descriptor, fulltext_bytes=fulltext),
            "locator drift",
            "FROZEN_FULLTEXT_LOCATOR_MISMATCH",
        )

        # The actual acquired complete-file digest is checked, not merely recorded.
        wrong_digest = copy.deepcopy(good)
        wrong_digest["fulltext_sha256"] = "0" * 64
        expect_failure(
            lambda: project(wrong_digest, descriptor=descriptor, fulltext_bytes=fulltext),
            "fulltext digest mismatch",
            "FULLTEXT_DIGEST_MISMATCH",
        )

        # PRESENT requires explicit complete-native-abstract attestation.
        wrong_attestation = copy.deepcopy(good)
        wrong_attestation["abstract_boundary_attestation"] = "NO_SOURCE_NATIVE_ABSTRACT_VERIFIED"
        expect_failure(
            lambda: project(wrong_attestation, descriptor=descriptor, fulltext_bytes=fulltext),
            "partial/native-boundary ambiguity",
            "ABSTRACT_BOUNDARY_ATTESTATION_INVALID",
        )

        # No native abstract is terminal; body fallback is not manufactured.
        absent = make_input(
            descriptor,
            fulltext_bytes=fulltext,
            abstract_state="ABSENT",
            abstract_text=None,
        )
        absent_path = root / "absent.json"
        absent_path.write_bytes(canonical_json_bytes(absent))
        absent_out = root / "absent-out"
        absent_receipt = execute(absent_path, fulltext_path, absent_out)
        if absent_receipt["classification"] != "SOURCE_NATIVE_ABSTRACT_ABSENT":
            raise AssertionError("abstract absence did not fail closed")
        if (absent_out / "bounded-source-surface.json").exists():
            raise AssertionError("absent abstract manufactured a body-derived surface")

        # 32 units pass; 33 units fail without truncation.
        exactly_32 = " ".join(f"Sentence {i}." for i in range(1, 33))
        exact = make_input(descriptor, fulltext_bytes=fulltext, abstract_text=exactly_32)
        surface32, receipt32 = project(exact, descriptor=descriptor, fulltext_bytes=fulltext)
        if surface32 is None or receipt32["segment_count"] != 32:
            raise AssertionError("exact 32-unit abstract should pass")
        over_32 = " ".join(f"Sentence {i}." for i in range(1, 34))
        over = make_input(descriptor, fulltext_bytes=fulltext, abstract_text=over_32)
        surface33, receipt33 = project(over, descriptor=descriptor, fulltext_bytes=fulltext)
        if surface33 is not None:
            raise AssertionError("33-unit abstract was silently truncated")
        if receipt33["classification"] != "SOURCE_NATIVE_ABSTRACT_UNIT_BOUND_EXCEEDED":
            raise AssertionError("33-unit abstract failure class drift")
        if receipt33["segment_count"] != 33:
            raise AssertionError("over-bound receipt lost observed segment count")

        # Existing evidence roots are immutable.
        expect_failure(
            lambda: execute(good_path, fulltext_path, out),
            "output overwrite",
            "OUTPUT_DIRECTORY_ALREADY_EXISTS",
        )

    print("PAPER2_BOUNDED_SOURCE_PROJECTION_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path)
    parser.add_argument("--fulltext-file", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        if args.self_test:
            self_test()
            return 0
        if args.input is None or args.fulltext_file is None or args.output_dir is None:
            fail("--input, --fulltext-file, and --output-dir are required outside --self-test")
        receipt = execute(args.input, args.fulltext_file, args.output_dir)
        print(json.dumps(receipt, sort_keys=True))
        return 0 if receipt["classification"] == "PROJECTED_SOURCE_NATIVE_ABSTRACT" else 3
    except (ProjectionError, OSError, json.JSONDecodeError, AssertionError) as exc:
        print(f"PAPER2_BOUNDED_SOURCE_PROJECTION_V1_INVALID: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
