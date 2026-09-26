#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from paper2_eligibility_adjudication_validate import (
    AdjudicationError,
    agreement_projection,
    assemble_accessible_record,
    compare_decisions,
    load_procedure,
    validate_decision,
    validate_source_bundle,
)

RUNNER_CONTRACT = Path("research/paper2/eligibility_runner_v1.json")
CONFIG_VERSION = "paper2-eligibility-runner-config-v1"


class RunnerError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write(path: Path, data: bytes) -> None:
    if path.exists():
        raise RunnerError(f"OUTPUT_ALREADY_EXISTS:{path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    if tmp.exists():
        raise RunnerError(f"OUTPUT_TEMP_ALREADY_EXISTS:{tmp}")
    try:
        with tmp.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def overwrite_receipt(path: Path, receipt: dict[str, Any]) -> None:
    data = canonical_json_bytes(receipt)
    tmp = path.with_name(f".{path.name}.tmp")
    with tmp.open("wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def validate_runner_contract(contract: dict[str, Any]) -> None:
    if contract.get("schema_version") != "paper2-eligibility-runner-contract-v1":
        raise RunnerError("RUNNER_CONTRACT_SCHEMA_MISMATCH")
    if contract.get("owner_issue") != 216 or contract.get("parent_issue") != 214:
        raise RunnerError("RUNNER_CONTRACT_OWNER_DRIFT")
    request = contract.get("request_contract", {})
    expected = {
        "endpoint_suffix": "/chat/completions",
        "stateless": True,
        "reasoning_effort": "none",
        "cache_prompt": False,
        "temperature": 0,
        "top_p": 1,
        "response_format": "json_object",
        "automatic_retry_count": 0,
        "pass_order": ["A", "B"],
        "adjudication_only_on_disagreement": True,
    }
    if request != expected:
        raise RunnerError("RUNNER_REQUEST_CONTRACT_DRIFT")
    if contract.get("output_directory_must_not_preexist") is not True:
        raise RunnerError("RUNNER_OUTPUT_DIRECTORY_POLICY_DRIFT")
    if contract.get("request_failure_after_submission_consumes_pass") is not True:
        raise RunnerError("RUNNER_SUBMISSION_CONSUMPTION_POLICY_DRIFT")
    if not isinstance(contract.get("real_execution_authorized"), bool):
        raise RunnerError("RUNNER_EXECUTION_AUTHORITY_INVALID")
    if contract.get("architecture_consequence") != "NONE":
        raise RunnerError("RUNNER_ARCHITECTURE_CONSEQUENCE_DRIFT")
    for info in contract.get("prompts", {}).values():
        path = Path(info["path"])
        if not path.is_file():
            raise RunnerError(f"RUNNER_PROMPT_MISSING:{path}")
        if sha256_bytes(path.read_bytes()) != info["sha256_utf8"]:
            raise RunnerError(f"RUNNER_PROMPT_DIGEST_MISMATCH:{path}")


def validate_config(config: dict[str, Any]) -> None:
    expected = {
        "schema_version",
        "classifier_identity",
        "classifier_revision",
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
        raise RunnerError("RUNNER_CONFIG_FIELD_SET_INVALID")
    if config["schema_version"] != CONFIG_VERSION:
        raise RunnerError("RUNNER_CONFIG_SCHEMA_MISMATCH")
    for key in ("classifier_identity", "classifier_revision", "base_url", "model"):
        if not isinstance(config[key], str) or not config[key].strip():
            raise RunnerError(f"RUNNER_CONFIG_STRING_INVALID:{key}")
    if not config["base_url"].startswith(("http://", "https://")):
        raise RunnerError("RUNNER_CONFIG_BASE_URL_INVALID")
    if config["temperature"] != 0 or config["top_p"] != 1:
        raise RunnerError("RUNNER_CONFIG_DECODING_DRIFT")
    if not isinstance(config["max_tokens"], int) or config["max_tokens"] < 1:
        raise RunnerError("RUNNER_CONFIG_MAX_TOKENS_INVALID")
    if (
        not isinstance(config["timeout_seconds"], int)
        or not 1 <= config["timeout_seconds"] <= 3600
    ):
        raise RunnerError("RUNNER_CONFIG_TIMEOUT_INVALID")
    if config["response_format"] != "json_object":
        raise RunnerError("RUNNER_CONFIG_RESPONSE_FORMAT_DRIFT")
    if config["api_key_env"] is not None and (
        not isinstance(config["api_key_env"], str)
        or not config["api_key_env"].strip()
    ):
        raise RunnerError("RUNNER_CONFIG_API_KEY_ENV_INVALID")


def validate_binding(binding: dict[str, Any]) -> None:
    expected = {
        "provider_work_id",
        "era",
        "rank",
        "ranked_artifact_sha256",
        "source_access_version",
        "adjudication_version",
    }
    if set(binding) != expected:
        raise RunnerError("RUNNER_BINDING_FIELD_SET_INVALID")
    if not isinstance(binding["provider_work_id"], str) or not binding["provider_work_id"]:
        raise RunnerError("RUNNER_BINDING_WORK_ID_INVALID")
    if not isinstance(binding["era"], str) or not binding["era"]:
        raise RunnerError("RUNNER_BINDING_ERA_INVALID")
    if not isinstance(binding["rank"], int) or binding["rank"] < 1:
        raise RunnerError("RUNNER_BINDING_RANK_INVALID")
    digest = binding["ranked_artifact_sha256"]
    if not isinstance(digest, str) or len(digest) != 64:
        raise RunnerError("RUNNER_BINDING_RANKED_DIGEST_INVALID")
    for key in ("source_access_version", "adjudication_version"):
        if not isinstance(binding[key], str) or not binding[key]:
            raise RunnerError(f"RUNNER_BINDING_STRING_INVALID:{key}")


def request_payload(
    config: dict[str, Any],
    *,
    system_prompt: str,
    user_value: dict[str, Any],
) -> dict[str, Any]:
    return {
        "model": config["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": canonical_json_bytes(user_value).decode("utf-8").rstrip("\n"),
            },
        ],
        "temperature": 0,
        "top_p": 1,
        "max_tokens": config["max_tokens"],
        "reasoning_effort": "none",
        "cache_prompt": False,
        "response_format": {"type": "json_object"},
    }


def perform_request(
    config: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    endpoint = config["base_url"].rstrip("/") + "/chat/completions"
    headers = {"Content-Type": "application/json"}
    env = config["api_key_env"]
    if env is not None:
        token = os.environ.get(env)
        if not token:
            raise RunnerError(f"RUNNER_API_KEY_ENV_ABSENT:{env}")
        headers["Authorization"] = f"Bearer {token}"
    req = Request(
        endpoint,
        data=canonical_json_bytes(payload),
        headers=headers,
        method="POST",
    )
    try:
        with urlopen(req, timeout=config["timeout_seconds"]) as response:
            raw = response.read()
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RunnerError(f"RUNNER_HTTP_ERROR:{exc.code}:{detail[:300]}") from exc
    except URLError as exc:
        raise RunnerError(f"RUNNER_TRANSPORT_ERROR:{exc}") from exc
    try:
        envelope = json.loads(raw.decode("utf-8"))
        content = envelope["choices"][0]["message"]["content"]
        decision = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
        raise RunnerError("RUNNER_RESPONSE_NOT_JSON_DECISION") from exc
    if not isinstance(decision, dict):
        raise RunnerError("RUNNER_RESPONSE_DECISION_NOT_OBJECT")
    return decision


def initial_receipt(
    *,
    config: dict[str, Any],
    bundle_sha: str,
    binding_sha: str,
) -> dict[str, Any]:
    return {
        "schema_version": "paper2-eligibility-runner-receipt-v1",
        "owner_issue": 216,
        "started_at": utc_now(),
        "completed_at": None,
        "status": "EXECUTION_STARTED",
        "classifier": {
            "identity": config["classifier_identity"],
            "revision": config["classifier_revision"],
            "model": config["model"],
            "config_sha256": sha256_bytes(canonical_json_bytes(config)),
        },
        "source_bundle_sha256": bundle_sha,
        "binding_sha256": binding_sha,
        "requests": {
            "A": {"submitted": False, "request_sha256": None, "response_sha256": None},
            "B": {"submitted": False, "request_sha256": None, "response_sha256": None},
            "ADJUDICATION": {
                "required": None,
                "submitted": False,
                "request_sha256": None,
                "response_sha256": None,
            },
        },
        "failure": None,
    }


def submit_once(
    *,
    pass_id: str,
    config: dict[str, Any],
    payload: dict[str, Any],
    bundle: dict[str, Any],
    procedure: dict[str, Any],
    root: Path,
    receipt_path: Path,
    receipt: dict[str, Any],
) -> dict[str, Any]:
    req_bytes = canonical_json_bytes(payload)
    req_sha = sha256_bytes(req_bytes)
    atomic_write(root / "requests" / f"{pass_id}.sha256", (req_sha + "\n").encode("ascii"))
    request_state = receipt["requests"][pass_id]
    if request_state["submitted"]:
        raise RunnerError(f"RUNNER_PASS_ALREADY_SUBMITTED:{pass_id}")
    request_state["request_sha256"] = req_sha
    request_state["submitted"] = True
    overwrite_receipt(receipt_path, receipt)

    decision = perform_request(config, payload)
    validate_decision(decision, bundle=bundle, procedure=procedure)
    response_bytes = canonical_json_bytes(decision)
    response_sha = sha256_bytes(response_bytes)
    atomic_write(root / "responses" / f"{pass_id}.json", response_bytes)
    atomic_write(
        root / "responses" / f"{pass_id}.sha256",
        (response_sha + "\n").encode("ascii"),
    )
    request_state["response_sha256"] = response_sha
    overwrite_receipt(receipt_path, receipt)
    return decision


def execute(
    *,
    contract_path: Path,
    procedure_path: Path,
    config_path: Path,
    source_bundle_path: Path,
    binding_path: Path,
    output_dir: Path,
    allow_real: bool,
) -> Path:
    contract = load_json(contract_path)
    validate_runner_contract(contract)
    if not allow_real and contract.get("real_execution_authorized") is not True:
        raise RunnerError("REAL_ELIGIBILITY_RUNNER_EXECUTION_NOT_AUTHORIZED")
    procedure = load_procedure(procedure_path)
    config = load_json(config_path)
    validate_config(config)
    bundle = load_json(source_bundle_path)
    validate_source_bundle(bundle)
    binding = load_json(binding_path)
    validate_binding(binding)
    if bundle["source_access_status"] == "INACCESSIBLE":
        raise RunnerError("RUNNER_ACCESSIBLE_BUNDLE_REQUIRED")
    if output_dir.exists():
        raise RunnerError(f"OUTPUT_DIRECTORY_ALREADY_EXISTS:{output_dir}")
    output_dir.mkdir(parents=True)

    bundle_bytes = canonical_json_bytes(bundle)
    binding_bytes = canonical_json_bytes(binding)
    atomic_write(output_dir / "source-bundle.json", bundle_bytes)
    atomic_write(output_dir / "binding.json", binding_bytes)

    receipt_path = output_dir / "receipt.json"
    receipt = initial_receipt(
        config=config,
        bundle_sha=sha256_bytes(bundle_bytes),
        binding_sha=sha256_bytes(binding_bytes),
    )
    atomic_write(receipt_path, canonical_json_bytes(receipt))

    classifier_prompt = Path(contract["prompts"]["classifier"]["path"]).read_text(
        encoding="utf-8"
    )
    disagreement_prompt = Path(
        contract["prompts"]["disagreement_adjudicator"]["path"]
    ).read_text(encoding="utf-8")

    try:
        payload_a = request_payload(
            config,
            system_prompt=classifier_prompt,
            user_value=bundle,
        )
        pass_a = submit_once(
            pass_id="A",
            config=config,
            payload=payload_a,
            bundle=bundle,
            procedure=procedure,
            root=output_dir,
            receipt_path=receipt_path,
            receipt=receipt,
        )

        payload_b = request_payload(
            config,
            system_prompt=classifier_prompt,
            user_value=bundle,
        )
        pass_b = submit_once(
            pass_id="B",
            config=config,
            payload=payload_b,
            bundle=bundle,
            procedure=procedure,
            root=output_dir,
            receipt_path=receipt_path,
            receipt=receipt,
        )

        comparison = compare_decisions(
            pass_a,
            pass_b,
            bundle=bundle,
            procedure=procedure,
        )
        atomic_write(output_dir / "agreement.json", canonical_json_bytes(comparison))
        receipt["requests"]["ADJUDICATION"]["required"] = bool(
            comparison["adjudication_required"]
        )
        overwrite_receipt(receipt_path, receipt)

        adjudication = None
        if comparison["adjudication_required"]:
            adjudication_user = {
                "source_bundle": bundle,
                "projection_a": agreement_projection(pass_a),
                "projection_b": agreement_projection(pass_b),
            }
            payload_adj = request_payload(
                config,
                system_prompt=disagreement_prompt,
                user_value=adjudication_user,
            )
            adjudication = submit_once(
                pass_id="ADJUDICATION",
                config=config,
                payload=payload_adj,
                bundle=bundle,
                procedure=procedure,
                root=output_dir,
                receipt_path=receipt_path,
                receipt=receipt,
            )

        assembled = assemble_accessible_record(
            bundle=bundle,
            pass_a=pass_a,
            pass_b=pass_b,
            adjudication=adjudication,
            procedure=procedure,
            provider_work_id=binding["provider_work_id"],
            era=binding["era"],
            rank=binding["rank"],
            ranked_artifact_sha256=binding["ranked_artifact_sha256"],
            source_access_version=binding["source_access_version"],
            adjudication_version=binding["adjudication_version"],
        )
        atomic_write(output_dir / "assembled-record.json", canonical_json_bytes(assembled))
        receipt["status"] = "ELIGIBILITY_RECORD_FROZEN"
        receipt["completed_at"] = utc_now()
        receipt["assembled_record_sha256"] = sha256_bytes(canonical_json_bytes(assembled))
        overwrite_receipt(receipt_path, receipt)
        return receipt_path
    except Exception as exc:
        receipt["status"] = "EXECUTION_FAILED"
        receipt["completed_at"] = utc_now()
        receipt["failure"] = f"{type(exc).__name__}:{exc}"
        overwrite_receipt(receipt_path, receipt)
        raise


class MockHandler(BaseHTTPRequestHandler):
    mode = "agreement"
    seen_payloads: list[dict[str, Any]] = []
    ordinary_count = 0

    def log_message(self, format: str, *args: Any) -> None:
        return

    @classmethod
    def reset(cls, mode: str) -> None:
        cls.mode = mode
        cls.seen_payloads = []
        cls.ordinary_count = 0

    def do_POST(self) -> None:
        if self.path != "/v1/chat/completions":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8"))
        self.__class__.seen_payloads.append(payload)
        user_value = json.loads(payload["messages"][1]["content"])

        if "source_bundle" in user_value:
            bundle = user_value["source_bundle"]
            decision = synthetic_decision(bundle["bundle_id"], "ELIGIBILITY_UNCERTAIN")
        else:
            bundle = user_value
            self.__class__.ordinary_count += 1
            if self.__class__.mode == "disagreement" and self.__class__.ordinary_count == 2:
                decision = synthetic_decision(bundle["bundle_id"], "EXCLUDE")
            else:
                decision = synthetic_decision(bundle["bundle_id"], "INCLUDE")

        envelope = {
            "choices": [
                {"message": {"role": "assistant", "content": json.dumps(decision)}}
            ]
        }
        data = json.dumps(envelope).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def synthetic_decision(bundle_id: str, state: str) -> dict[str, Any]:
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
                "claim_id": "c1",
                "source_locator": "s1",
                "route": "A_EXPLICIT_COGNITIVE_CAPACITY",
                "generalization": "YES",
                "operational_roles": ["CONTEXT"],
                "construct_level_relevance": "YES",
            }
        ]
    elif state == "EXCLUDE":
        checks["task_use_only"] = True
        reasons = ["X1_TASK_USE_ONLY"]
    elif state == "ELIGIBILITY_UNCERTAIN":
        reasons = ["INSUFFICIENT_SOURCE_GROUNDING"]
    return {
        "schema_version": "paper2-eligibility-decision-v1",
        "bundle_id": bundle_id,
        "claims": claims,
        "exclusion_checks": checks,
        "decision": {"state": state, "reason_codes": reasons},
    }


def self_test() -> None:
    import tempfile

    contract = load_json(RUNNER_CONTRACT)
    validate_runner_contract(contract)
    assert contract["real_execution_authorized"] is False

    procedure_path = Path("research/paper2/eligibility_adjudication_v1.json")
    bundle = {
        "schema_version": "paper2-eligibility-source-bundle-v1",
        "bundle_id": "E0001",
        "source_language": "en",
        "source_access_status": "ABSTRACT_ONLY",
        "source_spans": [{"span_id": "s1", "text": "Synthetic general capacity claim."}],
    }
    binding = {
        "provider_work_id": "W-SECRET-BINDING",
        "era": "2020-2026",
        "rank": 17,
        "ranked_artifact_sha256": "a" * 64,
        "source_access_version": "synthetic-v1",
        "adjudication_version": "paper2-eligibility-adjudication-v1",
    }

    server = ThreadingHTTPServer(("127.0.0.1", 0), MockHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        for mode, expected_requests, expected_state in (
            ("agreement", 2, "INCLUDE"),
            ("disagreement", 3, "ELIGIBILITY_UNCERTAIN"),
        ):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                config_path = root / "config.json"
                bundle_path = root / "bundle.json"
                binding_path = root / "binding.json"
                output_dir = root / "run"
                config = {
                    "schema_version": CONFIG_VERSION,
                    "classifier_identity": "mock",
                    "classifier_revision": "selftest-v1",
                    "base_url": f"http://127.0.0.1:{port}/v1",
                    "model": "mock-model",
                    "temperature": 0,
                    "top_p": 1,
                    "max_tokens": 1024,
                    "timeout_seconds": 30,
                    "response_format": "json_object",
                    "api_key_env": None,
                }
                config_path.write_bytes(canonical_json_bytes(config))
                bundle_path.write_bytes(canonical_json_bytes(bundle))
                binding_path.write_bytes(canonical_json_bytes(binding))
                MockHandler.reset(mode)

                receipt_path = execute(
                    contract_path=RUNNER_CONTRACT,
                    procedure_path=procedure_path,
                    config_path=config_path,
                    source_bundle_path=bundle_path,
                    binding_path=binding_path,
                    output_dir=output_dir,
                    allow_real=True,
                )
                receipt = load_json(receipt_path)
                assembled = load_json(output_dir / "assembled-record.json")
                if len(MockHandler.seen_payloads) != expected_requests:
                    raise AssertionError("unexpected mock request count")
                if assembled["decision"]["state"] != expected_state:
                    raise AssertionError("unexpected assembled decision")
                if receipt["requests"]["A"]["submitted"] is not True:
                    raise AssertionError("A must be submitted")
                if receipt["requests"]["B"]["submitted"] is not True:
                    raise AssertionError("B must be submitted")
                if (
                    receipt["requests"]["ADJUDICATION"]["submitted"]
                    != (mode == "disagreement")
                ):
                    raise AssertionError("adjudication submission mismatch")

                for index, payload in enumerate(MockHandler.seen_payloads):
                    if payload["reasoning_effort"] != "none":
                        raise AssertionError("reasoning must be disabled")
                    if payload["cache_prompt"] is not False:
                        raise AssertionError("prompt cache must be disabled")
                    if payload["temperature"] != 0 or payload["top_p"] != 1:
                        raise AssertionError("decoding config drift")
                    serialized = canonical_json_bytes(payload).decode("utf-8")
                    for secret in (
                        binding["provider_work_id"],
                        binding["era"],
                        str(binding["rank"]),
                        binding["ranked_artifact_sha256"],
                        binding["source_access_version"],
                        binding["adjudication_version"],
                    ):
                        if secret in serialized:
                            raise AssertionError(
                                f"model request leaked binding field at request {index}: {secret}"
                            )

                try:
                    execute(
                        contract_path=RUNNER_CONTRACT,
                        procedure_path=procedure_path,
                        config_path=config_path,
                        source_bundle_path=bundle_path,
                        binding_path=binding_path,
                        output_dir=output_dir,
                        allow_real=True,
                    )
                except RunnerError as exc:
                    if "OUTPUT_DIRECTORY_ALREADY_EXISTS" not in str(exc):
                        raise
                else:
                    raise AssertionError("runner must reject existing output directory")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    print("PAPER2_ELIGIBILITY_RUNNER_APPARATUS_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=RUNNER_CONTRACT)
    parser.add_argument(
        "--procedure",
        type=Path,
        default=Path("research/paper2/eligibility_adjudication_v1.json"),
    )
    parser.add_argument("--config", type=Path)
    parser.add_argument("--source-bundle", type=Path)
    parser.add_argument("--binding", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    if args.config is None or args.source_bundle is None or args.binding is None or args.output_dir is None:
        raise SystemExit("--config, --source-bundle, --binding, and --output-dir are required")

    receipt = execute(
        contract_path=args.contract,
        procedure_path=args.procedure,
        config_path=args.config,
        source_bundle_path=args.source_bundle,
        binding_path=args.binding,
        output_dir=args.output_dir,
        allow_real=False,
    )
    print(
        json.dumps(
            {
                "classification": "PAPER2_ELIGIBILITY_RUNNER_EXECUTED",
                "receipt": str(receipt),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
