#!/usr/bin/env python3
"""Validate completed AHV-8 author human review against frozen candidates."""
from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from pathlib import Path
from typing import Any

from paper2_claim_ir_validate import validate as validate_claim_ir

ROOT=Path("paper/validation/jgps-major-revision")
CAND=ROOT/"ahv8-claimir-candidates-v1"
REV=ROOT/"ahv8-claimir-human-reviewed-v1"
PROGRESS=ROOT/"ahv8-human-review-progress-v1.json"
SUMMARY=ROOT/"ahv8-human-review-summary-v1.json"

IDS=(
 "AHV-MEM-01","AHV-LRN-01","AHV-SKL-01","AHV-ATT-01",
 "AHV-PRD-01","AHV-CTL-01","AHV-BLF-01","AHV-CNC-01",
)

EXPECTED={
 "AHV-MEM-01":"REVISE",
 "AHV-LRN-01":"REVISE",
 "AHV-SKL-01":"ACCEPT",
 "AHV-ATT-01":"REVISE",
 "AHV-PRD-01":"REVISE",
 "AHV-CTL-01":"ACCEPT",
 "AHV-BLF-01":"ACCEPT",
 "AHV-CNC-01":"REVISE",
}

class Error(ValueError):
    pass

def load(p:Path)->dict[str,Any]:
    return json.loads(p.read_text(encoding="utf-8"))

def expected_reviewed(vid:str, candidate:dict[str,Any])->dict[str,Any]:
    x=copy.deepcopy(candidate)
    x["extraction"]["manual_review_status"]="reviewed"

    if vid=="AHV-MEM-01":
        for n in x["claim_core"]["nodes"]:
            if n["id"] in {"limited_item_account","divisible_resource_account"}:
                n["role"]="other"
    elif vid=="AHV-LRN-01":
        r4=next(r for r in x["claim_core"]["relations"] if r["id"]=="r4")
        r4["arguments"]=[
          "conditioned_cue","predicted_reward","reward_discrepancy",
          "neural_response","learned_behavior"
        ]
    elif vid=="AHV-ATT-01":
        x["claim_core"]["nodes"]=[
          n for n in x["claim_core"]["nodes"] if n["id"]!="perceptual_selection_process"
        ]
    elif vid=="AHV-PRD-01":
        x["claim_core"]["relations"]=[
          r for r in x["claim_core"]["relations"] if r["id"]!="r3"
        ]
    elif vid=="AHV-CNC-01":
        for n in x["claim_core"]["nodes"]:
            if n["id"] in {"exemplar_account","additive_feature_account"}:
                n["role"]="other"
    return x

def validate()->dict[str,Any]:
    progress=load(PROGRESS)
    summary=load(SUMMARY)

    if progress["status"]!="COMPLETE":
        raise Error("progress status is not COMPLETE")
    if progress["reviewed_count"]!=8 or progress["total_count"]!=8:
        raise Error("progress count drift")
    if progress["downstream_validation_authorized"] is not True:
        raise Error("downstream validation not authorized after complete review")
    if progress["terminal"]!="AHV8_HUMAN_REVIEW_COMPLETE_8_OF_8":
        raise Error("progress terminal drift")

    entries=progress["entries"]
    if [e["validation_claim_id"] for e in entries]!=list(IDS):
        raise Error("review order/membership drift")
    if {e["validation_claim_id"]:e["human_review_decision"] for e in entries}!=EXPECTED:
        raise Error("review decision drift")

    for e in entries:
        if e["reviewer"]!="author" or e["review_date"]!="2026-10-01":
            raise Error(f"{e['validation_claim_id']}: reviewer/date drift")
        for key in (
          "evidence_profile_inspected",
          "grammar_mapping_inspected",
          "layered_projection_inspected",
          "assertion_carrier_validation_inspected",
        ):
            if e[key] is not False:
                raise Error(f"{e['validation_claim_id']}: downstream inspection leaked into human review")

    expected_files=sorted(f"{vid}.json" for vid in IDS)
    got=sorted(p.name for p in REV.glob("*.json"))
    if got!=expected_files:
        raise Error(f"reviewed-copy membership drift got={got}")

    receipts=[]
    for vid in IDS:
        cand=load(CAND/f"{vid}.json")
        rev=load(REV/f"{vid}.json")
        validate_claim_ir(cand)
        validate_claim_ir(rev)
        if cand["extraction"]["manual_review_status"]!="unreviewed":
            raise Error(f"{vid}: frozen candidate was modified")
        if rev["extraction"]["manual_review_status"]!="reviewed":
            raise Error(f"{vid}: reviewed copy not marked reviewed")
        exp=expected_reviewed(vid,cand)
        if rev!=exp:
            raise Error(f"{vid}: reviewed copy differs from authorized human-review transformation")
        decision=EXPECTED[vid]
        changed=(rev!=dict(cand, extraction={**cand["extraction"],"manual_review_status":"reviewed"}))
        if decision=="ACCEPT" and changed:
            raise Error(f"{vid}: ACCEPT contains substantive change")
        if decision=="REVISE" and not changed:
            raise Error(f"{vid}: REVISE lacks substantive change")
        receipts.append({
          "validation_claim_id":vid,
          "decision":decision,
          "nodes":len(rev["claim_core"]["nodes"]),
          "relations":len(rev["claim_core"]["relations"]),
        })

    counts=Counter(EXPECTED.values())
    wanted={"ACCEPT":3,"REVISE":5,"REJECT":0}
    got_counts={k:counts.get(k,0) for k in wanted}
    if got_counts!=wanted:
        raise Error(f"decision-count drift: {got_counts}")

    if summary["status"]!="FROZEN_HUMAN_REVIEW_COMPLETE":
        raise Error("summary status drift")
    if summary["counts"]!={"ACCEPT":3,"REVISE":5,"REJECT":0,"total":8}:
        raise Error("summary counts drift")
    if summary["downstream_validation_authorized"] is not True:
        raise Error("summary downstream authorization drift")
    b=summary["review_boundary"]
    for key in (
      "evidence_profile_inspected",
      "grammar_mapping_inspected",
      "layered_projection_inspected",
      "assertion_carrier_validation_inspected",
    ):
        if b[key] is not False:
            raise Error(f"summary review boundary drift: {key}")

    return {
      "schema":"relay-theory.paper2.ahv8_human_review_validation.v1",
      "status":"PASS",
      "reviewed":8,
      "decision_counts":wanted,
      "downstream_validation_authorized":True,
      "receipts":receipts,
      "terminal":"AHV8_HUMAN_REVIEW_VALIDATION_PASS",
    }

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    a=validate()
    b=validate()
    if a!=b:
        raise Error("non-deterministic validation")
    payload=json.dumps(a,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.write_text(payload,encoding="utf-8")
    else:
        print(payload,end="")
    print("AHV8_HUMAN_REVIEW_GATE_PASS")

if __name__=="__main__":
    main()
