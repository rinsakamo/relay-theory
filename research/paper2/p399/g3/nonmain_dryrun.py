#!/usr/bin/env python3
"""Executable purely constructed non-MAIN source-packet transport demonstration.
Different functions/processes are NOT independent scientific assessors.
"""
import json
from pathlib import Path
from qualify_g3_v11 import raw_sha, check_completeness

ROOT = Path(__file__).resolve().parent
FILE = ROOT / "fixtures/nonmain_constructed_primary_v1.txt"
HEADERS = ("TITLE:", "AUTHOR:", "VENUE:", "DOI:")
CATEGORIES = {
    "sections": {"S1": "SECTION S1:"},
    "equations": {"eq-1": "EQUATION eq-1:", "eq-2": "EQUATION eq-2:"},
    "figures": {"fig-1": "FIGURE fig-1:"},
    "states": {"st-A": "STATE st-A:", "st-B": "STATE st-B:"},
    "dependencies": {"dep-1": "DEPENDENCY dep-1:"},
    "temporal": {"time-1": "TEMPORAL time-1:"},
    "variants": {"variant-1": "VARIANT variant-1:", "variant-2": "VARIANT variant-2:"},
    "negative": {"neg-1": "NEGATIVE neg-1:"},
    "boundaries": {"boundary-1": "BOUNDARY boundary-1:"},
}

def assemble_constructed_packet():
    source = FILE.read_bytes()  # actual original FIXTURE bytes; not publisher material
    lines = source.decode("utf-8").splitlines(keepends=True)
    redactions = []
    masked = []
    for line in lines:
        if line.startswith(HEADERS):
            heading = line.split(":", 1)[0]
            redactions.append(dict(source_locator="SYNTHETIC:"+heading,
                                   redacted_field=heading, scientific_load_bearing=False,
                                   replacement="[REMOVED_NONESSENTIAL_IDENTITY]"))
            masked.append(heading + ": [REMOVED_NONESSENTIAL_IDENTITY]\n")
        else:
            masked.append(line)
    packet = "".join(masked).encode("utf-8")
    src_text, packet_text = source.decode("utf-8"), packet.decode("utf-8")
    evidence = []
    required = {}
    for category, witnesses in CATEGORIES.items():
        required[category] = sorted(witnesses)
        for wid, anchor in witnesses.items():
            if src_text.count(anchor) != 1 or packet_text.count(anchor) != 1:
                raise ValueError("CONSTRUCTED_SOURCE_OR_PACKET_MISSING_OR_DUPLICATE:"+wid)
            original = [l.strip() for l in src_text.splitlines() if l.startswith(anchor)][0]
            preserved = [l.strip() for l in packet_text.splitlines() if l.startswith(anchor)][0]
            if original != preserved:
                raise ValueError("SOURCE_MECHANISTIC_INFORMATION_CHANGED:"+wid)
            evidence.append(dict(source_atom_id=wid, original_locator="constructed:"+anchor,
                                 preserved_packet_locator="constructed:"+anchor,
                                 checked_by="SCRIPTED_TEXT_EQUALITY_NOT_INDEPENDENT_REVIEW"))
    fingerprints = dict(source_raw_sha256=raw_sha(source), packet_raw_sha256=raw_sha(packet))
    doc = dict(schema_version="G3_SOURCE_COMPLETENESS_V1_1",
        paper_token="NONMAIN_CONSTRUCTED_ONLY", source_fingerprint=fingerprints["source_raw_sha256"],
        native_reference_digest="f"*64, source_locked_before_D=True,
        required=required, preserved={k:list(v) for k,v in required.items()}, redactions=redactions,
        curator=dict(actor_id="SCRIPTED_MOCK_CURATOR", execution_id="NONMAIN_SCRIPT_ONLY",
                     attestation_raw_sha256=None),
        second_review=dict(status="CURATOR_ONLY_UNVALIDATED", actor_id=None,
                           execution_id=None, attestation_raw_sha256=None),
        reference_status="SINGLE_REFERENCE_UNVALIDATED",
        evidence_audit=evidence)
    check_completeness(doc)
    return source, packet, doc, fingerprints

if __name__ == "__main__":
    _, _, doc, f = assemble_constructed_packet()
    print(json.dumps({"scope": "NON_MAIN_CONSTRUCTED_ONLY",
        "status": "EXECUTED_SCRIPTED_SOURCE_PACKET_TRANSPORT_NOT_INDEPENDENT_SEMANTIC_ASSESSMENT",
        "witnesses_preserved": len(doc["evidence_audit"]), "actor_count_real": 0, **f},
        sort_keys=True))
