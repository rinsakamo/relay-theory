#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROFILES = json.loads((ROOT / "W6_SOURCE_NATIVE_PROFILE_FRAGMENTS_v1.json").read_text(encoding="utf-8"))
PAIRS = json.loads((ROOT / "W6_BOUNDED_PAIR_ADJUDICATIONS_v1.json").read_text(encoding="utf-8"))
GAPS = json.loads((ROOT / "W6_SOURCE_GAPS_AND_BLOCKERS_v1.json").read_text(encoding="utf-8"))
PROV = json.loads((ROOT / "W6_GIT_PROVENANCE_RECEIPT_v1.json").read_text(encoding="utf-8"))

EXPECTED_DOIS = {
    "INT-13": "10.1371/journal.pcbi.1014796",
    "INT-14": "10.1371/journal.pcbi.1007594",
    "INT-15": "10.1371/journal.pcbi.1010047",
    "INT-16": "10.1371/journal.pcbi.1004060",
}
ALLOWED_STATUSES = {
    "PROFILE_FRAGMENT_READY",
    "SOURCE_BLOCKED",
    "SCIENTIFIC_ANCESTRY_UNDERDETERMINED",
}
ALLOWED_PAIR = {
    "DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY",
    "SHARED_CONSTITUENT_ONLY",
    "BOUNDED_SOURCE_NATIVE_DIFFERENCE",
    "UNDERDETERMINED",
}
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def profile_map():
    rows = PROFILES["profiles"]
    ids = [r["id"] for r in rows]
    assert len(rows) == 4
    assert len(ids) == len(set(ids))
    assert {r["id"]: r["doi"] for r in rows} == EXPECTED_DOIS
    return {r["id"]: r for r in rows}


def pair_map():
    rows = PAIRS["adjudications"]
    ids = [r["pair_id"] for r in rows]
    assert len(rows) == 110
    assert len(ids) == len(set(ids))
    assert all(r["adjudication"] in ALLOWED_PAIR for r in rows)
    return {r["pair_id"]: r for r in rows}


def get_pair(rows, a, b):
    key = "×".join(sorted((a, b)))
    assert key in rows
    return rows[key]


def walk_key(obj, key):
    if isinstance(obj, dict):
        if key in obj:
            yield obj[key]
        for value in obj.values():
            yield from walk_key(value, key)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk_key(value, key)


def test_exact_four_doi_identities_and_completion_states():
    profiles = profile_map()
    assert all(p["completion_status"] in ALLOWED_STATUSES for p in profiles.values())
    assert all(p["completion_status"] == "PROFILE_FRAGMENT_READY" for p in profiles.values())


def test_operator_ids_are_unique_and_paper_local():
    profiles = profile_map()
    all_ops = []
    for ident, p in profiles.items():
        ops = p["native_core_operators"]
        assert len(ops) == len(set(ops))
        assert all(op.startswith(ident + ":") for op in ops)
        assert set(p["operator_source_descriptions"]) == set(ops)
        all_ops.extend(ops)
    assert len(all_ops) == len(set(all_ops))


def test_int13_cannot_be_silently_promoted_to_corrected_final_vor():
    p = profile_map()["INT-13"]
    edition = p["adopted_edition"]
    assert edition["status"] == "AUTHOR_APPROVED_FROZEN_PUBLISHER_UNCORRECTED_PROOF"
    assert edition["final_corrected_vor"] is False
    assert "uncorrected proof" in edition["firstparty_live_recheck_2026_10_05"].lower()
    assert "MISSING_FINAL_CORRECTED_EDITION" in {
        x["kind"] for x in GAPS["papers"][0]["source_gaps"]
    }


def test_int14_crp_is_constituent_not_whole_family_identity():
    row = get_pair(pair_map(), "INT-01", "INT-14")
    assert row["adjudication"] == "SHARED_CONSTITUENT_ONLY"
    assert "CRP" in row["basis"]
    assert row["global_family_independence_certified"] is False
    assert "Whole historical family remains underdetermined" in row["basis"]


def test_int15_p18_bounded_difference_is_not_independence():
    row = get_pair(pair_map(), "INT-15", "P18")
    assert row["adjudication"] == "BOUNDED_SOURCE_NATIVE_DIFFERENCE"
    assert row["evidence_class"] == "REUSED_BOUNDED_SOURCE_WITNESS"
    assert row["global_family_independence_certified"] is False


def test_int16_p09_bounded_difference_is_not_independence():
    row = get_pair(pair_map(), "INT-16", "P09")
    assert row["adjudication"] == "BOUNDED_SOURCE_NATIVE_DIFFERENCE"
    assert row["evidence_class"] == "REUSED_BOUNDED_SOURCE_WITNESS"
    assert row["global_family_independence_certified"] is False


def test_required_existing_bounded_witnesses_are_reused():
    rows = pair_map()
    required = [
        ("INT-01", "INT-13"),
        ("INT-01", "INT-14"),
        ("INT-15", "P18"),
        ("INT-16", "P09"),
    ]
    for a, b in required:
        row = get_pair(rows, a, b)
        assert row["evidence_class"] == "REUSED_BOUNDED_SOURCE_WITNESS"
        assert row["adjudication"] != "UNDERDETERMINED"


def test_pair_denominators_and_fail_closed_counts():
    assert PAIRS["counts"]["pair_count"] == 110
    assert PAIRS["counts"]["reused_bounded_pair_count"] == 5
    assert PAIRS["counts"]["newly_added_bounded_pair_count"] == 6
    assert PAIRS["counts"]["adjudication_counts"] == {
        "UNDERDETERMINED": 99,
        "BOUNDED_SOURCE_NATIVE_DIFFERENCE": 10,
        "SHARED_CONSTITUENT_ONLY": 1,
    }
    assert PAIRS["counts"]["global_family_independence_certified"] == 0


def test_no_global_independence_or_main_authorization_promotion():
    for doc in (PROFILES, PAIRS, GAPS, PROV):
        vals = list(walk_key(doc, "global_family_independence_certified"))
        assert all(v is False or v == 0 for v in vals)
        main_vals = list(walk_key(doc, "main_authorized"))
        assert all(v is False for v in main_vals)


def test_ancestry_exhaustiveness_never_promoted():
    profiles = profile_map()
    assert PROFILES["ancestry_exhaustiveness"] == "NOT_ATTESTED"
    for p in profiles.values():
        assert p["ancestry_exhaustiveness"] == "NOT_ATTESTED"


def test_direct_ancestor_values_are_dois_only():
    for p in profile_map().values():
        for doi in p["direct_model_ancestors"]:
            assert doi.startswith("10.")
            assert " " not in doi
            assert not doi.startswith("DOI:")


def test_exact_git_ref_blob_receipt_is_fail_closed():
    entries = PROV["verified_entries"]
    assert PROV["all_exact_ref_path_blob_checks_passed"] is True
    assert PROV["shared_pr_438_profile_blob_preserved"] is True
    assert len(entries) == 10
    seen = set()
    for e in entries:
        key = (e["ref"], e["path"])
        assert key not in seen
        seen.add(key)
        assert e["verified"] is True
        assert HEX40.fullmatch(e["ref"])
        assert HEX40.fullmatch(e["blob"])
    expected = {
        ("15ee0a2a74b7e47adb439d8b30f499103d1f7eb1",
         "research/paper2/p399/g2/int_g2d/G2D_V15B_SELECTED_INT15_INT16_VS_G1_P18_P09_NATIVE_OPERATOR_BOUNDED_PAIR_AUDIT.json"):
            "63296efe609a52f33e84dc58411c96a20ca62a09",
        ("15ee0a2a74b7e47adb439d8b30f499103d1f7eb1",
         "research/paper2/p399/g2/int_g2d/G2D_V16B_INT01_INT14_FIRSTPARTY_CRP_NATIVE_FAMILY_20261005.json"):
            "609a4fbd32fc832d86910dfa24e797cc6e09cee3",
        ("15ee0a2a74b7e47adb439d8b30f499103d1f7eb1",
         "research/paper2/p399/g2/int_g2d/G2D_V20_INT01_THREE_ADDITIONAL_PAIRS_INT09_OFFICIAL_FIG9_CORRIGENDUM_AND_35_QUEUE.json"):
            "886bed52531abec3457f3b9976f39236b8899007",
        ("ae044a8f475fb0dc9140a91e360e1ff26a0b5e3a",
         "research/paper2/p399/g4/genealogy_accelerator_v1/ORIGINAL_NATIVE_PROFILES_v1.json"):
            "903f8db6e1569ed27507cf47e668f7599a08cd98",
    }
    got = {(e["ref"], e["path"]): e["blob"] for e in entries}
    for key, blob in expected.items():
        assert got[key] == blob


def test_shared_profile_and_main_science_are_declared_untouched():
    assert PROFILES["authority"]["shared_profile_file_modified"] is False
    assert PROFILES["authority"]["main_science_performed"] is False
    assert PAIRS["authority"]["shared_pair_matrix_modified"] is False
    assert PAIRS["authority"]["main_science_performed"] is False
    assert "The shared 26-profile accelerator file remains untouched; integration has not occurred." in GAPS["global_blockers"]
