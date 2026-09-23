#!/usr/bin/env python3
"""Own one llama.cpp lifetime for the Paper 2 #147 extraction pilot.

This transaction wrapper is adapted from RelaySelf's
experiments/mineflayer_cognition_llama_cpp_transaction.py.

It owns the llama-server process, attests the exact runtime before scientific
spend, runs the frozen ten-call A/B extraction exactly once, validates the
execution receipt, generates the basis-blind agreement report, and terminates
the owned server.

No basis decomposition is performed.
"""

from __future__ import annotations

import argparse
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
from pathlib import Path
from typing import Any

import paper2_extraction_openai_runner as extraction_runner
from paper2_extraction_assemble_compare import assemble_and_compare


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 1234
DEFAULT_CONTEXT = 8192
DEFAULT_SLOTS = 1
READY_TIMEOUT_SECONDS = 120.0
READY_POLL_SECONDS = 0.5
EXPECTED_GGUF_SHA256 = "c088a44859de42a1966851b552ba628c0ff4419b87c4622539d69430f40024ed"
EXPECTED_TARGET_QUANTIZATION = "Q4_K_M"
_FTYPE_EQUIVALENCE = {"Q4_K - Medium": "Q4_K_M"}


class PhysicalTransactionError(RuntimeError):
    pass


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _run_text(command: list[str], *, cwd: Path | None = None) -> str:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise PhysicalTransactionError(
            f"command could not start: {shlex.join(command)}: {type(exc).__name__}: {exc}"
        ) from exc
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise PhysicalTransactionError(
            f"command failed ({completed.returncode}): {shlex.join(command)}: {detail}"
        )
    return completed.stdout or completed.stderr


def _require_clean_repo(repo_root: Path) -> tuple[str, str]:
    if not (repo_root / ".git").exists():
        raise PhysicalTransactionError(f"repo-root is not a git checkout: {repo_root}")
    status = _run_text(["git", "status", "--porcelain"], cwd=repo_root)
    if status.strip():
        raise PhysicalTransactionError(
            "physical transaction requires a clean isolated RelayTheory checkout"
        )
    head = _run_text(["git", "rev-parse", "HEAD"], cwd=repo_root).strip()
    tree = _run_text(["git", "rev-parse", "HEAD^{tree}"], cwd=repo_root).strip()
    return head, tree


def _port_is_free(host: str, port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((host, port))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def _require_llama_cpp_paths(llama_cpp_root: Path, server_binary: Path) -> None:
    if not (llama_cpp_root / ".git").exists():
        raise PhysicalTransactionError(
            f"llama.cpp root is not a git checkout: {llama_cpp_root}"
        )
    if not server_binary.is_file() or not os.access(server_binary, os.X_OK):
        raise PhysicalTransactionError(
            f"llama-server is not executable: {server_binary}"
        )


def _collect_llama_revision(llama_cpp_root: Path) -> str:
    revision = _run_text(["git", "rev-parse", "HEAD"], cwd=llama_cpp_root).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise PhysicalTransactionError(
            "llama.cpp revision is not a lowercase 40-hex commit"
        )
    return revision


def _collect_server_version(server_binary: Path) -> dict[str, object]:
    version = _run_text([str(server_binary), "--version"]).strip()
    match = re.search(r"\bbuild\s+(\d+)\b", version)
    if match is None:
        raise PhysicalTransactionError(
            "could not parse llama-server build number from --version"
        )
    return {"version": version, "buildNumber": int(match.group(1))}


def _verify_artifact(artifact_path: Path, expected_sha256: str) -> str:
    if not artifact_path.is_file():
        raise PhysicalTransactionError(
            f"pinned GGUF is not a file: {artifact_path}"
        )
    actual = _sha256_file(artifact_path)
    if actual != expected_sha256:
        raise PhysicalTransactionError(
            f"GGUF sha256 mismatch: expected={expected_sha256} actual={actual}"
        )
    return actual


def _collect_gpu_identity(*, required: bool) -> str:
    try:
        return _run_text(
            [
                "nvidia-smi",
                "--query-gpu=name,driver_version,memory.total",
                "--format=csv,noheader",
            ]
        ).strip()
    except PhysicalTransactionError:
        if required:
            raise
        return "NOT_REQUIRED_IN_SELFTEST"


def _server_command(
    *,
    server_binary: Path,
    artifact_path: Path,
    port: int,
    log_path: Path,
) -> list[str]:
    return [
        str(server_binary),
        "-m",
        str(artifact_path),
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


def _start_server(command: list[str]) -> subprocess.Popen[str]:
    try:
        return subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except OSError as exc:
        raise PhysicalTransactionError(
            f"failed to launch transaction-owned llama-server: {exc}"
        ) from exc


def _get_json(url: str, *, timeout: float) -> Any:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json"},
        method="GET",
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
        raise PhysicalTransactionError(f"GET {url} failed: {exc}") from exc


def _wait_until_ready(process: subprocess.Popen[str], origin: str) -> None:
    deadline = time.monotonic() + READY_TIMEOUT_SECONDS
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise PhysicalTransactionError(
                "transaction-owned llama-server exited before readiness: "
                f"{process.returncode}"
            )
        try:
            health = _get_json(f"{origin}/health", timeout=5.0)
            if isinstance(health, dict) and health.get("status") == "ok":
                return
        except PhysicalTransactionError as exc:
            last_error = exc
        time.sleep(READY_POLL_SECONDS)
    suffix = f": {last_error}" if last_error else ""
    raise PhysicalTransactionError(
        f"transaction-owned llama-server did not become ready{suffix}"
    )


def _model_ids(payload: object) -> list[str]:
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise PhysicalTransactionError(
            "llama-server /v1/models response is invalid"
        )
    result: list[str] = []
    for item in payload["data"]:
        if isinstance(item, dict) and isinstance(item.get("id"), str) and item["id"]:
            result.append(item["id"])
    return result


def _ftype_matches(value: object) -> bool:
    if value == EXPECTED_TARGET_QUANTIZATION:
        return True
    return (
        isinstance(value, str)
        and _FTYPE_EQUIVALENCE.get(value) == EXPECTED_TARGET_QUANTIZATION
    )


def _attest_runtime(
    *,
    health: object,
    models: object,
    props: object,
    slots: object,
    artifact_path: Path,
    artifact_sha256: str,
    llama_identity: dict[str, object],
) -> dict[str, object]:
    if not isinstance(health, dict) or health.get("status") != "ok":
        raise PhysicalTransactionError("llama-server /health is not ready")

    model_ids = _model_ids(models)
    if len(model_ids) != 1:
        raise PhysicalTransactionError(
            "single-model transaction requires exactly one /v1/models id"
        )

    if not isinstance(props, dict):
        raise PhysicalTransactionError("/props must return an object")
    if not isinstance(slots, list) or len(slots) != DEFAULT_SLOTS:
        raise PhysicalTransactionError(
            "transaction requires exactly one /slots entry"
        )

    build_number = llama_identity["buildNumber"]
    revision = llama_identity["revision"]
    build_info = props.get("build_info")
    if not isinstance(build_info, str):
        raise PhysicalTransactionError("props.build_info must be a string")
    if str(build_number) not in build_info:
        raise PhysicalTransactionError(
            "llama-server --version build does not match /props build_info"
        )
    if not isinstance(revision, str) or (
        revision not in build_info and revision[:7] not in build_info
    ):
        raise PhysicalTransactionError(
            "llama.cpp git revision does not match /props build_info"
        )

    model_alias = props.get("model_alias")
    if model_alias != model_ids[0]:
        raise PhysicalTransactionError(
            "/props model_alias does not match /v1/models id"
        )

    model_path = props.get("model_path")
    if (
        not isinstance(model_path, str)
        or Path(model_path).resolve() != artifact_path
    ):
        raise PhysicalTransactionError(
            "/props model_path does not match pinned GGUF"
        )

    settings = props.get("default_generation_settings")
    if not isinstance(settings, dict) or settings.get("n_ctx") != DEFAULT_CONTEXT:
        raise PhysicalTransactionError(
            "/props context does not equal 8192"
        )
    if props.get("total_slots") != DEFAULT_SLOTS:
        raise PhysicalTransactionError(
            "/props total_slots does not equal 1"
        )

    slot = slots[0]
    if (
        not isinstance(slot, dict)
        or slot.get("id") != 0
        or slot.get("n_ctx") != DEFAULT_CONTEXT
    ):
        raise PhysicalTransactionError(
            "single /slots entry must be id=0 with n_ctx=8192"
        )

    if not _ftype_matches(props.get("model_ftype")):
        raise PhysicalTransactionError(
            "props.model_ftype does not match target quantization Q4_K_M"
        )

    chat_template = props.get("chat_template")
    if not isinstance(chat_template, str) or not chat_template:
        raise PhysicalTransactionError(
            "props.chat_template must be a non-empty string"
        )

    return {
        "requestModel": model_ids[0],
        "buildInfo": build_info,
        "modelAlias": model_alias,
        "modelPath": str(artifact_path),
        "modelFtype": props.get("model_ftype"),
        "targetQuantization": EXPECTED_TARGET_QUANTIZATION,
        "artifactSha256": artifact_sha256,
        "chatTemplateSha256": hashlib.sha256(
            chat_template.encode("utf-8")
        ).hexdigest(),
        "context": DEFAULT_CONTEXT,
        "slots": DEFAULT_SLOTS,
        "contextShiftEnabled": False,
        "requestReasoningEffort": "none",
        "cachePrompt": False,
    }


def _probe_and_attest(
    *,
    origin: str,
    artifact_path: Path,
    artifact_sha256: str,
    llama_identity: dict[str, object],
) -> dict[str, object]:
    health = _get_json(f"{origin}/health", timeout=20.0)
    models = _get_json(f"{origin}/v1/models", timeout=20.0)
    props = _get_json(f"{origin}/props", timeout=20.0)
    slots = _get_json(f"{origin}/slots", timeout=20.0)
    return {
        "health": health,
        "models": models,
        "props": props,
        "slots": slots,
        "attested": _attest_runtime(
            health=health,
            models=models,
            props=props,
            slots=slots,
            artifact_path=artifact_path,
            artifact_sha256=artifact_sha256,
            llama_identity=llama_identity,
        ),
        "nonGenerativeRequestCount": 4,
    }


def _terminate_owned_process(process: subprocess.Popen[str]) -> int | None:
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=15.0)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5.0)
    return process.returncode


def _runner_config(
    *,
    origin: str,
    model: str,
    revision: str,
    build_number: int,
    artifact_sha256: str,
) -> dict[str, Any]:
    return {
        "schema_version": extraction_runner.CONFIG_VERSION,
        "extractor_identity": "transaction-owned-llama.cpp-gemma4-12b",
        "extractor_revision": (
            f"llama.cpp={revision};build={build_number};"
            f"gguf_sha256={artifact_sha256}"
        ),
        "base_url": f"{origin}/v1",
        "model": model,
        "temperature": 0.2,
        "top_p": 1.0,
        "max_tokens": 2048,
        "timeout_seconds": 180,
        "response_format": "json_object",
        "api_key_env": None,
    }


def run_transaction(
    *,
    repo_root: Path,
    llama_cpp_root: Path,
    artifact_path: Path,
    source_texts_path: Path,
    package_path: Path,
    prompt_path: Path,
    provenance_path: Path,
    evidence_root: Path,
    port: int,
    expected_artifact_sha256: str,
    enforce_default_port: bool,
    require_gpu: bool,
) -> tuple[int, dict[str, object]]:
    summary: dict[str, object] = {
        "formatVersion": 1,
        "ownerIssue": 147,
        "disposition": None,
        "serverLaunchCount": 0,
        "runnerInvocationCount": 0,
        "modelCallCount": 0,
        "retryCount": 0,
        "replayCount": 0,
        "fallbackCount": 0,
        "basisDecompositionExecuted": False,
        "evidenceRoot": str(evidence_root),
    }
    telemetry = {"model_call_count": 0}
    process: subprocess.Popen[str] | None = None
    exit_code = 2

    log_path = evidence_root / "llama-server.log"
    config_path = evidence_root / "runner-config.json"
    run_output = evidence_root / "run"
    agreement_output = evidence_root / "agreement"
    summary_path = evidence_root / "transaction-summary.json"

    try:
        head, tree = _require_clean_repo(repo_root)
        summary["relayTheory"] = {"head": head, "tree": tree}

        if enforce_default_port and port != DEFAULT_PORT:
            raise PhysicalTransactionError(
                "current physical condition requires port 1234"
            )
        if not _port_is_free(DEFAULT_HOST, port):
            raise PhysicalTransactionError(
                f"{DEFAULT_HOST}:{port} is already occupied"
            )

        server_binary = llama_cpp_root / "build" / "bin" / "llama-server"
        _require_llama_cpp_paths(llama_cpp_root, server_binary)
        revision = _collect_llama_revision(llama_cpp_root)
        version = _collect_server_version(server_binary)
        artifact_sha256 = _verify_artifact(
            artifact_path,
            expected_artifact_sha256,
        )
        gpu_identity = _collect_gpu_identity(required=require_gpu)

        llama_identity = {
            "revision": revision,
            **version,
            "gpu": gpu_identity,
        }
        summary["llamaCpp"] = llama_identity
        summary["artifact"] = {
            "path": str(artifact_path),
            "sha256": artifact_sha256,
        }

        command = _server_command(
            server_binary=server_binary,
            artifact_path=artifact_path,
            port=port,
            log_path=log_path,
        )
        summary["serverCommand"] = command
        process = _start_server(command)
        summary["serverLaunchCount"] = 1

        origin = f"http://{DEFAULT_HOST}:{port}"
        _wait_until_ready(process, origin)
        runtime = _probe_and_attest(
            origin=origin,
            artifact_path=artifact_path,
            artifact_sha256=artifact_sha256,
            llama_identity=llama_identity,
        )
        summary["runtime"] = runtime

        attested = runtime["attested"]
        assert isinstance(attested, dict)
        model = attested["requestModel"]
        assert isinstance(model, str)

        config = _runner_config(
            origin=origin,
            model=model,
            revision=revision,
            build_number=int(version["buildNumber"]),
            artifact_sha256=artifact_sha256,
        )
        extraction_runner.validate_config(config)
        _write_json(config_path, config)
        summary["config"] = {
            **config,
            "sha256": extraction_runner.configuration_sha256(config),
        }

        summary["runnerInvocationCount"] = 1
        receipt_path = extraction_runner.execute(
            package_path=package_path,
            prompt_path=prompt_path,
            source_texts_path=source_texts_path,
            config_path=config_path,
            output_dir=run_output,
            telemetry=telemetry,
        )
        summary["modelCallCount"] = telemetry["model_call_count"]
        if telemetry["model_call_count"] != 10:
            raise PhysicalTransactionError(
                "successful runner must consume exactly ten model calls"
            )

        receipt_sha256 = _sha256_file(receipt_path)
        summary["receipt"] = {
            "path": str(receipt_path),
            "sha256": receipt_sha256,
            "validation": "PASS",
        }

        report = assemble_and_compare(
            receipt_path,
            package_path,
            provenance_path,
            agreement_output,
        )
        report_path = agreement_output / "agreement-report.json"
        summary["agreement"] = {
            "path": str(report_path),
            "sha256": _sha256_file(report_path),
            "aggregate": report["aggregate"],
        }

        summary["disposition"] = "COMPLETED"
        exit_code = 0

    except Exception as exc:
        summary["modelCallCount"] = telemetry["model_call_count"]
        summary["error"] = {
            "type": type(exc).__name__,
            "message": str(exc),
        }
        summary["disposition"] = (
            "PREEXECUTION_BLOCKED"
            if telemetry["model_call_count"] == 0
            else "SCIENTIFIC_TRANSACTION_CONSUMED_INCOMPLETE"
        )
        exit_code = 2

    finally:
        cleanup: dict[str, object] = {
            "ownedProcess": process is not None,
            "terminated": False,
            "exitCode": None,
        }
        if process is not None:
            cleanup["exitCode"] = _terminate_owned_process(process)
            cleanup["terminated"] = process.poll() is not None
        summary["cleanup"] = cleanup
        _write_json(summary_path, summary)

    return exit_code, summary


def _git_init_clean_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    _run_text(["git", "init", "-q"], cwd=path)
    _run_text(["git", "config", "user.email", "selftest@example.invalid"], cwd=path)
    _run_text(["git", "config", "user.name", "selftest"], cwd=path)
    (path / "README").write_text("selftest\n", encoding="utf-8")
    _run_text(["git", "add", "README"], cwd=path)
    _run_text(["git", "commit", "-qm", "selftest"], cwd=path)


def _write_fake_llama_server(path: Path) -> None:
    fake = r'''#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

if "--version" in sys.argv:
    print("llama.cpp fake build 9999")
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
args, _ = parser.parse_known_args()

root = Path(__file__).resolve().parents[2]
revision = subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=root, text=True
).strip()

if args.log_file:
    Path(args.log_file).write_text("fake llama-server started\n", encoding="utf-8")

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *items):
        return

    def _json(self, value, status=200):
        raw = json.dumps(value).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == "/health":
            self._json({"status": "ok"})
        elif self.path == "/v1/models":
            self._json({"data": [{"id": "fake-model"}]})
        elif self.path == "/props":
            self._json({
                "build_info": f"fake build 9999 {revision}",
                "model_alias": "fake-model",
                "model_path": str(Path(args.m).resolve()),
                "default_generation_settings": {"n_ctx": args.c},
                "total_slots": args.np,
                "model_ftype": "Q4_K - Medium",
                "chat_template": "fake-template",
            })
        elif self.path == "/slots":
            self._json([{"id": 0, "n_ctx": args.c}])
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path != "/v1/chat/completions":
            self._json({"error": "not found"}, 404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length).decode("utf-8"))
        if body.get("reasoning_effort") != "none":
            self._json({"error": "reasoning_effort must be none"}, 400)
            return
        if body.get("cache_prompt") is not False:
            self._json({"error": "cache_prompt must be false"}, 400)
            return
        messages = body.get("messages")
        if not isinstance(messages, list) or len(messages) != 2:
            self._json({"error": "messages"}, 400)
            return
        bundle = json.loads(messages[1]["content"])
        bid = bundle["bundle_id"]
        candidate = {
            "schema_version": "paper2-extraction-candidate-v1",
            "bundle_id": bid,
            "claim_core": {
                "claim_type": "relation",
                "modality": "descriptive",
                "scope": {
                    "conditions": [],
                    "population": [],
                    "substrate": [],
                    "task": [],
                    "temporal_scope": [],
                },
                "nodes": [{
                    "id": "observed_state",
                    "role": "state_or_structure",
                    "description": "a source-grounded observed state",
                    "source_span_ids": ["s1"],
                    "grounding": "explicit",
                }],
                "relations": [],
            },
        }
        self._json({
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": json.dumps(candidate),
                },
                "finish_reason": "stop",
            }]
        })

ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()
'''
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(fake, encoding="utf-8")
    path.chmod(0o755)


def _find_free_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((DEFAULT_HOST, 0))
        return int(sock.getsockname()[1])
    finally:
        sock.close()


def self_test(
    *,
    package_path: Path,
    prompt_path: Path,
    provenance_path: Path,
) -> None:
    import copy

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        repo_root = root / "relay-theory"
        _git_init_clean_repo(repo_root)

        llama_root = root / "llama.cpp"
        _git_init_clean_repo(llama_root)
        server_binary = llama_root / "build" / "bin" / "llama-server"
        _write_fake_llama_server(server_binary)

        artifact = root / "fake-model.gguf"
        artifact.write_bytes(b"fake gguf for transaction selftest")
        artifact_sha = _sha256_file(artifact)

        real_package = extraction_runner.load_json(package_path)
        synthetic_package, texts = extraction_runner.synthetic_package(real_package)
        synthetic_package_path = root / "package.json"
        source_texts_path = root / "source-texts.json"
        synthetic_package_path.write_bytes(
            extraction_runner.canonical_json_bytes(synthetic_package)
        )
        source_texts_path.write_bytes(
            extraction_runner.canonical_json_bytes(texts)
        )

        evidence_root = root / "evidence"
        evidence_root.mkdir()

        port = _find_free_port()
        rc, summary = run_transaction(
            repo_root=repo_root,
            llama_cpp_root=llama_root,
            artifact_path=artifact,
            source_texts_path=source_texts_path,
            package_path=synthetic_package_path,
            prompt_path=prompt_path,
            provenance_path=provenance_path,
            evidence_root=evidence_root,
            port=port,
            expected_artifact_sha256=artifact_sha,
            enforce_default_port=False,
            require_gpu=False,
        )

        if rc != 0 or summary.get("disposition") != "COMPLETED":
            raise AssertionError(
                f"owned transaction selftest failed: {summary}"
            )
        if summary.get("serverLaunchCount") != 1:
            raise AssertionError("owned transaction must launch server exactly once")
        if summary.get("runnerInvocationCount") != 1:
            raise AssertionError("owned transaction must invoke runner exactly once")
        if summary.get("modelCallCount") != 10:
            raise AssertionError("owned transaction must consume exactly ten calls")
        cleanup = summary.get("cleanup")
        if not isinstance(cleanup, dict) or cleanup.get("terminated") is not True:
            raise AssertionError("owned server must be terminated")
        agreement = summary.get("agreement")
        if not isinstance(agreement, dict):
            raise AssertionError("agreement summary missing")
        aggregate = agreement.get("aggregate")
        if not isinstance(aggregate, dict):
            raise AssertionError("agreement aggregate missing")
        if aggregate.get("overall_exact_structural_equivalence") != 5:
            raise AssertionError("synthetic A/B agreement must be 5/5")

    print("PAPER2_LLAMA_CPP_OWNED_TRANSACTION_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Own llama.cpp server lifetime and execute Paper 2 #147 A/B "
            "extraction exactly once."
        )
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--llama-cpp-root",
        default=str(Path.home() / "src" / "llama.cpp"),
    )
    parser.add_argument(
        "--artifact-path",
        default=str(
            Path.home()
            / "models"
            / "gguf"
            / "gemma-4-12B-it-Q4_K_M.gguf"
        ),
    )
    parser.add_argument(
        "--package",
        type=Path,
        default=Path("research/paper2/extraction_run_package_v1.json"),
    )
    parser.add_argument(
        "--prompt",
        type=Path,
        default=Path("research/paper2/extraction_prompt_v1.md"),
    )
    parser.add_argument(
        "--provenance",
        type=Path,
        default=Path("research/paper2/extraction_provenance_v1.json"),
    )
    parser.add_argument("--source-texts", type=Path)
    parser.add_argument("--evidence-root", type=Path)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test(
            package_path=args.package,
            prompt_path=args.prompt,
            provenance_path=args.provenance,
        )
        return 0

    if args.source_texts is None:
        print("PREEXECUTION_BLOCKED: --source-texts is required")
        return 2

    repo_root = Path(args.repo_root).resolve()
    llama_cpp_root = Path(args.llama_cpp_root).expanduser().resolve()
    artifact_path = Path(args.artifact_path).expanduser().resolve()
    source_texts_path = args.source_texts.expanduser().resolve()

    if args.evidence_root is None:
        evidence_root = Path(
            tempfile.mkdtemp(prefix="relaytheory-147-gemma4-")
        ).resolve()
    else:
        evidence_root = args.evidence_root.expanduser().resolve()
        evidence_root.mkdir(parents=True, exist_ok=False)

    rc, summary = run_transaction(
        repo_root=repo_root,
        llama_cpp_root=llama_cpp_root,
        artifact_path=artifact_path,
        source_texts_path=source_texts_path,
        package_path=args.package.resolve(),
        prompt_path=args.prompt.resolve(),
        provenance_path=args.provenance.resolve(),
        evidence_root=evidence_root,
        port=args.port,
        expected_artifact_sha256=EXPECTED_GGUF_SHA256,
        enforce_default_port=True,
        require_gpu=True,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
