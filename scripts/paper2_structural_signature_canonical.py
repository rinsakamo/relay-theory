"""Canonical structural identity and replay helpers for Paper 2 #142."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

from paper2_claim_ir_validate import normalize_text, validate as validate_claim_ir
from paper2_structural_signature_contract import (
    CONTROL_KEYS, PRESENT_STATE, SCHEMA_VERSION, normalize_source_ref, validate,
)

# ----- Canonical structural identity -----


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _claim_ir_node_signature(node: dict[str, Any]) -> tuple[Any, ...]:
    # Mirrors #147 comparator convention: node IDs are presentation tokens.
    return (
        node["role"],
        node["grounding"],
        tuple(sorted(node["source_span_ids"])),
        normalize_text(node["description"]),
    )


def _claim_ir_node_map(claim_ir: dict[str, Any]) -> dict[str, tuple[Any, ...]]:
    return {node["id"]: _claim_ir_node_signature(node) for node in claim_ir["claim_core"]["nodes"]}


def _claim_ir_relation_signature(relation: dict[str, Any], node_map: dict[str, tuple[Any, ...]]) -> tuple[Any, ...]:
    return (
        relation["kind"],
        relation["grounding"],
        tuple(node_map[arg] for arg in relation["arguments"]),
        tuple(sorted(relation["source_span_ids"])),
        normalize_text(relation["description"]),
    )


def _claim_ir_relation_map(claim_ir: dict[str, Any]) -> dict[str, tuple[Any, ...]]:
    node_map = _claim_ir_node_map(claim_ir)
    return {
        rel["id"]: _claim_ir_relation_signature(rel, node_map)
        for rel in claim_ir["claim_core"]["relations"]
    }


def _canon_ref(ref: dict[str, Any], claim_ir: dict[str, Any]) -> Any:
    if ref["space"] == "basis_coordinate":
        return ("basis_coordinate", ref["ref"])
    if ref["space"] == "claim_ir_node":
        return ("claim_ir_node", _claim_ir_node_map(claim_ir)[ref["ref"]])
    if ref["space"] == "claim_ir_relation":
        return ("claim_ir_relation", _claim_ir_relation_map(claim_ir)[ref["ref"]])
    raise AssertionError("validated reference space expected")


def structural_payload(attempt: dict[str, Any], claim_ir: dict[str, Any]) -> dict[str, Any]:
    validate_claim_ir(claim_ir)
    node_map = _claim_ir_node_map(claim_ir)
    rel_map = _claim_ir_relation_map(claim_ir)
    core = claim_ir["claim_core"]
    claim_core_signature = {
        "claim_type": core["claim_type"],
        "modality": core["modality"],
        "scope": {key: sorted(normalize_text(v) for v in values) for key, values in sorted(core["scope"].items())},
        "nodes": sorted((_canonical_json(sig) for sig in node_map.values())),
        "relations": sorted((_canonical_json(sig) for sig in rel_map.values())),
    }

    coordinates = []
    for coord in attempt["basis_instantiation"]["coordinates"]:
        provenance = dict(coord["provenance"])
        if provenance["origin"] == "claim_ir_node":
            provenance["ref"] = node_map[provenance["ref"]]
        elif provenance["origin"] == "claim_ir_relation":
            provenance["ref"] = rel_map[provenance["ref"]]
        else:
            provenance["ref"] = normalize_source_ref(provenance["ref"])
        coordinates.append({
            "coordinate_id": coord["coordinate_id"],
            "role": coord["role"],
            "required": coord["required"],
            "provenance": provenance,
        })
    coordinates.sort(key=lambda item: item["coordinate_id"])

    relations = []
    for relation in attempt["relation_topology"]:
        args = [_canon_ref(ref, claim_ir) for ref in relation["arguments"]]
        if not relation["ordered_arguments"]:
            args = sorted(args, key=_canonical_json)
        conditions = sorted((_canon_ref(ref, claim_ir) for ref in relation["conditional_on"]), key=_canonical_json)
        relations.append({
            "kind": relation["kind"],
            "arguments": args,
            "ordered_arguments": relation["ordered_arguments"],
            "grounding": {
                "state": relation["grounding"]["state"],
                "source_refs": sorted(normalize_source_ref(v) for v in relation["grounding"]["source_refs"]),
            },
            "conditional_on": conditions,
            "temporal_direction": relation["temporal_direction"],
        })
    relations.sort(key=_canonical_json)

    temporal = copy.deepcopy(attempt["temporal_structure"])
    temporal["ordering"] = sorted(
        (
            {"before": _canon_ref(item["before"], claim_ir), "after": _canon_ref(item["after"], claim_ir)}
            for item in temporal["ordering"]
        ),
        key=_canonical_json,
    )

    controls = copy.deepcopy(attempt["control_surface"])
    for key in CONTROL_KEYS:
        item = controls[key]
        if item["state"] == PRESENT_STATE:
            item["value"]["provenance"]["source_refs"] = sorted(
                normalize_source_ref(v) for v in item["value"]["provenance"]["source_refs"]
            )

    assumptions = [
        {
            "statement": normalize_text(item["statement"]),
            "grounding": item["grounding"],
            "source_refs": sorted(normalize_source_ref(v) for v in item["source_refs"]),
        }
        for item in attempt["bridge_assumptions"]
    ]
    assumptions.sort(key=_canonical_json)

    # Readability macros, local IDs, analyzer identity, outcome, and witness are
    # intentionally outside the structural identity. Their replayability is
    # validated separately in the full artifact.
    return {
        "claim_ir_structural_signature": claim_core_signature,
        "basis_coordinates": coordinates,
        "relation_topology": relations,
        "temporal_structure": temporal,
        "control_surface": controls,
        "approximation_uncertainty": copy.deepcopy(attempt["approximation_uncertainty"]),
        "bridge_assumptions": assumptions,
    }


def structural_digest(attempt: dict[str, Any], claim_ir: dict[str, Any]) -> str:
    payload = structural_payload(attempt, claim_ir)
    data = (_canonical_json(payload) + "\n").encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def canonical_artifact_bytes(data: dict[str, Any]) -> bytes:
    validate(data)
    out = copy.deepcopy(data)
    out["paper"]["claims"].sort(key=lambda c: c["claim_id"])
    for claim in out["paper"]["claims"]:
        claim["source_span_ids"] = sorted(claim["source_span_ids"])
        claim["source_construct_labels"] = sorted(claim["source_construct_labels"])
        claim["claim_ir_records"].sort(key=lambda ir: ir["ir_id"])
        for ir in claim["claim_ir_records"]:
            ir["decomposition_attempts"].sort(key=lambda a: a["attempt_id"])
            for attempt in ir["decomposition_attempts"]:
                attempt["basis_instantiation"]["coordinates"].sort(key=lambda c: c["coordinate_id"])
                attempt["relation_topology"].sort(key=lambda r: r["relation_id"])
                attempt["bridge_assumptions"].sort(key=lambda a: a["assumption_id"])
                attempt["derived_macros"].sort(key=lambda m: m["label"])
                attempt["analysis_identity"]["analysis_labels"] = sorted(attempt["analysis_identity"]["analysis_labels"])
                for control in attempt["control_surface"].values():
                    if control["state"] == PRESENT_STATE:
                        control["value"]["provenance"]["source_refs"] = sorted(control["value"]["provenance"]["source_refs"])
    return (_canonical_json(out) + "\n").encode("utf-8")
