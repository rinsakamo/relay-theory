#!/usr/bin/env python3
"""Run the frozen Paper 2 ClaimIR extraction pilot on an OpenAI-compatible endpoint.

Owner: #147.

This runner is intended for local llama.cpp / LM Studio / other compatible
endpoints. It performs ten stateless chat-completion requests: five bundles in
pass A and the same five bundles in pass B. Each request contains only the
frozen extraction prompt and one opaque source bundle.

The runner:
- verifies local raw abstracts against the frozen run-package digests;
- prepares opaque source bundles;
- uses one identical extractor configuration across A/B;
- validates every returned extraction candidate;
- freezes candidate bytes and digests;
- emits a v1 execution receipt;
- validates that receipt before reporting success.

It does not perform basis decomposition.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import threading
import time
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from paper2_extraction_bundle_prepare import (
    canonical_json_bytes,
    normalize_text,
    prepare,
    sha256_text,
)
from paper2_extraction_procedure_validate import (
    ContractError as CandidateContractError,
    validate_candidate,
)
from paper2_extraction_receipt_validate import (
    PACKAGE_MERGE,
    PACKAGE_VERSION,
    PROMPT_SHA256,
    RECEIPT_VERSION,
    validate_receipt,
)


CONFIG_VERSION = "paper2-openai-runner-config-v1"
EXPECTED_BUNDLES = {"B0001", "B0002", "B0003", "B0004", "B0005"}


class RunnerError(ValueError):
    pass


def fail(message: str) -> None:
    raise RunnerError(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_config(config: Any) -> dict[str, Any]:
    if not isinstance(config, dict):
        fail("config must be an object")
    expected = {
        "schema_version",
        "extractor_identity",
        "extractor_revision",
        "base_url",
        "model",
        "temperature",
        "top_p",
        "max_tokens",
        "timeout_seconds",
        "response_format",
        "api_key_env",
    }
    if set(config) != expected:
        fail(
            "config key mismatch "
            f"missing={sorted(expected-set(config))} extra={sorted(set(config)-expected)}"
        )
    if config["schema_version"] != CONFIG_VERSION:
        fail("config schema_version mismatch")
    for key in ("extractor_identity", "extractor_revision", "base_url", "model"):
        if not isinstance(config[key], str) or not config[key].strip():
            fail(f"config.{key} must be non-empty string")
    if not config["base_url"].startswith(("http://", "https://")):
        fail("config.base_url must be http(s)")
    if not isinstance(config["temperature"], (int, float)) or isinstance(config["temperature"], bool):
        fail("config.temperature must be numeric")
    if not 0 <= float(config["temperature"]) <= 2:
        fail("config.temperature outside [0,2]")
    if not isinstance(config["top_p"], (int, float)) or isinstance(config["top_p"], bool):
        fail("config.top_p must be numeric")
    if not 0 < float(config["top_p"]) <= 1:
        fail("config.top_p outside (0,1]")
    for key, upper in (("max_tokens", None), ("timeout_seconds", 3600)):
        value = config[key]
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            fail(f"config.{key} must be positive integer")
        if upper is not None and value > upper:
            fail(f"config.{key} exceeds {upper}")
    if config["response_format"] not in {"none", "json_object"}:
        fail("config.response_format invalid")
    if config["api_key_env"] is not None:
        if not isinstance(config["api_key_env"], str) or not config["api_key_env"].strip():
            fail("config.api_key_env must be null or non-empty string")
    return config


def configuration_sha256(config: dict[str, Any]) -> str:
    return sha256_bytes(canonical_json_bytes(config))


def request_payload(
    config: dict[str, Any],
    prompt: str,
    bundle: dict[str, Any],
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": config["model"],
        "messages": [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": canonical_json_bytes(bundle).decode("utf-8").rstrip("\n"),
            },
        ],
        "temperature": config["temperature"],
        "top_p": config["top_p"],
        "max_tokens": config["max_tokens"],
    }
    if config["response_format"] == "json_object":
        payload["response_format"] = {"type": "json_object"}
    return payload


def chat_completion(
    config: dict[str, Any],
    prompt: str,
    bundle: dict[str, Any],
) -> dict[str, Any]:
    endpoint = config["base_url"].rstrip("/") + "/chat/completions"
    payload = canonical_json_bytes(request_payload(config, prompt, bundle))
    headers = {"Content-Type": "application/json"}

    env_name = config["api_key_env"]
    if env_name is not None:
        value = os.environ.get(env_name)
        if not value:
            fail(f"API key environment variable {env_name!r} is not set")
        headers["Authorization"] = f"Bearer {value}"

    request = Request(endpoint, data=payload, headers=headers, method="POST")
    try:
        with urlopen(request, timeout=config["timeout_seconds"]) as response:
            raw = response.read()
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RunnerError(f"endpoint HTTP {exc.code}: {detail[:500]}") from exc
    except URLError as exc:
        raise RunnerError(f"endpoint request failed: {exc}") from exc

    try:
        envelope = json.loads(raw.decode("utf-8"))
        content = envelope["choices"][0]["message"]["content"]
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
        raise RunnerError("endpoint response is not OpenAI-compatible chat content") from exc

    if not isinstance(content, str):
        fail("assistant message content must be string")
    try:
        candidate = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RunnerError(
            "assistant content must be pure JSON matching extraction_candidate_v1"
        ) from exc

    try:
        validate_candidate(candidate, bundle)
    except CandidateContractError as exc:
        raise RunnerError(f"invalid extraction candidate: {exc}") from exc
    return candidate


def package_source_map(package: dict[str, Any]) -> dict[str, dict[str, Any]]:
    sources = package.get("sources")
    if not isinstance(sources, list) or len(sources) != 5:
        fail("run package must contain five sources")
    result = {item["bundle_id"]: item for item in sources}
    if set(result) != EXPECTED_BUNDLES:
        fail("run package bundle membership mismatch")
    return result


def run_pass(
    *,
    pass_id: str,
    config: dict[str, Any],
    prompt: str,
    package: dict[str, Any],
    bundles_dir: Path,
    output_dir: Path,
) -> dict[str, Any]:
    started = utc_now()
    run_id = f"{pass_id}-{uuid.uuid4()}"
    context_id = f"context-{pass_id}-{uuid.uuid4()}"
    source_map = package_source_map(package)
    candidates: list[dict[str, Any]] = []

    for bundle_id in sorted(EXPECTED_BUNDLES):
        bundle_path = bundles_dir / f"{bundle_id}.json"
        bundle_raw = bundle_path.read_bytes()
        bundle = json.loads(bundle_raw.decode("utf-8"))
        if bundle.get("bundle_id") != bundle_id:
            fail(f"{bundle_path}: bundle_id mismatch")

        candidate = chat_completion(config, prompt, bundle)
        candidate_raw = canonical_json_bytes(candidate)
        rel = Path("candidates") / pass_id / f"{bundle_id}.json"
        path = output_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(candidate_raw)

        candidates.append(
            {
                "bundle_id": bundle_id,
                "source_text_sha256": source_map[bundle_id]["abstract_sha256_nfkc_ws1"],
                "bundle_sha256": sha256_bytes(bundle_raw),
                "candidate_path": str(rel),
                "candidate_sha256": sha256_bytes(candidate_raw),
            }
        )

    completed = utc_now()
    return {
        "pass_id": pass_id,
        "run_id": run_id,
        "context_id": context_id,
        "started_at": started,
        "completed_at": completed,
        "isolation_attestation": {
            "fresh_context": True,
            "other_pass_output_visible": False,
            "other_bundle_output_visible": False,
            "basis_or_decomposition_visible": False,
            "procedure_modified_after_first_output": False,
            "attestation_scope": "executor_attestation_not_independent_proof",
        },
        "candidates": candidates,
    }


def execute(
    *,
    package_path: Path,
    prompt_path: Path,
    source_texts_path: Path,
    config_path: Path,
    output_dir: Path,
) -> Path:
    package = load_json(package_path)
    config = validate_config(load_json(config_path))
    prompt_raw = prompt_path.read_bytes()
    if sha256_bytes(prompt_raw) != PROMPT_SHA256:
        fail("frozen extraction prompt digest mismatch")
    prompt = prompt_raw.decode("utf-8")

    source_texts = load_json(source_texts_path)
    if not isinstance(source_texts, dict):
        fail("source-texts input must map sample_id to raw abstract text")

    bundles_dir = output_dir / "bundles"
    prepared = prepare(package, source_texts, bundles_dir)
    if len(prepared) != 5:
        fail("expected exactly five prepared bundles")

    # Each model request is stateless and contains only prompt + current bundle.
    # A and B reuse the same frozen config and bundle bytes.
    pass_a = run_pass(
        pass_id="A",
        config=config,
        prompt=prompt,
        package=package,
        bundles_dir=bundles_dir,
        output_dir=output_dir,
    )
    pass_b = run_pass(
        pass_id="B",
        config=config,
        prompt=prompt,
        package=package,
        bundles_dir=bundles_dir,
        output_dir=output_dir,
    )

    receipt = {
        "schema_version": RECEIPT_VERSION,
        "owner_issue": 147,
        "status": "CANDIDATES_FROZEN_BEFORE_COMPARISON",
        "run_package": {
            "merge_sha": PACKAGE_MERGE,
            "prompt_sha256": PROMPT_SHA256,
            "package_schema": PACKAGE_VERSION,
        },
        "extractor": {
            "identity": config["extractor_identity"],
            "revision": config["extractor_revision"],
            "configuration_sha256": configuration_sha256(config),
            "configuration_note": (
                f"OpenAI-compatible runner v1; model={config['model']}; "
                f"temperature={config['temperature']}; top_p={config['top_p']}; "
                f"max_tokens={config['max_tokens']}; response_format={config['response_format']}"
            ),
        },
        "passes": [pass_a, pass_b],
    }

    receipt_path = output_dir / "receipt.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_bytes(canonical_json_bytes(receipt))
    validate_receipt(receipt, package, receipt_path, check_files=True)
    return receipt_path


def synthetic_package(package: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str]]:
    synthetic = copy.deepcopy(package)
    texts: dict[str, str] = {}
    for index, source in enumerate(synthetic["sources"], start=1):
        value = f"Synthetic abstract fixture number {index}."
        texts[source["sample_id"]] = value
        source["abstract_sha256_nfkc_ws1"] = sha256_text(normalize_text(value))
    return synthetic, texts


class MockHandler(BaseHTTPRequestHandler):
    requests_seen: list[dict[str, Any]] = []

    def log_message(self, format: str, *args: Any) -> None:
        return

    def do_POST(self) -> None:
        if self.path != "/v1/chat/completions":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        payload = json.loads(raw.decode("utf-8"))
        self.__class__.requests_seen.append(payload)

        messages = payload.get("messages")
        if not isinstance(messages, list) or len(messages) != 2:
            self.send_error(400)
            return
        user = messages[1]
        bundle = json.loads(user["content"])
        bundle_id = bundle["bundle_id"]
        candidate = {
            "schema_version": "paper2-extraction-candidate-v1",
            "bundle_id": bundle_id,
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
                "nodes": [
                    {
                        "id": "observed_state",
                        "role": "state_or_structure",
                        "description": "a source-grounded observed state",
                        "source_span_ids": ["s1"],
                        "grounding": "explicit",
                    }
                ],
                "relations": [],
            },
        }
        response = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": json.dumps(candidate, ensure_ascii=False),
                    }
                }
            ]
        }
        encoded = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def self_test(package_path: Path, prompt_path: Path) -> None:
    import tempfile

    package = load_json(package_path)
    synthetic, texts = synthetic_package(package)

    server = ThreadingHTTPServer(("127.0.0.1", 0), MockHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_file = root / "package.json"
            source_file = root / "sources.json"
            config_file = root / "config.json"
            output_dir = root / "run"

            package_file.write_bytes(canonical_json_bytes(synthetic))
            source_file.write_bytes(canonical_json_bytes(texts))
            config = {
                "schema_version": CONFIG_VERSION,
                "extractor_identity": "mock-openai-compatible",
                "extractor_revision": "selftest-v1",
                "base_url": f"http://127.0.0.1:{port}/v1",
                "model": "mock-model",
                "temperature": 0.2,
                "top_p": 1.0,
                "max_tokens": 1024,
                "timeout_seconds": 30,
                "response_format": "json_object",
                "api_key_env": None,
            }
            config_file.write_bytes(canonical_json_bytes(config))

            MockHandler.requests_seen = []
            receipt_path = execute(
                package_path=package_file,
                prompt_path=prompt_path,
                source_texts_path=source_file,
                config_path=config_file,
                output_dir=output_dir,
            )
            receipt = load_json(receipt_path)
            validate_receipt(receipt, synthetic, receipt_path, check_files=True)

            if len(MockHandler.requests_seen) != 10:
                raise AssertionError("runner must issue exactly ten isolated requests")
            for payload in MockHandler.requests_seen:
                messages = payload["messages"]
                if len(messages) != 2:
                    raise AssertionError("each request must contain exactly prompt + one bundle")
                bundle = json.loads(messages[1]["content"])
                current = bundle["bundle_id"]
                serialized = messages[1]["content"]
                for other in EXPECTED_BUNDLES - {current}:
                    if other in serialized:
                        raise AssertionError("request leaks another bundle id")

            # Both passes should contain the same five bundle digests but distinct
            # audit run/context IDs.
            a, b = receipt["passes"]
            if a["run_id"] == b["run_id"] or a["context_id"] == b["context_id"]:
                raise AssertionError("A/B audit identities must differ")
            by_a = {x["bundle_id"]: x for x in a["candidates"]}
            by_b = {x["bundle_id"]: x for x in b["candidates"]}
            for bundle in EXPECTED_BUNDLES:
                if by_a[bundle]["bundle_sha256"] != by_b[bundle]["bundle_sha256"]:
                    raise AssertionError("A/B bundle bytes must match")

    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    print("PAPER2_OPENAI_LOCAL_RUNNER_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
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
    parser.add_argument("--source-texts", type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        if args.self_test:
            self_test(args.package, args.prompt)
            return 0

        if args.source_texts is None or args.config is None or args.output_dir is None:
            fail("--source-texts, --config, and --output-dir are required")

        receipt = execute(
            package_path=args.package,
            prompt_path=args.prompt,
            source_texts_path=args.source_texts,
            config_path=args.config,
            output_dir=args.output_dir,
        )
        print(
            json.dumps(
                {
                    "status": "PAPER2_EXTRACTION_A_B_FROZEN",
                    "receipt": str(receipt),
                },
                sort_keys=True,
            )
        )
        return 0
    except (
        OSError,
        json.JSONDecodeError,
        RunnerError,
        CandidateContractError,
        ValueError,
    ) as exc:
        print(f"PAPER2_OPENAI_LOCAL_RUNNER_INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
