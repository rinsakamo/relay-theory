#!/usr/bin/env python3
"""Paper 2 sampling-v2 citation-ranking and eligibility-screening apparatus.

Owner: #167

This module does not authorize real work selection. It provides:
- provider-side era ranking acquisition under the frozen retrieval-v1 union;
- complete boundary citation-tie closure;
- local canonical ordering by citation count then OpenAlex Work ID;
- deterministic Top50 calibration exclusion;
- eligibility screening-template validation and first-k INCLUDE selection.

No decomposition field is accepted or emitted.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper2_openalex_enumerate as retrieval  # type: ignore
import paper2_sampling_v2 as sampling  # type: ignore

RANKING_SCHEMA = "paper2-sampling-v2-ranking-v1"
RANK_MANIFEST_SCHEMA = "paper2-sampling-v2-ranked-era-v1"
SCREENING_SCHEMA = "paper2-sampling-v2-screening-v1"

ALLOWED_STATES = {
    "UNSCREENED",
    "INCLUDE",
    "EXCLUDE",
    "ELIGIBILITY_UNCERTAIN",
    "SOURCE_INACCESSIBLE",
    "CALIBRATION_EXCLUDED",
}
TERMINAL_PRESTOP = ALLOWED_STATES - {"UNSCREENED"}
EXCLUSION_REASON_CODES = {
    "X1_TASK_USE_ONLY",
    "X2_COVARIATE_OR_SCORE_ONLY",
    "X3_LOCAL_ASSOCIATION_ONLY",
    "X4_APPLIED_OUTCOME_ONLY",
    "X5_IMPLEMENTATION_ONLY_NO_GENERAL_CLAIM",
    "X6_TERMINOLOGY_MATCH_ONLY",
    "X7_NO_INSPECTABLE_CLAIM",
    "N5_PURE_FORMALISM_WITHOUT_FUNCTIONAL_CAPACITY_CLAIM",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def normalize_doi(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if text.startswith(prefix):
            text = text[len(prefix):]
            break
    return text.rstrip("/") or None


def canonical_work_id(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("candidate missing OpenAlex Work ID")
    text = value.strip()
    if "/" in text:
        text = text.rsplit("/", 1)[-1]
    if not re.fullmatch(r"W\d+", text):
        raise ValueError(f"invalid OpenAlex Work ID: {value!r}")
    return text


def load_ranking_contract(path: Path) -> dict[str, Any]:
    value = load_json(path)
    if value.get("schema_version") != RANKING_SCHEMA:
        raise ValueError("unexpected ranking schema_version")
    surface = value.get("ranking_surface", {})
    if surface.get("provider") != "OpenAlex":
        raise ValueError("ranking provider must remain OpenAlex")
    if surface.get("provider_sort") != "cited_by_count:desc":
        raise ValueError("provider ranking sort drift")
    if surface.get("provider_page_size") != 100:
        raise ValueError("provider page size must remain 100")
    if surface.get("transport_attempts_per_request") != 1:
        raise ValueError("ranking transport attempts must remain exactly one")
    if surface.get("cursor_paging") is not True:
        raise ValueError("ranking acquisition must use cursor paging")
    if surface.get("complete_boundary_citation_tie") is not True:
        raise ValueError("boundary citation tie closure must remain enabled")
    ladder = value.get("candidate_ladder", {})
    if ladder.get("multiplier") != 5:
        raise ValueError("candidate ladder multiplier must remain 5")
    reserve = value.get("reserve", {})
    if reserve.get("post_freeze_replacement_limit") != 0:
        raise ValueError("post-freeze replacement limit must remain zero")
    if value.get("real_ranking_execution_authorized") is not False:
        raise ValueError("real ranking execution must remain blocked in apparatus contract")
    if value.get("real_eligibility_screening_authorized") is not False:
        raise ValueError("real eligibility screening must remain blocked in apparatus contract")
    return value


def era_conditions(era_freeze: dict[str, Any]) -> dict[str, str]:
    order = era_freeze["era_policy"]["frozen_order"]
    out: dict[str, str] = {}
    for era in order:
        if era == "PRE_1950":
            out[era] = "year <= (1949)"
            continue
        m = re.fullmatch(r"(\d{4})-(\d{4})", era)
        if not m:
            raise ValueError(f"unsupported frozen era label: {era}")
        lo, hi = int(m.group(1)), int(m.group(2))
        out[era] = f"year >= ({lo}) and year <= ({hi})"
    return out


def quota_map(era_freeze: dict[str, Any]) -> dict[str, int]:
    return {
        row["era"]: int(row["quota_k_d"])
        for row in era_freeze["primary_allocation"]["eras"]
    }


def seed_registry(retrieval_config: dict[str, Any]) -> list[dict[str, Any]]:
    seeds = retrieval_config.get("seeds")
    if not isinstance(seeds, list) or len(seeds) != 50:
        raise ValueError("retrieval-v1 must contain exactly 50 calibration seeds")
    out = []
    for seed in seeds:
        number = int(seed["number"])
        title = retrieval.normalize_title(str(seed["title"]))
        year = int(seed["year"])
        out.append(
            {
                "number": number,
                "title_norm": title,
                "year": year,
                "doi_norm": normalize_doi(seed.get("doi")),
            }
        )
    if [row["number"] for row in out] != list(range(1, 51)):
        raise ValueError("Top50 seed numbering/order drift")
    return out


def calibration_match(
    candidate: dict[str, Any],
    seeds: list[dict[str, Any]],
) -> tuple[int | None, str | None]:
    doi = normalize_doi(candidate.get("doi"))
    title = retrieval.normalize_title(str(candidate.get("title") or ""))
    year = int(candidate["year"])

    doi_hits = [
        seed for seed in seeds
        if doi is not None and seed["doi_norm"] is not None and doi == seed["doi_norm"]
    ]
    if len(doi_hits) > 1:
        raise ValueError("candidate DOI matches multiple Top50 seeds")
    if doi_hits:
        return int(doi_hits[0]["number"]), "DOI"

    title_hits = [
        seed for seed in seeds
        if seed["year"] == year and seed["title_norm"] == title
    ]
    if len(title_hits) > 1:
        raise ValueError("candidate title/year matches multiple Top50 seeds")
    if title_hits:
        return int(title_hits[0]["number"]), "TITLE_YEAR"
    return None, None


def normalize_provider_item(item: dict[str, Any]) -> dict[str, Any]:
    work_id = canonical_work_id(item.get("id"))
    title = item.get("display_name")
    if not isinstance(title, str) or not title.strip():
        raise ValueError(f"{work_id}: missing display_name")
    year = item.get("publication_year")
    if not isinstance(year, int):
        raise ValueError(f"{work_id}: missing integer publication_year")
    citations = item.get("cited_by_count")
    if not isinstance(citations, int) or citations < 1:
        raise ValueError(f"{work_id}: cited_by_count violates frozen citation floor")
    work_type = item.get("type")
    if work_type is not None and not isinstance(work_type, str):
        raise ValueError(f"{work_id}: invalid type")
    return {
        "provider_work_id": work_id,
        "doi": normalize_doi(item.get("doi")),
        "title": title,
        "year": year,
        "cited_by_count": citations,
        "type": work_type,
    }


def freeze_rank_rows(
    provider_rows: list[dict[str, Any]],
    *,
    minimum_rows: int,
    seeds: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    if minimum_rows < 1:
        raise ValueError("minimum_rows must be positive")
    if len(provider_rows) < minimum_rows:
        raise ValueError("provider rows do not reach required candidate ladder depth")

    normalized = [normalize_provider_item(row) for row in provider_rows]
    seen: set[str] = set()
    previous_citations: int | None = None
    for row in normalized:
        work_id = row["provider_work_id"]
        if work_id in seen:
            raise ValueError(f"duplicate provider Work ID during ranking transaction: {work_id}")
        seen.add(work_id)
        current = int(row["cited_by_count"])
        if previous_citations is not None and current > previous_citations:
            raise ValueError(
                "RANK_PROVIDER_ORDER_DRIFT: citation count increased across provider order"
            )
        previous_citations = current

    boundary = int(normalized[minimum_rows - 1]["cited_by_count"])
    if not any(int(row["cited_by_count"]) < boundary for row in normalized[minimum_rows:]):
        raise ValueError(
            "RANK_BOUNDARY_TIE_NOT_CLOSED: provider rows stop before observing a lower citation count"
        )

    kept = [row for row in normalized if int(row["cited_by_count"]) >= boundary]
    kept.sort(key=lambda row: (-int(row["cited_by_count"]), row["provider_work_id"]))

    out: list[dict[str, Any]] = []
    for rank, row in enumerate(kept, start=1):
        seed_number, match_basis = calibration_match(row, seeds)
        state = "CALIBRATION_EXCLUDED" if seed_number is not None else "UNSCREENED"
        out.append(
            {
                "rank": rank,
                **row,
                "calibration_seed_number": seed_number,
                "calibration_match_basis": match_basis,
                "screening_state": state,
                "source_locator": None,
                "claim_span_locators": [],
                "generalization": None,
                "operational_fields": [],
                "reason_codes": [],
                "classifier_version": "paper2-eligibility-v1.1",
            }
        )
    return out, boundary


def fetch_ranked_era(
    client: retrieval.OpenAlexClient,
    *,
    union_oql: str,
    era: str,
    condition: str,
    minimum_rows: int,
    seeds: list[dict[str, Any]],
    page_size: int = 100,
) -> dict[str, Any]:
    query = sampling.append_filter(union_oql, condition)
    started_at = retrieval.utc_now()
    cursor: str | None = "*"
    provider_rows: list[dict[str, Any]] = []
    page_count = 0
    meta_counts: list[int] = []
    boundary: int | None = None
    tie_closed = False

    while cursor:
        body = {
            "oql": query,
            "sort": "cited_by_count:desc",
            "select": "id,doi,display_name,publication_year,cited_by_count,type",
            "per_page": page_size,
            "cursor": cursor,
        }
        payload = client.request_json(
            retrieval.API_ROOT,
            method="POST",
            body=body,
            retries=1,
        )
        results = payload.get("results")
        if not isinstance(results, list):
            raise ValueError("ranking provider response missing results list")
        provider_rows.extend(row for row in results if isinstance(row, dict))
        meta = payload.get("meta") or {}
        meta_count = int(meta.get("count", -1))
        if meta_count < 0:
            raise ValueError("ranking provider response missing nonnegative meta.count")
        meta_counts.append(meta_count)
        page_count += 1

        # Validate enough structure to find the tie boundary while paging.
        partial = [normalize_provider_item(row) for row in provider_rows]
        seen: set[str] = set()
        prev: int | None = None
        for row in partial:
            wid = row["provider_work_id"]
            if wid in seen:
                raise ValueError(
                    f"RANK_PROVIDER_DUPLICATE_ID: duplicate Work ID {wid}"
                )
            seen.add(wid)
            current = int(row["cited_by_count"])
            if prev is not None and current > prev:
                raise ValueError(
                    "RANK_PROVIDER_ORDER_DRIFT: citation count increased across provider pages"
                )
            prev = current

        if len(partial) >= minimum_rows:
            boundary = int(partial[minimum_rows - 1]["cited_by_count"])
            if any(
                int(row["cited_by_count"]) < boundary
                for row in partial[minimum_rows:]
            ):
                tie_closed = True
                break

        cursor = meta.get("next_cursor")
        if cursor is None:
            # End-of-results itself closes the boundary tie if minimum depth exists.
            if len(partial) >= minimum_rows:
                tie_closed = True
                break
        if page_count > 100:
            raise RuntimeError("ranking transaction exceeded 100 pages unexpectedly")

    if not tie_closed or boundary is None:
        raise RuntimeError("RANK_BOUNDARY_TIE_NOT_CLOSED")

    # If end-of-results closed the tie without a lower row, append a synthetic
    # one-row sentinel only to satisfy freeze_rank_rows' closure check, then drop it.
    normalized_all = [normalize_provider_item(row) for row in provider_rows]
    lower_exists = any(
        int(row["cited_by_count"]) < boundary
        for row in normalized_all[minimum_rows:]
    )
    if lower_exists:
        frozen_rows, checked_boundary = freeze_rank_rows(
            provider_rows, minimum_rows=minimum_rows, seeds=seeds
        )
    else:
        # Entire era result set ends at the boundary citation count. In that case
        # every remaining tied row is already present, so local freeze is direct.
        kept = [
            row for row in normalized_all
            if int(row["cited_by_count"]) >= boundary
        ]
        kept.sort(key=lambda row: (-int(row["cited_by_count"]), row["provider_work_id"]))
        frozen_rows = []
        for rank, row in enumerate(kept, start=1):
            seed_number, match_basis = calibration_match(row, seeds)
            frozen_rows.append(
                {
                    "rank": rank,
                    **row,
                    "calibration_seed_number": seed_number,
                    "calibration_match_basis": match_basis,
                    "screening_state": (
                        "CALIBRATION_EXCLUDED" if seed_number is not None else "UNSCREENED"
                    ),
                    "source_locator": None,
                    "claim_span_locators": [],
                    "generalization": None,
                    "operational_fields": [],
                    "reason_codes": [],
                    "classifier_version": "paper2-eligibility-v1.1",
                }
            )
        checked_boundary = boundary

    return {
        "schema_version": RANK_MANIFEST_SCHEMA,
        "owner_issue": 167,
        "provider": "OpenAlex",
        "era": era,
        "era_condition": condition,
        "transaction_started_at": started_at,
        "transaction_completed_at": retrieval.utc_now(),
        "provider_sort": "cited_by_count:desc",
        "local_canonical_sort": "cited_by_count desc, provider_work_id asc",
        "provider_page_size": page_size,
        "transport_attempts_per_request": 1,
        "provider_pages": page_count,
        "provider_meta_count_first": meta_counts[0],
        "provider_meta_count_last": meta_counts[-1],
        "provider_meta_count_signed_drift": meta_counts[-1] - meta_counts[0],
        "minimum_candidate_rows": minimum_rows,
        "boundary_cited_by_count": checked_boundary,
        "boundary_tie_closed": True,
        "frozen_row_count": len(frozen_rows),
        "rows": frozen_rows,
    }


def validate_screening(
    ranked: dict[str, Any],
    *,
    quota: int,
) -> dict[str, Any]:
    if ranked.get("schema_version") != RANK_MANIFEST_SCHEMA:
        raise ValueError("unexpected ranked-era schema")
    rows = ranked.get("rows")
    if not isinstance(rows, list):
        raise ValueError("ranked-era manifest missing rows")

    seen: set[str] = set()
    previous_key: tuple[int, str] | None = None
    selected: list[str] = []
    stop_rank: int | None = None
    audit: list[dict[str, Any]] = []

    for index, row in enumerate(rows, start=1):
        if row.get("rank") != index:
            raise ValueError("ranking row numbers must be contiguous")
        work_id = canonical_work_id(row.get("provider_work_id"))
        if work_id in seen:
            raise ValueError("screening manifest contains duplicate Work ID")
        seen.add(work_id)
        key = (-int(row["cited_by_count"]), work_id)
        if previous_key is not None and key < previous_key:
            raise ValueError("screening manifest canonical order drift")
        previous_key = key

        state = row.get("screening_state")
        if state not in ALLOWED_STATES:
            raise ValueError(f"invalid screening_state: {state!r}")

        is_calibration = row.get("calibration_seed_number") is not None
        if is_calibration and state != "CALIBRATION_EXCLUDED":
            raise ValueError("Top50 calibration row must remain CALIBRATION_EXCLUDED")
        if not is_calibration and state == "CALIBRATION_EXCLUDED":
            raise ValueError("non-calibration row cannot be CALIBRATION_EXCLUDED")

        if stop_rank is None:
            if state == "UNSCREENED":
                raise ValueError(
                    "all rows before primary quota stop must have terminal screening state"
                )
            if state == "EXCLUDE":
                codes = row.get("reason_codes")
                if (
                    not isinstance(codes, list)
                    or not codes
                    or any(code not in EXCLUSION_REASON_CODES for code in codes)
                ):
                    raise ValueError("EXCLUDE row must carry frozen eligibility reason code(s)")
            if state == "INCLUDE":
                selected.append(work_id)
                if len(selected) == quota:
                    stop_rank = index
        else:
            if is_calibration:
                if state != "CALIBRATION_EXCLUDED":
                    raise AssertionError("calibration invariant")
            elif state != "UNSCREENED":
                raise ValueError(
                    "non-calibration rows after quota stop must remain UNSCREENED"
                )
        audit.append(
            {
                "rank": index,
                "provider_work_id": work_id,
                "screening_state": state,
                "selected_primary": work_id in selected,
            }
        )

    if stop_rank is None or len(selected) != quota:
        raise ValueError(
            "ERA_SCREENING_LADDER_EXHAUSTED: frozen candidate ladder did not yield quota"
        )

    # Recompute selected_primary exactly: membership alone is insufficient if
    # malformed duplicate IDs somehow entered earlier (already forbidden).
    selected_set = set(selected)
    for row in audit:
        row["selected_primary"] = (
            row["rank"] <= stop_rank and row["provider_work_id"] in selected_set
        )

    return {
        "schema_version": SCREENING_SCHEMA,
        "owner_issue": 167,
        "era": ranked["era"],
        "primary_quota": quota,
        "primary_stop_rank": stop_rank,
        "primary_work_ids": selected,
        "post_freeze_replacement_limit": 0,
        "audit": audit,
    }


def self_test() -> None:
    contract = load_ranking_contract(Path("research/paper2/sampling_v2_ranking.json"))
    protocol = sampling.load_protocol(Path("research/paper2/sampling_v2.json"))
    era_freeze = sampling.validate_era_freeze(protocol)
    retrieval_config = load_json(Path("research/paper2/retrieval_v1.json"))
    seeds = seed_registry(retrieval_config)

    quotas = quota_map(era_freeze)
    assert sum(quotas.values()) == 1000
    assert contract["candidate_ladder"]["multiplier"] == 5
    assert {
        era: 5 * quota for era, quota in quotas.items()
    }["2020-2026"] == 970

    conditions = era_conditions(era_freeze)
    assert conditions["PRE_1950"] == "year <= (1949)"
    assert conditions["1950-1959"] == "year >= (1950) and year <= (1959)"
    assert conditions["2020-2026"] == "year >= (2020) and year <= (2026)"

    # Boundary tie closure + local Work-ID tiebreak.
    provider_rows = [
        {
            "id": "https://openalex.org/W9",
            "doi": None,
            "display_name": "A",
            "publication_year": 2000,
            "cited_by_count": 100,
            "type": "article",
        },
        {
            "id": "https://openalex.org/W3",
            "doi": None,
            "display_name": "B",
            "publication_year": 2000,
            "cited_by_count": 80,
            "type": "article",
        },
        {
            "id": "https://openalex.org/W2",
            "doi": None,
            "display_name": "C",
            "publication_year": 2000,
            "cited_by_count": 80,
            "type": "article",
        },
        {
            "id": "https://openalex.org/W8",
            "doi": None,
            "display_name": "D",
            "publication_year": 2000,
            "cited_by_count": 80,
            "type": "article",
        },
        {
            "id": "https://openalex.org/W7",
            "doi": None,
            "display_name": "E",
            "publication_year": 2000,
            "cited_by_count": 79,
            "type": "article",
        },
    ]
    frozen, boundary = freeze_rank_rows(provider_rows, minimum_rows=3, seeds=seeds)
    assert boundary == 80
    assert [row["provider_work_id"] for row in frozen] == ["W9", "W2", "W3", "W8"]

    # Calibration exclusion: DOI-first and title/year fallback.
    simon = {
        "doi": "https://doi.org/10.2307/1884852",
        "title": "irrelevant provider title",
        "year": 1955,
    }
    assert calibration_match(simon, seeds) == (2, "DOI")
    hebb = {
        "doi": None,
        "title": "The Organization of Behavior: A Neuropsychological Theory",
        "year": 1949,
    }
    assert calibration_match(hebb, seeds) == (31, "TITLE_YEAR")

    # Screening quota and attrition behavior.
    ranked = {
        "schema_version": RANK_MANIFEST_SCHEMA,
        "era": "TEST",
        "rows": [
            {
                "rank": 1,
                "provider_work_id": "W1",
                "cited_by_count": 100,
                "screening_state": "CALIBRATION_EXCLUDED",
                "calibration_seed_number": 1,
                "reason_codes": [],
            },
            {
                "rank": 2,
                "provider_work_id": "W2",
                "cited_by_count": 90,
                "screening_state": "EXCLUDE",
                "calibration_seed_number": None,
                "reason_codes": ["X1_TASK_USE_ONLY"],
            },
            {
                "rank": 3,
                "provider_work_id": "W3",
                "cited_by_count": 80,
                "screening_state": "INCLUDE",
                "calibration_seed_number": None,
                "reason_codes": [],
            },
            {
                "rank": 4,
                "provider_work_id": "W4",
                "cited_by_count": 70,
                "screening_state": "SOURCE_INACCESSIBLE",
                "calibration_seed_number": None,
                "reason_codes": [],
            },
            {
                "rank": 5,
                "provider_work_id": "W5",
                "cited_by_count": 60,
                "screening_state": "INCLUDE",
                "calibration_seed_number": None,
                "reason_codes": [],
            },
            {
                "rank": 6,
                "provider_work_id": "W6",
                "cited_by_count": 50,
                "screening_state": "UNSCREENED",
                "calibration_seed_number": None,
                "reason_codes": [],
            },
        ],
    }
    screening = validate_screening(ranked, quota=2)
    assert screening["primary_stop_rank"] == 5
    assert screening["primary_work_ids"] == ["W3", "W5"]
    assert screening["post_freeze_replacement_limit"] == 0

    # Reject post-stop source inspection.
    bad = json.loads(json.dumps(ranked))
    bad["rows"][5]["screening_state"] = "INCLUDE"
    try:
        validate_screening(bad, quota=2)
        raise AssertionError("post-stop adjudication must fail")
    except ValueError as exc:
        assert "after quota stop" in str(exc)

    # Reject Top50 leakage.
    bad2 = json.loads(json.dumps(ranked))
    bad2["rows"][0]["screening_state"] = "INCLUDE"
    try:
        validate_screening(bad2, quota=2)
        raise AssertionError("Top50 leakage must fail")
    except ValueError as exc:
        assert "CALIBRATION_EXCLUDED" in str(exc)

    print("PAPER2_SAMPLING_V2_RANKING_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ranking-contract",
        type=Path,
        default=Path("research/paper2/sampling_v2_ranking.json"),
    )
    parser.add_argument(
        "--sampling-protocol",
        type=Path,
        default=Path("research/paper2/sampling_v2.json"),
    )
    parser.add_argument(
        "--era-freeze",
        type=Path,
        default=Path("research/paper2/sampling_v2_era_freeze.json"),
    )
    parser.add_argument(
        "--retrieval-config",
        type=Path,
        default=Path("research/paper2/retrieval_v1.json"),
    )
    parser.add_argument("--counts-artifact", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--era")
    parser.add_argument("--fetch-ranked-era", action="store_true")
    parser.add_argument("--validate-screening", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pause", type=float, default=0.12)
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    contract = load_ranking_contract(args.ranking_contract)
    protocol = sampling.load_protocol(args.sampling_protocol)
    era_freeze = sampling.validate_era_freeze(protocol, args.era_freeze)
    retrieval_config = load_json(args.retrieval_config)
    seeds = seed_registry(retrieval_config)
    quotas = quota_map(era_freeze)

    if args.fetch_ranked_era:
        if contract.get("real_ranking_execution_authorized") is not True:
            raise RuntimeError(
                "REAL_RANKING_EXECUTION_NOT_AUTHORIZED: apparatus contract remains synthetic-only"
            )
        if not args.era or args.era not in quotas:
            raise ValueError("--fetch-ranked-era requires one frozen --era")
        if args.counts_artifact is None:
            raise ValueError("--fetch-ranked-era requires --counts-artifact")
        frozen_counts = sampling.validate_counts_artifact(args.counts_artifact)
        conditions = era_conditions(era_freeze)
        multiplier = int(contract["candidate_ladder"]["multiplier"])
        client = retrieval.OpenAlexClient(
            api_key=None,
            mailto=None,
            pause=args.pause,
        )
        result = fetch_ranked_era(
            client,
            union_oql=frozen_counts["union_oql"],
            era=args.era,
            condition=conditions[args.era],
            minimum_rows=multiplier * quotas[args.era],
            seeds=seeds,
        )
    elif args.validate_screening is not None:
        ranked = load_json(args.validate_screening)
        era = ranked.get("era")
        if era not in quotas:
            raise ValueError("screening manifest era is not frozen")
        result = validate_screening(ranked, quota=quotas[str(era)])
    else:
        parser.error("choose --self-test, --fetch-ranked-era, or --validate-screening")
        return 2

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
