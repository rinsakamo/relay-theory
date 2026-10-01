#!/usr/bin/env python3
"""Check frozen F2 blind-pilot integrity, not independent semantic performance."""
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT=Path("paper/validation/jgps-major-revision/reflexive-audit-v1")
CONTRACT_SHA="be667106d04c598f5e6b0dd20ae75032f0447dd7"
FORMAT_SHA="6d2c470d642efd9213dbc7ab6d256519fabef7fe"
PACKET_SHA="fd03e0ec9735f419e69ad07ab5a38e7d9551042b"
F1_SHA="55f513e132537f902c9984a0fa5975d871c3930c"
V2_SHA="058e0bd1514fcfaf57a4e87e366920b2fbcda274"
V2_COMMIT="ad1c11789814413b1d9fd3ca8a4cfb6f7316f230"
LAYER_ALLOWED={"L_sys","L_ctx","L_claim"}
NODE_ROLE_ALLOWED={"input","response_or_outcome","criterion","state_or_structure"}
BANNED=("RFX","AHV","PVS","Paper 2","Grammar v0","Grand Null","RelayTheory")
EXPECTED_PAIRS={f"J{i}":2 for i in range(1,9)}

def j(p):
    return json.loads(p.read_text(encoding="utf-8"))

def cmd(*args):
    return subprocess.run(["git",*args],capture_output=True,text=True,check=True).stdout.strip()

def need(condition,message):
    if not condition:
        raise AssertionError(message)

def check():
    contract_path=ROOT/"stage-f2-blind-pilot-contract-v1.json"
    format_path=ROOT/"stage-f2-assessor-output-schema-v1.json"
    packet_path=ROOT/"stage-f2-blind-pilot-cards-v1.json"
    f1path=ROOT/"stage-f1-semantic-inventory-audit-v1.json"
    v2path=Path("frozen-v2/paper/validation/jgps-major-revision/l-claim-assertion-carrier-schema-v2.json")
    for path,expected in (
        (contract_path,CONTRACT_SHA),(format_path,FORMAT_SHA),
        (packet_path,PACKET_SHA),(f1path,F1_SHA),(v2path,V2_SHA)):
        need(cmd("hash-object",str(path))==expected,"frozen pilot input drift: "+str(path))
    need(cmd("-C","frozen-v2","rev-parse","HEAD")==V2_COMMIT,
         "original frozen v2 commit replaced")
    contract=j(contract_path);output=j(format_path);packet=j(packet_path);v2=j(v2path)
    need(contract["status"]=="PREREGISTERED_PILOT_PROTOCOL_BEFORE_BLIND_PACKET"
         and contract["frozen_inputs"]["f1_semantic_audit_sha"]==F1_SHA
         and contract["frozen_inputs"]["original_v2_schema_blob_sha"]==V2_SHA
         and packet["status"]=="BLIND_PACKET_PREPARED_NOT_ADMINISTERED",
         "F2 pre-registration and unadministered status drift")
    need(output["status"]=="FORMAT_ONLY_NO_ASSESSOR_SUBMISSION"
         and output["submission_status"].startswith("NOT_SUBMITTED"),
         "template not an independent assessment")
    need(packet["frozen_allowed_carrier"]["git_blob_sha"]==V2_SHA
         and packet["frozen_allowed_carrier"]["freeze_commit"]==V2_COMMIT,
         "blind packet permitted carrier authority drift")
    body=packet_path.read_text(encoding="utf-8")
    need(all(banned not in body for banned in BANNED),
         "Original paper labels leaked into blind assessor packet")
    cards=packet["cards"]
    need(len(cards)==16 and len({a["blind_card_id"] for a in cards})==16,
         "missing/duplicate blinded pilot cards")
    paircount=Counter(a["pair_token"] for a in cards)
    need(dict(paircount)==EXPECTED_PAIRS,"eight balanced minimal-pair tokens drift")
    for pair_token in EXPECTED_PAIRS:
        x=[c for c in cards if c["pair_token"]==pair_token]
        need(x[0]["source_kind"]==x[1]["source_kind"]=="other"
             and x[0]["source_arguments"]==x[1]["source_arguments"]
             and x[0]["typed_argument_domain"]==x[1]["typed_argument_domain"]
             and x[0]["statement"]!=x[1]["statement"],
             "not a matched same-argument adversarial contrast: "+pair_token)
    for card in cards:
        args=card["typed_argument_domain"]
        need(len(args)==len(card["source_arguments"])==2 and
             [a["ref"] for a in args]==card["source_arguments"]
             and len(set(card["source_arguments"]))==2,
             "blind card source arg integrity drift")
        need(all(a["layer"] in v2["architecture_layers"]
                 and a["node_role"] in NODE_ROLE_ALLOWED for a in args),
             "card contains unpermitted type or vocabulary")
        need(not any(token in card["statement"] for token in BANNED)
             and len(card["statement"])>50,
             "card too short or source paper term leak")
    need(all(v is False for v in packet["trial_state"].values()),
         "the independent blind assessor has NOT executed this packet")
    return {"status":"PASS","frozen_v2_exact_checkout":True,
            "pilot_cards":16,"matched_contrast_pairs":8,
            "paper_specific_labels_detected":0,
            "independent_assessor_submission_received":False,
            "full_68_source_relations_independently_reconstructed":False,
            "terminal":"F2_BLIND_PILOT_PACKET_INTEGRITY_PASS_ASSESSMENT_NOT_RUN"}

if __name__=="__main__":
    a=check()
    assert check()==a,"blind packet verifier nondeterministic"
    print(json.dumps(a,ensure_ascii=False,sort_keys=True,indent=2))
