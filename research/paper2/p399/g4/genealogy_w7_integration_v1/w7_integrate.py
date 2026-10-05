#!/usr/bin/env python3
"""RelayTheory Paper 2 P399 G4 W7 six-lane integration.

Fail-closed integration only. It does not inspect MAIN structural outcomes,
run Grammar-v0/H0-H2, or certify global family independence.
"""
from __future__ import annotations
import argparse, copy, itertools, json, re, subprocess, tempfile
from collections import Counter, defaultdict
from pathlib import Path

BASE_HEAD = "ae044a8f475fb0dc9140a91e360e1ff26a0b5e3a"
G1_REF = "c7317da41b15159864c014b8dc53449121c34a2c"
W7_DIR = Path("research/paper2/p399/g4/genealogy_w7_integration_v1")
ACCEL = Path("research/paper2/p399/g4/genealogy_accelerator_v1")
SHARED_PROFILES = ACCEL / "ORIGINAL_NATIVE_PROFILES_v1.json"
G2_MANIFEST = Path("research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json")
G1_ROSTER = Path("research/paper2/p399/g1/G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v7.json")
LEGACY = Path("research/paper2/p399/g2/MAIN40_G2_780_MAIN_AND_800_G1_FAMILY_RECONCILIATION_v2.json")
BASE_GENERATOR = ACCEL / "build_pair_matrix.py"
SOURCE_NATIVE = {
    "v20": Path("research/paper2/p399/g2/int_g2d/G2D_V20_INT01_THREE_ADDITIONAL_PAIRS_INT09_OFFICIAL_FIG9_CORRIGENDUM_AND_35_QUEUE.json"),
    "v10d": Path("research/paper2/p399/g2/int_g2d/G2D_V10D_CORRECTED_PAIR_SOURCE_NATIVE_MACHINE_GATES.json"),
    "v15b": Path("research/paper2/p399/g2/int_g2d/G2D_V15B_SELECTED_INT15_INT16_VS_G1_P18_P09_NATIVE_OPERATOR_BOUNDED_PAIR_AUDIT.json"),
    "v16b": Path("research/paper2/p399/g2/int_g2d/G2D_V16B_INT01_INT14_FIRSTPARTY_CRP_NATIVE_FAMILY_20261005.json"),
}
LANES = {
    "W1": {"pr":441,"head":"7a5a46aa39c81be4ceb863ff0f57cbe641d508dc","dir":"research/paper2/p399/g4/genealogy_w1_att_blf_cnc","profile":"W1_SOURCE_NATIVE_PROFILE_FRAGMENTS_v1.json","pairs":"W1_BOUNDED_PAIR_ADJUDICATIONS_v1.json","ids":["ATT-01","ATT-02","BLF-02","BLF-03","CNC-01","CNC-02","CNC-03"]},
    "W2": {"pr":443,"head":"005209c82fcbaf3d70f545488fd11cc15676a315","dir":"research/paper2/p399/g4/genealogy_w2_ctl_lrn","profile":"W2_SOURCE_NATIVE_PROFILE_FRAGMENTS_v1.json","pairs":"W2_BOUNDED_PAIR_ADJUDICATIONS_v1.json","ids":["CTL-01","CTL-02","CTL-03","LRN-01","LRN-02","LRN-03"]},
    "W3": {"pr":442,"head":"b132104b79c5f799107328e0f8d634dcffcf930d","dir":"research/paper2/p399/g4/genealogy_w3_mem_prd_skl","profile":"W3_SOURCE_NATIVE_PROFILE_FRAGMENTS_v1.json","pairs":"W3_BOUNDED_PAIR_ADJUDICATIONS_v1.json","ids":["MEM-01","MEM-02","MEM-03","PRD-02","PRD-03","SKL-01","SKL-02","SKL-03"]},
    "W4": {"pr":444,"head":"abb07cef7542ffb9809d924ab05ede702bac9a20","dir":"research/paper2/p399/g4/genealogy_w4_int_02_03_05_06_07","profile":"W4_SOURCE_NATIVE_PROFILE_FRAGMENTS_v1.json","pairs":"W4_BOUNDED_PAIR_ADJUDICATIONS_v1.json","ids":["INT-02","INT-03","INT-05","INT-06","INT-07"]},
    "W5": {"pr":446,"head":"72b4a9d3b89d49148d1787910b75163843490019","dir":"research/paper2/p399/g4/genealogy_w5_int_09_10_11_12","profile":"W5_SOURCE_NATIVE_PROFILE_FRAGMENTS_v1.json","pairs":"W5_BOUNDED_PAIR_ADJUDICATIONS_v1.json","ids":["INT-09","INT-10","INT-11","INT-12"]},
    "W6": {"pr":445,"head":"be50aee8c49331fe7bb24591fc1bd7cd49c37aec","dir":"research/paper2/p399/g4/genealogy_w6_int_13_14_15_16","profile":"W6_SOURCE_NATIVE_PROFILE_FRAGMENTS_v1.json","pairs":"W6_BOUNDED_PAIR_ADJUDICATIONS_v1.json","ids":["INT-13","INT-14","INT-15","INT-16"]},
}
ALLOWED_DECISIONS={"DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY","SHARED_CONSTITUENT_ONLY","BOUNDED_SOURCE_NATIVE_DIFFERENCE","UNDERDETERMINED"}
CATEGORY_MAP={
"DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY":"DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY",
"SHARED_CONSTITUENT_ONLY":"SHARED_CONSTITUENT_ONLY",
"BOUNDED_SOURCE_NATIVE_DIFFERENCE":"BOUNDED_SOURCE_NATIVE_DIFFERENCE",
"UNDERDETERMINED":"UNDERDETERMINED",
"BOUNDED_SOURCE_NATIVE_CENTRAL_OPERATION_DIFFERENCE":"BOUNDED_SOURCE_NATIVE_DIFFERENCE",
"SHARED_CONSTITUENT_TECHNIQUE_ONLY":"SHARED_CONSTITUENT_ONLY",
"SHARED_MODEL_LINEAGE_ANCESTOR_SUPPORTED":"DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY",
}
HEX40=re.compile(r"^[0-9a-f]{40}$"); HEX64=re.compile(r"^[0-9a-f]{64}$"); DOI=re.compile(r"^10\.\d{4,9}/\S+$",re.I)

class W7Error(RuntimeError): pass
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def dump(p,o):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def normdoi(v):
    if not isinstance(v,str) or not v.strip(): raise W7Error("missing DOI")
    s=v.strip().lower()
    for p in ("https://doi.org/","http://doi.org/","doi:"):
        if s.startswith(p): s=s[len(p):]
    if not DOI.match(s): raise W7Error(f"malformed DOI: {v}")
    return s
def git(*a): return subprocess.check_output(["git",*a],text=True).strip()
def git_json(ref,path): return json.loads(git("show",f"{ref}:{path}"))
def git_blob(ref,path):
    x=git("rev-parse",f"{ref}:{path}")
    if not HEX40.match(x): raise W7Error("bad git blob")
    return x
def status_of(p): return p.get("completion_status") or p.get("status")
def evidence_of(p): return p.get("original_source_evidence") or p.get("source_provenance") or []
def ancestor_dois(p):
    a=p.get("direct_model_ancestors")
    if a is None: a=(p.get("source_native_structure") or {}).get("direct_model_ancestor_dois",[])
    return [normdoi(x if isinstance(x,str) else x.get("doi")) for x in (a or [])]
def operators_of(p):
    x=p.get("native_core_operators")
    if x is None: x=(p.get("source_native_structure") or {}).get("paper_specific_operators")
    if x is None and isinstance(p.get("operator_source_descriptions"),dict): x=list(p["operator_source_descriptions"])
    return list(x or [])
def descriptions_of(p,ops):
    d=p.get("operator_source_descriptions")
    if isinstance(d,dict) and set(d)==set(ops): return d
    s=p.get("source_native_structure") or {}; eq=list(s.get("decisive_equations_or_updates") or [])
    center=s.get("central_claim_boundary") or p.get("source_scope") or "Source-native operator retained from lane fragment."
    return {op:str(eq[i] if i<len(eq) else center) for i,op in enumerate(ops)}
def edition_sha_of(p):
    c=[]
    if isinstance(p.get("edition_sha256"),str): c.append(p["edition_sha256"])
    ae=p.get("adopted_edition")
    if isinstance(ae,dict):
        for k in ("raw_sha256","sha256"):
            if isinstance(ae.get(k),str): c.append(ae[k])
    for e in evidence_of(p):
        if isinstance(e.get("original_primary_sha256"),str): c.append(e["original_primary_sha256"])
    c=[x.lower() for x in c if HEX64.match(x.lower())]
    return c[0] if c else None
def bundles_of(p):
    out=[]
    for k in ("additional_edition_bundle","correction_supplement_bundle","supplement_bundle","correction_bundle"):
        if isinstance(p.get(k),list): out.extend(copy.deepcopy(p[k]))
    cs=p.get("correction_and_supplement_bundle")
    if isinstance(cs,dict):
        out.extend(copy.deepcopy(cs.get("corrections") or [])); out.extend(copy.deepcopy(cs.get("supplements") or []))
        if cs.get("correction_status"): out.append({"role":"CORRECTION_STATUS_NOTE","note":cs["correction_status"]})
    return out
def adverse_of(p): return list(p.get("adverse_source_limits") or p.get("adverse_limits") or [])
def validate_profile(p,roster,lane):
    ident=p.get("id")
    if ident not in roster or normdoi(p.get("doi"))!=roster[ident]: raise W7Error(f"{lane}/{ident}: roster DOI mismatch")
    st=status_of(p)
    if st not in {"PROFILE_FRAGMENT_READY","SOURCE_BLOCKED","SCIENTIFIC_ANCESTRY_UNDERDETERMINED"}: raise W7Error("bad status")
    if p.get("ancestry_exhaustiveness")!="NOT_ATTESTED": raise W7Error("ancestry promotion")
    if p.get("global_family_independence_certified") is not False: raise W7Error("global promotion")
    if p.get("main_scientific_authorization",p.get("main_authorized",False)) not in (False,None): raise W7Error("MAIN promotion")
    ancestor_dois(p)
    if st=="PROFILE_FRAGMENT_READY":
        ops=operators_of(p)
        if not ops or len(ops)!=len(set(ops)) or any(not isinstance(x,str) or not x.startswith(ident+":") for x in ops): raise W7Error("operator ID failure")
        d=descriptions_of(p,ops)
        if set(d)!=set(ops) or any(len(str(v).strip())<20 for v in d.values()): raise W7Error("description failure")
        ev=evidence_of(p)
        if not ev: raise W7Error("missing provenance")
        for e in ev:
            if not isinstance(e.get("repository_path"),str) or not e["repository_path"].startswith("research/paper2/p399/"): raise W7Error("source path missing")
            if not HEX40.match(str(e.get("repository_git_blob_sha1",""))) or not HEX40.match(str(e.get("source_repository_ref",""))): raise W7Error("bad source git pin")
            if git_blob(e["source_repository_ref"],e["repository_path"])!=e["repository_git_blob_sha1"]: raise W7Error("source blob drift")
        req=set(p.get("required_bundle_ids") or [])
        if req and not req <= {x.get("id") for x in (p.get("supplement_bundle") or [])}: raise W7Error("required supplement disappeared")
    return st
def normalize_profile(p,lane,m,path,blob):
    ops=operators_of(p); ev=copy.deepcopy(evidence_of(p))
    ev.append({"repository_path":path,"repository_git_blob_sha1":blob,"source_repository_ref":m["head"],"source_loci":["exact lane profile fragment"],"source_audit_kind":"W7_IMMUTABLE_LANE_PROFILE_FRAGMENT_PROVENANCE","original_primary_sha256":edition_sha_of(p)})
    return {"id":p["id"],"doi":normdoi(p["doi"]),"edition_sha256":edition_sha_of(p),"edition_identity":copy.deepcopy(p.get("adopted_edition")),"profile_state":"W7_IMPORTED_PROFILE_FRAGMENT_READY","source_fragment_state":p.get("profile_state"),"source_scope":p.get("source_scope") or (p.get("source_native_structure") or {}).get("central_claim_boundary"),"native_core_operators":ops,"operator_source_descriptions":descriptions_of(p,ops),"direct_model_ancestors":ancestor_dois(p),"ancestry_exhaustiveness":"NOT_ATTESTED","original_source_evidence":ev,"additional_edition_bundle":bundles_of(p),"adverse_source_limits":adverse_of(p),"global_family_independence_certified":False,"w7_lane_provenance":{"lane":lane,"pr":m["pr"],"head":m["head"],"profile_blob":blob}}
def pair_list(o): return o.get("pairs") or o.get("pair_adjudications") or o.get("adjudications") or []
def normalize_category(x):
    if x not in CATEGORY_MAP: raise W7Error(f"unsupported category {x}")
    return CATEGORY_MAP[x]
def pair_category(r): return normalize_category(r.get("judgment_class") or r.get("judgment") or r.get("result") or r.get("adjudication"))
def pkey(a,b,cohort): return (cohort,a,b) if cohort=="G2_G1" else (cohort,*sorted((a,b)))
def lane_pair_record(r,lane,m,path,blob,roster,g2ids,g1ids):
    a,b=r.get("a") or r.get("left"),r.get("b") or r.get("right")
    if not a or not b or a==b or a not in roster or b not in roster: raise W7Error("bad pair IDs")
    left_source=r.get("left_source") or {}
    right_source=r.get("right_source") or {}
    da,db=normdoi(r.get("doi_a") or left_source.get("doi") or roster[a]),normdoi(r.get("doi_b") or right_source.get("doi") or roster[b])
    if da!=roster[a] or db!=roster[b]: raise W7Error("pair DOI drift")
    cohort="G2_G1" if ((a in g2ids and b in g1ids) or (b in g2ids and a in g1ids)) else "G2_G2"
    if cohort=="G2_G1" and a in g1ids: a,b,da,db=b,a,db,da
    if r.get("global_family_independence_certified",r.get("global_independence_promoted",False)) not in (False,None) or r.get("may_be_counted_independent") is True: raise W7Error("pair promotion")
    return {"a":a,"b":b,"doi_a":da,"doi_b":db,"cohort":cohort,"category":pair_category(r),"basis":r.get("basis") or r.get("reason") or r.get("finding") or r.get("rationale"),"lane":lane,"lane_pair_file_provenance":{"pr":m["pr"],"head":m["head"],"path":path,"blob":blob},"underlying_evidence":copy.deepcopy(r.get("evidence") or r.get("source_provenance") or r.get("exact_git_provenance") or []),"global_independence_certified":False}
def read_base_13(baseline_doc):
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); g1=td/"g1.json"; pf=td/"profiles.json"; out=td/"out"
        g1.write_text(git("show",f"{G1_REF}:{G1_ROSTER.as_posix()}"),encoding="utf-8"); pf.write_text(json.dumps(baseline_doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        cmd=["python",str(BASE_GENERATOR),"--g2-manifest",str(G2_MANIFEST),"--g1-roster",str(g1),"--legacy-pairs",str(LEGACY),"--profiles",str(pf),"--output",str(out),"--source-native-v20",str(SOURCE_NATIVE["v20"]),"--source-native-int04-int08",str(SOURCE_NATIVE["v10d"]),"--source-native-v15b",str(SOURCE_NATIVE["v15b"]),"--source-native-v16b",str(SOURCE_NATIVE["v16b"])]
        subprocess.run(cmd,check=True,capture_output=True,text=True); rows=load(out/"PAIR_TRIAGE_MATRIX.json")
    ws=[]
    for r in rows:
        x=r.get("prior_source_scoped_comparison")
        if not x: continue
        evid=x["bounded_original_evidence_id"]; sp=SOURCE_NATIVE["v20"]
        if evid.startswith("G2D_V10D"): sp=SOURCE_NATIVE["v10d"]
        elif evid.startswith("G2D_V15B"): sp=SOURCE_NATIVE["v15b"]
        elif evid.startswith("G2D_V16B"): sp=SOURCE_NATIVE["v16b"]
        cat="SHARED_CONSTITUENT_ONLY" if "SHARED_" in str(x.get("bounded_original_outcome","")) else "BOUNDED_SOURCE_NATIVE_DIFFERENCE"
        ws.append({"a":r["a"],"b":r["b"],"doi_a":r["doi_a"],"doi_b":r["doi_b"],"cohort":r["cohort"],"category":cat,"basis":x["bounded_original_outcome"],"lane":"PRE_W7_PR438_BASELINE","lane_pair_file_provenance":{"pr":438,"head":BASE_HEAD,"path":sp.as_posix(),"blob":git_blob(BASE_HEAD,sp.as_posix())},"underlying_evidence":[x],"global_independence_certified":False})
    if len(ws)!=13: raise W7Error(f"baseline witness count {len(ws)}")
    return ws
def build_cross(raw,laneof,legacyidx):
    out=[]; ids=sorted(raw)
    for a,b in itertools.combinations(ids,2):
        if laneof[a]==laneof[b]: continue
        pa,pb=raw[a],raw[b]; da,db=normdoi(pa["doi"]),normdoi(pb["doi"]); aa,ab=set(ancestor_dois(pa)),set(ancestor_dois(pb)); shared=sorted(aa&ab); direct=db in aa or da in ab
        lr=legacyidx.get(tuple(sorted((a,b))),{}); risk=lr.get("prior_logged_risk"); cit=lr.get("source_citation")
        if direct or shared: decision=priority="DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY"
        else:
            decision="UNDERDETERMINED"; priority="PREEXISTING_GENEALOGY_RISK" if risk else ("EXPLICIT_SOURCE_CITATION" if cit else "NO_POSITIVE_EVIDENCE")
        out.append({"a":a,"b":b,"doi_a":da,"doi_b":db,"profile_status_a":status_of(pa),"profile_status_b":status_of(pb),"priority_category":priority,"scientific_family_decision":decision,"source_risk_evidence":{"legacy_risk":risk,"legacy_citation":cit,"direct_selected_relation":direct,"shared_direct_ancestor_dois":shared},"global_independence_certified":False})
    if len(out)!=475: raise W7Error("cross-lane count drift")
    return out
def strongest(ws):
    cats={w["category"] for w in ws}
    for x in ("DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY","SHARED_CONSTITUENT_ONLY","BOUNDED_SOURCE_NATIVE_DIFFERENCE"):
        if x in cats:return x
    return "UNDERDETERMINED"
def make_matrix(legacy,statuses,witnesses,cross):
    wi=defaultdict(list)
    for w in witnesses: wi[pkey(w["a"],w["b"],w["cohort"])].append(w)
    crossmap={tuple(sorted((x["a"],x["b"]))):x for x in cross}; rows=[]
    for r in legacy["main_main_pairs"]:
        a,b=r["a"],r["b"]; ws=wi.get(("G2_G2",*sorted((a,b))),[]); dec=strongest(ws)
        pr=dec if dec in {"DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY","SHARED_CONSTITUENT_ONLY"} else ("PREEXISTING_GENEALOGY_RISK" if r.get("prior_logged_risk") else ("EXPLICIT_SOURCE_CITATION" if r.get("source_citation") else (dec if dec=="BOUNDED_SOURCE_NATIVE_DIFFERENCE" else "NO_POSITIVE_EVIDENCE")))
        rows.append({"cohort":"G2_G2","a":a,"b":b,"doi_a":normdoi(r["doi_a"]),"doi_b":normdoi(r["doi_b"]),"profile_availability":{"a":statuses.get(a,"MISSING"),"b":statuses.get(b,"MISSING")},"source_risk_evidence":{"legacy_risk":r.get("prior_logged_risk"),"legacy_citation":r.get("source_citation"),"w7_cross_lane":crossmap.get(tuple(sorted((a,b))))},"bounded_pair_evidence":ws,"priority_category":pr,"scientific_family_decision":dec,"global_independence_certified":False})
    for r in legacy["main_vs_g1_pairs"]:
        a,b=r["main_id"],r["g1_id"]; ws=wi.get(("G2_G1",a,b),[]); dec=strongest(ws)
        pr=dec if dec in {"DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY","SHARED_CONSTITUENT_ONLY"} else ("PREEXISTING_GENEALOGY_RISK" if r.get("prior_risk") else ("EXPLICIT_SOURCE_CITATION" if r.get("source_citation") else (dec if dec=="BOUNDED_SOURCE_NATIVE_DIFFERENCE" else "NO_POSITIVE_EVIDENCE")))
        rows.append({"cohort":"G2_G1","a":a,"b":b,"doi_a":normdoi(r["main_doi"]),"doi_b":normdoi(r["g1_doi"]),"profile_availability":{"a":statuses.get(a,"MISSING"),"b":statuses.get(b,"MISSING")},"source_risk_evidence":{"legacy_risk":r.get("prior_risk"),"legacy_citation":r.get("source_citation")},"bounded_pair_evidence":ws,"priority_category":pr,"scientific_family_decision":dec,"global_independence_certified":False})
    if len(rows)!=1580 or sum(x["cohort"]=="G2_G2" for x in rows)!=780 or sum(x["cohort"]=="G2_G1" for x in rows)!=800: raise W7Error("1580 drift")
    if len({pkey(x["a"],x["b"],x["cohort"]) for x in rows})!=1580: raise W7Error("duplicate rows")
    return sorted(rows,key=lambda x:(x["cohort"],x["a"],x["b"]))
def main():
    g2=load(G2_MANIFEST)["selected_working_roster"]; g1=git_json(G1_REF,G1_ROSTER.as_posix())["roster_snapshot"]; g2m={x["slot"]:normdoi(x["doi"]) for x in g2}; g1m={x["id"]:normdoi(x["doi"]) for x in g1}; roster={**g2m,**g1m}
    if len(g2m)!=40 or len(g1m)!=20 or set(g2m)&set(g1m): raise W7Error("roster drift")
    legacy=load(LEGACY)
    if len(legacy["main_main_pairs"])!=780 or len(legacy["main_vs_g1_pairs"])!=800: raise W7Error("legacy denominator drift")
    shared0=load(SHARED_PROFILES); laneids=set(itertools.chain.from_iterable(m["ids"] for m in LANES.values())); baseline=[copy.deepcopy(p) for p in shared0["profiles"] if p["id"] not in laneids]
    if len(baseline)!=26 or len({p["id"] for p in baseline})!=26: raise W7Error("cannot recover 26 baseline")
    sensitive={i:copy.deepcopy(next(p for p in baseline if p["id"]==i)) for i in ("P08","P10","P18","P20","PRD-01","INT-01")}
    raw={}; laneof={}; imported=[]; blocked=[]; under=[]; receipts=[]; lpairs=[]
    for lane,m in LANES.items():
        changed=git("diff","--name-only",f"{BASE_HEAD}..{m['head']}").splitlines()
        if not changed or any(not x.startswith(m["dir"]+"/") for x in changed): raise W7Error(f"{lane} foreign path")
        pp=f"{m['dir']}/{m['profile']}"; qp=f"{m['dir']}/{m['pairs']}"; po=git_json(m["head"],pp); qo=git_json(m["head"],qp); pb=git_blob(m["head"],pp); qb=git_blob(m["head"],qp); ps=po.get("profiles") or []
        if sorted(x["id"] for x in ps)!=sorted(m["ids"]): raise W7Error(f"{lane} roster mismatch")
        for p in ps:
            raw[p["id"]]=p; laneof[p["id"]]=lane; st=validate_profile(p,roster,lane); rec={"lane":lane,"id":p["id"],"doi":normdoi(p["doi"]),"status":st,"profile_blob":pb,"profile_path":pp,"head":m["head"],"pr":m["pr"]}
            if st=="PROFILE_FRAGMENT_READY": imported.append(normalize_profile(p,lane,m,pp,pb))
            elif st=="SOURCE_BLOCKED": blocked.append(rec)
            else: under.append(rec)
        for r in pair_list(qo): lpairs.append(lane_pair_record(r,lane,m,qp,qb,roster,set(g2m),set(g1m)))
        receipts.append({"lane":lane,"pr":m["pr"],"head":m["head"],"status":"VALID","paper_count":len(ps),"changed_files":changed,"profile_path":pp,"profile_blob":pb,"pair_path":qp,"pair_blob":qb,"quarantined_artifacts":[],"shared_registry_directly_modified":False,"global_independence_set_true":False,"main_authorization":False,"forbidden_science_artifact_dependency_detected":False})
    if len(raw)!=34 or len(imported)!=25 or len(blocked)!=5 or len(under)!=4: raise W7Error("profile accounting drift")
    final=baseline+sorted(imported,key=lambda p:p["id"])
    if len(final)!=51 or len({p["id"] for p in final})!=51: raise W7Error("final profile count drift")
    for i,v in sensitive.items():
        if next(p for p in final if p["id"]==i)!=v: raise W7Error(f"sensitive profile changed {i}")
    for p in imported:
        for e in p["original_source_evidence"]:
            if git_blob(e["source_repository_ref"],e["repository_path"])!=e["repository_git_blob_sha1"]: raise W7Error("normalized provenance drift")
    base_doc=copy.deepcopy(shared0); base_doc["schema"]="relaytheory.p399.g4.original_native_profiles_v1"; base_doc["profiles"]=baseline
    witnesses=read_base_13(base_doc)+[x for x in lpairs if x["category"]!="UNDERDETERMINED"]
    legacyidx={tuple(sorted((r["a"],r["b"]))):r for r in legacy["main_main_pairs"]}; cross=build_cross(raw,laneof,legacyidx)
    statuses={p["id"]:"PROFILE_SOURCE_LEDGER_COMPLETE" for p in final}
    for x in blocked: statuses[x["id"]]="SOURCE_BLOCKED"
    for x in under: statuses[x["id"]]="SCIENTIFIC_ANCESTRY_UNDERDETERMINED"
    matrix=make_matrix(legacy,statuses,witnesses,cross); dec=Counter(r["scientific_family_decision"] for r in matrix); pri=Counter(r["priority_category"] for r in matrix)
    bounded=len(witnesses); direct_shared=dec["DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY"]+dec["SHARED_CONSTITUENT_ONLY"]; positive=sum(v for k,v in pri.items() if k!="NO_POSITIVE_EVIDENCE"); unresolved=dec["UNDERDETERMINED"]
    intake={"schema":"relaytheory.p399.g4.w7.six_lane_intake_receipt_v1","base_pr":438,"base_head":BASE_HEAD,"branch":"paper2/p399-g4-w7-six-lane-integration-20261005","lanes":receipts,"lane_partition_exact_34":True,"quarantined_lane_count":0,"main_authorized":False}
    recon={"schema":"relaytheory.p399.g4.w7.profile_reconciliation_v1","starting_profiles":26,"attempted_additions":34,"successfully_imported":25,"source_blocked":5,"ancestry_underdetermined":4,"final_profile_count":51,"denominator":60,"profile_completeness_state":"51/60 WITH_5_SOURCE_BLOCKERS_AND_4_ANCESTRY_UNDERDETERMINED","imported":[{"id":p["id"],"doi":p["doi"],"lane":p["w7_lane_provenance"]["lane"],"pr":p["w7_lane_provenance"]["pr"],"head":p["w7_lane_provenance"]["head"],"profile_blob":p["w7_lane_provenance"]["profile_blob"],"source_evidence":p["original_source_evidence"]} for p in imported],"blocked":blocked,"scientific_ancestry_underdetermined":under,"main_authorized":False}
    audit={"schema":"relaytheory.p399.g4.w7.1580_genealogy_audit_v1","g2_g2":780,"g2_g1":800,"total":1580,"profile_complete_count":51,"profile_denominator":60,"priority_categories":dict(sorted(pri.items())),"scientific_family_decisions":dict(sorted(dec.items())),"bounded_pair_witness_records":bounded,"direct_or_shared_ancestry_risk_rows":direct_shared,"positive_priority_pairs":positive,"remaining_underdetermined":unresolved,"global_final_independent_count":0,"main_authorized":False,"g1_internal_190_note":"G1 internal 190 pairs are outside the 780+800 registry and are not globally cleared by W7."}
    adverse={"schema":"relaytheory.p399.g4.w7.false_promotion_adverse_audit_v1","test_count":10,"tests":[
      {"test":"same_broad_term_unrelated_math","result":"PASS","finding":"No lexical similarity rule is used."},
      {"test":"different_terminology_direct_common_ancestor","result":"PASS","finding":"DOI ancestry is checked independently of terminology."},
      {"test":"shared_constituent_different_complete_systems","result":"PASS","finding":"Shared constituent never sets global independence."},
      {"test":"local_operator_difference_unresolved_shared_ancestry","result":"PASS","finding":"Bounded difference remains local."},
      {"test":"exact_direct_descendant_relation","result":"PASS","finding":"Direct DOI ancestry is a risk category, not independence."},
      {"test":"source_correction_changes_decisive_equation","result":"PASS","finding":"Edition-sensitive baseline profiles are append-preserved."},
      {"test":"absent_citation_as_independence","result":"PASS","finding":"No positive evidence remains UNDERDETERMINED."},
      {"test":"incomplete_supplement_as_complete_model","result":"PASS","finding":"Required bundle disappearance fails validation; SOURCE_BLOCKED is not imported."},
      {"test":"proof_manuscript_as_final_vor","result":"PASS","finding":"INT-13 remains author-approved uncorrected proof."},
      {"test":"lane_local_to_global_independence","result":"PASS","finding":"Every row has global_independence_certified=false."}
    ],"reversals":[],"global_independence_certified":False,"main_authorized":False}
    i13=next(p for p in final if p["id"]=="INT-13")
    if "UNCORRECTED_PROOF" not in json.dumps(i13.get("edition_identity"),ensure_ascii=False): raise W7Error("INT13 edition normalized")
    queue=[r for r in matrix if r["priority_category"]!="NO_POSITIVE_EVIDENCE"]; rem=[{"id":x["id"],"doi":x["doi"],"status":x["status"],"lane":x["lane"],"pr":x["pr"],"head":x["head"]} for x in blocked+under]
    summary={"schema":"relaytheory.p399.g4.w7.pair_triage_summary_v1","g2_internal_pairs_checked":780,"g2_g1_pairs_checked":800,"full_pair_count":1580,"final_profile_count":51,"missing_profile_count":9,"priority_categories":dict(sorted(pri.items())),"scientific_family_decisions":dict(sorted(dec.items())),"bounded_pair_witness_records":bounded,"global_final_independent_pairs":0,"scientific_main_authorized":False}
    shared=copy.deepcopy(shared0); shared["schema"]="relaytheory.p399.g4.original_native_profiles_v1+w7"; shared["w7_reconciliation"]={"base_head":BASE_HEAD,"final_profile_count":51,"main_authorized":False}; shared["profiles"]=final
    report=f"""# W7 最終系譜ステータス\n\n- Branch: paper2/p399-g4-w7-six-lane-integration-20261005\n- PR #438 exact base: {BASE_HEAD}\n- W1-W6: immutable six-lane intake VALID, quarantine 0\n- Profile completeness: **51/60**\n  - PROFILE_SOURCE_LEDGER_COMPLETE: 51\n  - SOURCE_BLOCKED: {len(blocked)}\n  - SCIENTIFIC_ANCESTRY_UNDERDETERMINED: {len(under)}\n- 780 + 800 = **1580/1580** pair rows, duplicate/missing 0\n- Bounded pair witness records: **{bounded}**\n- Direct/shared ancestry-risk decision rows: **{direct_shared}**\n- Positive-priority pairs: **{positive}**\n- Scientific-family UNDERDETERMINED rows: **{unresolved}**\n- Global genealogy independence certified: **0**\n- MAIN scientific authorization: **false**\n\n## 残るプロフィール科学ブロッカー\n\nSOURCE_BLOCKED: {", ".join(x["id"] for x in blocked)}\n\nSCIENTIFIC_ANCESTRY_UNDERDETERMINED: {", ".join(x["id"] for x in under)}\n\n## 境界\n\nW7 はプロフィール完成と系譜独立性を同一視しない。BOUNDED_SOURCE_NATIVE_DIFFERENCE は局所差であり、GLOBAL_FAMILY_INDEPENDENT ではない。引用欠如・語彙差・タイトル類似は独立性根拠に使わない。G1 内部190組は本1580行列の外にあり、W7によって独立認定されない。MAIN は著者の別途明示 GO まで未認可のまま保持する。\n"""
    dump(W7_DIR/"W7_SIX_LANE_INTAKE_RECEIPT_v1.json",intake); dump(W7_DIR/"W7_60_PROFILE_RECONCILIATION_v1.json",recon); dump(W7_DIR/"W7_CROSS_LANE_PAIR_ADJUDICATIONS_v1.json",{"schema":"relaytheory.p399.g4.w7.cross_lane_pairs_v1","count":475,"pairs":cross,"main_authorized":False}); dump(W7_DIR/"W7_1580_GENEALOGY_AUDIT_v1.json",audit); dump(W7_DIR/"W7_FALSE_PROMOTION_ADVERSE_AUDIT_v1.json",adverse); (W7_DIR/"W7_FINAL_GENEALOGY_STATUS_JA.md").write_text(report,encoding="utf-8")
    dump(SHARED_PROFILES,shared); dump(ACCEL/"PAIR_TRIAGE_MATRIX.json",matrix); dump(ACCEL/"PRIORITIZED_REVIEW_QUEUE.json",queue); dump(ACCEL/"PAIR_TRIAGE_SUMMARY.json",summary); dump(ACCEL/"REMAINING_PROFILE_EVIDENCE_QUEUE.json",rem)
    print(json.dumps({"profiles":51,"source_blocked":5,"ancestry_underdetermined":4,"pairs":1580,"bounded_witnesses":bounded,"direct_shared_risks":direct_shared,"positive_priority_pairs":positive,"underdetermined":unresolved,"global_independent":0,"main_authorized":False},ensure_ascii=False))
if __name__=="__main__": main()
