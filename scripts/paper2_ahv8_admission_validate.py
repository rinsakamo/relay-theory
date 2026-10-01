#!/usr/bin/env python3
"""Validate AHV-8 held-out admission for AssertionCarrier validation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT=Path("paper/validation/jgps-major-revision")
LEDGER=Path("research/paper2/designed_source_candidate_ledger_v1.json")
MANIFEST=Path("research/paper2/designed_source_manifest_v1.json")
PVS=ROOT/"pvs16-admission-v1.json"
AHV=ROOT/"ahv8-admission-v1.json"

LANES=("Memory","Learning","Skill","Attention","Prediction","Control","Belief","Concept")

class Error(ValueError):
    pass

def load(p:Path)->dict[str,Any]:
    return json.loads(p.read_text(encoding="utf-8"))

def ident(x:dict[str,Any])->tuple[str,str]:
    return (x["kind"],str(x["value"]).strip().lower())

def validate()->dict[str,Any]:
    ledger=load(LEDGER)["records"]
    manifest=load(MANIFEST)["entries"]
    pvs=load(PVS)
    ahv=load(AHV)

    if ahv["status"]!="FROZEN_PRE_EXTRACTION_ADMISSION":
        raise Error("AHV status drift")
    if ahv["base_authority_commit"]!="dedc56f1f64d20154e0fa805b2d565fc921379c1":
        raise Error("carrier-freeze base commit drift")
    if ahv["selection_authority"]["assertion_carrier_freeze_commit"]!="dedc56f1f64d20154e0fa805b2d565fc921379c1":
        raise Error("carrier freeze authority drift")
    if ahv["scope"]["actual_claim_count"]!=8:
        raise Error("AHV count drift")
    if ahv["scope"]["claim_ir_created"] is not False:
        raise Error("ClaimIR unexpectedly created at admission")
    if ahv["scope"]["human_review_completed"] is not False:
        raise Error("human review unexpectedly completed at admission")
    if ahv["scope"]["downstream_mapping_started"] is not False:
        raise Error("downstream mapping unexpectedly started")

    activated={ident(e["stable_identity"]) for e in manifest}
    pvs_ids={ident(e["source_identity"]) for e in pvs["admissions"]}
    selected=[]
    for lane in LANES:
        candidates=[]
        for i,r in enumerate(ledger):
            if r["surface"]!="primary" or r["sampling_stratum"]!=lane:
                continue
            if r["candidate_state"]!="CANDIDATE":
                continue
            rid=ident(r["stable_identity"])
            if rid in activated or rid in pvs_ids:
                continue
            if r["source_access_class"]=="INACCESSIBLE":
                continue
            if "INACCESS" in str(r["read_status"]):
                continue
            candidates.append((i,r))
        if not candidates:
            raise Error(f"{lane}: no eligible held-out candidate")
        selected.append((lane,*candidates[0]))

    admissions=ahv["admissions"]
    if [a["lane"] for a in admissions]!=list(LANES):
        raise Error("lane order drift")
    if len({a["validation_claim_id"] for a in admissions})!=8:
        raise Error("duplicate validation_claim_id")

    expected=[]
    for lane,i,r in selected:
        expected.append({
          "lane":lane,
          "ledger_index":i,
          "slot_id":r["slot_id"],
          "candidate_rank":r["candidate_rank"],
          "identity":ident(r["stable_identity"]),
          "title":r["title"],
          "year":r["year"],
        })

    for a,e in zip(admissions,expected):
        p=a["preexisting_selection_rank_or_provenance"]
        got={
          "lane":a["lane"],
          "ledger_index":p["ledger_record_index_zero_based"],
          "slot_id":p["slot_id"],
          "candidate_rank":p["candidate_rank"],
          "identity":ident(a["source_identity"]),
          "title":a["title"],
          "year":a["year"],
        }
        if got!=e:
            raise Error(f"{a['validation_claim_id']}: selection mismatch got={got} expected={e}")
        eb=a["eligibility_basis"]
        if eb["unused_in_activated_60_manifest"] is not True or eb["unused_in_pvs16"] is not True:
            raise Error(f"{a['validation_claim_id']}: exclusion receipt missing")
        for k in (
          "assertion_carrier_schema_inspected_for_selection",
          "claim_ir_created",
          "human_review_completed",
          "evidence_profile_created",
          "grammar_mapping_started",
          "layered_projection_started",
          "assertion_carrier_validation_started",
        ):
            if a[k] is not False:
                raise Error(f"{a['validation_claim_id']}: {k} must be false at admission")

    return {
      "schema":"relay-theory.paper2.ahv8_admission_validation.v1",
      "status":"PASS",
      "claims":8,
      "lanes":8,
      "selected":[
        {"lane":lane,"ledger_index":i,"doi":r["stable_identity"]["value"]}
        for lane,i,r in selected
      ],
      "terminal":"AHV8_HELDOUT_ADMISSION_VALIDATION_PASS",
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
    print("AHV8_HELDOUT_ADMISSION_GATE_PASS")

if __name__=="__main__":
    main()
