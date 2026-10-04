# G2-D v2：独立したsource-native原著数学・不利な条件の追加監査（2026-10-04 JST）

**対象・不変条件**：Issue #399、G2親HEAD `69748673c80f421605f1c63607472903ac2ed68c`、INT独立PR #430。MAIN Grammar分解・再構築、H0/H1/H2、忠実度、予備科学結果の閲覧なし。原著の出版社正式版／既存モデルの継承／この論文で導入した差分を区別。以前のv1原著SHA記録、取得失敗と偽陰性記録は改変しない。以下の公式原著読解は、既存の獲得物理SHAと出版社ブラウザ本文に基づく**限定追加の数学・モデル資格審査**であり、全原著・全図ピクセル監査の完了またはグローバル系譜認定ではない。

## INT-B4：正式PLOS PDFの重要数式・主要図表を視認した新証拠

正式原著 DOI 10.1371/journal.pcbi.1012872、2025-09-26刊行。現独立実取得PDF 26頁/2,483,998B/SHA-256 `67fe0d5aaed06474e53344716de73050f08e1e900420fb078712921312fb5ef6`（旧G2-D取得ログ・独立再取得ページ索引実行 `37196750620`）。出版社本文 https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012872 、公式同PDF URL https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1012872&type=printable 。

### 式／図の原著視認済み範囲（PDFページ1起算）

- **PDF p16式(1)**：set-size slopeはset size 2,3,5,6の成績の線形重み差。機構の更新式ではなく行動指標。
- **PDF p17式(2–6)**：WM誤差 `delta_WM=r_t-W_t(s_t,a_t)`、完全更新 `alpha_WM=1`、trial間のWM忘却 `W<-W+phi(1/nA-W)`、基準容量重み `w_WM=rho*min(1,K/ns)`、協調型RL誤差 `rpe=r_t-[(w_WM*i)*W_t+(1-w_WM*i)*Q_RL,t]`。
- **PDF p18式(7–12)**：RL `Q_RL,t+1=Q_RL,t+alpha_RL*rpe`、行動選択はRL softmaxとWM softmaxの`w_WM`加重和、探索epsilon混合。testフェーズはRL最終価値のみのsoftmax＋epsilon（WM寄与ゼロ）。bias変種は負フィードバック時に両モジュール学習率を`1-eta`倍する。
- **PDF p19式(13–16a)**：asymbiasでは負フィードバック時`alpha_RL=0`で`alpha_WM=1-eta`、正フィードバックでは各基準学習率。**新規と自己記述されるsplit-WM-confidence変種**は、set size`ns<K`なら`rho_below`、`ns>K`なら`rho_above*K/ns`（正確な原稿印字条件）。choice-kernelは過去行動traceを更新。
- **PDF p20式(16b)**：choice-kernelありvariantの行動方策はnoise付き基本行動方策とchoice traceの`kappa`混合。
- **p8原著Fig3**：最終Model5はlearning/testの低・高set-size性能関係を再現するが、比較の独立RL+WMおよびset-size別RL-onlyでは同じ反転パターンを再現できない。
- **p9原著Table1**：実際の6 RLWM variantを固有モデル名・パラメータ・集計AICと照合：M1 146311、M2 143910、M3 143799、M4 143718、M5 143629、M6 143770。
- **p11原著Fig5／p12原著Fig6**：計10種のRL-only対照と比較。RL-only中の最良はset-size別学習率モデルのAIC 144170（ただし原著はRLWM対RL-onlyを完全網羅的・構造同一の厳密比較とは呼ばない）。Fig6はRL-onlyがanxietyとchoice noise等の異なるパラメータに相関を割り当てる例で、独立機構の因果証明ではない。

### 新規数理の限定・重要な原著曖昧性
本文Methods自身、これらの変種は**先行文献のRLWMモデルを主体として再利用し、新規変種として「容量の上下でWM方策重みを二分」するものが1つある**と明記する。協調型WM寄与`i`およびsoftmax混合はこの論文の基準RLWM内で重要な明示的結合であるが、独立発明として数えてはならない。原著の新たな寄与は容量依存分岐のパラメータ化、非対称負フィードバックを含む系列の比較、および不安指標との統計的関連付け。**既存RLWMではなく独立した新たな一般統合原理が生まれたとする証拠は未確定**。

**N_INT_B4_V2_001 — printed equality gap**：PDF p19式(15a,b)には`ns<K`／`ns>K`しか印刷されておらず、`ns=K`の同値点をどちらへ配分するか未記載。元のEq(5)の`min`は同値点で定義できるが、`rho_below`／`rho_above`が異なる場合、分割変種は不連続かつ境界値が未記載。Kは[2,6]の連続推定パラメータだが、整数set sizeと一致する可能性を数学上排除できない。**原著の図・本文から推測して片側に無断で閉じず、published piecewise definition boundaryはUNDERDETERMINED**。これは科学資格判定の出典限定の留保であり、発表されたデータの再計算失敗を主張しない。必要なら著者公開コード等を別ソースとして比較し、印刷原著の記載欠落は残す。

### 同一原著の不利・比較結果（独立ID）
- **N_INT_B4_V2_002**：集計最良M5のAIC 143629と次点M4の143718は近接し、M4の方が個人別最適モデルとなる参加者が多い。M4はM5へ包含され、M5追加パラメータは**全員に必要ではない**。追加パラメータ有効性を全個人へ一般化禁止。
- **N_INT_B4_V2_003**：行動群では身体的不安MASQ AAとの関係が主だが、認知的心配PSWQについて同様の行動・計算パラメータの有意な一般効果は認められていない。異なる尺度に拡張禁止。
- **N_INT_B4_V2_004**：RL-onlyのparameter attributionは対照仕様・set size・決定的feedback条件に敏感で、原著自身RLWMとの非網羅的/非直接的比較を留保する。臨床全体・環境一般への外挿も未検証。
- **N_INT_B4_V2_005**：Fig3の独立RL+WM対照の失敗はこの課題の学習/試験反転に関する限定比較。「あらゆる独立RL/WMモデル不可能」という一般的非存在証明ではない。
- **N_INT_B4_V2_006**：著者の報告は観察的個人差とモデル当てはまりであり、神経学的因果的独立モジュール存在の証明ではない。

未監査の図：Fig1/2/4/7その他出版PDF全体の全重要画素、定義補足S1原著独立資料、全訂正・CrossMark履歴。特にS1のmodel/parameter recoveryは本文にあるとの記載のみ、別資料の完全検算なし。**今回の限定結果：PRIMARY_CORE_EQUATIONS_AND_SELECTED_FIGURES_VISUALLY_REVIEWED、WHOLE_SOURCE_SCIENTIFIC_ELIGIBILITY_HOLD**。

## INT-B1 ↔ INT-12：独立正式原著の源流比較強化

2018年原著 https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006116 は環境の各contextに対して(1)目標・報酬`R`と(2)行動→cardinal mapping`phi`を分解し、CRP事前分布を用いたjoint単一クラスタとindependent二重クラスタを**両方すでに構築**（Eqs(4–8)、Fig1）。両方とも推定した構成要素をplanningで方策へ合成する。jointの利点は報酬と遷移が相関する環境、independentの利点は独立環境・移動効率等。新規2020年モデルの原著 https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007720 はMethodsで同じCRP先行、同じjoint/independent clustering機構を**2018年モデルから採用した**と明記。式(1–2)はBayesian posterior/CRP prior、式(3)は両モデルの予測rewardに基づくメタ選択重みで、2018年論文の統計的トレードオフを実験的な3種類の人間grid-world環境へ適用する。2020年独自の経験的貢献を否定しないが、**このペアの独立した新しい中心クラスタ計算系譜は不成立**。

原著2020年の重要な不利条件：6候補中3モデルは非一般化対照。すべてのモデルはcontext条件付き学習でchance超え。報酬の一般化を主に測り、mappingの一般化や学習中の一般化は主実験で評価外。実験は各人各識別指標につき概ね2–4 trialしかなく、実験3で個人ごとのmeta-generalizationか二つの固定strategy集団かは明確に識別できない。元のTransitionは完全MDPの一般遷移関数ではなく、簡素な決定的button/cardinal movement mappingへ縮約されている。2018年理論モデルと2020年人間検証は**実験対象が違うことと中心モデルが独立であることを混同しない**。B1はINT12存続下BLOCKEDを維持（正規正式原著物理SHA確認済み、全重要図画素監査はこの否決を覆さない限り合理的に中止可）。

## INT-B3／INT-B2：統合モデルとモデルの当てはめを区別

B3 eLife https://elifesciences.org/articles/57244 公式VOR 2021-03-16、正式出版社PDF固有SHA `9e13535592ff1cf36c9eb4a9a1daae23cb6dfa8a916a40586a6cc5c651b80d35`。論文は既成のspDCM（Friston/Razi）をSPM実装で使い、6つの前頭領域と4つの頭頂領域のfMRIクロススペクトル密度から時不変の推定有効結合を得る。Nee & D'Esposito 2016/2017の6前頭領域classical DCMを引用し、FPCN勾配の経験的な空間拡張を報告。**実際の脳ネットワーク相互作用の推定という価値はあるが、独自の学習/制御アルゴリズムを新たに定義しているかとは別**。元論文の制限：符号付きeffective connectivityを興奮性/抑制性と読み替えるのは注意を要し、未モデル化の領域Cが媒介している可能性がある。spDCMは細胞・分子過程のモデルではなく、この研究では時間不変結合を推定。CTL-B1とDOI共有、モデル独立数学・全図ピクセル・他MAIN衝突未解決で引き続きHOLD。

B2 eLife https://elifesciences.org/articles/39497 2018-10-19正式VOR出版社PDF `c2adddf8d232d851d9decbb304fb02107686cf55a5dad4cbbfd8b0fd7ac7d64a`。確率的外的cueと内的trial-history予測の両信号のbehavioral joint influenceとPFC融合を検討する。元設計ではtask sequenceがrandom化され内的履歴は客観的に非予測的なので、「最適外的cueのみ」モデルが対照となる。大脳で複数信号が同居するだけで独自数理統合則認定しない。何より**G1 P12代替として正式予約が未解除**、CTL-B2とも共有。現状INT側の採用候補へ格上げしない。G1科学判断を代行しない。

## INT-13 final publication／INT-01 first-party publisher

2026-10-04にPLOS INT13原著公式本文は依然`This is an uncorrected proof`と明示。原PDF/HTML再取得SHAが旧G2 v6に完全一致。研究目的に有用な選択＋反応時間PADDL対照と上記B4 RLWM比較は**未校正版の暫定参考**に留める。正式校正版登場までは全数式数学同一性を仮定しない。

INT01 Cognition/Elsevier正式原著は先行公式API core metadata 2057Bしか得られず、出版社本文/PDF両403。新しい別出版社第一者URLおよびChromiumを試す独立実行ワークフロー `.github/workflows/p399-g2d-int01-chromium.yml` を追加した。物理取得の成功は実際のrunログ照合前に宣言しない。

## 判定の進行と停止

今回の限定進捗はB4原著に関する重要な式(1–16b)と選択された重要図/モデル表、B1の直接継承・原著負例の文献照合、B3/B2の機構資格に関する不確定性の縮小。**完全原著科学資格0増、全G1/MAIN系譜独立認定0、正式バックアップ採用0**。出典を判定根拠とし、原著のeq15境界不足のモデル修正、既存RLWM協調更新の新規発明化、未知の出版社訂正の不在断定、推測されたINT13最終出版版への昇格は禁止。
