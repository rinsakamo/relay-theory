#!/usr/bin/env python3
"""Build JGPS #365 review-support artifacts from frozen Paper-2 inputs.

Outputs:
1. a deterministic 18/60 independent re-adjudication packet with original
   verdict/residual outcomes removed from the packet;
2. a 60-claim supplementary source/claim table.

This script is additive only and never modifies frozen scientific artifacts.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT=Path("research/paper2")
VAL=Path("paper/validation/jgps-major-revision")
AGG=ROOT/"grammar_v0_reverse_projection_aggregate_v1.json"
RESID=ROOT/"grammar_v0_residual_adjudication_v1.json"
SOURCES=ROOT/"designed_source_manifest_v1.json"
CLAIM_MANIFEST=ROOT/"chatgpt_reference_claimir_v1/manifest.json"
CLAIM_DIR=ROOT/"chatgpt_reference_claimir_v1"

SEED="JGPS365-INDEPENDENT-READJUDICATION-V1"
QUOTAS={"FULL":5,"PARTIAL":5,"RESIDUAL":8}
GRAMMAR_ROLES=["Pi","X","C","Q","P_in","P_out","K","T","rho/O"]
RESIDUAL_CLASSES=[
    "ROLE_GAP","RELATION_LANGUAGE_GAP","FORMAL_CARRIER_GAP",
    "DERIVED_STRUCTURE_GAP","SOURCE_CONTEXT_PARAMETER","UNDERDETERMINED",
]

class Error(ValueError): pass

def load(p:Path)->dict[str,Any]:
    return json.loads(p.read_text(encoding="utf-8"))

def slot_root(claim_id:str)->str:
    return claim_id.split(".",1)[0]

def score(label:str, claim_id:str)->str:
    return hashlib.sha256(f"{SEED}|{label}|{slot_root(claim_id)}".encode()).hexdigest()

def source_maps():
    src=load(SOURCES)
    sm={x["slot_id"]:x for x in src["entries"]}
    cm=load(CLAIM_MANIFEST)
    fm={x["slot_id"]:x["file"] for x in cm["entries"]}
    if len(sm)!=60 or len(fm)!=60 or set(sm)!=set(fm):
        raise Error("60-source/ClaimIR manifest mismatch")
    return sm,fm

def claim_data(slot:str, fm:dict[str,str])->dict[str,Any]:
    return load(CLAIM_DIR/fm[slot])

def select_18()->list[tuple[str,str]]:
    agg=load(AGG)
    groups={k:[] for k in QUOTAS}
    seen=set()
    for row in agg["claim_verdicts"]:
        cid=row["claim_id"]; verdict=row["verdict"]; root=slot_root(cid)
        if root in seen: raise Error(f"duplicate slot root in verdicts: {root}")
        seen.add(root)
        groups[verdict].append(cid)
    if len(seen)!=60: raise Error("expected 60 verdicts")
    out=[]
    for verdict,n in QUOTAS.items():
        chosen=sorted(groups[verdict], key=lambda c:score(verdict,c))[:n]
        if len(chosen)!=n: raise Error(f"quota underflow {verdict}")
        out.extend((verdict,c) for c in chosen)
    # Mix strata so packet order itself does not disclose quota grouping.
    out.sort(key=lambda vc:hashlib.sha256(f"{SEED}|packet|{slot_root(vc[1])}".encode()).hexdigest())
    return out

def structural_inventory(core:dict[str,Any])->dict[str,Any]:
    node_roles={}
    for n in core["nodes"]:
        node_roles[n["role"]]=node_roles.get(n["role"],0)+1
    relation_kinds={}
    for r in core["relations"]:
        relation_kinds[r["kind"]]=relation_kinds.get(r["kind"],0)+1
    return {"node_role_counts":node_roles,"relation_kind_counts":relation_kinds}

def build_packet()->dict[str,Any]:
    sm,fm=source_maps()
    selected=select_18()
    entries=[]
    for idx,(hidden_verdict,cid) in enumerate(selected,1):
        slot=slot_root(cid)
        src=sm[slot]
        claim=claim_data(slot,fm)
        anon=f"IR{idx:02d}"
        entries.append({
            "anonymous_id":anon,
            "source":{
                "paper_id":claim["provenance"]["paper_id"],
                "canonical_locator":src["canonical_locator"],
                "source_spans":claim["provenance"]["source_spans"],
                "source_access_class":src["source_access_class"],
                "read_status":src["read_status"],
            },
            "blinded_claim":{
                "schema_version":"paper2-blinded-claim-v1",
                "claim_id":anon,
                "claim_core":claim["claim_core"],
            },
            "structural_inventory":structural_inventory(claim["claim_core"]),
            "judgments":{
                "claimir_typing":{"decision":None,"corrections":None},
                "bounded_reusable_structure":{"decision":None,"notes":None},
                "grammar_projection":{"verdict":None,"supported_roles":None,"notes":None},
                "residual_primary_class":None,
                "role_gap_required":None,
                "reviewer_confidence":None,
            }
        })
    return {
        "schema":"relay-theory.paper2.independent_readjudication_packet.v1",
        "status":"FROZEN_BLINDED_PACKET_PENDING_INDEPENDENT_HUMAN",
        "authority_issue":365,
        "selection":{
            "population":60,
            "sample_size":18,
            "fraction":0.30,
            "seed":SEED,
            "quota_policy":{"FULL":5,"PARTIAL":5,"RESIDUAL":8},
            "residual_oversampled":True,
            "original_outcomes_in_packet":False,
        },
        "instructions":{
            "independence_requirement":"The adjudicator must not consult the existing Grammar-v0 reverse-projection or residual-adjudication result files while completing this packet.",
            "grammar_roles":GRAMMAR_ROLES,
            "verdicts":["FULL","PARTIAL","RESIDUAL"],
            "residual_classes":RESIDUAL_CLASSES,
            "role_gap_rule":"Use ROLE_GAP only if positive source-grounded evidence requires a recurrent cognitive-system role not representable as an existing role, relation-language issue, formal-carrier issue, derived structure, source/context parameter, or underdetermined modeling choice.",
            "claimir_typing_decisions":["ACCEPT","REVISE","REJECT"],
            "bounded_structure_decisions":["SUPPORTED","PARTIAL","NOT_SUPPORTED"],
        },
        "entries":entries,
        "terminal":"INDEPENDENT_READJUDICATION_18_PACKET_FROZEN_PENDING_HUMAN",
    }

def build_selection_receipt()->dict[str,Any]:
    # This receipt records membership and hidden strata for later scoring.
    # It is an audit artifact, not part of the blinded packet.
    selected=select_18()
    return {
        "schema":"relay-theory.paper2.independent_readjudication_selection_receipt.v1",
        "status":"FROZEN_SELECTION_AUDIT",
        "authority_issue":365,
        "seed":SEED,
        "quota_policy":QUOTAS,
        "entries":[
            {"anonymous_id":f"IR{i:02d}","claim_id":cid,"slot_id":slot_root(cid),"historical_verdict":verdict}
            for i,(verdict,cid) in enumerate(selected,1)
        ],
        "warning":"Do not provide this receipt to the independent adjudicator before response lock.",
    }

def summarize_claim(claim:dict[str,Any])->str:
    rel=[r["description"].strip() for r in claim["claim_core"]["relations"]]
    if rel:
        return " ".join(rel[:3])
    nodes=[n["description"].strip() for n in claim["claim_core"]["nodes"]]
    return " ".join(nodes[:2])

def supplement_rows()->list[dict[str,Any]]:
    sm,fm=source_maps()
    rows=[]
    for slot in sorted(sm):
        src=sm[slot]; claim=claim_data(slot,fm)
        rows.append({
            "slot_id":slot,
            "surface":src["surface"],
            "sampling_stratum":src["sampling_stratum"] or "",
            "challenge_pressure":src["challenge_pressure"] or "",
            "claim_id":claim["claim_id"],
            "doi_or_identity":f'{src["stable_identity"]["kind"]}:{src["stable_identity"]["value"]}',
            "canonical_locator":src["canonical_locator"],
            "title":src["title"],
            "year":src["year"],
            "source_access_class":src["source_access_class"],
            "claim_type":claim["claim_core"]["claim_type"],
            "modality":claim["claim_core"]["modality"],
            "claim_summary":summarize_claim(claim),
            "source_span_count":len(claim["provenance"]["source_spans"]),
        })
    if len(rows)!=60: raise Error("supplement must have 60 rows")
    return rows

def write_csv(path:Path, rows:list[dict[str,Any]]):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

def write_md(path:Path, rows:list[dict[str,Any]]):
    lines=[
        "# Paper 2 supplementary source/claim table v1","",
        "Generated mechanically from the frozen 60-source manifest and reviewed ClaimIR.",
        "It is descriptive only and does not include Grammar-v0 verdicts.","",
        "| Slot | Stratum | DOI / identity | Year | Claim ID | Claim summary |",
        "|---|---|---|---:|---|---|",
    ]
    for r in rows:
        summary=r["claim_summary"].replace("|","\\|")
        identity=r["doi_or_identity"].replace("|","\\|")
        lines.append(f'| {r["slot_id"]} | {r["sampling_stratum"] or r["challenge_pressure"]} | {identity} | {r["year"]} | {r["claim_id"]} | {summary} |')
    path.write_text("\n".join(lines)+"\n",encoding="utf-8")

def validate_packet(packet:dict[str,Any]):
    if len(packet["entries"])!=18: raise Error("packet not 18")
    for e in packet["entries"]:
        blob=json.dumps(e,ensure_ascii=False).casefold()
        for forbidden in ('"historical_verdict"','"residual_primary"','"role_gap": false','"role_gap": true'):
            if forbidden in blob: raise Error(f"outcome leakage in {e['anonymous_id']}: {forbidden}")
        if any(v is not None for v in e["judgments"]["claimir_typing"].values()): raise Error("pre-filled claimir judgment")
        if e["judgments"]["grammar_projection"]["verdict"] is not None: raise Error("pre-filled grammar verdict")
        if e["judgments"]["residual_primary_class"] is not None: raise Error("pre-filled residual class")
        if e["judgments"]["role_gap_required"] is not None: raise Error("pre-filled role gap")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--outdir",type=Path,required=True)
    args=ap.parse_args()
    args.outdir.mkdir(parents=True,exist_ok=True)
    packet=build_packet(); validate_packet(packet)
    receipt=build_selection_receipt()
    rows=supplement_rows()
    (args.outdir/"independent-readjudication-packet-v1.json").write_text(json.dumps(packet,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    (args.outdir/"independent-readjudication-selection-receipt-v1.json").write_text(json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    write_csv(args.outdir/"supplementary-source-claim-table-v1.csv",rows)
    write_md(args.outdir/"supplementary-source-claim-table-v1.md",rows)
    print("PAPER2_JGPS_REVIEW_SUPPORT_V1_PASS")
    print("READJUDICATION_SAMPLE=18/60")
    print("SUPPLEMENT_ROWS=60")
if __name__=="__main__":
    main()
