"""Basis instantiation and relation-topology validation for Paper 2 #142."""

from __future__ import annotations

from typing import Any

from paper2_structural_signature_contract_core import *


def validate_basis_and_relations(attempt: dict[str, Any], claim_ir: dict[str, Any], context: str) -> tuple[set[str], set[str], set[str], set[str]]:
    claim_node_ids = {node["id"] for node in claim_ir["claim_core"]["nodes"]}
    claim_relation_ids = {rel["id"] for rel in claim_ir["claim_core"]["relations"]}

    basis = expect_object(attempt["basis_instantiation"], f"{context}.basis_instantiation")
    exact_keys(basis, BASIS_KEYS, f"{context}.basis_instantiation")
    coordinates = expect_list(basis["coordinates"], f"{context}.basis_instantiation.coordinates")
    if not coordinates:
        fail(f"{context}.basis_instantiation.coordinates: must not be empty")
    basis_ids: set[str] = set()
    for index, coord_value in enumerate(coordinates):
        cpath = f"{context}.basis_instantiation.coordinates[{index}]"
        coord = expect_object(coord_value, cpath)
        exact_keys(coord, COORDINATE_KEYS, cpath)
        cid = expect_string(coord["coordinate_id"], f"{cpath}.coordinate_id")
        if not ID_RE.fullmatch(cid):
            fail(f"{cpath}.coordinate_id: invalid identifier")
        if cid in basis_ids:
            fail(f"{cpath}.coordinate_id: duplicate")
        basis_ids.add(cid)
        if coord["role"] not in BASIS_ROLES:
            fail(f"{cpath}.role: unexpected value")
        expect_bool(coord["required"], f"{cpath}.required")
        prov = expect_object(coord["provenance"], f"{cpath}.provenance")
        exact_keys(prov, COORD_PROV_KEYS, f"{cpath}.provenance")
        if prov["origin"] not in COORDINATE_ORIGINS:
            fail(f"{cpath}.provenance.origin: unexpected value")
        ref = expect_string(prov["ref"], f"{cpath}.provenance.ref")
        if prov["origin"] == "claim_ir_node" and ref not in claim_node_ids:
            fail(f"{cpath}.provenance.ref: unknown ClaimIR node")
        if prov["origin"] == "claim_ir_relation" and ref not in claim_relation_ids:
            fail(f"{cpath}.provenance.ref: unknown ClaimIR relation")

    relation_values = expect_list(attempt["relation_topology"], f"{context}.relation_topology")
    if not relation_values:
        fail(f"{context}.relation_topology: must not be empty; a flat basis-membership bag is not a structural signature")
    relation_ids: set[str] = set()
    for index, rel_value in enumerate(relation_values):
        rpath = f"{context}.relation_topology[{index}]"
        rel = expect_object(rel_value, rpath)
        exact_keys(rel, RELATION_KEYS, rpath)
        rid = expect_string(rel["relation_id"], f"{rpath}.relation_id")
        if not ID_RE.fullmatch(rid):
            fail(f"{rpath}.relation_id: invalid identifier")
        if rid in relation_ids:
            fail(f"{rpath}.relation_id: duplicate")
        relation_ids.add(rid)
        if rel["kind"] not in RELATION_KINDS:
            fail(f"{rpath}.kind: unexpected value")
        args = expect_list(rel["arguments"], f"{rpath}.arguments")
        if not args:
            fail(f"{rpath}.arguments: must not be empty")
        for arg_index, ref in enumerate(args):
            validate_ref(
                ref,
                f"{rpath}.arguments[{arg_index}]",
                basis_ids=basis_ids,
                node_ids=claim_node_ids,
                relation_ids=claim_relation_ids,
            )
        expect_bool(rel["ordered_arguments"], f"{rpath}.ordered_arguments")
        grounding = expect_object(rel["grounding"], f"{rpath}.grounding")
        exact_keys(grounding, REL_GROUND_KEYS, f"{rpath}.grounding")
        if grounding["state"] not in RELATION_GROUNDING:
            fail(f"{rpath}.grounding.state: unexpected value")
        unique_strings(grounding["source_refs"], f"{rpath}.grounding.source_refs", nonempty=True)
        conditions = expect_list(rel["conditional_on"], f"{rpath}.conditional_on")
        for cond_index, ref in enumerate(conditions):
            validate_ref(
                ref,
                f"{rpath}.conditional_on[{cond_index}]",
                basis_ids=basis_ids,
                node_ids=claim_node_ids,
                relation_ids=claim_relation_ids,
            )
        if rel["temporal_direction"] not in TEMPORAL_DIRECTIONS:
            fail(f"{rpath}.temporal_direction: unexpected value")
    return basis_ids, relation_ids, claim_node_ids, claim_relation_ids
