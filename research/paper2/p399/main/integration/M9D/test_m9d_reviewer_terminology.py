import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
M9D = ROOT / "research/paper2/p399/main/integration/M9D"
MAIN = (ROOT / "paper/venues/jgps/main.tex").read_text()
COVER = (ROOT / "paper/venues/jgps/cover-letter.md").read_text()
RESPONSE = (ROOT / "paper/venues/jgps/response-to-reviewers.md").read_text()
CHECKLIST = (ROOT / "paper/venues/jgps/submission-checklist.md").read_text()
AUDIT = json.loads((M9D / "M9D_MANUSCRIPT_TERMINOLOGY_AUDIT_v1.json").read_text())

checks = []
def check(name, cond):
    if not cond:
        raise AssertionError(name)
    checks.append(name)

check("schema", AUDIT["schema"] == "relaytheory.p399.main.m9d.manuscript_terminology_audit.v1")
check("base_m9c", AUDIT["base_m9c_head"] == "0366a51457d2d7d997ab0f4cd097fe8268359172")

reviewer_files = {
    "main": MAIN,
    "cover": COVER,
    "response": RESPONSE,
    "checklist": CHECKLIST,
}

banned = [
    "Archetype", "XLike", "ClaimIR", "MAIN40", "M7", "W9", "G2",
    "ROLE_GAP", "Grammar v0", "Grammar-v0", "fail-closed", "hostile",
    "least-lift", "falsifiability calibration", "A-state",
    "PAPER2_RESULT", "EXTRACTION_UNDERDETERMINED",
    "SOURCE_CONTEXT_PARAMETER", "RELATION_LANGUAGE_GAP",
    "source-native", "source-faithful", "System/World",
    "source-closed", "immutable-input", "bounded genealogy clearance",
    "held-fixed", "post-hoc",
]
for label, text in reviewer_files.items():
    low = text.lower()
    for term in banned:
        check(f"{label}_no_{term}", term.lower() not in low)

# Engineering strings and raw provenance identifiers stay out of the manuscript.
check("main_no_texttt", "\\texttt{" not in MAIN)
check("main_no_internal_repo_path", "research/paper2/" not in MAIN)
check("main_no_sha40", re.search(r"\b[0-9a-f]{40}\b", MAIN) is None)
check("main_no_workflow_run_id", "GitHub Actions run" not in MAIN)

# Scientific invariants.
for phrase in [
    "1770/1770=\\text{incomparable}",
    "206 unique reusable structural subobjects",
    "99\\ \\text{cross-stratum families}",
    "\\text{full}=21",
    "\\text{partial}=22",
    "\\text{residual}=17",
    "0/17\\ \\text{residual claims required an additional top-level role}",
    "A0=40,\\qquad A1=0,\\qquad A2=0",
    "24/24",
    "16/16",
    "Independent human re-adjudication was not performed",
    "does not imply genealogical independence",
]:
    check(f"main_invariant_{phrase}", phrase in MAIN)

# Reviewer-facing concepts retained.
for phrase in [
    "structural role grammar",
    "minimal faithful reconstruction level",
    "post hoc discriminability stress test",
    "pre-specified reconstruction contract",
    "system--environment",
    "POMDP-like",
    "procedural auditability",
]:
    check(f"main_concept_{phrase}", phrase in MAIN or phrase in RESPONSE)

# No hidden restoration of independent-validation claims.
check("safe_extraction_validation_disclaimer", "automated extraction was not independently validated" in MAIN)
for forbidden in [
    "40 independent replications prove",
    "POMDPs cannot encode the tested cognitive models",
    "independent human re-adjudication was performed",
]:
    check(f"no_overclaim_{forbidden}", forbidden not in MAIN)

print(f"M9D_TERMINOLOGY_PASS {len(checks)}/{len(checks)}")
