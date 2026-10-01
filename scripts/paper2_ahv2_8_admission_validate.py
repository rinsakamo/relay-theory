#!/usr/bin/env python3
"""Validate AHV2-8 post-v2 held-out admission."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

ROOT=Path("paper/validation/jgps-major-revision")
LEDGER=Path("research/paper2/designed_source_candidate_ledger_v1.json")
MANIFEST=Path("research/paper2/designed_source_manifest_v1.json")
PVS=ROOT/"pvs16-admission-v1.json"
AHV=ROOT/"ahv8-admission-v1.json"
AHV2=ROOT/"ahv2-8-admission-v1.json"
V2=ROOT/"l-claim-assertion-carrier-schema-v2.json"
LANES=("Memory","Learning","Skill","Attention","Prediction","Control","Belief","Concept")

class Error(ValueError): pass
def load(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding="utf-8"))
def ident(x:dict[str,Any])->tuple[str,str]: return (x["kind"],str(x["value"]).strip().lower())

def validate()->dict[str,Any]:
    ledger=load(LEDGER)["records"]
    manifest=load(MANIFEST)["entries"]
    pvs=load(PVS)["admissions"]
    ahv=load(AHV)["admissions"]
    ahv2=load(AHV2)
    v2=load(V2)

    if ahv2["status"]!="FROZEN_PRE_EXTRACTION_ADMISSION": raise Error("status drift")
    if ahv2["base_authority_commit"]!="ad1c11789814413b1d9fd3ca8a4cfb6f7316f230": raise Error("v2 base commit drift")
    if v2["status"]!="FROZEN_AHV8_DERIVED_PRE_NEW_HELDOUT_VALIDATION": raise Error("v2 schema status drift")
    if ahv2["selection_authority"]["assertion_carrier_v2_freeze_commit"]!="ad1c11789814413b1d9fd3ca8a4cfb6f7316f230": raise Error("v2 freeze authority drift")
    if ahv2["scope"]["actual_claim_count"]!=8: raise Error("count drift")
    if ahv2["scope"]["claim_ir_created"] is not False or ahv2["scope"]["human_review_completed"] is not False or ahv2["scope"]["downstream_validation_started"] is not False:
        raise Error("downstream work started before admission freeze")

    excluded={ident(e["stable_identity"]) for e in manifest}
    excluded|={ident(e["source_identity"]) for e in pvs}
    excluded|={ident(e["source_identity"]) for e in ahv}

    expected=[]
    for lane in LANES:
        matches=[]
        for i,r in enumerate(ledger):
            if r["surface"]!="primary" or r["sampling_stratum"]!=lane: continue
            if r["candidate_state"]!="CANDIDATE": continue
            if ident(r["stable_identity"]) in excluded: continue
            if r["source_access_class"]=="INACCESSIBLE" or "INACCESS" in str(r["read_status"]): continue
            matches.append((i,r))
        if not matches: raise Error(f"{lane}: no eligible candidate")
        expected.append((lane,*matches[0]))

    admissions=ahv2["admissions"]
    if [a["lane"] for a in admissions]!=list(LANES): raise Error("lane order drift")
    if len({a["validation_claim_id"] for a in admissions})!=8: raise Error("duplicate ids")
    for a,(lane,i,r) in zip(admissions,expected):
        p=a["preexisting_selection_rank_or_provenance"]
        got=(a["lane"],p["ledger_record_index_zero_based"],p["slot_id"],p["candidate_rank"],ident(a["source_identity"]),a["title"],a["year"])
        exp=(lane,i,r["slot_id"],r["candidate_rank"],ident(r["stable_identity"]),r["title"],r["year"])
        if got!=exp: raise Error(f"{a['validation_claim_id']}: selection mismatch")
        eb=a["eligibility_basis"]
        if not (eb["unused_in_activated_60_manifest"] and eb["unused_in_pvs16"] and eb["unused_in_ahv8"]):
            raise Error(f"{a['validation_claim_id']}: exclusion receipt missing")
        for k in ("assertion_carrier_v2_inspected_for_selection","claim_ir_created","human_review_completed","assertion_carrier_v2_validation_started"):
            if a[k] is not False: raise Error(f"{a['validation_claim_id']}: {k} must be false")

    return {
      "schema":"relay-theory.paper2.ahv2_8_admission_validation.v1",
      "status":"PASS","claims":8,"lanes":8,
      "selected":[{"lane":lane,"ledger_index":i,"doi":r["stable_identity"]["value"]} for lane,i,r in expected],
      "terminal":"AHV2_8_HELDOUT_ADMISSION_VALIDATION_PASS"
    }

def main()->None:
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=Path); args=ap.parse_args()
    a=validate(); b=validate()
    if a!=b: raise Error("non-deterministic validation")
    payload=json.dumps(a,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.output: args.output.write_text(payload,encoding="utf-8")
    else: print(payload,end="")
    print("AHV2_8_HELDOUT_ADMISSION_GATE_PASS")

if __name__=="__main__": main()
