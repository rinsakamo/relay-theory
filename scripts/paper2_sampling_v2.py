#!/usr/bin/env python3
"""Paper 2 temporally stratified citation-ranked sampling v2 utilities.

Owner: #167

This module freezes and mechanically validates the pre-outcome allocation rule
for Paper 2 sampling v2. Real provider measurement requires the exact frozen
#143 counts artifact; no full 31.55M-work manifest is required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper2_openalex_enumerate as retrieval  # type: ignore

SCHEMA_VERSION = "paper2-sampling-v2"
EXPECTED_COUNTS_SHA256 = "9b1d59c816a547d053fb5a34d7bd6da549d12bb43814b11095f863b4103ef40e"
EXPECTED_UNION_OQL_SHA256 = "5156ddf574e15f4b82f090dd8bf870775a31c50f292a48fd374967b4776157ab"
HISTORICAL_N_FRAME = 31_550_631


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def load_protocol(path: Path) -> dict[str, Any]:
    value = load_json(path)
    if value.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unexpected sampling-v2 schema_version")
    primary = value.get("primary_work_target", {})
    if primary.get("K") != 1000:
        raise ValueError("sampling-v2 K must remain 1000")
    if primary.get("minimum_per_included_era") != 50:
        raise ValueError("sampling-v2 minimum per included era must remain 50")
    if primary.get("weight") != "sqrt(N_d)":
        raise ValueError("sampling-v2 weighting must remain sqrt(N_d)")
    if primary.get("integer_apportionment") != "hamilton_largest_remainder":
        raise ValueError("sampling-v2 integer apportionment must remain Hamilton")
    if value.get("real_corpus_selection_authorized") is not False:
        raise ValueError("real corpus selection must remain blocked in this transaction")
    return value


def validate_counts_artifact(path: Path) -> dict[str, Any]:
    digest = sha256_file(path)
    if digest != EXPECTED_COUNTS_SHA256:
        raise ValueError(
            "counts artifact digest mismatch: expected frozen #143 artifact "
            f"{EXPECTED_COUNTS_SHA256}, got {digest}"
        )
    value = load_json(path)
    if value.get("schema_version") != "paper2-retrieval-v1":
        raise ValueError("counts artifact must be paper2-retrieval-v1")
    if value.get("provider") != "OpenAlex":
        raise ValueError("counts artifact provider must be OpenAlex")
    if int(value.get("N_frame", -1)) != HISTORICAL_N_FRAME:
        raise ValueError("counts artifact N_frame does not match frozen #143 evidence")
    topics = value.get("seed_topics_v1")
    if not isinstance(topics, list) or len(topics) != 59 or len(set(topics)) != 59:
        raise ValueError("counts artifact must carry exactly 59 unique SeedTopics_v1")
    union = value.get("union_oql")
    if not isinstance(union, str) or not union.strip():
        raise ValueError("counts artifact missing union_oql")
    union_digest = sha256_bytes(union.encode("utf-8"))
    if union_digest != EXPECTED_UNION_OQL_SHA256:
        raise ValueError(
            "union_oql digest mismatch: expected frozen #143 query "
            f"{EXPECTED_UNION_OQL_SHA256}, got {union_digest}"
        )
    return value


def parse_year_group_rows(rows: list[dict[str, Any]]) -> tuple[dict[int, int], int]:
    year_counts: dict[int, int] = {}
    unknown = 0
    for row in rows:
        raw_key = row.get("key")
        try:
            key = int(raw_key)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"invalid publication-year group key: {raw_key!r}") from exc
        count = int(row.get("count", -1))
        if count < 0:
            raise ValueError("publication-year group count must be nonnegative")
        if key == -111:
            unknown += count
            continue
        if key < 0 or key > 9999:
            raise ValueError(f"implausible publication year: {key}")
        if key in year_counts:
            raise ValueError(f"duplicate publication-year group: {key}")
        year_counts[key] = count
    return year_counts, unknown


def measurement_summary(year_counts: dict[int, int], unknown: int) -> list[dict[str, Any]]:
    buckets: list[dict[str, Any]] = []
    pre_1900 = sum(count for year, count in year_counts.items() if year <= 1899)
    buckets.append({"label": "PRE_1900", "count": pre_1900})
    for start in range(1900, 2020, 10):
        count = sum(
            value for year, value in year_counts.items()
            if start <= year <= start + 9
        )
        buckets.append({"label": f"{start}-{start + 9}", "count": count})
    buckets.append({
        "label": "2020-2026",
        "count": sum(
            value for year, value in year_counts.items() if 2020 <= year <= 2026
        ),
    })
    buckets.append({
        "label": "POST_2026",
        "count": sum(value for year, value in year_counts.items() if year >= 2027),
    })
    buckets.append({"label": "UNKNOWN_YEAR", "count": unknown})
    return buckets


def measure_era_counts(
    client: retrieval.OpenAlexClient,
    frozen_counts: dict[str, Any],
) -> dict[str, Any]:
    query = frozen_counts["union_oql"] + " group by year"
    cursor: str | None = "*"
    all_rows: list[dict[str, Any]] = []
    provider_count: int | None = None
    page_count = 0
    while cursor:
        payload = client.run_oql(query, per_page=100, cursor=cursor)
        meta = payload.get("meta") or {}
        current_count = int(meta.get("count", -1))
        if current_count < 0:
            raise ValueError("grouped OpenAlex response missing meta.count")
        if provider_count is None:
            provider_count = current_count
        elif current_count != provider_count:
            raise RuntimeError(
                "ERA_COUNT_PROVIDER_DRIFT: meta.count changed during grouped cursor traversal"
            )
        rows = payload.get("group_by")
        if not isinstance(rows, list):
            raise ValueError("grouped OpenAlex response missing group_by list")
        all_rows.extend(row for row in rows if isinstance(row, dict))
        cursor = meta.get("next_cursor")
        page_count += 1
        if page_count > 100:
            raise RuntimeError("unexpectedly many publication-year group pages")

    year_counts, unknown = parse_year_group_rows(all_rows)
    grouped_total = sum(year_counts.values()) + unknown
    if provider_count is None or grouped_total != provider_count:
        raise RuntimeError(
            "ERA_COUNT_PARTITION_MISMATCH: year-group total does not equal provider "
            f"union count ({grouped_total} != {provider_count})"
        )
    return {
        "schema_version": "paper2-sampling-v2-era-counts-v1",
        "owner_issue": 167,
        "provider": "OpenAlex",
        "access_timestamp": retrieval.utc_now(),
        "retrieval_counts_artifact_sha256": EXPECTED_COUNTS_SHA256,
        "union_oql_sha256": EXPECTED_UNION_OQL_SHA256,
        "historical_N_frame_2026_09_23": HISTORICAL_N_FRAME,
        "current_provider_union_count": provider_count,
        "year_group_pages": page_count,
        "unknown_year_count": unknown,
        "year_counts": {str(year): year_counts[year] for year in sorted(year_counts)},
        "measurement_buckets_are_final_sampling_eras": False,
        "measurement_summary": measurement_summary(year_counts, unknown),
    }


def hamilton_allocate(
    era_counts: dict[str, int], *, K: int = 1000, minimum: int = 50
) -> dict[str, Any]:
    if not era_counts:
        raise ValueError("era_counts must be non-empty")
    ordered = list(era_counts)
    counts: dict[str, int] = {}
    for era in ordered:
        n = int(era_counts[era])
        if n <= 0:
            raise ValueError(f"era {era} must have positive N_d")
        counts[era] = n

    D = len(counts)
    base = D * minimum
    if base > K:
        raise ValueError(
            f"minimum floor infeasible: D*minimum={base} exceeds K={K}"
        )
    remaining = K - base
    weights = {era: math.sqrt(n) for era, n in counts.items()}
    weight_total = sum(weights.values())
    exact_extra = {
        era: (remaining * weights[era] / weight_total if remaining else 0.0)
        for era in ordered
    }
    floors = {era: math.floor(exact_extra[era]) for era in ordered}
    leftover = remaining - sum(floors.values())
    tie_pos = {era: i for i, era in enumerate(ordered)}
    by_remainder = sorted(
        ordered,
        key=lambda era: (-(exact_extra[era] - floors[era]), tie_pos[era]),
    )
    extra = dict(floors)
    for era in by_remainder[:leftover]:
        extra[era] += 1
    quotas = {era: minimum + extra[era] for era in ordered}
    if sum(quotas.values()) != K:
        raise AssertionError("Hamilton apportionment failed to preserve K")
    if any(q < minimum for q in quotas.values()):
        raise AssertionError("minimum floor violated")
    return {
        "K": K,
        "minimum_per_included_era": minimum,
        "D": D,
        "base_total": base,
        "remaining_total": remaining,
        "eras": [
            {
                "era": era,
                "N_d": counts[era],
                "sqrt_N_d": weights[era],
                "exact_extra": exact_extra[era],
                "integer_extra": extra[era],
                "quota_k_d": quotas[era],
            }
            for era in ordered
        ],
    }


def self_test(protocol: dict[str, Any]) -> None:
    p = protocol["primary_work_target"]
    assert p["K"] == 1000
    assert p["minimum_per_included_era"] == 50
    assert p["weight"] == "sqrt(N_d)"
    assert protocol["real_corpus_selection_authorized"] is False

    parsed_years, parsed_unknown = parse_year_group_rows([
        {"key": 1959, "count": 10},
        {"key": 1960, "count": 20},
        {"key": 1969, "count": 30},
        {"key": 2026, "count": 140},
        {"key": -111, "count": 5},
    ])
    assert parsed_years == {1959: 10, 1960: 20, 1969: 30, 2026: 140}
    assert parsed_unknown == 5
    summary = {row["label"]: row["count"] for row in measurement_summary(parsed_years, 5)}
    assert summary["1950-1959"] == 10
    assert summary["1960-1969"] == 50
    assert summary["2020-2026"] == 140
    assert summary["UNKNOWN_YEAR"] == 5

    counts = {
        "1950s": 100,
        "1960s": 400,
        "1970s": 900,
        "1980s": 1600,
        "1990s": 2500,
        "2000s": 3600,
        "2010s": 4900,
        "2020s": 6400,
    }
    a = hamilton_allocate(counts, K=1000, minimum=50)
    b = hamilton_allocate(counts, K=1000, minimum=50)
    assert a == b
    assert sum(x["quota_k_d"] for x in a["eras"]) == 1000
    assert all(x["quota_k_d"] >= 50 for x in a["eras"])
    assert [x["integer_extra"] for x in a["eras"]] == [17, 33, 50, 67, 83, 100, 117, 133]
    assert [x["quota_k_d"] for x in a["eras"]] == [67, 83, 100, 117, 133, 150, 167, 183]

    tied = hamilton_allocate({"A": 1, "B": 1, "C": 1}, K=152, minimum=50)
    assert [x["quota_k_d"] for x in tied["eras"]] == [51, 51, 50]

    try:
        hamilton_allocate({f"E{i}": 1 for i in range(21)}, K=1000, minimum=50)
        raise AssertionError("infeasible floor must fail closed")
    except ValueError as exc:
        assert "infeasible" in str(exc)

    class FakeClient:
        def __init__(self) -> None:
            self.calls: list[tuple[str, int, str | None]] = []

        def run_oql(
            self, query: str, *, per_page: int = 1, cursor: str | None = None,
            select: str | None = None,
        ) -> dict[str, Any]:
            self.calls.append((query, per_page, cursor))
            if cursor == "*":
                return {
                    "meta": {"count": 35, "next_cursor": "next"},
                    "group_by": [
                        {"key": 1959, "count": 10},
                        {"key": 1960, "count": 20},
                    ],
                }
            if cursor == "next":
                return {
                    "meta": {"count": 35, "next_cursor": None},
                    "group_by": [{"key": -111, "count": 5}],
                }
            raise AssertionError("unexpected cursor")

    fake_counts = {
        "union_oql": "works where citation count >= (1) and "
        "(title/abstract has (memory))"
    }
    fake = FakeClient()
    measured = measure_era_counts(fake, fake_counts)  # type: ignore[arg-type]
    assert measured["current_provider_union_count"] == 35
    assert measured["year_group_pages"] == 2
    assert measured["unknown_year_count"] == 5
    assert measured["year_counts"] == {"1959": 10, "1960": 20}
    assert measured["measurement_buckets_are_final_sampling_eras"] is False
    assert all(call[1] == 100 for call in fake.calls)
    assert all(call[0].endswith("group by year") for call in fake.calls)

    print("PAPER2_SAMPLING_V2_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--protocol",
        type=Path,
        default=Path("research/paper2/sampling_v2.json"),
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--counts-artifact", type=Path)
    parser.add_argument("--measure-era-counts", action="store_true")
    parser.add_argument("--era-counts-json", type=Path)
    parser.add_argument("--allocate", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pause", type=float, default=0.12)
    args = parser.parse_args()

    protocol = load_protocol(args.protocol)
    if args.self_test:
        self_test(protocol)
        return 0

    if args.measure_era_counts:
        if args.counts_artifact is None:
            parser.error("--measure-era-counts requires --counts-artifact")
        frozen = validate_counts_artifact(args.counts_artifact)
        client = retrieval.OpenAlexClient(
            api_key=os.environ.get("OPENALEX_API_KEY"),
            mailto=os.environ.get("OPENALEX_MAILTO"),
            pause=args.pause,
        )
        result = measure_era_counts(client, frozen)
    elif args.allocate:
        if args.era_counts_json is None:
            parser.error("--allocate requires --era-counts-json")
        era_counts_doc = load_json(args.era_counts_json)
        era_counts = era_counts_doc.get("included_era_counts")
        if not isinstance(era_counts, dict):
            raise ValueError(
                "allocation input must contain included_era_counts after era boundaries are frozen"
            )
        p = protocol["primary_work_target"]
        result = hamilton_allocate(
            {str(k): int(v) for k, v in era_counts.items()},
            K=int(p["K"]),
            minimum=int(p["minimum_per_included_era"]),
        )
        result.update(
            {
                "schema_version": "paper2-sampling-v2-allocation-v1",
                "owner_issue": 167,
                "source_era_counts": str(args.era_counts_json),
            }
        )
    else:
        parser.error("choose --self-test, --measure-era-counts, or --allocate")
        return 2

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
