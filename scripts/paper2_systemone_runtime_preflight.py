#!/usr/bin/env python3
"""Synthetic physical qualification for the Paper 2 SystemOne runtime.

Owner: #162.

This tool owns two separate llama-server process lifetimes, one for synthetic
replicate A and one for synthetic replicate B. Each process receives:
- one synthetic Normal chat-completions probe;
- one 54-question SystemOne probe using the hardened v2 question surface.

No real literature text is used. Failure never consumes a scientific pilot.
The purpose is only to bind the exact local llama.cpp source/build/model/runtime
class before a separate real extraction transaction is authorized.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import subprocess
import tempfile
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import paper2_extraction_llama_cpp_transaction as physical
from paper2_extraction_two_pass_systemone_v2 import (
    UNRESOLVED,
    build_systemone_request,
    parse_systemone_response,
    synthetic_source,
)


MANIFEST_VERSION = "paper2-systemone-runtime-preflight-v1"
EXPECTED_REAL_GGUF_SHA256 = physical.EXPECTED_GGUF_SHA256
NORMAL_PROBES_PER_REPLICATE = 1
SYSTEMONE_PROBES_PER_REPLICATE = 1
EXPECTED_PROBES = 4
EXPECTED_SYSTEMONE_QUESTIONS = 54
EXPECTED_JEV_REMOTE = "https://github.com/kishida/llama.cpp"
EXPECTED_JEV_REVISION = "07183d010f5cf5d021a2550775f42fb4b4270e06"
EXPECTED_JEV_TREE = "4a654218342c2e179c0cd143e359632bff02bc22"
EXPECTED_SYSTEMONE_ROUTE = "/v1/systemone"
EXPECTED_ROUTE_SOURCE_PATHS = (
    "tools/server/server-jev.h",
    "tools/server/server-jev.cpp",
)


class RuntimePreflightError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise RuntimePreflightError(message)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_manifest(manifest: Any) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        fail("manifest must be object")
    if manifest.get("schema_version") != MANIFEST_VERSION:
        fail("manifest schema_version")
    if manifest.get("owner_issue") != 162:
        fail("manifest owner_issue")
    if manifest.get("real_paper_text_forbidden") is not True:
        fail("real paper text must remain forbidden")
    if manifest.get("process_policy") != (
        "separate_owned_llama_cpp_process_lifetime_per_replicate"
    ):
        fail("process isolation policy drift")
    if manifest.get("expected_server_launch_count") != 2:
        fail("server launch count drift")
    if manifest.get("expected_total_model_facing_probe_count") != EXPECTED_PROBES:
        fail("probe count drift")
    systemone = manifest.get("systemone_probe")
    if not isinstance(systemone, dict):
        fail("systemone_probe missing")
    if systemone.get("expected_question_count") != EXPECTED_SYSTEMONE_QUESTIONS:
        fail("SystemOne question count drift")
    target = manifest.get("target_source")
    if not isinstance(target, dict):
        fail("target_source missing")
    if target.get("repository_url") != EXPECTED_JEV_REMOTE:
        fail("target_source repository drift")
    if target.get("branch_observed_at_freeze") != "jev":
        fail("target_source branch drift")
    if target.get("revision") != EXPECTED_JEV_REVISION:
        fail("target_source revision drift")
    if target.get("tree") != EXPECTED_JEV_TREE:
        fail("target_source tree drift")
    if target.get("systemone_route") != EXPECTED_SYSTEMONE_ROUTE:
        fail("target_source SystemOne route drift")
    if tuple(target.get("route_source_paths", [])) != EXPECTED_ROUTE_SOURCE_PATHS:
        fail("target_source route source paths drift")

    cache = manifest.get("cache_boundary")
    if not isinstance(cache, dict):
        fail("cache_boundary missing")
    if cache.get("cache_prompt") is not False:
        fail("cache_prompt must remain false")
    if cache.get("cross_request_cache_reuse_required") is not False:
        fail("cross-request cache reuse must remain unnecessary")
    if cache.get("relaylm_3006_cache_correctness_dependency") is not False:
        fail("#162 runtime preflight must remain independent of RelayLM #3006")
    if cache.get("cache_correctness_claimed_by_this_preflight") is not False:
        fail("runtime preflight may not claim cache correctness")

    if manifest.get("real_pilot_authorized_by_this_artifact") is not False:
        fail("runtime qualification may not authorize real pilot by itself")
    return manifest


def _canonical_remote(value: str | None) -> str | None:
    if value is None:
        return None
    result = value.strip()
    if result.startswith("git@github.com:"):
        result = "https://github.com/" + result[len("git@github.com:"):]
    if result.endswith(".git"):
        result = result[:-4]
    return result.rstrip("/")


def _git_remote(root: Path) -> str | None:
    completed = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    value = completed.stdout.strip()
    return value or None


def _inspect_source_identity(root: Path) -> dict[str, Any]:
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if status.returncode != 0:
        fail("could not inspect Jev source git status")
    if status.stdout.strip():
        fail("Jev source checkout must be clean")

    revision = physical._collect_llama_revision(root)
    tree_result = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if tree_result.returncode != 0:
        fail("could not inspect Jev source tree")
    tree = tree_result.stdout.strip()

    route_hits: list[str] = []
    for relative in EXPECTED_ROUTE_SOURCE_PATHS:
        path = root / relative
        if path.is_file() and EXPECTED_SYSTEMONE_ROUTE in path.read_text(
            encoding="utf-8", errors="replace"
        ):
            route_hits.append(relative)

    return {
        "remote": _canonical_remote(_git_remote(root)),
        "revision": revision,
        "tree": tree,
        "systemoneRoute": EXPECTED_SYSTEMONE_ROUTE,
        "routeSourceHits": route_hits,
    }


def _validate_source_identity(
    identity: dict[str, Any],
    *,
    enforce_exact_pin: bool,
) -> None:
    if identity.get("remote") != EXPECTED_JEV_REMOTE:
        fail(
            "Jev source remote mismatch: "
            f"expected={EXPECTED_JEV_REMOTE} actual={identity.get('remote')}"
        )
    hits = identity.get("routeSourceHits")
    if not isinstance(hits, list) or not hits:
        fail("Jev source does not contain /v1/systemone route marker")
    if enforce_exact_pin:
        if identity.get("revision") != EXPECTED_JEV_REVISION:
            fail(
                "Jev source revision mismatch: "
                f"expected={EXPECTED_JEV_REVISION} actual={identity.get('revision')}"
            )
        if identity.get("tree") != EXPECTED_JEV_TREE:
            fail(
                "Jev source tree mismatch: "
                f"expected={EXPECTED_JEV_TREE} actual={identity.get('tree')}"
            )


def _post_json(url: str, payload: dict[str, Any], timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=physical.json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            value = json.loads(response.read().decode("utf-8"))
    except (
        urllib.error.URLError,
        TimeoutError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise RuntimePreflightError(f"POST {url} failed: {exc}") from exc
    if not isinstance(value, dict):
        fail(f"POST {url}: response must be object")
    return value


def _normal_probe(origin: str, model: str, timeout: float) -> dict[str, Any]:
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "This is a synthetic runtime probe. Reply with a short plain-text "
                    "statement that the synthetic source reports a relation."
                ),
            },
            {
                "role": "user",
                "content": "Synthetic source: variable A depends on variable B.",
            },
        ],
        "temperature": 0.2,
        "top_p": 1.0,
        "max_tokens": 64,
        "reasoning_effort": "none",
        "cache_prompt": False,
    }
    response = _post_json(f"{origin}/v1/chat/completions", payload, timeout)
    choices = response.get("choices")
    if not isinstance(choices, list) or len(choices) != 1:
        fail("Normal probe requires exactly one choice")
    item = choices[0]
    if not isinstance(item, dict):
        fail("Normal probe choice must be object")
    message = item.get("message")
    if not isinstance(message, dict):
        fail("Normal probe message missing")
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        fail("Normal probe produced empty content")
    return {
        "request": payload,
        "response_model": response.get("model"),
        "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "finish_reason": item.get("finish_reason"),
    }


def _systemone_probe(origin: str, model: str, timeout: float) -> dict[str, Any]:
    source = synthetic_source(
        [
            "Synthetic variable A.",
            "Synthetic variable B.",
            "Synthetic variable A depends on synthetic variable B.",
        ],
        bundle_id="B9901",
    )
    request_payload = build_systemone_request(
        source,
        "The synthetic source states that A depends on B.",
        model,
    )
    if len(request_payload["questions"]) != EXPECTED_SYSTEMONE_QUESTIONS:
        fail("unexpected maximum SystemOne question count")
    response = _post_json(f"{origin}/v1/systemone", request_payload, timeout)
    answers = parse_systemone_response(request_payload, response)
    if set(answers) != set(request_payload["questions"]):
        fail("SystemOne probe answer set mismatch")
    unresolved_count = sum(value == UNRESOLVED for value in answers.values())
    return {
        "request_sha256": hashlib.sha256(
            physical.json.dumps(
                request_payload,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest(),
        "question_count": len(request_payload["questions"]),
        "answer_count": len(answers),
        "unresolved_count": unresolved_count,
        "response_model": response.get("model"),
    }


def _server_command(
    *,
    server_binary: Path,
    artifact_path: Path,
    port: int,
    log_path: Path,
) -> list[str]:
    return physical._server_command(
        server_binary=server_binary,
        artifact_path=artifact_path,
        port=port,
        log_path=log_path,
    )


def _port_is_reusably_free(host: str, port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def _qualify_one(
    *,
    replicate: str,
    llama_cpp_root: Path,
    artifact_path: Path,
    artifact_sha256: str,
    port: int,
    evidence_root: Path,
    timeout: float,
    require_gpu: bool,
) -> dict[str, Any]:
    if replicate not in {"A", "B"}:
        fail("replicate must be A or B")
    if not _port_is_reusably_free(physical.DEFAULT_HOST, port):
        fail(f"{physical.DEFAULT_HOST}:{port} is occupied by a live listener")

    server_binary = llama_cpp_root / "build" / "bin" / "llama-server"
    physical._require_llama_cpp_paths(llama_cpp_root, server_binary)
    source_identity = _inspect_source_identity(llama_cpp_root)
    _validate_source_identity(
        source_identity,
        enforce_exact_pin=require_gpu,
    )
    revision = source_identity["revision"]
    assert isinstance(revision, str)
    version = physical._collect_server_version(server_binary)
    actual_sha = physical._verify_artifact(artifact_path, artifact_sha256)
    gpu = physical._collect_gpu_identity(required=require_gpu)
    remote = _git_remote(llama_cpp_root)

    log_path = evidence_root / replicate / "llama-server.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    command = _server_command(
        server_binary=server_binary,
        artifact_path=artifact_path,
        port=port,
        log_path=log_path,
    )
    process = physical._start_server(command)
    cleanup: dict[str, Any] = {
        "ownedProcess": True,
        "terminated": False,
        "exitCode": None,
    }
    try:
        origin = f"http://{physical.DEFAULT_HOST}:{port}"
        physical._wait_until_ready(process, origin)
        llama_identity = {
            "revision": revision,
            **version,
            "gpu": gpu,
        }
        runtime = physical._probe_and_attest(
            origin=origin,
            artifact_path=artifact_path,
            artifact_sha256=actual_sha,
            llama_identity=llama_identity,
        )
        attested = runtime["attested"]
        if not isinstance(attested, dict):
            fail("runtime attestation missing")
        model = attested.get("requestModel")
        if not isinstance(model, str) or not model:
            fail("attested model missing")

        normal = _normal_probe(origin, model, timeout)
        systemone = _systemone_probe(origin, model, timeout)
        return {
            "replicate": replicate,
            "llamaCpp": {
                "root": str(llama_cpp_root),
                "remote": remote,
                "revision": revision,
                "tree": source_identity["tree"],
                "systemoneRouteSourceHits": source_identity["routeSourceHits"],
                **version,
            },
            "artifact": {
                "path": str(artifact_path),
                "sha256": actual_sha,
            },
            "gpu": gpu,
            "serverCommand": command,
            "runtime": runtime,
            "normalProbe": normal,
            "systemOneProbe": systemone,
            "probeCount": 2,
        }
    finally:
        cleanup["exitCode"] = physical._terminate_owned_process(process)
        cleanup["terminated"] = process.poll() is not None
        if log_path.is_file():
            cleanup["logSha256"] = sha256_file(log_path)
        write_json(evidence_root / replicate / "cleanup.json", cleanup)


def run_preflight(
    *,
    repo_root: Path,
    llama_cpp_root: Path,
    artifact_path: Path,
    artifact_sha256: str,
    evidence_root: Path,
    port: int,
    timeout: float,
    require_gpu: bool,
) -> tuple[int, dict[str, Any]]:
    summary: dict[str, Any] = {
        "schema_version": MANIFEST_VERSION,
        "owner_issue": 162,
        "disposition": None,
        "scientific_model_calls": 0,
        "real_paper_text_used": False,
        "server_launch_count": 0,
        "synthetic_model_facing_probe_count": 0,
        "retry_count": 0,
        "replay_count": 0,
        "fallback_count": 0,
        "real_pilot_authorized": False,
        "evidence_root": str(evidence_root),
    }
    try:
        head, tree = physical._require_clean_repo(repo_root)
        summary["relayTheory"] = {"head": head, "tree": tree}
        results = []
        for replicate in ("A", "B"):
            result = _qualify_one(
                replicate=replicate,
                llama_cpp_root=llama_cpp_root,
                artifact_path=artifact_path,
                artifact_sha256=artifact_sha256,
                port=port,
                evidence_root=evidence_root,
                timeout=timeout,
                require_gpu=require_gpu,
            )
            results.append(result)
            summary["server_launch_count"] += 1
            summary["synthetic_model_facing_probe_count"] += result["probeCount"]

        if summary["server_launch_count"] != 2:
            fail("must launch exactly two isolated server lifetimes")
        if summary["synthetic_model_facing_probe_count"] != EXPECTED_PROBES:
            fail("synthetic probe count mismatch")

        a, b = results
        for key in ("revision", "tree", "buildNumber"):
            if a["llamaCpp"][key] != b["llamaCpp"][key]:
                fail(f"A/B llama.cpp {key} mismatch")
        if a["artifact"]["sha256"] != b["artifact"]["sha256"]:
            fail("A/B artifact SHA mismatch")
        if (
            a["runtime"]["attested"]["requestModel"]
            != b["runtime"]["attested"]["requestModel"]
        ):
            fail("A/B attested model mismatch")

        summary["replicates"] = results
        summary["disposition"] = "SYSTEMONE_RUNTIME_SYNTHETICALLY_QUALIFIED"
        write_json(evidence_root / "runtime-preflight-summary.json", summary)
        return 0, summary

    except Exception as exc:
        summary["disposition"] = "SYSTEMONE_RUNTIME_NOT_QUALIFIED"
        summary["error"] = {
            "type": type(exc).__name__,
            "message": str(exc),
        }
        write_json(evidence_root / "runtime-preflight-summary.json", summary)
        return 2, summary


def _run_text(command: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(completed.stderr or completed.stdout)
    return completed.stdout


def _init_git(path: Path, *, remote: str | None = None) -> str:
    path.mkdir(parents=True, exist_ok=True)
    _run_text(["git", "init", "-q"], path)
    _run_text(["git", "config", "user.email", "selftest@example.invalid"], path)
    _run_text(["git", "config", "user.name", "selftest"], path)
    (path / "README").write_text("selftest\n", encoding="utf-8")
    (path / ".gitignore").write_text("build/\n", encoding="utf-8")
    _run_text(["git", "add", "README", ".gitignore"], path)
    _run_text(["git", "commit", "-qm", "selftest"], path)
    if remote is not None:
        _run_text(["git", "remote", "add", "origin", remote], path)
    return _run_text(["git", "rev-parse", "HEAD"], path).strip()


def _fake_server(path: Path) -> None:
    code = r'''#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

if "--version" in sys.argv:
    print("llama.cpp fake build 9999")
    raise SystemExit(0)

parser=argparse.ArgumentParser(add_help=False)
parser.add_argument("-m")
parser.add_argument("--host")
parser.add_argument("--port",type=int)
parser.add_argument("-ngl")
parser.add_argument("-c",type=int)
parser.add_argument("-np",type=int)
parser.add_argument("--no-context-shift",action="store_true")
parser.add_argument("-lv")
parser.add_argument("--log-timestamps",action="store_true")
parser.add_argument("--log-file")
args,_=parser.parse_known_args()
root=Path(__file__).resolve().parents[2]
revision=subprocess.check_output(["git","rev-parse","HEAD"],cwd=root,text=True).strip()
if args.log_file:
    Path(args.log_file).write_text("fake server\n",encoding="utf-8")

class H(BaseHTTPRequestHandler):
    def log_message(self,*a): return
    def out(self,v,status=200):
        raw=json.dumps(v).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
    def do_GET(self):
        if self.path=="/health": self.out({"status":"ok"})
        elif self.path=="/v1/models": self.out({"data":[{"id":"fake-model"}]})
        elif self.path=="/props":
            self.out({
                "build_info":f"fake build 9999 {revision}",
                "model_alias":"fake-model",
                "model_path":str(Path(args.m).resolve()),
                "default_generation_settings":{"n_ctx":args.c},
                "total_slots":args.np,
                "model_ftype":"Q4_K - Medium",
                "chat_template":"fake-template"
            })
        elif self.path=="/slots": self.out([{"id":0,"n_ctx":args.c}])
        else: self.out({"error":"not found"},404)
    def do_POST(self):
        length=int(self.headers.get("Content-Length","0"))
        body=json.loads(self.rfile.read(length).decode())
        if self.path=="/v1/chat/completions":
            if body.get("reasoning_effort")!="none" or body.get("cache_prompt") is not False:
                self.out({"error":"normal config"},400); return
            self.out({
                "model":"fake-model",
                "choices":[{
                    "message":{"role":"assistant","content":"Synthetic relation observed."},
                    "finish_reason":"stop"
                }]
            }); return
        if self.path=="/v1/systemone":
            answers={}
            for name,q in body["questions"].items():
                keys=list(q["criteria"])
                choice=next((x for x in keys if x!="__unresolved__"),"__unresolved__")
                answers[name]={
                    "type":"choice",
                    "choice":choice,
                    "probabilities":{choice:1.0},
                    "confidence":1.0
                }
            self.out({
                "model":body["model"],
                "answers":answers,
                "usage":{"input_tokens":1,"output_tokens":0}
            }); return
        self.out({"error":"not found"},404)

ThreadingHTTPServer((args.host,args.port),H).serve_forever()
'''
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(code, encoding="utf-8")
    path.chmod(0o755)


def _free_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])
    finally:
        sock.close()


def self_test(manifest_path: Path) -> None:
    manifest = load_json(manifest_path)
    validate_manifest(manifest)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        repo = root / "relay-theory"
        _init_git(repo)
        llama = root / "llama.cpp"
        _init_git(llama, remote=EXPECTED_JEV_REMOTE + ".git")
        route_path = llama / EXPECTED_ROUTE_SOURCE_PATHS[0]
        route_path.parent.mkdir(parents=True, exist_ok=True)
        route_path.write_text(
            f'static constexpr const char * route = "{EXPECTED_SYSTEMONE_ROUTE}";\n',
            encoding="utf-8",
        )
        _run_text(["git", "add", str(route_path.relative_to(llama))], llama)
        _run_text(["git", "commit", "-qm", "add synthetic SystemOne route"], llama)
        server = llama / "build" / "bin" / "llama-server"
        _fake_server(server)
        observed = _inspect_source_identity(llama)
        _validate_source_identity(observed, enforce_exact_pin=False)
        mismatched = dict(observed)
        mismatched["revision"] = "0" * 40
        try:
            _validate_source_identity(mismatched, enforce_exact_pin=True)
        except RuntimePreflightError:
            pass
        else:
            raise AssertionError("exact Jev revision mismatch unexpectedly accepted")

        artifact = root / "fake.gguf"
        artifact.write_bytes(b"fake systemone artifact")
        sha = sha256_file(artifact)
        evidence = root / "evidence"
        evidence.mkdir()
        rc, summary = run_preflight(
            repo_root=repo,
            llama_cpp_root=llama,
            artifact_path=artifact,
            artifact_sha256=sha,
            evidence_root=evidence,
            port=_free_port(),
            timeout=10.0,
            require_gpu=False,
        )
        if rc != 0:
            raise AssertionError(summary)
        if summary["disposition"] != "SYSTEMONE_RUNTIME_SYNTHETICALLY_QUALIFIED":
            raise AssertionError("qualification disposition")
        if summary["server_launch_count"] != 2:
            raise AssertionError("server launch count")
        if summary["synthetic_model_facing_probe_count"] != EXPECTED_PROBES:
            raise AssertionError("probe count")
        if summary["scientific_model_calls"] != 0:
            raise AssertionError("scientific calls must remain zero")
        for replicate in ("A", "B"):
            cleanup = load_json(evidence / replicate / "cleanup.json")
            if cleanup.get("terminated") is not True:
                raise AssertionError(f"{replicate}: owned server not terminated")

    print("PAPER2_SYSTEMONE_RUNTIME_PREFLIGHT_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("research/paper2/systemone_runtime_preflight_v1.json"),
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--llama-cpp-root")
    parser.add_argument(
        "--artifact-path",
        default=str(
            Path.home() / "models" / "gguf" / "gemma-4-12B-it-Q4_K_M.gguf"
        ),
    )
    parser.add_argument("--expected-artifact-sha256", default=EXPECTED_REAL_GGUF_SHA256)
    parser.add_argument("--port", type=int, default=physical.DEFAULT_PORT)
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--evidence-root")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        manifest = load_json(args.manifest)
        validate_manifest(manifest)
        if args.self_test:
            self_test(args.manifest)
            return 0
        if not args.llama_cpp_root:
            fail("--llama-cpp-root is required for physical qualification")
        evidence = (
            Path(args.evidence_root).expanduser().resolve()
            if args.evidence_root
            else Path(tempfile.mkdtemp(prefix="relaytheory-systemone-preflight-"))
        )
        if args.evidence_root:
            evidence.mkdir(parents=True, exist_ok=False)
        rc, summary = run_preflight(
            repo_root=Path(args.repo_root).resolve(),
            llama_cpp_root=Path(args.llama_cpp_root).expanduser().resolve(),
            artifact_path=Path(args.artifact_path).expanduser().resolve(),
            artifact_sha256=args.expected_artifact_sha256,
            evidence_root=evidence,
            port=args.port,
            timeout=args.timeout,
            require_gpu=True,
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        return rc
    except Exception as exc:
        print(f"SYSTEMONE_RUNTIME_NOT_QUALIFIED: {type(exc).__name__}: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
