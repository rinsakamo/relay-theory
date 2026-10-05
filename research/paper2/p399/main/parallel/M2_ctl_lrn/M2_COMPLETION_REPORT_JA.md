# RelayTheory Paper 2 — MAIN M2 CTL/LRN 完了報告

## Authority / isolation

- Primary authority: Issue #399
- MAIN GO authority: Draft PR #452
- M2 Draft PR: #455 — `P399 MAIN M2 — CTL/LRN source-closed reconstruction and architectural adjudication`
- Branch: `paper2/p399-main-m2-ctl-lrn-20261005`
- Exact kickoff base: `3c2761ac13b04203aa7dbd8f47a1d687d506bf7b`
- Frozen MAIN40 manifest blob: `b97b67a34ad9c2858745dfa6aa60444520eaab13`
- Stage A all-six freeze HEAD: `935c5c9b12949758148a32f16ce52cddb64661e3`
- Stage C all-six freeze HEAD: `e563741558c2ceb2e1b4017018a1a87901fbd6f4`
- W9 authority HEAD: `71aab1c485446223bc8951ea3b8978aaeece3279`
- RIR v2.3.1 authority HEAD: `7f8750c5f4b1b87095f7dfdfbb558bba8e1c4157`
- substantive outputs: `research/paper2/p399/main/parallel/M2_ctl_lrn/` only
- shared MAIN result registries: 未変更
- M1 / M3–M6 scientific outputs: 未変更

最終PR HEADはこのファイル自身を含むcommitで変化するため、Draft PR metadata と外部完了報告を exact final HEAD authority とする。

## 6-paper result

| slot | DOI | source fidelity | final state | A0 | A1 | A2 | adapters | added stateful |
|---|---|---|---|---|---|---|---:|---:|
| CTL-01 | 10.1371/journal.pcbi.1012228 | SOURCE_CLOSED_ADJUDICATED | A0_FIDELITY | PASS | not needed | not attempted | 0 | 0 |
| CTL-02 | 10.7554/eLife.12029 | SOURCE_CLOSED_ADJUDICATED | A0_FIDELITY | PASS | not needed | not attempted | 0 | 0 |
| CTL-03 | 10.7554/eLife.28040 | SOURCE_CLOSED_ADJUDICATED | A0_FIDELITY | PASS | not needed | not attempted | 0 | 0 |
| LRN-01 | 10.1038/s41467-025-58848-6 | SOURCE_CLOSED_ADJUDICATED | A0_FIDELITY | PASS | not needed | not attempted | 0 | 0 |
| LRN-02 | 10.1371/journal.pcbi.1007963 | SOURCE_CLOSED_ADJUDICATED | A0_FIDELITY | PASS | not needed | not attempted | 0 | 0 |
| LRN-03 | 10.7554/eLife.21492 | SOURCE_CLOSED_ADJUDICATED | A0_FIDELITY | PASS | not needed | not attempted | 0 | 0 |

Counts:

- A0_FIDELITY = **6**
- A1_FIDELITY = **0**
- A2_FIDELITY = **0**
- FAILURE_LOCALIZED = **0**
- UNDERDETERMINED = **0**
- SOURCE_INELIGIBLE = **0**

A0 は source-architectural reconstruction fidelity の判定であり、系譜独立・生物学的実装・Paper 2 全体仮説の証明ではない。

## Source-closed chronology

6本すべてで以下を順序固定した。

1. authority/source lock
2. Stage A source-first decomposition
3. Stage A freeze
4. Stage B result-informed re-audit
5. Stage C source-closed adjudication
6. adjudicated source reconstruction freeze
7. frozen Grammar-v0 reconstruction
8. A0 attempt
9. A1/A2 gate evaluation
10. final permitted per-paper state
11. limitations / adverse evidence retention

RIR v2.3.1 の C1/C2 を適用した結果、B の攻撃点はすべて original Stage A ですでに境界づけられていた。したがって **append-only C patch = 0**。既存Aにある内容を重複パッチすることを避けた。

Standalone supplement は W9/profile provenance として identity / role / missing raw-SHA gap を保持したが、RIR v2.3.1 source-closed scope に従い、full HTMLに埋め込まれていない standalone content を新しい M2 A/B/C 根拠として導入していない。

## CTL/LRN boundary findings

- controller state vs learned parameter: 分離維持
- control update vs learning update: 分離維持
- policy execution vs policy acquisition: 分離維持
- value computation vs control: 分離維持
- environmental adaptation vs internal learning: 分離維持
- meta-control vs task instruction: 分離維持

主な境界所見:

- CTL-01: policy-prior learning と decision-local MCMC/eta を分離。DDM comparator を同一機構にしない。
- CTL-02: source-defined uncertainty/TAN feedback は保持するが、新しい上位 coordinator を二重追加しない。OpAL は継承。
- CTL-03: task demand / cTBS は World/intervention。DCM latent state/fit parameter を learned coordinator にしない。
- LRN-01: learned representation は test 時に保持されるが active coordinator とは数えない。feature variant の embedding は experimenter-defined。
- LRN-02: external switching schedule と internal volatility inference を分離。softmax は choice readout。
- LRN-03: value network は learning aid / baseline で、学習後 execution controller へ昇格させない。

## Added architecture

- added stateless adapters: **0**
- added persistently stateful mechanisms: **0**

source-defined CTL/LRN state は「追加 stateful mechanism」へ再計上していない。

## Negative / adverse evidence retained

代表例:

- CTL-01: base BCC inheritance; simulation scope; DDM non-identity; supplement raw-SHA gap.
- CTL-02: OpAL inheritance; cross-level analogy is not direct biological proof; experimental prediction testing remains prospective.
- CTL-03: present-sample 913-model search nonuniqueness; 19 plausible models before prior-sample adjudication; unexamined model-space alternatives; prior trait relation nonreplication; unexpected caudal Temporal-Control effect.
- LRN-01: generic policy-gradient inheritance; experimenter-defined feature embedding; direct neural implementation not established; supplement raw-SHA gap.
- LRN-02: approximate inference; binary moment matching / inference-only omega; switching-vs-generative mismatch; latent vs observation-space learning-rate distinction; supplement raw-SHA gap.
- LRN-03: inherited recurrent policy gradient; weak biological constraints / exact learning-rule plausibility; value network learning-vs-execution distinction.

Blocking unresolved blocker = **0**。ただし nonblocking source/model/genealogy uncertainty は消去していない。

## Genealogy boundary

W9 annotationsをそのままcontextとして保持した。

- global genealogical independence assumed = **false**
- bounded genealogy clearance = **0**
- ancestry exhaustiveness = **NOT_ATTESTED**
- `NO_PATH_FOUND => INDEPENDENT` を使用していない
- `NO_CITATION => INDEPENDENT` を使用していない
- `BOUNDED_SOURCE_NATIVE_DIFFERENCE => INDEPENDENT` を使用していない
- M2内部15 pairの bounded difference/shared constituent annotation は limitation として保持
- genealogy による roster alteration = **なし**

## MAIN denominator / roster

- exact frozen G2 MAIN40のみ
- G1 PILOT20 = MAIN evidence から **除外**
- G1 PILOT20 = MAIN denominator から **除外**
- roster replacement = **なし**
- backup activation = **なし**
- six papers all remain in M2 denominator

## Fail-closed validation / CI

`test_m2_fail_closed.py` はユーザー指定26項目を包含し、paper-local反復を含めて実行時に exact PASS count を出力する。isolated workflow:

`.github/workflows/p399-main-m2-ctl-lrn.yml`

CI run ID / final status は tracked report の自己参照更新を避けるため Draft PR metadata と外部完了報告を authority とする。

## H boundary

**M2 alone does not determine overall H0 / H1 / H2.**

M2は6本の source-closed reconstruction と architectural adjudication のみを完了した。全体結論は M7 以降の shared aggregation authority に委ねる。
