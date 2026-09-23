#!/usr/bin/env python3
"""Validate Paper 2 extraction-procedure v1 fixtures and isolation contract.

Owner: #147. This validates the mechanical procedure surface only.
It does not execute real literature extraction or establish faithfulness.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any


PROC_VERSION = "paper2-extraction-procedure-v1"
SOURCE_VERSION = "paper2-extraction-source-bundle-v1"
CANDIDATE_VERSION = "paper2-extraction-candidate-v1"
BUNDLE_RE = re.compile(r"^B[0-9]{4}$")
SPAN_RE = re.compile(r"^s[0-9]+$")
ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")

AUTHORITY_KEYS = {
    "title","authors","author","institutions","institution","venue",
    "citation_count","citations","registry_comment_id","registry_usage_comment_id",
    "paper_id","stable_identity","canonical_url","construct_labels",
    "top50_seed","sample_id","claim_form_stratum"
}
RESULT_KEYS = {
    "basis","basis_elements","basis_mapping","basis_witness","lean_theorem",
    "lean_result","decomposition_success","decomposition_failure",
    "decomposition_result","coverage","coverage_score","residual",
    "residual_type","acceptance_verdict","other_pass_output"
}
CLAIM_TYPES = {"relation","criterion","mapping","comparison","counterfactual","definition","constraint","other"}
MODALITIES = {"descriptive","necessary","sufficient","probabilistic","definitional","counterfactual","comparative","other"}
ROLES = {"condition","available_information","state_or_structure","intervention","response_or_outcome","criterion","probe","partition","other"}
RELATIONS = {"equals","differs","depends_on","changes","predicts","maps_to","satisfies","distinguishes","precedes","constrains","equivalent","other"}
GROUNDING = {"explicit","normalized"}


class ContractError(ValueError):
    pass


def fail(message: str) -> None:
    raise ContractError(message)


def walk_forbidden(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in AUTHORITY_KEYS:
                fail(f"{path}: authority key forbidden on extractor surface: {key}")
            if key in RESULT_KEYS:
                fail(f"{path}: result/basis key forbidden on extractor surface: {key}")
            walk_forbidden(item, f"{path}.{key}")
    elif isinstance(value, list):
        for i, item in enumerate(value):
            walk_forbidden(item, f"{path}[{i}]")


def expect_keys(obj: Any, required: set[str], path: str) -> dict[str, Any]:
    if not isinstance(obj, dict):
        fail(f"{path}: expected object")
    actual = set(obj)
    if actual != required:
        fail(f"{path}: key mismatch missing={sorted(required-actual)} extra={sorted(actual-required)}")
    return obj


def expect_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{path}: expected non-empty string")
    return value


def validate_source(data: Any) -> dict[str, Any]:
    root = expect_keys(data, {"schema_version","bundle_id","source_language","source_spans"}, "source")
    if root["schema_version"] != SOURCE_VERSION:
        fail("source.schema_version")
    bundle = expect_string(root["bundle_id"], "source.bundle_id")
    if not BUNDLE_RE.fullmatch(bundle):
        fail("source.bundle_id: opaque B#### identifier required")
    expect_string(root["source_language"], "source.source_language")
    spans = root["source_spans"]
    if not isinstance(spans, list) or not spans:
        fail("source.source_spans: non-empty array required")
    ids: set[str] = set()
    for i, raw in enumerate(spans):
        span = expect_keys(raw, {"span_id","text"}, f"source.source_spans[{i}]")
        sid = expect_string(span["span_id"], f"source.source_spans[{i}].span_id")
        if not SPAN_RE.fullmatch(sid):
            fail(f"source.source_spans[{i}].span_id")
        if sid in ids:
            fail(f"source.source_spans[{i}].span_id: duplicate")
        ids.add(sid)
        expect_string(span["text"], f"source.source_spans[{i}].text")
    walk_forbidden(root)
    return root


def validate_candidate(data: Any, source: dict[str, Any]) -> dict[str, Any]:
    root = expect_keys(data, {"schema_version","bundle_id","claim_core"}, "candidate")
    if root["schema_version"] != CANDIDATE_VERSION:
        fail("candidate.schema_version")
    if root["bundle_id"] != source["bundle_id"]:
        fail("candidate.bundle_id: must match source bundle")
    core = expect_keys(root["claim_core"], {"claim_type","modality","scope","nodes","relations"}, "candidate.claim_core")
    if core["claim_type"] not in CLAIM_TYPES:
        fail("candidate.claim_core.claim_type")
    if core["modality"] not in MODALITIES:
        fail("candidate.claim_core.modality")
    scope = expect_keys(core["scope"], {"conditions","population","substrate","task","temporal_scope"}, "candidate.claim_core.scope")
    for key, values in scope.items():
        if not isinstance(values, list):
            fail(f"candidate.claim_core.scope.{key}: expected array")
        for i, value in enumerate(values):
            expect_string(value, f"candidate.claim_core.scope.{key}[{i}]")

    source_spans = {s["span_id"] for s in source["source_spans"]}
    nodes = core["nodes"]
    if not isinstance(nodes, list) or not nodes:
        fail("candidate.claim_core.nodes: non-empty array required")
    node_ids: set[str] = set()
    for i, raw in enumerate(nodes):
        node = expect_keys(raw, {"id","role","description","source_span_ids","grounding"}, f"candidate.claim_core.nodes[{i}]")
        nid = expect_string(node["id"], f"candidate.claim_core.nodes[{i}].id")
        if not ID_RE.fullmatch(nid) or nid in node_ids:
            fail(f"candidate.claim_core.nodes[{i}].id")
        node_ids.add(nid)
        if node["role"] not in ROLES:
            fail(f"candidate.claim_core.nodes[{i}].role")
        expect_string(node["description"], f"candidate.claim_core.nodes[{i}].description")
        refs = node["source_span_ids"]
        if not isinstance(refs, list) or not refs:
            fail(f"candidate.claim_core.nodes[{i}].source_span_ids")
        if any(ref not in source_spans for ref in refs):
            fail(f"candidate.claim_core.nodes[{i}].source_span_ids: unknown span")
        if node["grounding"] not in GROUNDING:
            fail(f"candidate.claim_core.nodes[{i}].grounding")

    relations = core["relations"]
    if not isinstance(relations, list):
        fail("candidate.claim_core.relations: expected array")
    relation_ids: set[str] = set()
    for i, raw in enumerate(relations):
        rel = expect_keys(raw, {"id","kind","arguments","description","source_span_ids","grounding"}, f"candidate.claim_core.relations[{i}]")
        rid = expect_string(rel["id"], f"candidate.claim_core.relations[{i}].id")
        if not ID_RE.fullmatch(rid) or rid in relation_ids:
            fail(f"candidate.claim_core.relations[{i}].id")
        relation_ids.add(rid)
        if rel["kind"] not in RELATIONS:
            fail(f"candidate.claim_core.relations[{i}].kind")
        args = rel["arguments"]
        if not isinstance(args, list) or not args or any(arg not in node_ids for arg in args):
            fail(f"candidate.claim_core.relations[{i}].arguments")
        expect_string(rel["description"], f"candidate.claim_core.relations[{i}].description")
        refs = rel["source_span_ids"]
        if not isinstance(refs, list) or not refs or any(ref not in source_spans for ref in refs):
            fail(f"candidate.claim_core.relations[{i}].source_span_ids")
        if rel["grounding"] not in GROUNDING:
            fail(f"candidate.claim_core.relations[{i}].grounding")

    walk_forbidden(root)
    return root


def validate_procedure(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        fail("procedure: expected object")
    if data.get("schema_version") != PROC_VERSION:
        fail("procedure.schema_version")
    if data.get("owner_issue") != 147:
        fail("procedure.owner_issue")
    if data.get("status") != "FROZEN_BEFORE_EXTRACTION":
        fail("procedure.status")
    if data.get("passes") != ["A","B"]:
        fail("procedure.passes")

    inp = data.get("input_contract")
    if not isinstance(inp, dict):
        fail("procedure.input_contract")
    required_true = {"same_canonical_bundle_bytes_for_both_passes","opaque_bundle_id_only"}
    required_false = {
        "authority_metadata_visible","title_visible","authors_visible","institutions_visible",
        "venue_visible","citation_count_visible","registry_metadata_visible",
        "construct_label_list_visible","basis_visible","decomposition_outcome_visible",
        "other_pass_output_visible"
    }
    for key in required_true:
        if inp.get(key) is not True:
            fail(f"procedure.input_contract.{key}: must be true")
    for key in required_false:
        if inp.get(key) is not False:
            fail(f"procedure.input_contract.{key}: must be false")
    if inp.get("source_text_surface") != "abstract_only":
        fail("procedure.input_contract.source_text_surface")

    exe = data.get("execution_contract")
    if not isinstance(exe, dict):
        fail("procedure.execution_contract")
    for key in (
        "fresh_context_per_pass","cross_pass_messages_forbidden",
        "cross_pass_files_forbidden","other_claim_outputs_forbidden",
        "post_hoc_prompt_edits_between_passes_forbidden",
        "same_procedure_version_required","extractor_identity_and_version_recorded_after_output",
        "candidate_must_validate_before_assembly"
    ):
        if exe.get(key) is not True:
            fail(f"procedure.execution_contract.{key}: must be true")

    out = data.get("output_contract")
    if not isinstance(out, dict):
        fail("procedure.output_contract")
    for key in (
        "extractor_outputs_claim_core_only","provenance_added_after_extraction",
        "extraction_metadata_added_after_extraction",
        "claim_core_must_be_source_span_grounded",
        "no_basis_or_decomposition_fields","no_authority_metadata_fields"
    ):
        if out.get(key) is not True:
            fail(f"procedure.output_contract.{key}: must be true")

    adj = data.get("adjudication_contract")
    if not isinstance(adj, dict):
        fail("procedure.adjudication_contract")
    for key in (
        "begins_only_after_both_passes_are_frozen","source_text_visible","a_and_b_visible",
        "adjudication_must_record_reason_codes","adjudication_must_not_prefer_easier_decomposition"
    ):
        if adj.get(key) is not True:
            fail(f"procedure.adjudication_contract.{key}: must be true")
    for key in ("basis_visible","decomposition_outcome_visible"):
        if adj.get(key) is not False:
            fail(f"procedure.adjudication_contract.{key}: must be false")

    forbidden = data.get("forbidden_information_classes")
    if not isinstance(forbidden, list):
        fail("procedure.forbidden_information_classes")
    for required in (
        "author_identity","citation_prestige","source_construct_label_list",
        "basis_mapping","decomposition_success","other_pass_output"
    ):
        if required not in forbidden:
            fail(f"procedure.forbidden_information_classes missing {required}")

    seq = data.get("run_sequence")
    if not isinstance(seq, list) or len(seq) < 9:
        fail("procedure.run_sequence")
    return data


def expect_invalid(fn, label: str) -> None:
    try:
        fn()
    except ContractError:
        return
    raise AssertionError(f"{label}: unexpectedly valid")


def self_test(proc_path: Path, source_path: Path, candidate_path: Path) -> None:
    proc = json.loads(proc_path.read_text(encoding="utf-8"))
    source = json.loads(source_path.read_text(encoding="utf-8"))
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    validate_procedure(proc)
    validate_source(source)
    validate_candidate(candidate, source)

    n1 = copy.deepcopy(source)
    n1["authors"] = ["Named Author"]
    expect_invalid(lambda: validate_source(n1), "N1 authority metadata in source bundle")

    n2 = copy.deepcopy(source)
    n2["basis_mapping"] = {"x":"y"}
    expect_invalid(lambda: validate_source(n2), "N2 basis leakage in source bundle")

    n3 = copy.deepcopy(candidate)
    n3["provenance"] = {"paper_id":"p"}
    expect_invalid(lambda: validate_candidate(n3, source), "N3 provenance leakage in candidate")

    n4 = copy.deepcopy(candidate)
    n4["claim_core"]["nodes"][0]["source_span_ids"] = ["s999"]
    expect_invalid(lambda: validate_candidate(n4, source), "N4 ungrounded candidate node")

    n5 = copy.deepcopy(candidate)
    n5["claim_core"]["decomposition_success"] = True
    expect_invalid(lambda: validate_candidate(n5, source), "N5 result leakage in candidate")

    n6 = copy.deepcopy(proc)
    n6["input_contract"]["other_pass_output_visible"] = True
    expect_invalid(lambda: validate_procedure(n6), "N6 cross-pass visibility")

    print("PAPER2_EXTRACTION_PROCEDURE_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--procedure", type=Path, default=Path("research/paper2/extraction_procedure_v1.json"))
    parser.add_argument("--source", type=Path, default=Path("research/paper2/extraction_source_bundle_v1.example.json"))
    parser.add_argument("--candidate", type=Path, default=Path("research/paper2/extraction_candidate_v1.example.json"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        proc = json.loads(args.procedure.read_text(encoding="utf-8"))
        source = json.loads(args.source.read_text(encoding="utf-8"))
        candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
        validate_procedure(proc)
        validate_source(source)
        validate_candidate(candidate, source)
        if args.self_test:
            self_test(args.procedure, args.source, args.candidate)
        else:
            print("PAPER2_EXTRACTION_PROCEDURE_V1_VALID")
        return 0
    except (OSError, json.JSONDecodeError, ContractError, AssertionError) as exc:
        print(f"PAPER2_EXTRACTION_PROCEDURE_V1_INVALID: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
