#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M14 = ROOT / "research/paper2/p399/main/integration/M14"
M13 = ROOT / "research/paper2/p399/main/integration/M13"

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

spec = load(M14 / "M14_SPEC_v1.json")
pref = load(M14 / "M14_PREFREEZE_RECEIPT_v1.json")
proto = load(M14 / "M14_CROSS_MODEL_REPLICATION_PROTOCOL_v1.json")
manifest = load(M14 / "M14_CROSS_MODEL_INPUT_MANIFEST_v1.json")
blank = load(M14 / "M14_CROSS_MODEL_BLANK_RECORD_v1.json")
rules = load(M14 / "M14_CROSS_MODEL_COMPARISON_RULES_v1.json")
m13_sample = load(M13 / "M13_HUMAN_SOURCE_EXTRACTION_SAMPLE_v1.json")
m13_human = load(M13 / "M13_HUMAN_SOURCE_EXTRACTION_PROTOCOL_v1.json")

main = (ROOT / "paper/venues/jgps/main.tex").read_text(encoding="utf-8")
supp = (ROOT / "paper/venues/jgps/supplement.tex").read_text(encoding="utf-8")
prompt = (M14 / "M14_CROSS_MODEL_PROMPT_v1.md").read_text(encoding="utf-8")
readme = (M14 / "README.md").read_text(encoding="utf-8")

PARENT = "dfbd7e8292cb95052ecb1d3c3d28613a43d2757a"
THESIS = (
    "An inference from structural comparison to cognitive-capacity identity is "
    "epistemically licensed only if the comparison representation, preservation "
    "criterion, and granularity are specified and warranted for that inferential use."
)

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

assert THESIS in main
assert "From specification to licensed identity inference" in main
assert "A live dialectical target: which invariance can individuate?" in main
assert "Wajnerman-Paz and Rojas-L" in main
assert "ATT03--MEM04" in main
assert "TAIF" in main and "CPCG" in main
assert "RII is therefore the paper's primary target" in main
assert "cross-model source reconstruction" in main
assert "protocol is frozen but has not yet been executed" in main
assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in main
assert "Structural comparison can bear evidential weight in cognitive-capacity individuation only when" not in main

assert "Public cross-model source reconstruction replay" in supp
assert "PROTOCOL\\_FROZEN\\_CROSS\\_MODEL\\_REPLICATION\\_NOT\\_YET\\_PERFORMED" in supp
assert "Cross-model reproducibility, if later measured, must remain separate from independent human inter-rater reliability." in supp
assert "Procedural auditability is established; inter-rater reliability remains unmeasured." in supp

assert "Current result status: `PROTOCOL_FROZEN_CROSS_MODEL_REPLICATION_NOT_YET_PERFORMED`." in readme

# No completed cross-model output/result is allowed in M14 at this protocol-only stage.
for p in M14.rglob("*"):
    if p.is_file():
        upper = p.name.upper()
        assert "CROSS_MODEL_RESULTS" not in upper
        assert not upper.startswith("XM") or "INPUT" in upper

print("M14_INFERENCE_WARRANT_REPLICATION_GUARDS_PASS")
