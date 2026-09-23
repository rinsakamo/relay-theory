#!/usr/bin/env python3
"""Assemble provenance-bearing ClaimIR A/B pairs and report agreement.

Owner: #147.

This stage is intentionally basis-blind. It validates a frozen execution
receipt, restores fixed provenance only after candidate extraction, validates
full ClaimIR v1, and compares A/B claim structure before any decomposition.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from paper2_claim_ir_compare import compare
from paper2_claim_ir_validate import ValidationError, canonical_json_bytes, validate
from paper2_extraction_receipt_validate import (
    ReceiptError,
    validate_receipt,
)

REPORT_VERSION = "paper2-extraction-agreement-report-v1"
PROVENANCE_VERSION = "paper2-extraction-provenance-v1"
RECEIPT_CONTRACT_MERGE = "85820008cde4823cc6b1cd48f95af85dd899b601"
EXPECTED_BUNDLES = {"B0001", "B0002", "B0003", "B0004", "B0005"}
SCOPE_FIELDS = ("conditions", "population", "substrate", "task", "temporal_scope")


class AssemblyError(ValueError):
    pass


def fail(message: str) -> None:
    raise AssemblyError(message)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_write(path: Path, value: Any) -> str:
    raw = canonical_json_bytes(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return sha256_bytes(raw)


def validate_provenance(
    provenance: dict[str, Any],
    package: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    if provenance.get("schema_version") != PROVENANCE_VERSION:
        fail("provenance schema_version mismatch")
    if provenance.get("owner_issue") != 147:
        fail("provenance owner_issue mismatch")
    if provenance.get("status") != "FIXED_RESTORATION_METADATA":
        fail("provenance status mismatch")
    if provenance.get("receipt_contract_merge") != RECEIPT_CONTRACT_MERGE:
        fail("provenance receipt-contract authority mismatch")

    entries = provenance.get("entries")
    if not isinstance(entries, list) or len(entries) != 5:
        fail("provenance must contain exactly five entries")

    package_sources = package.get("sources")
    if not isinstance(package_sources, list) or len(package_sources) != 5:
        fail("run package source membership malformed")
    package_by_bundle = {item["bundle_id"]: item for item in package_sources}

    out: dict[str, dict[str, Any]] = {}
    required = {
        "bundle_id",
        "paper_id",
        "source_language",
        "source_spans",
        "authors",
        "institutions",
        "venue",
        "citation_count",
        "construct_labels",
    }
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != required:
            fail("provenance entry key mismatch")
        bundle = entry["bundle_id"]
        if bundle not in EXPECTED_BUNDLES or bundle in out:
            fail(f"invalid/duplicate provenance bundle {bundle!r}")
        package_source = package_by_bundle.get(bundle)
        if not isinstance(package_source, dict):
            fail(f"{bundle}: missing run-package source")
        if entry["paper_id"] != package_source["stable_identity"]:
            fail(f"{bundle}: paper_id does not match frozen stable identity")
        if entry["source_language"] != "en":
            fail(f"{bundle}: pilot source language must be en")
        if entry["source_spans"] != [{"span_id": "s1", "locator": "Abstract"}]:
            fail(f"{bundle}: pilot provenance must restore exactly abstract span s1")
        if not isinstance(entry["authors"], list):
            fail(f"{bundle}: authors must be list")
        if not isinstance(entry["institutions"], list):
            fail(f"{bundle}: institutions must be list")
        if entry["venue"] is not None and not isinstance(entry["venue"], str):
            fail(f"{bundle}: venue malformed")
        if entry["citation_count"] is not None:
            fail(f"{bundle}: citation_count must remain null in calibration restoration")
        if not isinstance(entry["construct_labels"], list):
            fail(f"{bundle}: construct_labels must be list")
        out[bundle] = copy.deepcopy(entry)
        del out[bundle]["bundle_id"]

    if set(out) != EXPECTED_BUNDLES:
        fail("provenance bundle membership mismatch")
    return out


def receipt_passes(receipt: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["pass_id"]: item for item in receipt["passes"]}


def candidate_items(run: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["bundle_id"]: item for item in run["candidates"]}


def assemble_claim(
    *,
    bundle: str,
    pass_record: dict[str, Any],
    candidate_item: dict[str, Any],
    receipt_path: Path,
    provenance: dict[str, Any],
    extractor: dict[str, Any],
) -> dict[str, Any]:
    candidate_path = (receipt_path.parent / candidate_item["candidate_path"]).resolve()
    candidate = load_json(candidate_path)
    claim = {
        "schema_version": "paper2-claim-ir-v1",
        "claim_id": bundle,
        "provenance": copy.deepcopy(provenance),
        "extraction": {
            "extractor": extractor["identity"],
            "extractor_version": extractor["revision"],
            "procedure_version": "paper2-extraction-procedure-v1",
            "extracted_at": pass_record["completed_at"],
            "manual_review_status": "unreviewed",
        },
        "claim_core": copy.deepcopy(candidate["claim_core"]),
    }
    try:
        validate(claim)
    except ValidationError as exc:
        raise AssemblyError(f"{bundle} pass {pass_record['pass_id']}: full ClaimIR invalid after provenance restoration: {exc}") from exc
    return claim


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    comps = [row["comparison"] for row in rows]
    scope = {
        field: sum(
            1
            for comp in comps
            if comp["scope_agreement_by_field"][field]["exact"]
        )
        for field in SCOPE_FIELDS
    }
    return {
        "n": len(rows),
        "same_claim_type": sum(1 for c in comps if c["same_claim_type"]),
        "same_modality": sum(1 for c in comps if c["same_modality"]),
        "source_span_exact": sum(1 for c in comps if c["source_span_agreement"]["exact"]),
        "node_structure_exact": sum(
            1 for c in comps if c["node_structure_exact_under_id_renaming"]
        ),
        "relation_structure_exact": sum(
            1 for c in comps if c["relation_structure_exact_under_id_renaming"]
        ),
        "node_descriptions_exact": sum(
            1 for c in comps if c["node_descriptions_exact_after_normalization"]
        ),
        "relation_descriptions_exact": sum(
            1 for c in comps if c["relation_descriptions_exact_after_normalization"]
        ),
        "overall_exact_structural_equivalence": sum(
            1 for c in comps if c["overall_exact_structural_equivalence"]
        ),
        "overall_exact_full_equivalence": sum(
            1 for c in comps if c["overall_exact_full_equivalence"]
        ),
        "scope_exact_by_field": scope,
    }


def assemble_and_compare(
    receipt_path: Path,
    package_path: Path,
    provenance_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    receipt_raw = receipt_path.read_bytes()
    receipt = json.loads(receipt_raw.decode("utf-8"))
    package = load_json(package_path)
    provenance_doc = load_json(provenance_path)

    validate_receipt(
        receipt,
        package,
        receipt_path,
        check_files=True,
    )
    provenance_by_bundle = validate_provenance(provenance_doc, package)
    passes = receipt_passes(receipt)
    if set(passes) != {"A", "B"}:
        fail("validated receipt unexpectedly lacks A/B")
    a_items = candidate_items(passes["A"])
    b_items = candidate_items(passes["B"])

    rows: list[dict[str, Any]] = []
    for bundle in sorted(EXPECTED_BUNDLES):
        claim_a = assemble_claim(
            bundle=bundle,
            pass_record=passes["A"],
            candidate_item=a_items[bundle],
            receipt_path=receipt_path,
            provenance=provenance_by_bundle[bundle],
            extractor=receipt["extractor"],
        )
        claim_b = assemble_claim(
            bundle=bundle,
            pass_record=passes["B"],
            candidate_item=b_items[bundle],
            receipt_path=receipt_path,
            provenance=provenance_by_bundle[bundle],
            extractor=receipt["extractor"],
        )

        claim_a_path = output_dir / "claim_ir" / "A" / f"{bundle}.json"
        claim_b_path = output_dir / "claim_ir" / "B" / f"{bundle}.json"
        sha_a = canonical_write(claim_a_path, claim_a)
        sha_b = canonical_write(claim_b_path, claim_b)
        comp = compare(claim_a, claim_b)

        rows.append(
            {
                "bundle_id": bundle,
                "paper_id": provenance_by_bundle[bundle]["paper_id"],
                "candidate_sha256_a": a_items[bundle]["candidate_sha256"],
                "candidate_sha256_b": b_items[bundle]["candidate_sha256"],
                "claim_ir_sha256_a": sha_a,
                "claim_ir_sha256_b": sha_b,
                "comparison": comp,
            }
        )

    report = {
        "schema_version": REPORT_VERSION,
        "owner_issue": 147,
        "status": "AGREEMENT_REPORTED_BEFORE_DECOMPOSITION",
        "receipt_sha256": sha256_bytes(receipt_raw),
        "extractor": {
            "identity": receipt["extractor"]["identity"],
            "revision": receipt["extractor"]["revision"],
            "configuration_sha256": receipt["extractor"]["configuration_sha256"],
        },
        "rows": rows,
        "aggregate": aggregate(rows),
    }
    canonical_write(output_dir / "agreement-report.json", report)
    return report


def synthetic_candidate(bundle: str, *, modality: str = "descriptive", description: str = "a source-grounded observed state") -> dict[str, Any]:
    return {
        "schema_version": "paper2-extraction-candidate-v1",
        "bundle_id": bundle,
        "claim_core": {
            "claim_type": "relation",
            "modality": modality,
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
                    "description": description,
                    "source_span_ids": ["s1"],
                    "grounding": "explicit",
                }
            ],
            "relations": [],
        },
    }


def build_synthetic_receipt(root: Path, package: dict[str, Any], *, drift_bundle: str | None = None, leak_label: bool = False) -> Path:
    source_by_bundle = {
        source["bundle_id"]: source["abstract_sha256_nfkc_ws1"]
        for source in package["sources"]
    }
    pass_records: list[dict[str, Any]] = []
    for pass_id in ("A", "B"):
        candidate_receipts = []
        for source in package["sources"]:
            bundle = source["bundle_id"]
            modality = (
                "necessary"
                if drift_bundle == bundle and pass_id == "B"
                else "descriptive"
            )
            description = "a source-grounded observed state"
            if leak_label and bundle == "B0002" and pass_id == "B":
                description = "the free-energy principle is a source-grounded observed state"
            candidate = synthetic_candidate(
                bundle,
                modality=modality,
                description=description,
            )
            raw = canonical_json_bytes(candidate)
            rel = Path("candidates") / pass_id / f"{bundle}.json"
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            candidate_receipts.append(
                {
                    "bundle_id": bundle,
                    "source_text_sha256": source_by_bundle[bundle],
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
        "schema_version": "paper2-extraction-execution-receipt-v1",
        "owner_issue": 147,
        "status": "CANDIDATES_FROZEN_BEFORE_COMPARISON",
        "run_package": {
            "merge_sha": "31346f0c128876201e0407bb5cbb6102428b60e8",
            "prompt_sha256": "dfbbf50c0cfad985abb091560a1d2db6d35f5e768d574841c151afd27a2e78f6",
            "package_schema": "paper2-extraction-run-package-v1",
        },
        "extractor": {
            "identity": "synthetic-selftest",
            "revision": "1",
            "configuration_sha256": hashlib.sha256(b"synthetic-config").hexdigest(),
            "configuration_note": "synthetic deterministic assembler self-test",
        },
        "passes": pass_records,
    }
    path = root / "receipt.json"
    path.write_bytes(canonical_json_bytes(receipt))
    return path


def self_test(package_path: Path, provenance_path: Path) -> None:
    import tempfile

    package = load_json(package_path)
    provenance = load_json(provenance_path)
    validate_provenance(provenance, package)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        exact_root = root / "exact"
        exact_root.mkdir()
        exact_receipt = build_synthetic_receipt(exact_root, package)
        exact_report = assemble_and_compare(
            exact_receipt,
            package_path,
            provenance_path,
            exact_root / "out",
        )
        if exact_report["aggregate"]["overall_exact_structural_equivalence"] != 5:
            raise AssertionError("exact-control structural count must be 5/5")
        if exact_report["aggregate"]["overall_exact_full_equivalence"] != 5:
            raise AssertionError("exact-control full count must be 5/5")

        drift_root = root / "drift"
        drift_root.mkdir()
        drift_receipt = build_synthetic_receipt(
            drift_root,
            package,
            drift_bundle="B0003",
        )
        drift_report = assemble_and_compare(
            drift_receipt,
            package_path,
            provenance_path,
            drift_root / "out",
        )
        if drift_report["aggregate"]["same_modality"] != 4:
            raise AssertionError("modality drift must produce 4/5 agreement")
        if drift_report["aggregate"]["overall_exact_structural_equivalence"] != 4:
            raise AssertionError("one structural drift must produce 4/5 exact structural agreement")

        leak_root = root / "leak"
        leak_root.mkdir()
        leak_receipt = build_synthetic_receipt(
            leak_root,
            package,
            leak_label=True,
        )
        try:
            assemble_and_compare(
                leak_receipt,
                package_path,
                provenance_path,
                leak_root / "out",
            )
        except AssemblyError:
            pass
        else:
            raise AssertionError("construct-label leakage must fail after provenance restoration")

    print("PAPER2_EXTRACTION_ASSEMBLE_COMPARE_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path, nargs="?")
    parser.add_argument(
        "--package",
        type=Path,
        default=Path("research/paper2/extraction_run_package_v1.json"),
    )
    parser.add_argument(
        "--provenance",
        type=Path,
        default=Path("research/paper2/extraction_provenance_v1.json"),
    )
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        if args.self_test:
            self_test(args.package, args.provenance)
            return 0

        if args.receipt is None or args.output_dir is None:
            fail("receipt and --output-dir are required outside --self-test")

        report = assemble_and_compare(
            args.receipt,
            args.package,
            args.provenance,
            args.output_dir,
        )
        print(
            json.dumps(
                {
                    "status": "PAPER2_EXTRACTION_AGREEMENT_REPORTED",
                    "n": report["aggregate"]["n"],
                    "overall_exact_structural_equivalence": report["aggregate"]["overall_exact_structural_equivalence"],
                    "report": str(args.output_dir / "agreement-report.json"),
                },
                sort_keys=True,
            )
        )
        return 0
    except (
        OSError,
        json.JSONDecodeError,
        ValidationError,
        ReceiptError,
        AssemblyError,
        AssertionError,
    ) as exc:
        print(f"PAPER2_EXTRACTION_ASSEMBLE_COMPARE_INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
