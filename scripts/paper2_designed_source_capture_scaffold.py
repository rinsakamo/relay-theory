#!/usr/bin/env python3
"""Generate local-only Paper 2 #239 source-capture input templates.

The templates deliberately do NOT satisfy the executable capture-input contract.
They use sentinel values and .template.json filenames so they cannot be consumed
accidentally by the assembler's B####.json input glob.

No source text is fetched and no model call is performed.
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any

from paper2_extraction_bundle_prepare import canonical_json_bytes

CAPTURE_DESCRIPTOR_PATH = Path("research/paper2/designed_source_capture_manifest_v1.json")
SCAFFOLD_VERSION = "paper2-designed-source-capture-scaffold-v1"


class ScaffoldError(ValueError):
    pass


def fail(message: str) -> None:
    raise ScaffoldError(message)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_template(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "_scaffold_version": SCAFFOLD_VERSION,
        "_instructions": (
            "Local-only template. Replace all __FILL_* sentinels, add at least "
            "one source-facing construct-label group, then save as B####.json. "
            "Do not commit raw source text or label terms to the repository."
        ),
        "schema_version": "paper2-designed-source-capture-input-v1",
        "bundle_id": record["opaque_bundle_id"],
        "stable_identity": record["stable_identity"],
        "capture_state": "__FILL_CAPTURE_READY_OR_TERMINAL_INACCESSIBLE__",
        "source_version": "__FILL_SOURCE_VERSION__",
        "retrieval_date": "__FILL_YYYY-MM-DD__",
        "source_language": "en",
        "capture_access_class": "__FILL_FULL_TEXT_OR_INACCESSIBLE__",
        "source_locator": record["public_fulltext_locator"],
        "raw_text": None,
        "label_groups": [],
        "capture_limitation": "__FILL_OR_NULL__",
    }


def emit(output_dir: Path) -> dict[str, Any]:
    if output_dir.exists():
        fail(f"OUTPUT_DIRECTORY_ALREADY_EXISTS:{output_dir}")
    descriptor = load_json(CAPTURE_DESCRIPTOR_PATH)
    if descriptor.get("state") != "CAPTURE_DESCRIPTOR_WEB_FULLTEXT_RECONCILED_PRE_TEXT":
        fail("unexpected reconciled capture descriptor state")
    records = descriptor.get("records")
    if not isinstance(records, list) or len(records) != 60:
        fail("expected exactly 60 frozen capture descriptors")
    ids = [r["opaque_bundle_id"] for r in records]
    if len(set(ids)) != 60:
        fail("opaque bundle IDs must be unique")

    output_dir.mkdir(parents=True, exist_ok=False)
    for record in sorted(records, key=lambda r: r["opaque_bundle_id"]):
        name = f"{record['opaque_bundle_id']}.template.json"
        (output_dir / name).write_bytes(canonical_json_bytes(build_template(record)))

    guide = {
        "schema_version": SCAFFOLD_VERSION,
        "template_count": 60,
        "executable_filename_rule": "rename completed B####.template.json to B####.json",
        "required_ready_fields": [
            "capture_state=CAPTURE_READY",
            "source_version",
            "retrieval_date",
            "capture_access_class=FULL_TEXT (public-web complete paper)",
            "source_locator",
            "raw_text",
            "label_groups with at least one L## group and one term",
        ],
        "terminal_inaccessible_fields": [
            "capture_state=TERMINAL_INACCESSIBLE",
            "capture_access_class=INACCESSIBLE",
            "raw_text=null",
            "label_groups=[]",
            "nonempty capture_limitation",
        ],
        "source_locator_prefilled_from_frozen_243_public_fulltext_manifest": True,
        "repository_commit_raw_text_forbidden": True,
        "model_calls": 0,
    }
    (output_dir / "SCAFFOLD.json").write_bytes(canonical_json_bytes(guide))
    return guide


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="relaytheory-239-scaffold-") as td:
        out = Path(td) / "templates"
        guide = emit(out)
        templates = sorted(out.glob("B*.template.json"))
        executable = sorted(out.glob("B[0-9][0-9][0-9][0-9].json"))
        if len(templates) != 60:
            raise AssertionError("expected exactly 60 scaffold templates")
        if executable:
            raise AssertionError("scaffold emitted accidentally executable B####.json")
        first = load_json(templates[0])
        if first["raw_text"] is not None or first["label_groups"] != []:
            raise AssertionError("scaffold unexpectedly contains source text or mask terms")
        if not first["capture_state"].startswith("__FILL_"):
            raise AssertionError("scaffold missing non-executable capture-state sentinel")
        if guide["model_calls"] != 0:
            raise AssertionError("scaffold must have zero model calls")
        if not first["source_locator"].startswith(("http://", "https://")):
            raise AssertionError("scaffold must prefill a frozen public full-text locator")

        try:
            emit(out)
        except ScaffoldError:
            pass
        else:
            raise AssertionError("existing output directory was overwritten")

    print("PAPER2_DESIGNED_SOURCE_CAPTURE_SCAFFOLD_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            return 0
        if args.output_dir is None:
            fail("--output-dir is required outside --self-test")
        guide = emit(args.output_dir)
        print(json.dumps(guide, sort_keys=True))
        return 0
    except (OSError, json.JSONDecodeError, ScaffoldError, AssertionError) as exc:
        print(f"PAPER2_DESIGNED_SOURCE_CAPTURE_SCAFFOLD_V1_INVALID: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
