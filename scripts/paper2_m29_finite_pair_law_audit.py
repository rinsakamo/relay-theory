#!/usr/bin/env python3
"""M29 exhaustive finite-pair calculation and non-promotion checks."""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
M29 = ROOT / "research/paper2/p399/main/integration/M29/M29_FINITE_PAIR_LAW_v1.json"
SPEC = json.loads(M29.read_text(encoding="utf-8"))
MAIN = (ROOT / "paper/venues/jgps/main.tex").read_text(encoding="utf-8")
SUPP = (ROOT / "paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
BIB = (ROOT / "paper/venues/jgps/references.bib").read_text(encoding="utf-8")
INDEX = (ROOT / "paper/venues/jgps/supplementary-materials-index.md").read_text(encoding="utf-8")
assert SPEC["parent_m28_head"] == "fb689ce586be1cf1d2d9b87a75eb385c2674ffda"
assert SPEC["new_corpus_run"] is False and SPEC["new_human_coding"] is False
assert SPEC["proof_model"]["no_automatic_defeater_from_rival_map"] is True

S = list(product(range(2), repeat=3))
assert len(S) == SPEC["proof_model"]["cardinality"] == 8

def C(s):
    return s[0]

def phi_x(s):
    return s[1]

def phi_y(s):
    return s[2]

for phi in (phi_x, phi_y):
    fibers = defaultdict(list)
    for state in S:
        fibers[phi(state)].append(state)
    assert set(fibers) == {0, 1}
    assert all(len(fiber) == 4 and {C(s) for s in fiber} == {0, 1} for fiber in fibers.values())

def pair_law(h):
    q = F(SPEC["proof_model"]["ordered_pair_distribution"]["q_eta_x_match_given_H" if h else "q_eta_x_match_given_nonH"])
    weights = {}
    for ca, xa, ya, ex, ey in product(range(2), repeat=5):
        a = ca, xa, ya
        b = (ca if h else 1-ca), xa ^ ex, ya ^ ey
        weight = F(1, 8) * (q if ex == 0 else 1-q) * F(1, 2)
        assert (a, b) not in weights
        weights[a, b] = weight
    assert len(weights) == SPEC["proof_model"]["ordered_pair_distribution"]["supported_ordered_pairs_per_hypothesis"] == 32
    assert sum(weights.values(), F(0)) == F(1)
    assert all((C(a) == C(b)) == h for a, b in weights)
    return weights

ph = pair_law(True)
pn = pair_law(False)

def motif_set(f):
    return {("x", f[1]), ("y", f[2])}

def event_probability(dist, which):
    return sum((p for (a, b), p in dist.items() if which(a, b)), F(0))

predicates = {
    "Ex": lambda a,b: phi_x(a) == phi_x(b),
    "Ey": lambda a,b: phi_y(a) == phi_y(b),
    "bounded_union": lambda a,b: bool(motif_set(a) & motif_set(b)),
}
for name, predicate in predicates.items():
    result = SPEC["proof_model"]["events"][name]
    same, other = event_probability(ph, predicate), event_probability(pn, predicate)
    assert same == F(result["given_same"]), (name, same)
    assert other == F(result["given_different"]), (name, other)
    assert same / other == F(result["LR"]), (name, same / other)

a, b, c = map(tuple, SPEC["proof_model"]["nontransitive_witness"])
assert motif_set(a) & motif_set(b)
assert motif_set(b) & motif_set(c)
assert not (motif_set(a) & motif_set(c))

ex_h = event_probability(ph, predicates["Ex"])
ex_n = event_probability(pn, predicates["Ex"])
ey_h = event_probability(ph, predicates["Ey"])
ey_n = event_probability(pn, predicates["Ey"])
for w, expected in [(F(0), F(1)), (F(1,2), F(13,7)), (F(1), F(4))]:
    numerator = w * ex_h + (1-w) * ey_h
    denominator = w * ex_n + (1-w) * ey_n
    assert numerator / denominator == expected
    if w == F(1,2):
        ev = SPEC["proof_model"]["events"]["map_unlabelled_weight_half"]
        assert numerator == F(ev["given_same"]) == F(13,20)
        assert denominator == F(ev["given_different"]) == F(7,20)
        assert numerator / denominator == F(ev["LR"])
        # When R=x is retained, its event has ratio 4 despite the rival.
        assert (w*ex_h) / (w*ex_n) == F(4)
        assert ((1-w)*ey_h) / ((1-w)*ey_n) == F(1)

assert SPEC["frozen_science"]["whole_pairs"] == "1770/1770 INCOMPARABLE"
assert SPEC["frozen_science"]["bounded_objects"] == 206
assert SPEC["frozen_science"]["cross_stratum_families"] == 99
assert SPEC["frozen_science"]["cpcg_signatures"] == 143
assert SPEC["frozen_science"]["cpcg_collisions"] == "63/99"
assert SPEC["frozen_science"]["reverse"] == "21 FULL / 22 PARTIAL / 17 RESIDUAL"
assert SPEC["frozen_science"]["residual_new_role"] == "0/17"
assert SPEC["frozen_science"]["human_inter_rater"] == "unmeasured"

for fragment in [
    r"\label{sec:finite-pair-law}",
    r"\mathcal F=\{(c,x,y)",
    r"\phi_x(c,x,y)=x",
    r"E_x\lor E_y",
    r"\label{tab:finite-pair}",
    "A rival map alone does not undercut correctly calibrated",
    "This conditional calculation requires uncertainty",
    "no actual corpus-level capacity identity",
    r"\citep{DawEtAl2011ModelBasedInfluences}",
]:
    assert fragment in MAIN, f"missing main: {fragment}"
for fragment in ["Finite pair-law derivation", "16 pairs", "The unlabelled-report mixture", "M28 numerical", "normalized"]:
    assert fragment in SUPP, f"missing supplement: {fragment}"
assert "@article{DawEtAl2011ModelBasedInfluences," in BIB
assert "10.1016/j.neuron.2011.02.027" in BIB
assert "M29_FINITE_PAIR_LAW_v1.json" in INDEX
print("M29_FINITE_PAIR_LAW_EXHAUSTIVE_GUARDS_PASS")
