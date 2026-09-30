# PVS-16 layered-architecture projection v1

Status: `FROZEN_PRE_EVIDENCE_LAYERED_PROJECTION`

Evidence levels are deliberately not used in this projection. The input is the already-frozen PVS-16 Grammar-v0 mapping plus the frozen layered/system–World architecture.

## Result

- total relations: 52
- direct `L_sys` relations inherited from Grammar-v0 mapping: 38
- non-strict system relations requiring layered recovery: 14
- architecture-placeable non-strict relations: **14/14**
- `ARCHITECTURE_GAP`: **0**
- top-level `ROLE_GAP`: **0**
- claim-level architecture-placeable: **16/16**
- `L_formal` required for source-claim recovery: **0**
- claim-carrier precision pressures: **1** (`PVS-CNC-02.r2`)

## Context placement

| Node | Claim | Primary | Secondary | Refinement |
|---|---|---|---|---|
| impaired_group | PVS-MEM-01 | EXPERIMENT_CONTEXT | — | L_ctx only |
| matched_group | PVS-MEM-01 | EXPERIMENT_CONTEXT | — | L_ctx only |
| task_emphasis | PVS-LRN-01 | EXPERIMENT_CONTEXT | — | E_exp protocol/task regime |
| stimulus_pair | PVS-ATT-02 | WORLD_CONTEXT | EXPERIMENT_CONTEXT | W selected/prepared by E_exp; Gamma_in not individually reconstructed |
| sensory_noise | PVS-PRD-01 | PARAMETER_ONLY | WORLD_CONTEXT, UNDERDETERMINED | L_ctx parameter; exact W/measurement/model locus remains underdetermined |
| category_type | PVS-CNC-02 | EXPERIMENT_CONTEXT | — | L_ctx comparison regime only |

## Recovery of the 14 non-strict relations

| Relation | System status | Layered status | L_claim assertion class | Layers |
|---|---|---|---|---|
| PVS-MEM-01.r1 | UNMAPPED | RECOVERED_CROSS_LAYER | COMPARATIVE_EQUIVALENCE | L_claim + L_ctx + L_sys |
| PVS-MEM-01.r3 | UNMAPPED | RECOVERED_CROSS_LAYER | CONTEXT_INDEXED_OUTCOME_ASSERTION | L_claim + L_ctx + L_sys |
| PVS-MEM-02.r4 | PARTIAL | RECOVERED_L_CLAIM | CROSS_CONTEXT_DISSOCIATION | L_claim + L_sys |
| PVS-LRN-01.r1 | UNMAPPED | RECOVERED_CROSS_LAYER | CONTEXT_INDEXED_DEPENDENCE | L_claim + L_ctx + L_sys |
| PVS-LRN-01.r2 | UNMAPPED | RECOVERED_CROSS_LAYER | CONTEXT_INDEXED_DEPENDENCE | L_claim + L_ctx + L_sys |
| PVS-LRN-01.r3 | PARTIAL | RECOVERED_L_CLAIM | SIGNED_ASSOCIATION | L_claim + L_sys |
| PVS-LRN-01.r5 | UNMAPPED | RECOVERED_CROSS_LAYER | MATCHED_COMPARISON | L_claim + L_ctx + L_sys |
| PVS-LRN-02.r1 | PARTIAL | RECOVERED_L_CLAIM | NULL_OR_PRESERVATION_COMPARISON | L_claim + L_sys |
| PVS-ATT-02.r1 | UNMAPPED | RECOVERED_CROSS_LAYER | CONTEXT_INDEXED_CHANGE | L_claim + L_ctx + L_sys |
| PVS-ATT-02.r3 | UNMAPPED | RECOVERED_CROSS_LAYER | MAGNITUDE_COMPARISON | L_claim + L_ctx + L_sys |
| PVS-PRD-01.r2 | UNMAPPED | RECOVERED_CROSS_LAYER | CONTEXT_INDEXED_DEPENDENCE | L_claim + L_ctx + L_sys |
| PVS-PRD-02.r3 | PARTIAL | RECOVERED_L_CLAIM | IMPLEMENTATION_MODALITY | L_claim + L_sys |
| PVS-CNC-01.r3 | PARTIAL | RECOVERED_L_CLAIM_WITH_E_EXP_PROVENANCE | EXPERIMENTAL_MANIPULATION_PROVENANCE | L_claim + L_sys |
| PVS-CNC-02.r2 | UNMAPPED | RECOVERED_CROSS_LAYER_WITH_CARRIER_PRESSURE | CONTRASTIVE_EXPLANATION | L_claim + L_ctx + L_sys |

## Main interpretation

The prior PVS failures do not require expanding `G_cog`. They decompose into scientific assertion semantics (`L_claim`) and source/study/World context (`L_ctx`), while the cognitive-system endpoints remain in `L_sys`.

`PVS-CNC-02.r2` is architecture-placeable but exposes a representation-precision issue: `causal_position` is required by the frozen relation description yet omitted from the frozen relation argument list. The ClaimIR is left unchanged.

Terminal: `PVS16_ALL_NONSTRICT_RELATIONS_LAYER_PLACEABLE_WITH_ONE_CLAIM_CARRIER_PRESSURE_AND_NO_ARCHITECTURE_GAP`
