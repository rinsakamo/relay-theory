#!/usr/bin/env python3
"""Assemble Paper 2 #239 pre-focus masked source surfaces.

Zero-model apparatus only.

Local source-facing inputs are consumed from an external directory and are never
copied into repository authority. The assembler:
  frozen #231 source identity
    -> local bounded raw source
    -> inherited #162 normalization/segmentation/masking
    -> <=32 authority-blind masked source units
    -> local receipt + final capture manifest

It does NOT perform Normal/SystemOne focus selection, ClaimIR extraction,
structural decomposition, Phi projection, or atlas analysis.
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

from paper2_extraction_bundle_prepare import canonical_json_bytes
from paper2_extraction_two_pass_prepare import (
    normalize_text,
    segment_text,
    mask_segments,
    validate_mask_policy,
)

CONTRACT_PATH = Path("research/paper2/designed_source_capture_assembly_v1.json")
DESIGNED_PATH = Path("research/paper2/designed_source_manifest_v1.json")
CAPTURE_DESCRIPTOR_PATH = Path("research/paper2/designed_source_capture_manifest_v1.json")
MASK_POLICY_PATH = Path("research/paper2/extraction_label_mask_v1.json")
PREP_IMPL_PATH = Path("scripts/paper2_extraction_two_pass_prepare.py")

INPUT_VERSION = "paper2-designed-source-capture-input-v1"
MASKED_VERSION = "paper2-designed-masked-source-surface-v1"
RECEIPT_VERSION = "paper2-designed-source-capture-receipt-v1"
FINAL_STATE = "SOURCE_CAPTURE_FROZEN"


class CaptureError(ValueError):
    pass


def fail(message: str) -> None:
    raise CaptureError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def git_blob_sha1(data: bytes) -> str:
    prefix = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(prefix + data).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canon_identity(value: dict[str, Any]) -> tuple[str, str]:
    if not isinstance(value, dict) or set(value) != {"kind", "value"}:
        fail("stable_identity field set mismatch")
    kind = value["kind"]
    raw = value["value"]
    if kind not in {"DOI", "ARXIV", "PMID"} or not isinstance(raw, str) or not raw.strip():
        fail("stable_identity invalid")
    raw = raw.strip()
    if kind == "DOI":
        raw = raw.casefold().removeprefix("https://doi.org/").removeprefix("doi:")
    else:
        raw = raw.casefold()
    return kind, raw


def validate_contract(contract: Any) -> dict[str, Any]:
    if not isinstance(contract, dict):
        fail("contract must be object")
    if contract.get("schema_version") != "paper2-designed-source-capture-assembly-v1":
        fail("contract version drift")
    if contract.get("owner_issue") != 239:
        fail("contract owner drift")
    if contract.get("status") != "SYNTHETIC_QUALIFICATION_ONLY":
        fail("contract status drift")
    if contract.get("architecture_consequence") != "NONE":
        fail("architecture consequence drift")

    assembly = contract.get("assembly")
    if not isinstance(assembly, dict):
        fail("assembly contract missing")
    exact_true = (
        "input_membership_exactly_frozen_opaque_bundle_set",
        "stable_identity_must_match_pretext_descriptor",
        "raw_text_repository_write_forbidden",
        "label_terms_repository_write_forbidden",
        "pre_focus_semantic_selection_forbidden",
        "masked_surface_preserves_all_segmented_units_in_order",
        "output_directory_must_not_exist",
        "overwrite_forbidden",
    )
    for key in exact_true:
        if assembly.get(key) is not True:
            fail(f"assembly.{key} must be true")
    if assembly.get("required_input_count") != 60 or assembly.get("model_calls") != 0:
        fail("assembly count/model-call boundary drift")

    sci = contract.get("scientific_boundary")
    if not isinstance(sci, dict) or any(value is not False for value in sci.values()):
        fail("scientific boundary must remain fully unauthorized")
    return contract


def validate_bound_authority(contract: dict[str, Any]) -> None:
    upstream = contract["upstream"]

    designed_bytes = DESIGNED_PATH.read_bytes()
    if sha256_bytes(designed_bytes) != upstream["designed_source_manifest_sha256"]:
        fail("designed source manifest digest drift")

    capture_bytes = CAPTURE_DESCRIPTOR_PATH.read_bytes()
    if sha256_bytes(capture_bytes) != upstream["pretext_capture_descriptor_sha256"]:
        fail("pretext capture descriptor digest drift")

    if git_blob_sha1(MASK_POLICY_PATH.read_bytes()) != upstream["inherited_mask_policy_blob"]:
        fail("inherited #162 mask policy blob drift")
    if git_blob_sha1(PREP_IMPL_PATH.read_bytes()) != upstream["inherited_prepare_script_blob"]:
        fail("inherited #162 prepare implementation blob drift")

    policy = load_json(MASK_POLICY_PATH)
    validate_mask_policy(policy)


INPUT_KEYS = {
    "schema_version", "bundle_id", "stable_identity", "capture_state",
    "source_version", "retrieval_date", "source_language",
    "capture_access_class", "source_locator", "raw_text", "label_groups",
    "capture_limitation",
}


def validate_label_groups(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        fail("label_groups must be list")
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for i, group in enumerate(value):
        if not isinstance(group, dict) or set(group) != {"label_id", "terms"}:
            fail(f"label_groups[{i}] fields invalid")
        label_id = group["label_id"]
        terms = group["terms"]
        if (
            not isinstance(label_id, str)
            or len(label_id) != 3
            or not label_id.startswith("L")
            or not label_id[1:].isdigit()
            or label_id in seen
        ):
            fail(f"label_groups[{i}].label_id invalid")
        seen.add(label_id)
        if not isinstance(terms, list) or not terms or any(
            not isinstance(term, str) or not term.strip() for term in terms
        ):
            fail(f"label_groups[{i}].terms invalid")
        if len({normalize_text(term).casefold() for term in terms}) != len(terms):
            fail(f"label_groups[{i}] duplicate normalized term")
        out.append({"label_id": label_id, "terms": list(terms)})
    return out


def validate_local_input(value: Any, descriptor: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != INPUT_KEYS:
        fail("capture input field set mismatch")
    if value["schema_version"] != INPUT_VERSION:
        fail("capture input version mismatch")
    if value["bundle_id"] != descriptor["opaque_bundle_id"]:
        fail("bundle_id does not match frozen descriptor")
    if canon_identity(value["stable_identity"]) != canon_identity(descriptor["stable_identity"]):
        fail("source identity does not match frozen #231 activation")
    for key in ("source_version", "retrieval_date", "source_locator"):
        if not isinstance(value[key], str) or not value[key].strip():
            fail(f"{key} must be non-empty")
    if value["source_language"] != "en":
        fail("v1 designed capture requires English source")
    state = value["capture_state"]
    access = value["capture_access_class"]
    if state not in {"CAPTURE_READY", "TERMINAL_INACCESSIBLE"}:
        fail("capture_state invalid")
    if access not in {"FULL_TEXT", "PARTIAL_TEXT", "ABSTRACT_ONLY", "INACCESSIBLE"}:
        fail("capture_access_class invalid")

    if state == "CAPTURE_READY":
        if access == "INACCESSIBLE":
            fail("ready capture cannot be inaccessible")
        if not isinstance(value["raw_text"], str) or not value["raw_text"].strip():
            fail("ready capture requires raw_text")
        validate_label_groups(value["label_groups"])
    else:
        if access != "INACCESSIBLE":
            fail("terminal inaccessible requires INACCESSIBLE")
        if value["raw_text"] is not None:
            fail("terminal inaccessible must not carry raw_text")
        if value["label_groups"] != []:
            fail("terminal inaccessible must not carry label groups")
        if not isinstance(value["capture_limitation"], str) or not value["capture_limitation"].strip():
            fail("terminal inaccessible requires capture limitation")
    if value["capture_limitation"] is not None and (
        not isinstance(value["capture_limitation"], str)
        or not value["capture_limitation"].strip()
    ):
        fail("capture_limitation invalid")
    return value


def build_masked_surface(value: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = normalize_text(value["raw_text"])
    segments = segment_text(raw)
    masked, marker_map = mask_segments(segments, value["label_groups"])
    if len(masked) != len(segments):
        fail("masking changed segment cardinality")
    surface = {
        "schema_version": MASKED_VERSION,
        "bundle_id": value["bundle_id"],
        "source_language": value["source_language"],
        "source_spans": [
            {"span_id": f"s{i}", "text": text}
            for i, text in enumerate(masked, start=1)
        ],
    }
    if not (1 <= len(surface["source_spans"]) <= 32):
        fail("masked source surface cardinality")
    receipt = {
        "schema_version": RECEIPT_VERSION,
        "bundle_id": value["bundle_id"],
        "stable_identity": copy.deepcopy(value["stable_identity"]),
        "source_version": value["source_version"],
        "retrieval_date": value["retrieval_date"],
        "capture_access_class": value["capture_access_class"],
        "source_locator": value["source_locator"],
        "raw_normalized_sha256": sha256_bytes(raw.encode("utf-8")),
        "mask_authority_sha256": sha256_json(value["label_groups"]),
        "masked_source_surface_sha256": sha256_json(surface),
        "segment_count": len(segments),
        "marker_count": len(marker_map),
        "capture_limitation": value["capture_limitation"],
        "model_calls": 0,
    }
    return surface, receipt


def receipt_bytes(receipt: dict[str, Any]) -> bytes:
    return canonical_json_bytes(receipt)


def assemble_all(
    input_dir: Path,
    output_dir: Path,
    *,
    allow_synthetic_execution: bool = False,
) -> dict[str, Any]:
    contract = validate_contract(load_json(CONTRACT_PATH))
    validate_bound_authority(contract)
    if not allow_synthetic_execution and contract["scientific_boundary"]["real_source_capture_authorized"] is not True:
        fail("REAL_SOURCE_CAPTURE_NOT_AUTHORIZED")
    if output_dir.exists():
        fail(f"OUTPUT_DIRECTORY_ALREADY_EXISTS:{output_dir}")

    capture = load_json(CAPTURE_DESCRIPTOR_PATH)
    if capture.get("state") != "CAPTURE_DESCRIPTOR_FROZEN_PRE_TEXT":
        fail("capture descriptor must be pre-text")
    descriptors = {r["opaque_bundle_id"]: r for r in capture["records"]}
    if len(descriptors) != 60:
        fail("expected 60 frozen capture descriptors")

    paths = sorted(input_dir.glob("B[0-9][0-9][0-9][0-9].json"))
    if {p.stem for p in paths} != set(descriptors):
        fail(
            "input membership mismatch: "
            f"missing={sorted(set(descriptors)-{p.stem for p in paths})} "
            f"extra={sorted({p.stem for p in paths}-set(descriptors))}"
        )

    output_dir.mkdir(parents=True, exist_ok=False)
    bundles_dir = output_dir / "masked-surfaces"
    receipts_dir = output_dir / "receipts"
    bundles_dir.mkdir()
    receipts_dir.mkdir()

    final_capture = copy.deepcopy(capture)
    final_by_bundle = {r["opaque_bundle_id"]: r for r in final_capture["records"]}
    failures: list[str] = []
    built = 0

    for path in paths:
        raw_input = path.read_bytes()
        value = json.loads(raw_input.decode("utf-8"))
        descriptor = descriptors[path.stem]
        validate_local_input(value, descriptor)
        target = final_by_bundle[path.stem]

        if value["capture_state"] == "TERMINAL_INACCESSIBLE":
            target["capture_state"] = "CAPTURE_FAILED"
            target["source_version"] = value["source_version"]
            target["retrieval_date"] = value["retrieval_date"]
            target["capture_access_class"] = "INACCESSIBLE"
            target["capture_limitation"] = value["capture_limitation"]
            failures.append(path.stem)
            receipt = {
                "schema_version": RECEIPT_VERSION,
                "bundle_id": path.stem,
                "stable_identity": copy.deepcopy(value["stable_identity"]),
                "source_version": value["source_version"],
                "retrieval_date": value["retrieval_date"],
                "capture_access_class": "INACCESSIBLE",
                "source_locator": value["source_locator"],
                "raw_normalized_sha256": None,
                "mask_authority_sha256": None,
                "masked_source_surface_sha256": None,
                "segment_count": 0,
                "marker_count": 0,
                "capture_limitation": value["capture_limitation"],
                "model_calls": 0,
            }
            (receipts_dir / f"{path.stem}.json").write_bytes(receipt_bytes(receipt))
            continue

        surface, receipt = build_masked_surface(value)
        surface_bytes = canonical_json_bytes(surface)
        receipt_raw = receipt_bytes(receipt)
        (bundles_dir / f"{path.stem}.json").write_bytes(surface_bytes)
        (receipts_dir / f"{path.stem}.json").write_bytes(receipt_raw)

        target["capture_state"] = "CAPTURED"
        target["source_version"] = value["source_version"]
        target["retrieval_date"] = value["retrieval_date"]
        target["capture_access_class"] = value["capture_access_class"]
        target["exact_span_locators"] = [
            f"{value['source_locator']}#segment={i}"
            for i in range(1, receipt["segment_count"] + 1)
        ]
        target["masked_source_surface_sha256"] = receipt["masked_source_surface_sha256"]
        target["local_evidence_descriptor_sha256"] = sha256_bytes(receipt_raw)
        target["mask_authority_sha256"] = receipt["mask_authority_sha256"]
        target["capture_limitation"] = value["capture_limitation"]
        built += 1

    summary = {
        "schema_version": "paper2-designed-source-capture-transaction-summary-v1",
        "owner_issue": 239,
        "attempted": 60,
        "captured": built,
        "terminal_inaccessible": len(failures),
        "failed_bundle_ids": failures,
        "model_calls": 0,
        "real_source_capture_authorized_by_repository_contract": contract["scientific_boundary"]["real_source_capture_authorized"],
        "classification": (
            "SOURCE_CAPTURE_FROZEN"
            if not failures
            else "PAPER2_SOURCE_CAPTURE_INSUFFICIENT"
        ),
    }

    if failures:
        # Preserve attempt evidence, but do not manufacture a frozen 60-source manifest.
        (output_dir / "capture-attempt-manifest.json").write_bytes(
            canonical_json_bytes(final_capture)
        )
    else:
        final_capture["state"] = FINAL_STATE
        final_capture["source_text_captured"] = True
        (output_dir / "frozen-source-capture-manifest.json").write_bytes(
            canonical_json_bytes(final_capture)
        )
    (output_dir / "transaction-summary.json").write_bytes(canonical_json_bytes(summary))
    return summary


def synthetic_input(bundle_id: str, identity: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "schema_version": INPUT_VERSION,
        "bundle_id": bundle_id,
        "stable_identity": copy.deepcopy(identity),
        "capture_state": "CAPTURE_READY",
        "source_version": "synthetic-v1",
        "retrieval_date": "2026-09-27",
        "source_language": "en",
        "capture_access_class": "ABSTRACT_ONLY",
        "source_locator": f"synthetic://{bundle_id}/abstract",
        "raw_text": (
            f"Working memory synthetic fixture {index} carries a bounded relation. "
            "Observed performance changes under a declared synthetic condition."
        ),
        "label_groups": [
            {"label_id": "L01", "terms": ["working memory"]}
        ],
        "capture_limitation": "SYNTHETIC_FIXTURE",
    }


def expect_failure(call, label: str, contains: str | None = None) -> None:
    try:
        call()
    except (CaptureError, json.JSONDecodeError, OSError) as exc:
        if contains and contains not in str(exc):
            raise AssertionError(f"{label}: wrong failure {exc}") from exc
        return
    raise AssertionError(f"{label}: unexpectedly succeeded")


def self_test() -> None:
    contract = validate_contract(load_json(CONTRACT_PATH))
    validate_bound_authority(contract)
    capture = load_json(CAPTURE_DESCRIPTOR_PATH)
    descriptors = {r["opaque_bundle_id"]: r for r in capture["records"]}

    with tempfile.TemporaryDirectory(prefix="relaytheory-239-") as td:
        root = Path(td)
        inputs = root / "inputs"
        inputs.mkdir()
        for i, bundle_id in enumerate(sorted(descriptors), start=1):
            value = synthetic_input(bundle_id, descriptors[bundle_id]["stable_identity"], i)
            (inputs / f"{bundle_id}.json").write_bytes(canonical_json_bytes(value))

        out = root / "out"
        summary = assemble_all(inputs, out, allow_synthetic_execution=True)
        if summary != {
            "schema_version": "paper2-designed-source-capture-transaction-summary-v1",
            "owner_issue": 239,
            "attempted": 60,
            "captured": 60,
            "terminal_inaccessible": 0,
            "failed_bundle_ids": [],
            "model_calls": 0,
            "real_source_capture_authorized_by_repository_contract": False,
            "classification": "SOURCE_CAPTURE_FROZEN",
        }:
            raise AssertionError(f"synthetic summary drift: {summary}")
        if len(list((out / "masked-surfaces").glob("B*.json"))) != 60:
            raise AssertionError("synthetic output surface count drift")
        if len(list((out / "receipts").glob("B*.json"))) != 60:
            raise AssertionError("synthetic receipt count drift")
        frozen = load_json(out / "frozen-source-capture-manifest.json")
        if frozen["state"] != FINAL_STATE or frozen["source_text_captured"] is not True:
            raise AssertionError("synthetic frozen manifest state drift")
        rendered = (out / "masked-surfaces" / "B0001.json").read_text(encoding="utf-8")
        if "working memory" in rendered.casefold():
            raise AssertionError("construct label leaked into masked source surface")
        if "[CONSTRUCT_01]" not in rendered:
            raise AssertionError("construct marker missing")

        # Real execution path must remain blocked by repository contract.
        expect_failure(
            lambda: assemble_all(inputs, root / "real-blocked"),
            "real source capture gate",
            "REAL_SOURCE_CAPTURE_NOT_AUTHORIZED",
        )

        # Stable identity mismatch fails closed.
        bad_inputs = root / "bad-identity"
        bad_inputs.mkdir()
        for p in inputs.glob("B*.json"):
            (bad_inputs / p.name).write_bytes(p.read_bytes())
        first = sorted(bad_inputs.glob("B*.json"))[0]
        bad = load_json(first)
        bad["stable_identity"]["value"] = "10.0000/wrong"
        first.write_bytes(canonical_json_bytes(bad))
        expect_failure(
            lambda: assemble_all(bad_inputs, root / "bad-identity-out", allow_synthetic_execution=True),
            "identity mismatch",
            "source identity",
        )

        # Missing one frozen opaque bundle fails before output creation.
        missing_inputs = root / "missing"
        missing_inputs.mkdir()
        for p in sorted(inputs.glob("B*.json"))[1:]:
            (missing_inputs / p.name).write_bytes(p.read_bytes())
        expect_failure(
            lambda: assemble_all(missing_inputs, root / "missing-out", allow_synthetic_execution=True),
            "membership mismatch",
            "input membership mismatch",
        )

        # One explicit inaccessible source preserves evidence but cannot freeze 60/60.
        inaccessible_inputs = root / "inaccessible"
        inaccessible_inputs.mkdir()
        for p in inputs.glob("B*.json"):
            (inaccessible_inputs / p.name).write_bytes(p.read_bytes())
        first = sorted(inaccessible_inputs.glob("B*.json"))[0]
        inc = load_json(first)
        inc["capture_state"] = "TERMINAL_INACCESSIBLE"
        inc["capture_access_class"] = "INACCESSIBLE"
        inc["raw_text"] = None
        inc["label_groups"] = []
        inc["capture_limitation"] = "SYNTHETIC_INACCESSIBLE"
        first.write_bytes(canonical_json_bytes(inc))
        inc_out = root / "inaccessible-out"
        inc_summary = assemble_all(inaccessible_inputs, inc_out, allow_synthetic_execution=True)
        if inc_summary["classification"] != "PAPER2_SOURCE_CAPTURE_INSUFFICIENT":
            raise AssertionError("inaccessible source did not fail designed capture")
        if (inc_out / "frozen-source-capture-manifest.json").exists():
            raise AssertionError("insufficient capture manufactured frozen manifest")

    print("PAPER2_DESIGNED_SOURCE_CAPTURE_ASSEMBLY_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        if args.self_test:
            self_test()
            return 0
        if args.input_dir is None or args.output_dir is None:
            fail("--input-dir and --output-dir are required outside --self-test")
        summary = assemble_all(args.input_dir, args.output_dir)
        print(json.dumps(summary, sort_keys=True))
        return 0
    except (CaptureError, json.JSONDecodeError, OSError, AssertionError) as exc:
        print(f"PAPER2_DESIGNED_SOURCE_CAPTURE_ASSEMBLY_V1_INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
