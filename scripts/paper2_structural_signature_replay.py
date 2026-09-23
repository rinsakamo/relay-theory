"""Machine-readable replay view for Paper 2 #142."""

from __future__ import annotations

import copy
from typing import Any

from paper2_structural_signature_canonical import structural_digest
from paper2_structural_signature_contract import SCHEMA_VERSION, validate

def replay_summary(data: dict[str, Any]) -> dict[str, Any]:
    """Emit a machine-readable replay view without rereading source prose.

    This deliberately exposes the preserved dissection rather than only counts:
    basis expansion, relation graph, P/Q/Pi/C identities and fixation evidence,
    temporal assumptions, bridge assumptions, witness identity/provenance, and
    residual localization all survive into the replay surface.
    """
    validate(data)
    rows = []
    for claim in data["paper"]["claims"]:
        for ir in claim["claim_ir_records"]:
            claim_ir = ir["claim_ir"]
            for attempt in ir["decomposition_attempts"]:
                outcome = attempt["outcome"]
                witness_records = (
                    [outcome["witness"]]
                    if outcome["status"] == "PASS"
                    else outcome["witness_attempts"]
                )
                row = {
                    "claim_id": claim["claim_id"],
                    "source_span_ids": sorted(claim["source_span_ids"]),
                    "ir_id": ir["ir_id"],
                    "attempt_id": attempt["attempt_id"],
                    "claim_ir_version": claim_ir["schema_version"],
                    "basis_expansion": sorted(
                        copy.deepcopy(attempt["basis_instantiation"]["coordinates"]),
                        key=lambda item: item["coordinate_id"],
                    ),
                    "relation_graph": copy.deepcopy(attempt["relation_topology"]),
                    "control_surface": copy.deepcopy(attempt["control_surface"]),
                    "temporal_structure": copy.deepcopy(attempt["temporal_structure"]),
                    "approximation_uncertainty": copy.deepcopy(
                        attempt["approximation_uncertainty"]
                    ),
                    "bridge_assumptions": copy.deepcopy(attempt["bridge_assumptions"]),
                    "derived_macros": copy.deepcopy(attempt["derived_macros"]),
                    "outcome": outcome["status"],
                    "failure_localization": (
                        copy.deepcopy(outcome["residual"])
                        if outcome["status"] == "RESIDUAL"
                        else {"state": "not_applicable"}
                    ),
                    "witnesses": [
                        {
                            "generic_schema_id": witness["generic_schema_id"],
                            "theorem_refs": copy.deepcopy(witness["theorem_refs"]),
                            "instantiated_obligation": witness["instantiated_obligation"],
                            "verification": copy.deepcopy(witness["verification"]),
                        }
                        for witness in witness_records
                    ],
                    "structural_sha256": structural_digest(attempt, claim_ir),
                }
                rows.append(row)
    return {
        "schema_version": SCHEMA_VERSION,
        "paper_id": data["paper"]["paper_id"],
        "source_identity": copy.deepcopy(data["paper"]["source_identity"]),
        "rows": rows,
    }
