# AHV-8 held-out AssertionCarrier validation v1

Status: `FROZEN_HELDOUT_RESULT`

The target set was frozen before carrier mapping and contains all 28 relations from the eight human-reviewed AHV ClaimIR files. AssertionCarrier v1 was not modified during validation.

## Result

FULL: 11/28 (39.3%)
GAP: 17/28 (60.7%)
Claim-level FULL: 1/8

| Claim | Relations | FULL | GAP | Claim status |
|---|---:|---:|---:|---|
| AHV-MEM-01 | 3 | 1 | 2 | GAP |
| AHV-LRN-01 | 4 | 4 | 0 | FULL |
| AHV-SKL-01 | 4 | 2 | 2 | GAP |
| AHV-ATT-01 | 4 | 0 | 4 | GAP |
| AHV-PRD-01 | 2 | 1 | 1 | GAP |
| AHV-CTL-01 | 3 | 2 | 1 | GAP |
| AHV-BLF-01 | 4 | 0 | 4 | GAP |
| AHV-CNC-01 | 4 | 1 | 3 | GAP |

## Gap families

- ARGUMENT_LAYER_L_CLAIM_OR_THEORY_OBJECT_MISSING: 4
- PREDICATE_MAPPING_OR_TRANSFORMATION_MISSING: 4
- QUALIFIER_INCREASES_MISSING: 3
- QUALIFIER_BETTER_SUPPORTED_OR_PREFERENCE_MISSING: 1
- QUALIFIER_INCREASES_OR_FASTER_MISSING: 1
- QUALIFIER_DECREASES_MISSING: 1
- QUALIFIER_OPPOSITE_DIRECTION_MISSING: 1
- QUALIFIER_NEGATIVE_EFFECT_OR_LIMITATION_MISSING: 1
- PREDICATE_DISTINCTION_MISSING: 1
- QUALIFIER_DISTINCT_OR_DIFFERENT_TARGET_MISSING: 1
- QUALIFIER_BETTER_FIT_OR_MODEL_PREFERENCE_MISSING: 1

## What succeeded

- ordinary dependence assertions;
- association;
- context-indexed dependence;
- one contrastive explanation using the existing `CONTRASTIVE_RATHER_THAN` qualifier;
- additive semantic-reference recovery in `AHV-LRN-01.r4` using the already-existing `obtained_reward` ClaimIR node.

## What failed

- monotonic/directional meaning such as increases, decreases, faster, limiting, and opposite-direction effects;
- mapping/transformation assertions (`maps_to`) as a first-class assertion family;
- explicit distinction/different-target semantics;
- model preference / better-fit or better-supported semantics;
- arguments that are theoretical accounts rather than `L_sys` or `L_ctx` objects.

## Interpretation

The held-out result rejects a completeness reading of AssertionCarrier v1. The failure does not imply a missing cognitive-system role: the observed pressure is in `L_claim` vocabulary and argument-layer typing.

Because v1 is now held-out-falsified as complete, it must not be patched inside this run. A future v2 can be derived from these frozen gaps, but any v2 requires a newly admitted post-v2 held-out set for independent validation.

Terminal: `AHV8_HELDOUT_ASSERTION_CARRIER_REJECTS_V1_COMPLETENESS_WITH_11_OF_28_FULL_AND_17_GAPS`
