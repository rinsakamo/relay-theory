# RelayTheory Paper 2 — G4 W8-S 完了報告

## Authority / isolation

- Primary authority: Issue #399
- W7 integration authority: Draft PR #447
- Frozen W7 HEAD: `4325a9a4cba4da651e7cdf2617f7bc8b08c90f54`
- W8-S branch: `paper2/p399-g4-w8s-source-blockers-20261005`
- W8-S Draft PR: #448
- 対象は W7 の SOURCE_BLOCKED 5件だけ。CNC-01 / MEM-01 / INT-03 / INT-06 は未変更。
- W7共有profile registry、pair-matrix科学判定、G1 genealogy、Grammar-v0、H0/H1/H2、MAIN science は直接変更していない。

## Raw supplement freeze

PLOS Computational Biology の公式 supplementary endpoint から指定9ファイルを取得し、raw PDF bytesを無加工で凍結した。全9件で MIME=application/pdf、raw SHA256、byte length、公式URL、PLOS production object-storage redirect provenanceを記録した。抽出テキストは監査補助であり authority ではない。

| paper | supplement | bytes | SHA256 |
|---|---|---:|---|
| BLF-02 | 10.1371/journal.pcbi.1006972.s005 | 76300 | `c1c11e2389ced2b40e5b5d007bf53701ee3a4dbe6e7338e3757d23845be52817` |
| MEM-03 | 10.1371/journal.pcbi.1004003.s001 | 1107546 | `3580b43915404b6784254ecf939c84054fd12209188eee107cb9715de85b9084` |
| SKL-01 | 10.1371/journal.pcbi.1012455.s001 | 588305 | `59a381fed8520bab23eaa937d36d900eef2cbd399dcb4e90c1f7f3a5667e7832` |
| SKL-03 | 10.1371/journal.pcbi.1006839.s002 | 53752 | `3ebf4a20b8e37b452ac17e6f2ea107c3a6ba5538211ee4e25cc5451e4bada5ec` |
| SKL-03 | 10.1371/journal.pcbi.1006839.s003 | 38005 | `22b1632310abc012a52d32e892319fb86e8af775e09a1b283cdf91ebc28e8e0c` |
| INT-07 | 10.1371/journal.pcbi.1003383.s001 | 95482 | `aa7f5c64223053b98c6ccbb1465110799fc2c9a9ee8fdd2b2c25a6ba530d45cc` |
| INT-07 | 10.1371/journal.pcbi.1003383.s002 | 98773 | `c758ed0ca81813359dd6a6d146069c8dec8ce1d251a8a945e53132e69af354c1` |
| INT-07 | 10.1371/journal.pcbi.1003383.s003 | 111336 | `fcaf2f446427d6ef7defd5f836f76aa0bbd4b04f8e165f57da431cbd07f44763` |
| INT-07 | 10.1371/journal.pcbi.1003383.s004 | 89366 | `55efe954cfb74e5ce905b476e2ec421ef942a93887af0bfdc7ad91d4ee810d90` |

取得/必須 = **9/9**。SHA256 freeze = **9/9**。

## Five-paper resolution

| Paper | W8-S state | 科学的効果 |
|---|---|---|
| BLF-02 | PROFILE_FRAGMENT_READY | S1でflat leaky-beta comparatorとdelta-ruleの関係を閉じた。zero-prior・large-nでの漸近同値に限定し、priorが残る一般形では同一視しない。 |
| MEM-03 | PROFILE_FRAGMENT_READY | Fisher information / memory fidelity導出とhierarchical-code分析を確認。storage/update/readoutのcore operatorは変更せず、近似条件とscaling依存性を明示。 |
| SKL-01 | PROFILE_FRAGMENT_READY | HML式と収束解析を確認。指数収束は無条件ではなく、探索ノイズなし、PE、十分なtimescale separation、Ωc内初期化等に限定。探索ノイズありではO(|σu|)近傍への有界化。 |
| SKL-03 | PROFILE_FRAGMENT_READY | S2→初期variance estimates、S3→3パラメータbootstrap fitの鎖を閉じた。S2/S3を数学的model definitionには昇格させない。 |
| INT-07 | PROFILE_FRAGMENT_READY | S1–S4で非線形flow近似、filter/backward recursion、augmented input inference、precision weightingを閉じた。gammaとoffline alpha-betaを分離し、latent input inferenceをpolicyに昇格させない。 |

READY = **5/5**、SOURCE_BLOCKED = **0/5**、SOURCE_CONFLICT = **0/5**。
したがってW7の51/60から、W8-S提案fragmentを取り込めば profile denominator は **56/60** になり得る。

## Downstream handoff

BLF-02↔BLF-03 は W7 で missing S1 が pair-undertermination の一因だったため、source-gap premiseを外した状態で W8-A/W9 に再審査flagを渡す。ただしW8-Sはpair decisionを変更していない。5件すべて ancestry_exhaustiveness は NOT_ATTESTED のままで、source closureからgenealogy independenceを推論していない。

## Safety / authorization

- global family independence certified: **false**
- global independent count: **0のまま（W8-Sでは再計算・変更しない）**
- MAIN authorization: **false**
- selected MAIN40 roster: unchanged
- backups: not activated

## Tests / CI

W8-S専用 `test_w8s_fail_closed.py` と read-only CI `.github/workflows/w8s_source_blockers_ci.yml` を追加した。

検証内容:

- exact five target DOIs only
- exact required supplement identifiers
- READYにはraw SHA256と実raw fileが必須
- SHA256をraw bytesから再計算してreceiptと照合
- mandatory supplement欠落を模擬するとREADY validationが失敗すること
- SKL-03 S2/S3の2/2必須
- INT-07 Text S1-S4の4/4必須
- PLOS公式endpoint以外へのsource substitutionなし
- `global_family_independence_certified=true` が成果物内に存在しないこと
- MAIN authorization=false
- W7 shared registry / pair science / G1 / Grammar-v0 / H0-H2 / MAIN scienceが未変更であること

検証run `37267450061` は head `0b9587a876257f1cbb381fb0ba746fc7646a5a50` に対して SUCCESS。以後のcompletion-report-only更新後も同一test suiteを再実行する。
