#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M12 = ROOT / "research/paper2/p399/main/integration/M12"
HV = M12 / "human_validation"
MAIN = ROOT / "paper/venues/jgps/main.tex"
SUPP = ROOT / "paper/venues/jgps/supplement.tex"
MANIFEST = ROOT / "research/paper2/chatgpt_reference_claimir_v1/manifest.json"
M9B = ROOT / "research/paper2/p399/main/integration/M9B/M9B_MAIN40_PAPER_LEVEL_EVIDENCE_v1.json"

def load(p: Path):
    with p.open("r", encoding="utf-8") as fh:
        return json.load(fh)

spec = load(M12 / "M12_DIALECTICAL_CONSOLIDATION_SPEC_v1.json")
pref = load(M12 / "M12_PREFREEZE_RECEIPT_v1.json")
sample = load(M12 / "M12_HUMAN_READJUDICATION_SAMPLE_v1.json")
app = load(M12 / "M12_SEMANTIC_MEMORY_DOWNSTREAM_APPLICATION_v1.json")
tax = load(M12 / "M12_RESULT_EPISTEMIC_CLASSIFICATION_v1.json")
manifest = load(MANIFEST)
m9b = load(M9B)
main = MAIN.read_text(encoding="utf-8")
supp = SUPP.read_text(encoding="utf-8")

# Frozen M12 authority and scientific invariants.
assert spec["status"] == "FROZEN_BEFORE_M12_MANUSCRIPT_REWRITE_AND_HUMAN_PACKET_SELECTION"
assert spec["exact_parent_head"] == "e6b01717129b5f924e489dd8b89d3ee647d252a1"
assert pref["status"] == "PREFREEZE"
assert pref["human_readjudication_result"] == "NOT_PERFORMED"
assert pref["independent_human_readjudication"] == "NOT_PERFORMED"
imm = spec["immutable_scientific_results"]
assert imm["whole_claim"] == "1770/1770 incomparable"
assert imm["bounded_objects"] == 206
assert imm["cross_stratum_families"] == 99
assert imm["reverse_projection"] == "21 full / 22 partial / 17 residual"
assert imm["residual_new_top_level_role"] == "0/17"
assert imm["prospective_MAIN40"] == "A0=40 / A1=0 / A2=0"
assert imm["independent_human_readjudication"] == "NOT_PERFORMED"

# Dialectical targets and semantic-memory downstream boundary.
assert len(spec["dialectical_targets"]) == 3
assert {x["id"] for x in spec["dialectical_targets"]} == {"DT_LABEL","DT_UNIFICATION","DT_INVARIANCE"}
assert app["adjudication"]["label_only_route"] == "EVIDENTIALLY_INSUFFICIENT_FOR_STRUCTURAL_IDENTITY"
assert app["adjudication"]["unified_capacity_thesis"] == "OPEN_NOT_REJECTED"
assert app["frozen_tests"]["bounded_archetype_overlap"] == 0
assert app["frozen_tests"]["CPCG_projected_signature_overlap"] == 0
assert "Semantic memory is not a capacity" in spec["downstream_application"]["prohibited_conclusion"]
assert len(app["preservation_debt_for_unified_capacity_thesis"]) >= 5

# Epistemic classification must explicitly demote design-driven results.
classes = {x["result"]: x["class"] for x in tax["results"]}
assert classes["1770/1770 whole-claim incomparable"] == "REPRESENTATION_DIAGNOSTIC"
assert classes["206 bounded objects / 99 cross-stratum families"] == "SOURCE_GROUNDED_FINDING"
assert classes["MAIN40 A0=40/A1=0/A2=0"] == "SOURCE_GROUNDED_FINDING"
assert classes["encoding-permissive weaker views 40/40 A0"] == "REPRESENTATION_DIAGNOSTIC"
assert classes["direct-preservation weaker views 0/40 A0 and 40/40 A1"] == "REPRESENTATION_DIAGNOSTIC"
assert classes["INT-10 A1 and INT-16 A2 perturbations"] == "CONSTRUCTED_CONTROL"
assert tax["lexical_coding_boundary"]["author_source_coding_concept_blindness"] == "NOT_ESTABLISHED"

# Human validation sample and packet completeness, with NO human results.
assert sample["status"] == "FROZEN_SAMPLE_NO_HUMAN_RESULTS"
assert sample["human_result"] == "NOT_PERFORMED"
assert len(sample["claim_cases"]) == 20
assert len(sample["prospective_cases"]) == 10
assert sum(x["arm"] == "component" for x in sample["prospective_cases"]) == 6
assert sum(x["arm"] == "integrated" for x in sample["prospective_cases"]) == 4

for i in range(1, 21):
    p = HV / "claim_packets" / f"HC{i:02d}.json"
    assert p.exists(), p
    v = load(p)
    mask = v["metadata_masking"]
    assert mask["original_slot_withheld"] is True
    assert mask["doi_withheld"] is True
    assert mask["authors_withheld"] is True
    assert mask["venue_withheld"] is True
    assert mask["construct_labels_withheld"] is True
    assert mask["conceptual_blindness_established"] is False
    assert len(v["candidate_bounded_objects"]) == 2

for i in range(1, 11):
    p = HV / "prospective_packets" / f"HP{i:02d}.json"
    assert p.exists(), p
    v = load(p)
    assert "source_first_artifact" in v
    assert "state_reference" not in v
    assert "architectural_outcome" not in v

claim_form = (HV / "M12_HUMAN_CLAIM_CODER_FORM_v1.csv").read_text(encoding="utf-8")
pro_form = (HV / "M12_HUMAN_PROSPECTIVE_CODER_FORM_v1.csv").read_text(encoding="utf-8")
assert claim_form.count("\n") >= 21
assert pro_form.count("\n") >= 11
readme_upper = (HV / "README.md").read_text(encoding="utf-8").upper().replace("-", "_")
assert ("NOT_PERFORMED" in readme_upper or "NO HUMAN RESULTS" in readme_upper or "NO INDEPENDENT HUMAN RESULT HAS BEEN OBTAINED" in readme_upper)

# No synthetic/completed response or scored-result artifact is permitted in M12 authority.
for p in HV.rglob("*"):
    if p.is_file():
        name = p.name.upper()
        assert "COMPLETED_RESPONSE" not in name
        assert "HUMAN_RESULT" not in name
        assert "AGREEMENT_RESULT" not in name

scorer = (ROOT / "scripts/paper2_m12_score_human_readjudication.py").read_text(encoding="utf-8")
assert "require_complete" in scorer
assert "COMPUTED_FROM_SUPPLIED_COMPLETED_HUMAN_FORMS" in scorer

exporter = (ROOT / "scripts/paper2_m12_export_strict_blind_packet.py").read_text(encoding="utf-8")
assert "normalized_node_roles_withheld" in exporter
assert "normalized_relation_kinds_withheld" in exporter
assert "paper_id_withheld" in exporter
assert "doi_withheld" in exporter
assert "M12_STRICT_BLIND_EXPORT_PASS" in exporter
readme = (HV / "README.md").read_text(encoding="utf-8")
assert "Strict coder export" in readme
assert "paper2_m12_export_strict_blind_packet.py" in readme

M25_PATH=ROOT/"research/paper2/p399/main/integration/M25/M25_SPEC_v1.json"
if M25_PATH.exists():
    M25=load(M25_PATH)
    assert M25["terminal_state"]=="M25_QUESTION_RELATIVE_DEFEATER_AND_PROCESS_WITNESS_CLARIFIED"
    assert "Structural Similarity and Cognitive-Capacity Identity: A Discrimination Requirement" in main
    for phrase in [
        "The Discrimination Requirement",
        "Structural invariance as a live target",
        "target alignment",
        "capacity-relevant bridge warrant",
        "representational discrimination",
        "Secondary procedural robustness diagnostics",
        "The capacity thesis remains open, but the preservation debt is explicit.",
    ]:
        assert phrase in main, phrase
    assert "Independent human re-adjudication was not performed." in main
    assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in main
    print("M12_DIALECTICAL_CONSOLIDATION_GUARDS_PASS_VIA_M25_SUCCESSOR")
    raise SystemExit(0)

# Main manuscript philosophical foreground and validation boundary.
m21 = (ROOT / "research/paper2/p399/main/integration/M21/M21_SPEC_v1.json").exists()
m19 = (ROOT / "research/paper2/p399/main/integration/M19/M19_SPEC_v1.json").exists()
m17 = (ROOT / "research/paper2/p399/main/integration/M17/M17_SPEC_v1.json").exists()
m14 = (ROOT / "research/paper2/p399/main/integration/M14/M14_SPEC_v1.json").exists()
if m21:
    assert "A Discrimination Requirement for Structural Approaches to Cognitive-Capacity Individuation" in main
else:
    assert "When Does Structural Comparison Support Cognitive-Capacity Individuation?" in main
if m19:
    for phrase in [
        "The Discrimination Requirement",
        "Structural invariance as a live target",
        "target alignment",
        "capacity-relevant bridge warrant",
        "representational discrimination",
        "Secondary procedural robustness diagnostics",
        "The capacity thesis remains open, but the preservation debt is explicit.",
    ]:
        assert phrase in main, phrase
elif m17:
    for phrase in [
        "From reconstruction success to licensed identity inference",
        "The argument can be stated directly",
        "Structural invariance as a live target",
        "Beni's structural-realist proposal",
        "North's defense of objective or non-pragmatic perspicuity",
        "The present claim adds a non-circularity constraint",
        "The capacity thesis remains open, but the preservation debt is explicit.",
        "Validation diagnostics: separating claim selection from decomposition",
    ]:
        assert phrase in main, phrase
else:
    assert "terminological carryover inference" in main
    assert "reconstruction-to-identity inference" in main
    assert "local-invariance promotion" in main
    assert "The capacity thesis remains open, but it now carries explicit preservation debt." in main
    assert "objective or non-pragmatic perspicuity" in main
    if m14:
        assert "Successful direct reconstruction therefore does not select the exact role inventory." in main
        assert "representation diagnostic" in main

assert "Independent human re-adjudication was not performed." in main
assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in main
assert "Paper 2" not in main
assert "construct-label-neutral" not in main.lower()
assert "\\paragraph{" not in main

abstract = main.split("\\begin{abstract}",1)[1].split("\\end{abstract}",1)[0]
for forbidden in ["1,770","206","99 cross","143","63 of 99","62 cross","58/60","0/40"]:
    assert forbidden not in abstract, forbidden
if m19:
    assert "Discrimination Requirement" in abstract and "Beni" in abstract
elif m17:
    assert "Beni" in abstract and "representation-sensitivity" in abstract
else:
    assert "60-claim" in abstract
    assert "40-paper" in abstract

assert len(manifest["entries"]) == 60
assert len(m9b["rows"]) == 40
if m17:
    source_map = json.loads((ROOT / "paper/venues/jgps/reader-facing-source-map.json").read_text(encoding="utf-8"))
    assert len(source_map["original_60"]) == 60
    assert len(source_map["prospective_40"]) == 40
    for e in manifest["entries"]:
        assert e["stable_identity"].replace("DOI:","") in supp
    for r in m9b["rows"]:
        assert r["doi"] in supp
    for phrase in [
        "Independent human-coding boundary",
        "Prospective representation baselines",
        ("Named-model procedural robustness diagnostics" if m19 else "Named-model reconstruction validation"),
        "Procedural auditability is established; inter-rater reliability remains unmeasured.",
    ]:
        assert phrase in supp, phrase
    assert "paper2_m12_export_strict_blind_packet.py" not in supp
else:
    for e in manifest["entries"]:
        doi = e["stable_identity"].replace("DOI:","")
        assert e["slot_id"] in supp and doi in supp
    for r in m9b["rows"]:
        assert r["paper_id"] in supp
        assert r["doi"] in supp
        assert r["evidence"]["source_loci_artifact_path"] in supp
    for c in sample["claim_cases"]:
        assert c["case_id"] in supp and c["original_claim_id"] in supp and c["doi"] in supp
    for c in sample["prospective_cases"]:
        assert c["case_id"] in supp and c["original_paper_id"] in supp and c["doi"] in supp
    for required in [
        "a083dbc27e5a11d4e58363ccfed83c37c6a3a7b8",
        "218867d0d49613fc5559c7472f55c08777c9e936",
        "f7f771b7e129da6bdaf448000b78fc4806821531",
        "103272ef179e83f468ee7ecbbef1ce7f527aa745",
        "5f57bc410e6ed3046284af6ab1114956f35ebf34",
        "5dd13a26cfbe7c00dc9918a45194c0fe3e950525",
        "a212820d225050bbc10d395685e74cd2fb0d9912",
        "b31f670f31d2f015b65d8bbf2e4fb12178b46694",
        "1c22fcb177c434d2900ffb3af9ef6baee2af73ff",
    ]:
        assert required in supp
    assert "paper2_m12_export_strict_blind_packet.py" in supp

assert "\\paragraph{" not in supp

print("M12_DIALECTICAL_CONSOLIDATION_GUARDS_PASS")
