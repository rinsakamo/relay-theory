# RelayTheory Paper 2 — G4 Genealogy W3 完了報告

- Authority: Issue #399
- Accelerator: Draft PR #438
- W3 Draft PR: #442
- W3 branch: `paper2/p399-g4-w3-mem-prd-skl-native-20261005`
- exact base (PR #438 head at branch creation): `ae044a8f475fb0dc9140a91e360e1ff26a0b5e3a`
- scope: MEM-01/02/03, PRD-02/03, SKL-01/02/03 の8本のみ
- PRD-01: **比較対象のみ**。W3 profile として新規登録していない。
- MAIN scientific authorization: **false / NO-GO**
- global family independence certified: **0**

## 1. 8本の最終W3状態

| slot | DOI | status | source-native 中央機構（限定要約） |
|---|---|---|---|
| MEM-01 | 10.1007/s42113-023-00189-y | SCIENTIFIC_ANCESTRY_UNDERDETERMINED | ACT-R宣言記憶のtrace/base-level decay、contextual spreading activation、競合/partial-matching retrieval、blending reconstruction |
| MEM-02 | 10.1371/journal.pcbi.1008367 | PROFILE_FRAGMENT_READY | semantic generative model、beta-VAE rate-distortion encoding、latent reconstruction、delay-indexed compression variant |
| MEM-03 | 10.1371/journal.pcbi.1004003 | SOURCE_BLOCKED | population superposition storage、noisy population state、cue-conditioned Bayesian recall、mixed/hierarchical code variants |
| PRD-02 | 10.1371/journal.pcbi.1001003 | PROFILE_FRAGMENT_READY | reward-structure belief state、Bayesian reward/structure update、belief-state action selection、fixed/Q-learning comparators |
| PRD-03 | 10.1371/journal.pcbi.1007093 | PROFILE_FRAGMENT_READY | hidden trial-state HMM、observation likelihood integration、B/gamma past-evidence gate、posterior response likelihood |
| SKL-01 | 10.1371/journal.pcbi.1012455 | SOURCE_BLOCKED | synergy-factorized forward map、perceptual recency state、forward-error gradient、inverse-control gradient + exploration |
| SKL-02 | 10.1371/journal.pcbi.1005632 | PROFILE_FRAGMENT_READY | SORN recurrent dynamics、STDP、intrinsic plasticity、synaptic normalization、supervised motor readout |
| SKL-03 | 10.1371/journal.pcbi.1006839 | SOURCE_BLOCKED | last-success aim cache、reinforcement-gated aim update、outcome-dependent exploration variance、local reward-landscape sampling |

集計: **READY 4 / SOURCE_BLOCKED 3 / SCIENTIFIC_ANCESTRY_UNDERDETERMINED 1**。

## 2. source / edition / provenance

G2の凍結 working roster は
`research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json`
Git blob `b97b67a34ad9c2858745dfa6aa60444520eaab13`、
既存original-source receiptは
`research/paper2/p399/g2/MAIN40_G2_ACTUAL_SOURCE_RECEIPTS_AND_DECISIONS_v2.json`
Git blob `ac3ffa59fcdc078550df587bc972632b7ca5ff7f`
を exact base ref `ae044a8f475fb0dc9140a91e360e1ff26a0b5e3a` で照合した。

PLOS 7本は既存receiptのpublisher VoR PDF raw SHA256を保持した。MEM-01だけは既存G2 receiptでpublisher PDF bytesが取得されていないため、SpringerのVersion-of-Record complete HTMLを採用し、raw SHA256は **nullのまま** とした。HTMLとPDFをbyte-equivalentとは扱っていない。

W3のpublisher-page/correction sweepでは8本について新たなcorrection/corrigendumを確認しなかったが、これは2026-10-05時点のbounded sweepであり「将来も存在しない」という網羅主張ではない。

## 3. direct model ancestry

DOIを source-explicit に固定できたものだけを記録した。

- SKL-01: Pierella et al. 2019 `10.1371/journal.pcbi.1007118`; Jordan & Rumelhart 1992 `10.1207/s15516709cog1603_1`
- SKL-02: original SORN Lazar, Pipa & Triesch 2009 `10.3389/neuro.10.023.2009`
- SKL-03: Pekny et al. 2015 `10.1523/JNEUROSCI.3244-14.2015`; Therrien et al. 2018 `10.1523/ENEURO.0050-18.2018`

MEM-01のACT-Rは明白な歴史的継承を含むが、中央機構全体についてDOI-onlyの網羅的direct chainをsource-pinnedできないため、祖先DOIを推測投入せず `SCIENTIFIC_ANCESTRY_UNDERDETERMINED` とした。全8本で `ancestry_exhaustiveness = NOT_ATTESTED` を維持した。

## 4. source blockers

### MEM-03
`10.1371/journal.pcbi.1004003.s001` (S1 Text) に中央モデルの追加数学導出が含まれるが、現G2 receiptにraw bytes/SHAがない。main PDFだけで完全数学閉包とはしない。

### SKL-01
`10.1371/journal.pcbi.1012455.s001` (S1 File) にHML model details/convergence analysisがあるがraw freezeがない。main equationsとの不整合を検査できるまでSOURCE_BLOCKED。

### SKL-03
`10.1371/journal.pcbi.1006839.s002` (S2 Data) と `.s003` (S3 Data) がtrial-level variability / bootstrap best-fit parameter chainを担うがraw freezeがない。パラメータをmainから推定・補完しない。

## 5. bounded pair adjudication

必須比較対象を全件明示レコード化した。

- W3内部: **28/28**
- W3 × G1 20本: **160/160**
- W3 × 現在profile済G2 6本: **48/48**
- 合計: **236/236**

判定内訳:

| judgment | count |
|---|---:|
| DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY | 0 |
| SHARED_CONSTITUENT_ONLY | 21 |
| BOUNDED_SOURCE_NATIVE_DIFFERENCE | 45 |
| UNDERDETERMINED | 170 |

共有語彙（memory, prediction, motor learning, Bayesian, reinforcement, internal model等）だけでは系譜一致にしなかった。また `BOUNDED_SOURCE_NATIVE_DIFFERENCE` を global independence へ写像していない。236件すべて `global_independence_conclusion=false` / `may_be_counted_independent=false`。

特にreview priorityでは、PRD-02/P08・PRD-03/P08を「Bayesian/HMM constituent共有」に限定し、SKL-01/P20・SKL-03/P20も「motor exploration/controller constituent共有」に限定した。SKL-02/P19はsequence learningというexplanandum共有だけで同系譜にせず、SORN plasticity と HCRP sequence model のbounded differenceとした。

## 6. fail-closed validation

W3専用 `test_w3_failclosed.py` を追加した。共有CIは変更していない。

別経路でGitHub上の実ファイルを再読して以下を機械検査し **PASS**:

- exact 8 ID/DOI
- profile count 8 / duplicateなし
- PRD-01は新規profileに存在しない
- 全operator IDが paper-local prefix
- 全 `ancestry_exhaustiveness=NOT_ATTESTED`
- 全 global flags false
- mandatory supplementが blockerから消えていない
- SOURCE_BLOCKED 3本がREADYになっていない
- pair 236件が重複なし
- judgment vocabularyが許可4値のみ
- bounded differenceをglobal independenceへ昇格していない
- MAIN authorization=false
- frozen G2 roster/receipt Git blob provenance一致

W3専用GitHub Actions workflowは追加していない。PR #438の既存workflowは accelerator branch/path専用であり、Isolation ruleに従って変更・流用していない。

## 7. Isolation / MAIN NO-GO

変更は `research/paper2/p399/g4/genealogy_w3_mem_prd_skl/` 配下だけ。

**変更していないもの:**

- `genealogy_accelerator_v1/ORIGINAL_NATIVE_PROFILES_v1.json`
- shared pair-matrix generator
- shared CI
- G1 scientific decisions
- G2 MAIN40 roster / backup activation
- preliminary MAIN structure
- Grammar-v0 decomposition/reconstruction
- H0/H1/H2
- Paper 2 final result

したがって、W3完了は8本のsource-native fragmentとbounded genealogy evidenceの完成を意味するだけで、**MAIN scientific authorization は false のまま。MAIN NO-GO。**
