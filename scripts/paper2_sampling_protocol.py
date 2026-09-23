#!/usr/bin/env python3
"""Paper 2 outcome-blind held-out sampling/statistical protocol utilities.

Owner: #158
Coordination: #130
Upstream authorities: #133, #140, #143, #145

This module is intentionally fail-closed for real sampling until
research/paper2/sampling_v1.json explicitly freezes a final N, reserve N,
stopping rule, and real_sampling_authorized=true.

It never performs eligibility adjudication, ClaimIR extraction, decomposition,
basis revision, or real null-result evaluation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import heapq
import json
import math
import re
import sqlite3
import tempfile
from pathlib import Path
from typing import Any, Iterable

PROTOCOL_VERSION = "paper2-sampling-v1"
SAMPLE_MANIFEST_VERSION = "paper2-sample-manifest-v1"
EXPECTED_MANIFEST_ROLE = "candidate_manifest_not_eligible_corpus"
CHANNEL_ORDER = ("R1", "R2", "R3")
OUTCOME_FIELDS_FORBIDDEN = {
    "basis_mapping",
    "coverage_score",
    "decomposition_failure",
    "decomposition_result",
    "decomposition_success",
    "lean_result",
    "lean_theorem",
    "residual_type",
    "verified_pass",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def load_protocol(path: Path) -> dict[str, Any]:
    protocol = load_json(path)
    if protocol.get("schema_version") != PROTOCOL_VERSION:
        raise ValueError("unexpected sampling protocol version")
    if OUTCOME_FIELDS_FORBIDDEN & set(protocol):
        raise ValueError("sampling protocol contains forbidden outcome fields")
    if protocol.get("design", {}).get("phase_design") != "two-phase_probability_sample":
        raise ValueError("Paper 2 sampling v1 must remain two-phase")
    if protocol.get("claim_sampling", {}).get("max_claims_per_work") != 3:
        raise ValueError("Paper 2 sampling v1 claim cap must remain 3")
    if protocol.get("null_schedule", {}).get("permutations") != 100:
        raise ValueError("Paper 2 sampling v1 null schedule must remain J=100")
    return protocol


def sha_rank(*parts: str) -> str:
    h = hashlib.sha256()
    for i, part in enumerate(parts):
        if i:
            h.update(b"\x00")
        h.update(part.encode("utf-8"))
    return h.hexdigest()


def normalize_title(value: str) -> str:
    value = value.casefold()
    value = re.sub(r"[^\w\s]+", " ", value, flags=re.UNICODE)
    return " ".join(value.split())


def normalize_doi(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return re.sub(
        r"^https?://(?:dx\.)?doi\.org/", "", value.strip(), flags=re.I
    ).casefold()


def normalize_arxiv(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return re.sub(
        r"^https?://arxiv\.org/(?:abs|pdf)/", "", value.strip(), flags=re.I
    ).removesuffix(".pdf").casefold()


def normalize_isbn(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    result = re.sub(r"[^0-9Xx]", "", value).upper()
    return result or None


def citation_band(cited_by_count: int) -> str:
    if cited_by_count < 1:
        raise ValueError("retrieval-v1 held-out population cannot contain uncited work")
    if cited_by_count <= 9:
        return "1-9"
    if cited_by_count <= 99:
        return "10-99"
    if cited_by_count <= 999:
        return "100-999"
    if cited_by_count <= 9999:
        return "1000-9999"
    return ">=10000"


def channel_class(channels: Iterable[str]) -> str:
    observed = set(channels)
    if not observed or not observed <= set(CHANNEL_ORDER):
        raise ValueError(f"invalid retrieval-channel membership: {sorted(observed)}")
    result = "".join(ch for ch in CHANNEL_ORDER if ch in observed)
    if result not in {"R1", "R2", "R3", "R1R2", "R1R3", "R2R3", "R1R2R3"}:
        raise ValueError(f"invalid channel class: {result}")
    return result


def metadata_value(conn: sqlite3.Connection, key: str) -> Any:
    row = conn.execute("SELECT value FROM run_metadata WHERE key=?", (key,)).fetchone()
    if row is None:
        raise ValueError(f"manifest metadata missing: {key}")
    return json.loads(row[0])


def validate_population_manifest(conn: sqlite3.Connection) -> dict[str, Any]:
    schema = metadata_value(conn, "manifest_schema_version")
    status = metadata_value(conn, "run_status")
    role = metadata_value(conn, "artifact_role")
    digest = metadata_value(conn, "logical_manifest_digest")
    run_id = metadata_value(conn, "run_id")
    if schema != "paper2-retrieval-v1-manifest-transaction-v1":
        raise ValueError(f"unexpected retrieval manifest schema: {schema}")
    if status != "COMPLETE":
        raise ValueError("sampling requires a COMPLETE retrieval manifest")
    if role != EXPECTED_MANIFEST_ROLE:
        raise ValueError(f"unexpected retrieval manifest role: {role}")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError("sampling requires a frozen logical_manifest_digest")
    if not isinstance(run_id, str) or not run_id:
        raise ValueError("sampling requires a retrieval manifest run_id")
    return {"digest": digest, "run_id": run_id}


def top50_seed_keys(retrieval_config: dict[str, Any]) -> list[dict[str, Any]]:
    if retrieval_config.get("schema_version") != "paper2-retrieval-v1":
        raise ValueError("unexpected retrieval config version")
    seeds = retrieval_config.get("seeds")
    if not isinstance(seeds, list) or len(seeds) != 50:
        raise ValueError("Top50 retrieval config must contain exactly 50 seeds")
    return seeds


def stable_id_isbn(stable_ids_json: str) -> str | None:
    try:
        ids = json.loads(stable_ids_json)
    except json.JSONDecodeError as exc:
        raise ValueError("invalid stable_ids_json in retrieval manifest") from exc
    if not isinstance(ids, dict):
        return None
    for key, value in ids.items():
        if isinstance(key, str) and "isbn" in key.casefold():
            isbn = normalize_isbn(value)
            if isbn:
                return isbn
    return None


def matches_calibration_seed(work: dict[str, Any], seeds: list[dict[str, Any]]) -> bool:
    doi = normalize_doi(work.get("doi"))
    arxiv = normalize_arxiv(work.get("arxiv"))
    isbn = normalize_isbn(work.get("isbn"))
    title = normalize_title(str(work.get("title") or ""))
    year = work.get("publication_year")

    for seed in seeds:
        if doi and doi == normalize_doi(seed.get("doi")):
            return True
        if arxiv and arxiv == normalize_arxiv(seed.get("arxiv")):
            return True
        if isbn and isbn == normalize_isbn(seed.get("isbn")):
            return True
        if (
            title
            and year is not None
            and title == normalize_title(str(seed.get("title") or ""))
            and int(year) == int(seed.get("year"))
        ):
            return True
    return False


def iter_population_rows(
    conn: sqlite3.Connection,
    retrieval_config: dict[str, Any],
    counters: dict[str, int] | None = None,
) -> Iterable[dict[str, Any]]:
    seeds = top50_seed_keys(retrieval_config)
    if counters is None:
        counters = {}
    counters.clear()
    counters.update(
        {
            "manifest_rows_seen": 0,
            "calibration_works_excluded": 0,
            "heldout_works_seen": 0,
        }
    )
    sql = """
      SELECT
        w.work_id,
        w.title,
        w.publication_year,
        w.doi,
        w.arxiv,
        w.stable_ids_json,
        w.cited_by_count,
        EXISTS(SELECT 1 FROM retrieval_channels r WHERE r.work_id=w.work_id AND r.channel='R1'),
        EXISTS(SELECT 1 FROM retrieval_channels r WHERE r.work_id=w.work_id AND r.channel='R2'),
        EXISTS(SELECT 1 FROM retrieval_channels r WHERE r.work_id=w.work_id AND r.channel='R3')
      FROM works w
    """
    for (
        work_id,
        title,
        year,
        doi,
        arxiv,
        stable_ids_json,
        cited,
        r1,
        r2,
        r3,
    ) in conn.execute(sql):
        counters["manifest_rows_seen"] += 1
        channels = [ch for ch, present in zip(CHANNEL_ORDER, (r1, r2, r3)) if present]
        work = {
            "work_id": work_id,
            "title": title,
            "publication_year": year,
            "doi": doi,
            "arxiv": arxiv,
            "isbn": stable_id_isbn(stable_ids_json),
            "cited_by_count": int(cited),
            "channels": channels,
        }
        if matches_calibration_seed(work, seeds):
            counters["calibration_works_excluded"] += 1
            continue
        counters["heldout_works_seen"] += 1
        yield work


def read_population_rows(
    conn: sqlite3.Connection, retrieval_config: dict[str, Any]
) -> tuple[list[dict[str, Any]], int]:
    """Small-fixture helper. Real sampling uses streaming_top_k_population."""
    counters: dict[str, int] = {}
    rows = list(iter_population_rows(conn, retrieval_config, counters))
    return rows, counters["calibration_works_excluded"]


def rank_population(rows: list[dict[str, Any]], work_seed: str) -> list[dict[str, Any]]:
    """Reference implementation for bounded synthetic fixtures."""
    ranked = [
        {
            **row,
            "rank_key": sha_rank(PROTOCOL_VERSION, work_seed, str(row["work_id"])),
        }
        for row in rows
    ]
    if len({str(row["work_id"]) for row in rows}) != len(rows):
        raise ValueError("duplicate canonical work identity")
    ranked.sort(key=lambda x: (x["rank_key"], x["work_id"]))
    return ranked


def streaming_top_k_population(
    conn: sqlite3.Connection,
    retrieval_config: dict[str, Any],
    work_seed: str,
    k: int,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Select the K smallest deterministic hash ranks in O(K) memory."""
    if k < 1:
        raise ValueError("streaming sample size must be positive")
    counters: dict[str, int] = {}

    def ranked_rows() -> Iterable[dict[str, Any]]:
        for row in iter_population_rows(conn, retrieval_config, counters):
            yield {
                **row,
                "rank_key": sha_rank(PROTOCOL_VERSION, work_seed, str(row["work_id"])),
            }

    selected = heapq.nsmallest(
        k,
        ranked_rows(),
        key=lambda x: (x["rank_key"], x["work_id"]),
    )
    if len(selected) < k:
        raise ValueError(
            f"sample exceeds held-out population: requested={k}, available={len(selected)}"
        )
    return selected, counters


def make_sample_manifest(
    *,
    ranked_rows: list[dict[str, Any]],
    population_digest: str,
    population_run_id: str,
    work_seed: str,
    primary_n: int,
    reserve_n: int,
) -> dict[str, Any]:
    if primary_n < 1 or reserve_n < 0:
        raise ValueError("invalid primary/reserve sample size")
    if primary_n + reserve_n > len(ranked_rows):
        raise ValueError("sample exceeds held-out population")
    selected = []
    for ordinal, row in enumerate(ranked_rows[: primary_n + reserve_n], start=1):
        channels = list(row["channels"])
        selected.append(
            {
                "canonical_work_id": row["work_id"],
                "sampling_rank": ordinal,
                "rank_key": row["rank_key"],
                "stratum": channel_class(channels),
                "retrieval_channel_membership": channels,
                "citation_band": citation_band(int(row["cited_by_count"])),
                "publication_year": row["publication_year"],
                "sample_role": "PRIMARY" if ordinal <= primary_n else "RESERVE",
            }
        )
    return {
        "schema_version": SAMPLE_MANIFEST_VERSION,
        "sample_protocol_version": PROTOCOL_VERSION,
        "eligibility_protocol_version": "paper2-eligibility-v1.1",
        "generation_timestamp": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "population_manifest_digest": population_digest,
        "population_manifest_run_id": population_run_id,
        "sample_seed": work_seed,
        "stratum_definition": {
            "primary": "unstratified deterministic hash-rank probability draw over held-out work identities",
            "diagnostic": "exact R1/R2/R3 membership, citation band, publication year; diagnostic-only fills are never pooled into primary",
        },
        "allocation_rule": (
            f"lowest {primary_n} eligible hash ranks -> PRIMARY; "
            f"next {reserve_n} -> ordered RESERVE"
        ),
        "selected_works": selected,
    }


def select_claims(
    candidates: list[dict[str, str]], claim_seed: str, cap: int = 3
) -> list[dict[str, str]]:
    if cap < 1:
        raise ValueError("claim cap must be positive")
    required = {"work_id", "source_locator", "source_span_digest"}
    identities: set[tuple[str, str, str]] = set()
    ranked = []
    for candidate in candidates:
        if not required <= set(candidate):
            raise ValueError("claim candidate lacks stable source-grounded identity")
        identity = tuple(candidate[k] for k in ("work_id", "source_locator", "source_span_digest"))
        if identity in identities:
            raise ValueError("duplicate claim candidate identity")
        identities.add(identity)
        ranked.append(
            {
                **candidate,
                "_rank_key": sha_rank(
                    "paper2-claim-sampling-v1",
                    claim_seed,
                    candidate["work_id"],
                    candidate["source_locator"],
                    candidate["source_span_digest"],
                ),
            }
        )
    ranked.sort(key=lambda x: (x["_rank_key"], x["work_id"], x["source_locator"], x["source_span_digest"]))
    result = []
    for row in ranked[:cap]:
        row = dict(row)
        row.pop("_rank_key")
        result.append(row)
    return result


def null_target_permutation(row_ids: list[str], null_seed: str, index: int) -> dict[str, str]:
    if index < 0:
        raise ValueError("permutation index must be nonnegative")
    if len(row_ids) < 2:
        raise ValueError("target permutation requires at least two rows")
    if len(set(row_ids)) != len(row_ids):
        raise ValueError("row IDs must be unique")
    ordered = sorted(
        row_ids,
        key=lambda rid: (sha_rank("paper2-null-v1", null_seed, str(index), rid), rid),
    )
    return {rid: ordered[(i + 1) % len(ordered)] for i, rid in enumerate(ordered)}


def nominal_n_for_half_width(half_width: float, z: float = 1.96) -> int:
    if not 0 < half_width < 1:
        raise ValueError("half width must be in (0,1)")
    return math.ceil((z * z * 0.25) / (half_width * half_width))


def independent_two_prop_reference_n(delta: float, z_alpha: float = 1.96, z_power: float = 0.84) -> int:
    if not 0 < delta < 1:
        raise ValueError("delta must be in (0,1)")
    return math.ceil(2.0 * ((z_alpha + z_power) ** 2) * 0.25 / (delta * delta))


def precision_plan(protocol: dict[str, Any]) -> dict[str, Any]:
    precision = protocol["precision"]
    deffs = [float(x) for x in precision["design_effect_sensitivity"]]
    rows = []
    for half_width in precision["target_half_widths"]:
        base = nominal_n_for_half_width(float(half_width))
        rows.append(
            {
                "half_width": float(half_width),
                "nominal_independent_n": base,
                "design_effect_sensitivity": [
                    {"DEFF": deff, "required_analyzable_n": math.ceil(base * deff)}
                    for deff in deffs
                ],
            }
        )
    null_rows = [
        {
            "D": d,
            "independent_two_proportion_reference_n_per_condition": independent_two_prop_reference_n(d),
        }
        for d in (0.05, 0.10, 0.20)
    ]
    attrition = [
        {
            "retained_fraction": r,
            "gross_draw_multiplier": 1.0 / r,
            "note": "operational sensitivity only; not an observed retention rate",
        }
        for r in (1.0, 0.8, 0.5, 0.25)
    ]
    return {
        "schema_version": "paper2-sampling-precision-plan-v1",
        "coverage_precision": rows,
        "null_discrimination_reference": null_rows,
        "attrition_sensitivity": attrition,
        "warning": "reference calculations do not assert IID literature claims or an empirical design effect",
    }


def require_real_sampling_authority(protocol: dict[str, Any]) -> tuple[int, int]:
    freeze = protocol["freeze_state"]
    if freeze.get("real_sampling_authorized") is not True:
        raise RuntimeError("REAL_SAMPLING_BLOCKED: protocol has not authorized a real draw")
    primary_n = freeze.get("final_work_draw_n")
    reserve_n = freeze.get("final_reserve_work_n")
    stopping = freeze.get("stopping_rule")
    if not isinstance(primary_n, int) or primary_n < 1:
        raise RuntimeError("REAL_SAMPLING_BLOCKED: final_work_draw_n is not frozen")
    if not isinstance(reserve_n, int) or reserve_n < 0:
        raise RuntimeError("REAL_SAMPLING_BLOCKED: final_reserve_work_n is not frozen")
    if not isinstance(stopping, str) or stopping == "NOT_YET_FROZEN":
        raise RuntimeError("REAL_SAMPLING_BLOCKED: stopping rule is not frozen")
    return primary_n, reserve_n



def hash_uniform_index(
    size: int,
    seed: str,
    replicate: int,
    draw_position: int,
) -> int:
    """Deterministically map SHA-256 output to an unbiased index by rejection."""
    if size < 1:
        raise ValueError("bootstrap cluster count must be positive")
    if replicate < 0 or draw_position < 0:
        raise ValueError("bootstrap coordinates must be nonnegative")
    space = 1 << 256
    limit = space - (space % size)
    counter = 0
    while True:
        value = int(
            sha_rank(
                "paper2-paper-cluster-bootstrap-v1",
                seed,
                str(replicate),
                str(draw_position),
                str(counter),
            ),
            16,
        )
        if value < limit:
            return value % size
        counter += 1


def paper_cluster_bootstrap_indices(
    n_clusters: int,
    replicate: int,
    seed: str,
) -> list[int]:
    if n_clusters < 2:
        raise ValueError("paper-cluster bootstrap requires at least two clusters")
    return [
        hash_uniform_index(n_clusters, seed, replicate, draw_position)
        for draw_position in range(n_clusters)
    ]


def type7_quantile(values: list[float], q: float) -> float:
    """R/NumPy-style Type-7 linear quantile, implemented with stdlib only."""
    if not values:
        raise ValueError("quantile requires at least one value")
    if not 0.0 <= q <= 1.0:
        raise ValueError("quantile probability must be in [0,1]")
    ordered = sorted(float(x) for x in values)
    if len(ordered) == 1:
        return ordered[0]
    h = (len(ordered) - 1) * q
    lo = math.floor(h)
    hi = math.ceil(h)
    if lo == hi:
        return ordered[lo]
    weight = h - lo
    return ordered[lo] * (1.0 - weight) + ordered[hi] * weight


def synthetic_retrieval_config() -> dict[str, Any]:
    seeds = [
        {"number": i, "title": f"Calibration {i}", "year": 2000 + i, "doi": None, "arxiv": None, "isbn": None}
        for i in range(1, 51)
    ]
    seeds[0]["title"] = "Calibration Match"
    seeds[0]["year"] = 2001
    seeds[0]["doi"] = "10.1/calibration"
    return {
        "schema_version": "paper2-retrieval-v1",
        "provider": "OpenAlex",
        "citation_floor": 1,
        "seeds": seeds,
        "text_queries": [],
        "anchor_queries": [],
    }


def make_synthetic_manifest(path: Path, row_order: list[int]) -> None:
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        CREATE TABLE works(
          work_id TEXT PRIMARY KEY,
          provider_work_id TEXT,
          title TEXT NOT NULL,
          publication_year INTEGER,
          doi TEXT,
          arxiv TEXT,
          stable_ids_json TEXT NOT NULL,
          cited_by_count INTEGER NOT NULL,
          first_author TEXT,
          first_seen_at TEXT NOT NULL,
          last_seen_at TEXT NOT NULL
        );
        CREATE TABLE retrieval_channels(
          work_id TEXT NOT NULL,
          channel TEXT NOT NULL,
          PRIMARY KEY(work_id,channel)
        );
        CREATE TABLE run_metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);
        """
    )
    meta = {
        "manifest_schema_version": "paper2-retrieval-v1-manifest-transaction-v1",
        "run_status": "COMPLETE",
        "artifact_role": EXPECTED_MANIFEST_ROLE,
        "logical_manifest_digest": "a" * 64,
        "run_id": "synthetic-run",
    }
    conn.executemany(
        "INSERT INTO run_metadata VALUES(?,?)",
        [(k, json.dumps(v)) for k, v in meta.items()],
    )
    works = [
        ("W1", "Work 1", 2020, "10.1/1", 1, ("R1",)),
        ("W2", "Work 2", 2019, "10.1/2", 10, ("R2",)),
        ("W3", "Work 3", 2018, "10.1/3", 100, ("R3",)),
        ("W4", "Work 4", 2017, "10.1/4", 1000, ("R1", "R2")),
        ("W5", "Work 5", 2016, "10.1/5", 10000, ("R1", "R3")),
        ("W6", "Work 6", 2015, "10.1/6", 42, ("R2", "R3")),
        ("W7", "Work 7", 2014, "10.1/7", 420, ("R1", "R2", "R3")),
        ("W8", "Work 8", 2013, "10.1/8", 7, ("R1",)),
        ("WCAL", "Calibration Match", 2001, "10.1/calibration", 99999, ("R1", "R2")),
    ]
    now = "2000-01-01T00:00:00+00:00"
    for idx in row_order:
        wid, title, year, doi, cited, channels = works[idx]
        conn.execute(
            "INSERT INTO works VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (wid, wid, title, year, doi, None, "{}", cited, "Synthetic Author", now, now),
        )
        for ch in channels:
            conn.execute("INSERT INTO retrieval_channels VALUES(?,?)", (wid, ch))
    conn.commit()
    conn.close()


def self_test(protocol: dict[str, Any]) -> None:
    assert protocol["freeze_state"]["real_sampling_authorized"] is False
    assert protocol["statistical_units"]["iid_claim_interpretation_forbidden"] is True
    assert protocol["denominator_contract"]["pipeline_failure_as_residual_forbidden"] is True
    assert protocol["uncertainty"]["paper_cluster_bootstrap"]["replicates"] == 2000
    assert protocol["expansion_policy"]["result_dependent_sample_expansion_forbidden"] is True
    try:
        require_real_sampling_authority(protocol)
        raise AssertionError("real sampling authority gate failed open")
    except RuntimeError as exc:
        assert "REAL_SAMPLING_BLOCKED" in str(exc)

    with tempfile.TemporaryDirectory(prefix="paper2-sampling-selftest-") as tmp:
        root = Path(tmp)
        db_a = root / "a.sqlite3"
        db_b = root / "b.sqlite3"
        make_synthetic_manifest(db_a, list(range(9)))
        make_synthetic_manifest(db_b, list(reversed(range(9))))
        config = synthetic_retrieval_config()

        results = []
        for db in (db_a, db_b):
            conn = sqlite3.connect(db)
            authority = validate_population_manifest(conn)
            ranked, counters = streaming_top_k_population(
                conn,
                config,
                protocol["randomization"]["work_seed"],
                8,
            )
            conn.close()
            assert counters["calibration_works_excluded"] == 1
            assert counters["manifest_rows_seen"] == 9
            assert counters["heldout_works_seen"] == 8
            assert len(ranked) == 8
            assert len({x["work_id"] for x in ranked}) == 8
            results.append((authority, ranked, counters))

        assert [x["work_id"] for x in results[0][1]] == [x["work_id"] for x in results[1][1]]
        assert [x["rank_key"] for x in results[0][1]] == [x["rank_key"] for x in results[1][1]]

        fixture_protocol = json.loads(json.dumps(protocol))
        fixture_protocol["freeze_state"].update(
            {
                "real_sampling_authorized": True,
                "final_work_draw_n": 4,
                "final_reserve_work_n": 2,
                "stopping_rule": "fixed drawn work N in synthetic fixture",
            }
        )
        primary_n, reserve_n = require_real_sampling_authority(fixture_protocol)
        manifest = make_sample_manifest(
            ranked_rows=results[0][1],
            population_digest=results[0][0]["digest"],
            population_run_id=results[0][0]["run_id"],
            work_seed=protocol["randomization"]["work_seed"],
            primary_n=primary_n,
            reserve_n=reserve_n,
        )
        assert len(manifest["selected_works"]) == 6
        assert [x["sample_role"] for x in manifest["selected_works"]] == [
            "PRIMARY", "PRIMARY", "PRIMARY", "PRIMARY", "RESERVE", "RESERVE"
        ]
        assert all(x["canonical_work_id"] != "WCAL" for x in manifest["selected_works"])
        assert len({x["canonical_work_id"] for x in manifest["selected_works"]}) == 6
        assert {
            channel_class(["R1"]), channel_class(["R2"]), channel_class(["R3"]),
            channel_class(["R1","R2"]), channel_class(["R1","R3"]),
            channel_class(["R2","R3"]), channel_class(["R1","R2","R3"])
        } == {"R1","R2","R3","R1R2","R1R3","R2R3","R1R2R3"}

        claims = [
            {"work_id": "W1", "source_locator": f"p{i}", "source_span_digest": f"{i:064x}"}
            for i in range(6)
        ]
        a = select_claims(claims, protocol["randomization"]["claim_seed"], cap=3)
        b = select_claims(list(reversed(claims)), protocol["randomization"]["claim_seed"], cap=3)
        assert a == b
        assert len(a) == 3

        row_ids = [f"claim-{i}" for i in range(11)]
        for j in range(protocol["null_schedule"]["permutations"]):
            mapping = null_target_permutation(row_ids, protocol["randomization"]["null_seed"], j)
            assert set(mapping) == set(row_ids)
            assert set(mapping.values()) == set(row_ids)
            assert all(k != v for k, v in mapping.items())

    bootstrap_seed = protocol["uncertainty"]["paper_cluster_bootstrap"]["seed"]
    b0 = paper_cluster_bootstrap_indices(7, 0, bootstrap_seed)
    b0_again = paper_cluster_bootstrap_indices(7, 0, bootstrap_seed)
    b1 = paper_cluster_bootstrap_indices(7, 1, bootstrap_seed)
    assert b0 == b0_again
    assert len(b0) == 7 and all(0 <= x < 7 for x in b0)
    assert len(b1) == 7 and all(0 <= x < 7 for x in b1)
    assert type7_quantile([0.0, 1.0], 0.5) == 0.5
    assert type7_quantile([0.0, 1.0, 2.0, 3.0], 0.25) == 0.75

    plan = precision_plan(protocol)
    by_h = {row["half_width"]: row["nominal_independent_n"] for row in plan["coverage_precision"]}
    assert by_h == {0.05: 385, 0.03: 1068, 0.02: 2401, 0.01: 9604}
    null_ref = {
        row["D"]: row["independent_two_proportion_reference_n_per_condition"]
        for row in plan["null_discrimination_reference"]
    }
    assert null_ref == {0.05: 1568, 0.1: 392, 0.2: 98}
    print("PAPER2_SAMPLING_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--protocol",
        type=Path,
        default=Path("research/paper2/sampling_v1.json"),
    )
    parser.add_argument(
        "--retrieval-config",
        type=Path,
        default=Path("research/paper2/retrieval_v1.json"),
    )
    parser.add_argument("--manifest-db", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    protocol = load_protocol(args.protocol)

    if args.self_test:
        self_test(protocol)
        return 0

    if args.plan:
        print(json.dumps(precision_plan(protocol), indent=2, sort_keys=True))
        return 0

    if args.manifest_db:
        primary_n, reserve_n = require_real_sampling_authority(protocol)
        retrieval_config = load_json(args.retrieval_config)
        conn = sqlite3.connect(args.manifest_db)
        authority = validate_population_manifest(conn)
        ranked, counters = streaming_top_k_population(
            conn,
            retrieval_config,
            protocol["randomization"]["work_seed"],
            primary_n + reserve_n,
        )
        conn.close()
        result = make_sample_manifest(
            ranked_rows=ranked,
            population_digest=authority["digest"],
            population_run_id=authority["run_id"],
            work_seed=protocol["randomization"]["work_seed"],
            primary_n=primary_n,
            reserve_n=reserve_n,
        )
        result["calibration_works_excluded"] = counters["calibration_works_excluded"]
        result["population_heldout_work_count"] = counters["heldout_works_seen"]
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
        return 0

    parser.error("choose --self-test, --plan, or --manifest-db")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
