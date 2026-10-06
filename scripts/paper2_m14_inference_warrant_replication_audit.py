#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M14 = ROOT / "research/paper2/p399/main/integration/M14"
M13 = ROOT / "research/paper2/p399/main/integration/M13"

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

spec = load(M14 / "M14_SPEC_v1.json")
pref = load(M14 / "M14_PREFREEZE_RECEIPT_v1.json")
proto = load(M14 / "M14_CROSS_MODEL_REPLICATION_PROTOCOL_v1.json")
manifest = load(M14 / "M14_CROSS_MODEL_INPUT_MANIFEST_v1.json")
blank = load(M14 / "M14_CROSS_MODEL_BLANK_RECORD_v1.json")
rules = load(M14 / "M14_CROSS_MODEL_COMPARISON_RULES_v1.json")
provenance = load(M14 / "M14_ASTRA_UI_PROVENANCE_SUPPLEMENT_v1.json")
results = load(M14 / "M14_REPLAY_COMPARISON_RESULTS_v1.json")
comparison_receipt = load(M14 / "M14_REPLAY_COMPARISON_RECEIPT_v1.json")
m13_sample = load(M13 / "M13_HUMAN_SOURCE_EXTRACTION_SAMPLE_v1.json")
m13_human = load(M13 / "M13_HUMAN_SOURCE_EXTRACTION_PROTOCOL_v1.json")

main = (ROOT / "paper/venues/jgps/main.tex").read_text(encoding="utf-8")
supp = (ROOT / "paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
prompt = (M14 / "M14_CROSS_MODEL_PROMPT_v1.md").read_text(encoding="utf-8")
frozen_readme = (M14 / "M14_CROSS_MODEL_REPLAY_README_FROZEN_v1.md").read_text(encoding="utf-8")
readme = (M14 / "README.md").read_text(encoding="utf-8")
comparison_report = (M14 / "M14_REPLAY_COMPARISON_REPORT_v1.md").read_text(encoding="utf-8")

PARENT = "dfbd7e8292cb95052ecb1d3c3d28613a43d2757a"
THESIS = (
    "An inference from structural comparison to cognitive-capacity identity is "
    "epistemically licensed only if the comparison representation, preservation "
    "criterion, and granularity are specified and warranted for that inferential use."
)
RULES_SHA256 = "eb54f84a6b4d38ea645f7d93db8b950a960776b90a6d2f2302e3dfc3e9f247b1"
INPUT_PACKET_SHA256 = "3b7c1ae0d981415d065bf1c841089f4bdffeeab8b1e0f374ae9d3b20e6890cf5"
ASTRA_PACKAGE_SHA256 = "3b7911f2288c6a1f9ee4ab6cd033cc6eaba5c10fedf5b002170562b6ca531d04"
ASTRA_RECEIPT_SHA256 = "c148424f3cc12ce0911a6e1ad02793fbb35b12857b9b4c37c1c9715f0dc5f435"
SOL_PACKAGE_SHA256 = "b09ed20aa54c302843e069d10f9ad925ad1bf0f43b8832d96085df6bcf52dd73"
SOL_RECEIPT_SHA256 = "68446ebab712cc7b648524c528661195a18929914d7f4c903c3cffe19f2579d1"
TERMINAL = "M14_TWO_REPLAYS_COMPARED_FOCAL_CLAIM_SELECTION_CONFOUND_IDENTIFIED"

# Original scientific authority is unchanged.
assert spec["authority"]["exact_parent_head"] == PARENT
assert pref["exact_parent_head"] == PARENT
assert pref["status"] == "PREFREEZE"
assert spec["central_thesis"] == THESIS
assert spec["warrant_definition"]["independence_kind"] == "inferential_non_circularity"

imm = spec["immutable_scientific_results"]
assert imm["whole_claim"] == "1770/1770 INCOMPARABLE"
assert imm["bounded_objects"] == 206
assert imm["cross_stratum_families"] == 99
assert imm["reverse_projection"] == "21 FULL / 22 PARTIAL / 17 RESIDUAL"
assert imm["residual_new_top_level_role"] == "0/17"
assert imm["prospective_MAIN40"] == "40/40 A0"
assert imm["encoding_permissive_six_weak_representations"] == "40/40 A0 each"
assert imm["direct_preservation_six_weak_representations"] == "0/40 A0 / 40/40 A1 each"
assert imm["global_genealogical_independence"] == "NOT_CLAIMED"

# Historical pre-result protocol files remain historical. Do not rewrite them to
# pretend that their prefreeze status was already a post-result status.
assert proto["status"] == "PROTOCOL_FROZEN_CROSS_MODEL_REPLICATION_NOT_YET_PERFORMED"
assert proto["result"] == "NOT_PERFORMED"
assert proto["epistemic_class"] == "CROSS_MODEL_REPLICATION"
assert "human inter-rater reliability" in proto["not_equivalent_to"]
assert m13_human["status"] == "PROTOCOL_FROZEN_HUMAN_EXTRACTION_NOT_PERFORMED"
assert m13_human["result"] == "NOT_PERFORMED"

m14_rows = [(r["slot_id"], r["doi"]) for r in manifest["rows"]]
m13_rows = [(r["slot_id"], r["doi"]) for r in m13_sample["rows"]]
assert m14_rows == m13_rows
assert len(m14_rows) == 10
assert [r["case_id"] for r in manifest["rows"]] == [f"XM{i:02d}" for i in range(1, 11)]

assert blank["uncertainty"]["status"] == "COMPLETE|ABSTAIN|UNDERDETERMINED"
assert list(rules["classes"]) == [
    "EXACT_OR_NORMALIZED_RECOVERY",
    "COMPATIBLE_ALTERNATIVE_DECOMPOSITION",
    "SUBSTANTIVE_DISAGREEMENT",
    "ABSTENTION_OR_UNDERDETERMINED",
]

for phrase in [
    "Do **not** use any retained ClaimIR",
    "ABSTAIN",
    "UNDERDETERMINED",
    "Complete and freeze your output before seeing any retained reference record",
    "Return only the completed JSON record",
]:
    assert phrase in prompt, phrase

# The blinded public packet must retain the exact pre-result README content,
# not the live post-result M14 status README.
assert "PROTOCOL_FROZEN_CROSS_MODEL_REPLICATION_NOT_YET_PERFORMED" in frozen_readme
assert "0 exact" not in frozen_readme
assert "focal-claim-selection confound" not in frozen_readme
assert "M14_TWO_REPLAYS_COMPARED" not in frozen_readme

# Post-freeze product-level provenance supplement never mutates the original receipt.
assert provenance["status"] == "POSTFREEZE_PROVENANCE_SUPPLEMENT_SCIENTIFIC_OUTPUT_UNCHANGED"
assert provenance["replay_package_sha256"] == ASTRA_PACKAGE_SHA256
assert provenance["original_freeze_receipt_sha256"] == ASTRA_RECEIPT_SHA256
assert provenance["original_manifest_model_identity_status"]["astra_identity_verified"] is False
assert provenance["original_manifest_model_identity_status"]["cross_model_family_independence_verified"] is False
assert provenance["supported_interpretation"]["label"] == "GPT-6 Astra / Medium"
assert provenance["supported_interpretation"]["exact_backend_snapshot_verified"] is False
assert provenance["supported_interpretation"]["internal_routing_verified"] is False
assert provenance["supported_interpretation"]["model_family_independence_from_retained_pipeline_verified"] is False

# Post-freeze comparison authority.
assert results["status"] == "POSTFREEZE_COMPARISON_COMPLETE"
assert results["frozen_authority"]["rules_sha256"] == RULES_SHA256
assert results["frozen_authority"]["input_packet_sha256"] == INPUT_PACKET_SHA256
assert results["replay_inputs"]["astra_medium"]["package_sha256"] == ASTRA_PACKAGE_SHA256
assert results["replay_inputs"]["astra_medium"]["receipt_sha256"] == ASTRA_RECEIPT_SHA256
assert results["replay_inputs"]["gpt61_sol_medium"]["package_sha256"] == SOL_PACKAGE_SHA256
assert results["replay_inputs"]["gpt61_sol_medium"]["receipt_sha256"] == SOL_RECEIPT_SHA256
assert len(results["cases"]) == 10
assert [c["case_id"] for c in results["cases"]] == [f"XM{i:02d}" for i in range(1, 11)]

assert results["aggregate"]["astra_medium"] == {
    "EXACT_OR_NORMALIZED_RECOVERY": 0,
    "COMPATIBLE_ALTERNATIVE_DECOMPOSITION": 1,
    "SUBSTANTIVE_DISAGREEMENT": 8,
    "ABSTENTION_OR_UNDERDETERMINED": 1,
}
assert results["aggregate"]["gpt61_sol_medium"] == {
    "EXACT_OR_NORMALIZED_RECOVERY": 0,
    "COMPATIBLE_ALTERNATIVE_DECOMPOSITION": 3,
    "SUBSTANTIVE_DISAGREEMENT": 7,
    "ABSTENTION_OR_UNDERDETERMINED": 0,
}
assert results["posthoc_descriptive_checks"]["status"] == "NOT_A_PREFROZEN_SCORE"
assert results["posthoc_descriptive_checks"]["same_focal_region_among_both_complete"] == "8/9"
assert results["posthoc_descriptive_checks"]["same_focal_region_with_exact_same_source_bytes"] == "7/8"
assert results["terminal_state"] == TERMINAL

assert comparison_receipt["status"] == "COMPARISON_COMPLETE"
assert comparison_receipt["rules_sha256"] == RULES_SHA256
assert comparison_receipt["comparison_inputs"]["astra_package_sha256"] == ASTRA_PACKAGE_SHA256
assert comparison_receipt["comparison_inputs"]["astra_receipt_sha256"] == ASTRA_RECEIPT_SHA256
assert comparison_receipt["comparison_inputs"]["gpt61_sol_package_sha256"] == SOL_PACKAGE_SHA256
assert comparison_receipt["comparison_inputs"]["gpt61_sol_receipt_sha256"] == SOL_RECEIPT_SHA256
assert comparison_receipt["terminal_state"] == TERMINAL
assert any("claim selection and decomposition" in x for x in comparison_receipt["limitations"])

# No fifth scored class was introduced post hoc.
allowed = set(rules["classes"])
for case in results["cases"]:
    assert case["astra"]["class"] in allowed
    assert case["sol"]["class"] in allowed
assert "SAME_FOCAL_REGION" not in allowed
assert "DIFFERENT_FOCAL_CLAIMS" not in allowed

# Interpretation boundary.
assert results["interpretation_boundary"]["human_inter_rater_reliability"] == "UNMEASURED"
assert results["interpretation_boundary"]["independent_human_validation"] == "NOT_PERFORMED"
assert results["interpretation_boundary"]["cross_provider_replication"] == "NOT_PERFORMED"
assert results["interpretation_boundary"]["model_family_independence"] == "NOT_CLAIMED"
assert results["interpretation_boundary"]["aggregate_match_rate_is_primary_result"] is False

# Manuscript now reports the result without converting it into human reliability.
assert THESIS in main
assert "From specification to licensed identity inference" in main
assert "A live dialectical target: which invariance can individuate?" in main
assert "Wajnerman-Paz and Rojas-L" in main
assert "ATT03--MEM04" in main
assert "TAIF" in main and "CPCG" in main
assert "RII is therefore the paper's primary target" in main
assert "Blinded named-model replay: claim selection and decomposition separate" in main
assert "Astra yielded one compatible alternative decomposition, eight substantive disagreements, and one abstention" in main
assert "Sol yielded three compatible alternative decompositions and seven substantive disagreements" in main
assert "same broad focal region in eight" in main
assert "focal-claim anchor" in main
assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in main
assert "Structural comparison can bear evidential weight in cognitive-capacity individuation only when" not in main

assert "Public cross-model source reconstruction replay" in supp
assert "GPT-6 Astra / Medium" in supp
assert "GPT-6.1 Sol / Medium" in supp
assert "XM10 & CH12 & SUBSTANTIVE & SUBSTANTIVE" in supp
assert "0 exact, 1 compatible, 8 substantive, and 1 abstention" in supp
assert "0 exact, 3 compatible, 7 substantive, and 0 abstentions" in supp
assert "same broad focal region in eight" in supp
assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in supp

# Live status README reports results; frozen README does not.
assert TERMINAL in readme
assert "focal-claim-selection confound" in readme
assert "pre-result frozen replay protocol" in readme
assert "must not be retroactively rewritten" in readme
assert "public replay artifact must package the frozen README" in readme
assert "focal-claim selection is a confound" in comparison_report
assert "not** reported as a single reliability or recovery score" in comparison_report

print("M14_INFERENCE_WARRANT_REPLAY_COMPARISON_GUARDS_PASS")
