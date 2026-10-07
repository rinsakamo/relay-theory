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
- GPT-6.1 Sol / Medium: **FROZEN**
- 10 COMPLETE / 0 ABSTAIN / 0 UNDERDETERMINED / 0 CONTAMINATED
- package SHA256: `9399e3333b58800d89946ffc0926b4ea55360b6ee9dbe6b35c0f63bdd05a3a7f`
- freeze receipt SHA256: `c8adaa662b2ec49a58ea6a430dfc8fc921725e647dd0cd0e90cf0a097f63f191`
- retained comparison: NOT PERFORMED
- exact backend snapshot / internal routing: UNVERIFIED
- external receipt: `M15_B_EXTERNAL_FREEZE_RECEIPT_v1.json`
- non-scientific packaging caveat: manifest/SHA256SUMS list one generated `__pycache__/acquire.cpython-312.pyc` entry that is absent from the ZIP; all 10 RAW and 10 RECORD scientific payloads are present and their listed hashes are intact.

Current execution state:

`M15_A_AND_B_CLAIM_ANCHORED_REPLAYS_FROZEN_COMPARISON_AUTHORIZED`

Both named-model runs are now independently frozen. Retained and pairwise M15 comparison may begin under the predeclared M15 comparison rules. Do not rewrite either frozen replay package.
