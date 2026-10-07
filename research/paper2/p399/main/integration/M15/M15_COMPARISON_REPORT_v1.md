# M15 claim-anchored v2 comparison report

## Result

Both M15 runs were frozen before comparison. Under the predeclared four-class rule:

| Case | Slot | Astra vs retained | Sol vs retained | Astra vs Sol |
|---|---|---|---|---|
| XM01 | ATT03 | COMPATIBLE | COMPATIBLE | COMPATIBLE |
| XM02 | BLF04 | COMPATIBLE | COMPATIBLE | COMPATIBLE |
| XM03 | CNC01 | COMPATIBLE | COMPATIBLE | COMPATIBLE |
| XM04 | CTL01 | COMPATIBLE | COMPATIBLE | COMPATIBLE |
| XM05 | LRN03 | SUBSTANTIVE_DISAGREEMENT | SUBSTANTIVE_DISAGREEMENT | COMPATIBLE |
| XM06 | MEM02 | COMPATIBLE | COMPATIBLE | COMPATIBLE |
| XM07 | PRD05 | COMPATIBLE | COMPATIBLE | COMPATIBLE |
| XM08 | SKL06 | COMPATIBLE | COMPATIBLE | COMPATIBLE |
| XM09 | CH03 | COMPATIBLE | COMPATIBLE | COMPATIBLE |
| XM10 | CH12 | COMPATIBLE | COMPATIBLE | COMPATIBLE |

Aggregate:

- Astra vs retained: **0 exact / 9 compatible / 1 substantive / 0 abstention**.
- GPT-6.1 Sol vs retained: **0 exact / 9 compatible / 1 substantive / 0 abstention**.
- Astra vs Sol: **0 exact / 10 compatible / 0 substantive / 0 abstention**.

The predeclared primary compatible-reconstruction fraction is therefore **9/10 for each replay**.

## What changed from v1

This is a repair-test comparison, not independent confirmation. M15 was designed after M14 v1 exposed focal-claim selection as a confound. On the same sources, compatible-or-exact retained recovery changes descriptively from 1/10 to 9/10 for the Astra line and from 3/10 to 9/10 for the Sol line. No hypothesis test is attached to that change.

The result supports the v1 diagnosis: once claim identity is fixed, the two named-model runs usually preserve the same identity-relevant scientific commitments even though they do not reproduce the retained first-class factorization exactly.

## No exact factorization recovery

Neither replay yields an exact-or-normalized retained decomposition on any of the ten cases. The records commonly collapse or repartition retained nodes, criteria, probes, or context notes while preserving the anchored dependencies. This is consistent with the paper's broader non-uniqueness argument: compatible structural recovery does not imply a unique primitive factorization.

## XM05: the sole substantive case is a retained-reference problem

XM05 is not a model-model disagreement. Both replays independently flag the same source issue.

The frozen retained record contains a `matched_initial_activity_time` commitment and the M15 anchor describes the focal comparison as occurring under matched study time including Experiment 2. The Supporting Online Material instead specifies:

- Experiment 1: concept mapping 5+25 = 30 minutes; retrieval 5+10+5+10 = 30 minutes, explicitly described as identical total learning time.
- Experiment 2: concept mapping 5+20 = 25 minutes; retrieval 5+7+5+7 = 24 minutes.

Accordingly, both replay-vs-retained comparisons are scored `SUBSTANTIVE_DISAGREEMENT` under the frozen rule. Astra vs Sol remains `COMPATIBLE_ALTERNATIVE_DECOMPOSITION`: both source-grounded records preserve the retrieval-practice advantage and both identify the timing qualification.

This is recorded as the descriptive flag `ANCHOR_SOURCE_CONFLICT`, not as a fifth comparison class.

## Interpretation

M15 measures a different target than M14 v1. Claim selection is fixed, and decomposition is allowed to vary. The result supports reproducibility of identity-relevant commitments for these ten repaired same-source cases, not exact graph recovery, unseen-source generalization, human inter-rater reliability, or a unique ontology.

Because M15 was constructed after the v1 failure, the result is prospective relative to M15 outputs but not independent of M14's diagnostic result.

The XM05 finding now creates a separate source-correction obligation. The frozen retained ClaimIR must not be silently rewritten. A successor sensitivity lane should correct the time-matching condition and quantify any downstream effect on whole-claim comparison, bounded objects, role projection, and manuscript claims.

**Procedural auditability is established; inter-rater reliability remains unmeasured.**
