#!/usr/bin/env python3
"""Paper 2 reference structural adjudication v1.

Owner: #267.
Compiles a valid ClaimIR v1 plus explicit adjudication metadata into the
already-frozen structural-signature v1 / paper2-working-basis-v1 surface.

The verified witness covers structural preservation/adjudication only. It does
not re-prove source truth or source->ClaimIR extraction faithfulness.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from paper2_claim_ir_validate import normalize_text, validate as validate_claim_ir
from paper2_phi_compare import project_first
from paper2_structural_signature_canonical import structural_digest
from paper2_structural_signature_constants import (
    ABSENCE_STATES, FAILURE_LAYERS, ID_RE, RELATION_GROUNDING, RESIDUAL_KINDS,
)
from paper2_structural_signature_contract import validate as validate_structural_signature

SCHEMA_VERSION = "paper2-reference-structural-adjudication-v1"
SCRIPT_VERSION = "1"
STRUCTURAL_VERSION = "paper2-structural-signature-v1"
CLAIM_IR_VERSION = "paper2-claim-ir-v1"
BASIS_VERSION = "paper2-working-basis-v1"
WITNESS_VERSION = "paper2-witness-ref-v1"
RESIDUAL_VERSION = "paper2-residual-taxonomy-v1"

CONTROL_KEYS = ("probe_P", "criterion_Q", "partition_Pi", "resource_C")
TEMPORAL_KEYS = ("time_index", "history_window", "future_horizon", "recurrence", "persistence")
APPROX_KEYS = ("threshold", "tolerance", "confidence", "loss", "comparison_criterion")
ANALYSIS_MODES = {"deterministic", "stochastic", "approximate"}
CONTROL_PROVENANCE = {"source_declared", "experimental_contract", "pre_frozen_generic"}

ROLE_MAP = {
    "condition": "condition",
    "available_information": "information",
    "state_or_structure": "state_or_structure",
    "intervention": "intervention",
    "response_or_outcome": "response_or_outcome",
    "criterion": "criterion",
    "probe": "probe",
    "partition": "partition",
    "other": "other",
}
DIRECT_RELATION_MAP = {
    "depends_on": "depends_on",
    "maps_to": "maps_to",
    "precedes": "precedes",
    "constrains": "constrains",
    "distinguishes": "distinguishes",
    "equivalent": "equivalent",
    "other": "other",
}
UNSUPPORTED_TO_OTHER = {"equals", "differs", "changes", "predicts", "satisfies"}


class AdjudicationError(ValueError):
    pass


def fail(message: str) -> None:
    raise AdjudicationError(message)


def exact_keys(value: Any, expected: set[str], context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{context}: expected object")
    actual = set(value)
    if actual != expected:
        fail(f"{context}: keys differ; missing={sorted(expected-actual)} extra={sorted(actual-expected)}")
    return value


def expect_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{context}: expected nonempty string")
    return value


def expect_list(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{context}: expected array")
    return value


def expect_bool(value: Any, context: str) -> bool:
    if not isinstance(value, bool):
        fail(f"{context}: expected boolean")
    return value


def node_map(claim_ir: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in claim_ir["claim_core"]["nodes"]}


def span_ids(claim_ir: dict[str, Any]) -> set[str]:
    return {item["span_id"] for item in claim_ir["provenance"]["source_spans"]}


def validate_span_refs(values: Any, spans: set[str], context: str, *, nonempty: bool = True) -> list[str]:
    items = expect_list(values, context)
    if nonempty and not items:
        fail(f"{context}: must not be empty")
    out = []
    for i, item in enumerate(items):
        value = expect_string(item, f"{context}[{i}]")
        if value not in spans:
            fail(f"{context}[{i}]: unknown source span {value!r}")
        out.append(value)
    if len(out) != len(set(out)):
        fail(f"{context}: duplicate source span")
    return out


def validate_state(value: Any, spans: set[str], context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{context}: expected object")
    if value.get("state") == "present":
        exact_keys(value, {"state", "source_span_ids"}, context)
        validate_span_refs(value["source_span_ids"], spans, f"{context}.source_span_ids")
    else:
        exact_keys(value, {"state"}, context)
        if value["state"] not in ABSENCE_STATES:
            fail(f"{context}.state: unexpected value")
    return value


def walk_strings(value: Any):
    # Schema keys are frozen contract vocabulary, not analyst-authored content.
    # Leakage checks therefore inspect values only; otherwise a source construct
    # such as "confidence" can collide with the mandatory approximation.confidence
    # field name and create a false positive.
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)


def reject_label_leakage(adjudication: dict[str, Any], claim_ir: dict[str, Any]) -> None:
    forbidden = list(claim_ir["provenance"]["construct_labels"])
    forbidden += list(claim_ir["provenance"]["authors"])
    forbidden += list(claim_ir["provenance"]["institutions"])
    if claim_ir["provenance"]["venue"]:
        forbidden.append(claim_ir["provenance"]["venue"])
    analysis = {key: value for key, value in adjudication.items() if key != "adjudicator"}
    haystacks = [f" {normalize_text(value)} " for value in walk_strings(analysis)]
    for term in forbidden:
        needle = normalize_text(term)
        if needle and any(f" {needle} " in hay for hay in haystacks):
            fail(f"analysis surface leaks source authority/construct term {term!r}")


def validate_adjudication(adjudication: Any, claim_ir: dict[str, Any]) -> dict[str, Any]:
    validate_claim_ir(claim_ir)
    root = exact_keys(
        adjudication,
        {
            "schema_version", "claim_id", "adjudicator", "coordinate_map",
            "controls", "temporal", "approximation", "bridge_assumptions", "decision",
        },
        "root",
    )
    if root["schema_version"] != SCHEMA_VERSION:
        fail("root.schema_version: unexpected value")
    if root["claim_id"] != claim_ir["claim_id"]:
        fail("root.claim_id: ClaimIR mismatch")

    adjudicator = exact_keys(
        root["adjudicator"], {"tool", "version", "procedure", "adjudicated_at"}, "root.adjudicator"
    )
    for key, value in adjudicator.items():
        expect_string(value, f"root.adjudicator.{key}")

    nodes = node_map(claim_ir)
    spans = span_ids(claim_ir)

    coords = expect_list(root["coordinate_map"], "root.coordinate_map")
    if len(coords) != len(nodes):
        fail("root.coordinate_map: exactly one coordinate per ClaimIR node is required")
    seen_nodes: set[str] = set()
    seen_coords: set[str] = set()
    for i, item in enumerate(coords):
        path = f"root.coordinate_map[{i}]"
        row = exact_keys(item, {"claim_node_id", "coordinate_id", "required"}, path)
        node_id = expect_string(row["claim_node_id"], f"{path}.claim_node_id")
        coord_id = expect_string(row["coordinate_id"], f"{path}.coordinate_id")
        if node_id not in nodes:
            fail(f"{path}.claim_node_id: unknown ClaimIR node")
        if not ID_RE.fullmatch(coord_id):
            fail(f"{path}.coordinate_id: invalid identifier")
        if node_id in seen_nodes or coord_id in seen_coords:
            fail(f"{path}: duplicate node or coordinate")
        seen_nodes.add(node_id)
        seen_coords.add(coord_id)
        expect_bool(row["required"], f"{path}.required")
    if seen_nodes != set(nodes):
        fail("root.coordinate_map: incomplete ClaimIR-node coverage")

    controls = exact_keys(root["controls"], set(CONTROL_KEYS), "root.controls")
    for key in CONTROL_KEYS:
        path = f"root.controls.{key}"
        value = controls[key]
        if not isinstance(value, dict):
            fail(f"{path}: expected object")
        if value.get("state") == "present":
            row = exact_keys(
                value, {"state", "claim_node_ids", "provenance_kind", "fixed_before_phi"}, path
            )
            ids = expect_list(row["claim_node_ids"], f"{path}.claim_node_ids")
            if not ids:
                fail(f"{path}.claim_node_ids: must not be empty")
            for i, node_id in enumerate(ids):
                expect_string(node_id, f"{path}.claim_node_ids[{i}]")
                if node_id not in nodes:
                    fail(f"{path}.claim_node_ids[{i}]: unknown ClaimIR node")
            if len(ids) != len(set(ids)):
                fail(f"{path}.claim_node_ids: duplicate node")
            if row["provenance_kind"] not in CONTROL_PROVENANCE:
                fail(f"{path}.provenance_kind: unexpected value")
            if expect_bool(row["fixed_before_phi"], f"{path}.fixed_before_phi") is not True:
                fail(f"{path}.fixed_before_phi: must be true")
        else:
            exact_keys(value, {"state"}, path)
            if value["state"] not in ABSENCE_STATES:
                fail(f"{path}.state: unexpected value")

    temporal = exact_keys(root["temporal"], {*TEMPORAL_KEYS, "ordering"}, "root.temporal")
    for key in TEMPORAL_KEYS:
        validate_state(temporal[key], spans, f"root.temporal.{key}")
    for i, item in enumerate(expect_list(temporal["ordering"], "root.temporal.ordering")):
        path = f"root.temporal.ordering[{i}]"
        row = exact_keys(item, {"before_coordinate_id", "after_coordinate_id", "source_span_ids"}, path)
        before = expect_string(row["before_coordinate_id"], f"{path}.before_coordinate_id")
        after = expect_string(row["after_coordinate_id"], f"{path}.after_coordinate_id")
        if before not in seen_coords or after not in seen_coords:
            fail(f"{path}: unknown coordinate reference")
        validate_span_refs(row["source_span_ids"], spans, f"{path}.source_span_ids")

    approximation = exact_keys(root["approximation"], {"mode", *APPROX_KEYS}, "root.approximation")
    if approximation["mode"] not in ANALYSIS_MODES:
        fail("root.approximation.mode: unexpected value")
    for key in APPROX_KEYS:
        validate_state(approximation[key], spans, f"root.approximation.{key}")

    bridge_ids: set[str] = set()
    for i, item in enumerate(expect_list(root["bridge_assumptions"], "root.bridge_assumptions")):
        path = f"root.bridge_assumptions[{i}]"
        row = exact_keys(item, {"assumption_id", "statement", "grounding", "source_span_ids"}, path)
        aid = expect_string(row["assumption_id"], f"{path}.assumption_id")
        if not ID_RE.fullmatch(aid) or aid in bridge_ids:
            fail(f"{path}.assumption_id: invalid or duplicate")
        bridge_ids.add(aid)
        expect_string(row["statement"], f"{path}.statement")
        if row["grounding"] not in RELATION_GROUNDING:
            fail(f"{path}.grounding: unexpected value")
        validate_span_refs(row["source_span_ids"], spans, f"{path}.source_span_ids")

    decision = root["decision"]
    if not isinstance(decision, dict):
        fail("root.decision: expected object")
    if decision.get("status") == "PASS":
        exact_keys(decision, {"status"}, "root.decision")
    elif decision.get("status") == "RESIDUAL":
        row = exact_keys(
            decision,
            {"status", "residual_kind", "failure_layer", "unmet_obligations", "details"},
            "root.decision",
        )
        if row["residual_kind"] not in RESIDUAL_KINDS:
            fail("root.decision.residual_kind: unexpected value")
        if row["failure_layer"] not in FAILURE_LAYERS:
            fail("root.decision.failure_layer: unexpected value")
        unmet = expect_list(row["unmet_obligations"], "root.decision.unmet_obligations")
        if not unmet:
            fail("root.decision.unmet_obligations: must not be empty")
        for i, value in enumerate(unmet):
            expect_string(value, f"root.decision.unmet_obligations[{i}]")
        expect_string(row["details"], "root.decision.details")
    else:
        fail("root.decision.status: expected PASS or RESIDUAL")

    reject_label_leakage(root, claim_ir)
    return root


def state_to_structural(value: dict[str, Any]) -> dict[str, Any]:
    if value["state"] != "present":
        return {"state": value["state"]}
    return {
        "state": "present",
        "value": {"source_refs": [f"source_span:{x}" for x in sorted(value["source_span_ids"])]},
    }


def relation_kind(kind: str) -> str:
    if kind in DIRECT_RELATION_MAP:
        return DIRECT_RELATION_MAP[kind]
    if kind in UNSUPPORTED_TO_OTHER:
        return "other"
    fail(f"unsupported ClaimIR relation kind {kind!r}")


def adjudication_sha256(adjudication: dict[str, Any]) -> str:
    raw = json.dumps(adjudication, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def compile_record(claim_ir: dict[str, Any], adjudication: dict[str, Any]) -> dict[str, Any]:
    validate_adjudication(adjudication, claim_ir)
    nodes = node_map(claim_ir)
    coord_map = {item["claim_node_id"]: item for item in adjudication["coordinate_map"]}

    coordinates = [
        {
            "coordinate_id": coord_map[node_id]["coordinate_id"],
            "role": ROLE_MAP[node["role"]],
            "required": coord_map[node_id]["required"],
            "provenance": {"origin": "claim_ir_node", "ref": node_id},
        }
        for node_id, node in nodes.items()
    ]

    relations = []
    for rel in claim_ir["claim_core"]["relations"]:
        relations.append({
            "relation_id": f"rel.{rel['id']}",
            "kind": relation_kind(rel["kind"]),
            "arguments": [
                {"space": "basis_coordinate", "ref": coord_map[arg]["coordinate_id"]}
                for arg in rel["arguments"]
            ],
            "ordered_arguments": True,
            "grounding": {
                "state": rel["grounding"],
                "source_refs": [f"source_span:{x}" for x in sorted(rel["source_span_ids"])],
            },
            "conditional_on": [],
            "temporal_direction": "forward" if rel["kind"] == "precedes" else "unspecified",
        })

    temporal = {key: state_to_structural(adjudication["temporal"][key]) for key in TEMPORAL_KEYS}
    temporal["ordering"] = [
        {
            "before": {"space": "basis_coordinate", "ref": row["before_coordinate_id"]},
            "after": {"space": "basis_coordinate", "ref": row["after_coordinate_id"]},
        }
        for row in adjudication["temporal"]["ordering"]
    ]

    controls = {}
    for key in CONTROL_KEYS:
        value = adjudication["controls"][key]
        if value["state"] != "present":
            controls[key] = {"state": value["state"]}
            continue
        refs: set[str] = set()
        for node_id in value["claim_node_ids"]:
            refs.update(nodes[node_id]["source_span_ids"])
        controls[key] = {
            "state": "present",
            "value": {
                "identity": f"control.{key}",
                "description": "source-grounded control assignment from preserved ClaimIR nodes",
                "provenance": {
                    "kind": value["provenance_kind"],
                    "source_refs": [f"source_span:{x}" for x in sorted(refs)],
                    "fixed_before_target_analysis": True,
                },
            },
        }

    approximation = {"mode": adjudication["approximation"]["mode"]}
    for key in APPROX_KEYS:
        approximation[key] = state_to_structural(adjudication["approximation"][key])

    bridges = [
        {
            "assumption_id": row["assumption_id"],
            "statement": row["statement"],
            "grounding": row["grounding"],
            "source_refs": [f"source_span:{x}" for x in sorted(row["source_span_ids"])],
        }
        for row in adjudication["bridge_assumptions"]
    ]

    if adjudication["decision"]["status"] == "PASS":
        outcome = {
            "status": "PASS",
            "witness": {
                "schema_version": WITNESS_VERSION,
                "generic_schema_id": SCHEMA_VERSION,
                "theorem_refs": [{"kind": "generic_schema", "ref": "github:#267"}],
                "instantiated_obligation": "complete ClaimIR preservation and source-grounded adjudication under the frozen Paper 2 working basis",
                "verification": {
                    "status": "verified",
                    "checker": "paper2_reference_structural_adjudication.py",
                    "checker_version": SCRIPT_VERSION,
                    "kernel": "deterministic-python-contract",
                    "evidence_ref": f"sha256:{adjudication_sha256(adjudication)}",
                },
            },
        }
    else:
        decision = adjudication["decision"]
        outcome = {
            "status": "RESIDUAL",
            "residual": {
                "taxonomy_version": RESIDUAL_VERSION,
                "residual_kind": decision["residual_kind"],
                "failure_layer": decision["failure_layer"],
                "unmet_obligations": decision["unmet_obligations"],
                "details": decision["details"],
            },
            "witness_attempts": [],
        }

    claim_raw = json.dumps(claim_ir, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    record = {
        "schema_version": STRUCTURAL_VERSION,
        "contract_versions": {
            "structural_signature": STRUCTURAL_VERSION,
            "claim_ir": CLAIM_IR_VERSION,
            "basis": BASIS_VERSION,
            "witness_ref": WITNESS_VERSION,
            "residual_taxonomy": RESIDUAL_VERSION,
        },
        "paper": {
            "paper_id": claim_ir["provenance"]["paper_id"],
            "source_identity": {
                "stable_id": claim_ir["provenance"]["paper_id"],
                "version": f"sha256:{hashlib.sha256(claim_raw).hexdigest()}",
                "kind": "source_grounded_claim_ir",
            },
            "claims": [{
                "claim_id": claim_ir["claim_id"],
                "source_span_ids": [row["span_id"] for row in claim_ir["provenance"]["source_spans"]],
                "source_construct_labels": claim_ir["provenance"]["construct_labels"],
                "claim_ir_records": [{
                    "ir_id": "ir.primary",
                    "claim_ir": copy.deepcopy(claim_ir),
                    "decomposition_attempts": [{
                        "attempt_id": "attempt.primary",
                        "analysis_identity": {
                            "blinded_claim_id": claim_ir["claim_id"],
                            "analysis_labels": [],
                            "analyzer": {"tool": "paper2_reference_structural_adjudication.py", "version": SCRIPT_VERSION},
                        },
                        "basis_instantiation": {"coordinates": coordinates},
                        "relation_topology": relations,
                        "temporal_structure": temporal,
                        "control_surface": controls,
                        "approximation_uncertainty": approximation,
                        "bridge_assumptions": bridges,
                        "derived_macros": [],
                        "outcome": outcome,
                    }],
                }],
            }],
        },
    }
    validate_structural_signature(record)
    return record


def verify_compiled_record(claim_ir: dict[str, Any], adjudication: dict[str, Any], record: dict[str, Any]) -> None:
    expected = compile_record(claim_ir, adjudication)
    validate_structural_signature(record)
    if record != expected:
        fail("compiled structural record differs from deterministic reference compilation")


def expect_invalid(fn, label: str) -> None:
    try:
        fn()
    except Exception:
        return
    raise AssertionError(f"{label}: unexpectedly accepted")


def self_test(claim_path: Path, adjudication_path: Path) -> None:
    claim = json.loads(claim_path.read_text(encoding="utf-8"))
    adj = json.loads(adjudication_path.read_text(encoding="utf-8"))
    record = compile_record(claim, adj)
    verify_compiled_record(claim, adj, record)
    ir1 = record["paper"]["claims"][0]["claim_ir_records"][0]
    assert ir1["decomposition_attempts"][0]["outcome"]["status"] == "PASS"

    bad = copy.deepcopy(record)
    bad["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]["basis_instantiation"]["coordinates"].pop()
    expect_invalid(lambda: verify_compiled_record(claim, adj, bad), "dropped ClaimIR node")

    bad = copy.deepcopy(record)
    bad["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]["relation_topology"].pop()
    expect_invalid(lambda: verify_compiled_record(claim, adj, bad), "dropped ClaimIR relation")

    bad_adj = copy.deepcopy(adj)
    bad_adj["controls"]["probe_P"] = {
        "state": "present", "claim_node_ids": ["missing_node"],
        "provenance_kind": "source_declared", "fixed_before_phi": True,
    }
    expect_invalid(lambda: validate_adjudication(bad_adj, claim), "fabricated control")

    bad_adj = copy.deepcopy(adj)
    first_node = claim["claim_core"]["nodes"][0]["id"]
    bad_adj["controls"]["probe_P"] = {
        "state": "present", "claim_node_ids": [first_node],
        "provenance_kind": "source_declared", "fixed_before_phi": False,
    }
    expect_invalid(lambda: validate_adjudication(bad_adj, claim), "post-hoc control")

    bad_adj = copy.deepcopy(adj)
    bad_adj["bridge_assumptions"] = [{
        "assumption_id": "bridge.leak",
        "statement": claim["provenance"]["construct_labels"][0],
        "grounding": "normalized",
        "source_span_ids": [claim["provenance"]["source_spans"][0]["span_id"]],
    }]
    expect_invalid(lambda: validate_adjudication(bad_adj, claim), "construct-label leakage")

    unsupported_claim = copy.deepcopy(claim)
    unsupported_claim["claim_core"]["relations"][0]["kind"] = "predicts"
    unsupported = compile_record(unsupported_claim, adj)
    uattempt = unsupported["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
    assert uattempt["relation_topology"][0]["kind"] == "other"
    bad = copy.deepcopy(unsupported)
    bad["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]["relation_topology"][0]["kind"] = "maps_to"
    expect_invalid(lambda: verify_compiled_record(unsupported_claim, adj, bad), "semantic strengthening")

    renamed_claim = copy.deepcopy(claim)
    renames = {row["id"]: f"renamed_{i}" for i, row in enumerate(renamed_claim["claim_core"]["nodes"], 1)}
    for node in renamed_claim["claim_core"]["nodes"]:
        node["id"] = renames[node["id"]]
    for rel in renamed_claim["claim_core"]["relations"]:
        rel["arguments"] = [renames[arg] for arg in rel["arguments"]]
    renamed_adj = copy.deepcopy(adj)
    for row in renamed_adj["coordinate_map"]:
        row["claim_node_id"] = renames[row["claim_node_id"]]
    for control in renamed_adj["controls"].values():
        if control["state"] == "present":
            control["claim_node_ids"] = [renames[x] for x in control["claim_node_ids"]]
    renamed_record = compile_record(renamed_claim, renamed_adj)
    ir2 = renamed_record["paper"]["claims"][0]["claim_ir_records"][0]
    assert structural_digest(ir1["decomposition_attempts"][0], ir1["claim_ir"]) == structural_digest(
        ir2["decomposition_attempts"][0], ir2["claim_ir"]
    )

    residual_adj = copy.deepcopy(adj)
    residual_adj["decision"] = {
        "status": "RESIDUAL",
        "residual_kind": "witness_failure",
        "failure_layer": "witness",
        "unmet_obligations": ["synthetic residual fixture"],
        "details": "synthetic residual remains explicit",
    }
    residual_record = compile_record(claim, residual_adj)
    project_first(residual_record)

    print("PAPER2_REFERENCE_STRUCTURAL_ADJUDICATION_V1_SELFTEST_PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim-ir", type=Path)
    parser.add_argument("--adjudication", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--example-claim", type=Path, default=Path("research/paper2/claim_ir_v1.example.json"))
    parser.add_argument(
        "--example-adjudication",
        type=Path,
        default=Path("research/paper2/reference_structural_adjudication_v1.example.json"),
    )
    args = parser.parse_args()

    if args.self_test:
        self_test(args.example_claim, args.example_adjudication)
        return
    if args.claim_ir is None or args.adjudication is None:
        parser.error("--claim-ir and --adjudication are required unless --self-test is used")

    claim = json.loads(args.claim_ir.read_text(encoding="utf-8"))
    adjudication = json.loads(args.adjudication.read_text(encoding="utf-8"))
    record = compile_record(claim, adjudication)
    payload = json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
