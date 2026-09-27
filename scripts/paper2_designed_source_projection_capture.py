#!/usr/bin/env python3
"""Compose Paper 2 #250 projection with #253 global masking for #239.

Production path:

  frozen #243 public full-text source
    -> #250 complete source-native abstract projection
    -> #253 one global eight-label mask vocabulary
    -> paper2-designed-masked-source-surface-v1
    -> local receipts + final #239 capture manifest

This is a zero-model source transaction. It performs no Normal/SystemOne call,
ClaimIR extraction, structural-signature generation, Phi mapping, or atlas
analysis. Raw full-text, native abstract text, and masked source text remain in
local evidence only.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

from paper2_bounded_source_projection import (
    ProjectionError,
    descriptor_map as projection_descriptor_map,
    project as project_bounded_source,
    validate_contract as validate_projection_contract,
)
from paper2_designed_mask_authority_validate import (
    MaskAuthorityError,
    validate as validate_mask_authority,
)
from paper2_extraction_bundle_prepare import canonical_json_bytes
from paper2_extraction_two_pass_prepare import PreparationError, mask_segments

BASE = Path(__file__).resolve().parent.parent
CONTRACT_PATH = BASE / "research/paper2/designed_source_projection_capture_v1.json"
CAPTURE_DESCRIPTOR_PATH = BASE / "research/paper2/designed_source_capture_manifest_v1.json"
MASK_AUTHORITY_PATH = BASE / "research/paper2/designed_extraction_mask_terms_v1.json"

BOUND_FILES = {
    "capture_descriptor_blob": BASE / "research/paper2/designed_source_capture_manifest_v1.json",
    "bounded_source_contract_blob": BASE / "research/paper2/bounded_source_projection_v1.json",
    "bounded_source_input_schema_blob": BASE / "research/paper2/bounded_source_projection_input_v1.schema.json",
    "bounded_source_surface_schema_blob": BASE / "research/paper2/bounded_source_surface_v1.schema.json",
    "bounded_source_receipt_schema_blob": BASE / "research/paper2/bounded_source_projection_receipt_v1.schema.json",
    "bounded_source_projector_blob": BASE / "scripts/paper2_bounded_source_projection.py",
    "designed_mask_authority_blob": BASE / "research/paper2/designed_extraction_mask_terms_v1.json",
    "designed_mask_validator_blob": BASE / "scripts/paper2_designed_mask_authority_validate.py",
    "inherited_prepare_script_blob": BASE / "scripts/paper2_extraction_two_pass_prepare.py",
}

CONTRACT_VERSION = "paper2-designed-source-projection-capture-v1"
MASKED_VERSION = "paper2-designed-masked-source-surface-v1"
CAPTURE_RECEIPT_VERSION = "paper2-designed-projected-source-capture-receipt-v1"
SUMMARY_VERSION = "paper2-designed-projected-source-capture-summary-v1"
FINAL_STATE = "SOURCE_CAPTURE_FROZEN"
EXPECTED_CAPTURE_DESCRIPTOR_SHA256 = (
    "ca335a00c60f8817c9e703231137decacfe1a59c4ee41fba7daa7d3d8f3228ab"
)
EXPECTED_BLOBS = {
    "capture_descriptor_blob": "b406776e866ea938531da32ae5b2cc35b081ba42",
    "bounded_source_contract_blob": "6a1415f2e85554816b5c25a3de21a08a8ae2018b",
    "bounded_source_input_schema_blob": "0867444ed163f80e186e8b8778c08c0fea72d8cd",
    "bounded_source_surface_schema_blob": "f92781de2b9def5d08c4a6fc001c1ee82aa9ce53",
    "bounded_source_receipt_schema_blob": "22af598cddaf0e1e991f5aad7d887adc0a6f26b7",
    "bounded_source_projector_blob": "1bdc206919b910797268f87cda7019f641cf85a4",
    "designed_mask_authority_blob": "30799324529d1dee12e05e603f6f7724149a75fb",
    "designed_mask_validator_blob": "0799299954de795c99af37b7fb299fd2011808a1",
    "inherited_prepare_script_blob": "bbabb1f910459c64a340bb70c2e05dd88fd6f1df",
}


class CompositionError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise CompositionError(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CompositionError(f"JSON_LOAD_FAILED:{path}:{exc}") from exc


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def canon_identity(value: dict[str, Any]) -> tuple[str, str]:
    if not isinstance(value, dict) or set(value) != {"kind", "value"}:
        fail("STABLE_IDENTITY_FIELD_SET_INVALID")
    kind = value["kind"]
    raw = value["value"]
    if kind not in {"DOI", "ARXIV", "PMID"} or not isinstance(raw, str) or not raw.strip():
        fail("STABLE_IDENTITY_INVALID")
    raw = raw.strip()
    if kind == "DOI":
        raw = raw.casefold().removeprefix("https://doi.org/").removeprefix("doi:")
    else:
        raw = raw.casefold()
    return kind, raw


def validate_composition_contract() -> dict[str, Any]:
    contract = load_json(CONTRACT_PATH)
    if contract.get("schema_version") != CONTRACT_VERSION:
        fail("COMPOSITION_CONTRACT_VERSION_DRIFT")
    if contract.get("owner_issue") != 239:
        fail("COMPOSITION_CONTRACT_OWNER_DRIFT")
    if contract.get("status") != "REAL_SOURCE_PROJECTION_CAPTURE_REAUTHORIZED_UNSPENT":
        fail("COMPOSITION_CONTRACT_STATUS_DRIFT")
    children = contract.get("terminal_children", {})
    if children != {
        "bounded_source_projection_issue": 250,
        "bounded_source_projection_classification": "PAPER2_BOUNDED_SOURCE_PROJECTION_FROZEN",
        "designed_mask_authority_issue": 253,
        "designed_mask_authority_classification": "PAPER2_DESIGNED_MASK_AUTHORITY_FROZEN",
    }:
        fail("TERMINAL_CHILD_BINDING_DRIFT")

    bound = contract.get("bound_authority", {})
    if bound.get("capture_descriptor_sha256") != EXPECTED_CAPTURE_DESCRIPTOR_SHA256:
        fail("CAPTURE_DESCRIPTOR_DECLARED_DIGEST_DRIFT")
    for key, expected in EXPECTED_BLOBS.items():
        if bound.get(key) != expected:
            fail(f"DECLARED_BOUND_BLOB_DRIFT:{key}")
        path = BOUND_FILES[key]
        if not path.is_file():
            fail(f"BOUND_FILE_MISSING:{path}")
        actual = git_blob_sha(path.read_bytes())
        if actual != expected:
            fail(f"BOUND_BLOB_DRIFT:{key}:{actual}")

    capture_raw = CAPTURE_DESCRIPTOR_PATH.read_bytes()
    if sha256_bytes(capture_raw) != EXPECTED_CAPTURE_DESCRIPTOR_SHA256:
        fail("CAPTURE_DESCRIPTOR_CONTENT_DIGEST_DRIFT")

    layout = contract.get("local_input_layout", {})
    if layout != {
        "required_bundle_directories": 60,
        "bundle_directory_pattern": "B####",
        "projection_input_filename": "projection-input.json",
        "fulltext_filename": "fulltext.bin",
        "template_filename_forbidden_during_execution": "projection-input.template.json",
        "projection_input_schema": "paper2-bounded-source-projection-input-v1",
        "arbitrary_raw_text_field": "forbidden",
        "operator_label_groups": "forbidden",
    }:
        fail("LOCAL_INPUT_LAYOUT_DRIFT")

    composition = contract.get("composition", {})
    if composition != {
        "projection_mode": "SOURCE_NATIVE_COMPLETE_ABSTRACT_ONLY",
        "fulltext_access_remains_required": True,
        "source_native_abstract_only": True,
        "body_fallback_allowed": False,
        "manual_claim_window_allowed": False,
        "semantic_search_or_selection_allowed": False,
        "summarization_allowed": False,
        "paraphrase_allowed": False,
        "truncation_allowed": False,
        "mask_authority": "research/paper2/designed_extraction_mask_terms_v1.json derived_label_groups",
        "same_global_mask_vocabulary_for_all_60": True,
        "per_source_mask_term_tuning_allowed": False,
        "masked_surface_preserves_projection_span_order": True,
        "masked_surface_preserves_projection_span_count": True,
        "model_calls": 0,
    }:
        fail("COMPOSITION_POLICY_DRIFT")

    sci = contract.get("scientific_boundary", {})
    expected_sci = {
        "real_source_projection_capture_authorized": True,
        "model_execution_authorized": False,
        "claim_ir_authorized": False,
        "structural_signature_authorized": False,
        "phi_authorized": False,
        "atlas_analysis_authorized": False,
        "paper210_execution_authorized": False,
    }
    if sci != expected_sci:
        fail("SCIENTIFIC_BOUNDARY_DRIFT")
    if contract.get("architecture_consequence") != "NONE":
        fail("ARCHITECTURE_CONSEQUENCE_DRIFT")

    # Child apparatus must validate independently under current main.
    validate_projection_contract()
    validate_mask_authority()
    return contract


def validate_projection_surface(surface: dict[str, Any], bundle_id: str) -> list[str]:
    if not isinstance(surface, dict) or set(surface) != {
        "schema_version", "bundle_id", "source_language", "source_spans"
    }:
        fail("BOUNDED_SURFACE_FIELD_SET_INVALID")
    if surface["schema_version"] != "paper2-bounded-source-surface-v1":
        fail("BOUNDED_SURFACE_VERSION_DRIFT")
    if surface["bundle_id"] != bundle_id or surface["source_language"] != "en":
        fail("BOUNDED_SURFACE_BINDING_DRIFT")
    spans = surface["source_spans"]
    if not isinstance(spans, list) or not 1 <= len(spans) <= 32:
        fail("BOUNDED_SURFACE_CARDINALITY_INVALID")
    texts: list[str] = []
    for index, span in enumerate(spans, start=1):
        if not isinstance(span, dict) or set(span) != {"span_id", "text"}:
            fail("BOUNDED_SURFACE_SPAN_FIELD_SET_INVALID")
        if span["span_id"] != f"s{index}":
            fail("BOUNDED_SURFACE_SPAN_ORDER_DRIFT")
        if not isinstance(span["text"], str) or not span["text"].strip():
            fail("BOUNDED_SURFACE_EMPTY_TEXT")
        texts.append(span["text"])
    return texts


def build_masked_surface(
    bounded: dict[str, Any],
    label_groups: list[dict[str, Any]],
) -> tuple[dict[str, Any], int]:
    texts = validate_projection_surface(bounded, bounded["bundle_id"])
    masked, marker_map = mask_segments(texts, label_groups)
    if len(masked) != len(texts):
        fail("MASKING_CHANGED_SPAN_CARDINALITY")
    surface = {
        "schema_version": MASKED_VERSION,
        "bundle_id": bounded["bundle_id"],
        "source_language": "en",
        "source_spans": [
            {"span_id": f"s{i}", "text": text}
            for i, text in enumerate(masked, start=1)
        ],
    }
    if [x["span_id"] for x in surface["source_spans"]] != [
        x["span_id"] for x in bounded["source_spans"]
    ]:
        fail("MASKING_CHANGED_SPAN_ORDER")
    return surface, len(marker_map)


def input_layout(root: Path, bundle_ids: set[str]) -> dict[str, tuple[Path, Path]]:
    if not root.is_dir():
        fail(f"INPUT_ROOT_NOT_DIRECTORY:{root}")
    found = {
        p.name for p in root.iterdir()
        if p.is_dir() and len(p.name) == 5 and p.name.startswith("B") and p.name[1:].isdigit()
    }
    if found != bundle_ids:
        fail(
            "INPUT_BUNDLE_MEMBERSHIP_MISMATCH:"
            f"missing={sorted(bundle_ids-found)}:extra={sorted(found-bundle_ids)}"
        )
    out: dict[str, tuple[Path, Path]] = {}
    for bundle in sorted(bundle_ids):
        d = root / bundle
        if (d / "projection-input.template.json").exists():
            fail(f"UNFINALIZED_TEMPLATE_PRESENT:{bundle}")
        inp = d / "projection-input.json"
        full = d / "fulltext.bin"
        if not inp.is_file():
            fail(f"PROJECTION_INPUT_MISSING:{bundle}")
        if not full.is_file():
            fail(f"FULLTEXT_FILE_MISSING:{bundle}")
        out[bundle] = (inp, full)
    return out


def make_capture_receipt(
    *,
    bundle_id: str,
    projection_receipt: dict[str, Any],
    projected_surface: dict[str, Any],
    masked_surface: dict[str, Any],
    mask_authority_sha256: str,
    marker_count: int,
) -> dict[str, Any]:
    return {
        "schema_version": CAPTURE_RECEIPT_VERSION,
        "owner_issue": 239,
        "bundle_id": bundle_id,
        "stable_identity": copy.deepcopy(projection_receipt["stable_identity"]),
        "public_fulltext_locator": projection_receipt["public_fulltext_locator"],
        "retrieved_at": projection_receipt["retrieved_at"],
        "fulltext_sha256": projection_receipt["fulltext_sha256"],
        "abstract_locator": projection_receipt["abstract_locator"],
        "projection_mode": projection_receipt["projection_mode"],
        "normalized_abstract_sha256": projection_receipt["normalized_abstract_sha256"],
        "projection_receipt_sha256": sha256_json(projection_receipt),
        "projected_surface_sha256": sha256_json(projected_surface),
        "mask_authority_sha256": mask_authority_sha256,
        "masked_source_surface_sha256": sha256_json(masked_surface),
        "segment_count": len(masked_surface["source_spans"]),
        "marker_count": marker_count,
        "model_calls": 0,
        "claim_ir_consumed": False,
        "structural_signature_consumed": False,
        "phi_consumed": False,
        "atlas_outcome_consumed": False,
    }


def compose_all(
    input_root: Path,
    output_root: Path,
    *,
    allow_synthetic_execution: bool = False,
) -> dict[str, Any]:
    contract = validate_composition_contract()
    if (
        not allow_synthetic_execution
        and contract["scientific_boundary"]["real_source_projection_capture_authorized"] is not True
    ):
        fail("REAL_SOURCE_PROJECTION_CAPTURE_NOT_AUTHORIZED")
    if output_root.exists():
        fail(f"OUTPUT_DIRECTORY_ALREADY_EXISTS:{output_root}")

    descriptors = projection_descriptor_map()
    if set(descriptors) != {f"B{i:04d}" for i in range(1, 61)}:
        fail("FROZEN_OPAQUE_BUNDLE_SET_DRIFT")
    layout = input_layout(input_root, set(descriptors))

    mask_authority = validate_mask_authority()
    label_groups = mask_authority["derived_label_groups"]
    mask_authority_sha256 = sha256_bytes(MASK_AUTHORITY_PATH.read_bytes())

    capture = load_json(CAPTURE_DESCRIPTOR_PATH)
    final_capture = copy.deepcopy(capture)
    final_by_bundle = {r["opaque_bundle_id"]: r for r in final_capture["records"]}

    output_root.mkdir(parents=True, exist_ok=False)
    projection_receipts_dir = output_root / "projection-receipts"
    bounded_dir = output_root / "bounded-surfaces"
    masked_dir = output_root / "masked-surfaces"
    capture_receipts_dir = output_root / "capture-receipts"
    for d in (projection_receipts_dir, bounded_dir, masked_dir, capture_receipts_dir):
        d.mkdir()

    failures: list[dict[str, str]] = []
    captured = 0

    for bundle_id in sorted(descriptors):
        inp_path, full_path = layout[bundle_id]
        value = load_json(inp_path)
        try:
            fulltext_bytes = full_path.read_bytes()
        except OSError as exc:
            raise CompositionError(f"FULLTEXT_READ_FAILED:{bundle_id}:{exc}") from exc

        # #250 performs frozen identity/locator/file-digest/native-abstract checks.
        projected, projection_receipt = project_bounded_source(
            value,
            descriptor=descriptors[bundle_id],
            fulltext_bytes=fulltext_bytes,
        )
        projection_receipt_raw = canonical_json_bytes(projection_receipt)
        (projection_receipts_dir / f"{bundle_id}.json").write_bytes(projection_receipt_raw)

        target = final_by_bundle[bundle_id]
        if projected is None:
            failure_class = projection_receipt["classification"]
            failures.append({"bundle_id": bundle_id, "classification": failure_class})
            target["capture_state"] = "CAPTURE_FAILED"
            target["source_version"] = "source-native-abstract-projection-v1"
            target["retrieval_date"] = projection_receipt["retrieved_at"]
            target["capture_access_class"] = "FULL_TEXT"
            target["exact_span_locators"] = []
            target["masked_source_surface_sha256"] = None
            target["local_evidence_descriptor_sha256"] = sha256_bytes(projection_receipt_raw)
            target["mask_authority_sha256"] = mask_authority_sha256
            target["capture_limitation"] = failure_class
            continue

        texts = validate_projection_surface(projected, bundle_id)
        if sha256_json(projected) != projection_receipt["projected_surface_sha256"]:
            fail(f"PROJECTED_SURFACE_DIGEST_MISMATCH:{bundle_id}")
        (bounded_dir / f"{bundle_id}.json").write_bytes(canonical_json_bytes(projected))

        try:
            masked_surface, marker_count = build_masked_surface(projected, label_groups)
        except PreparationError as exc:
            failure_class = "MASK_SEMANTIC_COLLAPSE"
            failures.append({"bundle_id": bundle_id, "classification": failure_class})
            target["capture_state"] = "CAPTURE_FAILED"
            target["source_version"] = "source-native-abstract-projection-v1"
            target["retrieval_date"] = projection_receipt["retrieved_at"]
            target["capture_access_class"] = "FULL_TEXT"
            target["exact_span_locators"] = []
            target["masked_source_surface_sha256"] = None
            target["local_evidence_descriptor_sha256"] = sha256_bytes(projection_receipt_raw)
            target["mask_authority_sha256"] = mask_authority_sha256
            target["capture_limitation"] = failure_class
            # Preserve only the failure class in durable JSON, never source text in error strings.
            continue

        if len(masked_surface["source_spans"]) != len(texts):
            fail(f"MASKED_SURFACE_CARDINALITY_DRIFT:{bundle_id}")
        masked_raw = canonical_json_bytes(masked_surface)
        (masked_dir / f"{bundle_id}.json").write_bytes(masked_raw)

        capture_receipt = make_capture_receipt(
            bundle_id=bundle_id,
            projection_receipt=projection_receipt,
            projected_surface=projected,
            masked_surface=masked_surface,
            mask_authority_sha256=mask_authority_sha256,
            marker_count=marker_count,
        )
        capture_receipt_raw = canonical_json_bytes(capture_receipt)
        (capture_receipts_dir / f"{bundle_id}.json").write_bytes(capture_receipt_raw)

        target["capture_state"] = "CAPTURED"
        target["source_version"] = "source-native-abstract-projection-v1"
        target["retrieval_date"] = projection_receipt["retrieved_at"]
        target["capture_access_class"] = "FULL_TEXT"
        abstract_locator = projection_receipt["abstract_locator"]
        target["exact_span_locators"] = [
            f"{abstract_locator}#segment=s{i}"
            for i in range(1, len(masked_surface["source_spans"]) + 1)
        ]
        target["masked_source_surface_sha256"] = capture_receipt["masked_source_surface_sha256"]
        target["local_evidence_descriptor_sha256"] = sha256_bytes(capture_receipt_raw)
        target["mask_authority_sha256"] = mask_authority_sha256
        target["capture_limitation"] = (
            "MODEL_FACING_SURFACE_SOURCE_NATIVE_ABSTRACT_ONLY;"
            "COMPLETE_FULL_TEXT_BOUND_AS_ACCESS_AND_AUDIT_AUTHORITY"
        )
        captured += 1

    summary = {
        "schema_version": SUMMARY_VERSION,
        "owner_issue": 239,
        "attempted": 60,
        "captured": captured,
        "failed": len(failures),
        "failures": failures,
        "model_calls": 0,
        "claim_ir_consumed": False,
        "structural_signature_consumed": False,
        "phi_consumed": False,
        "atlas_outcome_consumed": False,
        "real_source_projection_capture_authorized_by_repository_contract":
            contract["scientific_boundary"]["real_source_projection_capture_authorized"],
        "classification": (
            "SOURCE_CAPTURE_FROZEN"
            if not failures and captured == 60
            else "PAPER2_SOURCE_CAPTURE_INSUFFICIENT"
        ),
    }

    if summary["classification"] == "SOURCE_CAPTURE_FROZEN":
        final_capture["state"] = FINAL_STATE
        final_capture["source_text_captured"] = True
        (output_root / "frozen-source-capture-manifest.json").write_bytes(
            canonical_json_bytes(final_capture)
        )
    else:
        (output_root / "capture-attempt-manifest.json").write_bytes(
            canonical_json_bytes(final_capture)
        )
    (output_root / "transaction-summary.json").write_bytes(canonical_json_bytes(summary))
    return summary


def synthetic_projection_input(
    descriptor: dict[str, Any],
    *,
    fulltext_bytes: bytes,
    index: int,
    abstract_text: str | None = None,
    state: str = "PRESENT",
) -> dict[str, Any]:
    present = state == "PRESENT"
    if abstract_text is None and present:
        abstract_text = (
            f"Memory and Learning synthetic source {index} reports a bounded relation. "
            "Observed performance changes under a declared condition while the retained "
            "scientific description remains sufficiently rich for the masking gate."
        )
    return {
        "schema_version": "paper2-bounded-source-projection-input-v1",
        "bundle_id": descriptor["opaque_bundle_id"],
        "stable_identity": copy.deepcopy(descriptor["stable_identity"]),
        "public_fulltext_locator": descriptor["public_fulltext_locator"],
        "retrieved_at": "2026-09-27T00:00:00Z",
        "source_language": "en",
        "fulltext_sha256": sha256_bytes(fulltext_bytes),
        "abstract_state": state,
        "abstract_locator": f"synthetic://{descriptor['opaque_bundle_id']}#abstract" if present else None,
        "abstract_text": abstract_text if present else None,
        "abstract_boundary_attestation": (
            "SOURCE_NATIVE_COMPLETE_ABSTRACT_VERIFIED"
            if present
            else "NO_SOURCE_NATIVE_ABSTRACT_VERIFIED"
        ),
    }


def build_synthetic_input_root(root: Path, descriptors: dict[str, dict[str, Any]]) -> Path:
    inp = root / "inputs"
    inp.mkdir()
    for index, bundle_id in enumerate(sorted(descriptors), start=1):
        d = inp / bundle_id
        d.mkdir()
        fulltext = (
            f"Synthetic complete full-text artifact for {bundle_id}. "
            "BODY_ONLY_SENTINEL must not enter the projected abstract surface."
        ).encode("utf-8")
        (d / "fulltext.bin").write_bytes(fulltext)
        value = synthetic_projection_input(
            descriptors[bundle_id],
            fulltext_bytes=fulltext,
            index=index,
        )
        (d / "projection-input.json").write_bytes(canonical_json_bytes(value))
    return inp


def expect_failure(call, label: str, contains: str | None = None) -> None:
    try:
        call()
    except (CompositionError, ProjectionError, MaskAuthorityError, PreparationError, OSError, json.JSONDecodeError) as exc:
        if contains and contains not in str(exc):
            raise AssertionError(f"{label}: wrong failure {exc}") from exc
        return
    raise AssertionError(f"{label}: unexpectedly succeeded")


def self_test() -> None:
    contract = validate_composition_contract()
    if contract["scientific_boundary"]["model_execution_authorized"] is not False:
        raise AssertionError("model execution unexpectedly authorized")
    descriptors = projection_descriptor_map()

    with tempfile.TemporaryDirectory(prefix="relaytheory-239-compose-") as td:
        root = Path(td)
        inputs = build_synthetic_input_root(root, descriptors)

        out = root / "out"
        summary = compose_all(inputs, out, allow_synthetic_execution=True)
        if summary["classification"] != "SOURCE_CAPTURE_FROZEN":
            raise AssertionError(f"synthetic 60/60 composition failed: {summary}")
        if summary["captured"] != 60 or summary["failed"] != 0 or summary["model_calls"] != 0:
            raise AssertionError("synthetic 60/60 accounting drift")
        if len(list((out / "projection-receipts").glob("B*.json"))) != 60:
            raise AssertionError("projection receipt count drift")
        if len(list((out / "bounded-surfaces").glob("B*.json"))) != 60:
            raise AssertionError("bounded surface count drift")
        if len(list((out / "masked-surfaces").glob("B*.json"))) != 60:
            raise AssertionError("masked surface count drift")
        if len(list((out / "capture-receipts").glob("B*.json"))) != 60:
            raise AssertionError("capture receipt count drift")
        first_masked = (out / "masked-surfaces" / "B0001.json").read_text(encoding="utf-8")
        if "memory" in first_masked.casefold() or "learning" in first_masked.casefold():
            raise AssertionError("global canonical label leaked")
        if "BODY_ONLY_SENTINEL" in first_masked:
            raise AssertionError("full-text body leaked into abstract-only model surface")
        if "[CONSTRUCT_" not in first_masked:
            raise AssertionError("global mask marker missing")
        frozen = load_json(out / "frozen-source-capture-manifest.json")
        if frozen["state"] != FINAL_STATE or frozen["source_text_captured"] is not True:
            raise AssertionError("final capture manifest state drift")

        # Arbitrary raw_text / operator label_groups cannot enter the production input surface.
        injection = root / "injection"
        injection.mkdir()
        for d in inputs.iterdir():
            target = injection / d.name
            target.mkdir()
            (target / "fulltext.bin").write_bytes((d / "fulltext.bin").read_bytes())
            value = load_json(d / "projection-input.json")
            if d.name == "B0001":
                value["raw_text"] = "operator-selected body claim"
                value["label_groups"] = [{"label_id": "L99", "terms": ["custom"]}]
            (target / "projection-input.json").write_bytes(canonical_json_bytes(value))
        expect_failure(
            lambda: compose_all(injection, root / "injection-out", allow_synthetic_execution=True),
            "arbitrary raw text and mask terms",
            "FIELD_SET",
        )

        # Missing a frozen bundle fails before transaction output.
        missing = root / "missing"
        missing.mkdir()
        for d in sorted(inputs.iterdir())[1:]:
            target = missing / d.name
            target.mkdir()
            (target / "fulltext.bin").write_bytes((d / "fulltext.bin").read_bytes())
            (target / "projection-input.json").write_bytes((d / "projection-input.json").read_bytes())
        expect_failure(
            lambda: compose_all(missing, root / "missing-out", allow_synthetic_execution=True),
            "missing bundle",
            "INPUT_BUNDLE_MEMBERSHIP_MISMATCH",
        )
        if (root / "missing-out").exists():
            raise AssertionError("membership failure created output root")

        # Unfinalized scaffold templates are never executable.
        templated = root / "templated"
        templated.mkdir()
        for d in inputs.iterdir():
            target = templated / d.name
            target.mkdir()
            (target / "fulltext.bin").write_bytes((d / "fulltext.bin").read_bytes())
            (target / "projection-input.json").write_bytes((d / "projection-input.json").read_bytes())
        (templated / "B0001" / "projection-input.template.json").write_text("{}", encoding="utf-8")
        expect_failure(
            lambda: compose_all(templated, root / "templated-out", allow_synthetic_execution=True),
            "unfinalized template",
            "UNFINALIZED_TEMPLATE_PRESENT",
        )

        # No native abstract produces explicit insufficiency; no body fallback.
        absent = root / "absent"
        absent.mkdir()
        for d in inputs.iterdir():
            target = absent / d.name
            target.mkdir()
            (target / "fulltext.bin").write_bytes((d / "fulltext.bin").read_bytes())
            value = load_json(d / "projection-input.json")
            if d.name == "B0001":
                value["abstract_state"] = "ABSENT"
                value["abstract_locator"] = None
                value["abstract_text"] = None
                value["abstract_boundary_attestation"] = "NO_SOURCE_NATIVE_ABSTRACT_VERIFIED"
            (target / "projection-input.json").write_bytes(canonical_json_bytes(value))
        absent_out = root / "absent-out"
        absent_summary = compose_all(absent, absent_out, allow_synthetic_execution=True)
        if absent_summary["classification"] != "PAPER2_SOURCE_CAPTURE_INSUFFICIENT":
            raise AssertionError("absent abstract did not fail designed capture")
        if (absent_out / "frozen-source-capture-manifest.json").exists():
            raise AssertionError("absent abstract manufactured frozen manifest")
        if (absent_out / "masked-surfaces" / "B0001.json").exists():
            raise AssertionError("absent abstract manufactured body-derived masked surface")

        # 33-unit native abstract fails without truncation.
        over = root / "over"
        over.mkdir()
        for d in inputs.iterdir():
            target = over / d.name
            target.mkdir()
            (target / "fulltext.bin").write_bytes((d / "fulltext.bin").read_bytes())
            value = load_json(d / "projection-input.json")
            if d.name == "B0001":
                value["abstract_text"] = " ".join(f"Sentence {i}." for i in range(1, 34))
            (target / "projection-input.json").write_bytes(canonical_json_bytes(value))
        over_out = root / "over-out"
        over_summary = compose_all(over, over_out, allow_synthetic_execution=True)
        if over_summary["classification"] != "PAPER2_SOURCE_CAPTURE_INSUFFICIENT":
            raise AssertionError("over-bound native abstract did not fail designed capture")
        failure = next(x for x in over_summary["failures"] if x["bundle_id"] == "B0001")
        if failure["classification"] != "SOURCE_NATIVE_ABSTRACT_UNIT_BOUND_EXCEEDED":
            raise AssertionError("over-bound failure classification drift")

        # Frozen source/file binding remains active inside the composed path.
        bad_digest = root / "bad-digest"
        bad_digest.mkdir()
        for d in inputs.iterdir():
            target = bad_digest / d.name
            target.mkdir()
            (target / "fulltext.bin").write_bytes((d / "fulltext.bin").read_bytes())
            value = load_json(d / "projection-input.json")
            if d.name == "B0001":
                value["fulltext_sha256"] = "0" * 64
            (target / "projection-input.json").write_bytes(canonical_json_bytes(value))
        expect_failure(
            lambda: compose_all(bad_digest, root / "bad-digest-out", allow_synthetic_execution=True),
            "fulltext digest mismatch",
            "FULLTEXT_DIGEST_MISMATCH",
        )

        # Evidence roots are immutable.
        expect_failure(
            lambda: compose_all(inputs, out, allow_synthetic_execution=True),
            "output overwrite",
            "OUTPUT_DIRECTORY_ALREADY_EXISTS",
        )

    print("PAPER2_DESIGNED_SOURCE_PROJECTION_CAPTURE_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", type=Path)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            return 0
        if args.input_root is None or args.output_root is None:
            fail("--input-root and --output-root are required outside --self-test")
        summary = compose_all(args.input_root, args.output_root)
        print(json.dumps(summary, sort_keys=True))
        return 0 if summary["classification"] == "SOURCE_CAPTURE_FROZEN" else 3
    except (
        CompositionError,
        ProjectionError,
        MaskAuthorityError,
        PreparationError,
        OSError,
        json.JSONDecodeError,
        AssertionError,
    ) as exc:
        print(f"PAPER2_DESIGNED_SOURCE_PROJECTION_CAPTURE_V1_INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
