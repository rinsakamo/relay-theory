#!/usr/bin/env python3
"""Qualify a two-pass Normal -> SystemOne -> ClaimIR compiler on synthetic data.

Owner: #160.

This module does not execute real paper extraction. It separates:
1. a free semantic interpretation string;
2. one bounded SystemOne-style choice request;
3. a finite decision record;
4. deterministic compilation into the existing extraction candidate v1.

The original blinded source bundle remains present in the SystemOne state.
The normal-pass interpretation is advisory and is never copied directly into
ClaimIR fields. All candidate prose is host-derived from source spans or fixed
templates.

Architecture consequence: NONE.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from paper2_extraction_bundle_prepare import canonical_json_bytes, normalize_text
from paper2_extraction_procedure_validate import (
    CLAIM_TYPES,
    GROUNDING,
    MODALITIES,
    RELATIONS,
    ROLES,
    ContractError,
    validate_candidate,
    validate_source,
)


MANIFEST_VERSION = "paper2-two-pass-systemone-v1"
DECISION_VERSION = "paper2-systemone-decision-v1"
MAX_SPANS = 3
MAX_SYSTEMONE_QUESTIONS = 64
NODE_SLOTS = ("n1", "n2", "n3")
RELATION_SLOTS = ("r1", "r2")
SCOPE_FIELDS = ("conditions", "population", "substrate", "task", "temporal_scope")
YES_NO = {"yes": "selected", "no": "not selected"}
ARG_OPTIONS = {"none": "no second argument", **{slot: f"node {slot}" for slot in NODE_SLOTS}}
AUTHORITY_TOKENS = {
    "author", "authors", "institution", "institutions", "venue",
    "citation_count", "citations", "paper_id", "title", "construct_labels",
}
RESULT_TOKENS = {
    "basis", "basis_mapping", "basis_witness", "decomposition_success",
    "decomposition_failure", "coverage", "coverage_score", "residual",
    "residual_type", "acceptance_verdict",
}


class TwoPassError(ValueError):
    pass


def fail(message: str) -> None:
    raise TwoPassError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_digest(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


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


def validate_manifest(manifest: Any) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        fail("manifest: expected object")
    if manifest.get("schema_version") != MANIFEST_VERSION:
        fail("manifest.schema_version")
    if manifest.get("owner_issue") != 160:
        fail("manifest.owner_issue")
    if manifest.get("status") != "SYNTHETIC_QUALIFICATION_ONLY":
        fail("manifest.status")
    bounded = manifest.get("bounded_surface")
    if not isinstance(bounded, dict):
        fail("manifest.bounded_surface")
    if bounded.get("max_source_spans") != MAX_SPANS:
        fail("manifest.bounded_surface.max_source_spans")
    if bounded.get("max_nodes") != len(NODE_SLOTS):
        fail("manifest.bounded_surface.max_nodes")
    if bounded.get("max_relations") != len(RELATION_SLOTS):
        fail("manifest.bounded_surface.max_relations")
    systemone = manifest.get("systemone_pass")
    if not isinstance(systemone, dict):
        fail("manifest.systemone_pass")
    if systemone.get("max_questions") != MAX_SYSTEMONE_QUESTIONS:
        fail("manifest.systemone_pass.max_questions")

    limitations = manifest.get("known_limitations")
    if not isinstance(limitations, dict):
        fail("manifest.known_limitations")
    for key in (
        "semantic_entailment_mechanically_verified",
        "construct_label_suppression_for_real_sources_qualified",
        "real_pilot_authorized",
        "systemone_probability_calibration_claimed",
    ):
        if limitations.get(key) is not False:
            fail(f"manifest.known_limitations.{key}")

    scope = manifest.get("qualification_scope")
    if not isinstance(scope, dict):
        fail("manifest.qualification_scope")
    for key in (
        "synthetic_sources_only",
        "real_paper_text_forbidden",
        "consumed_147_sample_forbidden",
        "real_model_calls_forbidden",
        "basis_decomposition_forbidden",
        "corpus_claims_forbidden",
    ):
        if scope.get(key) is not True:
            fail(f"manifest.qualification_scope.{key}")
    return manifest


def source_span_map(source: dict[str, Any]) -> dict[str, str]:
    validate_source(source)
    spans = source["source_spans"]
    if len(spans) > MAX_SPANS:
        fail(f"source has {len(spans)} spans; v1 synthetic bound is {MAX_SPANS}")
    return {item["span_id"]: normalize_text(item["text"]) for item in spans}


def _choice(criteria: dict[str, str], instructions: str) -> dict[str, Any]:
    return {
        "type": "choice",
        "instructions": instructions,
        "criteria": criteria,
    }


def build_questions(source: dict[str, Any]) -> dict[str, Any]:
    spans = source_span_map(source)
    span_criteria = {sid: f"source span {sid}" for sid in spans}
    questions: dict[str, Any] = {
        "claim_type": _choice(
            {value: value for value in sorted(CLAIM_TYPES)},
            "Choose the narrowest ClaimIR claim_type supported by the source.",
        ),
        "modality": _choice(
            {value: value for value in sorted(MODALITIES)},
            "Choose the least committal ClaimIR modality supported by the source.",
        ),
    }

    for field in SCOPE_FIELDS:
        for sid in spans:
            questions[f"scope__{field}__{sid}"] = _choice(
                YES_NO,
                f"Should {sid} contribute literally to scope.{field}?",
            )

    for slot in NODE_SLOTS:
        questions[f"{slot}__active"] = _choice(
            YES_NO,
            f"Is structural node slot {slot} required by the source claim?",
        )
        questions[f"{slot}__role"] = _choice(
            {value: value for value in sorted(ROLES)},
            f"Choose the ClaimIR role for {slot} if active.",
        )
        questions[f"{slot}__grounding"] = _choice(
            {value: value for value in sorted(GROUNDING)},
            f"Choose grounding for {slot} if active.",
        )
        for sid in spans:
            questions[f"{slot}__span__{sid}"] = _choice(
                YES_NO,
                f"Does source span {sid} ground {slot}?",
            )

    for slot in RELATION_SLOTS:
        questions[f"{slot}__active"] = _choice(
            YES_NO,
            f"Is relation slot {slot} required by the source claim?",
        )
        questions[f"{slot}__kind"] = _choice(
            {value: value for value in sorted(RELATIONS)},
            f"Choose the ClaimIR relation kind for {slot} if active.",
        )
        questions[f"{slot}__arg1"] = _choice(
            {node: f"first argument {node}" for node in NODE_SLOTS},
            f"Choose the first node argument for {slot} if active.",
        )
        questions[f"{slot}__arg2"] = _choice(
            ARG_OPTIONS,
            f"Choose the optional second node argument for {slot}.",
        )
        questions[f"{slot}__grounding"] = _choice(
            {value: value for value in sorted(GROUNDING)},
            f"Choose grounding for {slot} if active.",
        )
        for sid in spans:
            questions[f"{slot}__span__{sid}"] = _choice(
                YES_NO,
                f"Does source span {sid} ground {slot}?",
            )
    if len(questions) > MAX_SYSTEMONE_QUESTIONS:
        fail(
            f"SystemOne question count {len(questions)} exceeds "
            f"frozen maximum {MAX_SYSTEMONE_QUESTIONS}"
        )
    return questions


def build_systemone_request(
    source: dict[str, Any],
    interpretation: str,
    model: str,
) -> dict[str, Any]:
    validate_source(source)
    if not isinstance(interpretation, str) or not interpretation.strip():
        fail("normal interpretation must be non-empty text")
    if not isinstance(model, str) or not model.strip():
        fail("SystemOne model must be non-empty")
    return {
        "state": {
            "source": source,
            "interpretation": interpretation,
            "authority_rule": (
                "The original source is authoritative. The interpretation is advisory. "
                "Do not choose structure unsupported by cited source spans."
            ),
        },
        "model": model,
        "questions": build_questions(source),
    }


def _answer_choice(answer: Any, question: dict[str, Any], name: str) -> str:
    if not isinstance(answer, dict):
        fail(f"answer {name}: expected object")
    choice = answer.get("choice")
    if not isinstance(choice, str):
        fail(f"answer {name}: missing choice")
    criteria = question.get("criteria")
    if not isinstance(criteria, dict) or choice not in criteria:
        fail(f"answer {name}: choice outside frozen criteria: {choice!r}")
    return choice


def parse_systemone_response(
    request_payload: dict[str, Any],
    response_payload: Any,
) -> dict[str, Any]:
    if not isinstance(response_payload, dict):
        fail("SystemOne response: expected object")
    answers = response_payload.get("answers")
    if not isinstance(answers, dict):
        fail("SystemOne response.answers: expected object")
    questions = request_payload["questions"]
    if set(answers) != set(questions):
        fail(
            "SystemOne answers must match frozen question set exactly "
            f"missing={sorted(set(questions)-set(answers))} "
            f"extra={sorted(set(answers)-set(questions))}"
        )
    return {
        name: _answer_choice(answers[name], question, name)
        for name, question in questions.items()
    }


def decision_from_answers(
    source: dict[str, Any],
    answers: dict[str, str],
) -> dict[str, Any]:
    spans = source_span_map(source)
    span_ids = tuple(spans)

    scope: dict[str, list[str]] = {}
    for field in SCOPE_FIELDS:
        scope[field] = [
            sid for sid in span_ids
            if answers[f"scope__{field}__{sid}"] == "yes"
        ]

    nodes: list[dict[str, Any]] = []
    active_nodes: set[str] = set()
    for slot in NODE_SLOTS:
        if answers[f"{slot}__active"] != "yes":
            continue
        refs = [
            sid for sid in span_ids
            if answers[f"{slot}__span__{sid}"] == "yes"
        ]
        if not refs:
            fail(f"{slot}: active node requires at least one source span")
        active_nodes.add(slot)
        nodes.append({
            "slot": slot,
            "role": answers[f"{slot}__role"],
            "source_span_ids": refs,
            "grounding": answers[f"{slot}__grounding"],
        })

    if not nodes:
        fail("at least one node must be active")

    relations: list[dict[str, Any]] = []
    for slot in RELATION_SLOTS:
        if answers[f"{slot}__active"] != "yes":
            continue
        arg1 = answers[f"{slot}__arg1"]
        arg2 = answers[f"{slot}__arg2"]
        args = [arg1] + ([] if arg2 == "none" else [arg2])
        if any(arg not in active_nodes for arg in args):
            fail(f"{slot}: relation argument names inactive node")
        refs = [
            sid for sid in span_ids
            if answers[f"{slot}__span__{sid}"] == "yes"
        ]
        if not refs:
            fail(f"{slot}: active relation requires at least one source span")
        relations.append({
            "slot": slot,
            "kind": answers[f"{slot}__kind"],
            "arguments": args,
            "source_span_ids": refs,
            "grounding": answers[f"{slot}__grounding"],
        })

    decision = {
        "schema_version": DECISION_VERSION,
        "bundle_id": source["bundle_id"],
        "claim_type": answers["claim_type"],
        "modality": answers["modality"],
        "scope": scope,
        "nodes": nodes,
        "relations": relations,
    }
    validate_decision(decision, source)
    return decision


def validate_decision(decision: Any, source: dict[str, Any]) -> dict[str, Any]:
    root = expect_exact_keys(
        decision,
        {"schema_version", "bundle_id", "claim_type", "modality", "scope", "nodes", "relations"},
        "decision",
    )
    if root["schema_version"] != DECISION_VERSION:
        fail("decision.schema_version")
    if root["bundle_id"] != source["bundle_id"]:
        fail("decision.bundle_id")
    if root["claim_type"] not in CLAIM_TYPES:
        fail("decision.claim_type")
    if root["modality"] not in MODALITIES:
        fail("decision.modality")

    spans = source_span_map(source)
    scope = expect_exact_keys(root["scope"], set(SCOPE_FIELDS), "decision.scope")
    for field in SCOPE_FIELDS:
        refs = scope[field]
        if not isinstance(refs, list) or len(refs) != len(set(refs)):
            fail(f"decision.scope.{field}: unique array required")
        if any(ref not in spans for ref in refs):
            fail(f"decision.scope.{field}: unknown source span")

    nodes = root["nodes"]
    if not isinstance(nodes, list) or not 1 <= len(nodes) <= len(NODE_SLOTS):
        fail("decision.nodes")
    seen_nodes: set[str] = set()
    for index, node in enumerate(nodes):
        item = expect_exact_keys(
            node, {"slot", "role", "source_span_ids", "grounding"},
            f"decision.nodes[{index}]",
        )
        slot = item["slot"]
        if slot not in NODE_SLOTS or slot in seen_nodes:
            fail(f"decision.nodes[{index}].slot")
        seen_nodes.add(slot)
        if item["role"] not in ROLES:
            fail(f"decision.nodes[{index}].role")
        if item["grounding"] not in GROUNDING:
            fail(f"decision.nodes[{index}].grounding")
        refs = item["source_span_ids"]
        if not isinstance(refs, list) or not refs or len(refs) != len(set(refs)):
            fail(f"decision.nodes[{index}].source_span_ids")
        if any(ref not in spans for ref in refs):
            fail(f"decision.nodes[{index}].source_span_ids: unknown source span")

    relations = root["relations"]
    if not isinstance(relations, list) or len(relations) > len(RELATION_SLOTS):
        fail("decision.relations")
    seen_relations: set[str] = set()
    for index, relation in enumerate(relations):
        item = expect_exact_keys(
            relation, {"slot", "kind", "arguments", "source_span_ids", "grounding"},
            f"decision.relations[{index}]",
        )
        slot = item["slot"]
        if slot not in RELATION_SLOTS or slot in seen_relations:
            fail(f"decision.relations[{index}].slot")
        seen_relations.add(slot)
        if item["kind"] not in RELATIONS:
            fail(f"decision.relations[{index}].kind")
        if item["grounding"] not in GROUNDING:
            fail(f"decision.relations[{index}].grounding")
        args = item["arguments"]
        if not isinstance(args, list) or not 1 <= len(args) <= 2:
            fail(f"decision.relations[{index}].arguments")
        if any(arg not in seen_nodes for arg in args):
            fail(f"decision.relations[{index}].arguments: unknown node")
        refs = item["source_span_ids"]
        if not isinstance(refs, list) or not refs or len(refs) != len(set(refs)):
            fail(f"decision.relations[{index}].source_span_ids")
        if any(ref not in spans for ref in refs):
            fail(f"decision.relations[{index}].source_span_ids: unknown source span")
    return root


def _joined_source_text(refs: list[str], spans: dict[str, str]) -> str:
    return " | ".join(spans[ref] for ref in refs)


def compile_candidate(
    source: dict[str, Any],
    decision: dict[str, Any],
) -> dict[str, Any]:
    validate_decision(decision, source)
    spans = source_span_map(source)

    scope = {
        field: [spans[ref] for ref in decision["scope"][field]]
        for field in SCOPE_FIELDS
    }

    nodes = []
    for node in decision["nodes"]:
        nodes.append({
            "id": node["slot"],
            "role": node["role"],
            "description": _joined_source_text(node["source_span_ids"], spans),
            "source_span_ids": list(node["source_span_ids"]),
            "grounding": node["grounding"],
        })

    relations = []
    for relation in decision["relations"]:
        args = list(relation["arguments"])
        relation_text = (
            f"{args[0]} {relation['kind']}"
            if len(args) == 1
            else f"{args[0]} {relation['kind']} {args[1]}"
        )
        relations.append({
            "id": relation["slot"],
            "kind": relation["kind"],
            "arguments": args,
            "description": relation_text,
            "source_span_ids": list(relation["source_span_ids"]),
            "grounding": relation["grounding"],
        })

    candidate = {
        "schema_version": "paper2-extraction-candidate-v1",
        "bundle_id": source["bundle_id"],
        "claim_core": {
            "claim_type": decision["claim_type"],
            "modality": decision["modality"],
            "scope": scope,
            "nodes": nodes,
            "relations": relations,
        },
    }
    validate_candidate(candidate, source)
    return candidate


def audit_record(
    *,
    source: dict[str, Any],
    interpretation: str,
    systemone_request: dict[str, Any],
    response: dict[str, Any],
    decision: dict[str, Any],
    candidate: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "paper2-two-pass-systemone-audit-v1",
        "owner_issue": 160,
        "source_bundle_sha256": canonical_digest(source),
        "normal_interpretation_sha256": sha256_bytes(
            interpretation.encode("utf-8")
        ),
        "systemone_request_sha256": canonical_digest(systemone_request),
        "systemone_response_sha256": canonical_digest(response),
        "decision_sha256": canonical_digest(decision),
        "candidate_sha256": canonical_digest(candidate),
        "candidate_validation": "PASS",
        "probabilities_are_audit_metadata_only": True,
        "real_model_call": False,
        "basis_decomposition": False,
    }


def post_systemone(
    endpoint: str,
    payload: dict[str, Any],
    timeout_seconds: int = 10,
) -> dict[str, Any]:
    request = Request(
        endpoint,
        data=canonical_json_bytes(payload),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read()
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise TwoPassError(f"SystemOne HTTP {exc.code}: {detail[:500]}") from exc
    except URLError as exc:
        raise TwoPassError(f"SystemOne request failed: {exc}") from exc
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TwoPassError("SystemOne response is not valid JSON") from exc
    if not isinstance(value, dict):
        fail("SystemOne response must be object")
    return value


def synthetic_source(text: str, *, bundle_id: str = "B9001") -> dict[str, Any]:
    return {
        "schema_version": "paper2-extraction-source-bundle-v1",
        "bundle_id": bundle_id,
        "source_language": "en",
        "source_spans": [{"span_id": "s1", "text": text}],
    }


def base_answers(source: dict[str, Any]) -> dict[str, str]:
    request = build_systemone_request(
        source,
        "Synthetic semantic interpretation.",
        "synthetic-systemone",
    )
    answers: dict[str, str] = {}
    for name, question in request["questions"].items():
        criteria = question["criteria"]
        answers[name] = next(iter(criteria))
    answers["claim_type"] = "relation"
    answers["modality"] = "descriptive"
    for field in SCOPE_FIELDS:
        for sid in source_span_map(source):
            answers[f"scope__{field}__{sid}"] = "no"
    for slot in NODE_SLOTS:
        answers[f"{slot}__active"] = "no"
        answers[f"{slot}__role"] = "other"
        answers[f"{slot}__grounding"] = "explicit"
        for sid in source_span_map(source):
            answers[f"{slot}__span__{sid}"] = "no"
    for slot in RELATION_SLOTS:
        answers[f"{slot}__active"] = "no"
        answers[f"{slot}__kind"] = "other"
        answers[f"{slot}__arg1"] = "n1"
        answers[f"{slot}__arg2"] = "none"
        answers[f"{slot}__grounding"] = "explicit"
        for sid in source_span_map(source):
            answers[f"{slot}__span__{sid}"] = "no"
    return answers


def relation_answers(
    source: dict[str, Any],
    *,
    modality: str = "descriptive",
    relation_kind: str = "depends_on",
) -> dict[str, str]:
    answers = base_answers(source)
    answers["claim_type"] = "relation"
    answers["modality"] = modality
    answers["n1__active"] = "yes"
    answers["n1__role"] = "state_or_structure"
    answers["n1__span__s1"] = "yes"
    answers["n2__active"] = "yes"
    answers["n2__role"] = "response_or_outcome"
    answers["n2__span__s1"] = "yes"
    answers["r1__active"] = "yes"
    answers["r1__kind"] = relation_kind
    answers["r1__arg1"] = "n1"
    answers["r1__arg2"] = "n2"
    answers["r1__span__s1"] = "yes"
    return answers


def node_only_answers(source: dict[str, Any]) -> dict[str, str]:
    answers = base_answers(source)
    answers["claim_type"] = "other"
    answers["modality"] = "descriptive"
    answers["n1__active"] = "yes"
    answers["n1__role"] = "state_or_structure"
    answers["n1__span__s1"] = "yes"
    return answers


def response_for(
    request_payload: dict[str, Any],
    choices: dict[str, str],
) -> dict[str, Any]:
    answers = {}
    for name, question in request_payload["questions"].items():
        choice = choices[name]
        answers[name] = {
            "choice": choice,
            "probabilities": {key: (1.0 if key == choice else 0.0) for key in question["criteria"]},
            "confidence": 1.0,
        }
    return {
        "model": request_payload["model"],
        "answers": answers,
        "usage": {"input_tokens": 0, "output_tokens": 0},
    }


class MockSystemOneHandler(BaseHTTPRequestHandler):
    fixture_choices: dict[str, str] = {}
    requests_seen: list[dict[str, Any]] = []

    def log_message(self, format: str, *args: Any) -> None:
        return

    def do_POST(self) -> None:
        if self.path != "/v1/systemone":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8"))
        self.__class__.requests_seen.append(payload)
        response = response_for(payload, self.__class__.fixture_choices)
        raw = json.dumps(response, sort_keys=True).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


def expect_invalid(fn, label: str) -> None:
    try:
        fn()
    except (TwoPassError, ContractError):
        return
    raise AssertionError(f"{label}: unexpectedly valid")


def run_case(
    source: dict[str, Any],
    interpretation: str,
    choices: dict[str, str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    request_payload = build_systemone_request(
        source,
        interpretation,
        "synthetic-systemone",
    )
    response = response_for(request_payload, choices)
    answers = parse_systemone_response(request_payload, response)
    decision = decision_from_answers(source, answers)
    candidate = compile_candidate(source, decision)
    return decision, candidate, audit_record(
        source=source,
        interpretation=interpretation,
        systemone_request=request_payload,
        response=response,
        decision=decision,
        candidate=candidate,
    )


def self_test(manifest_path: Path) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate_manifest(manifest)

    # Surface bound — even the maximum admitted 3-span source stays within 64 questions.
    max_source = {
        "schema_version": "paper2-extraction-source-bundle-v1",
        "bundle_id": "B9099",
        "source_language": "en",
        "source_spans": [
            {"span_id": "s1", "text": "Synthetic span one."},
            {"span_id": "s2", "text": "Synthetic span two."},
            {"span_id": "s3", "text": "Synthetic span three."},
        ],
    }
    if len(build_questions(max_source)) != 51:
        raise AssertionError("maximum v1 question surface must be exactly 51")

    # P1 — explicit relation.
    p1 = synthetic_source("Synthetic state A depends on synthetic state B.")
    p1_decision, p1_candidate, p1_audit = run_case(
        p1,
        "A dependency is stated.",
        relation_answers(p1),
    )
    if p1_candidate["claim_core"]["relations"][0]["kind"] != "depends_on":
        raise AssertionError("P1 relation kind")
    if p1_audit["candidate_validation"] != "PASS":
        raise AssertionError("P1 audit")

    # P2 — probabilistic relation.
    p2 = synthetic_source("Signal A probabilistically predicts outcome B.", bundle_id="B9002")
    _, p2_candidate, _ = run_case(
        p2,
        "A probabilistic predictive relation is stated.",
        relation_answers(p2, modality="probabilistic", relation_kind="predicts"),
    )
    if p2_candidate["claim_core"]["modality"] != "probabilistic":
        raise AssertionError("P2 modality")

    # P3 — node-only candidate; no relation may be invented.
    p3 = synthetic_source("Synthetic state A is observed.", bundle_id="B9003")
    _, p3_candidate, _ = run_case(
        p3,
        "One state is described.",
        node_only_answers(p3),
    )
    if p3_candidate["claim_core"]["relations"]:
        raise AssertionError("P3 invented relation")

    # N1 — normal-pass hallucination cannot directly enter candidate.
    _, n1_candidate, _ = run_case(
        p3,
        "The source says A causes B and C, although that is not in the source.",
        node_only_answers(p3),
    )
    serialized_n1 = canonical_json_bytes(n1_candidate).decode("utf-8")
    if "causes B and C" in serialized_n1:
        raise AssertionError("N1 normal-pass prose leaked into candidate")
    if n1_candidate["claim_core"]["relations"]:
        raise AssertionError("N1 hallucinated relation entered candidate")

    # N2 — answer outside frozen criteria.
    n2_request = build_systemone_request(p1, "dependency", "synthetic-systemone")
    n2_response = response_for(n2_request, relation_answers(p1))
    n2_response["answers"]["modality"]["choice"] = "absolutely_certain"
    expect_invalid(
        lambda: parse_systemone_response(n2_request, n2_response),
        "N2 invalid SystemOne option",
    )

    # N3 — nonexistent source span.
    n3 = copy.deepcopy(p1_decision)
    n3["nodes"][0]["source_span_ids"] = ["s999"]
    expect_invalid(lambda: validate_decision(n3, p1), "N3 unknown span")

    # N4 — relation references inactive/unknown node.
    n4 = copy.deepcopy(p1_decision)
    n4["relations"][0]["arguments"] = ["n1", "n3"]
    expect_invalid(lambda: validate_decision(n4, p1), "N4 unknown relation arg")

    # N5 — authority/result smuggling is excluded from the candidate surface.
    n5 = copy.deepcopy(p1_decision)
    n5["basis_mapping"] = {"x": "y"}
    expect_invalid(lambda: validate_decision(n5, p1), "N5 result smuggling")
    candidate_text = canonical_json_bytes(p1_candidate).decode("utf-8")
    if any(token in candidate_text for token in AUTHORITY_TOKENS | RESULT_TOKENS):
        raise AssertionError("N5 forbidden token leaked into candidate")

    # N6 — presentation-only interpretation variation leaves candidate bytes stable.
    _, n6a, _ = run_case(p1, "A dependency is stated.", relation_answers(p1))
    _, n6b, _ = run_case(
        p1,
        "The passage describes one item as depending upon another.",
        relation_answers(p1),
    )
    if canonical_json_bytes(n6a) != canonical_json_bytes(n6b):
        raise AssertionError("N6 interpretation wording changed candidate bytes")

    # N7 — one admitted decision perturbation changes only that field.
    alt = relation_answers(p1)
    alt["modality"] = "necessary"
    _, n7b, _ = run_case(p1, "A dependency is stated.", alt)
    n7a = copy.deepcopy(n6a)
    n7a["claim_core"]["modality"] = "necessary"
    if canonical_json_bytes(n7a) != canonical_json_bytes(n7b):
        raise AssertionError("N7 modality perturbation changed extra fields")

    # Wire-path control: one real local HTTP request to a mock /v1/systemone.
    request_payload = build_systemone_request(
        p1,
        "A dependency is stated.",
        "synthetic-systemone",
    )
    MockSystemOneHandler.fixture_choices = relation_answers(p1)
    MockSystemOneHandler.requests_seen = []
    server = ThreadingHTTPServer(("127.0.0.1", 0), MockSystemOneHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        response = post_systemone(
            f"http://127.0.0.1:{port}/v1/systemone",
            request_payload,
        )
        parsed = parse_systemone_response(request_payload, response)
        decision = decision_from_answers(p1, parsed)
        candidate = compile_candidate(p1, decision)
        if candidate != p1_candidate:
            raise AssertionError("wire-path candidate mismatch")
        if len(MockSystemOneHandler.requests_seen) != 1:
            raise AssertionError("wire-path must issue exactly one SystemOne request")
        state = MockSystemOneHandler.requests_seen[0].get("state")
        if not isinstance(state, dict) or state.get("source") != p1:
            raise AssertionError("wire-path must include original source in state")
        if state.get("interpretation") != "A dependency is stated.":
            raise AssertionError("wire-path must include normal interpretation in state")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    print("PAPER2_TWO_PASS_SYSTEMONE_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("research/paper2/extraction_two_pass_systemone_v1.json"),
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        validate_manifest(manifest)
        if args.self_test:
            self_test(args.manifest)
        else:
            print("PAPER2_TWO_PASS_SYSTEMONE_V1_VALID")
        return 0
    except (
        OSError,
        json.JSONDecodeError,
        TwoPassError,
        ContractError,
        AssertionError,
    ) as exc:
        print(f"PAPER2_TWO_PASS_SYSTEMONE_V1_INVALID: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
