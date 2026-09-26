#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

import paper2_eligibility_openai_runner as runner
from paper2_eligibility_adjudication_validate import validate_source_bundle

QUALIFICATION_CONTRACT = Path(
    "research/paper2/eligibility_runtime_qualification_v1.json"
)
RUNNER_PROCEDURE = Path("research/paper2/eligibility_adjudication_v1.json")
RUNTIME_MANIFEST_SCHEMA = "paper2-eligibility-runtime-manifest-v1"


class QualificationError(RuntimeError):
    pass


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


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    if path.exists():
        raise QualificationError(f"OUTPUT_ALREADY_EXISTS:{path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    if tmp.exists():
        raise QualificationError(f"OUTPUT_TEMP_ALREADY_EXISTS:{tmp}")
    try:
        with tmp.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def overwrite_json(path: Path, value: dict[str, Any]) -> None:
    data = canonical_json_bytes(value)
    tmp = path.with_name(f".{path.name}.tmp")
    with tmp.open("wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def git_text(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise QualificationError(
            f"GIT_COMMAND_FAILED:{' '.join(args)}:{proc.stderr.strip()[:300]}"
        )
    return proc.stdout.strip()


def load_qualification_contract(
    path: Path = QUALIFICATION_CONTRACT,
) -> dict[str, Any]:
    contract = load_json(path)
    if contract.get("schema_version") != "paper2-eligibility-runtime-qualification-v1":
        raise QualificationError("QUALIFICATION_CONTRACT_SCHEMA_MISMATCH")
    if contract.get("owner_issue") != 218:
        raise QualificationError("QUALIFICATION_OWNER_DRIFT")
    if contract.get("parent_runner_issue") != 216:
        raise QualificationError("QUALIFICATION_RUNNER_OWNER_DRIFT")
    if contract.get("parent_adjudication_issue") != 214:
        raise QualificationError("QUALIFICATION_ADJUDICATION_OWNER_DRIFT")
    if contract.get("fixture_order") != [
        "Q1_ROUTE_A_INCLUDE",
        "Q2_ROUTE_B_INCLUDE",
        "Q3_TASK_ONLY_EXCLUDE",
        "Q4_PURE_FORMALISM_EXCLUDE",
    ]:
        raise QualificationError("QUALIFICATION_FIXTURE_ORDER_DRIFT")
    execution = contract.get("execution", {})
    expected_execution = {
        "fixture_order_fixed": True,
        "stop_on_first_failure": True,
        "automatic_retry_count": 0,
        "output_root_must_not_preexist": True,
        "pass_a_per_fixture": 1,
        "pass_b_per_fixture": 1,
        "adjudication_max_per_fixture": 1,
        "adjudication_only_on_disagreement": True,
        "minimum_total_model_calls": 8,
        "maximum_total_model_calls": 12,
        "later_fixture_after_failure": False,
    }
    if execution != expected_execution:
        raise QualificationError("QUALIFICATION_EXECUTION_CONTRACT_DRIFT")
    if contract.get("synthetic_runtime_qualification_authorized") is not True:
        raise QualificationError("SYNTHETIC_QUALIFICATION_NOT_AUTHORIZED")
    if contract.get("real_ranked_work_screening_authorized") is not False:
        raise QualificationError("RANKED_WORK_MUST_REMAIN_UNAUTHORIZED")
    if contract.get("model_facing_ranked_work_allowed") is not False:
        raise QualificationError("RANKED_WORK_MODEL_FACING_DRIFT")
    if contract.get("top50_source_text_allowed") is not False:
        raise QualificationError("TOP50_SOURCE_TEXT_MUST_REMAIN_FORBIDDEN")
    for field in (
        "claim_ir_authorized",
        "decomposition_authorized",
        "null_execution_authorized",
    ):
        if contract.get(field) is not False:
            raise QualificationError(f"DOWNSTREAM_AUTHORITY_DRIFT:{field}")
    if contract.get("architecture_consequence") != "NONE":
        raise QualificationError("ARCHITECTURE_CONSEQUENCE_DRIFT")

    fixtures = contract.get("fixtures")
    if not isinstance(fixtures, dict):
        raise QualificationError("QUALIFICATION_FIXTURE_MAP_MISSING")
    for fixture_id in contract["fixture_order"]:
        info = fixtures.get(fixture_id)
        if not isinstance(info, dict):
            raise QualificationError(f"QUALIFICATION_FIXTURE_MISSING:{fixture_id}")
        fixture_path = Path(info["path"])
        if not fixture_path.is_file():
            raise QualificationError(f"QUALIFICATION_FIXTURE_FILE_MISSING:{fixture_id}")
        observed = sha256_file(fixture_path)
        if observed != info["sha256_utf8"]:
            raise QualificationError(
                f"QUALIFICATION_FIXTURE_DIGEST_MISMATCH:{fixture_id}:{observed}"
            )
        bundle = load_json(fixture_path)
        validate_source_bundle(bundle)
    return contract


def validate_runtime_manifest(
    manifest: dict[str, Any],
    *,
    config_path: Path,
    contract: dict[str, Any],
) -> dict[str, Any]:
    expected_fields = {
        "schema_version",
        "captured_at",
        "repo_head",
        "repo_tree",
        "llama_cpp_revision",
        "llama_cpp_build",
        "server_base_url",
        "model_id",
        "gguf_path",
        "gguf_sha256",
        "gpu_identity",
        "runner_config_sha256",
    }
    if set(manifest) != expected_fields:
        raise QualificationError("RUNTIME_MANIFEST_FIELD_SET_INVALID")
    if manifest.get("schema_version") != RUNTIME_MANIFEST_SCHEMA:
        raise QualificationError("RUNTIME_MANIFEST_SCHEMA_MISMATCH")

    for field in (
        "captured_at",
        "llama_cpp_revision",
        "llama_cpp_build",
        "server_base_url",
        "model_id",
        "gguf_path",
        "gpu_identity",
    ):
        if not isinstance(manifest.get(field), str) or not manifest[field].strip():
            raise QualificationError(f"RUNTIME_MANIFEST_STRING_INVALID:{field}")

    for field in ("repo_head", "repo_tree"):
        value = manifest.get(field)
        if not isinstance(value, str) or len(value) != 40:
            raise QualificationError(f"RUNTIME_MANIFEST_GIT_ID_INVALID:{field}")
    for field in ("gguf_sha256", "runner_config_sha256"):
        value = manifest.get(field)
        if not isinstance(value, str) or len(value) != 64:
            raise QualificationError(f"RUNTIME_MANIFEST_SHA256_INVALID:{field}")

    actual_head = git_text("rev-parse", "HEAD")
    actual_tree = git_text("rev-parse", "HEAD^{tree}")
    if manifest["repo_head"] != actual_head:
        raise QualificationError(
            f"RUNTIME_REPO_HEAD_MISMATCH:{manifest['repo_head']}!={actual_head}"
        )
    if manifest["repo_tree"] != actual_tree:
        raise QualificationError(
            f"RUNTIME_REPO_TREE_MISMATCH:{manifest['repo_tree']}!={actual_tree}"
        )

    required_ancestor = contract["required_runner_merge_head"]
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", required_ancestor, actual_head],
        check=False,
        capture_output=True,
        text=True,
    )
    if ancestor.returncode != 0:
        raise QualificationError(
            f"REQUIRED_RUNNER_AUTHORITY_NOT_ANCESTOR:{required_ancestor}"
        )

    config = load_json(config_path)
    runner.validate_config(config)
    config_sha = sha256_file(config_path)
    if manifest["runner_config_sha256"] != config_sha:
        raise QualificationError(
            f"RUNNER_CONFIG_RAW_SHA256_MISMATCH:{manifest['runner_config_sha256']}!={config_sha}"
        )
    if config["base_url"].rstrip("/") != manifest["server_base_url"].rstrip("/"):
        raise QualificationError("RUNNER_CONFIG_BASE_URL_RUNTIME_MISMATCH")
    if config["model"] != manifest["model_id"]:
        raise QualificationError("RUNNER_CONFIG_MODEL_RUNTIME_MISMATCH")
    if config["classifier_identity"] != "local-llama-cpp":
        raise QualificationError("QUALIFICATION_CLASSIFIER_IDENTITY_NOT_LOCAL_LLAMA_CPP")

    gguf = Path(manifest["gguf_path"]).expanduser()
    if not gguf.is_file():
        raise QualificationError(f"QUALIFICATION_GGUF_NOT_FOUND:{gguf}")
    observed_gguf_sha = sha256_file(gguf)
    if observed_gguf_sha != manifest["gguf_sha256"]:
        raise QualificationError(
            f"QUALIFICATION_GGUF_SHA256_MISMATCH:{observed_gguf_sha}"
        )

    return {
        "repo_head": actual_head,
        "repo_tree": actual_tree,
        "runner_config_sha256": config_sha,
        "gguf_sha256": observed_gguf_sha,
    }


def synthetic_binding(fixture_id: str, rank: int) -> dict[str, Any]:
    return {
        "provider_work_id": f"SYNTHETIC-{fixture_id}",
        "era": "SYNTHETIC_QUALIFICATION",
        "rank": rank,
        "ranked_artifact_sha256": "0" * 64,
        "source_access_version": "synthetic-runtime-qualification-v1",
        "adjudication_version": "paper2-eligibility-adjudication-v1",
    }


def count_submitted(receipt: dict[str, Any]) -> int:
    requests = receipt.get("requests", {})
    total = 0
    for pass_id in ("A", "B", "ADJUDICATION"):
        state = requests.get(pass_id, {})
        if state.get("submitted") is True:
            total += 1
    return total


def validate_fixture_output(
    *,
    fixture_id: str,
    output_dir: Path,
    expected: dict[str, Any],
) -> dict[str, Any]:
    receipt_path = output_dir / "receipt.json"
    assembled_path = output_dir / "assembled-record.json"
    agreement_path = output_dir / "agreement.json"
    for path in (receipt_path, assembled_path, agreement_path):
        if not path.is_file():
            raise QualificationError(
                f"QUALIFICATION_REQUIRED_OUTPUT_MISSING:{fixture_id}:{path.name}"
            )
    receipt = load_json(receipt_path)
    assembled = load_json(assembled_path)
    agreement = load_json(agreement_path)

    if receipt.get("status") != "ELIGIBILITY_RECORD_FROZEN":
        raise QualificationError(
            f"QUALIFICATION_RUNNER_STATUS_INVALID:{fixture_id}:{receipt.get('status')}"
        )
    requests = receipt.get("requests", {})
    for pass_id in ("A", "B"):
        state = requests.get(pass_id, {})
        if state.get("submitted") is not True:
            raise QualificationError(
                f"QUALIFICATION_REQUIRED_PASS_NOT_SUBMITTED:{fixture_id}:{pass_id}"
            )
        if not state.get("request_sha256") or not state.get("response_sha256"):
            raise QualificationError(
                f"QUALIFICATION_PASS_DIGEST_MISSING:{fixture_id}:{pass_id}"
            )

    adj_required = bool(agreement.get("adjudication_required"))
    adj_state = requests.get("ADJUDICATION", {})
    if adj_state.get("required") is not adj_required:
        raise QualificationError(
            f"QUALIFICATION_ADJUDICATION_REQUIREMENT_MISMATCH:{fixture_id}"
        )
    if bool(adj_state.get("submitted")) != adj_required:
        raise QualificationError(
            f"QUALIFICATION_ADJUDICATION_SUBMISSION_MISMATCH:{fixture_id}"
        )
    if adj_required and (
        not adj_state.get("request_sha256") or not adj_state.get("response_sha256")
    ):
        raise QualificationError(
            f"QUALIFICATION_ADJUDICATION_DIGEST_MISSING:{fixture_id}"
        )

    state = assembled.get("decision", {}).get("state")
    if state != expected["expected_state"]:
        raise QualificationError(
            f"QUALIFICATION_EXPECTED_STATE_MISMATCH:{fixture_id}:{state}"
        )

    required_route = expected.get("required_route")
    if required_route is not None:
        claims = assembled.get("claims")
        if not isinstance(claims, list) or not any(
            claim.get("route") == required_route
            and claim.get("generalization") == "YES"
            and claim.get("construct_level_relevance") == "YES"
            and isinstance(claim.get("operational_roles"), list)
            and len(claim["operational_roles"]) >= 1
            for claim in claims
            if isinstance(claim, dict)
        ):
            raise QualificationError(
                f"QUALIFICATION_REQUIRED_ROUTE_MISSING:{fixture_id}:{required_route}"
            )

    required_check = expected.get("required_exclusion_check")
    if required_check is not None:
        checks = assembled.get("exclusion_checks")
        if not isinstance(checks, dict) or checks.get(required_check) is not True:
            raise QualificationError(
                f"QUALIFICATION_REQUIRED_EXCLUSION_CHECK_MISSING:{fixture_id}:{required_check}"
            )

    return {
        "fixture_id": fixture_id,
        "decision_state": state,
        "agreement": bool(agreement.get("agreement")),
        "adjudication_required": adj_required,
        "submitted_model_calls": count_submitted(receipt),
        "assembled_record_sha256": sha256_file(assembled_path),
        "receipt_sha256": sha256_file(receipt_path),
    }


def initial_campaign_receipt(
    *,
    contract: dict[str, Any],
    runtime_manifest: dict[str, Any],
    runtime_manifest_sha256: str,
    config_sha256: str,
) -> dict[str, Any]:
    return {
        "schema_version": "paper2-eligibility-runtime-qualification-receipt-v1",
        "owner_issue": 218,
        "status": "QUALIFICATION_STARTED",
        "classification": None,
        "required_runner_merge_head": contract["required_runner_merge_head"],
        "repo_head": runtime_manifest["repo_head"],
        "repo_tree": runtime_manifest["repo_tree"],
        "runtime_manifest_sha256": runtime_manifest_sha256,
        "runner_config_sha256": config_sha256,
        "fixture_order": list(contract["fixture_order"]),
        "completed_fixtures": [],
        "fixture_results": [],
        "submitted_model_calls": 0,
        "failure": None,
    }


def execute_campaign(
    *,
    contract_path: Path,
    config_path: Path,
    runtime_manifest_path: Path,
    output_root: Path,
) -> Path:
    contract = load_qualification_contract(contract_path)
    if output_root.exists():
        raise QualificationError(f"QUALIFICATION_OUTPUT_ROOT_ALREADY_EXISTS:{output_root}")

    runtime_manifest = load_json(runtime_manifest_path)
    identity = validate_runtime_manifest(
        runtime_manifest,
        config_path=config_path,
        contract=contract,
    )

    output_root.mkdir(parents=True)
    atomic_write(
        output_root / "qualification-contract.json",
        canonical_json_bytes(contract),
    )
    atomic_write(
        output_root / "runtime-manifest.json",
        canonical_json_bytes(runtime_manifest),
    )
    atomic_write(
        output_root / "runner-config.json",
        config_path.read_bytes(),
    )

    receipt_path = output_root / "qualification-receipt.json"
    receipt = initial_campaign_receipt(
        contract=contract,
        runtime_manifest=runtime_manifest,
        runtime_manifest_sha256=sha256_file(runtime_manifest_path),
        config_sha256=identity["runner_config_sha256"],
    )
    atomic_write(receipt_path, canonical_json_bytes(receipt))

    try:
        for index, fixture_id in enumerate(contract["fixture_order"], start=1):
            info = contract["fixtures"][fixture_id]
            fixture_path = Path(info["path"])
            if sha256_file(fixture_path) != info["sha256_utf8"]:
                raise QualificationError(
                    f"QUALIFICATION_FIXTURE_CHANGED_BEFORE_EXECUTION:{fixture_id}"
                )

            binding = synthetic_binding(fixture_id, index)
            binding_path = output_root / "inputs" / f"{fixture_id}.binding.json"
            atomic_write(binding_path, canonical_json_bytes(binding))
            fixture_output = output_root / "fixtures" / fixture_id

            try:
                runner.execute(
                    contract_path=runner.RUNNER_CONTRACT,
                    procedure_path=RUNNER_PROCEDURE,
                    config_path=config_path,
                    source_bundle_path=fixture_path,
                    binding_path=binding_path,
                    output_dir=fixture_output,
                    allow_real=True,
                )
                result = validate_fixture_output(
                    fixture_id=fixture_id,
                    output_dir=fixture_output,
                    expected=info,
                )
            except QualificationError:
                raise
            except Exception as exc:
                raise runner.RunnerError(
                    f"QUALIFICATION_FIXTURE_RUNNER_FAILURE:{fixture_id}:{type(exc).__name__}:{exc}"
                ) from exc

            receipt["completed_fixtures"].append(fixture_id)
            receipt["fixture_results"].append(result)
            receipt["submitted_model_calls"] += int(result["submitted_model_calls"])
            overwrite_json(receipt_path, receipt)

        total = int(receipt["submitted_model_calls"])
        minimum = int(contract["execution"]["minimum_total_model_calls"])
        maximum = int(contract["execution"]["maximum_total_model_calls"])
        if not minimum <= total <= maximum:
            raise QualificationError(
                f"QUALIFICATION_TOTAL_CALL_BUDGET_INVALID:{total}:{minimum}-{maximum}"
            )
        if receipt["completed_fixtures"] != contract["fixture_order"]:
            raise QualificationError("QUALIFICATION_FIXTURE_COMPLETION_ORDER_INVALID")

        receipt["status"] = "QUALIFICATION_TERMINAL"
        receipt["classification"] = "PAPER2_ELIGIBILITY_RUNNER_QUALIFIED"
        overwrite_json(receipt_path, receipt)
        return receipt_path

    except QualificationError as exc:
        receipt["status"] = "QUALIFICATION_TERMINAL"
        receipt["classification"] = "PAPER2_ELIGIBILITY_RUNNER_QUALIFICATION_BLOCKED"
        receipt["failure"] = f"{type(exc).__name__}:{exc}"
        overwrite_json(receipt_path, receipt)
        raise
    except runner.RunnerError as exc:
        receipt["status"] = "QUALIFICATION_TERMINAL"
        receipt["classification"] = "PAPER2_ELIGIBILITY_RUNNER_RUNTIME_FAILED"
        receipt["failure"] = f"{type(exc).__name__}:{exc}"
        # Count submitted requests from a partially written failing fixture if present.
        current = contract["fixture_order"][len(receipt["completed_fixtures"])]
        partial_receipt = output_root / "fixtures" / current / "receipt.json"
        if partial_receipt.is_file():
            receipt["submitted_model_calls"] += count_submitted(load_json(partial_receipt))
        overwrite_json(receipt_path, receipt)
        raise


def fake_assembled_for(fixture_id: str, expected: dict[str, Any]) -> dict[str, Any]:
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
    if expected["expected_state"] == "INCLUDE":
        claims = [
            {
                "claim_id": "elig-001",
                "source_locator": "s1",
                "route": expected["required_route"],
                "generalization": "YES",
                "operational_roles": ["CONTEXT"],
                "construct_level_relevance": "YES",
            }
        ]
    else:
        checks[expected["required_exclusion_check"]] = True
    return {
        "claims": claims,
        "exclusion_checks": checks,
        "decision": {
            "state": expected["expected_state"],
            "reason_codes": [],
        },
    }


def self_test() -> None:
    import tempfile

    contract = load_qualification_contract()
    runner_contract = load_json(runner.RUNNER_CONTRACT)
    runner.validate_runner_contract(runner_contract)
    assert runner_contract["real_execution_authorized"] is False
    assert contract["synthetic_runtime_qualification_authorized"] is True
    assert contract["real_ranked_work_screening_authorized"] is False

    for fixture_id in contract["fixture_order"]:
        info = contract["fixtures"][fixture_id]
        path = Path(info["path"])
        assert sha256_file(path) == info["sha256_utf8"]
        bundle = load_json(path)
        validate_source_bundle(bundle)

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = root / fixture_id
            out.mkdir()
            receipt = {
                "status": "ELIGIBILITY_RECORD_FROZEN",
                "requests": {
                    "A": {
                        "submitted": True,
                        "request_sha256": "a" * 64,
                        "response_sha256": "b" * 64,
                    },
                    "B": {
                        "submitted": True,
                        "request_sha256": "c" * 64,
                        "response_sha256": "d" * 64,
                    },
                    "ADJUDICATION": {
                        "required": False,
                        "submitted": False,
                        "request_sha256": None,
                        "response_sha256": None,
                    },
                },
            }
            assembled = fake_assembled_for(fixture_id, info)
            agreement = {
                "agreement": True,
                "adjudication_required": False,
            }
            atomic_write(out / "receipt.json", canonical_json_bytes(receipt))
            atomic_write(
                out / "assembled-record.json",
                canonical_json_bytes(assembled),
            )
            atomic_write(out / "agreement.json", canonical_json_bytes(agreement))
            result = validate_fixture_output(
                fixture_id=fixture_id,
                output_dir=out,
                expected=info,
            )
            assert result["submitted_model_calls"] == 2
            assert result["decision_state"] == info["expected_state"]

    assert contract["execution"]["minimum_total_model_calls"] == 8
    assert contract["execution"]["maximum_total_model_calls"] == 12
    assert sum(
        2 for _ in contract["fixture_order"]
    ) == contract["execution"]["minimum_total_model_calls"]
    print("PAPER2_ELIGIBILITY_RUNTIME_QUALIFICATION_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--contract",
        type=Path,
        default=QUALIFICATION_CONTRACT,
    )
    parser.add_argument("--config", type=Path)
    parser.add_argument("--runtime-manifest", type=Path)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    if args.config is None or args.runtime_manifest is None or args.output_root is None:
        raise SystemExit(
            "--config, --runtime-manifest, and --output-root are required"
        )

    try:
        receipt = execute_campaign(
            contract_path=args.contract,
            config_path=args.config,
            runtime_manifest_path=args.runtime_manifest,
            output_root=args.output_root,
        )
    except (QualificationError, runner.RunnerError) as exc:
        raise SystemExit(str(exc)) from exc

    print(
        json.dumps(
            {
                "classification": "PAPER2_ELIGIBILITY_RUNNER_QUALIFIED",
                "receipt": str(receipt),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
