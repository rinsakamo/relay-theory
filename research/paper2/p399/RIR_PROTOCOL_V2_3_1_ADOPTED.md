# RelayTheory #399 — AUTHOR ADOPTION: v2.3.1, two mandatory C safeguards
**Authority:** User's explicit 2026-10-04 JST decision: 「2点を採用する。進めて」 following the three-case v2.3 QP03/QP04/QP05 development comparison. **Prospective** incremental replacement of C requirements in author-adopted v2.3, NOT a retroactive scientific upgrade.

## Unchanged procedural core
Author-approved v2.2.2 source universe = DOI-linked **publisher-designated complete original full HTML only**, including material actually visible in HTML. Any standalone linked supplement **not embedded in full HTML is entirely out of scope**; never download/require or certify its unshown contents. Before new A, freeze official edition/correction/source-scope and model/lineage provenance. A original-first freezes the graph. B gets the same full original HTML **plus all exact immutable A**, challenges every A item/edge and separately reviews all source sections in source order, including B=0. C gets original + frozen complete A/B, source-reopens each objection *individually*, weighs opposing interpretations and contradiction, emits append-only deltas, and independently re-sweeps source in original order. Existing Grammar and all old A/B/C frozen.

## MANDATORY NEW safeguard C1 — original A coverage and overpatch avoidance
**Before any C correction/addition/precision patch**, C must reopen the **entire original immutable A** (including related nodes and edges), identify original A IDs, accurately summarize what A actually claimed and record an explicit *source-versus-original-A gap test*. Allowed findings:
- `SOURCE_GAP_CONFIRMED`: distinct supported content missing/misrepresented in original A; only this licenses append-only ACCEPT with a genuinely novel delta.
- `ALREADY_QUALIFIED_IN_A`: A already bounds this exact source claim; `REJECT_ALREADY_QUALIFIED_IN_A`, **NO PATCH**. Preserve unrelated real uncertainty separately.
- `NO_IN_SCOPE_SOURCE_DEFECT`: reject unsupported or excluded-external-supplement objection without patch.
- `UNRESOLVED`: mark affected material claim underdetermined; use exception only where substantive.

**Regression example:** QP03 historical new C' unnecessarily appended a reduced-covariance qualifier to A10, which had only asserted the full nine-state formulation. This must be blocked by the prepatch original-A comparison. Do not alter that frozen historical C' or pretend a retrospectively observed defect is independent new detection.

## MANDATORY NEW safeguard C2 — material source-local negative/limit enumeration
For **every in-HTML passage/figure/equation reopened to adjudicate** an objection or C-only discovery, actively inspect its immediate original-context qualifiers, boundary restrictions, contrary cases, negative results and failed attempted rescues. Record the material condition IDs against the evidence and reconcile every identified ID **exactly once** in a condition ledger, with source locator and treatment: `IN_PATCH` (patch ID and binding rationale), `ALREADY_IN_A` (old A ID), `CLAIM_LIMITED` (explicit bounded wording), or `EXCLUDE_AS_UNRESOLVED` (affected claim + exception). If genuinely none are found, record where/how the passage was inspected and the reason. C may not close an issue with a known unaccounted material condition.

**Regression example:** QP04 original publisher HTML Discussion's deep-tree test says context fails to dominate as first PC unless multiplied by a **very large scalar** AND **training remains unstable even after such scaling**. C that notes only the large-scalar exception still fails the test. Preserve separate Fig5 Oja input-mask ambiguity rather than inventing resolution.

## Human gate and validation
Continue v2.3 **exception-only** human adjudication for unresolved decisive original-HTML ambiguities/unreadable essential in-HTML math or high-risk novel coordinator/H hypotheses; routine author signoff and legacy blanket sampling are no longer mandatory. The user waived independent residual-accuracy benchmarking as an adoption requirement, NOT as evidence of higher measured accuracy. C source closure with both safeguards is required; a structural validator can verify reported original-A comparison and complete *reported* condition ledgers, **not discover undisclosed omissions or prove that original scientific interpretation is true**. Keep any needed material claim UNDERDETERMINED.

## Actual local implementation and retention
Complete separate local code/docs/fixture package `P399_V231_TWO_SAFEGUARDS_ADOPTED_20261004.zip`, SHA256 **`02f00e721458e6a7c3d8ad0449166bebc33635f8dfcc8beb219f4038dac01c0d`**, contains:
- `validate_c_v231.py` SHA256 `508f4d5dd7e1fe7e79f7d95b668855352666a731ec08626b5178df426d5608b4`
- `test_validate_c_v231.py` SHA256 `e8326a99e182f81ce9f28440683e873bc40d4c5c0a966fa77ff1126712ed5ccc`
- full worker prompt/protocol, Japanese result, derived QP05 retrospective annotated C check and machine-receipt + member hashes.

**ACTUALLY RAN**: new **41/41** v2.3.1 tests (including known QP03 false-patch, known QP04 both limitations); old unchanged **28/28** v2.3 C tests; original unchanged **35/35** v2.2.2 source/A/B tests = **104/104 synthetic STRUCTURAL tests**. Derived QP05 check has **2 B findings / 3 existing append-only patches / 0 unresolved exceptions** and passes v2.3.1 structural checker, but its **old QP05 C is immutable** and this is **outcome-exposed retrospective regression**, not an independent qualified new pilot. All original eight input file digests and new ZIP member hashes/CRC verified.

**Git integration boundary:** this PR records the adopted v2.3.1 method and reproducible content-addressed import instructions; the large local Python scripts/complete source fixtures are **not yet Git-tracked or CI-deployed**. Import exact verified ZIP into the repo through separately reviewed LocalCodex/CI transaction; do not claim GitHub validation from local unit tests. No MAIN authorization: independently predeclared and lineage/source/edition-qualified **4 NEW diverse prospective PILOT chains**, the broader 20-PILOT plan and frozen outcome-blind MAIN source manifest are separately required. Current formal **0/4**, **MAIN NO-GO**.
