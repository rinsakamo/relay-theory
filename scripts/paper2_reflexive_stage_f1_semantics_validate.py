#!/usr/bin/env python3
"""Validate frozen, adversarial F1 semantic inventory under original unchanged v2.

An absent explicit operator is a strict direct-representation challenge, NOT
a theorem that no alternative composition can possibly express the claim.
"""
import json
import subprocess
from pathlib import Path

ROOT=Path("paper/validation/jgps-major-revision/reflexive-audit-v1")
V2=Path("frozen-v2/paper/validation/jgps-major-revision/l-claim-assertion-carrier-schema-v2.json")
SCHEMA_SHA="058e0bd1514fcfaf57a4e87e366920b2fbcda274"
F1_SHA="f45593c1616ca0aceb43179ce9dc3fbc1ac279ab"
CH_SHA="d5af950c3b1b6ec5d6b7b155d5bba84cf4608fda"
CONTRACT_SHA="f6abb3dfac040c0af8fb6576650233175402ce25"
RESULT_SHA="55f513e132537f902c9984a0fa5975d871c3930c"
FREEZE_COMMIT="ad1c11789814413b1d9fd3ca8a4cfb6f7316f230"
FEATURES={
  "LOGICAL_NON_ENTAILMENT",
  "EPISTEMIC_NON_ESTABLISHMENT",
  "CRITERION_RELATIVE_LICENSE",
  "VALIDATION_PROVENANCE_TEMPORAL_ORDER",
  "SCHEMA_COMPOSITION_POSITIVE_CONTROL",
  "NUMERIC_CARDINALITY_AND_CLASSIFICATION",
  "PRESERVE_REFERENT_CARRIER_PRECISION_WITNESS"
}

def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def git(*args):
    return subprocess.run(["git",*args],capture_output=True,text=True,check=True).stdout.strip()

def ok(pred,msg):
    if not pred:
        raise AssertionError(msg)

def validate():
    ch=j(ROOT/"stage-f1-semantic-challenges-v1.json")
    t=j(ROOT/"stage-f1-strict-direct-type-audit-v1.json")
    q=j(ROOT/"stage-f1-strict-direct-contract-v1.json")
    a=j(ROOT/"stage-f1-semantic-inventory-audit-v1.json")
    v2=j(V2)
    expected_sha=[
      (ROOT/"stage-f1-semantic-challenges-v1.json",CH_SHA),
      (ROOT/"stage-f1-strict-direct-type-audit-v1.json",F1_SHA),
      (ROOT/"stage-f1-strict-direct-contract-v1.json",CONTRACT_SHA),
      (ROOT/"stage-f1-semantic-inventory-audit-v1.json",RESULT_SHA),
      (V2,SCHEMA_SHA)
    ]
    for path,sha in expected_sha:
        ok(git("hash-object",str(path))==sha,"SHA drift "+str(path))
    ok(git("-C","frozen-v2","rev-parse","HEAD")==FREEZE_COMMIT,
       "frozen original v2 source commit mismatch")
    ok(a["status"]=="F1_SEMANTIC_INVENTORY_AUDITED_EXACT_FIDELITY_STILL_OPEN"
       and a["frozen_inputs"]["precommitted_challenges_sha"]==CH_SHA
       and a["frozen_inputs"]["strict_direct_type_screen_sha"]==F1_SHA
       and a["frozen_inputs"]["precommitted_f1_contract_sha"]==CONTRACT_SHA
       and a["frozen_inputs"]["v2_sha"]==SCHEMA_SHA,
       "semantic evaluation must use earlier frozen F1 inputs")
    ok({x["feature"] for x in a["audits"]}==FEATURES
       and len(a["audits"])==len(ch["challenges"])==7,
       "seven predeclared semantic comparison families not preserved")
    tags=set()
    for actual,original in zip(a["audits"],ch["challenges"]):
        ok(actual["feature"]==original["feature"]
           and actual["precommitted_target_ids"]==original["target_ids"]
           and actual["distinct_contrast_obligation"]==
               original["precommitted_decisive_test"]
           and "universal" in actual["inferential_guardrail"],
           "original contrast/order/anti-overclaim altered")
        tags.update(actual["precommitted_target_ids"])
    ok(len(tags)==25 and
       tags==set(x["audit_id"] for x in t["relations"]
                 if x["precommitted_challenge_features"]),
       "semantic challenge target coverage drift")
    fields=list(v2["carrier_fields"])
    has_epistemic=any(("EPISTEM" in y or "ESTABLISH" in y)
        for y in [*v2["predicate_families"],*v2["qualifiers"],*map(str.upper,fields)])
    has_entailment=any(("ENTAIL" in y or "MODAL" in y)
        for y in v2["predicate_families"])
    has_positive=("COMPARISON" in v2["predicate_families"]
        and "DISTINCT" in v2["qualifiers"]
        and "EQUIVALENT" in v2["qualifiers"])
    ok(not has_epistemic and not has_entailment and has_positive,
       "frozen v2 semantic vocabulary facts changed")
    actual=a["summary"]
    ok(actual["challenge_families"]==7
       and actual["distinct_target_relations"]==25
       and actual["direct_v2_epistemic_status_operator_declared"] is False
       and actual["direct_v2_logical_entailment_operator_declared"] is False
       and actual["positive_comparison_distinct_controls_available"] is True
       and actual["constructed_composition_candidates"]==2
       and actual["independently_confirmed_full_semantic_encodings"]==0
       and actual["logical_or_epistemic_semantic_failure_as_universal_theorem"] is False,
       "F1 semantic audit made an unsupported completeness/impossibility claim")
    ok({x["relation"] for x in a["key_witnesses"]}==
       {"RFX13C.r2","RFX01A.r1","RFX15D.r5","RFX10B.r2"},
       "direct explicit challenge/positive witnesses have changed")
    return {"status":"PASS","frozen_semantic_challenge_families":7,
        "target_relations":25,"explicit_v2_logical_entailment_operator":False,
        "explicit_v2_epistemic_status_operator":False,
        "positive_distinction_candidate_records":2,
        "independent_semantic_FULL_confirmed":0,
        "global_nonencodability_proved":False,
        "terminal":"RFX47_F1_SEMANTIC_INVENTORY_SCOPE_CI_PASS"}

if __name__=="__main__":
    a=validate()
    assert validate()==a,"F1 semantic inventory nondeterministic"
    print(json.dumps(a,sort_keys=True,indent=2,ensure_ascii=False))
