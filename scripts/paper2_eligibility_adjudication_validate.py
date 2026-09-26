#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

PROCEDURE_PATH = Path("research/paper2/eligibility_adjudication_v1.json")
PROMPT_PATH = Path("research/paper2/eligibility_adjudication_prompt_v1.md")
SOURCE_SCHEMA = "paper2-eligibility-source-bundle-v1"
DECISION_SCHEMA = "paper2-eligibility-decision-v1"

ROUTES = {
    "A_EXPLICIT_COGNITIVE_CAPACITY",
    "B_GENERAL_ADAPTIVE_INFORMATION_PROCESSING",
}
ROLES = {
    "CONTEXT",
    "INPUT_OR_INTERVENTION",
    "INFORMATION_OR_REPRESENTATION",
    "INTERNAL_OR_RELATIONAL_STRUCTURE",
    "RESPONSE_OR_OUTPUT",
    "CRITERION_OR_COMPARISON",
    "DEPENDENCY_OR_SENSITIVITY",
    "TIME_OR_HORIZON",
}
CHECKS = (
    "task_use_only",
    "covariate_or_score_only",
    "local_association_only",
    "applied_outcome_only",
    "implementation_only_no_general_claim",
    "terminology_match_only",
    "pure_formalism_without_functional_capacity_claim",
    "no_inspectable_claim",
)
DECISIONS = {"INCLUDE", "EXCLUDE", "ELIGIBILITY_UNCERTAIN"}


class AdjudicationError(RuntimeError):
    pass


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_json(value: Any) -> str:
    return sha256_bytes(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )


def normalized_key(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def reject_forbidden_keys(value: Any, forbidden: set[str], path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            norm = normalized_key(str(key))
            if norm in forbidden:
                raise AdjudicationError(f"FORBIDDEN_CLASSIFIER_FIELD:{path}.{key}")
            reject_forbidden_keys(child, forbidden, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_forbidden_keys(child, forbidden, f"{path}[{index}]")


def load_procedure(path: Path = PROCEDURE_PATH) -> dict[str, Any]:
    procedure = load_json(path)
    if procedure.get("schema_version") != "paper2-eligibility-adjudication-procedure-v1":
        raise AdjudicationError("PROCEDURE_SCHEMA_MISMATCH")
    if procedure.get("owner_issue") != 214:
        raise AdjudicationError("PROCEDURE_OWNER_DRIFT")
    if procedure.get("parent_screening_issue") != 212:
        raise AdjudicationError("PARENT_SCREENING_OWNER_DRIFT")
    if procedure.get("eligibility_schema") != "paper2-eligibility-v1.1":
        raise AdjudicationError("ELIGIBILITY_SCHEMA_DRIFT")
    if procedure.get("source_bundle_schema") != SOURCE_SCHEMA:
        raise AdjudicationError("SOURCE_BUNDLE_SCHEMA_DRIFT")
    if procedure.get("decision_schema") != DECISION_SCHEMA:
        raise AdjudicationError("DECISION_SCHEMA_DRIFT")
    if procedure.get("passes") != ["A", "B"]:
        raise AdjudicationError("PASS_SET_DRIFT")
    prompt = procedure.get("prompt")
    if not isinstance(prompt, dict):
        raise AdjudicationError("PROMPT_AUTHORITY_MISSING")
    if prompt.get("path") != str(PROMPT_PATH):
        raise AdjudicationError("PROMPT_PATH_DRIFT")
    if prompt.get("sha256_utf8") != sha256_file(PROMPT_PATH):
        raise AdjudicationError("PROMPT_SHA256_DRIFT")
    for field in (
        "real_source_acquisition_authorized",
        "real_model_execution_authorized",
        "real_adjudication_authorized",
    ):
        if not isinstance(procedure.get(field), bool):
            raise AdjudicationError(f"AUTHORITY_FIELD_INVALID:{field}")
    if procedure.get("architecture_consequence") != "NONE":
        raise AdjudicationError("ARCHITECTURE_CONSEQUENCE_DRIFT")
    return procedure


def validate_source_bundle(bundle: dict[str, Any]) -> None:
    if set(bundle) != {
        "schema_version",
        "bundle_id",
        "source_language",
        "source_access_status",
        "source_spans",
    }:
        raise AdjudicationError("SOURCE_BUNDLE_FIELD_SET_INVALID")
    if bundle.get("schema_version") != SOURCE_SCHEMA:
        raise AdjudicationError("SOURCE_BUNDLE_SCHEMA_MISMATCH")
    bundle_id = bundle.get("bundle_id")
    if (
        not isinstance(bundle_id, str)
        or len(bundle_id) != 5
        or bundle_id[0] != "E"
        or not bundle_id[1:].isdigit()
    ):
        raise AdjudicationError("SOURCE_BUNDLE_ID_INVALID")
    language = bundle.get("source_language")
    if not isinstance(language, str) or len(language.strip()) < 2:
        raise AdjudicationError("SOURCE_LANGUAGE_INVALID")
    if bundle.get("source_access_status") not in {
        "FULL_TEXT",
        "PARTIAL_TEXT",
        "ABSTRACT_ONLY",
    }:
        raise AdjudicationError("SOURCE_ACCESS_STATUS_INVALID")
    spans = bundle.get("source_spans")
    if not isinstance(spans, list) or not spans:
        raise AdjudicationError("SOURCE_SPANS_MISSING")
    seen: set[str] = set()
    for span in spans:
        if not isinstance(span, dict) or set(span) != {"span_id", "text"}:
            raise AdjudicationError("SOURCE_SPAN_FIELD_SET_INVALID")
        span_id = span.get("span_id")
        text = span.get("text")
        if (
            not isinstance(span_id, str)
            or len(span_id) < 2
            or span_id[0] != "s"
            or not span_id[1:].isdigit()
        ):
            raise AdjudicationError("SOURCE_SPAN_ID_INVALID")
        if span_id in seen:
            raise AdjudicationError(f"DUPLICATE_SOURCE_SPAN_ID:{span_id}")
        seen.add(span_id)
        if not isinstance(text, str) or not text.strip():
            raise AdjudicationError(f"SOURCE_SPAN_TEXT_INVALID:{span_id}")


def validate_claim(claim: dict[str, Any], valid_locators: set[str]) -> None:
    if set(claim) != {
        "claim_id",
        "source_locator",
        "route",
        "generalization",
        "operational_roles",
        "construct_level_relevance",
    }:
        raise AdjudicationError("DECISION_CLAIM_FIELD_SET_INVALID")
    if not isinstance(claim.get("claim_id"), str) or not claim["claim_id"]:
        raise AdjudicationError("DECISION_CLAIM_ID_INVALID")
    locator = claim.get("source_locator")
    if locator not in valid_locators:
        raise AdjudicationError(f"DECISION_SOURCE_LOCATOR_NOT_IN_BUNDLE:{locator}")
    if claim.get("route") not in ROUTES:
        raise AdjudicationError("DECISION_ROUTE_INVALID")
    if claim.get("generalization") not in {"YES", "NO", "UNCERTAIN"}:
        raise AdjudicationError("DECISION_GENERALIZATION_INVALID")
    if claim.get("construct_level_relevance") not in {"YES", "NO", "UNCERTAIN"}:
        raise AdjudicationError("DECISION_RELEVANCE_INVALID")
    roles = claim.get("operational_roles")
    if not isinstance(roles, list):
        raise AdjudicationError("DECISION_OPERATIONAL_ROLES_INVALID")
    if len(roles) != len(set(roles)) or any(role not in ROLES for role in roles):
        raise AdjudicationError("DECISION_OPERATIONAL_ROLE_INVALID")


def is_qualifying_claim(claim: dict[str, Any]) -> bool:
    return (
        claim.get("route") in ROUTES
        and claim.get("generalization") == "YES"
        and claim.get("construct_level_relevance") == "YES"
        and isinstance(claim.get("operational_roles"), list)
        and len(claim["operational_roles"]) >= 1
    )


def validate_decision(
    decision: dict[str, Any],
    *,
    bundle: dict[str, Any],
    procedure: dict[str, Any],
) -> None:
    forbidden = {
        normalized_key(name)
        for name in procedure["forbidden_key_names_recursive"]
    }
    reject_forbidden_keys(decision, forbidden)

    if set(decision) != {
        "schema_version",
        "bundle_id",
        "claims",
        "exclusion_checks",
        "decision",
    }:
        raise AdjudicationError("DECISION_FIELD_SET_INVALID")
    if decision.get("schema_version") != DECISION_SCHEMA:
        raise AdjudicationError("DECISION_SCHEMA_MISMATCH")
    if decision.get("bundle_id") != bundle.get("bundle_id"):
        raise AdjudicationError("DECISION_BUNDLE_ID_MISMATCH")

    valid_locators = {
        span["span_id"]
        for span in bundle["source_spans"]
    }
    claims = decision.get("claims")
    if not isinstance(claims, list):
        raise AdjudicationError("DECISION_CLAIMS_INVALID")
    claim_ids: set[str] = set()
    for claim in claims:
        if not isinstance(claim, dict):
            raise AdjudicationError("DECISION_CLAIM_NOT_OBJECT")
        validate_claim(claim, valid_locators)
        if claim["claim_id"] in claim_ids:
            raise AdjudicationError(f"DUPLICATE_DECISION_CLAIM_ID:{claim['claim_id']}")
        claim_ids.add(claim["claim_id"])

    checks = decision.get("exclusion_checks")
    if not isinstance(checks, dict) or set(checks) != set(CHECKS):
        raise AdjudicationError("DECISION_EXCLUSION_CHECK_SET_INVALID")
    if any(not isinstance(checks[name], bool) for name in CHECKS):
        raise AdjudicationError("DECISION_EXCLUSION_CHECK_VALUE_INVALID")

    decision_obj = decision.get("decision")
    if not isinstance(decision_obj, dict) or set(decision_obj) != {
        "state",
        "reason_codes",
    }:
        raise AdjudicationError("DECISION_RESULT_FIELD_SET_INVALID")
    state = decision_obj.get("state")
    if state not in DECISIONS:
        raise AdjudicationError("DECISION_STATE_INVALID")
    reasons = decision_obj.get("reason_codes")
    if (
        not isinstance(reasons, list)
        or any(not isinstance(reason, str) or not reason for reason in reasons)
    ):
        raise AdjudicationError("DECISION_REASON_CODES_INVALID")

    qualifying = [claim for claim in claims if is_qualifying_claim(claim)]
    if state == "INCLUDE":
        if any(checks.values()):
            raise AdjudicationError("INCLUDE_WITH_ACTIVE_EXCLUSION_CHECK")
        if not qualifying:
            raise AdjudicationError("INCLUDE_WITHOUT_QUALIFYING_CLAIM")
    elif state == "EXCLUDE":
        if not any(checks.values()):
            raise AdjudicationError("EXCLUDE_WITHOUT_ACTIVE_EXCLUSION_CHECK")
        if not reasons:
            raise AdjudicationError("EXCLUDE_WITHOUT_REASON_CODE")


def claim_signature(claim: dict[str, Any]) -> tuple[Any, ...]:
    return (
        claim["route"],
        claim["generalization"],
        claim["construct_level_relevance"],
        tuple(sorted(claim["operational_roles"])),
        claim["source_locator"],
    )


def agreement_projection(decision: dict[str, Any]) -> dict[str, Any]:
    claims = sorted(
        [claim_signature(claim) for claim in decision["claims"]],
        key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True),
    )
    active_checks = sorted(
        key for key, value in decision["exclusion_checks"].items() if value
    )
    return {
        "decision_state": decision["decision"]["state"],
        "active_exclusion_checks": active_checks,
        "qualifying_claim_exists": any(
            is_qualifying_claim(claim)
            for claim in decision["claims"]
        ),
        "claim_signatures": claims,
    }


def compare_decisions(
    pass_a: dict[str, Any],
    pass_b: dict[str, Any],
    *,
    bundle: dict[str, Any],
    procedure: dict[str, Any],
) -> dict[str, Any]:
    validate_decision(pass_a, bundle=bundle, procedure=procedure)
    validate_decision(pass_b, bundle=bundle, procedure=procedure)
    projection_a = agreement_projection(pass_a)
    projection_b = agreement_projection(pass_b)
    agrees = projection_a == projection_b
    return {
        "schema_version": "paper2-eligibility-agreement-v1",
        "bundle_id": bundle["bundle_id"],
        "agreement": agrees,
        "classification": (
            "ELIGIBILITY_TWO_PASS_AGREEMENT"
            if agrees
            else "ELIGIBILITY_TWO_PASS_DISAGREEMENT"
        ),
        "projection_a": projection_a,
        "projection_b": projection_b,
        "adjudication_required": not agrees,
    }


def canonicalize_decision(decision: dict[str, Any]) -> dict[str, Any]:
    claims_sorted = sorted(
        decision["claims"],
        key=lambda claim: json.dumps(
            claim_signature(claim),
            ensure_ascii=False,
            sort_keys=True,
        ),
    )
    canonical_claims = []
    for index, claim in enumerate(claims_sorted, start=1):
        canonical_claims.append(
            {
                "claim_id": f"elig-{index:03d}",
                "source_locator": claim["source_locator"],
                "route": claim["route"],
                "generalization": claim["generalization"],
                "operational_roles": sorted(claim["operational_roles"]),
                "construct_level_relevance": claim[
                    "construct_level_relevance"
                ],
            }
        )
    return {
        "claims": canonical_claims,
        "exclusion_checks": {
            key: bool(decision["exclusion_checks"][key])
            for key in CHECKS
        },
        "decision": {
            "state": decision["decision"]["state"],
            "reason_codes": sorted(set(decision["decision"]["reason_codes"])),
        },
    }


def assemble_accessible_record(
    *,
    bundle: dict[str, Any],
    pass_a: dict[str, Any],
    pass_b: dict[str, Any],
    procedure: dict[str, Any],
    provider_work_id: str,
    era: str,
    rank: int,
    ranked_artifact_sha256: str,
    source_access_version: str,
    adjudication_version: str,
    adjudication: dict[str, Any] | None = None,
) -> dict[str, Any]:
    validate_source_bundle(bundle)
    comparison = compare_decisions(
        pass_a,
        pass_b,
        bundle=bundle,
        procedure=procedure,
    )

    if comparison["agreement"]:
        if adjudication is not None:
            raise AdjudicationError("ADJUDICATION_FORBIDDEN_WHEN_PASSES_AGREE")
        final_decision = pass_a
        adjudication_sha = None
        resolution = "TWO_PASS_AGREEMENT"
        reason_codes = sorted(
            set(pass_a["decision"]["reason_codes"])
            | set(pass_b["decision"]["reason_codes"])
        )
        final_decision = json.loads(json.dumps(final_decision))
        final_decision["decision"]["reason_codes"] = reason_codes
    else:
        if adjudication is None:
            raise AdjudicationError("ADJUDICATION_REQUIRED_FOR_DISAGREEMENT")
        validate_decision(adjudication, bundle=bundle, procedure=procedure)
        final_decision = adjudication
        adjudication_sha = sha256_json(adjudication)
        resolution = "SOURCE_TEXT_ONLY_ADJUDICATION"

    canonical = canonicalize_decision(final_decision)
    return {
        "provider_work_id": provider_work_id,
        "era": era,
        "rank": rank,
        "ranked_artifact_sha256": ranked_artifact_sha256,
        "source_access": {
            "status": bundle["source_access_status"],
            "version": source_access_version,
        },
        **canonical,
        "classifier_version": "paper2-eligibility-v1.1",
        "adjudication_version": adjudication_version,
        "source_bundle_sha256": sha256_json(bundle),
        "pass_a_sha256": sha256_json(pass_a),
        "pass_b_sha256": sha256_json(pass_b),
        "adjudication_sha256": adjudication_sha,
        "eligibility_resolution": resolution,
        "agreement_projection_sha256": sha256_json(comparison),
    }


def assemble_inaccessible_record(
    *,
    provider_work_id: str,
    era: str,
    rank: int,
    ranked_artifact_sha256: str,
    source_access_version: str,
    adjudication_version: str,
    acquisition_receipt_sha256: str,
) -> dict[str, Any]:
    if len(acquisition_receipt_sha256) != 64:
        raise AdjudicationError("ACQUISITION_RECEIPT_SHA256_INVALID")
    return {
        "provider_work_id": provider_work_id,
        "era": era,
        "rank": rank,
        "ranked_artifact_sha256": ranked_artifact_sha256,
        "source_access": {
            "status": "INACCESSIBLE",
            "version": source_access_version,
        },
        "claims": [],
        "exclusion_checks": {key: False for key in CHECKS},
        "decision": {
            "state": "SOURCE_INACCESSIBLE",
            "reason_codes": ["SOURCE_INACCESSIBLE"],
        },
        "classifier_version": "paper2-eligibility-v1.1",
        "adjudication_version": adjudication_version,
        "source_bundle_sha256": None,
        "pass_a_sha256": None,
        "pass_b_sha256": None,
        "adjudication_sha256": None,
        "acquisition_receipt_sha256": acquisition_receipt_sha256,
        "eligibility_resolution": "SOURCE_INACCESSIBLE_BYPASS",
    }


def synthetic_bundle() -> dict[str, Any]:
    return {
        "schema_version": SOURCE_SCHEMA,
        "bundle_id": "E0001",
        "source_language": "en",
        "source_access_status": "ABSTRACT_ONLY",
        "source_spans": [
            {
                "span_id": "s1",
                "text": "The source makes a general functional claim about a bounded system.",
            },
            {
                "span_id": "s2",
                "text": "A second span describes a measurable response.",
            },
        ],
    }


def blank_checks() -> dict[str, bool]:
    return {key: False for key in CHECKS}


def synthetic_include(
    *,
    bundle_id: str = "E0001",
    route: str = "A_EXPLICIT_COGNITIVE_CAPACITY",
    claim_order: tuple[str, ...] = ("s1",),
) -> dict[str, Any]:
    claims = []
    for index, locator in enumerate(claim_order, start=1):
        claims.append(
            {
                "claim_id": f"c{index}",
                "source_locator": locator,
                "route": route,
                "generalization": "YES",
                "operational_roles": ["CONTEXT", "RESPONSE_OR_OUTPUT"],
                "construct_level_relevance": "YES",
            }
        )
    return {
        "schema_version": DECISION_SCHEMA,
        "bundle_id": bundle_id,
        "claims": claims,
        "exclusion_checks": blank_checks(),
        "decision": {"state": "INCLUDE", "reason_codes": []},
    }


def synthetic_exclude(
    check: str,
    *,
    reason: str,
    bundle_id: str = "E0001",
) -> dict[str, Any]:
    checks = blank_checks()
    checks[check] = True
    return {
        "schema_version": DECISION_SCHEMA,
        "bundle_id": bundle_id,
        "claims": [],
        "exclusion_checks": checks,
        "decision": {"state": "EXCLUDE", "reason_codes": [reason]},
    }


def synthetic_uncertain(bundle_id: str = "E0001") -> dict[str, Any]:
    return {
        "schema_version": DECISION_SCHEMA,
        "bundle_id": bundle_id,
        "claims": [],
        "exclusion_checks": blank_checks(),
        "decision": {
            "state": "ELIGIBILITY_UNCERTAIN",
            "reason_codes": ["INSUFFICIENT_SOURCE_GROUNDING"],
        },
    }


def expect_error(fn, text: str) -> None:
    try:
        fn()
    except AdjudicationError as exc:
        if text not in str(exc):
            raise AssertionError(f"expected {text!r}, got {exc!r}") from exc
    else:
        raise AssertionError(f"expected error containing {text!r}")


def self_test() -> None:
    procedure = load_procedure()
    assert procedure["real_source_acquisition_authorized"] is False
    assert procedure["real_model_execution_authorized"] is False
    assert procedure["real_adjudication_authorized"] is False

    bundle = synthetic_bundle()
    validate_source_bundle(bundle)

    route_a = synthetic_include()
    validate_decision(route_a, bundle=bundle, procedure=procedure)

    route_b = synthetic_include(route="B_GENERAL_ADAPTIVE_INFORMATION_PROCESSING")
    validate_decision(route_b, bundle=bundle, procedure=procedure)

    task_only = synthetic_exclude(
        "task_use_only",
        reason="X1_TASK_USE_ONLY",
    )
    validate_decision(task_only, bundle=bundle, procedure=procedure)

    pure_formalism = synthetic_exclude(
        "pure_formalism_without_functional_capacity_claim",
        reason="PURE_FORMALISM_WITHOUT_FUNCTIONAL_CAPACITY_CLAIM",
    )
    validate_decision(pure_formalism, bundle=bundle, procedure=procedure)

    uncertain = synthetic_uncertain()
    validate_decision(uncertain, bundle=bundle, procedure=procedure)

    pass_a = synthetic_include(claim_order=("s1", "s2"))
    pass_b = synthetic_include(claim_order=("s2", "s1"))
    comparison = compare_decisions(
        pass_a,
        pass_b,
        bundle=bundle,
        procedure=procedure,
    )
    assert comparison["agreement"] is True
    assert comparison["adjudication_required"] is False

    assembled = assemble_accessible_record(
        bundle=bundle,
        pass_a=pass_a,
        pass_b=pass_b,
        procedure=procedure,
        provider_work_id="W-SYN-1",
        era="2020-2026",
        rank=1,
        ranked_artifact_sha256="a" * 64,
        source_access_version="synthetic-v1",
        adjudication_version="paper2-eligibility-adjudication-v1",
    )
    assert assembled["decision"]["state"] == "INCLUDE"
    assert assembled["eligibility_resolution"] == "TWO_PASS_AGREEMENT"
    assert assembled["adjudication_sha256"] is None
    assert [claim["source_locator"] for claim in assembled["claims"]] == ["s1", "s2"]

    disagreement = compare_decisions(
        pass_a,
        task_only,
        bundle=bundle,
        procedure=procedure,
    )
    assert disagreement["agreement"] is False
    assert disagreement["adjudication_required"] is True
    expect_error(
        lambda: assemble_accessible_record(
            bundle=bundle,
            pass_a=pass_a,
            pass_b=task_only,
            procedure=procedure,
            provider_work_id="W-SYN-2",
            era="2020-2026",
            rank=2,
            ranked_artifact_sha256="b" * 64,
            source_access_version="synthetic-v1",
            adjudication_version="paper2-eligibility-adjudication-v1",
        ),
        "ADJUDICATION_REQUIRED_FOR_DISAGREEMENT",
    )

    adjudicated = assemble_accessible_record(
        bundle=bundle,
        pass_a=pass_a,
        pass_b=task_only,
        adjudication=uncertain,
        procedure=procedure,
        provider_work_id="W-SYN-2",
        era="2020-2026",
        rank=2,
        ranked_artifact_sha256="b" * 64,
        source_access_version="synthetic-v1",
        adjudication_version="paper2-eligibility-adjudication-v1",
    )
    assert adjudicated["decision"]["state"] == "ELIGIBILITY_UNCERTAIN"
    assert adjudicated["eligibility_resolution"] == "SOURCE_TEXT_ONLY_ADJUDICATION"
    assert isinstance(adjudicated["adjudication_sha256"], str)

    inaccessible = assemble_inaccessible_record(
        provider_work_id="W-SYN-3",
        era="2020-2026",
        rank=3,
        ranked_artifact_sha256="c" * 64,
        source_access_version="synthetic-v1",
        adjudication_version="paper2-eligibility-adjudication-v1",
        acquisition_receipt_sha256="d" * 64,
    )
    assert inaccessible["decision"]["state"] == "SOURCE_INACCESSIBLE"
    assert inaccessible["eligibility_resolution"] == "SOURCE_INACCESSIBLE_BYPASS"
    assert inaccessible["pass_a_sha256"] is None

    forbidden = synthetic_include()
    forbidden["basis_mapping"] = ["forbidden"]
    expect_error(
        lambda: validate_decision(
            forbidden,
            bundle=bundle,
            procedure=procedure,
        ),
        "FORBIDDEN_CLASSIFIER_FIELD",
    )

    bad_source = json.loads(json.dumps(bundle))
    bad_source["rank"] = 1
    expect_error(lambda: validate_source_bundle(bad_source), "SOURCE_BUNDLE_FIELD_SET_INVALID")

    print("PAPER2_ELIGIBILITY_ADJUDICATION_APPARATUS_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--procedure", type=Path, default=PROCEDURE_PATH)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--source-bundle", type=Path)
    parser.add_argument("--pass-a", type=Path)
    parser.add_argument("--pass-b", type=Path)
    parser.add_argument("--adjudication", type=Path)
    parser.add_argument("--compare", action="store_true")
    args = parser.parse_args()

    procedure = load_procedure(args.procedure)
    if args.self_test:
        self_test()
        return 0

    if procedure.get("real_model_execution_authorized") is not True:
        raise AdjudicationError("REAL_ELIGIBILITY_MODEL_EXECUTION_NOT_AUTHORIZED")

    if args.compare:
        if args.source_bundle is None or args.pass_a is None or args.pass_b is None:
            raise AdjudicationError("COMPARE_INPUTS_MISSING")
        bundle = load_json(args.source_bundle)
        pass_a = load_json(args.pass_a)
        pass_b = load_json(args.pass_b)
        validate_source_bundle(bundle)
        result = compare_decisions(
            pass_a,
            pass_b,
            bundle=bundle,
            procedure=procedure,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    parser.error("choose --self-test or --compare")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
