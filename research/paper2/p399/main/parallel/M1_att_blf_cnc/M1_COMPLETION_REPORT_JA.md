# RelayTheory Paper 2 — MAIN M1 Completion Report (JA)

## Authority / scope

- Issue: #399
- Branch: `paper2/p399-main-m1-att-blf-cnc-20261005`
- Exact kickoff base SHA: `3c2761ac13b04203aa7dbd8f47a1d687d506bf7b`
- MAIN GO: Draft PR #452
- W9 authority: Draft PR #451 / `71aab1c485446223bc8951ea3b8978aaeece3279`
- MAIN40 manifest blob: `b97b67a34ad9c2858745dfa6aa60444520eaab13`
- RIR v2.3.1 reference HEAD: `7f8750c5f4b1b87095f7dfdfbb558bba8e1c4157`
- Grammar v0 blob: `a688edb063c0ad43c25df15f497918817e8b74cd`
- Stage authority commits:
  - Source authority lock: `6c35a8a531aa0d5eeb9dbf5f5dd26ae3becd7350`
  - Stage A: `541b9a269b31b21dbea595b172dda4f37be19f78`
  - Stage B: `ea298e106fe2dd800ffdc8f26479d1f09be5864a`
  - Stage C: `9e597539244d161a7f20320ecf22ece1bf32b400`

- Draft PR: **#453** — `P399 MAIN M1 — ATT/BLF/CNC source-closed reconstruction and architectural adjudication`
- Exact scientific HEAD: `fddeefaaa209623c95858e578fa3d31a3389e672`
- CI run: **37283369126 SUCCESS** on exact scientific HEAD `fddeefaaa209623c95858e578fa3d31a3389e672`
- CI job: `m1-fail-closed` / **25/25 PASS**

この追記自体は metadata-only commit とするため、最終 branch ref は self-referential に本文へ埋め込まず、GitHub ref/PR を authority とする。

## 9-paper status

| Slot | DOI | Final state | Source fidelity |
|---|---|---|---|
| ATT-01 | 10.1007/s42113-024-00197-6 | A0_FIDELITY | SOURCE_FIDELITY_WITH_ONE_SOURCE_DEFINED_STAGE_C_CLARIFICATION |
| ATT-02 | 10.1371/journal.pcbi.1004770 | A0_FIDELITY | SOURCE_FIDELITY_BOUNDED_BY_EXPLICIT_MODEL_SCOPE |
| ATT-03 | 10.1016/j.neuron.2009.01.002 | A0_FIDELITY | BOUNDED_A0_MAIN_EQUATIONS_WITH_EXPLICIT_UNRESOLVED_SUPPLEMENT |
| BLF-01 | 10.1016/j.isci.2025.112844 | A0_FIDELITY | BOUNDED_A0_WITH_PUBLICATION_DESCRIPTION_DISCREPANCIES |
| BLF-02 | 10.1371/journal.pcbi.1006972 | A0_FIDELITY | SOURCE_FIDELITY_WITH_W8S_OFFICIAL_SUPPLEMENT |
| BLF-03 | 10.7554/eLife.08825 | A0_FIDELITY | SOURCE_FIDELITY_WITH_EXPLICIT_NORMATIVE_AND_APPROXIMATION_BOUNDARIES |
| CNC-01 | 10.1038/s41562-023-01719-1 | A0_FIDELITY | SOURCE_FIDELITY_WITH_EXPLICIT_NON_DOI_ANCESTRY_AND_RESOURCE_LIMITS |
| CNC-02 | 10.1371/journal.pcbi.1011954 | A0_FIDELITY | SOURCE_FIDELITY_PRESERVING_NON_UNIQUE_MODEL_VARIANT_SPACE |
| CNC-03 | 10.7554/eLife.77185 | A0_FIDELITY | SOURCE_FIDELITY_WITH_EXPLICIT_INHERITED_LINEAGE_AND_HIPPOCAMPAL_SCOPE |

## Outcome counts

- A0_FIDELITY: **9**
- A1_FIDELITY: **0**
- A2_FIDELITY: **0**
- FAILURE_LOCALIZED: **0**
- UNDERDETERMINED: **0**
- SOURCE_INELIGIBLE: **0**

全9本で A0 が source-grounded に成立したため、A1/A2 は protocol 上 NOT_REACHED。再構築困難を理由に A2 を推定していない。

## Added structure

- added stateless adapters: **0**
- added stateful coordination mechanisms: **0**
- added assumptions: **0**

ATT-01 の Stage C correction 1件は、既に source-defined な response-likelihood branch の明示化であり、追加 adapter/assumption ではない。

## Negative / adverse evidence retained

主なもの:
- ATT-02: fine temporal dynamics / synchrony / noise correlation / surround suppression の非モデル化、+20% parameter sensitivity。
- ATT-03: companion derivational supplement 未取得、定量 fit / biophysical circuitry / onset dynamics の非提示、inherited normalization provenance。
- BLF-01: cross-source null、reproduction-task null、12 vs 16 coefficient discrepancy、three vs four alternative-description discrepancy、S1 未確認。
- BLF-02: flat model と delta rule の equivalence は **conditional**。persistent prior counts が差を残し、zero-prior large-n のみ asymptotic identity。
- BLF-03: hazard-rate learning bias と suboptimal approximation の限定。
- CNC-01: vague concept に対する deterministic likelihood 制約、conditional primitive 欠如。
- CNC-02: training memorization でも generalization failure があり、複数の neural solution が source 上 viable。
- CNC-03: hippocampal-only scope と inherited C-HORSE lineage。

## Unresolved blockers / exceptions

最終 state を UNDERDETERMINED にするほど central reconstruction を破壊する blocker は無い。ただし source-fidelity exception は残す:
- ATT-03: companion derivational supplement 未取得。A0 は frozen main equations / main-text limiting conditions に限定。
- BLF-01: publication-description discrepancies と未確認 S1。
- CNC-02: source 内で biological implementation が non-unique。
- W9 の residual genealogy uncertainty は全9本で継続。

## Fail-closed

`test_m1_fail_closed.py` は要求された 25 条件を個別に検査し、GitHub Actions run **37283369126** で **25/25 PASS / SUCCESS**。

CI は exact scientific HEAD `fddeefaaa209623c95858e578fa3d31a3389e672` に対して実行された。

## Boundary confirmations

- roster replacement: **なし**
- backup activation: **なし**
- M2-M6 scientific processing: **なし**
- genealogy-independence promotion: **なし**
- global genealogical independence assumed: **false**
- G1 PILOT20 counted as MAIN evidence: **false**
- Grammar v0 modification: **なし**
- RIR v2.3.1 modification: **なし**
- aggregate H0/H1/H2 majority claim: **なし**

**M1 単独では Paper 2 全体の H0/H1/H2 を決定しない。** ここでの A0 は各 source model に限定された direct-composition evidence であり、M7 の40本統合以前に universal architecture や majority H conclusion へ昇格させない。
