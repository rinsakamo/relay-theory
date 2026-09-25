#!/usr/bin/env python3
"""Validate the Paper 2 bundle-level EXTRACTION_ABSTAIN v2 interface.

Owner: #191.

This module is synthetic/static protocol infrastructure only.  It does not
authorize or execute real-paper model calls, and it does not modify ClaimIR v1
or SystemOne decision v2.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from paper2_extraction_procedure_validate import ContractError
from paper2_claim_ir_validate import ValidationError
from paper2_extraction_two_pass_systemone_v2 import (
    DecisionUnresolved,
    TwoPassV2Error,
    UNRESOLVED,
    build_systemone_request,
    compile_candidate,
    decision_from_answers,
    parse_systemone_response,
    relation_answers,
    response_for,
    synthetic_source,
)


CONTRACT_VERSION = "paper2-extraction-abstention-v2"
EXPECTED_BUNDLE_OUTCOMES = {
    "VALID_CLAIM_IR",
    "EXTRACTION_ABSTAIN",
    "EXTRACTION_FAILURE",
}
EXPECTED_TRANSACTION_FAILURES = {
    "TRANSACTION_TRANSPORT_FAILURE",
    "TRANSACTION_RESPONSE_CONTRACT_FAILURE",
    "TRANSACTION_RUNTIME_FAILURE",
    "TRANSACTION_CLEANUP_FAILURE",
}
EXPECTED_FIXTURES = {
    "resolved_bundle_produces_valid_claim_ir",
    "active_required_unresolved_produces_extraction_abstain",
    "inactive_dependent_unresolved_does_not_abstain",
    "malformed_response_is_transaction_failure",
    "runtime_failure_is_transaction_failure",
    "abstain_never_compiles_claim_ir",
    "abstain_is_not_residual",
    "abstain_remains_in_selected_attempt_accounting",
    "abstain_is_excluded_from_primary_analyzable_denominator",
    "result_dependent_replacement_is_rejected",
}


class AbstentionContractError(ValueError):
    pass


def fail(message: str) -> None:
    raise AbstentionContractError(message)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def expect_exact_keys(value: Any, keys: set[str], path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{path}: expected object")
    actual = set(value)
    if actual != keys:
        fail(
            f"{path}: key mismatch missing={sorted(keys-actual)} "
            f"extra={sorted(actual-keys)}"
        )
    return value


def validate_contract(
    contract: Any,
    *,
    sampling: Any,
    postmortem: Any,
) -> dict[str, Any]:
    root = expect_exact_keys(
        contract,
        {
            "schema_version",
            "owner_issue",
            "status",
            "parent_authority",
            "scope",
            "bundle_outcomes",
            "abstention_rule",
            "transaction_failures",
            "transaction_boundary",
            "denominator_contract",
            "provenance_contract",
            "synthetic_destructive_fixtures",
            "exit_classifications",
            "architecture_consequence",
        },
        "contract",
    )
    if root["schema_version"] != CONTRACT_VERSION:
        fail("contract.schema_version")
    if root["owner_issue"] != 191:
        fail("contract.owner_issue")
    if root["status"] != "SYNTHETIC_QUALIFICATION_CANDIDATE":
        fail("contract.status")
    if root["architecture_consequence"] != "NONE":
        fail("architecture consequence must remain NONE")

    parent = root["parent_authority"]
    if parent.get("postmortem_path") != (
        "research/paper2/extraction_abstention_postmortem_v1.json"
    ):
        fail("parent postmortem path")
    if parent.get("postmortem_terminal_classification") != (
        "EXTRACTION_UNDERDETERMINED_ON_B0002"
    ):
        fail("parent terminal classification")
    if parent.get("consumed_transaction_issue") != 184:
        fail("parent transaction issue")
    if parent.get("consumed_transaction_replay_forbidden") is not True:
        fail("consumed transaction replay must remain forbidden")

    if not isinstance(postmortem, dict):
        fail("postmortem must be object")
    if (
        postmortem.get("terminal_diagnostic", {}).get("primary_classification")
        != "EXTRACTION_UNDERDETERMINED_ON_B0002"
    ):
        fail("current postmortem does not support #191")
    future = postmortem.get("future_protocol_boundary", {})
    if future.get("required_bundle_outcome") != "EXTRACTION_ABSTAIN":
        fail("postmortem future bundle outcome drift")
    if future.get("claim_ir_conversion_forbidden") is not True:
        fail("postmortem must forbid ClaimIR rescue")
    if future.get("residual_conversion_forbidden") is not True:
        fail("postmortem must forbid residual conversion")

    scope = root["scope"]
    required_false = (
        "real_paper_model_calls_authorized",
        "basis_decomposition_authorized",
        "heldout_execution_authorized",
        "changes_claim_ir_v1",
        "changes_systemone_decision_v2",
    )
    if scope.get("synthetic_only") is not True:
        fail("scope must be synthetic_only")
    for key in required_false:
        if scope.get(key) is not False:
            fail(f"scope.{key} must be false")

    outcomes = root["bundle_outcomes"]
    if set(outcomes) != EXPECTED_BUNDLE_OUTCOMES:
        fail("bundle outcome taxonomy drift")
    valid = outcomes["VALID_CLAIM_IR"]
    if (
        valid.get("claim_ir_permitted") is not True
        or valid.get("primary_analyzable") is not True
        or valid.get("selected_attempt_row_retained") is not True
        or valid.get("maps_to_sampling_v1") is not None
    ):
        fail("VALID_CLAIM_IR semantics")

    abstain = outcomes["EXTRACTION_ABSTAIN"]
    if (
        abstain.get("claim_ir_permitted") is not False
        or abstain.get("primary_analyzable") is not False
        or abstain.get("selected_attempt_row_retained") is not True
        or abstain.get("maps_to_sampling_v1") != "EXTRACTION_FAILURE"
    ):
        fail("EXTRACTION_ABSTAIN semantics")

    extraction_failure = outcomes["EXTRACTION_FAILURE"]
    if (
        extraction_failure.get("claim_ir_permitted") is not False
        or extraction_failure.get("primary_analyzable") is not False
        or extraction_failure.get("selected_attempt_row_retained") is not True
        or extraction_failure.get("maps_to_sampling_v1") != "EXTRACTION_FAILURE"
    ):
        fail("EXTRACTION_FAILURE semantics")

    if not isinstance(sampling, dict):
        fail("sampling must be object")
    taxonomy = sampling.get("outcome_taxonomy")
    if not isinstance(taxonomy, list) or "EXTRACTION_FAILURE" not in taxonomy:
        fail("#158 sampling authority lacks EXTRACTION_FAILURE")
    denominator = sampling.get("denominator_contract", {})
    if denominator.get("pipeline_failure_as_residual_forbidden") is not True:
        fail("#158 pipeline-failure/residual boundary drift")

    rule = root["abstention_rule"]
    if rule.get("wire_choice") != UNRESOLVED:
        fail("abstention wire choice")
    if rule.get("trigger") != (
        "explicit_unresolved_on_semantically_required_active_field_after_valid_response_parse"
    ):
        fail("abstention trigger")
    for key in (
        "inactive_dependent_field_unresolved_is_ignored",
        "claim_ir_conversion_forbidden",
        "residual_conversion_forbidden",
        "candidate_repair_forbidden",
        "retry_for_resolution_forbidden",
    ):
        if rule.get(key) is not True:
            fail(f"abstention_rule.{key} must be true")

    failures = root["transaction_failures"]
    if not isinstance(failures, list) or set(failures) != EXPECTED_TRANSACTION_FAILURES:
        fail("transaction failure taxonomy drift")

    boundary = root["transaction_boundary"]
    for key in (
        "transaction_failure_is_bundle_abstention",
        "bundle_abstention_is_transaction_integrity_failure",
        "malformed_systemone_response_is_bundle_abstention",
        "runtime_exception_is_bundle_abstention",
    ):
        if boundary.get(key) is not False:
            fail(f"transaction_boundary.{key} must be false")

    denom = root["denominator_contract"]
    if denom.get("selected_extraction_attempt_denominator_includes_abstain") is not True:
        fail("selected-attempt denominator must retain abstain")
    if denom.get("primary_analyzable_denominator_includes_abstain") is not False:
        fail("primary analyzable denominator must exclude abstain")
    for key in (
        "abstain_reported_as_explicit_attrition",
        "result_dependent_replacement_forbidden",
        "replacement_must_not_erase_original_attrition_row",
    ):
        if denom.get(key) is not True:
            fail(f"denominator_contract.{key} must be true")
    for key in ("abstain_may_be_silently_dropped", "abstain_may_be_residual"):
        if denom.get(key) is not False:
            fail(f"denominator_contract.{key} must be false")

    provenance = root["provenance_contract"]
    for key in (
        "preserve_unresolved_field_name",
        "preserve_unresolved_choice",
        "preserve_probabilities_when_present",
        "preserve_confidence_when_present",
        "preserve_source_bundle_digest",
        "preserve_normal_output_digest",
    ):
        if provenance.get(key) is not True:
            fail(f"provenance_contract.{key} must be true")
    if provenance.get("raw_or_masked_source_text_in_repository_artifact") is not False:
        fail("repository artifact must not contain source text")

    fixtures = root["synthetic_destructive_fixtures"]
    if not isinstance(fixtures, list) or set(fixtures) != EXPECTED_FIXTURES:
        fail("synthetic destructive fixture set drift")

    exits = root["exit_classifications"]
    required_exits = {
        "EXTRACTION_ABSTENTION_INTERFACE_V2_SYNTHETICALLY_QUALIFIED",
        "EXTRACTION_ABSTENTION_INTERFACE_UNDERDETERMINED",
        "TRANSACTION_FAILURE_AND_BUNDLE_ABSTENTION_NOT_SEPARATED",
        "UNDERDETERMINED",
    }
    if not isinstance(exits, list) or set(exits) != required_exits:
        fail("exit classification drift")

    return root


def unresolved_field_from_error(exc: DecisionUnresolved) -> str:
    message = str(exc)
    field = message.split(":", 1)[0].strip()
    if not field:
        fail("DecisionUnresolved did not identify a field")
    return field


def classify_parsed_answers(
    source: dict[str, Any],
    answers: dict[str, str],
) -> dict[str, Any]:
    try:
        decision = decision_from_answers(source, answers)
        candidate = compile_candidate(source, decision)
    except DecisionUnresolved as exc:
        return {
            "layer": "bundle",
            "outcome": "EXTRACTION_ABSTAIN",
            "unresolved_field": unresolved_field_from_error(exc),
            "unresolved_choice": UNRESOLVED,
            "claim_ir_compilation_permitted": False,
            "candidate": None,
        }
    except (TwoPassV2Error, ContractError, ValidationError) as exc:
        return {
            "layer": "bundle",
            "outcome": "EXTRACTION_FAILURE",
            "error_type": type(exc).__name__,
            "claim_ir_compilation_permitted": False,
            "candidate": None,
        }

    return {
        "layer": "bundle",
        "outcome": "VALID_CLAIM_IR",
        "claim_ir_compilation_permitted": True,
        "candidate": candidate,
    }


def classify_systemone_response(
    source: dict[str, Any],
    request_payload: dict[str, Any],
    response_payload: Any,
) -> dict[str, Any]:
    try:
        answers = parse_systemone_response(request_payload, response_payload)
    except (TwoPassV2Error, ContractError, ValidationError) as exc:
        return {
            "layer": "transaction",
            "classification": "TRANSACTION_RESPONSE_CONTRACT_FAILURE",
            "bundle_outcome": None,
            "error_type": type(exc).__name__,
        }
    return classify_parsed_answers(source, answers)


def classify_runtime_exception(exc: BaseException) -> dict[str, Any]:
    return {
        "layer": "transaction",
        "classification": "TRANSACTION_RUNTIME_FAILURE",
        "bundle_outcome": None,
        "error_type": type(exc).__name__,
    }


def summarize_bundle_outcomes(records: list[dict[str, str]]) -> dict[str, int]:
    seen: set[str] = set()
    counts = {key: 0 for key in EXPECTED_BUNDLE_OUTCOMES}
    for row in records:
        bundle_id = row.get("bundle_id")
        outcome = row.get("outcome")
        if not isinstance(bundle_id, str) or not bundle_id:
            fail("bundle outcome row requires bundle_id")
        if bundle_id in seen:
            fail(f"duplicate bundle outcome row: {bundle_id}")
        seen.add(bundle_id)
        if outcome not in EXPECTED_BUNDLE_OUTCOMES:
            fail(f"unknown bundle outcome: {outcome}")
        counts[outcome] += 1
    return {
        "selected_extraction_attempts": len(records),
        "valid_claim_ir": counts["VALID_CLAIM_IR"],
        "extraction_abstain": counts["EXTRACTION_ABSTAIN"],
        "extraction_failure": counts["EXTRACTION_FAILURE"],
        "primary_analyzable": counts["VALID_CLAIM_IR"],
        "explicit_attrition": (
            counts["EXTRACTION_ABSTAIN"] + counts["EXTRACTION_FAILURE"]
        ),
    }


def validate_replacement_attempt(
    *,
    reason: str,
    erase_original_row: bool,
) -> None:
    if reason in EXPECTED_BUNDLE_OUTCOMES:
        fail("result-dependent replacement is forbidden")
    if erase_original_row:
        fail("replacement must not erase original attrition row")


def self_test(
    contract_path: Path,
    sampling_path: Path,
    postmortem_path: Path,
) -> None:
    contract = load_json(contract_path)
    sampling = load_json(sampling_path)
    postmortem = load_json(postmortem_path)
    validate_contract(contract, sampling=sampling, postmortem=postmortem)

    source = synthetic_source(
        [
            "Synthetic state A.",
            "Synthetic outcome B.",
            "Synthetic state A depends on synthetic outcome B.",
        ],
        bundle_id="B9001",
    )
    request_payload = build_systemone_request(
        source,
        "Synthetic source-supported dependency.",
        "synthetic-systemone",
    )

    # Resolved bundle -> valid candidate surface.
    resolved_choices = relation_answers(source)
    resolved_response = response_for(request_payload, resolved_choices)
    resolved = classify_systemone_response(source, request_payload, resolved_response)
    if resolved["outcome"] != "VALID_CLAIM_IR":
        raise AssertionError(f"resolved bundle: {resolved}")
    if resolved["candidate"] is None:
        raise AssertionError("resolved bundle must compile a candidate")

    # Active required unresolved -> explicit bundle abstention, no candidate rescue.
    active_unresolved_choices = copy.deepcopy(resolved_choices)
    active_unresolved_choices["n1__role"] = UNRESOLVED
    active_unresolved_response = response_for(
        request_payload,
        active_unresolved_choices,
    )
    active_unresolved = classify_systemone_response(
        source,
        request_payload,
        active_unresolved_response,
    )
    if active_unresolved.get("outcome") != "EXTRACTION_ABSTAIN":
        raise AssertionError(f"active unresolved: {active_unresolved}")
    if active_unresolved.get("unresolved_field") != "n1__role":
        raise AssertionError("active unresolved provenance field")
    if active_unresolved.get("candidate") is not None:
        raise AssertionError("abstention must never compile a candidate")
    if active_unresolved.get("claim_ir_compilation_permitted") is not False:
        raise AssertionError("abstention must forbid ClaimIR compilation")

    # Inactive dependent fields are semantically irrelevant: unresolved there
    # must not manufacture an abstention.
    inactive_choices = copy.deepcopy(resolved_choices)
    inactive_choices["n3__active"] = "no"
    inactive_choices["n3__role"] = UNRESOLVED
    inactive_choices["n3__anchor"] = UNRESOLVED
    inactive_choices["n3__grounding"] = UNRESOLVED
    for sid in ("s1", "s2", "s3"):
        inactive_choices[f"n3__span__{sid}"] = UNRESOLVED
    inactive_response = response_for(request_payload, inactive_choices)
    inactive = classify_systemone_response(source, request_payload, inactive_response)
    if inactive.get("outcome") != "VALID_CLAIM_IR":
        raise AssertionError(f"inactive unresolved must be ignored: {inactive}")

    # Malformed wire/response contract remains transaction failure.
    malformed = copy.deepcopy(resolved_response)
    malformed["answers"].pop("claim_type")
    malformed_result = classify_systemone_response(
        source,
        request_payload,
        malformed,
    )
    if malformed_result.get("classification") != (
        "TRANSACTION_RESPONSE_CONTRACT_FAILURE"
    ):
        raise AssertionError(f"malformed response classification: {malformed_result}")
    if malformed_result.get("bundle_outcome") is not None:
        raise AssertionError("transaction response failure is not bundle abstention")

    runtime_result = classify_runtime_exception(OSError("synthetic runtime failure"))
    if runtime_result.get("classification") != "TRANSACTION_RUNTIME_FAILURE":
        raise AssertionError("runtime failure classification")
    if runtime_result.get("bundle_outcome") is not None:
        raise AssertionError("runtime failure is not bundle abstention")

    # Denominator layering: abstention remains in selected-attempt accounting,
    # is explicit attrition, and is excluded from the primary analyzable count.
    summary = summarize_bundle_outcomes(
        [
            {"bundle_id": "B9001", "outcome": "VALID_CLAIM_IR"},
            {"bundle_id": "B9002", "outcome": "EXTRACTION_ABSTAIN"},
            {"bundle_id": "B9003", "outcome": "EXTRACTION_FAILURE"},
        ]
    )
    expected_summary = {
        "selected_extraction_attempts": 3,
        "valid_claim_ir": 1,
        "extraction_abstain": 1,
        "extraction_failure": 1,
        "primary_analyzable": 1,
        "explicit_attrition": 2,
    }
    if summary != expected_summary:
        raise AssertionError(f"denominator accounting: {summary}")

    if contract["denominator_contract"]["abstain_may_be_residual"] is not False:
        raise AssertionError("abstention must not become RESIDUAL")
    if contract["bundle_outcomes"]["EXTRACTION_ABSTAIN"]["claim_ir_permitted"]:
        raise AssertionError("abstention ClaimIR rescue forbidden")

    # Outcome-dependent replacement is rejected; even predeclared replacement
    # semantics cannot erase the original attrition row.
    try:
        validate_replacement_attempt(
            reason="EXTRACTION_ABSTAIN",
            erase_original_row=False,
        )
    except AbstentionContractError:
        pass
    else:
        raise AssertionError("outcome-dependent replacement unexpectedly allowed")

    try:
        validate_replacement_attempt(
            reason="PREDECLARED_RESERVE",
            erase_original_row=True,
        )
    except AbstentionContractError:
        pass
    else:
        raise AssertionError("attrition-row erasure unexpectedly allowed")

    validate_replacement_attempt(
        reason="PREDECLARED_RESERVE",
        erase_original_row=False,
    )

    print("PAPER2_EXTRACTION_ABSTENTION_V2_SELFTEST_PASS")
    print("EXTRACTION_ABSTENTION_INTERFACE_V2_SYNTHETICALLY_QUALIFIED")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path("research/paper2/extraction_abstention_v2.json"),
    )
    parser.add_argument(
        "--sampling",
        type=Path,
        default=Path("research/paper2/sampling_v1.json"),
    )
    parser.add_argument(
        "--postmortem",
        type=Path,
        default=Path("research/paper2/extraction_abstention_postmortem_v1.json"),
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        contract = load_json(args.contract)
        sampling = load_json(args.sampling)
        postmortem = load_json(args.postmortem)
        validate_contract(contract, sampling=sampling, postmortem=postmortem)
        if args.self_test:
            self_test(args.contract, args.sampling, args.postmortem)
        else:
            print("PAPER2_EXTRACTION_ABSTENTION_V2_VALID")
        return 0
    except (
        OSError,
        json.JSONDecodeError,
        AbstentionContractError,
        AssertionError,
        TwoPassV2Error,
        ContractError,
        ValidationError,
    ) as exc:
        print(f"PAPER2_EXTRACTION_ABSTENTION_V2_INVALID: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
