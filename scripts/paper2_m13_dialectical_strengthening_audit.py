#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
M13=ROOT/"research/paper2/p399/main/integration/M13"
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))

spec=load(M13/"M13_SPEC_v1.json")
pref=load(M13/"M13_PREFREEZE_RECEIPT_v1.json")
pcs=load(M13/"M13_COMPARATOR_POSITIVE_CONTROL_SPEC_v1.json")
pcr=load(M13/"M13_COMPARATOR_POSITIVE_CONTROL_RESULTS_v1.json")
cap=load(M13/"M13_CAPACITY_LEVEL_CASES_v1.json")
att=load(M13/"M13_ATT01_BLF01_APPLICATION_v1.json")
rep=load(M13/"M13_REPRESENTATION_SENSITIVE_CASE_v1.json")
hvp=load(M13/"M13_HUMAN_SOURCE_EXTRACTION_PROTOCOL_v1.json")
hvs=load(M13/"M13_HUMAN_SOURCE_EXTRACTION_SAMPLE_v1.json")
global_a=load(ROOT/"research/paper2/global_archetype_reconstruction_v1.json")
cpcg=load(ROOT/"research/paper2/p399/main/integration/M11/M11_LOSSY_RIVAL_RESULTS_v1.json")
manifest=load(ROOT/"research/paper2/chatgpt_reference_claimir_v1/manifest.json")
main=(ROOT/"paper/venues/jgps/main.tex").read_text(encoding="utf-8")
supp=(ROOT/"paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
bib=(ROOT/"paper/venues/jgps/references.bib").read_text(encoding="utf-8")
beni=(M13/"M13_BENI_DIALECTICAL_RECONSTRUCTION_v1.md").read_text(encoding="utf-8")

PARENT="cbf9240b7188776748af07f847b3002af55aefe7"
assert spec["authority"]["exact_parent_head"]==PARENT
assert pref["exact_parent_head"]==PARENT and pref["status"]=="PREFREEZE"
imm=spec["immutable_scientific_results"]
assert imm["whole_claim"]=="1770/1770 INCOMPARABLE"
assert imm["bounded_objects"]==206 and imm["cross_stratum_families"]==99
assert imm["reverse_projection"]=="21 FULL / 22 PARTIAL / 17 RESIDUAL"
assert imm["residual_new_top_level_role"]=="0/17"
assert imm["prospective_MAIN40"]=="40/40 A0"
assert imm["encoding_permissive_six_weak_representations"]=="40/40 A0 each"
assert imm["direct_preservation_six_weak_representations"]=="0/40 A0 / 40/40 A1 each"
assert imm["global_genealogical_independence"]=="NOT_CLAIMED"
assert imm["independent_human_validation"]=="NOT_PERFORMED"

assert "kind individuation" in beni
assert "does not argue against PP/FEP" in beni
assert "not claimed to be final or uniquely correct" in beni
assert "mechanistic" in beni and "perspicuity" in beni

cases={x["id"]:x for x in cap["cases"]}
assert cases["MEM04xCNC05"]["fine_bounded_overlap"]==0 and cases["MEM04xCNC05"]["cpcg_overlap"]==0
assert cases["ATT01xBLF01"]["shared_bounded_object"]=="A-3b814de4da04"
assert cases["ATT03xMEM04"]["fine_working_basis_bounded_overlap"]==0
assert cases["ATT03xMEM04"]["cpcg_projected_overlap"]==1
assert att["whole_claim_comparison"]=="INCOMPARABLE"
assert att["bounded_reconstruction"]["object"]=="A-3b814de4da04"

support={}
for a in global_a["global_archetype_objects"]:
    for ids in a.get("derived_support_claim_ids_by_lane",{}).values():
        for cid in ids: support.setdefault(cid,set()).add(a["global_archetype_id"])
assert support["ATT03"].isdisjoint(support["MEM04"])
assert "A-53b16535e1c2" in support["ATT03"]
assert "A-af97ed649c6f" in support["MEM04"]
groups=[g for g in cpcg["all_groups"] if {"A-53b16535e1c2","A-af97ed649c6f"} <= set(g["original_archetype_ids"])]
assert len(groups)==1
g=groups[0]
assert "ATT03" in g["member_claim_ids"] and "MEM04" in g["member_claim_ids"]
assert rep["CPCG"]["signature"]==g["signature"]

assert pcs["epistemic_class"]=="CONSTRUCTED_CONTROL"
assert [r["observed"] for r in pcr["results"]]==["EQUIVALENT","EQUIVALENT","RIGHT_STRICT_REFINEMENT_OF_LEFT"]
assert pcr["corpus_effect"]=="NONE"

assert hvp["status"]=="PROTOCOL_FROZEN_HUMAN_EXTRACTION_NOT_PERFORMED"
assert hvp["result"]=="NOT_PERFORMED"
assert len(hvs["rows"])==10
salt=hvs["salt"]
entries={e["slot_id"]:e for e in manifest["entries"]}
expected=[]
for lane in ["ATT","BLF","CNC","CTL","LRN","MEM","PRD","SKL"]:
    ids=[f"{lane}{i:02d}" for i in range(1,7)]
    expected.append(min(ids,key=lambda x:hashlib.sha256(f"{PARENT}|{salt}|{x}".encode()).hexdigest()))
ch=[f"CH{i:02d}" for i in range(1,13)]
expected += sorted(ch,key=lambda x:hashlib.sha256(f"{PARENT}|{salt}|{x}".encode()).hexdigest())[:2]
assert [r["slot_id"] for r in hvs["rows"]]==expected
for r in hvs["rows"]:
    assert r["human_record_status"]=="NOT_PERFORMED"
    assert entries[r["slot_id"]]["stable_identity"]=="DOI:"+r["doi"]
    assert r["sha256_rank"]==hashlib.sha256(f"{PARENT}|{salt}|{r['slot_id']}".encode()).hexdigest()

m17 = (ROOT / "research/paper2/p399/main/integration/M17/M17_SPEC_v1.json").exists()
m14 = (ROOT / "research/paper2/p399/main/integration/M14/M14_SPEC_v1.json").exists()
if m17:
    strong = (
        "An inference from structural comparison to cognitive-capacity identity is "
        "epistemically licensed only if the comparison representation, preservation "
        "criterion, and granularity are specified and warranted for that inferential use."
    )
    assert strong in main
    for phrase in [
        "From reconstruction success to licensed identity inference",
        "Structural invariance as a live target",
        "Beni's structural-realist proposal",
        "This is not an attribution of a simple fallacy to Beni",
        "North's defense of objective or non-pragmatic perspicuity",
        "The present claim adds a non-circularity constraint",
        "Capacity-level consequences",
        "Botvinick et al.--Tulving comparison",
        "Worked example: from source evidence to a capacity constraint",
        "Procedural auditability is established; inter-rater reliability remains unmeasured.",
    ]:
        assert phrase in main, phrase
elif m14:
    strong = (
        "An inference from structural comparison to cognitive-capacity identity is "
        "epistemically licensed only if the comparison representation, preservation "
        "criterion, and granularity are specified and warranted for that inferential use."
    )
    assert strong in main
    for phrase in [
        "From specification to licensed identity inference",
        "A live dialectical target: which invariance can individuate?",
        "terminological carryover inference",
        "reconstruction-to-identity inference",
        "local-invariance promotion",
        "Beni's structural-realist proposal",
        "Wajnerman-Paz and Rojas-L",
        "Capacity-level adjudication",
        "ATT03--MEM04",
        "End-to-end worked example",
        "Procedural auditability is established; inter-rater reliability remains unmeasured.",
    ]:
        assert phrase in main, phrase
else:
    assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in main

assert "zero valid structured claim record records" not in main
assert "the present study consequently claims" not in main
assert "Independent human re-adjudication was not performed." in main

if m17:
    source_map=json.loads((ROOT/"paper/venues/jgps/reader-facing-source-map.json").read_text(encoding="utf-8"))
    assert len(source_map["original_60"])==60
    assert "Capacity-level witness cases" in supp
    assert "Independent human-coding boundary" in supp
    assert "inter-rater reliability remains unmeasured" in supp
else:
    for slot in ["ATT03","BLF04","CNC01","CTL01","LRN03","MEM02","PRD05","SKL06","CH03","CH12"]:
        assert slot in supp
    assert "Comparator positive controls and capacity-level cases" in supp
    assert "Independent 10-source extraction protocol" in supp

assert "Krickel2024CognitiveOntology" in bib and "Kohar2025ScalingUp" in bib

print("M13_DIALECTICAL_STRENGTHENING_GUARDS_PASS")
