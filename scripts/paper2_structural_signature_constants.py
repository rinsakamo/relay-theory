"""Version and enum constants for Paper 2 structural-signature v1."""

import re

SCHEMA_VERSION = "paper2-structural-signature-v1"
CLAIM_IR_VERSION = "paper2-claim-ir-v1"
SYNTHETIC_BASIS_VERSION = "paper2-synthetic-basis-v1"
WITNESS_REF_VERSION = "paper2-witness-ref-v1"
RESIDUAL_TAXONOMY_VERSION = "paper2-residual-taxonomy-v1"

# Deliberately conservative. This is not a basis freeze. Real basis versions
# remain rejected until an independent authority owner freezes one and this
# compatibility table is explicitly updated.
SUPPORTED_VERSION_TUPLES = {
    (
        SCHEMA_VERSION,
        CLAIM_IR_VERSION,
        SYNTHETIC_BASIS_VERSION,
        WITNESS_REF_VERSION,
        RESIDUAL_TAXONOMY_VERSION,
    )
}

ID_RE = re.compile(r"^[a-z][a-z0-9_.-]{0,127}$")
CLAIM_ID_RE = re.compile(r"^[A-Z][A-Z0-9._-]{0,63}$")

ABSENCE_STATES = {
    "explicitly_absent",
    "not_required",
    "not_measured",
    "not_recoverable",
    "unknown",
    "unspecified",
    "not_applicable",
}
PRESENT_STATE = "present"

BASIS_ROLES = {
    "condition",
    "information",
    "state_or_structure",
    "intervention",
    "response_or_outcome",
    "criterion",
    "probe",
    "partition",
    "resource",
    "temporal",
    "relation",
    "other",
}
COORDINATE_ORIGINS = {
    "claim_ir_node",
    "claim_ir_relation",
    "formal_contract",
    "synthetic_fixture",
}
RELATION_KINDS = {
    "depends_on",
    "conditional_dependence",
    "maps_to",
    "precedes",
    "constrains",
    "distinguishes",
    "equivalent",
    "intervenes_on",
    "observes",
    "conditions",
    "other",
}
RELATION_GROUNDING = {"explicit", "normalized", "formal_contract", "synthetic_fixture"}
TEMPORAL_DIRECTIONS = {"forward", "backward", "simultaneous", "atemporal", "unspecified"}
CONTROL_PROVENANCE = {
    "source_declared",
    "experimental_contract",
    "pre_frozen_generic",
    "synthetic_fixture",
}
ANALYSIS_MODES = {"deterministic", "stochastic", "approximate"}
OUTCOMES = {"PASS", "RESIDUAL"}
RESIDUAL_KINDS = {
    "source_ambiguity",
    "claim_ir_insufficiency",
    "basis_insufficiency",
    "witness_failure",
    "formal_verification_failure",
    "missing_grounding",
    "unsupported_contract",
    "other",
}
FAILURE_LAYERS = {
    "source",
    "claim_ir",
    "basis_instantiation",
    "relation_topology",
    "control_surface",
    "temporal_structure",
    "approximation",
    "bridge",
    "witness",
    "formal_verification",
}
WITNESS_VERIFICATION = {"verified", "synthetic_verified", "failed", "not_run"}
