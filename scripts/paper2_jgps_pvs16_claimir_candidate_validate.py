#!/usr/bin/env python3
"""Validate pre-mapping PVS-16 ClaimIR candidates for JGPS validation #365.

This gate validates only source-grounded ClaimIR structure and admission
identity. It explicitly forbids Grammar-v0 / Archetype / residual outcome
information and requires the records to remain UNREVIEWED until the author
reviews them.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from paper2_claim_ir_validate import validate as validate_claim_ir, blinded_bytes

ROOT = Path("paper/validation/jgps-major-revision")
ADMISSION = ROOT / "pvs16-admission-v1.json"
ADMISSION_SHA = ROOT / "pvs16-admission-v1.sha256"
SOURCE_AUTH = ROOT / "pvs16-source-authority-v1.json"
MANIFEST = ROOT / "pvs16-claimir-candidate-manifest-v1.json"
CANDIDATES = ROOT / "pvs16-claimir-candidates-v1"
EXPECTED_ADMISSION_SHA = "0a4454887189730cf4b13d12061f4cab93fb8e4d8f0ec089a08f77bc088dc123"
PROCEDURE = "jgps-pvs16-source-grounded-candidate-v1:#365"

FORBIDDEN_DOWNSTREAM = (
    "grammar v0", "grammar_v0", "role_gap", "archetype", "p_in", "p_out",
    "rho/o", "basis_mapping", "basis_elements", "decomposition_success",
    "decomposition_failure", "residual_type", "acceptance_verdict",
)

class Error(ValueError):
    pass

def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def norm_doi(value: str) -> str:
    v=value.strip().lower()
    for prefix in ("https://doi.org/","doi:"):
        if v.startswith(prefix):
            v=v[len(prefix):]
    return v

def validate_all() -> dict[str, Any]:
    if sha(ADMISSION) != EXPECTED_ADMISSION_SHA:
        raise Error("PVS admission digest drift")
    sidecar = ADMISSION_SHA.read_text(encoding="utf-8").split()[0]
    if sidecar != EXPECTED_ADMISSION_SHA:
        raise Error("PVS admission sidecar drift")

    admission=load(ADMISSION)
    source=load(SOURCE_AUTH)
    manifest=load(MANIFEST)

    if admission["scope"]["mapping_started"] is not False:
        raise Error("admission already marks mapping started")
    if source["grammar_mapping_authorized"] is not False:
        raise Error("source authority unexpectedly authorizes Grammar mapping")
    if manifest["grammar_mapping_started"] is not False:
        raise Error("candidate manifest unexpectedly marks mapping started")
    if manifest["review_state"] != "unreviewed":
        raise Error("candidate manifest review state must remain unreviewed")
    if manifest["procedure_version"] != PROCEDURE:
        raise Error("procedure drift")

    expected={}
    for row in admission["admissions"]:
        vid=row["validation_claim_id"]
        if row["grammar_mapping_inspected"] is not False:
            raise Error(f"{vid}: admission says Grammar mapping inspected")
        ident=row["source_identity"]
        if ident["kind"] != "DOI":
            raise Error(f"{vid}: non-DOI identity not supported by this transaction")
        expected[f"{vid}.json"]=(vid,norm_doi(ident["value"]))

    files=sorted(p.name for p in CANDIDATES.glob("*.json"))
    if files != sorted(expected):
        raise Error(f"candidate membership mismatch: got={files} expected={sorted(expected)}")
    if sorted(manifest["expected_files"]) != sorted(expected):
        raise Error("checked-in candidate manifest membership mismatch")

    source_by_id={x["validation_claim_id"]:x for x in source["entries"]}
    if set(source_by_id) != {x[0] for x in expected.values()}:
        raise Error("source-authority membership mismatch")

    receipts=[]
    for filename in files:
        vid,doi=expected[filename]
        path=CANDIDATES/filename
        raw=path.read_text(encoding="utf-8")
        low=raw.casefold()
        for marker in FORBIDDEN_DOWNSTREAM:
            if marker in low:
                raise Error(f"{filename}: downstream marker leaked before mapping: {marker}")

        obj=load(path)
        validate_claim_ir(obj)
        if obj["claim_id"] != f"{vid}.C1":
            raise Error(f"{filename}: claim_id mismatch")
        if norm_doi(obj["provenance"]["paper_id"]) != doi:
            raise Error(f"{filename}: DOI mismatch")
        ext=obj["extraction"]
        if ext["procedure_version"] != PROCEDURE:
            raise Error(f"{filename}: procedure mismatch")
        if ext["manual_review_status"] != "unreviewed":
            raise Error(f"{filename}: candidate must remain unreviewed")

        src=source_by_id[vid]
        if norm_doi(src["stable_identity"]) != doi:
            raise Error(f"{filename}: source authority DOI mismatch")
        if src["claimir_candidate_status"] != "UNREVIEWED":
            raise Error(f"{filename}: source authority review-state mismatch")
        if src["grammar_mapping_inspected"] is not False:
            raise Error(f"{filename}: source authority says mapping inspected")
        if src["source_text_committed"] is not False:
            raise Error(f"{filename}: raw source text must not be committed")

        receipts.append({
            "validation_claim_id":vid,
            "file":filename,
            "paper_id":obj["provenance"]["paper_id"],
            "claimir_sha256":sha(path),
            "blinded_claimir_sha256":hashlib.sha256(blinded_bytes(obj)).hexdigest(),
            "manual_review_status":"unreviewed",
            "grammar_mapping_inspected":False,
        })

    return {
        "schema":"relay-theory.paper2.pvs16_claimir_candidate_receipt.v1",
        "status":"VALIDATED_UNREVIEWED_PRE_MAPPING_CANDIDATES",
        "authority_issue":365,
        "admission_manifest_sha256":EXPECTED_ADMISSION_SHA,
        "candidate_count":len(receipts),
        "receipts":receipts,
        "grammar_mapping_authorized":False,
        "author_review_required_before_mapping":True,
        "terminal":"PVS16_CLAIMIR_CANDIDATES_VALIDATED_PENDING_AUTHOR_REVIEW",
    }

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    first=validate_all()
    second=validate_all()
    if first != second:
        raise Error("non-deterministic candidate validation")
    payload=json.dumps(first,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.write_text(payload,encoding="utf-8")
    else:
        print(payload,end="")
    print("PVS16_CLAIMIR_CANDIDATE_GATE_PASS")

if __name__=="__main__":
    main()
