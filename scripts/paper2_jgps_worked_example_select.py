#!/usr/bin/env python3
"""Deterministically select three JGPS worked-example candidates from frozen data.

The selection is descriptive only. It does not change ClaimIR, Archetypes,
Grammar mappings, or residual adjudications.
"""
from __future__ import annotations
import argparse, hashlib, json
from itertools import combinations, product
from pathlib import Path
from typing import Any

ROOT=Path("research/paper2")
MAN=ROOT/"chatgpt_reference_claimir_v1/manifest.json"
CLAIMS=ROOT/"chatgpt_reference_claimir_v1"
GLOBAL=ROOT/"global_archetype_reconstruction_v1.json"
AGG=ROOT/"grammar_v0_reverse_projection_aggregate_v1.json"
RESID=ROOT/"grammar_v0_residual_adjudication_v1.json"
SOURCES=ROOT/"designed_source_manifest_v1.json"
SEED="JGPS365-WORKED-EXAMPLES-V1"

class Error(ValueError): pass
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def root_id(x): return x.split(".",1)[0]
def h(*xs): return hashlib.sha256("|".join(map(str,xs)).encode()).hexdigest()

def inventory(core):
    nr=sorted({x["role"] for x in core["nodes"]})
    rk=sorted({x["kind"] for x in core["relations"]})
    return {"node_roles":nr,"relation_kinds":rk,"node_count":len(core["nodes"]),"relation_count":len(core["relations"])}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=Path,required=True); args=ap.parse_args()
    manifest=load(MAN); glob=load(GLOBAL); resid=load(RESID); src=load(SOURCES); agg=load(AGG)
    files={x["slot_id"]:x["file"] for x in manifest["entries"]}
    source={x["slot_id"]:x for x in src["entries"]}
    claims={}
    for slot,file in files.items():
        j=load(CLAIMS/file)
        claims[slot]={
            "labels":set(j["provenance"]["construct_labels"]),
            "spans":j["provenance"]["source_spans"],
            "paper_id":j["provenance"]["paper_id"],
            "core":j["claim_core"],
            "inventory":inventory(j["claim_core"]),
            "source":source[slot],
        }

    arch_by_claim={s:set() for s in claims}
    obj_by_id={}
    for o in glob["global_archetype_objects"]:
        oid=o["global_archetype_id"]; obj_by_id[oid]=o
        for ids in o.get("derived_support_claim_ids_by_lane",{}).values():
            for cid in ids:
                if cid in arch_by_claim: arch_by_claim[cid].add(oid)

    # 1) Different construct labels, exact same cross-lane Archetype.
    shared=[]
    for comp in glob["exact_cross_lane_equivalence_components"]:
        oid=comp["global_archetype_id"]
        origins=comp["origins"]
        for oa,ob in combinations(origins,2):
            if oa["lane"]==ob["lane"]: continue
            for a,b in product(oa["member_claim_ids"],ob["member_claim_ids"]):
                if a not in claims or b not in claims: continue
                if claims[a]["labels"] & claims[b]["labels"]: continue
                total_support=sum(x["support_size"] for x in origins)
                shared.append((-total_support,h(SEED,"shared",oid,a,b),oid,a,b))
    if not shared: raise Error("no disjoint-label exact-Archetype pair")
    _,_,shared_oid,shared_a,shared_b=min(shared)

    # 2) Same exact construct label, structurally divergent bounded support.
    same=[]
    slots=sorted(claims)
    for a,b in combinations(slots,2):
        labels=claims[a]["labels"] & claims[b]["labels"]
        if not labels: continue
        common=arch_by_claim[a] & arch_by_claim[b]
        ia,ib=claims[a]["inventory"],claims[b]["inventory"]
        role_diff=len(set(ia["node_roles"]) ^ set(ib["node_roles"]))
        rel_diff=len(set(ia["relation_kinds"]) ^ set(ib["relation_kinds"]))
        # Prefer zero shared bounded Archetypes; then greater structural contrast.
        same.append((len(common),-(role_diff+rel_diff),-len(labels),h(SEED,"same",a,b),a,b,sorted(labels),sorted(common)))
    if not same: raise Error("no shared construct-label pair")
    _,_,_,_,same_a,same_b,same_labels,same_common=min(same)

    # 3) Residual example: prefer RELATION_LANGUAGE_GAP, explicitly non-ROLE_GAP.
    residual_candidates=[]
    for row in resid["claims"]:
        if row.get("role_gap") is not False: continue
        pri=[row["primary"]]+row.get("secondary",[])
        priority=0 if "RELATION_LANGUAGE_GAP" in pri else 1
        residual_candidates.append((priority,h(SEED,"residual",row["claim_id"]),row))
    if not residual_candidates: raise Error("no non-ROLE_GAP residual")
    _,_,rr=min(residual_candidates)
    residual_slot=root_id(rr["claim_id"])

    lane_path={}
    for ls in agg["lane_sources"]:
        lane_path[ls["lane"]]=ls["path"]

    def claim_view(slot):
        c=claims[slot]
        return {
            "slot_id":slot,
            "paper_id":c["paper_id"],
            "canonical_locator":c["source"]["canonical_locator"],
            "construct_labels":sorted(c["labels"]),
            "source_spans":c["spans"],
            "structural_inventory":c["inventory"],
        }

    out={
        "schema":"relay-theory.paper2.jgps_worked_example_selection.v1",
        "status":"FROZEN_CANDIDATE_SELECTION_FROM_EXISTING_RESULTS",
        "authority_issue":365,
        "selection_seed":SEED,
        "examples":{
            "different_labels_shared_structure":{
                "claim_a":claim_view(shared_a),
                "claim_b":claim_view(shared_b),
                "shared_exact_archetype_id":shared_oid,
                "shared_archetype_object":obj_by_id[shared_oid]["canonical_structural_object"],
                "criterion":"different exact construct-label sets with an exact cross-lane Archetype identity",
            },
            "same_label_different_structure":{
                "claim_a":claim_view(same_a),
                "claim_b":claim_view(same_b),
                "shared_construct_labels":same_labels,
                "shared_bounded_archetype_ids":same_common,
                "whole_claim_relation":"INCOMPARABLE under frozen whole-claim comparison (all 1770 pairs)",
                "criterion":"shared exact construct label; minimize shared bounded-Archetype support, then maximize ClaimIR role/relation contrast",
            },
            "residual_case":{
                "claim":claim_view(residual_slot),
                "historical_claim_id":rr["claim_id"],
                "residual_primary":rr["primary"],
                "residual_secondary":rr.get("secondary",[]),
                "role_gap":rr["role_gap"],
                "rationale":rr["rationale"],
                "reverse_projection_artifact":rr["source_artifact"],
                "criterion":"non-ROLE_GAP residual, prioritizing RELATION_LANGUAGE_GAP pressure",
            },
        },
        "manuscript_use":{
            "required_chain":"source locator -> ClaimIR -> Phi/bounded subobject -> Grammar mapping",
            "selection_is_not_new_scientific_adjudication":True,
            "manual_exposition_still_required":True,
        },
        "terminal":"JGPS_THREE_WORKED_EXAMPLE_CANDIDATES_SELECTED",
    }
    args.output.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("JGPS_THREE_WORKED_EXAMPLE_CANDIDATES_SELECTED")
    print(shared_a,shared_b,shared_oid)
    print(same_a,same_b,same_labels,len(same_common))
    print(rr["claim_id"],rr["primary"],rr.get("secondary",[]))

if __name__=="__main__": main()
