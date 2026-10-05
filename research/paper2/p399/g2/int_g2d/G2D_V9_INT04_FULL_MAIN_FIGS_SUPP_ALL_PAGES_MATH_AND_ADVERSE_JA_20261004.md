# G2-D v9 — INT-04: 正式主図1–7・公式補足全9頁／補足図1–3／式1–3原著視覚監査（2026-10-04 JST）

## 権限・技術的実行証拠
- GitHub issue #399、G2凍結 parent `69748673c80f421605f1c63607472903ac2ed68c`、INT専用Draft PR #430。MAIN原稿の分解／Grammar対応／本番結果／H0-H2／fideli​ty値を見ない、共有G2 MAIN40・他レーン予約を変更しない、正式バックアップ採用0。
- INT04原著 DOI `10.1038/s41562-023-01799-z`、Nature Human Behaviour **正式VOR 2024-01-19**。初回v7原本取得とv8再取得に続き、[v9 GHA run 37205772232](https://github.com/rinsakamo/relay-theory/actions/runs/37205772232)で**二つの独立マトリクスjob（main/supp）ともSUCCESS**。各jobで元Nature実ページに掲載された3つの正式出版社媒体の正規リンクから12秒timeoutで実取得し、PDF署名/頁数/サイズと**既に固定したSHA完全一致**を各job独立照合。
- 原本3件：main VOR 20頁 2,666,492B `b78a62b28775ec55610aeeca2252bc43b1ba782486c083a5065a3419ed3cde31`；公式科学補足9頁 2,912,573B `6f9baebc2f95492b4ce275c64ed0cb640105cd480d401b78dee09c5abbb03612`；出版社Reporting Summary2頁 47,812B `a9b713fbc8d39e24534ecaceb9c6deb53f13d36b0ec21843130bb69f67ad93bf`。31頁のPDF抽出SHA索引を継続。公刊元サイエンス補足の表紙にある"authors and unedited"は**出版元自身がリンクする正式補足**の編集属性であり、preprintや非公認mirrorに切り替えたのではない。
- 物理一致原本をPyMuPDFで直接renderした各JPEGをGHA各jobログからモデルが**実際に閲覧**。v8時点のmain PDF p3 Fig1/p4 Fig2に続き、v9で**main p5–p14の10ページ（Fig3–7をすべて含む）と公式supp p1–p9の9ページすべて**を実視認。総計元原著main Fig1–7とsupp Fig1–3の**10/10刊行主科学図の構造とキャプションを確認**。ただし参照内のすべての模擬元raw pixel、公開コードの独立再実行、全改版が無いことまで証明したわけではない。社外の検索エンジンの画像から図の形を推定していない。

## 正式主原著の中核実体と7図のsource-native限定判定

| 正式Figure／画像を実視認した原本ページ | 中核操作と具体的証拠 | 誤昇格を防ぐ留保 |
|---|---|---|
| Fig1 main p3 | hippocampal MHNの**one-shot teacher trace**、ランダム入力でreplay、皮質VAE decoder/encoderの潜在表現をreplayで段階学習。scene episodic / imagined / semantic outputsを区別。 | 既存MHN/VAE/teacher–studentを当論文の独自発明にしない。図上の神経投射は実ヒト神経結合因果測定ではない。 |
| Fig2 p4 | Extended：既知の概念的latent prediction と、高reconstruction-errorな感覚的残差を海馬側に一緒に関連付ける。 | Basic Fig1とextended Fig2を混同しない。潜在変数はまだ不安定なので長期生体固定化を実計測したわけではない。 |
| Fig3 p5 | latent decoding accuracyの学習推移、色/形などvector arithmeticと潜在変数補間、サンプリングからのimagined objects。 | シミュレーション上の分類／潜在操作で、任意の新概念推論の生体因果証明ではない。 |
| Fig4 p6 | MINST手書き文字のVAE recallでprototype寄りへ統計的収縮、Shapes3Dのbound extension/contractionとlatent UMAP。 | 対応する人間図との定性的/関連先行比較は本論文自体で新規人間神経実験をしたことを意味しない。 |
| Fig5 p7 | extended modelの記憶時`prediction/reconstruction-error threshold`を上げると**海馬MHNに保存する感覚特徴数が減る一方、再構成誤差が増える**。noiseからのreplayとconcept/sensory組合せを表示。 | 圧縮と精度の有意なtradeoff。**無制約に保存量減らして精度も同時向上**との宣伝は禁止。 |
| Fig6 p8 | 曖昧な像（rabbit/hat等）に異なる外的概念ラベルを同時に付与すると、後の復元が一方の原型へ歪む。 | model memory biasの例であり、普遍的な個人の事象歪みのすべてを示す実測ではない。 |
| Fig7 p9 | DRM false-memory：モデル内の学習済み共起語VAEに`id_n`特異的リスト表現を与え、未提示の意味関連lureも想起する。20単語リスト×20 subsetsで**400 simulated trials**の平均、リストが長いほどlure想起確率が増加し引用された人間傾向を**定性的**再現。 | この論文で新たに400人を実測したわけではない。humanと数値全域で完全一致／毎回false lure必発とはしない。 |

## 補足全9頁：全3図と数学を元の画素で実確認

- **正式補足 p1**：出版社正式表紙、`authors-provided and unedited`の告知あり。Nature自身の元公開リンクとraw SHAにより**正式補足**として扱い、出版社校正済み本文VORと編集状態を同一視しない。
- **p2**：supp結果・モデル仕様。DRMの残り18リストはfalse lureが「often but not always」、実際の成績は完全必発ではない。SVMでclassifier shape few-shot：`VAE latent > low-level intermediate conv input`のsource-native設定限定で優位。一般分類器・あらゆるデータへの普遍性能ではない。Shape3D 64x64 RGB 1大VAE、MNIST 28x28白黒1小VAE。
- **supp Fig1 p3**：18 DRMリストの主要棒グラフ全体で、赤lureがある場合／ない場合、青presented・灰semantic intrusionの両方を確認。main Fig7の少数代表例から全リストに同率のfalse-lureを外挿しない。
- **supp Fig2 p4**：held-out central shapeのfew-shot SVMで大VAEの**latent-code入力が入力画素および4段conv中間特徴より速く形状accuracyを伸ばす**傾向。これは比較したアーキテクチャ・データ／SVMでのsample efficiencyであり万能の抽象化理論の実証ではない。
- **p4–p5**：64x64大VAEの具体的encoder（4 conv層32/64/128/256、mean/logvar）とdecoder（潜在次元20→dense4096→転置conv etc）、dropout0.2；小VAEの別構成を区別。**論文自身、モデル性能最適化なし・architecture choice経験依存**と記載。
- **supp Fig3 p6**：元大VAEの配線図。補足例の顔のlatent vector操作（smiling/sunglasses等）は引用元Houらのillustrationとcaptionが明示し、Shapes3D本試験で測定した新顔実験と偽ることは禁止。
- **p7 数式(1),(2)**：既存Hopfield系のenergyおよびdense polynomial (F(x))拡張を先行モデルの導入として説明。Eq(1) classical (E=-\frac12\sum_{i,j}\sigma_i T_{ij}\sigma_j)、 (T_{ij}=\sum_{\mu}\xi_i^\mu\xi_j^\mu)。Eq(2) dense (E=-\sum_\mu F(\sum_i\xi_i^\mu\sigma_i))、illustrative (F(x)=x^3)なら三階テンソル。**Krotov/Hopfield等の既発表数式**でありINT04独自に新設した保存則ではない。
- **p8 数式(3)**：特に今回用いるmodern Hopfieldの先行実装は (\xi^{new}=X\mathrm{softmax}(\beta X^{T}\xi)\)；高い逆温度`beta`で個々の記憶へのattractorを優先。Feature neuronとmemory neuronの**二部グラフ解釈**、Hebbian one-shot bindingという既存先行系譜。原著main methodsの設定は`beta=20`。**当論文の新規発明でなく、使用する既成元モデルの明示数理**。supp p9はReferencesのみ。
- 本件は正式補足に掲載されたモデル中核式(1)–(3)および全3図を**公式原画素で視認**。公開元に補足外の著者独自未提示公式ソースがあると推定して改変しない。著者コードを数学的独立再計算したとは書かない。

## 主本文Methods/Discussion p10–p14：明示的負例／未実装

- **N_INT04_V9_001 部品流用**：MHN、VAE・teacher–studentの先行技術を原著本文とsupp Eq1–3が明示。独自寄与の本質は既成部品のmemory-replay／generative-schema**結合**の具体的提案、発明の総初出ではない。
- **N_INT04_V9_002 無しとした試験**：basicのイベント全体predictabilityだけによる選択的海馬保存は**explicitly not simulated**；extendedのpixel threshold decompositionは実装。論文は自動消去／capacity制約／減衰をMHN側でsimulateせず。latent schemaの永続安定化も未解決。
- **N_INT04_V9_003 精度との関係**：Fig5のthreshold増で保存感覚ピクセル数減、reconstruction error増、basic/extended両結果のシミュレーション結果は別々。threshold=0で完全再構成となる元実装と、実装された容量制約は別問題。
- **N_INT04_V9_004 教師信号**：VAEはmain Methodsで`latent dimension=20, learning rate=.001, KL=1`と明記、MHN=10,000 patterns per Shapes3D、replay=10,000 training samples/epoch。元データ/擬似replay量と独立被験者Nを混同禁止。**標準backpropの生物学的不自然さ**は著者が明記。高効率の既知学習則の代替可能性は将来仮説。
- **N_INT04_V9_005 データ/外挿**：一回のsimulationで単一modal dataset（画像、DRMは文字）、多感覚同時encoderは**実装していない**。DRMは共起語のbag-of-wordsで順序や時間的な物語系列を学習していない。lifetime continual-learningとcatastrophic forgetting対策（双方向generative replay提案）は未実装。
- **N_INT04_V9_006 semantic/episodic**：PFC/entorhinal/alTLへの実神経部位対応と海馬損傷患者の具体的予測は**提案モデル解釈**であり元simulation/出版社図から直接脳回路因果観測されたとの主張禁止。

## INT-08暫定ペアと個別資格境界

- 選定INT04 `10.1038/s41562-023-01799-z`：元MHNで素早いencoding→offline replayでVAEの潜在`schema`重みを学習、extendedでは予測困難な感覚要素を海馬残余として保存。
- 選定INT08 `10.7554/eLife.74445`：既存LSTM/A2C/LCAに対し、progressing episode内でrecurrent controlがepisodic memory encoding/retrievalを**オンラインでゲート**して次状態予測へ活用。
- **局所source-native操作差分は提示済み**。共通の海馬／皮質祖先・各々の先行理論からの部品流用、G1 PILOT20およびMAIN40全候補との独立性は引き続き限定的。今回の元記事全図・補足数学を独立に検査したからといってINT08自身の全sourceを点検せず2件の最終family独立性が自動成立するわけではない。

## 厳格な結論

**INT04**：版源 firstparty main+official science supp+Reporting `3/3`取得、独立SHA再取得v7/v8/v9、主原著の実science Fig1–7`7/7`と公式補足Fig1–3`3/3`の限定視覚レビュー、公式supp主要数式(1)–(3)元画素検証、重大な反証・未実装条件を記録。この範囲では `INDIVIDUAL_ORIGINAL_MAIN_AND_SUPPLEMENT_VISUAL_MATH_BOUNDED_REVIEW_COMPLETED`。**実験コードの独立再現、出版社の未調査の全version history、別レーンを含む全G1/MAIN40数学的中心family独立資格を意味しない**。今回も「FULL_GLOBAL_SCIENTIFIC_QUALIFIED」の新規認定0、他候補の源流採用0。INT03 PNAS直接／Chromium再取得失敗、INT01 publisher真正原本未取得、INT13 PLOS当日表示uncorrected proof。G2-D_PARTIAL／バックアップ正式採用0／MAIN_NOT_AUTHORIZED。
