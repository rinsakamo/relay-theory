#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HV = ROOT / "research/paper2/p399/main/integration/M12/human_validation"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def strict_claim(case: dict) -> dict:
    core = case["claim_core"]
    return {
        "schema": "relaytheory.p399.main.m12.strict_blind_claim_case.v1",
        "case_id": case["case_id"],
        "masking": {
            "original_slot_withheld": True,
            "doi_withheld": True,
            "authors_withheld": True,
            "venue_withheld": True,
            "construct_labels_withheld": True,
            "source_locator_identity_withheld": True,
            "normalized_node_roles_withheld": True,
            "normalized_relation_kinds_withheld": True,
            "conceptual_blindness_established": False,
            "note": (
                "Strict downstream re-adjudication surface. Scientific descriptions remain, "
                "so topic identity may still be inferable; this is not independent source extraction."
            ),
        },
        "source_span_aliases": [{"span_id": x["span_id"]} for x in case.get("source_spans", [])],
        "claim_record": {
            "claim_type": core.get("claim_type"),
            "modality": core.get("modality"),
            "scope": core.get("scope"),
            "nodes": [
                {
                    "id": n.get("id"),
                    "description": n.get("description"),
                    "source_span_ids": n.get("source_span_ids", []),
                }
                for n in core.get("nodes", [])
            ],
            "relations": [
                {
                    "id": r.get("id"),
                    "arguments": r.get("arguments", []),
                    "description": r.get("description"),
                    "source_span_ids": r.get("source_span_ids", []),
                }
                for r in core.get("relations", [])
            ],
        },
        "candidate_bounded_objects": case["candidate_bounded_objects"],
        "coder_tasks": case["coder_tasks"],
    }


def drop_identity(obj):
    if isinstance(obj, list):
        return [drop_identity(x) for x in obj]
    if not isinstance(obj, dict):
        return obj
    blocked = {
        "slot",
        "doi",
        "source_authority_lock_commit",
        "source_lock",
        "lane_head",
        "lane_pr",
        "architectural_outcome_blob",
    }
    out = {}
    for k, v in obj.items():
        if k in blocked:
            continue
        out[k] = drop_identity(v)
    return out


def strict_prospective(case: dict) -> dict:
    return {
        "schema": "relaytheory.p399.main.m12.strict_blind_prospective_case.v1",
        "case_id": case["case_id"],
        "masking": {
            "paper_id_withheld": True,
            "doi_withheld": True,
            "corpus_arm_withheld": True,
            "repository_path_withheld": True,
            "lane_head_withheld": True,
            "architectural_outcome_withheld": True,
            "conceptual_blindness_established": False,
            "note": (
                "Identity metadata is removed, but native model content can reveal topic or lineage. "
                "Do not inspect repository answer artifacts before coding."
            ),
        },
        "source_first_decomposition": drop_identity(case["source_first_artifact"]),
        "decision_rule": case["decision_rule"],
        "coder_tasks": case["coder_tasks"],
    }


def assert_strict_claim(obj):
    text = json.dumps(obj)
    assert '"doi"' not in text
    assert '"authors"' not in text
    assert '"venue"' not in text
    assert '"construct_labels"' not in text
    assert '"role"' not in json.dumps(obj["claim_record"]["nodes"])
    assert '"kind"' not in json.dumps(obj["claim_record"]["relations"])
    assert "locator" not in json.dumps(obj["source_span_aliases"])


def _all_keys(obj):
    if isinstance(obj, list):
        out = set()
        for x in obj:
            out |= _all_keys(x)
        return out
    if isinstance(obj, dict):
        out = set(obj)
        for v in obj.values():
            out |= _all_keys(v)
        return out
    return set()


def assert_strict_prospective(obj):
    keys = _all_keys(obj)
    for forbidden in {
        "doi",
        "slot",
        "source_first_artifact_path",
        "source_first_lane_head",
        "architectural_outcome",
        "architectural_outcome_blob",
        "lane_head",
        "lane_pr",
    }:
        assert forbidden not in keys, forbidden


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    (out / "claims").mkdir(parents=True)
    (out / "prospective").mkdir(parents=True)

    claim_files = sorted((HV / "claim_packets").glob("HC*.json"))
    pro_files = sorted((HV / "prospective_packets").glob("HP*.json"))
    assert len(claim_files) == 20
    assert len(pro_files) == 10

    for p in claim_files:
        obj = strict_claim(load(p))
        assert_strict_claim(obj)
        dump(out / "claims" / p.name, obj)

    for p in pro_files:
        obj = strict_prospective(load(p))
        assert_strict_prospective(obj)
        dump(out / "prospective" / p.name, obj)

    shutil.copy2(HV / "M12_HUMAN_CLAIM_CODER_FORM_v1.csv", out / "M12_HUMAN_CLAIM_CODER_FORM_v1.csv")
    shutil.copy2(HV / "M12_HUMAN_PROSPECTIVE_CODER_FORM_v1.csv", out / "M12_HUMAN_PROSPECTIVE_CODER_FORM_v1.csv")

    readme = """# M12 strict blind export

Use this directory for coder distribution. Do not distribute the repository reference-key files or the unredacted coordinator materials.

Claims: 20 metadata-masked structured-record cases. Original normalized node-role labels, relation-kind labels, source identity locators, DOI, authors, venue, and historical construct labels are withheld. This tests downstream structural re-adjudication after source extraction; it is not an independent extraction study.

Prospective: 10 source-first decomposition cases with paper ID, DOI, corpus arm, repository path, lane head, and architectural outcome withheld.

Because scientific prose can itself reveal a topic, this is procedural/metadata blindness rather than guaranteed conceptual blindness. Independent human re-adjudication remains NOT PERFORMED until completed forms are returned by a genuinely independent human.
"""
    (out / "README.md").write_text(readme, encoding="utf-8")
    print(f"M12_STRICT_BLIND_EXPORT_PASS claims={len(claim_files)} prospective={len(pro_files)} out={out}")


if __name__ == "__main__":
    main()
