#!/usr/bin/env python3
"""Paper 2 #210 prospective real SystemOne-v3 calibration runner.

The runner is a new versioned surface.  It imports stable low-level transport /
source-freeze helpers from the consumed #193 v2 runner but never mutates or
replays that historical transaction.  Real execution requires a separate
read-back authorization.  --attest-only performs zero model calls.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import socket
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import paper2_extraction_two_pass_llama_cpp_transaction_v2 as base
import paper2_extraction_two_pass_systemone_v3 as v3
from paper2_claim_ir_compare import compare as compare_claim_ir
from paper2_claim_ir_validate import ValidationError, validate as validate_claim_ir
from paper2_extraction_bundle_prepare import canonical_json_bytes
from paper2_extraction_procedure_validate import ContractError

OWNER_ISSUE = 210
MANIFEST_VERSION = "paper2-v3-real-calibration-transaction-v1"
RECEIPT_VERSION = "paper2-v3-real-calibration-transaction-receipt-v1"
SUMMARY_VERSION = "paper2-v3-real-calibration-transaction-summary-v1"
MANIFEST_PATH = Path("research/paper2/extraction_v3_real_calibration_transaction_v1.json")
RUNNER_PATH = Path("scripts/paper2_extraction_two_pass_llama_cpp_transaction_v3.py")
SYSTEMONE_ROUTE = "/v1/systemone"
UNSCHEDULED_TERMINAL = "NOT_SCHEDULED_AFTER_TERMINAL_BUNDLE_OUTCOME"
UNSCHEDULED_NO_RELATIONS = "NOT_SCHEDULED_NO_ACTIVE_RELATIONS"

EXPECTED_BUNDLES = base.EXPECTED_BUNDLES
EXPECTED_SAMPLE_IDS = base.EXPECTED_SAMPLE_IDS


class V3TransactionError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise V3TransactionError(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise V3TransactionError(f"could not load JSON {path}: {exc}") from exc


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def require_manifest(manifest_path: Path, repo_root: Path) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    if manifest.get("schema_version") != MANIFEST_VERSION:
        fail("transaction manifest schema drift")
    if manifest.get("owner_issue") != OWNER_ISSUE:
        fail("transaction manifest owner drift")
    if manifest.get("status") != "PREPARATION_ONLY_NOT_SCIENTIFICALLY_AUTHORIZED":
        fail("transaction manifest status drift")
    if manifest.get("scientific_transaction_authorized") is not False:
        fail("manifest must not self-authorize scientific execution")
    for field in (
        "paper167_execution_authorized",
        "heldout_execution_authorized",
        "basis_decomposition_authorized",
        "null_execution_authorized",
    ):
        if manifest.get(field) is not False:
            fail(f"downstream authority drift: {field}")
    if manifest.get("architecture_consequence") != "NONE":
        fail("architecture consequence drift")

    topology = manifest.get("topology", {})
    expected_topology = {
        "replicates": ["A", "B"],
        "server_launches_exact": 2,
        "normal_calls_exact": 10,
        "systemone_calls_min": 10,
        "systemone_calls_max": 30,
        "total_model_calls_min": 20,
        "total_model_calls_max": 40,
        "stages_max": 3,
        "stage_order": [1, 2, 3],
        "later_stage_after_terminal_bundle_outcome": False,
        "unscheduled_stage_marker": UNSCHEDULED_TERMINAL,
    }
    if topology != expected_topology:
        fail("variable-call topology drift")
    if manifest.get("bundle_outcomes") != [
        "VALID_CLAIM_IR",
        "EXTRACTION_ABSTAIN",
        "EXTRACTION_FAILURE",
    ]:
        fail("bundle outcome vocabulary drift")
    guards = manifest.get("execution_guards", {})
    for field in ("retry", "replay", "fallback", "repair", "replacement"):
        if guards.get(field) != 0:
            fail(f"execution guard drift: {field}")
    for field in (
        "fresh_owned_process_per_replicate",
        "cross_replicate_visibility_forbidden",
        "cache_reuse_across_replicates_forbidden",
        "new_nonexistent_evidence_root_required",
        "authorization_comment_readback_required",
    ):
        if guards.get(field) is not True:
            fail(f"execution guard drift: {field}")

    historical = manifest.get("historical_v2", {})
    if historical != {
        "transaction_issue": 193,
        "runner_must_remain_byte_identical": True,
        "outcomes": {
            "VALID_CLAIM_IR": 0,
            "EXTRACTION_ABSTAIN": 8,
            "EXTRACTION_FAILURE": 2,
        },
    }:
        fail("historical #193 provenance drift")

    bound = manifest.get("bound_repository_blobs")
    if not isinstance(bound, dict) or not bound:
        fail("bound repository blobs missing")
    for rel, expected in bound.items():
        path = repo_root / rel
        if not path.is_file():
            fail(f"bound parent missing: {rel}")
        actual = git_blob_sha(path.read_bytes())
        if actual != expected:
            fail(f"bound parent blob changed: {rel}: {actual} != {expected}")

    # Re-run the synthetic v3 contract/schema validators against the committed
    # #203 files.  This does not authorize any real model call.
    v3.validate_manifest(load_json(repo_root / "research/paper2/extraction_two_pass_systemone_v3.json"))
    v3.validate_schema(load_json(repo_root / "research/paper2/extraction_systemone_decision_v3.schema.json"))
    return manifest


def verify_authorization(
    *,
    repo_root: Path,
    evidence_root: Path,
    manifest: dict[str, Any],
    comment_id: int | None,
    status: str | None,
    authorized_head: str | None,
    authorized_tree: str | None,
    authorized_runner_blob: str | None,
    authorized_manifest_blob: str | None,
    authorized_v3_schema_blob: str | None,
    authorized_v3_contract_blob: str | None,
    authorized_v3_compiler_blob: str | None,
    authorized_claim_ir_blob: str | None,
    authorized_evidence_root: str | None,
) -> dict[str, Any]:
    if comment_id is None or comment_id <= 0:
        fail("#210 authorization comment ID is required")
    if status != "SCIENTIFIC_TRANSACTION_AUTHORIZED_UNSPENT":
        fail("#210 authorization status is missing or not exact")
    head = base.run_text(["git", "rev-parse", "HEAD"], cwd=repo_root).strip()
    tree = base.run_text(["git", "rev-parse", "HEAD^{tree}"], cwd=repo_root).strip()
    if authorized_head != head or authorized_tree != tree:
        fail("authorization HEAD/tree does not match execution checkout")

    def blob(rel: str) -> str:
        return base.run_text(["git", "rev-parse", f"HEAD:{rel}"], cwd=repo_root).strip()

    runner_blob = blob(str(RUNNER_PATH))
    manifest_blob = blob(str(MANIFEST_PATH))
    if authorized_runner_blob != runner_blob:
        fail("authorization runner blob mismatch")
    if authorized_manifest_blob != manifest_blob:
        fail("authorization transaction-manifest blob mismatch")

    bound = manifest["bound_repository_blobs"]
    checks = {
        "research/paper2/extraction_systemone_decision_v3.schema.json": authorized_v3_schema_blob,
        "research/paper2/extraction_two_pass_systemone_v3.json": authorized_v3_contract_blob,
        "scripts/paper2_extraction_two_pass_systemone_v3.py": authorized_v3_compiler_blob,
        "research/paper2/claim_ir_v1.schema.json": authorized_claim_ir_blob,
    }
    for rel, supplied in checks.items():
        current = blob(rel)
        if current != bound[rel] or supplied != current:
            fail(f"authorization bound blob mismatch: {rel}")

    if authorized_evidence_root is None:
        fail("authorization evidence root is required")
    if Path(authorized_evidence_root).expanduser().resolve() != evidence_root.resolve():
        fail("authorization evidence root mismatch")
    return {
        "comment_id": comment_id,
        "status": status,
        "head": head,
        "tree": tree,
        "runner_blob": runner_blob,
        "manifest_blob": manifest_blob,
        "v3_schema_blob": checks["research/paper2/extraction_systemone_decision_v3.schema.json"],
        "v3_contract_blob": checks["research/paper2/extraction_two_pass_systemone_v3.json"],
        "v3_compiler_blob": checks["scripts/paper2_extraction_two_pass_systemone_v3.py"],
        "claim_ir_blob": checks["research/paper2/claim_ir_v1.schema.json"],
        "evidence_root": str(evidence_root.resolve()),
    }


def validate_real_envelope(
    *,
    repo_root: Path,
    manifest_path: Path,
    protocol_path: Path,
    prompt_path: Path,
    mask_terms_path: Path,
    preprocessing_freeze_path: Path,
    bundle_dir: Path,
    package_path: Path,
    provenance_path: Path,
    llama_root: Path,
    server_binary: Path,
    model_path: Path,
    evidence_root: Path,
    port: int,
    require_gpu: bool,
    require_authorization: bool,
    authorization: dict[str, Any],
) -> dict[str, Any]:
    base.require_new_evidence_root(evidence_root, repo_root)
    relay_head, relay_tree = base.require_clean_git_checkout(
        repo_root, label="RelayTheory checkout"
    )
    manifest = require_manifest(manifest_path, repo_root)

    prompt_bytes = prompt_path.read_bytes()
    protocol = base.validate_protocol(
        load_json(protocol_path), prompt_bytes, synthetic=False
    )
    frozen = manifest["frozen_surface"]
    if sha256_bytes(prompt_bytes) != frozen["normal_prompt_sha256"]:
        fail("Normal prompt digest differs from #210 freeze")
    if sha256_file(mask_terms_path) != frozen["mask_authority_sha256"]:
        fail("mask authority digest differs from #210 freeze")
    if sha256_file(preprocessing_freeze_path) != frozen["preprocessing_sha256"]:
        fail("preprocessing freeze digest differs from #210 freeze")

    freeze = load_json(preprocessing_freeze_path)
    entries, bundle_raw, bundles = base.validate_freeze_and_bundles(
        freeze,
        bundle_dir,
        mask_terms_path=mask_terms_path,
        freeze_path=preprocessing_freeze_path,
        synthetic=False,
    )
    if list(EXPECTED_BUNDLES) != frozen["bundle_order"]:
        fail("bundle order differs from #210 manifest")
    if list(EXPECTED_SAMPLE_IDS) != frozen["sample_ids"]:
        fail("sample identity differs from #210 manifest")
    for bundle_id in EXPECTED_BUNDLES:
        observed = sha256_bytes(bundle_raw[bundle_id])
        if observed != frozen["prepared_bundle_sha256"][bundle_id]:
            fail(f"{bundle_id}: prepared bundle SHA-256 differs from #210 freeze")

    package_by_bundle, provenance_by_bundle = base.validate_package_and_provenance(
        load_json(package_path),
        load_json(provenance_path),
        freeze_entries=entries,
    )

    runtime_manifest = manifest["runtime"]
    runtime_protocol = protocol["systemone"]["exact_runtime_identity"]
    for source_key, manifest_key in (
        ("repository", "repository"),
        ("revision", "revision"),
        ("tree", "tree"),
        ("version", "version"),
        ("build_number", "build_number"),
        ("binary_sha256", "binary_sha256"),
        ("model_artifact_sha256", "model_sha256"),
        ("systemone_route", "systemone_route"),
    ):
        if runtime_protocol[source_key] != runtime_manifest[manifest_key]:
            fail(f"#162/#210 runtime identity mismatch: {source_key}")
    runtime = base.verify_runtime(
        repo_root=repo_root,
        llama_root=llama_root,
        server_binary=server_binary,
        model_path=model_path,
        protocol_runtime=runtime_protocol,
        port=port,
        require_gpu=require_gpu,
        synthetic=False,
    )

    auth_result: dict[str, Any] = {"authorized": False}
    if require_authorization:
        auth_result = verify_authorization(
            repo_root=repo_root,
            evidence_root=evidence_root,
            manifest=manifest,
            **authorization,
        )
        auth_result["authorized"] = True

    base.path_outside(bundle_dir, repo_root, label="masked source bundle directory")
    base.path_outside(
        preprocessing_freeze_path, repo_root, label="preprocessing evidence"
    )
    return {
        "relaytheory": {"head": relay_head, "tree": relay_tree},
        "manifest": {
            "path": str(manifest_path),
            "sha256": sha256_file(manifest_path),
            "status": manifest["status"],
        },
        "protocol": {
            "path": str(protocol_path),
            "sha256": sha256_file(protocol_path),
            "status": protocol["status"],
        },
        "prompt": {"path": str(prompt_path), "sha256": sha256_bytes(prompt_bytes)},
        "preprocessing": {
            "freeze_path": str(preprocessing_freeze_path),
            "freeze_sha256": sha256_file(preprocessing_freeze_path),
            "mask_terms_path": str(mask_terms_path),
            "mask_terms_sha256": sha256_file(mask_terms_path),
            "bundles": [
                {
                    "bundle_id": x["bundle_id"],
                    "raw_normalized_sha256": x["raw_normalized_sha256"],
                    "masked_bundle_sha256": x["masked_bundle_sha256"],
                }
                for x in entries
            ],
        },
        "runtime": runtime,
        "authorization": auth_result,
        "package_sha256": sha256_file(package_path),
        "provenance_sha256": sha256_file(provenance_path),
        "prompt_bytes": prompt_bytes,
        "bundle_raw": bundle_raw,
        "bundles": bundles,
        "package_by_bundle": package_by_bundle,
        "provenance_by_bundle": provenance_by_bundle,
    }


def build_stage_request(
    *,
    full_source: dict[str, Any],
    focus_source: dict[str, Any],
    interpretation: str,
    model: str,
    stage: int,
    questions: dict[str, Any],
) -> dict[str, Any]:
    return {
        "model": model,
        "state": {
            "source": full_source,
            "focus_source": focus_source,
            "interpretation": interpretation,
            "authority_rule": (
                "Original source authoritative; Normal text advisory. "
                "Applicable uncertainty is __unresolved__."
            ),
            "decision_surface": v3.VERSION,
            "stage": stage,
        },
        "questions": questions,
        "cache_prompt": False,
    }


def init_stages() -> dict[str, Any]:
    return {
        str(stage): {
            "stage": stage,
            "status": "NOT_SCHEDULED_YET",
            "attempted": False,
            "completed": False,
        }
        for stage in (1, 2, 3)
    }


def mark_later_unscheduled(row: dict[str, Any], after_stage: int) -> None:
    for stage in range(after_stage + 1, 4):
        state = row["systemone"]["stages"][str(stage)]
        if state["status"] == "NOT_SCHEDULED_YET":
            state["status"] = UNSCHEDULED_TERMINAL


def stage_call(
    *,
    root: Path,
    row_root: Path,
    row: dict[str, Any],
    stage: int,
    questions: dict[str, Any],
    full_source: dict[str, Any],
    focus_source: dict[str, Any],
    interpretation: str,
    model: str,
    origin: str,
    counters: dict[str, int],
) -> dict[str, str]:
    state = row["systemone"]["stages"][str(stage)]
    if state["status"] != "NOT_SCHEDULED_YET":
        fail(f"stage {stage} scheduling state invalid")
    request = build_stage_request(
        full_source=full_source,
        focus_source=focus_source,
        interpretation=interpretation,
        model=model,
        stage=stage,
        questions=questions,
    )
    state["request"] = base.freeze_artifact(
        root,
        row_root / f"systemone-stage{stage}-request.json",
        canonical_json_bytes(request),
    )
    state["status"] = "SUBMITTED"
    state["attempted"] = True
    counters["systemone_calls_attempted"] += 1
    counters[f"stage{stage}_calls_attempted"] += 1
    try:
        raw, response = base.post_json(
            f"{origin}{SYSTEMONE_ROUTE}", request, timeout=base.HTTP_TIMEOUT_SECONDS
        )
    except Exception as exc:
        if isinstance(exc, base.HttpTransactionError) and exc.raw:
            state["response"] = base.freeze_artifact(
                root,
                row_root / f"systemone-stage{stage}-response.raw",
                exc.raw,
            )
        state["error"] = base.parse_artifact_error(exc)
        raise
    state["response"] = base.freeze_artifact(
        root,
        row_root / f"systemone-stage{stage}-response.json",
        raw,
    )
    # A wire-valid response that violates the finite response contract is a
    # transaction-integrity failure, not an extraction outcome.
    answers = v3.parse_round(
        focus_source, interpretation, model, questions, response
    )
    state["answers"] = base.freeze_artifact(
        root,
        row_root / f"systemone-stage{stage}-answers.json",
        canonical_json_bytes(answers),
    )
    state["status"] = "COMPLETED"
    state["completed"] = True
    counters["systemone_calls_completed"] += 1
    counters[f"stage{stage}_calls_completed"] += 1
    return answers


def build_claim_ir(
    *,
    bundle_id: str,
    bundle: dict[str, Any],
    candidate: dict[str, Any],
    provenance: dict[str, Any],
    extractor_identity: str,
    extractor_revision: str,
) -> dict[str, Any]:
    restored = copy.deepcopy(provenance)
    restored.pop("bundle_id", None)
    restored["source_spans"] = [
        {
            "span_id": item["span_id"],
            "locator": f"Abstract evidence unit {item['span_id']}",
        }
        for item in bundle["source_spans"]
    ]
    claim = {
        "schema_version": base.CLAIM_VERSION,
        "claim_id": bundle_id,
        "provenance": restored,
        "extraction": {
            "extractor": extractor_identity,
            "extractor_version": extractor_revision,
            "procedure_version": v3.MANIFEST_VERSION,
            "extracted_at": base.utc_now(),
            "manual_review_status": "unreviewed",
        },
        "claim_core": copy.deepcopy(candidate["claim_core"]),
    }
    try:
        validate_claim_ir(claim)
    except ValidationError as exc:
        raise V3TransactionError(
            f"{bundle_id}: full ClaimIR validation failed: {exc}"
        ) from exc
    return claim


def terminal_abstain(
    *,
    root: Path,
    row_root: Path,
    row: dict[str, Any],
    stage: int,
    exc: Exception,
    counters: dict[str, int],
) -> dict[str, Any]:
    field = str(exc).split(":", 1)[0].strip()
    row["outcome"] = "EXTRACTION_ABSTAIN"
    row["abstention"] = {
        "stage": stage,
        "field": field,
        "choice": v3.U,
        "claim_ir_conversion_forbidden": True,
        "residual_conversion_forbidden": True,
        "retry_for_resolution_forbidden": True,
    }
    row["candidate_valid"] = False
    row["claim_ir_valid"] = False
    mark_later_unscheduled(row, stage)
    counters["extraction_abstain"] += 1
    base.write_json_exclusive(row_root / "artifact-record.json", row)
    return row


def terminal_failure(
    *,
    root: Path,
    row_root: Path,
    row: dict[str, Any],
    stage: int,
    exc: Exception,
    counters: dict[str, int],
) -> dict[str, Any]:
    row["outcome"] = "EXTRACTION_FAILURE"
    row["extraction_failure"] = {
        "stage": stage,
        **base.parse_artifact_error(exc),
    }
    row["candidate_valid"] = False
    row["claim_ir_valid"] = False
    mark_later_unscheduled(row, stage)
    counters["extraction_failure"] += 1
    base.write_json_exclusive(row_root / "artifact-record.json", row)
    return row


def execute_bundle(
    *,
    root: Path,
    replicate_id: str,
    bundle_id: str,
    bundle_raw: bytes,
    bundle: dict[str, Any],
    source_digest: str,
    prompt: str,
    model: str,
    origin: str,
    provenance: dict[str, Any],
    extractor_identity: str,
    extractor_revision: str,
    counters: dict[str, int],
) -> dict[str, Any]:
    row_root = root / replicate_id / bundle_id
    row_root.mkdir(parents=True, exist_ok=False)
    row: dict[str, Any] = {
        "bundle_id": bundle_id,
        "outcome": None,
        "source_text_sha256": source_digest,
        "bundle_sha256": sha256_bytes(bundle_raw),
        "normal": {"attempted": False, "completed": False},
        "systemone": {
            "focus_span_ids": None,
            "stages": init_stages(),
        },
        "repair_count": 0,
    }
    row["bundle_artifact"] = base.freeze_artifact(
        root, row_root / "source-bundle.json", bundle_raw
    )

    normal_request = base.build_normal_request(prompt, bundle_raw, model)
    row["normal"]["request"] = base.freeze_artifact(
        root,
        row_root / "normal-request.json",
        canonical_json_bytes(normal_request),
    )
    counters["normal_calls_attempted"] += 1
    row["normal"]["attempted"] = True
    try:
        normal_raw, normal_response = base.post_json(
            f"{origin}/v1/chat/completions",
            normal_request,
            timeout=base.HTTP_TIMEOUT_SECONDS,
        )
    except Exception as exc:
        if isinstance(exc, base.HttpTransactionError) and exc.raw:
            row["normal"]["response"] = base.freeze_artifact(
                root, row_root / "normal-response.raw", exc.raw
            )
        row["normal"]["error"] = base.parse_artifact_error(exc)
        raise
    row["normal"]["response"] = base.freeze_artifact(
        root, row_root / "normal-response.json", normal_raw
    )
    interpretation = base.parse_normal_response(normal_response, model)
    row["normal"]["output"] = base.freeze_artifact(
        root,
        row_root / "normal-output.txt",
        interpretation.encode("utf-8"),
    )
    row["normal"]["completed"] = True
    counters["normal_calls_completed"] += 1

    selected = base.normal_focus_span_ids(bundle, interpretation)
    focus_source = base.compact_focus_bundle(
        bundle, selected + [base.NONE] * (3 - len(selected))
    )
    row["systemone"]["focus_span_ids"] = selected
    row["systemone"]["focus_source_sha256"] = base.canonical_digest(focus_source)

    # Stage 1.
    q1 = v3.stage1(focus_source)
    a1 = stage_call(
        root=root,
        row_root=row_root,
        row=row,
        stage=1,
        questions=q1,
        full_source=bundle,
        focus_source=focus_source,
        interpretation=interpretation,
        model=model,
        origin=origin,
        counters=counters,
    )
    try:
        q2 = v3.stage2(focus_source, a1)
    except v3.v2.DecisionUnresolved as exc:
        return terminal_abstain(
            root=root, row_root=row_root, row=row, stage=1, exc=exc, counters=counters
        )
    except (v3.v2.TwoPassV2Error, ContractError, ValidationError) as exc:
        return terminal_failure(
            root=root, row_root=row_root, row=row, stage=1, exc=exc, counters=counters
        )

    # Stage 2.
    a2 = stage_call(
        root=root,
        row_root=row_root,
        row=row,
        stage=2,
        questions=q2,
        full_source=bundle,
        focus_source=focus_source,
        interpretation=interpretation,
        model=model,
        origin=origin,
        counters=counters,
    )
    try:
        q3 = v3.stage3(focus_source, a1, a2)
    except v3.v2.DecisionUnresolved as exc:
        return terminal_abstain(
            root=root, row_root=row_root, row=row, stage=2, exc=exc, counters=counters
        )
    except (v3.v2.TwoPassV2Error, ContractError, ValidationError) as exc:
        return terminal_failure(
            root=root, row_root=row_root, row=row, stage=2, exc=exc, counters=counters
        )

    if q3:
        a3 = stage_call(
            root=root,
            row_root=row_root,
            row=row,
            stage=3,
            questions=q3,
            full_source=bundle,
            focus_source=focus_source,
            interpretation=interpretation,
            model=model,
            origin=origin,
            counters=counters,
        )
    else:
        row["systemone"]["stages"]["3"]["status"] = UNSCHEDULED_NO_RELATIONS
        a3 = {}

    try:
        decision = v3.decision_from_rounds(focus_source, a1, a2, a3)
    except v3.v2.DecisionUnresolved as exc:
        return terminal_abstain(
            root=root, row_root=row_root, row=row, stage=3, exc=exc, counters=counters
        )
    except (v3.v2.TwoPassV2Error, ContractError, ValidationError) as exc:
        return terminal_failure(
            root=root, row_root=row_root, row=row, stage=3, exc=exc, counters=counters
        )
    row["decision"] = base.freeze_artifact(
        root, row_root / "decision.json", canonical_json_bytes(decision)
    )

    try:
        candidate = v3.compile_candidate(focus_source, decision)
    except (v3.v2.TwoPassV2Error, ContractError, ValidationError) as exc:
        return terminal_failure(
            root=root, row_root=row_root, row=row, stage=3, exc=exc, counters=counters
        )
    row["candidate"] = base.freeze_artifact(
        root, row_root / "candidate.json", canonical_json_bytes(candidate)
    )

    try:
        claim = build_claim_ir(
            bundle_id=bundle_id,
            bundle=bundle,
            candidate=candidate,
            provenance=provenance,
            extractor_identity=extractor_identity,
            extractor_revision=extractor_revision,
        )
    except V3TransactionError as exc:
        return terminal_failure(
            root=root, row_root=row_root, row=row, stage=3, exc=exc, counters=counters
        )
    row["claim_ir"] = base.freeze_artifact(
        root, row_root / "claim-ir.json", canonical_json_bytes(claim)
    )
    row["candidate_valid"] = True
    row["claim_ir_valid"] = True
    row["outcome"] = "VALID_CLAIM_IR"
    counters["claim_ir_valid"] += 1
    base.write_json_exclusive(row_root / "artifact-record.json", row)
    return row


def compare_pairs(
    *,
    root: Path,
    replicates: list[dict[str, Any]],
    source_bundles: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows = {
        rec["replicate_id"]: {row["bundle_id"]: row for row in rec["rows"]}
        for rec in replicates
    }
    report_rows: list[dict[str, Any]] = []
    exact = 0
    both_valid = 0
    adjudication_required = 0
    pair_names = (
        "BOTH_VALID",
        "BOTH_ABSTAIN",
        "A_VALID_B_ABSTAIN",
        "A_ABSTAIN_B_VALID",
        "PAIR_EXTRACTION_FAILURE",
    )
    for bundle_id in EXPECTED_BUNDLES:
        a = rows["A"][bundle_id]
        b = rows["B"][bundle_id]
        oa, ob = a["outcome"], b["outcome"]
        comparison = None
        if oa == ob == "VALID_CLAIM_IR":
            pair = "BOTH_VALID"
            both_valid += 1
            ca = load_json(root / a["claim_ir"]["path"])
            cb = load_json(root / b["claim_ir"]["path"])
            comparison = compare_claim_ir(ca, cb)
            if comparison["overall_exact_structural_equivalence"]:
                exact += 1
            else:
                adjudication_required += 1
        elif oa == ob == "EXTRACTION_ABSTAIN":
            pair = "BOTH_ABSTAIN"
        elif oa == "VALID_CLAIM_IR" and ob == "EXTRACTION_ABSTAIN":
            pair = "A_VALID_B_ABSTAIN"
        elif oa == "EXTRACTION_ABSTAIN" and ob == "VALID_CLAIM_IR":
            pair = "A_ABSTAIN_B_VALID"
        else:
            pair = "PAIR_EXTRACTION_FAILURE"
        report_rows.append(
            {
                "bundle_id": bundle_id,
                "source_bundle_sha256": sha256_bytes(
                    canonical_json_bytes(source_bundles[bundle_id])
                ),
                "outcome_a": oa,
                "outcome_b": ob,
                "pair_outcome": pair,
                "comparison": comparison,
                "source_only_adjudication_required": bool(
                    comparison is not None
                    and not comparison["overall_exact_structural_equivalence"]
                ),
            }
        )
    pair_counts = {
        name: sum(row["pair_outcome"] == name for row in report_rows)
        for name in pair_names
    }
    return {
        "schema_version": "paper2-v3-real-calibration-ab-comparison-v1",
        "owner_issue": OWNER_ISSUE,
        "basis_visible": False,
        "decomposition_outcome_visible": False,
        "claim_ir_comparison_restricted_to_both_valid": True,
        "rows": report_rows,
        "aggregate": {
            "pair_outcome_counts": pair_counts,
            "claim_ir_comparison_denominator": both_valid,
            "exact_structural_agreement_count": exact,
            "exact_structural_agreement_rate": (
                exact / both_valid if both_valid else None
            ),
            "source_only_adjudication_required_count": adjudication_required,
        },
    }


def initial_summary(evidence_root: Path, *, synthetic: bool) -> dict[str, Any]:
    return {
        "schema_version": SUMMARY_VERSION,
        "owner_issue": OWNER_ISSUE,
        "classification": None,
        "interpretation": None,
        "synthetic": synthetic,
        "evidence_root": str(evidence_root),
        "plan": {
            "server_launches_exact": 2,
            "normal_calls_exact": 10,
            "systemone_calls_min": 10,
            "systemone_calls_max": 30,
            "total_calls_min": 20,
            "total_calls_max": 40,
        },
        "counters": {
            "server_launches": 0,
            "normal_calls_attempted": 0,
            "normal_calls_completed": 0,
            "systemone_calls_attempted": 0,
            "systemone_calls_completed": 0,
            "stage1_calls_attempted": 0,
            "stage1_calls_completed": 0,
            "stage2_calls_attempted": 0,
            "stage2_calls_completed": 0,
            "stage3_calls_attempted": 0,
            "stage3_calls_completed": 0,
            "total_calls_attempted": 0,
            "total_calls_completed": 0,
            "scientific_calls_attempted": 0,
            "claim_ir_valid": 0,
            "extraction_abstain": 0,
            "extraction_failure": 0,
        },
        "retry_replay_fallback_repair_replacement": {
            "retry": 0,
            "replay": 0,
            "fallback": 0,
            "repair": 0,
            "replacement": 0,
        },
        "basis_decomposition_executed": False,
        "paper167_execution": False,
        "replicates": [],
    }


def validate_completed(summary: dict[str, Any]) -> None:
    c = summary["counters"]
    c["total_calls_attempted"] = (
        c["normal_calls_attempted"] + c["systemone_calls_attempted"]
    )
    c["total_calls_completed"] = (
        c["normal_calls_completed"] + c["systemone_calls_completed"]
    )
    if c["server_launches"] != 2:
        fail("completed transaction must have exactly two server launches")
    if c["normal_calls_attempted"] != 10 or c["normal_calls_completed"] != 10:
        fail("completed transaction must have exactly ten Normal calls")
    if not 10 <= c["systemone_calls_attempted"] <= 30:
        fail("SystemOne call count outside frozen variable bounds")
    if c["systemone_calls_completed"] != c["systemone_calls_attempted"]:
        fail("completed transaction has incomplete SystemOne calls")
    if not 20 <= c["total_calls_attempted"] <= 40:
        fail("total call count outside frozen variable bounds")
    if c["stage1_calls_attempted"] != 10:
        fail("every bundle attempt must schedule Stage 1 exactly once")
    for stage in (1, 2, 3):
        if c[f"stage{stage}_calls_completed"] != c[f"stage{stage}_calls_attempted"]:
            fail(f"stage {stage} completed/attempted mismatch")
    outcomes = c["claim_ir_valid"] + c["extraction_abstain"] + c["extraction_failure"]
    if outcomes != 10:
        fail("all ten replicate/bundle attempts must have terminal outcomes")
    if len(summary["replicates"]) != 2:
        fail("completed transaction must retain both replicate records")
    for rec in summary["replicates"]:
        if rec["bundle_order"] != list(EXPECTED_BUNDLES):
            fail("replicate bundle order drift")
        if len(rec["rows"]) != 5:
            fail("replicate row count drift")
        if not rec["cleanup"]["terminated"]:
            fail("owned server was not cleanly terminated")
        for row in rec["rows"]:
            if row["outcome"] not in {
                "VALID_CLAIM_IR",
                "EXTRACTION_ABSTAIN",
                "EXTRACTION_FAILURE",
            }:
                fail("nonterminal bundle outcome")
            if row["outcome"] in {"EXTRACTION_ABSTAIN", "EXTRACTION_FAILURE"}:
                stages = row["systemone"]["stages"]
                # Once a stage is terminal, any later untouched stage must be
                # explicitly marked rather than silently absent.
                attempted = [
                    int(k) for k, v in stages.items() if v["attempted"]
                ]
                terminal_stage = max(attempted) if attempted else 0
                for stage in range(terminal_stage + 1, 4):
                    if stages[str(stage)]["status"] not in {
                        UNSCHEDULED_TERMINAL,
                        UNSCHEDULED_NO_RELATIONS,
                    }:
                        fail("later stage missing explicit unscheduled marker")


def run_core(
    *,
    preflight_data: dict[str, Any],
    llama_root: Path,
    server_binary: Path,
    model_path: Path,
    evidence_root: Path,
    port: int,
    synthetic: bool,
    fixture_plan: Path | None,
) -> tuple[int, dict[str, Any]]:
    summary = initial_summary(evidence_root, synthetic=synthetic)
    process: subprocess.Popen[str] | None = None
    evidence_created = False
    try:
        evidence_root.mkdir(parents=True, exist_ok=False)
        evidence_created = True
        authority = {
            key: value
            for key, value in preflight_data.items()
            if key not in {
                "prompt_bytes",
                "bundle_raw",
                "bundles",
                "package_by_bundle",
                "provenance_by_bundle",
            }
        }
        summary["authority"] = authority
        base.write_json_exclusive(
            evidence_root / "preflight-attestation.json", authority
        )
        prompt = preflight_data["prompt_bytes"].decode("utf-8")
        runtime = preflight_data["runtime"]
        relay_head = preflight_data["relaytheory"]["head"]
        extractor_identity = "paper2-two-pass-llama-cpp-transaction-v3"
        extractor_revision = (
            f"relaytheory={relay_head};jev={runtime['head']};"
            f"build={runtime['build_number']};model_sha256={runtime['model_sha256']}"
        )
        base.write_json_exclusive(
            evidence_root / "runner-contract.json",
            {
                "owner_issue": OWNER_ISSUE,
                "extractor_identity": extractor_identity,
                "extractor_revision": extractor_revision,
                "decision_surface": v3.VERSION,
                "procedure_version": v3.MANIFEST_VERSION,
                "cache_prompt": False,
                "normal_calls_exact": 10,
                "systemone_calls_min": 10,
                "systemone_calls_max": 30,
                "total_calls_min": 20,
                "total_calls_max": 40,
                "retry_replay_fallback_repair_replacement": {
                    "retry": 0,
                    "replay": 0,
                    "fallback": 0,
                    "repair": 0,
                    "replacement": 0,
                },
            },
        )

        counters = summary["counters"]
        model: str | None = None
        for replicate_id in ("A", "B"):
            rec: dict[str, Any] = {
                "replicate_id": replicate_id,
                "started_at": base.utc_now(),
                "bundle_order": [],
                "rows": [],
                "cleanup": {
                    "owned_process": False,
                    "terminated": False,
                    "exit_code": None,
                },
            }
            process = None
            try:
                if not base.port_is_free(base.DEFAULT_HOST, port):
                    fail(f"{base.DEFAULT_HOST}:{port} occupied before {replicate_id}")
                if sha256_file(server_binary) != runtime["binary_sha256"]:
                    fail("llama-server binary changed after preflight")
                if sha256_file(model_path) != runtime["model_sha256"]:
                    fail("GGUF changed after preflight")
                current_head = base.run_text(
                    ["git", "rev-parse", "HEAD"], cwd=llama_root
                ).strip()
                current_tree = base.run_text(
                    ["git", "rev-parse", "HEAD^{tree}"], cwd=llama_root
                ).strip()
                if (
                    current_head != runtime["head"]
                    or current_tree != runtime["tree"]
                ):
                    fail("Jev HEAD/tree changed after preflight")

                log_path = evidence_root / replicate_id / "llama-server.log"
                command = base.server_command(
                    server_binary=server_binary,
                    model_path=model_path,
                    port=port,
                    log_path=log_path,
                    replicate_id=replicate_id,
                    fixture_plan=fixture_plan,
                )
                process = base.start_owned_server(command)
                counters["server_launches"] += 1
                rec["cleanup"]["owned_process"] = True
                rec["pid"] = process.pid
                rec["server_command"] = command
                origin = f"http://{base.DEFAULT_HOST}:{port}"
                base.wait_until_ready(process, origin)
                rec["runtime"] = base.attest_runtime_http(
                    origin=origin,
                    server_binary=server_binary,
                    model_path=model_path,
                    runtime=runtime,
                )
                attested_model = rec["runtime"]["model"]
                if model is None:
                    model = attested_model
                elif model != attested_model:
                    fail("A/B model aliases differ")

                for bundle_id in EXPECTED_BUNDLES:
                    rec["bundle_order"].append(bundle_id)
                    row = execute_bundle(
                        root=evidence_root,
                        replicate_id=replicate_id,
                        bundle_id=bundle_id,
                        bundle_raw=preflight_data["bundle_raw"][bundle_id],
                        bundle=preflight_data["bundles"][bundle_id],
                        source_digest=next(
                            x["raw_normalized_sha256"]
                            for x in preflight_data["preprocessing"]["bundles"]
                            if x["bundle_id"] == bundle_id
                        ),
                        prompt=prompt,
                        model=model,
                        origin=origin,
                        provenance=preflight_data["provenance_by_bundle"][bundle_id],
                        extractor_identity=extractor_identity,
                        extractor_revision=extractor_revision,
                        counters=counters,
                    )
                    rec["rows"].append(row)
            finally:
                if process is not None:
                    rec["cleanup"]["exit_code"] = base.terminate_owned_server(process)
                    rec["cleanup"]["terminated"] = process.poll() is not None
                rec["completed_at"] = base.utc_now()
                summary["replicates"].append(rec)
                process = None
            if replicate_id == "A" and not base.port_is_free(
                base.DEFAULT_HOST, port
            ):
                fail("replicate A did not release port before B")

        validate_completed(summary)
        summary["comparison"] = compare_pairs(
            root=evidence_root,
            replicates=summary["replicates"],
            source_bundles=preflight_data["bundles"],
        )
        summary["classification"] = (
            "SYNTHETIC_TRANSACTION_COMPLETED"
            if synthetic
            else "SCIENTIFIC_TRANSACTION_COMPLETED"
        )
        summary["interpretation"] = (
            "SYNTHETIC_ONLY"
            if synthetic
            else (
                "V3_ZERO_YIELD_NULL_DESTROYED_ON_FROZEN_CALIBRATION_SURFACE"
                if summary["counters"]["claim_ir_valid"] > 0
                else "V3_VALID_CLAIMIR_YIELD_ZERO_ON_FROZEN_CALIBRATION_SURFACE"
            )
        )
        counters["scientific_calls_attempted"] = (
            0 if synthetic else counters["total_calls_attempted"]
        )
    except Exception as exc:
        c = summary["counters"]
        c["total_calls_attempted"] = (
            c["normal_calls_attempted"] + c["systemone_calls_attempted"]
        )
        c["total_calls_completed"] = (
            c["normal_calls_completed"] + c["systemone_calls_completed"]
        )
        c["scientific_calls_attempted"] = 0 if synthetic else c["total_calls_attempted"]
        summary["error"] = base.parse_artifact_error(exc)
        summary["classification"] = (
            "V3_REAL_CALIBRATION_PREEXECUTION_BLOCKED"
            if c["scientific_calls_attempted"] == 0
            else "SCIENTIFIC_TRANSACTION_CONSUMED_INCOMPLETE"
        )
    finally:
        if process is not None:
            base.terminate_owned_server(process)
        if evidence_created:
            receipt = {
                "schema_version": RECEIPT_VERSION,
                "owner_issue": OWNER_ISSUE,
                "status": summary["classification"],
                "synthetic": synthetic,
                "plan": summary["plan"],
                "counters": summary["counters"],
                "authority": summary.get("authority", {}),
                "replicates": summary["replicates"],
                "retry_replay_fallback_repair_replacement": summary[
                    "retry_replay_fallback_repair_replacement"
                ],
                "evidence_root": summary["evidence_root"],
                "basis_decomposition_executed": False,
                "paper167_execution": False,
            }
            base.write_json_exclusive(
                evidence_root / "transaction-receipt.json", receipt
            )
            base.write_json_exclusive(
                evidence_root / "transaction-summary.json", summary
            )
    ok = summary["classification"] in {
        "SCIENTIFIC_TRANSACTION_COMPLETED",
        "SYNTHETIC_TRANSACTION_COMPLETED",
    }
    return (0 if ok else 2), summary


FAKE_SERVER = r'''#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

if "--version" in sys.argv:
    print("llama-server 0.4.1-dev (build 11066, commit synthetic)")
    raise SystemExit(0)

p = argparse.ArgumentParser(add_help=False)
p.add_argument("-m")
p.add_argument("--host")
p.add_argument("--port", type=int)
p.add_argument("-c", type=int)
p.add_argument("-np", type=int)
p.add_argument("--log-file")
p.add_argument("--fixture-plan")
p.add_argument("--replicate-id")
args, _ = p.parse_known_args()
root = Path(__file__).resolve().parents[2]
revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
plan = json.loads(Path(args.fixture_plan).read_text()) if args.fixture_plan else {}
replicate = args.replicate_id or "REAL"
record_path = Path(plan["record"]) if plan.get("record") else None
if args.log_file:
    Path(args.log_file).parent.mkdir(parents=True, exist_ok=True)
    Path(args.log_file).write_text("synthetic v3 server started\n")

def selected(kind, bundle, stage=None):
    key = kind if stage is None else f"{kind}_stage{stage}"
    return bundle in plan.get(key, {}).get(replicate, [])

def record(kind, body, bundle, stage=None):
    if record_path:
        with record_path.open("a") as h:
            h.write(json.dumps({
                "pid": os.getpid(), "replicate": replicate, "kind": kind,
                "bundle_id": bundle, "stage": stage, "payload": body
            }, sort_keys=True) + "\n")

def answer(name, q, source_ids, stage, bundle):
    criteria = q["criteria"]
    if name == "claim_type":
        value = "relation"
    elif name == "modality":
        value = "descriptive"
    elif name.startswith("scope__"):
        value = "no"
    elif name == "n1__seed":
        value = f"{source_ids[0]}::state_or_structure"
    elif name == "n2__seed":
        value = f"{source_ids[1]}::response_or_outcome" if len(source_ids) > 1 else "NONE"
    elif name == "n3__seed":
        value = "NONE"
    elif name in ("n1__grounding", "n2__grounding"):
        value = "explicit"
    elif name.startswith("n1__span__") or name.startswith("n2__span__"):
        value = "no"
    elif name == "r1__tuple":
        if selected("no_relation", bundle, stage):
            value = "NONE"
        elif "n1::n2" in criteria:
            value = "n1::n2"
        else:
            value = "n1"
    elif name == "r2__tuple":
        value = "NONE"
    elif name == "r1__kind":
        value = "depends_on"
    elif name == "r1__grounding":
        value = "explicit"
    elif name.startswith("r1__span__"):
        if selected("invalid_relation", bundle, stage):
            value = "no"
        else:
            value = "yes" if name.endswith(source_ids[-1]) else "no"
    else:
        value = next(x for x in criteria if x != "__unresolved__")
    if selected("unresolved", bundle, stage):
        target = {1: "claim_type", 2: "n1__grounding", 3: "r1__kind"}[stage]
        if name == target:
            value = "__unresolved__"
    return value

class H(BaseHTTPRequestHandler):
    def log_message(self, fmt, *items): return
    def send(self, value, status=200):
        raw = json.dumps(value, sort_keys=True).encode()
        self.send_response(status); self.send_header("Content-Type","application/json")
        self.send_header("Content-Length", str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        if self.path == "/health": self.send({"status":"ok"}); return
        if self.path == "/v1/models": self.send({"data":[{"id":"fake-model"}]}); return
        if self.path == "/props":
            self.send({
                "build_info": f"build 11066 revision {revision}",
                "model_alias":"fake-model",
                "model_path":str(Path(args.m).resolve()),
                "default_generation_settings":{"n_ctx":args.c},
                "total_slots":args.np,
                "model_ftype":"Q4_K_M",
                "chat_template":"synthetic-template"
            }); return
        if self.path == "/slots": self.send([{"id":0,"n_ctx":args.c}]); return
        self.send({"error":"not found"},404)
    def do_POST(self):
        n=int(self.headers.get("Content-Length","0"))
        body=json.loads(self.rfile.read(n))
        if self.path == "/v1/chat/completions":
            source=json.loads(body["messages"][1]["content"])
            bundle=source["bundle_id"]; record("normal",body,bundle)
            if selected("normal_fail",bundle): self.send({"error":"normal failure"},500); return
            self.send({"model":"fake-model","choices":[{"message":{"content":"Use source spans s1 s2 s3."}}]}); return
        if self.path == "/v1/systemone":
            focus=body["state"]["focus_source"]; bundle=focus["bundle_id"]
            stage=int(body["state"]["stage"]); record("systemone",body,bundle,stage)
            if selected("transport_fail",bundle,stage): self.send({"error":"transport failure"},500); return
            ids=[x["span_id"] for x in focus["source_spans"]]
            answers={}
            for name,q in body["questions"].items():
                v=answer(name,q,ids,stage,bundle)
                answers[name]={"type":"choice","choice":v,"probabilities":{v:1.0},"confidence":1.0}
            if selected("malformed",bundle,stage) and answers:
                del answers[next(iter(answers))]
            self.send({"model":"fake-model","answers":answers,"usage":{"input_tokens":1,"output_tokens":0}}); return
        self.send({"error":"not found"},404)

ThreadingHTTPServer((args.host,args.port),H).serve_forever()
'''


def write_fake_server(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FAKE_SERVER, encoding="utf-8")
    path.chmod(0o755)


def free_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((base.DEFAULT_HOST, 0))
        return int(sock.getsockname()[1])
    finally:
        sock.close()


def make_synthetic_inputs(root: Path, plan: dict[str, Any]) -> dict[str, Any]:
    llama = root / "llama.cpp"
    base.init_git_repo(llama, remote=base.EXPECTED_JEV_REMOTE + ".git")
    server = llama / "build/bin/llama-server"
    write_fake_server(server)
    base.run_text(["git", "add", "build/bin/llama-server"], cwd=llama)
    base.run_text(["git", "commit", "-qm", "synthetic v3 server"], cwd=llama)
    head = base.run_text(["git", "rev-parse", "HEAD"], cwd=llama).strip()
    tree = base.run_text(["git", "rev-parse", "HEAD^{tree}"], cwd=llama).strip()
    model = root / "synthetic-model.gguf"
    model.write_bytes(b"synthetic v3 model")
    prompt = "Synthetic Normal prompt.\n"

    bundles: dict[str, dict[str, Any]] = {}
    raws: dict[str, bytes] = {}
    provenance: dict[str, dict[str, Any]] = {}
    prep_rows = []
    for bundle_id in EXPECTED_BUNDLES:
        source = {
            "schema_version": base.SOURCE_VERSION,
            "bundle_id": bundle_id,
            "source_language": "en",
            "source_spans": [
                {"span_id":"s1","text":f"Synthetic state for {bundle_id}."},
                {"span_id":"s2","text":f"Synthetic response for {bundle_id}."},
                {"span_id":"s3","text":f"The state depends on the response for {bundle_id}."},
            ],
        }
        raw = canonical_json_bytes(source)
        bundles[bundle_id] = source
        raws[bundle_id] = raw
        provenance[bundle_id] = {
            "bundle_id": bundle_id,
            "paper_id": f"synthetic:{bundle_id}",
            "source_language": "en",
            "source_spans": [{"span_id":"s1","locator":"Synthetic"}],
            "authors": [],
            "institutions": [],
            "venue": None,
            "citation_count": None,
            "construct_labels": [],
        }
        prep_rows.append({
            "bundle_id": bundle_id,
            "raw_normalized_sha256": sha256_bytes(f"raw:{bundle_id}".encode()),
            "masked_bundle_sha256": sha256_bytes(raw),
        })
    record = root / "requests.jsonl"
    plan_path = root / "plan.json"
    plan_path.write_bytes(canonical_json_bytes({**plan, "record": str(record)}))
    runtime = {
        "repository": base.EXPECTED_JEV_REMOTE,
        "head": head,
        "tree": tree,
        "server_binary": str(server),
        "version": base.EXPECTED_JEV_VERSION,
        "build_number": base.EXPECTED_JEV_BUILD,
        "binary_sha256": sha256_file(server),
        "model_path": str(model),
        "model_sha256": sha256_file(model),
        "gpu": {"synthetic": True},
        "host": base.DEFAULT_HOST,
        "port": free_port(),
        "route": SYSTEMONE_ROUTE,
    }
    return {
        "relaytheory": {"head":"synthetic-relaytheory","tree":"synthetic-tree"},
        "manifest": {"status":"SYNTHETIC"},
        "protocol": {"status":"SYNTHETIC"},
        "prompt": {"sha256":sha256_bytes(prompt.encode())},
        "preprocessing": {"bundles":prep_rows},
        "runtime": runtime,
        "authorization": {"synthetic": True},
        "prompt_bytes": prompt.encode(),
        "bundle_raw": raws,
        "bundles": bundles,
        "provenance_by_bundle": provenance,
        "package_by_bundle": {},
        "llama": llama,
        "server": server,
        "model": model,
        "fixture_plan": plan_path,
        "record": record,
    }


def request_log(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def expect(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def synthetic_case(
    root: Path,
    name: str,
    plan: dict[str, Any],
) -> tuple[int, dict[str, Any], list[dict[str, Any]]]:
    inputs = make_synthetic_inputs(root / name, plan)
    evidence = root / name / "evidence"
    rc, summary = run_core(
        preflight_data=inputs,
        llama_root=inputs["llama"],
        server_binary=inputs["server"],
        model_path=inputs["model"],
        evidence_root=evidence,
        port=inputs["runtime"]["port"],
        synthetic=True,
        fixture_plan=inputs["fixture_plan"],
    )
    return rc, summary, request_log(inputs["record"])


def self_test() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    manifest = require_manifest(repo_root / MANIFEST_PATH, repo_root)
    expect(manifest["scientific_transaction_authorized"] is False, "no self authorization")
    expect(
        manifest["historical_v2"]["runner_must_remain_byte_identical"] is True,
        "#193 read-only provenance",
    )
    expect(manifest["paper167_execution_authorized"] is False, "#167 forbidden")

    with tempfile.TemporaryDirectory(prefix="relaytheory-210-v3-selftest-") as td:
        root = Path(td)

        # Full 3-stage valid path: 10 Normal + 30 SystemOne = 40 calls.
        rc, summary, log = synthetic_case(root, "full", {})
        expect(rc == 0, "full v3 transaction completes")
        expect(summary["counters"]["claim_ir_valid"] == 10, "ten valid rows")
        expect(summary["counters"]["systemone_calls_attempted"] == 30, "max staged calls")
        expect(summary["counters"]["total_calls_attempted"] == 40, "max total calls")
        expect(len({x["pid"] for x in log if x["replicate"] == "A"}) == 1, "A one process")
        expect(len({x["pid"] for x in log if x["replicate"] == "B"}) == 1, "B one process")
        expect(
            {x["pid"] for x in log if x["replicate"] == "A"}
            != {x["pid"] for x in log if x["replicate"] == "B"},
            "A/B fresh process isolation",
        )
        expect(
            summary["comparison"]["aggregate"]["claim_ir_comparison_denominator"] == 5,
            "comparator only BOTH_VALID",
        )

        # Stage-specific abstention and continuation to later bundles.
        plan = {
            "unresolved_stage1": {"A":["B0001"], "B":["B0001"]},
            "unresolved_stage2": {"A":["B0002"], "B":["B0002"]},
            "unresolved_stage3": {"A":["B0003"], "B":["B0003"]},
            "no_relation_stage2": {"A":["B0004"], "B":["B0004"]},
        }
        rc, summary, log = synthetic_case(root, "staged", plan)
        expect(rc == 0, "staged abstention transaction completes")
        expect(summary["counters"]["extraction_abstain"] == 6, "six abstentions")
        expect(summary["counters"]["claim_ir_valid"] == 4, "four valid rows")
        expect(summary["counters"]["systemone_calls_attempted"] < 30, "early stops reduce calls")
        expect(len(summary["replicates"][0]["rows"]) == 5, "A continues after abstention")
        expect(len(summary["replicates"][1]["rows"]) == 5, "B continues after abstention")
        for rec in summary["replicates"]:
            r1 = rec["rows"][0]
            expect(r1["systemone"]["stages"]["2"]["status"] == UNSCHEDULED_TERMINAL, "stage1 abstain skips 2")
            expect(r1["systemone"]["stages"]["3"]["status"] == UNSCHEDULED_TERMINAL, "stage1 abstain skips 3")
            r2 = rec["rows"][1]
            expect(r2["systemone"]["stages"]["3"]["status"] == UNSCHEDULED_TERMINAL, "stage2 abstain skips 3")
            r4 = rec["rows"][3]
            expect(r4["systemone"]["stages"]["3"]["status"] == UNSCHEDULED_NO_RELATIONS, "inactive relation is N/A")
            expect(r4["outcome"] == "VALID_CLAIM_IR", "inactive omission is not abstention")

        # Deterministic post-response decision failure is row-local extraction failure.
        rc, summary, _ = synthetic_case(
            root,
            "deterministic-failure",
            {"invalid_relation_stage3":{"A":["B0002"]}},
        )
        expect(rc == 0, "deterministic extraction failure does not consume transaction")
        expect(summary["counters"]["extraction_failure"] == 1, "one extraction failure")
        expect(
            summary["comparison"]["aggregate"]["pair_outcome_counts"]["PAIR_EXTRACTION_FAILURE"] == 1,
            "pair failure classifier",
        )

        # Malformed finite response is transaction-integrity failure, with no retry.
        rc, summary, log = synthetic_case(
            root,
            "malformed",
            {"malformed_stage2":{"A":["B0002"]}},
        )
        expect(rc == 2, "malformed response fails transaction")
        expect(summary["retry_replay_fallback_repair_replacement"] == {
            "retry":0,"replay":0,"fallback":0,"repair":0,"replacement":0
        }, "no retry/repair path")
        malformed_calls = [
            x for x in log
            if x["replicate"] == "A" and x["bundle_id"] == "B0002" and x["stage"] == 2
        ]
        expect(len(malformed_calls) == 1, "malformed request submitted once")

        # HTTP transport failure also consumes once and stops.
        rc, summary, log = synthetic_case(
            root,
            "transport",
            {"transport_fail_stage1":{"A":["B0002"]}},
        )
        expect(rc == 2, "transport failure stops transaction")
        attempts = [
            x for x in log
            if x["replicate"] == "A" and x["bundle_id"] == "B0002" and x["stage"] == 1
        ]
        expect(len(attempts) == 1, "transport failure no retry")

        # Evidence root replay is impossible.
        inputs = make_synthetic_inputs(root / "existing", {})
        evidence = root / "existing" / "evidence"
        evidence.mkdir()
        (evidence / "sentinel").write_text("preserve\n")
        try:
            evidence.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            pass
        else:
            raise AssertionError("existing evidence root must block exclusive creation")

    print("PAPER2_V3_REAL_CALIBRATION_TRANSACTION_SELFTEST_PASS")


def authorization_kwargs(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "comment_id": args.authorization_comment_id,
        "status": args.authorization_status,
        "authorized_head": args.authorized_head,
        "authorized_tree": args.authorized_tree,
        "authorized_runner_blob": args.authorized_runner_blob,
        "authorized_manifest_blob": args.authorized_manifest_blob,
        "authorized_v3_schema_blob": args.authorized_v3_schema_blob,
        "authorized_v3_contract_blob": args.authorized_v3_contract_blob,
        "authorized_v3_compiler_blob": args.authorized_v3_compiler_blob,
        "authorized_claim_ir_blob": args.authorized_claim_ir_blob,
        "authorized_evidence_root": args.authorized_evidence_root,
    }


def main() -> int:
    p = argparse.ArgumentParser(
        description="Paper 2 #210 prospective real SystemOne-v3 calibration transaction"
    )
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--attest-only", action="store_true")
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    p.add_argument("--protocol", type=Path, default=Path("research/paper2/extraction_two_pass_real_protocol_v1.json"))
    p.add_argument("--prompt", type=Path, default=Path("research/paper2/extraction_normal_prompt_v1.md"))
    p.add_argument("--mask-terms", type=Path, default=Path("research/paper2/extraction_calibration_mask_terms_v1.json"))
    p.add_argument("--preprocessing-freeze", type=Path)
    p.add_argument("--bundles-dir", type=Path)
    p.add_argument("--package", type=Path, default=Path("research/paper2/extraction_run_package_v1.json"))
    p.add_argument("--provenance", type=Path, default=Path("research/paper2/extraction_provenance_v1.json"))
    p.add_argument("--jev-root", type=Path)
    p.add_argument("--server-binary", type=Path)
    p.add_argument("--model", type=Path)
    p.add_argument("--evidence-root", type=Path)
    p.add_argument("--port", type=int, default=base.DEFAULT_PORT)
    p.add_argument("--authorization-comment-id", type=int)
    p.add_argument("--authorization-status")
    p.add_argument("--authorized-head")
    p.add_argument("--authorized-tree")
    p.add_argument("--authorized-runner-blob")
    p.add_argument("--authorized-manifest-blob")
    p.add_argument("--authorized-v3-schema-blob")
    p.add_argument("--authorized-v3-contract-blob")
    p.add_argument("--authorized-v3-compiler-blob")
    p.add_argument("--authorized-claim-ir-blob")
    p.add_argument("--authorized-evidence-root")
    args = p.parse_args()

    if args.self_test:
        try:
            self_test()
            return 0
        except (AssertionError, OSError, V3TransactionError, base.TransactionError) as exc:
            print(f"PAPER2_V3_REAL_CALIBRATION_TRANSACTION_SELFTEST_FAIL: {exc}")
            return 2

    required = {
        "--preprocessing-freeze": args.preprocessing_freeze,
        "--bundles-dir": args.bundles_dir,
        "--jev-root": args.jev_root,
        "--server-binary": args.server_binary,
        "--model": args.model,
        "--evidence-root": args.evidence_root,
    }
    if not args.attest_only:
        required.update({
            "--authorization-comment-id": args.authorization_comment_id,
            "--authorization-status": args.authorization_status,
            "--authorized-head": args.authorized_head,
            "--authorized-tree": args.authorized_tree,
            "--authorized-runner-blob": args.authorized_runner_blob,
            "--authorized-manifest-blob": args.authorized_manifest_blob,
            "--authorized-v3-schema-blob": args.authorized_v3_schema_blob,
            "--authorized-v3-contract-blob": args.authorized_v3_contract_blob,
            "--authorized-v3-compiler-blob": args.authorized_v3_compiler_blob,
            "--authorized-claim-ir-blob": args.authorized_claim_ir_blob,
            "--authorized-evidence-root": args.authorized_evidence_root,
        })
    missing = [k for k,v in required.items() if v is None]
    if missing:
        p.error("missing required arguments: " + ", ".join(missing))

    repo_root = args.repo_root.resolve()
    try:
        preflight = validate_real_envelope(
            repo_root=repo_root,
            manifest_path=(repo_root / args.manifest).resolve() if not args.manifest.is_absolute() else args.manifest.resolve(),
            protocol_path=(repo_root / args.protocol).resolve() if not args.protocol.is_absolute() else args.protocol.resolve(),
            prompt_path=(repo_root / args.prompt).resolve() if not args.prompt.is_absolute() else args.prompt.resolve(),
            mask_terms_path=(repo_root / args.mask_terms).resolve() if not args.mask_terms.is_absolute() else args.mask_terms.resolve(),
            preprocessing_freeze_path=args.preprocessing_freeze.resolve(),
            bundle_dir=args.bundles_dir.resolve(),
            package_path=(repo_root / args.package).resolve() if not args.package.is_absolute() else args.package.resolve(),
            provenance_path=(repo_root / args.provenance).resolve() if not args.provenance.is_absolute() else args.provenance.resolve(),
            llama_root=args.jev_root.resolve(),
            server_binary=args.server_binary.resolve(),
            model_path=args.model.resolve(),
            evidence_root=args.evidence_root.resolve(),
            port=args.port,
            require_gpu=True,
            require_authorization=not args.attest_only,
            authorization=authorization_kwargs(args),
        )
    except (V3TransactionError, base.TransactionError) as exc:
        print(json.dumps({
            "classification":"V3_REAL_CALIBRATION_PREEXECUTION_BLOCKED",
            "error":str(exc),
            "model_calls":0,
        }, sort_keys=True))
        return 2

    if args.attest_only:
        public = {
            k:v for k,v in preflight.items()
            if k not in {"prompt_bytes","bundle_raw","bundles","package_by_bundle","provenance_by_bundle"}
        }
        print(json.dumps({
            "classification":"V3_REAL_CALIBRATION_PHYSICAL_REATTESTATION_READY",
            "scientific_calls":0,
            "attestation":public,
        }, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    rc, summary = run_core(
        preflight_data=preflight,
        llama_root=args.jev_root.resolve(),
        server_binary=args.server_binary.resolve(),
        model_path=args.model.resolve(),
        evidence_root=args.evidence_root.resolve(),
        port=args.port,
        synthetic=False,
        fixture_plan=None,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
