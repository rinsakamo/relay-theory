# M15 — claim-anchored replay v2

M14 v1 revealed that an unanchored replay mixes two questions:

1. which source-grounded claim is selected;
2. how that claim is structurally decomposed.

M15 freezes a v2 repair that isolates question 2.

Each XM01-XM10 case now supplies only:

- the original source;
- source locator(s);
- a minimally identifying proposition naming the focal scientific claim;
- a blank structured-record schema;
- the frozen reconstruction prompt.

The anchor intentionally reveals claim identity while withholding the retained structural answer.

## Interpretation boundary

M15 is prospective relative to its own outputs, but it was designed after observing the M14 v1 claim-selection confound. It is therefore a repair/follow-up test, not an independent confirmatory study relative to v1.

The same ten sources are reused so that v1 versus v2 can isolate the effect of claim anchoring on those cases. Any improvement does not by itself establish generalization to unseen sources.

## Frozen execution order

1. GPT-6 Astra / Medium in a fresh conversation.
2. GPT-6.1 Sol / Medium in a separate fresh conversation.

Neither run may see M14 v1 outputs, M14 comparison results, retained structural answers, or the other M15 run before its ten records are frozen.

## Current comparison status

Both frozen named-model v2 runs have now been compared under the predeclared four-class M15 rule.

### Retained-reference comparison

| Replay | EXACT | COMPATIBLE | SUBSTANTIVE | ABSTENTION |
|---|---:|---:|---:|---:|
| GPT-6 Astra / Medium | 0 | 9 | 1 | 0 |
| GPT-6.1 Sol / Medium | 0 | 9 | 1 | 0 |

Predeclared primary compatible-reconstruction fraction:

- Astra / Medium: **9/10**
- GPT-6.1 Sol / Medium: **9/10**

### Pairwise replay comparison

Astra vs Sol:

- 0 exact
- **10 compatible**
- 0 substantive
- 0 abstention

This pairwise result is descriptive named-model agreement under a common anchored claim, not human inter-rater reliability or cross-provider replication.

### Relation to M14 v1

This is a repair-test result, not independent confirmation. M15 was designed after M14 v1 exposed a focal-claim-selection confound.

Descriptively, on the same ten sources:

- Astra retained compatible-or-exact: v1 **1/10** -> v2 **9/10**
- Sol retained compatible-or-exact: v1 **3/10** -> v2 **9/10**

No hypothesis test is attached to this change.

### XM05 retained-reference conflict

The sole substantive retained-reference case is XM05 / LRN03 for both replay configurations.

Both source-grounded replays identify the same problem in the frozen anchor/retained reference:

- Experiment 1: concept mapping 5+25 = 30 min; retrieval 5+10+5+10 = 30 min.
- Experiment 2: concept mapping 5+20 = 25 min; retrieval 5+7+5+7 = 24 min.

Therefore the frozen `matched_initial_activity_time` commitment is supported for Experiment 1 but not exactly for Experiment 2.

This is recorded as descriptive metadata `ANCHOR_SOURCE_CONFLICT`, not as a fifth comparison class. The frozen ClaimIR and frozen M15 anchor are not silently edited.

A successor source-correction sensitivity lane is required before treating LRN03 as corrected in the corpus.

### Interpretation boundary

- independent human validation: NOT PERFORMED
- human inter-rater reliability: UNMEASURED
- cross-provider replication: NOT PERFORMED
- exact backend identity: UNVERIFIED
- model-family independence: NOT CLAIMED
- unseen-source generalization: NOT ESTABLISHED
- unique structural factorization: NOT ESTABLISHED

**Procedural auditability is established; inter-rater reliability remains unmeasured.**

Current terminal state:

`M15_CLAIM_ANCHORED_V2_COMPARISON_COMPLETE_XM05_REFERENCE_CORRECTION_REQUIRED`
