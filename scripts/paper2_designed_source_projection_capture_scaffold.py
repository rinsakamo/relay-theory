#!/usr/bin/env python3
"""Generate local-only #239 projection/capture templates for all 60 bundles.

The scaffold contains no source text and no per-source mask authority.  It
prefills only frozen source identity / public-web locator fields.  The operator
must acquire the complete public source locally, hash it, verify/copy the
source-native complete abstract into the #250 input shape, and rename the
template before the composed zero-model transaction can run.
"""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from pathlib import Path
from typing import Any

from paper2_bounded_source_projection import descriptor_map
from paper2_extraction_bundle_prepare import canonical_json_bytes

VERSION = "paper2-designed-source-projection-capture-scaffold-v1"


class ScaffoldError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ScaffoldError(message)


def template(descriptor: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "paper2-bounded-source-projection-input-v1",
        "bundle_id": descriptor["opaque_bundle_id"],
        "stable_identity": copy.deepcopy(descriptor["stable_identity"]),
        "public_fulltext_locator": descriptor["public_fulltext_locator"],
        "retrieved_at": "__FILL_RETRIEVED_AT__",
        "source_language": "en",
        "fulltext_sha256": "__FILL_FULLTEXT_SHA256__",
        "abstract_state": "__FILL_PRESENT_OR_ABSENT__",
        "abstract_locator": "__FILL_SOURCE_NATIVE_ABSTRACT_LOCATOR_OR_NULL__",
        "abstract_text": "__FILL_COMPLETE_SOURCE_NATIVE_ABSTRACT_OR_NULL__",
        "abstract_boundary_attestation": "__FILL_SOURCE_NATIVE_ABSTRACT_ATTESTATION__",
    }


def generate(output_root: Path) -> dict[str, Any]:
    if output_root.exists():
        fail(f"OUTPUT_DIRECTORY_ALREADY_EXISTS:{output_root}")
    descriptors = descriptor_map()
    if set(descriptors) != {f"B{i:04d}" for i in range(1, 61)}:
        fail("FROZEN_OPAQUE_BUNDLE_SET_DRIFT")
    output_root.mkdir(parents=True, exist_ok=False)
    for bundle in sorted(descriptors):
        d = output_root / bundle
        d.mkdir()
        (d / "projection-input.template.json").write_bytes(
            canonical_json_bytes(template(descriptors[bundle]))
        )
    guide = {
        "schema_version": VERSION,
        "owner_issue": 239,
        "bundle_count": 60,
        "source_files_committed_to_repository": False,
        "mask_terms_entered_by_operator": False,
        "instructions": [
            "For each B####, acquire the complete public-web source through the frozen public_fulltext_locator and save the exact acquired bytes locally as fulltext.bin.",
            "Set fulltext_sha256 to SHA-256(fulltext.bin) and retrieved_at to the acquisition time.",
            "Verify whether the source has a source-native complete abstract. Do not choose a body excerpt, claim window, summary, or paraphrase.",
            "If present, copy the complete source-native abstract exactly into abstract_text, record its source locator, and use SOURCE_NATIVE_COMPLETE_ABSTRACT_VERIFIED.",
            "If absent, set abstract_state=ABSENT, abstract_locator=null, abstract_text=null, and NO_SOURCE_NATIVE_ABSTRACT_VERIFIED.",
            "Replace every sentinel, rename projection-input.template.json to projection-input.json, and leave no template file in an executable bundle directory.",
            "Do not add raw_text or label_groups. The composed transaction derives the fixed global mask vocabulary from frozen #253 authority.",
            "Do not commit fulltext.bin, projection inputs containing source text, bounded surfaces, or masked source surfaces to the repository."
        ],
        "execution": (
            "python scripts/paper2_designed_source_projection_capture.py "
            "--input-root <LOCAL_FINALIZED_ROOT> --output-root <NEW_NONEXISTENT_LOCAL_EVIDENCE_ROOT>"
        ),
        "model_calls": 0,
    }
    (output_root / "SCAFFOLD.json").write_bytes(canonical_json_bytes(guide))
    return guide


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="relaytheory-239-scaffold-") as td:
        root = Path(td) / "scaffold"
        guide = generate(root)
        dirs = sorted(p for p in root.iterdir() if p.is_dir())
        if len(dirs) != 60:
            raise AssertionError("scaffold bundle count drift")
        first = json.loads((dirs[0] / "projection-input.template.json").read_text(encoding="utf-8"))
        expected = {
            "schema_version", "bundle_id", "stable_identity",
            "public_fulltext_locator", "retrieved_at", "source_language",
            "fulltext_sha256", "abstract_state", "abstract_locator",
            "abstract_text", "abstract_boundary_attestation",
        }
        if set(first) != expected:
            raise AssertionError("scaffold field surface drift")
        if "raw_text" in first or "label_groups" in first:
            raise AssertionError("forbidden operator degree of freedom leaked into scaffold")
        if (dirs[0] / "fulltext.bin").exists():
            raise AssertionError("scaffold manufactured source bytes")
        if guide["model_calls"] != 0:
            raise AssertionError("scaffold performed model calls")
        try:
            generate(root)
        except ScaffoldError:
            pass
        else:
            raise AssertionError("scaffold overwrote existing root")
    print("PAPER2_DESIGNED_SOURCE_PROJECTION_CAPTURE_SCAFFOLD_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            return 0
        if args.output_root is None:
            fail("--output-root is required outside --self-test")
        guide = generate(args.output_root)
        print(json.dumps(guide, sort_keys=True))
        return 0
    except (ScaffoldError, OSError, json.JSONDecodeError, AssertionError) as exc:
        print(f"PAPER2_DESIGNED_SOURCE_PROJECTION_CAPTURE_SCAFFOLD_V1_INVALID: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
