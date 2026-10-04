# G2-D v2a：v2追加監査の科学的訂正・完全主本文ページ範囲・Chromium実ログ（2026-10-04 JST）

**これは旧v2を削除せず追補するappend-only訂正。** v2の「B4 p16–20 Eq(1–16b)」はRLWM主モデル群の範囲として正しいが、**これだけを全原著数式と読んではならない**。出版社正式PDF後半p22–23に**別のRL-only対照の式(17–24b)**があると改めて確認した。今回、原著同一SHAの公式PDFの対応ページ画像と出版社正式完全HTMLで追加確認した。科学的文献引用、訂正履歴、全MAIN系譜独立性は別の条件であり、MAIN解析はしない。

## A. INT-B4の主本文重要数式・全7図・主要表の視覚範囲

**原著の真正媒体**：PLOS出版社正式26頁の公開PDF `10.1371/journal.pcbi.1012872`、既存G2-D独立物理取得SHA `67fe0d5aaed06474e53344716de73050f08e1e900420fb078712921312fb5ef6`（2,483,998B）。PDF first-party URL `https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1012872&type=printable`。全26頁のテキスト索引／raw SHA一致は独立CI `37196750620` 成功。ページ画像で実際に次のPDF印字ページを視覚検査した（印字ページは1起算）。

| 出版社正式PDF頁 | 本文で実確認した対象 | 範囲 |
|---|---|---|
| p5, p6 | Fig1とFig2 | set-size実験、学習/テスト時系列、身体的/認知的症状分離；PSWQ大半非有意 |
| p8 | Fig3 | RLWM M5の学習／遅延test set-size関係、独立RL+WM / RL-onlyの限定比較 |
| p9 | Table1 | RLWM全6変種、パラメータ差、AIC表の数値原典 |
| p10 | Fig4 | MASQ AA/PSWQとM5パラメータの分離；多重比較後非有意項目を有意と誤記しない |
| p11, p12 | Fig5, Fig6 | RL-only全10対照AICとMASQ AAとの関連パラメータ比較 |
| p16 | 式(1) | set-size slopeのbehavioral contrastでありモデル更新式ではない |
| p17–p20 | 式(2)–(16b) | WM/RL協調誤差、容量重み、方策混合、試験時WM不使用、bias/asymbias/split-rho/choice-kernel主モデルすべて |
| p21 | Fig7 | 個人単位でM4の採用割合がM5を上回る。集計AIC順位との違い |
| p22–p23 | **式(17)–(24b)** | RL-only基準prediction error/価値更新/softmax/noise/試験方策、choice kernel/忘却/負feedback全対照更新則 |

従って**この原著の主本文に印刷された式(1)から式(24b)、Fig1–7、Table1のsource-native数学・図表の候補資格範囲は確認**した。本文外のS1 Textにあるモデル・パラメータ回復の補助図A–Gや外部コードは独立して全数式図を資格化していないので、「すべての独立付録の数学・数値再現」とは表現しない。出版社主本文でS1はデータ回復等を補強する別資料であり、主本文の数理式(1)–(24b)を別添S1に全面委譲してはいない。元#399のpublisher original PDF優先/正式complete publisher HTML同格規則を守り、S1の原典を同等物へ無断編入しない。

### RL-only対照の数学的情報の正確な修正

追加で実確認したp22–23式(17–24b)：RL-only元モデルは`rpe_t=r_t-Q_t(s,a)`、`Q_{t+1}=Q_t+alpha*rpe`、softmax＋epsilonの行動確率、テスト時は最終RL価値のみのsoftmax。2クラス（共有単一学習率`RL_alpha`、set-size別5学習率`RL_5alpha`）に各5変種（基準＋choice-kernel＋RL忘却＋負フィードバック）を組み合わせ、表・Fig5の合計**10 RL-only対照**を構成する。実Methods文は「8追加」と記載するが、これは**2基準+8追加=10総数**で矛盾しない。各クラス4増分と解釈しない。二クラス共通の既存RL計算モデルでありB4が新しい独立RLWM統合機構を作ったことの証明ではない。

### 原著の有利・不利な境界を保存
- Eq(5)単一`rho`の容量重み、Eq(6)既存協調パラメータ`i`、Eq(8)WM/RL加重softmax混合は**継承RLWMの中心結合**。原著は比較変種で新規にsplit`rho`（容量K未満/超過）を導入したと説明する。split`rho`は新たな条件付き重みだが、独立した新しい大域的協調機構を発明したとはまだ証明されていない。
- **N_INT_B4_V2_001**：Eq(15a,b)は印刷上`ns<K`と`ns>K`のみで`ns=K`未定義。Kは実推定で[2,6]連続可。著者未確認の数学的閉包を勝手に補完しない。
- **N_INT_B4_V2_002**：M5集計AIC 143629とM4 143718は僅差、原著Fig7の個人別勝者はM4が多い。S1のモデル回復報告（本文は記載）を実証再計算したとは言わない。
- **N_INT_B4_V2_003**：同じ課題Fig2/Fig4/Fig6では認知的心配PSWQと一連の有意な性能・モデル関連はない。Fig4のWM negative-feedback WM eta相関は**多重比較補正後非有意**。身体的不安とPSWQや未測定疾患を混同しない。
- **N_INT_B4_V2_004**：Fig3における単純独立RLWMとRL-onlyの失敗は**この実験の学習/試験のset-size反転**に限定。全モデル不可能性を主張しない。Fig5/Fig6のRL-onlyは当該課題構造/決定的feedbackへの依存があり、著者も網羅的な等構造比較とは主張しない。
- **N_INT_B4_V2_005**：原著はオンラインn164の行動とパラメータ相関であり、不安による神経回路因果を測定していない。さらにFig7の個体間差は誰もがsplit-rhoを必要とするという主張を排除。

**科学的限定結果**：`MAIN_ARTICLE_CORE_MATH_AND_ALL_MAIN_FIGURES_VISUALLY_INSPECTED_BOUNDED`は認める。訂正履歴の完全検証、Eq(15)の正規境界の明示、S1に依存する独立モデル回復数値検証、Collins/Frank 2012・2018／INT13最終版・全G1・全MAINの中心モデル独立性は**未解決**。現在の正式バックアップ資格・採用ともにHOLD、正式採用0。

## B. INT01新規出版社経路の物理診断

既存Elsevier通常HTTP403・正規出版社API書誌core-onlyからさらに異なる**第一者publisher Chromium実行**を追加。[run 37197511423](https://github.com/rinsakamo/relay-theory/actions/runs/37197511423) SUCCESSは全試行ログ出力の意味であり、原著取得成功ではない。実結果：
- ScienceDirectブラウザ通常DOI-PIIページ403/本文729chars・正式全文節0、別クエリ`via=ihub` 403/本文729chars・正式全文節0。
- Elsevier linkinghub初期200も最後のScienceDirect制限ページ403へ転送され本文729charsのみ。
- ScienceDirect redirected PDFは403/非PDF payload 1,208,114B。出版社ars.els-cdn第一者PDF候補は400/非PDF 219B。DOI原著完全HTMLまたは正式PDF **0**。
- 結論：今回試した複数第一者の直接HTTP・Chromium・別PDF経路はどれも正式版の原文を得なかった。**INT01正式原著HOLD**を維持。この試行範囲外のすべての可能な取得経路が不可能という一般的断言はしない。既存PMC12052257のAuthor manuscript昇格は禁止。

## C. 原著科学と合同承認を分離

B1の2018年モデルからの直接継承（2020年の新規実験と独立新数理は別）によりINT12維持中はBLOCKED、B2はG1 P12の予約を尊重、B3の既存spDCMへの当てはめ対独自新規統合数理の最終判定はHOLD。B4は主原著数学をより深く資格化したがグローバル中心系譜未確定。INT13は正式出版社の表示が引き続きuncorrected proofでHOLD。現時点でMAIN科学的解体・再構築・忠実度・H評価・予備結果閲覧はなし。正式採用数0／全G1/MAINの最終中心系譜独立認定0／MAIN許可なし。
