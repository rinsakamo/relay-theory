# RelayTheory Paper2 G2 v7 — 事前第1備候補の原著モデル境界、ATT必須S3、PRD第2候補の限定審査

**2026-10-04 JST。判定：G2_PARTIAL / MAIN_NOT_AUTHORIZED**。これは論文選定前の原著・原著モデル系譜・掲載版に限ったG2 PRE_A補助監査である。MAIN原著の科学分解、Grammar v0役割への再構築、H0/H1/H2、MAIN忠実度・予想結果は一切閲覧・実施しない。Issue #399/G4 #420、最初の40 DOI、v1–v6の生証拠、PF01–04/G1/G3および別#398を変更しない。**正式な備候補置換は0件**。

## 1. 原出版社の新たな物理媒体2件（条件付きの候補のみ）

出版社原著だけを独立GitHub Actions [実ジョブ 37188410375](https://github.com/rinsakamo/relay-theory/actions/runs/37188410375) で実取得。原文の著作物そのものをGitに公開せず、出版社所有原本URL・元PDFページ構成・raw SHA256などの証拠のみ保存。

- **ATT-B1の原著が式を委ねる正式なS3 Text** はPLOS自身にリンクされた元DOI `10.1371/journal.pcbi.1011283.s003`、**6頁・210,828B・原本SHA256 `c71313033e52ccbbe5b0b3e8579959dfb7ac75c52ca254a36abca89ac8fcb72f`**。実PDF抽出テキストにS1/S19が現れる。SH-CoR本体のcolor saliency、color competition、target location、selection-historyの主要数学と五つの当てはめ変種の詳細は本体PDF20頁ではなく正式なこの別添S3に明示委任される。元の第1候補の20頁生SHAはv6 `8c190f4d6e981061e4ccd67f4797b83ccdeb8f1d47d8368fdafe137f1ef44209` のまま。**本体だけの原著監査でSH-CoRの全式・変種にPASSを与えることは不可能**。S3の物理取得は完了したが、版対応・各数学の原ページ可視監査・どの数学的定義をprimary-scopeに含めるか事前資格を欠く。
- **PRD第2順位PRD-B2**、PLOS正式 `10.1371/journal.pcbi.1009557`、**39頁・2,306,402B・原著SHA256 `7b6e4192bfe1b60d794d197e14822997b77d22e437db89850fc4cddcb79482db`**。本文実抽出に固有原題をなす語5個が全出現、出版社公式完全HTMLはDOI一致。pypdf元PDF p0–1のDOI連続文字列抽出は失敗したので「PDF原ページ画像でDOI確認済み」などとは記載しない。**第2備候補の原本物理取得のみ**であり、初期40 DOIに1件も追加せず、PRD-B2の自動昇格も行わない。

## 2. 第1順位3件＋第2順位PRD候補のsource-native対照

| 備候補 | 元モデル原著と既存原著との比較 | 限定処分 |
|---|---|---|
| **ATT-B1** `1011283` | Original PLOS SH-CoRはtarget-selectionとmovement-productionを**並列**に動かし、前試行targetの促進とdistractor抑制を5変種で扱う。競合色選択と動的神経場は自己前駆CoRLEGOからの明示的拡張。現ATT-01は選択履歴・saliency・taskに応じた統合priority map、ex-Gaussian応答時間と7変種。実験の応答・構築手法は違うがhistory factorを両者とも用いる。単なる話題差から中心系譜独立を証明しない。さらにATT-B1の主要数学は上記S3にある。 | `HOLD_PRIMARY_SOURCE_SCOPE_PLUS_FAMILY` |
| **BLF-B1** `1003810` | Diaconescuらの社会的助言の正確性・助言者の意図変動モデルは、2011 Mathys等の**既存HGF**を3階層Gaussian random walk型の学習器として採用し、RWと2階層HGF、social/non-social response model合成で**12個のモデル比較**を行う。現BLF-02 `1006972` は**2個の条件付き遷移確率を同一の急峻なchange pointで連動**させる実験と階層Bayes vs fixed-leak平坦学習器を対比する。公式原文上、BLF-B1のHGF連続変動の式とBLF-02のchange-pointのモデルを1個の同じ厳密数式とはできない。しかし共通の階層不確実性学習・2011 Mathys系の文献接続は存在し、全親族（全MAIN/G1）を見ずに独立性は認定できない。 | `PROVISIONAL_DIFFERENT_EXACT_FORMALISM_FAMILY_NOT_CLEARED` |
| **PRD-B1** `1010740` | 公式原著が実際に検証するのは**行動の前後の手掛かりから運動成績に関する確信度を推定**するBayesian sensorimotor confidence（Ideal両方 / Retrospective only / Prospective only、motor/proprioceptive/setting noise）。予測／時間方向の用語が一致するからといって、原PRD-01の**適応的な順・逆方向予測のシーケンス機構**を同じと判定しない。PRD全レーンの事前定義が別の「予測的confidence family」を第3の独立系譜として認めるかは、源資料と別のsampling-policy問題。 | `HOLD_SLOT_MECHANISM_FIT_PROVISIONAL_MISMATCH` |
| **PRD-B2** `1009557` | 著者原著は内部生成モデルに基づく感覚神経の事後分布表現の下で、task dependent neural covariability / choice probability / differential correlationsを**解析的に導出**。これも感覚Bayesian predictionとの関連はあるが、元PRD-01の順・逆方向シーケンス予測と同一原著メカニズムではない。BLF-B2・LRN-B2にも**同一DOIが事前予約**されており、仮に広義PRD系譜として認めても同時採用は禁止。 | `HOLD_SLOT_MECHANISM_FIT_AND_SHARED_BACKUP_UNIQUENESS` |

BLF-B1の2014年正式訂正（`10.1371/journal.pcbi.1003952`）が第2著者所属の欠落だけを補う点はv6どおり維持する。数理・図の**訂正通知には修正が書かれていない**だけで、当該モデル数学の全版精査を終えたと解釈しない。PRD-B1の正式訂正版原文全頁、PRD-B2の数式・図の全原本目視監査、BLF-B1の原著12候補比較・不利条件・全MAIN/G1対照は未完了。

## 3. 原著スコープが論文の方法を決めている（ATT-B1）

G1の独立作業で、LRNのP13 `10.1371/journal.pcbi.1006681` は「本文26頁の中心数式が正式S1 Appendix32頁に委任されている」という事実から、**PRE_Aより前に本体＋出版社正式S1を別々に生SHA凍結し、同一作品の不可欠な元数式として科学審査**した実例がある（G1 Draft #418 source-only scope）。この厳密なprecedentをG2 ATT-B1へ自動移植するわけではない。G2側でも、S3を**正式不可欠の原著数学同梱物**としてPRE_A内で明示宣言し、#399/G4の一primary publication medium規則との整合を先行確定する必要がある。補足を「別論文」に数えて候補数や出版社多様性を水増ししない。現時点ではsource scopeとmodel-familyの二重HOLD。

## 4. 現在の分母と別レーン同期

G2主提案40 DOI（24 component +16 integration）は**不変**。実主候補原著の取得は**36/40**（本体raw PDF SHA31、別の正式全文PDFブラウザのみ2、正式完全HTMLのみ3）。元の出版社完全原著未取得は**4件 ATT-03/BLF-01/PRD-01/INT-01**。これまでの事前第1備候補PLOS原本**3PDF**、今回のATT-B1別添**S3 PDF1**、事前第2PRD-B2候補**元PDF1**はすべて主候補原著36件とは独立の取得証拠。正式に科学的完全原著採用できた主40件**0/40**、予備候補**0件**、中央family独立性承認**0件**、実際の置換**0件**。

G1 Draft #418観測HEAD `216d60dde5e793a1ddee19a7ac11925904dd5b62` はPF4＋P05/P07/P09/P13＝**8/20源資料に限定した独立資格**、8つの主レーン全て最低1件科学校正済み。残り12件の主原著科学監査とG1全20凍結、**実際に校正された8件がすべてPLOSという出版社多様性欠落**はG1の独立障害。G2はこれらG1判断を上書きせず、最終版で再照合する。

**次のG2意思決定前条件**：ATT-B1必須S3の同一作品スコープ確定＋全主要式の実原画像監査とATT-01/G1源モデル比較、BLF-B1のHGF vs BLF-02・G1全数学系譜判別、PRD-B1/B2のPRDレーン定義に照らしたsource-native対象不一致の明示処分、原PRD-01訂正後本体へのアクセス代替方針。恣意的な事後追加・予想H判定での候補差替えは認めず、G4独立合同監査と著者による明示GOまで**MAINに着手しない**。
