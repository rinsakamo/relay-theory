#!/usr/bin/env python3
"""Durable materializer for the frozen Paper 2 OpenAlex retrieval frame v1.

Owner: #143
Authority: #133

Bibliographic candidate-manifest infrastructure only. This does not perform
eligibility classification, ClaimIR extraction, decomposition, or scientific
source-text adjudication.

The frozen seed-topic snapshot comes from the authoritative counts artifact.
Each provider page and its checkpoint commit atomically, so replay after
interruption is idempotent and provenance-preserving.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable

import paper2_openalex_enumerate as retrieval

SCHEMA_VERSION = "paper2-retrieval-v1-manifest-transaction-v1"
PER_PAGE = 200
RESUMABLE_STATUSES = {"RUNNING", "FAILED", "INTERRUPTED", "INCOMPLETE"}
CHANNELS = ("R1", "R2", "R3")


def utc_now() -> str:
    return retrieval.utc_now()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json_digest(value: Any) -> str:
    return sha256_bytes(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    )


def normalize_doi(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return re.sub(
        r"^https?://(?:dx\.)?doi\.org/", "", value.strip(), flags=re.I
    ).casefold()


def stable_ids(work: dict[str, Any]) -> dict[str, str]:
    raw = work.get("ids") or {}
    result: dict[str, str] = {}
    if isinstance(raw, dict):
        for key, value in raw.items():
            if isinstance(key, str) and isinstance(value, str) and value.strip():
                result[key] = value.strip()
    doi = normalize_doi(work.get("doi"))
    if doi and "doi" not in {k.casefold() for k in result}:
        result["doi"] = f"https://doi.org/{doi}"
    return dict(sorted(result.items()))


def extract_arxiv(work: dict[str, Any], ids: dict[str, str]) -> str | None:
    for key, value in ids.items():
        if "arxiv" in key.casefold():
            return re.sub(
                r"^https?://arxiv\.org/(?:abs|pdf)/", "", value
            ).removesuffix(".pdf")
    location = work.get("primary_location") or {}
    url = location.get("landing_page_url")
    if isinstance(url, str):
        match = re.search(r"arxiv\.org/(?:abs|pdf)/([^?#]+)", url, flags=re.I)
        if match:
            return match.group(1).removesuffix(".pdf")
    return None


def first_author_name(work: dict[str, Any]) -> str | None:
    authorships = work.get("authorships") or []
    if not isinstance(authorships, list) or not authorships:
        return None
    author = (authorships[0] or {}).get("author") or {}
    name = author.get("display_name")
    return name.strip() if isinstance(name, str) and name.strip() else None


def isbn_identity(ids: dict[str, str]) -> str | None:
    for key, value in ids.items():
        if "isbn" in key.casefold() and value.strip():
            return re.sub(r"[^0-9Xx]", "", value).upper()
    return None


def canonical_work_identity(work: dict[str, Any]) -> tuple[str, str | None]:
    provider_id = work.get("id")
    if isinstance(provider_id, str) and provider_id.strip():
        short = retrieval.short_openalex_id(provider_id)
        if short:
            return short, short

    doi = normalize_doi(work.get("doi"))
    if doi:
        return f"doi:{doi}", None

    ids = stable_ids(work)
    arxiv = extract_arxiv(work, ids)
    if arxiv:
        return f"arxiv:{arxiv.casefold()}", None

    isbn = isbn_identity(ids)
    if isbn:
        return f"isbn:{isbn}", None

    title = retrieval.normalize_title(str(work.get("display_name") or ""))
    year = work.get("publication_year")
    author = retrieval.normalize_title(first_author_name(work) or "")
    if title and year is not None and author:
        key = sha256_bytes(f"{title}\n{int(year)}\n{author}".encode("utf-8"))
        return f"title-year-author:{key}", None

    raise ValueError(
        "work lacks OpenAlex ID and all frozen fallback identity coordinates"
    )


def prepare_work_row(
    work: dict[str, Any], citation_floor: int, seen_at: str
) -> tuple[Any, ...]:
    work_id, provider_work_id = canonical_work_identity(work)
    cited = int(work.get("cited_by_count") or 0)
    if cited < citation_floor:
        raise ValueError(
            f"provider returned work below frozen citation floor: {work_id}={cited}"
        )
    ids = stable_ids(work)
    return (
        work_id,
        provider_work_id,
        str(work.get("display_name") or ""),
        work.get("publication_year"),
        normalize_doi(work.get("doi")),
        extract_arxiv(work, ids),
        json.dumps(ids, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        cited,
        first_author_name(work),
        seen_at,
        seen_at,
    )


def init_db(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;
        PRAGMA synchronous=FULL;

        CREATE TABLE IF NOT EXISTS works (
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

        CREATE UNIQUE INDEX IF NOT EXISTS idx_works_provider_work_id
          ON works(provider_work_id)
          WHERE provider_work_id IS NOT NULL;

        CREATE TABLE IF NOT EXISTS retrieval_channels (
          work_id TEXT NOT NULL REFERENCES works(work_id) ON DELETE CASCADE,
          channel TEXT NOT NULL CHECK(channel IN ('R1','R2','R3')),
          PRIMARY KEY(work_id, channel)
        );

        CREATE TABLE IF NOT EXISTS work_r1_topics (
          work_id TEXT NOT NULL REFERENCES works(work_id) ON DELETE CASCADE,
          topic_id TEXT NOT NULL,
          PRIMARY KEY(work_id, topic_id)
        );

        CREATE TABLE IF NOT EXISTS work_r2_queries (
          work_id TEXT NOT NULL REFERENCES works(work_id) ON DELETE CASCADE,
          query_id TEXT NOT NULL,
          query_text TEXT NOT NULL,
          PRIMARY KEY(work_id, query_id)
        );

        CREATE TABLE IF NOT EXISTS work_r3_anchors (
          work_id TEXT NOT NULL REFERENCES works(work_id) ON DELETE CASCADE,
          anchor_id TEXT NOT NULL,
          anchor_text TEXT NOT NULL,
          PRIMARY KEY(work_id, anchor_id)
        );

        CREATE TABLE IF NOT EXISTS run_metadata (
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS checkpoints (
          channel TEXT NOT NULL CHECK(channel IN ('R1','R2','R3')),
          source_index INTEGER NOT NULL CHECK(source_index >= 0),
          source_key TEXT NOT NULL,
          query_digest TEXT NOT NULL,
          next_cursor TEXT,
          pages_committed INTEGER NOT NULL CHECK(pages_committed >= 0),
          records_seen INTEGER NOT NULL CHECK(records_seen >= 0),
          last_request_cursor TEXT,
          last_page_rows INTEGER,
          status TEXT NOT NULL CHECK(status IN ('RUNNING','COMPLETE')),
          updated_at TEXT NOT NULL,
          PRIMARY KEY(channel, source_index)
        );
        """
    )
    return conn


def set_meta(conn: sqlite3.Connection, key: str, value: Any) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO run_metadata(key,value) VALUES(?,?)",
        (
            key,
            json.dumps(
                value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ),
        ),
    )


def get_meta(conn: sqlite3.Connection, key: str, default: Any = None) -> Any:
    row = conn.execute(
        "SELECT value FROM run_metadata WHERE key=?", (key,)
    ).fetchone()
    return default if row is None else json.loads(row[0])


def validate_counts_artifact(
    counts: dict[str, Any], config: dict[str, Any]
) -> list[str]:
    if counts.get("schema_version") != config["schema_version"]:
        raise ValueError("counts artifact schema_version mismatch")
    if counts.get("provider") != "OpenAlex":
        raise ValueError("counts artifact provider must be OpenAlex")
    if int(counts.get("citation_floor", -1)) != int(config["citation_floor"]):
        raise ValueError("counts artifact citation floor mismatch")

    topics = sorted(set(counts.get("seed_topics_v1") or []))
    if not topics:
        raise ValueError("counts artifact has no frozen seed_topics_v1")

    raw = counts.get("raw_counts") or {}
    if set((raw.get("R2") or {}).keys()) != set(config["text_queries"]):
        raise ValueError("counts artifact R2 keys do not match frozen config")
    if set((raw.get("R3") or {}).keys()) != set(config["anchor_queries"]):
        raise ValueError("counts artifact R3 keys do not match frozen config")

    expected_union = retrieval.union_query(
        topics,
        config["text_queries"],
        config["anchor_queries"],
        int(config["citation_floor"]),
    )
    if counts.get("union_oql") != expected_union:
        raise ValueError("counts artifact union_oql mismatch")
    if int(counts.get("N_frame", -1)) < 0:
        raise ValueError("counts artifact N_frame is missing or invalid")
    return topics


def source_specs(
    config: dict[str, Any], seed_topics: list[str]
) -> list[dict[str, Any]]:
    floor = int(config["citation_floor"])
    tc = retrieval.topic_clause(seed_topics)
    if not tc:
        raise ValueError("frozen seed-topic set is empty")
    specs: list[dict[str, Any]] = [
        {
            "channel": "R1",
            "source_index": 0,
            "source_key": "seed_topics_v1",
            "query": retrieval.base_count_query(tc, floor),
        }
    ]
    for i, text in enumerate(config["text_queries"]):
        specs.append(
            {
                "channel": "R2",
                "source_index": i,
                "source_key": text,
                "query": retrieval.base_count_query(
                    retrieval.text_clause(text), floor
                ),
            }
        )
    for i, text in enumerate(config["anchor_queries"]):
        specs.append(
            {
                "channel": "R3",
                "source_index": i,
                "source_key": text,
                "query": retrieval.base_count_query(
                    retrieval.text_clause(text, exact=True), floor
                ),
            }
        )
    for spec in specs:
        spec["query_digest"] = sha256_bytes(spec["query"].encode("utf-8"))
    return specs


def validate_source_spec(
    spec: dict[str, Any], config: dict[str, Any], seed_topics: list[str]
) -> None:
    expected = {
        (s["channel"], s["source_index"]): s
        for s in source_specs(config, seed_topics)
    }
    key = (spec.get("channel"), spec.get("source_index"))
    if key not in expected:
        raise ValueError(f"unknown retrieval source {key}")
    canonical = expected[key]
    for field in ("source_key", "query_digest"):
        if spec.get(field) != canonical[field]:
            raise ValueError(f"malformed retrieval provenance for {key}: {field}")


def ensure_checkpoint(conn: sqlite3.Connection, spec: dict[str, Any]) -> None:
    row = conn.execute(
        "SELECT source_key,query_digest,next_cursor,pages_committed,"
        "records_seen,status FROM checkpoints WHERE channel=? AND source_index=?",
        (spec["channel"], spec["source_index"]),
    ).fetchone()
    if row is None:
        with conn:
            conn.execute(
                """
                INSERT INTO checkpoints(
                  channel,source_index,source_key,query_digest,next_cursor,
                  pages_committed,records_seen,last_request_cursor,last_page_rows,
                  status,updated_at
                ) VALUES(?,?,?,?,?,0,0,NULL,NULL,'RUNNING',?)
                """,
                (
                    spec["channel"],
                    spec["source_index"],
                    spec["source_key"],
                    spec["query_digest"],
                    "*",
                    utc_now(),
                ),
            )
        return

    source_key, query_digest, next_cursor, pages, records, status = row
    if source_key != spec["source_key"] or query_digest != spec["query_digest"]:
        raise ValueError("checkpoint provenance mismatch")
    if pages < 0 or records < 0:
        raise ValueError("checkpoint contains negative counters")
    if status == "RUNNING" and next_cursor in (None, ""):
        raise ValueError("corrupt checkpoint: RUNNING source has no next cursor")
    if status == "COMPLETE" and next_cursor not in (None, ""):
        raise ValueError("corrupt checkpoint: COMPLETE source retains next cursor")


def load_checkpoint(
    conn: sqlite3.Connection, spec: dict[str, Any]
) -> dict[str, Any]:
    ensure_checkpoint(conn, spec)
    row = conn.execute(
        """
        SELECT next_cursor,pages_committed,records_seen,status
        FROM checkpoints WHERE channel=? AND source_index=?
        """,
        (spec["channel"], spec["source_index"]),
    ).fetchone()
    assert row is not None
    return {
        "next_cursor": row[0],
        "pages_committed": int(row[1]),
        "records_seen": int(row[2]),
        "status": row[3],
    }


def page_select() -> str:
    return (
        "id,ids,doi,display_name,publication_year,cited_by_count,"
        "topics,authorships,primary_location"
    )


def fetch_page(
    client: retrieval.OpenAlexClient, query: str, cursor: str
) -> dict[str, Any]:
    payload = client.run_oql(
        query, per_page=PER_PAGE, cursor=cursor, select=page_select()
    )
    results = payload.get("results")
    meta = payload.get("meta")
    if not isinstance(results, list) or not isinstance(meta, dict):
        raise RuntimeError("provider page missing results/meta")
    next_cursor = meta.get("next_cursor")
    if next_cursor == cursor and results:
        raise RuntimeError("provider returned a repeated cursor")
    return {"results": results, "next_cursor": next_cursor}


def ingest_page(
    conn: sqlite3.Connection,
    *,
    spec: dict[str, Any],
    config: dict[str, Any],
    seed_topics: list[str],
    request_cursor: str,
    results: list[dict[str, Any]],
    next_cursor: str | None,
    fault_after_works: bool = False,
) -> None:
    validate_source_spec(spec, config, seed_topics)
    seen_at = utc_now()
    work_rows: dict[str, tuple[Any, ...]] = {}
    channel_rows: set[tuple[str, str]] = set()
    r1_rows: set[tuple[str, str]] = set()
    r2_rows: set[tuple[str, str, str]] = set()
    r3_rows: set[tuple[str, str, str]] = set()
    topic_set = set(seed_topics)

    for work in results:
        row = prepare_work_row(work, int(config["citation_floor"]), seen_at)
        work_id = str(row[0])
        work_rows[work_id] = row
        channel = spec["channel"]
        channel_rows.add((work_id, channel))
        if channel == "R1":
            matched = sorted(
                topic_set
                & {
                    retrieval.short_openalex_id(topic["id"])
                    for topic in (work.get("topics") or [])
                    if isinstance(topic, dict) and topic.get("id")
                }
            )
            if not matched:
                raise ValueError(
                    f"R1 provider hit has no matching frozen seed topic: {work_id}"
                )
            r1_rows.update((work_id, topic_id) for topic_id in matched)
        elif channel == "R2":
            qid = f"R2-{int(spec['source_index']) + 1:03d}"
            r2_rows.add((work_id, qid, spec["source_key"]))
        elif channel == "R3":
            aid = f"R3-{int(spec['source_index']) + 1:03d}"
            r3_rows.add((work_id, aid, spec["source_key"]))
        else:
            raise ValueError(f"unknown retrieval channel {channel}")

    status = "COMPLETE" if not next_cursor else "RUNNING"
    stored_next = None if status == "COMPLETE" else next_cursor

    with conn:
        conn.executemany(
            """
            INSERT INTO works(
              work_id,provider_work_id,title,publication_year,doi,arxiv,
              stable_ids_json,cited_by_count,first_author,first_seen_at,last_seen_at
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(work_id) DO UPDATE SET
              provider_work_id=COALESCE(excluded.provider_work_id,works.provider_work_id),
              title=excluded.title,
              publication_year=excluded.publication_year,
              doi=excluded.doi,
              arxiv=excluded.arxiv,
              stable_ids_json=excluded.stable_ids_json,
              cited_by_count=excluded.cited_by_count,
              first_author=excluded.first_author,
              last_seen_at=excluded.last_seen_at
            """,
            work_rows.values(),
        )
        if fault_after_works:
            raise RuntimeError("synthetic page failure after works")
        conn.executemany(
            "INSERT OR IGNORE INTO retrieval_channels(work_id,channel) VALUES(?,?)",
            channel_rows,
        )
        conn.executemany(
            "INSERT OR IGNORE INTO work_r1_topics(work_id,topic_id) VALUES(?,?)",
            r1_rows,
        )
        conn.executemany(
            """
            INSERT OR IGNORE INTO work_r2_queries(work_id,query_id,query_text)
            VALUES(?,?,?)
            """,
            r2_rows,
        )
        conn.executemany(
            """
            INSERT OR IGNORE INTO work_r3_anchors(work_id,anchor_id,anchor_text)
            VALUES(?,?,?)
            """,
            r3_rows,
        )
        conn.execute(
            """
            UPDATE checkpoints
            SET next_cursor=?,
                pages_committed=pages_committed+1,
                records_seen=records_seen+?,
                last_request_cursor=?,
                last_page_rows=?,
                status=?,
                updated_at=?
            WHERE channel=? AND source_index=?
              AND source_key=? AND query_digest=?
            """,
            (
                stored_next,
                len(results),
                request_cursor,
                len(results),
                status,
                utc_now(),
                spec["channel"],
                spec["source_index"],
                spec["source_key"],
                spec["query_digest"],
            ),
        )
        if conn.execute("SELECT changes()").fetchone()[0] != 1:
            raise RuntimeError("checkpoint update did not affect exactly one row")


def logical_manifest_digest(conn: sqlite3.Connection) -> str:
    h = hashlib.sha256()
    table_queries = [
        (
            "works",
            """
            SELECT work_id,provider_work_id,title,publication_year,doi,arxiv,
                   stable_ids_json,cited_by_count,first_author
            FROM works ORDER BY work_id
            """,
        ),
        (
            "retrieval_channels",
            "SELECT work_id,channel FROM retrieval_channels ORDER BY work_id,channel",
        ),
        (
            "work_r1_topics",
            "SELECT work_id,topic_id FROM work_r1_topics ORDER BY work_id,topic_id",
        ),
        (
            "work_r2_queries",
            """
            SELECT work_id,query_id,query_text FROM work_r2_queries
            ORDER BY work_id,query_id
            """,
        ),
        (
            "work_r3_anchors",
            """
            SELECT work_id,anchor_id,anchor_text FROM work_r3_anchors
            ORDER BY work_id,anchor_id
            """,
        ),
    ]
    for table, query in table_queries:
        h.update((table + "\n").encode("utf-8"))
        for row in conn.execute(query):
            h.update(
                (
                    json.dumps(
                        list(row), ensure_ascii=False, separators=(",", ":")
                    )
                    + "\n"
                ).encode("utf-8")
            )
    return h.hexdigest()


def integrity_qc(conn: sqlite3.Connection) -> dict[str, Any]:
    integrity_rows = [row[0] for row in conn.execute("PRAGMA integrity_check")]
    fk_rows = list(conn.execute("PRAGMA foreign_key_check"))

    work_stats = conn.execute(
        """
        SELECT
          COUNT(*),
          SUM(CASE WHEN doi IS NOT NULL THEN 1 ELSE 0 END),
          SUM(CASE WHEN arxiv IS NOT NULL THEN 1 ELSE 0 END),
          SUM(CASE WHEN publication_year IS NULL THEN 1 ELSE 0 END),
          SUM(CASE WHEN title IS NULL OR trim(title)='' THEN 1 ELSE 0 END)
        FROM works
        """
    ).fetchone()
    assert work_stats is not None

    channel_stats = conn.execute(
        """
        WITH per_work AS (
          SELECT
            work_id,
            MAX(CASE WHEN channel='R1' THEN 1 ELSE 0 END) AS r1,
            MAX(CASE WHEN channel='R2' THEN 1 ELSE 0 END) AS r2,
            MAX(CASE WHEN channel='R3' THEN 1 ELSE 0 END) AS r3
          FROM retrieval_channels
          GROUP BY work_id
        )
        SELECT
          COALESCE(SUM(r1),0),
          COALESCE(SUM(r2),0),
          COALESCE(SUM(r3),0),
          COALESCE(SUM(CASE WHEN r1=1 AND r2=1 THEN 1 ELSE 0 END),0),
          COALESCE(SUM(CASE WHEN r1=1 AND r3=1 THEN 1 ELSE 0 END),0),
          COALESCE(SUM(CASE WHEN r2=1 AND r3=1 THEN 1 ELSE 0 END),0),
          COALESCE(SUM(CASE WHEN r1=1 AND r2=1 AND r3=1 THEN 1 ELSE 0 END),0)
        FROM per_work
        """
    ).fetchone()
    assert channel_stats is not None

    checkpoint_rows = list(
        conn.execute(
            "SELECT channel,source_index,status,next_cursor FROM checkpoints "
            "ORDER BY channel,source_index"
        )
    )
    return {
        "N_unique_works": int(work_stats[0]),
        "N_R1_members": int(channel_stats[0]),
        "N_R2_members": int(channel_stats[1]),
        "N_R3_members": int(channel_stats[2]),
        "N_channel_overlap": {
            "R1_R2": int(channel_stats[3]),
            "R1_R3": int(channel_stats[4]),
            "R2_R3": int(channel_stats[5]),
            "R1_R2_R3": int(channel_stats[6]),
        },
        "provenance_edges": {
            "R1_topic_attributions": int(
                conn.execute("SELECT COUNT(*) FROM work_r1_topics").fetchone()[0]
            ),
            "R2_query_attributions": int(
                conn.execute("SELECT COUNT(*) FROM work_r2_queries").fetchone()[0]
            ),
            "R3_anchor_attributions": int(
                conn.execute("SELECT COUNT(*) FROM work_r3_anchors").fetchone()[0]
            ),
        },
        "identifier_completeness": {
            "DOI_count": int(work_stats[1] or 0),
            "arXiv_count": int(work_stats[2] or 0),
            "year_missing": int(work_stats[3] or 0),
            "title_missing": int(work_stats[4] or 0),
        },
        "duplicate_constraint_violations": {
            "works": 0,
            "retrieval_channels": 0,
            "r1_topics": 0,
            "r2_queries": 0,
            "r3_anchors": 0,
            "enforcement": "PRIMARY KEY / UNIQUE constraints + PRAGMA integrity_check",
        },
        "sqlite_integrity_check": integrity_rows,
        "foreign_key_violations": len(fk_rows),
        "checkpoints": [
            {
                "channel": row[0],
                "source_index": row[1],
                "status": row[2],
                "next_cursor_present": row[3] not in (None, ""),
            }
            for row in checkpoint_rows
        ],
    }


def validate_integrity_for_completion(qc: dict[str, Any]) -> None:
    if qc["sqlite_integrity_check"] != ["ok"]:
        raise RuntimeError(f"SQLite integrity_check failed: {qc['sqlite_integrity_check']}")
    if qc["foreign_key_violations"] != 0:
        raise RuntimeError("SQLite foreign_key_check failed")
    duplicate_counts = {
        key: value
        for key, value in qc["duplicate_constraint_violations"].items()
        if key != "enforcement"
    }
    if any(duplicate_counts.values()):
        raise RuntimeError("duplicate constraint violation detected")
    if any(row["status"] != "COMPLETE" for row in qc["checkpoints"]):
        raise RuntimeError("cannot complete manifest with unfinished checkpoint")


def fixture_storage_metrics() -> dict[str, float]:
    with tempfile.TemporaryDirectory(prefix="paper2-manifest-storage-") as tmp:
        base = Path(tmp)
        p1 = base / "works.sqlite3"
        p2 = base / "edges.sqlite3"
        now = "2000-01-01T00:00:00+00:00"
        rows = [
            (
                f"W{i:09d}",
                f"W{i:09d}",
                f"Synthetic work {i} with representative bibliographic title",
                2000 + i % 25,
                f"10.0000/{i}",
                None,
                json.dumps(
                    {
                        "openalex": f"https://openalex.org/W{i:09d}",
                        "doi": f"https://doi.org/10.0000/{i}",
                    },
                    separators=(",", ":"),
                ),
                1 + i,
                f"Author {i}",
                now,
                now,
            )
            for i in range(1000)
        ]

        c1 = init_db(p1)
        with c1:
            c1.executemany("INSERT INTO works VALUES(?,?,?,?,?,?,?,?,?,?,?)", rows)
        c1.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        c1.execute("VACUUM")
        c1.close()
        works_bytes = p1.stat().st_size

        c2 = init_db(p2)
        with c2:
            c2.executemany("INSERT INTO works VALUES(?,?,?,?,?,?,?,?,?,?,?)", rows)
            c2.executemany(
                "INSERT INTO retrieval_channels VALUES(?,?)",
                [
                    (f"W{i:09d}", channel)
                    for i in range(1000)
                    for channel in CHANNELS
                ],
            )
            c2.executemany(
                "INSERT INTO work_r1_topics VALUES(?,?)",
                [(f"W{i:09d}", f"T{i % 59:03d}") for i in range(1000)],
            )
            c2.executemany(
                "INSERT INTO work_r2_queries VALUES(?,?,?)",
                [
                    (f"W{i:09d}", f"R2-{i % 35 + 1:03d}", f"query {i % 35}")
                    for i in range(1000)
                ],
            )
            c2.executemany(
                "INSERT INTO work_r3_anchors VALUES(?,?,?)",
                [
                    (f"W{i:09d}", f"R3-{i % 15 + 1:03d}", f"anchor {i % 15}")
                    for i in range(1000)
                ],
            )
        c2.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        c2.execute("VACUUM")
        c2.close()
        all_bytes = p2.stat().st_size

    return {
        "synthetic_bytes_per_work": works_bytes / 1000.0,
        "synthetic_incremental_bytes_per_edge": max(
            0.0, (all_bytes - works_bytes) / 6000.0
        ),
        "synthetic_fixture_works": 1000,
        "synthetic_fixture_edges": 6000,
    }


def resource_preflight(
    counts: dict[str, Any],
    output: Path,
    *,
    r1_topic_edge_multiplier: float | None,
    safety_factor: float,
) -> dict[str, Any]:
    metrics = fixture_storage_metrics()
    raw = counts["raw_counts"]
    n_frame = int(counts["N_frame"])
    r1_raw = int(raw.get("R1") or 0)
    r2_edges = sum(int(x) for x in (raw.get("R2") or {}).values())
    r3_edges = sum(int(x) for x in (raw.get("R3") or {}).values())
    output.parent.mkdir(parents=True, exist_ok=True)
    free = shutil.disk_usage(output.parent.resolve()).free

    report: dict[str, Any] = {
        **metrics,
        "N_frame_counts_snapshot": n_frame,
        "known_R1_raw_hits": r1_raw,
        "known_R2_query_edges": r2_edges,
        "known_R3_anchor_edges": r3_edges,
        "free_bytes": free,
        "safety_factor": safety_factor,
        "basis": "synthetic SQLite calibration; measured R1 topic-edge multiplier required",
    }
    if r1_topic_edge_multiplier is None or r1_topic_edge_multiplier < 1.0:
        report.update(
            {
                "authorized": False,
                "classification": "PREEXECUTION_RESOURCE_BLOCKED",
                "reason": "R1_TOPIC_EDGE_MULTIPLIER_UNMEASURED",
            }
        )
        return report

    r1_edges = int(r1_raw * r1_topic_edge_multiplier)
    channel_edges_upper = 3 * n_frame
    provenance_edges = r1_edges + r2_edges + r3_edges + channel_edges_upper
    estimated = (
        metrics["synthetic_bytes_per_work"] * n_frame
        + metrics["synthetic_incremental_bytes_per_edge"] * provenance_edges
    )
    required = int(estimated * safety_factor)
    report.update(
        {
            "r1_topic_edge_multiplier": r1_topic_edge_multiplier,
            "estimated_R1_topic_edges": r1_edges,
            "conservative_channel_membership_edges": channel_edges_upper,
            "estimated_storage_bytes": int(estimated),
            "required_free_bytes_with_safety_factor": required,
            "authorized": free >= required,
            "classification": (
                "RESOURCE_PREFLIGHT_PASS"
                if free >= required
                else "PREEXECUTION_RESOURCE_BLOCKED"
            ),
            "reason": None if free >= required else "INSUFFICIENT_FREE_SPACE",
        }
    )
    return report


def initialize_or_resume(
    *,
    conn: sqlite3.Connection,
    output: Path,
    config_digest: str,
    manifest_script_digest: str,
    enumerator_script_digest: str,
    counts_digest: str,
    counts: dict[str, Any],
    seed_topics: list[str],
    run_id: str,
    resume: bool,
) -> str:
    existing_schema = get_meta(conn, "manifest_schema_version")
    if existing_schema is None:
        if resume:
            raise ValueError("cannot resume database without manifest metadata")
        with conn:
            set_meta(conn, "manifest_schema_version", SCHEMA_VERSION)
            set_meta(conn, "run_id", run_id)
            set_meta(conn, "run_status", "RUNNING")
            set_meta(conn, "artifact_role", "candidate_manifest_not_eligible_corpus")
            set_meta(conn, "provider", "OpenAlex")
            set_meta(conn, "provider_api_form", "OpenAlex OQL POST")
            set_meta(conn, "per_page", PER_PAGE)
            set_meta(conn, "access_start_timestamp", utc_now())
            set_meta(conn, "access_end_timestamp", None)
            set_meta(conn, "retrieval_config_digest", config_digest)
            set_meta(conn, "query_bank_config_digest", config_digest)
            set_meta(conn, "manifest_script_digest", manifest_script_digest)
            set_meta(conn, "enumerator_script_digest", enumerator_script_digest)
            set_meta(conn, "counts_artifact_digest", counts_digest)
            set_meta(conn, "counts_access_timestamp", counts.get("access_timestamp"))
            set_meta(conn, "counts_N_frame", counts.get("N_frame"))
            set_meta(
                conn,
                "seed_resolution_snapshot_digest",
                canonical_json_digest(counts.get("seed_resolution") or []),
            )
            set_meta(conn, "seed_topics_digest", canonical_json_digest(seed_topics))
            set_meta(conn, "resume_count", 0)
        return run_id

    if not resume:
        raise ValueError(
            f"output already contains a manifest transaction; use --resume: {output}"
        )
    if existing_schema != SCHEMA_VERSION:
        raise ValueError("manifest schema mismatch; refusing resume")

    expected = {
        "retrieval_config_digest": config_digest,
        "manifest_script_digest": manifest_script_digest,
        "enumerator_script_digest": enumerator_script_digest,
        "counts_artifact_digest": counts_digest,
        "seed_topics_digest": canonical_json_digest(seed_topics),
    }
    for key, value in expected.items():
        if get_meta(conn, key) != value:
            raise ValueError(f"resume digest mismatch: {key}")

    old_status = get_meta(conn, "run_status")
    if old_status == "COMPLETE":
        raise ValueError("completed manifest cannot be resumed")
    if old_status not in RESUMABLE_STATUSES:
        raise ValueError(f"manifest status is not resumable: {old_status}")
    stored_run_id = get_meta(conn, "run_id")
    if run_id and run_id != stored_run_id:
        raise ValueError("run_id mismatch on resume")

    with conn:
        set_meta(conn, "resume_from_status", old_status)
        set_meta(conn, "run_status", "RUNNING")
        set_meta(conn, "resume_count", int(get_meta(conn, "resume_count", 0)) + 1)
        set_meta(conn, "last_resume_timestamp", utc_now())
    return stored_run_id


def run_manifest(
    *,
    client: retrieval.OpenAlexClient,
    config: dict[str, Any],
    counts: dict[str, Any],
    counts_path: Path,
    config_path: Path,
    output: Path,
    run_id: str,
    resume: bool,
    max_pages_total: int | None,
    logical_digest: bool,
) -> dict[str, Any]:
    seed_topics = validate_counts_artifact(counts, config)
    config_digest = sha256_file(config_path)
    counts_digest = sha256_file(counts_path)
    manifest_script = Path(__file__).resolve()
    enumerator_script = Path(retrieval.__file__).resolve()
    manifest_script_digest = sha256_file(manifest_script)
    enumerator_script_digest = sha256_file(enumerator_script)

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not resume:
        raise ValueError(f"output exists; refusing fresh overwrite: {output}")
    if resume and not output.exists():
        raise ValueError(f"resume requested but output does not exist: {output}")

    conn = init_db(output)
    actual_run_id = initialize_or_resume(
        conn=conn,
        output=output,
        config_digest=config_digest,
        manifest_script_digest=manifest_script_digest,
        enumerator_script_digest=enumerator_script_digest,
        counts_digest=counts_digest,
        counts=counts,
        seed_topics=seed_topics,
        run_id=run_id,
        resume=resume,
    )

    pages_this_invocation = 0
    try:
        for spec in source_specs(config, seed_topics):
            cp = load_checkpoint(conn, spec)
            if cp["status"] == "COMPLETE":
                continue
            cursor = cp["next_cursor"]
            assert cursor
            while cursor:
                if (
                    max_pages_total is not None
                    and pages_this_invocation >= max_pages_total
                ):
                    with conn:
                        set_meta(conn, "run_status", "INCOMPLETE")
                        set_meta(conn, "access_end_timestamp", utc_now())
                    qc = integrity_qc(conn)
                    conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
                    conn.close()
                    return {
                        "classification": "MANIFEST_PILOT_INCOMPLETE",
                        "run_id": actual_run_id,
                        "database": str(output),
                        "pages_committed_this_invocation": pages_this_invocation,
                        "complete": False,
                        "qc": qc,
                    }

                page = fetch_page(client, spec["query"], cursor)
                ingest_page(
                    conn,
                    spec=spec,
                    config=config,
                    seed_topics=seed_topics,
                    request_cursor=cursor,
                    results=page["results"],
                    next_cursor=page["next_cursor"],
                )
                pages_this_invocation += 1
                cursor = page["next_cursor"]

        qc = integrity_qc(conn)
        validate_integrity_for_completion(qc)
        logical = logical_manifest_digest(conn) if logical_digest else None
        unique = qc["N_unique_works"]
        counts_n = int(counts["N_frame"])
        reconciliation = (
            "MATCHED_ACROSS_DIFFERENT_ACCESS_WINDOWS"
            if unique == counts_n
            else "PROVIDER_DRIFT_OBSERVED"
        )

        with conn:
            set_meta(conn, "run_status", "COMPLETE")
            set_meta(conn, "access_end_timestamp", utc_now())
            set_meta(conn, "provider_drift_classification", reconciliation)
            set_meta(conn, "final_unique_works", unique)
            set_meta(conn, "logical_manifest_digest", logical)
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        conn.close()
        return {
            "classification": "PAPER2_RETRIEVAL_V1_MANIFEST_FROZEN",
            "run_id": actual_run_id,
            "database": str(output),
            "artifact_sha256": sha256_file(output),
            "logical_manifest_digest": logical,
            "pages_committed_this_invocation": pages_this_invocation,
            "complete": True,
            "counts_reconciliation": {
                "counts_N_frame": counts_n,
                "manifest_N_unique_works": unique,
                "classification": reconciliation,
                "snapshot_relation": "different_access_window",
            },
            "qc": qc,
        }
    except KeyboardInterrupt:
        with conn:
            set_meta(conn, "run_status", "INTERRUPTED")
            set_meta(conn, "access_end_timestamp", utc_now())
        conn.close()
        raise
    except Exception:
        with conn:
            set_meta(conn, "run_status", "FAILED")
            set_meta(conn, "access_end_timestamp", utc_now())
        conn.close()
        raise


def fake_work(
    wid: str | None,
    *,
    title: str = "Synthetic title",
    year: int = 2020,
    doi: str | None = None,
    topics: Iterable[str] = (),
    author: str = "Synthetic Author",
) -> dict[str, Any]:
    work: dict[str, Any] = {
        "id": f"https://openalex.org/{wid}" if wid else None,
        "ids": (
            {"openalex": f"https://openalex.org/{wid}"} if wid else {}
        ),
        "doi": f"https://doi.org/{doi}" if doi else None,
        "display_name": title,
        "publication_year": year,
        "cited_by_count": 2,
        "topics": [{"id": f"https://openalex.org/topics/{t}"} for t in topics],
        "authorships": [{"author": {"display_name": author}}],
        "primary_location": None,
    }
    if doi:
        work["ids"]["doi"] = f"https://doi.org/{doi}"
    return work


def initialize_fixture_db(
    path: Path, config: dict[str, Any], seed_topics: list[str]
) -> sqlite3.Connection:
    conn = init_db(path)
    with conn:
        set_meta(conn, "manifest_schema_version", SCHEMA_VERSION)
        set_meta(conn, "run_id", "fixture")
        set_meta(conn, "run_status", "RUNNING")
        set_meta(conn, "retrieval_config_digest", "config-a")
        set_meta(conn, "manifest_script_digest", "manifest-a")
        set_meta(conn, "enumerator_script_digest", "enum-a")
        set_meta(conn, "counts_artifact_digest", "counts-a")
        set_meta(conn, "seed_topics_digest", canonical_json_digest(seed_topics))
    for spec in source_specs(config, seed_topics):
        ensure_checkpoint(conn, spec)
    return conn


def self_test(config: dict[str, Any]) -> None:
    seed_topics = ["T1", "T2"]
    specs = source_specs(config, seed_topics)
    r1 = next(s for s in specs if s["channel"] == "R1")
    r2a = next(
        s for s in specs if s["channel"] == "R2" and s["source_index"] == 0
    )
    r2b = next(
        s for s in specs if s["channel"] == "R2" and s["source_index"] == 1
    )
    r3 = next(
        s for s in specs if s["channel"] == "R3" and s["source_index"] == 0
    )

    with tempfile.TemporaryDirectory(prefix="paper2-manifest-selftest-") as tmp:
        root = Path(tmp)

        # P1/P2/P3/P4/P6.
        db = root / "p1.sqlite3"
        conn = initialize_fixture_db(db, config, seed_topics)
        w1 = fake_work("W1", doi="10.1/a", topics=["T1"])
        w2 = fake_work("W2", doi="10.1/b", topics=["T2"])
        ingest_page(
            conn,
            spec=r1,
            config=config,
            seed_topics=seed_topics,
            request_cursor="*",
            results=[w1, w2],
            next_cursor=None,
        )
        for spec in (r2a, r2b, r3):
            ingest_page(
                conn,
                spec=spec,
                config=config,
                seed_topics=seed_topics,
                request_cursor="*",
                results=[w1],
                next_cursor=None,
            )
        before = (
            conn.execute("SELECT COUNT(*) FROM works").fetchone()[0],
            conn.execute("SELECT COUNT(*) FROM work_r2_queries").fetchone()[0],
        )
        with conn:
            conn.execute(
                "UPDATE checkpoints SET status='RUNNING',next_cursor='*' "
                "WHERE channel='R2' AND source_index=0"
            )
        ingest_page(
            conn,
            spec=r2a,
            config=config,
            seed_topics=seed_topics,
            request_cursor="*",
            results=[w1],
            next_cursor=None,
        )
        after = (
            conn.execute("SELECT COUNT(*) FROM works").fetchone()[0],
            conn.execute("SELECT COUNT(*) FROM work_r2_queries").fetchone()[0],
        )
        assert before == after == (2, 2)
        assert (
            conn.execute(
                "SELECT COUNT(*) FROM retrieval_channels WHERE work_id='W1'"
            ).fetchone()[0]
            == 3
        )
        conn.close()

        # P5 resume equivalence.
        pages = [
            ("*", [fake_work("W10", topics=["T1"])], "c2"),
            ("c2", [fake_work("W11", topics=["T1"])], "c3"),
            ("c3", [fake_work("W12", topics=["T2"])], None),
        ]
        clean = root / "clean.sqlite3"
        c1 = initialize_fixture_db(clean, config, seed_topics)
        for cursor, rows, nxt in pages:
            ingest_page(
                c1,
                spec=r1,
                config=config,
                seed_topics=seed_topics,
                request_cursor=cursor,
                results=rows,
                next_cursor=nxt,
            )
        clean_digest = logical_manifest_digest(c1)
        c1.close()

        resumed = root / "resumed.sqlite3"
        c2 = initialize_fixture_db(resumed, config, seed_topics)
        ingest_page(
            c2,
            spec=r1,
            config=config,
            seed_topics=seed_topics,
            request_cursor=pages[0][0],
            results=pages[0][1],
            next_cursor=pages[0][2],
        )
        c2.close()
        c2 = init_db(resumed)
        ensure_checkpoint(c2, r1)
        for cursor, rows, nxt in pages[1:]:
            ingest_page(
                c2,
                spec=r1,
                config=config,
                seed_topics=seed_topics,
                request_cursor=cursor,
                results=rows,
                next_cursor=nxt,
            )
        assert logical_manifest_digest(c2) == clean_digest
        c2.close()

        # P7 corrupt checkpoint detection.
        corrupt = root / "corrupt.sqlite3"
        c3 = initialize_fixture_db(corrupt, config, seed_topics)
        with c3:
            c3.execute(
                "UPDATE checkpoints SET next_cursor=NULL,status='RUNNING' "
                "WHERE channel='R1' AND source_index=0"
            )
        try:
            ensure_checkpoint(c3, r1)
            raise AssertionError("corrupt checkpoint was accepted")
        except ValueError:
            pass
        c3.close()

        # P8 page rollback.
        rollback = root / "rollback.sqlite3"
        c4 = initialize_fixture_db(rollback, config, seed_topics)
        try:
            ingest_page(
                c4,
                spec=r1,
                config=config,
                seed_topics=seed_topics,
                request_cursor="*",
                results=[fake_work("W20", topics=["T1"])],
                next_cursor=None,
                fault_after_works=True,
            )
            raise AssertionError("synthetic fault did not fire")
        except RuntimeError:
            pass
        assert (
            c4.execute(
                "SELECT COUNT(*) FROM works WHERE work_id='W20'"
            ).fetchone()[0]
            == 0
        )
        assert load_checkpoint(c4, r1)["pages_committed"] == 0
        c4.close()

        # N1 fallback identity.
        fallback = fake_work(None, doi="10.1234/Fallback")
        key, provider_id = canonical_work_identity(fallback)
        assert key == "doi:10.1234/fallback" and provider_id is None

        # N2 title collision.
        collision = root / "collision.sqlite3"
        c5 = initialize_fixture_db(collision, config, seed_topics)
        ingest_page(
            c5,
            spec=r1,
            config=config,
            seed_topics=seed_topics,
            request_cursor="*",
            results=[
                fake_work("W31", title="Same Title", topics=["T1"]),
                fake_work("W32", title="Same Title", topics=["T1"]),
            ],
            next_cursor=None,
        )
        assert c5.execute("SELECT COUNT(*) FROM works").fetchone()[0] == 2
        c5.close()

        # N3 malformed provenance.
        bad = dict(r2a)
        bad["source_key"] = "not-a-frozen-query"
        try:
            validate_source_spec(bad, config, seed_topics)
            raise AssertionError("malformed provenance was accepted")
        except ValueError:
            pass

        # N4 config digest mismatch on resume.
        mismatch = root / "mismatch.sqlite3"
        c6 = initialize_fixture_db(mismatch, config, seed_topics)
        try:
            initialize_or_resume(
                conn=c6,
                output=mismatch,
                config_digest="config-b",
                manifest_script_digest="manifest-a",
                enumerator_script_digest="enum-a",
                counts_digest="counts-a",
                counts={"access_timestamp": "x", "N_frame": 1},
                seed_topics=seed_topics,
                run_id="fixture",
                resume=True,
            )
            raise AssertionError("config digest mismatch was accepted")
        except ValueError:
            pass
        c6.close()

        metrics = fixture_storage_metrics()
        assert metrics["synthetic_bytes_per_work"] > 0
        assert metrics["synthetic_incremental_bytes_per_edge"] >= 0

    print("PAPER2_RETRIEVAL_V1_MANIFEST_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("research/paper2/retrieval_v1.json"),
    )
    parser.add_argument("--counts-artifact", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("paper2-retrieval-v1.sqlite3"),
    )
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--allow-large-run", action="store_true")
    parser.add_argument("--max-pages-total", type=int, default=None)
    parser.add_argument("--pause", type=float, default=0.12)
    parser.add_argument("--logical-digest", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--r1-topic-edge-multiplier", type=float, default=None)
    parser.add_argument("--free-space-safety-factor", type=float, default=1.5)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    config = retrieval.load_config(args.config)
    if args.self_test:
        self_test(config)
        return 0

    if args.counts_artifact is None:
        parser.error("--counts-artifact is required outside --self-test")
    counts = json.loads(args.counts_artifact.read_text(encoding="utf-8"))
    validate_counts_artifact(counts, config)

    preflight = resource_preflight(
        counts,
        args.output,
        r1_topic_edge_multiplier=args.r1_topic_edge_multiplier,
        safety_factor=args.free_space_safety_factor,
    )
    if args.preflight_only:
        rendered = json.dumps(preflight, ensure_ascii=False, indent=2) + "\n"
        if args.json_output:
            args.json_output.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 0 if preflight["authorized"] else 2

    if not args.allow_large_run and args.max_pages_total is None:
        parser.error("full manifest requires --allow-large-run")
    if args.allow_large_run and not preflight["authorized"]:
        raise SystemExit(
            "PREEXECUTION_RESOURCE_BLOCKED: run --preflight-only with a measured "
            "--r1-topic-edge-multiplier and sufficient free space"
        )
    if args.max_pages_total is not None and args.max_pages_total <= 0:
        parser.error("--max-pages-total must be positive")

    run_id = args.run_id or (
        "paper2-retrieval-v1-" + time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    )
    client = retrieval.OpenAlexClient(
        api_key=os.environ.get("OPENALEX_API_KEY"),
        mailto=os.environ.get("OPENALEX_MAILTO"),
        pause=args.pause,
    )
    result = run_manifest(
        client=client,
        config=config,
        counts=counts,
        counts_path=args.counts_artifact,
        config_path=args.config,
        output=args.output,
        run_id=run_id,
        resume=args.resume,
        max_pages_total=args.max_pages_total,
        logical_digest=args.logical_digest,
    )
    result["resource_preflight"] = preflight
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json_output:
        args.json_output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
