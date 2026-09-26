#!/usr/bin/env python3
"""Validate bounded source captures and assemble opaque Paper 2 eligibility bundles.

Synthetic/apparatus owner: #221.  This program does not fetch sources, call a
model, rank works, or make an eligibility decision.  It only validates an
already-bounded capture and either emits the exact #214 source-bundle shape or
an explicit non-bundle receipt.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from paper2_eligibility_adjudication_validate import validate_source_bundle

BASE = Path(__file__).resolve().parent.parent
CONTRACT_PATH = BASE / "research/paper2/eligibility_source_capture_assembly_v1.json"
SCHEMA_PATH = BASE / "research/paper2/eligibility_source_capture_v1.schema.json"

CAPTURE_VERSION = "paper2-eligibility-source-capture-v1"
CONTRACT_VERSION = "paper2-eligibility-source-capture-assembly-v1"
BUNDLE_VERSION = "paper2-eligibility-source-bundle-v1"
RECEIPT_VERSION = "paper2-eligibility-source-capture-assembly-receipt-v1"
ASSEMBLER_VERSION = "paper2-eligibility-source-capture-assembler-v1"

PARENT_BLOBS = {
    "research/paper2/eligibility_source_bundle_v1.schema.json":
        "8513dcb205767994e7a4f97fd090c4ed1a0e3546",
    "scripts/paper2_eligibility_adjudication_validate.py":
        "2473c6acb7ea529df91979026c72bd1b151b831d",
    "research/paper2/eligibility_adjudication_v1.json":
        "5bb4c8411e1cd01bf93ca3d626cbac909afc94e8",
}

CAPTURE_STATES = {
    "CAPTURE_READY",
    "TERMINAL_INACCESSIBLE",
    "TECHNICAL_FAILURE",
    "INTEGRITY_REVIEW_REQUIRED",
    "INTEGRITY_FAILED",
}
ACCESSIBLE_STATES = {"FULL_TEXT", "PARTIAL_TEXT", "ABSTRACT_ONLY"}
ACCESS_STATES = ACCESSIBLE_STATES | {"INACCESSIBLE"}
IDENTITY_STATES = {"VERIFIED", "REVIEW_REQUIRED", "FAILED"}
PAYLOAD_STATES = {
    "INSPECTABLE_SOURCE_TEXT",
    "MISMATCH_SUSPECTED",
    "NON_SOURCE_PAYLOAD",
    "NO_PAYLOAD",
    "UNDETERMINED",
}


class CaptureError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise CaptureError(message)


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
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CaptureError(f"JSON_LOAD_FAILED:{path}:{exc}") from exc


def write_exclusive(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise CaptureError(f"OUTPUT_ALREADY_EXISTS:{path}") from exc


def validate_contract(
    contract: dict[str, Any],
    *,
    base: Path = BASE,
) -> dict[str, Any]:
    if contract.get("schema_version") != CONTRACT_VERSION:
        fail("CONTRACT_SCHEMA_DRIFT")
    if contract.get("owner_issue") != 221:
        fail("CONTRACT_OWNER_DRIFT")
    if contract.get("parent_adjudication_issue") != 214:
        fail("CONTRACT_PARENT_ADJUDICATION_DRIFT")
    if contract.get("parent_screening_issue") != 212:
        fail("CONTRACT_PARENT_SCREENING_DRIFT")
    if contract.get("status") != "APPARATUS_ONLY_REAL_SOURCE_ACQUISITION_NOT_AUTHORIZED":
        fail("CONTRACT_STATUS_DRIFT")
    if contract.get("bound_parent_blobs") != PARENT_BLOBS:
        fail("CONTRACT_PARENT_BLOB_MAP_DRIFT")
    for rel, expected in PARENT_BLOBS.items():
        path = base / rel
        if not path.is_file():
            fail(f"PARENT_FILE_MISSING:{rel}")
        actual = git_blob_sha(path.read_bytes())
        if actual != expected:
            fail(f"PARENT_BLOB_DRIFT:{rel}:{actual}")
    if contract.get("capture_schema") != CAPTURE_VERSION:
        fail("CONTRACT_CAPTURE_SCHEMA_DRIFT")
    if contract.get("output_bundle_schema") != BUNDLE_VERSION:
        fail("CONTRACT_BUNDLE_SCHEMA_DRIFT")
    if set(contract.get("capture_states", [])) != CAPTURE_STATES:
        fail("CONTRACT_CAPTURE_STATES_DRIFT")
    if set(contract.get("accessible_source_states", [])) != ACCESSIBLE_STATES:
        fail("CONTRACT_ACCESSIBLE_STATES_DRIFT")
    if contract.get("inaccessible_source_state") != "INACCESSIBLE":
        fail("CONTRACT_INACCESSIBLE_STATE_DRIFT")

    req = contract.get("assembly_requirements", {})
    if req.get("capture_state") != "CAPTURE_READY":
        fail("CONTRACT_READY_STATE_DRIFT")
    if req.get("identity_binding") != "VERIFIED":
        fail("CONTRACT_IDENTITY_REQUIREMENT_DRIFT")
    if req.get("payload_class") != "INSPECTABLE_SOURCE_TEXT":
        fail("CONTRACT_PAYLOAD_REQUIREMENT_DRIFT")
    if req.get("max_content_units") != 32:
        fail("CONTRACT_UNIT_BOUND_DRIFT")
    if req.get("max_total_utf8_bytes") != 24576:
        fail("CONTRACT_BYTE_BOUND_DRIFT")
    for flag in ("preserve_all_units_exactly_once", "preserve_unit_order"):
        if req.get(flag) is not True:
            fail(f"CONTRACT_PRESERVATION_DRIFT:{flag}")
    for flag in (
        "truncate_allowed",
        "summarize_allowed",
        "semantic_search_or_selection_allowed",
        "source_text_repair_allowed",
    ):
        if req.get(flag) is not False:
            fail(f"CONTRACT_FORBIDDEN_TRANSFORM_DRIFT:{flag}")
    if req.get("opaque_span_ids") != "s1..sn":
        fail("CONTRACT_SPAN_ID_DRIFT")

    bypass = contract.get("inaccessible_bypass", {})
    if bypass != {
        "capture_state": "TERMINAL_INACCESSIBLE",
        "source_access_status": "INACCESSIBLE",
        "bundle_emitted": False,
        "receipt_state": "SOURCE_INACCESSIBLE",
    }:
        fail("CONTRACT_INACCESSIBLE_BYPASS_DRIFT")
    technical = contract.get("technical_failure", {})
    if technical != {
        "source_access_status_must_be_null": True,
        "bundle_emitted": False,
        "receipt_state": "TECHNICAL_FAILURE",
        "may_be_relabelled_inaccessible": False,
    }:
        fail("CONTRACT_TECHNICAL_FAILURE_DRIFT")

    for field in (
        "real_ranked_work_acquisition_authorized",
        "real_model_execution_authorized",
        "heldout_screening_authorized",
        "claim_ir_authorized",
        "decomposition_authorized",
        "null_execution_authorized",
    ):
        if contract.get(field) is not False:
            fail(f"AUTHORITY_DRIFT:{field}")
    if contract.get("architecture_consequence") != "NONE":
        fail("ARCHITECTURE_CONSEQUENCE_DRIFT")
    return contract


def validate_schema_document(schema: dict[str, Any]) -> None:
    if schema.get("$id") != CAPTURE_VERSION:
        fail("SCHEMA_ID_DRIFT")
    if schema.get("additionalProperties") is not False:
        fail("SCHEMA_ADDITIONAL_PROPERTIES_DRIFT")
    if schema.get("properties", {}).get("schema_version", {}).get("const") != CAPTURE_VERSION:
        fail("SCHEMA_VERSION_DRIFT")
    states = set(schema["properties"]["capture_state"]["enum"])
    if states != CAPTURE_STATES:
        fail("SCHEMA_CAPTURE_STATES_DRIFT")


def content_digest(units: list[dict[str, Any]]) -> str:
    return sha256_bytes(canonical_json_bytes(units))


def validate_capture(
    capture: dict[str, Any],
    *,
    contract: dict[str, Any],
) -> dict[str, Any]:
    exact = {
        "schema_version",
        "capture_id",
        "provider_work_id",
        "capture_state",
        "source_access_status",
        "source_language",
        "source_kind",
        "stable_locator",
        "retrieved_at",
        "captured_content_sha256",
        "content_units",
        "integrity",
    }
    if set(capture) != exact:
        fail(
            "CAPTURE_FIELD_SET_INVALID:"
            f"missing={sorted(exact-set(capture))}:"
            f"extra={sorted(set(capture)-exact)}"
        )
    if capture["schema_version"] != CAPTURE_VERSION:
        fail("CAPTURE_SCHEMA_MISMATCH")
    capture_id = capture["capture_id"]
    if (
        not isinstance(capture_id, str)
        or len(capture_id) != 5
        or capture_id[0] != "E"
        or not capture_id[1:].isdigit()
    ):
        fail("CAPTURE_ID_INVALID")
    if not isinstance(capture["provider_work_id"], str) or not capture["provider_work_id"]:
        fail("PROVIDER_WORK_ID_INVALID")
    state = capture["capture_state"]
    if state not in CAPTURE_STATES:
        fail("CAPTURE_STATE_INVALID")
    access = capture["source_access_status"]
    if access is not None and access not in ACCESS_STATES:
        fail("SOURCE_ACCESS_STATUS_INVALID")
    for field in ("source_kind", "stable_locator", "retrieved_at"):
        if not isinstance(capture[field], str) or not capture[field].strip():
            fail(f"CAPTURE_STRING_INVALID:{field}")
    language = capture["source_language"]
    if language is not None and (
        not isinstance(language, str) or len(language.strip()) < 2
    ):
        fail("SOURCE_LANGUAGE_INVALID")

    integrity = capture["integrity"]
    if not isinstance(integrity, dict) or set(integrity) != {
        "identity_binding",
        "payload_class",
    }:
        fail("INTEGRITY_FIELD_SET_INVALID")
    if integrity["identity_binding"] not in IDENTITY_STATES:
        fail("IDENTITY_BINDING_INVALID")
    if integrity["payload_class"] not in PAYLOAD_STATES:
        fail("PAYLOAD_CLASS_INVALID")

    units = capture["content_units"]
    if not isinstance(units, list):
        fail("CONTENT_UNITS_INVALID")
    max_units = contract["assembly_requirements"]["max_content_units"]
    if len(units) > max_units:
        fail(f"CAPTURE_UNIT_BOUND_EXCEEDED:{len(units)}>{max_units}")
    seen: set[str] = set()
    total_bytes = 0
    for index, unit in enumerate(units, start=1):
        if not isinstance(unit, dict) or set(unit) != {
            "capture_unit_id",
            "source_locator",
            "text",
        }:
            fail(f"CONTENT_UNIT_FIELD_SET_INVALID:{index}")
        expected_id = f"u{index}"
        if unit["capture_unit_id"] != expected_id:
            fail(
                f"CONTENT_UNIT_ORDER_OR_ID_INVALID:{unit['capture_unit_id']}!={expected_id}"
            )
        if unit["capture_unit_id"] in seen:
            fail(f"DUPLICATE_CONTENT_UNIT_ID:{unit['capture_unit_id']}")
        seen.add(unit["capture_unit_id"])
        if not isinstance(unit["source_locator"], str) or not unit["source_locator"].strip():
            fail(f"SOURCE_LOCATOR_INVALID:{expected_id}")
        if not isinstance(unit["text"], str) or not unit["text"].strip():
            fail(f"CONTENT_TEXT_INVALID:{expected_id}")
        total_bytes += len(unit["text"].encode("utf-8"))

    max_bytes = contract["assembly_requirements"]["max_total_utf8_bytes"]
    if total_bytes > max_bytes:
        fail(f"CAPTURE_BYTE_BOUND_EXCEEDED:{total_bytes}>{max_bytes}")

    expected_content_digest = content_digest(units)
    if capture["captured_content_sha256"] != expected_content_digest:
        fail(
            "CAPTURED_CONTENT_SHA256_MISMATCH:"
            f"{capture['captured_content_sha256']}!={expected_content_digest}"
        )

    # State-specific fail-closed semantics.
    if state == "CAPTURE_READY":
        if access not in ACCESSIBLE_STATES:
            fail("READY_CAPTURE_REQUIRES_ACCESSIBLE_SOURCE_STATE")
        if not isinstance(language, str) or len(language.strip()) < 2:
            fail("READY_CAPTURE_REQUIRES_LANGUAGE")
        if not units:
            fail("READY_CAPTURE_REQUIRES_CONTENT")
        if integrity != {
            "identity_binding": "VERIFIED",
            "payload_class": "INSPECTABLE_SOURCE_TEXT",
        }:
            fail("READY_CAPTURE_INTEGRITY_NOT_QUALIFIED")
    elif state == "TERMINAL_INACCESSIBLE":
        if access != "INACCESSIBLE":
            fail("TERMINAL_INACCESSIBLE_REQUIRES_INACCESSIBLE_STATE")
        if units:
            fail("TERMINAL_INACCESSIBLE_MUST_HAVE_NO_CONTENT")
        if integrity["payload_class"] != "NO_PAYLOAD":
            fail("TERMINAL_INACCESSIBLE_PAYLOAD_CLASS_INVALID")
        if integrity["identity_binding"] != "VERIFIED":
            fail("TERMINAL_INACCESSIBLE_REQUIRES_VERIFIED_WORK_IDENTITY")
    elif state == "TECHNICAL_FAILURE":
        if access is not None:
            fail("TECHNICAL_FAILURE_MUST_NOT_ASSIGN_SOURCE_ACCESS_STATE")
        if units:
            fail("TECHNICAL_FAILURE_MUST_NOT_EXPOSE_PARTIAL_PAYLOAD")
        if integrity["payload_class"] != "UNDETERMINED":
            fail("TECHNICAL_FAILURE_PAYLOAD_MUST_BE_UNDETERMINED")
    elif state == "INTEGRITY_REVIEW_REQUIRED":
        if integrity["identity_binding"] != "REVIEW_REQUIRED" and integrity[
            "payload_class"
        ] != "MISMATCH_SUSPECTED":
            fail("REVIEW_REQUIRED_REASON_MISSING")
    elif state == "INTEGRITY_FAILED":
        if integrity["identity_binding"] != "FAILED" and integrity[
            "payload_class"
        ] != "NON_SOURCE_PAYLOAD":
            fail("INTEGRITY_FAILED_REASON_MISSING")

    return {
        "total_utf8_bytes": total_bytes,
        "content_unit_count": len(units),
        "captured_content_sha256": expected_content_digest,
    }


def receipt_state(capture: dict[str, Any]) -> str:
    state = capture["capture_state"]
    if state == "CAPTURE_READY":
        return "BUNDLE_ASSEMBLED"
    if state == "TERMINAL_INACCESSIBLE":
        return "SOURCE_INACCESSIBLE"
    if state == "TECHNICAL_FAILURE":
        return "TECHNICAL_FAILURE"
    if state == "INTEGRITY_REVIEW_REQUIRED":
        return "INTEGRITY_REVIEW_REQUIRED"
    if state == "INTEGRITY_FAILED":
        return "INTEGRITY_FAILED"
    fail("UNKNOWN_CAPTURE_STATE")


def assemble(
    capture: dict[str, Any],
    *,
    capture_raw: bytes,
    contract: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    metrics = validate_capture(capture, contract=contract)
    bundle: dict[str, Any] | None = None
    mapping: list[dict[str, str]] = []
    bundle_sha: str | None = None

    if capture["capture_state"] == "CAPTURE_READY":
        spans = []
        for index, unit in enumerate(capture["content_units"], start=1):
            span_id = f"s{index}"
            spans.append({"span_id": span_id, "text": unit["text"]})
            mapping.append(
                {
                    "span_id": span_id,
                    "capture_unit_id": unit["capture_unit_id"],
                    "source_locator": unit["source_locator"],
                }
            )
        bundle = {
            "schema_version": BUNDLE_VERSION,
            "bundle_id": capture["capture_id"],
            "source_language": capture["source_language"],
            "source_access_status": capture["source_access_status"],
            "source_spans": spans,
        }
        validate_source_bundle(bundle)
        bundle_sha = sha256_bytes(canonical_json_bytes(bundle))

        # Mechanical preservation proof: same count/order/text; no transform.
        if [x["text"] for x in bundle["source_spans"]] != [
            x["text"] for x in capture["content_units"]
        ]:
            fail("TEXT_PRESERVATION_FAILURE")
        if [x["span_id"] for x in bundle["source_spans"]] != [
            f"s{i}" for i in range(1, len(bundle["source_spans"]) + 1)
        ]:
            fail("OPAQUE_SPAN_SEQUENCE_FAILURE")

    receipt = {
        "schema_version": RECEIPT_VERSION,
        "owner_issue": 221,
        "assembler_version": ASSEMBLER_VERSION,
        "capture_id": capture["capture_id"],
        "provider_work_id": capture["provider_work_id"],
        "capture_state": capture["capture_state"],
        "source_access_status": capture["source_access_status"],
        "capture_sha256": sha256_bytes(capture_raw),
        "captured_content_sha256": metrics["captured_content_sha256"],
        "integrity": copy.deepcopy(capture["integrity"]),
        "bundle_emitted": bundle is not None,
        "bundle_sha256": bundle_sha,
        "span_mapping": mapping,
        "receipt_state": receipt_state(capture),
        "model_calls": 0,
    }
    required = set(contract["receipt_required_fields"])
    if set(receipt) != required:
        fail("RECEIPT_FIELD_SET_DRIFT")
    return bundle, receipt


def execute(capture_path: Path, output_dir: Path) -> dict[str, Any]:
    if output_dir.exists():
        fail(f"OUTPUT_DIRECTORY_ALREADY_EXISTS:{output_dir}")
    contract = validate_contract(load_json(CONTRACT_PATH))
    validate_schema_document(load_json(SCHEMA_PATH))
    capture_raw = capture_path.read_bytes()
    try:
        capture = json.loads(capture_raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CaptureError(f"CAPTURE_JSON_INVALID:{exc}") from exc
    if not isinstance(capture, dict):
        fail("CAPTURE_MUST_BE_OBJECT")

    bundle, receipt = assemble(
        capture,
        capture_raw=capture_raw,
        contract=contract,
    )
    output_dir.mkdir(parents=True, exist_ok=False)
    try:
        write_exclusive(
            output_dir / "capture.json",
            capture_raw,
        )
        if bundle is not None:
            write_exclusive(
                output_dir / "source-bundle.json",
                canonical_json_bytes(bundle),
            )
        write_exclusive(
            output_dir / "assembly-receipt.json",
            canonical_json_bytes(receipt),
        )
    except Exception:
        # Preserve any durable evidence already written; never overwrite/retry.
        raise
    return receipt


def make_capture(
    *,
    capture_id: str = "E0001",
    state: str = "CAPTURE_READY",
    access: str | None = "ABSTRACT_ONLY",
    units: list[dict[str, str]] | None = None,
    integrity: dict[str, str] | None = None,
    language: str | None = "en",
    provider_work_id: str = "W-SYNTHETIC-1",
) -> dict[str, Any]:
    if units is None:
        units = [
            {
                "capture_unit_id": "u1",
                "source_locator": "abstract:p1",
                "text": "A synthetic bounded source claim about a general capacity.",
            },
            {
                "capture_unit_id": "u2",
                "source_locator": "abstract:p2",
                "text": "The synthetic capacity changes behavior under a stated condition.",
            },
        ]
    if integrity is None:
        integrity = {
            "identity_binding": "VERIFIED",
            "payload_class": "INSPECTABLE_SOURCE_TEXT",
        }
    return {
        "schema_version": CAPTURE_VERSION,
        "capture_id": capture_id,
        "provider_work_id": provider_work_id,
        "capture_state": state,
        "source_access_status": access,
        "source_language": language,
        "source_kind": "SYNTHETIC_SOURCE",
        "stable_locator": "synthetic://source/1",
        "retrieved_at": "2026-09-26T00:00:00Z",
        "captured_content_sha256": content_digest(units),
        "content_units": units,
        "integrity": integrity,
    }


def expect_failure(call, label: str, contains: str | None = None) -> None:
    try:
        call()
    except CaptureError as exc:
        if contains is not None and contains not in str(exc):
            raise AssertionError(
                f"{label}: wrong failure {exc!s}; expected {contains}"
            ) from exc
        return
    raise AssertionError(f"{label}: expected failure")


def self_test() -> None:
    contract = validate_contract(load_json(CONTRACT_PATH))
    validate_schema_document(load_json(SCHEMA_PATH))

    with tempfile.TemporaryDirectory(prefix="relaytheory-221-") as td:
        root = Path(td)

        # 1. verified ABSTRACT_ONLY -> valid opaque #214 bundle.
        abstract = make_capture()
        raw = canonical_json_bytes(abstract)
        bundle, receipt = assemble(abstract, capture_raw=raw, contract=contract)
        assert bundle is not None
        validate_source_bundle(bundle)
        assert receipt["receipt_state"] == "BUNDLE_ASSEMBLED"
        assert receipt["model_calls"] == 0

        # 2. verified bounded FULL_TEXT capture.
        full = make_capture(
            capture_id="E0002",
            access="FULL_TEXT",
            units=[
                {"capture_unit_id":"u1","source_locator":"sec:1","text":"First bounded full-text unit."},
                {"capture_unit_id":"u2","source_locator":"sec:2","text":"Second bounded full-text unit."},
                {"capture_unit_id":"u3","source_locator":"sec:3","text":"Third bounded full-text unit."},
            ],
        )
        full_bundle, _ = assemble(
            full, capture_raw=canonical_json_bytes(full), contract=contract
        )
        assert full_bundle is not None
        validate_source_bundle(full_bundle)

        # 3. exact order/text preservation.
        assert [x["text"] for x in full_bundle["source_spans"]] == [
            x["text"] for x in full["content_units"]
        ]
        assert [x["span_id"] for x in full_bundle["source_spans"]] == [
            "s1", "s2", "s3"
        ]

        # 4. deterministic repeated assembly.
        bundle2, receipt2 = assemble(
            abstract, capture_raw=raw, contract=contract
        )
        assert canonical_json_bytes(bundle) == canonical_json_bytes(bundle2)
        assert receipt["bundle_sha256"] == receipt2["bundle_sha256"]

        # 5. changed text + stale content digest rejects.
        stale = copy.deepcopy(abstract)
        stale["content_units"][0]["text"] += " changed"
        expect_failure(
            lambda: assemble(stale, capture_raw=canonical_json_bytes(stale), contract=contract),
            "stale content hash",
            "CAPTURED_CONTENT_SHA256_MISMATCH",
        )

        # 6. authority/provenance metadata is absent from model-facing bytes.
        rendered = canonical_json_bytes(bundle).decode("utf-8")
        for leaked in (
            abstract["provider_work_id"],
            abstract["stable_locator"],
            abstract["content_units"][0]["source_locator"],
        ):
            assert leaked not in rendered
        assert set(bundle) == {
            "schema_version",
            "bundle_id",
            "source_language",
            "source_access_status",
            "source_spans",
        }

        # 7. suspected mismatch is review-required and cannot emit a bundle.
        mismatch = make_capture(
            capture_id="E0003",
            state="INTEGRITY_REVIEW_REQUIRED",
            integrity={
                "identity_binding":"REVIEW_REQUIRED",
                "payload_class":"MISMATCH_SUSPECTED",
            },
        )
        mismatch_bundle, mismatch_receipt = assemble(
            mismatch, capture_raw=canonical_json_bytes(mismatch), contract=contract
        )
        assert mismatch_bundle is None
        assert mismatch_receipt["receipt_state"] == "INTEGRITY_REVIEW_REQUIRED"

        # 8. non-source payload is integrity-failed and cannot emit a bundle.
        boilerplate = make_capture(
            capture_id="E0004",
            state="INTEGRITY_FAILED",
            integrity={
                "identity_binding":"VERIFIED",
                "payload_class":"NON_SOURCE_PAYLOAD",
            },
        )
        boilerplate_bundle, boilerplate_receipt = assemble(
            boilerplate,
            capture_raw=canonical_json_bytes(boilerplate),
            contract=contract,
        )
        assert boilerplate_bundle is None
        assert boilerplate_receipt["receipt_state"] == "INTEGRITY_FAILED"

        # 9. technical failure cannot be relabelled as source inaccessible.
        technical = make_capture(
            capture_id="E0005",
            state="TECHNICAL_FAILURE",
            access=None,
            units=[],
            language=None,
            integrity={
                "identity_binding":"VERIFIED",
                "payload_class":"UNDETERMINED",
            },
        )
        technical["captured_content_sha256"] = content_digest([])
        technical_bundle, technical_receipt = assemble(
            technical,
            capture_raw=canonical_json_bytes(technical),
            contract=contract,
        )
        assert technical_bundle is None
        assert technical_receipt["receipt_state"] == "TECHNICAL_FAILURE"
        bad_technical = copy.deepcopy(technical)
        bad_technical["source_access_status"] = "INACCESSIBLE"
        expect_failure(
            lambda: assemble(
                bad_technical,
                capture_raw=canonical_json_bytes(bad_technical),
                contract=contract,
            ),
            "technical is not inaccessible",
            "TECHNICAL_FAILURE_MUST_NOT_ASSIGN_SOURCE_ACCESS_STATE",
        )

        # 10. terminal inaccessible is an explicit bypass, never an empty bundle.
        inaccessible = make_capture(
            capture_id="E0006",
            state="TERMINAL_INACCESSIBLE",
            access="INACCESSIBLE",
            units=[],
            language=None,
            integrity={
                "identity_binding":"VERIFIED",
                "payload_class":"NO_PAYLOAD",
            },
        )
        inaccessible["captured_content_sha256"] = content_digest([])
        inaccessible_bundle, inaccessible_receipt = assemble(
            inaccessible,
            capture_raw=canonical_json_bytes(inaccessible),
            contract=contract,
        )
        assert inaccessible_bundle is None
        assert inaccessible_receipt["receipt_state"] == "SOURCE_INACCESSIBLE"

        # 11a. unit-bound overflow rejects instead of truncating.
        too_many_units = [
            {
                "capture_unit_id":f"u{i}",
                "source_locator":f"unit:{i}",
                "text":"x",
            }
            for i in range(1, 34)
        ]
        over_units = make_capture(
            capture_id="E0007",
            units=too_many_units,
        )
        expect_failure(
            lambda: assemble(
                over_units,
                capture_raw=canonical_json_bytes(over_units),
                contract=contract,
            ),
            "unit bound",
            "CAPTURE_UNIT_BOUND_EXCEEDED",
        )

        # 11b. byte-bound overflow rejects instead of truncating.
        over_bytes = make_capture(
            capture_id="E0008",
            units=[
                {
                    "capture_unit_id":"u1",
                    "source_locator":"oversize",
                    "text":"x" * (contract["assembly_requirements"]["max_total_utf8_bytes"] + 1),
                }
            ],
        )
        expect_failure(
            lambda: assemble(
                over_bytes,
                capture_raw=canonical_json_bytes(over_bytes),
                contract=contract,
            ),
            "byte bound",
            "CAPTURE_BYTE_BOUND_EXCEEDED",
        )

        # 12. downstream/basis/decomposition field injection fails closed.
        injected = copy.deepcopy(abstract)
        injected["basis_mapping"] = {"anything":"forbidden"}
        expect_failure(
            lambda: assemble(
                injected,
                capture_raw=canonical_json_bytes(injected),
                contract=contract,
            ),
            "downstream injection",
            "CAPTURE_FIELD_SET_INVALID",
        )
        nested = copy.deepcopy(abstract)
        nested["content_units"][0]["decomposition"] = "PASS"
        nested["captured_content_sha256"] = content_digest(nested["content_units"])
        expect_failure(
            lambda: assemble(
                nested,
                capture_raw=canonical_json_bytes(nested),
                contract=contract,
            ),
            "nested downstream injection",
            "CONTENT_UNIT_FIELD_SET_INVALID",
        )

        # 13. every accessible emitted fixture validates under existing #214.
        for candidate in (bundle, full_bundle, bundle2):
            assert candidate is not None
            validate_source_bundle(candidate)

        # Execute-once output directory and stable durable bytes.
        capture_path = root / "capture.json"
        capture_path.write_bytes(raw)
        receipt_exec = execute(capture_path, root / "out")
        assert receipt_exec["bundle_sha256"] == receipt["bundle_sha256"]
        expect_failure(
            lambda: execute(capture_path, root / "out"),
            "output replay",
            "OUTPUT_DIRECTORY_ALREADY_EXISTS",
        )

    print("PAPER2_SOURCE_CAPTURE_ASSEMBLY_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--capture", type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    if args.self_test:
        try:
            self_test()
            return 0
        except (AssertionError, CaptureError, OSError) as exc:
            print(f"PAPER2_SOURCE_CAPTURE_ASSEMBLY_SELFTEST_FAIL: {exc}")
            return 2

    if args.capture is None or args.output_dir is None:
        parser.error("--capture and --output-dir are required")
    try:
        receipt = execute(args.capture, args.output_dir)
    except CaptureError as exc:
        print(json.dumps({
            "classification":"PAPER2_SOURCE_CAPTURE_ASSEMBLY_NOT_QUALIFIED",
            "error":str(exc),
            "model_calls":0,
        }, sort_keys=True))
        return 2
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
