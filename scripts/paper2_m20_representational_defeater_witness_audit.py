#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"paper/venues/jgps/main.tex").read_text(encoding="utf-8")
SUPP=(ROOT/"paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
M20=json.loads((ROOT/"research/paper2/p399/main/integration/M20/M20_SPEC_v1.json").read_text(encoding="utf-8"))
BENI=json.loads((ROOT/"research/paper2/p399/main/integration/M20/M20_BENI_SOURCE_PIN_v1.json").read_text(encoding="utf-8"))
POS=json.loads((ROOT/"research/paper2/p399/main/integration/M20/M20_POSITIVE_MINICASE_SOURCE_PIN_v1.json").read_text(encoding="utf-8"))
WIT=json.loads((ROOT/"research/paper2/p399/main/integration/M20/M20_CENTRAL_WITNESS_AUDIT_v1.json").read_text(encoding="utf-8"))
M19=json.loads((ROOT/"research/paper2/p399/main/integration/M19/M19_SPEC_v1.json").read_text(encoding="utf-8"))
M16=json.loads((ROOT/"research/paper2/p399/main/integration/M16/M16_LRN03_SENSITIVITY_RESULT_v1.json").read_text(encoding="utf-8"))
CPCG=json.loads((ROOT/"research/paper2/p399/main/integration/M11/M11_LOSSY_RIVAL_RESULTS_v1.json").read_text(encoding="utf-8"))
BOUNDED=json.loads((ROOT/"research/paper2/bounded_xlike_reconstruction_v1.json").read_text(encoding="utf-8"))

assert M20["exact_parent_head"]=="695041e985cd4e63dfbcc77deb6061132c356af2"
assert M20["terminal_state"]=="M20_REPRESENTATIONAL_DEFEATER_PINNED_CENTRAL_WITNESSES_AUDITABLE"
assert M19["terminal_state"]=="M19_DISCRIMINATION_REQUIREMENT_CONSOLIDATED_CLAIM_TO_CAPACITY_BRIDGE_EXPLICIT"
assert M16["terminal_state"]=="M16_LRN03_CORRECTION_STRUCTURALLY_INVARIANT"
assert M16["headline_results"]["material_change"] is False
assert M16["whole_claim_recalculation"]["matrix_relation_change_count"]==0

# Representational Defeater is a named, restricted corollary.
for phrase in [
    "A useful corollary is a \\emph{Representational Defeater}",
    "\\textbf{Representational Defeater.}",
    "This is not a global skeptical defeater.",
    "live, scientifically motivated alternative",
    "identity-relevant verdict",
]:
    assert phrase in MAIN, phrase

# Beni's strongest published claims are pinned rather than paraphrased vaguely.
assert BENI["status"]=="PUBLISHER_SOURCE_VERIFIED"
assert BENI["doi"]=="10.1007/s10838-025-09759-z"
assert BENI["verified_locations"][0]["publisher_pdf_page"]==8
assert BENI["verified_locations"][1]["publisher_pdf_pages"]==[8,9]
assert BENI["publisher_article_url"]=="https://link.springer.com/article/10.1007/s10838-025-09759-z"
assert BENI["publisher_pdf_url"]=="https://link.springer.com/content/pdf/10.1007/s10838-025-09759-z.pdf"
assert BENI["external_reverification_date"]=="2026-10-07"
for phrase in [
    "objective criterion for kind individuation",
    "publisher PDF p.~8",
    "publisher PDF pp.~8--9",
]:
    assert phrase in MAIN, phrase

# CPCG remains a live scientific alternative, not a privileged ontology.
for phrase in [
    "scientifically intelligible rather than arbitrary string deletion",
    "prima facie reason to ask the coarser question",
    "206 fine-grained reusable objects to 143 coarse signatures",
    "63 of the 99 fine cross-stratum families",
    "Neither result establishes equal adequacy of the rivals.",
]:
    assert phrase in MAIN, phrase
assert CPCG["projection"]["distinct_CPCG_signatures"]==143
assert CPCG["projection"]["original_99_cross_lane_families_collapsed_with_another_original_family"]==63

# Positive mini-case is publisher-pinned as an evidential illustration, not a capacity-identity verdict.
assert POS["status"]=="PUBLISHER_SOURCE_VERIFIED"
assert POS["doi"]=="10.1038/nrn2277"
assert POS["publisher_article_url"]=="https://www.nature.com/articles/nrn2277"
assert POS["external_reverification_date"]=="2026-10-07"
assert len(POS["supported_points"])==2
for phrase in [
    "A limited positive illustration already occurs within the analyzed literature.",
    "differential lesion prediction",
    "semantic-dementia evidence",
    "This does not by itself establish a cross-source capacity identity.",
]:
    assert phrase in MAIN, phrase

# Source records for central witnesses remain reviewed and source-local.
records={}
for name,path in {
    "ATT01":"research/paper2/chatgpt_reference_claimir_v1/ATT01.json",
    "BLF01":"research/paper2/chatgpt_reference_claimir_v1/BLF01.json",
    "ATT03":"research/paper2/chatgpt_reference_claimir_v1/ATT03.json",
    "MEM04":"research/paper2/chatgpt_reference_claimir_v1/MEM04.json",
    "CNC05":"research/paper2/chatgpt_reference_claimir_v1/CNC05.json",
}.items():
    records[name]=json.loads((ROOT/path).read_text(encoding="utf-8"))
    assert records[name]["extraction"]["manual_review_status"]=="reviewed"
    assert len(records[name]["provenance"]["source_spans"])>=3

def fine_overlap(a,b):
    return [
        fam["archetype_id"] for fam in BOUNDED["bounded_xlike_families"]
        if a in fam["member_claim_ids"] and b in fam["member_claim_ids"]
    ]

def coarse_overlap(a,b):
    return [
        g for g in CPCG["all_groups"]
        if a in g["member_claim_ids"] and b in g["member_claim_ids"]
    ]

assert len(fine_overlap("ATT01","BLF01"))>0
assert len(coarse_overlap("ATT01","BLF01"))>0
assert fine_overlap("MEM04","CNC05")==[]
assert coarse_overlap("MEM04","CNC05")==[]
assert fine_overlap("ATT03","MEM04")==[]
assert len(coarse_overlap("ATT03","MEM04"))==1

# Human-facing witness trails expose the relevant source-to-verdict path.
for phrase in [
    "Central witness audit trails",
    "Duncan--Behrens: cross-label bounded reuse",
    "Tulving--Patterson: a shared label without target alignment",
    "Botvinick--Tulving: representation-sensitive overlap",
    "Source locator: Duncan",
    "Source locator: Behrens et al.",
    "Source locator: Tulving",
    "Source locator: Patterson et al.",
    "Source locator: Botvinick et al.",
    "These tables do not constitute independent human recoding",
]:
    assert phrase in SUPP, phrase

# The machine-readable witness map agrees with the recomputation.
assert [c["reader_facing_case"] for c in WIT["cases"]]==[
    "Duncan--Behrens","Tulving--Patterson","Botvinick--Tulving"
]
assert WIT["cases"][0]["fine_overlap_positive"] is True
assert WIT["cases"][1]["fine_overlap_positive"] is False
assert WIT["cases"][1]["cpcg_overlap_positive"] is False
assert WIT["cases"][2]["fine_overlap_positive"] is False
assert WIT["cases"][2]["cpcg_overlap_positive"] is True
assert WIT["cpcg_aggregate"]["bounded_objects"]==206
assert WIT["cpcg_aggregate"]["distinct_signatures"]==143
assert WIT["cpcg_aggregate"]["collapsed_cross_lane_families"]==63

# Large machinery remains subordinate in main; detailed results stay in supplement.
for forbidden in ["40/40","9/10","10/10","nine of ten","mutually compatible in all ten"]:
    assert forbidden not in MAIN, forbidden
assert "Named-model procedural robustness diagnostics" in SUPP
assert "GPT-6 Astra / Medium" in SUPP
assert "GPT-6.1 Sol / Medium" in SUPP

# Reader-facing internal-code boundary.
for name,text in [("main",MAIN),("supplement",SUPP)]:
    assert re.search(r"\bM(?:1[0-9]|[0-9])\b",text) is None, name
    assert "ClaimIR" not in text, name
    assert re.search(r"\bA[012]\b",text) is None, name
    assert re.search(r"\bINT-\d+\b",text) is None, name
    assert re.search(r"\b(?:ATT|BLF|CNC|CTL|LRN|MEM|PRD|SKL|CH)\d{2}\b",text) is None, name
    assert re.search(r"\bfrozen\b",text,re.I) is None, name

assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in MAIN
assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in SUPP
assert "independent coding reliability" in MAIN
assert "population prevalence" in MAIN

print("M20_REPRESENTATIONAL_DEFEATER_WITNESS_AUDIT_GUARDS_PASS")
