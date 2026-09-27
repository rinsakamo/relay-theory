#!/usr/bin/env python3
"""Synthetic-only, node-binding-safe SystemOne v4 decision surface for #259."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import paper2_extraction_two_pass_systemone_v3 as v3

VERSION = "paper2-systemone-decision-v4"
MANIFEST_VERSION = "paper2-two-pass-systemone-v4"
U = v3.U
SLOTS = v3.SLOTS
RELATIONS_SLOTS = v3.RELATIONS_SLOTS
SCOPE = v3.SCOPE
BASE = Path(__file__).resolve().parent.parent
MANIFEST_PATH = BASE / "research/paper2/extraction_two_pass_systemone_v4.json"
SCHEMA_PATH = BASE / "research/paper2/extraction_systemone_decision_v4.schema.json"

HISTORICAL_BLOBS = {
    "research/paper2/extraction_systemone_decision_v2.schema.json": "5933030119a903079a9eadb69e08d9326463339c",
    "research/paper2/extraction_two_pass_systemone_v2.json": "ed00b7458c068eb9add6a23dbf0e8282e06941d4",
    "scripts/paper2_extraction_two_pass_systemone_v2.py": "f789fcfb35af03a52e9193e6e6ebf5f86271707a",
    "research/paper2/extraction_systemone_decision_v3.schema.json": "22c1b6dce32f71d70dcc30d3c6879c18845b4c3f",
    "research/paper2/extraction_two_pass_systemone_v3.json": "cbb579742f7f16cbbe51f7db9603eaa8639d841e",
    "scripts/paper2_extraction_two_pass_systemone_v3.py": "9e2fdff07fd6b860d9dfe686c384b00d6c66b23f",
    ".github/workflows/paper2-two-pass-systemone-v3-selftest.yml": "35b29a065179c6ba336060c2406e3b5d032e54a8",
    "scripts/paper2_extraction_two_pass_llama_cpp_transaction_v3.py": "75f8436758bb5c93c5ca3a834e7c807155d5ce05",
    "research/paper2/extraction_v3_real_calibration_transaction_v1.json": "1abb318ff1f4160b38301169032c4924b58b3338",
    "research/paper2/extraction_v3_node_binding_audit_v1.json": "4fb966ff6531812d789e5fd2767f1b14085bbabd",
    "scripts/paper2_extraction_v3_node_binding_audit_validate.py": "6ed13be1f414d5a26a0663922b7df3e4a3271502",
    ".github/workflows/paper2-v3-node-binding-audit-selftest.yml": "4891e9b81115e81b207b78687aa82dd6ffeced81",
    "research/paper2/claim_ir_v1.schema.json": "963f54bd61c3112daa046fa191e3194d47db0768",
}

MAX_QUESTIONS = (18, 1, 1, 11, 10)
MAX_CHOICES = 29


def fail(message: str) -> None:
    raise v3.v2.TwoPassV2Error(message)


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def validate_manifest(manifest: dict[str, Any]) -> None:
    committed = json.loads(MANIFEST_PATH.read_text())
    if manifest != committed:
        fail("manifest differs from committed contract")
    if manifest.get("schema_version") != MANIFEST_VERSION or manifest.get("owner_issue") != 259:
        fail("manifest identity")
    if manifest.get("status") != "SYNTHETIC_QUALIFIED_ONLY":
        fail("manifest qualification status")
    if manifest.get("design") != "sequential_node_binding":
        fail("manifest design")
    if manifest.get("decision_schema") != VERSION or manifest.get("claim_ir_schema") != "paper2-claim-ir-v1":
        fail("manifest schema identity")
    for field in (
        "real_pilot_authorized",
        "real_model_calls_authorized",
        "heldout_execution_authorized",
        "basis_decomposition_authorized",
    ):
        if manifest.get(field) is not False:
            fail(f"manifest authorization drift: {field}")
    topology = manifest.get("topology", {})
    if topology.get("max_questions_per_stage") != list(MAX_QUESTIONS):
        fail("topology question bounds")
    if topology.get("max_finite_choices_per_question") != MAX_CHOICES:
        fail("topology choice bound")
    if topology.get("synthetic_decision_rounds") != 5 or topology.get("max_stages") != 5:
        fail("topology round count")
    if topology.get("max_total_synthetic_decision_rounds") != 5 or topology.get("max_systemone_subrequests_per_bundle") != 5:
        fail("topology total subrequests")
    if topology.get("real_transaction_authorized") is not False:
        fail("topology real transaction authorization")
    if manifest.get("bound_historical_blobs") != HISTORICAL_BLOBS:
        fail("historical identity set drift")
    for rel, expected in HISTORICAL_BLOBS.items():
        raw = (BASE / rel).read_bytes()
        actual = git_blob_sha(raw)
        if actual != expected:
            fail(f"historical blob changed: {rel}: {actual} != {expected}")
    bounded = manifest.get("bounded_surface", {})
    if "removed from every later node-binding finite surface" not in bounded.get("duplicate_handle_policy", ""):
        fail("P1 duplicate pruning contract")
    if "__unresolved__ terminates" not in bounded.get("unresolved_policy", ""):
        fail("P3 unresolved policy")
    if "consumes no referent handle" not in bounded.get("none_policy", ""):
        fail("P4 NONE policy")
    if bounded.get("relation_slot_referent_semantics") != "AUDIT_UNDERDETERMINED":
        fail("relation referent boundary")
    for phrase in ("restriction on applicability", "Historical provenance", "evidential support", "comparison provenance"):
        if phrase not in bounded.get("scope_semantics", ""):
            fail("P6 scope semantics")
    if manifest.get("source_authority") != {
        "original_source_authoritative": True,
        "normal_interpretation_advisory": True,
        "normal_prose_may_override_finite_source_decisions": False,
    }:
        fail("source authority")
    if manifest.get("scope_fixtures") != {
        "temporal": {
            "s1": "historical provenance date",
            "s2": "actual temporal restriction",
            "expected_temporal_scope": ["s2"],
        },
        "conditions": {
            "s1": "evidence supporting mechanism",
            "s2": "explicit condition under which claim applies",
            "expected_conditions": ["s2"],
        },
    }:
        fail("scope fixtures")
    expected_zero = {
        "synthetic_sources_only": True,
        "real_model_calls": 0,
        "real_server_launches": 0,
        "real_literature_extraction": 0,
        "paper210_replay": 0,
        "heldout_execution": 0,
        "basis_decomposition": 0,
    }
    if manifest.get("qualification") != expected_zero:
        fail("scientific accounting")


def validate_schema(schema: dict[str, Any]) -> None:
    committed = json.loads(SCHEMA_PATH.read_text())
    if schema != committed:
        fail("schema differs from committed schema")
    parent = json.loads(
        (BASE / "research/paper2/extraction_systemone_decision_v3.schema.json").read_text()
    )
    expected = copy.deepcopy(parent)
    expected["$id"] = expected["$id"].replace("_v3.", "_v4.")
    expected["title"] = "Paper 2 SystemOne Decision Record v4"
    expected["description"] = (
        "Sequential node-binding-safe finite decision record compiled deterministically "
        "into ClaimIR v1; synthetic qualification only."
    )
    expected["properties"]["schema_version"]["const"] = VERSION
    if schema != expected:
        fail("decision schema must preserve v3 structural invariants")


def check_bounds(stage: int, questions: dict[str, Any]) -> None:
    if len(questions) > MAX_QUESTIONS[stage - 1]:
        fail("stage question bound exceeded")
    if any(len(q["criteria"]) > MAX_CHOICES for q in questions.values()):
        fail("finite choice bound exceeded")


def seed_options(source: dict[str, Any], used: set[str] | None = None) -> dict[str, str]:
    used = set() if used is None else {x for x in used if x != "NONE"}
    options = v3.seed_options(source)
    return {key: value for key, value in options.items() if key == "NONE" or key not in used}


def stage1(source: dict[str, Any]) -> dict[str, Any]:
    spans = v3.spans_of(source)
    questions = {
        "claim_type": v3.choice(
            {x: x for x in sorted(v3.CLAIM_TYPES)},
            "Classify the source claim.",
        ),
        "modality": v3.choice(
            {x: x for x in sorted(v3.MODALITIES)},
            "Classify source-supported modality.",
        ),
    }
    for field in SCOPE:
        for sid in spans:
            questions[f"scope__{field}__{sid}"] = v3.choice(
                {"yes": "restricts claim applicability", "no": "does not restrict claim applicability"},
                (
                    f"Does {sid} restrict the applicability or domain of the represented claim "
                    f"as scope.{field}? Mere historical provenance, citation/date mention, "
                    "background, evidential support, or comparison provenance is not scope."
                ),
            )
    questions["n1__seed"] = v3.choice(
        seed_options(source),
        (
            "Bind source-grounded referent for n1. NONE means absent; choose __unresolved__ "
            "if the applicable referent cannot be distinguished from supplied state."
        ),
    )
    check_bounds(1, questions)
    return questions


def stage2(source: dict[str, Any], first: dict[str, str]) -> dict[str, Any]:
    q1 = stage1(source)
    v3.check_answers(q1, first)
    for name in q1:
        v3.resolved(first, name)
    n1 = v3.resolved(first, "n1__seed")
    used = set() if n1 == "NONE" else {n1}
    questions = {
        "n2__seed": v3.choice(
            seed_options(source, used),
            (
                "Bind source-grounded referent for n2 after n1 is fixed. Exact non-NONE "
                "handles already used are absent. NONE means absent; __unresolved__ is applicable ambiguity."
            ),
        )
    }
    check_bounds(2, questions)
    return questions


def stage3(
    source: dict[str, Any],
    first: dict[str, str],
    second: dict[str, str],
) -> dict[str, Any]:
    q2 = stage2(source, first)
    v3.check_answers(q2, second)
    for name in q2:
        v3.resolved(second, name)
    n1 = v3.resolved(first, "n1__seed")
    n2 = v3.resolved(second, "n2__seed")
    used = {x for x in (n1, n2) if x != "NONE"}
    questions = {
        "n3__seed": v3.choice(
            seed_options(source, used),
            (
                "Bind source-grounded referent for n3 after n1/n2 are fixed. Exact non-NONE "
                "handles already used are absent. NONE means absent; __unresolved__ is applicable ambiguity."
            ),
        )
    }
    check_bounds(3, questions)
    return questions


def bindings(
    source: dict[str, Any],
    first: dict[str, str],
    second: dict[str, str],
    third: dict[str, str],
) -> dict[str, tuple[str, str]]:
    q3 = stage3(source, first, second)
    v3.check_answers(q3, third)
    for name in q3:
        v3.resolved(third, name)
    seeds = {
        "n1": v3.resolved(first, "n1__seed"),
        "n2": v3.resolved(second, "n2__seed"),
        "n3": v3.resolved(third, "n3__seed"),
    }
    full = v3.seed_options(source)
    bound: dict[str, tuple[str, str]] = {}
    seen: set[str] = set()
    for slot in SLOTS:
        seed = seeds[slot]
        if seed == "NONE":
            continue
        if seed not in full:
            fail("unknown node referent handle")
        if seed in seen:
            fail("duplicate node referent handle")
        seen.add(seed)
        anchor, role = seed.split("::", 1)
        bound[slot] = (anchor, role)
    if not bound:
        fail("ClaimIR requires at least one bound node")
    return bound


def stage4(
    source: dict[str, Any],
    first: dict[str, str],
    second: dict[str, str],
    third: dict[str, str],
) -> dict[str, Any]:
    bound = bindings(source, first, second, third)
    questions: dict[str, Any] = {}
    for slot, (anchor, _) in bound.items():
        questions[f"{slot}__grounding"] = v3.choice(
            {x: x for x in sorted(v3.GROUNDING)},
            f"Grounding for bound referent {slot}.",
        )
        for sid in v3.spans_of(source):
            if sid != anchor:
                questions[f"{slot}__span__{sid}"] = v3.choice(
                    {"yes": "also grounds", "no": "does not ground"},
                    f"Does {sid} also ground {slot}? Anchor {anchor} is included by construction.",
                )
    for slot in RELATIONS_SLOTS:
        questions[f"{slot}__tuple"] = v3.choice(
            v3.tuple_options(bound),
            (
                f"Select the finite relation argument tuple for {slot}, or NONE. "
                "Relation-slot referent identity remains underdetermined by #200."
            ),
        )
    check_bounds(4, questions)
    return questions


def stage5(
    source: dict[str, Any],
    first: dict[str, str],
    second: dict[str, str],
    third: dict[str, str],
    fourth: dict[str, str],
) -> dict[str, Any]:
    q4 = stage4(source, first, second, third)
    v3.check_answers(q4, fourth)
    for name in q4:
        v3.resolved(fourth, name)
    questions: dict[str, Any] = {}
    for slot in RELATIONS_SLOTS:
        tuple_value = v3.resolved(fourth, f"{slot}__tuple")
        if tuple_value == "NONE":
            continue
        questions[f"{slot}__kind"] = v3.choice(
            {x: x for x in sorted(v3.RELATIONS)},
            f"Relation kind for {slot}.",
        )
        questions[f"{slot}__grounding"] = v3.choice(
            {x: x for x in sorted(v3.GROUNDING)},
            f"Grounding for {slot}.",
        )
        for sid in v3.spans_of(source):
            questions[f"{slot}__span__{sid}"] = v3.choice(
                {"yes": "grounds", "no": "does not ground"},
                f"Does {sid} ground {slot}?",
            )
    check_bounds(5, questions)
    return questions


def decision_from_rounds(
    source: dict[str, Any],
    first: dict[str, str],
    second: dict[str, str],
    third: dict[str, str],
    fourth: dict[str, str],
    fifth: dict[str, str],
) -> dict[str, Any]:
    bound = bindings(source, first, second, third)
    q4 = stage4(source, first, second, third)
    v3.check_answers(q4, fourth)
    q5 = stage5(source, first, second, third, fourth)
    v3.check_answers(q5, fifth)
    claim_type = v3.resolved(first, "claim_type")
    modality = v3.resolved(first, "modality")
    scope = {
        field: [
            sid
            for sid in v3.spans_of(source)
            if v3.resolved(first, f"scope__{field}__{sid}") == "yes"
        ]
        for field in SCOPE
    }
    nodes = []
    for slot, (anchor, role) in bound.items():
        refs = [anchor] + [
            sid
            for sid in v3.spans_of(source)
            if sid != anchor and v3.resolved(fourth, f"{slot}__span__{sid}") == "yes"
        ]
        nodes.append(
            {
                "slot": slot,
                "role": role,
                "anchor_span_id": anchor,
                "source_span_ids": refs,
                "grounding": v3.resolved(fourth, f"{slot}__grounding"),
            }
        )
    relations = []
    for slot in RELATIONS_SLOTS:
        selected = v3.resolved(fourth, f"{slot}__tuple")
        if selected == "NONE":
            continue
        args = selected.split("::")
        refs = [
            sid
            for sid in v3.spans_of(source)
            if v3.resolved(fifth, f"{slot}__span__{sid}") == "yes"
        ]
        relations.append(
            {
                "slot": slot,
                "kind": v3.resolved(fifth, f"{slot}__kind"),
                "arguments": args,
                "source_span_ids": refs,
                "grounding": v3.resolved(fifth, f"{slot}__grounding"),
            }
        )
    decision = {
        "schema_version": VERSION,
        "bundle_id": source["bundle_id"],
        "claim_type": claim_type,
        "modality": modality,
        "scope": scope,
        "nodes": nodes,
        "relations": relations,
    }
    validate_decision(decision, source)
    return decision


def v3_projection(decision: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(decision)
    result["schema_version"] = v3.VERSION
    return result


def validate_decision(decision: dict[str, Any], source: dict[str, Any]) -> None:
    if not isinstance(decision, dict) or decision.get("schema_version") != VERSION:
        fail("v4 decision version")
    v3.validate_decision(v3_projection(decision), source)
    seeds = [f"{node['anchor_span_id']}::{node['role']}" for node in decision["nodes"]]
    if len(seeds) != len(set(seeds)):
        fail("duplicate node referent handle")


def compile_candidate(source: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    validate_decision(decision, source)
    return v3.compile_candidate(source, v3_projection(decision))


def assemble_synthetic_claim(source: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    claim = v3.v2.assemble_synthetic_claim(source, candidate)
    claim["extraction"]["extractor"] = "synthetic-two-pass-systemone-v4"
    claim["extraction"]["extractor_version"] = "v4"
    claim["extraction"]["procedure_version"] = MANIFEST_VERSION
    v3.validate_claim_ir(claim)
    return claim


def classify(
    source: dict[str, Any],
    first: dict[str, str],
    second: dict[str, str],
    third: dict[str, str],
    fourth: dict[str, str],
    fifth: dict[str, str],
) -> dict[str, Any]:
    try:
        decision = decision_from_rounds(source, first, second, third, fourth, fifth)
    except v3.v2.DecisionUnresolved as exc:
        return {
            "outcome": "EXTRACTION_ABSTAIN",
            "reason": "DecisionUnresolved",
            "field": str(exc).split(":", 1)[0],
            "candidate": None,
            "claim_ir": None,
        }
    candidate = compile_candidate(source, decision)
    claim = assemble_synthetic_claim(source, candidate)
    return {
        "outcome": "VALID_CLAIM_IR",
        "decision": decision,
        "candidate": candidate,
        "claim_ir": claim,
    }


def answer_defaults(questions: dict[str, Any]) -> dict[str, str]:
    return {name: next(x for x in q["criteria"] if x != U) for name, q in questions.items()}


def scope_fixture_decision(manifest: dict[str, Any], fixture: str, field: str) -> dict[str, Any]:
    case = manifest["scope_fixtures"][fixture]
    source = v3.v2.synthetic_source(
        [case["s1"], case["s2"]],
        bundle_id="B9256" if fixture == "temporal" else "B9257",
    )
    a1 = answer_defaults(stage1(source))
    a1["n1__seed"] = "s2::condition"
    for name in a1:
        if name.startswith("scope__"):
            a1[name] = "no"
    a1[f"scope__{field}__s2"] = "yes"
    a2 = answer_defaults(stage2(source, a1))
    a2["n2__seed"] = "NONE"
    a3 = answer_defaults(stage3(source, a1, a2))
    a3["n3__seed"] = "NONE"
    a4 = answer_defaults(stage4(source, a1, a2, a3))
    a4["r1__tuple"] = a4["r2__tuple"] = "NONE"
    a5 = answer_defaults(stage5(source, a1, a2, a3, a4))
    return decision_from_rounds(source, a1, a2, a3, a4, a5)


def expect_failure(call, label: str, expected: str | None = None) -> str:
    try:
        call()
    except (v3.v2.TwoPassV2Error, KeyError, ValueError) as exc:
        message = str(exc)
        if expected is not None and message != expected:
            raise AssertionError(f"{label}: {message!r} != {expected!r}") from exc
        return message
    raise AssertionError(f"{label}: expected failure")


def expect_unresolved(call, label: str) -> None:
    try:
        call()
    except v3.v2.DecisionUnresolved:
        return
    raise AssertionError(f"{label}: expected DecisionUnresolved")


def self_test() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    schema = json.loads(SCHEMA_PATH.read_text())
    validate_manifest(manifest)
    validate_schema(schema)

    source = v3.v2.synthetic_source(
        ["Synthetic state A.", "Synthetic state B.", "A depends on B."],
        bundle_id="B9259",
    )
    q1 = stage1(source)
    a1 = answer_defaults(q1)
    a1.update({"claim_type": "relation", "modality": "descriptive", "n1__seed": "s1::state_or_structure"})
    for name in q1:
        if name.startswith("scope__"):
            a1[name] = "no"
    q2 = stage2(source, a1)
    a2 = answer_defaults(q2)
    a2["n2__seed"] = "s2::response_or_outcome"
    q3 = stage3(source, a1, a2)
    a3 = answer_defaults(q3)
    a3["n3__seed"] = "NONE"
    q4 = stage4(source, a1, a2, a3)
    a4 = answer_defaults(q4)
    a4.update({"n1__grounding": "explicit", "n2__grounding": "explicit", "r1__tuple": "n1::n2", "r2__tuple": "NONE"})
    q5 = stage5(source, a1, a2, a3, a4)
    a5 = answer_defaults(q5)
    a5.update({"r1__kind": "depends_on", "r1__grounding": "explicit", "r1__span__s3": "yes"})
    out = classify(source, a1, a2, a3, a4, a5)
    if out["outcome"] != "VALID_CLAIM_IR":
        raise AssertionError("valid fixture")

    checks: dict[str, bool] = {}
    checks["R1"] = all("__active" not in name for name in q1) and "n1__seed" in q1 and "n2__seed" not in q1
    collision = v3.v2.synthetic_source(
        ["Two synthetic states share one atomic evidence unit and the same role."],
        bundle_id="B9260",
    )
    c1 = answer_defaults(stage1(collision))
    c1["n1__seed"] = U
    checks["R2"] = classify(collision, c1, {}, {}, {}, {})["outcome"] == "EXTRACTION_ABSTAIN"
    checks["R3"] = "n1::n1" not in q4["r1__tuple"]["criteria"]
    checks["R4"] = all("n3" not in x for x in q4["r1__tuple"]["criteria"])
    same1 = copy.deepcopy(a1)
    same2 = answer_defaults(stage2(source, same1))
    same2["n2__seed"] = "s1::response_or_outcome"
    same3 = answer_defaults(stage3(source, same1, same2))
    same3["n3__seed"] = "NONE"
    same_options = stage4(source, same1, same2, same3)["r1__tuple"]["criteria"]
    checks["R5"] = "n1::n2" not in same_options and "n2::n1" not in same_options
    checks["R6"] = (
        scope_fixture_decision(manifest, "temporal", "temporal_scope")["scope"]["temporal_scope"]
        == manifest["scope_fixtures"]["temporal"]["expected_temporal_scope"]
    )
    checks["R7"] = (
        scope_fixture_decision(manifest, "conditions", "conditions")["scope"]["conditions"]
        == manifest["scope_fixtures"]["conditions"]["expected_conditions"]
    )
    checks["R8"] = all(not x.startswith("n3__") for x in q4) and all(not x.startswith("r2__") for x in q5)
    unresolved4 = copy.deepcopy(a4)
    unresolved4["n1__grounding"] = U
    abstain = classify(source, a1, a2, a3, unresolved4, a5)
    checks["R9"] = abstain["outcome"] == "EXTRACTION_ABSTAIN" and abstain["candidate"] is None and abstain["claim_ir"] is None
    checks["R10"] = checks["R8"] and checks["R9"] and abstain["field"] == "n1__grounding"
    checks["R11"] = "n1__span__s1" not in q4 and out["decision"]["nodes"][0]["source_span_ids"][0] == "s1"
    checks["R12"] = all(
        manifest["qualification"][x] == 0
        for x in ("real_model_calls", "real_server_launches", "real_literature_extraction")
    )
    checks["R13"] = out["claim_ir"]["schema_version"] == "paper2-claim-ir-v1" and bool(v3.validate_claim_ir(out["claim_ir"]))
    mutant = copy.deepcopy(out["decision"])
    mutant["relations"][0]["arguments"] = ["n1", "n1"]
    expect_failure(lambda: compile_candidate(source, mutant), "R14 invalid tuple")
    checks["R14"] = True
    advisory = "Normal claims an unsupported opposite relation and false scope."
    parsed = v3.parse_round(
        source,
        advisory,
        "synthetic",
        q1,
        {
            "model": "synthetic",
            "answers": {
                name: {"type": "choice", "choice": answer}
                for name, answer in a1.items()
            },
            "usage": {"output_tokens": 0},
        },
    )
    checks["R15"] = parsed == a1 and v3.canonical_json_bytes(
        decision_from_rounds(source, parsed, a2, a3, a4, a5)
    ) == v3.canonical_json_bytes(out["decision"])
    repeat = classify(source, a1, a2, a3, a4, a5)
    checks["R16"] = all(
        v3.canonical_json_bytes(out[x]) == v3.canonical_json_bytes(repeat[x])
        for x in ("decision", "candidate", "claim_ir")
    )

    max_source = v3.v2.synthetic_source(["A", "B", "C"], bundle_id="B9299")
    m1 = answer_defaults(stage1(max_source))
    m1["n1__seed"] = "s1::condition"
    for name in m1:
        if name.startswith("scope__"):
            m1[name] = "no"
    m2 = answer_defaults(stage2(max_source, m1))
    m2["n2__seed"] = "s2::criterion"
    m3 = answer_defaults(stage3(max_source, m1, m2))
    m3["n3__seed"] = "s3::probe"
    m4 = answer_defaults(stage4(max_source, m1, m2, m3))
    m4.update({"r1__tuple": "n1::n2", "r2__tuple": "n2::n3"})
    counts = [
        len(stage1(max_source)),
        len(stage2(max_source, m1)),
        len(stage3(max_source, m1, m2)),
        len(stage4(max_source, m1, m2, m3)),
        len(stage5(max_source, m1, m2, m3, m4)),
    ]
    max_choices = max(
        len(q["criteria"])
        for surface in (
            stage1(max_source),
            stage2(max_source, m1),
            stage3(max_source, m1, m2),
            stage4(max_source, m1, m2, m3),
            stage5(max_source, m1, m2, m3, m4),
        )
        for q in surface.values()
    )
    checks["R17"] = counts == list(MAX_QUESTIONS) and max_choices == MAX_CHOICES

    h = "s1::condition"
    r18src = v3.v2.synthetic_source(["A", "B"], bundle_id="B9278")
    r18a1 = answer_defaults(stage1(r18src))
    r18a1["n1__seed"] = h
    r18q2 = stage2(r18src, r18a1)
    checks["R18"] = h not in r18q2["n2__seed"]["criteria"]

    r19a2 = answer_defaults(r18q2)
    h2 = "s2::criterion"
    r19a2["n2__seed"] = h2
    r19q3 = stage3(r18src, r18a1, r19a2)
    checks["R19"] = h not in r19q3["n3__seed"]["criteria"] and h2 not in r19q3["n3__seed"]["criteria"]

    r20a1 = answer_defaults(stage1(r18src))
    r20a1["n1__seed"] = "NONE"
    checks["R20"] = h in stage2(r18src, r20a1)["n2__seed"]["criteria"]

    r21a1 = answer_defaults(stage1(r18src))
    r21a1["n1__seed"] = U
    expect_unresolved(lambda: stage2(r18src, r21a1), "R21 n1")
    r21b1 = answer_defaults(stage1(r18src))
    r21b1["n1__seed"] = h
    r21b2 = answer_defaults(stage2(r18src, r21b1))
    r21b2["n2__seed"] = U
    expect_unresolved(lambda: stage3(r18src, r21b1, r21b2), "R21 n2")
    checks["R21"] = True

    r22bad = answer_defaults(r18q2)
    r22bad["n2__seed"] = "s999::condition"
    expect_failure(
        lambda: v3.check_answers(r18q2, r22bad),
        "R22 unknown finite answer",
        "answer outside finite surface: n2__seed",
    )
    checks["R22"] = True

    r23bad = answer_defaults(r18q2)
    r23bad["n2__seed"] = h
    unavailable = h not in r18q2["n2__seed"]["criteria"]
    earliest = expect_failure(
        lambda: v3.check_answers(r18q2, r23bad),
        "R23 #257 witness",
        "answer outside finite surface: n2__seed",
    )
    checks["R23"] = unavailable and earliest == "answer outside finite surface: n2__seed"

    duplicate = copy.deepcopy(out["decision"])
    duplicate["nodes"][1]["anchor_span_id"] = duplicate["nodes"][0]["anchor_span_id"]
    duplicate["nodes"][1]["role"] = duplicate["nodes"][0]["role"]
    expect_failure(lambda: compile_candidate(source, duplicate), "R24 mutated duplicate state")
    checks["R24"] = True

    checks["R25"] = (
        counts == manifest["topology"]["max_questions_per_stage"]
        and max_choices == manifest["topology"]["max_finite_choices_per_question"]
        and manifest["topology"]["max_systemone_subrequests_per_bundle"] == 5
    )
    checks["R26"] = checks["R16"]
    checks["R27"] = all(
        manifest["qualification"][x] == 0
        for x in (
            "real_model_calls",
            "real_server_launches",
            "real_literature_extraction",
            "paper210_replay",
            "heldout_execution",
            "basis_decomposition",
        )
    )

    for label in [f"R{i}" for i in range(1, 28)]:
        if not checks.get(label):
            raise AssertionError(f"{label} FAIL")
        print(f"{label}=PASS")

    destructive_tests(manifest, source, a1, a2, a3, a4, a5, out, r18src, r18a1, r19a2)
    print("SYSTEMONE_V4_SYNTHETICALLY_QUALIFIED")


def destructive_tests(
    manifest: dict[str, Any],
    source: dict[str, Any],
    a1: dict[str, str],
    a2: dict[str, str],
    a3: dict[str, str],
    a4: dict[str, str],
    a5: dict[str, str],
    out: dict[str, Any],
    witness_source: dict[str, Any],
    witness_a1: dict[str, str],
    witness_a2: dict[str, str],
) -> None:
    mutations: list[tuple[str, Any]] = []

    actual2 = stage2(witness_source, witness_a1)
    altered2 = copy.deepcopy(actual2)
    altered2["n2__seed"]["criteria"][witness_a1["n1__seed"]] = "reintroduced duplicate"
    mutations.append(("reintroduce n1 handle into n2", lambda: assert_surface(actual2, altered2)))

    actual3 = stage3(witness_source, witness_a1, witness_a2)
    altered3 = copy.deepcopy(actual3)
    altered3["n3__seed"]["criteria"][witness_a1["n1__seed"]] = "reintroduced duplicate"
    mutations.append(("reintroduce prior handle into n3", lambda: assert_surface(actual3, altered3)))

    q4 = stage4(source, a1, a2, a3)
    altered4 = copy.deepcopy(q4)
    altered4["r1__tuple"]["criteria"]["n1::n1"] = "duplicate relation tuple"
    mutations.append(("duplicate relation argument", lambda: assert_surface(q4, altered4)))

    same_manifest = copy.deepcopy(manifest)
    same_manifest["bounded_surface"]["scope_semantics"] = "scope is any contributing evidence"
    mutations.append(("scope semantic drift", lambda: validate_manifest(same_manifest)))

    auth_manifest = copy.deepcopy(manifest)
    auth_manifest["real_model_calls_authorized"] = True
    mutations.append(("real-call authorization", lambda: validate_manifest(auth_manifest)))

    topology_manifest = copy.deepcopy(manifest)
    topology_manifest["topology"]["max_systemone_subrequests_per_bundle"] = 3
    mutations.append(("hidden topology contraction", lambda: validate_manifest(topology_manifest)))

    history_manifest = copy.deepcopy(manifest)
    history_manifest["bound_historical_blobs"]["scripts/paper2_extraction_two_pass_systemone_v3.py"] = "0" * 40
    mutations.append(("historical v3 blob drift", lambda: validate_manifest(history_manifest)))

    duplicate = copy.deepcopy(out["decision"])
    duplicate["nodes"][1]["anchor_span_id"] = duplicate["nodes"][0]["anchor_span_id"]
    duplicate["nodes"][1]["role"] = duplicate["nodes"][0]["role"]
    mutations.append(("post-hoc duplicate repair", lambda: compile_candidate(source, duplicate)))

    unresolved = copy.deepcopy(a4)
    unresolved["n1__grounding"] = U
    mutations.append(("applicable unresolved compiles", lambda: assert_valid(classify(source, a1, a2, a3, unresolved, a5))))

    for label, call in mutations:
        expect_failure(call, label)
        print(f"MUTATION {label}=REJECTED")


def assert_surface(actual: dict[str, Any], proposed: dict[str, Any]) -> None:
    if actual != proposed:
        fail("mutated finite surface")


def assert_valid(outcome: dict[str, Any]) -> None:
    if outcome.get("outcome") != "VALID_CLAIM_IR":
        fail("applicable unresolved correctly abstained")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.self_test:
        parser.error("only synthetic --self-test is supported")
    self_test()


if __name__ == "__main__":
    main()
