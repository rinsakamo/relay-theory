#!/usr/bin/env python3
"""Validate Paper 2 #384 pre-review reflexive-audit freeze."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path("paper/validation/jgps-major-revision/reflexive-audit-v1")
PROTOCOL = ROOT / "reflexive-audit-protocol-v1.json"
CANDIDATES = ROOT / "reflexive-claimir-candidates-v1.json"
PROGRESS = ROOT / "human-review-progress-v1.json"
PACKET = ROOT / "author-review-packet-v1.md"

EXPECTED_IDS = [f"RFX{i:02d}" for i in range(1, 15)]

class ValidationError(ValueError):
    pass

def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def validate() -> dict[str, Any]:
    p = load(PROTOCOL)
    c = load(CANDIDATES)
    h = load(PROGRESS)
    review_text = PACKET.read_text(encoding="utf-8")

    if p.get("schema") != "relay-theory.paper2.reflexive_audit_protocol.v1":
        raise ValidationError("protocol schema drift")
    if p.get("status") != "FROZEN_PRE_REVIEW_PROTOCOL":
        raise ValidationError("protocol status drift")
    if p.get("authority_issue") != 384:
        raise ValidationError("protocol authority issue drift")
    if p.get("review_gate", {}).get("downstream_before_complete_review") is not False:
        raise ValidationError("protocol no longer forbids downstream work before review")
    if "Freeze protocol, UNREVIEWED candidates" not in p.get("first_transaction_stop", ""):
        raise ValidationError("first-transaction stop rule drift")

    if c.get("schema") != "relay-theory.paper2.reflexive_audit_claimir_candidates.v1":
        raise ValidationError("candidate packet schema drift")
    if c.get("status") != "UNREVIEWED_CANDIDATE_PACKET":
        raise ValidationError("candidate packet status drift")
    if c.get("authority_issue") != 384:
        raise ValidationError("candidate packet authority issue drift")
    if c.get("candidate_count") != 14:
        raise ValidationError("candidate count is not 14")
    if c.get("candidate_ids") != EXPECTED_IDS:
        raise ValidationError("candidate ID surface drift")
    if len(c.get("candidates", [])) != 14:
        raise ValidationError("candidate payload count is not 14")

    seen_claim_ids: set[str] = set()
    for expected_id, item in zip(EXPECTED_IDS, c["candidates"]):
        if item.get("self_target_id") != expected_id:
            raise ValidationError(f"{expected_id}: self_target_id drift")
        if item.get("grammar_mapping_inspected") is not False:
            raise ValidationError(f"{expected_id}: Grammar mapping inspected before review")
        if item.get("evidence_profile_created") is not False:
            raise ValidationError(f"{expected_id}: Evidence Profile created before review")
        if item.get("reflexive_verdict_created") is not False:
            raise ValidationError(f"{expected_id}: reflexive verdict created before review")

        ir = item.get("claimir", {})
        if ir.get("schema_version") != "paper2-claim-ir-v1":
            raise ValidationError(f"{expected_id}: ClaimIR schema drift")
        if ir.get("claim_id") != f"{expected_id}.C1":
            raise ValidationError(f"{expected_id}: ClaimIR ID drift")
        if ir["claim_id"] in seen_claim_ids:
            raise ValidationError(f"{expected_id}: duplicate ClaimIR ID")
        seen_claim_ids.add(ir["claim_id"])

        extraction = ir.get("extraction", {})
        if extraction.get("manual_review_status") != "unreviewed":
            raise ValidationError(f"{expected_id}: candidate is no longer unreviewed")

        prov = ir.get("provenance", {})
        spans = prov.get("source_spans", [])
        span_ids = [s.get("span_id") for s in spans]
        if not spans or len(span_ids) != len(set(span_ids)):
            raise ValidationError(f"{expected_id}: invalid source spans")
        span_set = set(span_ids)

        core = ir.get("claim_core", {})
        nodes = core.get("nodes", [])
        relations = core.get("relations", [])
        node_ids = [n.get("id") for n in nodes]
        rel_ids = [r.get("id") for r in relations]
        if not nodes or len(node_ids) != len(set(node_ids)):
            raise ValidationError(f"{expected_id}: invalid/duplicate nodes")
        if not relations or len(rel_ids) != len(set(rel_ids)):
            raise ValidationError(f"{expected_id}: invalid/duplicate relations")
        node_set = set(node_ids)

        for n in nodes:
            refs = n.get("source_span_ids", [])
            if not refs or not set(refs) <= span_set:
                raise ValidationError(f"{expected_id}: node source-span reference drift")
        for r in relations:
            if not r.get("arguments") or not set(r["arguments"]) <= node_set:
                raise ValidationError(f"{expected_id}: relation argument drift")
            refs = r.get("source_span_ids", [])
            if not refs or not set(refs) <= span_set:
                raise ValidationError(f"{expected_id}: relation source-span reference drift")

    if h.get("schema") != "relay-theory.paper2.reflexive_audit_human_review_progress.v1":
        raise ValidationError("review progress schema drift")
    expected_progress = {
        "total": 14,
        "reviewed": 0,
        "accepted": 0,
        "revised": 0,
        "rejected": 0,
        "downstream_authorized": False,
    }
    for key, expected in expected_progress.items():
        if h.get(key) != expected:
            raise ValidationError(f"review progress {key} drift")
    if h.get("decisions") != []:
        raise ValidationError("review decisions exist before author review")
    if h.get("remaining") != EXPECTED_IDS:
        raise ValidationError("review remaining set drift")
    if h.get("terminal") != "RFX14_HUMAN_REVIEW_0_OF_14_PENDING":
        raise ValidationError("review terminal drift")

    if "UNREVIEWED" not in review_text or "0 / 14" not in review_text:
        raise ValidationError("review packet status text drift")
    for cid in EXPECTED_IDS:
        if f"| {cid} |" not in review_text:
            raise ValidationError(f"review packet missing {cid}")

    return {
        "schema": "relay-theory.paper2.reflexive_audit_candidate_validation.v1",
        "status": "PASS",
        "authority_issue": 384,
        "candidate_count": 14,
        "human_reviewed": 0,
        "all_candidates_unreviewed": True,
        "grammar_mapping_inspected": False,
        "evidence_profile_created": False,
        "reflexive_verdict_created": False,
        "downstream_authorized": False,
        "terminal": "RFX14_PRE_REVIEW_GATE_VALIDATION_PASS",
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    first = validate()
    second = validate()
    if first != second:
        raise ValidationError("non-deterministic validation")

    payload = json.dumps(first, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    print("PAPER2_REFLEXIVE_AUDIT_PRE_REVIEW_GATE_PASS")

if __name__ == "__main__":
    main()
