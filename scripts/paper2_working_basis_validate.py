#!/usr/bin/env python3
"""Validate Paper 2 working measurement basis v1.

Owner: #226. Measurement contract only; not an ontology-completeness claim.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "paper2-working-basis-v1"
EXPECTED_SYMBOLS = ["S", "Pi", "K", "O", "T", "C", "Q", "P"]
EXPECTED_BINDING = {
    "S": ["basis_instantiation.coordinates"],
    "Pi": ["control_surface.partition_Pi", "basis_instantiation.coordinates", "relation_topology"],
    "K": ["relation_topology"],
    "O": ["basis_instantiation.coordinates", "relation_topology"],
    "T": ["temporal_structure"],
    "C": ["control_surface.resource_C"],
    "Q": ["control_surface.criterion_Q"],
    "P": ["control_surface.probe_P", "relation_topology"],
}
EXPECTED_RULES = {
    "construct_label_inference_forbidden": True,
    "author_venue_citation_inference_forbidden": True,
    "topology_preservation_required": True,
    "posthoc_control_selection_forbidden": True,
    "basis_growth_from_single_residual_forbidden": True,
    "coordinate_presence_not_equivalence": True,
}
EXPECTED_RESIDUAL_CLASSES = [
    "source_underdetermination",
    "claim_ir_expressivity_pressure",
    "basis_semantics_pressure",
    "basis_dimension_pressure",
    "missing_bridge_assumption",
    "formalization_or_witness_pressure",
]
ROOT_KEYS = {
    "schema_version", "status", "ontology_completeness_claim", "coordinates",
    "structural_binding", "assignment_rules", "residual_policy",
}


class ValidationError(ValueError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def exact_keys(value: dict[str, Any], expected: set[str], context: str) -> None:
    actual = set(value)
    if actual != expected:
        fail(f"{context}: keys differ; missing={sorted(expected-actual)} extra={sorted(actual-expected)}")


def validate(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        fail("root: expected object")
    exact_keys(data, ROOT_KEYS, "root")
    if data["schema_version"] != SCHEMA_VERSION:
        fail("root.schema_version: unexpected value")
    if data["status"] != "working_measurement_basis":
        fail("root.status: unexpected value")
    if data["ontology_completeness_claim"] is not False:
        fail("root.ontology_completeness_claim: must be false")

    coords = data["coordinates"]
    if not isinstance(coords, list) or len(coords) != 8:
        fail("root.coordinates: expected exactly eight coordinates")
    symbols = []
    names = set()
    for i, item in enumerate(coords):
        if not isinstance(item, dict):
            fail(f"root.coordinates[{i}]: expected object")
        exact_keys(item, {"symbol", "name", "description"}, f"root.coordinates[{i}]")
        if not all(isinstance(item[k], str) and item[k].strip() for k in ("symbol","name","description")):
            fail(f"root.coordinates[{i}]: nonempty strings required")
        symbols.append(item["symbol"])
        if item["name"] in names:
            fail(f"root.coordinates[{i}].name: duplicate")
        names.add(item["name"])
    if symbols != EXPECTED_SYMBOLS:
        fail(f"root.coordinates: symbol order/identity mismatch {symbols!r}")

    binding = data["structural_binding"]
    if binding != EXPECTED_BINDING:
        fail("root.structural_binding: must match frozen v1 structural bindings exactly")

    rules = data["assignment_rules"]
    if rules != EXPECTED_RULES:
        fail("root.assignment_rules: must match frozen anti-smuggling rules exactly")

    residual = data["residual_policy"]
    if not isinstance(residual, dict):
        fail("root.residual_policy: expected object")
    exact_keys(residual, {"automatic_basis_growth", "classes"}, "root.residual_policy")
    if residual["automatic_basis_growth"] is not False:
        fail("root.residual_policy.automatic_basis_growth: must be false")
    if residual["classes"] != EXPECTED_RESIDUAL_CLASSES:
        fail("root.residual_policy.classes: unexpected value/order")

    # The basis itself must remain construct-neutral.
    serialized = json.dumps(data, ensure_ascii=False).casefold()
    for forbidden in (
        "working memory", "attentionlike", "memorylike", "learninglike",
        "skilllike", "belieflike", "conceptlike", "habitlike",
    ):
        if forbidden in serialized:
            fail(f"root: construct-specific token leaked into basis contract: {forbidden!r}")
    return data


def self_test(path: Path) -> None:
    base = json.loads(path.read_text(encoding="utf-8"))
    validate(base)

    bad = copy.deepcopy(base)
    bad["ontology_completeness_claim"] = True
    try:
        validate(bad)
    except ValidationError:
        pass
    else:
        raise AssertionError("ontology-completeness trap unexpectedly validated")

    bad = copy.deepcopy(base)
    bad["coordinates"].pop()
    try:
        validate(bad)
    except ValidationError:
        pass
    else:
        raise AssertionError("missing-axis fixture unexpectedly validated")

    bad = copy.deepcopy(base)
    bad["assignment_rules"]["construct_label_inference_forbidden"] = False
    try:
        validate(bad)
    except ValidationError:
        pass
    else:
        raise AssertionError("construct-label shortcut unexpectedly validated")

    bad = copy.deepcopy(base)
    bad["structural_binding"]["K"] = []
    try:
        validate(bad)
    except ValidationError:
        pass
    else:
        raise AssertionError("empty-topology binding unexpectedly validated")

    bad = copy.deepcopy(base)
    bad["coordinates"][0]["description"] += " MemoryLike"
    try:
        validate(bad)
    except ValidationError:
        pass
    else:
        raise AssertionError("construct-specific basis leakage unexpectedly validated")

    print("PAPER2_WORKING_BASIS_V1_SELFTEST_PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="research/paper2/working_basis_v1.json",
        type=Path,
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    validate(data)
    if args.self_test:
        self_test(args.input)
    else:
        print("PAPER2_WORKING_BASIS_V1_VALID")


if __name__ == "__main__":
    main()
