#!/usr/bin/env python3
"""M32 fail-closed philosophical warrant-promotion & provenance audit."""
from __future__ import annotations
import json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=json.loads((ROOT/"research/paper2/p399/main/integration/M32/M32_EVIDENTIAL_PROMOTION_AUDIT_v1.json").read_text(encoding="utf-8"))
main=(ROOT/"paper/venues/jgps/main.tex").read_text(encoding="utf-8")
supp=(ROOT/"paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
index=(ROOT/"paper/venues/jgps/supplementary-materials-index.md").read_text(encoding="utf-8")
bib=(ROOT/"paper/venues/jgps/references.bib").read_text(encoding="utf-8")
m29=json.loads((ROOT/"research/paper2/p399/main/integration/M29/M29_FINITE_PAIR_LAW_v1.json").read_text(encoding="utf-8"))
m31=json.loads((ROOT/"research/paper2/p399/main/integration/M31/M31_SEMANTIC_HUB_APPLICATION_v1.json").read_text(encoding="utf-8"))

assert spec["exact_parent_m31_head"]=="4e1b5141baf64ba7283011aca0681e5c730e0f74"
p=spec["promotion_failure"]
n=p["known_map_negative_control"];yes=p["known_map_positive_control"]
assert n["R"]=="y" and yes["R"]=="x"
assert n["identity_LR"]=="1" and yes["identity_LR"]=="4"
assert n["task_accuracy"]==yes["task_accuracy"]=="3/4"
assert F(n["p_E_given_H"])/F(n["p_E_given_notH"])==F(1)
assert F(yes["p_E_given_H"])/F(yes["p_E_given_notH"])==F(4)
assert F(n["task_accuracy"])>F(1,2)
assert "not" not in n["R"]
assert "a new Bayesian principle" in p["not_claimed"]
assert "published scientists committed this exact error" in p["not_claimed"]
assert m29["proof_model"]["events"]["Ey"]["LR"] == "1"
assert m29["proof_model"]["events"]["Ex"]["LR"] == "4"

d=spec["distinctions"]
assert "One coarse match event" in d["D_U"] and "Two different" in d["x_y"]
assert "QUALIFIED" in d["partial_knowledge"]
assert "ACTIVATED_UNDERCUTTING" in d["partial_knowledge"]
q=spec["patterson_gainotti_fixed_question"]
assert q["same_identity_question"] is True
assert q["independent_C_justified"] is False
assert q["actual_pairwise_identity_measured"] is False
assert "underqualified" in q["outcome_for_known_task_match"].lower()
assert "NOT_PAIR_IDENTITY" in q["outcome_for_lesion_contrast"]
assert set(q["science_grounded_sources"])=={"PattersonNestorRogers2007Semantic","Gainotti2012SemanticFormat"}
for cite in q["science_grounded_sources"]:
    assert cite in bib
assert m31["conditional_application"]["C_is_construction_not_independently_established"] is True

checks={
 "main":[
    "evidential promotion",
    "known-map promotion error",
    "with a known map",
    r"\Pr(E_y\mid H_C)=\Pr(E_y\mid\neg H_C)=1/2",
    "identity-specific",
    "conditional illustration of how a support attribution can be undercut",
    "different epistemic situations",
    r"C_{\mathrm{role}}",
    r"Q_{\mathrm{role}}",
    r"C_{\mathrm{id}}",
    r"Q_{\mathrm{id}}",
    r"\citep{Beni2026KindsWithoutStructure}",
    r"\citep{Brousalis2026TheoryComparison}"
 ],
 "supp":[
    "Fixed-question evidence-transfer matrix",
    "Source-anchored semantic architecture",
    "known-map evidential promotion",
    "clinical",
    "qualif",
    "a separate reporting procedure",
    "not interchangeable",
    "M31 frozen baseline",
 ],
 "index":[
    "M32_EVIDENTIAL_PROMOTION_AUDIT_v1.json",
    "paper2_m32_evidential_promotion_audit.py",
    "4e1b5141baf64ba7283011aca0681e5c730e0f74",
    "M29 finite pair-law probability model"
 ]
}
for label,body in (("main",main),("supp",supp),("index",index)):
    for phrase in checks[label]:
        assert phrase in body, f"{label} missing: {phrase}"
for condition in (spec["corpus_rerun"],spec["recoded_claims"]):
    assert condition is False
assert spec["no_empirical_identity_defeater"] is True
assert spec["frozen_science"]["whole_pairs"]==m29["frozen_science"]["whole_pairs"]=="1770/1770 INCOMPARABLE"
assert spec["frozen_science"]["bounded_objects"]==m29["frozen_science"]["bounded_objects"]==206
assert spec["frozen_science"]["cross_stratum_families"]==m29["frozen_science"]["cross_stratum_families"]==99
assert spec["frozen_science"]["cpcg_signatures"]==m29["frozen_science"]["cpcg_signatures"]==143
assert spec["frozen_science"]["collision_families"]==m29["frozen_science"]["cpcg_collisions"]=="63/99"
assert spec["frozen_science"]["reverse_projection"]==m29["frozen_science"]["reverse"]
assert spec["frozen_science"]["human_inter_rater"]=="unmeasured"
print("M32_EVIDENTIAL_PROMOTION_AND_SOURCE_BOUNDARY_GUARDS_PASS")
