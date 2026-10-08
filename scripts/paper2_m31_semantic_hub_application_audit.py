#!/usr/bin/env python3
"""M31 fail-closed source-to-conditional-Q,C application audit.

This checks manuscript provenance and logical scope, not empirical truth of sources.
"""
from __future__ import annotations

import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / "research/paper2/p399/main/integration/M31/M31_SEMANTIC_HUB_APPLICATION_v1.json").read_text(encoding="utf-8"))
m30 = json.loads((root / "research/paper2/p399/main/integration/M30/M30_PROVENANCE_IDENTIFIABILITY_v1.json").read_text(encoding="utf-8"))
main = (root / "paper/venues/jgps/main.tex").read_text(encoding="utf-8")
supp = (root / "paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
bib = (root / "paper/venues/jgps/references.bib").read_text(encoding="utf-8")
index = (root / "paper/venues/jgps/supplementary-materials-index.md").read_text(encoding="utf-8")

assert data["exact_parent_m30_head"] == "566bb67ec85adbb4f0e126d6ae40cc5de2cbf0ea"
assert data["status"] == "IMPLEMENTED_PENDING_EXACT_HEAD_CI"
assert len(data["source_registry"]) == 2
sources = {s["id"]: s for s in data["source_registry"]}
assert set(sources) == {"PATTERSON2007", "GAINOTTI2012"}
assert sources["PATTERSON2007"]["type"] == "review"
assert sources["GAINOTTI2012"]["type"] == "position_paper"
assert sources["PATTERSON2007"]["doi"] == "10.1038/nrn2277"
assert sources["GAINOTTI2012"]["doi"] == "10.1016/j.cortex.2011.06.019"
for source in sources.values():
    assert source["doi"] in bib
    assert source["citation_key"] in bib
    assert source["publisher_url"].startswith("https://")
    assert source["locators"] and source["source_claims"]

c = data["conditional_application"]
assert c["C_is_construction_not_independently_established"] is True
assert c["maps_bear_on_same_Q_C"] is True
assert c["attribution_under_phi_task"] == "UNDERQUALIFIED_FOR_MECHANISTIC_CAPACITY_TYPE_IDENTITY"
assert c["clinical_data_type"] == "reviewed natural neurodegeneration, not randomized experimental lesion"
assert "NOT MEASURED" in c["phi_lesion_result"]
assert "NOT a reported" in c["contrast_source_scientific_question"]

rows = data["source_to_author_bridge"]
assert sum(z["stage"] == "SRC" for z in rows) == 4
assert sum(z["stage"] == "AUTHOR_STIPULATION" for z in rows) == 2
assert sum(z["stage"] == "METHOD_CONDITIONAL" for z in rows) == 1
for z in rows:
    assert (z["source_id"] in sources) == (z["stage"] == "SRC")
for val in data["limits"].values():
    if isinstance(val, bool):
        assert val is True
assert data["limits"]["human_independent_inter_rater_reliability"] == "unmeasured"
assert data["frozen_science"]["whole_claim_pairs"] == "1770/1770 INCOMPARABLE"
assert data["frozen_science"]["bounded_objects"] == 206
assert data["frozen_science"]["cross_stratum_families"] == 99
assert data["frozen_science"]["cpcg_signatures"] == 143
assert data["frozen_science"]["cpcg_cross_family_collisions"] == "63/99"
assert data["frozen_science"]["reverse_projection"] == "21 FULL / 22 PARTIAL / 17 RESIDUAL"
assert data["frozen_science"]["residual_new_top_level_roles"] == "0/17"
assert m30["scientific_authority_unchanged"]["whole_pairs"] == data["frozen_science"]["whole_claim_pairs"]
assert m30["scientific_authority_unchanged"]["bounded_objects"] == data["frozen_science"]["bounded_objects"]

for item in (
    r"Q_{\mathrm{sem}}",
    r"C_{\mathrm{sem}}",
    r"\phi_{\mathrm{task}}",
    r"\phi_{\mathrm{lesion}}",
    r"\citep{Gainotti2012SemanticFormat}",
    "Patterson, Nestor, and Rogers compare",
    "does not predict",
    "not",
    "source",
):
    assert item in main, f"main missing: {item}"
for item in (
    "Source-anchored semantic architecture",
    "Gainotti",
    "not itself a capacity-type comparison",
    "not a randomized lesion intervention",
    "does",
    r"Q_{\mathrm{sem}}",
):
    assert item in supp, f"supplement missing: {item}"
assert "M31_SEMANTIC_HUB_APPLICATION_v1.json" in index
assert "paper2_m31_semantic_hub_application_audit.py" in index
assert "@article{Gainotti2012SemanticFormat," in bib
assert "@article{PattersonNestorRogers2007Semantic" in bib
print("M31_SOURCE_ANCHORED_QC_SCOPE_AUDIT_PASS")
