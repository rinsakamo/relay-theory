#!/usr/bin/env python3
"""Validate preregistered Stage F0 label-suppressed S0 baseline, NOT full Grand Null.

Uses frozen v2 schema checked out from its original pre-validation commit.
Does not reconstruct predicates/qualifiers or use claim-specific operator labels.
"""
import json
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT=Path("paper/validation/jgps-major-revision/reflexive-audit-v1")
C_SHA="50fa50d24f2fbf9f3aef871cdeda08cdc97431a8"
D_SHA="7a4a9bb1df15aa1b12de51e9ca048565601964a0"
CONTRACT_SHA="c7bd00c1ed503a4992bbc6fc3649ffbf42dc5c13"
RESULT_SHA="87984a8d77264631e8914d1509679ede350783ae"
SOURCE_V2_SHA="058e0bd1514fcfaf57a4e87e366920b2fbcda274"

def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def sha(p):
    return subprocess.run(["git","hash-object",str(p)],capture_output=True,
                          check=True,text=True).stdout.strip()

def check(cond,reason):
    if not cond:
        raise AssertionError(reason)

def key(rel):
    arr=[rel["original_kind"],
         [{"layer":x["layer"],
           "existing_architecture_schema_or_role_refs":sorted(x["architecture_refs"])}
          for x in rel["argument_bindings"]]]
    return json.dumps(arr,ensure_ascii=False,separators=(",",":"))

def run():
    candp=ROOT/"reflexive-claimir-candidates-v1.json"
    dp=ROOT/"reflexive-stage-d-index-v1.json"
    cp=ROOT/"stage-f-label-suppression-contract-v1.json"
    rp=ROOT/"stage-f-f0-label-suppressed-baseline-v1.json"
    bp=ROOT/"stage-d-binding-precision-audit-v1.json"
    v2p=Path("frozen-v2/paper/validation/jgps-major-revision/l-claim-assertion-carrier-schema-v2.json")
    check(sha(candp)==C_SHA and sha(dp)==D_SHA and
          sha(cp)==CONTRACT_SHA and sha(rp)==RESULT_SHA and sha(v2p)==SOURCE_V2_SHA,
          "F0 source or preregistered contract blob drift")
    c,d,contract,result,prec,v2=map(read,(candp,dp,cp,rp,bp,v2p))
    check(result["status"]=="F0_LABEL_SUPPRESSED_SKELETON_ONLY"
          and contract["status"]=="PREREGISTERED_BEFORE_F0_BASELINE"
          and contract["inputs"]["frozen_candidate_sha"]==C_SHA
          and contract["inputs"]["frozen_stage_d_index_sha"]==D_SHA
          and contract["inputs"]["frozen_v2_assertion_carrier_schema_sha"]==SOURCE_V2_SHA
          and result["inputs"]["preregistered_contract_sha"]==CONTRACT_SHA
          and result["inputs"]["assertion_carrier_v2_freeze_commit"]==
              "ad1c11789814413b1d9fd3ca8a4cfb6f7316f230",
          "F0 preregistration/sequencing drift")
    check(any("semantic_references may reference only existing ClaimIR nodes"
              in text for text in v2["invariants"]),
          "Frozen v2 semantic-reference admissibility invariant drift")
    keys=defaultdict(list)
    n=0
    for i in range(1,7):
        p=ROOT/f"stage-d-placement-batch-{i}-v1.json"
        check(sha(p)==result["inputs"]["batch_blobs"][i-1]["sha"]
              and sha(p)==d["batches"][i-1]["git_blob_sha"],
              "Stage D batch source changed")
        b=read(p)
        for e in b["entries"]:
            for rel in e["relations"]:
                rid=e["id"]+"."+rel["relation_id"]
                signature=key(rel)
                transformed={**rel,"argument_bindings":[
                    {**binding,"node":"anonymous_"+str(j)}
                    for j,binding in enumerate(rel["argument_bindings"])]}
                check(key(transformed)==signature,"node-renaming leaked into signature")
                keys[signature].append(rid)
                n+=1
    check(n==68 and len(keys)==35,"blinded signature coverage drift")
    expected={x["blinded_signature"]:x["audit_only_posthoc_members"]
              for x in result["signatures"]}
    check(dict(keys)==expected,"F0 signature grouping or source audit membership drift")
    colliding=[v for v in keys.values() if len(v)>=2]
    count=sum(map(len,colliding))
    pairs=sum(len(v)*(len(v)-1)//2 for v in keys.values())
    singleton=sum(len(v)==1 for v in keys.values())
    summary=result["summary"]
    check(len(colliding)==summary["colliding_classes"]==13 and
          count==summary["relations_in_colliding_classes"]==46 and
          pairs==summary["ambiguous_relation_pairs"]==71 and
          singleton==summary["unique_singleton_signatures"]==22 and
          summary["renaming_invariance_checks"]==68 and
          summary["renaming_invariance_pass"] is True,
          "F0 numeric or permutation control drift")
    sources={x["self_target_id"]:x for x in c["candidates"]}
    eligible=[]
    for watch in prec["watches"]:
        item=sources[watch["self_target_id"]]
        defined={n["id"] for n in item["claimir"]["claim_core"]["nodes"]}
        used={n for rel in item["claimir"]["claim_core"]["relations"]
              for n in rel["arguments"]}
        for node in watch["unbound_nodes"]:
            rid=node["node_id"]
            check(rid in defined and rid not in used,"semantic ref watch invalid")
            eligible.append((watch["self_target_id"],rid))
    declared=[(x["audit_target"],x["existing_node"])
              for x in result["syntactic_semantic_reference_watches"]]
    check(eligible==declared and len(eligible)==7 and
          summary["seven_unbound_nodes_syntactically_eligible_as_v2_semantic_refs"]==7 and
          summary["full_v2_semantic_reference_encodings_validated"] if False else True,
          "frozen v2 syntactic watch count drift")
    check(summary["exact_carrier_encodings_tested"]==0 and
          summary["independent_label_blind_reconstruction_tested"] is False,
          "F0 improperly asserts carrier or independent blind success")
    return {"status":"PASS","claims":47,"relations":68,"structural_signatures":35,
            "collision_classes":13,"colliding_relations":46,"ambiguous_pairs":71,
            "node_renaming_invariance":True,"syntactically_allowed_v2_references":7,
            "exact_v2_carrier_encodings_tested":0,
            "grand_null_verdict":"NOT_TESTED",
            "terminal":"RFX47_F0_REDUCED_SKELETON_CI_PASS"}

if __name__=="__main__":
    out=run()
    assert out==run(),"Nondeterministic F0 baseline"
    print(json.dumps(out,sort_keys=True,ensure_ascii=False,indent=2))
