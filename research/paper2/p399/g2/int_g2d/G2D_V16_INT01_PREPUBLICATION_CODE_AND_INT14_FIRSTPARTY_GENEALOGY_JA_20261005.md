# G2-D v16：INT-01 出版前コードの同一性確定・印刷式の不一致の定量的な境界と INT-14 との原著系譜比較

**2026-10-05 JST／append-only／G2-D科学原著の個別限定監査のみ。** Issue #399、Draft PR #430、著者のINT13未校正稿研究版の狭い承認PR #434を遵守。既存G2 40DOI/G1/G3/G4/PF/Grammar v0/#398に変更なし。MAIN A/B/C・Grammar分解・H判定・予備結果閲覧なし。

## 1. INT-01元出版社原稿の証拠

ユーザーが通常ブラウザで保存したScienceDirect（Li & Collins, DOI 10.1016/j.cognition.2024.105967）**公式完全HTML MHT 5,754,741B、SHA256 `32158948f6d1f4ffd7170393c30a5742ce7db1b0a871928f64bd176cf9ab3b64`**、その中の出版社本文HTMLのみ**1,250,747B、SHA256 `0c6c2670f715b06e3a9596cf848df9e08bb5b5168d5dd57113730d3d50b8fc52`**を本セッションで独立再確認。同本文は Methods §2.3.1（task-setは行動のvalueを保存）、Algorithm 1、§2.3.2 Algorithm 2、§2.3.3、§2.3.4の印刷尤度式、本文Appendix A/Bを含む。MHTから著作権付き原著そのものは公開Gitへコピーしない。PubMed PMID 39368350 は初回オンライン2024-10-04、誌面2025年1月の区別を記載。

**論点**：出版社本文§2.3.4の例示的な周辺化尤度は印字上 `-log Σ_i Pr(TS_i|c_t;t) TS_i(s_t,a_t;t)`。同一原著§2.3.1はTSをstate/actionの「value」を記憶する表現と説明し、Algorithm 1の行動選択にはtemperature付きの確率変換と探索ノイズがある。したがって**印刷されたTS_iを生Q値のまま解釈**すれば、行動確率を計算するコードと一般には等しくない。一方、著者が印刷式のTS_iを行動確率の略記として再定義していた可能性は、出版社の正式注記／訂正文の証拠なく単独で排除・採用しない。

## 2. 「出版後のコード変更が原因」仮説をさらに審査

著者公開GitHub [jl3676/learning_hierarchy](https://github.com/jl3676/learning_hierarchy) のAPIを使い、**論文のオンライン公開前**に`modeling.py`を更新したと記録される [2024-09-11 commit `5f0832edb0a9342a9c6100a05a345e3bac063963`](https://github.com/jl3676/learning_hierarchy/commit/5f0832edb0a9342a9c6100a05a345e3bac063963)を実際に取得した。同コミットの`modeling.py` Git blob **`97104ec77c324654883cd96518d93e6304edb875`**は現行mainの**同じファイル全体と完全一致**した。2024-09-10にはlikelihoods reimplementedという先行コミット記録も存在。これは現行コードだけを見て「出版当時とは異なるかもしれない」とする古い曖昧性を実際に減らす。ただしGit記録の日付自体は第三者による独立実験ログではなく、出版当時の全解析環境・既発表フィット全数が当該コミットで実行された証明でもない。

出版前のコード実在行（同じblob現行と一致）：
- `modeling.py:106–107`：各TSの`Q_full`を`softmax(beta_2 * Q_full)`し、該当選択肢確率を`PTS_2`で周辺化、その後`(1-epsilon)`と`epsilon/4`で混合。
- `modeling.py:128–136`：compress1/compress2/fullの候補があるときはmeta posteriorで方策自体を加重混合した最終選択確率を作り、`llh += log(pchoice_2)`。
- `modeling.py:170`：`return -llh`。

**元論文の実験再現ではないillustrative反例**：`TS_1=[0.8,0.1,0.05,0.05], TS_2=[0.2,0.5,0.2,0.1], PTS=[0.7,0.3], beta=5, epsilon=0.1` の一例で、印刷式をQ値の重み付き和と読むなら対象行動の値は **0.62**、出版前コードのsoftmax→周辺化→epsilon選択確率は **0.647923132**、差 **0.027923132**。この数値は元著者のパラメータ推定やモデル比較を再現したものではなく、二形式を無条件に同一視できないことの小さい反例である。

**限定決定**：出版前モデルコードの位置・ファイル同一性は`QUALIFIED_BOUNDED_IMPLEMENTATION_WITNESS`。INT01のpolicy-meta/hierarchical/forward-backwardモデルの演算的な種類はsource-nativeに有限範囲で確定可能。ただし**印刷式の正しい最終記法、公式訂正・著者明示解釈、掲載済み全パラメータ適合結果の正確な数量再現はHOLD**。印刷式のsilent patch禁止。従ってINT01**全source-science無条件資格はまだHOLD**。

## 3. 追加 INT-01 × INT-14 同一 CRP数理の中心系譜比較

初めて独立に [INT-14 Tomov et al. 2020 PLOS出版社の公開原著完全HTML](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007594)を開き、**Theoretical background Eqs1–10、Fig3、後続Task/Reward distributionとDiscussion**を直接検査。旧G2が物理取得したINT14公式PDF SHA `52611f861e4bdf9e568b11332d4890c01506156607f81a50fd87178f82ce0fbb`は継承するが、今回全出版社PDF印刷ページの数学・全図・全補足をあらためて画素完全検査したとは主張しない。

- **共有した構成数理**：両原著は階層潜在構造とCRPによる非パラメトリッククラスタ先験を用いる。INT01出版社HTMLはTomov2020を階層表現研究として文献引用している。これだけではINT14の中心実装の直接コピーとも、CRPの独立再発明とも数えない。
- **異なる中心対象**：INT01は文脈別の**state-action task-set方策の再利用**・compressed2＋hierarchical1のmeta choice mixture・前向き／後ろ向き方策チャンクの転移。INT14は**既知の環境グラフG上の状態を高次クラスタとbridgesに分割したHを推論**し、P(G,H)の生成モデルと`P(H|G,tasks,rewards)`の事後更新・階層BFSで経路を計画。クラスタリング対象、事後推論での依存変数、最終readoutと実験課題が同一の中心演算ではない。
- **INT14の不利な原著境界**：自著の生成モデル全体の形式的最適性は証明したと主張せず、実験3のモデルと人間の効果量には差、既知で決定論的・双方向のグラフ、単一ノード単一クラスタという制約を置く。大規模グラフの近似推論／生物学的実装は提案・将来課題であって直接実証済みではない。

**限定系譜結果**：`SAME_GENERIC_CRP_COMPONENT_DIFFERENT_SOURCE_NATIVE_CORE_OPERATORS_FOR_THIS_PAIR`。同一名詞・共通CRPだけを理由とする**機械的重複認定は却下**できる。ただし全数学の変換可能性・他INT/G1との直接家系・両論文の完全式／補足審査まで含めた**最終global independent資格はUNDERDETERMINED**。独立数理の新規性を誇張せず、CRP自身は共有既存技術と記録する。

機械台帳：`G2D_V16_INT01_PREPUBLICATION_AUTHOR_CODE_AND_PRINTED_EQUATION_ADVERSARIAL_DECISION.json`、`G2D_V16B_INT01_INT14_FIRSTPARTY_CRP_NATIVE_FAMILY_20261005.json`。

## 4. G2-D全体の正式資格ゲート維持

INT13は著者承認の**PLOS未校正稿PDFを正式な研究用参照版**として維持。INT03は公式完全HTML媒体を技術選択済み。INT04は公式主原著＋補足＋reporting3媒体の実raw SHAと主要図が既に限定レビュー済み。INT06は主原著＋8元補足9/9媒体取得済み。INT01の閲覧障害はユーザー保存の元出版社HTMLで本セッション内解消。残り11件を含む全16原著の全数式／全図／変種／負例／訂正およびG1との中心家系独立の**全面資格を一斉に済ませたと見せかけない**。バックアップ正式発動0、主G2統合・G3/G4合同・#399の著者MAIN実行GOは別に必要。

**v16後もG2-D = PARTIAL／MAIN_NOT_AUTHORIZED。** 旧失敗のraw収集ログ、原著SHA、限定科学の正証・不利な原著記録はすべて保持。
