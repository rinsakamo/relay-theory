#!/usr/bin/env python3
"""P399 G4-B03: outcome-blind, fail-closed central-family pair triage.

This tool creates a COMPLETE review matrix, not scientific family independence.
It consumes existing G2 780+800 archival records, current G2 working roster and
an independently pinned G1 roster. Native profiles may be added incrementally.
No MAIN Grammar/R/H/result artifacts are read.
"""
import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


class InputMismatch(ValueError):
    pass


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalized_doi(value):
    if not isinstance(value, str) or not value.strip():
        raise InputMismatch("Missing DOI")
    v = value.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if v.startswith(prefix):
            v = v[len(prefix):]
    return v


def roster(items, id_field):
    if not isinstance(items, list):
        raise InputMismatch("Roster must be a list")
    out = {}
    for item in items:
        ident = item.get(id_field)
        if not isinstance(ident, str) or not ident or ident in out:
            raise InputMismatch("Duplicate or missing roster ID")
        out[ident] = normalized_doi(item.get("doi"))
    return out


def key_internal(a, b):
    return tuple(sorted((a, b)))


def key_external(main, pilot):
    return main, pilot


def unique_legacy(rows, key_fn, expected, label):
    if not isinstance(rows, list) or len(rows) != expected:
        raise InputMismatch(f"{label}: expected {expected} original rows")
    out = {}
    for row in rows:
        key = key_fn(row)
        if key in out:
            raise InputMismatch(f"{label}: repeated pair {key}")
        out[key] = row
    return out


def load_profiles(data, g2, g1):
    if set(data) - {"schema", "profiles"}:
        raise InputMismatch("Profile file has unrecognized top-level keys")
    profiles = {}
    for item in data.get("profiles", []):
        ident = item.get("id")
        if ident in profiles or ident not in (set(g2) | set(g1)):
            raise InputMismatch(f"Unknown/duplicate profile {ident}")
        if not item.get("original_source_evidence"):
            raise InputMismatch(f"Profile {ident} requires original-source evidence")
        if not isinstance(item.get("native_core_operators"), list):
            raise InputMismatch(f"Profile {ident} missing native_core_operators list")
        if not isinstance(item.get("direct_model_ancestors"), list):
            raise InputMismatch(f"Profile {ident} missing direct_model_ancestors list")
        if not isinstance(item.get("edition_sha256"), str) or len(item["edition_sha256"]) != 64:
            raise InputMismatch(f"Profile {ident}: edition digest required")
        profiles[ident] = item
    return profiles


def source_hints(a, b, profile_a, profile_b):
    """Hints only: missing edges, absent citations or nonshared ops prove nothing."""
    hints = []
    if profile_a and profile_b:
        ops_a = set(profile_a["native_core_operators"])
        ops_b = set(profile_b["native_core_operators"])
        # Explicit source-grounded stable IDs, NOT lexical name similarity.
        if ops_a & ops_b:
            hints.append("VERIFIED_PROFILE_SHARED_CORE_OPERATOR_CANDIDATE")
    if profile_a and b in profile_a["direct_model_ancestors"]:
        hints.append("PROFILE_A_DIRECT_ANCESTOR_CANDIDATE")
    if profile_b and a in profile_b["direct_model_ancestors"]:
        hints.append("PROFILE_B_DIRECT_ANCESTOR_CANDIDATE")
    return hints


def candidate(row, a, b, doi_a, doi_b, profiles):
    if doi_a == doi_b:
        priority, category = 0, "EXACT_DOI_CONFLICT"
    else:
        priority, category = 4, "NO_POSITIVE_COLLISION_EVIDENCE_NOT_CLEARED"
    hints = []
    risk = row.get("prior_logged_risk", row.get("prior_risk"))
    if risk:
        hints.append("EXISTING_LOGGED_SOURCE_RISK")
        if priority > 1:
            priority, category = 1, "EXISTING_RISK_SOURCE_REVIEW"
    if row.get("source_citation"):
        hints.append("ARCHIVED_SOURCE_CITATION_REVIEW_NOT_DUPLICATION")
        if priority > 2:
            priority, category = 2, "SOURCE_CITATION_NEEDS_NATIVE_REVIEW"
    profile_hints = source_hints(
        doi_a, doi_b, profiles.get(a), profiles.get(b)
    )
    hints.extend(profile_hints)
    if profile_hints and priority > 2:
        priority, category = 2, "PROFILE_STRUCTURAL_CANDIDATE_REVIEW"
    return {
        "priority": priority,
        "triage": category,
        "hints": sorted(set(hints)),
        "legacy_risk": risk,
        "legacy_citation": row.get("source_citation"),
        "scientific_family_decision": "UNDERDETERMINED",
        "global_independence_certified": False,
    }


def generate(g2_data, g1_data, legacy, profile_data):
    g2 = roster(g2_data["selected_working_roster"], "slot")
    g1 = roster(g1_data["roster_snapshot"], "id")
    if len(g2) != 40 or len(g1) != 20 or set(g2) & set(g1):
        raise InputMismatch("Expected exactly disjoint 40 G2 IDs and 20 G1 IDs")
    if len(set(g2.values())) != 40 or len(set(g1.values())) != 20:
        raise InputMismatch("Unexpected duplicate DOI within an input roster")
    archival_internal = unique_legacy(
        legacy["main_main_pairs"],
        lambda r: key_internal(r["a"], r["b"]), 780, "MAIN-MAIN"
    )
    archival_external = unique_legacy(
        legacy["main_vs_g1_pairs"],
        lambda r: key_external(r["main_id"], r["g1_id"]), 800, "MAIN-G1"
    )
    expected_internal = {key_internal(a, b) for a, b in itertools.combinations(g2, 2)}
    expected_external = set(itertools.product(g2, g1))
    if set(archival_internal) != expected_internal or set(archival_external) != expected_external:
        raise InputMismatch("Archival 780/800 pair identities do not match live rosters")
    # Verify independent authoritative G1 identities, not only old provisional G2 G1 table.
    for (a, b), row in archival_internal.items():
        if normalized_doi(row["doi_a"]) != g2[row["a"]] or normalized_doi(row["doi_b"]) != g2[row["b"]]:
            raise InputMismatch(f"Internal archived DOI drift: {a}, {b}")
    for (a, b), row in archival_external.items():
        if normalized_doi(row["main_doi"]) != g2[a] or normalized_doi(row["g1_doi"]) != g1[b]:
            raise InputMismatch(f"Cross-cohort DOI identity drift: {a}, {b}")
    profiles = load_profiles(profile_data, g2, g1)
    rows = []
    for a, b in itertools.combinations(g2, 2):
        row = archival_internal[key_internal(a, b)]
        outcome = candidate(row, a, b, g2[a], g2[b], profiles)
        rows.append({"cohort": "G2_G2", "a": a, "b": b, "doi_a": g2[a], "doi_b": g2[b], **outcome})
    for a, b in itertools.product(g2, g1):
        row = archival_external[(a, b)]
        outcome = candidate(row, a, b, g2[a], g1[b], profiles)
        rows.append({"cohort": "G2_G1", "a": a, "b": b, "doi_a": g2[a], "doi_b": g1[b], **outcome})
    if len(rows) != 1580:
        raise InputMismatch("All 1580 comparisons mandatory")
    rows.sort(key=lambda r: (r["priority"], r["cohort"], r["a"], r["b"]))
    categories = dict(sorted(Counter(r["triage"] for r in rows).items()))
    return rows, {
        "schema": "relaytheory.p399.g4.pair_triage_v1",
        "scope": "CANDIDATE_REVIEW_ONLY_NOT_SCIENTIFIC_CLEARANCE",
        "g2_slots": 40, "g1_slots": 20,
        "g2_internal_pairs_checked": 780, "g2_g1_pairs_checked": 800,
        "full_pair_count": 1580,
        "original_source_grounded_profiles": len(profiles),
        "priority_categories": categories,
        "global_final_independent_pairs": 0,
        "scientific_main_authorized": False,
    }


def main():
    p = argparse.ArgumentParser()
    for opt in ("g2-manifest", "g1-roster", "legacy-pairs", "profiles", "output"):
        p.add_argument("--" + opt, required=True)
    p.add_argument("--focus", help="Output incident pairs ONLY for one changed slot; not a global receipt")
    args = p.parse_args()
    paths = {k: Path(getattr(args, k.replace("-", "_"))) for k in
             ("g2-manifest", "g1-roster", "legacy-pairs", "profiles")}
    rows, summary = generate(
        load(paths["g2-manifest"]), load(paths["g1-roster"]),
        load(paths["legacy-pairs"]), load(paths["profiles"])
    )
    summary["raw_input_sha256"] = {k: digest(v) for k, v in sorted(paths.items())}
    if args.focus:
        if args.focus not in ({r["a"] for r in rows} | {r["b"] for r in rows}):
            raise InputMismatch("Unknown focus slot")
        rows = [r for r in rows if args.focus in (r["a"], r["b"])]
        expected = 59 if args.focus.startswith("INT-") or args.focus in {
            item["slot"] for item in load(paths["g2-manifest"])["selected_working_roster"]
        } else 40
        if len(rows) != expected:
            raise InputMismatch("Incremental incident comparison count mismatch")
        summary["partial_focus"] = args.focus
        summary["emitted_rows_only"] = len(rows)
        summary["NOT_A_GLOBAL_REVIEW_COMPLETION_RECEIPT"] = True
    else:
        summary["partial_focus"] = None
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "PAIR_TRIAGE_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output / "PAIR_TRIAGE_MATRIX.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "PRIORITIZED_REVIEW_QUEUE.json").write_text(
        json.dumps([r for r in rows if r["priority"] < 4], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in summary.items()
                      if k not in ("raw_input_sha256",)}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
