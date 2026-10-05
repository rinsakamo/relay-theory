#!/usr/bin/env python3
import json
import pathlib
import subprocess

R = pathlib.Path(__file__).resolve().parent
S = {
    "INT-12": "10.1371/journal.pcbi.1006116",
    "INT-13": "10.1371/journal.pcbi.1014796",
    "INT-14": "10.1371/journal.pcbi.1007594",
    "INT-15": "10.1371/journal.pcbi.1010047",
    "INT-16": "10.1371/journal.pcbi.1004060",
}
K = "3c2761ac13b04203aa7dbd8f47a1d687d506bf7b"
M = "b97b67a34ad9c2858745dfa6aa60444520eaab13"
A = "949347fa32ddb4af51832d25d3d9dca5ba3f79f2"
B = "6343c736266b5cbe6eb0202b4503888459ba02a1"

def L(path):
    return json.loads((R / path).read_text())

def G(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

checks = []

def ck(name, value):
    if not value:
        raise AssertionError(name)
    checks.append(name)
    print(f"PASS {len(checks):02d} {name}")

intake = L("M6_FIVE_PAPER_INTAKE_RECEIPT_v1.json")
reg = L("M6_FIVE_PAPER_OUTCOME_REGISTRY_v1.json")
neg = L("M6_NEGATIVE_AND_UNDERDETERMINED_REGISTER_v1.json")
bd = L("M6_INTEGRATION_BOUNDARY_AUDIT_v1.json")

outcomes = {s: L(f"{s}/ARCHITECTURAL_OUTCOME_v1.json") for s in S}
grammars = {s: L(f"{s}/GRAMMAR_V0_RECONSTRUCTION_v1.json") for s in S}
locks = {s: L(f"{s}/SOURCE_AUTHORITY_LOCK_v1.json") for s in S}
lims = {s: L(f"{s}/LIMITATIONS_AND_NEGATIVE_EVIDENCE_v1.json") for s in S}
pass_b = {s: L(f"{s}/PASS_B_RESULT_INFORMED_REAUDIT_v1.json") for s in S}
pass_c = {s: L(f"{s}/PASS_C_SOURCE_CLOSED_ADJUDICATION_v1.json") for s in S}

ck("01 exact 5-paper assignment", intake["exact_assignment"] == [{"slot": s, "doi": d} for s, d in S.items()])
ck("02 exact DOI identity", {r["slot"]: r["doi"] for r in reg["rows"]} == S)
ck("03 no paper outside M6", {p.name for p in R.iterdir() if p.is_dir() and p.name.startswith("INT-")} == set(S))
ck("04 exact kickoff HEAD ancestry", subprocess.call(["git", "merge-base", "--is-ancestor", K, "HEAD"]) == 0)
ck("05 exact frozen manifest blob", G("rev-parse", f"{K}:research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json") == M)
ck("06 no duplicate paper", len({r["slot"] for r in reg["rows"]}) == 5 and len({r["doi"] for r in reg["rows"]}) == 5)
ck("07 no roster substitution", intake["roster_substitution"] is False)
ck("08 no backup activation", intake["backup_activation"] is False)
ck("09 Stage A before B", subprocess.call(["git", "merge-base", "--is-ancestor", A, B]) == 0)
ck("10 B receives frozen A", all(pass_b[s]["frozen_A"]["stage_a_final_lane_head"] == A for s in S))
ck("11 C objections source-traced", all(
    pass_c[s]["c1_overpatch_safeguard"]["full_original_A_reopened"]
    and all(x["source_reopened_locus"] and x["original_A_reopened_in_full"] for x in pass_c[s]["c1_overpatch_safeguard"]["adjudications"])
    for s in S
))
ck("12 negative evidence retained", len(neg["entries"]) == 5 and all(lims[s]["retained_negative_and_adverse_evidence"] for s in S))
roles = {"Pi", "X", "C", "Q", "P_in", "P_out", "K", "T", "rho/O"}
ck("13 Grammar roles cannot silently change", all(set(grammars[s]["grammar_authority"]["roles"]) == roles and grammars[s]["grammar_authority"]["modified"] is False for s in S))
ck("14 hierarchy cannot auto-create coordinator", bd["cross_boundary_tests"]["hierarchy_vs_coordination"] == "PASS_NO_AUTO_PROMOTION")
ck("15 CRP clustering cannot auto-create meta-controller", bd["cross_boundary_tests"]["crp_vs_meta_controller"] == "PASS_DISTINGUISHED")
ck("16 graph abstraction cannot auto-create executive state", bd["cross_boundary_tests"]["abstraction_vs_controller"] == "PASS_DISTINGUISHED")
ck("17 decision accumulator cannot auto-create coordinator", bd["cross_boundary_tests"]["decision_accumulation_vs_coordination"] == "PASS_DISTINGUISHED")
ck("18 model-based/model-free combination cannot auto-create A2", outcomes["INT-15"]["final_architectural_state"] == "A0_FIDELITY" and outcomes["INT-15"]["reconstruction_added_stateful_mechanism_count"] == 0)
ck("19 source-defined RL/WM interaction cannot be double-counted as reconstruction-added A2", outcomes["INT-13"]["final_architectural_state"] == "A0_FIDELITY" and outcomes["INT-13"]["reconstruction_added_stateful_mechanism_count"] == 0)
ck("20 global neuromodulatory signal cannot auto-create executive control", bd["cross_boundary_tests"]["neuromodulation_vs_executive"] == "PASS_DISTINGUISHED")
ck("21 recurrent working-memory state cannot auto-create additional coordinator", all(outcomes[s]["reconstruction_added_stateful_mechanism_count"] == 0 for s in ("INT-13", "INT-16")))
ck("22 A2 requires documented A0+A1 failure", all(
    o["tests"][0]["result"] == "PASS" and o["tests"][1]["result"] == "NOT_REACHED_AFTER_A0_PASS" and o["tests"][2]["result"] == "NOT_REACHED_AFTER_A0_PASS"
    for o in outcomes.values()
))
ck("23 fit difficulty alone cannot imply A2", reg["counts"]["A2_FIDELITY"] == 0 and all(r["reconstruction_added_stateful_mechanism_type_count"]["count"] == 0 for r in reg["rows"]))
ck("24 INT-13 frozen proof status cannot be silently upgraded to corrected final VoR", locks["INT-13"]["adopted_source"]["edition"] == "AUTHOR_APPROVED_FROZEN_PUBLISHER_PROOF" and locks["INT-13"]["adopted_source"]["corrected_final_vor"] is False)
ck("25 INT-14 bounded CRP genealogy distinction cannot become independence", "SHARED_CONSTITUENT_ONLY" in locks["INT-14"]["genealogy_annotation"] and locks["INT-14"]["authority"]["genealogy_independence_assumed"] is False)
ck("26 INT-15/P18 bounded difference cannot become independence", "BOUNDED_SOURCE_NATIVE_DIFFERENCE" in locks["INT-15"]["genealogy_annotation"] and locks["INT-15"]["authority"]["genealogy_independence_assumed"] is False)
ck("27 INT-16/P09 bounded difference cannot become independence", "BOUNDED_SOURCE_NATIVE_DIFFERENCE" in locks["INT-16"]["genealogy_annotation"] and locks["INT-16"]["authority"]["genealogy_independence_assumed"] is False)
ck("28 UNDERDETERMINED preserved", any(e["slot"] == "INT-15" and e["status"] == "RETAINED_UNDERDETERMINATION" for e in neg["entries"]) and any(e["slot"] == "INT-14" and any("genealogy unresolved" in x for x in e["items"]) for e in neg["entries"]))
ck("29 SOURCE_INELIGIBLE cannot trigger replacement", reg["counts"]["SOURCE_INELIGIBLE"] == 0 and intake["roster_substitution"] is False and intake["backup_activation"] is False)
ck("30 genealogy cannot alter roster", {r["slot"] for r in reg["rows"]} == set(S) and len(reg["rows"]) == 5)
ck("31 no genealogy-independence promotion", all(o["genealogy_independence_claimed"] is False for o in outcomes.values()))
ck("32 G1 PILOT20 excluded", intake["g1_pilot20_excluded"] is True and intake["authority"]["g1_pilot20_main_evidence"] is False)
ck("33 final outcome count = 5", len(reg["rows"]) == 5 and reg["counts"]["total"] == 5 and sum(v for k, v in reg["counts"].items() if k != "total") == 5)
ck("34 M6 cannot issue overall H0/H1/H2 conclusion", reg["overall_H_verdict"] is None and all(o["h0_h1_h2_conclusion_issued"] is False for o in outcomes.values()))

print(f"M6_FAIL_CLOSED_PASS {len(checks)}/{len(checks)}")
