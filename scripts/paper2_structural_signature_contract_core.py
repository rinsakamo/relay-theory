"""Semantic validator for Paper 2 structural-signature v1."""

from __future__ import annotations

from typing import Any

from paper2_structural_signature_types import *

def validate_versions(root: dict[str, Any]) -> dict[str, str]:
    versions = expect_object(root["contract_versions"], "root.contract_versions")
    exact_keys(versions, VERSION_KEYS, "root.contract_versions")
    for key in VERSION_KEYS:
        expect_string(versions[key], f"root.contract_versions.{key}")
    if root["schema_version"] != SCHEMA_VERSION:
        fail("root.schema_version: unexpected value")
    if versions["structural_signature"] != root["schema_version"]:
        fail("root.contract_versions.structural_signature: must match root.schema_version")
    version_tuple = (
        versions["structural_signature"],
        versions["claim_ir"],
        versions["basis"],
        versions["witness_ref"],
        versions["residual_taxonomy"],
    )
    if version_tuple not in SUPPORTED_VERSION_TUPLES:
        fail(f"root.contract_versions: unsupported version tuple {version_tuple!r}")
    return versions


def validate_ref(ref_value: Any, context: str, *, basis_ids: set[str], node_ids: set[str], relation_ids: set[str]) -> tuple[str, str]:
    ref = expect_object(ref_value, context)
    exact_keys(ref, REF_KEYS, context)
    space = expect_string(ref["space"], f"{context}.space")
    target = expect_string(ref["ref"], f"{context}.ref")
    if space == "basis_coordinate":
        if target not in basis_ids:
            fail(f"{context}.ref: unknown basis coordinate {target!r}")
    elif space == "claim_ir_node":
        if target not in node_ids:
            fail(f"{context}.ref: unknown ClaimIR node {target!r}")
    elif space == "claim_ir_relation":
        if target not in relation_ids:
            fail(f"{context}.ref: unknown ClaimIR relation {target!r}")
    else:
        fail(f"{context}.space: unexpected value")
    return space, target


def validate_control(value: Any, context: str) -> None:
    obj = stateful(value, context)
    if obj["state"] != PRESENT_STATE:
        return
    payload = expect_object(obj["value"], f"{context}.value")
    exact_keys(payload, CONTROL_VALUE_KEYS, f"{context}.value")
    expect_string(payload["identity"], f"{context}.value.identity")
    expect_string(payload["description"], f"{context}.value.description")
    provenance = expect_object(payload["provenance"], f"{context}.value.provenance")
    exact_keys(provenance, CONTROL_PROV_KEYS, f"{context}.value.provenance")
    if provenance["kind"] not in CONTROL_PROVENANCE:
        fail(f"{context}.value.provenance.kind: unexpected value")
    unique_strings(
        provenance["source_refs"],
        f"{context}.value.provenance.source_refs",
        nonempty=True,
    )
    # #134/#136/#138: post-hoc P/Q/Pi selection must not become valid merely
    # because it is serialized as provenance.
    if expect_bool(
        provenance["fixed_before_target_analysis"],
        f"{context}.value.provenance.fixed_before_target_analysis",
    ) is not True:
        fail(f"{context}: present control must be fixed before target analysis")


def validate_witness(value: Any, context: str, *, require_verified: bool) -> dict[str, Any]:
    witness = expect_object(value, context)
    exact_keys(witness, WITNESS_KEYS, context)
    if witness["schema_version"] != WITNESS_REF_VERSION:
        fail(f"{context}.schema_version: unsupported witness-ref version")
    expect_string(witness["generic_schema_id"], f"{context}.generic_schema_id")
    refs = expect_list(witness["theorem_refs"], f"{context}.theorem_refs")
    if not refs:
        fail(f"{context}.theorem_refs: must not be empty")
    for index, ref_value in enumerate(refs):
        ref = expect_object(ref_value, f"{context}.theorem_refs[{index}]")
        exact_keys(ref, THEOREM_REF_KEYS, f"{context}.theorem_refs[{index}]")
        if ref["kind"] not in {"formal_theorem", "generic_schema", "synthetic_schema"}:
            fail(f"{context}.theorem_refs[{index}].kind: unexpected value")
        expect_string(ref["ref"], f"{context}.theorem_refs[{index}].ref")
    expect_string(witness["instantiated_obligation"], f"{context}.instantiated_obligation")
    verification = expect_object(witness["verification"], f"{context}.verification")
    exact_keys(verification, VERIFICATION_KEYS, f"{context}.verification")
    if verification["status"] not in WITNESS_VERIFICATION:
        fail(f"{context}.verification.status: unexpected value")
    for key in ("checker", "checker_version", "kernel", "evidence_ref"):
        expect_string(verification[key], f"{context}.verification.{key}")
    if require_verified and verification["status"] not in {"verified", "synthetic_verified"}:
        fail(f"{context}.verification.status: PASS requires verified witness")
    return witness
