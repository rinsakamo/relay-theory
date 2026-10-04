# G2-D v18 — INT-01 出版社完全HTML原著の本文・15図・2アルゴリズム・全付録の全体科学審査と限定系譜判断

2026-10-05 JST / Issue #399 / [G2-D draft PR #430](https://github.com/rinsakamo/relay-theory/pull/430)。本実行は原著の科学的な出典審査であり、MAIN Grammarの分解・再構成・盲検unmask・H判定ではない。G2/G1/G3/G4名簿、Grammar v0、別の歴史的#398は変更しない。

## 出典・原著全範囲の実体

ユーザー提供の通常ブラウザ出版社ScienceDirect完全HTML MHTを独立に再解析した。INT01 Li & Collins、DOI `10.1016/j.cognition.2024.105967`、PII `S0010027724002531`。**元MHT 5,754,741バイト／SHA256 `32158948f6d1f4ffd7170393c30a5742ce7db1b0a871928f64bd176cf9ab3b64`、記事本文HTMLのMIMEパート1,250,747バイト／SHA256 `0c6c2670f715b06e3a9596cf848df9e08bb5b5168d5dd57113730d3d50b8fc52`**。書誌・記事の一次URLは `https://www.sciencedirect.com/science/article/pii/S0010027724002531`。PubMed PMID 39368350の電子公刊2024-10-04／2025年1月掲載も照合。これらは**ユーザーが実際に持参した出版社ページスナップショットの完全性検査**であり、Elsevierの独立物理HTTP200の原応答同一性や公式PDF原本のSHAを証明しない。著作権のあるMHTや図を公開Gitへ一切コミットしない。

**実行した新しい媒体の全範囲確認：**
- Abstract、本文Introduction・Task/Data・Models（2.3.1～2.3.5）・Results（3.1/3.2.1/3.2.2）・Discussion・Conclusions、同一ページ内のAppendix A（A.1/A.2.1/A.2.2）、Appendix B、公開データ／コード案内を具体的に読んだ。必要な記事内**17節アンカーが17/17**存在。
- 元記事が掲載する**本文図Fig1–7の7点、付録図FigB.1–B.8の8点、印刷Algorithm1/2の2点、計17点**をMHT内の個別JPEG署名・復号・画像SHA256・サイズまで抽出した。**原MHT中に実際に埋め込まれた全17画像**を4組のcontact sheetで人間が画像表示し、各図の主要な情報、逆向き優位性の条件、負例等のレイアウトを照合した。17点の個別source-media SHAと寸法は隣接の機械台帳に記載。
- 主文の表1（試験条件別meta-action維持数）とAppendix表A.2（実験別・条件別・群別人数）も確認。主要MethodsのMathJax数式記号19/8/9/2（2.3.1/2.3.2/2.3.3/2.3.4）や原Algorithm図の印刷行から中心更新則を照合。**MHTが埋め込んだfigure画像はブラウザの小さなjpg表示版であり、`_lrg.jpg`リンク先の全高解像ファイルはMHT内に存在しない**。全図元ピクセル・すべてのパネル内の小文字の高解像照合や原著の全数値再実行を完了したとは扱わない。
- **実物検査10/10 PASS**：元MHT/HTML固定SHA、17節アンカー、元記事17図アルゴリズムの媒体ID・JPEG署名とdecode、2Algorithmと主7＋付録8、主要数式存在、群人数算術・原著印字75%との不一致検出。10件は出典構造・数値転記検査であって実証的なモデルfit再現テストではない。

## 統合モデルの原著内容／比較実証範囲

- **元研究**は1026人、12ブロック2段階4アクションを含み、事前設計済み7種の試験ブロック組合せV1/V2/V3を比較。Experiment 1はV1/V3、Experiment 2はV1/V2を試し、共有V1-V1を比較後、結果を一部統合した。運用上はtraining phaseからの階層方策表現とtestにおける転移・再合成を、主としてステージ2で検査する。
- **Algorithm1（§2.3.1）**：Xia & Collins 2021の既存階層アルゴリズムからoption表現をstate-action task-set value tableへ置換し、CRPによる新旧task-setのprior、同一blockのcontext pairing、Bayes belief更新、選択済み行動のWM mask、予測誤差を用いたvalue更新を用いる。**直接の先行モデルが存在する**。本原著がCRP・階層方策・softmaxすべてを初発明したとは判定しない。
- **Algorithm2（§2.3.2）**：圧縮ステージ1・圧縮ステージ2・完全階層3種のpolicy mixture。task-set事後確率とは**別の**policy-class beliefをBayes更新しsoftmax重みと忘却率で表現する。圧縮方策は別個の独立Qテーブルをオンライン学習するわけではなく**その時点の階層policyから計算するoff-policy**であることが重要。
- **§2.3.3前向き／後ろ向き**：同じ構成要素とパラメータ数の比較において、前向きはstage1がcontext・stage2がstate、後ろ向きはstage2がcontext・stage1がstate。stage2の試験後にstage1記憶を参照することが、Fig5/6の一部で学習済みchunkの再組合せに適する。
- **研究用尤度の唯一の計算仕様**：著者の指示に従い2024-09-11 [出版前 `modeling.py` 固定コミット](https://github.com/jl3676/learning_hierarchy/blob/5f0832edb0a9342a9c6100a05a345e3bac063963/modeling.py)（blob SHA `97104ec77c324654883cd96518d93e6304edb875`）の「`softmax(beta*TS_Q)`→各task-set選択確率をcontext beliefで周辺化→epsilon/4→必要な3方策混合→観測選択負対数尤度」。出版社の例示的§2.3.4印刷式との差は原著の負例注記として残し、勝手に原文を訂正しない。

## 図を含め実際に検査した重要な反証・適用境界

1. **被験者群**：random181・mid254・best591は**合計1026**。random181は本論文の後続モデル分析から除外。best群591を主本文に、mid群254をAppendix FigB.1/B.2に配置。k=3は教師なしPCA後の**解釈可能性に基づく選択**で、k=2/4とPC3/4感度は付録で示すが、参加者全員の同一効果の証明ではない。
2. **本原著内の新しい算術上の不整合を明示**：Discussion末尾は「**75% of all participants including top and mid performers**」と印字。しかしFig3BとAppendix A.2.1の人数は**591+254=845／1026=82.359%**であり、75%とは一致しない。著者が75%で指している別の未記載選択条件があり得るため**publisher typoを断言せず`UNDERDETERMINED_DESCRIPTIVE_DENOMINATOR`**。全モデル結果を無効とはせず、75%の一般化記述を独立の強い証拠として使わない。
3. **転移結果の境界**：V3とV1の第1試験ブロック差は全体t2.1/p=.037だが、別実験に分けるとExperiment1のV1標本はp=.32、Experiment2はp=.013。V3対V2はp=.078で非有意、V1対V2はp=.78。Fig3は全状態抽象での因果的優位を支持しない。
4. **代替モデル**：Fig4とB.6/B.7/B.8では完全階層だけ・2種類の圧縮方策だけ・Bayes更新なしでfixed policy-priorsの混合だけでは、最初の圧縮誤りの推移を適切に説明できない。Meta modelのAIC優位(t=24、p<1e-4)と個人レベルerror回復の差は**モデル比較の範囲に限定**。独立的な生物神経因果機序の証明に広げない。
5. **元データの予測強度**：Fig5はV3含有の3条件で後ろ向きに当てはまり優位、Fig6はV1/V2の混合転移で一部優位。ただし**Fig7の反復V1-V1/V2-V2では前向きと後ろ向きの有意差なし**、mid群FigB.2もV3-V1等で未確認の条件がある。FigB.6Bは忘却γ、学習率ηと階層prior p_Hの一部範囲で回復が弱い。
6. **サンプルと設計**：実験参加者は単一大学プログラムからの募集。別実験バッチは統合前にV1-V1で検査しているが、V3の実験バッチ固有効果を全て独立に排除したとは言えない。本研究のstage1 policy学習は独立にモデル化しておらず、既知決定論的feedback・2段階4択の課題外の無制限な人間階層推論・一般目的計画へ主張を延長しない。
7. **出版版**：単独元出版社完全HTMLを研究用主資料とする運用は#399と整合。ただし完全なElsevier版の独立HTTPバイト同一性、元PDF全ページ・リンク先高解像図群、publisher correction registryの完全照合は未証明。外部の訂正専用検索に本DOIの明白な訂正は発見できなかったが、検索陰性を正式訂正不存在の証明とはしない。

## 紙面モデル家系：実施した4組と認定の射程

- **Xia & Collins 2021**：INT01自身が明示する**直接の既存階層task-set/option系統**。これは引用だけでなくAlgorithm1の説明に明記される、**直接祖先エッジとして確定**。
- **INT12 Franklin & Frank 2018**：非パラメトリック潜在階層は共有するが、INT12はreward関数とtransition関数の別々／共同クラスタおよびその選択、INT01はcontext別action-value task-setとstage抽象policy-class Bayes arbitration。初出の構成数理を二重カウントせず、**当該2本の中心演算が同一であるとする根拠なし（局所的非同一）**。全歴史的直接派生／数理同型の不存在は未認定。
- **INT14 Tomov et al 2020**：共通CRPは既成prior。INT14は**環境グラフ状態分割H、タスク・報酬依存posteriorの推論、階層BFS計画**で、INT01の**stage別policy chunk・3方策meta-learning**とは異なる。INT01はTomov2020を階層研究の背景文献として引用する。共通CRPのみを理由とする同一扱いはしない。限定比較は明確だが歴史的全系列独立の最終認定なし。
- **G1 P12 Lieder et al 2018**：正式G1候補の [PLOS原著](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006043) で確認。G1 P12 Learned Value of Controlは**刺激・課題特徴から制御信号の選択や強度の価値をmeta-RLで学習**。INT01は**文脈ごとの圧縮階層policy chunkの構造と選択重み、後ろ向き再合成**。RLや制御選択という単語一致では重複認定せず、演算対象の相違を局所的に記録。G1 P12の出版版選択・科学資格と全G1モデル家系を本レーンで改変しない。

**残る巨大な問題**：INT01と残り13選定INT（比較済み12/14は局所限定のみ）、G1候補20件の全中心系譜をこの4比較で既に証明したふりはしない。G1最新#418は個別20/20原著証拠統合済みでも、全体コホートには出版媒体多様性・P10変種・族譜などの保留がある。

## 研究出典と最終判定を分ける

現段階の **`INT01_SOURCE_FULL_EMBEDDED_MHT_REVIEW_EXECUTED_WITH_NEW_ADVERSE_FINDING`** は実質的な科学審査の前進である。**無条件の原著全文科学資格**には、私人保存MHTの後続レビュアー管理アクセス保証、独立出版社最終訂正・版史の確認、必要な図元高解像精査・主要パネル、本文「75%」の具体的な原著意味の解決／除外範囲明記などの適切な停止条件を残す。これは著者のsoftmax採用を取り消すものではない。

**正式な G2-D全16件の完成／全INT・G1系譜独立／バックアップ採用／MAIN実行認可は全て未達。G2-D PARTIAL、MAIN_NOT_AUTHORIZED。** 機械台帳：`G2D_V18_INT01_FULL_PRIVATE_PUBLISHER_HTML_SOURCE_SCIENCE_AND_TARGETED_FAMILY_AUDIT.json`。
