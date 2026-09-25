#!/usr/bin/env python3
"""Own the Paper 2 #193 versioned Normal -> SystemOne transaction.

This entry point is a versioned successor to the consumed #184 runner.  It
owns two fresh llama-server lifetimes, performs all authority checks before a
model-facing request, freezes every response/artifact with a digest, and
stops at the first invalid result.  ``--self-test`` uses only synthetic source
bundles and a fake Jev-capable server; it never uses the local GGUF or real
literature.

The real CLI requires an explicit read-back authorization acknowledgement.
No retry, replay, fallback, candidate repair, or basis/decomposition input is
implemented here.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shlex
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from paper2_claim_ir_compare import compare as compare_claim_ir
from paper2_claim_ir_validate import ValidationError, validate as validate_claim_ir
from paper2_extraction_bundle_prepare import canonical_json_bytes
from paper2_extraction_procedure_validate import (
    ContractError,
    validate_candidate,
    validate_source,
)
from paper2_extraction_two_pass_prepare import compact_focus_bundle
from paper2_extraction_two_pass_systemone_v2 import (
    DecisionUnresolved,
    TwoPassV2Error,
    build_systemone_request,
    compile_candidate,
    decision_from_answers,
    parse_systemone_response,
)
from paper2_extraction_abstention_v2 import validate_contract as validate_abstention_contract


OWNER_ISSUE = 193
PROTOCOL_VERSION = "paper2-two-pass-real-protocol-v1"
SYSTEMONE_VERSION = "paper2-two-pass-systemone-v2"
SOURCE_VERSION = "paper2-extraction-source-bundle-v1"
CLAIM_VERSION = "paper2-claim-ir-v1"
RECEIPT_VERSION = "paper2-two-pass-extraction-transaction-receipt-v2"
SUMMARY_VERSION = "paper2-two-pass-extraction-transaction-summary-v2"

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 1234
DEFAULT_CONTEXT = 8192
DEFAULT_SLOTS = 1
READY_TIMEOUT_SECONDS = 120.0
READY_POLL_SECONDS = 0.5
HTTP_TIMEOUT_SECONDS = 180.0

EXPECTED_BUNDLES = (
    "B0001",
    "B0002",
    "B0003",
    "B0004",
    "B0005",
)
EXPECTED_SAMPLE_IDS = (
    "CAL-BEER-1995",
    "CAL-FRISTON-2010",
    "CAL-TISHBY-2000",
    "CAL-KOLCHINSKY-WOLPERT-2018",
    "CAL-COWAN-2001",
)
EXPECTED_NORMAL_PROMPT_SHA256 = (
    "a63aa5b0480653f0dbba018789b6e537bde252a12ce7abf8a58f9b198096ca99"
)
EXPECTED_MASK_TERMS_SHA256 = (
    "1b0963e07d6948d9d106a2200f48da680cb11a3705ecf8dd8bd8aa481df9badd"
)
EXPECTED_PREPROCESSING_SHA256 = (
    "a20c79555bc3b2bafb25ee805a2fb1f6b9ea1b65c16a493dd4792130c1da9ea2"
)
EXPECTED_JEV_REMOTE = "https://github.com/kishida/llama.cpp"
EXPECTED_JEV_HEAD = "07183d010f5cf5d021a2550775f42fb4b4270e06"
EXPECTED_JEV_TREE = "4a654218342c2e179c0cd143e359632bff02bc22"
EXPECTED_JEV_VERSION = "0.4.1-dev"
EXPECTED_JEV_BUILD = 11066
EXPECTED_SERVER_SHA256 = (
    "d3bb0875329ff7c384c44b94b18e56dbb86c4d752af03a835b23a67c44354e4a"
)
EXPECTED_MODEL_SHA256 = (
    "c088a44859de42a1966851b552ba628c0ff4419b87c4622539d69430f40024ed"
)
EXPECTED_SYSTEMONE_ROUTE = "/v1/systemone"
EXPECTED_PLAN = {
    "server_launches": 2,
    "normal_calls": 10,
    "systemone_calls": 10,
    "total_calls": 20,
}
UNRESOLVED = "__unresolved__"
NONE = "none"
SPAN_RE = re.compile(r"(?<![A-Za-z0-9_])(s[0-9]+)(?![A-Za-z0-9_])")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


class TransactionError(RuntimeError):
    """A fail-closed transaction error."""


class HttpTransactionError(TransactionError):
    def __init__(self, message: str, *, status: int | None = None, raw: bytes = b""):
        super().__init__(message)
        self.status = status
        self.raw = raw


def fail(message: str) -> None:
    raise TransactionError(message)


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TransactionError(f"could not load JSON {path}: {exc}") from exc


def write_exclusive(path: Path, raw: bytes) -> str:
    """Write one evidence artifact without ever replacing an existing file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise TransactionError(f"evidence artifact already exists: {path}") from exc
    return sha256_bytes(raw)


def write_json_exclusive(path: Path, value: Any) -> str:
    return write_exclusive(path, canonical_json_bytes(value))


def run_text(command: list[str], *, cwd: Path | None = None) -> str:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise TransactionError(
            f"command could not start: {shlex.join(command)}: {exc}"
        ) from exc
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise TransactionError(
            f"command failed ({completed.returncode}): {shlex.join(command)}: {detail}"
        )
    return completed.stdout or completed.stderr


def canonical_digest(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def require_hex64(value: Any, context: str) -> str:
    if not isinstance(value, str) or not HEX64_RE.fullmatch(value):
        fail(f"{context}: expected lowercase SHA-256")
    return value


def require_clean_git_checkout(root: Path, *, label: str) -> tuple[str, str]:
    if not root.is_dir():
        fail(f"{label} is not a directory: {root}")
    top = Path(run_text(["git", "rev-parse", "--show-toplevel"], cwd=root).strip())
    if top.resolve() != root.resolve():
        fail(f"{label} root mismatch: expected {root} got {top}")
    status = run_text(
        ["git", "status", "--porcelain", "--untracked-files=all"], cwd=root
    )
    if status.strip():
        fail(f"{label} must be clean: {status.strip()}")
    head = run_text(["git", "rev-parse", "HEAD"], cwd=root).strip()
    tree = run_text(["git", "rev-parse", "HEAD^{tree}"], cwd=root).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", head) or not re.fullmatch(
        r"[0-9a-f]{40}", tree
    ):
        fail(f"{label} Git identity is malformed")
    return head, tree


def path_outside(path: Path, root: Path, *, label: str) -> None:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return
    fail(f"{label} must be outside the RelayTheory checkout: {path}")


def port_is_free(host: str, port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def require_new_evidence_root(path: Path, repo_root: Path) -> None:
    if os.path.lexists(path):
        fail(f"evidence root must be new/nonexistent: {path}")
    path_outside(path, repo_root, label="evidence root")


def normalize_remote(value: str) -> str:
    value = value.strip()
    return value[:-4] if value.endswith(".git") else value


def collect_server_version(server_binary: Path) -> dict[str, Any]:
    version = run_text([str(server_binary), "--version"]).strip()
    match = re.search(r"\bbuild\s+(\d+)\b", version)
    if match is None:
        fail("llama-server --version does not expose a build number")
    return {"version": version, "build_number": int(match.group(1))}


def collect_gpu_identity(*, required: bool) -> str:
    try:
        return run_text(
            [
                "nvidia-smi",
                "--query-gpu=name,driver_version,memory.total",
                "--format=csv,noheader",
            ]
        ).strip()
    except TransactionError:
        if required:
            raise
        return "SYNTHETIC_GPU_NOT_REQUIRED"


def validate_protocol(
    protocol: Any,
    prompt_bytes: bytes,
    *,
    synthetic: bool,
) -> dict[str, Any]:
    if not isinstance(protocol, dict):
        fail("real protocol must be an object")
    if protocol.get("schema_version") != PROTOCOL_VERSION:
        fail("real protocol schema_version drift")
    if protocol.get("owner_issue") != 162:
        fail("real protocol owner_issue drift")
    if protocol.get("status") != "REAL_TWO_PASS_EXTRACTION_ENVELOPE_FROZEN":
        fail("real protocol is not frozen")
    if protocol.get("freeze_requirements_remaining") != {}:
        fail("real protocol still has freeze requirements")
    if protocol.get("real_pilot_authorized") is not False:
        fail("#162 protocol may not authorize the real pilot")
    if protocol.get("basis_decomposition_authorized") is not False:
        fail("#162 protocol may not authorize decomposition")

    sample = protocol.get("sample_authority")
    if not isinstance(sample, dict):
        fail("protocol.sample_authority missing")
    if sample.get("primary_heldout_owner_issue") != 167:
        fail("primary held-out authority drifted from #167")
    if sample.get("primary_heldout_selection_local_to_162") is not False:
        fail("#162 cannot select primary held-out works")
    items = sample.get("calibration_items")
    if items != list(EXPECTED_SAMPLE_IDS) and not synthetic:
        fail("frozen calibration item order drift")

    normal = protocol.get("normal_pass")
    if not isinstance(normal, dict):
        fail("protocol.normal_pass missing")
    prompt_sha = sha256_bytes(prompt_bytes)
    if normal.get("prompt_sha256_utf8") != prompt_sha:
        fail(
            "Normal prompt digest mismatch: "
            f"manifest={normal.get('prompt_sha256_utf8')} file={prompt_sha}"
        )
    if not synthetic and prompt_sha != EXPECTED_NORMAL_PROMPT_SHA256:
        fail("Normal prompt is not the frozen #162 prompt")
    for key, expected in (
        ("temperature", 0.2),
        ("top_p", 1.0),
        ("max_tokens", 1024),
        ("reasoning_effort", "none"),
        ("cache_prompt", False),
        ("context_length", 8192),
        ("response_format", "plain_text"),
    ):
        if normal.get(key) != expected:
            fail(f"protocol.normal_pass.{key} drift")

    systemone = protocol.get("systemone")
    if not isinstance(systemone, dict):
        fail("protocol.systemone missing")
    for key, expected in (
        ("decision_contract", SYSTEMONE_VERSION),
        ("endpoint", EXPECTED_SYSTEMONE_ROUTE),
        ("structural_stage", "paper2-systemone-decision-v2"),
        ("probabilities_and_confidence", "audit_metadata_only"),
    ):
        if systemone.get(key) != expected:
            fail(f"protocol.systemone.{key} drift")
    if systemone.get("focus_stage") != "finite_selection_of_up_to_three_masked_evidence_units":
        fail("protocol SystemOne focus stage drift")

    isolation = protocol.get("replicate_isolation")
    if not isinstance(isolation, dict):
        fail("protocol.replicate_isolation missing")
    if isolation.get("replicates") != ["A", "B"]:
        fail("replicate order drift")
    if isolation.get("policy") != "separate_owned_llama_cpp_process_lifetime_per_replicate":
        fail("A/B process policy drift")
    for key in (
        "same_model_artifact_required",
        "same_normal_prompt_required",
        "same_masked_source_bytes_required",
        "same_configs_required",
        "cross_replicate_visibility_forbidden",
        "cache_reuse_across_replicates_forbidden",
        "retry_after_first_scientific_call_forbidden",
    ):
        if isolation.get(key) is not True:
            fail(f"protocol.replicate_isolation.{key} must be true")

    runtime = systemone.get("exact_runtime_identity")
    if not isinstance(runtime, dict):
        fail("protocol exact runtime identity missing")
    for key, expected in (
        ("repository", EXPECTED_JEV_REMOTE),
        ("revision", EXPECTED_JEV_HEAD),
        ("tree", EXPECTED_JEV_TREE),
        ("version", EXPECTED_JEV_VERSION),
        ("build_number", EXPECTED_JEV_BUILD),
        ("binary_sha256", EXPECTED_SERVER_SHA256),
        ("model_artifact_sha256", EXPECTED_MODEL_SHA256),
        ("systemone_route", EXPECTED_SYSTEMONE_ROUTE),
    ):
        if not synthetic and runtime.get(key) != expected:
            fail(f"protocol runtime identity {key} drift")
    return protocol


def validate_package_and_provenance(
    package: Any,
    provenance: Any,
    *,
    freeze_entries: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    if not isinstance(package, dict) or package.get(
        "schema_version"
    ) != "paper2-extraction-run-package-v1":
        fail("frozen run package schema mismatch")
    authority = package.get("authority")
    if not isinstance(authority, dict):
        fail("run-package authority is missing")
    # The package is the older #147 source/provenance authority.  Its
    # historical prompt digest predates the #162 frozen Normal prompt; the
    # live prompt identity is validated against the #162 protocol above.
    sources = package.get("sources")
    if not isinstance(sources, list) or len(sources) != 5:
        fail("run package must contain five sources")
    package_by_bundle: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(sources):
        if not isinstance(item, dict):
            fail(f"run package source {index} malformed")
        bundle = item.get("bundle_id")
        if bundle != EXPECTED_BUNDLES[index]:
            fail("run package bundle order drift")
        if bundle in package_by_bundle:
            fail("duplicate run package bundle")
        require_hex64(item.get("abstract_sha256_nfkc_ws1"), f"package {bundle} source digest")
        package_by_bundle[bundle] = item

    freeze_by_bundle = {item["bundle_id"]: item for item in freeze_entries}
    for bundle in EXPECTED_BUNDLES:
        if package_by_bundle[bundle]["abstract_sha256_nfkc_ws1"] != freeze_by_bundle[
            bundle
        ]["raw_normalized_sha256"]:
            fail(f"{bundle}: package/raw source digest mismatch")

    if not isinstance(provenance, dict):
        fail("provenance must be an object")
    entries = provenance.get("entries")
    if not isinstance(entries, list) or len(entries) != 5:
        fail("provenance must contain five entries")
    provenance_by_bundle: dict[str, dict[str, Any]] = {}
    for item in entries:
        if not isinstance(item, dict) or item.get("bundle_id") not in EXPECTED_BUNDLES:
            fail("provenance bundle membership malformed")
        bundle = item["bundle_id"]
        if bundle in provenance_by_bundle:
            fail("duplicate provenance bundle")
        if item.get("paper_id") != package_by_bundle[bundle].get("stable_identity"):
            fail(f"{bundle}: provenance/package stable identity mismatch")
        provenance_by_bundle[bundle] = copy.deepcopy(item)
    if set(provenance_by_bundle) != set(EXPECTED_BUNDLES):
        fail("provenance bundle membership mismatch")
    return package_by_bundle, provenance_by_bundle


def validate_freeze_and_bundles(
    freeze: Any,
    bundle_dir: Path,
    *,
    mask_terms_path: Path,
    freeze_path: Path,
    synthetic: bool,
) -> tuple[list[dict[str, Any]], dict[str, bytes], dict[str, dict[str, Any]]]:
    if not isinstance(freeze, dict):
        fail("preprocessing freeze must be an object")
    if freeze.get("schema_version") != "paper2-calibration-preprocessing-freeze-v1":
        fail("preprocessing freeze schema mismatch")
    if freeze.get("owner_issue") != 162:
        fail("preprocessing freeze owner mismatch")
    if freeze.get("classification") != "CALIBRATION_PREPROCESSING_LOCALLY_FROZEN":
        fail("preprocessing freeze classification mismatch")
    if freeze.get("source_item_count") != 5 or len(freeze.get("entries", [])) != 5:
        fail("preprocessing freeze source count mismatch")
    if freeze.get("model_calls") != 0 or freeze.get("scientific_transaction_consumed") is not False:
        fail("preprocessing evidence must be zero-spend")
    if freeze.get("raw_abstract_text_committed") is not False or freeze.get(
        "masked_abstract_text_committed"
    ) is not False:
        fail("raw/masked source commitment policy drift")
    terms_sha = sha256_file(mask_terms_path)
    if not synthetic and terms_sha != EXPECTED_MASK_TERMS_SHA256:
        fail("mask-term authority SHA-256 mismatch")
    if freeze.get("mask_term_policy", {}).get("mask_terms_sha256") != terms_sha:
        fail("preprocessing freeze mask-term identity mismatch")
    if freeze.get("authority_sha256", {}).get("mask_terms") != terms_sha:
        fail("preprocessing authority mask-term hash mismatch")
    freeze_sha = sha256_file(freeze_path)
    if not synthetic and freeze_sha != EXPECTED_PREPROCESSING_SHA256:
        fail("preprocessing freeze SHA-256 mismatch")

    entries: list[dict[str, Any]] = []
    for index, item in enumerate(freeze["entries"]):
        if not isinstance(item, dict) or item.get("bundle_id") != EXPECTED_BUNDLES[index]:
            fail("frozen bundle order drift")
        if item.get("sample_id") != EXPECTED_SAMPLE_IDS[index] and not synthetic:
            fail(f"{item.get('bundle_id')}: frozen sample identity drift")
        if item.get("raw_digest_matches_frozen_v1") is not True:
            fail(f"{item.get('bundle_id')}: raw digest was not frozen/matched")
        require_hex64(item.get("raw_normalized_sha256"), f"{item.get('bundle_id')} raw digest")
        require_hex64(item.get("masked_bundle_sha256"), f"{item.get('bundle_id')} bundle digest")
        entries.append(item)

    if not bundle_dir.is_dir():
        fail(f"masked bundle directory does not exist: {bundle_dir}")
    expected_names = {f"{bundle}.json" for bundle in EXPECTED_BUNDLES}
    actual_names = {item.name for item in bundle_dir.iterdir() if item.is_file()}
    if actual_names != expected_names:
        fail(f"masked bundle membership mismatch: expected={sorted(expected_names)} actual={sorted(actual_names)}")

    raw_by_bundle: dict[str, bytes] = {}
    bundle_by_id: dict[str, dict[str, Any]] = {}
    for item in entries:
        bundle = item["bundle_id"]
        path = bundle_dir / f"{bundle}.json"
        raw = path.read_bytes()
        actual_sha = sha256_bytes(raw)
        if actual_sha != item["masked_bundle_sha256"]:
            fail(f"{bundle}: frozen source bundle digest mismatch")
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise TransactionError(f"{bundle}: source bundle is not UTF-8 JSON: {exc}") from exc
        if canonical_json_bytes(parsed) != raw:
            fail(f"{bundle}: source bundle bytes are not frozen canonical JSON")
        if parsed.get("bundle_id") != bundle or parsed.get("schema_version") != SOURCE_VERSION:
            fail(f"{bundle}: source bundle identity/schema mismatch")
        try:
            validate_source(parsed)
        except ContractError as exc:
            raise TransactionError(f"{bundle}: invalid frozen source bundle: {exc}") from exc
        raw_by_bundle[bundle] = raw
        bundle_by_id[bundle] = parsed
    return entries, raw_by_bundle, bundle_by_id


def verify_runtime(
    *,
    repo_root: Path,
    llama_root: Path,
    server_binary: Path,
    model_path: Path,
    protocol_runtime: dict[str, Any],
    port: int,
    require_gpu: bool,
    synthetic: bool,
) -> dict[str, Any]:
    require_clean_git_checkout(llama_root, label="Jev llama.cpp checkout")
    remote = normalize_remote(run_text(["git", "remote", "get-url", "origin"], cwd=llama_root))
    expected_remote = normalize_remote(str(protocol_runtime.get("repository", "")))
    if remote != expected_remote or remote != normalize_remote(EXPECTED_JEV_REMOTE):
        fail(f"Jev remote mismatch: expected={expected_remote} actual={remote}")
    head = run_text(["git", "rev-parse", "HEAD"], cwd=llama_root).strip()
    tree = run_text(["git", "rev-parse", "HEAD^{tree}"], cwd=llama_root).strip()
    if head != protocol_runtime.get("revision") or tree != protocol_runtime.get("tree"):
        fail(f"Jev HEAD/tree mismatch: expected={protocol_runtime.get('revision')}/{protocol_runtime.get('tree')} actual={head}/{tree}")
    if not synthetic and (head != EXPECTED_JEV_HEAD or tree != EXPECTED_JEV_TREE):
        fail("Jev HEAD/tree is not the frozen #162 runtime")
    if not server_binary.is_file() or not os.access(server_binary, os.X_OK):
        fail(f"llama-server is not executable: {server_binary}")
    try:
        server_binary.resolve().relative_to(llama_root.resolve())
    except ValueError:
        fail("llama-server must be inside the attested Jev checkout")
    version = collect_server_version(server_binary)
    if version["build_number"] != protocol_runtime.get("build_number"):
        fail("llama-server build number mismatch")
    if not synthetic and version["build_number"] != EXPECTED_JEV_BUILD:
        fail("llama-server build is not the frozen build")
    if EXPECTED_JEV_VERSION not in version["version"]:
        fail("llama-server version is not the frozen Jev version")
    binary_sha = sha256_file(server_binary)
    if binary_sha != protocol_runtime.get("binary_sha256"):
        fail("llama-server binary SHA-256 mismatch")
    if not synthetic and binary_sha != EXPECTED_SERVER_SHA256:
        fail("llama-server binary is not the frozen build")
    if not model_path.is_file():
        fail(f"GGUF model is not a file: {model_path}")
    model_sha = sha256_file(model_path)
    if model_sha != protocol_runtime.get("model_artifact_sha256"):
        fail("GGUF SHA-256 mismatch")
    if not synthetic and model_sha != EXPECTED_MODEL_SHA256:
        fail("GGUF is not the frozen model artifact")
    if not port_is_free(DEFAULT_HOST, port):
        fail(f"{DEFAULT_HOST}:{port} is occupied")
    gpu = collect_gpu_identity(required=require_gpu)
    return {
        "repository": remote,
        "head": head,
        "tree": tree,
        "server_binary": str(server_binary),
        "version": version["version"],
        "build_number": version["build_number"],
        "binary_sha256": binary_sha,
        "model_path": str(model_path),
        "model_sha256": model_sha,
        "gpu": gpu,
        "host": DEFAULT_HOST,
        "port": port,
        "route": EXPECTED_SYSTEMONE_ROUTE,
    }


def verify_authorization(
    *,
    repo_root: Path,
    comment_id: int | None,
    status: str | None,
    authorized_head: str | None,
    authorized_tree: str | None,
    authorized_runner_blob: str | None,
    synthetic: bool,
) -> dict[str, Any]:
    if synthetic:
        return {"synthetic": True}
    if comment_id is None or comment_id <= 0:
        fail("#193 authorization comment ID is required")
    if status != "SCIENTIFIC_TRANSACTION_AUTHORIZED_UNSPENT":
        fail("#193 authorization status is missing or not exact")
    head = run_text(["git", "rev-parse", "HEAD"], cwd=repo_root).strip()
    tree = run_text(["git", "rev-parse", "HEAD^{tree}"], cwd=repo_root).strip()
    if authorized_head != head or authorized_tree != tree:
        fail("authorization main HEAD/tree does not match the execution checkout")
    blob = run_text(
        [
            "git",
            "rev-parse",
            "HEAD:scripts/paper2_extraction_two_pass_llama_cpp_transaction_v2.py",
        ],
        cwd=repo_root,
    ).strip()
    if authorized_runner_blob != blob:
        fail("authorization runner blob does not match the execution checkout")
    return {
        "comment_id": comment_id,
        "status": status,
        "head": head,
        "tree": tree,
        "runner_blob": blob,
    }


def preflight(
    *,
    repo_root: Path,
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
    comment_id: int | None,
    authorization_status: str | None,
    authorized_head: str | None,
    authorized_tree: str | None,
    authorized_runner_blob: str | None,
    synthetic: bool,
) -> dict[str, Any]:
    require_new_evidence_root(evidence_root, repo_root)
    relay_head, relay_tree = require_clean_git_checkout(
        repo_root, label="RelayTheory checkout"
    )
    authority_root = (
        Path(__file__).resolve().parent.parent if synthetic else repo_root
    )
    abstention_contract_path = authority_root / "research/paper2/extraction_abstention_v2.json"
    sampling_path = authority_root / "research/paper2/sampling_v1.json"
    postmortem_path = authority_root / "research/paper2/extraction_abstention_postmortem_v1.json"
    abstention_contract = load_json(abstention_contract_path)
    validate_abstention_contract(
        abstention_contract,
        sampling=load_json(sampling_path),
        postmortem=load_json(postmortem_path),
    )
    prompt_bytes = prompt_path.read_bytes()
    protocol = validate_protocol(
        load_json(protocol_path), prompt_bytes, synthetic=synthetic
    )
    prompt_sha = sha256_bytes(prompt_bytes)
    freeze = load_json(preprocessing_freeze_path)
    entries, bundle_raw, bundle_by_id = validate_freeze_and_bundles(
        freeze,
        bundle_dir,
        mask_terms_path=mask_terms_path,
        freeze_path=preprocessing_freeze_path,
        synthetic=synthetic,
    )
    package_by_bundle, provenance_by_bundle = validate_package_and_provenance(
        load_json(package_path),
        load_json(provenance_path),
        freeze_entries=entries,
    )
    runtime_block = protocol["systemone"]["exact_runtime_identity"]
    runtime = verify_runtime(
        repo_root=repo_root,
        llama_root=llama_root,
        server_binary=server_binary,
        model_path=model_path,
        protocol_runtime=runtime_block,
        port=port,
        require_gpu=require_gpu,
        synthetic=synthetic,
    )
    authorization = verify_authorization(
        repo_root=repo_root,
        comment_id=comment_id,
        status=authorization_status,
        authorized_head=authorized_head,
        authorized_tree=authorized_tree,
        authorized_runner_blob=authorized_runner_blob,
        synthetic=synthetic,
    )

    if EXPECTED_PLAN != {
        "server_launches": 2,
        "normal_calls": 2 * len(EXPECTED_BUNDLES),
        "systemone_calls": 2 * len(EXPECTED_BUNDLES),
        "total_calls": 4 * len(EXPECTED_BUNDLES),
    }:
        fail("transaction topology constant drift")
    if protocol["normal_pass"]["cache_prompt"] is not False:
        fail("cache_prompt must be false")
    path_outside(bundle_dir, repo_root, label="masked source bundle directory")
    path_outside(preprocessing_freeze_path, repo_root, label="preprocessing evidence")
    # The mask-term file is committed protocol authority; only raw/masked
    # source evidence must remain outside the RelayTheory checkout.
    return {
        "relaytheory": {"head": relay_head, "tree": relay_tree},
        "protocol": {
            "path": str(protocol_path),
            "sha256": sha256_file(protocol_path),
            "status": protocol["status"],
        },
        "prompt": {"path": str(prompt_path), "sha256": prompt_sha},
        "abstention_v2": {
            "path": str(abstention_contract_path),
            "sha256": sha256_file(abstention_contract_path),
            "status": abstention_contract["status"],
            "parent_classification": abstention_contract["parent_authority"][
                "postmortem_terminal_classification"
            ],
        },
        "preprocessing": {
            "freeze_path": str(preprocessing_freeze_path),
            "freeze_sha256": sha256_file(preprocessing_freeze_path),
            "mask_terms_path": str(mask_terms_path),
            "mask_terms_sha256": sha256_file(mask_terms_path),
            "bundle_order": list(EXPECTED_BUNDLES),
            "bundles": [
                {
                    "bundle_id": item["bundle_id"],
                    "raw_normalized_sha256": item["raw_normalized_sha256"],
                    "masked_bundle_sha256": item["masked_bundle_sha256"],
                    "segment_count": item.get("segmentation_count"),
                }
                for item in entries
            ],
        },
        "runtime": runtime,
        "authorization": authorization,
        "package_sha256": sha256_file(package_path),
        "provenance_sha256": sha256_file(provenance_path),
        "prompt_bytes": prompt_bytes,
        "bundle_raw": bundle_raw,
        "bundles": bundle_by_id,
        "package_by_bundle": package_by_bundle,
        "provenance_by_bundle": provenance_by_bundle,
    }


def server_command(
    *,
    server_binary: Path,
    model_path: Path,
    port: int,
    log_path: Path,
    replicate_id: str,
    fixture_plan: Path | None,
) -> list[str]:
    command = [
        str(server_binary),
        "-m",
        str(model_path),
        "--host",
        DEFAULT_HOST,
        "--port",
        str(port),
        "-ngl",
        "999",
        "-c",
        str(DEFAULT_CONTEXT),
        "-np",
        str(DEFAULT_SLOTS),
        "--no-context-shift",
        "-lv",
        "4",
        "--log-timestamps",
        "--log-file",
        str(log_path),
    ]
    if fixture_plan is not None:
        command.extend(["--fixture-plan", str(fixture_plan), "--replicate-id", replicate_id])
    return command


def start_owned_server(command: list[str]) -> subprocess.Popen[str]:
    try:
        return subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except OSError as exc:
        raise TransactionError(f"failed to launch owned llama-server: {exc}") from exc


def terminate_owned_server(process: subprocess.Popen[str]) -> int | None:
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=15.0)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5.0)
    return process.returncode


def get_json(url: str, *, timeout: float) -> Any:
    request = urllib.request.Request(
        url, headers={"Accept": "application/json"}, method="GET"
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (
        urllib.error.URLError,
        TimeoutError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise TransactionError(f"GET {url} failed: {exc}") from exc


def wait_until_ready(process: subprocess.Popen[str], origin: str) -> None:
    deadline = time.monotonic() + READY_TIMEOUT_SECONDS
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            fail(f"owned llama-server exited before readiness: {process.returncode}")
        try:
            health = get_json(f"{origin}/health", timeout=5.0)
            if isinstance(health, dict) and health.get("status") == "ok":
                return
        except TransactionError as exc:
            last_error = exc
        time.sleep(READY_POLL_SECONDS)
    suffix = f": {last_error}" if last_error else ""
    fail(f"owned llama-server did not become ready{suffix}")


def attest_runtime_http(
    *,
    origin: str,
    server_binary: Path,
    model_path: Path,
    runtime: dict[str, Any],
) -> dict[str, Any]:
    health = get_json(f"{origin}/health", timeout=20.0)
    models = get_json(f"{origin}/v1/models", timeout=20.0)
    props = get_json(f"{origin}/props", timeout=20.0)
    slots = get_json(f"{origin}/slots", timeout=20.0)
    if not isinstance(health, dict) or health.get("status") != "ok":
        fail("/health did not attest ready")
    if not isinstance(models, dict) or not isinstance(models.get("data"), list) or len(models["data"]) != 1:
        fail("/v1/models must expose exactly one model")
    model_id = models["data"][0].get("id") if isinstance(models["data"][0], dict) else None
    if not isinstance(model_id, str) or not model_id:
        fail("/v1/models model id missing")
    if not isinstance(props, dict):
        fail("/props must return an object")
    if not isinstance(slots, list) or len(slots) != DEFAULT_SLOTS:
        fail("/slots must expose exactly one slot")
    build_info = props.get("build_info")
    if not isinstance(build_info, str) or str(runtime["build_number"]) not in build_info:
        fail("/props build_info does not attest the server build")
    if runtime["head"] not in build_info and runtime["head"][:7] not in build_info:
        fail("/props build_info does not attest the Jev revision")
    if props.get("model_alias") != model_id:
        fail("/props model_alias mismatch")
    if Path(str(props.get("model_path", ""))).resolve() != model_path.resolve():
        fail("/props model_path mismatch")
    settings = props.get("default_generation_settings")
    if not isinstance(settings, dict) or settings.get("n_ctx") != DEFAULT_CONTEXT:
        fail("/props context mismatch")
    if props.get("total_slots") != DEFAULT_SLOTS:
        fail("/props slot count mismatch")
    slot = slots[0]
    if not isinstance(slot, dict) or slot.get("id") != 0 or slot.get("n_ctx") != DEFAULT_CONTEXT:
        fail("/slots identity/context mismatch")
    if props.get("model_ftype") not in {"Q4_K_M", "Q4_K - Medium"}:
        fail("/props model quantization mismatch")
    template = props.get("chat_template")
    if not isinstance(template, str) or not template:
        fail("/props chat_template missing")
    return {
        "model": model_id,
        "build_info": build_info,
        "model_alias": props.get("model_alias"),
        "model_path": str(model_path),
        "context": DEFAULT_CONTEXT,
        "slots": DEFAULT_SLOTS,
        "cache_prompt": False,
        "reasoning_effort": "none",
        "chat_template_sha256": sha256_bytes(template.encode("utf-8")),
        "health": health,
        "models": models,
        "props": props,
        "slots_response": slots,
        "server_binary_sha256": sha256_file(server_binary),
    }


def post_json(url: str, payload: dict[str, Any], *, timeout: float) -> tuple[bytes, dict[str, Any]]:
    request = urllib.request.Request(
        url,
        data=canonical_json_bytes(payload),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        raise HttpTransactionError(
            f"POST {url} returned HTTP {exc.code}: {raw[:500]!r}",
            status=exc.code,
            raw=raw,
        ) from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise HttpTransactionError(f"POST {url} failed: {exc}") from exc
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HttpTransactionError(
            f"POST {url} returned invalid JSON: {exc}", raw=raw
        ) from exc
    if not isinstance(value, dict):
        raise HttpTransactionError(f"POST {url} returned a non-object JSON response", raw=raw)
    return raw, value


def build_normal_request(prompt: str, bundle_raw: bytes, model: str) -> dict[str, Any]:
    try:
        bundle_text = bundle_raw.decode("utf-8").rstrip("\n")
    except UnicodeDecodeError as exc:
        raise TransactionError(f"frozen bundle is not UTF-8: {exc}") from exc
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": bundle_text},
        ],
        "temperature": 0.2,
        "top_p": 1.0,
        "max_tokens": 1024,
        "reasoning_effort": "none",
        "cache_prompt": False,
    }


def parse_normal_response(payload: dict[str, Any], model: str) -> str:
    response_model = payload.get("model")
    if response_model is not None and response_model != model:
        fail("Normal response model does not match request model")
    choices = payload.get("choices")
    if not isinstance(choices, list) or len(choices) != 1:
        fail("Normal response must contain exactly one choice")
    choice = choices[0]
    if not isinstance(choice, dict) or choice.get("finish_reason") not in {None, "stop"}:
        fail("Normal response did not finish cleanly")
    message = choice.get("message") if isinstance(choice, dict) else None
    if not isinstance(message, dict):
        fail("Normal response message missing")
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        fail("Normal response content is empty")
    return content


def normal_focus_span_ids(bundle: dict[str, Any], interpretation: str) -> list[str]:
    span_ids = [item["span_id"] for item in bundle["source_spans"]]
    if len(span_ids) <= 3:
        return list(span_ids)
    mentioned = []
    for value in SPAN_RE.findall(interpretation):
        if value in span_ids and value not in mentioned:
            mentioned.append(value)
    if not mentioned:
        fail("Normal output did not provide a bounded source-span focus for v2 SystemOne")
    selected = [sid for sid in span_ids if sid in mentioned][:3]
    if not selected:
        fail("Normal output focus did not resolve to a frozen source span")
    return selected


def build_systemone_transaction_request(
    *,
    bundle: dict[str, Any],
    interpretation: str,
    model: str,
) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    selected = normal_focus_span_ids(bundle, interpretation)
    focus_choices = selected + [NONE] * (3 - len(selected))
    compact = compact_focus_bundle(bundle, focus_choices)
    request = build_systemone_request(compact, interpretation, model)
    # The full masked source remains authoritative in the SystemOne state.  The
    # bounded compact view is the v2 structural decision surface; the 20-call
    # transaction forbids a second endpoint request for a separate focus pass.
    request["state"]["source"] = bundle
    request["state"]["focus_source"] = compact
    request["state"]["focus_source_span_ids"] = selected
    request["cache_prompt"] = False
    return request, compact, selected


def parse_artifact_error(exc: Exception) -> dict[str, Any]:
    result = {"type": type(exc).__name__, "message": str(exc)}
    if isinstance(exc, HttpTransactionError):
        result["status"] = exc.status
        if exc.raw:
            result["response_sha256"] = sha256_bytes(exc.raw)
    return result


def artifact_ref(root: Path, path: Path, sha256: str, *, size: int) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(root)),
        "sha256": sha256,
        "size": size,
    }


def freeze_artifact(root: Path, path: Path, raw: bytes) -> dict[str, Any]:
    digest = write_exclusive(path, raw)
    return artifact_ref(root, path, digest, size=len(raw))


def build_claim_ir(
    *,
    bundle_id: str,
    bundle: dict[str, Any],
    candidate: dict[str, Any],
    provenance: dict[str, Any],
    extractor_identity: str,
    extractor_revision: str,
    extracted_at: str,
) -> dict[str, Any]:
    restored = copy.deepcopy(provenance)
    restored.pop("bundle_id", None)
    restored["source_spans"] = [
        {"span_id": item["span_id"], "locator": f"Abstract evidence unit {item['span_id']}"}
        for item in bundle["source_spans"]
    ]
    claim = {
        "schema_version": CLAIM_VERSION,
        "claim_id": bundle_id,
        "provenance": restored,
        "extraction": {
            "extractor": extractor_identity,
            "extractor_version": extractor_revision,
            "procedure_version": SYSTEMONE_VERSION,
            "extracted_at": extracted_at,
            "manual_review_status": "unreviewed",
        },
        "claim_core": copy.deepcopy(candidate["claim_core"]),
    }
    try:
        validate_claim_ir(claim)
    except ValidationError as exc:
        raise TransactionError(f"{bundle_id}: full ClaimIR validation failed: {exc}") from exc
    return claim



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
        "systemone": {"attempted": False, "completed": False},
        "repair_count": 0,
    }
    row["bundle_artifact"] = freeze_artifact(
        root, row_root / "source-bundle.json", bundle_raw
    )

    normal_request = build_normal_request(prompt, bundle_raw, model)
    normal_request_raw = canonical_json_bytes(normal_request)
    row["normal"]["request"] = freeze_artifact(
        root, row_root / "normal-request.json", normal_request_raw
    )
    counters["normal_calls_attempted"] += 1
    row["normal"]["attempted"] = True
    try:
        normal_response_raw, normal_response = post_json(
            f"{origin}/v1/chat/completions",
            normal_request,
            timeout=HTTP_TIMEOUT_SECONDS,
        )
    except Exception as exc:
        if isinstance(exc, HttpTransactionError) and exc.raw:
            row["normal"]["response"] = freeze_artifact(
                root, row_root / "normal-response.raw", exc.raw
            )
        row["normal"]["error"] = parse_artifact_error(exc)
        raise
    row["normal"]["response"] = freeze_artifact(
        root, row_root / "normal-response.json", normal_response_raw
    )
    interpretation = parse_normal_response(normal_response, model)
    row["normal"]["output"] = freeze_artifact(
        root, row_root / "normal-output.txt", interpretation.encode("utf-8")
    )
    row["normal"]["completed"] = True
    counters["normal_calls_completed"] += 1

    systemone_request, compact_bundle, focus_ids = build_systemone_transaction_request(
        bundle=bundle,
        interpretation=interpretation,
        model=model,
    )
    row["systemone"]["focus_span_ids"] = focus_ids
    row["systemone"]["compact_bundle_sha256"] = canonical_digest(compact_bundle)
    systemone_request_raw = canonical_json_bytes(systemone_request)
    row["systemone"]["request"] = freeze_artifact(
        root, row_root / "systemone-request.json", systemone_request_raw
    )
    counters["systemone_calls_attempted"] += 1
    row["systemone"]["attempted"] = True
    try:
        systemone_response_raw, systemone_response = post_json(
            f"{origin}{EXPECTED_SYSTEMONE_ROUTE}",
            systemone_request,
            timeout=HTTP_TIMEOUT_SECONDS,
        )
    except Exception as exc:
        if isinstance(exc, HttpTransactionError) and exc.raw:
            row["systemone"]["response"] = freeze_artifact(
                root, row_root / "systemone-response.raw", exc.raw
            )
        row["systemone"]["error"] = parse_artifact_error(exc)
        raise

    row["systemone"]["response"] = freeze_artifact(
        root, row_root / "systemone-response.json", systemone_response_raw
    )
    # Wire/response-contract failures remain transaction failures.
    answers = parse_systemone_response(systemone_request, systemone_response)
    row["systemone"]["answers"] = freeze_artifact(
        root,
        row_root / "systemone-answers.json",
        canonical_json_bytes(answers),
    )
    row["systemone"]["completed"] = True
    counters["systemone_calls_completed"] += 1

    try:
        decision = decision_from_answers(compact_bundle, answers)
    except DecisionUnresolved as exc:
        field = str(exc).split(":", 1)[0].strip()
        metadata = systemone_response.get("answers", {}).get(field, {})
        row["outcome"] = "EXTRACTION_ABSTAIN"
        row["abstention"] = {
            "field": field,
            "choice": UNRESOLVED,
            "probabilities": metadata.get("probabilities"),
            "confidence": metadata.get("confidence"),
            "source_bundle_sha256": row["bundle_sha256"],
            "normal_output_sha256": row["normal"]["output"]["sha256"],
            "claim_ir_conversion_forbidden": True,
            "residual_conversion_forbidden": True,
            "retry_for_resolution_forbidden": True,
        }
        row["candidate_valid"] = False
        row["claim_ir_valid"] = False
        counters["extraction_abstain"] += 1
        write_json_exclusive(row_root / "artifact-record.json", row)
        return row
    except (TwoPassV2Error, ContractError, ValidationError) as exc:
        row["outcome"] = "EXTRACTION_FAILURE"
        row["extraction_failure"] = parse_artifact_error(exc)
        row["candidate_valid"] = False
        row["claim_ir_valid"] = False
        counters["extraction_failure"] += 1
        write_json_exclusive(row_root / "artifact-record.json", row)
        return row

    row["decision"] = freeze_artifact(
        root, row_root / "decision.json", canonical_json_bytes(decision)
    )
    try:
        candidate = compile_candidate(compact_bundle, decision)
    except (TwoPassV2Error, ContractError, ValidationError) as exc:
        row["outcome"] = "EXTRACTION_FAILURE"
        row["extraction_failure"] = parse_artifact_error(exc)
        row["candidate_valid"] = False
        row["claim_ir_valid"] = False
        counters["extraction_failure"] += 1
        write_json_exclusive(row_root / "artifact-record.json", row)
        return row

    row["candidate"] = freeze_artifact(
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
            extracted_at=utc_now(),
        )
    except TransactionError as exc:
        if "full ClaimIR validation failed:" not in str(exc):
            raise
        row["outcome"] = "EXTRACTION_FAILURE"
        row["extraction_failure"] = parse_artifact_error(exc)
        row["candidate_valid"] = True
        row["claim_ir_valid"] = False
        counters["extraction_failure"] += 1
        write_json_exclusive(row_root / "artifact-record.json", row)
        return row

    row["claim_ir"] = freeze_artifact(
        root, row_root / "claim-ir.json", canonical_json_bytes(claim)
    )
    row["candidate_valid"] = True
    row["claim_ir_valid"] = True
    row["outcome"] = "VALID_CLAIM_IR"
    counters["claim_ir_valid"] += 1
    write_json_exclusive(row_root / "artifact-record.json", row)
    return row


def compare_completed_claims(
    *,
    root: Path,
    replicate_rows: dict[str, list[dict[str, Any]]],
    source_bundles: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows_by_pass = {
        pass_id: {row["bundle_id"]: row for row in replicate_rows[pass_id]}
        for pass_id in ("A", "B")
    }
    report_rows: list[dict[str, Any]] = []
    valid_comparisons: list[dict[str, Any]] = []

    for bundle in EXPECTED_BUNDLES:
        row_a = rows_by_pass["A"][bundle]
        row_b = rows_by_pass["B"][bundle]
        outcome_a = row_a["outcome"]
        outcome_b = row_b["outcome"]

        if outcome_a == "VALID_CLAIM_IR" and outcome_b == "VALID_CLAIM_IR":
            pair_outcome = "BOTH_VALID"
            claim_a = load_json(root / row_a["claim_ir"]["path"])
            claim_b = load_json(root / row_b["claim_ir"]["path"])
            comparison = compare_claim_ir(claim_a, claim_b)
            valid_comparisons.append(comparison)
            differing_fields = {
                "claim_type": not comparison["same_claim_type"],
                "modality": not comparison["same_modality"],
                "scope": {
                    field: not comparison["scope_agreement_by_field"][field]["exact"]
                    for field in comparison["scope_agreement_by_field"]
                },
                "source_spans": not comparison["source_span_agreement"]["exact"],
                "node_structure": not comparison[
                    "node_structure_exact_under_id_renaming"
                ],
                "relation_structure": not comparison[
                    "relation_structure_exact_under_id_renaming"
                ],
                "node_descriptions": not comparison[
                    "node_descriptions_exact_after_normalization"
                ],
                "relation_descriptions": not comparison[
                    "relation_descriptions_exact_after_normalization"
                ],
            }
            graph_disagreement = bool(
                differing_fields["node_structure"]
                or differing_fields["relation_structure"]
            )
            adjudication_required = not comparison[
                "overall_exact_structural_equivalence"
            ]
            comparison_block: dict[str, Any] | None = comparison
            claim_digests = {
                "claim_ir_sha256_a": row_a["claim_ir"]["sha256"],
                "claim_ir_sha256_b": row_b["claim_ir"]["sha256"],
            }
        else:
            comparison_block = None
            differing_fields = None
            graph_disagreement = None
            adjudication_required = False
            claim_digests = {
                "claim_ir_sha256_a": (
                    row_a.get("claim_ir", {}).get("sha256")
                    if outcome_a == "VALID_CLAIM_IR"
                    else None
                ),
                "claim_ir_sha256_b": (
                    row_b.get("claim_ir", {}).get("sha256")
                    if outcome_b == "VALID_CLAIM_IR"
                    else None
                ),
            }
            if outcome_a == "EXTRACTION_ABSTAIN" and outcome_b == "EXTRACTION_ABSTAIN":
                pair_outcome = "BOTH_ABSTAIN"
            elif outcome_a == "VALID_CLAIM_IR" and outcome_b == "EXTRACTION_ABSTAIN":
                pair_outcome = "A_VALID_B_ABSTAIN"
            elif outcome_a == "EXTRACTION_ABSTAIN" and outcome_b == "VALID_CLAIM_IR":
                pair_outcome = "A_ABSTAIN_B_VALID"
            else:
                pair_outcome = "PAIR_EXTRACTION_FAILURE"

        report_rows.append(
            {
                "bundle_id": bundle,
                "source_bundle_sha256": sha256_bytes(
                    canonical_json_bytes(source_bundles[bundle])
                ),
                "outcome_a": outcome_a,
                "outcome_b": outcome_b,
                "pair_outcome": pair_outcome,
                **claim_digests,
                "comparison": comparison_block,
                "field_wise_differences": differing_fields,
                "source_only_adjudication": {
                    "required": adjudication_required,
                    "status": (
                        "REQUIRED_SOURCE_ONLY"
                        if adjudication_required
                        else "NOT_REQUIRED"
                    ),
                    "basis_visible": False,
                    "decomposition_outcome_visible": False,
                },
                "decomposition_visible_graph_structure_disagreement": graph_disagreement,
            }
        )

    scope_fields = (
        "conditions",
        "population",
        "substrate",
        "task",
        "temporal_scope",
    )
    pair_counts = {
        name: sum(1 for row in report_rows if row["pair_outcome"] == name)
        for name in (
            "BOTH_VALID",
            "BOTH_ABSTAIN",
            "A_VALID_B_ABSTAIN",
            "A_ABSTAIN_B_VALID",
            "PAIR_EXTRACTION_FAILURE",
        )
    }
    if valid_comparisons:
        scope_counts = {
            field: sum(
                1
                for item in valid_comparisons
                if item["scope_agreement_by_field"][field]["exact"]
            )
            for field in scope_fields
        }
        valid_aggregate = {
            "n_both_valid": len(valid_comparisons),
            "exact_structural_agreement_count": sum(
                1
                for item in valid_comparisons
                if item["overall_exact_structural_equivalence"]
            ),
            "exact_structural_agreement_rate": sum(
                1
                for item in valid_comparisons
                if item["overall_exact_structural_equivalence"]
            )
            / len(valid_comparisons),
            "exact_full_agreement_count": sum(
                1
                for item in valid_comparisons
                if item["overall_exact_full_equivalence"]
            ),
            "same_claim_type_count": sum(
                1 for item in valid_comparisons if item["same_claim_type"]
            ),
            "same_modality_count": sum(
                1 for item in valid_comparisons if item["same_modality"]
            ),
            "scope_agreement_count_by_field": scope_counts,
        }
    else:
        valid_aggregate = {
            "n_both_valid": 0,
            "exact_structural_agreement_count": 0,
            "exact_structural_agreement_rate": None,
            "exact_full_agreement_count": 0,
            "same_claim_type_count": 0,
            "same_modality_count": 0,
            "scope_agreement_count_by_field": {field: 0 for field in scope_fields},
        }

    replicate_outcomes = [
        row["outcome"]
        for pass_id in ("A", "B")
        for row in replicate_rows[pass_id]
    ]
    aggregate = {
        "all_bundle_pairs_n": len(report_rows),
        "pair_outcome_counts": pair_counts,
        "replicate_outcome_counts": {
            "VALID_CLAIM_IR": replicate_outcomes.count("VALID_CLAIM_IR"),
            "EXTRACTION_ABSTAIN": replicate_outcomes.count("EXTRACTION_ABSTAIN"),
            "EXTRACTION_FAILURE": replicate_outcomes.count("EXTRACTION_FAILURE"),
        },
        "selected_extraction_attempts": len(replicate_outcomes),
        "primary_analyzable_replicate_rows": replicate_outcomes.count(
            "VALID_CLAIM_IR"
        ),
        "explicit_attrition_replicate_rows": (
            replicate_outcomes.count("EXTRACTION_ABSTAIN")
            + replicate_outcomes.count("EXTRACTION_FAILURE")
        ),
        "claim_ir_comparison_denominator": len(valid_comparisons),
        "valid_valid_comparison": valid_aggregate,
    }
    report = {
        "schema_version": "paper2-two-pass-ab-outcome-comparison-v2",
        "owner_issue": OWNER_ISSUE,
        "status": "BASIS_BLIND_OUTCOME_PAIRING_BEFORE_DECOMPOSITION",
        "basis_visible": False,
        "decomposition_outcome_visible": False,
        "all_five_pairs_reported": True,
        "claim_ir_comparison_restricted_to_both_valid": True,
        "rows": report_rows,
        "aggregate": aggregate,
    }
    report_path = root / "ab-outcome-comparison.json"
    report["report_artifact"] = freeze_artifact(
        root, report_path, canonical_json_bytes(report)
    )
    return report

def validate_receipt_contract(receipt: dict[str, Any]) -> None:
    expected = {
        "schema_version",
        "owner_issue",
        "status",
        "synthetic",
        "plan",
        "counters",
        "authority",
        "replicates",
        "retry_replay_fallback",
        "evidence_root",
        "basis_decomposition_executed",
    }
    if set(receipt) != expected:
        fail(f"receipt contract keys drift: missing={sorted(expected-set(receipt))} extra={sorted(set(receipt)-expected)}")
    if receipt["schema_version"] != RECEIPT_VERSION or receipt["owner_issue"] != OWNER_ISSUE:
        fail("receipt identity drift")
    if receipt["plan"] != EXPECTED_PLAN:
        fail("receipt plan drift")
    if receipt["basis_decomposition_executed"] is not False:
        fail("receipt basis decomposition flag must remain false")
    if receipt["retry_replay_fallback"] != {"retry": 0, "replay": 0, "fallback": 0}:
        fail("receipt retry/replay/fallback drift")
    counters = receipt["counters"]
    for key in (
        "server_launches",
        "normal_calls_attempted",
        "normal_calls_completed",
        "systemone_calls_attempted",
        "systemone_calls_completed",
        "total_calls_attempted",
        "total_calls_completed",
        "scientific_calls_attempted",
        "claim_ir_valid",
        "extraction_abstain",
        "extraction_failure",
    ):
        if not isinstance(counters.get(key), int) or counters[key] < 0:
            fail(f"receipt counter {key} malformed")
    if not isinstance(receipt["replicates"], list) or len(receipt["replicates"]) > 2:
        fail("receipt replicate records malformed")


def initial_summary(evidence_root: Path, *, synthetic: bool) -> dict[str, Any]:
    return {
        "schema_version": SUMMARY_VERSION,
        "owner_issue": OWNER_ISSUE,
        "classification": None,
        "synthetic": synthetic,
        "evidence_root": str(evidence_root),
        "plan": copy.deepcopy(EXPECTED_PLAN),
        "counters": {
            "server_launches": 0,
            "normal_calls_attempted": 0,
            "normal_calls_completed": 0,
            "systemone_calls_attempted": 0,
            "systemone_calls_completed": 0,
            "total_calls_attempted": 0,
            "total_calls_completed": 0,
            "scientific_calls_attempted": 0,
            "claim_ir_valid": 0,
            "extraction_abstain": 0,
            "extraction_failure": 0,
        },
        "retry_replay_fallback": {"retry": 0, "replay": 0, "fallback": 0},
        "basis_decomposition_executed": False,
        "replicates": [],
        "repair_count": 0,
    }


def run_transaction(
    *,
    repo_root: Path,
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
    comment_id: int | None = None,
    authorization_status: str | None = None,
    authorized_head: str | None = None,
    authorized_tree: str | None = None,
    authorized_runner_blob: str | None = None,
    synthetic: bool = False,
    fixture_plan: Path | None = None,
) -> tuple[int, dict[str, Any]]:
    summary = initial_summary(evidence_root, synthetic=synthetic)
    process: subprocess.Popen[str] | None = None
    evidence_created = False
    preflight_data: dict[str, Any] | None = None
    try:
        preflight_data = preflight(
            repo_root=repo_root,
            protocol_path=protocol_path,
            prompt_path=prompt_path,
            mask_terms_path=mask_terms_path,
            preprocessing_freeze_path=preprocessing_freeze_path,
            bundle_dir=bundle_dir,
            package_path=package_path,
            provenance_path=provenance_path,
            llama_root=llama_root,
            server_binary=server_binary,
            model_path=model_path,
            evidence_root=evidence_root,
            port=port,
            require_gpu=require_gpu,
            comment_id=comment_id,
            authorization_status=authorization_status,
            authorized_head=authorized_head,
            authorized_tree=authorized_tree,
            authorized_runner_blob=authorized_runner_blob,
            synthetic=synthetic,
        )
        summary["authority"] = {
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
        evidence_root.mkdir(parents=True, exist_ok=False)
        evidence_created = True
        write_json_exclusive(evidence_root / "preflight-attestation.json", summary["authority"])
        prompt = preflight_data["prompt_bytes"].decode("utf-8")
        runtime = preflight_data["runtime"]
        relay_head = preflight_data["relaytheory"]["head"]
        extractor_identity = "paper2-two-pass-llama-cpp-transaction-v2"
        extractor_revision = (
            f"relaytheory={relay_head};jev={runtime['head']};build={runtime['build_number']};"
            f"model_sha256={runtime['model_sha256']}"
        )
        write_json_exclusive(
            evidence_root / "runner-contract.json",
            {
                "extractor_identity": extractor_identity,
                "extractor_revision": extractor_revision,
                "normal_prompt_sha256": preflight_data["prompt"]["sha256"],
                "systemone_route": EXPECTED_SYSTEMONE_ROUTE,
                "cache_prompt": False,
                "temperature": 0.2,
                "top_p": 1.0,
                "max_tokens": 1024,
                "reasoning_effort": "none",
                "planned_topology": EXPECTED_PLAN,
                "retry_replay_fallback": {"retry": 0, "replay": 0, "fallback": 0},
            },
        )
        counters = summary["counters"]
        model: str | None = None
        for replicate_id in ("A", "B"):
            replicate_record: dict[str, Any] = {
                "replicate_id": replicate_id,
                "started_at": utc_now(),
                "bundle_order": [],
                "rows": [],
                "cleanup": {"owned_process": False, "terminated": False, "exit_code": None},
            }
            process = None
            try:
                if not port_is_free(DEFAULT_HOST, port):
                    fail(f"{DEFAULT_HOST}:{port} became occupied before replicate {replicate_id}")
                if sha256_file(server_binary) != runtime["binary_sha256"]:
                    fail("llama-server binary changed after preflight")
                if sha256_file(model_path) != runtime["model_sha256"]:
                    fail("GGUF changed after preflight")
                current_jev_head = run_text(["git", "rev-parse", "HEAD"], cwd=llama_root).strip()
                current_jev_tree = run_text(["git", "rev-parse", "HEAD^{tree}"], cwd=llama_root).strip()
                if current_jev_head != runtime["head"] or current_jev_tree != runtime["tree"]:
                    fail("Jev HEAD/tree changed after preflight")
                log_path = evidence_root / replicate_id / "llama-server.log"
                command = server_command(
                    server_binary=server_binary,
                    model_path=model_path,
                    port=port,
                    log_path=log_path,
                    replicate_id=replicate_id,
                    fixture_plan=fixture_plan,
                )
                process = start_owned_server(command)
                counters["server_launches"] += 1
                replicate_record["cleanup"]["owned_process"] = True
                replicate_record["pid"] = process.pid
                replicate_record["server_command"] = command
                origin = f"http://{DEFAULT_HOST}:{port}"
                wait_until_ready(process, origin)
                replicate_record["runtime"] = attest_runtime_http(
                    origin=origin,
                    server_binary=server_binary,
                    model_path=model_path,
                    runtime=runtime,
                )
                attested_model = replicate_record["runtime"]["model"]
                if model is None:
                    model = attested_model
                elif model != attested_model:
                    fail("A/B server model aliases differ")
                for bundle_id in EXPECTED_BUNDLES:
                    replicate_record["bundle_order"].append(bundle_id)
                    row = execute_bundle(
                        root=evidence_root,
                        replicate_id=replicate_id,
                        bundle_id=bundle_id,
                        bundle_raw=preflight_data["bundle_raw"][bundle_id],
                        bundle=preflight_data["bundles"][bundle_id],
                        source_digest=next(
                            item["raw_normalized_sha256"]
                            for item in preflight_data["preprocessing"]["bundles"]
                            if item["bundle_id"] == bundle_id
                        ),
                        prompt=prompt,
                        model=model,
                        origin=origin,
                        provenance=preflight_data["provenance_by_bundle"][bundle_id],
                        extractor_identity=extractor_identity,
                        extractor_revision=extractor_revision,
                        counters=counters,
                    )
                    replicate_record["rows"].append(row)
            finally:
                if process is not None:
                    replicate_record["cleanup"]["exit_code"] = terminate_owned_server(process)
                    replicate_record["cleanup"]["terminated"] = process.poll() is not None
                replicate_record["completed_at"] = utc_now()
                summary["replicates"].append(replicate_record)
                process = None
            if replicate_id == "A" and not port_is_free(DEFAULT_HOST, port):
                fail("owned replicate A did not release its port before replicate B")

        counters["total_calls_attempted"] = (
            counters["normal_calls_attempted"] + counters["systemone_calls_attempted"]
        )
        counters["total_calls_completed"] = (
            counters["normal_calls_completed"] + counters["systemone_calls_completed"]
        )
        if counters["server_launches"] != EXPECTED_PLAN["server_launches"]:
            fail("executed server-launch count does not equal frozen plan")
        if counters["normal_calls_attempted"] != EXPECTED_PLAN["normal_calls"]:
            fail("executed Normal-call count does not equal frozen plan")
        if counters["systemone_calls_attempted"] != EXPECTED_PLAN["systemone_calls"]:
            fail("executed SystemOne-call count does not equal frozen plan")
        if counters["total_calls_attempted"] != EXPECTED_PLAN["total_calls"]:
            fail("executed total model-facing call count does not equal frozen plan")
        total_bundle_outcomes = (
            counters["claim_ir_valid"]
            + counters["extraction_abstain"]
            + counters["extraction_failure"]
        )
        if total_bundle_outcomes != 2 * len(EXPECTED_BUNDLES):
            fail("not all ten bundle outcomes were frozen")
        summary["comparison"] = compare_completed_claims(
            root=evidence_root,
            replicate_rows={
                record["replicate_id"]: record["rows"]
                for record in summary["replicates"]
            },
            source_bundles=preflight_data["bundles"],
        )
        summary["classification"] = (
            "SYNTHETIC_TRANSACTION_COMPLETED"
            if synthetic
            else "SCIENTIFIC_TRANSACTION_COMPLETED"
        )
        counters["scientific_calls_attempted"] = 0 if synthetic else counters["total_calls_attempted"]
    except Exception as exc:
        counters = summary["counters"]
        counters["total_calls_attempted"] = (
            counters["normal_calls_attempted"] + counters["systemone_calls_attempted"]
        )
        counters["total_calls_completed"] = (
            counters["normal_calls_completed"] + counters["systemone_calls_completed"]
        )
        counters["scientific_calls_attempted"] = 0 if synthetic else counters["total_calls_attempted"]
        summary["error"] = parse_artifact_error(exc)
        summary["classification"] = (
            "PREEXECUTION_BLOCKED"
            if counters["scientific_calls_attempted"] == 0
            else "SCIENTIFIC_TRANSACTION_CONSUMED_INCOMPLETE"
        )
    finally:
        if process is not None:
            terminate_owned_server(process)
            process = None
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
                "retry_replay_fallback": summary["retry_replay_fallback"],
                "evidence_root": summary["evidence_root"],
                "basis_decomposition_executed": False,
            }
            validate_receipt_contract(receipt)
            receipt_path = evidence_root / "transaction-receipt.json"
            receipt_sha = write_json_exclusive(receipt_path, receipt)
            summary["receipt"] = artifact_ref(
                evidence_root, receipt_path, receipt_sha, size=receipt_path.stat().st_size
            )
            write_json_exclusive(evidence_root / "transaction-summary.json", summary)

    return (0 if summary["classification"] in {
        "SCIENTIFIC_TRANSACTION_COMPLETED",
        "SYNTHETIC_TRANSACTION_COMPLETED",
    } else 2), summary


def init_git_repo(path: Path, *, remote: str | None = None) -> None:
    path.mkdir(parents=True, exist_ok=True)
    run_text(["git", "init", "-q"], cwd=path)
    run_text(["git", "config", "user.email", "selftest@example.invalid"], cwd=path)
    run_text(["git", "config", "user.name", "selftest"], cwd=path)
    (path / "README").write_text("synthetic self-test\n", encoding="utf-8")
    run_text(["git", "add", "README"], cwd=path)
    run_text(["git", "commit", "-qm", "synthetic self-test"], cwd=path)
    if remote is not None:
        run_text(["git", "remote", "add", "origin", remote], cwd=path)


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

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-m")
parser.add_argument("--host")
parser.add_argument("--port", type=int)
parser.add_argument("-ngl")
parser.add_argument("-c", type=int)
parser.add_argument("-np", type=int)
parser.add_argument("--no-context-shift", action="store_true")
parser.add_argument("-lv")
parser.add_argument("--log-timestamps", action="store_true")
parser.add_argument("--log-file")
parser.add_argument("--fixture-plan")
parser.add_argument("--replicate-id")
args, _ = parser.parse_known_args()

root = Path(__file__).resolve().parents[2]
revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
plan = json.loads(Path(args.fixture_plan).read_text()) if args.fixture_plan else {}
replicate = args.replicate_id or "REAL"
record_path = Path(plan["record"]) if plan.get("record") else None
if args.log_file:
    Path(args.log_file).parent.mkdir(parents=True, exist_ok=True)
    Path(args.log_file).write_text("synthetic server started\n", encoding="utf-8")

def record(kind, payload, bundle_id):
    if record_path:
        record_path.parent.mkdir(parents=True, exist_ok=True)
        with record_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"replicate": replicate, "kind": kind, "bundle_id": bundle_id, "payload": payload}, sort_keys=True) + "\n")

def fail_for(kind, bundle_id):
    values = plan.get(kind, {}).get(replicate, [])
    return bundle_id in values

def answer_for(name, question, source_ids, collapse=False):
    criteria = question["criteria"]
    if name == "claim_type": return "relation"
    if name == "modality": return "descriptive"
    if name.startswith("scope__"): return "no"
    if name == "n1__active": return "yes"
    if name == "n1__role": return "state_or_structure"
    if name == "n1__anchor": return source_ids[0]
    if name == "n1__grounding": return "explicit"
    if name.startswith("n1__span__"): return "yes" if name.endswith(source_ids[0]) else "no"
    if name == "n2__active": return "yes" if len(source_ids) > 1 else "no"
    if name == "n2__role": return "response_or_outcome"
    if name == "n2__anchor": return source_ids[0] if collapse else source_ids[1]
    if name == "n2__grounding": return "explicit"
    if name.startswith("n2__span__"):
        target = source_ids[0] if collapse else source_ids[1]
        return "yes" if name.endswith(target) else "no"
    if name.startswith("n3__"):
        if name == "n3__active": return "no"
        return next(iter(criteria))
    if name == "r1__active": return "yes" if len(source_ids) > 1 else "no"
    if name == "r1__kind": return "depends_on"
    if name == "r1__arg1": return "n1"
    if name == "r1__arg2": return "n2"
    if name == "r1__grounding": return "explicit"
    if name.startswith("r1__span__"):
        target = source_ids[2] if len(source_ids) > 2 else source_ids[0]
        return "yes" if name.endswith(target) else "no"
    if name.startswith("r2__"):
        if name == "r2__active": return "no"
        return next(iter(criteria))
    return next(key for key in criteria if key != "__unresolved__")

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *items): return
    def out(self, value, status=200):
        raw = json.dumps(value, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
    def do_GET(self):
        if self.path == "/health": self.out({"status":"ok"}); return
        if self.path == "/v1/models": self.out({"data":[{"id":"fake-model"}]}); return
        if self.path == "/props":
            self.out({"build_info":f"fake build 11066 {revision}", "model_alias":"fake-model", "model_path":str(Path(args.m).resolve()), "default_generation_settings":{"n_ctx":args.c}, "total_slots":args.np, "model_ftype":"Q4_K - Medium", "chat_template":"synthetic-template"}); return
        if self.path == "/slots": self.out([{"id":0,"n_ctx":args.c}]); return
        self.out({"error":"not found"}, 404)
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length).decode("utf-8"))
        if body.get("cache_prompt") is not False:
            self.out({"error":"cache_prompt must be false"}, 400); return
        if self.path == "/v1/chat/completions":
            messages = body.get("messages")
            bundle = json.loads(messages[1]["content"])
            bundle_id = bundle["bundle_id"]
            record("normal", body, bundle_id)
            if fail_for("normal_fail", bundle_id): self.out({"error":"synthetic normal failure"}, 500); return
            self.out({"model":"fake-model", "choices":[{"message":{"role":"assistant","content":f"Synthetic {replicate}-only interpretation for {bundle_id}; focus s1 s2 s3."},"finish_reason":"stop"}]}); return
        if self.path == "/v1/systemone":
            source = body["state"]["source"]
            bundle_id = source["bundle_id"]
            record("systemone", body, bundle_id)
            if fail_for("systemone_fail", bundle_id): self.out({"error":"synthetic SystemOne failure"}, 500); return
            source_ids = [item["span_id"] for item in body["state"]["focus_source"]["source_spans"]]
            invalid = fail_for("invalid_choice", bundle_id)
            nonzero = fail_for("nonzero_tokens", bundle_id)
            collapse = fail_for("collapse_anchors", bundle_id)
            unresolved = fail_for("unresolved", bundle_id)
            answers = {}
            for name, question in body["questions"].items():
                choice = answer_for(name, question, source_ids, collapse=collapse)
                if invalid and name == "modality": choice = "not-a-frozen-choice"
                if unresolved and name == "n1__role": choice = "__unresolved__"
                answers[name] = {"type":"choice", "choice":choice, "probabilities":{choice:1.0}, "confidence":1.0}
            self.out({"model":"fake-model", "answers":answers, "usage":{"input_tokens":1,"output_tokens":1 if nonzero else 0}}); return
        self.out({"error":"not found"}, 404)

ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()
'''


def write_fake_server(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FAKE_SERVER, encoding="utf-8")
    path.chmod(0o755)


def free_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((DEFAULT_HOST, 0))
        return int(sock.getsockname()[1])
    finally:
        sock.close()


def make_synthetic_fixture(root: Path, plan: dict[str, Any] | None = None) -> dict[str, Any]:
    repo = root / "relay-theory"
    init_git_repo(repo)
    llama = root / "llama.cpp"
    init_git_repo(llama, remote=EXPECTED_JEV_REMOTE + ".git")
    server = llama / "build" / "bin" / "llama-server"
    write_fake_server(server)
    run_text(["git", "add", "build/bin/llama-server"], cwd=llama)
    run_text(["git", "commit", "-qm", "add synthetic server"], cwd=llama)
    jev_head = run_text(["git", "rev-parse", "HEAD"], cwd=llama).strip()
    jev_tree = run_text(["git", "rev-parse", "HEAD^{tree}"], cwd=llama).strip()
    model = root / "synthetic-model.gguf"
    model.write_bytes(b"synthetic model artifact")
    model_sha = sha256_file(model)
    prompt = root / "synthetic-prompt.md"
    prompt.write_text("Synthetic prompt; use s1 and s2.\n", encoding="utf-8")
    prompt_sha = sha256_file(prompt)
    mask_terms = root / "synthetic-mask-terms.json"
    mask_terms.write_text('{"synthetic":true}\n', encoding="utf-8")
    mask_sha = sha256_file(mask_terms)
    bundles = root / "bundles"
    bundles.mkdir()
    bundle_digests: dict[str, str] = {}
    raw_digests: dict[str, str] = {}
    for bundle_id in EXPECTED_BUNDLES:
        bundle = {
            "schema_version": SOURCE_VERSION,
            "bundle_id": bundle_id,
            "source_language": "en",
            "source_spans": [
                {"span_id": "s1", "text": f"Synthetic evidence {bundle_id} unit one."},
                {"span_id": "s2", "text": f"Synthetic evidence {bundle_id} unit two."},
                {"span_id": "s3", "text": f"Synthetic relation for {bundle_id}."},
            ],
        }
        raw = canonical_json_bytes(bundle)
        (bundles / f"{bundle_id}.json").write_bytes(raw)
        bundle_digests[bundle_id] = sha256_bytes(raw)
        raw_digests[bundle_id] = sha256_bytes(f"synthetic raw {bundle_id}".encode())
    freeze = {
        "schema_version": "paper2-calibration-preprocessing-freeze-v1",
        "owner_issue": 162,
        "classification": "CALIBRATION_PREPROCESSING_LOCALLY_FROZEN",
        "model_calls": 0,
        "scientific_transaction_consumed": False,
        "raw_abstract_text_committed": False,
        "masked_abstract_text_committed": False,
        "source_item_count": 5,
        "mask_term_policy": {"mask_terms_sha256": mask_sha},
        "authority_sha256": {"mask_terms": mask_sha},
        "entries": [
            {
                "bundle_id": bundle_id,
                "sample_id": f"SYNTHETIC-{bundle_id}",
                "raw_normalized_sha256": raw_digests[bundle_id],
                "raw_digest_matches_frozen_v1": True,
                "masked_bundle_sha256": bundle_digests[bundle_id],
                "segmentation_count": 3,
            }
            for bundle_id in EXPECTED_BUNDLES
        ],
    }
    freeze_path = root / "preprocessing-freeze.json"
    freeze_path.write_bytes(canonical_json_bytes(freeze))
    package = {
        "schema_version": "paper2-extraction-run-package-v1",
        "authority": {"prompt_sha256_utf8": prompt_sha},
        "sources": [
            {
                "bundle_id": bundle_id,
                "sample_id": f"SYNTHETIC-{bundle_id}",
                "stable_identity": f"synthetic:{bundle_id}",
                "abstract_sha256_nfkc_ws1": raw_digests[bundle_id],
            }
            for bundle_id in EXPECTED_BUNDLES
        ],
    }
    package_path = root / "package.json"
    package_path.write_bytes(canonical_json_bytes(package))
    provenance = {
        "entries": [
            {
                "bundle_id": bundle_id,
                "paper_id": f"synthetic:{bundle_id}",
                "source_language": "en",
                "source_spans": [{"span_id": "s1", "locator": "Synthetic"}],
                "authors": [],
                "institutions": [],
                "venue": None,
                "citation_count": None,
                "construct_labels": [],
            }
            for bundle_id in EXPECTED_BUNDLES
        ]
    }
    provenance_path = root / "provenance.json"
    provenance_path.write_bytes(canonical_json_bytes(provenance))
    runtime = {
        "repository": EXPECTED_JEV_REMOTE,
        "revision": jev_head,
        "tree": jev_tree,
        "version": EXPECTED_JEV_VERSION,
        "build_number": EXPECTED_JEV_BUILD,
        "binary_sha256": sha256_file(server),
        "model_artifact_sha256": model_sha,
        "systemone_route": EXPECTED_SYSTEMONE_ROUTE,
    }
    protocol = {
        "schema_version": PROTOCOL_VERSION,
        "owner_issue": 162,
        "status": "REAL_TWO_PASS_EXTRACTION_ENVELOPE_FROZEN",
        "freeze_requirements_remaining": {},
        "real_pilot_authorized": False,
        "basis_decomposition_authorized": False,
        "sample_authority": {
            "calibration_items": list(EXPECTED_SAMPLE_IDS),
            "primary_heldout_owner_issue": 167,
            "primary_heldout_selection_local_to_162": False,
        },
        "normal_pass": {
            "prompt_sha256_utf8": prompt_sha,
            "temperature": 0.2,
            "top_p": 1.0,
            "max_tokens": 1024,
            "reasoning_effort": "none",
            "cache_prompt": False,
            "context_length": 8192,
            "response_format": "plain_text",
        },
        "systemone": {
            "decision_contract": SYSTEMONE_VERSION,
            "endpoint": EXPECTED_SYSTEMONE_ROUTE,
            "focus_stage": "finite_selection_of_up_to_three_masked_evidence_units",
            "structural_stage": "paper2-systemone-decision-v2",
            "probabilities_and_confidence": "audit_metadata_only",
            "exact_runtime_identity": runtime,
        },
        "replicate_isolation": {
            "replicates": ["A", "B"],
            "policy": "separate_owned_llama_cpp_process_lifetime_per_replicate",
            "same_model_artifact_required": True,
            "same_normal_prompt_required": True,
            "same_masked_source_bytes_required": True,
            "same_configs_required": True,
            "cross_replicate_visibility_forbidden": True,
            "cache_reuse_across_replicates_forbidden": True,
            "retry_after_first_scientific_call_forbidden": True,
        },
    }
    protocol_path = root / "protocol.json"
    protocol_path.write_bytes(canonical_json_bytes(protocol))
    record = root / "requests.jsonl"
    fixture_plan = root / "fixture-plan.json"
    plan_value = copy.deepcopy(plan or {})
    plan_value["record"] = str(record)
    fixture_plan.write_bytes(canonical_json_bytes(plan_value))
    return {
        "repo": repo,
        "llama": llama,
        "server": server,
        "model": model,
        "prompt": prompt,
        "mask_terms": mask_terms,
        "freeze": freeze_path,
        "bundles": bundles,
        "package": package_path,
        "provenance": provenance_path,
        "protocol": protocol_path,
        "fixture_plan": fixture_plan,
        "record": record,
        "port": free_port(),
    }


def expect(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def load_request_log(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def run_fixture(fixture: dict[str, Any], *, plan: dict[str, Any] | None = None) -> tuple[int, dict[str, Any]]:
    if plan:
        fixture["fixture_plan"].write_bytes(canonical_json_bytes({**plan, "record": str(fixture["record"])}))
    evidence = fixture["repo"].parent / "evidence"
    return run_transaction(
        repo_root=fixture["repo"],
        protocol_path=fixture["protocol"],
        prompt_path=fixture["prompt"],
        mask_terms_path=fixture["mask_terms"],
        preprocessing_freeze_path=fixture["freeze"],
        bundle_dir=fixture["bundles"],
        package_path=fixture["package"],
        provenance_path=fixture["provenance"],
        llama_root=fixture["llama"],
        server_binary=fixture["server"],
        model_path=fixture["model"],
        evidence_root=evidence,
        port=fixture["port"],
        require_gpu=False,
        synthetic=True,
        fixture_plan=fixture["fixture_plan"],
    )


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="relaytheory-193-v2-selftest-") as temp:
        root = Path(temp)
        fixture = make_synthetic_fixture(root / "success")
        # Reproduce the historical #147 package authority: the source package
        # predates the current #162 Normal prompt and must not override it.
        package = load_json(fixture["package"])
        package["authority"]["prompt_sha256_utf8"] = "f" * 64
        fixture["package"].write_bytes(canonical_json_bytes(package))
        rc, summary = run_fixture(fixture)
        expect(rc == 0, f"synthetic success rc: {summary}")
        expect(summary["classification"] == "SYNTHETIC_TRANSACTION_COMPLETED", "synthetic classification")
        expect(summary["counters"]["server_launches"] == 2, "2-process topology")
        expect(summary["counters"]["normal_calls_attempted"] == 10, "10 Normal calls")
        expect(summary["counters"]["systemone_calls_attempted"] == 10, "10 SystemOne calls")
        expect(summary["counters"]["total_calls_attempted"] == 20, "20 total calls")
        expect(summary["counters"]["scientific_calls_attempted"] == 0, "synthetic calls are not scientific spend")
        expect(all(item["cleanup"]["terminated"] for item in summary["replicates"]), "owned cleanup")
        expect([item for item in summary["replicates"][0]["bundle_order"]] == list(EXPECTED_BUNDLES), "A order")
        expect([item for item in summary["replicates"][1]["bundle_order"]] == list(EXPECTED_BUNDLES), "B order")
        receipt = load_json(fixture["repo"].parent / "evidence" / "transaction-receipt.json")
        validate_receipt_contract(receipt)
        expect(receipt["plan"] == EXPECTED_PLAN, "receipt topology contract")
        log = load_request_log(fixture["record"])
        expect(len(log) == 20, "fake server observed exactly 20 calls")
        expect([row["bundle_id"] for row in log if row["kind"] == "normal"] == list(EXPECTED_BUNDLES) * 2, "frozen Normal order")
        expect([row["bundle_id"] for row in log if row["kind"] == "systemone"] == list(EXPECTED_BUNDLES) * 2, "frozen SystemOne order")
        expect({row["replicate"] for row in log} == {"A", "B"}, "A/B process ownership")
        for row in log:
            if row["replicate"] == "B":
                rendered = json.dumps(row["payload"], sort_keys=True)
                expect("A-only" not in rendered, "A output cannot become B input")
            expect(row["payload"].get("cache_prompt") is False, "cache_prompt=false throughout")

        # Each pre-execution corruption control must stop before server launch.
        controls = []
        altered = make_synthetic_fixture(root / "source-digest")
        altered_path = altered["bundles"] / "B0003.json"
        altered_path.write_bytes(altered_path.read_bytes() + b" ")
        controls.append((altered, "source digest"))
        altered = make_synthetic_fixture(root / "prompt-digest")
        altered["prompt"].write_text("altered synthetic prompt\n", encoding="utf-8")
        controls.append((altered, "prompt digest"))
        altered = make_synthetic_fixture(root / "jev-head")
        protocol = load_json(altered["protocol"])
        protocol["systemone"]["exact_runtime_identity"]["revision"] = "0" * 40
        altered["protocol"].write_bytes(canonical_json_bytes(protocol))
        controls.append((altered, "wrong Jev HEAD"))
        altered = make_synthetic_fixture(root / "jev-tree")
        protocol = load_json(altered["protocol"])
        protocol["systemone"]["exact_runtime_identity"]["tree"] = "0" * 40
        altered["protocol"].write_bytes(canonical_json_bytes(protocol))
        controls.append((altered, "wrong Jev tree"))
        altered = make_synthetic_fixture(root / "model-sha")
        altered["model"].write_bytes(b"altered synthetic model")
        controls.append((altered, "wrong model SHA"))
        for item, label in controls:
            rc, result = run_fixture(item)
            expect(rc == 2, f"{label} must block")
            expect(result["classification"] == "PREEXECUTION_BLOCKED", f"{label} classification")
            expect(result["counters"]["server_launches"] == 0, f"{label} no launch")
            expect(result["counters"]["total_calls_attempted"] == 0, f"{label} no call")

        occupied = make_synthetic_fixture(root / "occupied-port")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((DEFAULT_HOST, occupied["port"]))
        sock.listen(1)
        try:
            rc, result = run_fixture(occupied)
        finally:
            sock.close()
        expect(rc == 2 and result["classification"] == "PREEXECUTION_BLOCKED", "occupied port blocks")

        existing = make_synthetic_fixture(root / "existing-root")
        existing_evidence = existing["repo"].parent / "evidence"
        existing_evidence.mkdir()
        (existing_evidence / "sentinel").write_text("preserve\n", encoding="utf-8")
        rc, result = run_fixture(existing)
        expect(rc == 2 and result["classification"] == "PREEXECUTION_BLOCKED", "existing evidence root blocks")
        expect((existing_evidence / "sentinel").read_text(encoding="utf-8") == "preserve\n", "existing evidence preserved")

        for name, plan, expected_systemone in (
            ("invalid-choice", {"invalid_choice": {"A": ["B0002"]}}, 2),
            ("nonzero-output", {"nonzero_tokens": {"A": ["B0002"]}}, 2),
        ):
            failure = make_synthetic_fixture(root / name)
            rc, result = run_fixture(failure, plan=plan)
            expect(rc == 2, f"{name} must fail closed")
            expect(result["classification"] == "PREEXECUTION_BLOCKED", f"{name} synthetic spend remains zero")
            expect(result["counters"]["normal_calls_attempted"] == 2, f"{name} normal prefix")
            expect(result["counters"]["systemone_calls_attempted"] == expected_systemone, f"{name} SystemOne prefix")
            expect(result["repair_count"] == 0, f"{name} no repair")
            expect(all(item["cleanup"]["terminated"] for item in result["replicates"]), f"{name} cleanup")

        abstention = make_synthetic_fixture(root / "abstention")
        rc, result = run_fixture(
            abstention,
            plan={
                "unresolved": {
                    "A": ["B0002", "B0004"],
                    "B": ["B0002", "B0003"],
                }
            },
        )
        expect(rc == 0, f"abstention transaction must complete: {result}")
        expect(
            result["classification"] == "SYNTHETIC_TRANSACTION_COMPLETED",
            "abstention transaction classification",
        )
        expect(result["counters"]["total_calls_attempted"] == 20, "abstention preserves 20-call topology")
        expect(result["counters"]["extraction_abstain"] == 4, "four synthetic abstentions")
        expect(result["counters"]["claim_ir_valid"] == 6, "six valid ClaimIR rows")
        expect(result["counters"]["extraction_failure"] == 0, "no extraction failure in abstention fixture")
        expect(
            [row["bundle_id"] for row in result["replicates"][0]["rows"]]
            == list(EXPECTED_BUNDLES),
            "A continues after abstention",
        )
        expect(
            [row["bundle_id"] for row in result["replicates"][1]["rows"]]
            == list(EXPECTED_BUNDLES),
            "B continues after abstention",
        )
        expect(all(item["cleanup"]["terminated"] for item in result["replicates"]), "abstention owned cleanup")
        pair_counts = result["comparison"]["aggregate"]["pair_outcome_counts"]
        expect(pair_counts["BOTH_ABSTAIN"] == 1, "BOTH_ABSTAIN pair")
        expect(pair_counts["A_VALID_B_ABSTAIN"] == 1, "A_VALID_B_ABSTAIN pair")
        expect(pair_counts["A_ABSTAIN_B_VALID"] == 1, "A_ABSTAIN_B_VALID pair")
        expect(pair_counts["BOTH_VALID"] == 2, "BOTH_VALID pair count")
        expect(
            result["comparison"]["aggregate"]["claim_ir_comparison_denominator"] == 2,
            "ClaimIR comparison restricted to BOTH_VALID",
        )
        for record in result["replicates"]:
            for row in record["rows"]:
                if row["outcome"] == "EXTRACTION_ABSTAIN":
                    expect("claim_ir" not in row, "abstention must not have ClaimIR")
                    expect("candidate" not in row, "abstention must not have candidate")
                    expect(row["abstention"]["choice"] == UNRESOLVED, "abstention provenance")
        log = load_request_log(abstention["record"])
        expect(len(log) == 20, "abstention fixture observed exactly 20 calls")
        expect(
            [row["bundle_id"] for row in log if row["kind"] == "normal"]
            == list(EXPECTED_BUNDLES) * 2,
            "abstention does not alter Normal order",
        )
        expect(
            {row["replicate"] for row in log} == {"A", "B"},
            "abstention preserves fresh A/B ownership",
        )

        extraction_failure = make_synthetic_fixture(root / "extraction-failure")
        rc, result = run_fixture(
            extraction_failure,
            plan={"collapse_anchors": {"A": ["B0002"]}},
        )
        expect(rc == 0, f"bundle extraction failure must not become transaction failure: {result}")
        expect(result["counters"]["total_calls_attempted"] == 20, "extraction failure preserves 20-call topology")
        expect(result["counters"]["extraction_failure"] == 1, "one extraction failure row")
        expect(result["counters"]["extraction_abstain"] == 0, "candidate failure is not abstention")
        expect(
            result["comparison"]["aggregate"]["pair_outcome_counts"]["PAIR_EXTRACTION_FAILURE"] == 1,
            "pair extraction failure classification",
        )

        normal_failure = make_synthetic_fixture(root / "normal-failure")
        rc, result = run_fixture(normal_failure, plan={"normal_fail": {"A": ["B0003"]}})
        expect(rc == 2 and result["classification"] == "PREEXECUTION_BLOCKED", "Normal failure classification")
        expect(result["counters"]["normal_calls_attempted"] == 3, "Normal failure call count")
        expect(result["counters"]["systemone_calls_attempted"] == 2, "Normal failure skips same-row SystemOne")
        log = load_request_log(normal_failure["record"])
        expect(not any(row["kind"] == "systemone" and row["bundle_id"] == "B0003" for row in log), "Normal failure no SystemOne row")
        expect(all(item["cleanup"]["terminated"] for item in result["replicates"]), "Normal failure cleanup")

        midrun = make_synthetic_fixture(root / "midrun")
        rc, result = run_fixture(midrun, plan={"systemone_fail": {"B": ["B0002"]}})
        expect(rc == 2 and result["classification"] == "PREEXECUTION_BLOCKED", "mid-run failure classification")
        expect(len(result["replicates"]) == 2, "mid-run records A and B")
        expect(all(item["cleanup"]["terminated"] for item in result["replicates"]), "mid-run owned cleanup")

    print("PAPER2_TWO_PASS_LLAMA_CPP_TRANSACTION_V2_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the authorized Paper 2 #193 two-pass abstention-v2 transaction")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--protocol", type=Path, default=Path("research/paper2/extraction_two_pass_real_protocol_v1.json"))
    parser.add_argument("--prompt", type=Path, default=Path("research/paper2/extraction_normal_prompt_v1.md"))
    parser.add_argument("--mask-terms", type=Path, default=Path("research/paper2/extraction_calibration_mask_terms_v1.json"))
    parser.add_argument("--preprocessing-freeze", type=Path, required=False)
    parser.add_argument("--bundles-dir", type=Path, required=False)
    parser.add_argument("--package", type=Path, default=Path("research/paper2/extraction_run_package_v1.json"))
    parser.add_argument("--provenance", type=Path, default=Path("research/paper2/extraction_provenance_v1.json"))
    parser.add_argument("--jev-root", type=Path, required=False)
    parser.add_argument("--server-binary", type=Path, required=False)
    parser.add_argument("--model", type=Path, required=False)
    parser.add_argument("--evidence-root", type=Path, required=False)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--authorization-comment-id", type=int, required=False)
    parser.add_argument("--authorization-status", type=str, required=False)
    parser.add_argument("--authorized-head", type=str, required=False)
    parser.add_argument("--authorized-tree", type=str, required=False)
    parser.add_argument("--authorized-runner-blob", type=str, required=False)
    args = parser.parse_args()

    if args.self_test:
        try:
            self_test()
            return 0
        except (AssertionError, OSError, TransactionError) as exc:
            print(f"PAPER2_TWO_PASS_LLAMA_CPP_TRANSACTION_V2_SELFTEST_FAIL: {exc}")
            return 2

    required = {
        "--preprocessing-freeze": args.preprocessing_freeze,
        "--bundles-dir": args.bundles_dir,
        "--jev-root": args.jev_root,
        "--server-binary": args.server_binary,
        "--model": args.model,
        "--evidence-root": args.evidence_root,
        "--authorization-comment-id": args.authorization_comment_id,
        "--authorization-status": args.authorization_status,
        "--authorized-head": args.authorized_head,
        "--authorized-tree": args.authorized_tree,
        "--authorized-runner-blob": args.authorized_runner_blob,
    }
    missing = [name for name, value in required.items() if value is None]
    if missing:
        parser.error("real execution requires: " + ", ".join(missing))

    rc, summary = run_transaction(
        repo_root=args.repo_root.resolve(),
        protocol_path=args.protocol.resolve(),
        prompt_path=args.prompt.resolve(),
        mask_terms_path=args.mask_terms.resolve(),
        preprocessing_freeze_path=args.preprocessing_freeze.resolve(),
        bundle_dir=args.bundles_dir.resolve(),
        package_path=args.package.resolve(),
        provenance_path=args.provenance.resolve(),
        llama_root=args.jev_root.resolve(),
        server_binary=args.server_binary.resolve(),
        model_path=args.model.resolve(),
        evidence_root=args.evidence_root.resolve(),
        port=args.port,
        require_gpu=True,
        comment_id=args.authorization_comment_id,
        authorization_status=args.authorization_status,
        authorized_head=args.authorized_head,
        authorized_tree=args.authorized_tree,
        authorized_runner_blob=args.authorized_runner_blob,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
