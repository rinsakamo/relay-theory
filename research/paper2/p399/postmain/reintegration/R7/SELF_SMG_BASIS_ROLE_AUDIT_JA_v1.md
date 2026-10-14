# RelayTheory Paper2 — post-MAIN R7：RelaySelf S/M/G 基底・役割監査

**判定（2026-10-15）**：`NO_NEW_TOP_LEVEL_ROLE_WITNESS_IN_PINNED_SMG_SCOPE_WITH_UNQUALIFIED_CROSS_LANE_BRIDGES`

これは **新しい基底が不要だと証明した結果ではない**。指定したGitHub上の実装ファイルとDraftの範囲で、Paper2の既存役割に配置できない具体的な機構を確認できなかった、という限定的な工学・理論対応監査である。実行・コード変更・科学実験は行っていない。S/M/Gはそれぞれ別Draftであり、統合された一つのSelfでの資格を与えるものでもない。

## 凍結Authorityと検査対象

- 先行するRelayTheory [R6 / PR #477](https://github.com/rinsakamo/relay-theory/pull/477) のHEAD `9a134b25380c4302830c8d567e5ff52870a7b9ef` 上に**別レイヤーとして追加**。R6ファイルを変更しない。
- Paper2の作業基底 `B_P2 = {S, Pi, K, O, T, C, Q, P}` は凍結のまま。post-MAIN Grammar v0 の `{Pi, X, C, Q, P_in, P_out, K, T, rho/O}` は役割の再解釈であり、両者を一対一のPython classや追加実験結果として扱わない。
- MAIN40はcomponent 24/24、integrated 16/16、A0=40、A1=0、A2=0。今回、MAINの元論文・ClaimIR・残差・`ROLE_GAP`の再判定を**していない**。
- Source: RelaySelf [S #545](https://github.com/rinsakamo/relay-self/pull/545) `291417539497f42269af9a15512cea320f375310`、[M0 #617](https://github.com/rinsakamo/relay-self/pull/617) `4bdc9daf0444e55908cff321111bae9a2927942c`、[M2 #621](https://github.com/rinsakamo/relay-self/pull/621) `1e52eccf430fd16f4230e3387e3d2ff31891820d`、[G4/G3 #623](https://github.com/rinsakamo/relay-self/pull/623) `2a3e85826d1aeb9241006578da0dcf5932107bd3`、[V #625](https://github.com/rinsakamo/relay-self/pull/625) `5131bee88cbed6d116d265398f43fd4e7b69c21e`（VはPR記述に基づく補助的設計照合のみ）。
- 参照した具体ファイル・検査単位・限界は隣接JSONに固定。上記はそれぞれの**当時のHEAD**であり、後続pushを自動監査しない。

## 監査表

| 対象 | 理論側への対応 | 判定・上限 |
|---|---|---|
| S B0 実観測→L0→Action→E | 観測 `O/P_in`、選択 `K/Q`、型・入場 `Pi/C`、時系列 `T`、結果 `P_out/O` | 限定整合。真正EAT以外の入金を拒絶。動機学習は未証明 |
| S DEV入口 | System/Worldポート `P`、所有権 `S/C`、セッション順序 `T` | 限定整合。DEV_ONLYは資格・科学試験と違う |
| M0 身体・内受容 | `X/K/T/C` と、内部真値から観測への `rho/O` | 限定整合。物理エネルギー自体を価値 `Q` と同一視しない |
| M2 遺伝・繁殖模擬 | `Pi` 個体、`X` 特性、`K/T` 世代遷移、明示された `Q` 比較 | 合成で説明可能。遺伝RewardGenesは単なるスロット、手設計cueを価値創発と呼ばない |
| G4 初期変種生成 | 実験器側 `Pi/K/T/C/Q`。candidateのIDはWorld内個体性ではない | 合成で説明可能。多様性評価は個体内価値・適応度ではない |
| G3 資金付き出生照合 | `Pi/C/T/O/P` によるイベント同一性、ledger照合、入場 | 手続き整合。M/R原証拠認証は欠ける |
| V OFF介入 | route/retained-accessの操作 `K/C`、結果観測と比較 `O/Q` | 設計のみ。OFFによる能力・基底の因果的寄与は未測定 |

## 「基底の欠落」と「実行資格の欠落」を混同しない

1. **時間基準**：Sの決定epoch、MinecraftのWorld tick、M0の代謝tickを機械的に等置できない。これはまず `T` の*測定・接続契約*の問題。独立観測がない限り「実時間に応じたエネルギー消費」を宣言しない。
2. **真正な出生**：M2の `BirthRecord` とG3のsource/readback/計画識別の間に、正当な原証拠付き結合が未成立。G3 SHAは整合性検査であり第三者の真正性署名ではない。`Pi/C/O/P` の跨Owner結合の不足であって、現時点で新基底の積極的証拠ではない。
3. **権限の分散**：SのAction権限、Mのエネルギー所有、Gの系譜所有、Vの科学判定は別。現ファイルで新たな普遍的SelfStateは必要とされていないが、全統合call graphの不在証明ではない。
4. **環境と評価**：Mの身体存続条件やGの生成候補スコアを、そのまま本人が持つ認知的価値 `Q` と解釈しない。World/body truth と Sensor、Self policy、evaluator criteria を区別する。
5. **科学的上限**：Rの独立Source資格、Vの事前登録されたOFF/sham/cheap対照、真正なWorld outcomeがなければ、学習・進化・能力同一性の主張は出せない。

## 次のゲート

S/M/Gを実際にS productに組み込んだ**新しいexact HEAD**に対し、state ownership/Mutation authority/implicit side effects/clock joins/原証拠を再監査する。その際、全観測を既存役割へ無理に割り当てず、どの操作が表現不能かという**具体的な失敗witness**が現れた場合だけ、新しい役割候補として別途審査する。`ROLE_GAP=0` をこの工学監査の数値として再利用しない。

**最終評価**：`COMPATIBLE_IN_AUDITED_SCOPE / INTEGRATED_RUNTIME_UNQUALIFIED / PHYSICAL-SCIENTIFIC_NO_GO`

この結果はPaper2元データへの帰属ではなく、RelaySelf構築からの新しい限定的な**implementation feedback**である。
