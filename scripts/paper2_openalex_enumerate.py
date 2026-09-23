#!/usr/bin/env python3
"""Enumerate the frozen Paper 2 OpenAlex retrieval frame v1.

Owner: #143
Authority: #133

Default mode is counts-only. Manifest mode is intentionally gated because it
may traverse a very large result set and consume substantial API quota.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable

API_ROOT = "https://api.openalex.org/"
WORKS_ROOT = "https://api.openalex.org/works/"
USER_AGENT = "relay-theory-paper2-retrieval-v1/1.0"


def load_config(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "paper2-retrieval-v1":
        raise ValueError("unexpected retrieval schema_version")
    if data.get("provider") != "OpenAlex":
        raise ValueError("retrieval v1 provider must be OpenAlex")
    if data.get("citation_floor") != 1:
        raise ValueError("retrieval v1 citation floor must remain 1")
    if len(data.get("seeds", [])) != 50:
        raise ValueError("paper2-top50-v1 must contain exactly 50 seeds")
    return data


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def normalize_title(value: str) -> str:
    value = value.casefold()
    value = re.sub(r"[^\w\s]+", " ", value, flags=re.UNICODE)
    return " ".join(value.split())


def short_openalex_id(value: str) -> str:
    return value.rstrip("/").split("/")[-1]


def oql_quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def text_clause(value: str, exact: bool = False) -> str:
    """Match OpenAlex Works-search scope: title + abstract + available full text."""
    if exact:
        quoted = f'"{oql_quote(value)}"'
        return (
            f"(title/abstract has ({quoted}) or full text has ({quoted}))"
        )
    return (
        f"(title/abstract has ({value}) or full text has ({value}))"
    )


class OpenAlexClient:
    def __init__(self, api_key: str | None, mailto: str | None, pause: float) -> None:
        self.api_key = api_key
        self.mailto = mailto
        self.pause = pause

    def _url(self, base: str) -> str:
        params: dict[str, str] = {}
        if self.api_key:
            params["api_key"] = self.api_key
        if self.mailto:
            params["mailto"] = self.mailto
        if not params:
            return base
        sep = "&" if "?" in base else "?"
        return base + sep + urllib.parse.urlencode(params)

    def request_json(
        self,
        url: str,
        *,
        method: str = "GET",
        body: dict[str, Any] | None = None,
        retries: int = 5,
    ) -> dict[str, Any]:
        data = None
        headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        last_error: Exception | None = None
        for attempt in range(retries):
            try:
                req = urllib.request.Request(
                    self._url(url), data=data, headers=headers, method=method
                )
                with urllib.request.urlopen(req, timeout=60) as response:
                    payload = json.load(response)
                if self.pause:
                    time.sleep(self.pause)
                return payload
            except urllib.error.HTTPError as exc:
                last_error = exc
                if exc.code not in {429, 500, 502, 503, 504}:
                    detail = exc.read().decode("utf-8", "replace")
                    raise RuntimeError(f"OpenAlex HTTP {exc.code}: {detail}") from exc
            except (urllib.error.URLError, TimeoutError) as exc:
                last_error = exc
            time.sleep(min(2 ** attempt, 16))

        raise RuntimeError(f"OpenAlex request failed after retries: {last_error}")

    def run_oql(
        self,
        query: str,
        *,
        per_page: int = 1,
        cursor: str | None = None,
        select: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"oql": query, "per-page": per_page}
        if cursor is not None:
            body["cursor"] = cursor
        if select:
            body["select"] = select
        return self.request_json(API_ROOT, method="POST", body=body)

    def count(self, query: str) -> int:
        payload = self.run_oql(query, per_page=1)
        return int(payload["meta"]["count"])

    def by_doi(self, doi: str) -> dict[str, Any] | None:
        target = WORKS_ROOT + urllib.parse.quote(
            "https://doi.org/" + doi, safe=":/"
        )
        try:
            return self.request_json(target)
        except RuntimeError as exc:
            if "HTTP 404" in str(exc):
                return None
            raise


def seed_lookup_query(seed: dict[str, Any]) -> str:
    title = oql_quote(seed["title"])
    year = int(seed["year"])
    return f'works where title has ("{title}") and year is ({year})'


def resolve_seed(client: OpenAlexClient, seed: dict[str, Any]) -> dict[str, Any]:
    work: dict[str, Any] | None = None
    source = None

    if seed.get("doi"):
        work = client.by_doi(seed["doi"])
        if work is not None:
            source = "doi"

    if work is None:
        payload = client.run_oql(
            seed_lookup_query(seed),
            per_page=10,
            select="id,doi,display_name,publication_year,topics,primary_topic,cited_by_count",
        )
        exact = [
            item
            for item in payload.get("results", [])
            if normalize_title(item.get("display_name") or "")
            == normalize_title(seed["title"])
            and item.get("publication_year") == seed["year"]
        ]
        if len(exact) == 1:
            work = exact[0]
            source = "exact_title_year"
        elif len(exact) > 1:
            return {
                "seed_number": seed["number"],
                "title": seed["title"],
                "status": "AMBIGUOUS_PROVIDER_MATCH",
                "matches": [
                    {
                        "id": short_openalex_id(x["id"]),
                        "title": x.get("display_name"),
                        "year": x.get("publication_year"),
                        "doi": x.get("doi"),
                    }
                    for x in exact
                ],
            }

    if work is None:
        return {
            "seed_number": seed["number"],
            "title": seed["title"],
            "status": "SEED_PROVIDER_MISS",
        }

    topics = sorted(
        {
            short_openalex_id(topic["id"])
            for topic in work.get("topics", [])
            if topic.get("id")
        }
    )
    primary = work.get("primary_topic") or {}
    return {
        "seed_number": seed["number"],
        "title": seed["title"],
        "status": "RESOLVED",
        "resolution_source": source,
        "openalex_id": short_openalex_id(work["id"]),
        "provider_title": work.get("display_name"),
        "year": work.get("publication_year"),
        "doi": work.get("doi"),
        "cited_by_count": work.get("cited_by_count"),
        "primary_topic": (
            short_openalex_id(primary["id"]) if primary.get("id") else None
        ),
        "topic_ids": topics,
    }


def topic_clause(topic_ids: Iterable[str]) -> str | None:
    ids = sorted(set(topic_ids))
    if not ids:
        return None
    return "topic is (" + " or ".join(ids) + ")"


def base_count_query(clause: str, citation_floor: int) -> str:
    return f"works where citation count >= ({citation_floor}) and ({clause})"


def union_query(
    topic_ids: list[str],
    text_queries: list[str],
    anchors: list[str],
    citation_floor: int,
) -> str:
    parts: list[str] = []
    tc = topic_clause(topic_ids)
    if tc:
        parts.append(tc)
    parts.extend(text_clause(q) for q in text_queries)
    parts.extend(text_clause(q, exact=True) for q in anchors)
    return base_count_query(" or ".join(f"({part})" for part in parts), citation_floor)


def counts_mode(
    client: OpenAlexClient, config: dict[str, Any]
) -> dict[str, Any]:
    seed_results = [resolve_seed(client, seed) for seed in config["seeds"]]
    topic_ids = sorted(
        {
            topic
            for result in seed_results
            if result["status"] == "RESOLVED"
            for topic in result.get("topic_ids", [])
        }
    )
    floor = int(config["citation_floor"])

    raw: dict[str, Any] = {"R1": None, "R2": {}, "R3": {}}
    tc = topic_clause(topic_ids)
    if tc:
        raw["R1"] = client.count(base_count_query(tc, floor))

    for query in config["text_queries"]:
        raw["R2"][query] = client.count(
            base_count_query(text_clause(query), floor)
        )

    for query in config["anchor_queries"]:
        raw["R3"][query] = client.count(
            base_count_query(text_clause(query, exact=True), floor)
        )

    uq = union_query(
        topic_ids,
        config["text_queries"],
        config["anchor_queries"],
        floor,
    )
    frame_count = client.count(uq)

    return {
        "schema_version": config["schema_version"],
        "provider": "OpenAlex",
        "access_timestamp": utc_now(),
        "citation_floor": floor,
        "seed_resolution": seed_results,
        "seed_topics_v1": topic_ids,
        "raw_counts": raw,
        "N_frame": frame_count,
        "union_oql": uq,
    }


def init_db(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS works (
          openalex_id TEXT PRIMARY KEY,
          title TEXT NOT NULL,
          publication_year INTEGER,
          doi TEXT,
          cited_by_count INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS retrievals (
          openalex_id TEXT NOT NULL,
          channel TEXT NOT NULL,
          reason TEXT NOT NULL,
          PRIMARY KEY (openalex_id, channel, reason)
        );
        CREATE TABLE IF NOT EXISTS metadata (
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL
        );
        """
    )
    return conn


def stream_query(
    client: OpenAlexClient,
    query: str,
    *,
    max_pages: int | None = None,
) -> Iterable[dict[str, Any]]:
    cursor = "*"
    page = 0
    select = "id,doi,display_name,publication_year,cited_by_count,topics"
    while cursor:
        payload = client.run_oql(
            query, per_page=200, cursor=cursor, select=select
        )
        for item in payload.get("results", []):
            yield item
        cursor = payload.get("meta", {}).get("next_cursor")
        page += 1
        if max_pages is not None and page >= max_pages:
            break


def upsert_work(conn: sqlite3.Connection, work: dict[str, Any]) -> str:
    oid = short_openalex_id(work["id"])
    conn.execute(
        """
        INSERT INTO works(openalex_id, title, publication_year, doi, cited_by_count)
        VALUES(?, ?, ?, ?, ?)
        ON CONFLICT(openalex_id) DO UPDATE SET
          title=excluded.title,
          publication_year=excluded.publication_year,
          doi=excluded.doi,
          cited_by_count=excluded.cited_by_count
        """,
        (
            oid,
            work.get("display_name") or "",
            work.get("publication_year"),
            work.get("doi"),
            int(work.get("cited_by_count") or 0),
        ),
    )
    return oid


def add_retrieval(
    conn: sqlite3.Connection, openalex_id: str, channel: str, reason: str
) -> None:
    conn.execute(
        """
        INSERT OR IGNORE INTO retrievals(openalex_id, channel, reason)
        VALUES(?, ?, ?)
        """,
        (openalex_id, channel, reason),
    )


def manifest_mode(
    client: OpenAlexClient,
    config: dict[str, Any],
    output: Path,
    *,
    max_pages: int | None,
) -> dict[str, Any]:
    counts = counts_mode(client, config)
    topic_ids = counts["seed_topics_v1"]
    floor = int(config["citation_floor"])
    conn = init_db(output)

    tc = topic_clause(topic_ids)
    if tc:
        query = base_count_query(tc, floor)
        topic_set = set(topic_ids)
        for work in stream_query(client, query, max_pages=max_pages):
            oid = upsert_work(conn, work)
            matched = sorted(
                topic_set
                & {
                    short_openalex_id(topic["id"])
                    for topic in work.get("topics", [])
                    if topic.get("id")
                }
            )
            for tid in matched:
                add_retrieval(conn, oid, "R1", f"seed_topic:{tid}")
        conn.commit()

    for text in config["text_queries"]:
        query = base_count_query(text_clause(text), floor)
        for work in stream_query(client, query, max_pages=max_pages):
            oid = upsert_work(conn, work)
            add_retrieval(conn, oid, "R2", f"text:{text}")
        conn.commit()

    for anchor in config["anchor_queries"]:
        query = base_count_query(text_clause(anchor, exact=True), floor)
        for work in stream_query(client, query, max_pages=max_pages):
            oid = upsert_work(conn, work)
            add_retrieval(conn, oid, "R3", f"anchor:{anchor}")
        conn.commit()

    unique = conn.execute("SELECT COUNT(*) FROM works").fetchone()[0]
    retrievals = conn.execute("SELECT COUNT(*) FROM retrievals").fetchone()[0]
    conn.execute(
        "INSERT OR REPLACE INTO metadata(key, value) VALUES(?, ?)",
        ("provider_snapshot", json.dumps(counts, ensure_ascii=False)),
    )
    conn.commit()
    conn.close()
    return {
        "database": str(output),
        "unique_works_materialized": unique,
        "retrieval_attributions": retrievals,
        "provider_count_N_frame": counts["N_frame"],
        "max_pages_per_channel": max_pages,
        "complete": max_pages is None,
    }


def self_test(config: dict[str, Any]) -> None:
    numbers = [seed["number"] for seed in config["seeds"]]
    assert numbers == list(range(1, 51))
    assert len(config["text_queries"]) == len(set(config["text_queries"]))
    assert len(config["anchor_queries"]) == len(set(config["anchor_queries"]))
    assert config["citation_floor"] == 1
    q = union_query(["T1", "T2"], ["memory"], ["extended mind"], 1)
    assert "citation count >= (1)" in q
    assert "topic is (T1 or T2)" in q
    assert "title/abstract has (memory)" in q
    assert "full text has (memory)" in q
    assert 'title/abstract has ("extended mind")' in q
    assert 'full text has ("extended mind")' in q
    forbidden = {
        "basis_elements",
        "basis_mapping",
        "decomposition_success",
        "decomposition_failure",
        "lean_theorem",
        "lean_result",
        "residual_type",
        "basis_extension",
        "coverage_score",
    }
    assert not (forbidden & set(config))
    print("PAPER2_RETRIEVAL_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("research/paper2/retrieval_v1.json"),
    )
    parser.add_argument(
        "--mode",
        choices=("counts", "manifest"),
        default="counts",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("paper2-retrieval-v1.sqlite3"),
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=None,
        help="optional file for the counts/result JSON",
    )
    parser.add_argument(
        "--allow-large-run",
        action="store_true",
        help="required for manifest mode",
    )
    parser.add_argument(
        "--max-pages-per-channel",
        type=int,
        default=None,
        help="debug/pilot cap; any value makes manifest incomplete",
    )
    parser.add_argument(
        "--pause",
        type=float,
        default=0.12,
        help="seconds between provider requests",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.self_test:
        self_test(config)
        return 0

    api_key = os.environ.get("OPENALEX_API_KEY")
    mailto = os.environ.get("OPENALEX_MAILTO")
    client = OpenAlexClient(api_key=api_key, mailto=mailto, pause=args.pause)

    if args.mode == "counts":
        result = counts_mode(client, config)
    else:
        if not args.allow_large_run:
            parser.error("manifest mode requires --allow-large-run")
        result = manifest_mode(
            client,
            config,
            args.output,
            max_pages=args.max_pages_per_channel,
        )

    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json_output:
        args.json_output.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
