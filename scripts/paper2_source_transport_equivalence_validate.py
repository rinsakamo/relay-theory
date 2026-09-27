#!/usr/bin/env python3
"""Validate the Paper 2 #263 source-transport equivalence authority.

This is a synthetic/method qualification only.  It separates the frozen
scientific candidate identity from the public-web transport presentation while
preserving #239/#243 selection, rank, bounded projection, and fail-closed
capture semantics.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

BASE = Path(__file__).resolve().parent.parent
POLICY_PATH = BASE / "research/paper2/source_transport_equivalence_v1.json"

SCHEMA_VERSION = "paper2-source-transport-equivalence-v1"
STATE = "TRANSPORT_EQUIVALENCE_RULE_SYNTHETICALLY_QUALIFIED_ONLY"
RESULT = "GRAND_NULL_REJECTED_AT_AUTHORITY_STRUCTURE_LEVEL"

BOUND = {
    "research/paper2/designed_source_candidate_ledger_v1.json":
        "91da0cf304d03f0469df5c03ac7007f2040727e9",
    "research/paper2/designed_source_web_fulltext_manifest_v1.json":
        "be44887a8024bbf13c3a746452291e330349889a",
    "research/paper2/designed_source_capture_manifest_v1.json":
        "b406776e866ea938531da32ae5b2cc35b081ba42",
    "research/paper2/bounded_source_projection_v1.json":
        "6a1415f2e85554816b5c25a3de21a08a8ae2018b",
    "research/paper2/designed_source_projection_capture_v1.json":
        "776e6ce6311ad343f63bb6dc77f8761edaee7e55",
    "research/paper2/bounded_source_projection_input_v1.schema.json":
        "0867444ed163f80e186e8b8778c08c0fea72d8cd",
}

IDENTITY_FIELDS = [
    "slot_id",
    "activated_rank",
    "stable_identity",
    "title",
    "year",
    "source_type",
    "registry_reference",
    "author_lineage_key",
]

REQUIRED_LOCAL_PROVENANCE = [
    "actual_acquisition_route",
    "retrieved_at",
    "byte_size",
    "sha256",
    "transport_mode",
    "identity_attestation",
]

GATE = {
    "trigger_required": "FROZEN_REFERENCE_TRANSPORT_BLOCKED_OR_HUMAN_VERIFICATION_REQUIRED",
    "trigger_evidence_required": True,
    "alternate_route_predeclared_before_artifact_acceptance": True,
    "one_candidate_route_per_explicit_continuation": True,
    "public_web_only": True,
    "complete_full_text_required": True,
    "same_slot_required": True,
    "same_activated_rank_required": True,
    "same_stable_identity_required": True,
    "same_title_required": True,
    "same_year_required": True,
    "same_source_type_required": True,
    "same_scientific_candidate_required": True,
    "publication_version_identity_attestation_required": True,
    "source_native_abstract_boundary_required": True,
    "body_fallback_forbidden": True,
    "summary_or_paraphrase_forbidden": True,
    "claim_directed_route_choice_forbidden": True,
    "result_dependent_route_choice_forbidden": True,
    "downstream_outcome_visibility_forbidden": True,
    "reserve_rank_traversal_forbidden": True,
    "candidate_substitution_forbidden": True,
    "frozen_reference_locator_rewrite_forbidden": True,
    "byte_identity_may_be_claimed_only_if_measured": True,
    "fail_closed_on_equivalence_uncertainty": True,
}

AUTHORIZATION = {
    "b0003_alternate_route_download_for_equivalence_verification": True,
    "b0003_alternate_artifact_acceptance": False,
    "production_composed_capture": False,
    "model_execution": False,
    "claim_ir_extraction": False,
    "structural_signature_generation": False,
    "phi_mapping": False,
    "atlas_analysis": False,
}


class ValidationError(ValueError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def canonical_identity(value: Any) -> tuple[str, str]:
    if not isinstance(value, dict) or set(value) != {"kind", "value"}:
        fail("malformed stable identity")
    kind = value["kind"]
    ident = str(value["value"]).strip()
    if kind == "DOI":
        ident = ident.casefold().removeprefix("https://doi.org/").removeprefix("doi:")
    else:
        ident = ident.casefold()
    if not ident:
        fail("empty stable identity")
    return str(kind), ident


def by_slot(entries: list[dict[str, Any]], slot: str) -> dict[str, Any]:
    matches = [row for row in entries if row.get("slot_id") == slot]
    if len(matches) != 1:
        fail(f"{slot}: expected one frozen web entry")
    return matches[0]


def ledger_row(
    records: list[dict[str, Any]], slot: str, rank: int
) -> dict[str, Any]:
    matches = [
        row for row in records
        if row.get("slot_id") == slot and row.get("candidate_rank") == rank
    ]
    if len(matches) != 1:
        fail(f"{slot}/rank{rank}: expected one candidate row")
    return matches[0]


def capture_row(records: list[dict[str, Any]], bundle: str) -> dict[str, Any]:
    matches = [row for row in records if row.get("opaque_bundle_id") == bundle]
    if len(matches) != 1:
        fail(f"{bundle}: expected one capture descriptor")
    return matches[0]


def validate_bound_blobs(policy: dict[str, Any]) -> None:
    if policy.get("bound_repository_blobs") != BOUND:
        fail("bound repository blob set drift")
    for rel, expected in BOUND.items():
        actual = git_blob_sha((BASE / rel).read_bytes())
        if actual != expected:
            fail(f"bound authority changed: {rel}: {actual} != {expected}")


def validate(policy: Any) -> dict[str, Any]:
    if not isinstance(policy, dict):
        fail("policy root must be object")

    required = {
        "schema_version",
        "owner_issue",
        "parent_mapping_issue",
        "historical_accessibility_issue",
        "state",
        "grand_null",
        "result",
        "reason",
        "bound_repository_blobs",
        "authority_layers",
        "transport_equivalence_gate",
        "projection_semantics",
        "real_witnesses",
        "authorization",
        "destructive_requirements",
        "anti_overclaim",
        "architecture_consequence",
    }
    if set(policy) != required:
        fail(f"policy root keys drift: {sorted(set(policy) ^ required)}")

    if policy["schema_version"] != SCHEMA_VERSION:
        fail("schema version drift")
    if (
        policy["owner_issue"] != 263
        or policy["parent_mapping_issue"] != 239
        or policy["historical_accessibility_issue"] != 243
    ):
        fail("owner binding drift")
    if policy["state"] != STATE or policy["result"] != RESULT:
        fail("qualification state drift")
    if policy["architecture_consequence"] != "NONE":
        fail("architecture consequence overclaim")

    validate_bound_blobs(policy)

    layers = policy["authority_layers"]
    if set(layers) != {
        "scientific_candidate_identity",
        "frozen_reference_locator",
        "actual_acquisition_route",
        "acquired_artifact",
    }:
        fail("authority layer set drift")

    sci = layers["scientific_candidate_identity"]
    if (
        sci.get("intrinsic_for_this_transaction") is not True
        or sci.get("fields") != IDENTITY_FIELDS
        or sci.get("mutation_forbidden") is not True
    ):
        fail("scientific candidate identity policy drift")

    ref = layers["frozen_reference_locator"]
    if (
        ref.get("intrinsic_for_this_transaction") is not False
        or ref.get("field") != "public_fulltext_locator"
        or ref.get("mutation_forbidden_in_projection_input") is not True
    ):
        fail("reference locator semantics drift")

    route = layers["actual_acquisition_route"]
    if (
        route.get("repository_field") is not False
        or route.get("local_provenance_required") is not True
    ):
        fail("actual acquisition route semantics drift")

    artifact = layers["acquired_artifact"]
    if (
        artifact.get("local_only") is not True
        or artifact.get("required_provenance") != REQUIRED_LOCAL_PROVENANCE
    ):
        fail("artifact provenance policy drift")

    if policy["transport_equivalence_gate"] != GATE:
        fail("transport-equivalence gate drift")

    projection = policy["projection_semantics"]
    if projection != {
        "bounded_projection_authority": "#250",
        "complete_source_native_abstract_only": True,
        "alternate_route_does_not_change_projection_rule": True,
        "if_no_source_native_abstract": "PAPER2_SOURCE_CAPTURE_INSUFFICIENT",
        "if_complete_native_abstract_exceeds_32_units": "PAPER2_SOURCE_CAPTURE_INSUFFICIENT",
    }:
        fail("projection semantics drift")

    if policy["authorization"] != AUTHORIZATION:
        fail("authorization drift")

    if len(policy["destructive_requirements"]) != 10:
        fail("destructive requirement count drift")

    ledger = load(BASE / "research/paper2/designed_source_candidate_ledger_v1.json")
    web = load(BASE / "research/paper2/designed_source_web_fulltext_manifest_v1.json")
    capture = load(BASE / "research/paper2/designed_source_capture_manifest_v1.json")

    if len(web.get("entries", [])) != 60:
        fail("frozen web surface cardinality drift")
    if len(ledger.get("records", [])) != 180:
        fail("candidate ledger cardinality drift")
    if len(capture.get("records", [])) != 60:
        fail("capture descriptor cardinality drift")

    # Structural destruction of the Grand Null: the scientific candidate row
    # exists before and independently of #243's public_fulltext_locator.
    b3web = by_slot(web["entries"], "BLF03")
    b3ledger = ledger_row(ledger["records"], "BLF03", b3web["activated_rank"])
    if "public_fulltext_locator" in b3ledger:
        fail("candidate ledger unexpectedly contains transport locator")
    for field in (
        "stable_identity",
        "title",
        "year",
        "source_type",
        "registry_reference",
        "author_lineage_key",
    ):
        if b3web.get(field) != b3ledger.get(field):
            fail(f"BLF03: candidate identity drift in {field}")

    witnesses = policy["real_witnesses"]
    if not isinstance(witnesses, list) or len(witnesses) != 2:
        fail("real witness surface drift")
    b2 = next((w for w in witnesses if w.get("opaque_bundle_id") == "B0002"), None)
    b3 = next((w for w in witnesses if w.get("opaque_bundle_id") == "B0003"), None)
    if b2 is None or b3 is None:
        fail("required witness absent")

    b2capture = capture_row(capture["records"], "B0002")
    if (
        b2.get("slot_id") != b2capture.get("slot_id")
        or b2.get("activated_rank") != b2capture.get("activated_rank")
        or b2.get("alternate_host_used") is not False
        or b2.get("scientific_candidate_changed") is not False
        or b2.get("downstream_outcomes_consumed") is not False
    ):
        fail("B0002 witness drift")

    b3capture = capture_row(capture["records"], "B0003")
    expected_b3 = {
        "slot_id": "BLF03",
        "activated_rank": 1,
        "stable_identity": {"kind": "DOI", "value": "10.1146/annurev.neuro.29.051605.113038"},
        "title": "The Neural Basis of Decision Making",
        "year": 2007,
        "source_type": "journal_article",
    }
    for field, expected in expected_b3.items():
        if b3.get(field) != expected:
            fail(f"B0003 witness {field} drift")

    if b3capture.get("slot_id") != "BLF03":
        fail("B0003 opaque mapping drift")
    if canonical_identity(b3capture.get("stable_identity")) != canonical_identity(b3["stable_identity"]):
        fail("B0003 capture stable identity drift")
    if b3capture.get("activated_rank") != b3["activated_rank"]:
        fail("B0003 capture rank drift")

    for field in ("stable_identity", "title", "year", "source_type"):
        if b3web.get(field) != b3.get(field):
            fail(f"B0003/web identity drift: {field}")

    if b3.get("frozen_reference_locator") != b3web.get("public_fulltext_locator"):
        fail("B0003 frozen reference locator rewrite")
    if b3capture.get("public_fulltext_locator") != b3.get("frozen_reference_locator"):
        fail("B0003 capture/reference locator drift")

    if b3.get("transport_block_evidence_comment") != 5856196436:
        fail("B0003 transport block provenance drift")
    candidate_route = b3.get("verification_candidate_route")
    if (
        not isinstance(candidate_route, str)
        or not candidate_route.startswith("https://")
        or candidate_route == b3["frozen_reference_locator"]
    ):
        fail("B0003 alternate verification route drift")
    if b3.get("candidate_state") != "EQUIVALENCE_VERIFICATION_ONLY":
        fail("B0003 candidate state overclaim")
    if b3.get("artifact_accepted") is not False:
        fail("B0003 artifact acceptance not earned")
    if b3.get("scientific_candidate_changed") is not False:
        fail("B0003 source substitution")
    if b3.get("downstream_outcomes_consumed") is not False:
        fail("B0003 downstream outcome leak")

    return policy


def expect_invalid(policy: dict[str, Any], label: str) -> None:
    try:
        validate(policy)
    except ValidationError:
        return
    raise AssertionError(f"{label}: unexpectedly validated")


def self_test(base: dict[str, Any]) -> None:
    validate(base)

    x = copy.deepcopy(base)
    w = next(w for w in x["real_witnesses"] if w["opaque_bundle_id"] == "B0003")
    w["stable_identity"]["value"] = "10.0000/drift"
    expect_invalid(x, "stable identity drift")

    x = copy.deepcopy(base)
    w = next(w for w in x["real_witnesses"] if w["opaque_bundle_id"] == "B0003")
    w["activated_rank"] = 2
    expect_invalid(x, "activated rank drift")

    x = copy.deepcopy(base)
    w = next(w for w in x["real_witnesses"] if w["opaque_bundle_id"] == "B0003")
    w["frozen_reference_locator"] = w["verification_candidate_route"]
    expect_invalid(x, "reference locator rewrite")

    x = copy.deepcopy(base)
    w = next(w for w in x["real_witnesses"] if w["opaque_bundle_id"] == "B0003")
    w["candidate_state"] = "ACCEPTED"
    expect_invalid(x, "premature candidate acceptance")

    x = copy.deepcopy(base)
    w = next(w for w in x["real_witnesses"] if w["opaque_bundle_id"] == "B0003")
    w["artifact_accepted"] = True
    expect_invalid(x, "premature artifact acceptance")

    x = copy.deepcopy(base)
    x["authorization"]["b0003_alternate_artifact_acceptance"] = True
    expect_invalid(x, "real artifact acceptance authorization")

    x = copy.deepcopy(base)
    x["authorization"]["model_execution"] = True
    expect_invalid(x, "model authorization leak")

    x = copy.deepcopy(base)
    w = next(w for w in x["real_witnesses"] if w["opaque_bundle_id"] == "B0003")
    w["downstream_outcomes_consumed"] = True
    expect_invalid(x, "downstream outcome leak")

    x = copy.deepcopy(base)
    x["authority_layers"]["acquired_artifact"]["required_provenance"].remove("sha256")
    expect_invalid(x, "missing artifact provenance")

    x = copy.deepcopy(base)
    x["transport_equivalence_gate"]["fail_closed_on_equivalence_uncertainty"] = False
    expect_invalid(x, "fail-open equivalence")

    x = copy.deepcopy(base)
    x["bound_repository_blobs"]["research/paper2/designed_source_candidate_ledger_v1.json"] = "0" * 40
    expect_invalid(x, "bound authority drift")

    x = copy.deepcopy(base)
    w = next(w for w in x["real_witnesses"] if w["opaque_bundle_id"] == "B0003")
    w["title"] = "Same-title-only-is-not-enough"
    expect_invalid(x, "publication identity drift")

    print("PAPER2_SOURCE_TRANSPORT_EQUIVALENCE_V1_SELFTEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=Path, default=POLICY_PATH)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        policy = load(args.policy)
        validate(policy)
        if args.self_test:
            self_test(policy)
        else:
            print("PAPER2_SOURCE_TRANSPORT_EQUIVALENCE_V1_VALID")
        return 0
    except (ValidationError, OSError, json.JSONDecodeError, AssertionError) as exc:
        print(f"PAPER2_SOURCE_TRANSPORT_EQUIVALENCE_V1_INVALID: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
