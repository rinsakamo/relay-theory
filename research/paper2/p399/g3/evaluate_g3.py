#!/usr/bin/env python3
"""G3 synthetic structural scoring instrument. NOT the historical #401 v2.3.1 validator.
Never supplies independent source semantic evidence; only checks locked reported witnesses.
"""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
METRICS = ("nodes", "edges", "roles", "temporal", "restrictions", "boundary", "distinctions")
SCHEMA_FILES = {
    "reference": "reference-object.v1.schema.json",
    "packet": "analyst-packet.v1.schema.json",
    "evaluation": "evaluation.v1.schema.json",
    "receipt": "stage-receipt.v1.schema.json",
}


class G3Error(ValueError):
    pass


def schema_check(name, obj):
    # jsonschema is independent of the historic C checker.
    from jsonschema import Draft202012Validator
    schema = json.loads((ROOT / SCHEMA_FILES[name]).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    failures = sorted(Draft202012Validator(schema).iter_errors(obj), key=lambda x: str(x.path))
    if failures:
        f = failures[0]
        raise G3Error("%s SCHEMA: %s: %s" % (name, list(f.path), f.message))


def canonical_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def check_reference(reference):
    schema_check("reference", reference)
    if reference["freeze_state"] != "LOCKED":
        raise G3Error("REFERENCE_NOT_LOCKED")
    for v in reference["variants"]:
        ids = set()
        for name in ("nodes", "edges", "temporal", "restrictions", "boundaries",
                     "distinctions", "native_coordination"):
            for atom in v[name]:
                if atom["id"] in ids:
                    raise G3Error("DUPLICATE_REFERENCE_ATOM")
                ids.add(atom["id"])
        nodes = {n["id"] for n in v["nodes"]}
        if any(e["from"] not in nodes or e["to"] not in nodes for e in v["edges"]):
            raise G3Error("DANGLING_REFERENCE_EDGE")
    return True


def check_packet(packet):
    schema_check("packet", packet)
    if not packet["approved"] or not all(v for k, v in packet["scope_integrity"].items()
                                          if k != "checked_by"):
        raise G3Error("INCOMPLETE_OR_UNAPPROVED_PACKET")
    flags = set(packet["masking"]["leakage_flags"])
    if "FULLY_MASKED" in flags and flags.intersection(
            {"PARTIALLY_IDENTIFIABLE", "DIRECTLY_RECOGNIZABLE", "PREVIOUSLY_EXPOSED"}):
        raise G3Error("CONTRADICTORY_MASK_CLAIMS")
    if packet["masking"]["recognition_pre_D"] == "YES" and "FULLY_MASKED" in flags:
        raise G3Error("KNOWN_RECOGNITION_NOT_FULLY_BLIND")
    return True


def _metric(metric):
    required = set(metric["required_ids"])
    matched = set(metric["matched_ids"])
    unresolved = set(metric.get("unresolved_ids", []))
    critical = set(metric.get("critical_ids", []))
    if not matched <= required or not unresolved <= required or not critical <= required:
        raise G3Error("INVALID_REFERENCE_WITNESS_ID")
    if matched & unresolved:
        raise G3Error("SAME_WITNESS_MATCHED_AND_UNRESOLVED")
    anchors = metric.get("evidence_witnesses", {})
    if any(not isinstance(anchors.get(x), str) or not anchors[x].strip() for x in matched):
        raise G3Error("MATCH_WITHOUT_SOURCE_EVIDENCE")
    return {"numerator": len(matched), "denominator": len(required),
            "missing_ids": sorted(required - matched - unresolved),
            "unresolved_ids": sorted(unresolved),
            "critical_missing": sorted((required - matched - unresolved) & critical)}


def score(record):
    schema_check("evaluation", record)
    declared = record["declared_variant_ids"]
    reported = [v["variant_id"] for v in record["variants"]]
    if len(reported) != len(set(reported)) or set(declared) != set(reported):
        raise G3Error("MISSING_DUPLICATE_OR_UNDECLARED_VARIANT")
    excluded = [x["id"] for x in record["excluded_quantitative_targets"]]
    if len(excluded) != len(set(excluded)):
        raise G3Error("DUPLICATE_EXCLUDED_TARGET")
    if not record["attempted"]:
        return {"paper": "NOT_ATTEMPTED", "variant_outcomes": {}, "excluded_count": len(excluded)}
    invalid = record["source_state"] not in ("VERIFIED_PDF", "VERIFIED_HTML") or (
        record["packet_state"] != "VALID" or record["reference_state"] == "MISSING")
    reference_conflict = record["reference_state"] == "CONFLICT_UNRESOLVED"
    out = {}
    counters = {x: {"numerator": 0, "denominator": 0} for x in METRICS}
    for v in record["variants"]:
        values = {key: _metric(v["metrics"][key]) for key in METRICS}
        for m in METRICS:
            counters[m]["numerator"] += values[m]["numerator"]
            counters[m]["denominator"] += values[m]["denominator"]
        if any(set(excluded) & set(v["metrics"][m]["required_ids"]) for m in METRICS):
            raise G3Error("EXCLUDED_QUANTITATIVE_TARGET_IN_STRUCTURAL_DENOMINATOR")
        if not v["included"]:
            verdict = "NOT_ATTEMPTED"
        elif invalid:
            verdict = "INPUT_UNDERSPECIFIED"
        elif reference_conflict or v["unresolved_material"] or any(
                values[m]["unresolved_ids"] for m in METRICS):
            verdict = "UNDERDETERMINED"
        elif v["contradictions"] or v["essential_losses"] or any(
                values[m]["critical_missing"] for m in METRICS):
            verdict = "FAILED"
        elif any(values[m]["missing_ids"] for m in METRICS) or any(
                not a["source_grounded"] for a in record["assumptions"]):
            verdict = "PARTIAL"
        else:
            verdict = "FULL"
        out[v["variant_id"]] = {"verdict": verdict, "metrics": values,
                                "semantic_audit_independent": bool(v.get("independent_semantic_audit", False))}
    statuses = [v["verdict"] for v in out.values()]
    if all(x == "FULL" for x in statuses):
        paper = "FULL"
    elif len(set(statuses)) == 1:
        paper = statuses[0]
    else:
        paper = "MIXED"
    return {"paper": paper, "variant_outcomes": out,
            "source_conditional_only": True, "reference_independence": record["reference_state"],
            "excluded_count": len(excluded), "micro_counts": counters,
            "declared_variants": len(declared), "eligible_attempted_variants": sum(
                v["included"] for v in record["variants"]),
            "status_histogram": {k: statuses.count(k) for k in sorted(set(statuses))}}


def coordination(record):
    schema_check("evaluation", record)
    h = record["coordination"]
    claims = {level: [a for a in record["assumptions"] if a["level"] == level]
              for level in ("A0", "A1", "A2")}
    def certified(level):
        return all(a["source_grounded"] and a["necessity_test"] == "PASS"
                   for a in claims[level]) and bool(claims[level])
    requested = h["discrimination"]
    if requested == "H0_SOURCE_CONDITIONAL":
        valid = h["a0"] == "SUPPORTED" and not claims["A1"] and not claims["A2"]
    elif requested == "H1_SOURCE_CONDITIONAL":
        valid = (h["a0"] == "FAILED" and h["a1"] == "SUPPORTED" and certified("A1")
                 and not claims["A2"])
    elif requested == "H2_SOURCE_CONDITIONAL":
        valid = (h["a0"] == "FAILED" and h["a1"] == "FAILED" and h["a2"] == "SUPPORTED"
                 and certified("A2") and h["source_defined_functions_exhausted"]
                 and h["additional_state_source_grounded"])
    else:
        valid = True  # Explicitly non-discriminating/underdetermined, never proof of H2.
    return requested if valid else "UNSUPPORTED_COORDINATION_INFERENCE"


def destructive_control(baseline, mutant, mutation_kind, semantically_applicable,
                        source_discriminable):
    recognized = {"REMOVE_EDGE", "REVERSE_TEMPORAL", "SWAP_BOUNDARY",
                  "REMOVE_NATIVE_COORDINATOR", "MERGE_VARIANTS",
                  "STATEFUL_TO_STATELESS", "REMOVE_NEGATIVE", "G_DYN"}
    if mutation_kind not in recognized or not semantically_applicable:
        return "INVALID"
    first, second = score(baseline), score(mutant)
    if first["paper"] != "FULL":
        return "INVALID"
    if not source_discriminable:
        return "NON_DISCRIMINATING"
    if second["paper"] in ("PARTIAL", "FAILED", "MIXED"):
        return "INFORMATIVE"
    if second["paper"] in ("INPUT_UNDERSPECIFIED", "UNDERDETERMINED"):
        return "INVALID"
    return "FALSE_POSITIVE_RECONSTRUCTION"


STAGES = ("S0", "R0", "P0", "A", "B", "C", "D0", "D1", "D2", "E0", "ATLAS0", "UNMASK")


def verify_receipt_chain(receipts):
    if not receipts or receipts[0]["stage"] != "S0":
        raise G3Error("MISSING_SOURCE_PREFREEZE")
    for r in receipts:
        schema_check("receipt", r)
        if not r["signed_freeze"] or r["main_authorized"]:
            raise G3Error("UNSIGNED_OR_PREMATURE_AUTHORIZATION")
    base = receipts[0]
    seen = set()
    prior = None
    for r in receipts:
        stage = r["stage"]
        if stage in seen or (prior and STAGES.index(stage) <= STAGES.index(prior["stage"])):
            raise G3Error("STAGE_ORDER_OR_DUPLICATE")
        if r["paper_token"] != base["paper_token"] or r["primary_source_id"] != base["primary_source_id"] or r["protocol_sha256"] != base["protocol_sha256"]:
            raise G3Error("SOURCE_OR_PROTOCOL_SWAP")
        if prior and r["prior_raw_sha256"] != prior["artifact_raw_sha256"]:
            raise G3Error("BROKEN_SHA_CHAIN")
        seen.add(stage)
        prior = r
    if "UNMASK" in seen and "ATLAS0" not in seen:
        raise G3Error("PREMATURE_LABEL_UNMASK")
    if "C" in seen and not {"A", "B"} <= seen:
        raise G3Error("MISSING_SOURCE_REAUDIT")
    return True


def freeze_gate(g1, g2, protocol_test_pass, curator_ready, author_approved):
    # This is an advisory test fixture gate, NOT permission to start MAIN.
    return ("READY_FOR_JOINT_REVIEW" if all((g1, g2, protocol_test_pass, curator_ready,
                                            author_approved)) else "PRE_FREEZE_NO_MAIN")
