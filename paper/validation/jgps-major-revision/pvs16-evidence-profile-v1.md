# PVS-16 Evidence Profile v1

Status: `PROVISIONAL_RULE_GOVERNED_ANNOTATION`

Authority boundary: human-reviewed PVS-16 ClaimIR + frozen PVS-16 source spans/source-authority metadata only. Grammar-v0 mapping was not inspected.

Evidence levels describe claim-to-frozen-source warrant directness, not journal prestige, truth probability, or overall paper quality.

| Claim | Source basis | Relation-level range | Source surface |
|---|---|---|---|
| PVS-MEM-01 | PRIMARY_EMPIRICAL | E1–E1 | indexed_source_abstract |
| PVS-MEM-02 | REVIEW_SYNTHESIS | E0–E0 | indexed_source_abstract |
| PVS-LRN-01 | PRIMARY_EMPIRICAL | E1–E1 | publisher_abstract |
| PVS-LRN-02 | PRIMARY_EMPIRICAL | E1–E2 | fulltext_with_source_abstract |
| PVS-SKL-01 | REVIEW_SYNTHESIS | E0–E0 | fulltext_with_source_abstract |
| PVS-SKL-02 | REVIEW_SYNTHESIS | E0–E0 | indexed_source_abstract |
| PVS-ATT-01 | REVIEW_SYNTHESIS | E0–E0 | public_fulltext |
| PVS-ATT-02 | PRIMARY_EMPIRICAL | E2–E2 | fulltext_with_source_abstract |
| PVS-PRD-01 | PRIMARY_EMPIRICAL | E0–E1 | publisher_abstract |
| PVS-PRD-02 | MODEL_OR_THEORY | E0–E0 | indexed_source_abstract |
| PVS-CTL-01 | REVIEW_SYNTHESIS | E0–E0 | publisher_abstract_and_key_points |
| PVS-CTL-02 | PRIMARY_EMPIRICAL | E2–E3 | fulltext_with_source_abstract |
| PVS-BLF-01 | MIXED_MODEL_EMPIRICAL | E0–E1 | fulltext_with_source_abstract |
| PVS-BLF-02 | MODEL_OR_THEORY | E0–E0 | publisher_fulltext_with_abstract |
| PVS-CNC-01 | MIXED_MODEL_EMPIRICAL | E0–E2 | indexed_source_abstract |
| PVS-CNC-02 | MIXED_MODEL_EMPIRICAL | E1–E3 | publisher_abstract |

## Relation-level counts

- E0 MODEL_SYNTHESIS_OR_PROPOSAL: 25
- E1 DIRECT_NONINTERVENTIONAL: 15
- E2 DIRECT_INTERVENTIONAL: 8
- E3 EXPLICIT_REPLICATED_INTERVENTIONAL: 4

## Interpretation guardrails

- E0 does not mean weak, false, or low quality; it means that the frozen packet does not expose a direct empirical test of that exact relation.
- E3 adds explicit replicated intervention breadth. Causal leverage and breadth remain separately recorded.
- Abstract-only versus full-text source visibility is recorded separately and does not change the level.
- These annotations do not modify ClaimIR or authorize/alter Grammar mapping.
