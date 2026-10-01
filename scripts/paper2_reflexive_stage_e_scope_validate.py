#!/usr/bin/env python3
"""Independent Stage E scope test for 47 Paper 2 second-order targets.

Zero eligible direct system relations is NOT zero failures or a success percentage.
This script must not use or import Stage C Evidence Profile for classifications.
"""
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path("paper/validation/jgps-major-revision/reflexive-audit-v1")
C_SHA = "50fa50d24f2fbf9f3aef871cdeda08cdc97431a8"
D_INDEX_SHA = "7a4a9bb1df15aa1b12de51e9ca048565601964a0"
CONTRACT_SHA = "e47aee36b66b3767794865093716330466a2c2a5"
AUDIT_SHA = "1632c74265453368bbe61c67f0e53dec47123bcf"
FROZEN_LAYERS_SHA = "150fbb166541ba52abbe07124924fab63a1ad575"
ALLOWED = {"G_cog", "Pi", "X", "C", "Q", "P_in", "P_out", "K", "T", "rho/O"}
CATEGORY_COUNTS = {
 "ROLE_PROVENANCE_OR_FACTORING":5,
 "STRICT_COMPARATOR_META_VIEW":2,
 "ARCHITECTURE_SCHEMA_REFERENCE":2,
 "NEGATED_OR_NON_ENTAILED_ROLE_REFERENCE":4,
 "CROSS_BOUNDARY_TYPE_DISTINCTION":3
}

def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def gitsha(p):
    return subprocess.run(["git","hash-object",str(p)],capture_output=True,
                          text=True,check=True).stdout.strip()

def require(cond,msg):
    if not cond:
        raise AssertionError(msg)

def validate():
    base=ROOT
    c=read(base/"reflexive-claimir-candidates-v1.json")
    d=read(base/"reflexive-stage-d-index-v1.json")
    contract=read(base/"stage-e-role-reference-contract-v1.json")
    a=read(base/"stage-e-role-reference-audit-v1.json")
    layers=read("research/paper2/grammar_v0_layered_architecture_v1.json")
    require(gitsha(base/"reflexive-claimir-candidates-v1.json")==C_SHA and
            gitsha(base/"reflexive-stage-d-index-v1.json")==D_INDEX_SHA and
            gitsha(base/"stage-e-role-reference-contract-v1.json")==CONTRACT_SHA and
            gitsha(base/"stage-e-role-reference-audit-v1.json")==AUDIT_SHA and
            gitsha("research/paper2/grammar_v0_layered_architecture_v1.json")==FROZEN_LAYERS_SHA,
            "Stage E fixed authority blob drift")
    require(contract["status"]=="FROZEN_BEFORE_ROLE_REFERENCE_AUDIT"
            and contract["inputs"]["stage_d_index_blob_sha"]==D_INDEX_SHA
            and contract["inputs"]["layered_architecture_blob_sha"]==FROZEN_LAYERS_SHA
            and set(contract["allowed_schema_referents"])==ALLOWED,
            "Stage E contract or allowed roles drift")
    require(set(layers["layers"]["L_sys"]["roles"])==ALLOWED-{"G_cog"},
            "Frozen Grammar roles changed")
    require(a["inputs"]["contract_git_blob_sha"]==CONTRACT_SHA and
            a["inputs"]["stage_d_index_sha"]==D_INDEX_SHA,
            "Stage E audit sequencing drift")
    source={}
    for i in range(1,7):
        p=base/f"stage-d-placement-batch-{i}-v1.json"
        sha=gitsha(p)
        require(sha==a["inputs"]["stage_d_batch_pins"][i-1]["sha"]
                and sha==d["batches"][i-1]["git_blob_sha"],
                "Stage D batch pin drift")
        b=read(p)
        for entry in b["entries"]:
            for rel in entry["relations"]:
                source[entry["id"]+"."+rel["relation_id"]]=rel
    require(len(source)==68 and len(a["all_relation_scope"])==68
            and set(r["relation"] for r in a["all_relation_scope"])==set(source),
            "68 source relations not preserved")
    categories=Counter()
    direct=0
    bindings=0
    group_refs=[]
    det={}
    for r in a["all_relation_scope"]:
        k=r["relation"]
        src=source[k]
        present="L_sys" in src["referenced_layers"]
        require(r["l_sys_referent_present"]==present and
                r["assertion_type"]=="SECOND_ORDER_RESEARCH_OR_METHOD_ASSERTION"
                and r["direct_object_level_l_sys_relation"] is False
                and r["eligible_for_direct_role_full_partial_residual"] is False,
                "Meta-assertion illegitimately converted to system relation " + k)
        direct+=int(r["eligible_for_direct_role_full_partial_residual"])
    for r in a["referent_audit"]:
        k=r["relation"]
        require(k in source and "L_sys" in source[k]["referenced_layers"]
                and r["operator"]==source[k]["assertion_operator"]
                and r["source_argument_ids"]==source[k]["original_arguments"],
                "Stage E referent provenance drift " + k)
        sys=[n for n in source[k]["argument_bindings"] if n["layer"]=="L_sys"]
        require(len(sys)==len(r["l_sys_referents"]),
                "L_sys-bound argument loss " + k)
        for bound,ref in zip(sys,r["l_sys_referents"]):
            require(ref["node_id"]==bound["node"] and
                    ref["architecture_refs"]==bound["architecture_refs"] and
                    set(ref["architecture_refs"])<=ALLOWED and
                    ref["reference_verified_against_frozen_role_inventory"] is True,
                    "Non-frozen role introduction " + k)
            if not ref["architecture_refs"]:
                group_refs.append({"relation":k,"node_id":ref["node_id"]})
            bindings+=1
        require(r["direct_role_mapping_result"]=="NOT_TESTABLE_SECOND_ORDER_META_ASSERTION"
                and r["new_top_level_role_inferred"] is False and
                r["exact_carrier_encoding_inferred"] is False,
                "Unwarranted role or exact carrier result " + k)
        categories[r["category"]]+=1
        det[k]=r
    require(len(det)==16 and bindings==19 and
            dict(categories)==CATEGORY_COUNTS and direct==0,
            "Frozen role-reference scope count drift")
    summary=a["summary"]
    require(summary["relations"]==68
            and summary["l_sys_referent_bearing_meta_relations"]==16
            and summary["l_sys_referent_argument_bindings"]==19
            and summary["direct_object_level_cognitive_system_relations_eligible"]==0
            and summary["direct_system_role_coverage_denominator"]==0
            and summary["direct_system_role_coverage_rate"] is None
            and summary["new_top_level_role_proved_necessary"] is None
            and summary["new_top_level_role_absence_proved"] is False
            and summary["coarse_group_reference_nodes_not_explicitly_enumerated"]==group_refs,
            "Zero-denominator or coarse role reference overclaim")
    require(set(det).isdisjoint(set(k for k,r in source.items() if "L_sys" not in r["referenced_layers"])),
            "Role reference count inflated")
    return {"status":"PASS","claims":47,"relations":68,
            "l_sys_meta_references":16,"l_sys_argument_bindings":19,
            "direct_object_level_eligible":0,
            "role_fit_fraction":None,"role_gap_absence_proved":False,
            "coarse_unenumerated_role_groups":len(group_refs),
            "terminal":"RFX47_STAGE_E_SCOPED_ROLE_REFERENT_CI_PASS"}

if __name__=="__main__":
    a=validate()
    assert a==validate(),"Nondeterministic Stage E validation"
    print(json.dumps(a,ensure_ascii=False,sort_keys=True,indent=2))
