#!/usr/bin/env python3
"""Validate frozen AHV2-8 author review by exact candidate->reviewed transformations."""
from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from pathlib import Path

from paper2_claim_ir_validate import validate as validate_claim_ir

ROOT = Path("paper/validation/jgps-major-revision")
CAND = ROOT / "ahv2-8-claimir-candidates-v1"
REV = ROOT / "ahv2-8-claimir-human-reviewed-v1"
PROGRESS = ROOT / "ahv2-8-human-review-progress-v1.json"
SUMMARY = ROOT / "ahv2-8-human-review-summary-v1.json"
V2 = ROOT / "l-claim-assertion-carrier-schema-v2.json"

IDS = (
 "AHV2-MEM-01", "AHV2-LRN-01", "AHV2-SKL-01", "AHV2-ATT-01",
 "AHV2-PRD-01", "AHV2-CTL-01", "AHV2-BLF-01", "AHV2-CNC-01",
)
DECISIONS = ("REVISE", "REVISE", "REVISE", "ACCEPT", "REVISE", "ACCEPT", "ACCEPT", "REVISE")
BOUNDARY = (
 "assertion_carrier_v2_validation_inspected",
 "grammar_mapping_inspected",
 "layered_projection_inspected",
)

class Error(ValueError):
    pass

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def relation(x: dict, rid: str) -> dict:
    return next(r for r in x["claim_core"]["relations"] if r["id"] == rid)

def node(id: str, role: str, description: str, spans: list[str]) -> dict:
    return {"id":id,"role":role,"description":description,"source_span_ids":spans,"grounding":"normalized"}

def apply_authorized_revision(vid: str, candidate: dict) -> dict:
    x = copy.deepcopy(candidate)
    x["extraction"]["manual_review_status"] = "reviewed"
    nodes = x["claim_core"]["nodes"]
    relations = x["claim_core"]["relations"]

    if vid == "AHV2-MEM-01":
        nodes.extend([
            node("limited_resource", "state_or_structure",
                 "limited maintenance resource distributed across the currently maintained items", ["s1"]),
            node("represented_item_quantity", "state_or_structure",
                 "number of represented items as contrasted with representation quality in the resource proposal", ["s2"]),
        ])
        relation(x,"r2")["arguments"] = ["limited_resource","maintained_item_set","resource_allocation"]
        relation(x,"r4")["arguments"] = ["task_performance","representation_quality","represented_item_quantity"]

    elif vid == "AHV2-LRN-01":
        relation(x,"r1")["arguments"] = [
            "learning_stage", "prediction_error_signal", "reward_delivery",
            "conditioned_cue", "error_signal_timing",
        ]

    elif vid == "AHV2-SKL-01":
        nodes.append(node("focused_attention","state_or_structure",
            "focused attention subject to interference from automatically elicited attending responses", ["s3"]))
        relation(x,"r4")["arguments"] = [
            "automatic_attention_response", "controlled_search", "focused_attention",
        ]

    elif vid == "AHV2-PRD-01":
        nodes.append(node("pleasantness_rating","response_or_outcome",
            "rated pleasantness of the tactile sensation", ["s1"]))
        r1=relation(x,"r1")
        r1["arguments"]=[
          "self_produced_condition","external_condition","tactile_intensity_rating",
          "tickliness_rating","pleasantness_rating",
        ]
        r1["description"]="self-produced tactile stimulation is rated less intense, tickly, and pleasant than externally produced stimulation"
        relation(x,"r6")["description"]="in the authors' proposed forward-model account, greater prediction error is associated with less sensory attenuation (inverse directional relationship)"
        relations.append({
          "id":"r7","kind":"depends_on",
          "arguments":["tickliness_rating","prediction_error"],
          "description":"in the authors' proposed forward-model account, tickliness increases with the error between predicted and actual sensory feedback",
          "source_span_ids":["s4"],"grounding":"normalized",
        })

    elif vid == "AHV2-CNC-01":
        x["provenance"]["source_spans"].extend([
         {"span_id":"s5","locator":"Smith & Minda (1998), original article pp. 1416, 1418 and 1425 (Experiments 1, 2 and 4): early prototype-model fit advantage in large, better-differentiated categories depends on experiment/category condition; model fit is not direct identification of participants' internal processing."},
         {"span_id":"s6","locator":"Smith & Minda (1998), original article pp. 1422-1423, Figure 6 (Experiment 3), and pp. 1425-1426 (Experiment 4): for small, poorly differentiated categories, exemplar model fits better from early epochs and prototype model has no early fit advantage."},
         {"span_id":"s7","locator":"Smith & Minda (1998), original article pp. 1426-1428 (mixture-model interpretation, Figure 9) and p. 1432 (General Discussion): inferred prototype-to-exemplar transition applies particularly to large, better-differentiated categories and does not directly establish a unique cognitive mechanism."}
        ])
        nodes.extend([
          node("exemplar_model_fit","response_or_outcome",
            "relative fit of the standard exemplar model to observed category-learning performance profiles; a model-comparison result rather than directly measured processing", ["s2","s6"]),
          node("prototype_model_fit","response_or_outcome",
            "relative fit of the basic prototype model to observed category-learning performance profiles; a model-comparison result rather than directly measured processing", ["s3","s5"]),
        ])
        r1=relation(x,"r1")
        r1["arguments"]=["exemplar_model_fit","small_less_differentiated_structure","learning_stage"]
        r1["description"]="for small, poorly differentiated categories the standard exemplar model describes observed performance better, including at early learning stages; this is a model-fit result, not direct observation of exemplar processing"
        r1["source_span_ids"]=["s2","s6"]
        r2=relation(x,"r2")
        r2["arguments"]=["prototype_model_fit","large_more_differentiated_structure","learning_stage"]
        r2["description"]="for large, better-differentiated categories the prototype model has an early fit advantage in the reported qualifying task conditions, but not uniformly across all experimental conditions; this is a model-fit result, not direct observation of prototype processing"
        r2["source_span_ids"]=["s3","s5"]
        r3=relation(x,"r3")
        r3["arguments"]=[
          "learning_stage","large_more_differentiated_structure",
          "prototype_based_processing","exemplar_based_processing",
        ]
        r3["description"]="the authors interpret the learning-stage model-fit trajectory for large, better-differentiated categories as consistent with a gradual shift from prototype-based toward exemplar-based processing; this is an inferred mechanism, not a uniquely established psychological transition and does not generalize to small, poorly differentiated categories"
        r3["source_span_ids"]=["s4","s5","s6","s7"]

    return x

def validate() -> dict:
    progress,summary,v2=map(load,(PROGRESS,SUMMARY,V2))
    if v2["status"]!="FROZEN_AHV8_DERIVED_PRE_NEW_HELDOUT_VALIDATION":
        raise Error("frozen v2 schema status drift")
    if progress["status"]!="COMPLETE" or progress["reviewed_count"]!=8 or progress["total_count"]!=8:
        raise Error("human review not COMPLETE at 8/8")
    if progress["assertion_carrier_v2_validation_authorized"] is not True:
        raise Error("v2 validation not authorized after review")
    if progress["terminal"]!="AHV2_8_HUMAN_REVIEW_COMPLETE_8_OF_8":
        raise Error("review terminal drift")
    if [e["validation_claim_id"] for e in progress["entries"]]!=list(IDS):
        raise Error("review order/membership drift")
    if [e["human_review_decision"] for e in progress["entries"]]!=list(DECISIONS):
        raise Error("human decisions drift")
    for vid,decision,e in zip(IDS,DECISIONS,progress["entries"]):
        if e["reviewer"]!="author" or e["review_date"]!="2026-10-01":
            raise Error(f"{vid}: review authorship/date drift")
        if e["revision_applied"] is not (decision=="REVISE"):
            raise Error(f"{vid}: revision flag drift")
        for flag in BOUNDARY:
            if e[flag] is not False:
                raise Error(f"{vid}: downstream inspection before human-review completion")

    wanted=sorted(f"{vid}.json" for vid in IDS)
    if sorted(p.name for p in CAND.glob("*.json"))!=wanted:
        raise Error("frozen candidate membership drift")
    if sorted(p.name for p in REV.glob("*.json"))!=wanted:
        raise Error("reviewed-copy membership drift")

    receipts=[];original_relations=0;reviewed_relations=0
    for vid,decision,e in zip(IDS,DECISIONS,progress["entries"]):
        if e["original_candidate_file"]!=f"ahv2-8-claimir-candidates-v1/{vid}.json":
            raise Error(f"{vid}: original path drift")
        if e["reviewed_file"]!=f"ahv2-8-claimir-human-reviewed-v1/{vid}.json":
            raise Error(f"{vid}: reviewed path drift")
        candidate=load(CAND/f"{vid}.json")
        reviewed=load(REV/f"{vid}.json")
        validate_claim_ir(candidate); validate_claim_ir(reviewed)
        if candidate["extraction"]["manual_review_status"]!="unreviewed":
            raise Error(f"{vid}: frozen original candidate changed")
        if reviewed["extraction"]["manual_review_status"]!="reviewed":
            raise Error(f"{vid}: reviewed-copy status missing")
        expected=apply_authorized_revision(vid,candidate)
        if reviewed!=expected:
            raise Error(f"{vid}: reviewed copy differs from authorized human revision")
        originals_only=copy.deepcopy(candidate)
        originals_only["extraction"]["manual_review_status"]="reviewed"
        changed=reviewed!=originals_only
        if changed is not (decision=="REVISE"):
            raise Error(f"{vid}: decision/substantive-change mismatch")
        a=len(candidate["claim_core"]["relations"])
        b=len(reviewed["claim_core"]["relations"])
        original_relations+=a;reviewed_relations+=b
        receipts.append({"validation_claim_id":vid,"decision":decision,"original_relations":a,"reviewed_relations":b})

    if (original_relations,reviewed_relations)!=(33,34):
        raise Error(f"relation membership drift: originals={original_relations}, reviewed={reviewed_relations}")
    counts=Counter(DECISIONS)
    expected_counts={"ACCEPT":3,"REVISE":5,"REJECT":0,"total":8}
    if summary["status"]!="FROZEN_HUMAN_REVIEW_COMPLETE":
        raise Error("summary not frozen")
    if summary["counts"]!=expected_counts:
        raise Error("summary decision-count drift")
    if [x["decision"] for x in summary["decisions"]]!=list(DECISIONS):
        raise Error("summary decision-order drift")
    if [x["validation_claim_id"] for x in summary["decisions"]]!=list(IDS):
        raise Error("summary decision-membership drift")
    if summary["original_candidate_relations"]!=33 or summary["reviewed_relations"]!=34:
        raise Error("summary relation-count drift")
    if summary["assertion_carrier_v2_validation_authorized"] is not True:
        raise Error("summary v2 authorization drift")
    for flag in BOUNDARY:
        if summary["boundary"][flag] is not False:
            raise Error(f"summary leaks downstream inspection: {flag}")
    return {
      "schema":"relay-theory.paper2.ahv2_8_human_review_validation.v1",
      "status":"PASS",
      "reviewed":8,
      "decisions":{"ACCEPT":counts["ACCEPT"],"REVISE":counts["REVISE"],"REJECT":counts["REJECT"]},
      "original_relations":original_relations,
      "reviewed_relations":reviewed_relations,
      "v2_validation_authorized":True,
      "receipts":receipts,
      "terminal":"AHV2_8_HUMAN_REVIEW_VALIDATION_PASS"
    }

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    a=validate(); b=validate()
    if a!=b: raise Error("nondeterministic validation")
    payload=json.dumps(a,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.output:args.output.write_text(payload,encoding="utf-8")
    else:print(payload,end="")
    print("AHV2_8_HUMAN_REVIEW_GATE_PASS")

if __name__=="__main__": main()
