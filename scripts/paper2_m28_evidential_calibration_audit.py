#!/usr/bin/env python3
"""Fail-closed checks for the M28 conditional evidence manuscript revision."""
from __future__ import annotations
import json
import re
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "paper/venues/jgps/main.tex").read_text(encoding="utf-8")
SUPP = (ROOT / "paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
INDEX = (ROOT / "paper/venues/jgps/supplementary-materials-index.md").read_text(encoding="utf-8")
SPEC = json.loads((ROOT / "research/paper2/p399/main/integration/M28/M28_EVIDENTIAL_CALIBRATION_v1.json").read_text(encoding="utf-8"))
M27 = "dd043ce1312d658fdd3d47a8875114b59c19e096"

assert SPEC["exact_parent_m27_head"] == M27
assert SPEC["scientific_changes"] == "NONE"
assert not SPEC["new_empirical_corpus_execution"]
assert not SPEC["new_human_coding"]
assert not SPEC["crossing_alone_implies_non_support"]
assert SPEC["undercutting_is_not_automatically_rebutting"]
D = SPEC["diagnostic_coarse_map_D"]
U = SPEC["cross_preserving_rival_U"]
for p in (D, U):
    odds = Fraction(str(p["p_match_same"])) / Fraction(str(p["p_match_different"]))
    assert odds == Fraction(p["lr"])
def ratio(w: Fraction) -> Fraction:
    return (Fraction(1, 2) + Fraction(3, 10)*w) / (Fraction(1, 2) - Fraction(3, 10)*w)
assert ratio(Fraction(0)) == 1
assert ratio(Fraction(1, 2)) == Fraction(13, 7)
assert ratio(Fraction(1)) == 4
assert ratio(Fraction(0)) < ratio(Fraction(1, 2)) < ratio(Fraction(1))

for phrase in [
    r"\Lambda_R(B)", r"\Lambda_{\mathrm{mix}}(w)",
    r"\Pr(E_R\mid H_C,B)", "13/7", "not a theorem",
    "scientifically motivated same-", "The numerical probabilities are invented",
    "a ratio of", "need not be transitive",
    r"E_R^{\mathrm{bounded}}(f_A,f_B)",
    r"M_R(f_A)\cap M_R(f_B)",
    "The identity argument must identify the induced event",
    "Justifying", "procedural",
]:
    assert phrase in MAIN, f"main missing {phrase}"
for phrase in ["13/7", "four entries are stipulated", "The latter need not be transitive", "immutable source snapshot", M27]:
    assert phrase in SUPP, f"supplement missing {phrase}"
assert "M28_EVIDENTIAL_CALIBRATION_v1.json" in INDEX
assert M27 in INDEX
assert SPEC["frozen_scientific_authority"]["whole_claim_pairs"] == "1770/1770 INCOMPARABLE"
assert SPEC["frozen_scientific_authority"]["bounded_objects"] == 206
assert SPEC["frozen_scientific_authority"]["cross_stratum_families"] == 99
assert SPEC["frozen_scientific_authority"]["cpcg_signatures"] == 143
assert SPEC["frozen_scientific_authority"]["cpcg_colliding_cross_stratum_families"] == "63/99"
assert SPEC["frozen_scientific_authority"]["reverse_projection"] == "21 FULL / 22 PARTIAL / 17 RESIDUAL"
assert SPEC["frozen_scientific_authority"]["residual_new_top_level_roles"] == "0/17"
assert SPEC["frozen_scientific_authority"]["independent_human_inter_rater_reliability"] == "unmeasured"
for path, content in (("main", MAIN), ("supplement", SUPP)):
    assert not re.search(r"\bM2[78]\b", content), path
    assert "ClaimIR" not in content, path
print("M28_EVIDENTIAL_CALIBRATION_GUARDS_PASS")
