#!/usr/bin/env python3
import copy
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROFILE_PATH = HERE / "W1_SOURCE_NATIVE_PROFILE_FRAGMENTS_v1.json"
PAIR_PATH = HERE / "W1_BOUNDED_PAIR_ADJUDICATIONS_v1.json"
GAPS_PATH = HERE / "W1_SOURCE_GAPS_AND_BLOCKERS_v1.json"

EXPECTED = {
    "ATT-01": "10.1007/s42113-024-00197-6",
    "ATT-02": "10.1371/journal.pcbi.1004770",
    "BLF-02": "10.1371/journal.pcbi.1006972",
    "BLF-03": "10.7554/eLife.08825",
    "CNC-01": "10.1038/s41562-023-01719-1",
    "CNC-02": "10.1371/journal.pcbi.1011954",
    "CNC-03": "10.7554/eLife.77185",
}
ALLOWED_STATUS = {
    "PROFILE_FRAGMENT_READY",
    "SOURCE_BLOCKED",
    "SCIENTIFIC_ANCESTRY_UNDERDETERMINED",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SHA1 = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_BUNDLES = {
    "BLF-02": {("REQUIRED_MODEL_VARIANT_AND_ADVERSE_DETAIL", "10.1371/journal.pcbi.1006972.s005")},
}

def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def validate(profile_doc, pair_doc, gaps_doc):
    errors = []
    profiles = profile_doc.get("profiles", [])
    if profile_doc.get("profile_count") != 7 or len(profiles) != 7:
        errors.append("profile_count must be exactly seven")

    ids = [p.get("id") for p in profiles]
    if len(ids) != len(set(ids)):
        errors.append("duplicate profile id")
    if set(ids) != set(EXPECTED):
        errors.append("profile ids differ from exact W1 roster")

    for p in profiles:
        pid = p.get("id")
        if pid not in EXPECTED:
            continue
        if p.get("doi") != EXPECTED[pid]:
            errors.append(f"{pid}: DOI mismatch")
        if p.get("completion_status") not in ALLOWED_STATUS:
            errors.append(f"{pid}: invalid completion_status")
        if p.get("global_family_independence_certified") is not False:
            errors.append(f"{pid}: global independence must remain false")
        if p.get("ancestry_exhaustiveness") != "NOT_ATTESTED":
            errors.append(f"{pid}: ancestry exhaustiveness promotion forbidden")
        if not p.get("native_core_operators"):
            errors.append(f"{pid}: missing core operators")
        for op in p.get("native_core_operators", []):
            if not op.startswith(pid + ":"):
                errors.append(f"{pid}: non-local operator id {op}")

        esha = p.get("edition_sha256")
        if esha is None:
            if not p.get("edition_sha256_unavailable_reason"):
                errors.append(f"{pid}: null edition SHA without reason")
        elif not SHA256.fullmatch(esha):
            errors.append(f"{pid}: malformed edition SHA256")

        evidence = p.get("original_source_evidence", [])
        if len(evidence) < 2:
            errors.append(f"{pid}: insufficient repository evidence")
        for i, ev in enumerate(evidence):
            if not ev.get("repository_path"):
                errors.append(f"{pid}: evidence[{i}] missing path")
            if not SHA1.fullmatch(str(ev.get("repository_git_blob_sha1", ""))):
                errors.append(f"{pid}: evidence[{i}] malformed blob SHA1")
            if not SHA1.fullmatch(str(ev.get("source_repository_ref", ""))):
                errors.append(f"{pid}: evidence[{i}] malformed ref")
            psha = ev.get("original_primary_sha256")
            if psha is not None and not SHA256.fullmatch(str(psha)):
                errors.append(f"{pid}: evidence[{i}] malformed original SHA256")

        required = REQUIRED_BUNDLES.get(pid, set())
        present = {(b.get("role"), b.get("doi")) for b in p.get("additional_edition_bundle", [])}
        if not required.issubset(present):
            errors.append(f"{pid}: required correction/supplement disappeared")
        for b in p.get("additional_edition_bundle", []):
            sha = b.get("sha256")
            if sha is not None and not SHA256.fullmatch(str(sha)):
                errors.append(f"{pid}: malformed bundle SHA256")
            if sha is None and not b.get("sha256_unavailable_reason"):
                errors.append(f"{pid}: bundle missing SHA without reason")

    by_id = {p["id"]: p for p in profiles if "id" in p}
    if by_id.get("BLF-02", {}).get("completion_status") != "SOURCE_BLOCKED":
        errors.append("BLF-02 must fail closed while required S1 bytes/hash are missing")
    if by_id.get("CNC-01", {}).get("completion_status") != "SCIENTIFIC_ANCESTRY_UNDERDETERMINED":
        errors.append("CNC-01 must preserve explicit ancestor-identity uncertainty")

    pairs = pair_doc.get("pairs", [])
    if pair_doc.get("pair_count") != 7 or len(pairs) != 7:
        errors.append("pair_count must be exactly seven positive-priority judgments")
    if pair_doc.get("global_family_independence_certified") is not False:
        errors.append("pair document global independence must remain false")
    if pair_doc.get("main_authorized") is not False:
        errors.append("pair document MAIN authorization must remain false")
    for i, pair in enumerate(pairs):
        if pair.get("global_independence_promoted") is not False:
            errors.append(f"pair[{i}] illegally promotes global independence")
        for ev in pair.get("evidence", []):
            if not SHA1.fullmatch(str(ev.get("repository_git_blob_sha1", ""))):
                errors.append(f"pair[{i}] malformed evidence blob")
            if not SHA1.fullmatch(str(ev.get("source_repository_ref", ""))):
                errors.append(f"pair[{i}] malformed evidence ref")
            if not ev.get("repository_path"):
                errors.append(f"pair[{i}] evidence path missing")

    gap_status = {x.get("id"): x.get("status") for x in gaps_doc.get("paper_status", [])}
    if gap_status != {p["id"]: p["completion_status"] for p in profiles}:
        errors.append("gap ledger status does not exactly match profile status")
    if gaps_doc.get("main_authorized") is not False:
        errors.append("MAIN must remain unauthorized")
    if gaps_doc.get("global_family_independence_certified") is not False:
        errors.append("global family independence must remain false")

    if errors:
        raise AssertionError("\n".join(errors))
    return True

def main():
    validate(load_json(PROFILE_PATH), load_json(PAIR_PATH), load_json(GAPS_PATH))
    print("W1_FAIL_CLOSED_VERIFY_PASS")

if __name__ == "__main__":
    main()
