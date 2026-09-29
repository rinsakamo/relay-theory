#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P2 = ROOT / "research" / "paper2"


def load(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"PAPER2_FINAL_RESULT_AUDIT_FAIL: {message}")


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


manifest = load(P2 / "chatgpt_reference_claimir_v1" / "manifest.json")
aggregate = load(P2 / "grammar_v0_reverse_projection_aggregate_v1.json")
residual = load(P2 / "grammar_v0_residual_adjudication_v1.json")
minimality = load(P2 / "grammar_v0_minimality_comparator_v1.json")
placements = load(P2 / "source_context_architecture_placement_v1.json")
layered = load(P2 / "grammar_v0_layered_architecture_v1.json")
forgetful = load(P2 / "grammar_v0_forgetful_maps_v1.json")
system_world = load(P2 / "system_world_experiment_architecture_v1.json")
reliability = load(P2 / "claim_ir_reliability_boundary_v1.json")
expected = load(P2 / "paper2_result_v1.json")

entries = manifest["entries"]
require(len(entries) == 60, "reviewed ClaimIR manifest must contain 60 entries")
slot_ids = [e["slot_id"] for e in entries]
require(len(set(slot_ids)) == 60, "ClaimIR slot IDs must be unique")
require(
    manifest["state"] == "ALL_60_DESIGNED_CLAIMIR_SOURCE_GROUNDED_REVIEWED",
    "ClaimIR manifest state drift",
)

reviewed = 0
for entry in entries:
    claim = load(P2 / "chatgpt_reference_claimir_v1" / entry["file"])
    require(
        claim["extraction"]["manual_review_status"] == "reviewed",
        f'{entry["slot_id"]} manual_review_status drift',
    )
    require(
        claim["provenance"]["paper_id"] == entry["stable_identity"],
        f'{entry["slot_id"]} stable source identity drift',
    )
    reviewed += 1

claim_verdict_counts = Counter(x["verdict"] for x in aggregate["claim_verdicts"])
require(len(aggregate["claim_verdicts"]) == 60, "aggregate claim verdict count drift")
lane_sum = Counter()
for lane in aggregate["lane_sources"]:
    lane_sum.update(lane["verdict_counts"])

aggregate_counts = aggregate["aggregate_verdict_counts"]
for key in ("FULL", "PARTIAL", "RESIDUAL"):
    require(claim_verdict_counts[key] == aggregate_counts[key], f"{key} claim verdict mismatch")
    require(lane_sum[key] == aggregate_counts[key], f"{key} lane sum mismatch")
require(sum(claim_verdict_counts.values()) == aggregate_counts["TOTAL"] == 60, "verdict TOTAL mismatch")

role_order = ["Pi", "X", "C", "Q", "P_in", "P_out", "K", "T", "rho/O"]
role_counts = {}
for role in role_order:
    aggregate_count = aggregate["aggregate_role_frequency"][role]
    minimality_count = minimality["full_v0_role_support"][role]["claim_count"]
    require(aggregate_count == minimality_count, f"{role} cross-artifact role-count mismatch")
    role_counts[role] = aggregate_count

res_summary = residual["summary"]
require(res_summary["residual_claims"] == aggregate_counts["RESIDUAL"] == 17, "residual claim count mismatch")
require(res_summary["primary_class_counts"]["ROLE_GAP"] == 0, "ROLE_GAP must remain zero")
require(res_summary["role_gap_claims"] == [], "ROLE_GAP claim list must remain empty")
require(sum(res_summary["primary_class_counts"].values()) == 17, "residual primary taxonomy must partition 17 claims")

placement_rows = placements["placements"]
placement_counts = Counter(x["primary"] for x in placement_rows)
require(len(placement_rows) == placements["scope"]["residual_condition_nodes"] == 27, "source-context node count mismatch")
require(dict(placement_counts) == placements["primary_counts"], "source-context primary counts mismatch")
require(sum(placement_counts.values()) == 27, "source-context placement count must sum to 27")

gdyn = minimality["comparator_G_dyn"]
pomdp = minimality["comparator_G_pomdp_like"]
require(gdyn["claims_requiring_at_least_one_role_beyond_G_dyn"] == 59, "G_dyn beyond-role count drift")
require(gdyn["strict_full_direct_preservation_count"] == 0, "G_dyn strict FULL preservation drift")
require(pomdp["claims_requiring_Pi_or_C"] == 26, "POMDP-like Pi/C witness count drift")
require(pomdp["interface_directionality"]["both_P_in_and_P_out"] == 26, "POMDP-like interface split witness count drift")
require(pomdp["union_claims_affected_by_missing_Pi_or_C_or_collapsed_P_direction"] == 44, "POMDP-like union loss count drift")

require(
    layered["terminal_classification"]
    == "SYSTEM_GRAMMAR_SEPARATED_FROM_CLAIM_CONTEXT_AND_FORMAL_LAYERS_WITH_GRAMMAR_V0_UNCHANGED",
    "layered-architecture terminal drift",
)
require(
    forgetful["terminal_classification"]
    == "FORGETFUL_VIEWS_FORMALIZED_AND_FROZEN_DISTINCTION_LOSS_WITNESSED",
    "forgetful-map terminal drift",
)
require(
    system_world["terminal_classification"]
    == "COGNITIVE_SYSTEM_WORLD_COUPLING_AND_EXPERIMENT_SEPARATED_WITH_RUN_CUT_SEMANTICS",
    "system/World/experiment terminal drift",
)
require("GRAMMAR_V0_UNCHANGED" in system_world["architecture_consequence"], "system/World artifact must preserve Grammar v0")
require(aggregate["grammar_modified"] is False, "aggregate must not modify Grammar v0")
require(minimality["conclusions"]["grammar_v1_authorized"] is False, "Grammar v1 must remain unauthorized")

require(
    reliability["terminal_classification"]
    == "EXTRACTION_UNDERDETERMINED_WITH_SOURCE_AUDITED_REFERENCE_CORPUS",
    "ClaimIR reliability boundary drift",
)
require(reliability["independent_extractor_structural_agreement"] == "NOT_ESTABLISHED", "independent-extractor boundary drift")
require(reliability["deterministic_chatgpt_replay_claimed"] is False, "deterministic replay must not be claimed")
require(reliability["source_grounded_reviewed_reference_corpus"]["reviewed_claims"] == reviewed == 60, "reviewed corpus count mismatch")

grammar_path = ROOT / "formal" / "relay_theory" / "RelayTheory" / "UnifiedCognitiveStructuralGrammar.lean"
grammar_blob = git_blob_sha1(grammar_path)
require(
    grammar_blob == expected["formal_identity"]["grammar_git_blob_sha1"],
    "UnifiedCognitiveStructuralGrammar.lean blob drift",
)

actual = {
    "schema_version": "paper2-result-v1",
    "owner_issue": 351,
    "status": "FROZEN_DETERMINISTIC_RECONCILIATION",
    "source_review": {
        "reviewed_claims": reviewed,
        "total_claims": len(entries),
        "manifest_state": manifest["state"],
        "independent_extractor_agreement": reliability["independent_extractor_structural_agreement"],
        "deterministic_chatgpt_replay_claimed": reliability["deterministic_chatgpt_replay_claimed"],
        "reliability_terminal": reliability["terminal_classification"],
    },
    "reverse_projection": {
        "FULL": aggregate_counts["FULL"],
        "PARTIAL": aggregate_counts["PARTIAL"],
        "RESIDUAL": aggregate_counts["RESIDUAL"],
        "TOTAL": aggregate_counts["TOTAL"],
        "role_frequency": role_counts,
    },
    "residual_adjudication": {
        "residual_claims": res_summary["residual_claims"],
        "primary_class_counts": res_summary["primary_class_counts"],
        "role_gap_claims": res_summary["role_gap_claims"],
        "conclusion": res_summary["conclusion"],
    },
    "source_context_placement": {
        "residual_claims": placements["scope"]["residual_claims"],
        "condition_nodes": placements["scope"]["residual_condition_nodes"],
        "primary_counts": placements["primary_counts"],
        "terminal": placements["terminal_classification"],
    },
    "strict_preservation_comparators": {
        "G_dyn": {
            "claims_requiring_role_beyond_XKT": gdyn["claims_requiring_at_least_one_role_beyond_G_dyn"],
            "strict_full_direct_preservation_count": gdyn["strict_full_direct_preservation_count"],
            "result": gdyn["result"],
        },
        "G_pomdp_like": {
            "claims_requiring_Pi_or_C": pomdp["claims_requiring_Pi_or_C"],
            "claims_with_both_P_directions": pomdp["interface_directionality"]["both_P_in_and_P_out"],
            "union_affected_by_missing_Pi_C_or_direction_split": pomdp["union_claims_affected_by_missing_Pi_or_C_or_collapsed_P_direction"],
            "result": pomdp["result"],
        },
        "minimality_terminal": minimality["terminal_classification"],
    },
    "architecture": {
        "layered_terminal": layered["terminal_classification"],
        "forgetful_terminal": forgetful["terminal_classification"],
        "system_world_experiment_terminal": system_world["terminal_classification"],
        "grammar_v1_authorized": minimality["conclusions"]["grammar_v1_authorized"],
    },
    "formal_identity": {
        "grammar_git_blob_sha1": grammar_blob,
    },
    "manuscript_boundaries": {
        "grammar_is_complete_claim_language": False,
        "absolute_mathematical_minimality_claimed": False,
        "world_is_grammar_v0_role": False,
        "independent_extraction_reliability_claimed": False,
        "paper3_1000_work_validation_included": False,
    },
    "terminal_classification": "PAPER2_RESULT_V1_DETERMINISTICALLY_RECONCILED",
}

require(actual == expected, "paper2_result_v1.json does not equal recomputed result")
print("PAPER2_FINAL_RESULT_AUDIT_PASS")
print(json.dumps(actual, sort_keys=True, separators=(",", ":")))
