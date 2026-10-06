#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, math
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"research/paper2/p399/main/integration/M12/human_validation/reference"
CLAIM_KEYS=[
 BASE/"M12_CLAIM_REFERENCE_GROUP_A1_v1.json",
 BASE/"M12_CLAIM_REFERENCE_GROUP_A2_v1.json",
 BASE/"M12_CLAIM_REFERENCE_GROUP_B1_v1.json",
 BASE/"M12_CLAIM_REFERENCE_GROUP_B2_v1.json",
 BASE/"M12_CLAIM_REFERENCE_GROUP_C_v1.json",
]
PRO_KEY=BASE/"M12_PROSPECTIVE_REFERENCE_v1.json"
ROLES=["Pi","X","C","Q","P_in","P_out","K","T","rho/O"]

def load_json(p):
    return json.loads(p.read_text(encoding="utf-8"))

def kappa(a,b):
    assert len(a)==len(b) and a
    n=len(a); po=sum(x==y for x,y in zip(a,b))/n
    ca=Counter(a); cb=Counter(b)
    pe=sum((ca[k]/n)*(cb[k]/n) for k in set(ca)|set(cb))
    if abs(1-pe)<1e-12:
        return None
    return (po-pe)/(1-pe)

def prf(tp,fp,fn):
    p=tp/(tp+fp) if tp+fp else None
    r=tp/(tp+fn) if tp+fn else None
    f=2*p*r/(p+r) if p is not None and r is not None and p+r else None
    return {"precision":p,"recall":r,"f1":f}

def read_csv(path):
    with open(path,newline="",encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

def require_complete(rows, fields, label):
    missing=[]
    for r in rows:
        for f in fields:
            if not (r.get(f) or "").strip():
                missing.append((r.get("case_id","?"),f))
    if missing:
        raise SystemExit(f"{label} incomplete: {missing[:20]}")

def main():
    ap=argparse.ArgumentParser(description="Score completed independent-human M12 re-adjudication forms.")
    ap.add_argument("--claim-csv",required=True)
    ap.add_argument("--prospective-csv",required=True)
    ap.add_argument("--out")
    args=ap.parse_args()

    claim_ref={}
    for p in CLAIM_KEYS:
        for c in load_json(p)["cases"]:
            claim_ref[c["case_id"]]=c
    pro_ref={c["case_id"]:c for c in load_json(PRO_KEY)["cases"]}

    cr=read_csv(args.claim_csv)
    pr=read_csv(args.prospective_csv)
    require_complete(cr,["case_id","roles_semicolon","projection_verdict","candidate_A","candidate_B"],"claim form")
    require_complete(pr,["case_id","state","stateless_added","persistent_added"],"prospective form")
    if set(r["case_id"] for r in cr)!=set(claim_ref):
        raise SystemExit("claim case IDs do not match frozen 20-case sample")
    if set(r["case_id"] for r in pr)!=set(pro_ref):
        raise SystemExit("prospective case IDs do not match frozen 10-case sample")

    valid_verdict={"FULL","PARTIAL","RESIDUAL"}
    valid_cand={"SUPPORTED","NOT_SUPPORTED","UNDERDETERMINED"}
    valid_state={"A0","A1","A2","UNDERDETERMINED","FAILURE"}
    valid_tri={"TRUE","FALSE","UNDETERMINED"}

    claim_ver_ref=[]; claim_ver_h=[]
    role_counts={r:{"tp":0,"fp":0,"fn":0,"exact":0} for r in ROLES}
    role_exact=0; cand_ref=[]; cand_h=[]
    claim_disagreements=[]
    for row in cr:
        cid=row["case_id"]; ref=claim_ref[cid]
        verdict=row["projection_verdict"].strip().upper()
        if verdict not in valid_verdict: raise SystemExit(f"invalid verdict {cid}: {verdict}")
        roles={x.strip() for x in row["roles_semicolon"].split(";") if x.strip()}
        bad=roles-set(ROLES)
        if bad: raise SystemExit(f"invalid roles {cid}: {sorted(bad)}")
        rr=set(ref["grammar_roles_reference"])
        claim_ver_ref.append(ref["projection_verdict_reference"]); claim_ver_h.append(verdict)
        if roles==rr: role_exact+=1
        for role in ROLES:
            a=role in rr; b=role in roles
            if a and b: role_counts[role]["tp"]+=1
            elif (not a) and b: role_counts[role]["fp"]+=1
            elif a and (not b): role_counts[role]["fn"]+=1
        cref={x["candidate_id"]:x["reference_decision"] for x in ref["bounded_candidate_reference"]}
        for cand in ["A","B"]:
            hv=row[f"candidate_{cand}"].strip().upper()
            if hv not in valid_cand: raise SystemExit(f"invalid candidate decision {cid}/{cand}: {hv}")
            cand_ref.append(cref[cand]); cand_h.append(hv)
        if verdict!=ref["projection_verdict_reference"] or roles!=rr or any(row[f"candidate_{c}"].strip().upper()!=cref[c] for c in ["A","B"]):
            claim_disagreements.append({"case_id":cid,"reference_roles":sorted(rr),"human_roles":sorted(roles),"reference_verdict":ref["projection_verdict_reference"],"human_verdict":verdict,"notes":row.get("notes","")})

    pro_state_ref=[]; pro_state_h=[]; stat_ref=[];stat_h=[]; pers_ref=[];pers_h=[];pro_disagreements=[]
    def bool_to_text(v): return "TRUE" if v else "FALSE"
    for row in pr:
        cid=row["case_id"]; ref=pro_ref[cid]
        state=row["state"].strip().upper()
        sa=row["stateless_added"].strip().upper(); pa=row["persistent_added"].strip().upper()
        if state not in valid_state: raise SystemExit(f"invalid state {cid}: {state}")
        if sa not in valid_tri or pa not in valid_tri: raise SystemExit(f"invalid tri-state {cid}")
        sr=ref["state_reference"]; sar=bool_to_text(ref["stateless_added_reference"]); par=bool_to_text(ref["persistent_added_reference"])
        pro_state_ref.append(sr);pro_state_h.append(state);stat_ref.append(sar);stat_h.append(sa);pers_ref.append(par);pers_h.append(pa)
        if state!=sr or sa!=sar or pa!=par:
            pro_disagreements.append({"case_id":cid,"reference_state":sr,"human_state":state,"reference_stateless":sar,"human_stateless":sa,"reference_persistent":par,"human_persistent":pa,"notes":row.get("notes","")})

    role_stats={}
    for role,c in role_counts.items():
        role_stats[role]={**c,**prf(c["tp"],c["fp"],c["fn"])}
    micro={"tp":sum(c["tp"] for c in role_counts.values()),"fp":sum(c["fp"] for c in role_counts.values()),"fn":sum(c["fn"] for c in role_counts.values())}

    out={
      "schema":"relaytheory.p399.main.m12.human_readjudication_score.v1",
      "status":"COMPUTED_FROM_SUPPLIED_COMPLETED_HUMAN_FORMS",
      "warning":"This file is valid only if the supplied forms were completed by an actual independent human under the frozen protocol.",
      "claim_n":len(cr),"prospective_n":len(pr),
      "claim_projection":{"exact_agreement":sum(a==b for a,b in zip(claim_ver_ref,claim_ver_h))/len(cr),"cohen_kappa":kappa(claim_ver_ref,claim_ver_h)},
      "claim_role_set":{"exact_set_agreement":role_exact/len(cr),"by_role":role_stats,"micro":{**micro,**prf(**micro)}},
      "bounded_candidate":{"n":len(cand_ref),"exact_agreement":sum(a==b for a,b in zip(cand_ref,cand_h))/len(cand_ref),"cohen_kappa":kappa(cand_ref,cand_h)},
      "prospective_state":{"exact_agreement":sum(a==b for a,b in zip(pro_state_ref,pro_state_h))/len(pr),"cohen_kappa":kappa(pro_state_ref,pro_state_h)},
      "prospective_stateless":{"exact_agreement":sum(a==b for a,b in zip(stat_ref,stat_h))/len(pr),"cohen_kappa":kappa(stat_ref,stat_h)},
      "prospective_persistent":{"exact_agreement":sum(a==b for a,b in zip(pers_ref,pers_h))/len(pr),"cohen_kappa":kappa(pers_ref,pers_h)},
      "claim_disagreements":claim_disagreements,
      "prospective_disagreements":pro_disagreements
    }
    txt=json.dumps(out,indent=2,ensure_ascii=False)+"\n"
    if args.out: Path(args.out).write_text(txt,encoding="utf-8")
    else: print(txt,end="")

if __name__=="__main__":
    main()
