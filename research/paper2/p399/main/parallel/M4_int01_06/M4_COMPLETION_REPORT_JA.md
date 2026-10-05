# RelayTheory Paper 2 — MAIN M4 Completion Report (JA)

## Authority / scope

- Issue: #399
- Branch: `paper2/p399-main-m4-int01-06-20261005`
- Exact kickoff base SHA: `3c2761ac13b04203aa7dbd8f47a1d687d506bf7b`
- MAIN GO: Draft PR #452
- W9 authority: Draft PR #451 / `71aab1c485446223bc8951ea3b8978aaeece3279`
- MAIN40 manifest blob: `b97b67a34ad9c2858745dfa6aa60444520eaab13`
- RIR v2.3.1 reference HEAD: `7f8750c5f4b1b87095f7dfdfbb558bba8e1c4157`
- Grammar: frozen Grammar v0
- Stage authority commits:
  - Source authority lock: `a4ef8fbdafc3870ef100bafbfaed20f46adbe87f`
  - Stage A: `0992a46f38f4beefb4bf6f29a69a4b9637390e12`
  - Stage B: `cc1228ff16a612165e0d35caaa7d89c86ad556ae`
  - Stage C: `873031d8d45e7b41e6c89fb3c73c879d42e05900`
  - Grammar-v0 reconstruction freeze: `41a2d4d83968a7b5a0b3ae746742853116017797`
  - Per-paper completion: `eb9d35119b555dd815364e2e458de56a3cb25939`

- Draft PR: **#458** — `P399 MAIN M4 — INT01-06 source-closed reconstruction and architectural adjudication`
- Exact scientific/CI HEAD: `da4f7f6996e20625778a9bc1907923a770d74901`
- CI run: **37292314079 SUCCESS**
- CI job: `m4-fail-closed` / **36/36 PASS**

この completion report 追記自体は metadata-only commit とする。自己参照を避けるため、この本文には追記後 branch HEAD を埋め込まず、GitHub PR/ref を最終 ref authority とする。

## 6-paper status

| Slot | DOI | Final state | Source fidelity |
|---|---|---|---|
| INT-01 | 10.1016/j.cognition.2024.105967 | A0_FIDELITY | SOURCE_FIDELITY_BOUNDED_BY_AUTHOR_APPROVED_CODE_AND_PUBLISHED_LIKELIHOOD_AMBIGUITY |
| INT-02 | 10.3390/e26060484 | A0_FIDELITY | SOURCE_FIDELITY_BOUNDED_BY_EQ9_PRINTED_OMISSION_AND_SIMULATION_SCOPE |
| INT-03 | 10.1073/pnas.95.24.14529 | A0_FIDELITY | SOURCE_FIDELITY_BOUNDED_BY_FIRSTPARTY_HTML_AND_PARTIAL_STROOP_SCOPE |
| INT-04 | 10.1038/s41562-023-01799-z | A0_FIDELITY | SOURCE_FIDELITY_WITH_FROZEN_MAIN_SUPPLEMENT_REPORTING_BUNDLE_AND_BOUNDED_SEMANTIC_AUDIT |
| INT-05 | 10.1371/journal.pcbi.1004110 | A0_FIDELITY | SOURCE_FIDELITY_WITH_EXPLICIT_SYSTEM_WORLD_BOUNDARY_AND_VARIANT_NONUNIQUENESS |
| INT-06 | 10.1371/journal.pcbi.1000765 | A0_FIDELITY | SOURCE_FIDELITY_WITH_OFFICIAL_SUPPLEMENT_BUNDLE_AND_SOURCE_DEFINED_ROUTER_STATE |

## Outcome counts

- A0_FIDELITY: **6**
- A1_FIDELITY: **0**
- A2_FIDELITY: **0**
- FAILURE_LOCALIZED: **0**
- UNDERDETERMINED: **0**
- SOURCE_INELIGIBLE: **0**

全6本で、source-adjudicated mechanism と load-bearing dependency を frozen Grammar v0 に直接再構成できた。A0 が PASS したため A1/A2 は protocol 上 NOT_REACHED。統合が複雑、再帰的、workspace 的であることだけから A2 を推定していない。

## What integrates what

- **INT-01:** context/task-set inference + retained task-set policies を、source-defined Bayesian posterior / meta-policy weighting が hierarchical/compressed policy selection・composition と結合する。
- **INT-02:** DPEFE planning policy + counterfactual-learning policy を、source-defined entropy-dependent `beta(s,t)` と geometric/product pooling が統合する。
- **INT-03:** specialized/local processors + long-range recurrent global workspace を、source-defined recurrent gating、reward/vigilance、plasticity が統合する。
- **INT-04:** hippocampal/MHN rapid-memory teacher + cortical VAE/generative student を、source-defined offline replay/training flow が結合する。extended model では novelty/prediction residual path を追加する。
- **INT-05:** decision/evidence dynamics + action preparation/movement dynamics を統合し、Model 4 では source-defined physical position feedback が decision へ戻る closed loop を形成する。
- **INT-06:** parallel sensory/local processors + task-set/NMDA router + response-threshold circuit を、source-defined gating/buffering/reset が統合する。

## Source-defined coordination mechanisms

source-defined な coordination/state は消していない。

- INT-01: CRP context/task-set posterior、Bayesian meta-policy weighting、working-memory action mask。
- INT-02: state-dependent `beta(s,t)`、policy pooling。
- INT-03: recurrent global workspace、ascending/descending gating、reward/vigilance/plasticity。
- INT-04: teacher/student coupling through offline replay。これは separate persistent coordinator state ではなく source training flow。
- INT-05: decision-action feedback loop。body/world position は System/World boundary を越える source-defined feedback として保持。
- INT-06: task-set populations、NMDA router、response threshold、inhibitory reset。

これらは **原著側の機構**であり、reconstruction-added A2 として二重計上していない。

## Reconstruction-added structure

- reconstruction-added stateless interfaces: **0**
- reconstruction-added stateful mechanisms: **0**
- added assumptions: **0**
- generic universal coordinator: **なし**

## Retained negative / adverse evidence

- **INT-01:** published likelihood ambiguity は残存。adopted softmax は frozen prepublication author code に基づく user-approved research interpretation であり publisher corrigendum ではない。private MHT は public Git に出していない。75% vs 82.359% mismatch、repeat-condition null、parameter recovery limits も保持。
- **INT-02:** printed Eq.9 normalization omission を silent repair していない。historical code は VoR と別。Eq.8/Eq.16 は global identity ではない。mixed policy の優位は regime-specific。
- **INT-03:** adopted medium は official complete PNAS HTML。raw publisher bytes/SHA 不在、correction history 非網羅、partial Stroop simulation、Fig.3 simulation status を保持。
- **INT-04:** MHN/VAE/teacher-student primitives の prior existence、decay/deletion/capacity の非シミュレーション、basic vs extended novelty 差、supplement semantic audit の boundedness を保持。
- **INT-05:** embodiment を内部 cognitive state へ wholesale に移していない。biomechanics/action costs の簡略化、4 variants の非一意性、external code の edition 分離を保持。
- **INT-06:** finite router scope、task-order ablation でも PRP が残ること、supplementary null/semantic limits、INT-03 shared-framework-only relation を保持。

## Unresolved blockers / exceptions

最終 state を UNDERDETERMINED / SOURCE_INELIGIBLE にする decisive central-reconstruction blocker は **0**。ただし source-fidelity exceptions は上記の通り残り、M7 でも消してはならない。

特に:
- INT-01 の publisher-expression / author-code ambiguity は未解消の source record。
- INT-03 は raw publisher-byte hash と exhaustive correction reconciliation がない。
- INT-04 / INT-06 は frozen supplement bundle を持つが全 pixel/equation semantic の exhaustive certification ではない。
- INT-05 は source model space が一部 non-unique。
- 全6本で W9 residual genealogy uncertainty は継続。

## Genealogy boundary

- roster change: **なし**
- backup activation: **なし**
- genealogyによる post-hoc exclusion: **なし**
- global genealogical independence assumed: **false**
- bounded source-native difference => independence: **していない**
- INT-03 direct-extension ancestry: **provenance only**
- INT-06 direct implementation descent: resolved two predecessors only
- INT-03 -> INT-06 direct descent: **assertedしていない**（shared framework only）

## G1 / MAIN denominator

- G1 PILOT20 counted as MAIN evidence: **false**
- G1 PILOT20 counted in MAIN denominator: **false**
- M4 denominator: exact frozen G2 MAIN40 のうち INT-01〜INT-06 の **6/40**
- roster replacement: **0**
- backup activation: **0**

## Fail-closed

`test_m4_fail_closed.py` は要求31項目を包含する **36条件**を個別検査。

GitHub Actions run **37292314079**:
- workflow: `P399 MAIN M4 fail-closed`
- job: `m4-fail-closed`
- result: **SUCCESS**
- `Run 36 fail-closed checks`: **SUCCESS**
- exact scientific/CI HEAD: `da4f7f6996e20625778a9bc1907923a770d74901`

## Final boundary statement

**M4 単独では Paper 2 全体の H0/H1/H2 を決定しない。**

今回の 6/6 A0 は、各原著の source-defined integration mechanism を frozen Grammar v0 で reconstruction-added coordinator なしに保持できたという **source-scoped result** である。40本の aggregate H evidence、cross-lane consistency、genealogy limitation を含む全体判定は M7 integration の authority に残す。
