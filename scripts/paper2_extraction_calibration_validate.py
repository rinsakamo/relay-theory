#!/usr/bin/env python3
"""Validate the frozen Paper 2 extraction-calibration manifest.

Owner: #147. This validates freeze semantics only; it does not perform
scientific extraction or establish extraction faithfulness.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "paper2-extraction-calibration-v1"
EXPECTED_SAMPLES = {
    "CAL-BEER-1995",
    "CAL-FRISTON-2010",
    "CAL-TISHBY-2000",
    "CAL-KOLCHINSKY-WOLPERT-2018",
    "CAL-COWAN-2001",
}
FORBIDDEN_RESULT_KEYS = {
    "claim_ir",
    "claim_ir_a",
    "claim_ir_b",
    "extraction_result",
    "comparison_result",
    "agreement",
    "decomposition_result",
    "basis_mapping",
    "residual",
    "coverage",
}


class CalibrationManifestError(ValueError):
    pass


def fail(message: str) -> None:
    raise CalibrationManifestError(message)


def walk_keys(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in FORBIDDEN_RESULT_KEYS:
                fail(f"{path}: result-bearing key forbidden before extraction: {key}")
            walk_keys(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            walk_keys(item, f"{path}[{index}]")


def nonempty_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{path}: expected non-empty string")
    return value


def validate(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        fail("root: expected object")

    if data.get("schema_version") != SCHEMA_VERSION:
        fail("schema_version: unexpected value")
    if data.get("owner_issue") != 147:
        fail("owner_issue: expected 147")
    if data.get("status") != "FROZEN_BEFORE_EXTRACTION":
        fail("status: must remain FROZEN_BEFORE_EXTRACTION")
    if data.get("claim_ir_schema") != "paper2-claim-ir-v1":
        fail("claim_ir_schema: unexpected value")
    if data.get("comparison_schema") != "paper2-claim-ir-compare-v1":
        fail("comparison_schema: unexpected value")
    if data.get("source_surface") != "canonical_primary_source_abstract_only":
        fail("source_surface: pilot must remain abstract-only")
    if data.get("independent_extraction_passes") != 2:
        fail("independent_extraction_passes: expected exactly 2")

    for key in (
        "basis_access_during_extraction",
        "basis_access_during_adjudication",
        "decomposition_outcome_access_during_extraction",
    ):
        if data.get(key) is not False:
            fail(f"{key}: must be false")

    samples = data.get("samples")
    if not isinstance(samples, list):
        fail("samples: expected array")
    if len(samples) != len(EXPECTED_SAMPLES):
        fail(f"samples: expected {len(EXPECTED_SAMPLES)} frozen rows")

    sample_ids: set[str] = set()
    seed_ids: set[int] = set()
    registry_ids: set[int] = set()
    strata: set[str] = set()

    for index, sample in enumerate(samples):
        path = f"samples[{index}]"
        if not isinstance(sample, dict):
            fail(f"{path}: expected object")
        required = {
            "sample_id",
            "top50_seed",
            "claim_form_stratum",
            "title",
            "stable_identity",
            "canonical_url",
            "source_locator",
            "registry_comment_id",
            "registry_usage_comment_id",
            "accessed_on",
            "source_anchor_start",
            "source_anchor_end",
        }
        if set(sample) != required:
            fail(
                f"{path}: key mismatch missing={sorted(required-set(sample))} "
                f"extra={sorted(set(sample)-required)}"
            )

        sample_id = nonempty_string(sample["sample_id"], f"{path}.sample_id")
        if sample_id in sample_ids:
            fail(f"{path}.sample_id: duplicate")
        sample_ids.add(sample_id)

        seed = sample["top50_seed"]
        if not isinstance(seed, int) or isinstance(seed, bool) or seed <= 0:
            fail(f"{path}.top50_seed: expected positive integer")
        if seed in seed_ids:
            fail(f"{path}.top50_seed: duplicate")
        seed_ids.add(seed)

        stratum = nonempty_string(
            sample["claim_form_stratum"], f"{path}.claim_form_stratum"
        )
        if stratum in strata:
            fail(f"{path}.claim_form_stratum: duplicate in pilot")
        strata.add(stratum)

        for key in (
            "title",
            "stable_identity",
            "canonical_url",
            "source_locator",
            "accessed_on",
            "source_anchor_start",
            "source_anchor_end",
        ):
            nonempty_string(sample[key], f"{path}.{key}")

        if sample["source_locator"] != "Abstract":
            fail(f"{path}.source_locator: expected Abstract")
        if sample["accessed_on"] != "2026-09-23":
            fail(f"{path}.accessed_on: unexpected date")
        if not sample["canonical_url"].startswith("https://"):
            fail(f"{path}.canonical_url: expected https URL")

        registry_id = sample["registry_comment_id"]
        if not isinstance(registry_id, int) or isinstance(registry_id, bool):
            fail(f"{path}.registry_comment_id: expected integer")
        if registry_id in registry_ids:
            fail(f"{path}.registry_comment_id: duplicate")
        registry_ids.add(registry_id)

        usage_id = sample["registry_usage_comment_id"]
        if usage_id != 5786792748:
            fail(f"{path}.registry_usage_comment_id: unexpected value")

    if sample_ids != EXPECTED_SAMPLES:
        fail(
            "samples: frozen membership mismatch "
            f"missing={sorted(EXPECTED_SAMPLES-sample_ids)} "
            f"extra={sorted(sample_ids-EXPECTED_SAMPLES)}"
        )

    forbidden = data.get("forbidden_until_extraction_complete")
    if not isinstance(forbidden, list) or len(forbidden) < 5:
        fail("forbidden_until_extraction_complete: incomplete")

    selection_basis = data.get("selection_basis")
    if not isinstance(selection_basis, list) or len(selection_basis) < 4:
        fail("selection_basis: incomplete")

    nonempty_string(data.get("frozen_against_main"), "frozen_against_main")
    walk_keys(data)
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("research/paper2/extraction_calibration_v1.json"),
    )
    args = parser.parse_args()

    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        validate(data)
        print("PAPER2_EXTRACTION_CALIBRATION_V1_FROZEN")
        return 0
    except (OSError, json.JSONDecodeError, CalibrationManifestError) as exc:
        print(f"PAPER2_EXTRACTION_CALIBRATION_INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
