# RelayTheory Paper 2 — G4 独立合同 MAIN 承認監査（2026-10-04 JST）

**唯一の正式判定: `MAIN_NO_GO`。** 本監査は Issue [#399](https://github.com/rinsakamo/relay-theory/issues/399)、読取専用 PR [#416](https://github.com/rinsakamo/relay-theory/pull/416)、独立 G1 [#418](https://github.com/rinsakamo/relay-theory/pull/418) / G2 [#419](https://github.com/rinsakamo/relay-theory/pull/419) / G3 [#417](https://github.com/rinsakamo/relay-theory/pull/417) を照合したものである。各レーンの科学的再実行、予備 MAIN Grammar 結果へのアクセス、凍結済み PF01〜PF04 と Grammar v0、#398 の変更、未提出証拠の推測補修は行わない。**PR の統合は科学的承認ではなく、MAIN 科学的実行を開始してはならない。**

## 1. 入力状態・監査基準

main 基準 `3be3267858c0b735ef7da74a876868191664a6e1`。監査時固定 PR HEAD: #416 `20a1a4c7088f11ab0631789a195a9914f96c4df0`; #418/G1 `ac8edc6fcfe0c33520b71ac5559356e325e76788`; #419/G2 `c5f70a38611394b3d393b9fe466c245bf5707699`; #417/G3 `21f49e23248e7e68c138ac5040129afeba37982a`、実際の G3 合成試験対象 `3eaf0b4c8c7089cf7c2ab7e665fbc615eb57c88c`。比較は当該 Git SHA の資料に限る。後日の PR 追記は本判定に自動反映されない。

#399 の PDF-first／取得・可読性に失敗した際の出版社指定「完全な原著全文 HTML」代替、A 前に単一原著と版を固定する条件、採用済み v2.3.1 C1/C2 と例外限定人的判断は不変。#401 の元のバイト一致検証器の移植は別ソフトウェア案件であり、新しい科学的必須条件にしない。

## 2. PF01〜PF04 の正式受領を独立検算して固定

[#399 の4件の正式判定コメント](https://github.com/rinsakamo/relay-theory/issues/399)とそれぞれの監査ブランチから資格判定 JSON を再取得した。**全4件の UTF-8 生バイト SHA-256 は掲示された正式値と一致**。既存ステージや資格範囲は変更しない。

| 対象 | 正式判定 JSON SHA-256 | 不変の科学的制限 |
|---|---|---|
| [PF01](https://github.com/rinsakamo/relay-theory/issues/399#issuecomment-5975975031) | `afe9764b7de287cefc2916affc833bfdc1f09c6dca54cd330d9a69b1693d2e22` | 原著 Fig2B U 値、拡散開始条件に数値的不一致。離散ドリフトの近連続性は条件付き、一般 H0/H1/H2 判別不能。 |
| [PF02](https://github.com/rinsakamo/relay-theory/issues/399#issuecomment-5976277653) | `a79e4a03fae2885f6df3bdbd211c81c6dd47273c553298912d97111767027fd8` | Stemme 2005 の直接祖先、p33 OU の事前承認限定解釈、元数値・行動データ完全再現なし。 |
| [PF03](https://github.com/rinsakamo/relay-theory/issues/399#issuecomment-5976117803) | `6259c845d0bc2934a3551047fd8c70ce718b1a10717ffd4cba686c7c6de1578c` | Jiang/Rao 2023 直系祖先、3階層の原著のみから確定不能な厳密イベント・スカラー、旧 E 数値 PARTIAL を維持。 |
| [PF04](https://github.com/rinsakamo/relay-theory/issues/399#issuecomment-5976104988) | `4058025a2e3886327a98e0a8f1cf6cdf9ad5f9039afb1dd80bd240cbc6caaccf` | Eq10 分母 `omega(a')` は **A 前に著者が承認した研究者による解析的正規化**のみ。原著印刷 Eq10 の訂正・当時の原著適合コードや数値再現ではない。Daw 2005 等の祖先を開示。 |

4/4 `QUALIFIED` は**原著に拘束された構造・手続**についてのみ。人間の独立な解釈精度評価や普遍的 H2 証明、数値モデルの再実験合格に拡大しない。

## 3. G1 科学的多様性・原著受付

[G1 正式判定](https://github.com/rinsakamo/relay-theory/blob/ac8edc6fcfe0c33520b71ac5559356e325e76788/research/paper2/p399/g1/G1_FORMAL_DECISION_JA_20261004.md)は `G1_PARTIAL`。既存 PF 4 件正式資格 + P05〜P20 の新16件は発見枠。GitHub Actions [原著 PDF 取得](https://github.com/rinsakamo/relay-theory/actions/runs/37178895352)の成功と別台帳で **16/16 出版社 PDF 生バイト・SHA・ページ数**、[出版社 HTML 取得](https://github.com/rinsakamo/relay-theory/actions/runs/37179212269)で **16/16** および刊行日・P08 と P10 の訂正リンクを確認した。ただし決定的原著式・図・版と全訂正・全中央モデル祖先の正式監査は未完了。追加16件の正式原著採用 **0**、科学的 A→E 完了 **0**、追加資格 **0**。

P08 の訂正は逐次推論の科学的意味に影響、P10 は資金表記だけ。P05 の IVSN 直系、P16~PF01、P18~PF04、P19~PF03 の系譜は暫定検討済みで、包括的独立性 PASS ではない。PF で主レーンが実施済みなのは MEM/CTL/PRD/SKL の4件、ATT/BLF/CNC/LRN の科学的主レーン実績は未充足。候補20件の出版元は20/20 PLOS。eLife の P12 代替候補の原著 PDF を取得済みだが科学的・系譜的適格性および交換は未承認。**20件すべて肯定的 QUALIFIED という存在しない条件は作らない**。負例・未確定例も固定分母に残し、実際に実施した校正と多様性を判断する。

## 4. G2 MAIN40 原著・版・系譜・置換

[G2 判定](https://github.com/rinsakamo/relay-theory/blob/c5f70a38611394b3d393b9fe466c245bf5707699/research/paper2/p399/g2/MAIN40_G2_REPORT_20261004.md)は `G2_PARTIAL/WORKING`。G2 の実物マニフェストを読み、**40件すべて DOI 一意、24 COMPONENT（ATT/BLF/CNC/CTL/LRN/MEM/PRD/SKL 各3）+16 INTEGRATION** を確認した。#416 の以前の10件+空欄30件という幾何に対し、今回の G2 は提案名義40件を埋めたが **最終科学採用40件ではない**。原著出版社完全 HTML のブラウザ表示25件、出版社原著 PDF ブラウザ表示1件、実体取得・ハッシュ済み原著 PDF 0件、決定的式・図と全変種を備える版・原著適格 **0/40**、中央系譜最終合格 **0/40**。公式完全 HTML による適正代替は認めるが、この25件は原著全体の重要内容の監査が未完成である。

20 PILOT の現行候補と40 MAIN 候補を実際の台帳から照合し **完全一致 DOI 0、20×40=800件の作品IDペア**。これは中央モデル・機構祖先の独立性を示さない。G2 の 40 内比較780組のうち16件をリスク候補として明記し、764件は既定で未審査。重要対立: **INT-03/INT-06** 直接的 Dehaene 系譜、**INT-15/P18/PF04** MB/MF 近縁、INT-13 と従来 Collins/Frank RLWM の直系祖先。G1 の eLife P12 代替 DOI `10.7554/eLife.39497` は G2 の CTL-B2/INT-B2 も予約し衝突する。G2 の BLF-B2/LRN-B2/PRD-B2 等も複数予備候補に同一 DOI がある。ソース・系譜ゲート後に規定した優先順と一意採択を実行する必要がある。予測される Grammar 適合性・H 結果による差替えは禁止。

出版版未解決: **INT-13** は刊行後も出版社に `uncorrected proof` と表示、**PRD-01** は確定させるべき図表訂正あり、**BLF-03** の eLife 版記録と PDF footer 不一致、**INT-08** の eLife 版/アクセスと可読性が未確定。#398旧40、旧60二台帳等との DOI 照合を完全な中央機構系譜証明とみなさない。旧 #398 を現 MAIN に流用しない。

## 5. G3 測定・盲検化・比較・凍結手順

[G3 v1.0.0 PRE-FREEZE](https://github.com/rinsakamo/relay-theory/blob/21f49e23248e7e68c138ac5040129afeba37982a/research/paper2/p399/g3/PROTOCOL_G3_v1.0.0_PRE_FREEZE.md)で、Grammar v0 に先立つ独立した原著 native **R**、R 後かつ D 前の別の Role Bridge、元の重要科学内容を損なわない **curator/P** が構成する分析者用 packet、source-locked denominator、源泉に応じた FULL/PARTIAL/FAILED/INPUT_UNDERSPECIFIED/UNDERDETERMINED、同一情報量とソース目標での A0→A1（無状態）→A2（追加持続状態）、原著由来 H1/H2 対照の前提、7種破壊対照+固定 G_dyn、forgetful map と全 maximal common images のラベル開示前凍結、S0/R0/P0/A/B/C/D/E/ATLAS/UNMASK の SHA 連鎖を確認。B が全 A と原著を見る**結果情報を使う独立再監査**であることは維持し、R と分析者の役割分離と混同しない。

[実 CI 37179072375](https://github.com/rinsakamo/relay-theory/actions/runs/37179072375)は対象コミット `3eaf0b4...` で **69/69 合成・既知 PF 境界チェック PASS**。実 MAIN 用 R 評価者・独立 R2（使用できないときは SINGLE_REFERENCE_UNVALIDATED を表示）・原著別 P 完全性検証・認識/既曝露ログ・最終名簿別分母・署名済み役割分離は未実行。G3 の合成チェックを原著意味論や数値的再現の成功に昇格しない。R に完全原著を与え、analyst に R/bridge/暫定スコアや anticipated H を渡さない。数式からの既知モデル認識は記録して評価層別化し、認識だけで選択後除外しない。

## 6. 独立 SHA-256 検算と未凍結の区別

GitHub の**指定 Git HEAD の生 UTF-8 ファイル内容**を取得し、JSON の再直列化・改行修正をせず SHA-256 を独立計算。標準テストベクタ `abc → ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` を一致確認。

| 対象 | 検算 SHA-256 | 意味 |
|---|---|---|
| G1 作業台帳 | `0ba5efaadb44b7cef38f3f90646ec49cd349b11e8facf0a2dfa8869fd5473b60` | 未承認20候補情報 |
| G1 実 PDF 台帳 | `ba1e916d597a73ee9817903d6fabd91e4d13bd9c0b580f84bc334de9d90579ca` | 原著メタデータと各 PDF ハッシュを掲載。原著 PDF ファイル本体の再ハッシュではない |
| G2 作業用 MAIN40 | `56ceba1161394c19ead7e6da5af50fde65235db3a940d5ddc7f5799335c67e88` | 掲示値と一致、**作業用のみ** |
| G2 作業用ソース台帳 | `d378ac40e55f2c03f393a0ac53eb298a3461023d172d44257deaa48e9f89a98b` | 掲示値と一致、**物理 PDF 原著ハッシュではない** |
| G3 v1.0.0 プロトコル | `73cd3a9450a104d0bd00eae1a0eed7eb34d96ad68859899a637632dc891de672` | 掲示値と一致、**PRE-FREEZE** |
| G3 評価器 | `eb9153a9a5471424a6cfe940d2fa1f12eb647d53fc85573f624e472c7111ea98` | 掲示値と一致、合成試験コード |

**最終20/40採用マニフェスト・合同評価プロトコルの科学的凍結 SHA は未発行**。現在の作業版ハッシュを置き換えとして表示することは禁止。各発行後、確定した名簿・役割契約・版原著受領・負例制約・閾値・代替優先序列の RAW bytes を別々に固定し、最初の MAIN 構造解析より前の Git 祖先および実行ログを第三者に再現可能にする。

## 7. 実行可能な合同ブロッカー

| ID | 責任 | 解消条件と必要な証拠 |
|---|---|---|
| G4-B01 | G1 | P05–P20 原著の採用版・訂正・重要式/図・全変種・合法主資料を A 前に確定。既存実PDFのSHAだけで科学的採用としない。 |
| G4-B02 | G1 | 全体 PILOT20 の**実際の**段階校正と8レーン/中央ファミリー/出版社/媒体の科学的多様性を審査。失敗例を含め分母・不足を固定し解消。 |
| G4-B03 | G1+G2 | G1 最終20×G2最終40の中央系譜・予備候補予約、G2内部リスクと既定未審査ペア、#398等祖先を原著根拠で裁定。直接重複は固定した客観規則で置換。 |
| G4-B04 | G2 | 40/40 最終出版原著版（PDF優先・正規完全HTML代替）、訂正・全決定的式/図・変種・原著受付 receipts。INT-13/PRD-01/eLife版問題を明示解決。 |
| G4-B05 | G2 | 24の相異なる適格成分ファミリー、16の適格統合対象、PILOTと非重複、予備候補の一意優先序列を結果非依存に確定し最終名簿を発行。 |
| G4-B06 | G3 | 実際の最終40原著を基に R、完全性監査をする P、先行固定 Role Bridge、認識/曝露、原著別分母・対照・atlas/ラベル開封を実作業と署名記録に落とす。R2 がいなければその限界を表示。 |
| G4-B07 | G4+著者 | 最終名簿と最終合同プロトコルを**初回MAIN科学解析より前**に独立ハッシュ・固定し、すべての未完条件を検算。別途 #399 で明示的著者 GO。 |
| G4-B08 | MAIN全レーン | B01–B07完了までは MAIN の S0/R0/P0 を科学的本番として開始せず、A/D/結果閲覧/ラベル解封をしない。 |

## 8. 初回 MAIN 着手判定

**`MAIN_NO_GO`、承認証 `null`、初回 MAIN 論文の実行指定 `null`。** この二つの `null` は忘失ではなく、最終40と測定を欠いたまま暫定論文を選んで先走ることを防ぐ意図的な fail-closed 受領である。G1/G2/G3 がそれぞれ自分の独立成果物に不足証拠を正当に追加し、その Git HEAD・原著ハッシュ・最終科学判定を提出した後、**新しい G4 再監査**で相互照合する。全必須条件が PASS した場合に限り、最終マニフェスト/プロトコルのハッシュを発行し、#399 の著者に合同 GO と**最初の MAIN 論文の別途実行承認**を求める。

監査機械版: [G4_INPUT_SNAPSHOT_AND_MAIN_NO_GO_v1.json](G4_INPUT_SNAPSHOT_AND_MAIN_NO_GO_v1.json)。本 Draft PR は監査記録であって科学的実行許可ではない。
