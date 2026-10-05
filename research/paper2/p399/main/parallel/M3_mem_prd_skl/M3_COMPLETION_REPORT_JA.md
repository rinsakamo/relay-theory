# RelayTheory Paper 2 — MAIN M3 完了報告

## Authority / scope

- Branch: `paper2/p399-main-m3-mem-prd-skl-20261005`
- Exact kickoff base: `3c2761ac13b04203aa7dbd8f47a1d687d506bf7b`
- MAIN40 manifest blob: `b97b67a34ad9c2858745dfa6aa60444520eaab13`
- W9 authority: PR #451 / `71aab1c485446223bc8951ea3b8978aaeece3279`
- RIR v2.3.1 authority: PR #401 / `7f8750c5f4b1b87095f7dfdfbb558bba8e1c4157`
- Grammar v0 blob: `a688edb063c0ad43c25df15f497918817e8b74cd`
- G1 PILOT20 は MAIN evidence / denominator に含めていない。
- roster replacement = 0、backup activation = 0。
- genealogy independence は仮定していない。W9 bounded genealogy clearance = 0 を維持する。

## Nine-paper status

| Slot | DOI | Source fidelity | Final state | Adapter | Added stateful mechanism |
|---|---|---|---|---:|---:|
| MEM-01 | 10.1007/s42113-023-00189-y | SOURCE_CLOSED_HTML_AUTHORITY_WITH_RAW_PDF_UNFROZEN_LIMITATION | A0_FIDELITY | 0 | 0 |
| MEM-02 | 10.1371/journal.pcbi.1008367 | SOURCE_CLOSED_WITH_EXPLICIT_LIMITATIONS | A0_FIDELITY | 0 | 0 |
| MEM-03 | 10.1371/journal.pcbi.1004003 | SOURCE_CLOSED_WITH_MANDATORY_S1_AND_EXPLICIT_LIMITATIONS | A0_FIDELITY | 0 | 0 |
| PRD-01 | 10.1038/s41562-024-01930-8 | BOUNDED_SOURCE_FIDELITY_WITH_REGISTERED_EDITION_AND_FIG_S2_EXCLUSIONS | A0_FIDELITY | 0 | 0 |
| PRD-02 | 10.1371/journal.pcbi.1001003 | SOURCE_CLOSED_WITH_EXPLICIT_LIMITATIONS | A0_FIDELITY | 0 | 0 |
| PRD-03 | 10.1371/journal.pcbi.1007093 | SOURCE_CLOSED_WITH_EXPLICIT_LIMITATIONS | A0_FIDELITY | 0 | 0 |
| SKL-01 | 10.1371/journal.pcbi.1012455 | SOURCE_CLOSED_WITH_CONDITIONAL_CONVERGENCE | A0_FIDELITY | 0 | 0 |
| SKL-02 | 10.1371/journal.pcbi.1005632 | SOURCE_CLOSED_WITH_EXPLICIT_LIMITATIONS | A0_FIDELITY | 0 | 0 |
| SKL-03 | 10.1371/journal.pcbi.1006839 | SOURCE_CLOSED_WITH_DATA_MODEL_SEPARATION | A0_FIDELITY | 0 | 0 |

## Counts

- A0_FIDELITY: **9**
- A1_FIDELITY: **0**
- A2_FIDELITY: **0**
- FAILURE_LOCALIZED: **0**
- UNDERDETERMINED: **0**
- SOURCE_INELIGIBLE: **0**

A0 は「凍結 Grammar v0 の role のままで、source-defined な state / transition / interface / readout を忠実に再構成できた」という局所 fidelity 判定である。M3 は H0/H1/H2 の全体判定を発行しない。

## MEM / PRD / SKL boundary

memory state と predictive latent、retained model と learned parameter、prediction と retrieval、skill policy と action-selection interface、replay と planning、learned transition model と episodic trace、offline consolidation と online control、prediction error と learning signal、external trajectory と internal memory を個別監査した。いずれも source-specific distinction を保持し、便宜的 homogenization は行っていない。

## Added structure

- stateless adapters added: **0**
- stateful coordination mechanisms added: **0**
- source-defined memory / prediction / skill state の二重計上: **0**

## Adverse evidence retained

PRD-01 は NIH/PMC author manuscript + formal publisher correction + official supplement の bounded bundle のまま保持し、corrected publisher VoR とは呼んでいない。公式 supplement Fig S2 Study2 の diagram / caption / corrected-main 間の矛盾は修復せず、unsupported quantitative claim から除外した。SKL-01 は exact convergence の全条件と stochastic exploration の O(|sigma_u|) neighborhood limitation を保持した。MEM-01 の ACT-R 非 DOI ancestry、MEM-03/SKL-01/SKL-03 の W8-S source closures、SKL-03 の data-file / mathematical-model distinction も維持した。

## Remaining blockers / limitations

最終 architectural state を UNDERDETERMINED とした紙はないが、source-level uncertainty は消していない。主な残差は MEM-01 の biological decay/interference interpretation、MEM-02 の delay-to-beta interpretation、PRD-01 の登録済み出版矛盾、PRD-03 の transition acquisition / gamma-sigma identifiability、SKL-01 の neural implementation と conditional convergence、SKL-02 の human synaptic implementation、SKL-03 の latent intended aim / local phenomenology である。

## Fail-closed / CI

31 項目の fail-closed guard を `test_m3_fail_closed.py` に固定する。CI はこの completion artifact 群を凍結した後の final branch HEAD に対して実行し、run ID / conclusion は Draft PR check を authority とする。

## Explicit non-conclusions

M3 単独では overall Paper 2 H0/H1/H2 を決定しない。A0_FIDELITY の 9/9 は歴史的 genealogy independence、普遍的 cognitive architecture、脳レベル実装、または RelaySelf 工学上の優位性を意味しない。
