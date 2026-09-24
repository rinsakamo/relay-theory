#!/usr/bin/env python3
"""Paper 2 sampling-v2 sourcewise exact-union citation ranking.

Owner: #167

This version repairs the direct-union provider failure without changing the
frozen retrieval frame. It ranks each of the 51 frozen R1/R2/R3 source sets
separately, closes the citation tie at each source-local L boundary, unions and
deduplicates those prefixes, then computes the global citation-ranked ladder.

Under a static provider state this is exact: a work in the global top L of a
union must appear in the top L of at least one source set that contains it.
OpenAlex is live, so duplicate Work IDs observed with different citation counts
fail closed rather than being silently reconciled.

No eligibility/source-text adjudication, ClaimIR, decomposition, or null-control
execution is performed here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper2_openalex_enumerate as retrieval  # type: ignore
import paper2_openalex_manifest as manifest  # type: ignore
import paper2_sampling_v2 as sampling  # type: ignore
import paper2_sampling_v2_rank as rankv1  # type: ignore

SCHEMA_VERSION = "paper2-sampling-v2-ranking-sourcewise-v2"
RANKED_ERA_SCHEMA = "paper2-sampling-v2-ranked-era-sourcewise-v2"
SOURCE_PREFIX_SCHEMA = "paper2-sampling-v2-source-prefix-v2"
PAGE_SIZE = 100
MAX_BASIC_ROWS = 10_000


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_contract(path: Path) -> dict[str, Any]:
    value = load_json(path)
    if value.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unexpected sourcewise ranking schema_version")
    sources = value.get("retrieval_sources", {})
    if sources.get("source_count") != 51:
        raise ValueError("sourcewise ranking must retain exactly 51 frozen sources")
    surface = value.get("ranking_surface", {})
    if surface.get("provider") != "OpenAlex":
        raise ValueError("sourcewise ranking provider must remain OpenAlex")
    if surface.get("provider_sort") != "cited_by_count:desc":
        raise ValueError("sourcewise provider sort drift")
    if surface.get("provider_page_size") != PAGE_SIZE:
        raise ValueError("sourcewise page size drift")
    if surface.get("paging") != "basic_page":
        raise ValueError("sourcewise ranking must use basic page retrieval")
    if surface.get("basic_page_row_limit") != MAX_BASIC_ROWS:
        raise ValueError("sourcewise basic paging row-limit drift")
    if surface.get("transport_attempts_per_request") != 1:
        raise ValueError("sourcewise transport attempts must remain exactly one")
    if surface.get("complete_source_boundary_citation_tie") is not True:
        raise ValueError("source-local boundary tie closure must remain enabled")
    if surface.get("complete_global_boundary_citation_tie") is not True:
        raise ValueError("global boundary tie closure must remain enabled")
    ladder = value.get("candidate_ladder", {})
    if ladder.get("multiplier") != 5:
        raise ValueError("sourcewise candidate ladder multiplier must remain 5")
    execution = value.get("execution_protocol", {})
    if execution.get("granularity") != "one frozen source prefix per provider transaction, then local-only era merge":
        raise ValueError("sourcewise execution granularity drift")
    if execution.get("source_artifact_persistence") != "atomic JSON write after each successful source":
        raise ValueError("sourcewise source-artifact persistence drift")
    if execution.get("integrated_51_source_provider_run") != "DISABLED":
        raise ValueError("integrated 51-source provider run must remain disabled")
    if execution.get("merge_requires_all_51_sources") is not True:
        raise ValueError("local era merge must require all 51 sources")
    if execution.get("merge_provider_calls") != 0:
        raise ValueError("local era merge must perform zero provider calls")
    if value.get("real_eligibility_screening_authorized") is not False:
        raise ValueError("real eligibility screening must remain blocked")
    status = value.get("status")
    authorized = value.get("real_ranking_execution_authorized")
    if status == "APPARATUS_ONLY_REAL_EXECUTION_NOT_AUTHORIZED":
        if authorized is not False:
            raise ValueError("synthetic-only sourcewise contract must not authorize real ranking")
    elif status == "REAL_SOURCEWISE_RANKING_EXECUTION_AUTHORIZED_ELIGIBILITY_NOT_AUTHORIZED":
        if authorized is not True:
            raise ValueError("sourcewise ranking authorization/status mismatch")
    else:
        raise ValueError("unknown sourcewise ranking authorization state")
    return value


def source_id(spec: dict[str, Any]) -> str:
    channel = str(spec["channel"])
    index = int(spec["source_index"])
    if channel == "R1":
        if index != 0:
            raise ValueError("R1 source index drift")
        return "R1-001"
    if channel == "R2":
        return f"R2-{index + 1:03d}"
    if channel == "R3":
        return f"R3-{index + 1:03d}"
    raise ValueError(f"unknown source channel: {channel}")


def build_sources(
    retrieval_config: dict[str, Any],
    counts_artifact: dict[str, Any],
) -> list[dict[str, Any]]:
    topics = manifest.validate_counts_artifact(counts_artifact, retrieval_config)
    specs = manifest.source_specs(retrieval_config, topics)
    if len(specs) != 51:
        raise ValueError(f"expected 51 frozen retrieval sources, got {len(specs)}")
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for spec in specs:
        sid = source_id(spec)
        if sid in seen:
            raise ValueError(f"duplicate frozen source id: {sid}")
        seen.add(sid)
        out.append(
            {
                **spec,
                "source_id": sid,
                "query_digest": sha256_text(str(spec["query"])),
            }
        )
    return out


def normalize_item(item: dict[str, Any]) -> dict[str, Any]:
    return rankv1.normalize_provider_item(item)


def validate_provider_order(rows: list[dict[str, Any]], *, source: str) -> None:
    seen: set[str] = set()
    previous: int | None = None
    for row in rows:
        wid = row["provider_work_id"]
        if wid in seen:
            raise RuntimeError(f"SOURCE_DUPLICATE_WORK_ID:{source}:{wid}")
        seen.add(wid)
        current = int(row["cited_by_count"])
        if previous is not None and current > previous:
            raise RuntimeError(f"SOURCE_NONMONOTONE_CITATION_ORDER:{source}")
        previous = current


def source_prefix_from_rows(
    rows: list[dict[str, Any]],
    *,
    L: int,
    source: str,
    exhausted: bool,
) -> tuple[list[dict[str, Any]], int | None]:
    """Freeze one source-local top-L prefix with complete citation tie."""
    if L < 1:
        raise ValueError("L must be positive")
    validate_provider_order(rows, source=source)
    if not rows:
        if not exhausted:
            raise RuntimeError(f"SOURCE_PREFIX_INCOMPLETE:{source}")
        return [], None

    if len(rows) < L:
        if not exhausted:
            raise RuntimeError(f"SOURCE_PREFIX_INCOMPLETE:{source}")
        return list(rows), int(rows[-1]["cited_by_count"])

    boundary = int(rows[L - 1]["cited_by_count"])
    lower_seen = any(int(row["cited_by_count"]) < boundary for row in rows[L:])
    if not lower_seen and not exhausted:
        raise RuntimeError(f"SOURCE_BOUNDARY_TIE_NOT_CLOSED:{source}")
    kept = [row for row in rows if int(row["cited_by_count"]) >= boundary]
    return kept, boundary


def fetch_source_prefix(
    client: retrieval.OpenAlexClient,
    *,
    query: str,
    era_condition: str,
    source: str,
    L: int,
) -> dict[str, Any]:
    era_query = sampling.append_filter(query, era_condition)
    started_at = retrieval.utc_now()
    raw: list[dict[str, Any]] = []
    meta_counts: list[int] = []
    page = 1
    exhausted = False

    while True:
        if page * PAGE_SIZE > MAX_BASIC_ROWS:
            raise RuntimeError(f"SOURCE_BOUNDARY_TIE_EXCEEDS_BASIC_PAGING_LIMIT:{source}")

        payload = client.request_json(
            retrieval.API_ROOT,
            method="POST",
            body={
                "oql": era_query,
                "sort": "cited_by_count:desc",
                "select": "id,doi,display_name,publication_year,cited_by_count,type",
                "per_page": PAGE_SIZE,
                "page": page,
            },
            retries=1,
        )
        results = payload.get("results")
        meta = payload.get("meta") or {}
        if not isinstance(results, list):
            raise RuntimeError(f"SOURCE_PROVIDER_RESULTS_MALFORMED:{source}")
        count = int(meta.get("count", -1))
        if count < 0:
            raise RuntimeError(f"SOURCE_PROVIDER_COUNT_MALFORMED:{source}")
        meta_counts.append(count)

        normalized = [normalize_item(row) for row in results if isinstance(row, dict)]
        if len(normalized) != len(results):
            raise RuntimeError(f"SOURCE_PROVIDER_ROW_MALFORMED:{source}")
        raw.extend(normalized)
        validate_provider_order(raw, source=source)

        if len(results) < PAGE_SIZE or len(raw) >= count:
            exhausted = True

        if len(raw) >= L:
            boundary = int(raw[L - 1]["cited_by_count"])
            if any(int(row["cited_by_count"]) < boundary for row in raw[L:]):
                break
            if exhausted:
                break
        elif exhausted:
            break

        page += 1
        if page > 100:
            raise RuntimeError(f"SOURCE_PAGING_LIMIT_EXCEEDED:{source}")

    frozen, boundary = source_prefix_from_rows(
        raw, L=L, source=source, exhausted=exhausted
    )
    return {
        "source_id": source,
        "query_digest": sha256_text(era_query),
        "transaction_started_at": started_at,
        "transaction_completed_at": retrieval.utc_now(),
        "pages": page,
        "provider_meta_count_first": meta_counts[0],
        "provider_meta_count_last": meta_counts[-1],
        "provider_meta_count_signed_drift": meta_counts[-1] - meta_counts[0],
        "source_exhausted": exhausted,
        "source_boundary_cited_by_count": boundary,
        "frozen_row_count": len(frozen),
        "rows": frozen,
    }


def merge_source_prefixes(
    prefixes: list[dict[str, Any]],
    *,
    L: int,
    seeds: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    if L < 1:
        raise ValueError("L must be positive")
    by_id: dict[str, dict[str, Any]] = {}
    sources_by_id: dict[str, set[str]] = {}

    for prefix in prefixes:
        sid = str(prefix["source_id"])
        rows = prefix.get("rows")
        if not isinstance(rows, list):
            raise ValueError(f"{sid}: missing prefix rows")
        for row in rows:
            normalized = dict(row)
            wid = rankv1.canonical_work_id(normalized.get("provider_work_id"))
            cited = int(normalized["cited_by_count"])
            if wid in by_id:
                previous = by_id[wid]
                if int(previous["cited_by_count"]) != cited:
                    raise RuntimeError(
                        f"LIVE_DUPLICATE_CITATION_DRIFT:{wid}:"
                        f"{previous['cited_by_count']}!={cited}"
                    )
                for field in ("year", "title", "doi", "type"):
                    if previous.get(field) != normalized.get(field):
                        raise RuntimeError(f"LIVE_DUPLICATE_METADATA_DRIFT:{wid}:{field}")
            else:
                by_id[wid] = normalized
                sources_by_id[wid] = set()
            sources_by_id[wid].add(sid)

    merged = list(by_id.values())
    merged.sort(key=lambda row: (-int(row["cited_by_count"]), row["provider_work_id"]))
    if len(merged) < L:
        raise RuntimeError(
            f"GLOBAL_SOURCEWISE_UNION_TOO_SMALL:{len(merged)}<{L}"
        )

    boundary = int(merged[L - 1]["cited_by_count"])
    kept = [row for row in merged if int(row["cited_by_count"]) >= boundary]
    out: list[dict[str, Any]] = []
    for rank, row in enumerate(kept, start=1):
        seed_number, match_basis = rankv1.calibration_match(row, seeds)
        out.append(
            {
                "rank": rank,
                **row,
                "retrieved_by_sources": sorted(sources_by_id[row["provider_work_id"]]),
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
    return out, boundary


def fetch_ranked_era_sourcewise(
    client: retrieval.OpenAlexClient,
    *,
    sources: list[dict[str, Any]],
    era: str,
    era_condition: str,
    L: int,
    seeds: list[dict[str, Any]],
) -> dict[str, Any]:
    started_at = retrieval.utc_now()
    prefixes: list[dict[str, Any]] = []
    for spec in sources:
        prefixes.append(
            fetch_source_prefix(
                client,
                query=str(spec["query"]),
                era_condition=era_condition,
                source=str(spec["source_id"]),
                L=L,
            )
        )

    rows, global_boundary = merge_source_prefixes(prefixes, L=L, seeds=seeds)
    summaries = [
        {
            key: prefix[key]
            for key in (
                "source_id",
                "query_digest",
                "transaction_started_at",
                "transaction_completed_at",
                "pages",
                "provider_meta_count_first",
                "provider_meta_count_last",
                "provider_meta_count_signed_drift",
                "source_exhausted",
                "source_boundary_cited_by_count",
                "frozen_row_count",
            )
        }
        for prefix in prefixes
    ]
    return {
        "schema_version": RANKED_ERA_SCHEMA,
        "owner_issue": 167,
        "provider": "OpenAlex",
        "ranking_strategy": "sourcewise_exact_union_merge_v2",
        "era": era,
        "era_condition": era_condition,
        "transaction_started_at": started_at,
        "transaction_completed_at": retrieval.utc_now(),
        "provider_sort": "cited_by_count:desc",
        "local_canonical_sort": "cited_by_count desc, provider_work_id asc",
        "provider_page_size": PAGE_SIZE,
        "paging": "basic_page",
        "transport_attempts_per_request": 1,
        "frozen_source_count": len(prefixes),
        "minimum_candidate_rows": L,
        "global_boundary_cited_by_count": global_boundary,
        "global_boundary_tie_closed": True,
        "frozen_row_count": len(rows),
        "source_summaries": summaries,
        "rows": rows,
    }


def synthetic_prefix(
    source: str,
    full_rows: list[dict[str, Any]],
    *,
    L: int,
) -> dict[str, Any]:
    ordered = sorted(
        [dict(row) for row in full_rows],
        key=lambda row: (-int(row["cited_by_count"]), row["provider_work_id"]),
    )
    # Provider tie order may differ; citation monotonicity is the only assumed order.
    ordered.sort(key=lambda row: -int(row["cited_by_count"]))
    frozen, boundary = source_prefix_from_rows(
        ordered, L=L, source=source, exhausted=True
    )
    return {
        "source_id": source,
        "source_boundary_cited_by_count": boundary,
        "rows": frozen,
    }


def direct_global_ladder(
    sources: list[list[dict[str, Any]]],
    *,
    L: int,
) -> tuple[list[str], int]:
    by_id: dict[str, dict[str, Any]] = {}
    for rows in sources:
        for row in rows:
            wid = row["provider_work_id"]
            if wid in by_id and int(by_id[wid]["cited_by_count"]) != int(row["cited_by_count"]):
                raise ValueError("synthetic fixture has citation drift")
            by_id[wid] = dict(row)
    merged = list(by_id.values())
    merged.sort(key=lambda row: (-int(row["cited_by_count"]), row["provider_work_id"]))
    boundary = int(merged[L - 1]["cited_by_count"])
    return (
        [row["provider_work_id"] for row in merged if int(row["cited_by_count"]) >= boundary],
        boundary,
    )


def self_test() -> None:
    contract = load_contract(
        Path("research/paper2/sampling_v2_ranking_sourcewise.json")
    )
    protocol = sampling.load_protocol(Path("research/paper2/sampling_v2.json"))
    era_freeze = sampling.validate_era_freeze(protocol)
    retrieval_config = load_json(Path("research/paper2/retrieval_v1.json"))
    seeds = rankv1.seed_registry(retrieval_config)

    assert contract["real_eligibility_screening_authorized"] is False
    assert contract["candidate_ladder"]["multiplier"] == 5
    quotas = rankv1.quota_map(era_freeze)
    assert sum(5 * quota for quota in quotas.values()) == 5000

    fake_counts = {
        "schema_version": retrieval_config["schema_version"],
        "provider": "OpenAlex",
        "citation_floor": 1,
        "seed_topics_v1": ["T1", "T2"],
        "raw_counts": {
            "R1": 1,
            "R2": {q: 1 for q in retrieval_config["text_queries"]},
            "R3": {q: 1 for q in retrieval_config["anchor_queries"]},
        },
        "N_frame": 1,
        "union_oql": retrieval.union_query(
            ["T1", "T2"],
            retrieval_config["text_queries"],
            retrieval_config["anchor_queries"],
            1,
        ),
    }
    specs = build_sources(retrieval_config, fake_counts)
    assert len(specs) == 51
    assert specs[0]["source_id"] == "R1-001"
    assert specs[1]["source_id"] == "R2-001"
    assert specs[-1]["source_id"] == "R3-015"

    def row(wid: str, cited: int, title: str) -> dict[str, Any]:
        return {
            "provider_work_id": wid,
            "doi": None,
            "title": title,
            "year": 2000,
            "cited_by_count": cited,
            "type": "article",
        }

    s1 = [
        row("W1", 100, "a"),
        row("W2", 90, "b"),
        row("W3", 80, "c"),
        row("W4", 80, "d"),
        row("W5", 70, "e"),
    ]
    s2 = [
        row("W6", 95, "f"),
        row("W2", 90, "b"),
        row("W7", 85, "g"),
        row("W8", 80, "h"),
        row("W9", 60, "i"),
    ]
    s3 = [
        row("W10", 110, "j"),
        row("W11", 88, "k"),
        row("W12", 80, "l"),
        row("W13", 80, "m"),
        row("W14", 50, "n"),
    ]
    L = 5
    prefixes = [
        synthetic_prefix("S1", s1, L=L),
        synthetic_prefix("S2", s2, L=L),
        synthetic_prefix("S3", s3, L=L),
    ]
    merged, boundary = merge_source_prefixes(prefixes, L=L, seeds=seeds)
    expected_ids, expected_boundary = direct_global_ladder([s1, s2, s3], L=L)
    assert boundary == expected_boundary
    assert [r["provider_work_id"] for r in merged] == expected_ids

    # A source with >L rows and a boundary tie must retain the complete tie.
    tie_rows = [
        row("W20", 100, "t0"),
        row("W21", 90, "t1"),
        row("W22", 80, "t2"),
        row("W23", 80, "t3"),
        row("W24", 80, "t4"),
        row("W25", 70, "t5"),
    ]
    tie_prefix, tie_boundary = source_prefix_from_rows(
        tie_rows, L=3, source="TIE", exhausted=False
    )
    assert tie_boundary == 80
    assert [r["provider_work_id"] for r in tie_prefix] == [
        "W20", "W21", "W22", "W23", "W24"
    ]

    # Duplicate Work-ID citation drift must fail closed.
    drift = [
        {"source_id": "A", "rows": [row("W30", 10, "same")]},
        {"source_id": "B", "rows": [row("W30", 11, "same")]},
    ]
    try:
        merge_source_prefixes(drift, L=1, seeds=seeds)
        raise AssertionError("duplicate citation drift must fail")
    except RuntimeError as exc:
        assert "LIVE_DUPLICATE_CITATION_DRIFT" in str(exc)

    # Calibration exclusion survives sourcewise merge.
    simon = row("W40", 1000, "A Behavioral Model of Rational Choice")
    simon["doi"] = "10.2307/1884852"
    simon["year"] = 1955
    normal = row("W41", 900, "Not a seed")
    normal["year"] = 1955
    cal_rows, _ = merge_source_prefixes(
        [
            {"source_id": "A", "rows": [simon, normal]},
            {"source_id": "B", "rows": [simon]},
        ],
        L=1,
        seeds=seeds,
    )
    assert cal_rows[0]["screening_state"] == "CALIBRATION_EXCLUDED"
    assert cal_rows[0]["calibration_seed_number"] == 2

    assert contract["real_ranking_execution_authorized"] in (False, True)
    print("PAPER2_SAMPLING_V2_SOURCEWISE_RANKING_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path("research/paper2/sampling_v2_ranking_sourcewise.json"),
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
    parser.add_argument("--era")
    parser.add_argument("--fetch-ranked-era", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pause", type=float, default=0.12)
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    contract = load_contract(args.contract)
    if contract.get("real_ranking_execution_authorized") is not True:
        raise RuntimeError("REAL_SOURCEWISE_RANKING_EXECUTION_NOT_AUTHORIZED")

    protocol = sampling.load_protocol(args.sampling_protocol)
    era_freeze = sampling.validate_era_freeze(protocol, args.era_freeze)
    retrieval_config = load_json(args.retrieval_config)
    seeds = rankv1.seed_registry(retrieval_config)
    quotas = rankv1.quota_map(era_freeze)
    conditions = rankv1.era_conditions(era_freeze)

    if not args.fetch_ranked_era:
        parser.error("choose --self-test or --fetch-ranked-era")
    if not args.era or args.era not in quotas:
        raise ValueError("--fetch-ranked-era requires one frozen --era")
    if args.counts_artifact is None:
        raise ValueError("--fetch-ranked-era requires --counts-artifact")

    counts = sampling.validate_counts_artifact(args.counts_artifact)
    sources = build_sources(retrieval_config, counts)
    L = int(contract["candidate_ladder"]["multiplier"]) * quotas[args.era]
    client = retrieval.OpenAlexClient(
        api_key=os.environ.get("OPENALEX_API_KEY"),
        mailto=os.environ.get("OPENALEX_MAILTO"),
        pause=args.pause,
    )
    result = fetch_ranked_era_sourcewise(
        client,
        sources=sources,
        era=args.era,
        era_condition=conditions[args.era],
        L=L,
        seeds=seeds,
    )

    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
