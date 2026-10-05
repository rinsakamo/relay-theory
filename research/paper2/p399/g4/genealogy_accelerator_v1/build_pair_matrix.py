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
    """Admission to indexed limited-source *triage*, never final science."""
    allowed = {"schema", "profiles", "roster_reference", "science_method"}
    if set(data) - allowed:
        raise InputMismatch("Profile file has unrecognized top-level keys")
    profiles = {}
    known = {**g2, **g1}
    sha256 = __import__("re").compile(r"^[0-9a-f]{64}$")
    gitsha = __import__("re").compile(r"^[0-9a-f]{40}$")
    for item in data.get("profiles", []):
        ident = item.get("id")
        if ident in profiles or ident not in known:
            raise InputMismatch(f"Unknown/duplicate profile {ident}")
        if normalized_doi(item.get("doi")) != known[ident]:
            raise InputMismatch(f"Profile {ident} DOI does not match exact frozen roster")
        if item.get("profile_state") != "LEDGER_DERIVED_BOUNDED_NO_NEW_SOURCE_QUALIFICATION":
            raise InputMismatch(f"Profile {ident} exceeds permitted original science scope")
        if item.get("global_family_independence_certified") is not False:
            raise InputMismatch(f"Profile {ident} false final science promotion")
        if item.get("ancestry_exhaustiveness") != "NOT_ATTESTED":
            raise InputMismatch(f"Profile {ident} must not claim ancestry exhaustiveness")
        if not sha256.fullmatch(str(item.get("edition_sha256", ""))):
            raise InputMismatch(f"Profile {ident} missing real hex edition digest")
        ops = item.get("native_core_operators")
        descriptions = item.get("operator_source_descriptions")
        if not isinstance(ops, list) or not ops or len(ops) != len(set(ops)):
            raise InputMismatch(f"Profile {ident} missing/duplicate source-defined core operators")
        if any(not isinstance(v, str) or not v.startswith(ident + ":") for v in ops):
            raise InputMismatch(f"Profile {ident} core operators must use paper-local IDs")
        if not isinstance(descriptions, dict) or set(descriptions) != set(ops) or not all(
            isinstance(v, str) and len(v.strip()) >= 20 for v in descriptions.values()
        ):
            raise InputMismatch(f"Profile {ident} operator descriptions ungrounded")
        ancestry = item.get("direct_model_ancestors")
        if not isinstance(ancestry, list) or len(ancestry) != len(set(ancestry)):
            raise InputMismatch(f"Profile {ident} invalid direct DOI ancestry list")
        for doi in ancestry:
            if not normalized_doi(doi).startswith("10."):
                raise InputMismatch(f"Profile {ident} ancestor must be DOI not slot name")
        evidence = item.get("original_source_evidence")
        if not isinstance(evidence, list) or not evidence:
            raise InputMismatch(f"Profile {ident} source ledger evidence missing")
        for ev in evidence:
            if ev.get("source_audit_kind") != "PREEXISTING_FROZEN_BOUNDED_LEDGER_NOT_NEW_INDEPENDENT_READING":
                raise InputMismatch("Evidence grade may not imply new original science")
            if ev.get("original_primary_sha256") != item["edition_sha256"]:
                raise InputMismatch("Primary original hash not coherent with profile edition")
            if not gitsha.fullmatch(str(ev.get("repository_git_blob_sha1", ""))):
                raise InputMismatch("Source ledger exact Git blob is required")
            if not isinstance(ev.get("repository_path"), str) or not ev["repository_path"].startswith("research/paper2/p399/"):
                raise InputMismatch("Explicit existing source ledger repository path needed")
            if not gitsha.fullmatch(str(ev.get("source_repository_ref", ""))):
                raise InputMismatch("Pin the precise upstream source-bearing Git commit")
            if not isinstance(ev.get("source_loci"), list) or not ev["source_loci"]:
                raise InputMismatch("Original source-locus index required")
        for doc in item.get("additional_edition_bundle", []):
            if doc.get("role") == "author_adopted_prepublication_code":
                if ident != "INT-01" or not gitsha.fullmatch(str(doc.get("git_commit", ""))) or not gitsha.fullmatch(str(doc.get("git_blob", ""))):
                    raise InputMismatch("Only INT01 exact author-adopted prepublication code reference allowed")
            elif not sha256.fullmatch(str(doc.get("sha256", ""))):
                raise InputMismatch(f"Profile {ident} invalid necessary source bundle digest")
        profiles[ident] = item
    return profiles


def source_hints(doi_a, doi_b, profile_a, profile_b):
    """DOI-based ancestry only. Paper-local operator names never auto-match."""
    hints = []
    if profile_a and normalized_doi(doi_b) in {
        normalized_doi(d) for d in profile_a["direct_model_ancestors"]
    }:
        hints.append("DECLARED_DIRECT_ANCESTOR_DOI_SOURCE_REVIEW")
    if profile_b and normalized_doi(doi_a) in {
        normalized_doi(d) for d in profile_b["direct_model_ancestors"]
    }:
        hints.append("DECLARED_DIRECT_ANCESTOR_DOI_SOURCE_REVIEW")
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


def existing_scoped_comparisons(v20, g2, g1):
    """Reuse only individually indexed bounded witnesses, never their final status."""
    if v20 is None:
        return {}
    matrix = v20["updated_original35_matrix"]
    subject = matrix["subject"]
    if subject["slot"] != "INT-01" or normalized_doi(subject["doi"]) != g2["INT-01"]:
        raise InputMismatch("V20 source-native comparison subject drift")
    rows = matrix["pairs"]
    expected = ({("G2_INT", ident) for ident in g2 if ident.startswith("INT-") and ident != "INT-01"}
                | {("G1", ident) for ident in g1})
    got = [(row["other_lane"], row["other_slot"]) for row in rows]
    if len(rows) != 35 or set(got) != expected or len(got) != len(set(got)):
        raise InputMismatch("V20 full 35 comparison peers not faithfully preserved")
    bounded = {}
    for row in rows:
        ident = row["other_slot"]
        cohort = row["other_lane"]
        expected_doi = g1[ident] if cohort == "G1" else g2[ident]
        if normalized_doi(row["doi"]) != expected_doi:
            raise InputMismatch("V20 source-native comparison peer DOI drift")
        if row.get("final_central_family_independent_certified") is not False:
            raise InputMismatch("V20 must not silently promote any global-family decision")
        if row.get("source_scoped_evidence_id"):
            if row.get("source_scoped_only") is not True:
                raise InputMismatch("V20 indexed comparison must remain bounded")
            bounded[(cohort, ident)] = {
                "bounded_original_evidence_id": row["source_scoped_evidence_id"],
                "bounded_original_outcome": row["original_family_analysis"],
                "evidence_scope": "SOURCE_SCOPED_ONLY_NOT_GLOBAL_INDEPENDENCE",
            }
    return bounded


def int04_int08_bounded_witness(source, g2, profiles):
    """Reuse actual exact-source native *local* differences; no final family claim."""
    if source is None:
        return None
    docs = source["official_sources"]
    for ident in ("INT-04", "INT-08"):
        if normalized_doi(docs[ident]["doi"]) != g2[ident]:
            raise InputMismatch("INT04/08 source-specific DOI drift")
        profile = profiles.get(ident)
        source_hash = docs[ident]["raw_main20_sha256"] if ident == "INT-04" else docs[ident]["exact_G2_inherited_raw_sha256"]
        if profile is not None and profile["edition_sha256"] != source_hash:
            raise InputMismatch("INT04/08 profile and source source-original digest mismatch")
    witness = source["source_native_pairwise_delta"]
    if (witness["distinct_local_primary_learning_target_and_operations_source_confirmed"] is not True
        or witness["pairwise_all_figures_math_complete_qualified"] is not False
        or witness["full_G1_20_G2_40_independent_family_cleared"] is not False
        or source["MAIN_authorized"] is not False):
        raise InputMismatch("Invalid v10d limited source witness/false global promotion")
    if not docs["INT-08"]["manual_policy_hand_imposed_detected_on_corrected_run"]:
        raise InputMismatch("INT08 adverse source boundary was not preserved")
    return {
        "bounded_original_evidence_id": "G2D_V10D_INT04_INT08",
        "bounded_original_outcome": "BOUNDED_DIFFERENT_OFFLINE_REPLAY_VS_LEARNED_ONLINE_RETRIEVAL_GATING",
        "evidence_scope": "SOURCE_SCOPED_ONLY_NOT_GLOBAL_INDEPENDENCE"
    }


def additional_g2d_bounded_pairs(v15b, v16b, g2, g1, profiles):
    """Pinned existing G2-D original-native comparisons; never new GLOBAL science."""
    extra = {}
    if v15b is not None:
        gov = v15b["governance"]
        if gov["all_800_central_family_cleared"] is not False or gov["main_science"] is not False:
            raise InputMismatch("v15b global cross-family false promotion")
        expected = {("INT-15", "P18"), ("INT-16", "P09")}
        rows = v15b["pairs"]
        if len(rows) != 2:
            raise InputMismatch("v15b exact original limited pair count drift")
        found = set()
        for r in rows:
            a, b = r["pair"]
            if not a.startswith("G2_") or not b.startswith("G1_"):
                raise InputMismatch("v15b G2/G1 pair taxonomy corrupted")
            a, b = a[3:].replace("INT", "INT-"), b[3:]
            if (a, b) not in expected or (a, b) in found:
                raise InputMismatch("v15b unexpected or repeated source-scoped pair")
            found.add((a, b))
            if (normalized_doi(r["source"]["int_doi"]) != g2[a]
                or normalized_doi(r["source"]["g1_doi"]) != g1[b]
                or r["official_final_independent"] is not False
                or not r["bounded_judgment"].endswith("full formal learning-rule and ancestry equivalence review held") 
                    and "PROVISIONAL" not in r["bounded_judgment"]):
                raise InputMismatch("v15b source DOI/scope/final scientific decision mismatch")
            extra[("G2_G1", a, b)] = {
                "bounded_original_evidence_id": "G2D_V15B_" + a + "_" + b,
                "bounded_original_outcome": r["bounded_judgment"],
                "evidence_scope": "SOURCE_SCOPED_ONLY_NOT_GLOBAL_INDEPENDENCE"
            }
        if found != expected:
            raise InputMismatch("v15b exactly two source-bounded pair witnesses required")
    if v16b is not None:
        x, y, comp, gates = (v16b[k] for k in (
            "source_int01", "source_int14", "comparison", "gates"
        ))
        if (normalized_doi(x["doi"]) != g2["INT-01"]
            or normalized_doi(y["doi"]) != g2["INT-14"]
            or comp["pair_bounded_nonidentical_core_operator_judgment"] != "SUPPORTED"
            or comp["whole_historical_family_final_judgment"] != "UNDERDETERMINED"
            or comp["direct_mathematical_descendant_relation_demonstrated"] is not False
            or gates["all_16_global_family_independence"] is not False
            or gates["main_authorized"] is not False):
            raise InputMismatch("v16b INT01 vs INT14 scope or DOI false promotion")
        if profiles.get("INT-01") and x["mht_sha"] != profiles["INT-01"]["edition_sha256"]:
            raise InputMismatch("v16b INT01 private original source version drift")
        extra[("G2_G2", "INT-01", "INT-14")] = {
            "bounded_original_evidence_id": "G2D_V16B_INT01_INT14",
            "bounded_original_outcome": "SHARED_CRP_BUT_BOUNDED_DISTINCT_TASKSET_POLICY_VS_GRAPH_HIERARCHY_OPERATORS",
            "evidence_scope": "SOURCE_SCOPED_ONLY_NOT_GLOBAL_INDEPENDENCE"
        }
    return extra


def generate(g2_data, g1_data, legacy, profile_data, source_native_v20=None, source_native_int04_int08=None, source_native_v15b=None, source_native_v16b=None):
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
    scoped = existing_scoped_comparisons(source_native_v20, g2, g1)
    extra = int04_int08_bounded_witness(source_native_int04_int08, g2, profiles)
    more = additional_g2d_bounded_pairs(source_native_v15b, source_native_v16b, g2, g1, profiles)
    rows = []
    for a, b in itertools.combinations(g2, 2):
        row = archival_internal[key_internal(a, b)]
        outcome = candidate(row, a, b, g2[a], g2[b], profiles)
        witness = scoped.get(("G2_INT", b if a == "INT-01" else a)) if "INT-01" in (a, b) else None
        if extra and {a, b} == {"INT-04", "INT-08"}:
            if witness:
                raise InputMismatch("Duplicate bounded source witness")
            witness = extra
        additional = more.get(("G2_G2", *key_internal(a, b)))
        if additional:
            if witness:
                raise InputMismatch("Duplicate differently indexed bounded original source witness")
            witness = additional
        if witness:
            outcome["prior_source_scoped_comparison"] = witness
            if outcome["priority"] > 3:
                outcome["priority"] = 3
                outcome["triage"] = "BOUNDED_SOURCE_COMPARISON_GLOBAL_REVIEW_PENDING"
        rows.append({"cohort": "G2_G2", "a": a, "b": b, "doi_a": g2[a], "doi_b": g2[b], **outcome})
    for a, b in itertools.product(g2, g1):
        row = archival_external[(a, b)]
        outcome = candidate(row, a, b, g2[a], g1[b], profiles)
        witness = scoped.get(("G1", b)) if a == "INT-01" else None
        additional = more.get(("G2_G1", a, b))
        if additional:
            if witness:
                raise InputMismatch("Duplicate cross-cohort source witness")
            witness = additional
        if witness:
            outcome["prior_source_scoped_comparison"] = witness
            if outcome["priority"] > 3:
                outcome["priority"] = 3
                outcome["triage"] = "BOUNDED_SOURCE_COMPARISON_GLOBAL_REVIEW_PENDING"
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
        "source_ledger_derived_bounded_profiles": len(profiles),
        "new_full_original_scientific_qualifications_from_profiles": 0,
        "prior_indexed_native_scoped_pairs_reused": len(scoped) + int(extra is not None) + len(more),
        "priority_categories": categories,
        "global_final_independent_pairs": 0,
        "scientific_main_authorized": False,
    }


def main():
    p = argparse.ArgumentParser()
    for opt in ("g2-manifest", "g1-roster", "legacy-pairs", "profiles", "output"):
        p.add_argument("--" + opt, required=True)
    p.add_argument("--focus", help="Output incident pairs ONLY for one changed slot; not a global receipt")
    p.add_argument("--source-native-v20", help="Optional pinned G2-D INT01 35-pair limited native evidence; cannot promote science")
    p.add_argument("--source-native-int04-int08", help="Optional pinned v10d INT04-INT08 bounded original-native contrast")
    p.add_argument("--source-native-v15b", help="Pinned two INT15/INT16 vs G1 source-native bounded comparisons")
    p.add_argument("--source-native-v16b", help="Pinned shared-CRP but local-different operator comparison INT01/INT14")
    args = p.parse_args()
    paths = {k: Path(getattr(args, k.replace("-", "_"))) for k in
             ("g2-manifest", "g1-roster", "legacy-pairs", "profiles")}
    rows, summary = generate(
        load(paths["g2-manifest"]), load(paths["g1-roster"]),
        load(paths["legacy-pairs"]), load(paths["profiles"]),
        load(args.source_native_v20) if args.source_native_v20 else None,
        load(args.source_native_int04_int08) if args.source_native_int04_int08 else None,
        load(args.source_native_v15b) if args.source_native_v15b else None,
        load(args.source_native_v16b) if args.source_native_v16b else None
    )
    if args.source_native_v20:
        paths["source-native-v20"] = Path(args.source_native_v20)
    if args.source_native_int04_int08:
        paths["source-native-int04-int08"] = Path(args.source_native_int04_int08)
    if args.source_native_v15b:
        paths["source-native-v15b"] = Path(args.source_native_v15b)
    if args.source_native_v16b:
        paths["source-native-v16b"] = Path(args.source_native_v16b)
    # Complete, deterministic next-source queue: ranking aids curator scheduling ONLY.
    # A zero-risk incident count is NEVER absence of common ancestry or evidence.
    known_profiles = {p["id"] for p in load(paths["profiles"])["profiles"]}
    all_g2 = roster(load(paths["g2-manifest"])["selected_working_roster"], "slot")
    all_g1 = roster(load(paths["g1-roster"])["roster_snapshot"], "id")
    incident = Counter()
    limited_incident = Counter()
    for r in rows:
        if r["priority"] < 4:
            incident[r["a"]] += 1
            incident[r["b"]] += 1
        if r.get("prior_source_scoped_comparison"):
            limited_incident[r["a"]] += 1
            limited_incident[r["b"]] += 1
    profile_gaps = []
    for ident, doi in {**all_g2, **all_g1}.items():
        if ident in known_profiles:
            continue
        profile_gaps.append({
            "id": ident, "doi": doi,
            "cohort": "G2_WORKING" if ident in all_g2 else "G1_SOURCE_SCOPED_WORKING",
            "incident_positive_triage_pairs": incident[ident],
            "existing_source_bounded_comparison_incidents": limited_incident[ident],
            "total_incident_comparisons": 59 if ident in all_g2 else 40,
            "status": "PROFILE_NOT_YET_IMPORTED_SOURCE_SCIENCE_AVAILABILITY_UNDETERMINED",
            "sorting_is_science_outcome_blind": True
        })
    profile_gaps.sort(key=lambda r: (
        -r["incident_positive_triage_pairs"], -r["existing_source_bounded_comparison_incidents"],
        r["cohort"], r["id"]
    ))
    summary["missing_profiles_from_current_60_working_roster"] = len(profile_gaps)
    summary["priority_queue_profile_gap_ranking_is_NOT_independence_evidence"] = True
    if len(profile_gaps) + summary["source_ledger_derived_bounded_profiles"] != 60:
        raise InputMismatch("Working 60-profile accounting drift")
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
    (output / "REMAINING_PROFILE_EVIDENCE_QUEUE.json").write_text(
        json.dumps(profile_gaps, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "PRIORITIZED_REVIEW_QUEUE.json").write_text(
        json.dumps([r for r in rows if r["priority"] < 4], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in summary.items()
                      if k not in ("raw_input_sha256",)}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
