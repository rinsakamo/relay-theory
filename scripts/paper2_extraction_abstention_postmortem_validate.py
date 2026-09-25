#!/usr/bin/env python3
"""Validate the repository-safe Paper 2 #189 abstention postmortem.

This validator checks the immutable digest inventory and the source-only
adjudication record.  It deliberately rejects raw or masked source fields and
does not read the external evidence root.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "paper2-extraction-abstention-postmortem-v1"
ARTIFACT_PATH = Path("research/paper2/extraction_abstention_postmortem_v1.json")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
ROLE_CHOICES = [
    "condition",
    "available_information",
    "state_or_structure",
    "intervention",
    "response_or_outcome",
    "criterion",
    "probe",
    "partition",
    "other",
]
OBSERVED_ROLE_CHOICES = [
    "__unresolved__",
    "available_information",
    "condition",
    "criterion",
    "intervention",
    "other",
    "partition",
    "probe",
    "response_or_outcome",
    "state_or_structure",
]
EXPECTED_RESOLVED_ROLE_SHA256 = (
    "4c19bc2e3f4094288b2c658c1bf0ce9305a76cea6658a861bf2d01b011eba3b6"
)
EXPECTED_OBSERVED_ROLE_SHA256 = (
    "a3b3a5faf3efae8d7319334031fc6ad234fc2feb09d9c63653232bb1cfd50cd6"
)
FORBIDDEN_KEY_PARTS = (
    "raw_source_text",
    "masked_source_text",
    "source_text",
    "source_spans",
    "normal_interpretation_text",
    "abstract_text",
    "content",
)


class ContractError(ValueError):
    """Raised when the postmortem contract is violated."""


def fail(message: str) -> None:
    raise ContractError(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def expect_dict(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{path}: expected object")
    return value


def expect_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{path}: expected array")
    return value


def expect_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value:
        fail(f"{path}: expected non-empty string")
    return value


def expect_bool(value: Any, path: str, expected: bool = True) -> None:
    if value is not expected:
        fail(f"{path}: expected {expected!r}")


def expect_equal(actual: Any, expected: Any, path: str) -> None:
    if actual != expected:
        fail(f"{path}: expected {expected!r}, got {actual!r}")


def expect_sha256(value: Any, path: str) -> str:
    if not isinstance(value, str) or not HEX64_RE.fullmatch(value):
        fail(f"{path}: expected lowercase SHA-256 hex")
    return value


def walk_forbidden_keys(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            lowered = key.lower()
            if any(part in lowered for part in FORBIDDEN_KEY_PARTS):
                fail(f"{path}.{key}: raw/source-content field is forbidden")
            walk_forbidden_keys(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            walk_forbidden_keys(item, f"{path}[{index}]")


def canonical_list_sha256(values: list[str]) -> str:
    encoded = json.dumps(values, ensure_ascii=False, separators=(",", ":")).encode(
        "utf-8"
    )
    return sha256_bytes(encoded)


def validate_probability_map(value: Any, path: str) -> None:
    probabilities = expect_dict(value, path)
    if not probabilities:
        fail(f"{path}: empty probability map")
    total = 0.0
    for choice, probability in probabilities.items():
        expect_string(choice, f"{path}.{choice}")
        if not isinstance(probability, (int, float)) or isinstance(probability, bool):
            fail(f"{path}.{choice}: expected number")
        if probability < 0.0 or probability > 1.0:
            fail(f"{path}.{choice}: outside [0, 1]")
        total += float(probability)
    if abs(total - 1.0) > 0.002:
        fail(f"{path}: probabilities do not sum to one after rounding: {total}")


def validate_choice_record(value: Any, path: str, expected_choice: str | None = None) -> None:
    record = expect_dict(value, path)
    expect_string(record.get("choice"), f"{path}.choice")
    if expected_choice is not None:
        expect_equal(record["choice"], expected_choice, f"{path}.choice")
    confidence = record.get("confidence")
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
        fail(f"{path}.confidence: expected number")
    if confidence < 0.0 or confidence > 1.0:
        fail(f"{path}.confidence: outside [0, 1]")
    validate_probability_map(record.get("probabilities"), f"{path}.probabilities")


def validate_inventory(inventory: dict[str, Any]) -> None:
    expect_equal(inventory.get("root_name"), "paper2-184-20260924T152612Z", "evidence_inventory.root_name")
    expect_equal(inventory.get("digest_algorithm"), "SHA-256", "evidence_inventory.digest_algorithm")
    expect_equal(inventory.get("file_count"), 22, "evidence_inventory.file_count")
    files = expect_list(inventory.get("files"), "evidence_inventory.files")
    if len(files) != 22:
        fail("evidence_inventory.files: expected exactly 22 files")
    paths: list[str] = []
    serialized: list[str] = []
    for index, item in enumerate(files):
        record = expect_dict(item, f"evidence_inventory.files[{index}]")
        path = expect_string(record.get("path"), f"evidence_inventory.files[{index}].path")
        size = record.get("size_bytes")
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            fail(f"evidence_inventory.files[{index}].size_bytes: expected non-negative integer")
        digest = expect_sha256(record.get("sha256"), f"evidence_inventory.files[{index}].sha256")
        paths.append(path)
        serialized.append(f"{path}\t{size}\t{digest}")
    if paths != sorted(paths) or len(set(paths)) != len(paths):
        fail("evidence_inventory.files: paths must be unique and sorted")
    inventory_digest = sha256_bytes(("\n".join(serialized) + "\n").encode("utf-8"))
    expect_equal(inventory.get("inventory_sha256"), inventory_digest, "evidence_inventory.inventory_sha256")


def validate_role_vocabulary(value: dict[str, Any]) -> None:
    expect_equal(value.get("resolved_choices"), ROLE_CHOICES, "role_vocabulary.resolved_choices")
    expect_equal(value.get("explicit_unresolved_choice"), "__unresolved__", "role_vocabulary.explicit_unresolved_choice")
    expect_equal(value.get("resolved_choices_sha256"), EXPECTED_RESOLVED_ROLE_SHA256, "role_vocabulary.resolved_choices_sha256")
    expect_equal(value.get("observed_n1_role_question_choices_sorted"), OBSERVED_ROLE_CHOICES, "role_vocabulary.observed_n1_role_question_choices_sorted")
    expect_equal(value.get("observed_n1_role_question_choices_sha256"), EXPECTED_OBSERVED_ROLE_SHA256, "role_vocabulary.observed_n1_role_question_choices_sha256")
    expect_equal(canonical_list_sha256(ROLE_CHOICES), EXPECTED_RESOLVED_ROLE_SHA256, "computed resolved role digest")
    expect_equal(canonical_list_sha256(OBSERVED_ROLE_CHOICES), EXPECTED_OBSERVED_ROLE_SHA256, "computed observed role digest")
    expect_sha256(value.get("schema_sha256"), "role_vocabulary.schema_sha256")


def validate_artifact(value: Any) -> dict[str, Any]:
    root = expect_dict(value, "root")
    walk_forbidden_keys(root)
    expect_equal(root.get("schema_version"), SCHEMA_VERSION, "schema_version")
    expect_equal(root.get("owner_issue"), 189, "owner_issue")
    expect_equal(root.get("parent_transaction_issue"), 184, "parent_transaction_issue")
    expect_equal(root.get("status"), "TERMINAL_RECONCILED", "status")
    expect_equal(root.get("architecture_consequence"), "NONE", "architecture_consequence")

    authority = expect_dict(root.get("authority"), "authority")
    expect_equal(authority.get("main_head_at_inventory"), "e2dc226f34bda1a306b45ef43461c4b9fdb034a1", "authority.main_head_at_inventory")
    expect_equal(authority.get("main_tree_at_inventory"), "56c7d7d1d5fbde868a37c431b51a51620a110a62", "authority.main_tree_at_inventory")
    ruleset = expect_dict(authority.get("ruleset"), "authority.ruleset")
    expect_equal(ruleset.get("id"), 23769009, "authority.ruleset.id")
    expect_equal(ruleset.get("enforcement"), "active", "authority.ruleset.enforcement")
    expect_equal(ruleset.get("allowed_merge_methods"), ["squash"], "authority.ruleset.allowed_merge_methods")
    expect_bool(ruleset.get("required_linear_history"), "authority.ruleset.required_linear_history")
    expect_bool(ruleset.get("required_review_thread_resolution"), "authority.ruleset.required_review_thread_resolution")
    validate_inventory(expect_dict(root.get("evidence_inventory"), "evidence_inventory"))

    transaction = expect_dict(root.get("transaction"), "transaction")
    expect_equal(transaction.get("terminal_classification"), "SCIENTIFIC_TRANSACTION_CONSUMED_INCOMPLETE", "transaction.terminal_classification")
    for key in ("no_retry", "no_replay", "no_b0002_requery", "no_b0003_continuation"):
        expect_bool(transaction.get(key), f"transaction.{key}")
    expect_equal(transaction.get("error_type"), "DecisionUnresolved", "transaction.error_type")
    expect_equal(transaction.get("error_field"), "n1__role", "transaction.error_field")
    expect_equal(transaction.get("error_choice"), "__unresolved__", "transaction.error_choice")
    observed = expect_dict(transaction.get("observed"), "transaction.observed")
    for key, expected in {
        "replicate": "A",
        "last_bundle": "B0002",
        "server_launches": 1,
        "scientific_calls_attempted": 4,
        "total_calls_completed": 4,
        "valid_claim_ir_outputs": 1,
        "retry": 0,
        "replay": 0,
        "fallback": 0,
    }.items():
        expect_equal(observed.get(key), expected, f"transaction.observed.{key}")
    expect_bool(observed.get("basis_decomposition_executed"), "transaction.observed.basis_decomposition_executed", False)
    integrity = expect_dict(transaction.get("transaction_integrity"), "transaction.transaction_integrity")
    expect_equal(integrity.get("classification"), "NO_TRANSACTION_APPARATUS_DEFECT_EVIDENCED", "transaction.transaction_integrity.classification")
    cleanup = expect_dict(integrity.get("cleanup"), "transaction.transaction_integrity.cleanup")
    expect_bool(cleanup.get("recorded"), "transaction.transaction_integrity.cleanup.recorded")
    expect_bool(cleanup.get("owned_process"), "transaction.transaction_integrity.cleanup.owned_process")
    expect_bool(cleanup.get("terminated"), "transaction.transaction_integrity.cleanup.terminated")
    expect_equal(cleanup.get("exit_code"), 0, "transaction.transaction_integrity.cleanup.exit_code")
    server_log = expect_dict(integrity.get("separate_server_log"), "transaction.transaction_integrity.separate_server_log")
    expect_bool(server_log.get("present_in_inventory"), "transaction.transaction_integrity.separate_server_log.present_in_inventory", False)

    validate_role_vocabulary(expect_dict(root.get("role_vocabulary"), "role_vocabulary"))
    b0002 = expect_dict(root.get("b0002"), "b0002")
    expect_equal(b0002.get("replicate"), "A", "b0002.replicate")
    expect_equal(b0002.get("bundle_id"), "B0002", "b0002.bundle_id")
    expect_sha256(b0002.get("masked_bundle_sha256"), "b0002.masked_bundle_sha256")
    expect_sha256(b0002.get("raw_normalized_source_sha256"), "b0002.raw_normalized_source_sha256")
    expect_bool(b0002.get("raw_and_masked_source_bytes_committed"), "b0002.raw_and_masked_source_bytes_committed", False)
    source_bundle = expect_dict(b0002.get("source_bundle"), "b0002.source_bundle")
    expect_equal(source_bundle.get("span_count"), 5, "b0002.source_bundle.span_count")
    expect_equal(source_bundle.get("span_ids"), ["s1", "s2", "s3", "s4", "s5"], "b0002.source_bundle.span_ids")
    normal = expect_dict(b0002.get("normal"), "b0002.normal")
    expect_equal(normal.get("focus_span_ids_after_frozen_cap"), ["s1", "s3", "s4"], "b0002.normal.focus_span_ids_after_frozen_cap")
    expect_bool(normal.get("advisory_only"), "b0002.normal.advisory_only")
    systemone = expect_dict(b0002.get("systemone"), "b0002.systemone")
    expect_equal(systemone.get("focus_source_span_ids"), ["s1", "s3", "s4"], "b0002.systemone.focus_source_span_ids")
    expect_bool(systemone.get("cache_prompt"), "b0002.systemone.cache_prompt", False)
    n1 = expect_dict(systemone.get("n1"), "b0002.systemone.n1")
    validate_choice_record(n1.get("active"), "b0002.systemone.n1.active", "yes")
    validate_choice_record(n1.get("role"), "b0002.systemone.n1.role", "__unresolved__")
    validate_choice_record(n1.get("anchor"), "b0002.systemone.n1.anchor", "s1")
    validate_choice_record(n1.get("grounding"), "b0002.systemone.n1.grounding", "explicit")
    source_selections = expect_dict(n1.get("source_span_selections"), "b0002.systemone.n1.source_span_selections")
    if set(source_selections) != {"s1", "s3", "s4"}:
        fail("b0002.systemone.n1.source_span_selections: unexpected span set")
    for span_id in ("s1", "s3", "s4"):
        validate_choice_record(source_selections[span_id], f"b0002.systemone.n1.source_span_selections.{span_id}", "yes")
    absent = expect_list(b0002.get("absent_after_terminal_stop"), "b0002.absent_after_terminal_stop")
    if any(path in {item["path"] for item in expect_list(expect_dict(root["evidence_inventory"], "evidence_inventory").get("files"), "evidence_inventory.files")} for path in absent):
        fail("b0002.absent_after_terminal_stop: an absent artifact is listed in the inventory")

    adjudication = expect_dict(root.get("adjudication"), "adjudication")
    for key in ("basis_blind", "decomposition_outcome_blind", "author_prestige_blind", "venue_blind", "citation_count_blind"):
        expect_bool(adjudication.get(key), f"adjudication.{key}")
    expect_equal(adjudication["A_active_field"]["classification"], "ACTIVE_REQUIRED_FIELD", "adjudication.A_active_field.classification")
    expect_equal(adjudication["B_existing_role_support"]["classification"], "EXISTING_ROLE_SOURCE_SUPPORTED", "adjudication.B_existing_role_support.classification")
    expect_equal(adjudication["C_masking"]["classification"], "MASKING_NOT_CAUSAL", "adjudication.C_masking.classification")
    expect_equal(adjudication["D_normal_to_systemone"]["classification"], "DIRECTLY_SOURCE_MOTIVATED", "adjudication.D_normal_to_systemone.classification")
    expect_equal(adjudication["E_outcome"]["classification"], "EXTRACTION_UNDERDETERMINED_ON_B0002", "adjudication.E_outcome.classification")
    expect_bool(adjudication["E_outcome"]["explicit_unresolved_is_valid_claim_ir"], "adjudication.E_outcome.explicit_unresolved_is_valid_claim_ir", False)
    expect_bool(adjudication["E_outcome"]["valid_claim_ir_rescue_performed"], "adjudication.E_outcome.valid_claim_ir_rescue_performed", False)
    expect_bool(adjudication["E_outcome"]["extraction_abstain_equals_residual"], "adjudication.E_outcome.extraction_abstain_equals_residual", False)
    expect_bool(adjudication["E_outcome"]["original_row_remains_in_denominator"], "adjudication.E_outcome.original_row_remains_in_denominator")
    expect_bool(adjudication["E_outcome"]["replacement_may_erase_original_row"], "adjudication.E_outcome.replacement_may_erase_original_row", False)

    terminal = expect_dict(root.get("terminal_diagnostic"), "terminal_diagnostic")
    expect_equal(terminal.get("primary_classification"), "EXTRACTION_UNDERDETERMINED_ON_B0002", "terminal_diagnostic.primary_classification")
    expect_bool(terminal.get("transaction_integrity_failure"), "terminal_diagnostic.transaction_integrity_failure", False)
    expect_bool(terminal.get("one_bundle_not_extractable_under_frozen_interface"), "terminal_diagnostic.one_bundle_not_extractable_under_frozen_interface")
    future = expect_dict(root.get("future_protocol_boundary"), "future_protocol_boundary")
    expect_equal(future.get("required_bundle_outcome"), "EXTRACTION_ABSTAIN", "future_protocol_boundary.required_bundle_outcome")
    for key in ("claim_ir_conversion_forbidden", "residual_conversion_forbidden", "denominator_attrition_accounting_required", "result_dependent_replacement_forbidden"):
        expect_bool(future.get(key), f"future_protocol_boundary.{key}")
    for key in ("new_real_scientific_transaction_created", "new_real_scientific_transaction_authorized", "new_real_scientific_transaction_executed"):
        expect_bool(future.get(key), f"future_protocol_boundary.{key}", False)
    return root


def expect_failure(callback: Any, label: str) -> None:
    try:
        callback()
    except ContractError:
        return
    fail(f"self-test {label}: expected validation failure")


def self_test(path: Path) -> None:
    artifact = load_json(path)
    validate_artifact(artifact)

    mutated = copy.deepcopy(artifact)
    mutated["b0002"]["systemone"]["n1"]["active"]["choice"] = "no"
    expect_failure(lambda: validate_artifact(mutated), "inactive n1 mutation")

    mutated = copy.deepcopy(artifact)
    mutated["terminal_diagnostic"]["primary_classification"] = "BUNDLE_LEVEL_ABSTENTION_REQUIRED"
    expect_failure(lambda: validate_artifact(mutated), "terminal classification mutation")

    mutated = copy.deepcopy(artifact)
    mutated["raw_source_text"] = "must never be committed"
    expect_failure(lambda: validate_artifact(mutated), "raw source insertion")

    mutated = copy.deepcopy(artifact)
    mutated["evidence_inventory"]["inventory_sha256"] = "0" * 64
    expect_failure(lambda: validate_artifact(mutated), "inventory digest mutation")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ARTIFACT_PATH)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            self_test(args.input)
            print("PAPER2_EXTRACTION_ABSTENTION_POSTMORTEM_V1_SELFTEST_PASS")
        else:
            validate_artifact(load_json(args.input))
            print("PAPER2_EXTRACTION_ABSTENTION_POSTMORTEM_V1_VALID")
    except ContractError as exc:
        print(f"PAPER2_EXTRACTION_ABSTENTION_POSTMORTEM_V1_FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
