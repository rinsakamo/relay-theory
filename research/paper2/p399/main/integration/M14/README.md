# M14 — licensed identity inference, public replay, and post-freeze comparison

M14 has three layers that must remain separate:

1. the JGPS argument about when structural comparison licenses cognitive-capacity identity inference;
2. the **pre-result frozen replay protocol**, which remains historical authority and is not rewritten after seeing results;
3. the **post-freeze comparison layer**, which records what happened when two named-model product configurations executed the frozen protocol.

## Frozen replay authority

The v1 replay inputs remain:

- `M14_CROSS_MODEL_REPLICATION_PROTOCOL_v1.json`
- `M14_CROSS_MODEL_INPUT_MANIFEST_v1.json`
- `M14_CROSS_MODEL_BLANK_RECORD_v1.json`
- `M14_CROSS_MODEL_COMPARISON_RULES_v1.json`
- `M14_CROSS_MODEL_PROMPT_v1.md`
- `M14_CROSS_MODEL_REPLAY_README_FROZEN_v1.md`

The historical protocol status remains `PROTOCOL_FROZEN_CROSS_MODEL_REPLICATION_NOT_YET_PERFORMED` because that file records the state at pre-result freeze. It must not be retroactively rewritten.

The public replay artifact must package the frozen README above, **not this live status README**, so that later third-party replays do not receive post-result comparison information.

## Executed blinded replays

### GPT-6 Astra / Medium

- product-level configuration: supported by post-freeze UI evidence
- exact backend snapshot / internal routing: **UNVERIFIED**
- COMPLETE: 9
- ABSTAIN: 1 (XM03)
- CONTAMINATED: 0
- package SHA256: `3b7911f2288c6a1f9ee4ab6cd033cc6eaba5c10fedf5b002170562b6ca531d04`
- original receipt SHA256: `c148424f3cc12ce0911a6e1ad02793fbb35b12857b9b4c37c1c9715f0dc5f435`

The original frozen receipt is unchanged. `M14_ASTRA_UI_PROVENANCE_SUPPLEMENT_v1.json` only supplements product-level provenance after freeze.

### GPT-6.1 Sol / Medium

- product-level configuration: GPT-6.1 Sol / Medium
- exact backend snapshot / internal routing: **UNVERIFIED**
- COMPLETE: 10
- ABSTAIN: 0
- CONTAMINATED: 0
- package SHA256: `b09ed20aa54c302843e069d10f9ad925ad1bf0f43b8832d96085df6bcf52dd73`
- receipt SHA256: `68446ebab712cc7b648524c528661195a18929914d7f4c903c3cffe19f2579d1`

## Frozen-class comparison

The four predeclared classes were used without adding a fifth scored class.

| Replay | EXACT | COMPATIBLE | SUBSTANTIVE | ABSTENTION |
|---|---:|---:|---:|---:|
| Astra / Medium | 0 | 1 | 8 | 1 |
| GPT-6.1 Sol / Medium | 0 | 3 | 7 | 0 |

These totals are **not** interpreted as a simple reliability or recovery rate.

The v1 replay asked each model to identify one focal cognitive claim from each source, while the retained reference had already fixed one particular claim. Therefore the substantive class can combine two different phenomena:

- focal-claim selection divergence;
- decomposition divergence after a claim has been selected.

A post hoc descriptive check, explicitly not a frozen score, found that the two replay configurations selected the same broad focal region in 8/9 jointly completed cases and in 7/8 jointly completed cases with byte-identical source files. This does not replace the four frozen comparison classes.

The principal validation finding is therefore a **focal-claim-selection confound**. A future decomposition-specific replay should freeze a source-grounded claim anchor while withholding the retained structural decomposition. The v1 results must not be rescored under that future protocol.

Machine-readable comparison authority:

- `M14_ASTRA_UI_PROVENANCE_SUPPLEMENT_v1.json`
- `M14_REPLAY_COMPARISON_RESULTS_v1.json`
- `M14_REPLAY_COMPARISON_RECEIPT_v1.json`
- `M14_REPLAY_COMPARISON_REPORT_v1.md`

## Interpretation boundary

The replays are not independent human validation, not human inter-rater reliability, and not cross-provider replication. Exact backend snapshots are not independently verified, and model-family independence is not claimed.

**Procedural auditability is established; inter-rater reliability remains unmeasured.**

Current terminal state:

`M14_TWO_REPLAYS_COMPARED_FOCAL_CLAIM_SELECTION_CONFOUND_IDENTIFIED`
