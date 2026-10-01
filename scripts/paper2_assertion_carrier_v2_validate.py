#!/usr/bin/env python3
"""Validate AssertionCarrier v2 derivation and AHV-8 retrospective calibration."""
from __future__ import annotations

import argparse, json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT=Path("paper/validation/jgps-major-revision")
V1=ROOT/"l-claim-assertion-carrier-schema-v1.json"
V2=ROOT/"l-claim-assertion-carrier-schema-v2.json"
DER=ROOT/"assertion-carrier-v2-derivation-v1.json"
AHV1=ROOT/"ahv8-assertion-carrier-heldout-validation-v1.json"
CAL=ROOT/"ahv8-assertion-carrier-v2-retrospective-calibration-v1.json"
REV=ROOT/"ahv8-claimir-human-reviewed-v1"

IDS=("AHV-MEM-01","AHV-LRN-01","AHV-SKL-01","AHV-ATT-01","AHV-PRD-01","AHV-CTL-01","AHV-BLF-01","AHV-CNC-01")

class Error(ValueError): pass
def load(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding="utf-8"))

def validate()->dict[str,Any]:
    v1,v2,der,ahv1,cal=map(load,(V1,V2,DER,AHV1,CAL))
    if v2["status"]!="FROZEN_AHV8_DERIVED_PRE_NEW_HELDOUT_VALIDATION":
        raise Error("v2 status drift")
    if cal["status"]!="FROZEN_RETROSPECTIVE_CALIBRATION_NOT_INDEPENDENT_VALIDATION":
        raise Error("calibration status drift")
    if cal["calibration_boundary"]["independent_v2_validation_claimed"] is not False:
        raise Error("AHV-8 improperly claimed as independent v2 validation")
    if ahv1["terminal"]!="AHV8_HELDOUT_ASSERTION_CARRIER_REJECTS_V1_COMPLETENESS_WITH_11_OF_28_FULL_AND_17_GAPS":
        raise Error("v1 held-out failure authority drift")

    # strict additive superset
    for key in ("predicate_families","qualifiers","reference_roles","context_placement_classes","support_provenance_types"):
        old=set(v1[key]); new=set(v2[key])
        if not old <= new:
            raise Error(f"v2 removed v1 vocabulary from {key}")
    if set(v2["predicate_families"])-set(v1["predicate_families"]) != {"TRANSFORMATION"}:
        raise Error("new predicate family set drift")
    if set(v2["qualifiers"])-set(v1["qualifiers"]) != {"DISTINCT"}:
        raise Error("new qualifier set drift")
    if set(v2["reference_roles"])!=set(v1["reference_roles"]):
        raise Error("reference roles should be unchanged")
    if set(v2["context_placement_classes"])!=set(v1["context_placement_classes"]):
        raise Error("context classes should be unchanged")
    if set(v2["support_provenance_types"])!=set(v1["support_provenance_types"]):
        raise Error("support provenance types should be unchanged")
    if set(v2["architecture_layers"])-set(v1["architecture_layers"]) != {"L_claim"}:
        raise Error("only L_claim argument-binding layer should be added")
    if v2["claim_object_types"]!=["THEORETICAL_ACCOUNT"]:
        raise Error("claim object type drift")
    ext=v2["v2_extensions"]
    if ext["directionality"]["values"]!=["INCREASES","DECREASES","OPPOSITE_DIRECTION"]:
        raise Error("directionality values drift")
    if ext["evaluation"]["dimensions"]!=["EVIDENTIAL_SUPPORT","EMPIRICAL_FIT"]:
        raise Error("evaluation dimensions drift")

    ds=der["design_size"]
    expected_ds={"new_predicate_families":1,"new_qualifiers":1,"new_argument_binding_layers":1,"new_claim_object_types":1,"new_structured_modifier_fields":2,"new_reference_roles":0,"new_context_classes":0,"new_top_level_architecture_layers":0}
    if ds!=expected_ds:
        raise Error("design-size drift")

    v1g={e["assertion_id"]:e for e in ahv1["entries"] if e["carrier_status"]=="GAP"}
    v1f={e["assertion_id"]:e for e in ahv1["entries"] if e["carrier_status"]=="FULL"}
    if len(v1g)!=17 or len(v1f)!=11:
        raise Error("v1 held-out split drift")

    repairs={r["assertion_id"]:r for r in cal["repairs"]}
    if set(repairs)!=set(v1g):
        raise Error("v2 repair membership does not exactly equal v1 gap set")
    if len(repairs)!=17:
        raise Error("repair count drift")

    nodes={}
    for vid in IDS:
        c=load(REV/f"{vid}.json")
        nodes[vid]={n["id"]:n for n in c["claim_core"]["nodes"]}

    counts=Counter()
    for aid,r in repairs.items():
        src=v1g[aid]
        for k in ("validation_claim_id","claim_id","source_relation_id","source_kind","source_arguments","source_description"):
            if r[k]!=src[k]:
                raise Error(f"{aid}: source identity/content drift at {k}")
        if r["v1_gap_reasons"]!=src["gap_reasons"]:
            raise Error(f"{aid}: v1 gap reasons rewritten")
        if r["v2_carrier_status"]!="FULL":
            raise Error(f"{aid}: repair not FULL")
        if r["predicate_family"] not in v2["predicate_families"]:
            raise Error(f"{aid}: predicate outside v2")
        if any(q not in v2["qualifiers"] for q in r["qualifiers"]):
            raise Error(f"{aid}: qualifier outside v2")
        if [b["node_id"] for b in r["argument_bindings"]] != r["source_arguments"]:
            raise Error(f"{aid}: source argument binding order drift")
        uses_lclaim_object=False
        for b in r["argument_bindings"]:
            if b["layer"] not in v2["architecture_layers"]:
                raise Error(f"{aid}: bad binding layer")
            if b["layer"]=="L_claim":
                uses_lclaim_object=True
                if b.get("claim_object_type")!="THEORETICAL_ACCOUNT":
                    raise Error(f"{aid}: L_claim binding lacks THEORETICAL_ACCOUNT type")
                if nodes[r["validation_claim_id"]][b["node_id"]]["role"]!="other":
                    raise Error(f"{aid}: L_claim theory-object binding points to non-other ClaimIR node")
        if uses_lclaim_object:
            counts["l_claim_object_binding"]+=1
        if r["predicate_family"]=="TRANSFORMATION":
            counts["TRANSFORMATION"]+=1
        if "DISTINCT" in r["qualifiers"]:
            counts["DISTINCT"]+=1
        d=r["directionality"]
        if d is not None:
            counts["directionality"]+=1
            if d["kind"] not in v2["v2_extensions"]["directionality"]["values"]:
                raise Error(f"{aid}: bad directionality")
            if d["target_argument"] not in r["source_arguments"]:
                raise Error(f"{aid}: directionality target not in source arguments")
        ev=r["evaluation"]
        if ev is not None:
            counts["evaluation"]+=1
            if r["predicate_family"]!="COMPARISON":
                raise Error(f"{aid}: evaluation used outside COMPARISON")
            if ev["dimension"] not in v2["v2_extensions"]["evaluation"]["dimensions"]:
                raise Error(f"{aid}: bad evaluation dimension")
            if ev["preferred_argument"] not in r["source_arguments"]:
                raise Error(f"{aid}: preferred argument not in source arguments")

    expected_counts={"TRANSFORMATION":4,"DISTINCT":4,"directionality":7,"evaluation":2,"l_claim_object_binding":4}
    if dict(counts)!=expected_counts:
        raise Error(f"extension usage drift: {dict(counts)}")
    if cal["extension_usage_counts"]!=expected_counts:
        raise Error("calibration extension usage summary drift")
    b=cal["calibration_boundary"]
    if b["ahv8_relations"]!=28 or b["v1_full_carryover"]!=11 or b["v1_gaps_repaired"]!=17 or b["v2_retrospective_full"]!=28:
        raise Error("retrospective closure summary drift")

    return {
      "schema":"relay-theory.paper2.assertion_carrier_v2_derivation_validation.v1",
      "status":"PASS",
      "v1_heldout_full":11,
      "v1_heldout_gaps":17,
      "v2_retrospective_repairs":17,
      "v2_retrospective_total_full":28,
      "independent_v2_validation_claimed":False,
      "design_size":expected_ds,
      "extension_usage":expected_counts,
      "terminal":"ASSERTION_CARRIER_V2_DERIVATION_VALIDATION_PASS"
    }

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    a=validate(); b=validate()
    if a!=b: raise Error("non-deterministic validation")
    payload=json.dumps(a,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.output: args.output.write_text(payload,encoding="utf-8")
    else: print(payload,end="")
    print("ASSERTION_CARRIER_V2_DERIVATION_GATE_PASS")

if __name__=="__main__": main()
