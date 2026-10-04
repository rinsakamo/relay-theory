#!/usr/bin/env python3
"""Paper 2 #384 F1 strict direct type audit: 68 original ClaimIR relations.

NO schema expansion, no inference of globally impossible encodability, and no
independent F2 reconstruction is claimed. Original v2 is checked out separately.
"""
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT=Path("paper/validation/jgps-major-revision/reflexive-audit-v1")
V2=Path("frozen-v2/paper/validation/jgps-major-revision/l-claim-assertion-carrier-schema-v2.json")
C_SHA="50fa50d24f2fbf9f3aef871cdeda08cdc97431a8"
D_SHA="7a4a9bb1df15aa1b12de51e9ca048565601964a0"
V2_SHA="058e0bd1514fcfaf57a4e87e366920b2fbcda274"
F1_SHA="f45593c1616ca0aceb43179ce9dc3fbc1ac279ab"
CONTRACT_SHA="f6abb3dfac040c0af8fb6576650233175402ce25"
CHALLENGE_SHA="d5af950c3b1b6ec5d6b7b155d5bba84cf4608fda"
PINNED_COMMIT="ad1c11789814413b1d9fd3ca8a4cfb6f7316f230"
EXPECTED={"TYPE_DOMAIN_ADMISSIBLE":8,"UNQUALIFIED_L_CLAIM":38,
          "L_FORMAL":3,"L_FORMAL_AND_UNQUALIFIED_L_CLAIM":19}
POSITIVE={"RFX10B.r2","RFX10C.r3"}

def j(path):
    return json.loads(path.read_text(encoding="utf-8"))
def git(*args):
    return subprocess.run(["git",*args],capture_output=True,text=True,check=True).stdout.strip()
def sha(path):
    return git("hash-object",str(path))
def check(ok,msg):
    if not ok:
        raise AssertionError(msg)

def validate():
    cp=ROOT/"reflexive-claimir-candidates-v1.json"
    dp=ROOT/"reflexive-stage-d-index-v1.json"
    ctp=ROOT/"stage-f1-strict-direct-contract-v1.json"
    chp=ROOT/"stage-f1-semantic-challenges-v1.json"
    f1p=ROOT/"stage-f1-strict-direct-type-audit-v1.json"
    check(all([sha(cp)==C_SHA,sha(dp)==D_SHA,sha(V2)==V2_SHA,
               sha(ctp)==CONTRACT_SHA,sha(chp)==CHALLENGE_SHA,sha(f1p)==F1_SHA]),
          "Frozen F1 input or output blob drift")
    check(git("-C","frozen-v2","rev-parse","HEAD")==PINNED_COMMIT,
          "Original carrier schema not checked out at pinned pre-validation commit")
    c,d,contract,ch,f,v2=map(j,[cp,dp,ctp,chp,f1p,V2])
    check(contract["status"]=="FROZEN_BEFORE_F1_ENCODING_ATTEMPT"
          and ch["status"]=="FROZEN_BEFORE_F1_RESULT"
          and f["status"]=="F1_DIRECT_TYPE_SCREEN_FROZEN_SEMANTIC_PRESERVATION_NOT_CLOSED"
          and f["provenance"]["prior_f1_contract_sha"]==CONTRACT_SHA
          and f["provenance"]["prior_challenge_sha"]==CHALLENGE_SHA
          and f["provenance"]["frozen_v2_sha"]==V2_SHA,
          "F1 preregistered sequencing drift")
    check(v2["architecture_layers"]==["L_sys","L_ctx","L_claim"]
          and "THEORETICAL_ACCOUNT" in v2["claim_object_types"]
          and "L_formal" not in v2["architecture_layers"],
          "Frozen v2 direct type vocabulary changed")
    check("COMPARISON" in v2["predicate_families"]
          and all(z in v2["qualifiers"] for z in ("DISTINCT","EQUIVALENT"))
          and all(z in v2["reference_roles"] for z in ("SUBJECT","COMPARATOR")),
          "Positive control vocabulary no longer licensed")
    byid={x["self_target_id"]:x for x in c["candidates"]}
    expected_challenges={}
    for case in ch["challenges"]:
        for rid in case["target_ids"]:
            expected_challenges.setdefault(rid,[]).append(case["feature"])
    typerecs={}
    for i in range(1,7):
        path=ROOT/f"stage-d-placement-batch-{i}-v1.json"
        entry=d["batches"][i-1]
        check(entry["git_blob_sha"]==sha(path)
              and f["provenance"]["six_stage_d_pinned_batches"][i-1]["sha"]==sha(path),
              "Stage D type prefit blob drift")
        batch=j(path)
        for e in batch["entries"]:
            original=byid[e["id"]]["claimir"]["claim_core"]
            nodes={n["id"]:n for n in original["nodes"]}
            relations={r["id"]:r for r in original["relations"]}
            for r in e["relations"]:
                rid=e["id"]+"."+r["relation_id"]
                check(rid not in typerecs,"Duplicate relation "+rid)
                source=relations[r["relation_id"]]
                check(source["arguments"]==r["original_arguments"]
                      and source["kind"]==r["original_kind"],
                      "Frozen source relation changed "+rid)
                formal=[n["node"] for n in r["argument_bindings"]
                        if n["layer"]=="L_formal"]
                claim=[n["node"] for n in r["argument_bindings"]
                       if n["layer"]=="L_claim" and
                       nodes[n["node"]].get("claim_object_type")!="THEORETICAL_ACCOUNT"]
                typerecs[rid]=(source,formal,claim,r,nodes,byid[e["id"]]["claimir"]["claim_id"])
    check(len(typerecs)==68 and len(f["relations"])==68,
          "F1 complete 68 relation coverage drift")
    actual_counts=Counter()
    prospective=[]
    n_challenged=0
    eligible=[]
    for record in f["relations"]:
        rid=record["audit_id"]
        check(rid in typerecs and rid not in prospective,
              "Unexpected/duplicate F1 relation "+rid)
        prospective.append(rid)
        source,formal,claim,r,nodes,claim_id=typerecs[rid]
        expected_type=("L_FORMAL_AND_UNQUALIFIED_L_CLAIM" if formal and claim
                       else "L_FORMAL" if formal else
                       "UNQUALIFIED_L_CLAIM" if claim else "TYPE_DOMAIN_ADMISSIBLE")
        check(record["source_kind"]==source["kind"]
              and record["source_arguments"]==source["arguments"]
              and record["typed_domain_case"]==expected_type
              and record["unsupported_direct_formal_arguments"]==formal
              and record["claim_object_arguments_without_frozen_THEORETICAL_ACCOUNT_qualification"]==claim,
              "F1 typed screen is inconsistent with source ClaimIR "+rid)
        check(record["precommitted_challenge_features"]==expected_challenges.get(rid,[])
              and record["definitive_semantic_impossibility_claimed"] is False
              and record["exact_full_validated"] is False,
              "F1 adversarial qualification overclaim "+rid)
        if record["precommitted_challenge_features"]:
            n_challenged+=1
        actual_counts[expected_type]+=1
        obj=record["candidate_explicit_v2_record"]
        if rid in POSITIVE:
            check(expected_type=="TYPE_DOMAIN_ADMISSIBLE" and obj is not None,
                  "Positive control must be direct-type admissible "+rid)
            check(obj["assertion_id"]==rid and
                  obj["claim_id"]==claim_id and
                  obj["source_relation_id"]==r["relation_id"] and
                  obj["source_kind"]==source["kind"] and
                  obj["source_arguments"]==source["arguments"] and
                  obj["predicate_family"]=="COMPARISON" and
                  obj["qualifiers"]==["DISTINCT"] and
                  obj["directionality"] is None and obj["evaluation"] is None and
                  obj["semantic_references"]==[] and
                  obj["support_provenance"]==[] and
                  obj["assertion_scope_qualifiers"]==[],
                  "Unsupported positive control payload "+rid)
            check(obj["argument_bindings"]==
                  [{"node_id":a["node"],"semantic_role":
                    "SUBJECT" if ix==0 else "COMPARATOR","layer":a["layer"]}
                    for ix,a in enumerate(r["argument_bindings"])],
                  "Positive control source argument role/typing changed "+rid)
            check(obj["audit_status"]==
                  "CLOSED_VOCABULARY_COMPOSITION_CANDIDATE_PENDING_INDEPENDENT_RECONSTRUCTION"
                  and record["exact_semantic_result"]==
                  "COMPOSITION_CANDIDATE_ONLY_NOT_INDEPENDENT_FULL",
                  "Positive example improperly marked independent FULL")
        else:
            check(obj is None,"Unregistered positive control "+rid)
        if expected_type=="TYPE_DOMAIN_ADMISSIBLE":
            eligible.append(rid)
    check(dict(actual_counts)==EXPECTED and n_challenged==25
          and set(prospective)==set(typerecs),
          "F1 summary or challenge coverage drift")
    s=f["summary"]
    check(s["type_case_counts"]==EXPECTED and s["total_relations"]==68
          and s["l_formal_direct_binding_gap_incidence"]==22
          and s["unqualified_l_claim_binding_incidence"]==57
          and s["both_incidence"]==19
          and s["union_direct_binding_not_licensed"]==60
          and s["type_domain_admissible"]==8
          and s["precommitted_semantic_challenge_relations"]==25
          and set(s["scoped_schema_composition_candidate_ids"])==POSITIVE
          and s["independently_verified_semantically_FULL_count"]==0
          and s["proven_global_non_encodability_count"]==0,
          "F1 aggregation or unjustified success changed")
    check(len(eligible)==8,
          "Exactly eight relations must have no frozen direct-type blocker")
    return {"status":"PASS","original_claims":47,"relation_count":68,
            "frozen_direct_type_obstacles_union":60,
            "L_formal_occurrence_relations":22,
            "L_claim_unqualified_occurrence_relations":57,
            "overlap":19,"type_domain_admissible":8,
            "precommitted_semantic_challenges":25,
            "closed_vocabulary_composition_candidates":sorted(POSITIVE),
            "independently_verified_FULL":0,"global_impossibility_proved":False,
            "terminal":"RFX47_F1_STRICT_DIRECT_TYPE_SCREEN_VALIDATION_PASS"}

if __name__=="__main__":
    first=validate()
    assert validate()==first,"F1 validator nondeterministic"
    print(json.dumps(first,indent=2,sort_keys=True,ensure_ascii=False))
