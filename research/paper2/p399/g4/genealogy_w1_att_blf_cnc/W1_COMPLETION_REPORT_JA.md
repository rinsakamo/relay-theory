# RelayTheory Paper 2 — G4 Genealogy W1 完了報告

日付: 2026-10-05 JST  
Primary authority: Issue #399  
開始点: Draft PR #438 exact HEAD `ae044a8f475fb0dc9140a91e360e1ff26a0b5e3a`  
独立 branch: `paper2/p399-g4-w1-att-blf-cnc-native-20261005`

## 1. 隔離条件

W1 は PR #438 の exact HEAD から独立分岐した。共有
`research/paper2/p399/g4/genealogy_accelerator_v1/ORIGINAL_NATIVE_PROFILES_v1.json`
および共有 pair-matrix generator / shared CI は変更していない。W1 の成果物は
`research/paper2/p399/g4/genealogy_w1_att_blf_cnc/`
配下だけに置いた。

MAIN の分解・Grammar-v0 再構築・H0/H1/H2・Paper 2 結果推定は実施していない。
G1 科学判定、backup、MAIN40 選定も変更していない。
`global_family_independence_certified` は全 profile で false、
`ancestry_exhaustiveness` は全 profile で `NOT_ATTESTED` のまま。
MAIN scientific authorization は false のままである。

## 2. 7論文の資格状態

| slot | DOI | 状態 | 採用版・主要証拠 | 限定科学所見 / 残件 |
|---|---|---|---|---|
| ATT-01 | 10.1007/s42113-024-00197-6 | PROFILE_FRAGMENT_READY | Springer VoR complete HTML 2024-02-29。既存 ATT handoff と W1 publisher inspection | saliency/task/history → priority map → ex-Gaussian RT。raw publisher SHA は未取得。全 ancestry は未証明。 |
| ATT-02 | 10.1371/journal.pcbi.1004770 | PROFILE_FRAGMENT_READY | PLOS VoR PDF/HTML、SHA256 `3a1e6986…6232` | 二層 visual feedback + local divisive normalization。ATT-03 を normalization model として直接比較。 |
| BLF-02 | 10.1371/journal.pcbi.1006972 | **SOURCE_BLOCKED** | PLOS main VoR、SHA256 `1f7da5bb…d3ba` | coupled change-point hierarchy / confidence reset は main source で固定。必須 S1 File `10.1371/journal.pcbi.1006972.s005` の raw bytes/SHA が未凍結。 |
| BLF-03 | 10.7554/eLife.08825 | PROFILE_FRAGMENT_READY | eLife **Version of Record 2015-09-28**、publisher v2 SHA256 `d7cc51a4…d2dca` | hazard-conditioned LLR update、adaptive leak / stabilizing bound。Accepted Manuscript 2015-08-31 と明示的に分離。 |
| CNC-01 | 10.1038/s41562-023-01719-1 | **SCIENTIFIC_ANCESTRY_UNDERDETERMINED** | Nature Human Behaviour VoR HTML 2023-10-16 | dynamic concept library + adaptor grammar + Pitman-Yor/Gibbs cache/reuse。Liang et al. 2010 を明示的に adapt するが、source bibliography に DOI がなく DOI 祖先として捏造しない。 |
| CNC-02 | 10.1371/journal.pcbi.1011954 | PROFILE_FRAGMENT_READY | PLOS VoR PDF/HTML、SHA256 `a1f6a705…d1f0` | RNN/LR/MLP、f/r/ff-RNN、5 constraint regimes。複数の異なる TI 解が残る。 |
| CNC-03 | 10.7554/eLife.77185 | PROFILE_FRAGMENT_READY | eLife VoR 2023-12-11、publisher v1 SHA256 `b9a14a8b…f5ff` | C-HORSE TSP/MSP。Schapiro et al. 2017b DOI `10.1098/rstb.2016.0049` を直接祖先として固定。Ketz 2013 系譜も明示。 |

集計: **PROFILE_FRAGMENT_READY 5 / SOURCE_BLOCKED 1 / SCIENTIFIC_ANCESTRY_UNDERDETERMINED 1**。

## 3. source-native profile と版凍結

機械可読 profile は `W1_SOURCE_NATIVE_PROFILE_FRAGMENTS_v1.json` に exactly seven entries として凍結した。
各 operator は `<slot>:<operator-name>` の paper-local ID とし、同じ語彙だけで論文間の operator identity を作っていない。

既存 repository-first evidence:
- frozen G2 manifest: `research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json`, blob `b97b67a34ad9c2858745dfa6aa60444520eaab13`
- G2 source receipts: `research/paper2/p399/g2/MAIN40_G2_ACTUAL_SOURCE_RECEIPTS_AND_DECISIONS_v2.json`, blob `ac3ffa59fcdc078550df587bc972632b7ca5ff7f`
- ATT bounded handoff: `research/paper2/p399/g2/att_a/ATT_A_BOUNDED_SOURCE_GENEALOGY_HANDOFF_v1.json`, blob `dbafe32417fa12a783a12cdc71aa6ecb2dedf7bd`
- ATT integrator handoff: `research/paper2/p399/g2/att_a/ATT_A_G2_INTEGRATOR_FINAL_BOUNDED_HANDOFF_v2.json`, blob `81f23a6634493233ac6f39518ab2ab7b572b0c86`
- BLF bounded audit: `research/paper2/p399/g2/blf/BLF_BOUNDED_ORIGINAL_AND_FAMILY_DECISION_v1.json`, blob `5f9d8dba3516b4757a207e8f0eb5d423f9f93858`

不足分について出版社原著を再照合した結果は
`W1_EXTERNAL_SOURCE_INSPECTION_LEDGER_v1.json`
に固定した。これは MAIN science の結果ではなく、source-native genealogy 用の限定証拠台帳である。

## 4. positive-priority pair 監査

PR #438 baseline の sparse collision/risk registry から W1 に関係する事前登録 high-priority risk は7本だった。
W1 はその7本だけを source-supported に判定し、通常の W2–W6 未profile論文へ比較を拡張していない。

| pair | W1判定 | 要点 |
|---|---|---|
| ATT-01 × ATT-02 | BOUNDED_SOURCE_NATIVE_CENTRAL_OPERATION_DIFFERENCE | priority/history RT model と visual feedback-normalization network の中心演算差。 |
| ATT-02 × ATT-03 | SHARED_CONSTITUENT_TECHNIQUE_ONLY | ATT-02 は ATT-03 を直接引用し divisive normalization を共有するが、feedback architecture は別。 |
| BLF-02 × BLF-03 | UNDERDETERMINED | BLF-02 は BLF-03 を直接引用。中心演算差はあるが BLF-02 S1 source gap のため genealogy close しない。 |
| BLF-02 × P08 | BOUNDED_SOURCE_NATIVE_CENTRAL_OPERATION_DIFFERENCE | coupled transition statistics/change-point confidence と reversal-HMM current-state filtering の差。 |
| BLF-03 × P08 | UNDERDETERMINED | switching-state Bayesian filtering/HMM 系の共有 ancestry signal があり、唯一の直接祖先は未凍結。 |
| CNC-02 × CNC-03 | BOUNDED_SOURCE_NATIVE_CENTRAL_OPERATION_DIFFERENCE | generic task-trained TI networks と inherited anatomical C-HORSE の差。 |
| CNC-03 × P15 | SHARED_MODEL_LINEAGE_ANCESTOR_SUPPORTED | 両 evidence chain が Ketz et al. 2013 DOI `10.1371/journal.pcbi.1003067` を lineage ancestor として支持。 |

追加した bounded pair judgments: **7**。
いずれも `global_independence_promoted=false`。bounded difference を global genealogy independence として数えていない。

## 5. 未解決 blocker

1. **BLF-02 S1 File**: DOI `10.1371/journal.pcbi.1006972.s005`。main article が flat/delta-rule・heuristic control の詳細に参照するため W1 では required bundle とした。出版社リンクは確認できたが raw PDF 配信先をこの lane から取得できず、PR #438 baseline にも SHA256 がない。よって BLF-02 は SOURCE_BLOCKED。
2. **CNC-01 direct adapted ancestor identity**: Liang, Jordan & Klein 2010 ICML を原著が明示的に adapt するが、原著 bibliography に DOI がない。DOI形式の direct ancestor を作らず SCIENTIFIC_ANCESTRY_UNDERDETERMINED。
3. **BLF-03 × P08**: switching-state Bayesian filtering ancestry の全量比較未了。
4. **CNC-03 × P15**: Ketz 2013 共有 lineage ancestor が確認されたため、global independence は認定不能。これは source blocker ではなく正の genealogy signal。
5. ATT-01 / CNC-01 の publisher raw-byte SHA は未取得。ただし exact official VoR HTML の source-native semantic profile は限定的に形成可能として、欠落を adverse limit に保持した。

## 6. fail-closed tests

W1 専用:
- `verify_w1_failclosed.py`
- `test_w1_failclosed.py`
- `W1_FAILCLOSED_TEST_RECEIPT_v1.json`

検証条件:
exact seven DOI identities、duplicate rejection、SHA/ref format、global independence false、ancestry promotion rejection、required correction/supplement preservation、missing evidence fail-closed、pair global promotion rejection。

直接 local clone/test は実行 container の DNS が `github.com` を解決できず実行不能だった。
その失敗を PASS とせず、GitHub connector で実 branch の JSON blob を再取得して同一 gate を独立リプレイした。
**current bundle PASS + 9 negative mutations all correctly rejected = 10/10 PASS**。
最初の JS replay で unavailable primitive を使った試行は破棄し、訂正版の結果だけを正式 receipt に記録している。

## 7. 結論

W1 は7論文すべてを completion criterion のいずれかへ分類したため、lane 自体は **COMPLETE_WITH_EXPLICIT_BLOCKERS**。
5件 READY、1件 SOURCE_BLOCKED、1件 SCIENTIFIC_ANCESTRY_UNDERDETERMINED。

共有 PR #438 の profile file / generator / CI は変更していない。
MAIN science、MAIN authorization、G1 decisions、backup、MAIN40 selection は変更していない。
**MAIN remains unauthorized.**
