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

## Current status

`M15_CLAIM_ANCHORED_V2_PROTOCOL_FROZEN_REPLAYS_NOT_PERFORMED`

No M15 replay or comparison result exists at this freeze.
