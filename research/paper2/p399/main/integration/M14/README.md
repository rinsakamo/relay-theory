# M14 — licensed identity inference and public cross-model replay

M14 has two purposes:

1. slim the JGPS article around the epistemic question of when a structural comparison licenses a cognitive-capacity identity inference;
2. freeze a model-agnostic source-reconstruction replay that any third party can run with another model family.

## Cross-model replay

The replay sample is exactly the ten-source sample already frozen in M13. For each case, the replicator receives only:

- the original source identified by DOI;
- `M14_CROSS_MODEL_REPLICATION_PROTOCOL_v1.json`;
- `M14_CROSS_MODEL_PROMPT_v1.md`;
- `M14_CROSS_MODEL_BLANK_RECORD_v1.json`.

Do not reveal retained ClaimIR, bounded-object memberships, grammar verdicts, capacity-case outcomes, comparison answers, or another model's output until all ten new records are frozen.

Save the raw output verbatim and record provider/model/version, settings, retrieval/tool use, and access date. `ABSTAIN` and `UNDERDETERMINED` are admissible.

Only after all ten outputs are frozen should they be compared under `M14_CROSS_MODEL_COMPARISON_RULES_v1.json`.

## Interpretation boundary

Cross-model agreement is not independent human inter-rater reliability. A replay tests reproducibility across the tested model families and can expose model-sensitive fields. Human validation remains a separate open target.

**Procedural auditability is established; inter-rater reliability remains unmeasured.**

Current result status: `PROTOCOL_FROZEN_CROSS_MODEL_REPLICATION_NOT_YET_PERFORMED`.
