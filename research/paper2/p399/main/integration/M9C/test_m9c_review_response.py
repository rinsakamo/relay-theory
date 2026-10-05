import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[6]
M9C = ROOT / "research/paper2/p399/main/integration/M9C"

checks = []
def check(name, cond):
    if not cond:
        raise AssertionError(name)
    checks.append(name)

matrix = json.loads((M9C / "M9C_HOSTILE_REVIEW_RESPONSE_MATRIX_v1.json").read_text())
response = (ROOT / "paper/venues/jgps/response-to-reviewers.md").read_text()
manuscript = (ROOT / "paper/venues/jgps/main.tex").read_text()

check("schema", matrix["schema"] == "relaytheory.p399.main.m9c.hostile_review_response_matrix.v1")
check("base_m9b", matrix["base_m9b_head"] == "568aa41ead6c246120aa449b48c57a2e99094ef1")
check("ten_items", len(matrix["items"]) == 10)
check("unique_ids", len({x["id"] for x in matrix["items"]}) == 10)

by_id = {x["id"]: x for x in matrix["items"]}
required = {
    "R1_A_STATE_DISCRIMINABILITY",
    "R2_PAPER_LEVEL_EVIDENCE",
    "R3_PROSPECTIVE_CHRONOLOGY",
    "R4_INDEPENDENT_HUMAN_ADJUDICATION",
    "R5_GENEALOGY_AND_INDEPENDENCE",
    "R6_GRAMMAR_NONTRIVIALITY_AND_POMDP",
    "R7_CIRCULARITY_AND_LEAKAGE",
    "R8_PHILOSOPHICAL_PAYOFF",
    "R9_CLAIM_STRENGTH",
    "R10_MANUSCRIPT_AUTHORITY_WORDING",
}
check("required_ids", set(by_id) == required)
check("human_limitation",
      by_id["R4_INDEPENDENT_HUMAN_ADJUDICATION"]["disposition"] == "ACKNOWLEDGED_LIMITATION_NOT_REMEDIED")
check("genealogy_not_resolved",
      "NOT_RESOLVED" in by_id["R5_GENEALOGY_AND_INDEPENDENCE"]["disposition"])
check("circularity_not_eliminated",
      by_id["R7_CIRCULARITY_AND_LEAKAGE"]["disposition"] == "MITIGATED_NOT_ELIMINATED")

overall = matrix["overall"]
check("main_counts", overall["main40_counts"] == {"A0": 40, "A1": 0, "A2": 0})
check("no_human", overall["independent_human_adjudication_performed"] is False)
check("no_readjudication", overall["main40_re_adjudicated"] is False)

for phrase in [
    "procedural auditability rather than inter-rater reliability",
    "single-adjudicator, source-identity-separated prospective compatibility test",
    "POMDPs cannot encode the tested cognitive models",
    "Independent human re-adjudication was not performed",
]:
    check(f"response_{phrase}", phrase in response)

for phrase in [
    "construct individuation is not inherited from vocabulary",
    "informative negative compression result",
    "successful reconstruction is representation-relative",
    "single-adjudicator prospective compatibility corpus",
    "Independent human re-adjudication remains a distinct external validation opportunity",
    "The manuscript is the object submitted for scholarly review",
]:
    check(f"manuscript_{phrase}", phrase in manuscript)

for forbidden in [
    "The manuscript source is non-authoritative",
    "POMDPs cannot encode the tested cognitive models",
    "40 independent replications prove",
    "independent human re-adjudication was performed",
]:
    check(f"forbidden_{forbidden}", forbidden not in manuscript)

check("response_no_fake_human",
      "It was not performed in the present single-author study." in response)
check("response_posthoc_separation",
      "This calibration is explicitly post hoc." in response)

print(f"M9C_REVIEW_RESPONSE_PASS {len(checks)}/{len(checks)}")
