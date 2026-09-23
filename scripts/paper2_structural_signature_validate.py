#!/usr/bin/env python3
"""CLI for Paper 2 structural-signature v1 validation."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from paper2_claim_ir_validate import ValidationError as ClaimIRValidationError
from paper2_structural_signature_canonical import canonical_artifact_bytes
from paper2_structural_signature_contract import ValidationError, validate
from paper2_structural_signature_replay import replay_summary
from paper2_structural_signature_selftest import self_test

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("research/paper2/structural_signature_v1.example.json"),
    )
    parser.add_argument("--canonical-output", type=Path, default=None)
    parser.add_argument("--replay-output", type=Path, default=None)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        if args.self_test:
            self_test(args.input)
            return 0

        data = json.loads(args.input.read_text(encoding="utf-8"))
        validate(data)
        canonical = canonical_artifact_bytes(data)
        digest = hashlib.sha256(canonical).hexdigest()
        if args.canonical_output is not None:
            args.canonical_output.write_bytes(canonical)
        if args.replay_output is not None:
            args.replay_output.write_text(
                json.dumps(replay_summary(data), ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
            )
        print(f"PAPER2_STRUCTURAL_SIGNATURE_V1_VALID sha256={digest}")
        return 0
    except (OSError, json.JSONDecodeError, ValidationError, ClaimIRValidationError, AssertionError) as exc:
        print(f"PAPER2_STRUCTURAL_SIGNATURE_V1_INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
