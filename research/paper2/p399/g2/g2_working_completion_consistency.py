#!/usr/bin/env python3
"""G2 non-scientific fail-closed ledger/integrity checks. No MAIN source reconstruction."""
import copy, hashlib, json
from pathlib import Path
P=Path("research/paper2/p399/g2")
side=(P/"MAIN40_G2_V2_INDEPENDENT_RAW_UTF8_SHA256SUMS_20261004.txt").read_text().splitlines()
assert len(side)==5
for line in side:
    checksum, filename=line.split("  ",1)
    assert hashlib.sha256((P/filename).read_bytes()).hexdigest()==checksum,(filename,"SHA_MISMATCH")
m=json.loads((P/"MAIN40_G2_ADMISSION_WORKING_MANIFEST_v2.json").read_text())
s=json.loads((P/"MAIN40_G2_ACTUAL_SOURCE_RECEIPTS_AND_DECISIONS_v2.json").read_text())
v=json.loads((P/"MAIN40_G2_780_MAIN_AND_800_G1_FAMILY_RECONCILIATION_v2.json").read_text())
b=json.loads((P/"MAIN40_G2_OBJECTIVE_REPLACEMENT_EVENT_LOG_v2.json").read_text())
g=json.loads((P/"MAIN40_G2_G3_ROSTER_SPECIFIC_HANDOFF_UNSEALED_v2.json").read_text())
orig=json.loads((P/"MAIN40_G2_SOURCE_ADMISSION_WORKING_v1.json").read_text())
def check(q,ss,mm,bb,gg):
    a=q["selected_working_roster"];doi=[x["doi"].lower() for x in a]
    assert len(a)==40 and len(set(doi))==40
    assert [x["slot"] for x in a]==[x["slot_id"] for x in orig["entries"]]
    assert [x["doi"] for x in a]==[x["stable_identity"]["value"] for x in orig["entries"]]
    assert sum(x["slot"].startswith("INT-") for x in a)==16
    for t in ("ATT","BLF","CNC","CTL","LRN","MEM","PRD","SKL"):
        assert sum(x["slot"].startswith(t+"-") for x in a)==3
    assert len(ss["records"])==40 and sum(x["cloud_provenance"]["pdf_byte_acquired"] for x in ss["records"])==29
    assert sum(x["cloud_provenance"]["publisher_html_request_returned_match"] for x in ss["records"])==23
    assert len(mm["main_main_pairs"])==780 and len(mm["main_vs_g1_pairs"])==800
    assert all(not x["may_be_counted_independent"] for x in mm["main_main_pairs"])
    assert all(x["central_family_decision"]!="ADMITTED" for x in mm["main_vs_g1_pairs"])
    assert not any(x["exact_doi_same"] for x in mm["main_main_pairs"]+mm["main_vs_g1_pairs"])
    assert bb["replacement_activation_count"]==0 and not any(x["backup_activation_state"]!="NOT_ACTIVATED_PROSPECTIVE_ONLY" for x in a)
    assert len(gg["per_work"])==40 and not any(x["independent_reference_assessor_completed"] or x["analyst_masked_packet_ready"] for x in gg["per_work"])
    assert q["count"]["original_source_complete_version_model_variants_admitted"]==0
    assert q["count"]["central_family_admitted"]==0
    assert q["count"]["final_joint_frozen"]==0
    assert not q["main_authorized"] and all(not x["source_eligible"] for x in a)
check(m,s,v,b,g)
print("PASS: REAL WORKING V2 digest sidecar 5/5")
print("PASS: 40/40 identity, eight lanes x three plus sixteen integration")
print("PASS: 29/40 PDF original physical acquisition and 23/40 HTML original publication responses")
print("PASS: 780 MAIN pairs and 800 provisional G1 pairs, exact DOI overlap zero, no false central family approval")
print("PASS: zero unapproved substitute activation, no G3 masked/reference packet claims, zero scientific admits")
def negtest(f):
    try:f()
    except AssertionError:return True
    return False
def mutate(fn):
    mm,ss,cc,bb,gg=map(copy.deepcopy,(m,s,v,b,g))
    fn(mm,ss,cc,bb,gg)
    check(mm,ss,cc,bb,gg)
assert negtest(lambda:mutate(lambda mm,*_:mm["selected_working_roster"].pop()))
assert negtest(lambda:mutate(lambda mm,*_:mm["selected_working_roster"][1].update(doi=mm["selected_working_roster"][0]["doi"])))
assert negtest(lambda:mutate(lambda mm,*_:mm["count"].update(central_family_admitted=40)))
assert negtest(lambda:mutate(lambda _,__,cc,*___:cc["main_main_pairs"][0].update(may_be_counted_independent=True)))
assert negtest(lambda:mutate(lambda _,__,___,bb,*_:bb.update(replacement_activation_count=1)))
assert negtest(lambda:mutate(lambda *args:args[4]["per_work"][0].update(analyst_masked_packet_ready=True)))
print("PASS: six negative controls refuse denominator loss, DOI duplicate, false lineage, false independent pair, unadmitted backup, forged G3 packet")
print("RESULT: METADATA_CONSISTENCY_ONLY_NO_SEMANTIC_SOURCE_ELIGIBILITY_NO_MAIN_GO")
