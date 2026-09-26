#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

DEFAULT_CONTRACT = Path("research/paper2/eligibility_screening_v1.json")
ERA_SCHEMA = "paper2-eligibility-screening-era-v1"
CORPUS_SCHEMA = "paper2-primary-work-corpus-v1"
ADJUDICATION_SCHEMA = "paper2-eligibility-adjudications-v1"


class ScreeningError(RuntimeError):
    pass


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_json(value: Any) -> str:
    rendered = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(rendered).hexdigest()


def write_json_atomic(path: Path, value: Any) -> None:
    if path.exists():
        raise ScreeningError(f"OUTPUT_ALREADY_EXISTS:{path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    if tmp.exists():
        raise ScreeningError(f"OUTPUT_TEMP_ALREADY_EXISTS:{tmp}")
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


def normalized_key(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def reject_forbidden_keys(value: Any, forbidden: set[str], path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            norm = normalized_key(str(key))
            if norm in forbidden:
                raise ScreeningError(f"FORBIDDEN_ELIGIBILITY_FIELD:{path}.{key}")
            reject_forbidden_keys(child, forbidden, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_forbidden_keys(child, forbidden, f"{path}[{index}]")


def load_contract(path: Path = DEFAULT_CONTRACT) -> dict[str, Any]:
    contract = load_json(path)
    if contract.get("schema_version") != "paper2-eligibility-screening-contract-v1":
        raise ScreeningError("SCREENING_CONTRACT_SCHEMA_MISMATCH")
    if contract.get("owner_issue") != 212:
        raise ScreeningError("SCREENING_OWNER_DRIFT")
    eras = contract.get("frozen_era_order")
    quotas = contract.get("frozen_quotas")
    if not isinstance(eras, list) or len(eras) != 9:
        raise ScreeningError("FROZEN_ERA_ORDER_INVALID")
    if not isinstance(quotas, dict) or set(quotas) != set(eras):
        raise ScreeningError("FROZEN_QUOTA_MAP_INVALID")
    if sum(int(quotas[era]) for era in eras) != 1000:
        raise ScreeningError("FROZEN_QUOTA_SUM_INVALID")
    if contract.get("total_primary_work_target") != 1000:
        raise ScreeningError("PRIMARY_WORK_TARGET_DRIFT")
    for authority_field in (
        "real_source_acquisition_authorized",
        "real_eligibility_adjudication_authorized",
        "real_primary_corpus_freeze_authorized",
    ):
        if not isinstance(contract.get(authority_field), bool):
            raise ScreeningError(f"SCREENING_AUTHORITY_FIELD_INVALID:{authority_field}")
    if contract.get("architecture_consequence") != "NONE":
        raise ScreeningError("ARCHITECTURE_CONSEQUENCE_DRIFT")
    algorithm = contract.get("screening_algorithm", {})
    if algorithm.get("quota_fill_state") != "INCLUDE":
        raise ScreeningError("QUOTA_FILL_STATE_DRIFT")
    if algorithm.get("post_quota_noncalibration_state") != "UNSCREENED_AFTER_QUOTA":
        raise ScreeningError("POST_QUOTA_STATE_DRIFT")
    if algorithm.get("post_freeze_replacement_limit") != 0:
        raise ScreeningError("POST_FREEZE_REPLACEMENT_DRIFT")
    if algorithm.get("ladder_exhaustion_classification") != "LADDER_EXHAUSTED_BEFORE_QUOTA":
        raise ScreeningError("LADDER_EXHAUSTION_CLASSIFICATION_DRIFT")
    return contract


def validate_ladder(
    ladder: dict[str, Any],
    *,
    era: str,
    contract: dict[str, Any],
) -> list[dict[str, Any]]:
    accepted = set(contract["accepted_ranked_artifact_schemas"])
    if ladder.get("schema_version") not in accepted:
        raise ScreeningError(f"RANKED_ARTIFACT_SCHEMA_NOT_ACCEPTED:{ladder.get('schema_version')}")
    if ladder.get("era") != era:
        raise ScreeningError(f"RANKED_ARTIFACT_ERA_MISMATCH:{ladder.get('era')}!={era}")
    if ladder.get("global_boundary_tie_closed") is not True:
        raise ScreeningError("RANKED_ARTIFACT_GLOBAL_BOUNDARY_TIE_OPEN")
    if int(ladder.get("merge_provider_calls", -1)) != 0:
        raise ScreeningError("RANKED_ARTIFACT_MERGE_PROVIDER_CALLS_NONZERO")
    rows = ladder.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ScreeningError("RANKED_ARTIFACT_ROWS_MISSING")
    if int(ladder.get("frozen_row_count", -1)) != len(rows):
        raise ScreeningError("RANKED_ARTIFACT_ROW_COUNT_MISMATCH")

    seen_ids: set[str] = set()
    for expected_rank, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ScreeningError(f"RANKED_ROW_NOT_OBJECT:{expected_rank}")
        rank = row.get("rank")
        if rank != expected_rank:
            raise ScreeningError(
                f"RANK_SEQUENCE_INVALID:expected={expected_rank}:observed={rank}"
            )
        wid = row.get("provider_work_id")
        if not isinstance(wid, str) or not wid:
            raise ScreeningError(f"RANKED_ROW_WORK_ID_INVALID:{expected_rank}")
        if wid in seen_ids:
            raise ScreeningError(f"DUPLICATE_WORK_ID_WITHIN_LADDER:{wid}")
        seen_ids.add(wid)
        state = row.get("screening_state")
        if state not in {"UNSCREENED", "CALIBRATION_EXCLUDED"}:
            raise ScreeningError(f"RANKED_ROW_INITIAL_SCREENING_STATE_INVALID:{wid}:{state}")
    return rows


def validate_claim(claim: dict[str, Any], contract: dict[str, Any]) -> None:
    if not isinstance(claim.get("claim_id"), str) or not claim["claim_id"]:
        raise ScreeningError("ELIGIBILITY_CLAIM_ID_INVALID")
    if not isinstance(claim.get("source_locator"), str) or not claim["source_locator"]:
        raise ScreeningError("ELIGIBILITY_SOURCE_LOCATOR_INVALID")
    excerpt_hash = claim.get("source_excerpt_hash")
    if excerpt_hash is not None and (
        not isinstance(excerpt_hash, str) or len(excerpt_hash) != 64
    ):
        raise ScreeningError("ELIGIBILITY_SOURCE_EXCERPT_HASH_INVALID")
    if claim.get("route") not in set(contract["claim_routes"]):
        raise ScreeningError(f"ELIGIBILITY_ROUTE_INVALID:{claim.get('route')}")
    if claim.get("generalization") not in {"YES", "NO", "UNCERTAIN"}:
        raise ScreeningError("ELIGIBILITY_GENERALIZATION_INVALID")
    if claim.get("construct_level_relevance") not in {"YES", "NO", "UNCERTAIN"}:
        raise ScreeningError("ELIGIBILITY_CONSTRUCT_RELEVANCE_INVALID")
    roles = claim.get("operational_roles")
    if not isinstance(roles, list):
        raise ScreeningError("ELIGIBILITY_OPERATIONAL_ROLES_INVALID")
    allowed_roles = set(contract["operational_roles"])
    if len(set(roles)) != len(roles) or any(role not in allowed_roles for role in roles):
        raise ScreeningError("ELIGIBILITY_OPERATIONAL_ROLE_INVALID")


def validate_adjudication(
    record: dict[str, Any],
    *,
    row: dict[str, Any],
    era: str,
    ranked_sha256: str,
    contract: dict[str, Any],
) -> str:
    forbidden = {normalized_key(x) for x in contract["forbidden_key_names_recursive"]}
    reject_forbidden_keys(record, forbidden)

    wid = row["provider_work_id"]
    if record.get("provider_work_id") != wid:
        raise ScreeningError(f"ADJUDICATION_WORK_ID_MISMATCH:{wid}")
    if record.get("era") != era:
        raise ScreeningError(f"ADJUDICATION_ERA_MISMATCH:{wid}")
    if record.get("rank") != row["rank"]:
        raise ScreeningError(f"ADJUDICATION_RANK_MISMATCH:{wid}")
    if record.get("ranked_artifact_sha256") != ranked_sha256:
        raise ScreeningError(f"ADJUDICATION_RANKED_HASH_MISMATCH:{wid}")
    if record.get("classifier_version") != "paper2-eligibility-v1.1":
        raise ScreeningError(f"ADJUDICATION_CLASSIFIER_VERSION_MISMATCH:{wid}")
    if not isinstance(record.get("adjudication_version"), str) or not record["adjudication_version"]:
        raise ScreeningError(f"ADJUDICATION_VERSION_MISSING:{wid}")

    source_access = record.get("source_access")
    if not isinstance(source_access, dict):
        raise ScreeningError(f"SOURCE_ACCESS_RECORD_MISSING:{wid}")
    access = source_access.get("status")
    if access not in set(contract["source_access_states"]):
        raise ScreeningError(f"SOURCE_ACCESS_STATE_INVALID:{wid}:{access}")
    version = source_access.get("version")
    if version is not None and not isinstance(version, str):
        raise ScreeningError(f"SOURCE_ACCESS_VERSION_INVALID:{wid}")

    checks = record.get("exclusion_checks")
    required_checks = contract["exclusion_checks"]
    if not isinstance(checks, dict) or set(checks) != set(required_checks):
        raise ScreeningError(f"EXCLUSION_CHECK_SET_INVALID:{wid}")
    if any(not isinstance(checks[key], bool) for key in required_checks):
        raise ScreeningError(f"EXCLUSION_CHECK_VALUE_INVALID:{wid}")

    claims = record.get("claims")
    if not isinstance(claims, list):
        raise ScreeningError(f"ELIGIBILITY_CLAIMS_INVALID:{wid}")
    for claim in claims:
        if not isinstance(claim, dict):
            raise ScreeningError(f"ELIGIBILITY_CLAIM_NOT_OBJECT:{wid}")
        validate_claim(claim, contract)

    decision = record.get("decision")
    if not isinstance(decision, dict):
        raise ScreeningError(f"ELIGIBILITY_DECISION_MISSING:{wid}")
    state = decision.get("state")
    allowed = set(contract["adjudicated_noncalibration_states"])
    if state not in allowed:
        raise ScreeningError(f"ELIGIBILITY_DECISION_STATE_INVALID:{wid}:{state}")
    reasons = decision.get("reason_codes")
    if not isinstance(reasons, list) or any(not isinstance(x, str) or not x for x in reasons):
        raise ScreeningError(f"ELIGIBILITY_REASON_CODES_INVALID:{wid}")

    if access == "INACCESSIBLE" and state != "SOURCE_INACCESSIBLE":
        raise ScreeningError(f"INACCESSIBLE_SOURCE_MUST_BE_SOURCE_INACCESSIBLE:{wid}")
    if state == "SOURCE_INACCESSIBLE" and access != "INACCESSIBLE":
        raise ScreeningError(f"SOURCE_INACCESSIBLE_REQUIRES_INACCESSIBLE_ACCESS:{wid}")

    if state == "INCLUDE":
        if access == "INACCESSIBLE":
            raise ScreeningError(f"INCLUDE_WITH_INACCESSIBLE_SOURCE:{wid}")
        if any(checks.values()):
            raise ScreeningError(f"INCLUDE_WITH_ACTIVE_EXCLUSION_CHECK:{wid}")
        qualifying = [
            claim
            for claim in claims
            if claim.get("route") in set(contract["claim_routes"])
            and claim.get("generalization") == "YES"
            and claim.get("construct_level_relevance") == "YES"
            and isinstance(claim.get("operational_roles"), list)
            and len(claim["operational_roles"]) >= 1
        ]
        if not qualifying:
            raise ScreeningError(f"INCLUDE_WITHOUT_V1_1_QUALIFYING_CLAIM:{wid}")

    if state == "EXCLUDE":
        if not any(checks.values()):
            raise ScreeningError(f"EXCLUDE_WITHOUT_ACTIVE_EXCLUSION_CHECK:{wid}")
        if not reasons:
            raise ScreeningError(f"EXCLUDE_WITHOUT_REASON_CODE:{wid}")

    return state


def validate_adjudication_bundle(
    bundle: dict[str, Any],
    *,
    era: str,
    ranked_sha256: str,
) -> list[dict[str, Any]]:
    if bundle.get("schema_version") != ADJUDICATION_SCHEMA:
        raise ScreeningError("ADJUDICATION_BUNDLE_SCHEMA_MISMATCH")
    if bundle.get("era") != era:
        raise ScreeningError("ADJUDICATION_BUNDLE_ERA_MISMATCH")
    if bundle.get("ranked_artifact_sha256") != ranked_sha256:
        raise ScreeningError("ADJUDICATION_BUNDLE_RANKED_HASH_MISMATCH")
    records = bundle.get("records")
    if not isinstance(records, list):
        raise ScreeningError("ADJUDICATION_BUNDLE_RECORDS_MISSING")
    seen: set[str] = set()
    seen_ranks: set[int] = set()
    for record in records:
        if not isinstance(record, dict):
            raise ScreeningError("ADJUDICATION_RECORD_NOT_OBJECT")
        wid = record.get("provider_work_id")
        rank = record.get("rank")
        if not isinstance(wid, str) or not wid:
            raise ScreeningError("ADJUDICATION_RECORD_WORK_ID_INVALID")
        if not isinstance(rank, int) or rank < 1:
            raise ScreeningError(f"ADJUDICATION_RECORD_RANK_INVALID:{wid}")
        if wid in seen:
            raise ScreeningError(f"DUPLICATE_ADJUDICATION_WORK_ID:{wid}")
        if rank in seen_ranks:
            raise ScreeningError(f"DUPLICATE_ADJUDICATION_RANK:{rank}")
        seen.add(wid)
        seen_ranks.add(rank)
    return records


def freeze_era_from_objects(
    *,
    ladder: dict[str, Any],
    adjudication_bundle: dict[str, Any],
    era: str,
    ranked_sha256: str,
    ranked_index_sha256: str,
    adjudication_bundle_sha256: str,
    contract: dict[str, Any],
    quota_override: int | None = None,
) -> dict[str, Any]:
    rows = validate_ladder(ladder, era=era, contract=contract)
    quota = (
        int(quota_override)
        if quota_override is not None
        else int(contract["frozen_quotas"][era])
    )
    records = validate_adjudication_bundle(
        adjudication_bundle, era=era, ranked_sha256=ranked_sha256
    )
    by_id = {record["provider_work_id"]: record for record in records}

    selected: list[str] = []
    selected_ranks: list[int] = []
    ledger: list[dict[str, Any]] = []
    consumed_adjudications: set[str] = set()
    terminal_rank: int | None = None

    for row in rows:
        wid = row["provider_work_id"]
        rank = int(row["rank"])
        calibration = row.get("screening_state") == "CALIBRATION_EXCLUDED"

        if len(selected) >= quota:
            if calibration:
                state = "CALIBRATION_EXCLUDED"
            else:
                state = "UNSCREENED_AFTER_QUOTA"
                if wid in by_id:
                    raise ScreeningError(f"POST_QUOTA_ADJUDICATION_FORBIDDEN:{wid}")
            ledger.append(
                {
                    "rank": rank,
                    "provider_work_id": wid,
                    "screening_state": state,
                }
            )
            continue

        if calibration:
            if wid in by_id:
                raise ScreeningError(f"CALIBRATION_ROW_MUST_NOT_BE_ADJUDICATED:{wid}")
            state = "CALIBRATION_EXCLUDED"
        else:
            record = by_id.get(wid)
            if record is None:
                raise ScreeningError(f"SCREENING_HOLE_BEFORE_QUOTA:{wid}:rank={rank}")
            state = validate_adjudication(
                record,
                row=row,
                era=era,
                ranked_sha256=ranked_sha256,
                contract=contract,
            )
            consumed_adjudications.add(wid)
            if state == "INCLUDE":
                selected.append(wid)
                selected_ranks.append(rank)
                if len(selected) == quota:
                    terminal_rank = rank

        ledger_item = {
            "rank": rank,
            "provider_work_id": wid,
            "screening_state": state,
        }
        if not calibration:
            record = by_id.get(wid)
            if record is not None and wid in consumed_adjudications:
                ledger_item["adjudication_record_sha256"] = sha256_json(record)
        ledger.append(ledger_item)

    unused = sorted(set(by_id) - consumed_adjudications)
    if unused:
        raise ScreeningError(f"UNUSED_OR_POST_TERMINAL_ADJUDICATIONS:{','.join(unused)}")
    if len(selected) < quota:
        raise ScreeningError(
            f"LADDER_EXHAUSTED_BEFORE_QUOTA:{era}:{len(selected)}<{quota}"
        )
    if terminal_rank is None:
        raise ScreeningError("INTERNAL_TERMINAL_RANK_MISSING")

    counts = {state: 0 for state in contract["screening_states"]}
    for item in ledger:
        counts[item["screening_state"]] += 1

    if counts["INCLUDE"] != quota:
        raise ScreeningError("ERA_INCLUDE_COUNT_MISMATCH")
    if selected_ranks != sorted(selected_ranks):
        raise ScreeningError("SELECTED_RANK_ORDER_VIOLATION")
    if len(set(selected)) != len(selected):
        raise ScreeningError("DUPLICATE_SELECTED_WORK_WITHIN_ERA")

    return {
        "schema_version": ERA_SCHEMA,
        "owner_issue": 212,
        "eligibility_schema": "paper2-eligibility-v1.1",
        "sampling_schema": "paper2-sampling-v2",
        "era": era,
        "ranked_artifact_sha256": ranked_sha256,
        "ranked_index_sha256": ranked_index_sha256,
        "adjudication_bundle_sha256": adjudication_bundle_sha256,
        "ranked_artifact_schema": ladder["schema_version"],
        "quota_k_d": quota,
        "frozen_ladder_row_count": len(rows),
        "rows_screened_through_terminal_rank": terminal_rank,
        "terminal_rank": terminal_rank,
        "selected_count": len(selected),
        "selected_provider_work_ids": selected,
        "selected_ranks": selected_ranks,
        "screening_counts": counts,
        "post_freeze_replacement_limit": 0,
        "screening_ledger": ledger,
        "classification": "ERA_PRIMARY_WORK_SELECTION_FROZEN",
        "architecture_consequence": "NONE",
    }


def freeze_corpus_from_era_artifacts(
    artifacts: list[dict[str, Any]],
    *,
    contract: dict[str, Any],
) -> dict[str, Any]:
    era_order = contract["frozen_era_order"]
    by_era: dict[str, dict[str, Any]] = {}
    for artifact in artifacts:
        if artifact.get("schema_version") != ERA_SCHEMA:
            raise ScreeningError("ERA_SELECTION_SCHEMA_MISMATCH")
        era = artifact.get("era")
        if era not in era_order:
            raise ScreeningError(f"UNKNOWN_ERA_SELECTION_ARTIFACT:{era}")
        if era in by_era:
            raise ScreeningError(f"DUPLICATE_ERA_SELECTION_ARTIFACT:{era}")
        by_era[era] = artifact
    if set(by_era) != set(era_order):
        missing = sorted(set(era_order) - set(by_era))
        raise ScreeningError(f"ERA_SELECTION_SET_INCOMPLETE:{missing}")

    selected_global: list[dict[str, Any]] = []
    seen_work_ids: set[str] = set()
    era_summaries: list[dict[str, Any]] = []
    for era in era_order:
        artifact = by_era[era]
        quota = int(contract["frozen_quotas"][era])
        selected = artifact.get("selected_provider_work_ids")
        ranks = artifact.get("selected_ranks")
        if artifact.get("quota_k_d") != quota:
            raise ScreeningError(f"ERA_QUOTA_DRIFT:{era}")
        if artifact.get("selected_count") != quota:
            raise ScreeningError(f"ERA_SELECTED_COUNT_MISMATCH:{era}")
        if not isinstance(selected, list) or len(selected) != quota:
            raise ScreeningError(f"ERA_SELECTED_ID_LIST_INVALID:{era}")
        if not isinstance(ranks, list) or len(ranks) != quota or ranks != sorted(ranks):
            raise ScreeningError(f"ERA_SELECTED_RANKS_INVALID:{era}")
        ledger = artifact.get("screening_ledger")
        if not isinstance(ledger, list):
            raise ScreeningError(f"ERA_LEDGER_MISSING:{era}")
        state_by_id = {
            item.get("provider_work_id"): item.get("screening_state")
            for item in ledger
            if isinstance(item, dict)
        }
        for wid, rank in zip(selected, ranks):
            if state_by_id.get(wid) != "INCLUDE":
                raise ScreeningError(f"SELECTED_WORK_NOT_INCLUDE:{era}:{wid}")
            if wid in seen_work_ids:
                raise ScreeningError(f"DUPLICATE_SELECTED_WORK_ACROSS_ERAS:{wid}")
            seen_work_ids.add(wid)
            selected_global.append(
                {
                    "era": era,
                    "rank": rank,
                    "provider_work_id": wid,
                }
            )
        era_summaries.append(
            {
                "era": era,
                "quota_k_d": quota,
                "terminal_rank": artifact.get("terminal_rank"),
                "selected_count": quota,
                "ranked_artifact_sha256": artifact.get("ranked_artifact_sha256"),
                "ranked_index_sha256": artifact.get("ranked_index_sha256"),
                "adjudication_bundle_sha256": artifact.get(
                    "adjudication_bundle_sha256"
                ),
                "screening_counts": artifact.get("screening_counts"),
            }
        )

    if len(selected_global) != int(contract["total_primary_work_target"]):
        raise ScreeningError(
            f"PRIMARY_CORPUS_TOTAL_MISMATCH:{len(selected_global)}"
        )

    return {
        "schema_version": CORPUS_SCHEMA,
        "owner_issue": 212,
        "eligibility_schema": "paper2-eligibility-v1.1",
        "sampling_schema": "paper2-sampling-v2",
        "total_selected_works": len(selected_global),
        "frozen_era_order": era_order,
        "era_summaries": era_summaries,
        "selected_works": selected_global,
        "post_freeze_replacement_limit": 0,
        "classification": "PAPER2_PRIMARY_1000_WORK_CORPUS_FROZEN",
        "architecture_consequence": "NONE",
    }


def synthetic_row(rank: int, wid: str, state: str = "UNSCREENED") -> dict[str, Any]:
    return {
        "rank": rank,
        "provider_work_id": wid,
        "screening_state": state,
    }


def synthetic_record(
    wid: str,
    rank: int,
    *,
    era: str,
    ranked_sha256: str,
    state: str,
    access: str = "FULL_TEXT",
    forbidden: bool = False,
) -> dict[str, Any]:
    checks = {
        "task_use_only": False,
        "covariate_or_score_only": False,
        "local_association_only": False,
        "applied_outcome_only": False,
        "implementation_only_no_general_claim": False,
        "terminology_match_only": False,
        "pure_formalism_without_functional_capacity_claim": False,
        "no_inspectable_claim": False,
    }
    claims: list[dict[str, Any]] = []
    reasons: list[str] = []
    if state == "INCLUDE":
        claims = [
            {
                "claim_id": f"{wid}-c1",
                "source_locator": "synthetic:1",
                "source_excerpt_hash": "a" * 64,
                "route": "A_EXPLICIT_COGNITIVE_CAPACITY",
                "generalization": "YES",
                "operational_roles": ["CONTEXT"],
                "construct_level_relevance": "YES",
            }
        ]
    elif state == "EXCLUDE":
        checks["task_use_only"] = True
        reasons = ["X1_TASK_USE_ONLY"]
    elif state == "SOURCE_INACCESSIBLE":
        access = "INACCESSIBLE"
        reasons = ["SOURCE_INACCESSIBLE"]
    elif state == "ELIGIBILITY_UNCERTAIN":
        reasons = ["INSUFFICIENT_SOURCE_GROUNDING"]

    record: dict[str, Any] = {
        "provider_work_id": wid,
        "era": era,
        "rank": rank,
        "ranked_artifact_sha256": ranked_sha256,
        "source_access": {"status": access, "version": "synthetic-v1"},
        "claims": claims,
        "exclusion_checks": checks,
        "decision": {"state": state, "reason_codes": reasons},
        "classifier_version": "paper2-eligibility-v1.1",
        "adjudication_version": "synthetic-v1",
    }
    if forbidden:
        record["analysis"] = {"basis_mapping": ["forbidden"]}
    return record


def expect_error(fn, contains: str) -> None:
    try:
        fn()
    except ScreeningError as exc:
        if contains not in str(exc):
            raise AssertionError(f"expected {contains!r}, got {exc!r}") from exc
    else:
        raise AssertionError(f"expected ScreeningError containing {contains!r}")


def self_test() -> None:
    contract = load_contract()
    assert contract["real_source_acquisition_authorized"] is False
    assert contract["real_eligibility_adjudication_authorized"] is False
    assert contract["real_primary_corpus_freeze_authorized"] is False
    era = "PRE_1950"
    ranked_sha = "1" * 64
    index_sha = "2" * 64

    rows = [
        synthetic_row(1, "W-CAL", "CALIBRATION_EXCLUDED"),
        synthetic_row(2, "W-EX"),
        synthetic_row(3, "W-IN-1"),
        synthetic_row(4, "W-UN"),
        synthetic_row(5, "W-SRC"),
        synthetic_row(6, "W-IN-2"),
        synthetic_row(7, "W-LATE"),
    ]
    ladder = {
        "schema_version": "paper2-sampling-v2-ranked-era-sourcewise-v6",
        "era": era,
        "global_boundary_tie_closed": True,
        "merge_provider_calls": 0,
        "frozen_row_count": len(rows),
        "rows": rows,
    }
    records = [
        synthetic_record("W-EX", 2, era=era, ranked_sha256=ranked_sha, state="EXCLUDE"),
        synthetic_record("W-IN-1", 3, era=era, ranked_sha256=ranked_sha, state="INCLUDE"),
        synthetic_record(
            "W-UN", 4, era=era, ranked_sha256=ranked_sha,
            state="ELIGIBILITY_UNCERTAIN", access="ABSTRACT_ONLY"
        ),
        synthetic_record(
            "W-SRC", 5, era=era, ranked_sha256=ranked_sha,
            state="SOURCE_INACCESSIBLE"
        ),
        synthetic_record("W-IN-2", 6, era=era, ranked_sha256=ranked_sha, state="INCLUDE"),
    ]
    bundle = {
        "schema_version": ADJUDICATION_SCHEMA,
        "era": era,
        "ranked_artifact_sha256": ranked_sha,
        "records": records,
    }
    frozen = freeze_era_from_objects(
        ladder=ladder,
        adjudication_bundle=bundle,
        era=era,
        ranked_sha256=ranked_sha,
        ranked_index_sha256=index_sha,
        adjudication_bundle_sha256="5" * 64,
        contract=contract,
        quota_override=2,
    )
    assert frozen["selected_provider_work_ids"] == ["W-IN-1", "W-IN-2"]
    assert frozen["selected_ranks"] == [3, 6]
    assert frozen["terminal_rank"] == 6
    assert frozen["screening_counts"]["CALIBRATION_EXCLUDED"] == 1
    assert frozen["screening_counts"]["EXCLUDE"] == 1
    assert frozen["screening_counts"]["ELIGIBILITY_UNCERTAIN"] == 1
    assert frozen["screening_counts"]["SOURCE_INACCESSIBLE"] == 1
    assert frozen["screening_counts"]["INCLUDE"] == 2
    assert frozen["screening_counts"]["UNSCREENED_AFTER_QUOTA"] == 1
    assert frozen["screening_ledger"][-1]["screening_state"] == "UNSCREENED_AFTER_QUOTA"

    post_bundle = json.loads(json.dumps(bundle))
    post_bundle["records"].append(
        synthetic_record(
            "W-LATE", 7, era=era, ranked_sha256=ranked_sha, state="INCLUDE"
        )
    )
    expect_error(
        lambda: freeze_era_from_objects(
            ladder=ladder,
            adjudication_bundle=post_bundle,
            era=era,
            ranked_sha256=ranked_sha,
            ranked_index_sha256=index_sha,
            adjudication_bundle_sha256="5" * 64,
            contract=contract,
            quota_override=2,
        ),
        "POST_QUOTA_ADJUDICATION_FORBIDDEN",
    )

    hole_bundle = json.loads(json.dumps(bundle))
    hole_bundle["records"] = [
        record for record in hole_bundle["records"]
        if record["provider_work_id"] != "W-UN"
    ]
    expect_error(
        lambda: freeze_era_from_objects(
            ladder=ladder,
            adjudication_bundle=hole_bundle,
            era=era,
            ranked_sha256=ranked_sha,
            ranked_index_sha256=index_sha,
            adjudication_bundle_sha256="5" * 64,
            contract=contract,
            quota_override=2,
        ),
        "SCREENING_HOLE_BEFORE_QUOTA",
    )

    short_rows = [synthetic_row(1, "W-ONLY")]
    short_ladder = {
        "schema_version": "paper2-sampling-v2-ranked-era-sourcewise-v6",
        "era": era,
        "global_boundary_tie_closed": True,
        "merge_provider_calls": 0,
        "frozen_row_count": 1,
        "rows": short_rows,
    }
    short_bundle = {
        "schema_version": ADJUDICATION_SCHEMA,
        "era": era,
        "ranked_artifact_sha256": ranked_sha,
        "records": [
            synthetic_record(
                "W-ONLY", 1, era=era, ranked_sha256=ranked_sha, state="INCLUDE"
            )
        ],
    }
    expect_error(
        lambda: freeze_era_from_objects(
            ladder=short_ladder,
            adjudication_bundle=short_bundle,
            era=era,
            ranked_sha256=ranked_sha,
            ranked_index_sha256=index_sha,
            adjudication_bundle_sha256="5" * 64,
            contract=contract,
            quota_override=2,
        ),
        "LADDER_EXHAUSTED_BEFORE_QUOTA",
    )

    forbidden_record = synthetic_record(
        "W-FORBID", 1, era=era, ranked_sha256=ranked_sha,
        state="INCLUDE", forbidden=True
    )
    expect_error(
        lambda: validate_adjudication(
            forbidden_record,
            row=synthetic_row(1, "W-FORBID"),
            era=era,
            ranked_sha256=ranked_sha,
            contract=contract,
        ),
        "FORBIDDEN_ELIGIBILITY_FIELD",
    )

    out_of_order = json.loads(json.dumps(ladder))
    out_of_order["rows"][1], out_of_order["rows"][2] = (
        out_of_order["rows"][2],
        out_of_order["rows"][1],
    )
    expect_error(
        lambda: validate_ladder(out_of_order, era=era, contract=contract),
        "RANK_SEQUENCE_INVALID",
    )

    corpus_artifacts: list[dict[str, Any]] = []
    global_counter = 0
    for era_name in contract["frozen_era_order"]:
        quota = int(contract["frozen_quotas"][era_name])
        ids = []
        ranks = []
        ledger = []
        for rank in range(1, quota + 1):
            global_counter += 1
            wid = f"W-SYN-{global_counter:04d}"
            ids.append(wid)
            ranks.append(rank)
            ledger.append(
                {
                    "rank": rank,
                    "provider_work_id": wid,
                    "screening_state": "INCLUDE",
                }
            )
        corpus_artifacts.append(
            {
                "schema_version": ERA_SCHEMA,
                "era": era_name,
                "quota_k_d": quota,
                "selected_count": quota,
                "selected_provider_work_ids": ids,
                "selected_ranks": ranks,
                "screening_ledger": ledger,
                "terminal_rank": quota,
                "ranked_artifact_sha256": "3" * 64,
                "ranked_index_sha256": "4" * 64,
                "adjudication_bundle_sha256": "5" * 64,
                "screening_counts": {"INCLUDE": quota},
            }
        )
    corpus = freeze_corpus_from_era_artifacts(corpus_artifacts, contract=contract)
    assert corpus["total_selected_works"] == 1000
    assert len(corpus["selected_works"]) == 1000
    assert corpus["classification"] == "PAPER2_PRIMARY_1000_WORK_CORPUS_FROZEN"

    duplicated = json.loads(json.dumps(corpus_artifacts))
    duplicated[1]["selected_provider_work_ids"][0] = (
        duplicated[0]["selected_provider_work_ids"][0]
    )
    duplicated[1]["screening_ledger"][0]["provider_work_id"] = (
        duplicated[0]["selected_provider_work_ids"][0]
    )
    expect_error(
        lambda: freeze_corpus_from_era_artifacts(duplicated, contract=contract),
        "DUPLICATE_SELECTED_WORK_ACROSS_ERAS",
    )

    assert contract["retained_downstream_safeguards"]["max_selected_claims_per_work"] == 3
    assert contract["retained_downstream_safeguards"]["cluster_bootstrap_replicates"] == 2000
    assert contract["retained_downstream_safeguards"]["null_permutations"] == 100
    print("PAPER2_ELIGIBILITY_SCREENING_APPARATUS_SELFTEST_PASS")


def require_real_authority(contract: dict[str, Any]) -> None:
    if (
        contract.get("real_eligibility_adjudication_authorized") is not True
        or contract.get("real_primary_corpus_freeze_authorized") is not True
    ):
        raise ScreeningError("REAL_ELIGIBILITY_SCREENING_NOT_AUTHORIZED")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--freeze-era", action="store_true")
    parser.add_argument("--freeze-corpus", action="store_true")
    parser.add_argument("--era")
    parser.add_argument("--ladder", type=Path)
    parser.add_argument("--index", type=Path)
    parser.add_argument("--adjudications", type=Path)
    parser.add_argument("--era-artifact", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    contract = load_contract(args.contract)
    if args.self_test:
        self_test()
        return 0

    require_real_authority(contract)

    if args.freeze_era:
        if args.freeze_corpus:
            raise ScreeningError("CHOOSE_ONE_FREEZE_OPERATION")
        if not args.era or args.era not in contract["frozen_era_order"]:
            raise ScreeningError("VALID_FROZEN_ERA_REQUIRED")
        if args.ladder is None or args.index is None or args.adjudications is None:
            raise ScreeningError("FREEZE_ERA_INPUTS_MISSING")
        if args.output is None:
            raise ScreeningError("OUTPUT_REQUIRED")
        ladder = load_json(args.ladder)
        ranked_sha = sha256_file(args.ladder)
        index_sha = sha256_file(args.index)
        bundle = load_json(args.adjudications)
        bundle_sha = sha256_file(args.adjudications)
        result = freeze_era_from_objects(
            ladder=ladder,
            adjudication_bundle=bundle,
            era=args.era,
            ranked_sha256=ranked_sha,
            ranked_index_sha256=index_sha,
            adjudication_bundle_sha256=bundle_sha,
            contract=contract,
        )
        write_json_atomic(args.output, result)
        return 0

    if args.freeze_corpus:
        if args.output is None:
            raise ScreeningError("OUTPUT_REQUIRED")
        if len(args.era_artifact) != len(contract["frozen_era_order"]):
            raise ScreeningError("NINE_ERA_ARTIFACTS_REQUIRED")
        artifacts = [load_json(path) for path in args.era_artifact]
        result = freeze_corpus_from_era_artifacts(artifacts, contract=contract)
        write_json_atomic(args.output, result)
        return 0

    parser.error("choose --self-test, --freeze-era, or --freeze-corpus")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
