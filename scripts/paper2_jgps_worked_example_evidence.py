#!/usr/bin/env python3
"""Assemble JGPS worked-example evidence chains from frozen Paper-2 artifacts."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

ROOT=Path("research/paper2")
MAN=ROOT/"chatgpt_reference_claimir_v1/manifest.json"
CLAIMS=ROOT/"chatgpt_reference_claimir_v1"
ADJ=ROOT/"reference_structural_adjudication_v1"
PHI=ROOT/"reference_phi_projection_freeze_v1.json"
GLOBAL=ROOT/"global_archetype_reconstruction_v1.json"
AGG=ROOT/"grammar_v0_reverse_projection_aggregate_v1.json"

class Error(ValueError): pass
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def root_id(x): return x.split(".",1)[0]

def claim_files():
    return {x["slot_id"]:x["file"] for x in load(MAN)["entries"]}

def phi_map():
    return {root_id(x["claim_id"]):x for x in load(PHI)["claims"]}

def grammar_sources():
    return load(AGG)["lane_sources"]

def grammar_record(slot:str):
    prefix=slot[:3]
    lane = prefix
    if prefix=="CH0": lane=None
    # Challenge lane split is irrelevant to the three selected examples.
    for row in grammar_sources():
        if row["lane"]==lane:
            data=load(row["path"])
            for c in data["claims"]:
                if root_id(c["claim_id"])==slot:
                    return row["path"],c
    raise Error(f"Grammar record not found for {slot}")

def all_objects():
    return {o["global_archetype_id"]:o for o in load(GLOBAL)["global_archetype_objects"]}

def direct_objects_for(slot:str):
    out=[]
    for o in all_objects().values():
        for origin in o.get("direct_origins",[]):
            if slot in origin.get("member_claim_ids",[]):
                out.append(o)
                break
    if not out: raise Error(f"no direct bounded object for {slot}")
    out.sort(key=lambda o:(-(o["node_count"]+o["edge_count"]),o["global_archetype_id"]))
    return out

def compact_grammar(c:dict[str,Any])->dict[str,Any]:
    keep={
        "claim_id":c["claim_id"],
        "grammar_roles_instantiated":c.get("grammar_roles_instantiated",[]),
        "verdict":c.get("verdict"),
        "supported_relations":c.get("supported_relations",[]),
        "derived_feature_candidates":c.get("derived_feature_candidates",[]),
        "unmapped_residual":c.get("unmapped_residual",[]),
        "notes":c.get("notes",[]),
    }
    # Preserve lane-specific role mapping fields without assuming a uniform key style.
    for k,v in c.items():
        lk=k.casefold()
        if k in keep: continue
        if "mapping" in lk and any(t in lk for t in ("pi","x","c","q","p_in","p_out","p_in / p_out","k ","t ","rho","o mapping")):
            keep[k]=v
    return keep

def chain(slot:str, bounded_ids:list[str])->dict[str,Any]:
    files=claim_files(); claim=load(CLAIMS/files[slot])
    adjud=load(ADJ/f"{slot}.json")
    pm=phi_map().get(slot)
    if pm is None: raise Error(f"no Phi freeze entry for {slot}")
    gp,gc=grammar_record(slot)
    objs=all_objects()
    return {
        "slot_id":slot,
        "source":{
            "paper_id":claim["provenance"]["paper_id"],
            "source_spans":claim["provenance"]["source_spans"],
        },
        "claim_ir":{
            "claim_id":claim["claim_id"],
            "claim_type":claim["claim_core"]["claim_type"],
            "modality":claim["claim_core"]["modality"],
            "scope":claim["claim_core"]["scope"],
            "nodes":claim["claim_core"]["nodes"],
            "relations":claim["claim_core"]["relations"],
        },
        "phi_projection":{
            "freeze_decision":pm["decision"],
            "phi_sha256":pm["phi_sha256"],
            "structural_sha256":pm["structural_sha256"],
            "coordinate_map":adjud["coordinate_map"],
            "controls":adjud["controls"],
            "temporal":adjud["temporal"],
            "structural_decision":adjud["decision"],
        },
        "bounded_subobjects":[
            {
                "global_archetype_id":oid,
                "active_axes":objs[oid]["active_axes"],
                "canonical_structural_object":objs[oid]["canonical_structural_object"],
                "derived_support_lanes":objs[oid]["derived_support_lanes"],
                "derived_support_claim_ids_by_lane":objs[oid]["derived_support_claim_ids_by_lane"],
            } for oid in bounded_ids
        ],
        "grammar_reverse_projection":{
            "artifact":gp,
            "record":compact_grammar(gc),
        },
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--selection",type=Path,required=True)
    ap.add_argument("--json-output",type=Path,required=True)
    ap.add_argument("--md-output",type=Path,required=True)
    args=ap.parse_args()
    sel=load(args.selection)
    ex=sel["examples"]
    shared=ex["different_labels_shared_structure"]
    same=ex["same_label_different_structure"]
    resid=ex["residual_case"]

    shared_oid=shared["shared_exact_archetype_id"]
    same_a=direct_objects_for(same["claim_a"]["slot_id"])[0]["global_archetype_id"]
    same_b=direct_objects_for(same["claim_b"]["slot_id"])[0]["global_archetype_id"]
    resid_oid=direct_objects_for(resid["claim"]["slot_id"])[0]["global_archetype_id"]

    out={
        "schema":"relay-theory.paper2.jgps_worked_example_evidence.v1",
        "status":"ASSEMBLED_FROM_FROZEN_ARTIFACTS",
        "authority_issue":365,
        "examples":{
            "different_labels_shared_structure":{
                "selection":shared,
                "claim_a_chain":chain(shared["claim_a"]["slot_id"],[shared_oid]),
                "claim_b_chain":chain(shared["claim_b"]["slot_id"],[shared_oid]),
            },
            "same_label_different_structure":{
                "selection":same,
                "claim_a_chain":chain(same["claim_a"]["slot_id"],[same_a]),
                "claim_b_chain":chain(same["claim_b"]["slot_id"],[same_b]),
                "representative_direct_archetypes":[same_a,same_b],
            },
            "residual_case":{
                "selection":resid,
                "claim_chain":chain(resid["claim"]["slot_id"],[resid_oid]),
                "representative_direct_archetype":resid_oid,
            },
        },
        "boundary":{
            "new_scientific_adjudication":False,
            "source_rereading_performed":False,
            "frozen_inputs_modified":False,
            "purpose":"paper-level worked-example exposition",
        },
        "terminal":"JGPS_WORKED_EXAMPLE_EVIDENCE_CHAINS_ASSEMBLED",
    }
    args.json_output.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# JGPS worked-example evidence chains v1","",
        "Assembled mechanically from frozen artifacts; no new scientific adjudication.","",
    ]
    for key,title in [
        ("different_labels_shared_structure","Different labels / shared structure"),
        ("same_label_different_structure","Same labels / different structure"),
        ("residual_case","Residual case"),
    ]:
        e=out["examples"][key]; lines += [f"## {title}",""]
        if key=="different_labels_shared_structure":
            ca=e["claim_a_chain"]; cb=e["claim_b_chain"]
            lines += [
                f"- claims: `{ca['slot_id']}` and `{cb['slot_id']}`",
                f"- shared exact Archetype: `{shared_oid}`",
                f"- Grammar verdicts: {ca['grammar_reverse_projection']['record'].get('verdict')} / {cb['grammar_reverse_projection']['record'].get('verdict')}",
            ]
        elif key=="same_label_different_structure":
            ca=e["claim_a_chain"]; cb=e["claim_b_chain"]
            lines += [
                f"- claims: `{ca['slot_id']}` and `{cb['slot_id']}`",
                f"- shared construct labels: {', '.join(e['selection']['shared_construct_labels'])}",
                "- shared bounded Archetypes: none",
                f"- representative direct Archetypes: `{same_a}` / `{same_b}`",
                f"- Grammar verdicts: {ca['grammar_reverse_projection']['record'].get('verdict')} / {cb['grammar_reverse_projection']['record'].get('verdict')}",
            ]
        else:
            cc=e["claim_chain"]
            lines += [
                f"- claim: `{cc['slot_id']}`",
                f"- residual: {e['selection']['residual_primary']} + {', '.join(e['selection']['residual_secondary'])}",
                f"- ROLE_GAP: {str(e['selection']['role_gap']).lower()}",
                f"- representative direct Archetype: `{resid_oid}`",
                f"- Grammar verdict: {cc['grammar_reverse_projection']['record'].get('verdict')}",
            ]
        lines += ["","Evidence chain in the JSON artifact: source spans → ClaimIR → Φ/structural projection → bounded subobject → Grammar reverse projection.",""]
    lines += ["Terminal:","", "`JGPS_WORKED_EXAMPLE_EVIDENCE_CHAINS_ASSEMBLED`",""]
    args.md_output.write_text("\n".join(lines),encoding="utf-8")
    print("JGPS_WORKED_EXAMPLE_EVIDENCE_CHAINS_ASSEMBLED")

if __name__=="__main__": main()
