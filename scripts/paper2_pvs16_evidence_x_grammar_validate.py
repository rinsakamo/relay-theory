#!/usr/bin/env python3
"""Validate PVS-16 prospective Grammar-v0 mapping and evidence-stratified join.

The mapping artifact must remain structurally independent of the E0-E3
annotation layer. The diagnostic join is validated only after that mapping
artifact is frozen.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path("paper/validation/jgps-major-revision")
MAPPING = ROOT / "pvs16-grammar-v0-prospective-mapping-v1.json"
EVIDENCE = ROOT / "pvs16-evidence-profile-v1.json"
DIAGNOSTIC = ROOT / "pvs16-evidence-x-grammar-diagnostic-v1.json"

EXPECTED_CLAIMS = 16
EXPECTED_RELATIONS = 52
LEVELS = ("E0", "E1", "E2", "E3")
STATUSES = ("PRESERVED", "PARTIAL", "UNMAPPED")

class Error(ValueError):
    pass

def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def validate_all() -> dict[str, Any]:
    mapping_raw=MAPPING.read_text(encoding="utf-8")
    mapping=json.loads(mapping_raw)
    evidence=load(EVIDENCE)
    diag=load(DIAGNOSTIC)

    if mapping["status"] != "FROZEN_PROSPECTIVE_MAPPING":
        raise Error("mapping not frozen")
    if mapping["mapping_input_policy"]["evidence_profile_used_to_set_mapping_verdicts"] is not False:
        raise Error("mapping declares evidence-conditioned verdicts")
    if mapping["mapping_input_policy"]["evidence_profile_join_deferred"] is not True:
        raise Error("mapping did not defer evidence join")
    if mapping["evidence_join_performed"] is not False:
        raise Error("mapping artifact says evidence join already performed")
    for forbidden in ('"evidence_level"', '"E0"', '"E1"', '"E2"', '"E3"'):
        if forbidden in mapping_raw:
            raise Error(f"evidence annotation leaked into mapping artifact: {forbidden}")

    claims=mapping["claims"]
    if len(claims) != EXPECTED_CLAIMS:
        raise Error(f"mapping claim count {len(claims)} != {EXPECTED_CLAIMS}")
    if len({c["validation_claim_id"] for c in claims}) != EXPECTED_CLAIMS:
        raise Error("duplicate mapping validation_claim_id")

    relation_counts=Counter()
    verdict_counts=Counter()
    role_gap_relations=[]
    mapping_relations={}
    for c in claims:
        statuses=[r["status"] for r in c["relation_projections"]]
        if any(s not in STATUSES for s in statuses):
            raise Error(f"{c['validation_claim_id']}: bad relation status")
        expected_verdict = (
            "RESIDUAL" if "UNMAPPED" in statuses
            else "PARTIAL" if "PARTIAL" in statuses
            else "FULL"
        )
        if c["verdict"] != expected_verdict:
            raise Error(f"{c['validation_claim_id']}: verdict mismatch")
        verdict_counts[c["verdict"]]+=1
        for r in c["relation_projections"]:
            key=(c["validation_claim_id"],r["relation_id"])
            if key in mapping_relations:
                raise Error(f"duplicate mapped relation {key}")
            mapping_relations[key]=r
            relation_counts[r["status"]]+=1
        for u in c.get("unmapped_residuals",[]):
            if u["primary"] == "ROLE_GAP" or "ROLE_GAP" in u.get("secondary",[]):
                role_gap_relations.extend((c["validation_claim_id"],rid) for rid in u.get("relations",[]))

    if sum(relation_counts.values()) != EXPECTED_RELATIONS:
        raise Error(f"mapping relation count {sum(relation_counts.values())} != {EXPECTED_RELATIONS}")
    if dict(verdict_counts) != mapping["summary"]["claim_verdict_counts"]:
        raise Error("claim verdict summary drift")
    if dict(relation_counts) != mapping["summary"]["relation_projection_counts"]:
        raise Error("relation projection summary drift")
    if role_gap_relations:
        raise Error(f"unexpected ROLE_GAP: {role_gap_relations}")
    if mapping["summary"]["role_gap_claims"] != []:
        raise Error("mapping summary ROLE_GAP list not empty")

    evidence_relations={}
    for c in evidence["entries"]:
        vid=c["validation_claim_id"]
        for r in c["relations"]:
            key=(vid,r["relation_id"])
            if key in evidence_relations:
                raise Error(f"duplicate evidence relation {key}")
            if r["evidence_level"] not in LEVELS:
                raise Error(f"{key}: bad evidence level")
            evidence_relations[key]=r
    if len(evidence_relations) != EXPECTED_RELATIONS:
        raise Error(f"evidence relation count {len(evidence_relations)} != {EXPECTED_RELATIONS}")
    if set(evidence_relations) != set(mapping_relations):
        missing=sorted(set(mapping_relations)-set(evidence_relations))
        extra=sorted(set(evidence_relations)-set(mapping_relations))
        raise Error(f"mapping/evidence relation mismatch missing={missing} extra={extra}")

    joined=diag["joined_relations"]
    if len(joined) != EXPECTED_RELATIONS:
        raise Error(f"diagnostic joined relation count {len(joined)} != {EXPECTED_RELATIONS}")
    joined_keys={(r["validation_claim_id"],r["relation_id"]) for r in joined}
    if joined_keys != set(mapping_relations):
        raise Error("diagnostic joined relation membership mismatch")

    matrix={lv:{s:0 for s in STATUSES}|{"TOTAL":0} for lv in LEVELS}
    for r in joined:
        key=(r["validation_claim_id"],r["relation_id"])
        mr=mapping_relations[key]
        er=evidence_relations[key]
        if r["mapping_status"] != mr["status"]:
            raise Error(f"{key}: joined mapping status drift")
        if r["evidence_level"] != er["evidence_level"]:
            raise Error(f"{key}: joined evidence level drift")
        lv=r["evidence_level"]
        st=r["mapping_status"]
        matrix[lv][st]+=1
        matrix[lv]["TOTAL"]+=1

    for lv in LEVELS:
        got=diag["relation_level_matrix"][lv]
        for k in (*STATUSES,"TOTAL"):
            if got[k] != matrix[lv][k]:
                raise Error(f"{lv}: matrix {k} drift")
        strict=matrix[lv]["PRESERVED"]/matrix[lv]["TOTAL"] if matrix[lv]["TOTAL"] else 0.0
        covered=(matrix[lv]["PRESERVED"]+matrix[lv]["PARTIAL"])/matrix[lv]["TOTAL"] if matrix[lv]["TOTAL"] else 0.0
        if abs(got["strict_preservation_rate"]-strict)>1e-12:
            raise Error(f"{lv}: strict rate drift")
        if abs(got["covered_rate"]-covered)>1e-12:
            raise Error(f"{lv}: covered rate drift")

    expected_matrix={
        "E0":{"PRESERVED":22,"PARTIAL":2,"UNMAPPED":1,"TOTAL":25},
        "E1":{"PRESERVED":9,"PARTIAL":1,"UNMAPPED":5,"TOTAL":15},
        "E2":{"PRESERVED":4,"PARTIAL":2,"UNMAPPED":2,"TOTAL":8},
        "E3":{"PRESERVED":3,"PARTIAL":0,"UNMAPPED":1,"TOTAL":4},
    }
    for lv,exp in expected_matrix.items():
        for k,v in exp.items():
            if matrix[lv][k] != v:
                raise Error(f"{lv}: frozen expected {k}={v}, got {matrix[lv][k]}")

    e3_unmapped=[r for r in joined if r["evidence_level"]=="E3" and r["mapping_status"]=="UNMAPPED"]
    if [(r["validation_claim_id"],r["relation_id"],r["residual_primary"]) for r in e3_unmapped] != [
        ("PVS-CNC-02","r2","RELATION_LANGUAGE_GAP")
    ]:
        raise Error("E3 unmapped diagnostic drift")
    e2_unmapped=[r for r in joined if r["evidence_level"]=="E2" and r["mapping_status"]=="UNMAPPED"]
    if {(r["validation_claim_id"],r["relation_id"],r["residual_primary"]) for r in e2_unmapped} != {
        ("PVS-ATT-02","r1","SOURCE_CONTEXT_PARAMETER"),
        ("PVS-ATT-02","r3","SOURCE_CONTEXT_PARAMETER"),
    }:
        raise Error("E2 unmapped diagnostic drift")
    if any(r["residual_primary"]=="ROLE_GAP" for r in joined):
        raise Error("joined diagnostic unexpectedly contains ROLE_GAP")

    return {
        "schema":"relay-theory.paper2.pvs16_evidence_x_grammar_validation.v1",
        "status":"PASS",
        "claim_count":len(claims),
        "relation_count":len(joined),
        "claim_verdict_counts":dict(verdict_counts),
        "relation_projection_counts":dict(relation_counts),
        "evidence_matrix":matrix,
        "role_gap_relations":0,
        "terminal":"PVS16_EVIDENCE_X_GRAMMAR_VALIDATION_PASS",
    }

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    a=validate_all()
    b=validate_all()
    if a != b:
        raise Error("non-deterministic validation")
    payload=json.dumps(a,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.write_text(payload,encoding="utf-8")
    else:
        print(payload,end="")
    print("PVS16_EVIDENCE_X_GRAMMAR_GATE_PASS")

if __name__=="__main__":
    main()
