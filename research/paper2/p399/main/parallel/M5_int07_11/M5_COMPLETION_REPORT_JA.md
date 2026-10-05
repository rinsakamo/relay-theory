# RelayTheory Paper 2 — MAIN M5 完了報告

M5 は INT-07〜INT-11 の 5 本のみを、kickoff `3c2761ac13b04203aa7dbd8f47a1d687d506bf7b` から独立処理した。MAIN40 manifest blob は `b97b67a34ad9c2858745dfa6aa60444520eaab13`。G1 PILOT20 は MAIN evidence から除外した。

## Freeze chronology
- Stage A: `986b1447c9d50bd65ef8acfb06277e7f692d9197`
- Stage B: `a1bcf79923dcb8939ae0663be703ab4008a43ce3`（50 objections）
- Stage C: `17c49300c649e9bc33964a57f6de604e786201d0`（50 source reopen / 50 C2 conditions / accepted patch 0 / duplicate patch 0）

## 結果
| slot | what integrates what | outcome |
|---|---|---|
| INT-07 | state/observation + forward/backward + latent-input inference | A0_FIDELITY |
| INT-08 | LSTM/decision + source-defined EM retrieval gate + episodic store + LCA | A0_FIDELITY |
| INT-09 | state-dependent observation + estimator + affine feedback/feedforward controller | A0_FIDELITY |
| INT-10 | BG learner + CPG + cerebellar error-correction pipeline | A0_FIDELITY |
| INT-11 | FI + OI + joint context estimate + context-conditioned TD map | A0_FIDELITY |

Counts: A0=5, A1=0, A2=0, FAILURE_LOCALIZED=0, UNDERDETERMINED=0, SOURCE_INELIGIBLE=0。

reconstruction-added stateless interface = 0、reconstruction-added stateful mechanism = 0。source-defined gate/mediator は source-native のまま保持し、INT-08 の retrieval gate を A2 として二重計上していない。INT-08 の encoding 条件と INT-11 の joint-interaction window は experimenter/modeler-imposed として保持した。

INT-07 open-loop/policy 境界・Gamma/offline beta-alpha-beta、INT-09 original/corrected Fig9 と未凍結 S1、INT-10 Funding-only correction、INT-11 manual schedule / exploratory confidence threshold を negative/adverse evidence として保持。blocking unresolved = 0。roster replacement = 0、backup activation = 0、genealogy independence は仮定していない。

Draft PR 番号と final HEAD は PR 作成後の GitHub metadata を authority とする（commit SHA の自己参照は埋め込まない）。

**M5 単独では Paper 2 全体の H0/H1/H2 を決定しない。**
