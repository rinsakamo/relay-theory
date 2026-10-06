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

## Current execution status

The frozen public packet and pre-result protocol remain unchanged.

M15-A:
- GPT-6 Astra / Medium: **FROZEN**
- 10 COMPLETE / 0 ABSTAIN / 0 UNDERDETERMINED
- package SHA256: `ca6f1d557915777ae59e9846fd80ac90134c10e85b76ec9ae3e2ef53c1d22fb3`
- retained comparison: NOT PERFORMED
- exact backend snapshot: UNVERIFIED
- external receipt: `M15_A_EXTERNAL_FREEZE_RECEIPT_v1.json`

M15-B:
- GPT-6.1 Sol / Medium: NOT YET PERFORMED

Current execution state:

`M15_ASTRA_MEDIUM_CLAIM_ANCHORED_REPLAY_FROZEN_COMPARISON_NOT_PERFORMED`

Do not open M15-A scientific records for comparison before M15-B has independently frozen all ten cases.
