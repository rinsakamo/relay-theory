"""Top-level semantic validation for Paper 2 structural-signature v1."""

from __future__ import annotations

from typing import Any

from paper2_claim_ir_validate import ValidationError as ClaimIRValidationError
from paper2_claim_ir_validate import validate as validate_claim_ir
from paper2_structural_signature_attempt import validate_attempt
from paper2_structural_signature_contract_core import validate_versions
from paper2_structural_signature_types import *

def validate(data: Any) -> dict[str, Any]:
    # Do not globally reject JSON null: frozen ClaimIR v1 intentionally permits
    # null in provenance fields such as venue/citation_count. Structural fields
    # that carry scientific absence semantics are validated through explicit
    # state objects, so ambiguous null remains invalid there without changing
    # ClaimIR semantics.
    root = expect_object(data, "root")
    exact_keys(root, TOP_KEYS, "root")
    versions = validate_versions(root)

    paper = expect_object(root["paper"], "root.paper")
    exact_keys(paper, PAPER_KEYS, "root.paper")
    paper_id = expect_string(paper["paper_id"], "root.paper.paper_id")
    source_identity = expect_object(paper["source_identity"], "root.paper.source_identity")
    exact_keys(source_identity, SOURCE_IDENTITY_KEYS, "root.paper.source_identity")
    expect_string(source_identity["stable_id"], "root.paper.source_identity.stable_id")
    expect_string(source_identity["version"], "root.paper.source_identity.version")
    expect_string(source_identity["kind"], "root.paper.source_identity.kind")
    if source_identity["stable_id"] != paper_id:
        fail("root.paper.source_identity.stable_id: must match paper_id")

    claims = expect_list(paper["claims"], "root.paper.claims")
    if not claims:
        fail("root.paper.claims: must not be empty")
    claim_ids: set[str] = set()
    for claim_index, claim_value in enumerate(claims):
        cpath = f"root.paper.claims[{claim_index}]"
        claim = expect_object(claim_value, cpath)
        exact_keys(claim, CLAIM_KEYS, cpath)
        claim_id = expect_string(claim["claim_id"], f"{cpath}.claim_id")
        if not CLAIM_ID_RE.fullmatch(claim_id):
            fail(f"{cpath}.claim_id: invalid identifier")
        if claim_id in claim_ids:
            fail(f"{cpath}.claim_id: duplicate")
        claim_ids.add(claim_id)
        source_span_ids = unique_strings(claim["source_span_ids"], f"{cpath}.source_span_ids", nonempty=True)
        source_labels = unique_strings(claim["source_construct_labels"], f"{cpath}.source_construct_labels")

        ir_records = expect_list(claim["claim_ir_records"], f"{cpath}.claim_ir_records")
        if not ir_records:
            fail(f"{cpath}.claim_ir_records: must not be empty")
        ir_ids: set[str] = set()
        for ir_index, ir_value in enumerate(ir_records):
            ipath = f"{cpath}.claim_ir_records[{ir_index}]"
            ir_record = expect_object(ir_value, ipath)
            exact_keys(ir_record, IR_RECORD_KEYS, ipath)
            ir_id = expect_string(ir_record["ir_id"], f"{ipath}.ir_id")
            if not ID_RE.fullmatch(ir_id):
                fail(f"{ipath}.ir_id: invalid identifier")
            if ir_id in ir_ids:
                fail(f"{ipath}.ir_id: duplicate")
            ir_ids.add(ir_id)

            claim_ir = ir_record["claim_ir"]
            try:
                validate_claim_ir(claim_ir)
            except ClaimIRValidationError as exc:
                fail(f"{ipath}.claim_ir: invalid ClaimIR v1: {exc}")
            if claim_ir["schema_version"] != versions["claim_ir"]:
                fail(f"{ipath}.claim_ir.schema_version: contract mismatch")
            if claim_ir["claim_id"] != claim_id:
                fail(f"{ipath}.claim_ir.claim_id: claim nesting mismatch")
            if claim_ir["provenance"]["paper_id"] != paper_id:
                fail(f"{ipath}.claim_ir.provenance.paper_id: paper nesting mismatch")
            claim_ir_spans = {span["span_id"] for span in claim_ir["provenance"]["source_spans"]}
            if set(source_span_ids) - claim_ir_spans:
                fail(f"{cpath}.source_span_ids: unknown ClaimIR source spans")
            if sorted(source_labels) != sorted(claim_ir["provenance"]["construct_labels"]):
                fail(f"{cpath}.source_construct_labels: must match ClaimIR provenance construct_labels")

            attempts = expect_list(ir_record["decomposition_attempts"], f"{ipath}.decomposition_attempts")
            if not attempts:
                fail(f"{ipath}.decomposition_attempts: must not be empty")
            attempt_ids: set[str] = set()
            for attempt_index, attempt_value in enumerate(attempts):
                apath = f"{ipath}.decomposition_attempts[{attempt_index}]"
                attempt = validate_attempt(attempt_value, claim_ir, source_labels, versions, apath)
                if attempt["attempt_id"] in attempt_ids:
                    fail(f"{apath}.attempt_id: duplicate")
                attempt_ids.add(attempt["attempt_id"])

    return root
