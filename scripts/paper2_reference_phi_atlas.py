#!/usr/bin/env python3
"""Build the frozen Paper 2 reference Phi atlas from source-grounded ClaimIR.

Owner: #267. Comparison semantics remain owned by #225.
Sampling labels are attached only after pairwise Phi comparison and never enter
project_first() or compare_phi().
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from paper2_reference_structural_adjudication import compile_record
from paper2_phi_compare import compare_phi, project_first

SCHEMA_VERSION = "paper2-reference-phi-atlas-v1"
MANIFEST_VERSION = "paper2-reference-structural-manifest-v1"
SUMMARY_VERSION = "paper2-reference-phi-atlas-summary-v1"
EXPECTED_CLAIMS = 60
EXPECTED_PAIRS = EXPECTED_CLAIMS * (EXPECTED_CLAIMS - 1) // 2

PRIMARY_PREFIX_TO_STRATUM = {
    "MEM": "Memory",
    "LRN": "Learning",
    "SKL": "Skill",
    "ATT": "Attention",
    "PRD": "Prediction",
    "CTL": "Control",
    "BLF": "Belief",
    "CNC": "Concept",
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def slot_metadata(slot_id: str, source_by_slot: dict[str, Any]) -> dict[str, Any]:
    source = source_by_slot.get(slot_id, {})
    if slot_id.startswith("CH"):
        return {
            "surface": "challenge",
            "sampling_stratum": source.get("sampling_stratum"),
            "challenge_pressure": source.get("challenge_pressure"),
        }
    return {
        "surface": "primary",
        "sampling_stratum": source.get("sampling_stratum") or PRIMARY_PREFIX_TO_STRATUM.get(slot_id[:3]),
        "challenge_pressure": None,
    }


def classify_pair_meta(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    left_stratum = left.get("sampling_stratum")
    right_stratum = right.get("sampling_stratum")
    return {
        "surface_pair": "::".join(sorted([left["surface"], right["surface"]])),
        "same_sampling_stratum": (
            left["surface"] == "primary"
            and right["surface"] == "primary"
            and left_stratum is not None
            and left_stratum == right_stratum
        ),
        "cross_primary_stratum": (
            left["surface"] == "primary"
            and right["surface"] == "primary"
            and left_stratum is not None
            and right_stratum is not None
            and left_stratum != right_stratum
        ),
    }


def equivalence_components(slots: list[str], comparisons: list[dict[str, Any]]) -> list[list[str]]:
    parent = {slot: slot for slot in slots}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            if ra > rb:
                ra, rb = rb, ra
            parent[rb] = ra

    for row in comparisons:
        if row["comparison"]["relation"] == "EQUIVALENT":
            union(row["left"], row["right"])

    groups: dict[str, list[str]] = defaultdict(list)
    for slot in slots:
        groups[find(slot)].append(slot)
    return sorted(
        [sorted(group) for group in groups.values() if len(group) > 1],
        key=lambda group: (len(group), group),
    )


def build(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    source_manifest = load_json(args.source_manifest)
    source_by_slot = {row["slot_id"]: row for row in source_manifest["entries"]}

    pattern = f"{args.slot_prefix}[0-9][0-9].json" if args.slot_prefix else "[A-Z]*.json"
    adjudication_paths = sorted(args.adjudication_dir.glob(pattern))
    expected_claims = args.expected_claims if args.expected_claims is not None else EXPECTED_CLAIMS
    expected_pairs = expected_claims * (expected_claims - 1) // 2
    if len(adjudication_paths) != expected_claims:
        raise SystemExit(f"expected {expected_claims} adjudications, found {len(adjudication_paths)}")

    entries: list[dict[str, Any]] = []
    phi_by_slot: dict[str, dict[str, Any]] = {}
    metadata_by_slot: dict[str, dict[str, Any]] = {}

    for adjudication_path in adjudication_paths:
        slot_id = adjudication_path.stem
        claim_path = args.claim_dir / f"{slot_id}.json"
        if not claim_path.is_file():
            raise SystemExit(f"missing ClaimIR for {slot_id}")

        claim = load_json(claim_path)
        adjudication = load_json(adjudication_path)
        structural = compile_record(claim, adjudication)
        phi = project_first(structural)
        meta = slot_metadata(slot_id, source_by_slot)
        metadata_by_slot[slot_id] = meta
        phi_by_slot[slot_id] = phi

        attempt = structural["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
        entries.append({
            "slot_id": slot_id,
            "claim_id": claim["claim_id"],
            "source_identity": claim["provenance"]["paper_id"],
            **meta,
            "decision": attempt["outcome"]["status"],
            "active_axes": phi["active_axes"],
            "claim_ir_sha256": digest(claim),
            "adjudication_sha256": digest(adjudication),
            "structural_sha256": digest(structural),
            "phi_sha256": digest(phi),
        })

    comparisons: list[dict[str, Any]] = []
    relation_counts: Counter[str] = Counter()
    relation_by_scope: dict[str, Counter[str]] = defaultdict(Counter)
    cross_primary_structural_matches: list[dict[str, Any]] = []

    slots = sorted(phi_by_slot)
    for left, right in itertools.combinations(slots, 2):
        comparison = compare_phi(phi_by_slot[left], phi_by_slot[right])
        relation = comparison["relation"]
        relation_counts[relation] += 1

        pair_meta = classify_pair_meta(metadata_by_slot[left], metadata_by_slot[right])
        for key, enabled in pair_meta.items():
            if isinstance(enabled, bool) and enabled:
                relation_by_scope[key][relation] += 1
        relation_by_scope[pair_meta["surface_pair"]][relation] += 1

        row = {
            "left": left,
            "right": right,
            **pair_meta,
            "comparison": comparison,
        }
        comparisons.append(row)

        if pair_meta["cross_primary_stratum"] and relation != "INCOMPARABLE":
            cross_primary_structural_matches.append({
                "left": left,
                "right": right,
                "left_sampling_stratum": metadata_by_slot[left]["sampling_stratum"],
                "right_sampling_stratum": metadata_by_slot[right]["sampling_stratum"],
                "relation": relation,
            })

    if len(comparisons) != expected_pairs:
        raise SystemExit(f"expected {expected_pairs} pairs, found {len(comparisons)}")

    components = equivalence_components(slots, comparisons)
    manifest = {
        "schema_version": MANIFEST_VERSION,
        "claim_count": len(entries),
        "pair_count": len(comparisons),
        "entries": entries,
    }
    atlas = {
        "schema_version": SCHEMA_VERSION,
        "comparison_version": "paper2-phi-comparison-v1",
        "basis_version": "paper2-working-basis-v1",
        "claim_count": len(entries),
        "pair_count": len(comparisons),
        "comparisons": comparisons,
    }
    summary = {
        "schema_version": SUMMARY_VERSION,
        "claim_count": len(entries),
        "pair_count": len(comparisons),
        "decision_counts": dict(sorted(Counter(row["decision"] for row in entries).items())),
        "relation_counts": dict(sorted(relation_counts.items())),
        "relation_counts_by_scope": {
            scope: dict(sorted(counts.items())) for scope, counts in sorted(relation_by_scope.items())
        },
        "equivalence_components": components,
        "cross_primary_stratum_nonincomparable": cross_primary_structural_matches,
        "manifest_sha256": digest(manifest),
        "atlas_sha256": digest(atlas),
    }
    return manifest, atlas, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim-dir", type=Path, required=True)
    parser.add_argument("--adjudication-dir", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path, required=True)
    parser.add_argument("--atlas-output", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--slot-prefix", type=str)
    parser.add_argument("--expected-claims", type=int)
    args = parser.parse_args()

    manifest, atlas, summary = build(args)
    write_json(args.manifest_output, manifest)
    write_json(args.atlas_output, atlas)
    write_json(args.summary_output, summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
