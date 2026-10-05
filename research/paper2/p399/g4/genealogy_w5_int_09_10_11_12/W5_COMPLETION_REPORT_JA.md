# RelayTheory Paper 2 — G4 Genealogy W5 完了報告

- Authority: Issue #399
- Parent accelerator: Draft PR #438
- Exact parent HEAD: `ae044a8f475fb0dc9140a91e360e1ff26a0b5e3a`
- W5 branch: `paper2/p399-g4-w5-int09-10-11-12-native-20261005`
- Draft PR: #446
- Scope: INT-09 / INT-10 / INT-11 / INT-12 の4件のみ
- MAIN scientific authorization: **false / NO-GO**
- Global family independence certified: **0**
- Ancestry exhaustiveness: **NOT_ATTESTED**

## 1. 四論文の状態

| Slot | DOI | 状態 | 中心 source-native 機構 | 版・訂正の扱い |
|---|---|---|---|---|
| INT-09 | 10.1371/journal.pcbi.1005190 | PROFILE_FRAGMENT_READY | state-dependent sensory reliability を含む stochastic optimal control。controller/estimator を交互最適化し、affine observation noise により feedback + feedforward control を生む。 | 2016原著 + DOI 10.1371/journal.pcbi.1005370 の2017 Fig9 legend訂正を必須bundle化。訂正前captionを履歴として保持。 |
| INT-10 | 10.1371/journal.pcbi.1011024 | PROFILE_FRAGMENT_READY | BG の novelty-modulated three-factor Hebbian goal→action learning と、cerebellar reservoir の endpoint-error motor-program correction の協調。 | 現行PLOS原著を採用。DOI 10.1371/journal.pcbi.1011243 は Funding statement のみの訂正として別記録。旧proofと現行版を同一視しない。 |
| INT-11 | 10.1371/journal.pcbi.1014093 | PROFILE_FRAGMENT_READY | successor-feature による feature inference、outcome/reward map による outcome inference、両者の joint Bayesian contextual inference。 | 現行2026 PLOS原著。FI/OI の inherited model を直接祖先として限定記録。 |
| INT-12 | 10.1371/journal.pcbi.1006116 | PROFILE_FRAGMENT_READY | reward と mapping/transition を別々の CRP cluster に分解し planning で再結合する independent clustering。joint clustering と meta-agent を明示的 comparator/extension として分離。 | 2018 PLOS原著。S1 unknown-transition variant は raw byte未凍結のため canonical 化しない。 |

集計: **READY 4 / SOURCE_BLOCKED 0 / SCIENTIFIC_ANCESTRY_UNDERDETERMINED 0**。

## 2. Source provenance

W5 source freeze:

- `W5_SOURCE_EVIDENCE_FREEZE_v1.json`
- Git blob: `4e453eb63c662f167735ed929aa14d3cff88ddf6`
- source-bearing commit: `4abf6c229ff893fb51b56b7127a8d26f184d787d`

Profile fragments:

- `W5_SOURCE_NATIVE_PROFILE_FRAGMENTS_v1.json`
- Git blob before completion-report commit: `10ccbb525bdb364ab5344c58e7ade51aeacd8505`

Bounded pair ledger:

- `W5_BOUNDED_PAIR_ADJUDICATIONS_v1.json`
- Git blob before completion-report commit: `8ce90f79de39bf584f8e0ea1d7cf79f994a0ba86`

Source gaps/blockers:

- `W5_SOURCE_GAPS_AND_BLOCKERS_v1.json`
- Git blob before completion-report commit: `48aa74b1fad17931bf26d95f18ec19509a9853f8`

Frozen MAIN40 roster:

- `research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json`
- Git blob: `b97b67a34ad9c2858745dfa6aa60444520eaab13`
- 4 DOI は frozen roster と完全一致。

共有 accelerator profile manifest:

- `research/paper2/p399/g4/genealogy_accelerator_v1/ORIGINAL_NATIVE_PROFILES_v1.json`
- Git blob: `903f8db6e1569ed27507cf47e668f7599a08cd98`
- **W5では未変更**。

共有 pair generator:

- `research/paper2/p399/g4/genealogy_accelerator_v1/build_pair_matrix.py`
- Git blob: `4d9443d43ac911fbc3731c6f110c51abb8a0ed1c`
- **W5では未変更**。

## 3. 直接祖先の限定記録

direct ancestry は、原著が明示的に既存モデルを採用・基礎化しており、DOIを安全に同定できた場合だけ記録した。

- INT-09: `10.1162/0899766053491887` — Todorov stochastic optimal control/estimation algorithm。
- INT-10: `10.1111/ejn.14730`, `10.1523/JNEUROSCI.0874-18.2018`, `10.1111/ejn.12434` — BG component の明示的 previous/simplified-model ancestry。full BG+cerebellum model 全体の同一性ではない。
- INT-11: `10.1037/rev0000414`, `10.48550/arXiv.1906.07663` — feature-inference / outcome-inference constituent の明示的 existing-model ancestry。
- INT-12: `10.1037/a0030852`, `10.1016/j.cognition.2016.04.002` — joint clustering comparator の明示的 predecessor。independent compositional decomposition 自体の同一性を意味しない。

全 profile で `ancestry_exhaustiveness = "NOT_ATTESTED"` を維持した。

## 4. Pairwise bounded adjudication

必要比較を全列挙した。

- W5 internal: 6
- W5 × existing profiled G1/G2: 104
- 合計: **110**
- 既存 bounded witness 再利用: **1**（INT-09 × INT-01、G2-D v20）
- W5新規 bounded adjudication: **109**
- `BOUNDED_SOURCE_NATIVE_DIFFERENCE`: **104**
- `SHARED_CONSTITUENT_ONLY`: **6**
- `DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY`: **0**（今回の comparison-target 間）
- `UNDERDETERMINED`: **0**（今回要求された限定 pair set 内）

`SHARED_CONSTITUENT_ONLY` は次の6組に限定した。

1. INT-11 × INT-12 — CRP-family latent context/task clustering
2. INT-11 × INT-01 — CRP-family Bayesian latent-structure inference
3. INT-11 × P19 — CRP-family nonparametric clustering
4. INT-11 × PRD-01 — successor-style predictive representation
5. INT-12 × INT-01 — CRP-family task-structure reuse/creation
6. INT-12 × P19 — CRP-family nonparametric clustering

これらは constituent の共有であり、中心モデルの同一性・直接系譜・global family independence を意味しない。

特に INT-12 × P11 / P12 は control/gating/metareasoning という語彙の重なりだけでは系譜を成立させず、source-native operator の限定差として扱った。PBWM gating、LVOC/EVC と、INT-12 の separate CRP clustering + component-binding planning は同一演算子とはしていない。

## 5. Correction / supplement handling

### INT-09

publisher correction DOI `10.1371/journal.pcbi.1005370` を profile から消せない fail-closed 条件にした。訂正は Fig9 caption の panel relation のみを置換し、元の2016出版物そのものは履歴として残す。central model change は **false**。

### INT-10

publisher correction DOI `10.1371/journal.pcbi.1011243` は Funding statement の欠落修正のみ。科学モデルの訂正には昇格しない。旧proof・現行article・correction notice を分離した。

### INT-11

publisher main article 内で FI/OI の inherited models が明示されている。W5 review 時点で model-relevant correction は同定していないが、「訂正が存在しないことの完全証明」までは主張しない。

### INT-12

S1 Text の unknown-transition implementation と S2 Text は補足variantとして保持するが raw SHA はW5で独立凍結していない。したがって unknown-transition variant は canonical model に昇格不可。

## 6. 残る source / genealogy limitations

**profile completion を阻害する blocker は0件**。ただし fail-closed の非blocking gap は残す。

- INT-09 S1 Text raw bytes/SHA はW5独立凍結なし。
- INT-12 S1/S2 Text raw bytes/SHA はW5独立凍結なし。
- INT-10旧proofと現行原著のraw byte同一性は主張しない。
- INT-11について publisher correction registry の不存在を exhaustive には証明しない。
- 全4件とも ancestry exhaustiveness は NOT_ATTESTED。
- bounded pair difference は global family independence ではない。

## 7. Fail-closed tests / audit

W5専用:

- `test_w5_fail_closed.py`
- exact 4 DOI identities
- INT-01/04/08 new-profile禁止
- duplicate禁止
- exact Git blob/ref provenance
- INT-09 correction disappearance禁止
- global independence true禁止
- ancestry exhaustiveness promotion禁止
- bounded difference→independence promotion禁止
- unverified variant canonicalization禁止
- MAIN authorization false
- parent HEAD からの変更が W5専用directory外へ出ないこと

実行環境の container は `github.com` をDNS解決できず clone ベースの unittest 実行はできなかった。そのため同一 invariant を GitHub connector 上の**実ブランチ実ファイル・実blob・base comparison**に直接適用し、**PASS**を確認した。

検証時の隔離差分は5ファイルで、すべて
`research/paper2/p399/g4/genealogy_w5_int_09_10_11_12/`
配下のみ。completion report 自身を追加した後も同じprefix制約を再監査する。

共有 PR #438 の workflow/CI は変更していない。W5で shared CI を偽装して再利用せず、PR #438 の既存 successful baseline と W5限定監査を分離する。

## 8. MAIN gate

**MAIN NO-GO を明示維持する。**

- Grammar-v0 reconstruction: 未実行
- H0/H1/H2: 未分類
- preliminary MAIN result: 未閲覧
- MAIN final conclusion: 未推論
- backup activation: 0
- selected MAIN40 replacement: 0
- global family independence certified: 0
- MAIN scientific authorization: **false**

W5 は integration lane が検証済み fragment を後から取り込むための独立成果であり、共有26-profile manifest を直接変更していない。
