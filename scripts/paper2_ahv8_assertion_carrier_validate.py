#!/usr/bin/env python3
"""Validate AHV-8 held-out AssertionCarrier v1 result."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT=Path("paper/validation/jgps-major-revision")
SCHEMA=ROOT/"l-claim-assertion-carrier-schema-v1.json"
TARGET=ROOT/"ahv8-assertion-carrier-target-freeze-v1.json"
RESULT=ROOT/"ahv8-assertion-carrier-heldout-validation-v1.json"
REV=ROOT/"ahv8-claimir-human-reviewed-v1"

IDS=(
 "AHV-MEM-01","AHV-LRN-01","AHV-SKL-01","AHV-ATT-01",
 "AHV-PRD-01","AHV-CTL-01","AHV-BLF-01","AHV-CNC-01",
)

EXPECTED_STATUS={
 "AHV-MEM-01.r1":"FULL","AHV-MEM-01.r2":"GAP","AHV-MEM-01.r3":"GAP",
 "AHV-LRN-01.r1":"FULL","AHV-LRN-01.r2":"FULL","AHV-LRN-01.r3":"FULL","AHV-LRN-01.r4":"FULL",
 "AHV-SKL-01.r1":"GAP","AHV-SKL-01.r2":"FULL","AHV-SKL-01.r3":"FULL","AHV-SKL-01.r4":"GAP",
 "AHV-ATT-01.r1":"GAP","AHV-ATT-01.r2":"GAP","AHV-ATT-01.r3":"GAP","AHV-ATT-01.r4":"GAP",
 "AHV-PRD-01.r1":"FULL","AHV-PRD-01.r2":"GAP",
 "AHV-CTL-01.r1":"GAP","AHV-CTL-01.r2":"FULL","AHV-CTL-01.r3":"FULL",
 "AHV-BLF-01.r1":"GAP","AHV-BLF-01.r2":"GAP","AHV-BLF-01.r3":"GAP","AHV-BLF-01.r4":"GAP",
 "AHV-CNC-01.r1":"GAP","AHV-CNC-01.r2":"FULL","AHV-CNC-01.r3":"GAP","AHV-CNC-01.r4":"GAP",
}

EXPECTED_GAP_COUNTS={
 "ARGUMENT_LAYER_L_CLAIM_OR_THEORY_OBJECT_MISSING":4,
 "QUALIFIER_BETTER_SUPPORTED_OR_PREFERENCE_MISSING":1,
 "QUALIFIER_INCREASES_MISSING":3,
 "QUALIFIER_INCREASES_OR_FASTER_MISSING":1,
 "QUALIFIER_DECREASES_MISSING":1,
 "QUALIFIER_OPPOSITE_DIRECTION_MISSING":1,
 "QUALIFIER_NEGATIVE_EFFECT_OR_LIMITATION_MISSING":1,
 "PREDICATE_MAPPING_OR_TRANSFORMATION_MISSING":4,
 "PREDICATE_DISTINCTION_MISSING":1,
 "QUALIFIER_DISTINCT_OR_DIFFERENT_TARGET_MISSING":1,
 "QUALIFIER_BETTER_FIT_OR_MODEL_PREFERENCE_MISSING":1,
}

class Error(ValueError):
    pass

def load(p:Path)->dict[str,Any]:
    return json.loads(p.read_text(encoding="utf-8"))

def validate()->dict[str,Any]:
    schema=load(SCHEMA)
    target=load(TARGET)
    result=load(RESULT)

    if schema["status"]!="FROZEN_PVS_CALIBRATED_ASSERTION_CARRIER_SCHEMA":
        raise Error("carrier schema status drift")
    if target["status"]!="FROZEN_PRE_MAPPING_TARGET_SET":
        raise Error("target freeze status drift")
    if target["carrier_mapping_started"] is not False:
        raise Error("target was not frozen pre-mapping")
    if target["schema_tuning_after_target_freeze_forbidden"] is not True:
        raise Error("target freeze lacks no-tuning guardrail")
    if target["summary"]!={"claims":8,"relations":28}:
        raise Error("target count drift")
    if result["status"]!="FROZEN_HELDOUT_RESULT":
        raise Error("result status drift")

    if result["no_tuning"] != {
      "schema_modified":False,
      "predicate_family_added":False,
      "qualifier_added":False,
      "reference_role_added":False,
      "context_class_added":False,
      "target_relation_dropped":False,
    }:
        raise Error("no-tuning receipt drift")

    target_rel={}
    for c in target["claims"]:
        for r in c["relations"]:
            aid=r["assertion_id"]
            if aid in target_rel:
                raise Error(f"duplicate target {aid}")
            target_rel[aid]=r
    if len(target_rel)!=28:
        raise Error("target relation count != 28")

    entries=result["entries"]
    by={e["assertion_id"]:e for e in entries}
    if len(by)!=28 or set(by)!=set(target_rel):
        raise Error("result target membership mismatch")
    if {k:v["carrier_status"] for k,v in by.items()}!=EXPECTED_STATUS:
        raise Error("held-out FULL/GAP verdict drift")

    families=set(schema["predicate_families"])
    qualifiers=set(schema["qualifiers"])
    roles=set(schema["reference_roles"])
    layers=set(schema["architecture_layers"])
    ctx_classes=set(schema["context_placement_classes"])
    prov_types=set(schema["support_provenance_types"])

    claim_nodes={}
    for vid in IDS:
        claim=load(REV/f"{vid}.json")
        claim_nodes[vid]={n["id"] for n in claim["claim_core"]["nodes"]}

    full_count=0
    gap_count=0
    gap_counts=Counter()
    semantic_ref_ids=[]

    for aid,e in by.items():
        t=target_rel[aid]
        if e["source_relation_id"]!=t["source_relation_id"]:
            raise Error(f"{aid}: source relation id drift")
        if e["source_kind"]!=t["source_kind"]:
            raise Error(f"{aid}: source kind drift")
        if e["source_arguments"]!=t["source_arguments"]:
            raise Error(f"{aid}: source argument drift")
        if e["source_description"]!=t["description"]:
            raise Error(f"{aid}: source description drift")

        vid=e["validation_claim_id"]
        if e["carrier_status"]=="FULL":
            full_count+=1
            if e["predicate_family"] not in families:
                raise Error(f"{aid}: predicate outside frozen schema")
            if any(q not in qualifiers for q in e["qualifiers"]):
                raise Error(f"{aid}: qualifier outside frozen schema")
            bindings=e["argument_bindings"]
            if [b["node_id"] for b in bindings] != e["source_arguments"]:
                raise Error(f"{aid}: FULL bindings do not preserve source-argument order")
            for b in bindings:
                if b["semantic_role"] not in roles:
                    raise Error(f"{aid}: reference role outside frozen schema")
                if b["layer"] not in layers:
                    raise Error(f"{aid}: binding layer outside frozen schema")
                if b["layer"]=="L_ctx" and b.get("context_placement") not in ctx_classes:
                    raise Error(f"{aid}: context class outside frozen schema")
            for sr in e["semantic_references"]:
                semantic_ref_ids.append(aid)
                if sr["node_id"] in e["source_arguments"]:
                    raise Error(f"{aid}: semantic reference duplicates source argument")
                if sr["node_id"] not in claim_nodes[vid]:
                    raise Error(f"{aid}: semantic reference is not an existing ClaimIR node")
                if sr["semantic_role"] not in roles:
                    raise Error(f"{aid}: semantic-reference role outside schema")
                if sr["layer"] not in layers:
                    raise Error(f"{aid}: semantic-reference layer outside schema")
                if sr["layer"]=="L_ctx" and sr.get("context_placement") not in ctx_classes:
                    raise Error(f"{aid}: semantic-reference context class outside schema")
            for p in e["support_provenance"]:
                if p["type"] not in prov_types:
                    raise Error(f"{aid}: provenance type outside schema")
            if e["gap_reasons"]:
                raise Error(f"{aid}: FULL entry has gap reasons")
        elif e["carrier_status"]=="GAP":
            gap_count+=1
            if not e["gap_reasons"]:
                raise Error(f"{aid}: GAP entry lacks gap reason")
            for g in e["gap_reasons"]:
                gap_counts[g]+=1
            fam=e.get("attempted_predicate_family")
            if fam is not None and fam not in families:
                raise Error(f"{aid}: attempted family is not frozen vocabulary")
            if any(q not in qualifiers for q in e.get("attempted_qualifiers",[])):
                raise Error(f"{aid}: attempted qualifier is not frozen vocabulary")
        else:
            raise Error(f"{aid}: bad carrier status")

    if (full_count,gap_count)!=(11,17):
        raise Error(f"coverage drift FULL={full_count} GAP={gap_count}")
    if dict(gap_counts)!=EXPECTED_GAP_COUNTS:
        raise Error(f"gap-reason count drift: {dict(gap_counts)}")
    if semantic_ref_ids!=["AHV-LRN-01.r4"]:
        raise Error(f"semantic-reference case drift: {semantic_ref_ids}")

    summary=result["summary"]
    if summary["full_relations"]!=11 or summary["gap_relations"]!=17:
        raise Error("summary relation counts drift")
    if summary["full_claims"]!=1 or summary["gap_claims"]!=7:
        raise Error("summary claim counts drift")
    if abs(summary["relation_full_rate"]-(11/28))>1e-12:
        raise Error("summary rate drift")
    cs={x["validation_claim_id"]:x for x in summary["claim_summaries"]}
    if cs["AHV-LRN-01"]["claim_status"]!="FULL":
        raise Error("LRN claim should be the sole FULL claim")
    if sum(x["claim_status"]=="FULL" for x in cs.values())!=1:
        raise Error("FULL claim membership drift")
    if summary["gap_reason_counts"]!=EXPECTED_GAP_COUNTS:
        raise Error("summary gap-reason counts drift")
    if summary["added_semantic_reference_instances"]!=["AHV-LRN-01.r4"]:
        raise Error("summary semantic-reference drift")

    return {
      "schema":"relay-theory.paper2.ahv8_assertion_carrier_heldout_validation_receipt.v1",
      "status":"PASS",
      "claims":8,
      "relations":28,
      "full_relations":11,
      "gap_relations":17,
      "full_claims":1,
      "gap_claims":7,
      "semantic_reference_cases":["AHV-LRN-01.r4"],
      "terminal":"AHV8_ASSERTION_CARRIER_HELDOUT_VALIDATION_PASS",
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
    print("AHV8_ASSERTION_CARRIER_HELDOUT_GATE_PASS")

if __name__=="__main__":
    main()
