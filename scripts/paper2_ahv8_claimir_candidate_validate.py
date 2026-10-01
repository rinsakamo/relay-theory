#!/usr/bin/env python3
"""Validate AHV-8 source-grounded ClaimIR candidates and human-review gate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from paper2_claim_ir_validate import validate as validate_claim_ir

ROOT=Path("paper/validation/jgps-major-revision")
ADMISSION=ROOT/"ahv8-admission-v1.json"
AUTH=ROOT/"ahv8-source-authority-v1.json"
MANIFEST=ROOT/"ahv8-claimir-candidate-manifest-v1.json"
AUDIT=ROOT/"ahv8-source-consistency-audit-v1.json"
PACKET=ROOT/"ahv8-author-review-packet-v1.json"
PROGRESS=ROOT/"ahv8-human-review-progress-v1.json"
CAND=ROOT/"ahv8-claimir-candidates-v1"
PROCEDURE="jgps-ahv8-source-grounded-candidate-v1:#379"

FORBIDDEN_DOWNSTREAM=(
    "evidence_level","grammar_v0","grammar v0","role_gap","architecture_gap",
    "assertion_carrier","assertioncarrier","l_claim","layered_status",
    "p_in","p_out","rho/o","acceptance_verdict","residual_type",
)

class Error(ValueError):
    pass

def load(p:Path)->dict[str,Any]:
    return json.loads(p.read_text(encoding="utf-8"))

def norm_doi(v:str)->str:
    x=v.strip().lower()
    for prefix in ("https://doi.org/","doi:"):
        if x.startswith(prefix):
            x=x[len(prefix):]
    return x

def validate_all()->dict[str,Any]:
    admission=load(ADMISSION)
    auth=load(AUTH)
    manifest=load(MANIFEST)
    audit=load(AUDIT)
    packet=load(PACKET)
    progress=load(PROGRESS)

    if admission["status"]!="FROZEN_PRE_EXTRACTION_ADMISSION":
        raise Error("admission state drift")
    if manifest["status"]!="UNREVIEWED_SOURCE_GROUNDED_CANDIDATES":
        raise Error("manifest state drift")
    if manifest["procedure_version"]!=PROCEDURE:
        raise Error("procedure drift")
    for key in ("evidence_profile_started","grammar_mapping_started","layered_projection_started","assertion_carrier_validation_started"):
        if manifest[key] is not False:
            raise Error(f"manifest downstream state unexpectedly true: {key}")
    if auth["downstream_validation_authorized"] is not False:
        raise Error("source authority unexpectedly authorizes downstream validation")
    if packet["downstream_validation_authorized"] is not False:
        raise Error("review packet unexpectedly authorizes downstream validation")
    if packet["review_completion_must_be_human_authored"] is not True:
        raise Error("human review authorship gate missing")
    if progress["total_count"]!=8:
        raise Error("human review total-count drift")
    if progress["status"]=="PENDING":
        if progress["reviewed_count"]!=0 or progress["downstream_validation_authorized"] is not False:
            raise Error("pending human-review state must be 0/8 and downstream-disabled")
    elif progress["status"]=="COMPLETE":
        if progress["reviewed_count"]!=8 or progress["downstream_validation_authorized"] is not True:
            raise Error("complete human-review state must be 8/8 and downstream-authorized")
    else:
        raise Error(f"unexpected human-review lifecycle state: {progress['status']}")

    admissions=admission["admissions"]
    if len(admissions)!=8:
        raise Error("admission membership drift")
    expected={a["validation_claim_id"]:norm_doi(a["source_identity"]["value"]) for a in admissions}
    expected_files=sorted(f"{k}.json" for k in expected)
    files=sorted(p.name for p in CAND.glob("*.json"))
    if files!=expected_files:
        raise Error(f"candidate files mismatch got={files} expected={expected_files}")
    if sorted(manifest["expected_files"])!=expected_files:
        raise Error("manifest file membership drift")

    auth_by={e["validation_claim_id"]:e for e in auth["entries"]}
    audit_by={e["validation_claim_id"]:e for e in audit["entries"]}
    packet_by={e["validation_claim_id"]:e for e in packet["entries"]}
    if set(auth_by)!=set(expected) or set(audit_by)!=set(expected) or set(packet_by)!=set(expected):
        raise Error("authority/audit/review packet membership mismatch")

    receipts=[]
    for vid in expected:
        path=CAND/f"{vid}.json"
        raw=path.read_text(encoding="utf-8")
        low=raw.casefold()
        for marker in FORBIDDEN_DOWNSTREAM:
            if marker in low:
                raise Error(f"{vid}: downstream marker leaked into pre-review ClaimIR: {marker}")

        obj=load(path)
        validate_claim_ir(obj)
        if obj["claim_id"]!=f"{vid}.C1":
            raise Error(f"{vid}: claim_id mismatch")
        if norm_doi(obj["provenance"]["paper_id"])!=expected[vid]:
            raise Error(f"{vid}: DOI mismatch")
        ext=obj["extraction"]
        if ext["procedure_version"]!=PROCEDURE:
            raise Error(f"{vid}: procedure mismatch")
        if ext["manual_review_status"]!="unreviewed":
            raise Error(f"{vid}: candidate must remain unreviewed")

        a=auth_by[vid]
        if norm_doi(a["stable_identity"])!=expected[vid]:
            raise Error(f"{vid}: source authority DOI mismatch")
        if a["claimir_candidate_status"]!="UNREVIEWED":
            raise Error(f"{vid}: source authority review state drift")
        for key in ("human_review_completed","evidence_profile_created","grammar_mapping_inspected","layered_projection_inspected","assertion_carrier_validation_inspected"):
            if a[key] is not False:
                raise Error(f"{vid}: source authority downstream flag true: {key}")
        if a["source_text_committed"] is not False:
            raise Error(f"{vid}: raw source text must not be committed")

        au=audit_by[vid]
        if au["source_consistency"]!="PASS" or au["human_review_still_required"] is not True:
            raise Error(f"{vid}: assistant audit state invalid")
        for key in ("evidence_profile_inspected","grammar_mapping_inspected","layered_projection_inspected","assertion_carrier_validation_inspected"):
            if au[key] is not False:
                raise Error(f"{vid}: audit downstream flag true: {key}")

        p=packet_by[vid]
        if p["human_review_decision"] is not None or p["reviewer_name_or_initials"] is not None or p["review_date"] is not None:
            raise Error(f"{vid}: human review fields must be null")
        if p["assistant_source_consistency"]!="PASS":
            raise Error(f"{vid}: review packet assistant consistency drift")

        receipts.append({
          "validation_claim_id":vid,
          "paper_id":obj["provenance"]["paper_id"],
          "relation_count":len(obj["claim_core"]["relations"]),
          "node_count":len(obj["claim_core"]["nodes"]),
          "manual_review_status":"unreviewed",
        })

    if audit["scope"]!={"candidates":8,"passes":8,"failures":0,"human_review_required":True}:
        raise Error("audit summary drift")
    if packet["allowed_decisions"]!=["ACCEPT","REVISE","REJECT"]:
        raise Error("review decisions drift")

    return {
      "schema":"relay-theory.paper2.ahv8_claimir_candidate_gate.v1",
      "status":"PASS",
      "candidates":8,
      "assistant_source_consistency_passes":8,
      "human_review_completed":progress["reviewed_count"],
      "downstream_validation_authorized":progress["downstream_validation_authorized"],
      "receipts":receipts,
      "terminal":"AHV8_CLAIMIR_CANDIDATES_STABLE_ACROSS_HUMAN_REVIEW_LIFECYCLE",
    }

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    a=validate_all()
    b=validate_all()
    if a!=b:
        raise Error("non-deterministic validation")
    payload=json.dumps(a,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.write_text(payload,encoding="utf-8")
    else:
        print(payload,end="")
    print("AHV8_CLAIMIR_CANDIDATE_GATE_PASS")

if __name__=="__main__":
    main()
