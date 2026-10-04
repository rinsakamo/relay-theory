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
assert negtest(lambda:mutate(lambda aa,bbx,ccx,backup,*extras:backup.update(replacement_activation_count=1)))
assert negtest(lambda:mutate(lambda *args:args[4]["per_work"][0].update(analyst_masked_packet_ready=True)))
print("PASS: six negative controls refuse denominator loss, DOI duplicate, false lineage, false independent pair, unadmitted backup, forged G3 packet")
print("RESULT: METADATA_CONSISTENCY_ONLY_NO_SEMANTIC_SOURCE_ELIGIBILITY_NO_MAIN_GO")


# Versioned, immutable v3 addendum checks; do NOT modify historical v1/v2 artifacts.
checklist=(P/"MAIN40_G2_V3_RAW_UTF8_SHA256SUMS.txt").read_text().splitlines()
assert len(checklist)==3
for ln in checklist:
    digest,filename=ln.split("  ",1)
    assert hashlib.sha256((P/filename).read_bytes()).hexdigest()==digest,("v3-digest",filename)
n=json.loads((P/"MAIN40_G2_ADMISSION_WORKING_MANIFEST_v3.json").read_text())
r3=json.loads((P/"MAIN40_G2_EIGHT_FIRST_PARTY_RETRY_APPEND_ONLY_v3.json").read_text())
g13=json.loads((P/"MAIN40_G2_G1_CURRENT_BOUNDED_P07_RECONCILIATION_v3.json").read_text())
def check_v3(vv,ee,gg):
    old=m["selected_working_roster"];new=vv["selected_working_roster"]
    assert len(new)==len(old)==40
    assert [(x["slot"],x["doi"]) for x in new]==[(x["slot"],x["doi"]) for x in old]
    assert len(ee["results"])==8 and sum(bool(x["actual_primary_received"]) for x in ee["results"])==1
    result=[x for x in ee["results"] if x["actual_primary_received"]]
    assert len(result)==1 and result[0]["id"]=="INT-02"
    pdf=result[0]["official_publisher_raw_pdf"]
    assert pdf["sha256"]=="a1e644c826bf1b356187bc556d5947eb23638f3f9bc6c61835d46850b4f1cc37"
    assert pdf["bytes"]==2814783 and pdf["pages"]==14 and pdf["original_doi_exact_found_in_pdf"]
    working=[x for x in new if x["slot"]=="INT-02"][0]
    assert working["cloud_publisher_pdf_acquired"] and working["cloud_pdf_sha256"]==pdf["sha256"]
    assert sum(bool(x["cloud_publisher_pdf_acquired"]) for x in new)==30
    assert vv["count"]["actual_original_primary_media_access_distinct"]==33
    assert vv["count"]["full_original_access_outstanding"]==7
    assert vv["count"]["source_visually_semantically_admitted"]==0
    assert vv["count"]["central_family_admitted"]==0 and vv["count"]["final_joint_frozen"]==0
    assert vv["final_scientific_freeze_sha256"] is None and not vv["main_authorized"]
    assert all(not x["source_eligible"] for x in new)
    assert gg["p07_qualified_source_scoped"] and not gg["final20_scientific_roster_is_frozen"]
    assert not gg["g2_frozen_selected_exact_doi_collision_with_p07"]
check_v3(n,r3,g13)
print("PASS V3: 3/3 independently raw hashed supplementary working artifacts")
print("PASS V3: one truly new original publisher PDF; 30/40 raw original and 33/40 distinct first-party access")
print("PASS V3: unchanged 40 DOI allocation, 7 access failures, 0 scientific pass, no final freeze")
def neg_v3(f):
    n2,e2,g2=map(copy.deepcopy,(n,r3,g13))
    f(n2,e2,g2)
    try:check_v3(n2,e2,g2)
    except AssertionError:return True
    return False
assert neg_v3(lambda a,b,c:a["selected_working_roster"][0].update(doi="10.0000/forged"))
assert neg_v3(lambda a,b,c:a["count"].update(source_visually_semantically_admitted=30))
assert neg_v3(lambda a,b,c:a["count"].update(full_original_access_outstanding=0))
assert neg_v3(lambda a,b,c:a.update(main_authorized=True))
print("PASS V3: four additional false-promotion/collision/availability/MAIN-GO negative tests rejected")


# Addendum v4: independent raw UTF8 evidence; downloaded PDF bytes versus
# browser-only official publisher PDF must NEVER be collapsed into a fake SHA.
d4=(P/"MAIN40_G2_V4_RAW_UTF8_SHA256SUMS_20261004.txt").read_text().splitlines()
assert len(d4)==4
for ln in d4:
    digest, filename=ln.split("  ",1)
    assert hashlib.sha256((P/filename).read_bytes()).hexdigest()==digest,("v4-raw-evidence-tamper",filename)
v4=json.loads((P/"MAIN40_G2_ADMISSION_WORKING_MANIFEST_v4.json").read_text())
r4=json.loads((P/"MAIN40_G2_NATURE_PUBLISHER_BROWSER_AND_SECOND_OFFICIAL_RETRY_v4.json").read_text())
e4=json.loads((P/"MAIN40_G2_OBJECTIVE_EVENT_DELTA_v4.json").read_text())
def check_v4(ww,rr,ee):
    previous=n["selected_working_roster"];latest=ww["selected_working_roster"]
    assert len(latest)==40
    assert [(z["slot"],z["doi"]) for z in latest]==[(z["slot"],z["doi"]) for z in previous]
    assert len(rr["new_actual_official_browser_media"])==2
    assert {z["slot"] for z in rr["new_actual_official_browser_media"]}=={"CNC-01","INT-04"}
    assert {z["original_PDF_pages_tool_rendered"] for z in rr["new_actual_official_browser_media"]}=={15,20}
    assert all(z["original_pdf_browser_opened"] and
               z["identity_on_original_page0"]["doi_exact"] and
               z["cloud_actual_raw_pdf_bytes_sha256"] is None and
               not z["full_page_by_page_visual_inspection"] and
               not z["source_eligible"] for z in rr["new_actual_official_browser_media"])
    assert sum(bool(z["cloud_publisher_pdf_acquired"]) for z in latest)==30
    for sid in ("CNC-01","INT-04"):
        paper=[x for x in latest if x["slot"]==sid][0]
        assert paper["publisher_owned_complete_original_pdf_opened_in_browser"]
        assert not paper["original_full_publisher_pdf_raw_sha256_acquired"]
        assert not paper["all_model_critical_math_figures_variants_negatives_verified"]
    assert rr["counts"]["remaining_no_complete_original_first_party_media"]==5
    assert set(rr["counts"]["remaining_slots"])=={"LRN-01","PRD-01","ATT-03","BLF-01","INT-01"}
    assert ww["count"]["full_original_access_outstanding"]==5
    assert ww["count"]["actual_original_primary_media_access_distinct"]==35
    assert ww["count"]["current_publisher_pdf_byte_receipts"]==30
    assert ww["count"]["new_browser_first_party_pdf_opened_verified"]==2
    prd=[z for z in rr["official_browser_primary_no_full_original"] if z["slot"]=="PRD-01"][0]
    assert prd["corrected_p_trident"]==.69 and prd["corrected_p_planet"]==.31
    assert not prd["corrected_original_full_text_actual_retrieved"]
    assert len(rr["second_official_elsevier_retry"])==3
    assert all(z["no_first_party_complete_original"] for z in rr["second_official_elsevier_retry"])
    assert rr["counts"]["fully_scientifically_edition_variant_source_admitted"]==0
    assert rr["counts"]["central_model_family_independence_admitted"]==0
    assert ww["count"]["scientific_source_admitted"]==0
    assert ww["count"]["central_family_admitted"]==0 and ww["count"]["final_joint_frozen"]==0
    assert ww["g1_latest_observed_snapshot"]["source_scoped_qualified"]==6
    assert not ww["g1_latest_observed_snapshot"]["official_final_pilot20_roster_issued"]
    assert not any(z["source_eligible"] or z["central_family_independent_certified"] or
                   z["g3_actual_masked_packet_created"] for z in latest)
    assert ee["backups_activated"]==0 and len(ee["events"])==3
    assert not ww["main_authorized"] and not rr["main_authorized"]
    assert ww["final_scientific_freeze_sha256"] is None
check_v4(v4,r4,e4)
print("PASS V4: 4/4 independently raw-hashed immutable new evidence docs")
print("PASS V4: source identity 40 unchanged, raw original PDF 30 distinct; new 2 browser-only originals")
print("PASS V4: 35 actual original first-party access, 5 still blocked, 0 fully scientific qualified")
print("PASS V4: PRD corrected 0.69/0.31 figure labels NOT substitute for subscription original")
def neg_v4(f):
    a,b,c=map(copy.deepcopy,(v4,r4,e4))
    f(a,b,c)
    try:check_v4(a,b,c)
    except AssertionError:return True
    return False
assert neg_v4(lambda a,b,c:a["selected_working_roster"][0].update(doi="10.0000/fake"))
assert neg_v4(lambda a,b,c:a["count"].update(current_publisher_pdf_byte_receipts=32))
assert neg_v4(lambda a,b,c:a["count"].update(scientific_source_admitted=35))
assert neg_v4(lambda a,b,c:a.update(main_authorized=True))
assert neg_v4(lambda a,b,c:b["official_browser_primary_no_full_original"][1].update(corrected_original_full_text_actual_retrieved=True))
print("PASS V4: five adversarial false-roster / unowned SHA / false-science / GO / paid-preview tests rejected")


# V5: independent publisher original first-party Chromium reacquisition is raw-byte
# evidence, NOT automatically scientific semantic/figure/variant/lineage qualification.
d5=(P/"MAIN40_G2_V5_RAW_UTF8_SHA256SUMS_20261004.txt").read_text().splitlines()
assert len(d5)==4
for ln in d5:
    digest,name=ln.split("  ",1)
    assert hashlib.sha256((P/name).read_bytes()).hexdigest()==digest,("tampered-v5",name)
v5=json.loads((P/"MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json").read_text())
r5=json.loads((P/"MAIN40_G2_LRN01_FIRST_PARTY_DUAL_PHYSICAL_ACQUISITION_v5.json").read_text())
e5=json.loads((P/"MAIN40_G2_OBJECTIVE_EVENT_DELTA_v5.json").read_text())
def check_v5(ww,rr,ee):
    old=v4["selected_working_roster"];new=ww["selected_working_roster"]
    assert len(new)==40 and [(x["slot"],x["doi"]) for x in new]==[(x["slot"],x["doi"]) for x in old]
    assert sum(bool(x["cloud_publisher_pdf_acquired"]) for x in new)==31
    paper=next(x for x in new if x["slot"]=="LRN-01")
    original=rr["first_actual"]
    sha="638c40d95b03e9ed076949c1c17f469bed4e1c3c9959ca8a84dc65c8a0744718"
    assert paper["cloud_pdf_sha256"]==sha and original["actual_original_pdf_sha256"]==sha
    assert rr["second_actual"]["actual_original_pdf_sha256"]==sha
    assert rr["third_formally_successful_reacquisition"]["actual_sha256"]==sha
    assert rr["second_actual"]["job_status"].startswith("FAIL_DUE_TO_OVERSTRICT_")
    assert rr["third_formally_successful_reacquisition"]["formal_fixed_workflow_pass"]
    assert paper["cloud_pdf_bytes"]==59865461 and paper["cloud_pdf_pages"]==20
    assert paper["publisher_original_full_html_acquired"]
    assert paper["publisher_original_full_html_sha256"]==original["official_html_actual_response_raw_sha256"]
    assert rr["second_actual"]["official_html_second_response_sha256"]!=original["official_html_actual_response_raw_sha256"]
    assert ww["count"]["current_publisher_pdf_byte_receipts"]==31
    assert ww["count"]["actual_original_primary_media_access_distinct"]==36
    assert ww["count"]["full_original_access_outstanding"]==4
    assert set(ww["objective_first_party_media_blockers_remaining"])=={"PRD-01","ATT-03","BLF-01","INT-01"}
    assert all(not x["source_eligible"] and not x["central_family_independent_certified"] and
               not x["g3_actual_masked_packet_created"] for x in new)
    assert ww["count"]["source_visually_semantically_admitted"]==0
    assert ww["count"]["central_family_admitted"]==0 and ww["count"]["final_joint_frozen"]==0
    assert not ww["g1_latest_observed_snapshot"]["official_final_pilot20_roster_issued"]
    assert ww["g1_latest_observed_snapshot"]["source_scoped_qualified"]==7
    assert len(ee["events"])==5 and ee["count_new_actual_backup_activations"]==0
    assert not ww["main_authorized"] and not ee["main_authorized"]
    assert ww["final_scientific_freeze_sha256"] is None
check_v5(v5,r5,e5)
print("PASS V5: 4/4 independent raw GitHub UTF8 SHA and unchanged v4 40 identity")
print("PASS V5: 31/40 actual publisher raw PDF, 36/40 distinct primary media, four blockers")
print("PASS V5: 3x independent physical 20page 59MB original LRN01 PDF equal SHA256, corrected strict CI")
print("PASS V5: genuine first FAILED overstrict PDF title CI preserved, fixed PASS separate")
print("PASS V5: 0 science/lineage admits, 0 unauthorized replacements, 0 G3 packets, MAIN no-go")
def negative_v5(f):
    a,b,c=map(copy.deepcopy,(v5,r5,e5))
    f(a,b,c)
    try:check_v5(a,b,c)
    except AssertionError:return True
    return False
assert negative_v5(lambda a,b,c:a["selected_working_roster"][0].update(doi="10.0000/outcome-corrupt"))
assert negative_v5(lambda a,b,c:a["count"].update(current_publisher_pdf_byte_receipts=40))
assert negative_v5(lambda a,b,c:a["count"].update(source_visually_semantically_admitted=31))
assert negative_v5(lambda a,b,c:a.update(main_authorized=True))
assert negative_v5(lambda a,b,c:b["third_formally_successful_reacquisition"].update(actual_sha256="0"*64))
assert negative_v5(lambda a,b,c:c.update(count_new_actual_backup_activations=1))
print("PASS V5: six adversarial false identity, false raw provenance, false-science, false-GO, SHA tamper, unauthorized replacement rejected")
