#!/usr/bin/env python3
"""Read-only deterministic structural audit of the frozen AHV2-8 v2 held-out result.

This checks exact source membership, frozen file identities, v2 vocabulary, typed
bindings and all reported counts. It does NOT independently judge the semantic
correctness of expert FULL/GAP decisions.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT=Path("paper/validation/jgps-major-revision")
TARGET=ROOT/"ahv2-8-v2-heldout-target-freeze-v1.json"
PROTOCOL=ROOT/"ahv2-8-v2-heldout-adjudication-protocol-v1.json"
RESULT=ROOT/"ahv2-8-v2-heldout-validation-v1.json"
SCHEMA=ROOT/"l-claim-assertion-carrier-schema-v2.json"
REVIEW=ROOT/"ahv2-8-claimir-human-reviewed-v1"
PROGRESS=ROOT/"ahv2-8-human-review-progress-v1.json"
IDS=("AHV2-MEM-01","AHV2-LRN-01","AHV2-SKL-01","AHV2-ATT-01","AHV2-PRD-01","AHV2-CTL-01","AHV2-BLF-01","AHV2-CNC-01")

EXPECTED_PER_CLAIM=(("AHV2-MEM-01",4,0),("AHV2-LRN-01",0,3),
 ("AHV2-SKL-01",3,2),("AHV2-ATT-01",1,2),("AHV2-PRD-01",5,2),
 ("AHV2-CTL-01",0,4),("AHV2-BLF-01",3,1),("AHV2-CNC-01",0,4))
EXPECTED_FULL={
 "AHV2-MEM-01.r1","AHV2-MEM-01.r2","AHV2-MEM-01.r3","AHV2-MEM-01.r4",
 "AHV2-SKL-01.r1","AHV2-SKL-01.r3","AHV2-SKL-01.r5",
 "AHV2-ATT-01.r1",
 "AHV2-PRD-01.r2","AHV2-PRD-01.r3","AHV2-PRD-01.r5","AHV2-PRD-01.r6","AHV2-PRD-01.r7",
 "AHV2-BLF-01.r1","AHV2-BLF-01.r2","AHV2-BLF-01.r4"
}
ALLOWED_SCOPE={
 "under authors' proposed forward-model account",
 "based on reported experimental results",
}
EXPECTED_GAPS={
 "TEMPORAL_RELOCATION_FROM_TO_BINDING_MISSING":2,
 "STATISTICAL_SIGNIFICANCE_QUALIFIER_MISSING":2,
 "ACQUISITION_OR_EMERGENCE_MODIFIER_MISSING":1,
 "INTERRUPTION_OR_INTERFERENCE_PREDICATE_MISSING":1,
 "COMPONENT_ENCOMPASSMENT_PREDICATE_MISSING":1,
 "ARGUMENT_LOCAL_POSSIBILITY_MISSING":1,
 "DISTINCT_OUTCOME_CAUSATION_MAPPING_MISSING":1,
 "MULTI_OUTCOME_COMPARISON_DIRECTION_MISSING":1,
 "NECESSARY_CONDITION_MODALITY_MISSING":2,
 "TENTATIVE_NEURAL_INVOLVEMENT_PREDICATE_MISSING":1,
 "TENTATIVE_UNARY_STORAGE_LOCALIZATION_MISSING":1,
 "TRIADIC_PREFERENTIAL_ASSOCIATION_ORDERING_MISSING":1,
 "NONNECESSITY_OR_MAY_NOT_MODALITY_MISSING":1,
 "CLAIM_LEVEL_MODEL_FIT_RESULT_OBJECT_TYPE_MISSING":2,
 "MODEL_INFERENCE_EPISTEMIC_STATUS_MISSING":2
}
EXPECTED_USES={"TRANSFORMATION":2,"DISTINCT":3,"directionality":6,"evaluation":1,"lclaim_binding":3}

class Error(ValueError): pass
def load(p:Path)->dict[str,Any]:
    return json.loads(p.read_text(encoding="utf-8"))
def blob_sha(path:Path)->str:
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode("ascii")+b"\x00"+data).hexdigest()

def validate_payload(t:dict,s:dict,p:dict,r:dict,reviews:dict)->dict:
    if (t["status"],p["status"],r["status"])!=(
      "FROZEN_BEFORE_CARRIER_MAPPING","FROZEN_BEFORE_RESULT_MAPPING","FROZEN_HELDOUT_SEMANTIC_ADJUDICATION"):
        raise Error("target/protocol/result freeze status drift")
    if t["carrier_mapping_started"] is not False or t["carrier_v2_schema_tuning_forbidden"] is not True:
        raise Error("target not frozen pre-mapping")
    if p["target_freeze_commit"]!=r["authority"]["target_freeze_commit"]:
        raise Error("protocol/target commit identity mismatch")
    if s["status"]!="FROZEN_AHV8_DERIVED_PRE_NEW_HELDOUT_VALIDATION":
        raise Error("v2 schema status drift")
    if r["no_tuning"]!={"schema_modified":False,"predicate_family_added":False,
          "qualifier_added":False,"reference_role_added":False,"claim_object_type_added":False,
          "reviewed_source_relation_dropped":False}:
        raise Error("no-tuning receipts drift")
    if t["summary"]["claims"]!=8 or t["summary"]["relations"]!=34:
        raise Error("target count drift")
    if [x["validation_claim_id"] for x in t["claims"]]!=list(IDS):
        raise Error("target claim order or membership drift")

    target={}
    nodeby={}
    for c in t["claims"]:
        vid=c["validation_claim_id"]
        reviewed=reviews[vid]
        if reviewed["extraction"]["manual_review_status"]!="reviewed":
            raise Error(f"{vid}: candidate was not author reviewed")
        if c["claim_id"]!=reviewed["claim_id"] or c["source_identity"]!=reviewed["provenance"]["paper_id"]:
            raise Error(f"{vid}: claim/source identity drift")
        n1={n["id"]:(n["role"],n["description"]) for n in reviewed["claim_core"]["nodes"]}
        n2={n["id"]:(n["claimir_role"],n["description"]) for n in c["source_nodes"]}
        if n1!=n2:
            raise Error(f"{vid}: frozen source nodes drift")
        nodeby[vid]=n1
        rels=reviewed["claim_core"]["relations"]
        if len(c["relations"])!=len(rels):
            raise Error(f"{vid}: relation count drift")
        for tr,sr in zip(c["relations"],rels):
            aid=vid+"."+sr["id"]
            expected={
                "assertion_id":aid,"source_relation_id":sr["id"],"source_kind":sr["kind"],
                "source_arguments":sr["arguments"],"source_description":sr["description"],
                "source_span_ids":sr["source_span_ids"]
            }
            if tr!=expected or aid in target:
                raise Error(f"{aid}: source target drift or duplicate")
            target[aid]=(vid,c["claim_id"],tr)
    if len(target)!=34: raise Error("target membership/size drift")
    entries=r["entries"]
    if [e["assertion_id"] for e in entries]!=list(target):
        raise Error("result must enumerate exact frozen targets in frozen order")
    if {e["assertion_id"] for e in entries if e["carrier_status"]=="FULL"}!=EXPECTED_FULL:
        raise Error("frozen FULL/GAP verdict membership drift")

    families=set(s["predicate_families"]); qualifiers=set(s["qualifiers"])
    roles=set(s["reference_roles"]); layers=set(s["architecture_layers"])
    ctx_classes=set(s["context_placement_classes"]); claim_types=set(s["claim_object_types"])
    provtypes=set(s["support_provenance_types"])
    counts=Counter();gap_counts=Counter();uses=Counter();per=Counter();full_claims=0

    def checkbinding(aid,vid,b):
        if b["node_id"] not in nodeby[vid]:
            raise Error(f"{aid}: nonexistent ClaimIR node {b['node_id']}")
        if b["semantic_role"] not in roles or b["layer"] not in layers:
            raise Error(f"{aid}: unsupported reference role/layer")
        nr,description=nodeby[vid][b["node_id"]]
        layer=b["layer"]
        if layer=="L_claim":
            if b.get("claim_object_type") not in claim_types or nr!="other":
                raise Error(f"{aid}: L_claim binding must be typed actual theoretical account")
            if "account" not in description.lower():
                raise Error(f"{aid}: L_claim theoretical-account binding points at non-account")
        elif layer=="L_ctx":
            if b.get("context_placement") not in ctx_classes:
                raise Error(f"{aid}: missing valid context class")
            if nr!="condition":
                raise Error(f"{aid}: context binding is not a condition node")
        elif layer=="L_sys":
            if b.get("system_role") not in {"Pi","X","C","Q","P_in","P_out","K","T","rho/O"}:
                raise Error(f"{aid}: unsupported system role")
            if nr in {"condition","other"} or "relative fit" in description.lower():
                raise Error(f"{aid}: non-system or model-fit node incorrectly bound to L_sys")

    for e in entries:
        aid=e["assertion_id"]
        vid,claim_id,tgt=target[aid]
        for k in ("source_relation_id","source_kind","source_arguments","source_description","source_span_ids"):
            if e[k]!=tgt[k]: raise Error(f"{aid}: source {k} changed")
        if e["validation_claim_id"]!=vid or e["claim_id"]!=claim_id:
            raise Error(f"{aid}: claim ID drift")
        per[vid]+=1
        if e["carrier_status"]=="FULL":
            counts["FULL"]+=1
            if e["predicate_family"] not in families or any(q not in qualifiers for q in e["qualifiers"]):
                raise Error(f"{aid}: outside frozen predicate or qualifier vocabulary")
            if [b["node_id"] for b in e["argument_bindings"]]!=tgt["source_arguments"]:
                raise Error(f"{aid}: bound argument order/content drift")
            for b in e["argument_bindings"]:checkbinding(aid,vid,b)
            for b in e["semantic_references"]:
                if b["node_id"] in tgt["source_arguments"]:
                    raise Error(f"{aid}: semantic reference duplicates source argument")
                checkbinding(aid,vid,b)
            if e["support_provenance"]:
                for item in e["support_provenance"]:
                    if item.get("type") not in provtypes:raise Error(f"{aid}: unknown provenance type")
            if set(e["assertion_scope_qualifiers"])-ALLOWED_SCOPE:
                raise Error(f"{aid}: scope qualifier attempts core-semantic escape")
            d=e["directionality"]
            if d is not None:
                if d["kind"] not in s["v2_extensions"]["directionality"]["values"] or d["target_argument"] not in tgt["source_arguments"]:
                    raise Error(f"{aid}: unsupported or unanchored directionality")
                uses["directionality"]+=1
            ev=e["evaluation"]
            if ev is not None:
                if e["predicate_family"]!="COMPARISON" or ev["dimension"] not in s["v2_extensions"]["evaluation"]["dimensions"] or ev["preferred_argument"] not in tgt["source_arguments"]:
                    raise Error(f"{aid}: unsupported/unanchored evaluation")
                uses["evaluation"]+=1
            if e["gap_reasons"]:raise Error(f"{aid}: FULL entry contains gap reasons")
            if e["predicate_family"]=="TRANSFORMATION":uses["TRANSFORMATION"]+=1
            if "DISTINCT" in e["qualifiers"]:uses["DISTINCT"]+=1
            if any(b["layer"]=="L_claim" for b in e["argument_bindings"]+e["semantic_references"]):
                uses["lclaim_binding"]+=1
            per[vid+":full"]+=1
        elif e["carrier_status"]=="GAP":
            counts["GAP"]+=1
            if not e["gap_reasons"]:raise Error(f"{aid}: missing GAP reason")
            if e["attempted_predicate_family"] is not None and e["attempted_predicate_family"] not in families:
                raise Error(f"{aid}: attempted predicate not in frozen vocabulary")
            if any(q not in qualifiers for q in e["attempted_qualifiers"]):
                raise Error(f"{aid}: attempted qualifier outside frozen vocabulary")
            if e["provisional_argument_bindings"] or e["semantic_references"] or e["assertion_scope_qualifiers"]:
                raise Error(f"{aid}: GAP has unexplained provisional semantic escapes")
            gap_counts.update(e["gap_reasons"])
        else:raise Error(f"{aid}: invalid verdict")
        if not e["adjudication_note"]:
            raise Error(f"{aid}: reasoned adjudication note required")

    if (counts["FULL"],counts["GAP"])!=(16,18):
        raise Error("result totals drift")
    if dict(gap_counts)!=EXPECTED_GAPS:
        raise Error("gap taxonomy counts drift")
    if dict(uses)!=EXPECTED_USES:
        raise Error("extension usage counts drift")
    per_claim=[]
    for vid,f,g in EXPECTED_PER_CLAIM:
        if per[vid]!=(f+g) or per[vid+":full"]!=f:
            raise Error(f"{vid}: per-claim result counts drift")
        per_claim.append({
          "validation_claim_id":vid,"relations":f+g,"full":f,"gap":g,
          "claim_status":"FULL" if g==0 else "GAP"
        })
        if g==0:full_claims+=1
    expected_summary={
      "claims":8,"relations":34,"full_relations":16,"gap_relations":18,
      "full_rate":16/34,"full_claims":full_claims,"gap_claims":8-full_claims,
      "per_claim":per_claim,"gap_reason_counts":EXPECTED_GAPS,
      "extension_use_relations":EXPECTED_USES
    }
    if r["summary"]!=expected_summary:
        raise Error("reported summary not recomputable from frozen entries")
    if r["terminal"]!="AHV2_8_V2_HELDOUT_RESULT_16_OF_34_FULL_18_GAP":
        raise Error("result terminal drift")

    return {"schema":"relay-theory.paper2.ahv2_8_v2_heldout_validation_receipt.v1",
      "status":"PASS","claims":8,"relations":34,"full_relations":16,"gap_relations":18,
      "full_claims":full_claims,"gap_claims":8-full_claims,
      "extension_use_relations":EXPECTED_USES,
      "limit":"Structural/data-fidelity verification; does not independently verify semantic verdicts.",
      "terminal":"AHV2_8_V2_HELDOUT_STRUCTURE_AND_VOCABULARY_GATE_PASS"}

def validate()->dict:
    t,p,r,s=map(load,(TARGET,PROTOCOL,RESULT,SCHEMA))
    if r["authority"]["target_freeze_blob_sha"]!=blob_sha(TARGET) or r["authority"]["adjudication_protocol_blob_sha"]!=blob_sha(PROTOCOL) or r["authority"]["v2_schema_blob_sha"]!=blob_sha(SCHEMA):
        raise Error("frozen authority blob drift")
    if t["authority"]["v2_schema_blob_sha"]!=blob_sha(SCHEMA):
        raise Error("target schema identity drift")
    if r["authority"]["author_review_main_commit"]!=t["authority"]["reviewed_main_commit"]:
        raise Error("review main identity drift")
    reviews={}
    for c in t["claims"]:
        vid=c["validation_claim_id"]
        path=REVIEW/f"{vid}.json"
        if c["reviewed_claimir_blob_sha"]!=blob_sha(path):
            raise Error(f"{vid}: reviewed ClaimIR file hash drift")
        reviews[vid]=load(path)
    progress=load(PROGRESS)
    if (progress["status"],progress["reviewed_count"],progress["assertion_carrier_v2_validation_authorized"])!=("COMPLETE",8,True):
        raise Error("human gate invalid")
    return validate_payload(t,s,p,r,reviews)

def negative_tests()->list[str]:
    t,p,r,s=map(load,(TARGET,PROTOCOL,RESULT,SCHEMA))
    reviews={c["validation_claim_id"]:load(REVIEW/f'{c["validation_claim_id"]}.json') for c in t["claims"]}
    probes=[]
    def must_fail(name,fn):
        try:fn()
        except Error:probes.append(name)
        else:raise Error(f"negative fixture incorrectly PASS: {name}")
    def check(t1,s1,p1,r1):return validate_payload(t1,s1,p1,r1,reviews)
    x=copy.deepcopy(r);x["entries"].pop()
    must_fail("dropped_relation",lambda:check(t,s,p,x))
    x=copy.deepcopy(r);e=next(y for y in x["entries"] if y["assertion_id"]=="AHV2-MEM-01.r1");e["argument_bindings"].reverse()
    must_fail("reordered_source_binding",lambda:check(t,s,p,x))
    x=copy.deepcopy(r);e=next(y for y in x["entries"] if y["assertion_id"]=="AHV2-PRD-01.r2");e["directionality"]["kind"]="BIGGER"
    must_fail("new_directionality",lambda:check(t,s,p,x))
    x=copy.deepcopy(r);e=next(y for y in x["entries"] if y["assertion_id"]=="AHV2-MEM-01.r1");e["argument_bindings"][0]["layer"]="L_sys";e["argument_bindings"][0]["system_role"]="X"
    must_fail("theory_misbound_system",lambda:check(t,s,p,x))
    x=copy.deepcopy(r);e=next(y for y in x["entries"] if y["assertion_id"]=="AHV2-LRN-01.r2");e["carrier_status"]="FULL";e["predicate_family"]="ASSOCIATION";e["qualifiers"]=[];e["argument_bindings"]=[{"node_id":"ventral_striatal_response","semantic_role":"ASSOCIAND","layer":"L_sys","system_role":"rho/O"},{"node_id":"prediction_error_signal","semantic_role":"ASSOCIAND","layer":"L_sys","system_role":"X"}];e["directionality"]=None;e["evaluation"]=None
    must_fail("unsupported_verdict_flip",lambda:check(t,s,p,x))
    return probes

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    a=validate();b=validate()
    if a!=b:raise Error("nondeterministic receipt")
    a["negative_tests"]=negative_tests()
    payload=json.dumps(a,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.output:args.output.write_text(payload,encoding="utf-8")
    else:print(payload,end="")
    print("AHV2_8_V2_HELDOUT_GATE_PASS")

if __name__=="__main__": main()
