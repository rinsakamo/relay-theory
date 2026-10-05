#!/usr/bin/env python3
"""Verify exact source-ledger Git provenance of ten PREVIOUS bounded audits.

This cannot reverify non-Git original PDF/MHT bytes or mathematical semantics.
New paper IDs MUST receive an explicit evidence-mapping code review.
"""
import argparse
import json
import subprocess
from pathlib import Path
from build_pair_matrix import InputMismatch

G2_SOURCE_REF = "b9b238fe786cba2ae9df9efb26febc78ccd67486"
G2_INTEGRATED_REF = "15ee0a2a74b7e47adb439d8b30f499103d1f7eb1"
G1_SCIENCE_REF = "c7317da41b15159864c014b8dc53449121c34a2c"
ROOT = "research/paper2/p399/"
THREE = ROOT + "g2/three_primary_review_20261005/THREE_PRIMARY_SOURCE_FREEZE_AND_BOUNDED_SCIENCE_v1.json"
INT01 = ROOT + "g2/int_g2d/G2D_V18_INT01_FULL_PRIVATE_PUBLISHER_HTML_SOURCE_SCIENCE_AND_TARGETED_FAMILY_AUDIT.json"
INT04 = ROOT + "g2/int_g2d/G2D_V8_INT04_EXACT_ORIGINAL_RAW_AND_BOUNDED_FIGURES_MACHINE_GATES.json"
P05 = ROOT + "g1/p05/P05_PRE_A_ORIGINAL_SOURCE_EDITION_AND_ANCESTRY_v1.json"
P13 = ROOT + "g1/p13/P13_PRE_A_PUBLISHED_MAIN_PLUS_REQUIRED_ORIGINAL_S1_FAMILY_FREEZE_v1.json"
P09 = ROOT + "g1/p09/P09_SEPARATE_BOUNDED_SCIENTIFIC_QUALIFICATION_20261004.json"
P14 = ROOT + "g1/p14/P14_SEPARATE_BOUNDED_ORIGINAL_SCIENCE_QUALIFICATION_20261004.json"
INT08 = ROOT + "g2/int_g2d/G2D_V10D_CORRECTED_PAIR_SOURCE_NATIVE_MACHINE_GATES.json"

# Cross-checked actual Git blobs in the research repository, not raw external PDFs.
TRUSTED = {
    "ATT-03": (G2_SOURCE_REF, THREE, "021dd2856510a4ac04fbbb3221d93b103067bb17"),
    "BLF-01": (G2_SOURCE_REF, THREE, "021dd2856510a4ac04fbbb3221d93b103067bb17"),
    "PRD-01": (G2_SOURCE_REF, THREE, "021dd2856510a4ac04fbbb3221d93b103067bb17"),
    "INT-01": (G2_INTEGRATED_REF, INT01, "914ea88db618d75c9e1c05a0a862ad6d3b9ed3f2"),
    "INT-04": (G2_INTEGRATED_REF, INT04, "71a562480903591c61ce2133f3f8637e4f190d94"),
    "P05": (G1_SCIENCE_REF, P05, "68ff9016d51382d8295607d49e8dee5e3060d024"),
    "P13": (G1_SCIENCE_REF, P13, "90244cd348524ff37a7715e8a03acb3f33271c8c"),
    "P09": (G1_SCIENCE_REF, P09, "09e682b93a27f8e7c08eb754e83f67ada2fbcfe7"),
    "P14": (G1_SCIENCE_REF, P14, "1e063c0779b0a90ad499320bad612791f74fe8fb"),
    "INT-08": (G2_INTEGRATED_REF, INT08, "4ccb0f762a20b396afbcdf69e8e8211d2a7872bf"),
}


def git_blob(reader_ref, repository_path):
    ident = reader_ref + ":" + repository_path
    sha = subprocess.run(
        ["git", "rev-parse", ident], text=True, capture_output=True, check=True
    ).stdout.strip()
    body = subprocess.run(["git", "show", ident], capture_output=True, check=True).stdout
    return sha, json.loads(body.decode("utf-8"))


def primary_identity(ident, data):
    if ident == "ATT-03":
        row = data["files"]["ATT03"]
        return row["doi"], row["sha256"], []
    if ident == "BLF-01":
        row = data["files"]["BLF01"]
        return row["doi"], row["sha256"], []
    if ident == "PRD-01":
        row = data["files"]["PRD01"]
        docs = row["source_bundle"]
        if not row["author_substitution_authorized"]:
            raise InputMismatch("PRD01 author-approved source exception absent")
        return row["doi"], docs[0]["sha256"], [docs[1]["sha256"]]
    if ident == "INT-01":
        row = data["frozen"]
        if row["adopted_likelihood"] != "2026-10-05_AUTHOR_APPROVED_PREPUBLICATION_SOFTMAX_CODE":
            raise InputMismatch("INT01 author-approved variant changed")
        return row["doi"], row["mht_sha256"], [row["embedded_publisher_html_sha256"]]
    if ident == "INT-04":
        docs = data["source_media"]
        return "10.1038/s41562-023-01799-z", docs[0]["sha256"], [docs[1]["sha256"]]
    if ident == "P05":
        row = data["original_source"]
        return data["candidate"]["doi"], row["raw_sha256"], []
    if ident == "P09":
        return data["candidate"]["doi"], data["primary_original"]["sha256"], []
    if ident == "P14":
        items = data["adopted_original_sources"]
        return data["paper"]["doi"], items["main"]["raw_sha256"], [
            doc["sha256"] for doc in items["six_same_original_publisher_supplement_receipts"]
        ]
    if ident == "INT-08":
        record = data["official_sources"]["INT-08"]
        if not record["source_reacquired_on_corrected_run"] or not record["manual_policy_hand_imposed_detected_on_corrected_run"]:
            raise InputMismatch("INT08 corrected official source witness missing")
        return record["doi"], record["exact_G2_inherited_raw_sha256"], []
    if ident == "P13":
        row = data["frozen_main_original"]
        return data["work"]["doi"], row["raw_sha256"], [
            data["frozen_necessary_supplement"]["raw_sha256"]
        ]
    raise InputMismatch("Unexpected source subject")


def verify(profiles, loader=git_blob):
    if set(profiles) != set(TRUSTED) or len(profiles) != 10:
        raise InputMismatch("This snapshot's exact ten auditable profiles must be present")
    seen = {}
    for profile in profiles.values():
        ident = profile["id"]
        ref, path, blob = TRUSTED[ident]
        evs = profile["original_source_evidence"]
        if len(evs) != 1:
            raise InputMismatch(f"{ident}: no unverified evidence additions")
        ev = evs[0]
        if (ev["repository_path"], ev["repository_git_blob_sha1"], ev["source_repository_ref"]) != (
            path, blob, ref
        ):
            raise InputMismatch(f"{ident}: source audit provenance mismatch")
        if (ref, path) not in seen:
            seen[(ref, path)] = loader(ref, path)
        actual_blob, doc = seen[(ref, path)]
        if actual_blob != blob:
            raise InputMismatch(f"{ident}: source Git blob changed")
        source_doi, source_sha, supplements = primary_identity(ident, doc)
        if profile["doi"].lower() != source_doi.lower() or profile["edition_sha256"] != source_sha:
            raise InputMismatch(f"{ident}: DOI/source raw original hash mismatch")
        if ev["original_primary_sha256"] != source_sha:
            raise InputMismatch(f"{ident}: evidence raw hash mismatch")
        profiles_supps = [x["sha256"] for x in profile.get("additional_edition_bundle", [])
                           if x["role"] != "author_adopted_prepublication_code"]
        if sorted(profiles_supps) != sorted(supplements):
            raise InputMismatch(f"{ident}: mandatory original/correction bundle mismatch")
        if ident == "P05":
            source_ancestors = [x["doi"].lower() for x in doc["direct_ancestry"] if x.get("doi")]
            if [x.lower() for x in profile["direct_model_ancestors"]] != source_ancestors:
                raise InputMismatch("P05 historical direct IVSN ancestor missing/drifted")
        if ident == "INT-01":
            author_code = [
                x for x in profile["additional_edition_bundle"]
                if x["role"] == "author_adopted_prepublication_code"
            ]
            if len(author_code) != 1 or author_code[0]["git_commit"] != doc["frozen"]["immutable_code_commit"] or author_code[0]["git_blob"] != doc["frozen"]["immutable_code_blob"]:
                raise InputMismatch("INT01 author chosen executable model/code ref mismatch")
    return {
        "source_ledgers_distinct_git_blobs_crosschecked": len(seen),
        "profiles_crosschecked": len(profiles),
        "fresh_external_original_reacquisitions_performed_here": 0,
        "full_original_semantic_science_newly_certified": 0,
        "global_family_independence_newly_certified": 0,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--profiles", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    items = json.loads(Path(args.profiles).read_text(encoding="utf8"))["profiles"]
    if len(items) != len({p["id"] for p in items}):
        raise InputMismatch("Repeated profile ID")
    report = verify({p["id"]: p for p in items})
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf8"
    )
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
