#!/usr/bin/env python3
"""Prepare masked, segmented Paper 2 sources for two-pass extraction.

Owner: #162.

This is pre-execution apparatus code. It performs no model call and consumes no
scientific transaction. Raw primary-source text remains local and is never
written to repository authority by this module.

Pipeline:
raw source
-> NFKC/whitespace normalization
-> deterministic sentence-like segmentation
-> deterministic construct-label masking
-> Normal advisory input
-> finite SystemOne focus selection
-> <=3-span compact source for paper2-two-pass-systemone-v2

Primary held-out work selection is owned by #167, not this module.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from paper2_extraction_bundle_prepare import canonical_json_bytes
from paper2_extraction_procedure_validate import ContractError, validate_source


PROTOCOL_VERSION = "paper2-two-pass-real-protocol-v1"
MASK_VERSION = "paper2-extraction-label-mask-v1"
SOURCE_VERSION = "paper2-extraction-source-bundle-v1"
UNRESOLVED = "__unresolved__"
NONE = "none"
MAX_SEGMENTS = 32
MAX_FOCUS = 3
MIN_NON_MASK_WORDS = 5
SEGMENT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\[])")
MARKER_RE = re.compile(r"\[CONSTRUCT_[0-9]{2}\]")


class PreparationError(ValueError):
    pass


def fail(message: str) -> None:
    raise PreparationError(message)


def normalize_text(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        fail("source text must be a non-empty string")
    return " ".join(unicodedata.normalize("NFKC", text).split())


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_protocol(protocol: Any, prompt_bytes: bytes) -> dict[str, Any]:
    if not isinstance(protocol, dict):
        fail("protocol must be object")
    if protocol.get("schema_version") != PROTOCOL_VERSION:
        fail("protocol schema_version")
    if protocol.get("owner_issue") != 162:
        fail("protocol owner_issue")
    if protocol.get("real_pilot_authorized") is not False:
        fail("real pilot must remain unauthorized during preparation")
    if protocol.get("basis_decomposition_authorized") is not False:
        fail("basis decomposition must remain unauthorized")

    sample = protocol.get("sample_authority")
    if not isinstance(sample, dict):
        fail("sample_authority missing")
    if sample.get("primary_heldout_owner_issue") != 167:
        fail("primary heldout authority must be #167")
    if sample.get("primary_heldout_selection_local_to_162") is not False:
        fail("#162 must not select primary heldout works")
    if sample.get("primary_target_works") != 1000:
        fail("primary target must reflect current #167 K=1000")
    if sample.get("max_selected_claims_per_work_inherited_from_158") != 3:
        fail("claim cap must remain 3")

    normal = protocol.get("normal_pass")
    if not isinstance(normal, dict):
        fail("normal_pass missing")
    digest = hashlib.sha256(prompt_bytes).hexdigest()
    if digest != normal.get("prompt_sha256_utf8"):
        fail(
            "Normal prompt digest mismatch: "
            f"manifest={normal.get('prompt_sha256_utf8')} file={digest}"
        )
    if normal.get("temperature") != 0.2 or normal.get("top_p") != 1.0:
        fail("Normal stochastic config drift")
    if normal.get("max_tokens") != 1024:
        fail("Normal max_tokens drift")
    if normal.get("reasoning_effort") != "none":
        fail("Normal reasoning must be disabled")
    if normal.get("cache_prompt") is not False:
        fail("Normal cache_prompt must be false")
    if normal.get("context_length") != 8192:
        fail("Normal context must remain 8192")

    isolation = protocol.get("replicate_isolation")
    if not isinstance(isolation, dict):
        fail("replicate_isolation missing")
    if isolation.get("policy") != "separate_owned_llama_cpp_process_lifetime_per_replicate":
        fail("A/B process-level isolation policy drift")
    for key in (
        "same_model_artifact_required",
        "same_normal_prompt_required",
        "same_masked_source_bytes_required",
        "same_configs_required",
        "cross_replicate_visibility_forbidden",
        "cache_reuse_across_replicates_forbidden",
        "retry_after_first_scientific_call_forbidden",
    ):
        if isolation.get(key) is not True:
            fail(f"replicate_isolation.{key} must be true")
    return protocol


def validate_mask_policy(policy: Any) -> dict[str, Any]:
    if not isinstance(policy, dict):
        fail("mask policy must be object")
    if policy.get("schema_version") != MASK_VERSION:
        fail("mask schema_version")
    if policy.get("owner_issue") != 162:
        fail("mask owner_issue")
    segmentation = policy.get("segmentation")
    if not isinstance(segmentation, dict):
        fail("segmentation missing")
    if segmentation.get("maximum_units") != MAX_SEGMENTS:
        fail("segmentation maximum_units drift")
    if segmentation.get("truncate_when_over_limit") is not False:
        fail("source segmentation may not silently truncate")
    collapse = policy.get("semantic_collapse_gate")
    if not isinstance(collapse, dict):
        fail("semantic_collapse_gate missing")
    if collapse.get("minimum_non_marker_word_tokens_across_source") != MIN_NON_MASK_WORDS:
        fail("semantic collapse threshold drift")
    focus = policy.get("focus_selection")
    if not isinstance(focus, dict):
        fail("focus_selection missing")
    if focus.get("maximum_selected_units") != MAX_FOCUS:
        fail("focus maximum drift")
    if focus.get("explicit_unresolved_choice") != UNRESOLVED:
        fail("focus unresolved choice drift")
    return policy


def segment_text(raw_text: str) -> list[str]:
    normalized = normalize_text(raw_text)
    segments = [part.strip() for part in SEGMENT_RE.split(normalized) if part.strip()]
    if not segments:
        fail("segmentation produced no units")
    if len(segments) > MAX_SEGMENTS:
        fail(
            f"segmentation produced {len(segments)} units; "
            f"maximum is {MAX_SEGMENTS}; no truncation permitted"
        )
    return segments


def _normalized_terms(label_groups: list[dict[str, Any]]) -> list[tuple[str, str]]:
    seen_ids: set[str] = set()
    entries: list[tuple[str, str]] = []
    for index, group in enumerate(label_groups, start=1):
        if not isinstance(group, dict):
            fail(f"label_groups[{index-1}] must be object")
        label_id = group.get("label_id")
        terms = group.get("terms")
        if not isinstance(label_id, str) or not re.fullmatch(r"L[0-9]{2}", label_id):
            fail(f"invalid label_id at index {index-1}")
        if label_id in seen_ids:
            fail(f"duplicate label_id {label_id}")
        seen_ids.add(label_id)
        if not isinstance(terms, list) or not terms:
            fail(f"{label_id}: terms must be non-empty list")
        normalized_terms: set[str] = set()
        for term in terms:
            value = normalize_text(term)
            if value.casefold() in normalized_terms:
                fail(f"{label_id}: duplicate normalized term")
            normalized_terms.add(value.casefold())
            entries.append((label_id, value))
    entries.sort(key=lambda item: (-len(item[1]), item[0], item[1].casefold()))
    return entries


def _term_pattern(term: str) -> re.Pattern[str]:
    pieces = [re.escape(piece) for piece in term.split(" ")]
    body = r"\s+".join(pieces)
    return re.compile(rf"(?<!\w){body}(?!\w)", flags=re.IGNORECASE)


def mask_segments(
    segments: list[str],
    label_groups: list[dict[str, Any]],
) -> tuple[list[str], dict[str, str]]:
    entries = _normalized_terms(label_groups)
    label_ids = sorted({label_id for label_id, _ in entries})
    marker_by_label = {
        label_id: f"[CONSTRUCT_{index:02d}]"
        for index, label_id in enumerate(label_ids, start=1)
    }
    masked: list[str] = []
    for segment in segments:
        value = segment
        for label_id, term in entries:
            value = _term_pattern(term).sub(marker_by_label[label_id], value)
        masked.append(value)

    residual = MARKER_RE.sub(" ", " ".join(masked))
    words = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", residual)
    if len(words) < MIN_NON_MASK_WORDS:
        fail(
            "construct-label masking leaves insufficient non-marker semantic "
            f"surface: {len(words)} word tokens < {MIN_NON_MASK_WORDS}"
        )
    return masked, marker_by_label


def build_segmented_bundle(
    *,
    bundle_id: str,
    raw_text: str,
    label_groups: list[dict[str, Any]],
    source_language: str = "en",
) -> dict[str, Any]:
    raw_normalized = normalize_text(raw_text)
    raw_segments = segment_text(raw_normalized)
    masked_segments, marker_map = mask_segments(raw_segments, label_groups)
    bundle = {
        "schema_version": SOURCE_VERSION,
        "bundle_id": bundle_id,
        "source_language": source_language,
        "source_spans": [
            {"span_id": f"s{index}", "text": text}
            for index, text in enumerate(masked_segments, start=1)
        ],
    }
    validate_source(bundle)
    return {
        "raw_normalized_sha256": sha256_text(raw_normalized),
        "segmentation_count": len(raw_segments),
        "masked_bundle": bundle,
        "masked_bundle_sha256": sha256_json(bundle),
        "marker_count": len(marker_map),
    }


def build_focus_request(
    bundle: dict[str, Any],
    interpretation: str,
    model: str,
) -> dict[str, Any]:
    validate_source(bundle)
    if not isinstance(interpretation, str) or not interpretation.strip():
        fail("Normal interpretation must be non-empty")
    if not isinstance(model, str) or not model.strip():
        fail("SystemOne model must be non-empty")
    span_ids = [item["span_id"] for item in bundle["source_spans"]]
    criteria = {
        **{span_id: f"source evidence unit {span_id}" for span_id in span_ids},
        NONE: "No additional evidence unit is needed.",
        UNRESOLVED: "The source is insufficient to make this focus decision.",
    }
    return {
        "state": {
            "source": bundle,
            "interpretation": interpretation,
            "authority_rule": (
                "The masked source is authoritative. The Normal interpretation "
                "is advisory. Select evidence units only; do not reconstruct "
                "masked construct labels."
            ),
        },
        "model": model,
        "questions": {
            "focus_1": {
                "type": "choice",
                "instructions": "Select the primary evidence unit for the narrowest source-supported claim.",
                "criteria": criteria,
            },
            "focus_2": {
                "type": "choice",
                "instructions": "Select a second distinct evidence unit only if needed; otherwise choose none.",
                "criteria": criteria,
            },
            "focus_3": {
                "type": "choice",
                "instructions": "Select a third distinct evidence unit only if needed; otherwise choose none.",
                "criteria": criteria,
            },
        },
    }


def compact_focus_bundle(
    bundle: dict[str, Any],
    focus_choices: list[str],
) -> dict[str, Any]:
    validate_source(bundle)
    if not isinstance(focus_choices, list) or len(focus_choices) != MAX_FOCUS:
        fail("focus choices must contain exactly three ordered decisions")
    if focus_choices[0] in {NONE, UNRESOLVED}:
        fail("primary focus must resolve to one source span")
    if UNRESOLVED in focus_choices:
        fail("focus selection unresolved")
    chosen = [value for value in focus_choices if value != NONE]
    if len(chosen) != len(set(chosen)):
        fail("focus selection contains duplicate source spans")
    if not 1 <= len(chosen) <= MAX_FOCUS:
        fail("focus selection cardinality")
    span_map = {item["span_id"]: item for item in bundle["source_spans"]}
    unknown = [value for value in chosen if value not in span_map]
    if unknown:
        fail(f"focus selection references unknown spans: {unknown}")
    compact = {
        "schema_version": SOURCE_VERSION,
        "bundle_id": bundle["bundle_id"],
        "source_language": bundle["source_language"],
        "source_spans": [span_map[value] for value in chosen],
    }
    validate_source(compact)
    return compact


def replica_plan(
    masked_bundle_sha256: str,
    normal_prompt_sha256: str,
) -> dict[str, Any]:
    if not re.fullmatch(r"[0-9a-f]{64}", masked_bundle_sha256):
        fail("masked bundle digest")
    if not re.fullmatch(r"[0-9a-f]{64}", normal_prompt_sha256):
        fail("Normal prompt digest")
    return {
        "A": {
            "owned_process": "A",
            "masked_bundle_sha256": masked_bundle_sha256,
            "normal_prompt_sha256": normal_prompt_sha256,
            "may_read_from": [],
        },
        "B": {
            "owned_process": "B",
            "masked_bundle_sha256": masked_bundle_sha256,
            "normal_prompt_sha256": normal_prompt_sha256,
            "may_read_from": [],
        },
    }


def self_test(protocol_path: Path, mask_path: Path, prompt_path: Path) -> None:
    protocol = load_json(protocol_path)
    policy = load_json(mask_path)
    prompt_bytes = prompt_path.read_bytes()
    validate_protocol(protocol, prompt_bytes)
    validate_mask_policy(policy)

    # N1: construct label is masked while non-label content remains.
    prepared = build_segmented_bundle(
        bundle_id="B9001",
        raw_text=(
            "Working memory stores a limited set of items. "
            "Observed performance decreases when load rises."
        ),
        label_groups=[
            {"label_id": "L01", "terms": ["working memory"]},
        ],
    )
    bundle = prepared["masked_bundle"]
    rendered = canonical_json_bytes(bundle).decode("utf-8")
    if "working memory" in rendered.casefold():
        raise AssertionError("N1 construct label leaked")
    if "[CONSTRUCT_01]" not in rendered:
        raise AssertionError("N1 mask marker missing")

    # N2: substring trap — masking memory must not alter memoryless.
    prepared2 = build_segmented_bundle(
        bundle_id="B9002",
        raw_text=(
            "Memory supports the reported effect. "
            "A memoryless comparator remains unchanged."
        ),
        label_groups=[
            {"label_id": "L01", "terms": ["memory"]},
        ],
    )
    rendered2 = canonical_json_bytes(prepared2["masked_bundle"]).decode("utf-8")
    if "memoryless" not in rendered2.casefold():
        raise AssertionError("N2 substring trap rewrote unrelated word")

    # N3: label-only source fails closed.
    try:
        build_segmented_bundle(
            bundle_id="B9003",
            raw_text="Working memory. Working memory.",
            label_groups=[
                {"label_id": "L01", "terms": ["working memory"]},
            ],
        )
    except PreparationError:
        pass
    else:
        raise AssertionError("N3 semantic collapse unexpectedly passed")

    # N4: segmentation does not truncate.
    too_many = " ".join(f"Sentence {i}." for i in range(1, MAX_SEGMENTS + 2))
    try:
        segment_text(too_many)
    except PreparationError:
        pass
    else:
        raise AssertionError("N4 over-limit segmentation unexpectedly passed")

    # N5: focus selection is finite and deterministic.
    request = build_focus_request(
        bundle,
        "The source describes a limited storage claim at s1 and a load effect at s2.",
        "synthetic-systemone",
    )
    if set(request["questions"]) != {"focus_1", "focus_2", "focus_3"}:
        raise AssertionError("N5 focus question drift")
    compact = compact_focus_bundle(bundle, ["s1", "s2", NONE])
    if [x["span_id"] for x in compact["source_spans"]] != ["s1", "s2"]:
        raise AssertionError("N5 compact focus order drift")

    # N6: duplicate and unresolved focus decisions fail closed.
    for choices in (["s1", "s1", NONE], [UNRESOLVED, NONE, NONE]):
        try:
            compact_focus_bundle(bundle, list(choices))
        except PreparationError:
            pass
        else:
            raise AssertionError("N6 invalid focus selection unexpectedly passed")

    # N7: A/B plans share input digests but no cross-replicate read authority.
    plan = replica_plan(
        prepared["masked_bundle_sha256"],
        protocol["normal_pass"]["prompt_sha256_utf8"],
    )
    if plan["A"]["owned_process"] == plan["B"]["owned_process"]:
        raise AssertionError("N7 A/B must use distinct owned process lifetimes")
    if plan["A"]["may_read_from"] or plan["B"]["may_read_from"]:
        raise AssertionError("N7 cross-replicate visibility leaked")

    # N8: #162 may not become a local held-out selector.
    if protocol["sample_authority"]["primary_heldout_owner_issue"] != 167:
        raise AssertionError("N8 heldout authority drift")

    print("PAPER2_TWO_PASS_REAL_PREP_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--protocol",
        type=Path,
        default=Path("research/paper2/extraction_two_pass_real_protocol_v1.json"),
    )
    parser.add_argument(
        "--mask-policy",
        type=Path,
        default=Path("research/paper2/extraction_label_mask_v1.json"),
    )
    parser.add_argument(
        "--normal-prompt",
        type=Path,
        default=Path("research/paper2/extraction_normal_prompt_v1.md"),
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        protocol = load_json(args.protocol)
        policy = load_json(args.mask_policy)
        validate_protocol(protocol, args.normal_prompt.read_bytes())
        validate_mask_policy(policy)
        if args.self_test:
            self_test(args.protocol, args.mask_policy, args.normal_prompt)
        else:
            print("PAPER2_TWO_PASS_REAL_PREP_V1_VALID")
        return 0
    except (
        OSError,
        json.JSONDecodeError,
        PreparationError,
        ContractError,
        AssertionError,
    ) as exc:
        print(f"PAPER2_TWO_PASS_REAL_PREP_V1_INVALID: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
