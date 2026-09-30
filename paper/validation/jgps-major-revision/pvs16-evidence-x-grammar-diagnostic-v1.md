# PVS-16 Evidence × Grammar-v0 diagnostic v1

Status: `FROZEN_POST_MAPPING_JOIN`

The Grammar mapping was committed first. This report then joins the frozen mapping to the previously frozen Evidence Profile v1.

## Relation-level matrix

| Evidence | PRESERVED | PARTIAL | UNMAPPED | Total | Strict preserved | Covered (P+partial) |
|---|---:|---:|---:|---:|---:|---:|
| E0 | 22 | 2 | 1 | 25 | 88.0% | 96.0% |
| E1 | 9 | 1 | 5 | 15 | 60.0% | 66.7% |
| E2 | 4 | 2 | 2 | 8 | 50.0% | 75.0% |
| E3 | 3 | 0 | 1 | 4 | 75.0% | 75.0% |

## Decisive diagnostic

- E3: 3/4 strictly preserved. The one UNMAPPED relation is `PVS-CNC-02.r2`: `RELATION_LANGUAGE_GAP` primary, `SOURCE_CONTEXT_PARAMETER` secondary.
- E2: 4/8 strictly preserved, 2 PARTIAL, 2 UNMAPPED. Both UNMAPPED relations (`PVS-ATT-02.r1`, `r3`) are `SOURCE_CONTEXT_PARAMETER`; no E2 ROLE_GAP.
- E1: 9/15 strictly preserved, 1 PARTIAL, 5 UNMAPPED. All five UNMAPPED relations are source-context failures.
- E0: 22/25 strictly preserved, 2 PARTIAL, 1 UNMAPPED. The only UNMAPPED relation is source-context.

Therefore the observed high-evidence failures do **not** currently identify a missing top-level cognitive role. They identify pressure at the system/context boundary and at scientific relation/assertion semantics.

## High-evidence non-preserved relations

- PVS-LRN-02.r1 — E2 / PARTIAL
- PVS-ATT-02.r1 — E2 / UNMAPPED / SOURCE_CONTEXT_PARAMETER
- PVS-ATT-02.r3 — E2 / UNMAPPED / SOURCE_CONTEXT_PARAMETER
- PVS-CNC-01.r3 — E2 / PARTIAL
- PVS-CNC-02.r2 — E3 / UNMAPPED / RELATION_LANGUAGE_GAP

## Claim verdict by maximum relation evidence

| Max evidence | FULL | PARTIAL | RESIDUAL | Total |
|---|---:|---:|---:|---:|
| E0 | 5 | 2 | 0 | 7 |
| E1 | 1 | 0 | 3 | 4 |
| E2 | 0 | 2 | 1 | 3 |
| E3 | 1 | 0 | 1 | 2 |

## Interpretation boundary

This is a diagnostic stress-test, not a prevalence estimate. E0–E3 is claim-to-frozen-source warrant directness, not a truth score. A high-evidence UNMAPPED relation is stronger pressure on the representation, but its residual class determines whether the pressure targets the cognitive-system role inventory, source-context separation, or relation/assertion language.

Terminal: `PVS16_EVIDENCE_STRATIFIED_MAPPING_SHOWS_HIGH_EVIDENCE_PRESSURE_WITHOUT_TOP_LEVEL_ROLE_GAP`
