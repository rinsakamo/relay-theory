#!/usr/bin/env python3
"""Paper 2 Phi structural projection and comparison.

Owner: #225.
This compares frozen Paper 2 structural form, not full semantic identity.
"""

from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from paper2_structural_signature_contract import validate as validate_structural_signature
from paper2_structural_signature_constants import WORKING_BASIS_VERSION

PHI_VERSION = "paper2-phi-object-v1"
COMPARISON_VERSION = "paper2-phi-comparison-v1"
MAX_SEARCH_STATES = 100_000

BOTTOM = "not_required"
NON_ACTIVE = {"not_required", "not_applicable"}

ROLE_AXIS = {
    "state_or_structure": "S",
    "information": "O",
    "intervention": "P",
    "response_or_outcome": "O",
    "criterion": "Q",
    "probe": "P",
    "partition": "Pi",
    "resource": "C",
    "temporal": "T",
    "relation": "K",
}
CONTROL_AXIS = {
    "probe_P": "P",
    "criterion_Q": "Q",
    "partition_Pi": "Pi",
    "resource_C": "C",
}
SCOPE_KEYS = ("conditions", "population", "substrate", "task", "temporal_scope")
TEMPORAL_STATE_KEYS = ("time_index", "history_window", "future_horizon", "recurrence", "persistence")
APPROX_STATE_KEYS = ("threshold", "tolerance", "confidence", "loss", "comparison_criterion")


class PhiError(ValueError):
    pass


class ComparisonUnderdetermined(RuntimeError):
    pass


def _canon(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _state_shape(value: dict[str, Any]) -> dict[str, Any]:
    state = value["state"]
    if state == "present":
        return {"state": "present"}
    return {"state": state}


def _control_shape(value: dict[str, Any]) -> dict[str, Any]:
    state = value["state"]
    if state != "present":
        return {"state": state}
    return {
        "state": "present",
        "provenance_kind": value["value"]["provenance"]["kind"],
    }


def _ref_key(ref: dict[str, Any]) -> str:
    space = ref["space"]
    raw = ref["ref"]
    if space == "basis_coordinate":
        return f"basis:{raw}"
    if space == "claim_ir_node":
        return f"claim_node:{raw}"
    if space == "claim_ir_relation":
        return f"claim_relation:{raw}"
    raise PhiError(f"unexpected reference space {space!r}")


def project_first(data: dict[str, Any]) -> dict[str, Any]:
    validate_structural_signature(data)
    if data["contract_versions"]["basis"] != WORKING_BASIS_VERSION:
        raise PhiError(
            f"Phi v1 requires {WORKING_BASIS_VERSION!r}; "
            f"got {data['contract_versions']['basis']!r}"
        )

    claim = data["paper"]["claims"][0]
    ir_record = claim["claim_ir_records"][0]
    claim_ir = ir_record["claim_ir"]
    attempt = ir_record["decomposition_attempts"][0]

    # Working-basis Phi uses no analysis-label side channel.
    if attempt["analysis_identity"]["analysis_labels"]:
        raise PhiError("analysis_labels must be empty for working-basis Phi projection")

    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    active_axes: set[str] = set()

    core = claim_ir["claim_core"]

    for node in core["nodes"]:
        key = f"claim_node:{node['id']}"
        nodes[key] = {
            "space": "claim_ir_node",
            "role": node["role"],
            "grounding": node["grounding"],
        }

    for rel in core["relations"]:
        rkey = f"claim_relation:{rel['id']}"
        nodes[rkey] = {
            "space": "claim_ir_relation",
            "kind": rel["kind"],
            "grounding": rel["grounding"],
        }
        edges.append({
            "family": "claim_ir_relation",
            "kind": rel["kind"],
            "ordered_arguments": True,
            "arguments": [f"claim_node:{arg}" for arg in rel["arguments"]],
            "conditional_on": [],
            "temporal_direction": "unspecified",
            "grounding": rel["grounding"],
        })

    for coord in attempt["basis_instantiation"]["coordinates"]:
        key = f"basis:{coord['coordinate_id']}"
        role = coord["role"]
        axis = ROLE_AXIS.get(role)
        if axis:
            active_axes.add(axis)
        nodes[key] = {
            "space": "basis_coordinate",
            "role": role,
            "required": coord["required"],
            "provenance_origin": coord["provenance"]["origin"],
            "axis": axis,
        }
        origin = coord["provenance"]["origin"]
        if origin in {"claim_ir_node", "claim_ir_relation"}:
            target_space = "claim_ir_node" if origin == "claim_ir_node" else "claim_ir_relation"
            target = (
                f"claim_node:{coord['provenance']['ref']}"
                if target_space == "claim_ir_node"
                else f"claim_relation:{coord['provenance']['ref']}"
            )
            edges.append({
                "family": "coordinate_grounding",
                "kind": origin,
                "ordered_arguments": True,
                "arguments": [key, target],
                "conditional_on": [],
                "temporal_direction": "atemporal",
                "grounding": origin,
            })

    for rel in attempt["relation_topology"]:
        active_axes.add("K")
        edges.append({
            "family": "basis_relation",
            "kind": rel["kind"],
            "ordered_arguments": rel["ordered_arguments"],
            "arguments": [_ref_key(ref) for ref in rel["arguments"]],
            "conditional_on": sorted(_ref_key(ref) for ref in rel["conditional_on"]),
            "temporal_direction": rel["temporal_direction"],
            "grounding": rel["grounding"]["state"],
        })

    temporal = attempt["temporal_structure"]
    temporal_shape = {key: _state_shape(temporal[key]) for key in TEMPORAL_STATE_KEYS}
    for key in TEMPORAL_STATE_KEYS:
        if temporal[key]["state"] not in NON_ACTIVE:
            active_axes.add("T")
    for item in temporal["ordering"]:
        active_axes.add("T")
        edges.append({
            "family": "temporal_order",
            "kind": "precedes",
            "ordered_arguments": True,
            "arguments": [_ref_key(item["before"]), _ref_key(item["after"])],
            "conditional_on": [],
            "temporal_direction": "forward",
            "grounding": "structural_signature",
        })

    controls = {}
    for key, value in attempt["control_surface"].items():
        controls[key] = _control_shape(value)
        if value["state"] not in NON_ACTIVE:
            active_axes.add(CONTROL_AXIS[key])

    approx = attempt["approximation_uncertainty"]
    approximation = {
        "mode": approx["mode"],
        **{key: _state_shape(approx[key]) for key in APPROX_STATE_KEYS},
    }

    bridges = sorted(item["grounding"] for item in attempt["bridge_assumptions"])

    return {
        "schema_version": PHI_VERSION,
        "basis_version": WORKING_BASIS_VERSION,
        "claim_type": core["claim_type"],
        "modality": core["modality"],
        "scope_shape": {key: bool(core["scope"][key]) for key in SCOPE_KEYS},
        "active_axes": sorted(active_axes),
        "nodes": nodes,
        "edges": edges,
        "temporal": temporal_shape,
        "controls": controls,
        "approximation": approximation,
        "bridges": bridges,
    }


def _node_label(node: dict[str, Any]) -> str:
    return _canon(node)


def _edge_under_mapping(edge: dict[str, Any], mapping: dict[str, str]) -> str:
    args = [mapping[x] for x in edge["arguments"]]
    if not edge["ordered_arguments"]:
        args = sorted(args)
    cond = sorted(mapping[x] for x in edge["conditional_on"])
    projected = {
        "family": edge["family"],
        "kind": edge["kind"],
        "ordered_arguments": edge["ordered_arguments"],
        "arguments": args,
        "conditional_on": cond,
        "temporal_direction": edge["temporal_direction"],
        "grounding": edge["grounding"],
    }
    return _canon(projected)


def _edge_counter(obj: dict[str, Any]) -> Counter[str]:
    identity = {key: key for key in obj["nodes"]}
    return Counter(_edge_under_mapping(edge, identity) for edge in obj["edges"])


def _state_leq(a: dict[str, Any], b: dict[str, Any], *, exact: bool) -> bool:
    if exact:
        return a == b
    if a["state"] == BOTTOM:
        return True
    return a == b


def _multiset_leq(a: list[str], b: list[str]) -> bool:
    ca, cb = Counter(a), Counter(b)
    return all(cb[k] >= v for k, v in ca.items())


def _scalar_leq(a: dict[str, Any], b: dict[str, Any], *, exact: bool) -> bool:
    for key in ("claim_type", "modality", "scope_shape"):
        if a[key] != b[key]:
            return False
    if a["approximation"]["mode"] != b["approximation"]["mode"]:
        return False

    aa, ba = set(a["active_axes"]), set(b["active_axes"])
    if exact:
        if aa != ba:
            return False
    elif not aa <= ba:
        return False

    for key in TEMPORAL_STATE_KEYS:
        if not _state_leq(a["temporal"][key], b["temporal"][key], exact=exact):
            return False

    for key in CONTROL_AXIS:
        if not _state_leq(a["controls"][key], b["controls"][key], exact=exact):
            return False

    for key in APPROX_STATE_KEYS:
        if not _state_leq(a["approximation"][key], b["approximation"][key], exact=exact):
            return False

    if exact:
        return Counter(a["bridges"]) == Counter(b["bridges"])
    return _multiset_leq(a["bridges"], b["bridges"])


@dataclass
class EmbeddingResult:
    mapping: dict[str, str]
    search_states: int


def _find_embedding(a: dict[str, Any], b: dict[str, Any], *, exact: bool) -> EmbeddingResult | None:
    if not _scalar_leq(a, b, exact=exact):
        return None
    if exact and len(a["nodes"]) != len(b["nodes"]):
        return None
    if len(a["nodes"]) > len(b["nodes"]):
        return None

    b_by_label: dict[str, list[str]] = {}
    for bid, bnode in b["nodes"].items():
        b_by_label.setdefault(_node_label(bnode), []).append(bid)

    candidates: dict[str, list[str]] = {}
    for aid, anode in a["nodes"].items():
        opts = list(b_by_label.get(_node_label(anode), []))
        if not opts:
            return None
        candidates[aid] = opts

    order = sorted(a["nodes"], key=lambda x: (len(candidates[x]), _node_label(a["nodes"][x]), x))
    b_edges = _edge_counter(b)
    search_states = 0

    def edges_fit_partial(mapping: dict[str, str]) -> bool:
        # Only test edges whose referenced nodes are all mapped.
        partial_counter: Counter[str] = Counter()
        for edge in a["edges"]:
            refs = edge["arguments"] + edge["conditional_on"]
            if all(ref in mapping for ref in refs):
                partial_counter[_edge_under_mapping(edge, mapping)] += 1
        return all(b_edges[k] >= v for k, v in partial_counter.items())

    def rec(i: int, mapping: dict[str, str], used: set[str]) -> dict[str, str] | None:
        nonlocal search_states
        search_states += 1
        if search_states > MAX_SEARCH_STATES:
            raise ComparisonUnderdetermined(
                f"embedding search exceeded {MAX_SEARCH_STATES} states"
            )
        if i == len(order):
            mapped_edges = Counter(_edge_under_mapping(edge, mapping) for edge in a["edges"])
            if exact:
                if mapped_edges != b_edges:
                    return None
            else:
                if any(b_edges[k] < v for k, v in mapped_edges.items()):
                    return None
            return dict(mapping)

        aid = order[i]
        for bid in sorted(candidates[aid]):
            if bid in used:
                continue
            mapping[aid] = bid
            used.add(bid)
            if edges_fit_partial(mapping):
                found = rec(i + 1, mapping, used)
                if found is not None:
                    return found
            used.remove(bid)
            del mapping[aid]
        return None

    mapping = rec(0, {}, set())
    if mapping is None:
        return None
    return EmbeddingResult(mapping=mapping, search_states=search_states)


def _counter_difference(big: Counter[str], small: Counter[str]) -> list[str]:
    out: list[str] = []
    for key in sorted(big):
        n = big[key] - small.get(key, 0)
        out.extend([key] * max(0, n))
    return out


def _forgetting_witness(weaker: dict[str, Any], stronger: dict[str, Any], emb: EmbeddingResult) -> dict[str, Any]:
    image = set(emb.mapping.values())
    stronger_edges = _edge_counter(stronger)
    mapped_weaker_edges = Counter(
        _edge_under_mapping(edge, emb.mapping) for edge in weaker["edges"]
    )

    controls = {}
    for key in CONTROL_AXIS:
        if weaker["controls"][key] != stronger["controls"][key]:
            controls[key] = {
                "weaker": weaker["controls"][key],
                "stronger": stronger["controls"][key],
            }

    temporal = {}
    for key in TEMPORAL_STATE_KEYS:
        if weaker["temporal"][key] != stronger["temporal"][key]:
            temporal[key] = {
                "weaker": weaker["temporal"][key],
                "stronger": stronger["temporal"][key],
            }

    approx = {}
    for key in APPROX_STATE_KEYS:
        if weaker["approximation"][key] != stronger["approximation"][key]:
            approx[key] = {
                "weaker": weaker["approximation"][key],
                "stronger": stronger["approximation"][key],
            }

    bridge_diff = list((Counter(stronger["bridges"]) - Counter(weaker["bridges"])).elements())

    return {
        "mapping": dict(sorted(emb.mapping.items())),
        "forgotten_nodes": sorted(set(stronger["nodes"]) - image),
        "forgotten_relations": _counter_difference(stronger_edges, mapped_weaker_edges),
        "forgotten_axes": sorted(set(stronger["active_axes"]) - set(weaker["active_axes"])),
        "forgotten_controls": controls,
        "forgotten_temporal_states": temporal,
        "forgotten_approximation_states": approx,
        "forgotten_bridge_slots": sorted(bridge_diff),
    }


def compare_phi(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    if a["schema_version"] != PHI_VERSION or b["schema_version"] != PHI_VERSION:
        raise PhiError("unsupported Phi object version")
    if a["basis_version"] != WORKING_BASIS_VERSION or b["basis_version"] != WORKING_BASIS_VERSION:
        raise PhiError("basis-version mismatch")

    iso = _find_embedding(a, b, exact=True)
    if iso is not None:
        return {
            "comparison_version": COMPARISON_VERSION,
            "relation": "EQUIVALENT",
            "semantic_identity_claim": False,
            "left_to_right_isomorphism": dict(sorted(iso.mapping.items())),
        }

    ab = _find_embedding(a, b, exact=False)
    ba = _find_embedding(b, a, exact=False)

    if ab is not None and ba is None:
        return {
            "comparison_version": COMPARISON_VERSION,
            "relation": "RIGHT_STRICT_REFINEMENT_OF_LEFT",
            "forgetting_map_right_to_left": _forgetting_witness(a, b, ab),
        }
    if ba is not None and ab is None:
        return {
            "comparison_version": COMPARISON_VERSION,
            "relation": "LEFT_STRICT_REFINEMENT_OF_RIGHT",
            "forgetting_map_left_to_right": _forgetting_witness(b, a, ba),
        }
    if ab is not None and ba is not None:
        return {
            "comparison_version": COMPARISON_VERSION,
            "relation": "MUTUAL_EMBEDDABILITY_NONISOMORPHIC",
        }
    return {
        "comparison_version": COMPARISON_VERSION,
        "relation": "INCOMPARABLE",
    }


def _load_working_example(example_path: Path) -> dict[str, Any]:
    data = json.loads(example_path.read_text(encoding="utf-8"))
    data["contract_versions"]["basis"] = WORKING_BASIS_VERSION
    return data


def _rename_presentation(data: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(data)
    claim = out["paper"]["claims"][0]
    ir = claim["claim_ir_records"][0]
    claim_ir = ir["claim_ir"]
    attempt = ir["decomposition_attempts"][0]

    node_map = {
        claim_ir["claim_core"]["nodes"][0]["id"]: "renamed_node_a",
        claim_ir["claim_core"]["nodes"][1]["id"]: "renamed_node_b",
    }
    for node in claim_ir["claim_core"]["nodes"]:
        node["id"] = node_map[node["id"]]

    rel = claim_ir["claim_core"]["relations"][0]
    old_rel_id = rel["id"]
    rel["id"] = "renamed_claim_relation"
    rel["arguments"] = [node_map[x] for x in rel["arguments"]]

    coord_map = {}
    for i, coord in enumerate(attempt["basis_instantiation"]["coordinates"]):
        old = coord["coordinate_id"]
        new = f"renamed_coord_{i}"
        coord_map[old] = new
        coord["coordinate_id"] = new
        origin = coord["provenance"]["origin"]
        if origin == "claim_ir_node":
            coord["provenance"]["ref"] = node_map[coord["provenance"]["ref"]]
        elif origin == "claim_ir_relation" and coord["provenance"]["ref"] == old_rel_id:
            coord["provenance"]["ref"] = "renamed_claim_relation"

    for brel in attempt["relation_topology"]:
        brel["relation_id"] = "renamed_basis_relation"
        for ref in brel["arguments"] + brel["conditional_on"]:
            if ref["space"] == "basis_coordinate":
                ref["ref"] = coord_map[ref["ref"]]
            elif ref["space"] == "claim_ir_node":
                ref["ref"] = node_map[ref["ref"]]
            elif ref["space"] == "claim_ir_relation" and ref["ref"] == old_rel_id:
                ref["ref"] = "renamed_claim_relation"

    for order in attempt["temporal_structure"]["ordering"]:
        for side in ("before", "after"):
            ref = order[side]
            if ref["space"] == "basis_coordinate":
                ref["ref"] = coord_map[ref["ref"]]
            elif ref["space"] == "claim_ir_node":
                ref["ref"] = node_map[ref["ref"]]

    for macro in attempt["derived_macros"]:
        macro["expansion"]["coordinate_ids"] = [coord_map[x] for x in macro["expansion"]["coordinate_ids"]]
        macro["expansion"]["relation_ids"] = ["renamed_basis_relation" for _ in macro["expansion"]["relation_ids"]]
    attempt["attempt_id"] = "renamed_attempt"
    ir["ir_id"] = "renamed_ir"
    return out


def self_test(example_path: Path) -> None:
    base = _load_working_example(example_path)
    validate_structural_signature(base)
    phi_base = project_first(base)

    # 1. Same inventory, different topology must not be equivalent.
    topo = copy.deepcopy(base)
    topo["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]["relation_topology"][0]["kind"] = "maps_to"
    validate_structural_signature(topo)
    assert compare_phi(phi_base, project_first(topo))["relation"] == "INCOMPARABLE"

    # 2. Different source construct labels, same structure => equivalent.
    diff_label = copy.deepcopy(base)
    diff_label["paper"]["claims"][0]["source_construct_labels"] = ["learning"]
    diff_label["paper"]["claims"][0]["claim_ir_records"][0]["claim_ir"]["provenance"]["construct_labels"] = ["learning"]
    validate_structural_signature(diff_label)
    assert compare_phi(phi_base, project_first(diff_label))["relation"] == "EQUIVALENT"

    # 3. Same source construct label, different structure => not equivalent.
    same_label_diff = copy.deepcopy(topo)
    assert same_label_diff["paper"]["claims"][0]["source_construct_labels"] == base["paper"]["claims"][0]["source_construct_labels"]
    assert compare_phi(phi_base, project_first(same_label_diff))["relation"] == "INCOMPARABLE"

    # 4. Strict refinement by independently fixed resource criterion.
    refined = copy.deepcopy(base)
    refined_attempt = refined["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
    refined_attempt["control_surface"]["resource_C"] = {
        "state": "present",
        "value": {
            "identity": "fixture:resource:fixed",
            "description": "predeclared synthetic resource bound",
            "provenance": {
                "kind": "synthetic_fixture",
                "source_refs": ["fixture:resource:fixed"],
                "fixed_before_target_analysis": True,
            },
        },
    }
    validate_structural_signature(refined)
    cmp_refined = compare_phi(phi_base, project_first(refined))
    assert cmp_refined["relation"] == "RIGHT_STRICT_REFINEMENT_OF_LEFT"
    assert "C" in cmp_refined["forgetting_map_right_to_left"]["forgotten_axes"]

    # 5. Forgetting witness must identify the added resource surface.
    assert "resource_C" in cmp_refined["forgetting_map_right_to_left"]["forgotten_controls"]

    # 6. Answer-bearing side channel is rejected before comparison.
    trap = copy.deepcopy(base)
    trap["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]["analysis_identity"]["analysis_labels"] = ["desired_target_cluster"]
    validate_structural_signature(trap)
    try:
        project_first(trap)
    except PhiError:
        pass
    else:
        raise AssertionError("answer-bearing analysis label unexpectedly entered Phi")

    # 7. Presentation permutation must preserve equivalence.
    renamed = _rename_presentation(base)
    validate_structural_signature(renamed)
    assert compare_phi(phi_base, project_first(renamed))["relation"] == "EQUIVALENT"

    # 8. Incomparable independent additions must remain incomparable.
    left = copy.deepcopy(base)
    left_a = left["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
    left_a["control_surface"]["resource_C"] = {
        "state": "present",
        "value": {
            "identity": "fixture:resource:left",
            "description": "predeclared left resource bound",
            "provenance": {
                "kind": "synthetic_fixture",
                "source_refs": ["fixture:resource:left"],
                "fixed_before_target_analysis": True,
            },
        },
    }
    right = copy.deepcopy(base)
    right_a = right["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
    right_a["temporal_structure"]["recurrence"] = {"state": "present", "value": "recurrent"}
    validate_structural_signature(left)
    validate_structural_signature(right)
    assert compare_phi(project_first(left), project_first(right))["relation"] == "INCOMPARABLE"

    print("PAPER2_PHI_COMPARISON_V1_SELFTEST_PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--left", type=Path)
    parser.add_argument("--right", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--example",
        type=Path,
        default=Path("research/paper2/structural_signature_v1.example.json"),
    )
    args = parser.parse_args()

    if args.self_test:
        self_test(args.example)
        return

    if not args.left or not args.right:
        parser.error("--left and --right are required unless --self-test is used")

    left = json.loads(args.left.read_text(encoding="utf-8"))
    right = json.loads(args.right.read_text(encoding="utf-8"))
    result = compare_phi(project_first(left), project_first(right))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
