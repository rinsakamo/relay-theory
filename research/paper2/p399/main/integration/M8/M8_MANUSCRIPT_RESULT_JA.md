# RelayTheory Paper 2 — MAIN M8 JGPS manuscript integration

## 目的

M7で確定した exact frozen MAIN40 の科学結果を、既存JGPS稿の旧60-claim failure/recovery研究を上書きせず、別のprospective mechanism-composition validationとして論文化した。

## 固定入力

- M7 exact HEAD: `48b2cf3c627e030e7131af485206b0013d7e02f1`
- M7 Actions: `37297573776` SUCCESS / `M7_FAIL_CLOSED_PASS 40/40`
- MAIN40 manifest blob: `b97b67a34ad9c2858745dfa6aa60444520eaab13`
- original 60-claim source manifest blob: `dd34e2048020124561477ba8fe53f1e4e1452bb7`
- exact DOI overlap: **0**

## 論文へ追加した結果

- A0 = **40/40**
- A1 = **0**
- A2 = **0**
- component = **24/24 A0**
- integrated = **16/16 A0**
- reconstruction-added stateless adapter = **0**
- reconstruction-added persistent/stateful coordinator = **0**

この結果は、source-defined stateful coordinationそのものが存在しないという意味ではない。source-defined hierarchy/gating/memory/planner/accumulator/recurrent state等を保持したうえで、**再構成側が追加coordination layerを発明する必要がなかった**という結果として記述した。

## 推論境界

MAIN40の780 pair genealogyは 670 UNDERDETERMINED / 85 bounded difference / 25 shared constituent / 0 direct/shared whole-model ancestry、bounded clearance=0。したがって40本を独立反復として扱わない。40/40をbinomial significanceや母集団頻度へ変換せず、H1/H2の普遍的不在も主張しない。

M8ではoverallを `INSUFFICIENT_FOR_GLOBAL_H_DISCRIMINATION` のまま保持し、exact MAIN40内の記述的H0-like supportとglobal/universal claimを分離した。
