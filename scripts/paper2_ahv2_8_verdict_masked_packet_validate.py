#!/usr/bin/env python3
"""Read-only integrity gate for the 34-case verdict-masked AHV2-8 author challenge.

Confirms frozen ClaimIR/target identity, source-only presentation, a fixed
bijection, frozen v2 vocabulary, and an empty pre-review progress receipt.
Does not establish blinded author memory or external reviewer independence.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT=Path("paper/validation/jgps-major-revision")
PROTOCOL=ROOT/"ahv2-8-verdict-masked-protocol-v1.json"
PACKET=ROOT/"ahv2-8-verdict-masked-reviewer-packet-v1.json"
PROGRESS=ROOT/"ahv2-8-verdict-masked-progress-v1.json"
TARGET=ROOT/"ahv2-8-v2-heldout-target-freeze-v1.json"
ADMISSION=ROOT/"ahv2-8-admission-v1.json"
SOURCE=ROOT/"ahv2-8-source-authority-v1.json"
SCHEMA=ROOT/"l-claim-assertion-carrier-schema-v2.json"
REVIEWED=ROOT/"ahv2-8-claimir-human-reviewed-v1"
IDS=("AHV2-MEM-01","AHV2-LRN-01","AHV2-SKL-01","AHV2-ATT-01","AHV2-PRD-01","AHV2-CTL-01","AHV2-BLF-01","AHV2-CNC-01")

class Error(ValueError):pass

def load(p:Path)->dict:
    return json.loads(p.read_text(encoding="utf-8"))

def blob(p:Path)->str:
    b=p.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\x00"+b).hexdigest()

def check(protocol,packet,progress,target,admission,source,schema,reviewed):
    if protocol["status"]!="FROZEN_BEFORE_AUTHOR_REVIEW":
        raise Error("review protocol status drift")
    if protocol["sampling"]["population"]!="all 34 relations in frozen AHV2-8 target, no exclusions":
        raise Error("sampling target drift")
    if packet["status"]!="FROZEN_BEFORE_REVIEW" or packet["case_count"]!=34:
        raise Error("packet status/membership drift")
    if packet["protocol_commit"]!="cd0c28bb1a77755b4f007d6d09338a36d29ca4c1":
        raise Error("packet protocol commit drift")
    if (packet["previous_verdicts_disclosed"],packet["previous_mappings_disclosed"],packet["old_gap_reasons_disclosed"])!=(False,False,False):
        raise Error("prior verdict leakage receipt")
    if protocol["comparison_lock"].startswith("Do not compare") is False:
        raise Error("comparison lock drift")
    if schema["status"]!="FROZEN_AHV8_DERIVED_PRE_NEW_HELDOUT_VALIDATION":
        raise Error("v2 authority status drift")
    v=packet["frozen_v2_vocabulary"]
    for a,b in (("predicate_families","predicate_families"),("qualifiers","qualifiers"),
                ("reference_roles","reference_roles"),("architecture_layers","architecture_layers"),
                ("claim_object_types","claim_object_types"),("context_placement_classes","context_placement_classes")):
        if v[a]!=schema[b]:raise Error("v2 vocabulary drift: "+a)
    for k in ("directionality","evaluation"):
        if v[k]!=schema["v2_extensions"][k]:raise Error("v2 modifier drift: "+k)

    if [x["validation_claim_id"] for x in target["claims"]]!=list(IDS):
        raise Error("target claim order drift")
    admissions={x["validation_claim_id"]:x for x in admission["admissions"]}
    sources={x["validation_claim_id"]:x for x in source["entries"]}
    all_rel=[(c,r) for c in target["claims"] for r in c["relations"]]
    if len(all_rel)!=34 or len({r["assertion_id"] for c,r in all_rel})!=34:
        raise Error("target not exactly 34 unique relations")
    if len(packet["cases"])!=34:raise Error("packet incomplete")
    for i,case in enumerate(packet["cases"]):
        j=(11*i+5)%34
        c,r=all_rel[j]
        vid=c["validation_claim_id"]
        doc=reviewed[vid]
        ad=admissions[vid];su=sources[vid]
        expected_case_id="VMR-"+str(i+1).zfill(3)
        if case["case_id"]!=expected_case_id:
            raise Error(f"noncanonical case id at {i}")
        if c["reviewed_claimir_blob_sha"]!=blob(REVIEWED/f"{vid}.json"):
            raise Error(vid+" reviewed ClaimIR sha drift")
        if doc["extraction"]["manual_review_status"]!="reviewed":
            raise Error(vid+" not human-reviewed")
        if c["source_identity"]!=doc["provenance"]["paper_id"]:
            raise Error(vid+" DOI drift")
        expected_source={
          "title":ad["title"],"year":ad["year"],"doi":ad["source_identity"]["value"],
          "locator":su["source_locator"],
          "admitted_access_class":ad["eligibility_basis"]["source_access_class"],
          "source_surface_at_initial_extraction":su["source_surface"],
          "source_text_in_repository":False,
          "note":"ClaimIR provenance span locators are summaries/reviewer-recorded references, not primary-text quotations or proof of independent full-text access."
        }
        if case["source"]!=expected_source:
            raise Error(expected_case_id+": source identity/claim drift")
        if case["claim_context"]!={k:doc["claim_core"][k] for k in ("claim_type","modality","scope")}:
            # the packet uses 'type' instead of 'claim_type' for presentation
            expected_context={
               "type":doc["claim_core"]["claim_type"],
               "modality":doc["claim_core"]["modality"],
               "scope":doc["claim_core"]["scope"],
            }
            if case["claim_context"]!=expected_context:
                raise Error(expected_case_id+": claim context drift")
        by_node={x["id"]:x for x in c["source_nodes"]}
        by_span={x["span_id"]:x["locator"] for x in doc["provenance"]["source_spans"]}
        expected_relation={
         "kind":r["source_kind"],"description":r["source_description"],
         "ordered_arguments":[{
             "id":a,"role":by_node[a]["claimir_role"],"description":by_node[a]["description"]
            } for a in r["source_arguments"]],
         "source_span_locator_notes":[{
             "span_id":x,"locator_summary":by_span[x]
            } for x in r["source_span_ids"]],
        }
        if case["reviewed_relation"]!=expected_relation:
            raise Error(expected_case_id+": relation content drift")
        expected_others=[{"id":x["id"],"role":x["claimir_role"],"description":x["description"]}
             for x in c["source_nodes"] if x["id"] not in r["source_arguments"]]
        if case["optional_existing_semantic_reference_nodes"]!=expected_others:
            raise Error(expected_case_id+": extra reference nodes drift")
        if case["reviewer_fields"]!={k:None for k in (
          "source_verification","source_proposition_reconstruction","verdict",
          "v2_mapping","missing_semantic_distinction","reasoned_explanation","source_claim_dispute")}:
            raise Error(expected_case_id+": decisions entered before packet freeze")
        if set(case)!={"case_id","source","claim_context","reviewed_relation",
                       "optional_existing_semantic_reference_nodes","reviewer_fields"}:
            raise Error(expected_case_id+": packet added hidden-case metadata")
    if len({(11*i+5)%34 for i in range(34)})!=34:
        raise Error("non-bijective order")
    if progress["status"]!="PENDING_HUMAN_AUTHOR_CHALLENGE" or progress["reviewed_count"]!=0 or progress["sample_size"]!=34 or progress["entries"]!=[]:
        raise Error("review progress not blank 0/34")
    if progress["previous_verdict_crosswalk_unlocked"] is not False or progress["carrier_v3_design_started"] is not False:
        raise Error("premature comparison or v3 design")
    return {"status":"PASS","cases":34,"sources":8,
      "verdicts_disclosed":False,"v2_schema_modified":False,
      "prior_comparison_locked":True,"human_review":0,
      "limitation":"Masking covers reviewer-facing packet, not public repository history or author memory.",
      "terminal":"AHV2_8_VERDICT_MASKED_PACKET_GATE_PASS"}

def validate()->dict:
    protocol,packet,progress,target,admission,source,schema=map(
      load,(PROTOCOL,PACKET,PROGRESS,TARGET,ADMISSION,SOURCE,SCHEMA))
    docs={vid:load(REVIEWED/f"{vid}.json") for vid in IDS}
    return check(protocol,packet,progress,target,admission,source,schema,docs)

def negative_fixtures()->list[str]:
    protocol,packet,progress,target,admission,source,schema=map(
      load,(PROTOCOL,PACKET,PROGRESS,TARGET,ADMISSION,SOURCE,SCHEMA))
    docs={vid:load(REVIEWED/f"{vid}.json") for vid in IDS}
    good=lambda q,pg=progress:check(protocol,q,pg,target,admission,source,schema,docs)
    receipts=[]
    def rejects(label,q,pg=progress):
        try:good(q,pg)
        except Error:receipts.append(label)
        else:raise Error("negative fixture improperly accepted "+label)
    x=copy.deepcopy(packet);x["cases"].pop();rejects("dropped_case",x)
    x=copy.deepcopy(packet);x["cases"][1],x["cases"][2]=x["cases"][2],x["cases"][1];rejects("selection_permutation_changed",x)
    x=copy.deepcopy(packet);x["cases"][0]["prior_carrier_status"]="GAP";rejects("prior_verdict_leaked",x)
    x=copy.deepcopy(packet);x["cases"][0]["reviewed_relation"]["description"]="invented result";rejects("source_description_drift",x)
    x=copy.deepcopy(packet);x["frozen_v2_vocabulary"]["predicate_families"].append("NEW_PREDICATE");rejects("vocab_extension_leak",x)
    x=copy.deepcopy(progress);x["previous_verdict_crosswalk_unlocked"]=True;rejects("comparison_unlocked_before_review",packet,x)
    return receipts

def main()->None:
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    a=validate();b=validate()
    if a!=b:raise Error("nondeterministic")
    a["negative_fixtures"]=negative_fixtures()
    output=json.dumps(a,sort_keys=True,indent=2,ensure_ascii=False)+"\n"
    if args.output:args.output.write_text(output,encoding="utf-8")
    else:print(output,end="")
    print("AHV2_8_VERDICT_MASKED_REVIEW_PACKET_GATE_PASS")

if __name__=="__main__":
    main()
