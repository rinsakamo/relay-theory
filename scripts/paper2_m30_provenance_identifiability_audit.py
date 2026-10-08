#!/usr/bin/env python3
"""M30 provenance non-identifiability and positive-control audit."""
from __future__ import annotations
import json
from pathlib import Path
from fractions import Fraction as Q
from itertools import product

ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "paper/venues/jgps/main.tex").read_text(encoding="utf-8")
SUPP = (ROOT / "paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
INDEX = (ROOT / "paper/venues/jgps/supplementary-materials-index.md").read_text(encoding="utf-8")
DATA = json.loads((ROOT / "research/paper2/p399/main/integration/M30/M30_PROVENANCE_IDENTIFIABILITY_v1.json").read_text(encoding="utf-8"))
M29 = json.loads((ROOT / "research/paper2/p399/main/integration/M29/M29_FINITE_PAIR_LAW_v1.json").read_text(encoding="utf-8"))

assert DATA["parent_m29_exact_head"] == "513ac238a3f94b1723270ac52c659962e052d613"
assert DATA["new_corpus_run"] is False and DATA["new_human_recoding"] is False
assert DATA["thin_record"]["match"] is True
assert DATA["thin_record"]["omits"] == ["representation_map_R", "exact_match_event_id"]
assert DATA["counterexample"]["no_single_map_specific_LR_from_thin_record"] is True

# Reconstruct the original finite sampling distribution independently.
states = list(product((0, 1), repeat=3))
assert len(states) == 8
# Derive a shared, nontrivial ordinary predictive task under either hypothesis.
task = DATA["ordinary_task_control"]
scores = {}
for predictor in ("x", "y"):
    score = Q(0)
    for c,x,y,j in product((0,1), repeat=4):
        target = x if j == 0 else y
        guess = x if predictor == "x" else y
        if guess == target:
            score += Q(1,16)
    scores[predictor] = score
assert scores == {"x":Q(3,4), "y":Q(3,4)}
assert scores["x"] > Q(task["admissibility_threshold"]) == Q(2,3)
assert scores["x"] == Q(task["accuracy_phi_x"]) and scores["y"] == Q(task["accuracy_phi_y"])
assert task["same_ordinary_task"] is True and task["empirical_validation"] is False

def event_prob(h, which):
    q = Q(4, 5) if h else Q(1, 5)
    total = Q(0)
    for ca, xa, ya, ex, ey in product((0, 1), repeat=5):
        a = ca, xa, ya
        b = (ca if h else 1-ca), xa ^ ex, ya ^ ey
        p = Q(1, 8) * (q if ex == 0 else 1-q) * Q(1, 2)
        if (which == "x" and a[1] == b[1]) or (which == "y" and a[2] == b[2]) or (which == "union" and (a[1] == b[1] or a[2] == b[2])):
            total += p
    return total
full = {r: (event_prob(True, r), event_prob(False, r)) for r in ("x", "y", "union")}
ratios = {r: a/b for r,(a,b) in full.items()}
assert ratios == {"x":Q(4), "y":Q(1), "union":Q(3,2)}

records = DATA["full_records"]
assert len(records) == 2 and {r["R"] for r in records} == {"x", "y"}
assert records[0]["thin_key"] == records[1]["thin_key"]
assert records[0]["match"] == records[1]["match"] == True
for rec in records:
    num, den = full[rec["R"]]
    assert num == Q(rec["p_same"]) and den == Q(rec["p_diff"])
    assert num / den == Q(rec["lr"])
assert records[0]["lr"] != records[1]["lr"]
assert "ordinary_task_admissibility" in DATA["thin_record"]

# Negative: the unlabelled positive match has no unique calibrated LR without w.
def marginalized(w):
    same = w * full["x"][0] + (1-w)*full["y"][0]
    diff = w * full["x"][1] + (1-w)*full["y"][1]
    return same / diff
assert marginalized(Q(0)) == Q(1)
assert marginalized(Q(1, 2)) == Q(13, 7)
assert marginalized(Q(1)) == Q(4)
assert len({marginalized(Q(0)), marginalized(Q(1,2)), marginalized(Q(1))}) == 3
# Positive: when map identity is retained, its selection weight cancels.
w = Q(1, 2)
assert (w*full["x"][0])/(w*full["x"][1]) == Q(4)
assert ((1-w)*full["y"][0])/((1-w)*full["y"][1]) == Q(1)

cases = {x["id"]:x for x in DATA["controls"]}
assert set(cases) == {"P1","N1","P2","N2","P3","P4","N3"}
assert cases["P1"]["classification"] == "QUALIFIED_POSITIVE" and cases["P1"]["lr"] == "4"
assert cases["P1"]["rival_y_automatically_undercuts"] is False
assert cases["N1"]["classification"] == "QUALIFIED_NEUTRAL" and cases["N1"]["lr"] == "1"
assert cases["P2"]["lr"] == "13/7" and cases["N2"]["lr"] == "NOT_IDENTIFIED"
assert cases["P3"]["lr"] == "3/2" and cases["P3"]["equivalence_relation"] is False
assert cases["P4"]["classification"] == "DR_SATISFIED" and cases["P4"]["added_foundational_norm"] is False
assert cases["N3"]["classification"] == "OUT_OF_SCOPE" and cases["N3"]["active_defeater"] is False

for phrase in (
    r"\label{sec:provenance-identifiability}",
    "thin appraisal record",
    "no function of the thin record alone",
    "The five positive and negative appraisal controls",
    "equally and nontrivially predictive for the same toy task",
    "correctly calibrated",
    "standard appraisal already identifies",
    "not a new axiom of confirmation",
):
    assert phrase in MAIN, f"Main missing {phrase}"
for phrase in (
    "Provenance non-identifiability",
    r"\label{tab:provenance-controls}",
    r"\Pr(T=x)",
    "complete reporting record",
    "thin record",
    "can return the correct map-specific likelihood ratio",
    "not automatically a positive defeater",
):
    assert phrase in SUPP, f"Supplement missing {phrase}"
assert "M30_PROVENANCE_IDENTIFIABILITY_v1.json" in INDEX
assert DATA["scientific_authority_unchanged"]["whole_pairs"] == M29["frozen_science"]["whole_pairs"]
assert DATA["scientific_authority_unchanged"]["bounded_objects"] == M29["frozen_science"]["bounded_objects"]
assert DATA["scientific_authority_unchanged"]["cross_stratum_families"] == M29["frozen_science"]["cross_stratum_families"]
assert DATA["scientific_authority_unchanged"]["cpcg_signatures"] == M29["frozen_science"]["cpcg_signatures"]
assert DATA["scientific_authority_unchanged"]["cpcg_collisions"] == M29["frozen_science"]["cpcg_collisions"]
assert DATA["scientific_authority_unchanged"]["reverse"] == M29["frozen_science"]["reverse"]
for name, value in (("MAIN", MAIN),("SUPP", SUPP)):
    assert "ClaimIR" not in value, name
print("M30_PROVENANCE_IDENTIFIABILITY_GUARDS_PASS")
