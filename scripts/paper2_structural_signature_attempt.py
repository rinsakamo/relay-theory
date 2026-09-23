"""Per-attempt semantic validation for Paper 2 #142."""

from __future__ import annotations

from typing import Any

from paper2_structural_signature_contract_core import *
from paper2_structural_signature_attempt_structure import validate_basis_and_relations
def validate_attempt(attempt_value: Any, claim_ir: dict[str, Any], source_labels: list[str], versions: dict[str, str], context: str) -> dict[str, Any]:
    attempt = expect_object(attempt_value, context)
    exact_keys(attempt, ATTEMPT_KEYS, context)
    attempt_id = expect_string(attempt["attempt_id"], f"{context}.attempt_id")
    if not ID_RE.fullmatch(attempt_id):
        fail(f"{context}.attempt_id: invalid identifier")

    analysis_identity = expect_object(attempt["analysis_identity"], f"{context}.analysis_identity")
    exact_keys(analysis_identity, ANALYSIS_IDENTITY_KEYS, f"{context}.analysis_identity")
    if analysis_identity["blinded_claim_id"] != claim_ir["claim_id"]:
        fail(f"{context}.analysis_identity.blinded_claim_id: ClaimIR mismatch")
    unique_strings(analysis_identity["analysis_labels"], f"{context}.analysis_identity.analysis_labels")
    analyzer = expect_object(analysis_identity["analyzer"], f"{context}.analysis_identity.analyzer")
    exact_keys(analyzer, ANALYZER_KEYS, f"{context}.analysis_identity.analyzer")
    expect_string(analyzer["tool"], f"{context}.analysis_identity.analyzer.tool")
    expect_string(analyzer["version"], f"{context}.analysis_identity.analyzer.version")

    basis_ids, relation_ids, claim_node_ids, claim_relation_ids = validate_basis_and_relations(attempt, claim_ir, context)

    temporal = expect_object(attempt["temporal_structure"], f"{context}.temporal_structure")
    exact_keys(temporal, TEMPORAL_KEYS, f"{context}.temporal_structure")
    for key in ("time_index", "history_window", "future_horizon", "recurrence", "persistence"):
        stateful(temporal[key], f"{context}.temporal_structure.{key}")
    ordering = expect_list(temporal["ordering"], f"{context}.temporal_structure.ordering")
    for index, item in enumerate(ordering):
        opath = f"{context}.temporal_structure.ordering[{index}]"
        order = expect_object(item, opath)
        exact_keys(order, {"before", "after"}, opath)
        validate_ref(order["before"], f"{opath}.before", basis_ids=basis_ids, node_ids=claim_node_ids, relation_ids=claim_relation_ids)
        validate_ref(order["after"], f"{opath}.after", basis_ids=basis_ids, node_ids=claim_node_ids, relation_ids=claim_relation_ids)

    controls = expect_object(attempt["control_surface"], f"{context}.control_surface")
    exact_keys(controls, CONTROL_KEYS, f"{context}.control_surface")
    for key in CONTROL_KEYS:
        validate_control(controls[key], f"{context}.control_surface.{key}")

    approx = expect_object(attempt["approximation_uncertainty"], f"{context}.approximation_uncertainty")
    exact_keys(approx, APPROX_KEYS, f"{context}.approximation_uncertainty")
    if approx["mode"] not in ANALYSIS_MODES:
        fail(f"{context}.approximation_uncertainty.mode: unexpected value")
    for key in APPROX_KEYS - {"mode"}:
        stateful(approx[key], f"{context}.approximation_uncertainty.{key}")

    assumptions = expect_list(attempt["bridge_assumptions"], f"{context}.bridge_assumptions")
    assumption_ids: set[str] = set()
    for index, item in enumerate(assumptions):
        apath = f"{context}.bridge_assumptions[{index}]"
        assumption = expect_object(item, apath)
        exact_keys(assumption, BRIDGE_KEYS, apath)
        aid = expect_string(assumption["assumption_id"], f"{apath}.assumption_id")
        if not ID_RE.fullmatch(aid):
            fail(f"{apath}.assumption_id: invalid identifier")
        if aid in assumption_ids:
            fail(f"{apath}.assumption_id: duplicate")
        assumption_ids.add(aid)
        expect_string(assumption["statement"], f"{apath}.statement")
        if assumption["grounding"] not in RELATION_GROUNDING:
            fail(f"{apath}.grounding: unexpected value")
        unique_strings(assumption["source_refs"], f"{apath}.source_refs", nonempty=True)

    macros = expect_list(attempt["derived_macros"], f"{context}.derived_macros")
    for index, item in enumerate(macros):
        mpath = f"{context}.derived_macros[{index}]"
        macro = expect_object(item, mpath)
        exact_keys(macro, MACRO_KEYS, mpath)
        expect_string(macro["label"], f"{mpath}.label")
        expansion = expect_object(macro["expansion"], f"{mpath}.expansion")
        exact_keys(expansion, MACRO_EXPANSION_KEYS, f"{mpath}.expansion")
        coord_refs = unique_strings(expansion["coordinate_ids"], f"{mpath}.expansion.coordinate_ids", nonempty=True)
        rel_refs = unique_strings(expansion["relation_ids"], f"{mpath}.expansion.relation_ids", nonempty=True)
        unknown_coords = sorted(set(coord_refs) - basis_ids)
        unknown_rels = sorted(set(rel_refs) - relation_ids)
        if unknown_coords:
            fail(f"{mpath}.expansion.coordinate_ids: unknown {unknown_coords}")
        if unknown_rels:
            fail(f"{mpath}.expansion.relation_ids: unknown {unknown_rels}")
        expect_string(expansion["witness_schema_id"], f"{mpath}.expansion.witness_schema_id")

    outcome = expect_object(attempt["outcome"], f"{context}.outcome")
    status = outcome.get("status")
    if status not in OUTCOMES:
        fail(f"{context}.outcome.status: unexpected value")
    if status == "PASS":
        exact_keys(outcome, PASS_OUTCOME_KEYS, f"{context}.outcome")
        validate_witness(outcome["witness"], f"{context}.outcome.witness", require_verified=True)
    else:
        exact_keys(outcome, RESIDUAL_OUTCOME_KEYS, f"{context}.outcome")
        residual = expect_object(outcome["residual"], f"{context}.outcome.residual")
        exact_keys(residual, RESIDUAL_KEYS, f"{context}.outcome.residual")
        if residual["taxonomy_version"] != versions["residual_taxonomy"]:
            fail(f"{context}.outcome.residual.taxonomy_version: contract mismatch")
        if residual["residual_kind"] not in RESIDUAL_KINDS:
            fail(f"{context}.outcome.residual.residual_kind: unexpected value")
        if residual["failure_layer"] not in FAILURE_LAYERS:
            fail(f"{context}.outcome.residual.failure_layer: unexpected value")
        unique_strings(residual["unmet_obligations"], f"{context}.outcome.residual.unmet_obligations", nonempty=True)
        expect_string(residual["details"], f"{context}.outcome.residual.details")
        attempts = expect_list(outcome["witness_attempts"], f"{context}.outcome.witness_attempts")
        for index, witness in enumerate(attempts):
            validate_witness(witness, f"{context}.outcome.witness_attempts[{index}]", require_verified=False)

    # Structural expansion is mandatory; a macro is never a substitute.
    if macros and (not basis_ids or not relation_ids):
        fail(f"{context}: derived macro cannot replace structural expansion")

    reject_source_label_leakage(attempt, source_labels)
    return attempt
