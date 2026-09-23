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
EXPECTED_UNION_OQL_UTF8_SHA256 = "35f6a79454cb8a279cc397cfa1eea2c07cca15141744060cce3cf4454bad63b6"
EXPECTED_UNION_OQL_JQ_R_SHA256 = "5156ddf574e15f4b82f090dd8bf870775a31c50f292a48fd374967b4776157ab"
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
    authority = value.get("retrieval_authority", {})
    measurement = authority.get("era_count_measurement", {})
    if measurement.get("method") != "one_shot_bucket_counts_with_union_before_after_bracket":
        raise ValueError("sampling-v2 era-count method must remain one-shot bracketed counts")
    if measurement.get("transport_attempts_per_query") != 1:
        raise ValueError("sampling-v2 era-count transport attempts must remain exactly one")
    if measurement.get("cursor_paging_used") is not False:
        raise ValueError("sampling-v2 era-count measurement must not use cursor paging")
    if measurement.get("meta_count_equality_across_requests_required") is not False:
        raise ValueError("sampling-v2 must record live provider drift rather than require equality")
    if measurement.get("measurement_buckets_are_final_sampling_eras") is not False:
        raise ValueError("diagnostic measurement buckets must not become final eras implicitly")
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
    union_utf8_digest = sha256_bytes(union.encode("utf-8"))
    if union_utf8_digest != EXPECTED_UNION_OQL_UTF8_SHA256:
        raise ValueError(
            "union_oql UTF-8 string digest mismatch: expected exact JSON-string "
            f"bytes {EXPECTED_UNION_OQL_UTF8_SHA256}, got {union_utf8_digest}"
        )
    union_jq_r_digest = sha256_bytes((union + "\n").encode("utf-8"))
    if union_jq_r_digest != EXPECTED_UNION_OQL_JQ_R_SHA256:
        raise ValueError(
            "union_oql jq -r line digest mismatch: expected historical #143 "
            f"representation {EXPECTED_UNION_OQL_JQ_R_SHA256}, got {union_jq_r_digest}"
        )
    return value


def measurement_buckets() -> list[dict[str, str]]:
    """Diagnostic publication-year buckets; not yet final sampling eras."""
    buckets: list[dict[str, str]] = [
        {"label": "PRE_1900", "condition": "year <= (1899)"}
    ]
    for start in range(1900, 2020, 10):
        buckets.append(
            {
                "label": f"{start}-{start + 9}",
                "condition": f"year >= ({start}) and year <= ({start + 9})",
            }
        )
    buckets.extend(
        [
            {
                "label": "2020-2026",
                "condition": "year >= (2020) and year <= (2026)",
            },
            {"label": "POST_2026", "condition": "year >= (2027)"},
            {"label": "UNKNOWN_YEAR", "condition": "year is (unknown)"},
        ]
    )
    return buckets


def append_filter(union_oql: str, condition: str) -> str:
    if not union_oql.startswith("works where "):
        raise ValueError("frozen union_oql must start with 'works where '")
    if not condition or "works where" in condition:
        raise ValueError("invalid diagnostic filter condition")
    return f"{union_oql} and {condition}"


def count_once(
    client: retrieval.OpenAlexClient,
    query: str,
) -> dict[str, Any]:
    """Execute exactly one HTTP attempt and return a timestamped live count."""
    started_at = retrieval.utc_now()
    payload = client.request_json(
        retrieval.API_ROOT,
        method="POST",
        body={"oql": query, "per_page": 1},
        retries=1,
    )
    completed_at = retrieval.utc_now()
    meta = payload.get("meta") or {}
    count = int(meta.get("count", -1))
    if count < 0:
        raise ValueError("OpenAlex response missing nonnegative meta.count")
    return {
        "count": count,
        "started_at": started_at,
        "completed_at": completed_at,
    }


def measure_era_counts(
    client: retrieval.OpenAlexClient,
    frozen_counts: dict[str, Any],
) -> dict[str, Any]:
    """Measure diagnostic era buckets without cursor paging.

    OpenAlex documents live counts as mutable. This transaction therefore
    brackets the one-shot bucket queries with one total-union count before and
    after, records drift instead of requiring equality, and performs no retry.
    """
    union = frozen_counts["union_oql"]
    transaction_started_at = retrieval.utc_now()
    total_before = count_once(client, union)

    rows: list[dict[str, Any]] = []
    for bucket in measurement_buckets():
        measured = count_once(client, append_filter(union, bucket["condition"]))
        rows.append(
            {
                "label": bucket["label"],
                "condition": bucket["condition"],
                **measured,
            }
        )

    total_after = count_once(client, union)
    transaction_completed_at = retrieval.utc_now()
    bucket_total = sum(int(row["count"]) for row in rows)
    before = int(total_before["count"])
    after = int(total_after["count"])

    return {
        "schema_version": "paper2-sampling-v2-era-counts-v2",
        "owner_issue": 167,
        "provider": "OpenAlex",
        "measurement_method": "one_shot_bucket_counts_with_union_before_after_bracket",
        "transport_attempts_per_query": 1,
        "cursor_paging_used": False,
        "transaction_started_at": transaction_started_at,
        "transaction_completed_at": transaction_completed_at,
        "retrieval_counts_artifact_sha256": EXPECTED_COUNTS_SHA256,
        "union_oql_utf8_sha256": EXPECTED_UNION_OQL_UTF8_SHA256,
        "union_oql_jq_r_sha256": EXPECTED_UNION_OQL_JQ_R_SHA256,
        "historical_N_frame_2026_09_23": HISTORICAL_N_FRAME,
        "provider_union_count_before": total_before,
        "provider_union_count_after": total_after,
        "provider_union_count_signed_drift": after - before,
        "provider_union_count_absolute_drift": abs(after - before),
        "bucket_count_sum": bucket_total,
        "bucket_sum_minus_union_before": bucket_total - before,
        "bucket_sum_minus_union_after": bucket_total - after,
        "measurement_buckets_are_final_sampling_eras": False,
        "live_provider_counts_are_point_in_time_snapshot": False,
        "buckets": rows,
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


def validate_era_freeze(
    protocol: dict[str, Any],
    era_freeze_path: Path = Path("research/paper2/sampling_v2_era_freeze.json"),
) -> dict[str, Any]:
    freeze = load_json(era_freeze_path)
    if freeze.get("schema_version") != "paper2-sampling-v2-era-freeze-v1":
        raise ValueError("unexpected sampling-v2 era-freeze schema_version")
    if freeze.get("owner_issue") != 167 or freeze.get("status") != "PREOUTCOME_FROZEN":
        raise ValueError("sampling-v2 era freeze authority/status mismatch")
    source = freeze.get("source_measurement", {})
    if source.get("artifact_sha256") != "6614cc35b0c5db256840d31711001809b726c6fa361164a4a5d330fce7def4aa":
        raise ValueError("sampling-v2 era measurement artifact digest drift")
    if source.get("bucket_count_sum") != 33_699_941:
        raise ValueError("sampling-v2 era bucket total drift")
    if source.get("bucket_sum_minus_union_after") != 0:
        raise ValueError("sampling-v2 era transaction must retain recorded after-bracket closure")
    if source.get("live_provider_counts_are_point_in_time_snapshot") is not False:
        raise ValueError("live provider counts must not be relabeled as a point-in-time snapshot")

    era_policy = freeze.get("era_policy", {})
    order = era_policy.get("frozen_order")
    expected_order = [
        "PRE_1950",
        "1950-1959",
        "1960-1969",
        "1970-1979",
        "1980-1989",
        "1990-1999",
        "2000-2009",
        "2010-2019",
        "2020-2026",
    ]
    if order != expected_order:
        raise ValueError("sampling-v2 frozen era order drift")
    if era_policy.get("study_publication_year_cutoff") != 2026:
        raise ValueError("sampling-v2 publication-year cutoff drift")
    if era_policy.get("unknown_year", {}).get("count") != 7801:
        raise ValueError("sampling-v2 unknown-year count drift")
    if era_policy.get("post_cutoff_year", {}).get("count") != 4:
        raise ValueError("sampling-v2 post-cutoff count drift")

    counts = freeze.get("included_era_counts")
    if not isinstance(counts, dict) or list(counts) != expected_order:
        raise ValueError("sampling-v2 included era counts/order mismatch")
    allocation = hamilton_allocate(
        {str(k): int(v) for k, v in counts.items()},
        K=int(protocol["primary_work_target"]["K"]),
        minimum=int(protocol["primary_work_target"]["minimum_per_included_era"]),
    )
    computed = {row["era"]: row["quota_k_d"] for row in allocation["eras"]}
    frozen = {
        row["era"]: row["quota_k_d"]
        for row in freeze.get("primary_allocation", {}).get("eras", [])
    }
    protocol_frozen = protocol["primary_work_target"].get("frozen_era_allocation")
    if computed != frozen or computed != protocol_frozen:
        raise ValueError("sampling-v2 frozen quota allocation mismatch")
    if sum(computed.values()) != 1000:
        raise ValueError("sampling-v2 frozen quota sum must equal 1000")
    if freeze.get("included_design_count_total") != sum(int(v) for v in counts.values()):
        raise ValueError("sampling-v2 included design count total mismatch")
    return freeze


def self_test(protocol: dict[str, Any]) -> None:
    p = protocol["primary_work_target"]
    assert p["K"] == 1000
    assert p["minimum_per_included_era"] == 50
    assert p["weight"] == "sqrt(N_d)"
    assert protocol["real_corpus_selection_authorized"] is False
    authority = protocol["retrieval_authority"]
    assert authority["union_oql_utf8_sha256"] == EXPECTED_UNION_OQL_UTF8_SHA256
    assert authority["union_oql_jq_r_sha256"] == EXPECTED_UNION_OQL_JQ_R_SHA256
    assert sha256_bytes(b"synthetic") != sha256_bytes(b"synthetic\n")
    freeze = validate_era_freeze(protocol)
    assert freeze["primary_allocation"]["quota_sum"] == 1000
    assert freeze["included_design_count_total"] == 33_692_136

    buckets = measurement_buckets()
    assert buckets[0] == {"label": "PRE_1900", "condition": "year <= (1899)"}
    assert buckets[-3]["label"] == "2020-2026"
    assert buckets[-2]["label"] == "POST_2026"
    assert buckets[-1] == {"label": "UNKNOWN_YEAR", "condition": "year is (unknown)"}
    assert len(buckets) == 16
    filtered = append_filter(
        "works where citation count >= (1) and (title/abstract has (memory))",
        "year >= (2010) and year <= (2019)",
    )
    assert filtered.endswith("and year >= (2010) and year <= (2019)")

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
            self.calls: list[dict[str, Any]] = []
            # union-before, 16 buckets, union-after
            self.counts = iter([1000, *([62] * 15), 70, 1003])

        def request_json(
            self,
            url: str,
            *,
            method: str = "GET",
            body: dict[str, Any] | None = None,
            retries: int = 5,
        ) -> dict[str, Any]:
            self.calls.append(
                {
                    "url": url,
                    "method": method,
                    "body": body,
                    "retries": retries,
                }
            )
            return {"meta": {"count": next(self.counts)}}

    fake_counts = {
        "union_oql": "works where citation count >= (1) and "
        "(title/abstract has (memory))"
    }
    fake = FakeClient()
    measured = measure_era_counts(fake, fake_counts)  # type: ignore[arg-type]
    assert measured["schema_version"] == "paper2-sampling-v2-era-counts-v2"
    assert measured["provider_union_count_before"]["count"] == 1000
    assert measured["provider_union_count_after"]["count"] == 1003
    assert measured["provider_union_count_signed_drift"] == 3
    assert measured["provider_union_count_absolute_drift"] == 3
    assert measured["cursor_paging_used"] is False
    assert len(measured["buckets"]) == 16
    assert measured["buckets"][-1]["label"] == "UNKNOWN_YEAR"
    assert measured["buckets"][-1]["count"] == 70
    assert len(fake.calls) == 18
    assert all(call["retries"] == 1 for call in fake.calls)
    assert all(call["method"] == "POST" for call in fake.calls)
    assert all(call["body"]["per_page"] == 1 for call in fake.calls)

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
