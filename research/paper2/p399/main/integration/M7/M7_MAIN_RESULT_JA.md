# RelayTheory Paper 2 — MAIN M7 統合結果（JA）

## 結論

M7 は exact frozen G2 MAIN40 を **40/40 で科学統合まで完了**した。先行版で quarantine していた M6 は、科学成果物を変更せず CI infrastructure だけを追加した successor HEAD `baa033088191286962332d84fc04349d3d1604dd` で再検証され、PR-trigger run `37296888771` / job `m6-fail-closed` が SUCCESS、ログ終端は `M6_FAIL_CLOSED_PASS 34/34` となった。旧 M6 HEAD `a444cd326bd75c6b1990ad6b03289597896e5d7b` からの差分は `test_m6_fail_closed.py` と M6 workflow の2ファイルだけで、科学ファイルの変更は 0。

frozen manifest blob `b97b67a34ad9c2858745dfa6aa60444520eaab13` に対する roster identity は **40/40一致**。component 24、integrated 16、duplicate slot 0、duplicate DOI 0、missing 0、extra 0、roster substitution 0、backup activation 0、G1 PILOT20 混入 0 を維持した。

## MAIN40 scientific result

M1–M6 の immutable inputs はすべて ACCEPT。M7 final state は次のとおり。

- A0_FIDELITY = **40**
- A1_FIDELITY = **0**
- A2_FIDELITY = **0**
- FAILURE_LOCALIZED = **0**
- UNDERDETERMINED = **0**
- SOURCE_INELIGIBLE = **0**

reconstruction-added stateless adapter = **0**、reconstruction-added persistent/stateful mechanism = **0**。source-defined gate、hierarchy、belief、memory、planner/search、accumulator、workspace/recurrent state、learning state、feedback、neuromodulatory gating は reconstruction-added coordinator として二重計上していない。

component arm は **24/24 A0**、integrated arm は **16/16 A0**。したがって、凍結された MAIN40 内では integrated complexity の増加に伴って追加 adapter や persistent coordinator が必要になるという観察結果は得られなかった。

## Grammar v0

40本すべてで frozen semantics を維持した。lane surface の `P_in/P_out` は `P` の subrole、`rho_O` は `rho/O` の surface alias としてのみ normalization した。custom hidden primitive、lane-specific role redefinition、opaque K/X universal encoding、hidden universal coordinator、System/World conflation の検出は 0。

## H0 / H1 / H2

**H0:** exact MAIN40 の 40/40 が A0。したがって、この凍結コーパスの source scopes 内では direct composition に対する強い記述的支持がある。

**H1:** A1 case は 0。source-defined interface を reconstruction-added stateless adapter と数えていないため、H1 の positive evidence は 0。

**H2:** A2 case は 0。source-defined persistent state、CTL、belief、memory、planner/search、learned parameter、world/environment state、accumulator、temporal order、routing metadata を H2 に昇格していない。surviving A2 = **0**。

ただし overall は **INSUFFICIENT_FOR_GLOBAL_H_DISCRIMINATION** のままとする。これは MAIN40 の結果が曖昧だからではなく、非ランダムな凍結コーパスであり、系譜独立性も認証されていないため、40/40 をそのまま普遍的・母集団的主張へ昇格できないからである。

## Genealogy

W9 の MAIN40 (G2×G2) 780 pair:

- UNDERDETERMINED = **670**
- BOUNDED_SOURCE_NATIVE_DIFFERENCE = **85**
- SHARED_CONSTITUENT_ONLY = **25**
- DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY = **0**
- bounded genealogy clearance = **0**

したがって40本を independent statistical replicates として扱わない。independence-based p-value、naive binomial inference、モデルなしの effective sample size 推定は行わない。genealogy は post hoc に paper を denominator から除外する理由にもしていない。

## M7 final scientific statement

> Exact frozen MAIN40 では、40/40 の source-defined cognitive architectures が frozen Grammar v0 と各 source 自身の mechanisms による A0 direct composition として再構成され、reconstruction-added stateless adapter または additional persistent/stateful coordinator を必要とした事例は観察されなかった。

この statement は **MAIN40 に限定**される。global genealogical independence、universal cognitive architecture、universal brain architecture、RelaySelf engineering efficacy は主張しない。
