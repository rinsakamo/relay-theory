#!/usr/bin/env python3
"""Validate PVS-16 layered-architecture projection and evidence join."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT=Path("paper/validation/jgps-major-revision")
MAPPING=ROOT/"pvs16-grammar-v0-prospective-mapping-v1.json"
PROJECTION=ROOT/"pvs16-layered-architecture-projection-v1.json"
EVIDENCE=ROOT/"pvs16-evidence-profile-v1.json"
DIAGNOSTIC=ROOT/"pvs16-evidence-x-layered-architecture-diagnostic-v1.json"
CONTEXT=Path("research/paper2/source_context_architecture_placement_v1.json")

LEVELS=("E0","E1","E2","E3")
SYSTEM_STATUSES=("PRESERVED","PARTIAL","UNMAPPED")
ALLOWED_CONTEXT={
    "EXPERIMENT_CONTEXT","WORLD_CONTEXT","RUN_BOUNDARY_OR_PREHISTORY",
    "SYSTEM_INTRINSIC_CONSTRAINT_CANDIDATE","PARAMETER_ONLY","UNDERDETERMINED"
}

class Error(ValueError):
    pass

def load(p:Path)->dict[str,Any]:
    return json.loads(p.read_text(encoding="utf-8"))

def validate()->dict[str,Any]:
    mapping=load(MAPPING)
    projection_raw=PROJECTION.read_text(encoding="utf-8")
    projection=json.loads(projection_raw)
    evidence=load(EVIDENCE)
    diagnostic=load(DIAGNOSTIC)
    context=load(CONTEXT)

    if projection["status"]!="FROZEN_PRE_EVIDENCE_LAYERED_PROJECTION":
        raise Error("projection status drift")
    if projection["sequencing"]["evidence_profile_used_for_layer_placement"] is not False:
        raise Error("projection is evidence-conditioned")
    if projection["sequencing"]["evidence_join_deferred"] is not True:
        raise Error("projection did not defer evidence join")
    for forbidden in ('"evidence_level"', '"E0"', '"E1"', '"E2"', '"E3"'):
        if forbidden in projection_raw:
            raise Error(f"evidence annotation leaked into layered projection: {forbidden}")

    mapping_rel={}
    for c in mapping["claims"]:
        for r in c["relation_projections"]:
            key=f"{c['validation_claim_id']}.{r['relation_id']}"
            if key in mapping_rel:
                raise Error(f"duplicate mapping relation {key}")
            if r["status"] not in SYSTEM_STATUSES:
                raise Error(f"bad mapping status {key}")
            mapping_rel[key]=r["status"]
    if len(mapping_rel)!=52:
        raise Error(f"mapping relation count {len(mapping_rel)} != 52")

    nonstrict={k for k,v in mapping_rel.items() if v!="PRESERVED"}
    direct={k for k,v in mapping_rel.items() if v=="PRESERVED"}
    if len(direct)!=38 or len(nonstrict)!=14:
        raise Error("frozen system split drift")

    recoveries=projection["nonstrict_relation_recoveries"]
    rec_by={r["relation"]:r for r in recoveries}
    if len(rec_by)!=14 or set(rec_by)!=nonstrict:
        raise Error("layer recovery membership does not exactly match 14 non-strict system relations")
    if any(r["layered_status"]=="ARCHITECTURE_GAP" for r in recoveries):
        raise Error("unexpected architecture gap")
    for k,r in rec_by.items():
        if r["system_status"]!=mapping_rel[k]:
            raise Error(f"{k}: system status drift in recovery")
        if "L_claim" not in r["layers"]:
            raise Error(f"{k}: non-strict recovery missing L_claim")
        if not r["assertion_class"]:
            raise Error(f"{k}: empty assertion class")

    known_classes=set(context["placement_classes"])
    if known_classes != ALLOWED_CONTEXT:
        raise Error("upstream context placement vocabulary drift")
    for p in projection["context_placements"]:
        if p["primary"] not in ALLOWED_CONTEXT:
            raise Error(f"bad primary context class {p['primary']}")
        for s in p.get("secondary",[]):
            if s not in ALLOWED_CONTEXT:
                raise Error(f"bad secondary context class {s}")

    pressures=[r["relation"] for r in recoveries if r["carrier_status"]=="DESCRIPTION_LEVEL_REFERENCE"]
    if pressures!=["PVS-CNC-02.r2"]:
        raise Error(f"claim-carrier pressure drift: {pressures}")
    if projection["summary"]["architecture_gaps"]!=0:
        raise Error("summary architecture gap nonzero")
    if projection["summary"]["role_gap_count"]!=0:
        raise Error("summary role gap nonzero")
    if projection["summary"]["architecture_placeable_nonstrict_relations"]!=14:
        raise Error("summary nonstrict coverage drift")
    if projection["summary"]["claim_level_architecture_placeable"]!=16:
        raise Error("summary claim architecture coverage drift")

    evidence_rel={}
    for c in evidence["entries"]:
        for r in c["relations"]:
            key=f"{c['validation_claim_id']}.{r['relation_id']}"
            if key in evidence_rel:
                raise Error(f"duplicate evidence relation {key}")
            if r["evidence_level"] not in LEVELS:
                raise Error(f"bad evidence level {key}")
            evidence_rel[key]=r["evidence_level"]
    if set(evidence_rel)!=set(mapping_rel):
        raise Error("evidence/mapping relation membership mismatch")

    expected={
      "E0":{"DIRECT_L_SYS":22,"LAYER_RECOVERED":3,"ARCHITECTURE_GAP":0,"CARRIER_PRESSURE":0,"TOTAL":25},
      "E1":{"DIRECT_L_SYS":9,"LAYER_RECOVERED":6,"ARCHITECTURE_GAP":0,"CARRIER_PRESSURE":0,"TOTAL":15},
      "E2":{"DIRECT_L_SYS":4,"LAYER_RECOVERED":4,"ARCHITECTURE_GAP":0,"CARRIER_PRESSURE":0,"TOTAL":8},
      "E3":{"DIRECT_L_SYS":3,"LAYER_RECOVERED":1,"ARCHITECTURE_GAP":0,"CARRIER_PRESSURE":1,"TOTAL":4},
    }
    matrix={lv:{k:0 for k in ("DIRECT_L_SYS","LAYER_RECOVERED","ARCHITECTURE_GAP","CARRIER_PRESSURE","TOTAL")} for lv in LEVELS}
    for key,lv in evidence_rel.items():
        matrix[lv]["TOTAL"]+=1
        if mapping_rel[key]=="PRESERVED":
            matrix[lv]["DIRECT_L_SYS"]+=1
        elif key in rec_by:
            matrix[lv]["LAYER_RECOVERED"]+=1
            if rec_by[key]["carrier_status"]=="DESCRIPTION_LEVEL_REFERENCE":
                matrix[lv]["CARRIER_PRESSURE"]+=1
        else:
            matrix[lv]["ARCHITECTURE_GAP"]+=1

    for lv in LEVELS:
        for k,v in expected[lv].items():
            if matrix[lv][k]!=v:
                raise Error(f"{lv} {k}: expected {v}, got {matrix[lv][k]}")
        got=diagnostic["evidence_x_architecture_matrix"][lv]
        for k,v in expected[lv].items():
            if got[k]!=v:
                raise Error(f"diagnostic matrix drift {lv} {k}")
        coverage=(matrix[lv]["DIRECT_L_SYS"]+matrix[lv]["LAYER_RECOVERED"])/matrix[lv]["TOTAL"]
        if abs(got["architecture_coverage_rate"]-coverage)>1e-12:
            raise Error(f"{lv}: architecture coverage-rate drift")
        if coverage!=1.0:
            raise Error(f"{lv}: architecture coverage not complete")

    high={r["relation"] for r in diagnostic["high_evidence_recoveries"]}
    expected_high={
        "PVS-LRN-02.r1","PVS-ATT-02.r1","PVS-ATT-02.r3",
        "PVS-CNC-01.r3","PVS-CNC-02.r2"
    }
    if high!=expected_high:
        raise Error(f"high-evidence recovery membership drift: {sorted(high)}")

    cps=diagnostic["carrier_pressures"]
    if len(cps)!=1 or cps[0]["relation"]!="PVS-CNC-02.r2" or cps[0]["evidence_level"]!="E3":
        raise Error("E3 carrier-pressure diagnostic drift")

    return {
      "schema":"relay-theory.paper2.pvs16_layered_architecture_validation.v1",
      "status":"PASS",
      "claims":16,
      "relations":52,
      "direct_l_sys":38,
      "layer_recovered":14,
      "architecture_gaps":0,
      "role_gaps":0,
      "carrier_pressures":1,
      "evidence_matrix":matrix,
      "terminal":"PVS16_LAYERED_ARCHITECTURE_VALIDATION_PASS"
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
    print("PVS16_LAYERED_ARCHITECTURE_GATE_PASS")

if __name__=="__main__":
    main()
