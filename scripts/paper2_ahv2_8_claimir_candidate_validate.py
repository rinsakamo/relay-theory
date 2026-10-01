#!/usr/bin/env python3
"""Validate AHV2-8 source-grounded ClaimIR candidates and pre-v2-validation review gate."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any
from paper2_claim_ir_validate import validate as validate_claim_ir

ROOT=Path("paper/validation/jgps-major-revision")
ADMISSION=ROOT/"ahv2-8-admission-v1.json"
AUTH=ROOT/"ahv2-8-source-authority-v1.json"
MANIFEST=ROOT/"ahv2-8-claimir-candidate-manifest-v1.json"
AUDIT=ROOT/"ahv2-8-source-consistency-audit-v1.json"
PACKET=ROOT/"ahv2-8-author-review-packet-v1.json"
PROGRESS=ROOT/"ahv2-8-human-review-progress-v1.json"
CAND=ROOT/"ahv2-8-claimir-candidates-v1"
PROCEDURE="jgps-ahv2-8-source-grounded-candidate-v1:#390"

FORBIDDEN=("assertion_carrier","assertioncarrier","carrier_status","predicate_family","directionality","evaluation","architecture_gap","role_gap","grammar_v0","l_claim")

class Error(ValueError): pass
def load(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding="utf-8"))
def doi(v:str)->str:
    x=v.strip().lower()
    for p in ("doi:","https://doi.org/"):
        if x.startswith(p): x=x[len(p):]
    return x

def validate()->dict[str,Any]:
    admission,auth,manifest,audit,packet,progress=map(load,(ADMISSION,AUTH,MANIFEST,AUDIT,PACKET,PROGRESS))
    if admission["status"]!="FROZEN_PRE_EXTRACTION_ADMISSION": raise Error("admission drift")
    if manifest["status"]!="UNREVIEWED_SOURCE_GROUNDED_CANDIDATES": raise Error("manifest drift")
    if manifest["procedure_version"]!=PROCEDURE: raise Error("procedure drift")
    if manifest["assertion_carrier_v2_validation_started"] is not False: raise Error("v2 validation started")
    if auth["assertion_carrier_v2_validation_authorized"] is not False: raise Error("authority prematurely authorizes v2")
    if packet["assertion_carrier_v2_validation_authorized"] is not False: raise Error("packet prematurely authorizes v2")
    if packet["review_completion_must_be_human_authored"] is not True: raise Error("human authorship gate missing")
    if progress["total_count"]!=8: raise Error("review total-count drift")
    if progress["status"]=="PENDING":
        if progress["reviewed_count"]!=0 or progress["assertion_carrier_v2_validation_authorized"] is not False:
            raise Error("PENDING state must be 0/8 and v2-disabled")
    elif progress["status"]=="COMPLETE":
        if progress["reviewed_count"]!=8 or progress["assertion_carrier_v2_validation_authorized"] is not True:
            raise Error("COMPLETE state must be 8/8 and v2-authorized")
    else:
        raise Error("unexpected review-lifecycle state")

    expected={a["validation_claim_id"]:doi(a["source_identity"]["value"]) for a in admission["admissions"]}
    files=sorted(p.name for p in CAND.glob("*.json"))
    expfiles=sorted(f"{x}.json" for x in expected)
    if files!=expfiles or sorted(manifest["expected_files"])!=expfiles: raise Error("candidate membership drift")
    authby={e["validation_claim_id"]:e for e in auth["entries"]}
    auditby={e["validation_claim_id"]:e for e in audit["entries"]}
    packetby={e["validation_claim_id"]:e for e in packet["entries"]}
    if set(authby)!=set(expected) or set(auditby)!=set(expected) or set(packetby)!=set(expected): raise Error("metadata membership drift")

    receipts=[]
    total_relations=0
    for vid in expected:
        raw=(CAND/f"{vid}.json").read_text(encoding="utf-8")
        low=raw.casefold()
        for marker in FORBIDDEN:
            if marker in low: raise Error(f"{vid}: downstream marker leaked: {marker}")
        obj=json.loads(raw); validate_claim_ir(obj)
        if obj["claim_id"]!=f"{vid}.C1": raise Error(f"{vid}: claim id")
        if doi(obj["provenance"]["paper_id"])!=expected[vid]: raise Error(f"{vid}: DOI")
        if obj["extraction"]["procedure_version"]!=PROCEDURE or obj["extraction"]["manual_review_status"]!="unreviewed":
            raise Error(f"{vid}: extraction state")
        a=authby[vid]
        if doi(a["stable_identity"])!=expected[vid] or a["claimir_candidate_status"]!="UNREVIEWED" or a["source_text_committed"] is not False:
            raise Error(f"{vid}: authority state")
        for k in ("human_review_completed","assertion_carrier_v2_validation_inspected","grammar_mapping_inspected","layered_projection_inspected"):
            if a[k] is not False: raise Error(f"{vid}: authority downstream flag {k}")
        au=auditby[vid]
        if au["source_consistency"]!="PASS" or au["human_review_still_required"] is not True: raise Error(f"{vid}: audit state")
        for k in ("assertion_carrier_v2_validation_inspected","grammar_mapping_inspected","layered_projection_inspected"):
            if au[k] is not False: raise Error(f"{vid}: audit downstream flag {k}")
        p=packetby[vid]
        if p["human_review_decision"] is not None or p["reviewer_name_or_initials"] is not None or p["review_date"] is not None:
            raise Error(f"{vid}: human fields nonnull")
        if p["assistant_source_consistency"]!="PASS": raise Error(f"{vid}: packet audit")
        rc=len(obj["claim_core"]["relations"]); total_relations+=rc
        receipts.append({"validation_claim_id":vid,"nodes":len(obj["claim_core"]["nodes"]),"relations":rc})

    if audit["scope"]!={"candidates":8,"passes":8,"failures":0,"human_review_required":True}: raise Error("audit summary")
    if packet["allowed_decisions"]!=["ACCEPT","REVISE","REJECT"]: raise Error("decision vocabulary")
    if total_relations!=33: raise Error(f"relation total drift: {total_relations}")

    return {"schema":"relay-theory.paper2.ahv2_8_claimir_candidate_gate.v1","status":"PASS","candidates":8,"relations":33,"human_review_completed":progress["reviewed_count"],"v2_validation_authorized":progress["assertion_carrier_v2_validation_authorized"],"receipts":receipts,"terminal":"AHV2_8_CLAIMIR_CANDIDATES_STABLE_ACROSS_REVIEW_LIFECYCLE"}

def main()->None:
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=Path); args=ap.parse_args()
    a=validate(); b=validate()
    if a!=b: raise Error("non-deterministic validation")
    payload=json.dumps(a,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.output: args.output.write_text(payload,encoding="utf-8")
    else: print(payload,end="")
    print("AHV2_8_CLAIMIR_CANDIDATE_GATE_PASS")
if __name__=="__main__": main()
