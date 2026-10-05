# PRD-01 原著補足Fig S2出版誤表示の独立追究：出版前の著者公開実験コードで意図された確率を解明

**追記日：2026-10-05 JST。** 先行の`THREE_SUPPLEMENT_SCIENTIFIC_ADJUDICATION_JA_20261005.md`が物理原本に見つけた三値衝突を改竄しない。本文図2a/4aの正式訂正と、未訂正の補足図S2を厳密に区別したうえで、**追加の独立・出版前著者コード証拠**から採用すべき実験意図の値を推定する。

## 1. 先行原資料の実矛盾（引き続き真）

真正Nature補足原本17頁（SHA `10f5d55f971060fb325e3e5a0bb4be2df015407ecb1428af9ebd17a4bea6298c`）の**Fig S2 Study2／PDF p6**を原本画像で開いた。図には`trident p=0.33, planet p=0.67`と印刷されている。同頁図キャプションは反対の`trident 67%, planet 33%`を記す。一方、Nature正式通知（2024-08-08、DOI `10.1038/s41562-024-01978-6`）が指定する訂正対象は**本文Fig2a（Study2）および4a（Study4）のみ**で、本文採用値は`trident .69, planet .31`。通知は補足FigS2の差替えを宣言していない。**補足FigS2の図・説明・訂正本文が三者不一致である事実は残す**。FigS1 p5はStudy1で`.33/.67`が図・キャプションで一致し、**Study2の補正対象ではない**。

## 2. まったく別の独立資料：筆頭著者の出版前公開コード

公開原著コード：
[psharp1289/Humans-Adaptively-Deploy-Forward-and-Backward-Prediction](https://github.com/psharp1289/Humans-Adaptively-Deploy-Forward-and-Backward-Prediction)。
４つの該当ファイルのGitHub履歴を再確認し、**すべて2024-05-04 15:49:57 UTCの既存commit `ab131a9d0366df00ac2dc79438fe9a89e30f5767` に存在**、その後の個別修正commitなし。論文初公開2024-07-16より前の時点の証拠である。

| 実験 | 公開タスク実行JSが明示するtrialList | そのCSVの520行を直接数え直した内訳 |
|---|---|---|
| Study2 | [`study2.js`](https://github.com/psharp1289/Humans-Adaptively-Deploy-Forward-and-Backward-Prediction/blob/ab131a9d0366df00ac2dc79438fe9a89e30f5767/Study_2/task/study2.js) → [`Study2_learningtrials_r3.csv`](https://github.com/psharp1289/Humans-Adaptively-Deploy-Forward-and-Backward-Prediction/blob/ab131a9d0366df00ac2dc79438fe9a89e30f5767/Study_2/task/Study2_learningtrials_r3.csv) | `trident.png=360`, `planet.png=160` |
| Study4 | [`study5_pr.js`](https://github.com/psharp1289/Humans-Adaptively-Deploy-Forward-and-Backward-Prediction/blob/ab131a9d0366df00ac2dc79438fe9a89e30f5767/Study_4/task/study5_pr.js) → [`new_trials.csv`](https://github.com/psharp1289/Humans-Adaptively-Deploy-Forward-and-Backward-Prediction/blob/ab131a9d0366df00ac2dc79438fe9a89e30f5767/Study_4/task/new_trials.csv) | `trident.png=360`, `planet.png=160` |

さらにStudy2の`r2.csv`と`moretrials.csv`も別々に520行すべて確認し、**両方同一の360/160**。Study4の`study5_pr_2.js`も`new_trials.csv`を参照する。異なる公開実装・試行ファイルで一貫している。

この素の生起回数からそれぞれ`360/520=0.6923076923...`、`160/520=0.3076923077...`。小数２桁にすると**Trident `0.69`、Planet `0.31`**となり、著者承認済み本文Fig2a/4a・正式出版社訂正の両方と一致する。**補足FigS2図の`.33/.67`は確率の大小関係すら逆で、キャプション`.67/.33`も定量値として不正確**。

### 科学的判定

- **解消した事項**：Study2・4の**公開された出版前の具体的実験プログラムの学習試行設計におけるsource-nativeな採用比率**。仮説ではなく、公開コードが実際に参照するCSV行を全件集計した。本文の正式採用値`.69/.31`をこの追加証拠が独立に裏付ける。
- **解消したとは主張しない事項**：出版社の補足FigS2の画像は今も未訂正のまま。2024年の実験参加者が全員この公開コードと完全に同一の環境・trial listを実際に経験したことを、実験生ログ／版ごとの配布証跡で確定したわけではない。オリジナル数値フィッティングや参加者ごとの予測再現も未実施。補足S2の初版誤表示を「訂正済み出版社補足」と再命名しない。
- **G2/ G4への実務**：PRE_A数理上、**リリース済みコードの元試行数と正式訂正本文の一致を限定科学証拠として採用**し、補足FigS2の不一致は`PUBLISHED_SUPPLEMENT_FIGS2_UNCORRECTED`の版・図面フラグとして記録。同図からstudy2の確率の数字を読むことは禁止。実験参加者生ログの必要性が主張射程を超える場合、数値の経験的同一性は`UNDERDETERMINED`のまま。この限定処理は著者承認済みの原資料セットに対して元の判断を無断で改変するものではない。

詳細な４著者コードGit blob SHAと公開前commit、数値・留保は`PRD01_PREPUBLICATION_TASK_CODE_NUMERIC_RECONCILIATION_DELTA_v1.json`に追記。元`THREE_SUPPLEMENT_EXACT_SOURCE_AND_SCIENCE_RECEIPT_v1.json`の原本矛盾の事実・当時の保留はそのまま保持する。**３補足PDFの取得・本文に紐付けた原本凍結3/3、必要導出のソース科学審査3/3；最終MAIN40全数学・系譜・定量再現の資格化はまだ無条件ではない。G2_PARTIAL / MAIN_NOT_AUTHORIZED。**
