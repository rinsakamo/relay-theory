#!/usr/bin/env python3
"""Prepare authority-blind Paper 2 extraction source bundles from local abstracts.

Owner: #147.

Raw primary-source abstracts are intentionally not committed to the repository.
This tool verifies caller-supplied source text against the frozen normalized
SHA-256 values and emits only opaque B#### bundles for extractor consumption.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any


PACKAGE_VERSION = "paper2-extraction-run-package-v1"
SOURCE_VERSION = "paper2-extraction-source-bundle-v1"
PROMPT_SHA256 = "dfbbf50c0cfad985abb091560a1d2db6d35f5e768d574841c151afd27a2e78f6"


class PackageError(ValueError):
    pass


def fail(message: str) -> None:
    raise PackageError(message)


def normalize_text(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        fail("source text must be a non-empty string")
    return " ".join(unicodedata.normalize("NFKC", text).split())


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_package(package: dict[str, Any], prompt_bytes: bytes) -> None:
    if package.get("schema_version") != PACKAGE_VERSION:
        fail("unexpected package schema_version")
    if package.get("owner_issue") != 147:
        fail("unexpected owner_issue")
    if package.get("status") != "READY_FOR_INDEPENDENT_EXECUTION_NOT_EXECUTED":
        fail("run package must remain pre-execution")

    authority = package.get("authority")
    if not isinstance(authority, dict):
        fail("authority missing")
    expected_prompt = authority.get("prompt_sha256_utf8")
    actual_prompt = hashlib.sha256(prompt_bytes).hexdigest()
    if expected_prompt != PROMPT_SHA256 or actual_prompt != PROMPT_SHA256:
        fail(
            "prompt digest mismatch: "
            f"manifest={expected_prompt} file={actual_prompt}"
        )

    execution = package.get("execution")
    if not isinstance(execution, dict):
        fail("execution contract missing")
    for key in (
        "same_bundle_bytes_required_across_passes",
        "same_prompt_bytes_required_across_passes",
        "same_extractor_identity_and_configuration_required_across_passes",
        "fresh_context_per_bundle_per_pass",
        "cross_pass_visibility_forbidden",
        "cross_bundle_visibility_forbidden",
        "basis_and_decomposition_visibility_forbidden",
        "record_extractor_identity_after_candidate_freeze",
        "decomposition_blocked_until_comparison_report_frozen",
    ):
        if execution.get(key) is not True:
            fail(f"execution.{key} must be true")
    if execution.get("passes") != ["A", "B"]:
        fail("execution.passes must be exactly A/B")

    raw_policy = package.get("raw_text_policy")
    if not isinstance(raw_policy, dict):
        fail("raw_text_policy missing")
    if raw_policy.get("raw_abstracts_committed_to_repository") is not False:
        fail("raw abstracts must not be committed")

    sources = package.get("sources")
    if not isinstance(sources, list) or len(sources) != 5:
        fail("expected exactly five frozen sources")

    bundle_ids: set[str] = set()
    sample_ids: set[str] = set()
    for i, source in enumerate(sources):
        if not isinstance(source, dict):
            fail(f"sources[{i}] must be object")
        for key in (
            "bundle_id",
            "sample_id",
            "stable_identity",
            "canonical_url",
            "source_locator",
            "registry_comment_id",
            "abstract_sha256_nfkc_ws1",
        ):
            if key not in source:
                fail(f"sources[{i}] missing {key}")
        bundle_id = source["bundle_id"]
        sample_id = source["sample_id"]
        if bundle_id in bundle_ids or sample_id in sample_ids:
            fail("duplicate bundle_id or sample_id")
        bundle_ids.add(bundle_id)
        sample_ids.add(sample_id)
        if not (
            isinstance(bundle_id, str)
            and len(bundle_id) == 5
            and bundle_id.startswith("B")
            and bundle_id[1:].isdigit()
        ):
            fail(f"invalid bundle_id {bundle_id!r}")
        digest = source["abstract_sha256_nfkc_ws1"]
        if not (
            isinstance(digest, str)
            and len(digest) == 64
            and all(c in "0123456789abcdef" for c in digest)
        ):
            fail(f"invalid abstract digest for {bundle_id}")


def prepare(
    package: dict[str, Any],
    source_texts: dict[str, Any],
    output_dir: Path,
) -> list[dict[str, str]]:
    if set(source_texts) != {source["sample_id"] for source in package["sources"]}:
        expected = {source["sample_id"] for source in package["sources"]}
        actual = set(source_texts)
        fail(
            "source-text membership mismatch: "
            f"missing={sorted(expected-actual)} extra={sorted(actual-expected)}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, str]] = []

    for source in package["sources"]:
        sample_id = source["sample_id"]
        bundle_id = source["bundle_id"]
        normalized = normalize_text(source_texts[sample_id])
        actual_digest = sha256_text(normalized)
        expected_digest = source["abstract_sha256_nfkc_ws1"]
        if actual_digest != expected_digest:
            fail(
                f"{sample_id}: abstract digest mismatch "
                f"expected={expected_digest} actual={actual_digest}"
            )

        bundle = {
            "schema_version": SOURCE_VERSION,
            "bundle_id": bundle_id,
            "source_language": "en",
            "source_spans": [
                {
                    "span_id": "s1",
                    "text": normalized,
                }
            ],
        }
        encoded = canonical_json_bytes(bundle)
        path = output_dir / f"{bundle_id}.json"
        path.write_bytes(encoded)
        manifest.append(
            {
                "bundle_id": bundle_id,
                "source_text_sha256": actual_digest,
                "bundle_sha256": hashlib.sha256(encoded).hexdigest(),
            }
        )

    manifest_bytes = canonical_json_bytes(
        {
            "schema_version": "paper2-extraction-bundle-digests-v1",
            "bundles": manifest,
        }
    )
    (output_dir / "bundle-digests.json").write_bytes(manifest_bytes)
    return manifest


def self_test(package_path: Path, prompt_path: Path) -> None:
    package = load_json(package_path)
    prompt_bytes = prompt_path.read_bytes()
    validate_package(package, prompt_bytes)

    # Synthetic package keeps the exact execution contract but replaces
    # scientific source identities/digests so the generator can be tested
    # without committing copyrighted primary-source abstracts.
    synthetic = json.loads(json.dumps(package))
    texts: dict[str, str] = {}
    for index, source in enumerate(synthetic["sources"], start=1):
        value = f"Synthetic abstract fixture number {index}."
        texts[source["sample_id"]] = value
        source["abstract_sha256_nfkc_ws1"] = sha256_text(normalize_text(value))

    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "bundles"
        built = prepare(synthetic, texts, out)
        if len(built) != 5:
            raise AssertionError("expected five generated bundles")
        if not (out / "bundle-digests.json").is_file():
            raise AssertionError("bundle digest manifest missing")

        bad = dict(texts)
        first = synthetic["sources"][0]["sample_id"]
        bad[first] = bad[first] + " changed"
        try:
            prepare(synthetic, bad, Path(tmp) / "bad")
        except PackageError:
            pass
        else:
            raise AssertionError("digest mismatch negative control failed")

    print("PAPER2_EXTRACTION_RUN_PACKAGE_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--package",
        type=Path,
        default=Path("research/paper2/extraction_run_package_v1.json"),
    )
    parser.add_argument(
        "--prompt",
        type=Path,
        default=Path("research/paper2/extraction_prompt_v1.md"),
    )
    parser.add_argument("--source-texts", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        package = load_json(args.package)
        prompt_bytes = args.prompt.read_bytes()
        validate_package(package, prompt_bytes)

        if args.self_test:
            self_test(args.package, args.prompt)
            return 0

        if args.source_texts is None or args.output_dir is None:
            fail("--source-texts and --output-dir are required outside --self-test")

        raw = load_json(args.source_texts)
        if not isinstance(raw, dict):
            fail("--source-texts must be a JSON object mapping sample_id to text")
        built = prepare(package, raw, args.output_dir)
        print(
            json.dumps(
                {
                    "status": "PAPER2_EXTRACTION_BUNDLES_PREPARED",
                    "count": len(built),
                    "output_dir": str(args.output_dir),
                },
                sort_keys=True,
            )
        )
        return 0
    except (OSError, json.JSONDecodeError, PackageError, AssertionError) as exc:
        print(f"PAPER2_EXTRACTION_RUN_PACKAGE_INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
