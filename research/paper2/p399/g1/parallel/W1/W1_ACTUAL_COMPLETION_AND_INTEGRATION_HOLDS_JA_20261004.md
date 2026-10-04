# W1 独立科学作業の実結果 — 2026-10-04

**Authority:** Issue #399 / G1 Draft #418 / G4 Draft #420。着手点は凍結 charter の exact commit `38c5eb24c61b9e57371084a65fcbcb9fb9c62a4b`。W1 専用ブランチ `paper2/p399-g1-w1-source-adversarial-20261004` のみに科学ファイルを追加。W2/W3/W4、G2/G3/G4、Grammar v0、PF、従来 #398、共有 G1 v1–v6 台帳は無変更。

## 実行結論と統合分母

- **P06:** 2015 PLOS 39pp 出版原著 SHA `50a8e9fb...`。PRE_A→A→B→C→D→E を個別コミットで凍結。E 後の真の公式原著再取得と 6段階 exact Git introduction / 祖先順序は独立 CI **SUCCESS** [37192336977](https://github.com/rinsakamo/relay-theory/actions/runs/37192336977)。**限定個別資格を別記録**（元 V1 最大応答によるサリエンスと実験条件付き行動 RT race 式(30)のみ）。原著 Fig7 は6名の不棄却であって「完全な生成認知モデル」同定ではない。Fig10の spurious RE8 不棄却、CM/CMO 細胞仮定、緑条件 floor、extrastriate Eq35 を負例として保持。
- **P08:** 2017 PLOS 20pp 出版原著 SHA `58ab19b...` + **実質数学訂正** DOI `10.1371/journal.pcbi.1005908` 3pp SHA `3df4dd0...` + 公式原 S1 DOCX SHA `59162c...`。PRE_A→E を別コミット。E 後独立3件 SHA と6段階 Git intro [37192330885](https://github.com/rinsakamo/relay-theory/actions/runs/37192330885) **SUCCESS**。**訂正原著主本文に限定して個別資格**。原著 C3 の前窓で平滑化した境界事後の再使用は **非最適**。訂正 C5 は濾波境界を使う最適系列推論だが、原著の一次Markov課題では現時点の行動予測が Bayes filtering C1 と同一。元の fitted model の数値・VBM 相関は再解析なし不変でも、旧規範的独自性、11/79 L=1 戦略推定、ΔLL と灰白質相関の一意解釈は不可。
- **P10:** 2022 PLOS 22pp 原著 SHA `36839ae...` + 公式 **資金のみ訂正** SHA `eb4c59...` + 原著 S1 Text SHA `fb5526...` + S4 Fig SHA `d427f7...`。PRE_A→E を別コミット。E 後4件 SHA と6段階 Git intro の独立CI [37192266423](https://github.com/rinsakamo/relay-theory/actions/runs/37192266423) **SUCCESS**、別の独立再実行 [37192330878](https://github.com/rinsakamo/relay-theory/actions/runs/37192330878) も SUCCESS。**基礎 Eq(1)–(10) に限定して個別資格**：学習された feature RL value が serial hypothesis test の切替仮説を方向付ける。Bayes は原著内の即時貪欲 comparator、DQN は近似benchmark。S4の拡張が held-out fit を改善しても考慮特徴数の負例は残る。原著 S1 Text には未解決 `Equation ??` 参照が残る。

**共通の正式 G1 統合分母はあえて 9/20 qualified、残 11 のまま。** W1が追加できたのは *対象限定の独立3件の資格決定*。統合側で全3件の明記した適格範囲を受け入れる場合に限り **潜在的 +3 → 12/20、残 8** だが、**科学的 G1 統合資格や diversity や最終 family clearance を本W1では認可しない**。特に P10の optional model の厳密な Eq(11)–(13) まで W1の最初のsource-first A–E に含める要求なら **P10追加範囲は未資格**なので、統合側は +2 またはさらに厳密なら保留にすること。P08原著の S1埋め込み画像2点、P06数値最適化再実装はW1限定資格外。

## 凍結 Git 科学コミット

| Stage | P06 | P08 | P10 |
|---|---|---|---|
| PRE_A | `e9677b5a44e40996bf4dcc9c8a93f3ec98ac1d4d` | `74b6310d8af50f5e126ee50e01d1cf59834be65b` | `339c7d87e04903148322e51a959c58d2b906d33a` |
| A | `13f46bfe82c9c06729904dcd7f6a583a1d9ae0de` | `43db0f246ceeffbb5335e846bbd8bdd2185d516a` | `f06a31987d9261e7a2c2682280c89136d7df4d5c` |
| B | `dd68116bc75f735182edf9faac1aa2bb47ff881e` | `2efac266c981e3d0e79fdd2c4fa599f738384bbb` | `43c1ad0bc898a136e239b7ea836293c0149da771` |
| C | `ea0060dd6898314dfa04a9d4d1c637221705f987` | `db2e06d495273f7659e652cd4e1eeb99da636084` | `98e52fca82821d84f7fbf88cb264b62383023259` |
| D | `f1bbb464315bf50b2075a1857501e37980f2c5e3` | `1c84b7b44e529839d171b8660dfce04562932eb5` | `c3bcec6fca2b463e64ed314e052aec72a42e79d2` |
| E | `2c57e8a4b09e0ec26e534d208058c475add89586` | `7eb5b2df6df90c186ae5140806752ac62d544f94` | `dcfe66ff8c526ded46a262791d29c8bf6f1e35ee` |
| 資格決定 | `7c801317b692823249e21b6535eb9a3c1acf4f25` | `eb736be2373583124c3c497b00c023cef2cdb030` | `250f0e9d4006db7cf3b24612bb5266cd6ed196c8` |

原著に先行したAはそれぞれ 28 claims / 40依存、28/40、27/43。Bは A 全体を immutable 生値で埋めて独立再読し、Cは A 全体を**変更前に再展開**。Cの追加差分/不利条件はP06が4/18、P08が6/17、P10が6/18。Dは既存 Grammar v0 のみ、Eは元資料に基づく 8/7/9 の限定忠実度対象を明示。**同じAI研究者の連続して独立した段階であり、別個の盲検人間査読ではない**。原著数値の再学習、元被験者結果の数値追試は実施していない。

## 原著・訂正・追加確認の受領と赤い監査履歴

8本の初回出版社正式ファイル SHA・バイト数・ページを [37191138347](https://github.com/rinsakamo/relay-theory/actions/runs/37191138347) にてリアルに検証。拡張原著PDF限定ページ画像化 [37191293323](https://github.com/rinsakamo/relay-theory/actions/runs/37191293323) SUCCESS。E後で独立した全18 original first Git commit/現在バイト同一/祖先順を [37192303818](https://github.com/rinsakamo/relay-theory/actions/runs/37192303818) で **18/18 SUCCESS**。同じ一次資料のさらなる公式原著から P06追加8ページ/P08追加6ページ/P10追加5ページを再取得した [37192408492](https://github.com/rinsakamo/relay-theory/actions/runs/37192408492) も SUCCESS。P08のS1原 DOCX独立追加抽出 [37192411238](https://github.com/rinsakamo/relay-theory/actions/runs/37192411238) SUCCESS（347段落/埋込み画像2点は未画像意味監査）。

これら**後期**のP06 p33（Eq41–43）、P08 p15（Eq6–10）、P10 p18（optional Eq11–13）の実画像目視を **PRE_A以前に実施したことにはしない**。凍結科学記録は不変で、独立追補 `W1_POST_E_LATE_DECISIVE_SOURCE_APPEND_ONLY_SCOPE_20261004.json` に記録。元の個別限定判定より広い結論、未読文献・原著外で補った式、S1未監査図に依拠した結論を認めない。G1統合/G4が厳密な全variant PRE_A先行条件を適用する場合、該当variantの新しい独立した prospective A–E chain が必要。

失敗CIを成功記録で上書きしない。P06の公式502連続 [37191562584](https://github.com/rinsakamo/relay-theory/actions/runs/37191562584)、[37191596079](https://github.com/rinsakamo/relay-theory/actions/runs/37191596079)、[37191713967](https://github.com/rinsakamo/relay-theory/actions/runs/37191713967)。P08 S1の公式502 [37191640992](https://github.com/rinsakamo/relay-theory/actions/runs/37191640992) と3原著追加ページ取得502 [37191741673](https://github.com/rinsakamo/relay-theory/actions/runs/37191741673)。P08 E後の不当なPDFテキストアンカーで失敗した [37192264395](https://github.com/rinsakamo/relay-theory/actions/runs/37192264395) は source hash/edition や frozen stage を触らない **テストハーネスだけの修正**で後続PASS。成功・失敗の対象と限界の全メタデータは `W1_ACTUAL_EIGHT_OFFICIAL_SOURCE_RAW_SHA_AND_ALL_POSTE_CI_RECEIPTS_v1.json`。

## 中心モデル系譜：最終認証は禁止

P06のV1 feature-tuned pool 相対最大応答–behavioral race は、既資格P05の継承IVSN top-down features＋IOR＋return-fixationと共有する注意課題ではあるが、同一のsource-native作用を直接同定したわけではない。G2 working ATT01（履歴）、ATT02（視覚feedback抑制）、ATT03（除算正規化）との厳密な原著数理系譜は独立未確定。P08はP07 Game Theory of Mindとの Bayesian/Friston/Dolan先祖的共有があるが、原論文のfirst-order reversal HMM短窓推論vs対人recursive opponent modelling は異なる候補核。G2 BLF02／BLF03との volatility/confidenceによる共通隠れ状態の可能性を保留。P10の人間featureRL→値ガイドの逐次仮説切替と既資格P09の昆虫 KC新奇適応＋PCT学習抑制ループでは元native部品が異なりそうだが、「概念」ラベルだけで完全系譜独立としない。G2 CNC01/CNC02/CNC03 と INT15 RL候補も final 原著待ち。G2 roster はmetadata onlyで予備MAIN結果に一切アクセスしていない。

## G1/G4が解決する必要のある残余

- P10の optional full SHT **原著 Eq11–13** を科学主目的の全variantとして必須とする場合、元 source-first chain では個別に全式を再構築していない。新規前向き追補を要求するか、初回qualified core Eq1–10 だけを受け入れるか、統合側/G4が判断。原著S1 Text の未解決 `Equation ??` 参照を勝手に修復しない。
- P08独立 S1 埋込み2図の意味と追加posthoc VBMを包含する資格は**未付与**。原著 p15 の実画像監査は後期に成功し、凍結前の一次資料 official complete HTML と独立されたmandatory訂正 C1–C5による core 結論に限定している。G4はこの限定の PRE_A順序適合を評価。
- P06 exact histogram optimizer formulas の original p33目視は後期であり、今回 numerical optimizer 本体の再実装資格は付与していない。元のbehavioral予測成功を全生成機構の同定に拡張しない。
- 全9件旧資格の限定/PF frozen/原著履歴を維持。全4 Wレーンの原著審査と全G1/G2 20×40中央系譜/版/多様性再調整、G3最終プロトコル/G4別途 joint review、#399著者の明示的 MAIN認可まで、**G1_PARTIAL / MAIN_NOT_AUTHORIZED**。

**本W1は他レーン完了を待たず終了し、G1共有ブランチへのmergeも共通台帳の更新も行わない。**
