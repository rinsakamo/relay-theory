#!/usr/bin/env python3
"""Validate PVS-16 assistant source audit and human author-review packet."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path("paper/validation/jgps-major-revision")
CAND=ROOT/"pvs16-claimir-candidates-v1"
AUDIT=ROOT/"pvs16-source-consistency-audit-v1.json"
PACKET=ROOT/"pvs16-author-review-packet-v1.json"
ADMISSION_SHA="0a4454887189730cf4b13d12061f4cab93fb8e4d8f0ec089a08f77bc088dc123"
class Error(ValueError): pass
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    audit,packet=load(AUDIT),load(PACKET)
    if audit["admission_manifest_sha256"] != ADMISSION_SHA or packet["admission_manifest_sha256"] != ADMISSION_SHA: raise Error("admission authority drift")
    if audit["status"] != "ASSISTANT_SOURCE_CONSISTENCY_AUDIT_PASS_PENDING_HUMAN_REVIEW": raise Error("assistant audit status drift")
    if packet["status"] != "FROZEN_PENDING_HUMAN_AUTHOR_REVIEW": raise Error("author packet status drift")
    if packet["grammar_mapping_authorized"] is not False: raise Error("Grammar mapping prematurely authorized")
    if packet["review_completion_must_be_human_authored"] is not True: raise Error("human review requirement removed")
    a={x["validation_claim_id"]:x for x in audit["entries"]}
    p={x["validation_claim_id"]:x for x in packet["entries"]}
    if len(a)!=16 or set(a)!=set(p): raise Error("packet membership mismatch")
    for vid in sorted(a):
        ar,pr=a[vid],p[vid]
        path=CAND/pr["candidate_file"]
        if not path.exists(): raise Error(f"{vid}: missing candidate")
        digest=sha(path)
        if digest != ar["claimir_sha256"] or digest != pr["claimir_sha256"]: raise Error(f"{vid}: candidate hash drift")
        obj=load(path)
        if obj["extraction"]["manual_review_status"] != "unreviewed": raise Error(f"{vid}: candidate review state changed before human review transaction")
        if ar["source_consistency"] != "PASS" or ar["human_review_still_required"] is not True: raise Error(f"{vid}: audit semantics drift")
        if ar["grammar_mapping_inspected"] is not False: raise Error(f"{vid}: assistant audit claims Grammar inspection")
        for k in ("human_review_decision","reviewer_name_or_initials","review_date","revision_note"):
            if pr[k] is not None: raise Error(f"{vid}: human field must remain null in frozen pending packet: {k}")
    print("PVS16_SOURCE_AUDIT_AND_AUTHOR_REVIEW_PACKET_GATE_PASS")
    print("GRAMMAR_MAPPING_AUTHORIZED=false")
    print("HUMAN_AUTHOR_REVIEW_PENDING=true")
if __name__=="__main__": main()
