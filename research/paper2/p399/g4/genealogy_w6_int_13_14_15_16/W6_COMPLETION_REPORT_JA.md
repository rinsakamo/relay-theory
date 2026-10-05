# RelayTheory Paper 2 — G4 Genealogy W6 完了報告

**対象:** INT-13 / INT-14 / INT-15 / INT-16 の source-native profile completion  
**Authority:** Issue #399  
**親:** Draft PR #438 exact head `ae044a8f475fb0dc9140a91e360e1ff26a0b5e3a`  
**W6 branch:** `paper2/p399-g4-w6-int13-14-15-16-native-20261005`  
**Draft PR:** #445  
**PR URL:** https://github.com/rinsakamo/relay-theory/pull/445  
**この報告生成直前 head:** `edad79bed07d6388f02f86f549a6a0ccaa69b506`  
**MAIN:** **NO-GO / scientific authorization = false**

## 1. 結論

W6 の4本はすべて **PROFILE_FRAGMENT_READY** とした。これは source-native な中央演算子を統合用 fragment として固定できたという意味であり、モデル系譜の網羅性、全歴史的非導出性、あるいは global family independence を認定するものではない。

- READY = **4**
- SOURCE_BLOCKED = **0**
- SCIENTIFIC_ANCESTRY_UNDERDETERMINED = **0**
- `global_family_independence_certified = true` = **0**
- `ancestry_exhaustiveness` = 全4本 **NOT_ATTESTED**
- MAIN authorization = **false**

## 2. 4本の source-native status

| slot | DOI | 採用 source edition | source-native 中央機構 | W6 status |
|---|---|---|---|---|
| INT-13 | 10.1371/journal.pcbi.1014796 | 著者承認済み PLOS **uncorrected proof** 31pp, SHA256 `5f313f8690f377faaea6b9a3610013c71b880af86634c97dbd4a5344bede9258` | RLWM の並列 RL/WM 更新 → LBA による choice+RT evidence accumulation → set-size 依存 proactive bound | PROFILE_FRAGMENT_READY |
| INT-14 | 10.1371/journal.pcbi.1007594 | PLOS raw PDF, SHA256 `52611f861e4bdf9e568b11332d4890c01506156607f81a50fd87178f82ce0fbb` | connected CRP graph hierarchy → posterior P(H|D) の MCMC → HBFS hierarchical planning | PROFILE_FRAGMENT_READY |
| INT-15 | 10.1371/journal.pcbi.1010047 | PLOS raw PDF, SHA256 `5ec5b75247face8d05574ea60549a8717b707b96f61cc60078d5a76dafbfa597` | MB/MF value computation → between/within-system conflict → conflict-sensitive DDM / boundary caution | PROFILE_FRAGMENT_READY |
| INT-16 | 10.1371/journal.pcbi.1004060 | PLOS raw PDF, SHA256 `c36f0e8fd352dac013741edf8803f5432443ad5c2a85a43c78ffb087450ab105` | response-selection attentional feedback → synaptic trace/tag → global RPE neuromodulated plasticity; SARSA(lambda) 対応 | PROFILE_FRAGMENT_READY |

### INT-13 edition guard

2026-10-05 の PLOS first-party page 再確認でも **“This is an uncorrected proof.”** 表示が残っている。したがって既存の著者判断をそのまま保持し、**corrected final VoR とはラベルしない**。将来 corrected final edition が物理的に確認された場合も、別 edition として凍結・差分比較する必要がある。

PLOS article: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014796

INT-13 の source が明示的にモデル基盤／先行統合として使うもののうち、DOI を安全に source-support できた直接祖先のみ次を記録した。

- 10.1038/s41467-025-61099-0
- 10.3758/s13423-020-01774-z

他3本は、関連先行研究・標準 constituent の引用を **direct model ancestry DOI** に自動昇格させず、空リストのまま fail-closed とした。

## 3. supplements / correction status

- INT-13: PLOS S1 Text `10.1371/journal.pcbi.1014796.s001` を first-party HTML で確認。raw byte SHA は W6 では未取得。
- INT-14: PLOS S1 Appendix `10.1371/journal.pcbi.1007594.s001` を確認。raw byte SHA は未取得。
- INT-15: PLOS S1 Text `10.1371/journal.pcbi.1010047.s001` を確認。raw byte SHA は未取得。
- INT-16: current PLOS article page から paper-specific supporting information object を W6 では同定できなかった。ただし「存在しない」との網羅的な出版社索引証明にはしない。
- INT-14/15/16 について W6 first-party article-page review で correction は同定しなかったが、出版社 correction history 全体の不存在証明には昇格しない。

補足 raw-byte の取得は実行環境側 DNS 解決失敗のため成功数に数えていない。既存主原著 SHA は repository source ledger の exact blob/ref を用いた。

## 4. source-native adverse / scope limits

### INT-13

RLWM と LBA は inherited constituent であり、INT-13 がその初発明者という扱いはしない。clinical sample での fitted mechanism は causal neural implementation の証明ではない。proof edition の制約を保持する。

### INT-14

INT-01 と共有される CRP は constituent に限定する。INT-01 は context-specific task-set/action-policy mapping を cluster し、INT-14 は graph state を connected hierarchy H に cluster する。INT-14 の posterior update は MCMC、planning target は HBFS 系であり、これらを generic “CRP hierarchy” に潰さない。whole historical family は未確定。

### INT-15

between-system conflict と within-system conflict は source 自身が強い相関・識別限界を示す。combined DDM は source 上も full mechanistic cognitive process ではなく statistical approximation とされる。P18 との差は tested native operator の bounded difference に限定する。

### INT-16

AuGMEnT の persistent activity 自体の生物機構は一意に指定されず、recurrent activity は候補の一つに過ぎない。response-selection feedback、tags/traces、global neuromodulator、SARSA(lambda) 対応を区別する。P09 との generic neural plasticity 類似から family identity を推論しない。

## 5. pairwise adjudication

対象は W6 4本 × 既存26 profile = 104組、および W6 内6組、合計 **110組**を全列挙した。

- UNDERDETERMINED = **99**
- BOUNDED_SOURCE_NATIVE_DIFFERENCE = **10**
- SHARED_CONSTITUENT_ONLY = **1**
- DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY = **0**

### 再利用した bounded witness — 5組

| pair | W6 判定 | provenance |
|---|---|---|
| INT-01 × INT-13 | BOUNDED_SOURCE_NATIVE_DIFFERENCE | G2-D v20 + INT-13 proof decision |
| INT-01 × INT-14 | SHARED_CONSTITUENT_ONLY | G2-D v16b; shared CRP only, whole family UNDERDETERMINED |
| INT-01 × INT-15 | BOUNDED_SOURCE_NATIVE_DIFFERENCE | G2-D v20 |
| INT-15 × P18 | BOUNDED_SOURCE_NATIVE_DIFFERENCE | G2-D v15b |
| INT-16 × P09 | BOUNDED_SOURCE_NATIVE_DIFFERENCE | G2-D v15b |

### W6 で新規に追加した bounded pair — 6組

W6 内の全6組を一次 source-native operator の範囲で比較し、すべて **BOUNDED_SOURCE_NATIVE_DIFFERENCE** とした。

- INT-13 × INT-14
- INT-13 × INT-15
- INT-13 × INT-16
- INT-14 × INT-15
- INT-14 × INT-16
- INT-15 × INT-16

これらは中央状態・更新・decision/control operator の source-native 差分を示すだけであり、数理的非導出性や complete genealogy independence の証明ではない。

## 6. exact Git provenance

`W6_GIT_PROVENANCE_RECEIPT_v1.json` に、W6 が再利用する manifest / INT13 proof / v15b / v16b / v16c / v20 / shared 26-profile file と、W6 生成3 JSON の exact `ref:path -> blob` を固定した。

W6 実行中に GitHub contents API で **10/10** を exact ref から再取得し、expected blob と一致することを確認した。

主要 upstream source ref:

`15ee0a2a74b7e47adb439d8b30f499103d1f7eb1`

親 PR #438 exact head:

`ae044a8f475fb0dc9140a91e360e1ff26a0b5e3a`

## 7. fail-closed tests

`test_w6_fail_closed.py` を追加した。検査対象:

1. exact four DOI identities
2. INT-13 proof → corrected final VoR の silent promotion 禁止
3. INT-14 shared CRP → whole-family identity への昇格禁止
4. INT-15 × P18 bounded difference → independence 昇格禁止
5. INT-16 × P09 bounded difference → independence 昇格禁止
6. profile/operator/pair ID duplicate 禁止
7. exact Git ref/blob provenance receipt
8. `global_family_independence_certified: true` 禁止
9. ancestry exhaustiveness promotion 禁止
10. MAIN authorization false
11. 110-pair denominator と 5 reused / 6 new bounded count
12. shared profile / shared pair generator 非変更宣言

W6 の実ファイルを GitHub API から読み直した同等 validator は **PASS**。exact Git provenance は **10/10 PASS**。

### GitHub Actions CI

共有 workflow `.github/workflows/p399-g4-genealogy-1580-failclosed.yml` は accelerator branch への **push** と manual `workflow_dispatch` のみを trigger とし、W6 Draft PR の pull_request を自動実行しない。Isolation rule に従い共有 CI を変更していないため、**W6 固有の自動 GitHub Actions run は作成していない**。これは test failure ではなく trigger scope の制約である。

## 8. unresolved genealogy blockers

- 110組中 **99組**は pair-specific source witness が足りず UNDERDETERMINED。
- W6 の bounded difference 10組と shared constituent 1組はいずれも global family independence ではない。
- 4本すべて `ancestry_exhaustiveness = NOT_ATTESTED`。
- INT-13 corrected final VoR は未確認。ただし author-approved proof のため W6 fragment 作成自体は source-blocked ではない。
- INT-13/14/15 の S1 raw-byte SHA は W6 では未取得。
- correction history の網羅性は認定していない。
- shared 26-profile file への integration は後続 lane の責務。

## 9. isolation / MAIN NO-GO 確認

この W6 branch は以下を変更していない。

- `research/paper2/p399/g4/genealogy_accelerator_v1/ORIGINAL_NATIVE_PROFILES_v1.json`
- shared pair-matrix generator
- shared CI workflow
- G1 scientific decisions
- MAIN40 slot selection
- backup activation
- Grammar-v0 reconstruction
- H0/H1/H2 classification
- preliminary MAIN results
- Paper 2 final conclusions

**MAIN scientific authorization = false. MAIN GO は宣言しない。**
