#!/usr/bin/env python3
"""Validate the repository-safe Paper 2 #197 zero-yield postmortem.

The validator checks only the committed, source-free artifact.  It never reads
the local #193 evidence root or the frozen source root, so CI cannot silently
replace the byte-derived inventory with a different local checkout.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable


SCHEMA_VERSION = "paper2-extraction-zero-yield-postmortem-v1"
ARTIFACT_PATH = Path("research/paper2/extraction_zero_yield_postmortem_v1.json")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
EXPECTED_INVENTORY_SHA256 = "b0b83e8d6b4b962143e7ce5a2f50a6831494a05d2a96ea2ed0a2b7cb03f67332"
EXPECTED_PATH_SET_SHA256 = "f0c76aa035c6f87563779baf66f729ef3188b20748081199dc7b25a921a20206"
EXPECTED_BUNDLE_SHA256 = {
    "B0001": "7ae16a522905be942255dd4114e570bcb18917f21439484ccdd25db3c6949b90",
    "B0002": "94dfa9b9a512d80416a7a23e7c6d483af94e897d9947e5dc0d1ddf6e6e91d3d2",
    "B0003": "f88106ccb29976d0fccecc3aa21642bf3d4eef0edce8db2492f470aab0361005",
    "B0004": "422dd03791f71c32170d8bfe5e8c96d26e81e7b069a4bd5f9b9ea4e7897d44cf",
    "B0005": "068eff2109128dcff80c31bade79e67b0be560fb2b6782b3b3af5a2e8f6d4a3b",
}
EXPECTED_CATEGORY_COUNTS = {
    "row_record": 10,
    "masked_source_bundle_copy": 10,
    "normal_request": 10,
    "normal_response": 10,
    "normal_output": 10,
    "systemone_request": 10,
    "systemone_response": 10,
    "systemone_answers": 10,
    "aggregate_authority": 5,
}
FORBIDDEN_KEY_PARTS = (
    "raw_source",
    "masked_source_text",
    "source_text",
    "source_spans",
    "raw_text",
    "masked_text",
    "abstract_text",
    "full_text",
    "source_excerpt",
    "passage",
    "content_text",
    "normal_prose",
    "systemone_prose",
    "source_content",
)
SOURCE_SUPPORT_CLASSES = {
    "SOURCE_SUPPORTS_EXISTING_CHOICE",
    "SOURCE_SUPPORTS_NO_EXISTING_CHOICE",
    "SOURCE_INSUFFICIENT_TO_DECIDE",
    "MASKING_REMOVED_DECISIVE_EVIDENCE",
    "APPARATUS_EVIDENCE_INSUFFICIENT",
}


class ContractError(ValueError):
    """Raised when the committed artifact violates the frozen contract."""


def fail(message: str) -> None:
    raise ContractError(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")


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
        fail(f"{path}: expected {expected!r}, got {value!r}")


def expect_equal(actual: Any, expected: Any, path: str) -> None:
    if actual != expected:
        fail(f"{path}: expected {expected!r}, got {actual!r}")


def expect_sha256(value: Any, path: str) -> str:
    if not isinstance(value, str) or not HEX64_RE.fullmatch(value):
        fail(f"{path}: expected lowercase SHA-256 hex")
    return value


def expect_git_sha(value: Any, path: str) -> str:
    if not isinstance(value, str) or not HEX40_RE.fullmatch(value):
        fail(f"{path}: expected lowercase 40-character Git SHA")
    return value


def expect_number_01(value: Any, path: str) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        fail(f"{path}: expected number")
    if not 0.0 <= float(value) <= 1.0:
        fail(f"{path}: outside [0, 1]")


def walk_forbidden_keys(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            lowered = str(key).lower()
            if any(part in lowered for part in FORBIDDEN_KEY_PARTS):
                fail(f"{path}.{key}: raw/source-content field is forbidden")
            walk_forbidden_keys(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            walk_forbidden_keys(item, f"{path}[{index}]")


def validate_all_hash_fields(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            lowered = str(key).lower()
            if lowered.endswith("sha256") and not isinstance(item, (dict, list)):
                expect_sha256(item, f"{path}.{key}")
            elif lowered in {"head_sha", "tree_sha", "main_head_at_inventory", "main_tree_at_inventory"} and not isinstance(item, (dict, list)):
                expect_git_sha(item, f"{path}.{key}")
            validate_all_hash_fields(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            validate_all_hash_fields(item, f"{path}[{index}]")


def validate_authority(value: Any) -> None:
    authority = expect_dict(value, "authority")
    expect_equal(authority.get("repository"), "rinsakamo/relay-theory", "authority.repository")
    expect_equal(authority.get("main_head_at_inventory"), "3b00221ba6828c1748af2e7f96b8cc1b39e7c247", "authority.main_head_at_inventory")
    expect_equal(authority.get("main_tree_at_inventory"), "e6b23c63ec1032200292c4d6a9846241997cefe3", "authority.main_tree_at_inventory")
    ruleset = expect_dict(authority.get("ruleset"), "authority.ruleset")
    expect_equal(ruleset.get("id"), 23769009, "authority.ruleset.id")
    expect_equal(ruleset.get("name"), "main-protection", "authority.ruleset.name")
    expect_equal(ruleset.get("enforcement"), "active", "authority.ruleset.enforcement")
    expect_equal(ruleset.get("allowed_merge_methods"), ["squash"], "authority.ruleset.allowed_merge_methods")
    expect_bool(ruleset.get("required_linear_history"), "authority.ruleset.required_linear_history")
    expect_bool(ruleset.get("required_review_thread_resolution"), "authority.ruleset.required_review_thread_resolution")
    authority_files = expect_list(authority.get("repository_authority_files"), "authority.repository_authority_files")
    expect_equal(
        authority_files,
        [
            {"path": ".ai/README.md", "blob_sha": "d62d79f2016b8cba2ee555197f0bbef92f58282b"},
            {"path": ".ai/forge-protocol.md", "blob_sha": "25c15145c17979ae2c4e95e18c89a47669ff5ef5"},
        ],
        "authority.repository_authority_files",
    )
    expect_equal(authority.get("open_issue_numbers"), [23, 130, 143, 147, 158, 167, 197], "authority.open_issue_numbers")
    expect_equal(
        authority.get("open_pull_requests"),
        [{"number": 123, "base": "main", "head": "paper-1-draft-ja", "head_sha": "290748d2a0f60374c77c8ed04cb7121fae459c8b", "draft": True}],
        "authority.open_pull_requests",
    )
    expect_equal(
        authority.get("latest_comment_ids"),
        {
            "197_forensic": 5831559761,
            "193_terminal": 5829838222,
            "193_authorization": 5829235859,
            "189_terminal": 5828524456,
            "191_terminal": 5828672892,
            "130_latest": 5832304044,
            "147_latest": 5831153095,
            "158_latest": 5831153890,
        },
        "authority.latest_comment_ids",
    )


def validate_provenance(value: Any) -> None:
    provenance = expect_dict(value, "provenance")
    expected = {
        "evidence_root_name": "paper2-193-v2-20260925T081509Z",
        "frozen_source_root_name": "paper2-162-20260923T143357Z",
        "transaction_summary_sha256": "3faa4c8ce0c86f96116f571885489ebb2a8bcbb09d96f81df29bd2e77516eab4",
        "transaction_receipt_sha256": "773a5a812a4a11bca92d4784242bd73799c482d58cea0446ff8de1b9a35f0d8a",
        "ab_outcome_comparison_sha256": "2634d5ad9400b4daada1d7236742a5b8435023159bc5282e64eafe3cab5a6340",
        "preflight_attestation_sha256": "17d0952084bfb294afa0321aad82721487a943c129b168836279f78d748c1813",
        "runner_contract_sha256": "484650766148cf9a6e17712de6a888bbfb92d0f43862b7acfc096e888abd454f",
        "frozen_preprocessing_sha256": "a20c79555bc3b2bafb25ee805a2fb1f6b9ea1b65c16a493dd4792130c1da9ea2",
        "frozen_mask_term_authority_sha256": "1b0963e07d6948d9d106a2200f48da680cb11a3705ecf8dd8bd8aa481df9badd",
    }
    for key, expected_value in expected.items():
        expect_equal(provenance.get(key), expected_value, f"provenance.{key}")
    expect_equal(provenance.get("frozen_bundle_sha256"), EXPECTED_BUNDLE_SHA256, "provenance.frozen_bundle_sha256")
    expect_bool(provenance.get("evidence_bytes_mutated"), "provenance.evidence_bytes_mutated", False)
    expect_bool(provenance.get("frozen_source_bytes_mutated"), "provenance.frozen_source_bytes_mutated", False)
    expect_bool(provenance.get("source_bytes_committed"), "provenance.source_bytes_committed", False)


def _expected_inventory_metadata(relative_path: str) -> tuple[str, str | None, str | None, str, str]:
    parts = relative_path.split("/")
    if len(parts) == 3 and parts[0] in {"A", "B"}:
        replicate: str | None = parts[0]
        bundle_id: str | None = parts[1]
        name = parts[2]
    else:
        replicate = None
        bundle_id = None
        name = relative_path
    if name == "artifact-record.json":
        return "row_record", replicate, bundle_id, "row", "row_outcome"
    if name == "source-bundle.json":
        return "masked_source_bundle_copy", replicate, bundle_id, "preprocessing", "source_bundle"
    if name == "normal-request.json":
        return "normal_request", replicate, bundle_id, "normal", "request"
    if name == "normal-response.json":
        return "normal_response", replicate, bundle_id, "normal", "response"
    if name == "normal-output.txt":
        return "normal_output", replicate, bundle_id, "normal", "output"
    if name == "systemone-request.json":
        return "systemone_request", replicate, bundle_id, "systemone", "request"
    if name == "systemone-response.json":
        return "systemone_response", replicate, bundle_id, "systemone", "response"
    if name == "systemone-answers.json":
        return "systemone_answers", replicate, bundle_id, "systemone", "answers"
    aggregate_roles = {
        "ab-outcome-comparison.json": "comparison",
        "preflight-attestation.json": "preflight",
        "runner-contract.json": "runner_contract",
        "transaction-receipt.json": "receipt",
        "transaction-summary.json": "summary",
    }
    if relative_path in aggregate_roles:
        return "aggregate_authority", None, None, "aggregate", aggregate_roles[relative_path]
    fail(f"evidence_inventory.files: unexpected path {relative_path!r}")


def validate_inventory(value: Any) -> set[str]:
    inventory = expect_dict(value, "evidence_inventory")
    expect_equal(inventory.get("path_semantics"), "relative_to_immutable_evidence_root", "evidence_inventory.path_semantics")
    expect_equal(inventory.get("digest_algorithm"), "SHA-256", "evidence_inventory.digest_algorithm")
    expect_equal(inventory.get("line_serialization"), "path<TAB>size_bytes<TAB>sha256 followed by LF, sorted by path", "evidence_inventory.line_serialization")
    expect_equal(inventory.get("root_name"), "paper2-193-v2-20260925T081509Z", "evidence_inventory.root_name")
    expect_equal(inventory.get("file_count"), 85, "evidence_inventory.file_count")
    files = expect_list(inventory.get("files"), "evidence_inventory.files")
    if len(files) != 85:
        fail("evidence_inventory.files: expected exactly 85 files")
    paths: list[str] = []
    serialized: list[str] = []
    counts: dict[str, int] = {}
    for index, item in enumerate(files):
        path = f"evidence_inventory.files[{index}]"
        record = expect_dict(item, path)
        relative_path = expect_string(record.get("relative_path"), f"{path}.relative_path")
        if relative_path.startswith("/") or "\\" in relative_path or ".." in relative_path.split("/"):
            fail(f"{path}.relative_path: must be a relative POSIX path")
        size = record.get("size_bytes")
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            fail(f"{path}.size_bytes: expected non-negative integer")
        digest = expect_sha256(record.get("sha256"), f"{path}.sha256")
        artifact_type, replicate, bundle_id, stage, call_role = _expected_inventory_metadata(relative_path)
        expect_equal(record.get("artifact_type"), artifact_type, f"{path}.artifact_type")
        expect_equal(record.get("replicate"), replicate, f"{path}.replicate")
        expect_equal(record.get("bundle_id"), bundle_id, f"{path}.bundle_id")
        expect_equal(record.get("stage"), stage, f"{path}.stage")
        expect_equal(record.get("call_role"), call_role, f"{path}.call_role")
        paths.append(relative_path)
        serialized.append(f"{relative_path}\t{size}\t{digest}")
        counts[artifact_type] = counts.get(artifact_type, 0) + 1
    if paths != sorted(paths) or len(set(paths)) != len(paths):
        fail("evidence_inventory.files: paths must be unique and sorted")
    inventory_digest = hashlib.sha256(("\n".join(serialized) + "\n").encode("utf-8")).hexdigest()
    expect_equal(inventory.get("inventory_sha256"), inventory_digest, "evidence_inventory.inventory_sha256")
    path_set_digest = hashlib.sha256(("\n".join(paths) + "\n").encode("utf-8")).hexdigest()
    expect_equal(inventory.get("path_set_sha256"), path_set_digest, "evidence_inventory.path_set_sha256")
    expect_equal(inventory_digest, EXPECTED_INVENTORY_SHA256, "computed evidence inventory digest")
    expect_equal(path_set_digest, EXPECTED_PATH_SET_SHA256, "computed evidence path-set digest")
    expect_equal(inventory.get("category_counts"), EXPECTED_CATEGORY_COUNTS, "evidence_inventory.category_counts")
    expect_equal(counts, EXPECTED_CATEGORY_COUNTS, "computed evidence category counts")
    return set(paths)


def _row(rows: list[dict[str, Any]], replicate: str, bundle_id: str) -> dict[str, Any]:
    matches = [item for item in rows if item.get("replicate") == replicate and item.get("bundle_id") == bundle_id]
    if len(matches) != 1:
        fail(f"rows: expected exactly one row for {replicate}/{bundle_id}")
    return matches[0]


def _expected_row_contract(replicate: str, bundle_id: str) -> dict[str, Any]:
    contract: dict[tuple[str, str], dict[str, Any]] = {
        ("A", "B0001"): {"outcome":"EXTRACTION_FAILURE","node":"r2","field":"arg1/arg2","support":"SOURCE_INSUFFICIENT_TO_DECIDE","existing":None,"locators":[],"classification":"CANDIDATE_OR_CLAIMIR_VALIDATION_FAILURE","subtype":"DECISION_RECONSTRUCTION_PRE_CANDIDATE_VALIDATION_FAILURE","confidence":None,"probabilities":None,"preceding":{"r2__active":"yes","r2__kind":"maps_to"}},
        ("B", "B0001"): {"outcome":"EXTRACTION_FAILURE","node":"r2","field":"arg1/arg2","support":"SOURCE_INSUFFICIENT_TO_DECIDE","existing":None,"locators":[],"classification":"CANDIDATE_OR_CLAIMIR_VALIDATION_FAILURE","subtype":"DECISION_RECONSTRUCTION_PRE_CANDIDATE_VALIDATION_FAILURE","confidence":None,"probabilities":None,"preceding":{"r2__active":"yes","r2__kind":"maps_to"}},
        ("A", "B0002"): {"outcome":"EXTRACTION_ABSTAIN","node":"n1","field":"n1__active","support":"SOURCE_SUPPORTS_EXISTING_CHOICE","existing":"yes","locators":["s1","s5"],"classification":"UNDERDETERMINED","confidence":0.2081,"probabilities":{"__unresolved__":0.5719,"no":0.3601,"yes":0.0679},"preceding":{"claim_type":"definition","modality":"descriptive"}},
        ("B", "B0002"): {"outcome":"EXTRACTION_ABSTAIN","node":"n1","field":"n1__active","support":"SOURCE_SUPPORTS_EXISTING_CHOICE","existing":"yes","locators":["s1","s5"],"classification":"UNDERDETERMINED","confidence":0.9154,"probabilities":{"__unresolved__":0.9814,"no":0.0186,"yes":0.0},"preceding":{"claim_type":"definition","modality":"descriptive"}},
        ("A", "B0003"): {"outcome":"EXTRACTION_ABSTAIN","node":"n1","field":"n1__active","support":"SOURCE_SUPPORTS_EXISTING_CHOICE","existing":"yes","locators":["s1","s3"],"classification":"UNDERDETERMINED","confidence":0.3616,"probabilities":{"__unresolved__":0.5438,"no":0.4544,"yes":0.0018},"preceding":{"claim_type":"definition","modality":"definitional"}},
        ("B", "B0003"): {"outcome":"EXTRACTION_ABSTAIN","node":"n1","field":"n1__role","support":"SOURCE_SUPPORTS_EXISTING_CHOICE","existing":"available_information","locators":["s1","s3"],"classification":"UNDERDETERMINED","confidence":0.8607,"probabilities":{"__unresolved__":0.9052,"available_information":0.0936,"condition":0.0002,"criterion":0.0001,"intervention":0.0001,"other":0.0,"partition":0.0,"probe":0.0,"response_or_outcome":0.0007,"state_or_structure":0.0},"preceding":{"claim_type":"definition","modality":"definitional","n1__active":"yes","n1__anchor":"s1","n1__grounding":"explicit"}},
        ("A", "B0004"): {"outcome":"EXTRACTION_ABSTAIN","node":"n1","field":"n1__active","support":"SOURCE_SUPPORTS_EXISTING_CHOICE","existing":"yes","locators":["s3","s4","s5"],"classification":"UNDERDETERMINED","confidence":0.1819,"probabilities":{"__unresolved__":0.6399,"no":0.2079,"yes":0.1522},"preceding":{"claim_type":"definition","modality":"definitional"}},
        ("B", "B0004"): {"outcome":"EXTRACTION_ABSTAIN","node":"n1","field":"n1__role","support":"SOURCE_INSUFFICIENT_TO_DECIDE","existing":None,"locators":["s3","s4","s5"],"classification":"SOURCE_INSUFFICIENT","confidence":0.9328,"probabilities":{"__unresolved__":0.9666,"available_information":0.0318,"condition":0.0005,"criterion":0.0008,"intervention":0.0,"other":0.0,"partition":0.0,"probe":0.0,"response_or_outcome":0.0002,"state_or_structure":0.0002},"preceding":{"claim_type":"definition","modality":"definitional","n1__active":"yes","n1__grounding":"explicit"}},
        ("A", "B0005"): {"outcome":"EXTRACTION_ABSTAIN","node":"scope__temporal_scope","field":"scope__temporal_scope__s1","support":"SOURCE_SUPPORTS_EXISTING_CHOICE","existing":"no","locators":["s1"],"classification":"UNDERDETERMINED","confidence":0.3868,"probabilities":{"__unresolved__":0.5983,"no":0.4017,"yes":0.0},"preceding":{"claim_type":"constraint","modality":"descriptive"}},
        ("B", "B0005"): {"outcome":"EXTRACTION_ABSTAIN","node":"scope__temporal_scope","field":"scope__temporal_scope__s1","support":"SOURCE_SUPPORTS_EXISTING_CHOICE","existing":"no","locators":["s1"],"classification":"UNDERDETERMINED","confidence":0.9864,"probabilities":{"__unresolved__":0.9979,"no":0.0021,"yes":0.0},"preceding":{"claim_type":"constraint","modality":"descriptive"}},
    }
    return contract[(replicate, bundle_id)]


def validate_probability_map(value: Any, path: str) -> None:
    probabilities = expect_dict(value, path)
    if not probabilities:
        fail(f"{path}: empty probability map")
    total = 0.0
    for choice, probability in probabilities.items():
        expect_string(choice, f"{path}.{choice}")
        expect_number_01(probability, f"{path}.{choice}")
        total += float(probability)
    if abs(total - 1.0) > 0.002:
        fail(f"{path}: probabilities do not sum to one after rounding: {total}")


def validate_rows(value: Any, inventory_paths: set[str]) -> None:
    rows = expect_list(value, "rows")
    if len(rows) != 10:
        fail("rows: expected exactly ten A/B x B0001..B0005 records")
    seen: set[tuple[str, str]] = set()
    for index, raw in enumerate(rows):
        path = f"rows[{index}]"
        record = expect_dict(raw, path)
        replicate = expect_string(record.get("replicate"), f"{path}.replicate")
        bundle_id = expect_string(record.get("bundle_id"), f"{path}.bundle_id")
        if replicate not in {"A", "B"} or bundle_id not in EXPECTED_BUNDLE_SHA256:
            fail(f"{path}: unexpected replicate/bundle")
        key = (replicate, bundle_id)
        if key in seen:
            fail(f"{path}: duplicate replicate/bundle")
        seen.add(key)
        expected = _expected_row_contract(replicate, bundle_id)
        expect_equal(record.get("masked_bundle_sha256"), EXPECTED_BUNDLE_SHA256[bundle_id], f"{path}.masked_bundle_sha256")
        for field in ("original_outcome", "node", "field", "source_support_class", "source_supported_existing_choice", "source_locator_ids", "postmortem_class", "preceding_resolved_decisions"):
            expect_equal(record.get(field), expected[{
                "original_outcome":"outcome",
                "source_support_class":"support",
                "source_supported_existing_choice":"existing",
                "source_locator_ids":"locators",
                "postmortem_class":"classification",
                "preceding_resolved_decisions":"preceding",
            }.get(field, field)], f"{path}.{field}")
        expect_bool(record.get("active_required"), f"{path}.active_required")
        subsequent = expect_list(record.get("subsequent_wire_fields_not_semantically_evaluated"), f"{path}.subsequent_wire_fields_not_semantically_evaluated")
        if expected["outcome"] == "EXTRACTION_FAILURE":
            if subsequent:
                fail(f"{path}.subsequent_wire_fields_not_semantically_evaluated: failure row must be empty")
        elif not subsequent:
            fail(f"{path}.subsequent_wire_fields_not_semantically_evaluated: abstention row must preserve later fields")
        choice_or_failure = expect_dict(record.get("choice_or_failure"), f"{path}.choice_or_failure")
        if expected["outcome"] == "EXTRACTION_FAILURE":
            expect_equal(record.get("earliest_decisive_stage"), "post_parse_systemone_deterministic_decision_reconstruction", f"{path}.earliest_decisive_stage")
            expect_equal(choice_or_failure, {"relation":"r2","kind":"maps_to","arg1":"n1","arg2":"n1","failure_id":"DUPLICATE_RELATION_ARGUMENTS_FORBIDDEN","failure_message":"duplicate relation arguments are forbidden"}, f"{path}.choice_or_failure")
            expect_equal(record.get("postmortem_subtype"), expected["subtype"], f"{path}.postmortem_subtype")
            expect_equal(record.get("confidence"), None, f"{path}.confidence")
            expect_equal(record.get("probability_profile"), None, f"{path}.probability_profile")
        else:
            expect_equal(choice_or_failure, {"choice":"__unresolved__"}, f"{path}.choice_or_failure")
            expect_equal(record.get("earliest_decisive_stage"), "post_parse_systemone_decision_reconstruction", f"{path}.earliest_decisive_stage")
            expect_number_01(record.get("confidence"), f"{path}.confidence")
            expect_equal(record.get("confidence"), expected["confidence"], f"{path}.confidence")
            validate_probability_map(record.get("probability_profile"), f"{path}.probability_profile")
            expect_equal(record.get("probability_profile"), expected["probabilities"], f"{path}.probability_profile")
            if "postmortem_subtype" in record:
                fail(f"{path}.postmortem_subtype: only B0001 has a refined subtype")
        expect_bool(record.get("candidate_created"), f"{path}.candidate_created", False)
        expect_bool(record.get("claimir_created"), f"{path}.claimir_created", False)
        if record.get("source_support_class") not in SOURCE_SUPPORT_CLASSES:
            fail(f"{path}.source_support_class: unknown source support class")
        if not isinstance(record.get("source_locator_ids"), list):
            fail(f"{path}.source_locator_ids: expected array")
        refs = expect_list(record.get("evidence_refs"), f"{path}.evidence_refs")
        expected_refs = [
            f"{replicate}/{bundle_id}/artifact-record.json",
            f"{replicate}/{bundle_id}/normal-output.txt",
            f"{replicate}/{bundle_id}/normal-request.json",
            f"{replicate}/{bundle_id}/normal-response.json",
            f"{replicate}/{bundle_id}/source-bundle.json",
            f"{replicate}/{bundle_id}/systemone-answers.json",
            f"{replicate}/{bundle_id}/systemone-request.json",
            f"{replicate}/{bundle_id}/systemone-response.json",
        ]
        expect_equal(refs, expected_refs, f"{path}.evidence_refs")
        if not set(refs).issubset(inventory_paths):
            fail(f"{path}.evidence_refs: reference absent from inventory")
    expected_keys = {(replicate, bundle_id) for replicate in ("A", "B") for bundle_id in EXPECTED_BUNDLE_SHA256}
    expect_equal(seen, expected_keys, "rows.replicate_bundle_set")


def validate_transaction_integrity(value: Any) -> None:
    integrity = expect_dict(value, "transaction_integrity")
    expected = {
        "launcher_invocations": 1,
        "server_launches": 2,
        "normal_attempted": 10,
        "normal_completed": 10,
        "systemone_attempted": 10,
        "systemone_completed": 10,
        "scientific_calls_attempted": 20,
        "scientific_calls_completed": 20,
        "retry": 0,
        "replay": 0,
        "fallback": 0,
        "repair": 0,
        "valid_claim_ir": 0,
        "extraction_abstain": 8,
        "extraction_failure": 2,
    }
    for key, expected_value in expected.items():
        expect_equal(integrity.get(key), expected_value, f"transaction_integrity.{key}")
    expect_equal(integrity.get("response_contracts"), {"pass": 20, "total": 20}, "transaction_integrity.response_contracts")
    expect_bool(integrity.get("source_digests_exact"), "transaction_integrity.source_digests_exact")
    expect_bool(integrity.get("observed_transport_runtime_serialization_failure"), "transaction_integrity.observed_transport_runtime_serialization_failure", False)
    expect_bool(integrity.get("candidate_created"), "transaction_integrity.candidate_created", False)
    expect_bool(integrity.get("claimir_created"), "transaction_integrity.claimir_created", False)
    expect_bool(integrity.get("separate_server_log_files"), "transaction_integrity.separate_server_log_files", False)
    expect_bool(integrity.get("missing_server_logs_are_apparatus_defect"), "transaction_integrity.missing_server_logs_are_apparatus_defect", False)
    isolation = expect_dict(integrity.get("a_b_process_isolation"), "transaction_integrity.a_b_process_isolation")
    expect_equal(isolation.get("A"), {"pid":463537,"owned_process":True,"started_at":"2026-09-25T08:55:26Z","completed_at":"2026-09-25T08:57:29Z","cleanup_exit":0}, "transaction_integrity.a_b_process_isolation.A")
    expect_equal(isolation.get("B"), {"pid":463826,"owned_process":True,"started_at":"2026-09-25T08:57:29Z","completed_at":"2026-09-25T08:59:32Z","cleanup_exit":0}, "transaction_integrity.a_b_process_isolation.B")
    expect_bool(isolation.get("distinct_owned_process_lifetimes"), "transaction_integrity.a_b_process_isolation.distinct_owned_process_lifetimes")


def validate_pairs(value: Any) -> None:
    pairs = expect_list(value, "pair_reproducibility")
    if len(pairs) != 5:
        fail("pair_reproducibility: expected exactly five pairs")
    expected_levels = {
        "B0001": "DECISIVE_CHOICE_REPRODUCIBLE",
        "B0002": "DECISIVE_CHOICE_REPRODUCIBLE",
        "B0003": "OUTCOME_CLASS_REPRODUCIBLE",
        "B0004": "OUTCOME_CLASS_REPRODUCIBLE",
        "B0005": "DECISIVE_CHOICE_REPRODUCIBLE",
    }
    seen: set[str] = set()
    for index, raw in enumerate(pairs):
        path = f"pair_reproducibility[{index}]"
        pair = expect_dict(raw, path)
        bundle_id = expect_string(pair.get("bundle_id"), f"{path}.bundle_id")
        if bundle_id in seen or bundle_id not in expected_levels:
            fail(f"{path}.bundle_id: unexpected or duplicate bundle")
        seen.add(bundle_id)
        outcome = "EXTRACTION_FAILURE" if bundle_id == "B0001" else "EXTRACTION_ABSTAIN"
        expect_equal(pair.get("a_outcome"), outcome, f"{path}.a_outcome")
        expect_equal(pair.get("b_outcome"), outcome, f"{path}.b_outcome")
        expect_bool(pair.get("same_masked_bundle_digest"), f"{path}.same_masked_bundle_digest")
        expect_bool(pair.get("same_decisive_node"), f"{path}.same_decisive_node")
        expect_equal(pair.get("same_decisive_field"), bundle_id in {"B0001", "B0002", "B0005"}, f"{path}.same_decisive_field")
        expect_bool(pair.get("same_choice_or_failure"), f"{path}.same_choice_or_failure")
        expect_equal(pair.get("reproducibility"), expected_levels[bundle_id], f"{path}.reproducibility")
    expect_equal(seen, set(expected_levels), "pair_reproducibility.bundle_set")


def validate_denominator(value: Any) -> None:
    denominator = expect_dict(value, "denominator_accounting")
    expect_equal(denominator.get("selected_attempts"), 10, "denominator_accounting.selected_attempts")
    expect_equal(denominator.get("valid_claim_ir"), 0, "denominator_accounting.valid_claim_ir")
    expect_equal(denominator.get("extraction_abstain"), 8, "denominator_accounting.extraction_abstain")
    expect_equal(denominator.get("extraction_failure"), 2, "denominator_accounting.extraction_failure")
    expect_equal(denominator.get("primary_analyzable_denominator"), 0, "denominator_accounting.primary_analyzable_denominator")
    expect_equal(denominator.get("both_valid"), {"count": 0, "denominator": 5}, "denominator_accounting.both_valid")
    expect_equal(denominator.get("residual_conversions"), 0, "denominator_accounting.residual_conversions")
    expect_equal(denominator.get("replacement_or_erasure"), 0, "denominator_accounting.replacement_or_erasure")


def validate_artifact(value: Any) -> dict[str, Any]:
    root = expect_dict(value, "root")
    walk_forbidden_keys(root)
    validate_all_hash_fields(root)
    expect_equal(root.get("schema_version"), SCHEMA_VERSION, "schema_version")
    expect_equal(root.get("owner_issue"), 197, "owner_issue")
    expect_equal(root.get("parent_transaction_issue"), 193, "parent_transaction_issue")
    expect_equal(root.get("status"), "TERMINAL_RECONCILED", "status")
    expect_equal(root.get("architecture_consequence"), "NONE", "architecture_consequence")
    validate_authority(root.get("authority"))
    validate_provenance(root.get("provenance"))
    inventory_paths = validate_inventory(root.get("evidence_inventory"))
    validate_transaction_integrity(root.get("transaction_integrity"))
    validate_rows(root.get("rows"), inventory_paths)
    validate_pairs(root.get("pair_reproducibility"))
    global_repro = expect_dict(root.get("global_reproducibility"), "global_reproducibility")
    expect_equal(global_repro.get("strongest_earned"), "OUTCOME_CLASS_REPRODUCIBLE", "global_reproducibility.strongest_earned")
    expect_equal(global_repro.get("global_ceiling"), "OUTCOME_CLASS_REPRODUCIBLE", "global_reproducibility.global_ceiling")
    expect_equal(global_repro.get("forbidden_stronger_global_claims"), ["DECISIVE_FIELD_REPRODUCIBLE","DECISIVE_CHOICE_REPRODUCIBLE","SOURCE_ONLY_CAUSAL_CLASS_REPRODUCIBLE"], "global_reproducibility.forbidden_stronger_global_claims")
    comparison = expect_dict(root.get("comparison_to_issue_189"), "comparison_to_issue_189")
    expect_bool(comparison.get("same_frozen_B0002_bundle_digest"), "comparison_to_issue_189.same_frozen_B0002_bundle_digest")
    expect_equal(comparison.get("B0002_masked_bundle_sha256"), EXPECTED_BUNDLE_SHA256["B0002"], "comparison_to_issue_189.B0002_masked_bundle_sha256")
    expect_equal(comparison.get("issue_189"), {"comment_id":5828524456,"decisive_field":"n1__role","choice":"__unresolved__"}, "comparison_to_issue_189.issue_189")
    expect_equal(comparison.get("issue_193_A"), {"decisive_field":"n1__active","choice":"__unresolved__"}, "comparison_to_issue_189.issue_193_A")
    expect_equal(comparison.get("issue_193_B"), {"decisive_field":"n1__active","choice":"__unresolved__"}, "comparison_to_issue_189.issue_193_B")
    expect_equal(comparison.get("same_node_family"), "n1", "comparison_to_issue_189.same_node_family")
    expect_equal(comparison.get("same_unresolved_pattern"), "partial", "comparison_to_issue_189.same_unresolved_pattern")
    expect_bool(comparison.get("same_decisive_field"), "comparison_to_issue_189.same_decisive_field", False)
    expect_bool(comparison.get("exact_issue_189_decisive_role_event_reproduced"), "comparison_to_issue_189.exact_issue_189_decisive_role_event_reproduced", False)
    expect_bool(comparison.get("broader_source_backed_underdetermination_pressure_partially_reproduced"), "comparison_to_issue_189.broader_source_backed_underdetermination_pressure_partially_reproduced")
    expect_bool(comparison.get("masking_not_causal_pressure_remains_compatible"), "comparison_to_issue_189.masking_not_causal_pressure_remains_compatible")
    expect_bool(comparison.get("issue_189_is_answer_key"), "comparison_to_issue_189.issue_189_is_answer_key", False)
    validate_denominator(root.get("denominator_accounting"))
    grand_null = expect_dict(root.get("grand_null"), "grand_null")
    expect_equal(grand_null.get("status"), "NOT_DESTROYED", "grand_null.status")
    expect_bool(grand_null.get("apparatus_defect_supported"), "grand_null.apparatus_defect_supported", False)
    classification = expect_dict(root.get("classification"), "classification")
    expect_equal(classification.get("scientific_subclassification"), "ZERO_YIELD_EXPLAINED_BY_MIXED_EXTRACTION_BOUNDARIES", "classification.scientific_subclassification")
    expect_equal(classification.get("terminal_owner_classification"), "ZERO_YIELD_POSTMORTEM_UNDERDETERMINED", "classification.terminal_owner_classification")
    future = expect_dict(root.get("next_step_boundary"), "next_step_boundary")
    expect_equal(future.get("scientifically_plausible_future_owners"), ["SYNTHETIC_FIRST_ROLE_SCOPE_DECISION_SURFACE_AUDIT","INDEPENDENT_EXTRACTION_INSTRUMENT_COMPARISON"], "next_step_boundary.scientifically_plausible_future_owners")
    expect_equal(future.get("preference_or_ranking"), None, "next_step_boundary.preference_or_ranking")
    for key in ("new_real_scientific_transaction_created", "new_real_scientific_transaction_authorized", "new_real_scientific_transaction_executed"):
        expect_bool(future.get(key), f"next_step_boundary.{key}", False)
    accounting = expect_dict(root.get("postmortem_accounting"), "postmortem_accounting")
    for key in ("new_model_calls","new_llama_server_launches","new_normal_calls","new_systemone_calls","retry","replay","fallback","repair","source_regeneration","remask","paper2_167_execution"):
        expect_equal(accounting.get(key), 0, f"postmortem_accounting.{key}")
    return root


def expect_failure(callback: Callable[[], Any], label: str) -> None:
    try:
        callback()
    except ContractError:
        return
    fail(f"self-test {label}: expected validation failure")


def find_row(root: dict[str, Any], replicate: str, bundle_id: str) -> dict[str, Any]:
    rows = expect_list(root.get("rows"), "rows")
    return _row(rows, replicate, bundle_id)


def self_test(path: Path) -> None:
    artifact = load_json(path)
    validate_artifact(artifact)

    mutated = copy.deepcopy(artifact)
    find_row(mutated, "A", "B0002")["original_outcome"] = "VALID_CLAIM_IR"
    expect_failure(lambda: validate_artifact(mutated), "original outcome mutation")

    mutated = copy.deepcopy(artifact)
    find_row(mutated, "B", "B0003")["field"] = "n1__active"
    expect_failure(lambda: validate_artifact(mutated), "decisive field mutation")

    mutated = copy.deepcopy(artifact)
    find_row(mutated, "A", "B0002")["probability_profile"]["yes"] = 0.5
    expect_failure(lambda: validate_artifact(mutated), "probability map mutation")

    mutated = copy.deepcopy(artifact)
    find_row(mutated, "B", "B0004")["source_support_class"] = "SOURCE_SUPPORTS_EXISTING_CHOICE"
    expect_failure(lambda: validate_artifact(mutated), "B/B0004 source-support mutation")

    mutated = copy.deepcopy(artifact)
    next(pair for pair in mutated["pair_reproducibility"] if pair["bundle_id"] == "B0003")["reproducibility"] = "DECISIVE_CHOICE_REPRODUCIBLE"
    expect_failure(lambda: validate_artifact(mutated), "pair reproducibility mutation")

    mutated = copy.deepcopy(artifact)
    mutated["global_reproducibility"]["strongest_earned"] = "DECISIVE_FIELD_REPRODUCIBLE"
    expect_failure(lambda: validate_artifact(mutated), "global reproducibility mutation")

    mutated = copy.deepcopy(artifact)
    mutated["denominator_accounting"]["primary_analyzable_denominator"] = 1
    expect_failure(lambda: validate_artifact(mutated), "denominator mutation")

    mutated = copy.deepcopy(artifact)
    mutated["denominator_accounting"]["residual_conversions"] = 1
    expect_failure(lambda: validate_artifact(mutated), "RESIDUAL conversion mutation")

    mutated = copy.deepcopy(artifact)
    mutated["grand_null"]["status"] = "DESTROYED"
    expect_failure(lambda: validate_artifact(mutated), "Grand Null mutation")

    mutated = copy.deepcopy(artifact)
    mutated["grand_null"]["apparatus_defect_supported"] = True
    expect_failure(lambda: validate_artifact(mutated), "apparatus defect mutation")

    mutated = copy.deepcopy(artifact)
    mutated["classification"]["terminal_owner_classification"] = "ZERO_YIELD_POSTMORTEM_QUALIFIED"
    expect_failure(lambda: validate_artifact(mutated), "terminal classification mutation")

    mutated = copy.deepcopy(artifact)
    mutated["raw_source_text"] = "source passage must not be committed"
    expect_failure(lambda: validate_artifact(mutated), "raw source-text insertion")

    mutated = copy.deepcopy(artifact)
    mutated["evidence_inventory"]["inventory_sha256"] = "0" * 64
    expect_failure(lambda: validate_artifact(mutated), "inventory digest mutation")

    mutated = copy.deepcopy(artifact)
    mutated["evidence_inventory"]["files"][0]["sha256"] = "0" * 64
    expect_failure(lambda: validate_artifact(mutated), "evidence file digest mutation")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ARTIFACT_PATH)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            self_test(args.input)
            print("PAPER2_EXTRACTION_ZERO_YIELD_POSTMORTEM_V1_SELFTEST_PASS")
        else:
            validate_artifact(load_json(args.input))
            print("PAPER2_EXTRACTION_ZERO_YIELD_POSTMORTEM_V1_VALID")
    except ContractError as exc:
        print(f"PAPER2_EXTRACTION_ZERO_YIELD_POSTMORTEM_V1_FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
