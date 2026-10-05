# RelayTheory Paper2 — G2 v8：ATT-B1の単一正式原著＋不可欠S3をA以前に資料範囲固定

2026-10-04 JST。**G2_PARTIAL / MAIN_NOT_AUTHORIZED**。#399/#420と過去G2 v1–v7、元のMAIN40、別#398、PF01–04、Grammar v0、G1/G3独立判断は不変。今回の操作は**未採用の事前備候補ATT-B1だけのソース構成PRE_A固定と、今後の正式科学審査に先立つ原著に記載されたモデル候補・負例の範囲登録**であり、MAIN構造分解・Grammarマッピング・H0/H1/H2評価・成績による論文選択ではない。正式な原著科学的採用はしない。

## 1．技術的ソース構成を固定した

候補はMakwana, Zhang, Heinke & Song（2023）、`10.1371/journal.pcbi.1011283`。

- **唯一の主媒体**：PLOSが出版した正式な**20頁original PDF** `https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1011283&type=printable`、**1,760,491 B、SHA256 `8c190f4d6e981061e4ccd67f4797b83ccdeb8f1d47d8368fdafe137f1ef44209`**。
- **同一作品内の数学的に不可欠な正式出版社資料**：出版社自身が上記原著HTMLに公式に結び付けた**S3 Text 6頁** `https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1011283.s003&type=supplementary`、**210,828 B、SHA256 `c71313033e52ccbbe5b0b3e8579959dfb7ac75c52ca254a36abca89ac8fcb72f`**。
- 20頁本体がSH-CoRの色刺激特徴、競合神経、target-location map、selection history、movement production、パラメータ最適化の重要数学をS3 **Eq S1–S19／Tables A–D**へ明示的に委任している。これは「外部補足を全て主研究に混ぜる」ことではなく、**主媒体は20頁PDFただ一つ、数学的定義に必要な同一出版社S3を固定した同梱資料**とする。二つの別論文・二つのprimary PDFには数えない。
- S1/S2は自動追加しない。特にS2 Fig Cにしかある種の非最適パラメータの逆転効果の画像がないため、**画像を実確認しないうちはその追加図に依拠する強い主張を対象外**。本体Fig4の観察された不一致は本体内に記されており、**その狭い源資料の範囲**では負例登録できる。後日必要なら科学審査前に別途版付き登録し、無断拡張しない。

前回v6／v7の別々の物理取得に加え、[独立再取得GitHub Actions `37189209061`](https://github.com/rinsakamo/relay-theory/actions/runs/37189209061) で**両原本のそれぞれのraw SHA、バイト長、20頁＋6頁が一致**。同じ出版社の原著完全HTMLも別実取得し、正規DOIと正式S3へのpublisher-original linkが存在。実メタデータ受領raw SHA `e08e2394d858211813052a80302f246e92238fb7b5cc2eea3341c0c49bf6df16`。原本文書の著作物本文はGitへ保存しない。

**資格の厳密な区別：** 現在この「ソース構成の候補PRE_A技術凍結」は成立。ただし未認定のS3画像全ページ・文字と元画像数式との同一性、全variant/negative、同一出版版の訂正履歴、ATT01/G1/他MAINとの中心系譜独立性は未達。完全科学的原著資格やバックアップ稼働を主張しない。

## 2．S3の6頁物理原本ページ地図

同一raw SHAの6頁S3に対するPDFテキスト抽出の位置照合。文書内のS1～S19という**19個の識別子すべて存在**する。しかし抽出した文字の存在は各式のピクセル可読性・添字・分数・不等号までの数式同一検証を証明しない。

| S3 PDFページ（先頭を1とする） | 確認した式参照・役割 | 次の独立画像監査 |
|---|---|---|
| 1 | S3の資料冒頭、A～D表や模型・パラメータ索引 | 冒頭版・表索引 |
| 2 | S1～S5本体、S6の参照。Target Selection／色特徴 | 式S1～S5と色saliency・global inhibition |
| 3 | S3～S5の再登場、Target Selectionの続き | 数式の続き・定数/符号 |
| 4 | **S6～S14**、履歴機構とmovementへの接続 | 各式の状態・時間・入力／抑制・促進の違い |
| 5 | **S15～S19**、変種のfit/noise/評価。S1/S2/S6も再引用 | タイミング、5候補のパラメータ表と評価の一致 |
| 6 | 末尾の注記 | モデル解釈を左右する注記・条件がないか |

**原著陰性条件も固定：** 本文と正式S3の本体で、標的の促進のみM1、妨害抑制のみM2、同時実施M3a、促進→抑制M3b、抑制→促進M3cの**5候補を必ず保持**。本体ではmodel 3aが本来は無拘束なら再現の可能性があるが、著者の生物学的制約下で部分swap trajectoryを誤ると説明。M3bの序盤のswap引力の順序がhuman curvesと逆転する不利結果を削除してはならない。M3cの65%切換時の最良誤差 **0.64 ± 0.01**、同じM3cでも80%切換にすると誤差 **0.71**というパラメータ依存性、PCRの線形解釈の限界、2D限定simulationも保持する。原著にある値を索引化しただけで元の数値再シミュレーションは未実施。

## 3．既存ATT-01との厳密な重複防止が残る

現MAIN候補ATT-01 `10.1007/s42113-024-00197-6` は、歴史map・saliency mapとtask依存重みを統合し、reaction timeの**ex-Gaussian予測**と応答確率を比較、**7 variant（M1～M7）**を持つ。一方ATT-B1は過去のCoRLEGOを拡張した色競合／dynamic neural fieldsを介して、reach trajectoryと標的／妨害特徴の先後関係を5モデルで試す。**出力の運動軌跡とRTが違うだけでは系譜独立の証拠ではない**。両者はselection historyと競合saliencyの祖先を共有する恐れがあり、全ての数式・機構、引用元、G1の最終20作品との比較を課す。

並行するBLF第1備候補と既存BLF-02は、後者も**Mathys et al. 2011を直接引用**することを出版社原著で確認。BLF-B1はMathys自身が共著するHGF応用（連続変動社会的助言）であり、BLF-02の共有change-point突然変動モデルと**厳密な数式構造の相違**があっても、共通祖先がある以上、結論は従来どおり **別実装は仮説、中心family最終合格ではない**。BLF-B1の12比較モデル・不利条件・BLF-02の独立controlまで監査する。

## 4．元コーパス・G1/G3に影響しない

MAIN候補の40固有DOIは全て不変。物理的に一次出版社原著を取得できた元候補**36/40**（元PDFの生SHA**31**、公式原著全文PDFブラウザのみ2、公式完全HTMLのみ3）、未取得**4**。バックアップ第一順位の原著PDF3件、今回固定したATT-B1正式必須S3 1件、第二順位PRD-B2 1件は**元の36件に加算しない**。バックアップ完全科学資格0、中心family確定0、実置換0、元のMAIN40完全数学・全図・全変種の科学的原著資格**0/40**。

G1独立の観測結果はPF01–04およびP05/P07/P09/P13＝8/20限定科学資格で、最終20原著の同一版と系譜凍結は未完了。G3は別レーン、G4独立合同再監査と#399著者の明示的MAIN承認が必要。

## 5．次の実行順（事前に変更可能な範囲を狭く）

1. ATT-B1の版付き主PDF20頁＋不可欠S3 6頁の**決定的な数式・図・5変種の実画像**を審査し、源本文に隣接する反例を全て登録する。S2 Fig Cの実画像を使う必要が科学的に発生した場合、そのための別の明示的pre-A対象拡張の審査を先に行う。
2. ATT01の全原数式と両者のCoRLEGO/priority-mapの中心mechanism/ancestry、G1最終20と原著比較。source scope技術的凍結とcentral-family scientific資格は別の独立判定。
3. BLF-B1について2011 Mathys共有祖先に対し同式系を再利用したのか、異なる原著仮説か、原著12variantとBLF02突然変動モデルを対にして判別。
4. PRD-B1/B2は名前の「prospective/retrospective」を元PRD01のforward/backward sequence predictionへ強引に同一視しない。訂正後原著の入手か適格な事前standbyの選定基準を先に確定する。

**G2_PARTIAL。G2のsource bundleのみ先行固定。MAIN_NOT_AUTHORIZED。**
