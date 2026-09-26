#!/usr/bin/env python3
"""Synthetic-only, dependency-aware SystemOne v3 decision surface for #203."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import paper2_extraction_two_pass_systemone_v2 as v2
from paper2_extraction_bundle_prepare import canonical_json_bytes
from paper2_extraction_procedure_validate import CLAIM_TYPES, GROUNDING, MODALITIES, RELATIONS, ROLES
from paper2_claim_ir_validate import validate as validate_claim_ir

VERSION = "paper2-systemone-decision-v3"
MANIFEST_VERSION = "paper2-two-pass-systemone-v3"
U = v2.UNRESOLVED
SLOTS = v2.NODE_SLOTS
RELATIONS_SLOTS = v2.RELATION_SLOTS
SCOPE = v2.SCOPE_FIELDS
BASE = Path(__file__).resolve().parent.parent
MANIFEST_PATH = BASE / "research/paper2/extraction_two_pass_systemone_v3.json"
SCHEMA_PATH = BASE / "research/paper2/extraction_systemone_decision_v3.schema.json"
PARENT_BLOBS = {
    "research/paper2/extraction_decision_surface_audit_v1.json": "0a3efe63d0ff18ea04ba14393c58c8bd7cb2d38b",
    "research/paper2/extraction_systemone_decision_v2.schema.json": "5933030119a903079a9eadb69e08d9326463339c",
    "research/paper2/extraction_two_pass_systemone_v2.json": "ed00b7458c068eb9add6a23dbf0e8282e06941d4",
    "scripts/paper2_extraction_two_pass_systemone_v2.py": "f789fcfb35af03a52e9193e6e6ebf5f86271707a",
    "research/paper2/claim_ir_v1.schema.json": "963f54bd61c3112daa046fa191e3194d47db0768",
    "research/paper2/extraction_procedure_v1.json": "5e1b6c17c8cd9b4b3455de137b99a90f870233d0",
}


def fail(message: str) -> None:
    raise v2.TwoPassV2Error(message)


def choice(options: dict[str, str], instruction: str) -> dict[str, Any]:
    return v2._choice(options, instruction)


def spans_of(source: dict[str, Any]) -> tuple[str, ...]:
    return tuple(v2.source_span_map(source))


def validate_manifest(manifest: dict[str, Any]) -> None:
    committed = json.loads(MANIFEST_PATH.read_text())
    if manifest != committed:
        fail("manifest differs from committed contract")
    if manifest["schema_version"] != MANIFEST_VERSION or manifest["owner_issue"] != 203:
        fail("manifest identity")
    if manifest["status"] != "SYNTHETIC_QUALIFIED_ONLY":
        fail("manifest qualification status")
    if manifest["claim_ir_schema"] != "paper2-claim-ir-v1" or manifest["decision_schema"] != VERSION:
        fail("manifest schema version")
    for field in ("real_pilot_authorized", "real_model_calls_authorized", "heldout_execution_authorized", "basis_decomposition_authorized"):
        if manifest[field] is not False:
            fail(f"manifest {field}")
    expected_blobs = manifest["bound_parent_blobs"]
    if expected_blobs != PARENT_BLOBS:
        fail("bound parent identities")
    for name, blob in expected_blobs.items():
        # Git blob identity includes the object header, unlike a raw SHA-256.
        data = (BASE / name).read_bytes()
        actual = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        if actual != blob:
            fail(f"bound parent blob changed: {name}")
    if manifest["topology"]["max_questions_per_stage"] != [20, 11, 10]:
        fail("topology bound")
    if manifest["topology"]["max_finite_choices_per_question"] != 29:
        fail("choice bound")
    if manifest["topology"]["synthetic_decision_rounds"] != 3 or manifest["topology"]["max_stages"] != 3 or manifest["topology"]["max_total_synthetic_decision_rounds"] != 3 or manifest["topology"]["real_transaction_authorized"] is not False:
        fail("stage/authorization topology")
    if manifest["bounded_surface"]["relation_slot_referent_semantics"] != "AUDIT_UNDERDETERMINED":
        fail("relation referent boundary")
    if manifest["source_authority"] != {"original_source_authoritative": True, "normal_interpretation_advisory": True, "normal_prose_may_override_finite_source_decisions": False}:
        fail("source authority")
    scope = manifest["bounded_surface"]["scope_semantics"]
    for phrase in ("restriction on applicability", "Historical provenance", "evidential support", "comparison provenance"):
        if phrase not in scope:
            fail("scope applicability semantics")
    if manifest["scope_fixtures"] != {
        "temporal": {"s1": "historical provenance date", "s2": "actual temporal restriction", "expected_temporal_scope": ["s2"]},
        "conditions": {"s1": "evidence supporting mechanism", "s2": "explicit condition under which claim applies", "expected_conditions": ["s2"]},
    }:
        fail("scope contrast fixtures")
    if manifest["qualification"] != {
        "synthetic_sources_only": True,
        "real_model_calls": 0,
        "real_server_launches": 0,
        "real_literature_extraction": 0,
        "paper193_replay": 0,
        "paper167_execution": 0,
        "basis_decomposition": 0,
        "heldout_decomposition": 0,
    }:
        fail("qualification accounting")


def validate_schema(schema: dict[str, Any]) -> None:
    committed = json.loads(SCHEMA_PATH.read_text())
    if schema != committed:
        fail("schema differs from committed schema")
    base = json.loads((BASE / "research/paper2/extraction_systemone_decision_v2.schema.json").read_text())
    expected = copy.deepcopy(base)
    expected["$id"] = expected["$id"].replace("_v2.", "_v3.")
    expected["title"] = "Paper 2 SystemOne Decision Record v3"
    expected["description"] = "Dependency-aware finite decision record compiled deterministically into ClaimIR v1; synthetic qualification only."
    expected["properties"]["schema_version"]["const"] = VERSION
    if schema != expected:
        fail("decision schema must preserve v2 structural invariants")
    v2_equivalent = copy.deepcopy(schema)
    v2_equivalent["properties"]["schema_version"]["const"] = v2.DECISION_VERSION
    v2.validate_decision_schema(v2_equivalent)
    if schema["properties"]["schema_version"]["const"] != VERSION:
        fail("v3 schema version")


def seed_options(source: dict[str, Any]) -> dict[str, str]:
    options = {"NONE": "No node at this slot"}
    for sid in spans_of(source):
        for role in sorted(ROLES):
            options[f"{sid}::{role}"] = f"source span {sid}, role {role}"
    return options


def stage1(source: dict[str, Any]) -> dict[str, Any]:
    spans = spans_of(source)
    questions = {
        "claim_type": choice({x: x for x in sorted(CLAIM_TYPES)}, "Classify the source claim."),
        "modality": choice({x: x for x in sorted(MODALITIES)}, "Classify source-supported modality."),
    }
    for field in SCOPE:
        for sid in spans:
            questions[f"scope__{field}__{sid}"] = choice(
                {"yes": "restricts claim applicability", "no": "does not restrict claim applicability"},
                f"Does {sid} restrict the applicability or domain of the represented claim as scope.{field}? Mere historical provenance, citation/date mention, background, evidential support, or comparison provenance is not scope.",
            )
    for slot in SLOTS:
        questions[f"{slot}__seed"] = choice(
            seed_options(source),
            f"Bind source-grounded referent for {slot} before dependent fields. NONE means absent; choose __unresolved__ if two referents share a handle or the source does not distinguish them.",
        )
    check_bounds(1, questions)
    return questions


def resolved(answers: dict[str, str], name: str) -> str:
    if answers[name] == U:
        raise v2.DecisionUnresolved(f"{name}: applicable required decision unresolved")
    return answers[name]


def bindings(source: dict[str, Any], first: dict[str, str]) -> dict[str, tuple[str, str]]:
    check_answers(stage1(source), first)
    bound = {}
    seen = set()
    for slot in SLOTS:
        seed = resolved(first, f"{slot}__seed")
        if seed == "NONE":
            continue
        if seed not in seed_options(source) or seed in seen:
            fail("duplicate or unknown node referent handle")
        seen.add(seed)
        anchor, role = seed.split("::", 1)
        bound[slot] = (anchor, role)
    if not bound:
        fail("ClaimIR requires at least one bound node")
    return bound


def tuple_options(bound: dict[str, tuple[str, str]]) -> dict[str, str]:
    options = {"NONE": "No relation in this slot"}
    for a in bound:
        options[a] = f"unary relation on {a}"
        for b in bound:
            if a != b and bound[a][0] != bound[b][0]:
                options[f"{a}::{b}"] = f"ordered binary relation from {a} to {b}"
    return options


def stage2(source: dict[str, Any], first: dict[str, str]) -> dict[str, Any]:
    bound = bindings(source, first)
    for name in stage1(source):
        resolved(first, name)
    questions = {}
    for slot, (anchor, _) in bound.items():
        questions[f"{slot}__grounding"] = choice({x: x for x in sorted(GROUNDING)}, f"Grounding for bound referent {slot}.")
        for sid in spans_of(source):
            if sid != anchor:
                questions[f"{slot}__span__{sid}"] = choice({"yes": "also grounds", "no": "does not ground"}, f"Does {sid} also ground {slot}? Anchor {anchor} is included by construction.")
    for slot in RELATIONS_SLOTS:
        questions[f"{slot}__tuple"] = choice(tuple_options(bound), f"Select the finite relation argument tuple for {slot}, or NONE. Relation-slot referent identity remains underdetermined by #200.")
    check_bounds(2, questions)
    return questions


def stage3(source: dict[str, Any], first: dict[str, str], second: dict[str, str]) -> dict[str, Any]:
    q2 = stage2(source, first)
    check_answers(q2, second)
    for name in q2:
        resolved(second, name)
    questions = {}
    for slot in RELATIONS_SLOTS:
        tuple_value = resolved(second, f"{slot}__tuple")
        if tuple_value == "NONE":
            continue
        questions[f"{slot}__kind"] = choice({x: x for x in sorted(RELATIONS)}, f"Relation kind for {slot}.")
        questions[f"{slot}__grounding"] = choice({x: x for x in sorted(GROUNDING)}, f"Grounding for {slot}.")
        for sid in spans_of(source):
            questions[f"{slot}__span__{sid}"] = choice({"yes": "grounds", "no": "does not ground"}, f"Does {sid} ground {slot}?")
    check_bounds(3, questions)
    return questions


def check_bounds(stage: int, questions: dict[str, Any]) -> None:
    maxima = (20, 11, 10)
    if len(questions) > maxima[stage - 1]:
        fail("stage question bound exceeded")
    if any(len(q["criteria"]) > 29 for q in questions.values()):
        fail("finite choice bound exceeded")


def check_answers(questions: dict[str, Any], answers: dict[str, str]) -> None:
    if set(answers) != set(questions):
        fail("answers must match emitted questions exactly")
    for name, answer in answers.items():
        if not isinstance(answer, str) or answer not in questions[name]["criteria"]:
            fail(f"answer outside finite surface: {name}")


def parse_round(source: dict[str, Any], interpretation: str, model: str, questions: dict[str, Any], response: dict[str, Any]) -> dict[str, str]:
    request = {
        "model": model,
        "state": {"source": source, "interpretation": interpretation, "authority_rule": "Original source authoritative; Normal text advisory. Applicable uncertainty is __unresolved__."},
        "questions": questions,
    }
    return v2.parse_systemone_response(request, response)


def decision_from_rounds(source: dict[str, Any], first: dict[str, str], second: dict[str, str], third: dict[str, str]) -> dict[str, Any]:
    bound = bindings(source, first)
    check_answers(stage2(source, first), second)
    check_answers(stage3(source, first, second), third)
    claim_type = resolved(first, "claim_type")
    modality = resolved(first, "modality")
    scope = {field: [sid for sid in spans_of(source) if resolved(first, f"scope__{field}__{sid}") == "yes"] for field in SCOPE}
    nodes = []
    for slot, (anchor, role) in bound.items():
        refs = [anchor] + [sid for sid in spans_of(source) if sid != anchor and resolved(second, f"{slot}__span__{sid}") == "yes"]
        nodes.append({"slot": slot, "role": role, "anchor_span_id": anchor, "source_span_ids": refs, "grounding": resolved(second, f"{slot}__grounding")})
    relations = []
    for slot in RELATIONS_SLOTS:
        selected = resolved(second, f"{slot}__tuple")
        if selected == "NONE":
            continue
        args = selected.split("::")
        refs = [sid for sid in spans_of(source) if resolved(third, f"{slot}__span__{sid}") == "yes"]
        relations.append({"slot": slot, "kind": resolved(third, f"{slot}__kind"), "arguments": args, "source_span_ids": refs, "grounding": resolved(third, f"{slot}__grounding")})
    decision = {"schema_version": VERSION, "bundle_id": source["bundle_id"], "claim_type": claim_type, "modality": modality, "scope": scope, "nodes": nodes, "relations": relations}
    validate_decision(decision, source)
    return decision


def v2_projection(decision: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(decision)
    result["schema_version"] = v2.DECISION_VERSION
    return result


def validate_decision(decision: dict[str, Any], source: dict[str, Any]) -> None:
    if not isinstance(decision, dict) or decision.get("schema_version") != VERSION:
        fail("v3 decision version")
    v2.validate_decision(v2_projection(decision), source)
    seeds = [f"{node['anchor_span_id']}::{node['role']}" for node in decision["nodes"]]
    if len(seeds) != len(set(seeds)):
        fail("duplicate node referent handle")


def compile_candidate(source: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    validate_decision(decision, source)
    return v2.compile_candidate(source, v2_projection(decision))


def assemble_synthetic_claim(source: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    claim = v2.assemble_synthetic_claim(source, candidate)
    claim["extraction"]["extractor"] = "synthetic-two-pass-systemone-v3"
    claim["extraction"]["extractor_version"] = "v3"
    claim["extraction"]["procedure_version"] = MANIFEST_VERSION
    validate_claim_ir(claim)
    return claim


def classify(source: dict[str, Any], first: dict[str, str], second: dict[str, str], third: dict[str, str]) -> dict[str, Any]:
    try:
        decision = decision_from_rounds(source, first, second, third)
    except v2.DecisionUnresolved as exc:
        return {"outcome": "EXTRACTION_ABSTAIN", "reason": "DecisionUnresolved", "field": str(exc).split(":", 1)[0], "candidate": None, "claim_ir": None}
    candidate = compile_candidate(source, decision)
    claim = assemble_synthetic_claim(source, candidate)
    return {"outcome": "VALID_CLAIM_IR", "decision": decision, "candidate": candidate, "claim_ir": claim}


def answer_defaults(questions: dict[str, Any]) -> dict[str, str]:
    return {name: next(x for x in q["criteria"] if x != U) for name, q in questions.items()}


def scope_fixture_decision(manifest: dict[str, Any], fixture: str, field: str) -> dict[str, Any]:
    case = manifest["scope_fixtures"][fixture]
    source = v2.synthetic_source([case["s1"], case["s2"]], bundle_id="B9206" if fixture == "temporal" else "B9207")
    first = answer_defaults(stage1(source))
    first["n1__seed"] = "s2::condition"
    first["n2__seed"] = first["n3__seed"] = "NONE"
    for name in stage1(source):
        if name.startswith("scope__"):
            first[name] = "no"
    first[f"scope__{field}__s2"] = "yes"
    second = answer_defaults(stage2(source, first))
    second["r1__tuple"] = second["r2__tuple"] = "NONE"
    third = answer_defaults(stage3(source, first, second))
    return decision_from_rounds(source, first, second, third)


def expect_failure(call, label: str) -> None:
    try:
        call()
    except (v2.TwoPassV2Error, KeyError, ValueError):
        return
    raise AssertionError(f"{label}: expected failure")


def self_test() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    schema = json.loads(SCHEMA_PATH.read_text())
    validate_manifest(manifest)
    validate_schema(schema)
    source = v2.synthetic_source(["Synthetic state A.", "Synthetic state B.", "A depends on B."], bundle_id="B9203")
    q1 = stage1(source)
    a1 = answer_defaults(q1)
    a1.update({"claim_type": "relation", "modality": "descriptive", "n1__seed": "s1::state_or_structure", "n2__seed": "s2::response_or_outcome", "n3__seed": "NONE"})
    for name in q1:
        if name.startswith("scope__"):
            a1[name] = "no"
    q2 = stage2(source, a1)
    a2 = answer_defaults(q2)
    a2.update({"n1__grounding": "explicit", "n2__grounding": "explicit", "r1__tuple": "n1::n2", "r2__tuple": "NONE"})
    q3 = stage3(source, a1, a2)
    a3 = answer_defaults(q3)
    a3.update({"r1__kind": "depends_on", "r1__grounding": "explicit", "r1__span__s3": "yes"})
    out = classify(source, a1, a2, a3)
    if out["outcome"] != "VALID_CLAIM_IR":
        raise AssertionError("valid fixture")
    checks = {}
    checks["R1"] = all("__active" not in name for name in q1) and "n1__seed" in q1
    collision_source = v2.synthetic_source(["Two synthetic states share one atomic evidence unit and the same role."], bundle_id="B9204")
    collision_first = answer_defaults(stage1(collision_source)); collision_first["n1__seed"] = U
    checks["R2"] = classify(collision_source, collision_first, {}, {})["outcome"] == "EXTRACTION_ABSTAIN"
    checks["R3"] = "n1::n1" not in q2["r1__tuple"]["criteria"]
    checks["R4"] = all("n3" not in x for x in q2["r1__tuple"]["criteria"])
    same = copy.deepcopy(a1); same["n2__seed"] = "s1::response_or_outcome"
    same_options = stage2(source, same)["r1__tuple"]["criteria"]
    checks["R5"] = "n1::n2" not in same_options and "n2::n1" not in same_options
    checks["R6"] = scope_fixture_decision(manifest, "temporal", "temporal_scope")["scope"]["temporal_scope"] == manifest["scope_fixtures"]["temporal"]["expected_temporal_scope"]
    checks["R7"] = scope_fixture_decision(manifest, "conditions", "conditions")["scope"]["conditions"] == manifest["scope_fixtures"]["conditions"]["expected_conditions"]
    checks["R8"] = all(not x.startswith("n3__") for x in q2) and all(not x.startswith("r2__") for x in q3)
    unresolved = copy.deepcopy(a2); unresolved["n1__grounding"] = U
    abstain = classify(source, a1, unresolved, a3)
    checks["R9"] = abstain["outcome"] == "EXTRACTION_ABSTAIN" and abstain["candidate"] is None and abstain["claim_ir"] is None
    checks["R10"] = checks["R8"] and checks["R9"] and abstain["field"] == "n1__grounding"
    checks["R11"] = "n1__span__s1" not in q2 and out["decision"]["nodes"][0]["source_span_ids"][0] == "s1"
    checks["R12"] = all(manifest["qualification"][x] == 0 for x in ("real_model_calls", "real_server_launches", "real_literature_extraction", "paper193_replay", "paper167_execution"))
    checks["R13"] = out["claim_ir"]["schema_version"] == "paper2-claim-ir-v1" and bool(validate_claim_ir(out["claim_ir"]))
    mutant = copy.deepcopy(out["decision"]); mutant["relations"][0]["arguments"] = ["n1", "n1"]
    expect_failure(lambda: compile_candidate(source, mutant), "R14 invalid tuple")
    checks["R14"] = True
    advisory = "Normal claims an unsupported opposite relation and false scope."
    parsed = parse_round(source, advisory, "synthetic", q1, {"model": "synthetic", "answers": {name: {"type": "choice", "choice": answer} for name, answer in a1.items()}, "usage": {"output_tokens": 0}})
    checks["R15"] = parsed == a1 and canonical_json_bytes(decision_from_rounds(source, parsed, a2, a3)) == canonical_json_bytes(out["decision"])
    repeat = classify(source, a1, a2, a3)
    checks["R16"] = all(canonical_json_bytes(out[x]) == canonical_json_bytes(repeat[x]) for x in ("decision", "candidate", "claim_ir"))
    max_source = v2.synthetic_source(["A", "B", "C"], bundle_id="B9299")
    max_first = answer_defaults(stage1(max_source)); max_first.update({"n1__seed": "s1::condition", "n2__seed": "s2::criterion", "n3__seed": "s3::probe"})
    max_second = answer_defaults(stage2(max_source, max_first)); max_second.update({"r1__tuple": "n1::n2", "r2__tuple": "n2::n3"})
    checks["R17"] = [len(stage1(max_source)), len(stage2(max_source, max_first)), len(stage3(max_source, max_first, max_second))] == [20, 11, 10] and max(len(q["criteria"]) for q in stage1(max_source).values()) == 29
    for label, ok in checks.items():
        if not ok:
            raise AssertionError(f"{label} FAIL")
        print(f"{label}=PASS")
    destructive_tests(manifest, source, a1, a2, a3, out)
    print("SYSTEMONE_V3_SYNTHETICALLY_QUALIFIED")


def destructive_tests(manifest, source, a1, a2, a3, out) -> None:
    q1 = stage1(source); q2 = stage2(source, a1); q3 = stage3(source, a1, a2)
    mutants = []
    x = copy.deepcopy(q1); x["n1__active"] = choice({"yes": "yes", "no": "no"}, "anonymous active")
    mutants.append(("anonymous activation", lambda x=x: assert_surface(1, source, {}, x)))
    for label, token in (("duplicate relation argument", "n1::n1"), ("inactive relation argument", "n1::n3")):
        x = copy.deepcopy(q2); x["r1__tuple"]["criteria"][token] = "bad"
        mutants.append((label, lambda x=x: assert_surface(2, source, a1, x)))
    same = copy.deepcopy(a1); same["n2__seed"] = "s1::response_or_outcome"
    x = stage2(source, same); x["r1__tuple"]["criteria"]["n1::n2"] = "bad"
    mutants.append(("same-anchor binary", lambda x=x: assert_surface(2, source, same, x)))
    x = copy.deepcopy(manifest); x["bounded_surface"]["scope_semantics"] = "scope is any contributing evidence"
    mutants.append(("remove applicability semantics", lambda x=x: validate_manifest(x)))
    for label, field, sid in (("provenance as temporal scope", "temporal_scope", "s1"), ("evidence as conditions", "conditions", "s1")):
        x = copy.deepcopy(a1); x[f"scope__{field}__{sid}"] = "yes"
        mutants.append((label, lambda x=x, field=field, sid=sid: assert_scope_fixture(x, field, sid)))
    x = copy.deepcopy(q2); x["n3__grounding"] = choice({"explicit": "explicit"}, "inactive")
    mutants.append(("inactive field emitted", lambda x=x: assert_surface(2, source, a1, x)))
    x = copy.deepcopy(a2); x["n1__grounding"] = U
    mutants.append(("N/A equals unresolved", lambda x=x: assert_resolved(classify(source, a1, x, a3))))
    mutants.append(("active unresolved compiles", lambda x=x: assert_resolved(classify(source, a1, x, a3))))
    x = copy.deepcopy(out["decision"]); x["nodes"][0]["source_span_ids"] = []
    mutants.append(("zero node grounding", lambda x=x: compile_candidate(source, x)))
    x = copy.deepcopy(out["decision"]); x["relations"][0]["arguments"] = ["n1", "n1"]
    mutants.append(("semantic repair", lambda x=x: compile_candidate(source, x)))
    x = copy.deepcopy(manifest); x["claim_ir_schema"] = "paper2-claim-ir-v2"
    mutants.append(("ClaimIR version", lambda x=x: validate_manifest(x)))
    x = copy.deepcopy(manifest); x["real_model_calls_authorized"] = True
    mutants.append(("real model authorization", lambda x=x: validate_manifest(x)))
    x = copy.deepcopy(manifest); x["bound_parent_blobs"]["scripts/paper2_extraction_two_pass_systemone_v2.py"] = "0" * 40
    mutants.append(("v2 blob identity", lambda x=x: validate_manifest(x)))
    for label, call in mutants:
        expect_failure(call, label)
        print(f"MUTATION {label}=REJECTED")


def assert_surface(stage: int, source, prior, proposed) -> None:
    actual = stage1(source) if stage == 1 else stage2(source, prior)
    if proposed != actual:
        fail("mutated finite surface")


def assert_scope_fixture(answers, field: str, sid: str) -> None:
    if answers[f"scope__{field}__{sid}"] != "no":
        fail("non-applicability fixture entered scope")


def assert_resolved(outcome) -> None:
    if outcome["outcome"] != "VALID_CLAIM_IR":
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
