"""Exact object-key contracts for Paper 2 structural-signature v1."""

TOP_KEYS = {"schema_version", "contract_versions", "paper"}
VERSION_KEYS = {
    "structural_signature",
    "claim_ir",
    "basis",
    "witness_ref",
    "residual_taxonomy",
}
PAPER_KEYS = {"paper_id", "source_identity", "claims"}
SOURCE_IDENTITY_KEYS = {"stable_id", "version", "kind"}
CLAIM_KEYS = {
    "claim_id",
    "source_span_ids",
    "source_construct_labels",
    "claim_ir_records",
}
IR_RECORD_KEYS = {"ir_id", "claim_ir", "decomposition_attempts"}
ATTEMPT_KEYS = {
    "attempt_id",
    "analysis_identity",
    "basis_instantiation",
    "relation_topology",
    "temporal_structure",
    "control_surface",
    "approximation_uncertainty",
    "bridge_assumptions",
    "derived_macros",
    "outcome",
}
ANALYSIS_IDENTITY_KEYS = {"blinded_claim_id", "analysis_labels", "analyzer"}
ANALYZER_KEYS = {"tool", "version"}
BASIS_KEYS = {"coordinates"}
COORDINATE_KEYS = {"coordinate_id", "role", "required", "provenance"}
COORD_PROV_KEYS = {"origin", "ref"}
RELATION_KEYS = {
    "relation_id",
    "kind",
    "arguments",
    "ordered_arguments",
    "grounding",
    "conditional_on",
    "temporal_direction",
}
REF_KEYS = {"space", "ref"}
REL_GROUND_KEYS = {"state", "source_refs"}
TEMPORAL_KEYS = {
    "time_index",
    "history_window",
    "future_horizon",
    "ordering",
    "recurrence",
    "persistence",
}
CONTROL_KEYS = {"probe_P", "criterion_Q", "partition_Pi", "resource_C"}
APPROX_KEYS = {
    "mode",
    "threshold",
    "tolerance",
    "confidence",
    "loss",
    "comparison_criterion",
}
BRIDGE_KEYS = {"assumption_id", "statement", "grounding", "source_refs"}
MACRO_KEYS = {"label", "expansion"}
MACRO_EXPANSION_KEYS = {"coordinate_ids", "relation_ids", "witness_schema_id"}
CONTROL_VALUE_KEYS = {"identity", "description", "provenance"}
CONTROL_PROV_KEYS = {"kind", "source_refs", "fixed_before_target_analysis"}
PASS_OUTCOME_KEYS = {"status", "witness"}
RESIDUAL_OUTCOME_KEYS = {"status", "residual", "witness_attempts"}
WITNESS_KEYS = {
    "schema_version",
    "generic_schema_id",
    "theorem_refs",
    "instantiated_obligation",
    "verification",
}
THEOREM_REF_KEYS = {"kind", "ref"}
VERIFICATION_KEYS = {"status", "checker", "checker_version", "kernel", "evidence_ref"}
RESIDUAL_KEYS = {"taxonomy_version", "residual_kind", "failure_layer", "unmet_obligations", "details"}
