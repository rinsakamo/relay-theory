# PVS-16 Evidence × layered architecture diagnostic v1

Status: `FROZEN_POST_PROJECTION_EVIDENCE_JOIN`

The layered projection was frozen before E0–E3 was joined.

## Evidence-stratified result

| Evidence | Direct L_sys | Layer recovered | Architecture gap | Carrier pressure | Total | Architecture coverage |
|---|---:|---:|---:|---:|---:|---:|
| E0 | 22 | 3 | 0 | 0 | 25 | 100.0% |
| E1 | 9 | 6 | 0 | 0 | 15 | 100.0% |
| E2 | 4 | 4 | 0 | 0 | 8 | 100.0% |
| E3 | 3 | 1 | 0 | 1 | 4 | 100.0% |

All four evidence strata reach 100% architecture placement without adding a top-level cognitive-system role or a new architecture layer.

## High-evidence recoveries

- PVS-LRN-02.r1 — E2: PARTIAL -> RECOVERED_L_CLAIM; NULL_OR_PRESERVATION_COMPARISON; L_claim + L_sys
- PVS-ATT-02.r1 — E2: UNMAPPED -> RECOVERED_CROSS_LAYER; CONTEXT_INDEXED_CHANGE; L_claim + L_ctx + L_sys
- PVS-ATT-02.r3 — E2: UNMAPPED -> RECOVERED_CROSS_LAYER; MAGNITUDE_COMPARISON; L_claim + L_ctx + L_sys
- PVS-CNC-01.r3 — E2: PARTIAL -> RECOVERED_L_CLAIM_WITH_E_EXP_PROVENANCE; EXPERIMENTAL_MANIPULATION_PROVENANCE; L_claim + L_sys
- PVS-CNC-02.r2 — E3: UNMAPPED -> RECOVERED_CROSS_LAYER_WITH_CARRIER_PRESSURE; CONTRASTIVE_EXPLANATION; L_claim + L_ctx + L_sys

### E3 detail

`PVS-CNC-02.r2` is recovered as `L_claim + L_ctx + L_sys`: the category-type comparison context remains outside `G_cog`, while the contrastive explanatory predicate remains at `L_claim`. However, `causal_position` appears in the frozen relation description but not in its argument list, so a claim-carrier precision pressure remains.

## Interpretation

This is stronger than the system-only result: high-evidence failures are not left unexplained. They are assigned to already-frozen architectural layers. The result supports the system/claim/context separation, but it does **not** establish that `L_claim` is a complete or uniquely minimal formal logic.

Terminal: `PVS16_EVIDENCE_LEVELS_ALL_ARCHITECTURE_PLACEABLE_WITH_E3_CLAIM_CARRIER_PRESSURE_AND_NO_ROLE_OR_ARCHITECTURE_GAP`
