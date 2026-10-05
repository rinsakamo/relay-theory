# P399 MAIN M6 — INT-12〜INT-16 完了報告

日付: 2026-10-05 JST

## Authority / isolation

- Branch: `paper2/p399-main-m6-int12-16-20261005`
- Exact kickoff base: `3c2761ac13b04203aa7dbd8f47a1d687d506bf7b`
- MAIN GO: Draft PR #452
- W9 authority: Draft PR #451 / `71aab1c485446223bc8951ea3b8978aaeece3279`
- MAIN40 manifest blob: `b97b67a34ad9c2858745dfa6aa60444520eaab13`
- Method: RIR v2.3.1 source-closed-C, frozen Grammar v0
- Substantive writes: `research/paper2/p399/main/parallel/M6_int12_16/` only
- Scientific completion snapshot before this report commit: `4397aa4d4e898d5e8d95ce0875469597abaa2671`
- このファイル自身を含む最終 Git HEAD は自己参照できないため、Draft PR head / 対話の最終完了報告を exact final HEAD authority とする。

## Five-paper status

| Slot | DOI | Final state | What integrates what |
|---|---|---|---|
| INT-12 | 10.1371/journal.pcbi.1006116 | A0_FIDELITY | reward cluster + mapping/transition cluster を source-defined planning が policy に結合。source-defined meta-agent extension は independent/joint strategy を model evidence で選択。 |
| INT-13 | 10.1371/journal.pcbi.1014796 | A0_FIDELITY | parallel RL + capacity-limited WM を source-defined weighted mixture で統合し、その policy が LBA drift を駆動。set-size-dependent threshold も source-defined。 |
| INT-14 | 10.1371/journal.pcbi.1007594 | A0_FIDELITY | graph evidence から connected hierarchy H を Bayesian/MCMC inference し、同じ H を HBFS planning が利用。 |
| INT-15 | 10.1371/journal.pcbi.1010047 | A0_FIDELITY | MB/MF values と derived conflict を source-defined DDM に直接入力し、drift/boundary dynamics で choice/RT を生成。 |
| INT-16 | 10.1371/journal.pcbi.1004060 | A0_FIDELITY | response selection feedback が traces→tags を形成し、global RPE/neuromodulatory signal が tagged synapse plasticity を gate。 |

## Counts

- A0_FIDELITY: **5**
- A1_FIDELITY: **0**
- A2_FIDELITY: **0**
- FAILURE_LOCALIZED: **0**
- UNDERDETERMINED: **0**（paper-level final state。局所的 underdetermination は下記の limitation として保持）
- SOURCE_INELIGIBLE: **0**
- Total: **5**

## Integration boundary result

source-defined hierarchy/arbitration/gating と reconstruction-added mechanism を分離した。

- INT-12: CRP task clustering は representation。meta-agent は source-defined extension であり A2 ではない。
- INT-13: RL/WM weighted mixture と proactive decision-bound modulation は source-defined interaction/control。WM state / LBA accumulator は追加 coordinator ではない。
- INT-14: H は source-defined hierarchical representation。MCMC chain bookkeeping / HBFS frontier は generic executive state へ昇格させない。
- INT-15: MB/MF combination、conflict regressor、DDM accumulation から persistent arbitration state を追加しない。
- INT-16: selected-response feedback と global RPE/neuromodulation は source-defined plasticity gates。generic executive control へ昇格させない。

Reconstruction-added stateless interfaces: **0**  
Reconstruction-added stateful mechanisms: **0**

## Negative / adverse evidence retained

- INT-12: human learning が independent / joint / mixture のどれかは open。unknown-transition S1 は byte-frozen でなく noncanonical。
- INT-13: **AUTHOR_APPROVED_FROZEN_PUBLISHER_PROOF** を維持。corrected final VoR へ silent upgrade していない。S1 raw bytes 未凍結。clinical fit は causal neural implementation を確立しない。
- INT-14: exact posterior は intractable で MCMC approximation。HBFS は唯一の cognitively plausible planner と確立されていない。INT-01 との CRP sharing は constituent-level。
- INT-15: within/between-system conflict は強く相関し exact form は task から同定不能。combined DDM は source 自身が statistical approximation と限定。action-conflict effect は弱い/逆方向のケースを保持。
- INT-16: persistent activity の biophysical mechanism は source が一意に指定しない。AuGMEnT は SARSA(lambda) eligibility-trace correspondence を持つ。simulation は direct in-vivo proof ではない。

## Genealogy boundary

W9 annotations は provenance / limitation としてのみ保持した。

- NO_PATH_FOUND => INDEPENDENT を使用していない。
- NO_CITATION => INDEPENDENT を使用していない。
- BOUNDED_SOURCE_NATIVE_DIFFERENCE => INDEPENDENT を使用していない。
- INT-14 の INT-01 CRP relation は `SHARED_CONSTITUENT_ONLY` のまま。
- INT-15/P18 と INT-16/P09 は bounded difference のまま。
- global genealogical independence は **assumed / promoted していない**。

## Fail-closed

`M6_FAIL_CLOSED_TEST_RESULTS_v1.json` に 34 tests を固定。

- PASS: **34**
- FAIL: **0**
- Result: **PASS_34_OF_34**

Stage freeze genealogy:
- Stage A final: `949347fa32ddb4af51832d25d3d9dca5ba3f79f2`
- Stage B final: `6343c736266b5cbe6eb0202b4503888459ba02a1`
- Stage C final: `b2b7a022bdd78bad1ac2d93b2f33e6b337c38521`
- Grammar/outcomes final: `daff12a534bad89f4b3a10a0d4e7e5a30c421b8e`

## Denominator / verdict guardrails

- roster replacement: **none**
- backup activation: **none**
- G1 PILOT20: **MAIN evidence から除外**
- all five remain in MAIN denominator
- M6 単独では overall **H0/H1/H2 を決定しない**
