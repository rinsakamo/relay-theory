#!/usr/bin/env python3
"""Validate the pre-mapping PVS-16 admission lock for Paper 2 JGPS #365.

The validator derives the expected 16 admissions only from the frozen
180-source ledger and the activated 60-source manifest. It does not inspect
Grammar mappings or create ClaimIR.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

LEDGER = Path("research/paper2/designed_source_candidate_ledger_v1.json")
ACTIVE = Path("research/paper2/designed_source_manifest_v1.json")
ADMISSION = Path("paper/validation/jgps-major-revision/pvs16-admission-v1.json")

EXPECTED_LEDGER_SHA256 = "7e6ce72363251c312f2eeb72a4b52900f0158db535e47844e7a39254de55c194"
EXPECTED_ACTIVE_SHA256 = "e37ef0bf9d8a7499daddac5112b31e8fd52fb9ab727c468faa1ad337bbcd2409"

LANES = (
    ("Memory", "MEM"),
    ("Learning", "LRN"),
    ("Skill", "SKL"),
    ("Attention", "ATT"),
    ("Prediction", "PRD"),
    ("Control", "CTL"),
    ("Belief", "BLF"),
    ("Concept", "CNC"),
)


class AdmissionError(ValueError):
    pass


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _identity(identity: dict[str, Any]) -> tuple[str, str]:
    kind = identity["kind"]
    value = str(identity["value"]).strip()
    if kind == "DOI":
        value = value.casefold().removeprefix("https://doi.org/").removeprefix("doi:")
    return kind, value


def expected_admissions() -> list[dict[str, Any]]:
    if _sha(LEDGER) != EXPECTED_LEDGER_SHA256:
        raise AdmissionError("candidate ledger digest drift")
    if _sha(ACTIVE) != EXPECTED_ACTIVE_SHA256:
        raise AdmissionError("activated manifest digest drift")

    ledger = _load(LEDGER)
    active = _load(ACTIVE)

    if ledger.get("state") != "CANDIDATE_LEDGER_FROZEN":
        raise AdmissionError("candidate ledger not frozen")
    if ledger.get("selection_outcome_blind") is not True:
        raise AdmissionError("candidate ledger lost outcome-blind flag")
    if any(
        ledger.get(k) is not False
        for k in ("claim_ir_consumed", "structural_signature_consumed", "phi_consumed")
    ):
        raise AdmissionError("candidate ledger was not frozen pre-ClaimIR/Phi")

    used = {_identity(row["stable_identity"]) for row in active["entries"]}
    if len(used) != 60:
        raise AdmissionError("activated source identity count is not 60")

    out: list[dict[str, Any]] = []
    for lane, code in LANES:
        admitted = 0
        for index, row in enumerate(ledger["records"]):
            if admitted == 2:
                break
            if row["surface"] != "primary":
                continue
            if row["sampling_stratum"] != lane:
                continue
            if row["candidate_state"] != "CANDIDATE":
                continue
            if _identity(row["stable_identity"]) in used:
                continue
            if row["source_access_class"] == "INACCESS" or row["read_status"] == "NOT_READ":
                continue

            admitted += 1
            out.append({
                "validation_claim_id": f"PVS-{code}-{admitted:02d}",
                "lane": lane,
                "source_identity": row["stable_identity"],
                "doi_or_stable_locator": row["canonical_locator"],
                "title": row["title"],
                "year": row["year"],
                "preexisting_selection_rank_or_provenance": {
                    "ledger_path": str(LEDGER),
                    "ledger_record_index_zero_based": index,
                    "slot_id": row["slot_id"],
                    "candidate_rank": row["candidate_rank"],
                    "selection_order": (
                        "frozen ledger record order validated by "
                        "paper2_designed_source_candidate_ledger_validate.py"
                    ),
                },
                "eligibility_basis": {
                    "candidate_state": row["candidate_state"],
                    "source_access_class": row["source_access_class"],
                    "read_status": row["read_status"],
                    "unused_in_activated_60_manifest": True,
                    "surface": row["surface"],
                },
                "grammar_mapping_inspected": False,
            })
        if admitted != 2:
            raise AdmissionError(f"{lane}: could not admit two frozen unused candidates")
    return out


def validate() -> str:
    doc = _load(ADMISSION)
    expected = expected_admissions()

    if doc.get("schema") != "relay-theory.paper2.pvs16_admission.v1":
        raise AdmissionError("schema mismatch")
    if doc.get("status") != "FROZEN_PRE_MAPPING_ADMISSION":
        raise AdmissionError("status mismatch")
    if doc.get("authority_issue") != 365:
        raise AdmissionError("authority issue mismatch")
    if doc["selection_authority"]["candidate_ledger_sha256"] != EXPECTED_LEDGER_SHA256:
        raise AdmissionError("ledger authority mismatch")
    if doc["selection_authority"]["activated_manifest_sha256"] != EXPECTED_ACTIVE_SHA256:
        raise AdmissionError("active manifest authority mismatch")
    if doc["selection_authority"]["candidate_ledger_record_order_is_validator_bound"] is not True:
        raise AdmissionError("record-order authority missing")

    scope = doc["scope"]
    if scope != {
        "actual_claim_count": 16,
        "claim_ir_created_for_pvs": False,
        "claims_per_lane": 2,
        "mapping_started": False,
        "target_claim_count": 16,
        "validation_set_id": "PVS-16",
    }:
        raise AdmissionError("scope/pre-mapping lock mismatch")

    if doc.get("admissions") != expected:
        raise AdmissionError("checked-in admissions differ from mechanically derived PVS-16")

    if len({_identity(x["source_identity"]) for x in expected}) != 16:
        raise AdmissionError("duplicate source identity in PVS-16")
    if any(x["grammar_mapping_inspected"] is not False for x in expected):
        raise AdmissionError("mapping-inspected flag is not uniformly false")

    guardrails = doc["guardrails"]
    if not all(guardrails.values()):
        raise AdmissionError("one or more post-admission guardrails disabled")

    if doc.get("terminal") != "PVS16_ADMISSION_FROZEN_BEFORE_GRAMMAR_MAPPING":
        raise AdmissionError("terminal mismatch")

    return _sha(ADMISSION)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-sha", type=Path)
    args = parser.parse_args()

    digest = validate()
    if args.emit_sha:
        args.emit_sha.write_text(
            f"{digest}  {ADMISSION.as_posix()}\n",
            encoding="utf-8",
        )
    print(f"PVS16_MANIFEST_SHA256={digest}")
    print("PVS16_ADMISSION_VALIDATED_BEFORE_GRAMMAR_MAPPING")


if __name__ == "__main__":
    main()
