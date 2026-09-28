#!/usr/bin/env python3
"""Diagnostic decomposition of the frozen Paper 2 global Phi incomparability result.

Reads frozen adjudications and comparison semantics. Does not modify or relax them.
"""
from __future__ import annotations

import argparse
import collections
import itertools
import json
from pathlib import Path

from paper2_reference_structural_adjudication import compile_record
from paper2_phi_compare import (
    APPROX_STATE_KEYS,
    CONTROL_AXIS,
    TEMPORAL_STATE_KEYS,
    _find_embedding,
    _multiset_leq,
    _node_label,
    _state_leq,
    project_first,
)

PRIMARY = ("ATT", "BLF", "CNC", "CTL", "LRN", "MEM", "PRD", "SKL")


def claim_ids() -> list[str]:
    out = [f"{p}{i:02d}" for p in PRIMARY for i in range(1, 7)]
    out += [f"CH{i:02d}" for i in range(1, 13)]
    assert len(out) == 60
    return out


def load_phi(claim_dir: Path, adjudication_dir: Path, cid: str):
    claim = json.loads((claim_dir / f"{cid}.json").read_text())
    adjudication = json.loads((adjudication_dir / f"{cid}.json").read_text())
    return project_first(compile_record(claim, adjudication))


def scalar_failures(a: dict, b: dict, *, drop_claim_metadata: bool = False, drop_approx_mode: bool = False) -> list[str]:
    reasons: list[str] = []
    if not drop_claim_metadata:
        for key in ("claim_type", "modality", "scope_shape"):
            if a[key] != b[key]:
                reasons.append(key)
    if not drop_approx_mode and a["approximation"]["mode"] != b["approximation"]["mode"]:
        reasons.append("approximation.mode")

    if not set(a["active_axes"]) <= set(b["active_axes"]):
        reasons.append("active_axes")

    for key in TEMPORAL_STATE_KEYS:
        if not _state_leq(a["temporal"][key], b["temporal"][key], exact=False):
            reasons.append(f"temporal.{key}")

    for key in CONTROL_AXIS:
        if not _state_leq(a["controls"][key], b["controls"][key], exact=False):
            reasons.append(f"control.{key}")

    for key in APPROX_STATE_KEYS:
        if not _state_leq(a["approximation"][key], b["approximation"][key], exact=False):
            reasons.append(f"approximation.{key}")

    if not _multiset_leq(a["bridges"], b["bridges"]):
        reasons.append("bridges")
    return reasons


def node_label_counter(phi: dict) -> collections.Counter[str]:
    return collections.Counter(_node_label(n) for n in phi["nodes"].values())


def node_label_subset(a: dict, b: dict) -> bool:
    ca, cb = node_label_counter(a), node_label_counter(b)
    return all(cb[k] >= v for k, v in ca.items())


def profile(phi: dict) -> dict:
    return {
        "claim_type": phi["claim_type"],
        "modality": phi["modality"],
        "scope_shape": phi["scope_shape"],
        "approximation_mode": phi["approximation"]["mode"],
        "active_axes": phi["active_axes"],
        "temporal": phi["temporal"],
        "controls": phi["controls"],
        "approximation_states": {
            k: phi["approximation"][k] for k in APPROX_STATE_KEYS
        },
        "node_count": len(phi["nodes"]),
        "edge_count": len(phi["edges"]),
    }


def canon(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--claim-dir", type=Path, required=True)
    ap.add_argument("--adjudication-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    ids = claim_ids()
    phis = {cid: load_phi(args.claim_dir, args.adjudication_dir, cid) for cid in ids}

    scalar_reason_counts = collections.Counter()
    stage_counts = collections.Counter()
    pair_scalar_pass_counts = collections.Counter()
    deepest_examples: dict[str, list[dict]] = collections.defaultdict(list)
    directed_records = []

    for left, right in itertools.combinations(ids, 2):
        dir_rows = []
        for a_id, b_id in ((left, right), (right, left)):
            a, b = phis[a_id], phis[b_id]
            reasons = scalar_failures(a, b)
            if reasons:
                stage = "scalar"
                scalar_reason_counts.update(reasons)
                embeds = False
            elif len(a["nodes"]) > len(b["nodes"]):
                stage = "node_count"
                embeds = False
            elif not node_label_subset(a, b):
                stage = "node_label_multiset"
                embeds = False
            else:
                emb = _find_embedding(a, b, exact=False)
                if emb is None:
                    stage = "topology"
                    embeds = False
                else:
                    stage = "embeds"
                    embeds = True

            stage_counts[stage] += 1
            row = {
                "source": a_id,
                "target": b_id,
                "stage": stage,
                "scalar_failures": reasons,
                "source_nodes": len(a["nodes"]),
                "target_nodes": len(b["nodes"]),
                "source_edges": len(a["edges"]),
                "target_edges": len(b["edges"]),
                "embeds": embeds,
            }
            dir_rows.append(row)
            directed_records.append(row)
            if len(deepest_examples[stage]) < 20:
                deepest_examples[stage].append(row)

        scalar_pass_n = sum(r["stage"] != "scalar" for r in dir_rows)
        pair_scalar_pass_counts[f"{scalar_pass_n}_directions_scalar_pass"] += 1

    # Signature diversity.
    # Non-authoritative ablation diagnostics. These do not define alternative Phi relations;
    # they only localize which frozen scalar surfaces suppress directed comparability.
    ablation_counts = collections.Counter()
    active_axes_relation_counts = collections.Counter()
    for left, right in itertools.combinations(ids, 2):
        a, b = phis[left], phis[right]
        for x, y in ((a, b), (b, a)):
            if not scalar_failures(x, y):
                ablation_counts["frozen_scalar_pass_directed"] += 1
            if not scalar_failures(x, y, drop_claim_metadata=True):
                ablation_counts["drop_claim_metadata_scalar_pass_directed"] += 1
            if not scalar_failures(x, y, drop_claim_metadata=True, drop_approx_mode=True):
                ablation_counts["drop_claim_metadata_and_approx_mode_scalar_pass_directed"] += 1
            if set(x["active_axes"]) <= set(y["active_axes"]):
                ablation_counts["active_axes_subset_directed"] += 1

        la, ra = set(a["active_axes"]), set(b["active_axes"])
        if la == ra:
            active_axes_relation_counts["equal"] += 1
        elif la < ra or ra < la:
            active_axes_relation_counts["strict_subset_comparable"] += 1
        else:
            active_axes_relation_counts["incomparable"] += 1

    profile_counters = {}
    for name, fn in {
        "claim_type": lambda p: p["claim_type"],
        "modality": lambda p: p["modality"],
        "scope_shape": lambda p: canon(p["scope_shape"]),
        "approximation_mode": lambda p: p["approximation"]["mode"],
        "active_axes": lambda p: canon(p["active_axes"]),
        "temporal": lambda p: canon(p["temporal"]),
        "controls": lambda p: canon(p["controls"]),
        "approximation_states": lambda p: canon({k: p["approximation"][k] for k in APPROX_STATE_KEYS}),
        "node_label_multiset": lambda p: canon(sorted(node_label_counter(p).items())),
        "edge_shape_multiset": lambda p: canon(sorted(collections.Counter(
            canon({
                "family": e["family"],
                "kind": e["kind"],
                "ordered_arguments": e["ordered_arguments"],
                "arity": len(e["arguments"]),
                "conditional_arity": len(e["conditional_on"]),
                "temporal_direction": e["temporal_direction"],
                "grounding": e["grounding"],
            }) for e in p["edges"]
        ).items())),
    }.items():
        c = collections.Counter(fn(phis[cid]) for cid in ids)
        profile_counters[name] = {
            "unique_profiles": len(c),
            "largest_multiplicity": max(c.values()),
            "multiplicity_histogram": dict(sorted(collections.Counter(c.values()).items())),
        }

    # MEM close-pair diagnostic, chosen independently from the frozen comparison result
    # because these pairs were already recorded as raw-coordinate-near during qualification.
    mem_pairs = [("MEM01","MEM03"),("MEM01","MEM06"),("MEM02","MEM05"),("MEM03","MEM04"),("MEM04","MEM05")]
    mem_diag = []
    for a_id,b_id in mem_pairs:
        row = {"pair":[a_id,b_id],"directions":[]}
        for x,y in ((a_id,b_id),(b_id,a_id)):
            reasons=scalar_failures(phis[x],phis[y])
            if reasons:
                stage="scalar"
            elif len(phis[x]["nodes"])>len(phis[y]["nodes"]):
                stage="node_count"
            elif not node_label_subset(phis[x],phis[y]):
                stage="node_label_multiset"
            else:
                stage="embeds" if _find_embedding(phis[x],phis[y],exact=False) is not None else "topology"
            row["directions"].append({"source":x,"target":y,"stage":stage,"scalar_failures":reasons})
        mem_diag.append(row)

    output = {
        "schema_version": "paper2-global-incomparability-diagnostic-v1",
        "claim_count": 60,
        "unordered_pair_count": 1770,
        "directed_pair_count": 3540,
        "directed_stage_counts": dict(sorted(stage_counts.items())),
        "directed_scalar_failure_reason_counts": dict(sorted(scalar_reason_counts.items())),
        "unordered_pair_scalar_pass_direction_counts": dict(sorted(pair_scalar_pass_counts.items())),
        "profile_diversity": profile_counters,
        "non_authoritative_ablation_counts": dict(sorted(ablation_counts.items())),
        "active_axes_only_unordered_relations": dict(sorted(active_axes_relation_counts.items())),
        "deepest_examples": dict(deepest_examples),
        "mem_preidentified_raw_near_pair_diagnostic": mem_diag,
    }

    assert stage_counts["embeds"] == 0
    assert sum(stage_counts.values()) == 3540
    assert sum(pair_scalar_pass_counts.values()) == 1770

    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
