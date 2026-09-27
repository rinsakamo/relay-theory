#!/usr/bin/env python3
"""Validate Paper 2 web-fulltext reconciliation manifest v1.

Owner: #243. This validator binds each reconciled slot to the frozen #231
candidate ladder and proves that accessibility replacement is rank-preserving,
pre-ClaimIR, and complete for all 60 designed slots.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "paper2-web-fulltext-reconciliation-v1"
GEOMETRY_VERSION = "paper2-designed-corpus-geometry-v1"
LEDGER_VERSION = "paper2-designed-source-candidate-ledger-v1"
LEDGER_SHA256 = "7e6ce72363251c312f2eeb72a4b52900f0158db535e47844e7a39254de55c194"
ACCESS_GATE_HEAD = "5f7398c54c3089d5938adff6515e12d50f617911"
STATE = "WEB_FULLTEXT_60_SOURCE_MANIFEST_FROZEN"
PASS = {"PASS_FULL_TEXT", "PASS_FULL_TEXT_PDF"}
FAIL = {"FAIL_ABSTRACT_ONLY", "FAIL_PARTIAL", "FAIL_PAYWALL", "FAIL_NOT_FOUND"}
AUDIT_COMMENT_IDS = [
    5853001063, 5853633002, 5853637674, 5853652409, 5853667229,
    5853682554, 5853697500, 5853706329, 5853746961,
]

class ValidationError(ValueError):
    pass

def fail(message: str) -> None:
    raise ValidationError(message)

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def canonical_identity(identity: dict[str, Any]) -> tuple[str, str]:
    if not isinstance(identity, dict) or set(identity) != {"kind", "value"}:
        fail("malformed stable identity")
    kind = identity["kind"]
    value = str(identity["value"]).strip()
    if kind == "DOI":
        value = value.casefold().removeprefix("https://doi.org/").removeprefix("doi:")
    else:
        value = value.casefold()
    if not value:
        fail("empty stable identity")
    return kind, value

def slot_order(geometry: dict[str, Any]) -> list[tuple[str, str, str | None, str | None]]:
    out = []
    for row in geometry["primary"]["slots"]:
        out.append((row["slot_id"], "primary", row["sampling_stratum"], None))
    for row in geometry["challenge"]["slots"]:
        out.append((row["slot_id"], "challenge", None, row["pressure"]))
    return out

def ledger_index(ledger: dict[str, Any]) -> dict[tuple[str, int], dict[str, Any]]:
    if ledger.get("schema_version") != LEDGER_VERSION:
        fail("ledger version drift")
    rows = ledger.get("records")
    if not isinstance(rows, list) or len(rows) != 180:
        fail("ledger must contain 180 candidates")
    out = {}
    for row in rows:
        key = (row["slot_id"], row["candidate_rank"])
        if key in out:
            fail(f"duplicate ledger position {key}")
        out[key] = row
    return out

def computed_summary(entries: list[dict[str, Any]]) -> dict[str, Any]:
    ranks = {"1": 0, "2": 0, "3": 0}
    for row in entries:
        ranks[str(row["activated_rank"])] += 1
    return {
        "slots": len(entries),
        "primary": sum(row["surface"] == "primary" for row in entries),
        "challenge": sum(row["surface"] == "challenge" for row in entries),
        "rank_counts": ranks,
        "accessibility_substitutions": sum(row["activated_rank"] > 1 for row in entries),
        "terminal_inaccessible": 0,
    }

def validate(data: Any, ledger: dict[str, Any], geometry: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        fail("manifest root must be object")
    required = {
        "schema_version", "owner_issue", "parent_mapping_issue", "geometry_version",
        "candidate_ledger_version", "candidate_ledger_sha256", "access_gate_merge_head",
        "state", "accessed_on", "audit_comment_ids", "access_policy",
        "selection_outcome_blind", "claim_ir_consumed", "structural_signature_consumed",
        "phi_consumed", "atlas_outcome_consumed", "model_calls_consumed", "summary", "entries",
    }
    if set(data) != required:
        fail(f"manifest root keys drift: {sorted(set(data) ^ required)}")
    if data["schema_version"] != SCHEMA_VERSION:
        fail("schema version drift")
    if data["owner_issue"] != 243 or data["parent_mapping_issue"] != 239:
        fail("owner binding drift")
    if data["geometry_version"] != GEOMETRY_VERSION:
        fail("geometry version drift")
    if data["candidate_ledger_version"] != LEDGER_VERSION:
        fail("candidate ledger version drift")
    if data["candidate_ledger_sha256"] != LEDGER_SHA256:
        fail("candidate ledger digest drift")
    if data["access_gate_merge_head"] != ACCESS_GATE_HEAD:
        fail("access gate head drift")
    if data["state"] != STATE:
        fail("manifest state drift")
    if data["accessed_on"] != "2026-09-27":
        fail("audit date drift")
    if data["audit_comment_ids"] != AUDIT_COMMENT_IDS:
        fail("audit comment provenance drift")
    if data["selection_outcome_blind"] is not True:
        fail("selection outcome blindness must remain true")
    if any(data[k] for k in (
        "claim_ir_consumed", "structural_signature_consumed",
        "phi_consumed", "atlas_outcome_consumed",
    )):
        fail("web-fulltext reconciliation must remain pre-outcome")
    if data["model_calls_consumed"] != 0:
        fail("web-fulltext reconciliation must consume zero model calls")

    policy = data["access_policy"]
    if policy != {
        "complete_public_web_full_text_required": True,
        "accepted_surfaces": [
            "PUBLIC_HTML_FULL_TEXT",
            "PUBLIC_DOWNLOADABLE_COMPLETE_PDF",
            "PUBLIC_AUTHOR_UPLOADED_COMPLETE_COPY",
        ],
        "rejected_surfaces": [
            "ABSTRACT_ONLY",
            "METADATA_ONLY",
            "PREVIEW_OR_PARTIAL",
            "PAYWALL_OR_INSTITUTIONAL_LOGIN",
            "PURCHASE_ONLY",
            "REQUEST_A_COPY_ONLY",
        ],
        "rank_order": [1, 2, 3],
        "rank4_forbidden": True,
        "result_dependent_replacement_forbidden": True,
    }:
        fail("access policy drift")

    expected = slot_order(geometry)
    entries = data["entries"]
    if not isinstance(entries, list) or len(entries) != 60:
        fail("entries must contain exactly 60 slots")
    idx = ledger_index(ledger)
    seen_identities: set[tuple[str, str]] = set()

    for i, (entry, expected_slot) in enumerate(zip(entries, expected)):
        if not isinstance(entry, dict):
            fail(f"entries[{i}] must be object")
        slot, surface, stratum, pressure = expected_slot
        if (
            entry.get("slot_id") != slot
            or entry.get("surface") != surface
            or entry.get("sampling_stratum") != stratum
            or entry.get("challenge_pressure") != pressure
        ):
            fail(f"{slot}: geometry/order drift")
        rank = entry.get("activated_rank")
        if rank not in {1, 2, 3}:
            fail(f"{slot}: invalid activated rank")
        candidate = idx.get((slot, rank))
        if candidate is None:
            fail(f"{slot}: activated candidate absent from frozen ledger")
        for key in ("stable_identity", "title", "year", "source_type", "registry_reference", "author_lineage_key"):
            if entry.get(key) != candidate.get(key):
                fail(f"{slot}: selected candidate {key} drift")
        ident = canonical_identity(entry["stable_identity"])
        if ident in seen_identities:
            fail(f"{slot}: duplicate selected stable identity")
        seen_identities.add(ident)

        expected_outcome = (
            "ACTIVATED_RANK_1_WEB_FULLTEXT"
            if rank == 1
            else f"ACTIVATED_RANK_{rank}_AFTER_ACCESS_FAILURE"
        )
        if entry.get("activation_outcome") != expected_outcome:
            fail(f"{slot}: activation outcome drift")
        expected_reason = None if rank == 1 else "PUBLIC_WEB_FULLTEXT_ACCESS_FAILURE_AT_HIGHER_RANKS"
        if entry.get("replacement_reason") != expected_reason:
            fail(f"{slot}: replacement reason drift")
        if entry.get("capture_access_class") != "FULL_TEXT":
            fail(f"{slot}: selected source must be FULL_TEXT")
        if entry.get("public_fulltext_verdict") not in PASS:
            fail(f"{slot}: selected source lacks PASS verdict")
        locator = entry.get("public_fulltext_locator")
        if not isinstance(locator, str) or not locator.startswith(("http://", "https://")):
            fail(f"{slot}: public full-text locator required")
        if entry.get("accessed_on") != "2026-09-27":
            fail(f"{slot}: access date drift")

        attempts = entry.get("access_attempts")
        if not isinstance(attempts, list) or len(attempts) != rank:
            fail(f"{slot}: attempts must be contiguous rank1..activated_rank")
        for j, attempt in enumerate(attempts, start=1):
            if attempt.get("candidate_rank") != j:
                fail(f"{slot}: rank traversal skipped or reordered")
            cand_j = idx.get((slot, j))
            if cand_j is None:
                fail(f"{slot}: attempt candidate absent from frozen ledger")
            if attempt.get("stable_identity") != cand_j.get("stable_identity"):
                fail(f"{slot}: attempt identity drift at rank {j}")
            if attempt.get("title") != cand_j.get("title"):
                fail(f"{slot}: attempt title drift at rank {j}")
            if attempt.get("audit_comment_id") not in AUDIT_COMMENT_IDS:
                fail(f"{slot}: attempt audit provenance drift")
            verdict = attempt.get("verdict")
            if j < rank and verdict not in FAIL:
                fail(f"{slot}: earlier rank must fail the frozen accessibility gate")
            if j == rank and verdict not in PASS:
                fail(f"{slot}: activated rank must PASS")
            note = attempt.get("evidence_note")
            if not isinstance(note, str) or not note.strip():
                fail(f"{slot}: evidence note required")

    if len(seen_identities) != 60:
        fail("selected surface must contain 60 unique identities")
    summary = computed_summary(entries)
    if data["summary"] != summary:
        fail(f"summary drift: {data['summary']} != {summary}")
    if summary != {
        "slots": 60,
        "primary": 48,
        "challenge": 12,
        "rank_counts": {"1": 55, "2": 4, "3": 1},
        "accessibility_substitutions": 5,
        "terminal_inaccessible": 0,
    }:
        fail("terminal reconciliation counts drift")
    return data

def expect_invalid(data: dict[str, Any], ledger: dict[str, Any], geometry: dict[str, Any], label: str) -> None:
    try:
        validate(data, ledger, geometry)
    except ValidationError:
        return
    raise AssertionError(f"{label}: unexpectedly validated")

def self_test(base: dict[str, Any], ledger: dict[str, Any], geometry: dict[str, Any]) -> None:
    validate(base, ledger, geometry)

    x = copy.deepcopy(base)
    x["entries"].pop()
    expect_invalid(x, ledger, geometry, "missing slot")

    x = copy.deepcopy(base)
    row = next(r for r in x["entries"] if r["slot_id"] == "PRD06")
    row["access_attempts"].pop(0)
    expect_invalid(x, ledger, geometry, "skipped frozen rank")

    x = copy.deepcopy(base)
    row = next(r for r in x["entries"] if r["slot_id"] == "BLF05")
    row["access_attempts"][0]["verdict"] = "PASS_FULL_TEXT"
    expect_invalid(x, ledger, geometry, "earlier rank passed but was skipped")

    x = copy.deepcopy(base)
    x["entries"][0]["stable_identity"] = {"kind": "DOI", "value": "10.0000/drift"}
    expect_invalid(x, ledger, geometry, "selected identity drift")

    x = copy.deepcopy(base)
    x["entries"][0]["public_fulltext_locator"] = ""
    expect_invalid(x, ledger, geometry, "missing public locator")

    x = copy.deepcopy(base)
    x["claim_ir_consumed"] = True
    expect_invalid(x, ledger, geometry, "ClaimIR leak")

    x = copy.deepcopy(base)
    x["summary"]["accessibility_substitutions"] = 4
    expect_invalid(x, ledger, geometry, "summary drift")

    print("PAPER2_WEB_FULLTEXT_RECONCILIATION_V1_SELFTEST_PASS")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("research/paper2/designed_source_web_fulltext_manifest_v1.json"),
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        default=Path("research/paper2/designed_source_candidate_ledger_v1.json"),
    )
    parser.add_argument(
        "--geometry",
        type=Path,
        default=Path("research/paper2/designed_corpus_geometry_v1.json"),
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    data, ledger, geometry = load(args.manifest), load(args.ledger), load(args.geometry)
    validate(data, ledger, geometry)
    if args.self_test:
        self_test(data, ledger, geometry)
    else:
        print("PAPER2_WEB_FULLTEXT_RECONCILIATION_V1_VALID")

if __name__ == "__main__":
    main()
