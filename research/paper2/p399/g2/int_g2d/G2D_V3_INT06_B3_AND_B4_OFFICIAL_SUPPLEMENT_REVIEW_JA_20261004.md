# G2-D v3：選定INT06×INT03系譜・B3不利な標本結果・B4正式S1原著を実際に追加確認（2026-10-04 JST）

## Scope and exact provenance

G2起点HEADは `69748673c80f421605f1c63607472903ac2ed68c` で不変。INT独立draft PR #430へのappend-only追補であり、旧G2-D B4主本文数式・図監査／INT01失敗／INT13 proof判定は維持する。**MAIN Grammar対応・再構築、H分類、プレビュー・MAIN科学結果閲覧はゼロ、正式バックアップ採用ゼロ。** 下記は原著の source-native taxonomy・新規数理の由来・反例を区別した限定科学監査。初回リダイレクト検証失敗も保全し、CI PASSは論文の科学内容の真理を証明するものではない。

今回実際に走らせた[独立GitHub Actions 37198446072](https://github.com/rinsakamo/relay-theory/actions/runs/37198446072)は当該workflow HEAD `94a1d1e6ed01329508c3c7053845ef51c63bbe30` で出版社始点限定の4/4物理取得・SHA/形式の監査を実証。配信はPLOS公式記事URLからPLOS公式署名発行主体`wombat-sa@plos-prod.iam.gserviceaccount.com`による`plos-corpus-prod`の論文固有パス（受信URL署名とファイル名一致）だけを認める。Googleの一般ストレージや第三者ホストを承認していない。署名URLの一時トークンは原著の恒久ID・永続レファレンスに用いない。歴史的初回ラン`37198377401`では正規出版社転送を第3者URLと誤判定、`37198431676`では署名バケットファイル名の正規表現ミスでなお失敗。**両方の過去の偽陰性とその原因はそのまま保存**し、再検証でソースの偽造・弱いホスト許可を行わず修正。

| 原著スロット／公式DOI | 検証済み最終媒体 | raw bytes / SHA-256 |
|---|---|---|
| 選定INT-06 `10.1371/journal.pcbi.1000765` | PLOS正式main 23-page PDF、旧G2取得raw SHA完全一致 | 3,127,883 / `c276294fa7a111e5df98f35aa0da933af28d45a1e1347940a1b57753c0980706` |
| 選定INT-06 `10.1371/journal.pcbi.1000765.s007` | PLOS正式 Supporting Notes Text S1 の22,016B原DOC（OLEシグネチャ） | `ceec10ca95ae7bd2207d95c1ddb45098f2dc9741697c3608497dc2efd9b33bb5` |
| 選定INT-06 `10.1371/journal.pcbi.1000765.s008` | PLOS正式 Table S1 ANOVA原DOC（OLE） | 31,744 / `0813b44b5770f03b833a0623da876a76dde6e2ee5cd8dcbaf5ec8257fa04b504` |
| 待機INT-B4 `10.1371/journal.pcbi.1012872.s001` | PLOS正式 S1 Text補足11-page PDF | 1,627,464 / `64f1e1f18bb51909e89b22112929125914ccff75c2ffd1c91ace4851ae091e88` |

### INT-B4：補足本文から実際に新規審査した反証と頑健性

S1本文正式原典（出版社公式 DOI `10.1371/journal.pcbi.1012872.s001`、11頁）を全文テキスト索引、出版社PDF本文テキストと出典照合。元v2aで**未資格としていた原典S1の物理取得を新規成立**。全A–Gの図captionのページ候補位置：Fig A=p1、B=p2、C=p3、D=p4、E=p5（本文再言及p8）、F=p6、G=p7。p8–11は補足統計とモデル比較・反証。以下はキャプションと補足本文**source native textual adjudication**であり、PDF全11頁各画像ピクセルを人間が視認したとの記録ではない。

- Fig C：採用M5のparametric recovery、および特に有意なRL learning rate／WM decayの復元。図の生データ再計算は未実施、パラメータ全員完璧復元などの表現は禁止。
- Fig D：M2/M4/M5間に加えてRL-onlyとも比較するmodel recovery。原著のシミュレーションは1生成モデル当たり`N=492`であり、BICでは複雑な生成機構を単純モデルに誤分類しがちな**原著の不利な証拠**が明記。AICによる主モデル採用とBIC結果の不利条件を必ず併記する。
- Fig E／補足p8：追加choice kernel M6はM5に対しAIC改善なし。元M5の2主要効果のM6への感度検査は有意差なし（RL rate U=13796,p=0.686、WM decay U=13669,p=0.797）。追加habit-like perseverationを全被験者に必須の成分としてモデル化する根拠にならない。
- 補足p8–9：少数パラメータのM4でも身体的不安MASQ AAに対するRL学習率の低下 `rho=-0.270,FWE p=0.004` とWM decay増加 `rho=0.245,FWE p=0.001` を報告。探索的BIC/他モデル選択の有利不利はモデル識別性の限界であり、M5 split-rho gateがこれらの効果そのものに絶対必須という主張は誤り。
- 補足p9–11：主被験者除外基準の分布、反応時間のset-size効果、および認知的不安PSWQの主効果・交互作用が認められない結果が明記。単一set-sizeの未補正p値が出ても全体のPSWQ主効果へ昇格しない。補足の抑うつ尺度は探索・非有意という限界を守る。

**B4残存致命的な原著上の不確定性**：主本文Eq(15a,b)の`ns=K`における明記欠落はS1の補足テキストによって自動修正されない。ここで印刷数理を恣意的に連続補間しない。公開解析コードの正確な同値枝が取得・版凍結されない限り`PUBLISHED_EQ15_EQUALITY_GAP_OPEN`。補足文面の科学的読解は前進したが、**全11頁の図画素・全出版訂正履歴・全G1/G2親族独立性の全面資格は未成立**。

### INT-B3：正式eLife 2021-03-16 VORとネガティブ結果・実際の演算

正式eLife DOI `10.7554/eLife.57244`、35頁公開publisher VOR原PDF旧取得＋再索引固定SHA `9e13535592ff1cf36c9eb4a9a1daae23cb6dfa8a916a40586a6cc5c651b80d35`。公式完全テキスト `https://elifesciences.org/articles/57244`、全Figure/Source data `https://elifesciences.org/articles/57244/figures`。eLifeの研究・公開peer reviewとAppendix1の科学的留保を参照。中心主張は6PFC＋4PPCの**先行元データに基づく新しいネットワークレベルの空間的勾配、静的・動的統合の経験的識別**であり、新しい自作spDCMアルゴリズムを新規定義した論文ではない。既存Friston/Razi spDCM（SPM12/DCM12.5）を10領域静的状態推定に採用、Cole/Friston流PPIを拡張して動的相互作用を検討。PPI原著回帰式は`Y_target=B_conn*Y_source+B_uni*X+B_dep[(bin(X)*C).*Y_source]`のsource-native predictor interactions。spDCMは主本文で**時不変**、PPIが時変を補助する。2016/2017のNee & D'Espositoは同一元データPFC限定classic DCMで**直接の著者先行系譜**。経験的な新しい全前頭頭頂の有効結合トポロジーは先行アルゴリズムの再利用と区別し、「全て過去データと同一結果」とも「独自の新規学習モデル」とも誤記しない。

**重大な原著不利条件をsource native追加審査**：
- PPIの独立2標本の一致度：baseline context-independent r=0.86、temporal control r=0.32（弱い）、contextual control r=0.78、stimulus domain r=0.88。**sensory-motor PPI r=-0.06で再現なし**。元のsensory-motor効果の検証に刺激領域刺激ドメインのPPIをproxy代用しており、同一の観測・同一の実験操作と認定しない。contextual control×stimulus domain interactionも再現不足で後続モデル分析から除外。
- Fig6静的spDCMの有効結合はsource/target abstraction の交互作用が両標本で正、有効結合のsource abstraction二次効果は両標本で負（mid-level integrationピーク）という**回帰の経験的パターン**。静的符号のpositive/negativeを細胞レベルの個別興奮/抑制神経活動と同一視禁止。媒介している未選択第三領域の存在を排除できない。
- 減弱smoothingの代替pipelineでは重要な**network integration → cognitive abilityの予測結果が再現しない**とDiscussionが明記。他の多数の神経学的パターンが再現したことは、この予測結果の弱さを打ち消す証拠ではない。少数標本のtrait相関やneuromodulation予測の効果量は過大になりうるため大きな独立標本での再現が必要。
- 空間勾配の見かけの連続性はデータ集団平均/平滑化の帰結かもしれず、神経領域の離散区分との優劣を同論文は確定していない。

**中心数理分類**：`EMPIRICAL_CONNECTIVITY_TOPOLOGY_NEW_RELATIVE_TO_2016_2017` と `INHERITED_SPECTRAL_DCM_PLUS_PPI_ALGORITHM` を同時保存。「新しい独立計算ルールの初出」を要件とするback-up qualificationなら、本論文を新規独立モデルアルゴリズムとして昇格させる証拠は未提示。逆に「既成生成モデルで独立した科学的ネットワーク配置を推定」なら新規経験的結果を認められるため、採用可否は凍結適格性規則との照合が必要。他レーンCTL-B1と完全同一DOI、最終G1×MAINにも未照合、**INT-B3 HOLD/NOT_ACTIVATED**。

### 選定INT-06 ↔ 選定INT-03：元の思想と実装差を分離

INT-03 `10.1073/pnas.95.24.14529`、1998 Dehaene/Kerszberg/ChangeuxのPNA​S global workspace原典、公式完全HTMLブラウザ閲覧は元G2の引継ぎ判定のみ（今回raw媒体新規取得なし）。元モデルは長距離結合を有するglobal workspace細胞群と専用perceptual/motor/memory/evaluative/attention processorの分離・選択的動員、Stroop課題のモデルシミュレーション。INT-06 `10.1371/journal.pcbi.1000765`、2010 Zylberberg et al. PLOS公式23頁full original SHA上表。**同じglobal workplace思想をDehaene共著で明示的に継承**しているため「名称が同じだけの無関係」を否定する。他方、2010は具体的に二感覚モダリティ階層、task-settingの自己維持と相互抑制、router内での stochastic sensory evidence の蓄積、T1終了時抑制解除→T2へ回路切替、PRP二重課題平均RT／RT分布とattention blinkでのT2失敗条件（mask/decay）を明示的に構築。1998 Stroop workspace動員と**完全な同一モデル式・同一実験**との断定も避ける。抽象中心思想を直接継承するがspiking router回路の実装差は実際に追加された。

INT06原著の不利な事実：被験者の神経活動を直接計測してdual-task因果局在を証明したものではなく、条件付きシミュレーションからの予測。競合刺激の有無・短SOA・maskの操作に依存する結果を、すべての複数課題の普遍的制約とは主張しない。正式Supporting Notes S7とANOVA Table S8の**物理原本**は上記runで得たが、原DOCの数式本文と全図（S1–S6 TIF等）の完全視覚監査は未了。だから今回`INT06_RAW_MAIN_AND_TWO_CRITICAL_DOC_SOURCE_GATES_CLOSED`のみ新設、`INT06_COMPLETE_SOURCE_SCIENCE_QUALIFIED`は依然false。INT03/06両方を維持できるかは残存全数学親族審査で未定、名義の同一性だけで除外・独自実装だけで独立認定はしない。

## 総合的に残す停止条件

- **物理取得の新規成果**：選定INT06正式main旧SHA再現＋新規2原著DOC SHA固定、待機B4正式S1原著11頁SHAとA–G図のテキスト索引成立。v3全4媒体原典数・モデルの科学合格数は別の分母。
- **科学的新規性分類の成果**：B3は新しいFPCN結果を得たが既存DCM/PPIの新規アルゴリズムと誤認しない。INT03/INT06は思想継承とspiking-router実装の両方を記録。B4の本文主7図に対し別S1 7図のサポート本文の有利・不利・モデル回復を追加し、未検証のS1図画素と印刷同値境界は未合格。
- **保持する停止**：INT01 Elsevier真正媒体依然未取得、INT13 publisher 2026-10-04未校正版、B1 INT12重複のため条件付きBLOCK、B2 G1代替の予約中、B3/B4中心モデル家系未解決、他12件の全数式・全図と全G1×G2系譜未了。G2 working40変更なし／正式バックアップ採用0／MAIN_NOT_AUTHORIZED。
