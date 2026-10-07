#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any

from paper2_phi_compare import compare_phi, project_first
from paper2_reference_structural_adjudication import compile_record
from paper2_structural_signature_canonical import structural_digest

ROOT = Path(__file__).resolve().parents[1]
CLAIM_DIR = ROOT / "research/paper2/chatgpt_reference_claimir_v1"
ADJ_DIR = ROOT / "research/paper2/reference_structural_adjudication_v1"
M14 = ROOT / "research/paper2/p399/main/integration/M14"
M15 = ROOT / "research/paper2/p399/main/integration/M15"
M16 = ROOT / "research/paper2/p399/main/integration/M16"

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def canonical_sha(value: Any) -> str:
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def nested_diff(a: Any, b: Any, path: str = "") -> list[str]:
    if type(a) is not type(b):
        return [path or "$"]
    if isinstance(a, dict):
        out: list[str] = []
        for key in sorted(set(a) | set(b)):
            p = f"{path}.{key}" if path else key
            if key not in a or key not in b:
                out.append(p)
            else:
                out.extend(nested_diff(a[key], b[key], p))
        return out
    if isinstance(a, list):
        out: list[str] = []
        if len(a) != len(b):
            out.append(path + ".length")
        for i, (x, y) in enumerate(zip(a, b)):
            out.extend(nested_diff(x, y, f"{path}[{i}]"))
        return out
    return [] if a == b else [path or "$"]

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    original_claim = load(CLAIM_DIR / "LRN03.json")
    original_adj = load(ADJ_DIR / "LRN03.json")
    corrected_claim = load(M16 / "M16_LRN03_CORRECTED_CLAIMIR_v1.json")
    corrected_adj = load(M16 / "M16_LRN03_CORRECTED_ADJUDICATION_v1.json")
    correction = load(M16 / "M16_LRN03_SOURCE_CORRECTION_v1.json")
    role_overlay = load(M16 / "M16_LRN03_ROLE_PROJECTION_SUCCESSOR_v1.json")

    # Frozen parents are not modified.
    assert original_claim["claim_id"] == "LRN03.C1"
    assert original_adj["claim_id"] == "LRN03.C1"
    assert correction["mutation_boundary"]["frozen_claimir_modified"] is False
    assert correction["mutation_boundary"]["frozen_adjudication_modified"] is False

    # Only the source-faithfulness fields identified by M15 are changed in ClaimIR.
    diffs = nested_diff(original_claim, corrected_claim)
    expected_diffs = {
        "claim_core.scope.conditions[2]",
        "claim_core.nodes[2].description",
        "claim_core.nodes[2].source_span_ids[2]",
        "claim_core.relations[2].description",
        "claim_core.relations[2].source_span_ids[2]",
    }
    assert set(diffs) == expected_diffs, diffs

    # Structural adjudication changes only successor provenance metadata.
    ad_diffs = nested_diff(original_adj, corrected_adj)
    assert set(ad_diffs) == {
        "adjudicator.procedure",
        "adjudicator.adjudicated_at",
    }, ad_diffs

    orig_record = compile_record(original_claim, original_adj)
    corr_record = compile_record(corrected_claim, corrected_adj)

    orig_attempt = orig_record["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
    corr_attempt = corr_record["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
    orig_structural_digest = structural_digest(orig_attempt, original_claim)
    corr_structural_digest = structural_digest(corr_attempt, corrected_claim)
    assert orig_structural_digest != corr_structural_digest

    orig_phi = project_first(orig_record)
    corr_phi = project_first(corr_record)
    assert orig_phi == corr_phi
    orig_phi_sha = canonical_sha(orig_phi)
    corr_phi_sha = canonical_sha(corr_phi)
    assert orig_phi_sha == corr_phi_sha

    # Compile the full 60-claim corpus and replace only LRN03 with its corrected successor.
    original_phi: dict[str, dict[str, Any]] = {}
    corrected_phi: dict[str, dict[str, Any]] = {}
    claim_files = sorted(p for p in CLAIM_DIR.glob("*.json") if p.name != "manifest.json")
    assert len(claim_files) == 60, len(claim_files)
    for claim_path in claim_files:
        stem = claim_path.stem
        adj_path = ADJ_DIR / f"{stem}.json"
        assert adj_path.is_file(), stem
        claim = load(claim_path)
        adj = load(adj_path)
        record = compile_record(claim, adj)
        cid = claim["claim_id"]
        original_phi[cid] = project_first(record)
        corrected_phi[cid] = original_phi[cid]

    corrected_phi["LRN03.C1"] = corr_phi
    assert set(original_phi) == set(corrected_phi)
    assert len(original_phi) == 60

    # Recompute the complete corrected 1,770-pair surface.
    relation_counts: Counter[str] = Counter()
    corrected_pairs: dict[str, str] = {}
    ids = sorted(corrected_phi)
    for left, right in itertools.combinations(ids, 2):
        rel = compare_phi(corrected_phi[left], corrected_phi[right])["relation"]
        relation_counts[rel] += 1
        corrected_pairs[f"{left}::{right}"] = rel
    assert sum(relation_counts.values()) == 1770

    frozen_global = load(ROOT / "research/paper2/reference_global_phi_freeze_v1.json")
    assert frozen_global["claim_count"] == 60
    assert frozen_global["pair_count"] == 1770
    assert frozen_global["relation_counts"] == {"INCOMPARABLE": 1770}
    assert dict(relation_counts) == frozen_global["relation_counts"]

    # Directly recompute every potentially affected pair in old and corrected form.
    affected_pair_changes = []
    for other in sorted(set(ids) - {"LRN03.C1"}):
        old = compare_phi(original_phi["LRN03.C1"], original_phi[other])["relation"]
        new = compare_phi(corrected_phi["LRN03.C1"], corrected_phi[other])["relation"]
        if old != new:
            affected_pair_changes.append({"other": other, "old": old, "new": new})
    assert affected_pair_changes == []

    # Bounded family sensitivity: exact Phi equality means every deterministic
    # Phi-derived subobject/membership input is identical. Report the frozen
    # bounded surface and the LRN03 support memberships for audit.
    bounded = load(ROOT / "research/paper2/bounded_xlike_reconstruction_v1.json")
    assert bounded["bounded_xlike_count"] == 206
    assert bounded["cross_lane_xlike_count"] == 99
    lrn03_xlikes = sorted(
        row["xlike_id"]
        for row in bounded["bounded_xlike_families"]
        if "LRN03" in row["member_claim_ids"]
    )

    # Grammar-v0 successor sensitivity. C remains present but is scoped to
    # Experiment 1 exact matching; therefore the role inventory/verdict remains.
    lrn = load(ROOT / "research/paper2/lrn_grammar_v0_reverse_projection_v1.json")
    lrn03 = next(row for row in lrn["claims"] if row["claim_id"] == "LRN03.C1")
    assert lrn03["verdict"] == "FULL"
    assert lrn03["grammar_roles_instantiated"] == ["C","Q","P_in","P_out","T","rho/O"]
    assert role_overlay["verdict"] == "FULL"
    assert role_overlay["grammar_roles_instantiated"] == lrn03["grammar_roles_instantiated"]
    assert role_overlay["corrected_C_mapping"]["status"] == "SUPPORTED"
    assert role_overlay["other_role_mappings_changed"] is False
    assert role_overlay["residual_changed"] is False

    reverse_agg = load(ROOT / "research/paper2/grammar_v0_reverse_projection_aggregate_v1.json")
    verdict_counts = Counter(row["verdict"] for row in reverse_agg["claim_verdicts"])
    assert verdict_counts == {"FULL": 21, "PARTIAL": 22, "RESIDUAL": 17}

    # Headline authorities remain unchanged. MAIN40 is a separate prospective
    # denominator and does not contain this designed-corpus ClaimIR.
    m14 = load(M14 / "M14_SPEC_v1.json")
    imm = m14["immutable_scientific_results"]
    assert imm["whole_claim"] == "1770/1770 INCOMPARABLE"
    assert imm["bounded_objects"] == 206
    assert imm["cross_stratum_families"] == 99
    assert imm["reverse_projection"] == "21 FULL / 22 PARTIAL / 17 RESIDUAL"
    assert imm["residual_new_top_level_role"] == "0/17"
    assert imm["prospective_MAIN40"] == "40/40 A0"

    # M15 result remains historical and is never post-hoc rescored.
    m15 = load(M15 / "M15_COMPARISON_RESULTS_v1.json")
    assert m15["aggregate"]["astra_vs_retained"]["primary_compatible_fraction"] == "9/10"
    assert m15["aggregate"]["sol_vs_retained"]["primary_compatible_fraction"] == "9/10"

    result = {
        "schema": "relaytheory.p399.main.m16.lrn03_source_correction_sensitivity_result.v1",
        "status": "COMPLETE",
        "correction": {
            "claim_id": "LRN03.C1",
            "original_claimir_sha256": file_sha(CLAIM_DIR / "LRN03.json"),
            "corrected_claimir_sha256": file_sha(M16 / "M16_LRN03_CORRECTED_CLAIMIR_v1.json"),
            "original_adjudication_sha256": file_sha(ADJ_DIR / "LRN03.json"),
            "corrected_adjudication_sha256": file_sha(M16 / "M16_LRN03_CORRECTED_ADJUDICATION_v1.json"),
            "claimir_changed_paths": diffs,
            "adjudication_changed_paths": ad_diffs,
        },
        "structural_sensitivity": {
            "canonical_semantic_structural_digest_original": orig_structural_digest,
            "canonical_semantic_structural_digest_corrected": corr_structural_digest,
            "canonical_semantic_structural_digest_changed": True,
            "phi_sha256_original": orig_phi_sha,
            "phi_sha256_corrected": corr_phi_sha,
            "phi_exactly_equal": True,
            "interpretation": "The source-faithfulness correction changes ClaimIR semantic/provenance detail but lies below the frozen Phi comparison granularity."
        },
        "whole_claim_recalculation": {
            "claims": 60,
            "pairs": 1770,
            "corrected_relation_counts": dict(sorted(relation_counts.items())),
            "affected_lrn03_pair_count": 59,
            "affected_pair_relation_changes": affected_pair_changes,
            "matrix_relation_change_count": 0,
            "terminal": "1770/1770 INCOMPARABLE unchanged"
        },
        "bounded_sensitivity": {
            "reason_for_invariance": "corrected LRN03 Phi is exactly identical to frozen LRN03 Phi",
            "bounded_xlike_count": bounded["bounded_xlike_count"],
            "cross_lane_xlike_count": bounded["cross_lane_xlike_count"],
            "lrn03_xlike_membership_count": len(lrn03_xlikes),
            "lrn03_xlike_ids": lrn03_xlikes,
            "membership_change_count": 0,
            "count_change": False
        },
        "reverse_projection_sensitivity": {
            "lrn03_verdict_before": lrn03["verdict"],
            "lrn03_verdict_after": role_overlay["verdict"],
            "roles_before": lrn03["grammar_roles_instantiated"],
            "roles_after": role_overlay["grammar_roles_instantiated"],
            "C_scope_after": role_overlay["corrected_C_mapping"]["scope"],
            "aggregate_counts_after": dict(sorted(verdict_counts.items())),
            "verdict_changed": False,
            "role_inventory_changed": False
        },
        "headline_results": {
            "whole_claim": "1770/1770 INCOMPARABLE",
            "bounded_objects": 206,
            "cross_stratum_families": 99,
            "reverse_projection": "21 FULL / 22 PARTIAL / 17 RESIDUAL",
            "residual_new_top_level_role": "0/17",
            "prospective_MAIN40": "40/40 A0",
            "material_change": False
        },
        "validation_boundary": {
            "m15_historical_result_rescored": False,
            "m15_primary_result_remains": "9/10 compatible for Astra and 9/10 compatible for Sol under the frozen M15 scoring",
            "independent_human_validation": "NOT_PERFORMED",
            "human_inter_rater_reliability": "UNMEASURED"
        },
        "terminal_state": "M16_LRN03_CORRECTION_STRUCTURALLY_INVARIANT"
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("M16_LRN03_SOURCE_CORRECTION_SENSITIVITY_PASS")
    print(json.dumps(result["whole_claim_recalculation"], sort_keys=True))

if __name__ == "__main__":
    main()
