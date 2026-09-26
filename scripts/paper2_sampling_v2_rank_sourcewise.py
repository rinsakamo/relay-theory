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
are reconciled only by a frozen first-observation rule: the earliest durable
source transaction supplies the ranking score, while every observation is
preserved for audit. Optional OpenAlex type drift is also preserved, but type is
not allowed to affect ranking or calibration identity. An era with observed
live drift is explicitly a transaction-local frozen capture rather than being
silently presented as one provider snapshot.

No eligibility/source-text adjudication, ClaimIR, decomposition, or null-control
execution is performed here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper2_openalex_enumerate as retrieval  # type: ignore
import paper2_openalex_manifest as manifest  # type: ignore
import paper2_sampling_v2 as sampling  # type: ignore
import paper2_sampling_v2_rank as rankv1  # type: ignore

SCHEMA_VERSION = "paper2-sampling-v2-ranking-sourcewise-v6"
RANKED_ERA_SCHEMA = "paper2-sampling-v2-ranked-era-sourcewise-v6"
SOURCE_PREFIX_SCHEMA = "paper2-sampling-v2-source-prefix-v2"
PAGE_SIZE = 100
MAX_BASIC_ROWS = 10_000
RATE_LIMIT_ROOT = "https://api.openalex.org/rate-limit"
MIN_REMAINING_CREDITS = 1_500
LIST_CALL_CREDIT_COST = 1


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
    if surface.get("duplicate_work_id_policy") != (
        "DEDUP_BY_WORK_ID; CITATION DRIFT -> FREEZE EARLIEST SOURCE-TRANSACTION "
        "OBSERVATION AND PRESERVE ALL OBSERVATIONS"
    ):
        raise ValueError("duplicate Work-ID citation policy drift")
    if surface.get("live_duplicate_citation_resolution") != (
        "earliest transaction_started_at, then source_id ascending; later duplicate "
        "observations never overwrite the frozen ranking score"
    ):
        raise ValueError("live citation resolution policy drift")
    if surface.get("capture_exactness_policy") != (
        "STATIC_PROVIDER_EXACT_IF_NO_OBSERVED_CITATION_DRIFT; "
        "OTHERWISE_TRANSACTION_LOCAL_FROZEN_CAPTURE"
    ):
        raise ValueError("capture exactness policy drift")
    ladder = value.get("candidate_ladder", {})
    if ladder.get("multiplier") != 5:
        raise ValueError("sourcewise candidate ladder multiplier must remain 5")
    metadata = value.get("optional_bibliographic_metadata_policy", {})
    if metadata.get("display_name_required_for_ranking") is not False:
        raise ValueError("display_name must remain optional for ranking")
    if metadata.get("publication_year_required_for_ranking") is not True:
        raise ValueError("publication_year must remain required for ranking")
    if metadata.get("cited_by_count_required_for_ranking") is not True:
        raise ValueError("cited_by_count must remain required for ranking")
    if metadata.get("work_id_required_for_ranking") is not True:
        raise ValueError("work_id must remain required for ranking")
    if metadata.get("optional_string_normalization") != (
        "display_name/title and type are retained only when non-empty strings; "
        "null, blank, and non-string provider values normalize to null"
    ):
        raise ValueError("optional bibliographic string normalization drift")
    if metadata.get("duplicate_optional_field_policy") != (
        "doi: coalesce null/non-null and fail closed on conflicting non-null "
        "values; title: preserve all observations, require calibration-outcome "
        "consistency across distinct non-null titles, and freeze earliest non-null "
        "observation; type: preserve all observations and freeze earliest non-null "
        "source-transaction observation"
    ):
        raise ValueError("optional bibliographic metadata merge policy drift")
    if metadata.get("title_drift_role") != (
        "title is not a ranking key but participates in Top50 calibration fallback "
        "identity with publication year when DOI does not identify a seed"
    ):
        raise ValueError("optional title drift role authority drift")
    if metadata.get("title_drift_resolution") != (
        "sort observations by transaction_started_at then source_id; evaluate every "
        "distinct non-null title with frozen DOI/year through the calibration matcher; "
        "require one identical calibration outcome across all distinct non-null titles; "
        "select earliest non-null title; preserve all observations and outcomes"
    ):
        raise ValueError("optional title drift resolution authority drift")
    if metadata.get("title_missingness_policy") != (
        "null title is missing metadata rather than an alternative identity claim; "
        "null/non-null coalescence is allowed and calibration-consistency comparison "
        "is over distinct non-null titles only"
    ):
        raise ValueError("optional title missingness policy drift")
    if metadata.get("type_drift_role") != (
        "descriptive metadata only; type is not a ranking key and is not used "
        "for Top50 calibration identity"
    ):
        raise ValueError("optional type drift role authority drift")
    if metadata.get("type_drift_resolution") != (
        "sort observations by transaction_started_at then source_id; select "
        "earliest non-null type; preserve all observations and distinct non-null values"
    ):
        raise ValueError("optional type drift resolution authority drift")
    if metadata.get("duplicate_required_field_policy") != (
        "year mismatch fails closed; cited_by_count drift is preserved and resolved "
        "only by the frozen earliest-observation policy"
    ):
        raise ValueError("required duplicate metadata policy drift")
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
    if execution.get("live_duplicate_citation_drift_policy") != (
        "provider-free merge only; preserve all duplicate citation observations, "
        "freeze earliest observation for ranking, report drift count/range, and "
        "downgrade snapshot exactness classification"
    ):
        raise ValueError("live duplicate citation drift execution policy drift")
    if execution.get("live_duplicate_optional_title_drift_policy") != (
        "provider-free merge only; preserve all title observations; permit conflicting "
        "non-null titles only when their Top50 calibration outcomes are identical under "
        "the frozen DOI/year; otherwise fail closed with "
        "LIVE_DUPLICATE_CALIBRATION_IDENTITY_DRIFT"
    ):
        raise ValueError("live duplicate optional title drift policy drift")
    if execution.get("live_duplicate_optional_type_drift_policy") != (
        "provider-free merge only; type conflicts do not affect ranking or "
        "calibration identity, are preserved in an observation ledger, and set "
        "single_provider_snapshot_claimed=false"
    ):
        raise ValueError("live duplicate optional type drift policy drift")
    if execution.get("source_union_drift_audit_scope") != (
        "deduplicated union of all 51 frozen source-prefix artifacts before the "
        "global L cutoff"
    ):
        raise ValueError("source-union drift audit scope drift")
    if execution.get("ranked_row_scope") != (
        "global top-L plus complete global citation-boundary tie after source-union "
        "deduplication"
    ):
        raise ValueError("ranked row scope drift")
    if execution.get("drift_witness_retention") != (
        "retain one provider-free audit witness per drifted Work ID even when that "
        "Work falls below the global ranked ladder; witness records ranked-membership "
        "plus only the drifted dimension ledgers"
    ):
        raise ValueError("drift witness retention policy drift")
    if execution.get("rank_membership_rule") != (
        "drift witness retention is audit-only and never promotes a Work into ranked rows"
    ):
        raise ValueError("drift witness rank-membership policy drift")
    if execution.get("drift_summary_required_on_provider_free_merge") is not True:
        raise ValueError("provider-free merge must emit source-union drift summary")
    if execution.get("failed_ranked_artifact_policy") != (
        "a merge artifact that writes successfully but fails qualification remains "
        "immutable historical evidence; a repaired authority must write a new "
        "versioned output path rather than overwrite or delete it"
    ):
        raise ValueError("failed ranked artifact preservation policy drift")

    if execution.get("openalex_api_key_required") is not True:
        raise ValueError("real sourcewise ranking must require an OpenAlex API key")
    if execution.get("mailto_rate_limit_control") is not False:
        raise ValueError("mailto must not be treated as a rate-limit control")
    if execution.get("rate_limit_preflight_required_after_429") is not True:
        raise ValueError("rate-limit preflight must remain required after 429")
    if execution.get("rate_limit_endpoint") != RATE_LIMIT_ROOT:
        raise ValueError("OpenAlex rate-limit endpoint drift")
    if execution.get("rate_limit_authentication") != (
        "api_key query parameter, identical to ranking client"
    ):
        raise ValueError("OpenAlex rate-limit authentication parity drift")
    if execution.get("minimum_remaining_credits_before_resume") != MIN_REMAINING_CREDITS:
        raise ValueError("minimum remaining credit authority drift")
    if execution.get("list_call_credit_cost") != LIST_CALL_CREDIT_COST:
        raise ValueError("OpenAlex list-call credit cost authority drift")
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


def require_openalex_api_key() -> str:
    value = os.environ.get("OPENALEX_API_KEY")
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(
            "OPENALEX_API_KEY_REQUIRED:"
            "real ranked-candidate acquisition must not use the anonymous budget"
        )
    return value.strip()


def parse_rate_limit_status(
    payload: dict[str, Any],
    headers: dict[str, str],
    *,
    minimum_remaining_credits: int = MIN_REMAINING_CREDITS,
) -> dict[str, Any]:
    lower_headers = {str(k).lower(): str(v) for k, v in headers.items()}
    remaining_raw = lower_headers.get("x-ratelimit-remaining")
    limit_raw = lower_headers.get("x-ratelimit-limit")
    reset_raw = lower_headers.get("x-ratelimit-reset")

    rate = payload.get("rate_limit")
    if not isinstance(rate, dict):
        rate = {}

    if remaining_raw is None:
        candidate = rate.get("credits_remaining")
        if isinstance(candidate, (int, float)):
            remaining_raw = str(candidate)
    if limit_raw is None:
        candidate = rate.get("credits_limit")
        if isinstance(candidate, (int, float)):
            limit_raw = str(candidate)
    if reset_raw is None:
        candidate = rate.get("resets_in_seconds")
        if isinstance(candidate, (int, float)):
            reset_raw = str(candidate)

    if remaining_raw is None:
        raise RuntimeError("OPENALEX_RATE_LIMIT_REMAINING_UNAVAILABLE")

    try:
        remaining = int(float(remaining_raw))
    except ValueError as exc:
        raise RuntimeError("OPENALEX_RATE_LIMIT_REMAINING_MALFORMED") from exc

    limit_value: int | None = None
    if limit_raw is not None:
        try:
            limit_value = int(float(limit_raw))
        except ValueError:
            limit_value = None

    reset_seconds: int | None = None
    if reset_raw is not None:
        try:
            reset_seconds = int(float(reset_raw))
        except ValueError:
            reset_seconds = None

    list_call_equivalent = remaining // LIST_CALL_CREDIT_COST
    if remaining < minimum_remaining_credits:
        raise RuntimeError(
            "OPENALEX_RATE_LIMIT_BUDGET_INSUFFICIENT:"
            f"remaining_credits={remaining}:"
            f"required_credits={minimum_remaining_credits}:"
            f"reset_seconds={reset_seconds}"
        )

    return {
        "schema_version": "paper2-openalex-rate-limit-preflight-v1",
        "provider": "OpenAlex",
        "checked_at": retrieval.utc_now(),
        "api_key_present": True,
        "api_key_value_recorded": False,
        "credits_limit": limit_value,
        "credits_remaining": remaining,
        "list_call_credit_cost": LIST_CALL_CREDIT_COST,
        "remaining_list_call_equivalent": list_call_equivalent,
        "minimum_remaining_credits_required": minimum_remaining_credits,
        "minimum_remaining_list_call_equivalent_required": (
            minimum_remaining_credits // LIST_CALL_CREDIT_COST
        ),
        "reset_seconds": reset_seconds,
        "classification": "OPENALEX_KEYED_BUDGET_PREFLIGHT_PASS",
    }


def rate_limit_preflight(api_key: str) -> dict[str, Any]:
    # Use the same api_key query-parameter authentication form as the ranking client.
    # OpenAlex documents query-param and Bearer authentication as equivalent, but
    # keeping both surfaces identical removes preflight-only auth divergence.
    url = RATE_LIMIT_ROOT + "?" + urllib.parse.urlencode({"api_key": api_key})
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": retrieval.USER_AGENT,
            "Accept": "application/json",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            payload = json.load(response)
            headers = {str(k): str(v) for k, v in response.headers.items()}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        if exc.code == 401:
            raise RuntimeError(
                "OPENALEX_API_KEY_INVALID:"
                "provider returned HTTP 401 for keyed rate-limit preflight"
            ) from exc
        raise RuntimeError(
            f"OPENALEX_RATE_LIMIT_PREFLIGHT_HTTP_{exc.code}:{detail}"
        ) from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"OPENALEX_RATE_LIMIT_PREFLIGHT_TRANSPORT:{exc}") from exc

    if not isinstance(payload, dict):
        raise RuntimeError("OPENALEX_RATE_LIMIT_PREFLIGHT_MALFORMED")
    # Never persist any provider-returned api_key field.
    payload = {k: v for k, v in payload.items() if str(k).lower() != "api_key"}
    return parse_rate_limit_status(payload, headers)


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


def _merge_source_prefixes_core(
    prefixes: list[dict[str, Any]],
    *,
    L: int,
    seeds: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int, dict[str, Any]]:
    if L < 1:
        raise ValueError("L must be positive")
    by_id: dict[str, dict[str, Any]] = {}
    sources_by_id: dict[str, set[str]] = {}
    citation_observations_by_id: dict[str, list[dict[str, Any]]] = {}
    title_observations_by_id: dict[str, list[dict[str, Any]]] = {}
    type_observations_by_id: dict[str, list[dict[str, Any]]] = {}

    for prefix in prefixes:
        sid = str(prefix["source_id"])
        started_at = prefix.get("transaction_started_at")
        if not isinstance(started_at, str) or not started_at.strip():
            raise ValueError(f"{sid}: missing transaction_started_at for merge")
        rows = prefix.get("rows")
        if not isinstance(rows, list):
            raise ValueError(f"{sid}: missing prefix rows")
        for row in rows:
            normalized = dict(row)
            wid = rankv1.canonical_work_id(normalized.get("provider_work_id"))
            cited = int(normalized["cited_by_count"])
            citation_observations_by_id.setdefault(wid, []).append(
                {
                    "source_id": sid,
                    "transaction_started_at": started_at,
                    "cited_by_count": cited,
                }
            )
            title_observations_by_id.setdefault(wid, []).append(
                {
                    "source_id": sid,
                    "transaction_started_at": started_at,
                    "title": normalized.get("title"),
                }
            )
            type_observations_by_id.setdefault(wid, []).append(
                {
                    "source_id": sid,
                    "transaction_started_at": started_at,
                    "type": normalized.get("type"),
                }
            )
            if wid in by_id:
                previous = by_id[wid]
                if int(previous["year"]) != int(normalized["year"]):
                    raise RuntimeError(f"LIVE_DUPLICATE_METADATA_DRIFT:{wid}:year")
                # DOI participates directly in calibration identity. Conflicting
                # non-null DOI observations remain fail-closed.
                old_doi = previous.get("doi")
                new_doi = normalized.get("doi")
                if old_doi is None and new_doi is not None:
                    previous["doi"] = new_doi
                elif (
                    old_doi is not None
                    and new_doi is not None
                    and old_doi != new_doi
                ):
                    raise RuntimeError(
                        f"LIVE_DUPLICATE_METADATA_DRIFT:{wid}:doi"
                    )
            else:
                by_id[wid] = normalized
                sources_by_id[wid] = set()
            sources_by_id[wid].add(sid)

    for wid, row in by_id.items():
        citation_observations = sorted(
            citation_observations_by_id[wid],
            key=lambda item: (
                str(item["transaction_started_at"]),
                str(item["source_id"]),
            ),
        )
        frozen_citation = citation_observations[0]
        counts = [int(item["cited_by_count"]) for item in citation_observations]
        row["cited_by_count"] = int(frozen_citation["cited_by_count"])
        row["citation_resolution_policy"] = "earliest_source_transaction_observation"
        row["citation_selected_source_id"] = frozen_citation["source_id"]
        row["citation_selected_transaction_started_at"] = frozen_citation["transaction_started_at"]
        row["citation_observation_count"] = len(citation_observations)
        row["citation_count_min_observed"] = min(counts)
        row["citation_count_max_observed"] = max(counts)
        row["citation_count_drift"] = max(counts) - min(counts)
        row["citation_observations"] = citation_observations

        title_observations = sorted(
            title_observations_by_id[wid],
            key=lambda item: (
                str(item["transaction_started_at"]),
                str(item["source_id"]),
            ),
        )
        non_null_title_observations = [
            item for item in title_observations if item.get("title") is not None
        ]
        selected_title_observation = (
            non_null_title_observations[0]
            if non_null_title_observations
            else None
        )
        distinct_titles = sorted(
            {str(item["title"]) for item in non_null_title_observations}
        )
        title_outcomes_by_value: dict[str, tuple[int | None, str | None]] = {}
        for title_value in distinct_titles:
            title_outcomes_by_value[title_value] = rankv1.calibration_match(
                {
                    "doi": row.get("doi"),
                    "title": title_value,
                    "year": row["year"],
                },
                seeds,
            )
        distinct_title_outcomes = set(title_outcomes_by_value.values())
        if len(distinct_title_outcomes) > 1:
            raise RuntimeError(
                f"LIVE_DUPLICATE_CALIBRATION_IDENTITY_DRIFT:{wid}:title"
            )
        title_observations_with_outcomes: list[dict[str, Any]] = []
        for item in title_observations:
            enriched = dict(item)
            if item.get("title") is None:
                enriched["calibration_seed_number"] = None
                enriched["calibration_match_basis"] = None
                enriched["calibration_outcome_compared"] = False
            else:
                outcome = title_outcomes_by_value[str(item["title"])]
                enriched["calibration_seed_number"] = outcome[0]
                enriched["calibration_match_basis"] = outcome[1]
                enriched["calibration_outcome_compared"] = True
            title_observations_with_outcomes.append(enriched)
        consensus_title_outcome = (
            next(iter(distinct_title_outcomes))
            if distinct_title_outcomes
            else (None, None)
        )
        row["title"] = (
            selected_title_observation["title"]
            if selected_title_observation is not None
            else None
        )
        row["title_resolution_policy"] = (
            "earliest_non_null_source_transaction_observation_after_"
            "calibration_outcome_consistency"
        )
        row["title_selected_source_id"] = (
            selected_title_observation["source_id"]
            if selected_title_observation is not None
            else None
        )
        row["title_selected_transaction_started_at"] = (
            selected_title_observation["transaction_started_at"]
            if selected_title_observation is not None
            else None
        )
        row["title_observation_count"] = len(title_observations)
        row["title_distinct_non_null_values"] = distinct_titles
        row["title_metadata_drift"] = len(distinct_titles) > 1
        row["title_calibration_consistent"] = True
        row["title_calibration_consensus_seed_number"] = consensus_title_outcome[0]
        row["title_calibration_consensus_match_basis"] = consensus_title_outcome[1]
        row["title_observations"] = title_observations_with_outcomes

        type_observations = sorted(
            type_observations_by_id[wid],
            key=lambda item: (
                str(item["transaction_started_at"]),
                str(item["source_id"]),
            ),
        )
        non_null_type_observations = [
            item for item in type_observations if item.get("type") is not None
        ]
        selected_type_observation = (
            non_null_type_observations[0] if non_null_type_observations else None
        )
        distinct_types = sorted(
            {str(item["type"]) for item in non_null_type_observations}
        )
        row["type"] = (
            selected_type_observation["type"]
            if selected_type_observation is not None
            else None
        )
        row["type_resolution_policy"] = "earliest_non_null_source_transaction_observation"
        row["type_selected_source_id"] = (
            selected_type_observation["source_id"]
            if selected_type_observation is not None
            else None
        )
        row["type_selected_transaction_started_at"] = (
            selected_type_observation["transaction_started_at"]
            if selected_type_observation is not None
            else None
        )
        row["type_observation_count"] = len(type_observations)
        row["type_distinct_non_null_values"] = distinct_types
        row["type_metadata_drift"] = len(distinct_types) > 1
        row["type_observations"] = type_observations

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
        consensus_seed = row.get("title_calibration_consensus_seed_number")
        consensus_basis = row.get("title_calibration_consensus_match_basis")
        if row.get("title") is not None and (seed_number, match_basis) != (
            consensus_seed,
            consensus_basis,
        ):
            raise RuntimeError(
                f"INTERNAL_CALIBRATION_CONSENSUS_MISMATCH:{row['provider_work_id']}"
            )
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
    ranked_ids = {row["provider_work_id"] for row in out}
    source_union_summary = live_drift_summary(merged)
    drift_witnesses = build_source_union_drift_witnesses(
        merged,
        ranked_ids=ranked_ids,
    )
    audit = {
        **source_union_summary,
        "drift_summary_scope": "DEDUPLICATED_SOURCE_PREFIX_UNION_BEFORE_GLOBAL_L_CUT",
        "source_union_unique_work_count": len(merged),
        "ranked_row_count": len(out),
        "drift_witness_count": len(drift_witnesses),
        "ranked_drift_witness_count": sum(
            1 for witness in drift_witnesses if witness["in_ranked_rows"]
        ),
        "outside_ranked_drift_witness_count": sum(
            1 for witness in drift_witnesses if not witness["in_ranked_rows"]
        ),
        "source_union_drift_witnesses": drift_witnesses,
        "ranked_row_drift_summary": live_drift_summary(out),
    }
    return out, boundary, audit


def build_source_union_drift_witnesses(
    rows: list[dict[str, Any]],
    *,
    ranked_ids: set[str],
) -> list[dict[str, Any]]:
    witnesses: list[dict[str, Any]] = []
    for row in rows:
        citation_drift = int(row.get("citation_count_drift", 0)) > 0
        title_drift = row.get("title_metadata_drift") is True
        type_drift = row.get("type_metadata_drift") is True
        if not (citation_drift or title_drift or type_drift):
            continue
        witness: dict[str, Any] = {
            "provider_work_id": row["provider_work_id"],
            "in_ranked_rows": row["provider_work_id"] in ranked_ids,
            "drift_dimensions": [
                name
                for name, active in (
                    ("citation", citation_drift),
                    ("title", title_drift),
                    ("type", type_drift),
                )
                if active
            ],
        }
        if citation_drift:
            witness["citation"] = {
                "selected_cited_by_count": row["cited_by_count"],
                "citation_resolution_policy": row["citation_resolution_policy"],
                "citation_selected_source_id": row["citation_selected_source_id"],
                "citation_selected_transaction_started_at": row[
                    "citation_selected_transaction_started_at"
                ],
                "citation_observation_count": row["citation_observation_count"],
                "citation_count_min_observed": row["citation_count_min_observed"],
                "citation_count_max_observed": row["citation_count_max_observed"],
                "citation_count_drift": row["citation_count_drift"],
                "citation_observations": row["citation_observations"],
            }
        if title_drift:
            witness["title"] = {
                "selected_title": row["title"],
                "title_resolution_policy": row["title_resolution_policy"],
                "title_selected_source_id": row["title_selected_source_id"],
                "title_selected_transaction_started_at": row[
                    "title_selected_transaction_started_at"
                ],
                "title_observation_count": row["title_observation_count"],
                "title_distinct_non_null_values": row[
                    "title_distinct_non_null_values"
                ],
                "title_calibration_consistent": row[
                    "title_calibration_consistent"
                ],
                "title_calibration_consensus_seed_number": row[
                    "title_calibration_consensus_seed_number"
                ],
                "title_calibration_consensus_match_basis": row[
                    "title_calibration_consensus_match_basis"
                ],
                "title_observations": row["title_observations"],
            }
        if type_drift:
            witness["type"] = {
                "selected_type": row["type"],
                "type_resolution_policy": row["type_resolution_policy"],
                "type_selected_source_id": row["type_selected_source_id"],
                "type_selected_transaction_started_at": row[
                    "type_selected_transaction_started_at"
                ],
                "type_observation_count": row["type_observation_count"],
                "type_distinct_non_null_values": row[
                    "type_distinct_non_null_values"
                ],
                "type_observations": row["type_observations"],
            }
        witnesses.append(witness)
    witnesses.sort(key=lambda witness: witness["provider_work_id"])
    return witnesses


def merge_source_prefixes(
    prefixes: list[dict[str, Any]],
    *,
    L: int,
    seeds: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    rows, boundary, _audit = _merge_source_prefixes_core(
        prefixes,
        L=L,
        seeds=seeds,
    )
    return rows, boundary


def merge_source_prefixes_with_audit(
    prefixes: list[dict[str, Any]],
    *,
    L: int,
    seeds: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int, dict[str, Any]]:
    return _merge_source_prefixes_core(prefixes, L=L, seeds=seeds)


def live_drift_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    citation_drifted = [
        row for row in rows if int(row.get("citation_count_drift", 0)) > 0
    ]
    title_drifted = [
        row for row in rows if row.get("title_metadata_drift") is True
    ]
    type_drifted = [
        row for row in rows if row.get("type_metadata_drift") is True
    ]
    any_optional_drift = bool(title_drifted or type_drifted)
    return {
        "citation_resolution_policy": "earliest_source_transaction_observation",
        "duplicate_citation_drift_work_count": len(citation_drifted),
        "maximum_duplicate_citation_drift": max(
            (int(row["citation_count_drift"]) for row in citation_drifted),
            default=0,
        ),
        "optional_title_resolution_policy": (
            "earliest_non_null_source_transaction_observation_after_"
            "calibration_outcome_consistency"
        ),
        "duplicate_optional_title_drift_work_count": len(title_drifted),
        "maximum_distinct_non_null_title_values": max(
            (
                len(row.get("title_distinct_non_null_values", []))
                for row in title_drifted
            ),
            default=0,
        ),
        "title_calibration_consistency_required": True,
        "optional_type_resolution_policy": (
            "earliest_non_null_source_transaction_observation"
        ),
        "duplicate_optional_type_drift_work_count": len(type_drifted),
        "maximum_distinct_non_null_type_values": max(
            (
                len(row.get("type_distinct_non_null_values", []))
                for row in type_drifted
            ),
            default=0,
        ),
        "capture_exactness": (
            "STATIC_PROVIDER_EXACT_NO_OBSERVED_CITATION_DRIFT"
            if not citation_drifted
            else "TRANSACTION_LOCAL_FROZEN_CAPTURE_OBSERVED_CITATION_DRIFT"
        ),
        "optional_metadata_capture": (
            "NO_CONFLICTING_NON_NULL_OPTIONAL_METADATA_OBSERVATIONS"
            if not any_optional_drift
            else "TRANSACTION_LOCAL_FROZEN_OPTIONAL_METADATA_OBSERVATIONS"
        ),
        "single_provider_snapshot_claimed": not (
            citation_drifted or any_optional_drift
        ),
    }

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

    rows, global_boundary, drift_audit = merge_source_prefixes_with_audit(
        prefixes, L=L, seeds=seeds
    )
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
        "ranking_strategy": "sourcewise_first_observation_freeze_v3",
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
        **drift_audit,
        "frozen_row_count": len(rows),
        "source_summaries": summaries,
        "rows": rows,
    }


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    if path.exists():
        raise RuntimeError(f"OUTPUT_ALREADY_EXISTS:{path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    if tmp.exists():
        raise RuntimeError(f"OUTPUT_TEMP_ALREADY_EXISTS:{tmp}")
    rendered = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    try:
        with tmp.open("x", encoding="utf-8") as handle:
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def make_source_artifact(
    *,
    era: str,
    era_condition: str,
    L: int,
    spec: dict[str, Any],
    prefix: dict[str, Any],
) -> dict[str, Any]:
    sid = str(spec["source_id"])
    if prefix.get("source_id") != sid:
        raise ValueError("source prefix/source spec identity mismatch")
    rows = prefix.get("rows")
    if not isinstance(rows, list):
        raise ValueError("source prefix missing rows")
    return {
        "schema_version": SOURCE_PREFIX_SCHEMA,
        "owner_issue": 167,
        "provider": "OpenAlex",
        "ranking_strategy": "sourcewise_first_observation_freeze_v3",
        "era": era,
        "era_condition": era_condition,
        "source_id": sid,
        "source_channel": spec["channel"],
        "source_index": int(spec["source_index"]),
        "source_key_digest": sha256_text(str(spec["source_key"])),
        "base_query_digest": sha256_text(str(spec["query"])),
        "era_query_digest": prefix["query_digest"],
        "minimum_candidate_rows": L,
        "provider_sort": "cited_by_count:desc",
        "provider_page_size": PAGE_SIZE,
        "paging": "basic_page",
        "transport_attempts_per_request": 1,
        "transaction_started_at": prefix["transaction_started_at"],
        "transaction_completed_at": prefix["transaction_completed_at"],
        "pages": int(prefix["pages"]),
        "provider_meta_count_first": int(prefix["provider_meta_count_first"]),
        "provider_meta_count_last": int(prefix["provider_meta_count_last"]),
        "provider_meta_count_signed_drift": int(
            prefix["provider_meta_count_signed_drift"]
        ),
        "source_exhausted": bool(prefix["source_exhausted"]),
        "source_boundary_cited_by_count": prefix["source_boundary_cited_by_count"],
        "source_boundary_tie_closed": True,
        "frozen_row_count": len(rows),
        "rows": rows,
    }


def validate_source_artifact(
    artifact: dict[str, Any],
    *,
    era: str,
    era_condition: str,
    L: int,
    spec: dict[str, Any],
) -> None:
    sid = str(spec["source_id"])
    if artifact.get("schema_version") != SOURCE_PREFIX_SCHEMA:
        raise ValueError(f"{sid}: source artifact schema mismatch")
    if artifact.get("era") != era or artifact.get("era_condition") != era_condition:
        raise ValueError(f"{sid}: source artifact era mismatch")
    if artifact.get("source_id") != sid:
        raise ValueError(f"{sid}: source artifact identity mismatch")
    if artifact.get("source_channel") != spec["channel"]:
        raise ValueError(f"{sid}: source channel mismatch")
    if int(artifact.get("source_index", -1)) != int(spec["source_index"]):
        raise ValueError(f"{sid}: source index mismatch")
    if artifact.get("base_query_digest") != sha256_text(str(spec["query"])):
        raise ValueError(f"{sid}: base query digest mismatch")
    expected_era_query = sampling.append_filter(str(spec["query"]), era_condition)
    if artifact.get("era_query_digest") != sha256_text(expected_era_query):
        raise ValueError(f"{sid}: era query digest mismatch")
    if int(artifact.get("minimum_candidate_rows", -1)) != L:
        raise ValueError(f"{sid}: source artifact L mismatch")
    if artifact.get("provider_sort") != "cited_by_count:desc":
        raise ValueError(f"{sid}: provider sort mismatch")
    if artifact.get("paging") != "basic_page":
        raise ValueError(f"{sid}: paging mode mismatch")
    if artifact.get("transport_attempts_per_request") != 1:
        raise ValueError(f"{sid}: transport-attempt invariant mismatch")
    if artifact.get("source_boundary_tie_closed") is not True:
        raise ValueError(f"{sid}: source boundary tie not closed")

    rows = artifact.get("rows")
    if not isinstance(rows, list):
        raise ValueError(f"{sid}: source artifact rows missing")
    if int(artifact.get("frozen_row_count", -1)) != len(rows):
        raise ValueError(f"{sid}: source artifact row-count mismatch")
    validate_provider_order(rows, source=sid)

    exhausted = artifact.get("source_exhausted") is True
    boundary = artifact.get("source_boundary_cited_by_count")
    if not rows:
        if not exhausted or boundary is not None:
            raise ValueError(f"{sid}: invalid empty source artifact")
        return

    if len(rows) < L:
        if not exhausted:
            raise ValueError(f"{sid}: short source prefix without exhaustion")
        if int(boundary) != int(rows[-1]["cited_by_count"]):
            raise ValueError(f"{sid}: exhausted-source boundary mismatch")
    else:
        if boundary is None:
            raise ValueError(f"{sid}: missing source boundary")
        if int(rows[-1]["cited_by_count"]) != int(boundary):
            raise ValueError(f"{sid}: source boundary/tail mismatch")
        if any(int(row["cited_by_count"]) < int(boundary) for row in rows):
            raise ValueError(f"{sid}: source artifact contains below-boundary row")


def load_complete_source_directory(
    source_dir: Path,
    *,
    era: str,
    era_condition: str,
    L: int,
    sources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    expected_names = {f"{spec['source_id']}.json" for spec in sources}
    actual_names = {path.name for path in source_dir.glob("*.json")}
    if actual_names != expected_names:
        missing = sorted(expected_names - actual_names)
        extra = sorted(actual_names - expected_names)
        raise RuntimeError(
            f"SOURCE_ARTIFACT_SET_INCOMPLETE:missing={missing}:extra={extra}"
        )

    artifacts: list[dict[str, Any]] = []
    for spec in sources:
        path = source_dir / f"{spec['source_id']}.json"
        artifact = load_json(path)
        validate_source_artifact(
            artifact,
            era=era,
            era_condition=era_condition,
            L=L,
            spec=spec,
        )
        artifacts.append(artifact)
    return artifacts


def merge_source_artifacts(
    artifacts: list[dict[str, Any]],
    *,
    era: str,
    era_condition: str,
    L: int,
    seeds: list[dict[str, Any]],
) -> dict[str, Any]:
    if len(artifacts) != 51:
        raise RuntimeError(f"SOURCE_ARTIFACT_COUNT_MISMATCH:{len(artifacts)}")
    prefixes = [
        {
            "source_id": artifact["source_id"],
            "transaction_started_at": artifact["transaction_started_at"],
            "rows": artifact["rows"],
        }
        for artifact in artifacts
    ]
    rows, global_boundary, drift_audit = merge_source_prefixes_with_audit(
        prefixes, L=L, seeds=seeds
    )
    summaries = [
        {
            key: artifact[key]
            for key in (
                "source_id",
                "base_query_digest",
                "era_query_digest",
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
        for artifact in artifacts
    ]
    return {
        "schema_version": RANKED_ERA_SCHEMA,
        "owner_issue": 167,
        "provider": "OpenAlex",
        "ranking_strategy": "sourcewise_first_observation_freeze_v3",
        "execution_protocol": "durable_per_source_then_local_merge",
        "era": era,
        "era_condition": era_condition,
        "provider_sort": "cited_by_count:desc",
        "local_canonical_sort": "cited_by_count desc, provider_work_id asc",
        "provider_page_size": PAGE_SIZE,
        "paging": "basic_page",
        "transport_attempts_per_request": 1,
        "frozen_source_count": len(artifacts),
        "minimum_candidate_rows": L,
        "global_boundary_cited_by_count": global_boundary,
        "global_boundary_tie_closed": True,
        "merge_provider_calls": 0,
        **drift_audit,
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
        "transaction_started_at": f"2000-01-01T00:00:{source[-1] if source[-1].isdigit() else '0'}0+00:00",
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
    assert contract["execution_protocol"]["openalex_api_key_required"] is True
    assert contract["execution_protocol"]["minimum_remaining_credits_before_resume"] == 1500
    assert contract["candidate_ladder"]["multiplier"] == 5
    assert contract["execution_protocol"]["integrated_51_source_provider_run"] == "DISABLED"
    assert contract["execution_protocol"]["merge_provider_calls"] == 0
    quotas = rankv1.quota_map(era_freeze)
    assert sum(5 * quota for quota in quotas.values()) == 5000

    rate_status = parse_rate_limit_status(
        {
            "rate_limit": {
                "credits_limit": 10000,
                "credits_remaining": 10000,
                "resets_in_seconds": 3600,
            }
        },
        {},
    )
    assert rate_status["credits_remaining"] == 10000
    assert rate_status["remaining_list_call_equivalent"] == 10000
    assert rate_status["api_key_value_recorded"] is False
    try:
        parse_rate_limit_status(
            {"rate_limit": {"credits_remaining": 1499}},
            {},
        )
        raise AssertionError("insufficient OpenAlex budget must fail closed")
    except RuntimeError as exc:
        assert "OPENALEX_RATE_LIMIT_BUDGET_INSUFFICIENT" in str(exc)

    # Authentication failure remains distinct from budget exhaustion and ranking.
    simulated_401 = RuntimeError(
        "OPENALEX_API_KEY_INVALID:"
        "provider returned HTTP 401 for keyed rate-limit preflight"
    )
    assert "OPENALEX_API_KEY_INVALID" in str(simulated_401)

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

    durable_condition = "year >= (2000) and year <= (2009)"
    durable_rows = [
        {"provider_work_id":"W901","doi":None,"title":"durable-a","year":2000,"cited_by_count":100,"type":"article"},
        {"provider_work_id":"W902","doi":None,"title":"durable-b","year":2000,"cited_by_count":90,"type":"article"},
        {"provider_work_id":"W903","doi":None,"title":"durable-c","year":2000,"cited_by_count":80,"type":"article"},
    ]
    durable_era_query = sampling.append_filter(str(specs[0]["query"]), durable_condition)
    durable_prefix = {
        "source_id": specs[0]["source_id"],
        "query_digest": sha256_text(durable_era_query),
        "transaction_started_at":"2000-01-01T00:00:00+00:00",
        "transaction_completed_at":"2000-01-01T00:00:01+00:00",
        "pages":1,
        "provider_meta_count_first":3,
        "provider_meta_count_last":3,
        "provider_meta_count_signed_drift":0,
        "source_exhausted":True,
        "source_boundary_cited_by_count":80,
        "rows":durable_rows,
    }
    durable_artifact = make_source_artifact(
        era="2000-2009", era_condition=durable_condition, L=3,
        spec=specs[0], prefix=durable_prefix,
    )
    validate_source_artifact(
        durable_artifact, era="2000-2009", era_condition=durable_condition,
        L=3, spec=specs[0],
    )
    assert durable_artifact["frozen_row_count"] == 3

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

    # Missing display_name is valid ranking metadata; title/year calibration
    # fallback simply becomes unavailable for that row.
    missing_title = rankv1.normalize_provider_item(
        {
            "id": "https://openalex.org/W110556196",
            "doi": None,
            "display_name": None,
            "publication_year": 1975,
            "cited_by_count": 42,
            "type": "article",
        }
    )
    assert missing_title["provider_work_id"] == "W110556196"
    assert missing_title["title"] is None
    assert rankv1.calibration_match(missing_title, seeds) == (None, None)

    # Blank/non-string optional provider values normalize to null as well.
    for bad_title in ("", "   ", 123, [], {}):
        normalized = rankv1.normalize_provider_item(
            {
                "id": "https://openalex.org/W110556196",
                "doi": None,
                "display_name": bad_title,
                "publication_year": 1975,
                "cited_by_count": 42,
                "type": {"unexpected": "shape"},
            }
        )
        assert normalized["title"] is None
        assert normalized["type"] is None
        assert rankv1.calibration_match(normalized, seeds) == (None, None)

    # Optional null/non-null metadata is coalesced deterministically.
    optional_null = row("W29", 77, "filled title")
    optional_null["title"] = None
    optional_null["doi"] = None
    optional_filled = row("W29", 77, "filled title")
    optional_filled["doi"] = "10.1000/example"
    coalesced, _ = merge_source_prefixes(
        [
            {"source_id": "A", "transaction_started_at": "2000-01-01T00:00:01+00:00", "rows": [optional_null]},
            {"source_id": "B", "transaction_started_at": "2000-01-01T00:00:02+00:00", "rows": [optional_filled]},
        ],
        L=1,
        seeds=seeds,
    )
    assert coalesced[0]["title"] == "filled title"
    assert coalesced[0]["doi"] == "10.1000/example"

    # Non-null title drift is allowed only when every distinct title produces
    # the same Top50 calibration outcome under the frozen DOI/year.
    title_a = row("W28", 76, "title-a")
    title_b = row("W28", 76, "title-b")
    title_rows, _ = merge_source_prefixes(
        [
            {"source_id": "A", "transaction_started_at": "2000-01-01T00:00:01+00:00", "rows": [title_a]},
            {"source_id": "B", "transaction_started_at": "2000-01-01T00:00:02+00:00", "rows": [title_b]},
        ],
        L=1,
        seeds=seeds,
    )
    assert title_rows[0]["title"] == "title-a"
    assert title_rows[0]["title_metadata_drift"] is True
    assert title_rows[0]["title_calibration_consistent"] is True
    assert title_rows[0]["title_distinct_non_null_values"] == ["title-a", "title-b"]
    assert title_rows[0]["calibration_seed_number"] is None
    assert live_drift_summary(title_rows) == {
        "citation_resolution_policy": "earliest_source_transaction_observation",
        "duplicate_citation_drift_work_count": 0,
        "maximum_duplicate_citation_drift": 0,
        "optional_title_resolution_policy": (
            "earliest_non_null_source_transaction_observation_after_"
            "calibration_outcome_consistency"
        ),
        "duplicate_optional_title_drift_work_count": 1,
        "maximum_distinct_non_null_title_values": 2,
        "title_calibration_consistency_required": True,
        "optional_type_resolution_policy": "earliest_non_null_source_transaction_observation",
        "duplicate_optional_type_drift_work_count": 0,
        "maximum_distinct_non_null_type_values": 0,
        "capture_exactness": "STATIC_PROVIDER_EXACT_NO_OBSERVED_CITATION_DRIFT",
        "optional_metadata_capture": "TRANSACTION_LOCAL_FROZEN_OPTIONAL_METADATA_OBSERVATIONS",
        "single_provider_snapshot_claimed": False,
    }

    seed0 = retrieval_config["seeds"][0]
    calibration_title = row("W281", 76, str(seed0["title"]))
    calibration_title["year"] = int(seed0["year"])
    noncal_title = row("W281", 76, "synthetic non-seed title")
    noncal_title["year"] = int(seed0["year"])
    try:
        merge_source_prefixes(
            [
                {"source_id": "A", "transaction_started_at": "2000-01-01T00:00:01+00:00", "rows": [calibration_title]},
                {"source_id": "B", "transaction_started_at": "2000-01-01T00:00:02+00:00", "rows": [noncal_title]},
            ],
            L=1,
            seeds=seeds,
        )
        raise AssertionError("calibration-changing title drift must fail")
    except RuntimeError as exc:
        assert "LIVE_DUPLICATE_CALIBRATION_IDENTITY_DRIFT:W281:title" in str(exc)

    doi_a = row("W282", 76, "same-title")
    doi_a["doi"] = "10.1000/a"
    doi_b = row("W282", 76, "same-title")
    doi_b["doi"] = "10.1000/b"
    try:
        merge_source_prefixes(
            [
                {"source_id": "A", "transaction_started_at": "2000-01-01T00:00:01+00:00", "rows": [doi_a]},
                {"source_id": "B", "transaction_started_at": "2000-01-01T00:00:02+00:00", "rows": [doi_b]},
            ],
            L=1,
            seeds=seeds,
        )
        raise AssertionError("conflicting non-null DOI must fail")
    except RuntimeError as exc:
        assert "LIVE_DUPLICATE_METADATA_DRIFT:W282:doi" in str(exc)

    # Optional type drift is descriptive only. Preserve every observation,
    # freeze the earliest non-null type, and do not let it affect ranking or
    # calibration identity.
    type_a = row("W27", 75, "same-title")
    type_a["type"] = "article"
    type_b = row("W27", 75, "same-title")
    type_b["type"] = "book-chapter"
    type_rows, _ = merge_source_prefixes(
        [
            {"source_id": "A", "transaction_started_at": "2000-01-01T00:00:01+00:00", "rows": [type_a]},
            {"source_id": "B", "transaction_started_at": "2000-01-01T00:00:02+00:00", "rows": [type_b]},
        ],
        L=1,
        seeds=seeds,
    )
    assert type_rows[0]["type"] == "article"
    assert type_rows[0]["type_metadata_drift"] is True
    assert type_rows[0]["type_distinct_non_null_values"] == ["article", "book-chapter"]
    assert type_rows[0]["type_observation_count"] == 2
    assert type_rows[0]["type_selected_source_id"] == "A"
    assert live_drift_summary(type_rows) == {
        "citation_resolution_policy": "earliest_source_transaction_observation",
        "duplicate_citation_drift_work_count": 0,
        "maximum_duplicate_citation_drift": 0,
        "optional_title_resolution_policy": (
            "earliest_non_null_source_transaction_observation_after_"
            "calibration_outcome_consistency"
        ),
        "duplicate_optional_title_drift_work_count": 0,
        "maximum_distinct_non_null_title_values": 0,
        "title_calibration_consistency_required": True,
        "optional_type_resolution_policy": "earliest_non_null_source_transaction_observation",
        "duplicate_optional_type_drift_work_count": 1,
        "maximum_distinct_non_null_type_values": 2,
        "capture_exactness": "STATIC_PROVIDER_EXACT_NO_OBSERVED_CITATION_DRIFT",
        "optional_metadata_capture": "TRANSACTION_LOCAL_FROZEN_OPTIONAL_METADATA_OBSERVATIONS",
        "single_provider_snapshot_claimed": False,
    }

    type_null = row("W26", 74, "same-title")
    type_null["type"] = None
    type_later = row("W26", 74, "same-title")
    type_later["type"] = "article"
    type_null_rows, _ = merge_source_prefixes(
        [
            {"source_id": "A", "transaction_started_at": "2000-01-01T00:00:01+00:00", "rows": [type_null]},
            {"source_id": "B", "transaction_started_at": "2000-01-01T00:00:02+00:00", "rows": [type_later]},
        ],
        L=1,
        seeds=seeds,
    )
    assert type_null_rows[0]["type"] == "article"
    assert type_null_rows[0]["type_metadata_drift"] is False

    # Drift audit is over the entire deduplicated source-prefix union, not only
    # the global ranked ladder. A drifted Work below the L boundary remains an
    # audit witness but is never promoted into ranked rows.
    high = row("W320", 100, "high")
    low_type_a = row("W321", 10, "low")
    low_type_a["type"] = "article"
    low_type_b = row("W321", 10, "low")
    low_type_b["type"] = "book-chapter"
    audited_rows, audited_boundary, audited = merge_source_prefixes_with_audit(
        [
            {"source_id": "A", "transaction_started_at": "2000-01-01T00:00:01+00:00", "rows": [high, low_type_a]},
            {"source_id": "B", "transaction_started_at": "2000-01-01T00:00:02+00:00", "rows": [low_type_b]},
        ],
        L=1,
        seeds=seeds,
    )
    assert audited_boundary == 100
    assert [item["provider_work_id"] for item in audited_rows] == ["W320"]
    assert audited["drift_summary_scope"] == (
        "DEDUPLICATED_SOURCE_PREFIX_UNION_BEFORE_GLOBAL_L_CUT"
    )
    assert audited["source_union_unique_work_count"] == 2
    assert audited["ranked_row_count"] == 1
    assert audited["duplicate_optional_type_drift_work_count"] == 1
    assert audited["drift_witness_count"] == 1
    assert audited["ranked_drift_witness_count"] == 0
    assert audited["outside_ranked_drift_witness_count"] == 1
    assert audited["source_union_drift_witnesses"][0]["provider_work_id"] == "W321"
    assert audited["source_union_drift_witnesses"][0]["in_ranked_rows"] is False
    assert audited["source_union_drift_witnesses"][0]["type"][
        "type_distinct_non_null_values"
    ] == ["article", "book-chapter"]

    # Duplicate Work-ID citation drift is preserved without allowing a later
    # observation to overwrite the first frozen score.
    drift = [
        {"source_id": "A", "transaction_started_at": "2000-01-01T00:00:01+00:00", "rows": [row("W30", 10, "same")]},
        {"source_id": "B", "transaction_started_at": "2000-01-01T00:00:02+00:00", "rows": [row("W30", 11, "same")]},
    ]
    drift_rows, _ = merge_source_prefixes(drift, L=1, seeds=seeds)
    assert drift_rows[0]["cited_by_count"] == 10
    assert drift_rows[0]["citation_count_min_observed"] == 10
    assert drift_rows[0]["citation_count_max_observed"] == 11
    assert drift_rows[0]["citation_count_drift"] == 1
    assert drift_rows[0]["citation_observation_count"] == 2
    assert drift_rows[0]["citation_selected_source_id"] == "A"
    assert live_drift_summary(drift_rows) == {
        "citation_resolution_policy": "earliest_source_transaction_observation",
        "duplicate_citation_drift_work_count": 1,
        "maximum_duplicate_citation_drift": 1,
        "optional_title_resolution_policy": (
            "earliest_non_null_source_transaction_observation_after_"
            "calibration_outcome_consistency"
        ),
        "duplicate_optional_title_drift_work_count": 0,
        "maximum_distinct_non_null_title_values": 0,
        "title_calibration_consistency_required": True,
        "optional_type_resolution_policy": "earliest_non_null_source_transaction_observation",
        "duplicate_optional_type_drift_work_count": 0,
        "maximum_distinct_non_null_type_values": 0,
        "capture_exactness": "TRANSACTION_LOCAL_FROZEN_CAPTURE_OBSERVED_CITATION_DRIFT",
        "optional_metadata_capture": "NO_CONFLICTING_NON_NULL_OPTIONAL_METADATA_OBSERVATIONS",
        "single_provider_snapshot_claimed": False,
    }

    reverse_drift = [
        {"source_id": "A", "transaction_started_at": "2000-01-01T00:00:01+00:00", "rows": [row("W31", 12, "same")]},
        {"source_id": "B", "transaction_started_at": "2000-01-01T00:00:02+00:00", "rows": [row("W31", 9, "same")]},
    ]
    reverse_rows, _ = merge_source_prefixes(reverse_drift, L=1, seeds=seeds)
    assert reverse_rows[0]["cited_by_count"] == 12
    assert reverse_rows[0]["citation_count_drift"] == 3

    # Calibration exclusion survives sourcewise merge.
    simon = row("W40", 1000, "A Behavioral Model of Rational Choice")
    simon["doi"] = "10.2307/1884852"
    simon["year"] = 1955
    normal = row("W41", 900, "Not a seed")
    normal["year"] = 1955
    cal_rows, _ = merge_source_prefixes(
        [
            {"source_id": "A", "transaction_started_at": "2000-01-01T00:00:01+00:00", "rows": [simon, normal]},
            {"source_id": "B", "transaction_started_at": "2000-01-01T00:00:02+00:00", "rows": [simon]},
        ],
        L=1,
        seeds=seeds,
    )
    assert cal_rows[0]["screening_state"] == "CALIBRATION_EXCLUDED"
    assert cal_rows[0]["calibration_seed_number"] == 2

    # Durable provider-free merge must expose the audit at artifact top level.
    # Use 51 synthetic durable artifacts without invoking any provider.
    artifact_rows = [row("W500", 100, "artifact-high")]
    synthetic_artifacts = []
    for idx in range(51):
        synthetic_artifacts.append(
            {
                "source_id": f"S{idx:03d}",
                "base_query_digest": f"base-{idx}",
                "era_query_digest": f"era-{idx}",
                "transaction_started_at": f"2000-01-01T00:{idx:02d}:00+00:00",
                "transaction_completed_at": f"2000-01-01T00:{idx:02d}:01+00:00",
                "pages": 1,
                "provider_meta_count_first": 1,
                "provider_meta_count_last": 1,
                "provider_meta_count_signed_drift": 0,
                "source_exhausted": True,
                "source_boundary_cited_by_count": 100,
                "frozen_row_count": 1,
                "rows": artifact_rows,
            }
        )
    merged_artifact = merge_source_artifacts(
        synthetic_artifacts,
        era="2000-2009",
        era_condition="synthetic",
        L=1,
        seeds=seeds,
    )
    assert merged_artifact["schema_version"] == RANKED_ERA_SCHEMA
    assert merged_artifact["merge_provider_calls"] == 0
    assert merged_artifact["drift_summary_scope"] == (
        "DEDUPLICATED_SOURCE_PREFIX_UNION_BEFORE_GLOBAL_L_CUT"
    )
    assert merged_artifact["source_union_unique_work_count"] == 1
    assert "source_union_drift_witnesses" in merged_artifact
    assert "ranked_row_drift_summary" in merged_artifact

    assert contract["real_ranking_execution_authorized"] in (False, True)
    print("PAPER2_SAMPLING_V2_SOURCEWISE_RANKING_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=Path("research/paper2/sampling_v2_ranking_sourcewise.json"))
    parser.add_argument("--sampling-protocol", type=Path, default=Path("research/paper2/sampling_v2.json"))
    parser.add_argument("--era-freeze", type=Path, default=Path("research/paper2/sampling_v2_era_freeze.json"))
    parser.add_argument("--retrieval-config", type=Path, default=Path("research/paper2/retrieval_v1.json"))
    parser.add_argument("--counts-artifact", type=Path)
    parser.add_argument("--era")
    parser.add_argument("--source-id")
    parser.add_argument("--source-dir", type=Path)
    parser.add_argument("--fetch-source", action="store_true")
    parser.add_argument("--merge-era-sources", action="store_true")
    parser.add_argument("--fetch-ranked-era", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--rate-limit-preflight", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pause", type=float, default=0.12)
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    contract = load_contract(args.contract)

    if args.rate_limit_preflight:
        if args.fetch_source or args.merge_era_sources or args.fetch_ranked_era:
            raise ValueError("rate-limit preflight must be a standalone operation")
        if args.output is None:
            raise ValueError("--rate-limit-preflight requires --output")
        if args.output.exists():
            raise RuntimeError(f"OUTPUT_ALREADY_EXISTS:{args.output}")
        api_key = require_openalex_api_key()
        status = rate_limit_preflight(api_key)
        write_json_atomic(args.output, status)
        return 0
    if contract.get("real_ranking_execution_authorized") is not True:
        raise RuntimeError("REAL_SOURCEWISE_RANKING_EXECUTION_NOT_AUTHORIZED")
    if args.fetch_ranked_era:
        raise RuntimeError(
            "INTEGRATED_ERA_PROVIDER_RUN_DISABLED:"
            "use --fetch-source then --merge-era-sources"
        )

    protocol = sampling.load_protocol(args.sampling_protocol)
    era_freeze = sampling.validate_era_freeze(protocol, args.era_freeze)
    retrieval_config = load_json(args.retrieval_config)
    seeds = rankv1.seed_registry(retrieval_config)
    quotas = rankv1.quota_map(era_freeze)
    conditions = rankv1.era_conditions(era_freeze)

    if not args.era or args.era not in quotas:
        raise ValueError("a frozen --era is required")
    if args.counts_artifact is None:
        raise ValueError("--counts-artifact is required")
    if args.output is None:
        raise ValueError("--output is required")
    if args.output.exists():
        raise RuntimeError(f"OUTPUT_ALREADY_EXISTS:{args.output}")

    counts = sampling.validate_counts_artifact(args.counts_artifact)
    sources = build_sources(retrieval_config, counts)
    L = int(contract["candidate_ladder"]["multiplier"]) * quotas[args.era]
    era_condition = conditions[args.era]

    if args.fetch_source:
        if args.merge_era_sources:
            raise ValueError("choose exactly one durable operation")
        if not args.source_id:
            raise ValueError("--fetch-source requires --source-id")
        matched = [spec for spec in sources if spec["source_id"] == args.source_id]
        if len(matched) != 1:
            raise ValueError(f"unknown frozen source id: {args.source_id}")
        spec = matched[0]
        api_key = require_openalex_api_key()
        client = retrieval.OpenAlexClient(
            api_key=api_key,
            mailto=None,
            pause=args.pause,
        )
        prefix = fetch_source_prefix(
            client, query=str(spec["query"]), era_condition=era_condition,
            source=str(spec["source_id"]), L=L,
        )
        artifact = make_source_artifact(
            era=args.era, era_condition=era_condition, L=L,
            spec=spec, prefix=prefix,
        )
        validate_source_artifact(
            artifact, era=args.era, era_condition=era_condition,
            L=L, spec=spec,
        )
        write_json_atomic(args.output, artifact)
        return 0

    if args.merge_era_sources:
        if args.source_id:
            raise ValueError("--merge-era-sources does not accept --source-id")
        if args.source_dir is None:
            raise ValueError("--merge-era-sources requires --source-dir")
        artifacts = load_complete_source_directory(
            args.source_dir, era=args.era, era_condition=era_condition,
            L=L, sources=sources,
        )
        result = merge_source_artifacts(
            artifacts, era=args.era, era_condition=era_condition,
            L=L, seeds=seeds,
        )
        write_json_atomic(args.output, result)
        return 0

    parser.error("choose --self-test, --fetch-source, or --merge-era-sources")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
