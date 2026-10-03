#!/usr/bin/env python3
"""Structural cloud provenance gate for Paper 2. NOT a scientific source adjudicator."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

HEX = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
TRACK_STAGES = {
    "P398_PRETEST": ("SOURCE", "REFERENCE", "MASKED", "RECONSTRUCTION", "COMPARISON"),
    "P398_MAIN": ("SOURCE", "REFERENCE", "MASKED", "RECONSTRUCTION"),
    "P399_NEW_PILOT": ("SOURCE", "A", "B", "C"),
}
P398_KINDS = {
    "PUBLISHER_FULL_HTML",
    "PUBLISHER_ORIGINAL_PDF",
    "VERIFIED_PUBLISHER_COPY",
    "VERIFIED_MODEL_EQUIVALENT_COPY",
}
COPY_KINDS = {"VERIFIED_PUBLISHER_COPY", "VERIFIED_MODEL_EQUIVALENT_COPY"}


class GateError(ValueError):
    pass


def require(ok, explanation):
    if not ok:
        raise GateError(explanation)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def digest(value):
    return isinstance(value, str) and bool(HEX.fullmatch(value))


def pinned_commit(value):
    return isinstance(value, str) and bool(COMMIT.fullmatch(value))


def safe_artifact_path(value):
    """Only derived Paper 2 artifacts; never ingest user-supplied external paths."""
    if not nonempty(value):
        return False
    p = PurePosixPath(value)
    return (
        not p.is_absolute()
        and ".." not in p.parts
        and len(p.parts) > 2
        and p.parts[:2] == ("research", "paper2")
        and p.suffix.lower() in (".json", ".md")
        and all(part not in ("", ".") for part in p.parts)
    )


def git_read(commit, path):
    proc = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    require(proc.returncode == 0, f"pinned artifact unavailable: {commit}:{path}")
    return proc.stdout


def git_ancestor(earlier, later):
    proc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", earlier, later],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    return proc.returncode == 0


def check_pin(pin, read_blob):
    require(isinstance(pin, dict), "stage/lock must be an object")
    commit, path, sha = pin.get("commit"), pin.get("path"), pin.get("sha256")
    require(pinned_commit(commit), "invalid immutable commit SHA")
    require(safe_artifact_path(path), "invalid/out-of-scope derived-artifact path")
    require(digest(sha), "invalid pinned artifact SHA256")
    actual = hashlib.sha256(read_blob(commit, path)).hexdigest()
    require(actual == sha, f"frozen artifact mismatch at {commit}:{path}")
    return commit


def validate_receipt(record, read_blob=git_read, ancestor=git_ancestor):
    require(isinstance(record, dict), "receipt must be an object")
    require(record.get("schema") == "relay-theory.paper2.cloud-receipt.v1", "schema mismatch")
    track = record.get("track")
    require(track in TRACK_STAGES, "unknown protocol track")
    require(nonempty(record.get("run_id")), "missing immutable run ID")
    require(nonempty(record.get("source_id")), "missing canonical source ID")

    source = record.get("source")
    require(isinstance(source, dict), "missing source audit")
    require(nonempty(source.get("canonical_work")), "missing canonical bibliography/work identity")
    require(nonempty(source.get("url")) and source["url"].startswith("https://"), "source URL must be HTTPS")
    require(digest(source.get("scope_metadata_sha256")), "missing source-scope metadata digest")
    require(source.get("edition_status") in ("VERIFIED", "PENDING"), "invalid edition status")
    require(source.get("lineage_status") in ("VERIFIED_DISTINCT", "CHECKED_DISCLOSED_REUSE", "PENDING"),
            "invalid lineage status")
    require(nonempty(source.get("family_id")), "missing central model-family audit identifier")

    kind = source.get("kind")
    if track == "P399_NEW_PILOT":
        require(kind == "PUBLISHER_FULL_HTML", "P399 source policy: official full HTML ONLY")
        require(source.get("publisher_designated_complete") is True,
                "P399 publisher complete-HTML designation missing")
        require(source.get("standalone_supplements") == "OUT_OF_SCOPE",
                "P399 must not make standalone supplements a gate")
        require(record.get("historical_case") is False,
                "development/historical P399 case cannot be counted as NEW")
    else:
        require(kind in P398_KINDS, "invalid #398 source kind")
        if kind in COPY_KINDS:
            require(digest(source.get("copy_sha256")), "verified copy needs actual byte SHA256")
            require(nonempty(source.get("equivalence_evidence")),
                    "verified copy needs independently documented equivalence evidence")
        if track == "P398_PRETEST":
            require(source["lineage_status"] in ("VERIFIED_DISTINCT", "PENDING"),
                    "pilot/main model-family separation is mandatory")
    stages = record.get("stages")
    require(isinstance(stages, list), "stages must be a list (possibly empty)")
    order = TRACK_STAGES[track]
    require(len(stages) <= len(order), "too many stages")
    require([x.get("phase") for x in stages if isinstance(x, dict)] == list(order[:len(stages)])
            and all(isinstance(x, dict) for x in stages), "phase gap/reorder/duplicate")
    if len(stages) > 1:
        require(source["edition_status"] == "VERIFIED" and source["lineage_status"] != "PENDING",
                "source and lineage must be qualified before analysis")
    # A receipt with only SOURCE describes staging, not pilot qualification.
    commits = []
    for stage in stages:
        commit = check_pin(stage, read_blob)
        if commits:
            require(commit != commits[-1] and ancestor(commits[-1], commit),
                    "stage not frozen in a later descendant commit")
        commits.append(commit)

    if track == "P398_MAIN" and len(stages) >= 4:
        locks = record.get("locks")
        require(isinstance(locks, dict) and set(locks) >= {"main_manifest", "pilot_protocol"},
                "MAIN requires frozen roster and independently qualified pilot procedure")
        main_commit = check_pin(locks["main_manifest"], read_blob)
        protocol_commit = check_pin(locks["pilot_protocol"], read_blob)
        require(ancestor(main_commit, protocol_commit) and
                ancestor(protocol_commit, commits[-1]) and
                main_commit != protocol_commit != commits[-1],
                "MAIN freeze chronology/ancestry failure")
        require(record.get("pilot_qualification") == "HUMAN_REVIEWED_AND_FROZEN",
                "main scientific procedure remains unqualified")
    if track == "P398_MAIN" and stages and stages[-1]["phase"] == "RECONSTRUCTION":
        require(nonempty(record.get("masking_and_leakage_record")),
                "MAIN must document source/reference masking and recognizability")
    if track == "P399_NEW_PILOT" and len(stages) == 4:
        require(record.get("author_exception_review") in ("NONE_NEEDED", "RESOLVED", "UNRESOLVED"),
                "P399 C requires explicit exception-gate status")
        # UNRESOLVED may be a valid negative/underdetermined scientific result.
    return (track, record["run_id"], source["canonical_work"], source["family_id"])


def validate_directory(directory):
    files = sorted(Path(directory).glob("*.json"))
    if not files:
        print("SCAFFOLD_ONLY: 0 scientific receipts; no admission or MAIN authorization inferred")
        return 0
    runs = set()
    pretest, main = set(), set()
    pretest_families, main_families = set(), set()
    for file in files:
        try:
            track, run, work, family = validate_receipt(json.loads(file.read_text(encoding="utf-8")))
            require(run not in runs, f"duplicate run ID: {run}")
            runs.add(run)
            if track == "P398_PRETEST":
                pretest.add(work)
                pretest_families.add(family)
            if track == "P398_MAIN":
                main.add(work)
                main_families.add(family)
            print(f"STRUCTURAL_PROVENANCE_PASS {file.name}: {track} {run}")
        except (GateError, ValueError, OSError, subprocess.SubprocessError) as exc:
            raise GateError(f"{file}: {exc}") from exc
    require(not (pretest & main), "same canonical work in pretest and MAIN")
    require(not (pretest_families & main_families), "same declared model family in pretest and MAIN")
    print(f"VALIDATED: {len(files)} source/phase provenance receipts ONLY; scientific qualification NOT established")
    return len(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipts-dir", default="research/paper2/cloud60/receipts")
    args = parser.parse_args()
    try:
        validate_directory(args.receipts_dir)
    except (GateError, ValueError) as exc:
        print(f"PROVENANCE_FAIL: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
