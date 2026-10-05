# RelayTheory Paper 2 — MAIN M7 統合結果（JA）

## 結論

M7 は **40/40 の最終科学統合を fail-closed で停止**した。理由は M6 の required immutable input に successful final CI を検証できず、GitHub Actions run 0件・commit status 0件だったためである。M6 の科学内容を否定したのではなく、指示どおり **QUARANTINE** とした。したがって M6 が lane 内で報告した 5/5 A0 は M7 の H 判定へ投入していない。

一方、frozen manifest blob `b97b67a34ad9c2858745dfa6aa60444520eaab13` に対する roster identity は **40/40一致**した。component 24、integrated 16、duplicate slot 0、duplicate DOI 0、missing 0、extra 0、roster substitution 0、backup activation 0、G1 PILOT20 混入 0 である。

## 受理できた科学結果

M1–M5 の immutable inputs は ACCEPT。M7 が科学的に import できたのは **35/40** で、component は **24/24**、integrated は INT-01〜INT-11 の **11/16**。

受理35本の final state:

- A0_FIDELITY = **35**
- A1_FIDELITY = **0**
- A2_FIDELITY = **0**
- FAILURE_LOCALIZED = **0**
- UNDERDETERMINED = **0**
- SOURCE_INELIGIBLE = **0**

reconstruction-added stateless adapter = **0**、reconstruction-added persistent/stateful mechanism = **0**。source-defined gate、hierarchy、memory、belief、planner/search、accumulator、workspace/recurrent state、learning stateを追加 coordinator として二重計上していない。

M6 は lane registry 上 INT-12〜INT-16 が 5/5 A0、A1=0、A2=0 だが、CI intake failure のため **lane-reported / M7-unconsumed** としてのみ記録した。「40/40 A0」を M7 certified result としては報告しない。

## Grammar v0

受理35本では frozen semantics を維持した。`P_in/P_out` は `P` の subrole、`rho_O` は `rho/O` の surface alias としてのみ normalization した。accepted scope で custom hidden primitive、lane-specific role redefinition、opaque K/X universal encoding、hidden universal coordinator の検出は 0。

## H0 / H1 / H2

**H0:** accepted 35本すべてが A0。source-scoped には direct composition を支持する強い evidence がある。ただし M6 quarantine のため MAIN40 verdict には昇格しない。

**H1:** accepted scope で A1 case は 0。source-defined interface を reconstruction-added adapter と数えていないため、H1 の positive evidence は 0。

**H2:** accepted scope で A2 case は 0。source-defined state、CTL、belief、memory、planner/search、learned parameter、world/environment state、accumulator、temporal order、routing metadata を H2 に昇格していない。surviving A2 = **0**。

したがって overall adjudication は **INSUFFICIENT_FOR_GLOBAL_H_DISCRIMINATION**。補助的な accepted-35 pattern は「H0-like direct composition, H1/H2 additions observed = 0」だが、final MAIN40 result ではない。

## Component / integrated

accepted component arm は **24/24 A0**。accepted integrated arm は **11/11 A0**。複雑な integrated source model でも INT-01〜INT-11 では source-defined coupling のみで再構成でき、reconstruction-added coordinator は不要だった。ただし INT-12〜INT-16 を含めた 16/16 integrated arm の certification は M6 quarantine が解けるまで行わない。

## Genealogy

W9 の MAIN40 (G2×G2) 780 pair:

- UNDERDETERMINED = **670**
- BOUNDED_SOURCE_NATIVE_DIFFERENCE = **85**
- SHARED_CONSTITUENT_ONLY = **25**
- DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY = **0**
- bounded genealogy clearance = **0**

したがって40本を independent statistical replicates として扱わない。independence-based p-value、naive binomial inference、モデルなしの effective sample size 推定は行わない。genealogy は post hoc に paper を denominator から除外する理由にもしていない。

## 次の blocking action

frozen M6 scientific input に対する **verifiable successful final CI** を得ること。これが満たされれば、M6 の科学状態を好都合に書き換えることなく5本を intake し、M7 40/40 adjudication を再開できる。
