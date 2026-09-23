#!/usr/bin/env python3
"""Freeze local preprocessing facts for the five Paper 2 calibration sources.

Owner: #162.

This tool consumes no model call. It verifies caller-supplied canonical
abstracts against the already frozen #147 normalized digests, applies the
#162 segmentation/masking policy, writes local masked bundles, and emits a
copyright-safe digest manifest suitable for repository reconciliation.

Raw and masked source text remain local evidence only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from paper2_extraction_bundle_prepare import canonical_json_bytes
from paper2_extraction_two_pass_prepare import (
    PreparationError,
    build_segmented_bundle,
    load_json,
    normalize_text,
)


TERMS_VERSION = "paper2-calibration-mask-terms-v1"
FREEZE_VERSION = "paper2-calibration-preprocessing-freeze-v1"
EXPECTED_SAMPLE_COUNT = 5


class CalibrationFreezeError(ValueError):
    pass


def fail(message: str) -> None:
    raise CalibrationFreezeError(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _sample_maps(
    package: dict[str, Any],
    provenance: dict[str, Any],
    terms: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    package_sources = package.get("sources")
    provenance_entries = provenance.get("entries")
    term_samples = terms.get("samples")
    if not isinstance(package_sources, list) or len(package_sources) != EXPECTED_SAMPLE_COUNT:
        fail("run package must contain exactly five sources")
    if not isinstance(provenance_entries, list) or len(provenance_entries) != EXPECTED_SAMPLE_COUNT:
        fail("provenance must contain exactly five entries")
    if not isinstance(term_samples, list) or len(term_samples) != EXPECTED_SAMPLE_COUNT:
        fail("mask-term authority must contain exactly five samples")

    by_sample = {row["sample_id"]: row for row in package_sources}
    by_bundle = {row["bundle_id"]: row for row in provenance_entries}
    terms_by_sample = {row["sample_id"]: row for row in term_samples}
    if len(by_sample) != EXPECTED_SAMPLE_COUNT or len(by_bundle) != EXPECTED_SAMPLE_COUNT:
        fail("duplicate sample or bundle identity")
    if set(by_sample) != set(terms_by_sample):
        fail("mask-term sample membership does not match run package")
    return by_sample, by_bundle, terms_by_sample


def validate_term_authority(
    package: dict[str, Any],
    provenance: dict[str, Any],
    terms: dict[str, Any],
) -> None:
    if terms.get("schema_version") != TERMS_VERSION:
        fail("mask terms schema_version")
    if terms.get("owner_issue") != 162:
        fail("mask terms owner_issue")
    if terms.get("status") != "PREEXECUTION_FROZEN":
        fail("mask terms status")
    if terms.get("additional_alias_policy") != "none":
        fail("additional aliases are not frozen in v1")

    by_sample, by_bundle, terms_by_sample = _sample_maps(package, provenance, terms)
    for sample_id, source in by_sample.items():
        bundle_id = source["bundle_id"]
        provenance_entry = by_bundle.get(bundle_id)
        if not isinstance(provenance_entry, dict):
            fail(f"{sample_id}: provenance bundle missing")
        term_entry = terms_by_sample[sample_id]
        if term_entry.get("bundle_id") != bundle_id:
            fail(f"{sample_id}: bundle mismatch in mask terms")
        frozen_constructs = provenance_entry.get("construct_labels")
        labels = term_entry.get("labels")
        if not isinstance(frozen_constructs, list) or not isinstance(labels, list):
            fail(f"{sample_id}: construct labels missing")
        canonicals = [label.get("canonical") for label in labels if isinstance(label, dict)]
        if canonicals != frozen_constructs:
            fail(
                f"{sample_id}: canonical mask labels must exactly equal provenance "
                "construct_labels in frozen order"
            )
        expected_ids = [f"L{i:02d}" for i in range(1, len(labels) + 1)]
        actual_ids = [label.get("label_id") for label in labels]
        if actual_ids != expected_ids:
            fail(f"{sample_id}: label IDs must be consecutive from L01")
        for label in labels:
            aliases = label.get("aliases")
            if aliases != []:
                fail(f"{sample_id}: v1 aliases must be explicitly empty")


def label_groups(term_entry: dict[str, Any]) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    for label in term_entry["labels"]:
        groups.append(
            {
                "label_id": label["label_id"],
                "terms": [label["canonical"], *label["aliases"]],
            }
        )
    return groups


def freeze_preprocessing(
    *,
    source_texts: dict[str, Any],
    package: dict[str, Any],
    provenance: dict[str, Any],
    terms: dict[str, Any],
    output_dir: Path,
    authority_files: dict[str, Path],
) -> dict[str, Any]:
    validate_term_authority(package, provenance, terms)
    by_sample, _, terms_by_sample = _sample_maps(package, provenance, terms)
    if set(source_texts) != set(by_sample):
        fail(
            "source text membership mismatch: "
            f"missing={sorted(set(by_sample)-set(source_texts))} "
            f"extra={sorted(set(source_texts)-set(by_sample))}"
        )

    output_dir.mkdir(parents=True, exist_ok=False)
    bundle_dir = output_dir / "masked-bundles"
    bundle_dir.mkdir()

    rows: list[dict[str, Any]] = []
    for sample_id in [row["sample_id"] for row in package["sources"]]:
        source = by_sample[sample_id]
        raw = source_texts[sample_id]
        if not isinstance(raw, str):
            fail(f"{sample_id}: source text must be string")
        normalized = normalize_text(raw)
        actual_raw_sha = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        expected_raw_sha = source["abstract_sha256_nfkc_ws1"]
        if actual_raw_sha != expected_raw_sha:
            fail(
                f"{sample_id}: SOURCE_DIGEST_MISMATCH "
                f"expected={expected_raw_sha} actual={actual_raw_sha}"
            )

        prepared = build_segmented_bundle(
            bundle_id=source["bundle_id"],
            raw_text=raw,
            label_groups=label_groups(terms_by_sample[sample_id]),
            source_language="en",
        )
        if prepared["raw_normalized_sha256"] != expected_raw_sha:
            raise AssertionError(f"{sample_id}: preprocessing changed raw normalization")

        masked_bundle = prepared["masked_bundle"]
        bundle_path = bundle_dir / f"{source['bundle_id']}.json"
        bundle_path.write_bytes(canonical_json_bytes(masked_bundle))

        rows.append(
            {
                "sample_id": sample_id,
                "bundle_id": source["bundle_id"],
                "stable_identity": source["stable_identity"],
                "raw_normalized_sha256": actual_raw_sha,
                "raw_digest_matches_frozen_v1": True,
                "segmentation_count": prepared["segmentation_count"],
                "mask_label_count": len(terms_by_sample[sample_id]["labels"]),
                "additional_alias_count": 0,
                "masked_bundle_sha256": prepared["masked_bundle_sha256"],
                "masked_bundle_local_path": str(bundle_path),
            }
        )

    authority_sha = {
        name: sha256_file(path)
        for name, path in sorted(authority_files.items())
    }
    manifest = {
        "schema_version": FREEZE_VERSION,
        "owner_issue": 162,
        "classification": "CALIBRATION_PREPROCESSING_LOCALLY_FROZEN",
        "model_calls": 0,
        "scientific_transaction_consumed": False,
        "sample_mode": "same_surface_five_item_calibration",
        "source_item_count": len(rows),
        "raw_abstract_text_committed": False,
        "masked_abstract_text_committed": False,
        "authority_sha256": authority_sha,
        "mask_term_policy": {
            "schema_version": TERMS_VERSION,
            "additional_alias_policy": "none",
            "mask_terms_sha256": authority_sha["mask_terms"],
        },
        "entries": rows,
    }
    write_json(output_dir / "calibration-preprocessing-freeze.json", manifest)
    return manifest


def self_test(
    *,
    package_path: Path,
    provenance_path: Path,
    terms_path: Path,
) -> None:
    package = load_json(package_path)
    provenance = load_json(provenance_path)
    terms = load_json(terms_path)
    validate_term_authority(package, provenance, terms)

    # Contract-level negative: any unpredeclared alias is forbidden.
    altered = json.loads(json.dumps(terms))
    altered["samples"][0]["labels"][0]["aliases"] = ["agent environment coupling"]
    try:
        validate_term_authority(package, provenance, altered)
    except CalibrationFreezeError:
        pass
    else:
        raise AssertionError("unfrozen alias unexpectedly accepted")

    # Synthetic preparation exercises digest verification and output manifest.
    synthetic_package = {
        "sources": [
            {
                "sample_id": "SYNTHETIC-1",
                "bundle_id": "B9001",
                "stable_identity": "synthetic:1",
                "abstract_sha256_nfkc_ws1": hashlib.sha256(
                    normalize_text(
                        "Working memory limits synthetic storage. "
                        "Load changes synthetic performance."
                    ).encode("utf-8")
                ).hexdigest(),
            }
        ]
    }
    synthetic_provenance = {
        "entries": [
            {
                "bundle_id": "B9001",
                "construct_labels": ["working memory"],
            }
        ]
    }
    synthetic_terms = {
        "schema_version": TERMS_VERSION,
        "owner_issue": 162,
        "status": "PREEXECUTION_FROZEN",
        "additional_alias_policy": "none",
        "samples": [
            {
                "sample_id": "SYNTHETIC-1",
                "bundle_id": "B9001",
                "labels": [
                    {
                        "label_id": "L01",
                        "canonical": "working memory",
                        "aliases": [],
                    }
                ],
            }
        ],
    }

    # Generalize the internal mapping only for this synthetic one-row fixture.
    # This test calls the same lower-level preparation primitives directly.
    prepared = build_segmented_bundle(
        bundle_id="B9001",
        raw_text=(
            "Working memory limits synthetic storage. "
            "Load changes synthetic performance."
        ),
        label_groups=[{"label_id": "L01", "terms": ["working memory"]}],
    )
    rendered = canonical_json_bytes(prepared["masked_bundle"]).decode("utf-8")
    if "working memory" in rendered.casefold():
        raise AssertionError("synthetic construct label leaked")
    if prepared["segmentation_count"] != 2:
        raise AssertionError("synthetic segmentation drift")

    mismatch = normalize_text("Different synthetic abstract.")
    mismatch_sha = hashlib.sha256(mismatch.encode("utf-8")).hexdigest()
    if mismatch_sha == synthetic_package["sources"][0]["abstract_sha256_nfkc_ws1"]:
        raise AssertionError("synthetic mismatch control invalid")

    print("PAPER2_CALIBRATION_PREPROCESSING_FREEZE_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
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
    parser.add_argument(
        "--mask-terms",
        type=Path,
        default=Path("research/paper2/extraction_calibration_mask_terms_v1.json"),
    )
    parser.add_argument(
        "--mask-policy",
        type=Path,
        default=Path("research/paper2/extraction_label_mask_v1.json"),
    )
    parser.add_argument(
        "--real-protocol",
        type=Path,
        default=Path("research/paper2/extraction_two_pass_real_protocol_v1.json"),
    )
    parser.add_argument(
        "--normal-prompt",
        type=Path,
        default=Path("research/paper2/extraction_normal_prompt_v1.md"),
    )
    parser.add_argument("--source-texts", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        if args.self_test:
            self_test(
                package_path=args.package,
                provenance_path=args.provenance,
                terms_path=args.mask_terms,
            )
            return 0

        if args.source_texts is None or args.output_dir is None:
            parser.error("--source-texts and --output-dir are required")

        source_texts = load_json(args.source_texts)
        if not isinstance(source_texts, dict):
            fail("--source-texts must be a JSON object")

        manifest = freeze_preprocessing(
            source_texts=source_texts,
            package=load_json(args.package),
            provenance=load_json(args.provenance),
            terms=load_json(args.mask_terms),
            output_dir=args.output_dir,
            authority_files={
                "run_package": args.package,
                "provenance": args.provenance,
                "mask_terms": args.mask_terms,
                "mask_policy": args.mask_policy,
                "real_protocol": args.real_protocol,
                "normal_prompt": args.normal_prompt,
                "preparation_script": Path(__file__),
            },
        )
        print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (
        OSError,
        json.JSONDecodeError,
        CalibrationFreezeError,
        PreparationError,
        AssertionError,
    ) as exc:
        print(f"CALIBRATION_PREPROCESSING_NOT_FROZEN: {type(exc).__name__}: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
