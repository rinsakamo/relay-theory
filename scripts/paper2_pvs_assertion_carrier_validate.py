#!/usr/bin/env python3
"""Validate frozen PVS-calibrated L_claim AssertionCarrier artifacts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT=Path("paper/validation/jgps-major-revision")
SCHEMA=ROOT/"l-claim-assertion-carrier-schema-v1.json"
CAL=ROOT/"pvs16-l-claim-assertion-carrier-calibration-v1.json"
LAYERED=ROOT/"pvs16-layered-architecture-projection-v1.json"
CLAIMS=ROOT/"pvs16-claimir-human-reviewed-v1"

ALLOWED_LAYERS={"L_sys","L_ctx"}

class Error(ValueError):
    pass

def load(p:Path)->dict[str,Any]:
    return json.loads(p.read_text(encoding="utf-8"))

def validate()->dict[str,Any]:
    schema=load(SCHEMA)
    cal_raw=CAL.read_text(encoding="utf-8")
    cal=json.loads(cal_raw)
    layered=load(LAYERED)

    if schema["status"]!="FROZEN_PVS_CALIBRATED_ASSERTION_CARRIER_SCHEMA":
        raise Error("schema status drift")
    if schema["scope_boundary"]["independent_validation_claimed"] is not False:
        raise Error("schema improperly claims independent validation")
    if cal["status"]!="FROZEN_PVS_CALIBRATION":
        raise Error("calibration status drift")
    if cal["calibration_boundary"]["independent_validation_claimed"] is not False:
        raise Error("calibration improperly claims independent validation")
    if '"evidence_level"' in cal_raw:
        raise Error("evidence annotation leaked into assertion carrier calibration")

    instances=cal["instances"]
    if len(instances)!=14:
        raise Error(f"expected 14 instances, got {len(instances)}")
    ids=[x["assertion_id"] for x in instances]
    if len(ids)!=len(set(ids)):
        raise Error("duplicate assertion_id")

    expected_nonstrict={r["relation"] for r in layered["nonstrict_relation_recoveries"]}
    if set(ids)!=expected_nonstrict:
        raise Error(f"carrier membership mismatch expected={sorted(expected_nonstrict)} got={sorted(ids)}")

    families=set(schema["predicate_families"])
    qualifiers=set(schema["qualifiers"])
    ref_roles=set(schema["reference_roles"])
    ctx_classes=set(schema["context_placement_classes"])

    claim_cache={}
    for inst in instances:
        vid=inst["validation_claim_id"]
        if vid not in claim_cache:
            claim_cache[vid]=load(CLAIMS/f"{vid}.json")
        claim=claim_cache[vid]
        if claim["claim_id"]!=inst["claim_id"]:
            raise Error(f"{inst['assertion_id']}: claim_id mismatch")

        nodes={n["id"]:n for n in claim["claim_core"]["nodes"]}
        rels={r["id"]:r for r in claim["claim_core"]["relations"]}
        rid=inst["source_relation_id"]
        if rid not in rels:
            raise Error(f"{inst['assertion_id']}: missing source relation")
        rel=rels[rid]
        if inst["source_kind"]!=rel["kind"]:
            raise Error(f"{inst['assertion_id']}: source kind drift")
        if inst["source_arguments"]!=rel["arguments"]:
            raise Error(f"{inst['assertion_id']}: source argument drift")

        if inst["predicate_family"] not in families:
            raise Error(f"{inst['assertion_id']}: bad predicate family")
        if len(inst["qualifiers"])!=len(set(inst["qualifiers"])):
            raise Error(f"{inst['assertion_id']}: duplicate qualifier")
        if any(q not in qualifiers for q in inst["qualifiers"]):
            raise Error(f"{inst['assertion_id']}: bad qualifier")

        bindings=inst["argument_bindings"]
        bound=[b["node_id"] for b in bindings]
        if bound!=inst["source_arguments"]:
            raise Error(f"{inst['assertion_id']}: bindings must exactly preserve source argument order")
        if any(b["semantic_role"] not in ref_roles for b in bindings):
            raise Error(f"{inst['assertion_id']}: bad argument semantic role")
        for b in bindings:
            if b["node_id"] not in nodes:
                raise Error(f"{inst['assertion_id']}: unknown bound node")
            if b["layer"] not in ALLOWED_LAYERS:
                raise Error(f"{inst['assertion_id']}: bad layer")
            if b["layer"]=="L_ctx":
                if b.get("context_placement") not in ctx_classes:
                    raise Error(f"{inst['assertion_id']}: bad context placement")
                if "system_role" in b:
                    raise Error(f"{inst['assertion_id']}: L_ctx binding has system_role")
            else:
                if not b.get("system_role"):
                    raise Error(f"{inst['assertion_id']}: L_sys binding lacks system_role")
                if "context_placement" in b:
                    raise Error(f"{inst['assertion_id']}: L_sys binding has context placement")

        seen_refs=set()
        for sr in inst["semantic_references"]:
            nid=sr["node_id"]
            if nid in seen_refs:
                raise Error(f"{inst['assertion_id']}: duplicate semantic reference")
            seen_refs.add(nid)
            if nid not in nodes:
                raise Error(f"{inst['assertion_id']}: unknown semantic reference {nid}")
            if nid in inst["source_arguments"]:
                raise Error(f"{inst['assertion_id']}: semantic reference duplicates source argument {nid}")
            if sr["semantic_role"] not in ref_roles:
                raise Error(f"{inst['assertion_id']}: bad semantic-reference role")
            if sr["layer"] not in ALLOWED_LAYERS:
                raise Error(f"{inst['assertion_id']}: bad semantic-reference layer")

        if inst["carrier_status"] not in {"FULL","GAP"}:
            raise Error(f"{inst['assertion_id']}: bad carrier status")

    semantic_ref_cases=[x for x in instances if x["semantic_references"]]
    if len(semantic_ref_cases)!=1 or semantic_ref_cases[0]["assertion_id"]!="PVS-CNC-02.r2":
        raise Error("unexpected semantic-reference case set")
    sr=semantic_ref_cases[0]["semantic_references"][0]
    if (sr["node_id"],sr["semantic_role"],sr["layer"],sr["system_role"])!=("causal_position","EXPLANANS","L_sys","X"):
        raise Error("PVS-CNC-02.r2 semantic reference drift")
    cnc02=claim_cache["PVS-CNC-02"]
    desc=next(r for r in cnc02["claim_core"]["relations"] if r["id"]=="r2")["description"]
    if "causal position" not in desc.lower():
        raise Error("PVS-CNC-02.r2 frozen description no longer requires causal position")

    prov_cases=[x for x in instances if x["support_provenance"]]
    if len(prov_cases)!=1 or prov_cases[0]["assertion_id"]!="PVS-CNC-01.r3":
        raise Error("unexpected support-provenance case set")
    prov=prov_cases[0]["support_provenance"][0]
    if prov["type"]!="EXPERIMENTAL_MANIPULATION_REPORTED" or prov["creates_p_in"] is not False:
        raise Error("PVS-CNC-01.r3 provenance drift")
    cnc01=claim_cache["PVS-CNC-01"]
    if any(n["role"]=="intervention" for n in cnc01["claim_core"]["nodes"]):
        raise Error("PVS-CNC-01 unexpectedly has an intervention node; provenance rule must be revisited")

    if any(x["carrier_status"]!="FULL" for x in instances):
        raise Error("carrier gap present in frozen calibration")

    summary=cal["summary"]
    if summary["instances"]!=14 or summary["full"]!=14 or summary["gaps"]!=0:
        raise Error("calibration summary drift")
    if summary["added_semantic_reference_count"]!=1:
        raise Error("semantic reference count drift")
    if summary["assertions_with_added_semantic_references"]!=["PVS-CNC-02.r2"]:
        raise Error("semantic-reference summary drift")
    if summary["assertions_with_relation_level_support_provenance"]!=["PVS-CNC-01.r3"]:
        raise Error("support-provenance summary drift")

    return {
        "schema":"relay-theory.paper2.assertion_carrier_calibration_validation.v1",
        "status":"PASS",
        "calibration_instances":14,
        "full":14,
        "gaps":0,
        "predicate_families_used":len({x["predicate_family"] for x in instances}),
        "added_semantic_references":1,
        "support_provenance_cases":1,
        "independent_validation_claimed":False,
        "terminal":"PVS14_ASSERTION_CARRIER_CALIBRATION_VALIDATION_PASS",
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
    print("PVS14_ASSERTION_CARRIER_CALIBRATION_GATE_PASS")

if __name__=="__main__":
    main()
