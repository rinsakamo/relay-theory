#!/usr/bin/env python3
"""Compare two valid Paper 2 ClaimIR v1 extractions.

Owner: #147

This tool measures syntactic / structural agreement only. It deliberately does
not infer semantic equivalence of paraphrases and does not inspect any
downstream basis, witness, residual, or decomposition outcome.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from paper2_claim_ir_validate import ValidationError, normalize_text, validate


COMPARE_SCHEMA_VERSION = "paper2-claim-ir-compare-v1"
SCOPE_FIELDS = (
    "conditions",
    "population",
    "substrate",
    "task",
    "temporal_scope",
)


def normalized_set(values: list[str]) -> set[str]:
    return {normalize_text(value) for value in values}


def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    if not union:
        return 1.0
    return len(left & right) / len(union)


def used_source_spans(data: dict[str, Any]) -> set[str]:
    core = data["claim_core"]
    spans: set[str] = set()
    for node in core["nodes"]:
        spans.update(node["source_span_ids"])
    for relation in core["relations"]:
        spans.update(relation["source_span_ids"])
    return spans


def node_signature(
    node: dict[str, Any],
    *,
    include_description: bool,
) -> tuple[Any, ...]:
    signature: tuple[Any, ...] = (
        node["role"],
        node["grounding"],
        tuple(sorted(node["source_span_ids"])),
    )
    if include_description:
        signature += (normalize_text(node["description"]),)
    return signature


def node_signature_map(
    data: dict[str, Any],
    *,
    include_description: bool,
) -> dict[str, tuple[Any, ...]]:
    return {
        node["id"]: node_signature(node, include_description=include_description)
        for node in data["claim_core"]["nodes"]
    }


def node_multiset(
    data: dict[str, Any],
    *,
    include_description: bool,
) -> Counter[tuple[Any, ...]]:
    return Counter(
        node_signature(node, include_description=include_description)
        for node in data["claim_core"]["nodes"]
    )


def relation_signature(
    relation: dict[str, Any],
    node_map: dict[str, tuple[Any, ...]],
    *,
    include_description: bool,
) -> tuple[Any, ...]:
    # Relation argument order is preserved. No relation kind is assumed
    # commutative unless a future contract explicitly declares it.
    args = tuple(node_map[arg] for arg in relation["arguments"])
    signature: tuple[Any, ...] = (
        relation["kind"],
        relation["grounding"],
        args,
        tuple(sorted(relation["source_span_ids"])),
    )
    if include_description:
        signature += (normalize_text(relation["description"]),)
    return signature


def relation_multiset(
    data: dict[str, Any],
    *,
    include_description: bool,
) -> Counter[tuple[Any, ...]]:
    node_map = node_signature_map(
        data,
        include_description=include_description,
    )
    return Counter(
        relation_signature(
            relation,
            node_map,
            include_description=include_description,
        )
        for relation in data["claim_core"]["relations"]
    )


def description_multiset(data: dict[str, Any], kind: str) -> Counter[str]:
    values = data["claim_core"][kind]
    return Counter(normalize_text(item["description"]) for item in values)


def scope_report(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    report: dict[str, Any] = {}
    left_scope = left["claim_core"]["scope"]
    right_scope = right["claim_core"]["scope"]
    for field in SCOPE_FIELDS:
        a = normalized_set(left_scope[field])
        b = normalized_set(right_scope[field])
        report[field] = {
            "exact": a == b,
            "jaccard": jaccard(a, b),
            "left_count": len(a),
            "right_count": len(b),
        }
    return report


def compare(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    validate(left)
    validate(right)

    scope = scope_report(left, right)
    spans_left = used_source_spans(left)
    spans_right = used_source_spans(right)

    nodes_structural = (
        node_multiset(left, include_description=False)
        == node_multiset(right, include_description=False)
    )
    nodes_full = (
        node_multiset(left, include_description=True)
        == node_multiset(right, include_description=True)
    )
    relations_structural = (
        relation_multiset(left, include_description=False)
        == relation_multiset(right, include_description=False)
    )
    relations_full = (
        relation_multiset(left, include_description=True)
        == relation_multiset(right, include_description=True)
    )

    node_descriptions = (
        description_multiset(left, "nodes")
        == description_multiset(right, "nodes")
    )
    relation_descriptions = (
        description_multiset(left, "relations")
        == description_multiset(right, "relations")
    )

    same_claim_type = (
        left["claim_core"]["claim_type"] == right["claim_core"]["claim_type"]
    )
    same_modality = (
        left["claim_core"]["modality"] == right["claim_core"]["modality"]
    )
    all_scope_exact = all(item["exact"] for item in scope.values())
    source_span_exact = spans_left == spans_right

    structural_equivalence = all(
        (
            same_claim_type,
            same_modality,
            all_scope_exact,
            source_span_exact,
            nodes_structural,
            relations_structural,
        )
    )
    full_equivalence = all(
        (
            structural_equivalence,
            nodes_full,
            relations_full,
            node_descriptions,
            relation_descriptions,
        )
    )

    return {
        "schema_version": COMPARE_SCHEMA_VERSION,
        "same_claim_id": left["claim_id"] == right["claim_id"],
        "same_paper_id": (
            left["provenance"]["paper_id"]
            == right["provenance"]["paper_id"]
        ),
        "same_claim_type": same_claim_type,
        "same_modality": same_modality,
        "scope_agreement_by_field": scope,
        "source_span_agreement": {
            "exact": source_span_exact,
            "jaccard": jaccard(spans_left, spans_right),
            "left_used": sorted(spans_left),
            "right_used": sorted(spans_right),
        },
        "node_structure_exact_under_id_renaming": nodes_structural,
        "relation_structure_exact_under_id_renaming": relations_structural,
        "node_descriptions_exact_after_normalization": node_descriptions,
        "relation_descriptions_exact_after_normalization": relation_descriptions,
        "node_full_signatures_exact": nodes_full,
        "relation_full_signatures_exact": relations_full,
        "overall_exact_structural_equivalence": structural_equivalence,
        "overall_exact_full_equivalence": full_equivalence,
        "interpretation": (
            "syntactic_structural_only_not_semantic_equivalence"
        ),
    }


def renamed_and_reordered(data: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(data)
    nodes = out["claim_core"]["nodes"]
    mapping = {
        node["id"]: f"node_{index + 1}"
        for index, node in enumerate(reversed(nodes))
    }
    for node in nodes:
        node["id"] = mapping[node["id"]]
    nodes.reverse()

    relations = out["claim_core"]["relations"]
    for index, relation in enumerate(relations):
        relation["id"] = f"relation_{index + 1}"
        relation["arguments"] = [
            mapping[arg] for arg in relation["arguments"]
        ]
    relations.reverse()
    return out


def expect(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def self_test(example_path: Path) -> None:
    base = json.loads(example_path.read_text(encoding="utf-8"))
    validate(base)

    # P1 — pure presentation renaming / ordering changes.
    p1 = renamed_and_reordered(base)
    r = compare(base, p1)
    expect(r["overall_exact_structural_equivalence"], "P1 structural equivalence")
    expect(r["overall_exact_full_equivalence"], "P1 full equivalence")

    # N1 — modality drift.
    n1 = copy.deepcopy(base)
    n1["claim_core"]["modality"] = "necessary"
    r = compare(base, n1)
    expect(not r["same_modality"], "N1 modality drift")
    expect(not r["overall_exact_structural_equivalence"], "N1 aggregate drift")

    # N2 — node-role drift.
    n2 = copy.deepcopy(base)
    n2["claim_core"]["nodes"][0]["role"] = "criterion"
    r = compare(base, n2)
    expect(
        not r["node_structure_exact_under_id_renaming"],
        "N2 node-role drift",
    )
    expect(
        not r["relation_structure_exact_under_id_renaming"],
        "N2 propagated relation-argument drift",
    )

    # N3 — relation-kind drift.
    n3 = copy.deepcopy(base)
    n3["claim_core"]["relations"][0]["kind"] = "predicts"
    r = compare(base, n3)
    expect(
        not r["relation_structure_exact_under_id_renaming"],
        "N3 relation-kind drift",
    )

    # N4 — source-grounding drift.
    n4 = copy.deepcopy(base)
    n4["claim_core"]["nodes"][0]["source_span_ids"] = ["s2"]
    r = compare(base, n4)
    expect(
        not r["node_structure_exact_under_id_renaming"],
        "N4 source-grounding drift",
    )

    # N5 — paraphrase-only wording. Structural comparison deliberately
    # remains equal while exact normalized-description agreement fails.
    n5 = copy.deepcopy(base)
    n5["claim_core"]["nodes"][0]["description"] = (
        "information presented during the earlier observation"
    )
    n5["claim_core"]["relations"][0]["description"] = (
        "changes in earlier information covary with changes in the later response"
    )
    validate(n5)
    r = compare(base, n5)
    expect(
        r["node_structure_exact_under_id_renaming"],
        "N5 node structure should remain equal",
    )
    expect(
        r["relation_structure_exact_under_id_renaming"],
        "N5 relation structure should remain equal",
    )
    expect(
        not r["node_descriptions_exact_after_normalization"],
        "N5 node wording drift",
    )
    expect(
        not r["relation_descriptions_exact_after_normalization"],
        "N5 relation wording drift",
    )
    expect(
        r["overall_exact_structural_equivalence"],
        "N5 structural equivalence should survive wording drift",
    )
    expect(
        not r["overall_exact_full_equivalence"],
        "N5 full exact equivalence must fail",
    )

    print("PAPER2_CLAIM_IR_COMPARE_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("left", type=Path, nargs="?")
    parser.add_argument("right", type=Path, nargs="?")
    parser.add_argument(
        "--example",
        type=Path,
        default=Path("research/paper2/claim_ir_v1.example.json"),
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        if args.self_test:
            self_test(args.example)
            return 0

        if args.left is None or args.right is None:
            parser.error("left and right ClaimIR paths are required unless --self-test")

        left = json.loads(args.left.read_text(encoding="utf-8"))
        right = json.loads(args.right.read_text(encoding="utf-8"))
        result = compare(left, right)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (OSError, json.JSONDecodeError, ValidationError, AssertionError) as exc:
        print(f"CLAIM_IR_COMPARE_INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
