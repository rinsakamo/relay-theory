#!/usr/bin/env python3
"""Validate a frozen two-pass Paper 2 extraction execution receipt.

Owner: #147.

This validator checks package authority, same extractor/configuration,
candidate-file integrity, five-bundle completeness, candidate syntax,
and matched source/bundle digests across passes.

It does NOT independently prove that two runtime contexts were isolated.
The isolation block is explicitly an executor attestation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from paper2_extraction_procedure_validate import (
    ContractError as CandidateContractError,
    validate_candidate,
)


RECEIPT_VERSION = "paper2-extraction-execution-receipt-v1"
PACKAGE_VERSION = "paper2-extraction-run-package-v1"
PACKAGE_MERGE = "31346f0c128876201e0407bb5cbb6102428b60e8"
PROMPT_SHA256 = "dfbbf50c0cfad985abb091560a1d2db6d35f5e768d574841c151afd27a2e78f6"
EXPECTED_BUNDLES = {"B0001", "B0002", "B0003", "B0004", "B0005"}
HEX64 = set("0123456789abcdef")


class ReceiptError(ValueError):
    pass


def fail(message: str) -> None:
    raise ReceiptError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_hex64(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(ch in HEX64 for ch in value)
    )


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_package(package: dict[str, Any]) -> dict[str, str]:
    if package.get("schema_version") != PACKAGE_VERSION:
        fail("run package schema mismatch")
    authority = package.get("authority")
    if not isinstance(authority, dict):
        fail("run package authority missing")
    if authority.get("prompt_sha256_utf8") != PROMPT_SHA256:
        fail("run package prompt digest mismatch")

    sources = package.get("sources")
    if not isinstance(sources, list) or len(sources) != 5:
        fail("run package source count mismatch")

    mapping: dict[str, str] = {}
    for source in sources:
        if not isinstance(source, dict):
            fail("run package source must be object")
        bundle = source.get("bundle_id")
        digest = source.get("abstract_sha256_nfkc_ws1")
        if bundle not in EXPECTED_BUNDLES:
            fail(f"unexpected run-package bundle {bundle!r}")
        if not is_hex64(digest):
            fail(f"invalid source digest for {bundle}")
        mapping[bundle] = digest

    if set(mapping) != EXPECTED_BUNDLES:
        fail("run package bundle membership mismatch")
    return mapping


def validate_candidate_file(
    candidate_path: Path,
    expected_bundle: str,
    expected_sha: str,
) -> None:
    raw = candidate_path.read_bytes()
    actual_sha = sha256_bytes(raw)
    if actual_sha != expected_sha:
        fail(
            f"{candidate_path}: candidate digest mismatch "
            f"expected={expected_sha} actual={actual_sha}"
        )

    candidate = json.loads(raw.decode("utf-8"))
    if candidate.get("bundle_id") != expected_bundle:
        fail(f"{candidate_path}: candidate bundle_id mismatch")

    # Actual Stage-B bundles contain exactly one bounded abstract span, s1.
    # A placeholder source object is sufficient to validate candidate syntax
    # and source-span references without storing the copyrighted abstract.
    placeholder_source = {
        "schema_version": "paper2-extraction-source-bundle-v1",
        "bundle_id": expected_bundle,
        "source_language": "en",
        "source_spans": [{"span_id": "s1", "text": "digest-verified external source"}],
    }
    try:
        validate_candidate(candidate, placeholder_source)
    except CandidateContractError as exc:
        fail(f"{candidate_path}: invalid extraction candidate: {exc}") from exc


def validate_receipt(
    receipt: dict[str, Any],
    package: dict[str, Any],
    receipt_path: Path,
    *,
    check_files: bool,
) -> None:
    if receipt.get("schema_version") != RECEIPT_VERSION:
        fail("receipt schema_version mismatch")
    if receipt.get("owner_issue") != 147:
        fail("receipt owner_issue mismatch")
    if receipt.get("status") != "CANDIDATES_FROZEN_BEFORE_COMPARISON":
        fail("receipt status must be CANDIDATES_FROZEN_BEFORE_COMPARISON")

    run_package = receipt.get("run_package")
    if not isinstance(run_package, dict):
        fail("receipt run_package missing")
    expected_rp_keys = {"merge_sha", "prompt_sha256", "package_schema"}
    if set(run_package) != expected_rp_keys:
        fail("receipt run_package key mismatch")
    if run_package["merge_sha"] != PACKAGE_MERGE:
        fail("receipt run_package.merge_sha mismatch")
    if run_package["prompt_sha256"] != PROMPT_SHA256:
        fail("receipt run_package.prompt_sha256 mismatch")
    if run_package["package_schema"] != PACKAGE_VERSION:
        fail("receipt run_package.package_schema mismatch")

    extractor = receipt.get("extractor")
    if not isinstance(extractor, dict):
        fail("receipt extractor missing")
    expected_extractor_keys = {
        "identity", "revision", "configuration_sha256", "configuration_note"
    }
    if set(extractor) != expected_extractor_keys:
        fail("receipt extractor key mismatch")
    for key in ("identity", "revision", "configuration_note"):
        if not isinstance(extractor[key], str) or not extractor[key].strip():
            fail(f"receipt extractor.{key} empty")
    if not is_hex64(extractor["configuration_sha256"]):
        fail("receipt extractor.configuration_sha256 invalid")

    source_digest_by_bundle = validate_package(package)

    passes = receipt.get("passes")
    if not isinstance(passes, list) or len(passes) != 2:
        fail("receipt must contain exactly two passes")

    by_id: dict[str, dict[str, Any]] = {}
    for run in passes:
        if not isinstance(run, dict):
            fail("pass must be object")
        expected_pass_keys = {
            "pass_id", "run_id", "context_id", "started_at", "completed_at",
            "isolation_attestation", "candidates"
        }
        if set(run) != expected_pass_keys:
            fail(f"pass key mismatch: {run.get('pass_id')!r}")
        pass_id = run.get("pass_id")
        if pass_id not in {"A", "B"} or pass_id in by_id:
            fail("passes must contain unique A and B")
        by_id[pass_id] = run

        for key in ("run_id", "context_id", "started_at", "completed_at"):
            if not isinstance(run[key], str) or not run[key].strip():
                fail(f"pass {pass_id}: {key} empty")

        att = run.get("isolation_attestation")
        expected_att_keys = {
            "fresh_context",
            "other_pass_output_visible",
            "other_bundle_output_visible",
            "basis_or_decomposition_visible",
            "procedure_modified_after_first_output",
            "attestation_scope",
        }
        if not isinstance(att, dict) or set(att) != expected_att_keys:
            fail(f"pass {pass_id}: isolation attestation malformed")
        if att["fresh_context"] is not True:
            fail(f"pass {pass_id}: fresh_context must be true")
        for key in (
            "other_pass_output_visible",
            "other_bundle_output_visible",
            "basis_or_decomposition_visible",
            "procedure_modified_after_first_output",
        ):
            if att[key] is not False:
                fail(f"pass {pass_id}: {key} must be false")
        if att["attestation_scope"] != "executor_attestation_not_independent_proof":
            fail(f"pass {pass_id}: attestation scope mismatch")

        candidates = run.get("candidates")
        if not isinstance(candidates, list) or len(candidates) != 5:
            fail(f"pass {pass_id}: expected exactly five candidates")
        bundles: set[str] = set()
        for item in candidates:
            if not isinstance(item, dict):
                fail(f"pass {pass_id}: candidate receipt must be object")
            expected_item_keys = {
                "bundle_id", "source_text_sha256", "bundle_sha256",
                "candidate_path", "candidate_sha256"
            }
            if set(item) != expected_item_keys:
                fail(f"pass {pass_id}: candidate receipt key mismatch")
            bundle = item["bundle_id"]
            if bundle not in EXPECTED_BUNDLES or bundle in bundles:
                fail(f"pass {pass_id}: invalid/duplicate bundle {bundle!r}")
            bundles.add(bundle)

            source_sha = item["source_text_sha256"]
            bundle_sha = item["bundle_sha256"]
            candidate_sha = item["candidate_sha256"]
            if source_sha != source_digest_by_bundle[bundle]:
                fail(f"pass {pass_id} {bundle}: source digest mismatch")
            if not is_hex64(bundle_sha):
                fail(f"pass {pass_id} {bundle}: bundle digest invalid")
            if not is_hex64(candidate_sha):
                fail(f"pass {pass_id} {bundle}: candidate digest invalid")
            path_value = item["candidate_path"]
            if not isinstance(path_value, str) or not path_value.strip():
                fail(f"pass {pass_id} {bundle}: candidate_path empty")

            if check_files:
                candidate_path = (receipt_path.parent / path_value).resolve()
                try:
                    candidate_path.relative_to(receipt_path.parent.resolve())
                except ValueError as exc:
                    fail(f"pass {pass_id} {bundle}: candidate path escapes receipt directory") from exc
                validate_candidate_file(candidate_path, bundle, candidate_sha)

        if bundles != EXPECTED_BUNDLES:
            fail(f"pass {pass_id}: bundle membership mismatch")

    if set(by_id) != {"A", "B"}:
        fail("receipt must contain A and B")

    a, b = by_id["A"], by_id["B"]
    if a["run_id"] == b["run_id"]:
        fail("A/B run_id must differ")
    if a["context_id"] == b["context_id"]:
        fail("A/B context_id must differ")

    def items_by_bundle(run: dict[str, Any]) -> dict[str, dict[str, Any]]:
        return {item["bundle_id"]: item for item in run["candidates"]}

    a_items = items_by_bundle(a)
    b_items = items_by_bundle(b)
    for bundle in sorted(EXPECTED_BUNDLES):
        if a_items[bundle]["source_text_sha256"] != b_items[bundle]["source_text_sha256"]:
            fail(f"{bundle}: A/B source digest differs")
        if a_items[bundle]["bundle_sha256"] != b_items[bundle]["bundle_sha256"]:
            fail(f"{bundle}: A/B bundle bytes differ")

        # Candidate equality is allowed. Independent passes may legitimately
        # converge byte-for-byte. We therefore never require different outputs.


def synthetic_candidate(bundle: str) -> dict[str, Any]:
    return {
        "schema_version": "paper2-extraction-candidate-v1",
        "bundle_id": bundle,
        "claim_core": {
            "claim_type": "relation",
            "modality": "descriptive",
            "scope": {
                "conditions": [],
                "population": [],
                "substrate": [],
                "task": [],
                "temporal_scope": [],
            },
            "nodes": [
                {
                    "id": "observed_state",
                    "role": "state_or_structure",
                    "description": "a source-grounded observed state",
                    "source_span_ids": ["s1"],
                    "grounding": "explicit",
                }
            ],
            "relations": [],
        },
    }


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def self_test(package_path: Path) -> None:
    package = load_json(package_path)
    source_mapping = validate_package(package)

    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pass_records: list[dict[str, Any]] = []
        for pass_id in ("A", "B"):
            candidate_receipts = []
            for source in package["sources"]:
                bundle = source["bundle_id"]
                candidate = synthetic_candidate(bundle)
                raw = canonical_json_bytes(candidate)
                rel = Path(pass_id) / f"{bundle}.json"
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
                candidate_receipts.append(
                    {
                        "bundle_id": bundle,
                        "source_text_sha256": source_mapping[bundle],
                        "bundle_sha256": hashlib.sha256(
                            f"same-bundle-{bundle}".encode("utf-8")
                        ).hexdigest(),
                        "candidate_path": str(rel),
                        "candidate_sha256": sha256_bytes(raw),
                    }
                )
            pass_records.append(
                {
                    "pass_id": pass_id,
                    "run_id": f"run-{pass_id}",
                    "context_id": f"context-{pass_id}",
                    "started_at": f"2026-09-23T0{1 if pass_id == 'A' else 2}:00:00Z",
                    "completed_at": f"2026-09-23T0{1 if pass_id == 'A' else 2}:01:00Z",
                    "isolation_attestation": {
                        "fresh_context": True,
                        "other_pass_output_visible": False,
                        "other_bundle_output_visible": False,
                        "basis_or_decomposition_visible": False,
                        "procedure_modified_after_first_output": False,
                        "attestation_scope": "executor_attestation_not_independent_proof",
                    },
                    "candidates": candidate_receipts,
                }
            )

        receipt = {
            "schema_version": RECEIPT_VERSION,
            "owner_issue": 147,
            "status": "CANDIDATES_FROZEN_BEFORE_COMPARISON",
            "run_package": {
                "merge_sha": PACKAGE_MERGE,
                "prompt_sha256": PROMPT_SHA256,
                "package_schema": PACKAGE_VERSION,
            },
            "extractor": {
                "identity": "synthetic-selftest",
                "revision": "1",
                "configuration_sha256": hashlib.sha256(b"synthetic-config").hexdigest(),
                "configuration_note": "synthetic deterministic self-test",
            },
            "passes": pass_records,
        }
        receipt_path = root / "receipt.json"
        receipt_path.write_bytes(canonical_json_bytes(receipt))
        validate_receipt(receipt, package, receipt_path, check_files=True)

        # N1: same context ID invalidates the pass-separation receipt.
        n1 = json.loads(json.dumps(receipt))
        n1["passes"][1]["context_id"] = n1["passes"][0]["context_id"]
        try:
            validate_receipt(n1, package, receipt_path, check_files=False)
        except ReceiptError:
            pass
        else:
            raise AssertionError("N1 same-context negative control failed")

        # N2: source bundle bytes must match across A/B.
        n2 = json.loads(json.dumps(receipt))
        n2["passes"][1]["candidates"][0]["bundle_sha256"] = "0" * 64
        try:
            validate_receipt(n2, package, receipt_path, check_files=False)
        except ReceiptError:
            pass
        else:
            raise AssertionError("N2 bundle mismatch negative control failed")

        # N3: candidate tampering must be detected by candidate digest.
        target_rel = Path(receipt["passes"][0]["candidates"][0]["candidate_path"])
        target = root / target_rel
        original = target.read_bytes()
        target.write_bytes(original + b" ")
        try:
            validate_receipt(receipt, package, receipt_path, check_files=True)
        except ReceiptError:
            pass
        else:
            raise AssertionError("N3 candidate tampering negative control failed")
        target.write_bytes(original)

        # N4: invalid candidate structure must be rejected even if its digest is updated.
        bad = load_json(target)
        bad["claim_core"]["nodes"][0]["source_span_ids"] = ["s999"]
        bad_raw = canonical_json_bytes(bad)
        target.write_bytes(bad_raw)
        n4 = json.loads(json.dumps(receipt))
        n4["passes"][0]["candidates"][0]["candidate_sha256"] = sha256_bytes(bad_raw)
        try:
            validate_receipt(n4, package, receipt_path, check_files=True)
        except ReceiptError:
            pass
        else:
            raise AssertionError("N4 invalid candidate negative control failed")

    print("PAPER2_EXTRACTION_EXECUTION_RECEIPT_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path, nargs="?")
    parser.add_argument(
        "--package",
        type=Path,
        default=Path("research/paper2/extraction_run_package_v1.json"),
    )
    parser.add_argument("--no-file-check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        if args.self_test:
            self_test(args.package)
            return 0

        if args.receipt is None:
            fail("receipt path is required outside --self-test")

        receipt = load_json(args.receipt)
        package = load_json(args.package)
        validate_receipt(
            receipt,
            package,
            args.receipt,
            check_files=not args.no_file_check,
        )
        print("PAPER2_EXTRACTION_EXECUTION_RECEIPT_V1_VALID")
        return 0
    except (
        OSError,
        json.JSONDecodeError,
        ReceiptError,
        CandidateContractError,
        AssertionError,
    ) as exc:
        print(f"PAPER2_EXTRACTION_EXECUTION_RECEIPT_V1_INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
