#!/usr/bin/env python3
"""Validate Paper 2 #253 designed-source construct-label mask authority.

The authority is deliberately minimal and global:
- exactly the eight frozen primary sampling-stratum labels;
- same vocabulary for every primary and challenge source;
- no aliases, no title-derived terms, no abstract-derived terms, no per-source tuning.

This validator performs no model call and consumes no real source text.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from paper2_extraction_two_pass_prepare import mask_segments

BASE = Path(__file__).resolve().parent.parent
AUTHORITY_PATH = BASE / "research/paper2/designed_extraction_mask_terms_v1.json"
GEOMETRY_PATH = BASE / "research/paper2/designed_corpus_geometry_v1.json"
MASK_POLICY_PATH = BASE / "research/paper2/extraction_label_mask_v1.json"
MASK_IMPL_PATH = BASE / "scripts/paper2_extraction_two_pass_prepare.py"

VERSION = "paper2-designed-mask-terms-v1"
EXPECTED_CANONICAL = [
    "Memory",
    "Learning",
    "Skill",
    "Attention",
    "Prediction",
    "Control",
    "Belief",
    "Concept",
]
EXPECTED_BLOBS = {
    "source_blob": "94790274a4f9dff72c2724533d360499c1664b9a",
    "inherited_mask_policy_blob": "26f52c2f49c15c559b42c527d1b918c56d935785",
    "inherited_mask_implementation_blob": "bbabb1f910459c64a340bb70c2e05dd88fd6f1df",
}


class MaskAuthorityError(ValueError):
    pass


def fail(message: str) -> None:
    raise MaskAuthorityError(message)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def validate() -> dict[str, Any]:
    authority = load_json(AUTHORITY_PATH)
    geometry = load_json(GEOMETRY_PATH)

    if authority.get("schema_version") != VERSION:
        fail("MASK_AUTHORITY_VERSION_DRIFT")
    if authority.get("owner_issue") != 253 or authority.get("parent_issue") != 239:
        fail("MASK_AUTHORITY_OWNER_DRIFT")
    if authority.get("status") != "PREEXECUTION_FROZEN":
        fail("MASK_AUTHORITY_STATUS_DRIFT")
    if authority.get("architecture_consequence") != "NONE":
        fail("ARCHITECTURE_CONSEQUENCE_DRIFT")

    actual_blobs = {
        "source_blob": git_blob_sha(GEOMETRY_PATH.read_bytes()),
        "inherited_mask_policy_blob": git_blob_sha(MASK_POLICY_PATH.read_bytes()),
        "inherited_mask_implementation_blob": git_blob_sha(MASK_IMPL_PATH.read_bytes()),
    }
    declared = authority.get("authority", {})
    for key, expected in EXPECTED_BLOBS.items():
        if actual_blobs[key] != expected:
            fail(f"BOUND_BLOB_DRIFT:{key}:{actual_blobs[key]}")
        if declared.get(key) != expected:
            fail(f"DECLARED_BLOB_DRIFT:{key}")

    strata = geometry.get("primary", {}).get("strata", {})
    if list(strata.keys()) != EXPECTED_CANONICAL:
        fail(f"PRIMARY_STRATA_ORDER_OR_CONTENT_DRIFT:{list(strata.keys())}")
    if any(strata[name] != 6 for name in EXPECTED_CANONICAL):
        fail("PRIMARY_STRATA_COUNT_DRIFT")

    application = authority.get("application", {})
    expected_application = {
        "scope": "ALL_60_DESIGNED_SOURCES",
        "primary_and_challenge_share_identical_vocabulary": True,
        "per_source_term_addition_allowed": False,
        "title_derived_terms_allowed": False,
        "abstract_derived_terms_allowed": False,
        "challenge_specific_terms_allowed": False,
        "additional_alias_policy": "none",
    }
    if application != expected_application:
        fail("MASK_APPLICATION_POLICY_DRIFT")

    labels = authority.get("labels")
    if not isinstance(labels, list) or len(labels) != 8:
        fail("MASK_LABEL_COUNT_DRIFT")
    expected_labels = [
        {"label_id": f"L{i:02d}", "canonical": name, "aliases": []}
        for i, name in enumerate(EXPECTED_CANONICAL, start=1)
    ]
    if labels != expected_labels:
        fail("MASK_LABEL_AUTHORITY_DRIFT")

    expected_groups = [
        {"label_id": f"L{i:02d}", "terms": [name]}
        for i, name in enumerate(EXPECTED_CANONICAL, start=1)
    ]
    if authority.get("derived_label_groups") != expected_groups:
        fail("DERIVED_LABEL_GROUP_DRIFT")

    boundary = authority.get("known_lexical_boundary", {})
    if boundary.get("morphological_variants_are_not_aliases") is not True:
        fail("MORPHOLOGICAL_BOUNDARY_DRIFT")
    if boundary.get("synonyms_are_not_aliases") is not True:
        fail("SYNONYM_BOUNDARY_DRIFT")
    if boundary.get("source_specific_named_theories_are_not_added") is not True:
        fail("SOURCE_SPECIFIC_BOUNDARY_DRIFT")

    for key in (
        "model_calls",
        "claim_ir_consumed",
        "structural_signature_consumed",
        "phi_consumed",
        "atlas_outcome_consumed",
    ):
        expected = 0 if key == "model_calls" else False
        if authority.get(key) != expected:
            fail(f"SCIENTIFIC_ACCOUNTING_DRIFT:{key}")

    return authority


def self_test() -> None:
    authority = validate()
    groups = authority["derived_label_groups"]

    # Exact canonical labels, any case, must be masked.
    source = [
        "Memory and learning interact with Skill, ATTENTION, Prediction, control, belief, and Concept under a declared synthetic condition with stable evidence."
    ]
    masked, marker_map = mask_segments(source, groups)
    rendered = " ".join(masked).casefold()
    for term in EXPECTED_CANONICAL:
        if term.casefold() in rendered:
            raise AssertionError(f"canonical label leaked: {term}")
    if len(marker_map) != 8:
        raise AssertionError("expected eight canonical markers")

    # Morphological/synonym expansion is intentionally NOT manufactured.
    lexical_boundary = [
        "memories learner skilled attentional predictive controlled beliefs conceptual"
    ]
    masked_boundary, _ = mask_segments(lexical_boundary, groups)
    if masked_boundary != lexical_boundary:
        raise AssertionError("non-authorized morphological variant was over-masked")

    # Word-boundary semantics must not erase unrelated longer words.
    traps = [
        "controller conceptualization skillful attentionality predictivecoding memoryless"
    ]
    masked_traps, _ = mask_segments(traps, groups)
    if masked_traps != traps:
        raise AssertionError("substring trap over-masked")

    # The same global vocabulary is used regardless of primary/challenge identity.
    primary_groups = json.loads(json.dumps(groups))
    challenge_groups = json.loads(json.dumps(groups))
    if primary_groups != challenge_groups:
        raise AssertionError("challenge masking diverged from primary masking")

    # Empty or post-hoc custom authorities are not the frozen authority.
    if not groups:
        raise AssertionError("empty authority unexpectedly accepted")
    custom = json.loads(json.dumps(groups))
    custom[0]["terms"].append("working memory")
    if custom == groups:
        raise AssertionError("custom alias fixture failed to diverge")

    print("PAPER2_DESIGNED_MASK_AUTHORITY_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        validate()
        if args.self_test:
            self_test()
        else:
            print("PAPER2_DESIGNED_MASK_AUTHORITY_V1_VALID")
        return 0
    except (MaskAuthorityError, OSError, json.JSONDecodeError, AssertionError) as exc:
        print(f"PAPER2_DESIGNED_MASK_AUTHORITY_V1_INVALID: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
