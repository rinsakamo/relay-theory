#!/usr/bin/env python3
"""Validate the synthetic Paper 2 #200 decision-surface audit artifact.

This validator is intentionally repository-local and deterministic.  It checks
the frozen v2 identities, the bounded dependency graph, all twelve synthetic
probes, and the no-real-operation boundary.  It never calls a model, starts a
server, reads literature, or mutates a v2 input.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable


REPOSITORY = "rinsakamo/relay-theory"
SCHEMA_VERSION = "paper2-extraction-decision-surface-audit-v1"
ARTIFACT_RELATIVE_PATH = Path(
    "research/paper2/extraction_decision_surface_audit_v1.json"
)

EXPECTED_BOUND_INPUTS = [
    {
        "role": "frozen_v2_decision_schema",
        "path": "research/paper2/extraction_systemone_decision_v2.schema.json",
        "blob_sha": "5933030119a903079a9eadb69e08d9326463339c",
    },
    {
        "role": "frozen_v2_contract",
        "path": "research/paper2/extraction_two_pass_systemone_v2.json",
        "blob_sha": "ed00b7458c068eb9add6a23dbf0e8282e06941d4",
        "mutation": "forbidden",
    },
    {
        "role": "frozen_v2_compiler",
        "path": "scripts/paper2_extraction_two_pass_systemone_v2.py",
        "blob_sha": "f789fcfb35af03a52e9193e6e6ebf5f86271707a",
        "mutation": "forbidden",
    },
    {
        "role": "frozen_claim_ir_v1_schema",
        "path": "research/paper2/claim_ir_v1.schema.json",
        "blob_sha": "963f54bd61c3112daa046fa191e3194d47db0768",
    },
    {
        "role": "frozen_extraction_procedure",
        "path": "research/paper2/extraction_procedure_v1.json",
        "blob_sha": "5e1b6c17c8cd9b4b3455de137b99a90f870233d0",
    },
    {
        "role": "parent_postmortem_artifact",
        "path": "research/paper2/extraction_zero_yield_postmortem_v1.json",
        "blob_sha": "4f09089eef5db543e17e782ee96a7b4e3efa2ff6",
    },
]

ALLOWED_TAXONOMY = [
    "NO_DEFECT",
    "POSTPARSE_VALIDATION_ONLY",
    "QUESTION_REFERENT_UNDERDEFINED",
    "QUESTION_DEPENDENCY_LEAK",
    "CHOICE_VOCABULARY_INSUFFICIENT",
    "SCOPE_SEMANTICS_UNDERDEFINED",
    "NOT_APPLICABLE_STATE_MISSING",
    "AUDIT_UNDERDETERMINED",
]
EARNED_CLASSES = [
    "QUESTION_REFERENT_UNDERDEFINED",
    "QUESTION_DEPENDENCY_LEAK",
    "SCOPE_SEMANTICS_UNDERDEFINED",
    "NOT_APPLICABLE_STATE_MISSING",
]
PROBE_IDS = [f"P{index}" for index in range(1, 13)]
EXPECTED_PROBE_CLASSIFICATIONS = {
    "P1": "QUESTION_REFERENT_UNDERDEFINED",
    "P2": "QUESTION_REFERENT_UNDERDEFINED",
    "P3": "QUESTION_DEPENDENCY_LEAK",
    "P4": "QUESTION_DEPENDENCY_LEAK",
    "P5": "QUESTION_DEPENDENCY_LEAK",
    "P6": "SCOPE_SEMANTICS_UNDERDEFINED",
    "P7": "SCOPE_SEMANTICS_UNDERDEFINED",
    "P8": "NO_DEFECT",
    "P9": "NO_DEFECT",
    "P10": "NOT_APPLICABLE_STATE_MISSING",
    "P11": "QUESTION_DEPENDENCY_LEAK",
    "P12": "NO_DEFECT",
}
EXPECTED_PROBE_WIRE = {probe_id: "PASS" for probe_id in PROBE_IDS}
EXPECTED_PROBE_DECISIONS = {
    "P1": "UNDERDEFINED",
    "P2": "UNDERDEFINED",
    "P3": "FAIL",
    "P4": "FAIL",
    "P5": "FAIL",
    "P6": "UNDERDEFINED",
    "P7": "UNDERDEFINED",
    "P8": "PASS",
    "P9": "DecisionUnresolved",
    "P10": "PASS",
    "P11": "FAIL",
    "P12": "PASS",
}
REQUIRED_GRAPH_EDGES = {
    ("node_referent", "node_active"),
    ("node_active", "node_role"),
    ("node_active", "node_anchor"),
    ("node_active", "node_source_spans"),
    ("node_active", "node_grounding"),
    ("node_active", "active_node_set"),
    ("node_anchor", "node_anchor_distinctions"),
    ("active_node_set", "relation_arg1"),
    ("active_node_set", "relation_arg2"),
    ("node_anchor_distinctions", "relation_arg1"),
    ("node_anchor_distinctions", "relation_arg2"),
}


class ValidationError(ValueError):
    """Raised when the committed artifact is not the qualified artifact."""


def fail(message: str) -> None:
    raise ValidationError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def require_type(value: Any, expected: type, path: str) -> None:
    require(isinstance(value, expected), f"{path}: expected {expected.__name__}")


def require_equal(actual: Any, expected: Any, path: str) -> None:
    require(actual == expected, f"{path}: expected {expected!r}, got {actual!r}")


def require_string(value: Any, path: str) -> None:
    require(isinstance(value, str) and value, f"{path}: expected non-empty string")


def require_git_sha(value: Any, path: str) -> None:
    require(
        isinstance(value, str)
        and len(value) == 40
        and all(character in "0123456789abcdef" for character in value),
        f"{path}: expected lowercase Git SHA-1",
    )


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def artifact_path(repo_root: Path) -> Path:
    return repo_root / ARTIFACT_RELATIVE_PATH


def validate_root(value: Any) -> dict[str, Any]:
    require_type(value, dict, "artifact")
    artifact = value
    require_equal(artifact.get("schema_version"), SCHEMA_VERSION, "schema_version")
    require_equal(artifact.get("owner_issue"), 200, "owner_issue")
    require_equal(artifact.get("parent_postmortem_issue"), 197, "parent_postmortem_issue")
    require_equal(
        artifact.get("status"),
        "DECISION_SURFACE_AUDIT_QUALIFIED",
        "status",
    )
    require_equal(artifact.get("architecture_consequence"), "NONE", "architecture_consequence")
    require_equal(
        artifact.get("terminal_owner_classification"),
        "DECISION_SURFACE_AUDIT_QUALIFIED",
        "terminal_owner_classification",
    )
    require_equal(
        artifact.get("scientific_classification"),
        "CURRENT_V2_DECISION_SURFACE_HAS_LOCAL_SEMANTIC_DEPENDENCY_DEFECTS",
        "scientific_classification",
    )
    return artifact


def validate_authority(value: Any) -> None:
    require_type(value, dict, "authority")
    require_equal(value.get("repository"), REPOSITORY, "authority.repository")
    require_equal(
        value.get("fresh_starting_main"),
        "3b3d6825def826784fe3f1ab4eef472c76d9bbe1",
        "authority.fresh_starting_main",
    )
    require_equal(
        value.get("fresh_starting_tree"),
        "782f00d2fafa1ed0272a801097c8d3c6a423128c",
        "authority.fresh_starting_tree",
    )
    ruleset = value.get("ruleset")
    require_type(ruleset, dict, "authority.ruleset")
    require_equal(ruleset.get("id"), 23769009, "authority.ruleset.id")
    require_equal(ruleset.get("name"), "main-protection", "authority.ruleset.name")
    require_equal(ruleset.get("enforcement"), "active", "authority.ruleset.enforcement")
    require_equal(ruleset.get("allowed_merge_methods"), ["squash"], "authority.ruleset.allowed_merge_methods")
    require_equal(ruleset.get("required_linear_history"), True, "authority.ruleset.required_linear_history")
    require_equal(
        ruleset.get("required_review_thread_resolution"),
        True,
        "authority.ruleset.required_review_thread_resolution",
    )
    require_equal(
        value.get("repository_authority_files"),
        [
            {"path": ".ai/README.md", "blob_sha": "d62d79f2016b8cba2ee555197f0bbef92f58282b"},
            {"path": ".ai/forge-protocol.md", "blob_sha": "25c15145c17979ae2c4e95e18c89a47669ff5ef5"},
        ],
        "authority.repository_authority_files",
    )
    require_equal(
        value.get("open_pull_requests_at_start"),
        [
            {
                "number": 123,
                "base": "main",
                "head": "paper-1-draft-ja",
                "head_sha": "290748d2a0f60374c77c8ed04cb7121fae459c8b",
                "draft": True,
            }
        ],
        "authority.open_pull_requests_at_start",
    )
    require_equal(value.get("latest_audit_comment"), 5833163702, "authority.latest_audit_comment")


def validate_bound_inputs(value: Any, repo_root: Path) -> None:
    require_equal(value, EXPECTED_BOUND_INPUTS, "bound_inputs")
    for index, expected in enumerate(EXPECTED_BOUND_INPUTS):
        path = repo_root / expected["path"]
        require(path.is_file(), f"bound_inputs[{index}]: missing {expected['path']}")
        actual = git_blob_sha(path)
        require_equal(actual, expected["blob_sha"], f"current blob {expected['path']}")


def validate_audit_criterion(value: Any) -> None:
    require_type(value, dict, "audit_criterion")
    require_equal(
        value.get("text"),
        "If a finite choice is already impossible from fixed finite state, the question surface must not present it as locally admissible.",
        "audit_criterion.text",
    )
    require_equal(value.get("declaration"), "DECLARED_AUDIT_CRITERION", "audit_criterion.declaration")
    require_equal(value.get("ontology"), False, "audit_criterion.ontology")


def validate_graph(value: Any) -> None:
    require_type(value, dict, "dependency_graph")
    require_equal(
        value.get("graph_kind"),
        "semantic_and_wire_dependency_graph",
        "dependency_graph.graph_kind",
    )
    require_equal(
        value.get("relation_slot_referent_audit"),
        "AUDIT_UNDERDETERMINED",
        "dependency_graph.relation_slot_referent_audit",
    )
    field_families = value.get("field_families")
    require_type(field_families, list, "dependency_graph.field_families")
    expected_families = [
        "claim_type",
        "modality",
        "scope_membership",
        "node_referent",
        "node_active",
        "node_role",
        "node_anchor",
        "node_source_spans",
        "node_grounding",
        "relation_referent",
        "relation_active",
        "relation_kind",
        "relation_arg1",
        "relation_arg2",
        "relation_source_spans",
        "relation_grounding",
    ]
    require_equal(
        [item.get("field_family") for item in field_families],
        expected_families,
        "dependency_graph.field_families.order",
    )
    required_keys = {
        "field_family",
        "referent",
        "semantic_prerequisites",
        "wire_prerequisites",
        "not_applicable_condition",
        "downstream_invariants",
        "current_enforcement_point",
    }
    for index, item in enumerate(field_families):
        path = f"dependency_graph.field_families[{index}]"
        require_type(item, dict, path)
        require_equal(set(item), required_keys, f"{path}.keys")
        require_string(item["referent"], f"{path}.referent")
        for key in ("semantic_prerequisites", "wire_prerequisites", "downstream_invariants"):
            require_type(item[key], list, f"{path}.{key}")
            require(item[key], f"{path}.{key}: must not be empty")
        require_string(item["not_applicable_condition"], f"{path}.not_applicable_condition")
        require_string(item["current_enforcement_point"], f"{path}.current_enforcement_point")
    require_equal(value.get("derived_nodes"), ["active_node_set", "node_anchor_distinctions"], "dependency_graph.derived_nodes")

    edges = value.get("edges")
    require_type(edges, list, "dependency_graph.edges")
    edge_pairs: list[tuple[str, str]] = []
    known_nodes = set(expected_families) | {"active_node_set", "node_anchor_distinctions"}
    for index, edge in enumerate(edges):
        path = f"dependency_graph.edges[{index}]"
        require_type(edge, dict, path)
        require_equal(set(edge), {"from", "to"}, f"{path}.keys")
        source = edge["from"]
        target = edge["to"]
        require(source in known_nodes, f"{path}.from: unknown node {source!r}")
        require(target in known_nodes, f"{path}.to: unknown node {target!r}")
        require(source != target, f"{path}: self-edge is not allowed")
        edge_pairs.append((source, target))
    require(REQUIRED_GRAPH_EDGES.issubset(set(edge_pairs)), "dependency_graph.edges: required dependency edge missing")

    adjacency: dict[str, list[str]] = {node: [] for node in known_nodes}
    for source, target in edge_pairs:
        adjacency[source].append(target)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            fail(f"dependency_graph.edges: cycle through {node}")
        if node in visited:
            return
        visiting.add(node)
        for child in adjacency[node]:
            visit(child)
        visiting.remove(node)
        visited.add(node)

    for node in known_nodes:
        visit(node)


def probes_by_id(value: Any) -> dict[str, dict[str, Any]]:
    require_type(value, dict, "synthetic_probe_suite")
    require_equal(value.get("synthetic_only"), True, "synthetic_probe_suite.synthetic_only")
    require_equal(value.get("probe_count"), 12, "synthetic_probe_suite.probe_count")
    probes = value.get("probes")
    require_type(probes, list, "synthetic_probe_suite.probes")
    require_equal([probe.get("id") for probe in probes], PROBE_IDS, "synthetic_probe_suite.probes.ids")
    return {probe["id"]: probe for probe in probes}


def validate_probes(value: Any) -> None:
    probes = probes_by_id(value)
    for probe_id in PROBE_IDS:
        probe = probes[probe_id]
        path = f"synthetic_probe_suite.probes[{probe_id}]"
        require_type(probe, dict, path)
        require_string(probe.get("synthetic_case"), f"{path}.synthetic_case")
        require_equal(
            probe.get("expected_wire_result"),
            EXPECTED_PROBE_WIRE[probe_id],
            f"{path}.expected_wire_result",
        )
        require_equal(
            probe.get("expected_semantic_decision"),
            EXPECTED_PROBE_DECISIONS[probe_id],
            f"{path}.expected_semantic_decision",
        )
        require_equal(
            probe.get("classification"),
            EXPECTED_PROBE_CLASSIFICATIONS[probe_id],
            f"{path}.classification",
        )
        for key in ("real_literature_extraction", "real_model_calls", "real_server_launches"):
            require(probe.get(key, False) is False, f"{path}.{key}: real operation is forbidden")

    require_equal(probes["P3"].get("failure"), "duplicate relation arguments are forbidden", "P3.failure")
    require_equal(probes["P4"].get("failure"), "relation argument names inactive node", "P4.failure")
    require_equal(probes["P5"].get("failure"), "distinct relation arguments require distinct node anchors", "P5.failure")
    require_equal(probes["P11"].get("failure"), "active node requires at least one source span", "P11.failure")

    require_equal(probes["P8"].get("inactive_behavior"), "ignored_without_abstention", "P8.inactive_behavior")
    require_equal(probes["P8"].get("must_not_abstain"), True, "P8.must_not_abstain")
    require_equal(probes["P9"].get("active_unresolved_behavior"), "DecisionUnresolved", "P9.active_unresolved_behavior")
    require_equal(probes["P9"].get("must_abstain"), True, "P9.must_abstain")

    p10_wire = probes["P10"].get("wire_omission_test")
    require_type(p10_wire, dict, "P10.wire_omission_test")
    require_equal(p10_wire.get("omission_wire_result"), "FAIL", "P10.omission_wire_result")
    require_equal(p10_wire.get("omission_failure"), "exact full-wire coverage is required", "P10.omission_failure")
    require_equal(p10_wire.get("complete_wire_result"), "PASS", "P10.complete_wire_result")
    require_equal(p10_wire.get("complete_wire_inactive_values"), "arbitrary_or___unresolved__", "P10.complete_wire_inactive_values")
    require_equal(p10_wire.get("compile_equivalence_after_active_no"), True, "P10.compile_equivalence_after_active_no")
    require_equal(
        probes["P10"].get("n_a_conclusion"),
        "Semantically inactive dependent fields require explicit N/A semantics or omission; the current mandatory full wire supplies neither.",
        "P10.n_a_conclusion",
    )


def validate_taxonomy(value: Any) -> None:
    require_type(value, dict, "pressure_taxonomy")
    require_equal(value.get("allowed"), ALLOWED_TAXONOMY, "pressure_taxonomy.allowed")
    require_equal(value.get("earned"), EARNED_CLASSES, "pressure_taxonomy.earned")
    require_equal(value.get("not_earned"), ["CHOICE_VOCABULARY_INSUFFICIENT"], "pressure_taxonomy.not_earned")
    require_equal(value.get("relation_slot_referent"), "AUDIT_UNDERDETERMINED", "pressure_taxonomy.relation_slot_referent")
    require("CHOICE_VOCABULARY_INSUFFICIENT" not in value["earned"], "choice vocabulary insufficiency was incorrectly earned")


def validate_grand_null(value: Any) -> None:
    require_type(value, dict, "grand_null")
    require_equal(value.get("status"), "DESTROYED_BOUNDED_LOCAL_CLAUSES", "grand_null.status")
    require_equal(
        value.get("destroyed_clauses"),
        [
            "node activation always has a well-defined referent",
            "finite structurally impossible combinations are excluded before reconstruction",
            "scope membership uniquely distinguishes applicability from provenance/evidence",
            "all mandatory questions have meaningful semantics when inactive",
        ],
        "grand_null.destroyed_clauses",
    )
    require_equal(
        value.get("surviving_properties"),
        [
            "per-question finite vocabularies are valid",
            "exact full-wire completeness works",
            "deterministic postparse validation works",
            "inactive unresolved dependents do not manufacture abstention",
            "active required unresolved fails closed",
        ],
        "grand_null.surviving_properties",
    )


def validate_parent_linkage(value: Any) -> None:
    require_type(value, dict, "parent_postmortem_linkage")
    require_equal(value.get("issue"), 197, "parent_postmortem_linkage.issue")
    require_equal(value.get("terminal_classification"), "ZERO_YIELD_POSTMORTEM_UNDERDETERMINED", "parent_postmortem_linkage.terminal_classification")
    require_equal(value.get("scientific_subclass"), "ZERO_YIELD_EXPLAINED_BY_MIXED_EXTRACTION_BOUNDARIES", "parent_postmortem_linkage.scientific_subclass")
    require_equal(value.get("provenance_scope"), "BOUNDED_PROVENANCE_ONLY", "parent_postmortem_linkage.provenance_scope")
    require_equal(value.get("p3_independently_reproduces"), "the same failure class as #197 B0001 using synthetic data", "parent_postmortem_linkage.p3_independently_reproduces")
    require_equal(
        value.get("does_not_prove"),
        ["#200 defects caused B0001", "#200 defects caused the other #193 rows"],
        "parent_postmortem_linkage.does_not_prove",
    )


def validate_future_boundary(value: Any) -> None:
    require_type(value, dict, "future_boundary")
    require_equal(
        value.get("properties"),
        [
            "node referent must be bound before activation/role classification",
            "dependent finite choices should exclude choices already impossible from fixed state",
            "scope semantics must distinguish applicability restriction from provenance/evidential support",
            "semantically inactive dependent fields require explicit N/A semantics or omission",
        ],
        "future_boundary.properties",
    )
    for key in (
        "v3_created",
        "v3_authorized",
        "real_transaction_created",
        "real_transaction_authorized",
        "real_transaction_executed",
    ):
        require_equal(value.get(key), False, f"future_boundary.{key}")


def validate_accounting(value: Any) -> None:
    require_type(value, dict, "accounting")
    expected = {
        "real_model_calls": 0,
        "real_llama_server_launches": 0,
        "real_literature_extraction": 0,
        "replay_193": 0,
        "execution_167": 0,
        "basis_decomposition": 0,
        "v2_mutation": 0,
        "v2_compiler_mutation": 0,
        "v2_contract_mutation": 0,
        "claim_ir_mutation": 0,
        "retry": 0,
        "repair": 0,
    }
    require_equal(value, expected, "accounting")


def validate_scientific_result(value: Any) -> None:
    require_type(value, dict, "scientific_result")
    require_equal(value.get("terminal_owner_classification"), "DECISION_SURFACE_AUDIT_QUALIFIED", "scientific_result.terminal_owner_classification")
    require_equal(value.get("classification"), "CURRENT_V2_DECISION_SURFACE_HAS_LOCAL_SEMANTIC_DEPENDENCY_DEFECTS", "scientific_result.classification")
    require_equal(value.get("earned_local_classes"), EARNED_CLASSES, "scientific_result.earned_local_classes")
    require_equal(value.get("global_invalidity_claim"), False, "scientific_result.global_invalidity_claim")


def validate_artifact(value: Any, repo_root: Path) -> None:
    artifact = validate_root(value)
    validate_authority(artifact.get("authority"))
    validate_bound_inputs(artifact.get("bound_inputs"), repo_root)
    validate_audit_criterion(artifact.get("audit_criterion"))
    validate_graph(artifact.get("dependency_graph"))
    validate_probes(artifact.get("synthetic_probe_suite"))
    validate_taxonomy(artifact.get("pressure_taxonomy"))
    validate_grand_null(artifact.get("grand_null"))
    validate_parent_linkage(artifact.get("parent_postmortem_linkage"))
    validate_future_boundary(artifact.get("future_boundary"))
    for key in (
        "v3_created",
        "v3_authorized",
        "real_transaction_created",
        "real_transaction_authorized",
        "real_transaction_executed",
    ):
        require_equal(artifact.get(key), False, key)
    validate_accounting(artifact.get("accounting"))
    validate_scientific_result(artifact.get("scientific_result"))


def load_artifact(repo_root: Path) -> dict[str, Any]:
    path = artifact_path(repo_root)
    require(path.is_file(), f"missing artifact: {ARTIFACT_RELATIVE_PATH}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read artifact: {exc}")
    require_type(value, dict, "artifact")
    return value


def probe(value: dict[str, Any], probe_id: str) -> dict[str, Any]:
    probes = value["synthetic_probe_suite"]["probes"]
    return next(item for item in probes if item["id"] == probe_id)


def run_self_test(artifact: dict[str, Any], repo_root: Path) -> None:
    validate_artifact(artifact, repo_root)
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("P1 classification", lambda item: probe(item, "P1").__setitem__("classification", "NO_DEFECT")),
        ("P3 wire result", lambda item: probe(item, "P3").__setitem__("expected_wire_result", "FAIL")),
        ("P3 failure string", lambda item: probe(item, "P3").__setitem__("failure", "wrong failure")),
        ("P4 classification", lambda item: probe(item, "P4").__setitem__("classification", "NO_DEFECT")),
        ("P5 expected decision result", lambda item: probe(item, "P5").__setitem__("expected_semantic_decision", "PASS")),
        ("P6 scope classification", lambda item: probe(item, "P6").__setitem__("classification", "NO_DEFECT")),
        ("P8 inactive behavior", lambda item: probe(item, "P8").__setitem__("inactive_behavior", "abstain")),
        ("P9 active unresolved behavior", lambda item: probe(item, "P9").__setitem__("active_unresolved_behavior", "PASS")),
        ("P10 N/A conclusion", lambda item: probe(item, "P10").__setitem__("n_a_conclusion", "N/A is already complete")),
        ("P11 failure string", lambda item: probe(item, "P11").__setitem__("failure", "not required")),
        (
            "dependency edge node_referent -> node_active",
            lambda item: item["dependency_graph"]["edges"].remove({"from": "node_referent", "to": "node_active"}),
        ),
        ("Grand Null status", lambda item: item["grand_null"].__setitem__("status", "NOT_DESTROYED")),
        (
            "scientific classification",
            lambda item: item.__setitem__("scientific_classification", "GLOBAL_INVALIDITY"),
        ),
        ("architecture consequence", lambda item: item.__setitem__("architecture_consequence", "CHANGE_REQUIRED")),
        ("v3_authorized flag", lambda item: item.__setitem__("v3_authorized", True)),
        ("real_transaction_authorized flag", lambda item: item.__setitem__("real_transaction_authorized", True)),
        (
            "bound v2 compiler blob",
            lambda item: item["bound_inputs"][2].__setitem__("blob_sha", "0" * 40),
        ),
    ]
    for name, mutation in mutations:
        candidate = copy.deepcopy(artifact)
        mutation(candidate)
        try:
            validate_artifact(candidate, repo_root)
        except ValidationError:
            continue
        fail(f"self-test mutation unexpectedly passed: {name}")
    print("PAPER2_EXTRACTION_DECISION_SURFACE_AUDIT_V1_SELFTEST_PASS")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run adversarial in-memory mutations")
    args = parser.parse_args(argv)
    repo_root = Path(__file__).resolve().parents[1]
    try:
        artifact = load_artifact(repo_root)
        if args.self_test:
            run_self_test(artifact, repo_root)
        else:
            validate_artifact(artifact, repo_root)
            print("PAPER2_EXTRACTION_DECISION_SURFACE_AUDIT_V1_VALID")
    except ValidationError as exc:
        print(f"VALIDATION_ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
