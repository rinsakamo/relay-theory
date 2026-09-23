#!/usr/bin/env python3
"""Harden the Paper 2 Normal -> SystemOne -> ClaimIR compiler on synthetic data.

Owner: #162.

v2 preserves the terminal #160/v1 artifacts and addresses hostile-review
findings before any real two-pass pilot:
- every SystemOne choice surface includes explicit UNRESOLVED;
- active nodes carry a finite source anchor;
- distinct relation arguments require distinct anchors;
- the Jev response parser checks the current RelaySelf-style wire contract;
- decision-schema/Python-validator parity is checked;
- compilation is validated as candidate-v1 and then as full ClaimIR v1;
- compiler prose is neutral and never copies Normal prose or source text.

No real literature or real model call is used here.
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

from paper2_claim_ir_validate import ValidationError, validate as validate_claim_ir
from paper2_extraction_bundle_prepare import canonical_json_bytes
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


MANIFEST_VERSION = "paper2-two-pass-systemone-v2"
DECISION_VERSION = "paper2-systemone-decision-v2"
UNRESOLVED = "__unresolved__"
MAX_SPANS = 3
MAX_SYSTEMONE_QUESTIONS = 64
NODE_SLOTS = ("n1", "n2", "n3")
RELATION_SLOTS = ("r1", "r2")
SCOPE_FIELDS = ("conditions", "population", "substrate", "task", "temporal_scope")
YES_NO = {"yes": "selected", "no": "not selected"}
ARG2_OPTIONS = {"none": "no second argument", **{slot: f"node {slot}" for slot in NODE_SLOTS}}

MANIFEST_TOP_KEYS = {
    "schema_version", "owner_issue", "status", "supersedes_for_future_real_use",
    "claim_ir_schema", "candidate_schema", "decision_schema", "normal_pass",
    "systemone_pass", "bounded_surface", "compiler", "qualification_scope",
    "known_limitations",
}
NORMAL_PASS_KEYS = {
    "purpose", "free_text_allowed", "claim_ir_generation_forbidden",
    "basis_visible", "decomposition_outcome_visible",
}
SYSTEMONE_PASS_KEYS = {
    "wire_endpoint", "question_type", "state_contains_original_source",
    "state_contains_normal_interpretation", "source_is_authoritative",
    "normal_interpretation_is_advisory", "free_text_claim_ir_generation_forbidden",
    "explicit_unresolved_choice", "answer_type_required",
    "response_model_if_present_must_match_request",
    "nonzero_output_tokens_forbidden_when_reported",
    "probabilities_and_confidence_are_optional_audit_metadata",
    "max_questions",
}
BOUNDED_KEYS = {
    "max_source_spans", "source_unit_policy", "max_nodes", "max_relations",
    "relation_arity", "node_anchor_policy", "relation_argument_anchor_policy",
    "scope_values", "node_descriptions", "relation_descriptions",
}
COMPILER_KEYS = {
    "deterministic", "repairs_invalid_decisions", "assigns_node_ids",
    "assigns_relation_ids", "validates_with_existing_candidate_validator",
    "validates_full_claim_ir_before_qualification",
}
QUALIFICATION_KEYS = {
    "synthetic_sources_only", "real_paper_text_forbidden",
    "real_147_source_text_forbidden_in_synthetic_qualification",
    "real_model_calls_forbidden", "basis_decomposition_forbidden",
    "corpus_claims_forbidden",
}
LIMITATION_KEYS = {
    "normal_pass_model_qualified", "semantic_entailment_mechanically_verified",
    "construct_label_suppression_for_real_sources_qualified",
    "real_pilot_authorized", "systemone_probability_calibration_claimed",
    "real_source_segmentation_frozen",
}


class TwoPassV2Error(ValueError):
    pass


class DecisionUnresolved(TwoPassV2Error):
    pass


def fail(message: str) -> None:
    raise TwoPassV2Error(message)


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


def _non_negative_int(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        fail(f"{path}: expected non-negative integer")
    return value


def _probability(value: Any, path: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        fail(f"{path}: expected numeric probability")
    number = float(value)
    if not 0.0 <= number <= 1.0:
        fail(f"{path}: probability outside [0,1]")
    return number


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_manifest(manifest: Any) -> dict[str, Any]:
    root = expect_exact_keys(manifest, MANIFEST_TOP_KEYS, "manifest")
    if root["schema_version"] != MANIFEST_VERSION:
        fail("manifest.schema_version")
    if root["owner_issue"] != 162:
        fail("manifest.owner_issue")
    if root["status"] != "SYNTHETIC_HARDENING_ONLY":
        fail("manifest.status")
    if root["supersedes_for_future_real_use"] != "paper2-two-pass-systemone-v1":
        fail("manifest.supersedes_for_future_real_use")
    if root["claim_ir_schema"] != "paper2-claim-ir-v1":
        fail("manifest.claim_ir_schema")
    if root["candidate_schema"] != "paper2-extraction-candidate-v1":
        fail("manifest.candidate_schema")
    if root["decision_schema"] != DECISION_VERSION:
        fail("manifest.decision_schema")

    normal = expect_exact_keys(root["normal_pass"], NORMAL_PASS_KEYS, "manifest.normal_pass")
    if normal != {
        "purpose": "semantic_interpretation_only",
        "free_text_allowed": True,
        "claim_ir_generation_forbidden": True,
        "basis_visible": False,
        "decomposition_outcome_visible": False,
    }:
        fail("manifest.normal_pass values")

    systemone = expect_exact_keys(
        root["systemone_pass"], SYSTEMONE_PASS_KEYS, "manifest.systemone_pass"
    )
    required_systemone = {
        "wire_endpoint": "/v1/systemone",
        "question_type": "choice",
        "state_contains_original_source": True,
        "state_contains_normal_interpretation": True,
        "source_is_authoritative": True,
        "normal_interpretation_is_advisory": True,
        "free_text_claim_ir_generation_forbidden": True,
        "explicit_unresolved_choice": UNRESOLVED,
        "answer_type_required": "choice",
        "response_model_if_present_must_match_request": True,
        "nonzero_output_tokens_forbidden_when_reported": True,
        "probabilities_and_confidence_are_optional_audit_metadata": True,
        "max_questions": MAX_SYSTEMONE_QUESTIONS,
    }
    if systemone != required_systemone:
        fail("manifest.systemone_pass values")

    bounded = expect_exact_keys(
        root["bounded_surface"], BOUNDED_KEYS, "manifest.bounded_surface"
    )
    if bounded["max_source_spans"] != MAX_SPANS:
        fail("manifest.bounded_surface.max_source_spans")
    if bounded["max_nodes"] != len(NODE_SLOTS):
        fail("manifest.bounded_surface.max_nodes")
    if bounded["max_relations"] != len(RELATION_SLOTS):
        fail("manifest.bounded_surface.max_relations")
    if bounded["source_unit_policy"] != "presegmented_atomic_evidence_units":
        fail("manifest.bounded_surface.source_unit_policy")
    if bounded["relation_arity"] != "one_or_two_unique_arguments":
        fail("manifest.bounded_surface.relation_arity")
    if bounded["node_anchor_policy"] != "exactly_one_anchor_span_in_node_grounding":
        fail("manifest.bounded_surface.node_anchor_policy")
    if bounded["relation_argument_anchor_policy"] != (
        "distinct_arguments_require_distinct_anchor_spans"
    ):
        fail("manifest.bounded_surface.relation_argument_anchor_policy")
    if bounded["scope_values"] != "deterministic_source_span_references":
        fail("manifest.bounded_surface.scope_values")
    if bounded["node_descriptions"] != "deterministic_role_and_anchor_template":
        fail("manifest.bounded_surface.node_descriptions")
    if bounded["relation_descriptions"] != "deterministic_kind_and_argument_template":
        fail("manifest.bounded_surface.relation_descriptions")

    compiler = expect_exact_keys(root["compiler"], COMPILER_KEYS, "manifest.compiler")
    if compiler != {
        "deterministic": True,
        "repairs_invalid_decisions": False,
        "assigns_node_ids": list(NODE_SLOTS),
        "assigns_relation_ids": list(RELATION_SLOTS),
        "validates_with_existing_candidate_validator": True,
        "validates_full_claim_ir_before_qualification": True,
    }:
        fail("manifest.compiler values")

    qualification = expect_exact_keys(
        root["qualification_scope"], QUALIFICATION_KEYS, "manifest.qualification_scope"
    )
    if any(qualification[key] is not True for key in QUALIFICATION_KEYS):
        fail("manifest.qualification_scope values")

    limitations = expect_exact_keys(
        root["known_limitations"], LIMITATION_KEYS, "manifest.known_limitations"
    )
    if any(limitations[key] is not False for key in LIMITATION_KEYS):
        fail("manifest.known_limitations values")
    return root


def validate_decision_schema(schema: Any) -> dict[str, Any]:
    root = expect_exact_keys(
        schema,
        {
            "$schema", "$id", "title", "description", "type",
            "additionalProperties", "required", "properties",
        },
        "decision_schema",
    )
    if root["type"] != "object" or root["additionalProperties"] is not False:
        fail("decision_schema root object contract")
    required = {
        "schema_version", "bundle_id", "claim_type", "modality",
        "scope", "nodes", "relations",
    }
    if set(root["required"]) != required:
        fail("decision_schema.required")
    props = root["properties"]
    if props["schema_version"] != {"const": DECISION_VERSION}:
        fail("decision_schema.schema_version")
    if set(props["claim_type"]["enum"]) != CLAIM_TYPES:
        fail("decision_schema.claim_type enum drift")
    if set(props["modality"]["enum"]) != MODALITIES:
        fail("decision_schema.modality enum drift")

    scope = props["scope"]
    if scope.get("additionalProperties") is not False:
        fail("decision_schema.scope additionalProperties")
    if set(scope["required"]) != set(SCOPE_FIELDS):
        fail("decision_schema.scope required drift")
    for field in SCOPE_FIELDS:
        field_schema = scope["properties"][field]
        if field_schema.get("uniqueItems") is not True:
            fail(f"decision_schema scope {field} must be unique")

    nodes_schema = props["nodes"]
    if nodes_schema.get("minItems") != 1 or nodes_schema.get("maxItems") != len(NODE_SLOTS):
        fail("decision_schema node cardinality drift")
    node = nodes_schema["items"]
    if node.get("additionalProperties") is not False:
        fail("decision_schema node additionalProperties")
    if set(node["required"]) != {
        "slot", "role", "anchor_span_id", "source_span_ids", "grounding"
    }:
        fail("decision_schema node required drift")
    if set(node["properties"]["slot"]["enum"]) != set(NODE_SLOTS):
        fail("decision_schema node slot drift")
    if set(node["properties"]["role"]["enum"]) != ROLES:
        fail("decision_schema node role drift")
    if set(node["properties"]["grounding"]["enum"]) != GROUNDING:
        fail("decision_schema node grounding drift")
    if node["properties"]["source_span_ids"].get("uniqueItems") is not True:
        fail("decision_schema node source spans must be unique")

    relations_schema = props["relations"]
    if relations_schema.get("maxItems") != len(RELATION_SLOTS):
        fail("decision_schema relation cardinality drift")
    relation = relations_schema["items"]
    if relation.get("additionalProperties") is not False:
        fail("decision_schema relation additionalProperties")
    if set(relation["properties"]["slot"]["enum"]) != set(RELATION_SLOTS):
        fail("decision_schema relation slot drift")
    if set(relation["properties"]["kind"]["enum"]) != RELATIONS:
        fail("decision_schema relation kind drift")
    args = relation["properties"]["arguments"]
    if args.get("minItems") != 1 or args.get("maxItems") != 2:
        fail("decision_schema relation arity drift")
    if args.get("uniqueItems") is not True:
        fail("decision_schema relation arguments must be unique")
    if set(args["items"]["enum"]) != set(NODE_SLOTS):
        fail("decision_schema relation argument vocabulary drift")
    if relation["properties"]["source_span_ids"].get("uniqueItems") is not True:
        fail("decision_schema relation source spans must be unique")
    return root


def source_span_map(source: dict[str, Any]) -> dict[str, str]:
    validate_source(source)
    spans = source["source_spans"]
    if len(spans) > MAX_SPANS:
        fail(f"source has {len(spans)} spans; v2 synthetic bound is {MAX_SPANS}")
    return {item["span_id"]: item["text"] for item in spans}


def _choice(criteria: dict[str, str], instructions: str) -> dict[str, Any]:
    if UNRESOLVED in criteria:
        fail("reserved unresolved choice collision")
    return {
        "type": "choice",
        "instructions": instructions,
        "criteria": {
            **criteria,
            UNRESOLVED: (
                "The supplied source and advisory interpretation are insufficient "
                "or contradictory for this decision."
            ),
        },
    }


def build_questions(source: dict[str, Any]) -> dict[str, Any]:
    spans = source_span_map(source)
    span_choices = {sid: f"source evidence unit {sid}" for sid in spans}
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
                f"Should {sid} contribute to scope.{field}?",
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
        questions[f"{slot}__anchor"] = _choice(
            span_choices,
            f"Choose the single evidence-unit anchor identifying {slot} if active.",
        )
        questions[f"{slot}__grounding"] = _choice(
            {value: value for value in sorted(GROUNDING)},
            f"Choose grounding for {slot} if active.",
        )
        for sid in spans:
            questions[f"{slot}__span__{sid}"] = _choice(
                YES_NO,
                f"Does source evidence unit {sid} ground {slot}?",
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
            ARG2_OPTIONS,
            f"Choose the optional second node argument for {slot}.",
        )
        questions[f"{slot}__grounding"] = _choice(
            {value: value for value in sorted(GROUNDING)},
            f"Choose grounding for {slot} if active.",
        )
        for sid in spans:
            questions[f"{slot}__span__{sid}"] = _choice(
                YES_NO,
                f"Does source evidence unit {sid} ground {slot}?",
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
                "Choose __unresolved__ whenever the source does not justify a decision."
            ),
        },
        "model": model,
        "questions": build_questions(source),
    }


def _answer_choice(answer: Any, question: dict[str, Any], name: str) -> str:
    if not isinstance(answer, dict):
        fail(f"answer {name}: expected object")
    if answer.get("type") != "choice":
        fail(f"answer {name}: type must be choice")
    choice = answer.get("choice")
    if not isinstance(choice, str) or not choice:
        fail(f"answer {name}: missing choice")
    criteria = question.get("criteria")
    if not isinstance(criteria, dict) or choice not in criteria:
        fail(f"answer {name}: choice outside frozen criteria: {choice!r}")

    probabilities = answer.get("probabilities")
    if probabilities is not None:
        if not isinstance(probabilities, dict):
            fail(f"answer {name}: probabilities must be object when present")
        if not set(probabilities).issubset(criteria):
            fail(f"answer {name}: probability key outside criteria")
        if choice not in probabilities:
            fail(f"answer {name}: selected choice missing from probabilities")
        for key, value in probabilities.items():
            _probability(value, f"answer {name}.probabilities.{key}")

    confidence = answer.get("confidence")
    if confidence is not None:
        _probability(confidence, f"answer {name}.confidence")
    return choice


def parse_systemone_response(
    request_payload: dict[str, Any],
    response_payload: Any,
) -> dict[str, str]:
    if not isinstance(response_payload, dict):
        fail("SystemOne response: expected object")
    response_model = response_payload.get("model")
    if response_model is not None and response_model != request_payload["model"]:
        fail("SystemOne response model does not match request model")

    usage = response_payload.get("usage")
    if usage is not None:
        if not isinstance(usage, dict):
            fail("SystemOne response.usage: expected object when present")
        if "input_tokens" in usage:
            _non_negative_int(usage["input_tokens"], "SystemOne usage.input_tokens")
        if "output_tokens" in usage:
            if _non_negative_int(
                usage["output_tokens"], "SystemOne usage.output_tokens"
            ) != 0:
                fail("SystemOne output_tokens must be zero when reported")

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


def _resolved(answers: dict[str, str], name: str) -> str:
    value = answers[name]
    if value == UNRESOLVED:
        raise DecisionUnresolved(f"{name}: SystemOne returned explicit unresolved")
    return value


def decision_from_answers(
    source: dict[str, Any],
    answers: dict[str, str],
) -> dict[str, Any]:
    spans = source_span_map(source)
    span_ids = tuple(spans)

    claim_type = _resolved(answers, "claim_type")
    modality = _resolved(answers, "modality")

    scope: dict[str, list[str]] = {}
    for field in SCOPE_FIELDS:
        values: list[str] = []
        for sid in span_ids:
            choice = _resolved(answers, f"scope__{field}__{sid}")
            if choice == "yes":
                values.append(sid)
        scope[field] = values

    nodes: list[dict[str, Any]] = []
    active_nodes: set[str] = set()
    for slot in NODE_SLOTS:
        active = _resolved(answers, f"{slot}__active")
        if active == "no":
            continue
        role = _resolved(answers, f"{slot}__role")
        anchor = _resolved(answers, f"{slot}__anchor")
        grounding = _resolved(answers, f"{slot}__grounding")
        refs: list[str] = []
        for sid in span_ids:
            membership = _resolved(answers, f"{slot}__span__{sid}")
            if membership == "yes":
                refs.append(sid)
        if not refs:
            fail(f"{slot}: active node requires at least one source span")
        if anchor not in refs:
            fail(f"{slot}: anchor_span_id must be included in source_span_ids")
        active_nodes.add(slot)
        nodes.append({
            "slot": slot,
            "role": role,
            "anchor_span_id": anchor,
            "source_span_ids": refs,
            "grounding": grounding,
        })

    if not nodes:
        fail("at least one node must be active")

    node_anchors = {node["slot"]: node["anchor_span_id"] for node in nodes}
    relations: list[dict[str, Any]] = []
    for slot in RELATION_SLOTS:
        active = _resolved(answers, f"{slot}__active")
        if active == "no":
            continue
        kind = _resolved(answers, f"{slot}__kind")
        arg1 = _resolved(answers, f"{slot}__arg1")
        arg2 = _resolved(answers, f"{slot}__arg2")
        grounding = _resolved(answers, f"{slot}__grounding")
        args = [arg1] + ([] if arg2 == "none" else [arg2])
        if len(args) != len(set(args)):
            fail(f"{slot}: duplicate relation arguments are forbidden")
        if any(arg not in active_nodes for arg in args):
            fail(f"{slot}: relation argument names inactive node")
        if len(args) > 1 and len({node_anchors[arg] for arg in args}) != len(args):
            fail(
                f"{slot}: distinct relation arguments require distinct node anchors"
            )
        refs: list[str] = []
        for sid in span_ids:
            membership = _resolved(answers, f"{slot}__span__{sid}")
            if membership == "yes":
                refs.append(sid)
        if not refs:
            fail(f"{slot}: active relation requires at least one source span")
        relations.append({
            "slot": slot,
            "kind": kind,
            "arguments": args,
            "source_span_ids": refs,
            "grounding": grounding,
        })

    decision = {
        "schema_version": DECISION_VERSION,
        "bundle_id": source["bundle_id"],
        "claim_type": claim_type,
        "modality": modality,
        "scope": scope,
        "nodes": nodes,
        "relations": relations,
    }
    validate_decision(decision, source)
    return decision


def validate_decision(decision: Any, source: dict[str, Any]) -> dict[str, Any]:
    root = expect_exact_keys(
        decision,
        {
            "schema_version", "bundle_id", "claim_type", "modality",
            "scope", "nodes", "relations",
        },
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
    anchor_by_node: dict[str, str] = {}
    for index, node in enumerate(nodes):
        item = expect_exact_keys(
            node,
            {"slot", "role", "anchor_span_id", "source_span_ids", "grounding"},
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
        anchor = item["anchor_span_id"]
        if anchor not in spans:
            fail(f"decision.nodes[{index}].anchor_span_id: unknown source span")
        if anchor not in refs:
            fail(
                f"decision.nodes[{index}].anchor_span_id must be in source_span_ids"
            )
        anchor_by_node[slot] = anchor

    relations = root["relations"]
    if not isinstance(relations, list) or len(relations) > len(RELATION_SLOTS):
        fail("decision.relations")
    seen_relations: set[str] = set()
    for index, relation in enumerate(relations):
        item = expect_exact_keys(
            relation,
            {"slot", "kind", "arguments", "source_span_ids", "grounding"},
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
        if (
            not isinstance(args, list)
            or not 1 <= len(args) <= 2
            or len(args) != len(set(args))
        ):
            fail(f"decision.relations[{index}].arguments")
        if any(arg not in seen_nodes for arg in args):
            fail(f"decision.relations[{index}].arguments: unknown node")
        if len(args) > 1 and len({anchor_by_node[arg] for arg in args}) != len(args):
            fail(
                f"decision.relations[{index}].arguments: anchors do not distinguish nodes"
            )
        refs = item["source_span_ids"]
        if not isinstance(refs, list) or not refs or len(refs) != len(set(refs)):
            fail(f"decision.relations[{index}].source_span_ids")
        if any(ref not in spans for ref in refs):
            fail(f"decision.relations[{index}].source_span_ids: unknown source span")
    return root


def compile_candidate(
    source: dict[str, Any],
    decision: dict[str, Any],
) -> dict[str, Any]:
    validate_decision(decision, source)

    scope = {
        field: [f"source-span:{ref}" for ref in decision["scope"][field]]
        for field in SCOPE_FIELDS
    }

    nodes = [
        {
            "id": node["slot"],
            "role": node["role"],
            "description": (
                f"source-grounded {node['role']} at {node['anchor_span_id']}"
            ),
            "source_span_ids": list(node["source_span_ids"]),
            "grounding": node["grounding"],
        }
        for node in decision["nodes"]
    ]

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
    _validate_candidate_claimir_parity(candidate)
    return candidate


def _validate_candidate_claimir_parity(candidate: dict[str, Any]) -> None:
    core = candidate["claim_core"]
    for index, node in enumerate(core["nodes"]):
        refs = node["source_span_ids"]
        if len(refs) != len(set(refs)):
            fail(f"candidate node {index}: duplicate source_span_ids")
    for index, relation in enumerate(core["relations"]):
        args = relation["arguments"]
        refs = relation["source_span_ids"]
        if len(args) != len(set(args)):
            fail(f"candidate relation {index}: duplicate arguments")
        if len(refs) != len(set(refs)):
            fail(f"candidate relation {index}: duplicate source_span_ids")


def assemble_synthetic_claim(
    source: dict[str, Any],
    candidate: dict[str, Any],
) -> dict[str, Any]:
    claim = {
        "schema_version": "paper2-claim-ir-v1",
        "claim_id": source["bundle_id"],
        "provenance": {
            "paper_id": f"synthetic:{source['bundle_id']}",
            "source_language": source["source_language"],
            "source_spans": [
                {"span_id": item["span_id"], "locator": f"Synthetic:{item['span_id']}"}
                for item in source["source_spans"]
            ],
            "authors": [],
            "institutions": [],
            "venue": None,
            "citation_count": None,
            "construct_labels": [],
        },
        "extraction": {
            "extractor": "synthetic-two-pass-systemone-v2",
            "extractor_version": "v2",
            "procedure_version": MANIFEST_VERSION,
            "extracted_at": "synthetic-fixture",
            "manual_review_status": "unreviewed",
        },
        "claim_core": copy.deepcopy(candidate["claim_core"]),
    }
    validate_claim_ir(claim)
    return claim


def audit_record(
    *,
    source: dict[str, Any],
    interpretation: str,
    systemone_request: dict[str, Any],
    response: dict[str, Any],
    decision: dict[str, Any],
    candidate: dict[str, Any],
    manifest: dict[str, Any],
    decision_schema: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "paper2-two-pass-systemone-audit-v2",
        "owner_issue": 162,
        "manifest_sha256": canonical_digest(manifest),
        "decision_schema_sha256": canonical_digest(decision_schema),
        "compiler_file_sha256": file_digest(Path(__file__)),
        "candidate_validator_file_sha256": file_digest(
            Path(__file__).with_name("paper2_extraction_procedure_validate.py")
        ),
        "claim_ir_validator_file_sha256": file_digest(
            Path(__file__).with_name("paper2_claim_ir_validate.py")
        ),
        "source_bundle_sha256": canonical_digest(source),
        "normal_interpretation_sha256": hashlib.sha256(
            interpretation.encode("utf-8")
        ).hexdigest(),
        "systemone_request_sha256": canonical_digest(systemone_request),
        "systemone_response_sha256": canonical_digest(response),
        "decision_sha256": canonical_digest(decision),
        "candidate_sha256": canonical_digest(candidate),
        "candidate_validation": "PASS",
        "full_claim_ir_validation": "PASS",
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
        raise TwoPassV2Error(f"SystemOne HTTP {exc.code}: {detail[:500]}") from exc
    except URLError as exc:
        raise TwoPassV2Error(f"SystemOne request failed: {exc}") from exc
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TwoPassV2Error("SystemOne response is not valid JSON") from exc
    if not isinstance(value, dict):
        fail("SystemOne response must be object")
    return value


def synthetic_source(
    spans: str | list[str],
    *,
    bundle_id: str = "B9001",
) -> dict[str, Any]:
    values = [spans] if isinstance(spans, str) else spans
    if not isinstance(values, list) or not 1 <= len(values) <= MAX_SPANS:
        fail("synthetic source requires one to three evidence units")
    return {
        "schema_version": "paper2-extraction-source-bundle-v1",
        "bundle_id": bundle_id,
        "source_language": "en",
        "source_spans": [
            {"span_id": f"s{index}", "text": text}
            for index, text in enumerate(values, start=1)
        ],
    }


def base_answers(source: dict[str, Any]) -> dict[str, str]:
    request = build_systemone_request(
        source,
        "Synthetic semantic interpretation.",
        "synthetic-systemone",
    )
    answers: dict[str, str] = {}
    for name, question in request["questions"].items():
        normal_choices = [key for key in question["criteria"] if key != UNRESOLVED]
        answers[name] = normal_choices[0]
    answers["claim_type"] = "relation"
    answers["modality"] = "descriptive"
    span_ids = tuple(source_span_map(source))
    for field in SCOPE_FIELDS:
        for sid in span_ids:
            answers[f"scope__{field}__{sid}"] = "no"
    for slot in NODE_SLOTS:
        answers[f"{slot}__active"] = "no"
        answers[f"{slot}__role"] = "other"
        answers[f"{slot}__anchor"] = span_ids[0]
        answers[f"{slot}__grounding"] = "explicit"
        for sid in span_ids:
            answers[f"{slot}__span__{sid}"] = "no"
    for slot in RELATION_SLOTS:
        answers[f"{slot}__active"] = "no"
        answers[f"{slot}__kind"] = "other"
        answers[f"{slot}__arg1"] = "n1"
        answers[f"{slot}__arg2"] = "none"
        answers[f"{slot}__grounding"] = "explicit"
        for sid in span_ids:
            answers[f"{slot}__span__{sid}"] = "no"
    return answers


def relation_answers(
    source: dict[str, Any],
    *,
    modality: str = "descriptive",
    relation_kind: str = "depends_on",
    n1_anchor: str = "s1",
    n2_anchor: str = "s2",
    relation_span: str = "s3",
) -> dict[str, str]:
    answers = base_answers(source)
    answers["claim_type"] = "relation"
    answers["modality"] = modality
    answers["n1__active"] = "yes"
    answers["n1__role"] = "state_or_structure"
    answers["n1__anchor"] = n1_anchor
    answers[f"n1__span__{n1_anchor}"] = "yes"
    answers["n2__active"] = "yes"
    answers["n2__role"] = "response_or_outcome"
    answers["n2__anchor"] = n2_anchor
    answers[f"n2__span__{n2_anchor}"] = "yes"
    answers["r1__active"] = "yes"
    answers["r1__kind"] = relation_kind
    answers["r1__arg1"] = "n1"
    answers["r1__arg2"] = "n2"
    answers[f"r1__span__{relation_span}"] = "yes"
    return answers


def node_only_answers(source: dict[str, Any]) -> dict[str, str]:
    answers = base_answers(source)
    answers["claim_type"] = "other"
    answers["modality"] = "descriptive"
    answers["n1__active"] = "yes"
    answers["n1__role"] = "state_or_structure"
    answers["n1__anchor"] = "s1"
    answers["n1__span__s1"] = "yes"
    return answers


def response_for(
    request_payload: dict[str, Any],
    choices: dict[str, str],
    *,
    output_tokens: int = 0,
) -> dict[str, Any]:
    answers = {}
    for name, question in request_payload["questions"].items():
        choice = choices[name]
        answers[name] = {
            "type": "choice",
            "choice": choice,
            "probabilities": {
                key: (1.0 if key == choice else 0.0)
                for key in question["criteria"]
            },
            "confidence": 1.0,
        }
    return {
        "model": request_payload["model"],
        "answers": answers,
        "usage": {"input_tokens": 123, "output_tokens": output_tokens},
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
    except (TwoPassV2Error, ContractError, ValidationError):
        return
    raise AssertionError(f"{label}: unexpectedly valid")


def run_case(
    source: dict[str, Any],
    interpretation: str,
    choices: dict[str, str],
    *,
    manifest: dict[str, Any],
    decision_schema: dict[str, Any],
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
    assemble_synthetic_claim(source, candidate)
    return decision, candidate, audit_record(
        source=source,
        interpretation=interpretation,
        systemone_request=request_payload,
        response=response,
        decision=decision,
        candidate=candidate,
        manifest=manifest,
        decision_schema=decision_schema,
    )


def self_test(manifest_path: Path, decision_schema_path: Path) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = json.loads(decision_schema_path.read_text(encoding="utf-8"))
    validate_manifest(manifest)
    validate_decision_schema(schema)

    max_source = synthetic_source(
        ["Synthetic A.", "Synthetic B.", "Synthetic relation."],
        bundle_id="B9099",
    )
    if len(build_questions(max_source)) != 54:
        raise AssertionError("maximum v2 question surface must be exactly 54")

    p1 = synthetic_source([
        "Synthetic state A.",
        "Synthetic state B.",
        "Synthetic state A depends on synthetic state B.",
    ])
    p1_decision, p1_candidate, p1_audit = run_case(
        p1,
        "A dependency is stated.",
        relation_answers(p1),
        manifest=manifest,
        decision_schema=schema,
    )
    if p1_candidate["claim_core"]["relations"][0]["kind"] != "depends_on":
        raise AssertionError("P1 relation kind")
    if p1_candidate["claim_core"]["nodes"][0]["description"] != (
        "source-grounded state_or_structure at s1"
    ):
        raise AssertionError("P1 node description must be neutral host template")
    if p1_audit["full_claim_ir_validation"] != "PASS":
        raise AssertionError("P1 full ClaimIR validation")

    p2 = synthetic_source([
        "Synthetic signal A.",
        "Synthetic outcome B.",
        "Signal A probabilistically predicts outcome B.",
    ], bundle_id="B9002")
    _, p2_candidate, _ = run_case(
        p2,
        "A probabilistic predictive relation is stated.",
        relation_answers(
            p2,
            modality="probabilistic",
            relation_kind="predicts",
        ),
        manifest=manifest,
        decision_schema=schema,
    )
    if p2_candidate["claim_core"]["modality"] != "probabilistic":
        raise AssertionError("P2 modality")

    p3 = synthetic_source("Synthetic state A is observed.", bundle_id="B9003")
    _, p3_candidate, _ = run_case(
        p3,
        "One state is described.",
        node_only_answers(p3),
        manifest=manifest,
        decision_schema=schema,
    )
    if p3_candidate["claim_core"]["relations"]:
        raise AssertionError("P3 invented relation")

    # Normal-pass prose cannot enter the candidate.
    _, n1_candidate, _ = run_case(
        p3,
        "The source says A causes B and C, although that is not in the source.",
        node_only_answers(p3),
        manifest=manifest,
        decision_schema=schema,
    )
    serialized_n1 = canonical_json_bytes(n1_candidate).decode("utf-8")
    if "causes B and C" in serialized_n1:
        raise AssertionError("N1 normal-pass prose leaked into candidate")

    # Invalid SystemOne option.
    n2_request = build_systemone_request(p1, "dependency", "synthetic-systemone")
    n2_response = response_for(n2_request, relation_answers(p1))
    n2_response["answers"]["modality"]["choice"] = "absolutely_certain"
    expect_invalid(
        lambda: parse_systemone_response(n2_request, n2_response),
        "N2 invalid SystemOne option",
    )

    # Explicit unresolved must fail closed before a decision/candidate exists.
    n3_choices = relation_answers(p1)
    n3_choices["modality"] = UNRESOLVED
    n3_response = response_for(n2_request, n3_choices)
    n3_answers = parse_systemone_response(n2_request, n3_response)
    expect_invalid(
        lambda: decision_from_answers(p1, n3_answers),
        "N3 explicit unresolved",
    )

    # Unknown anchor and duplicate relation arguments.
    n4 = copy.deepcopy(p1_decision)
    n4["nodes"][0]["anchor_span_id"] = "s999"
    expect_invalid(lambda: validate_decision(n4, p1), "N4 unknown anchor")
    n5 = copy.deepcopy(p1_decision)
    n5["relations"][0]["arguments"] = ["n1", "n1"]
    expect_invalid(lambda: validate_decision(n5, p1), "N5 duplicate relation arg")

    # Distinct relation arguments cannot collapse onto the same semantic anchor.
    n6 = copy.deepcopy(p1_decision)
    n6["nodes"][1]["anchor_span_id"] = "s1"
    n6["nodes"][1]["source_span_ids"] = ["s1"]
    expect_invalid(lambda: validate_decision(n6, p1), "N6 collapsed anchors")

    # Presentation-only Normal variation leaves candidate bytes stable.
    _, n7a, _ = run_case(
        p1, "A dependency is stated.", relation_answers(p1),
        manifest=manifest, decision_schema=schema,
    )
    _, n7b, _ = run_case(
        p1,
        "The passage describes one item as depending upon another.",
        relation_answers(p1),
        manifest=manifest,
        decision_schema=schema,
    )
    if canonical_json_bytes(n7a) != canonical_json_bytes(n7b):
        raise AssertionError("N7 interpretation wording changed candidate bytes")

    # One admitted finite-decision perturbation changes only the target field.
    alt = relation_answers(p1)
    alt["modality"] = "necessary"
    _, n8b, _ = run_case(
        p1, "A dependency is stated.", alt,
        manifest=manifest, decision_schema=schema,
    )
    n8a = copy.deepcopy(n7a)
    n8a["claim_core"]["modality"] = "necessary"
    if canonical_json_bytes(n8a) != canonical_json_bytes(n8b):
        raise AssertionError("N8 modality perturbation changed extra fields")

    # RelaySelf-style wire contract: type=choice; nonzero output tokens fail
    # when usage is reported, while optional observational metadata may be absent.
    bad_type = response_for(n2_request, relation_answers(p1))
    bad_type["answers"]["claim_type"]["type"] = "score"
    expect_invalid(
        lambda: parse_systemone_response(n2_request, bad_type),
        "N9 answer type mismatch",
    )
    nonzero = response_for(n2_request, relation_answers(p1), output_tokens=1)
    expect_invalid(
        lambda: parse_systemone_response(n2_request, nonzero),
        "N10 nonzero SystemOne output tokens",
    )
    wrong_model = response_for(n2_request, relation_answers(p1))
    wrong_model["model"] = "wrong-model"
    expect_invalid(
        lambda: parse_systemone_response(n2_request, wrong_model),
        "N11 response model mismatch",
    )
    minimal_wire = response_for(n2_request, relation_answers(p1))
    del minimal_wire["model"]
    del minimal_wire["usage"]
    for answer in minimal_wire["answers"].values():
        answer.pop("probabilities", None)
        answer.pop("confidence", None)
    parse_systemone_response(n2_request, minimal_wire)

    # Inactive slots may report unresolved on irrelevant subquestions without
    # forcing a false global failure. Only decisions that become semantically
    # active are required to resolve.
    inactive_unresolved = node_only_answers(p3)
    for name in list(inactive_unresolved):
        if name.startswith("n2__") or name.startswith("n3__"):
            if not name.endswith("__active"):
                inactive_unresolved[name] = UNRESOLVED
        if name.startswith("r1__") or name.startswith("r2__"):
            if not name.endswith("__active"):
                inactive_unresolved[name] = UNRESOLVED
    inactive_request = build_systemone_request(
        p3, "One state is described.", "synthetic-systemone"
    )
    inactive_response = response_for(inactive_request, inactive_unresolved)
    inactive_answers = parse_systemone_response(inactive_request, inactive_response)
    inactive_decision = decision_from_answers(p3, inactive_answers)
    if len(inactive_decision["nodes"]) != 1 or inactive_decision["relations"]:
        raise AssertionError("N12 inactive unresolved altered compiled structure")

    # Schema/Python parity control: schema requires unique relation arguments.
    relation_args_schema = (
        schema["properties"]["relations"]["items"]["properties"]["arguments"]
    )
    if relation_args_schema.get("uniqueItems") is not True:
        raise AssertionError("N13 schema lost relation argument uniqueness")

    # Full ClaimIR parity control: a duplicate candidate argument must be caught
    # before full assembly, matching paper2_claim_ir_validate unique_strings.
    duplicate_candidate = copy.deepcopy(p1_candidate)
    duplicate_candidate["claim_core"]["relations"][0]["arguments"] = ["n1", "n1"]
    expect_invalid(
        lambda: _validate_candidate_claimir_parity(duplicate_candidate),
        "N14 candidate/full-ClaimIR parity",
    )
    duplicate_claim = assemble_synthetic_claim(p1, p1_candidate)
    duplicate_claim["claim_core"]["relations"][0]["arguments"] = ["n1", "n1"]
    expect_invalid(
        lambda: validate_claim_ir(duplicate_claim),
        "N15 full ClaimIR duplicate relation argument",
    )

    # Local HTTP mock uses the same response shape expected above.
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
        assemble_synthetic_claim(p1, candidate)
        if candidate != p1_candidate:
            raise AssertionError("wire-path candidate mismatch")
        if len(MockSystemOneHandler.requests_seen) != 1:
            raise AssertionError("wire-path must issue exactly one SystemOne request")
        state = MockSystemOneHandler.requests_seen[0].get("state")
        if not isinstance(state, dict) or state.get("source") != p1:
            raise AssertionError("wire-path must include original source in state")
        if state.get("interpretation") != "A dependency is stated.":
            raise AssertionError("wire-path must include Normal interpretation in state")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    print("PAPER2_TWO_PASS_SYSTEMONE_V2_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("research/paper2/extraction_two_pass_systemone_v2.json"),
    )
    parser.add_argument(
        "--decision-schema",
        type=Path,
        default=Path("research/paper2/extraction_systemone_decision_v2.schema.json"),
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        schema = json.loads(args.decision_schema.read_text(encoding="utf-8"))
        validate_manifest(manifest)
        validate_decision_schema(schema)
        if args.self_test:
            self_test(args.manifest, args.decision_schema)
        else:
            print("PAPER2_TWO_PASS_SYSTEMONE_V2_VALID")
        return 0
    except (
        OSError,
        json.JSONDecodeError,
        TwoPassV2Error,
        ContractError,
        ValidationError,
        AssertionError,
    ) as exc:
        print(f"PAPER2_TWO_PASS_SYSTEMONE_V2_INVALID: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
