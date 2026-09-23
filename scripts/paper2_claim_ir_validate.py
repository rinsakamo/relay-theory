#!/usr/bin/env python3
"""Validate Paper 2 ClaimIR v1 and emit its deterministic blinded projection.

Owner: #145
ClaimIR is analysis infrastructure, not RelayTheory ontology.
The validator intentionally uses only Python's standard library.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "paper2-claim-ir-v1"
BLINDED_SCHEMA_VERSION = "paper2-blinded-claim-v1"

TOP_KEYS = {"schema_version", "claim_id", "provenance", "extraction", "claim_core"}
PROVENANCE_KEYS = {
    "paper_id",
    "source_language",
    "source_spans",
    "authors",
    "institutions",
    "venue",
    "citation_count",
    "construct_labels",
}
SPAN_KEYS = {"span_id", "locator"}
EXTRACTION_KEYS = {
    "extractor",
    "extractor_version",
    "procedure_version",
    "extracted_at",
    "manual_review_status",
}
CORE_KEYS = {"claim_type", "modality", "scope", "nodes", "relations"}
SCOPE_KEYS = {"conditions", "population", "substrate", "task", "temporal_scope"}
NODE_KEYS = {"id", "role", "description", "source_span_ids", "grounding"}
RELATION_KEYS = {
    "id",
    "kind",
    "arguments",
    "description",
    "source_span_ids",
    "grounding",
}

CLAIM_TYPES = {
    "relation",
    "criterion",
    "mapping",
    "comparison",
    "counterfactual",
    "definition",
    "constraint",
    "other",
}
MODALITIES = {
    "descriptive",
    "necessary",
    "sufficient",
    "probabilistic",
    "definitional",
    "counterfactual",
    "comparative",
    "other",
}
NODE_ROLES = {
    "condition",
    "available_information",
    "state_or_structure",
    "intervention",
    "response_or_outcome",
    "criterion",
    "probe",
    "partition",
    "other",
}
RELATION_KINDS = {
    "equals",
    "differs",
    "depends_on",
    "changes",
    "predicts",
    "maps_to",
    "satisfies",
    "distinguishes",
    "precedes",
    "constrains",
    "equivalent",
    "other",
}
GROUNDING = {"explicit", "normalized"}
REVIEW_STATES = {"unreviewed", "reviewed", "adjudicated"}

FORBIDDEN_RESULT_MARKERS = {
    "basis_elements",
    "basis_mapping",
    "basis_witness",
    "decomposition_success",
    "decomposition_failure",
    "coverage_score",
    "lean_theorem",
    "lean_result",
    "residual_type",
    "basis_extension",
    "acceptance_verdict",
}
ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
CLAIM_ID_RE = re.compile(r"^[A-Z][A-Z0-9._-]{0,63}$")


class ValidationError(ValueError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def expect_object(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{context}: expected object")
    return value


def expect_list(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{context}: expected array")
    return value


def expect_string(value: Any, context: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        fail(f"{context}: expected string")
    if not allow_empty and not value.strip():
        fail(f"{context}: empty string")
    return value


def exact_keys(obj: dict[str, Any], expected: set[str], context: str) -> None:
    actual = set(obj)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        fail(f"{context}: key mismatch; missing={missing} extra={extra}")


def unique_strings(values: Any, context: str, *, nonempty: bool = False) -> list[str]:
    items = expect_list(values, context)
    if nonempty and not items:
        fail(f"{context}: must not be empty")
    out: list[str] = []
    for index, item in enumerate(items):
        out.append(expect_string(item, f"{context}[{index}]"))
    if len(out) != len(set(out)):
        fail(f"{context}: duplicate values")
    return out


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    value = re.sub(r"[^\w]+", " ", value, flags=re.UNICODE)
    return " ".join(value.split())


def string_tree(value: Any, path: str = "claim_core") -> Iterable[tuple[str, str]]:
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, list):
        for i, item in enumerate(value):
            yield from string_tree(item, f"{path}[{i}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            yield f"{path}.__key__", str(key)
            yield from string_tree(item, f"{path}.{key}")


def authority_terms(provenance: dict[str, Any]) -> list[str]:
    terms: list[str] = []
    terms.extend(provenance["authors"])
    terms.extend(provenance["institutions"])
    terms.extend(provenance["construct_labels"])
    if provenance["venue"]:
        terms.append(provenance["venue"])
    return [term for term in terms if normalize_text(term)]


def reject_leakage(data: dict[str, Any]) -> None:
    provenance = data["provenance"]
    forbidden_terms = authority_terms(provenance)
    marker_terms = [marker.replace("_", " ") for marker in FORBIDDEN_RESULT_MARKERS]

    for path, value in string_tree(data["claim_core"]):
        normalized = normalize_text(value)
        padded = f" {normalized} "
        for term in forbidden_terms:
            needle = normalize_text(term)
            if needle and f" {needle} " in padded:
                fail(f"{path}: authority/construct label leaks into claim_core: {term!r}")
        for marker in marker_terms:
            needle = normalize_text(marker)
            if needle and f" {needle} " in padded:
                fail(f"{path}: decomposition-result marker leaks into claim_core: {marker!r}")

    claim_id = normalize_text(data["claim_id"])
    for term in forbidden_terms:
        needle = normalize_text(term)
        if needle and needle in claim_id:
            fail("claim_id: authority/construct label leakage")


def validate(data: Any) -> dict[str, Any]:
    root = expect_object(data, "root")
    exact_keys(root, TOP_KEYS, "root")

    if root["schema_version"] != SCHEMA_VERSION:
        fail("root.schema_version: unexpected value")

    claim_id = expect_string(root["claim_id"], "root.claim_id")
    if not CLAIM_ID_RE.fullmatch(claim_id):
        fail("root.claim_id: invalid identifier")

    provenance = expect_object(root["provenance"], "root.provenance")
    exact_keys(provenance, PROVENANCE_KEYS, "root.provenance")
    expect_string(provenance["paper_id"], "root.provenance.paper_id")
    expect_string(provenance["source_language"], "root.provenance.source_language")
    authors = unique_strings(provenance["authors"], "root.provenance.authors")
    institutions = unique_strings(
        provenance["institutions"], "root.provenance.institutions"
    )
    construct_labels = unique_strings(
        provenance["construct_labels"], "root.provenance.construct_labels"
    )
    venue = provenance["venue"]
    if venue is not None:
        expect_string(venue, "root.provenance.venue")
    citation_count = provenance["citation_count"]
    if citation_count is not None:
        if not isinstance(citation_count, int) or isinstance(citation_count, bool):
            fail("root.provenance.citation_count: expected non-negative integer or null")
        if citation_count < 0:
            fail("root.provenance.citation_count: expected non-negative integer or null")

    spans = expect_list(provenance["source_spans"], "root.provenance.source_spans")
    if not spans:
        fail("root.provenance.source_spans: must not be empty")
    span_ids: set[str] = set()
    for index, span_value in enumerate(spans):
        span = expect_object(span_value, f"root.provenance.source_spans[{index}]")
        exact_keys(span, SPAN_KEYS, f"root.provenance.source_spans[{index}]")
        span_id = expect_string(
            span["span_id"], f"root.provenance.source_spans[{index}].span_id"
        )
        if not ID_RE.fullmatch(span_id):
            fail(f"root.provenance.source_spans[{index}].span_id: invalid identifier")
        if span_id in span_ids:
            fail(f"root.provenance.source_spans[{index}].span_id: duplicate")
        span_ids.add(span_id)
        expect_string(
            span["locator"], f"root.provenance.source_spans[{index}].locator"
        )

    extraction = expect_object(root["extraction"], "root.extraction")
    exact_keys(extraction, EXTRACTION_KEYS, "root.extraction")
    for key in ("extractor", "extractor_version", "procedure_version", "extracted_at"):
        expect_string(extraction[key], f"root.extraction.{key}")
    if extraction["manual_review_status"] not in REVIEW_STATES:
        fail("root.extraction.manual_review_status: unexpected value")

    core = expect_object(root["claim_core"], "root.claim_core")
    exact_keys(core, CORE_KEYS, "root.claim_core")
    if core["claim_type"] not in CLAIM_TYPES:
        fail("root.claim_core.claim_type: unexpected value")
    if core["modality"] not in MODALITIES:
        fail("root.claim_core.modality: unexpected value")

    scope = expect_object(core["scope"], "root.claim_core.scope")
    exact_keys(scope, SCOPE_KEYS, "root.claim_core.scope")
    for key in sorted(SCOPE_KEYS):
        values = expect_list(scope[key], f"root.claim_core.scope.{key}")
        for index, item in enumerate(values):
            expect_string(item, f"root.claim_core.scope.{key}[{index}]")

    nodes = expect_list(core["nodes"], "root.claim_core.nodes")
    if not nodes:
        fail("root.claim_core.nodes: must not be empty")
    node_ids: set[str] = set()
    for index, node_value in enumerate(nodes):
        path = f"root.claim_core.nodes[{index}]"
        node = expect_object(node_value, path)
        exact_keys(node, NODE_KEYS, path)
        node_id = expect_string(node["id"], f"{path}.id")
        if not ID_RE.fullmatch(node_id):
            fail(f"{path}.id: invalid identifier")
        if node_id in node_ids:
            fail(f"{path}.id: duplicate")
        node_ids.add(node_id)
        if node["role"] not in NODE_ROLES:
            fail(f"{path}.role: unexpected value")
        expect_string(node["description"], f"{path}.description")
        refs = unique_strings(node["source_span_ids"], f"{path}.source_span_ids", nonempty=True)
        unknown = sorted(set(refs) - span_ids)
        if unknown:
            fail(f"{path}.source_span_ids: unknown spans {unknown}")
        if node["grounding"] not in GROUNDING:
            fail(f"{path}.grounding: unexpected value")

    relations = expect_list(core["relations"], "root.claim_core.relations")
    relation_ids: set[str] = set()
    for index, relation_value in enumerate(relations):
        path = f"root.claim_core.relations[{index}]"
        relation = expect_object(relation_value, path)
        exact_keys(relation, RELATION_KEYS, path)
        relation_id = expect_string(relation["id"], f"{path}.id")
        if not ID_RE.fullmatch(relation_id):
            fail(f"{path}.id: invalid identifier")
        if relation_id in relation_ids:
            fail(f"{path}.id: duplicate")
        relation_ids.add(relation_id)
        if relation["kind"] not in RELATION_KINDS:
            fail(f"{path}.kind: unexpected value")
        arguments = unique_strings(relation["arguments"], f"{path}.arguments", nonempty=True)
        unknown_nodes = sorted(set(arguments) - node_ids)
        if unknown_nodes:
            fail(f"{path}.arguments: unknown node ids {unknown_nodes}")
        expect_string(relation["description"], f"{path}.description")
        refs = unique_strings(
            relation["source_span_ids"], f"{path}.source_span_ids", nonempty=True
        )
        unknown = sorted(set(refs) - span_ids)
        if unknown:
            fail(f"{path}.source_span_ids: unknown spans {unknown}")
        if relation["grounding"] not in GROUNDING:
            fail(f"{path}.grounding: unexpected value")

    # Keep variables referenced so accidental type regressions remain visible in review.
    _ = authors, institutions, construct_labels
    reject_leakage(root)
    return root


def blinded_projection(data: dict[str, Any]) -> dict[str, Any]:
    validate(data)
    return {
        "schema_version": BLINDED_SCHEMA_VERSION,
        "claim_id": data["claim_id"],
        "claim_core": copy.deepcopy(data["claim_core"]),
    }


def canonical_json_bytes(value: Any) -> bytes:
    rendered = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return (rendered + "\n").encode("utf-8")


def blinded_bytes(data: dict[str, Any]) -> bytes:
    return canonical_json_bytes(blinded_projection(data))


def expect_invalid(data: dict[str, Any], label: str) -> None:
    try:
        validate(data)
    except ValidationError:
        return
    raise AssertionError(f"{label}: adversarial fixture unexpectedly validated")


def self_test(example_path: Path) -> None:
    data = json.loads(example_path.read_text(encoding="utf-8"))
    validate(data)

    blinded = blinded_projection(data)
    assert set(blinded) == {"schema_version", "claim_id", "claim_core"}
    rendered = blinded_bytes(data).decode("utf-8")
    for forbidden in (
        "Example Author",
        "Example Laboratory",
        "Example Journal",
        "working memory",
        "citation_count",
        "paper_id",
        "provenance",
        "basis_mapping",
        "decomposition_success",
    ):
        assert forbidden not in rendered

    n1 = copy.deepcopy(data)
    n1["claim_core"]["basis_mapping"] = []
    expect_invalid(n1, "N1 basis-result smuggling")

    n2 = copy.deepcopy(data)
    n2["claim_core"]["nodes"][0]["description"] = (
        "working memory information available at an earlier observation"
    )
    expect_invalid(n2, "N2 construct-label leakage")

    n3 = copy.deepcopy(data)
    n3["claim_core"]["nodes"][0]["source_span_ids"] = []
    expect_invalid(n3, "N3 ungrounded node")

    n4 = copy.deepcopy(data)
    n4["claim_core"]["relations"][0]["description"] = (
        "Example Author associates the earlier information with the later response"
    )
    expect_invalid(n4, "N4 authority leakage")

    reordered = {key: data[key] for key in reversed(list(data))}
    reordered["claim_core"] = {
        key: data["claim_core"][key]
        for key in reversed(list(data["claim_core"]))
    }
    assert blinded_bytes(data) == blinded_bytes(reordered)

    digest = hashlib.sha256(blinded_bytes(data)).hexdigest()
    assert len(digest) == 64
    print(f"PAPER2_CLAIM_IR_V1_SELFTEST_PASS sha256={digest}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("research/paper2/claim_ir_v1.example.json"),
    )
    parser.add_argument("--blinded-output", type=Path, default=None)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        if args.self_test:
            self_test(args.input)
            return 0

        data = json.loads(args.input.read_text(encoding="utf-8"))
        validate(data)
        output = blinded_bytes(data)
        digest = hashlib.sha256(output).hexdigest()
        if args.blinded_output is not None:
            args.blinded_output.write_bytes(output)
        print(f"CLAIM_IR_V1_VALID sha256={digest}")
        return 0
    except (OSError, json.JSONDecodeError, ValidationError, AssertionError) as exc:
        print(f"CLAIM_IR_V1_INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
