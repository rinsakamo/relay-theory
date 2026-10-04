# G2-D v4：B3原著の反証条件、INT03×INT06の原著中心系譜、INT13版状態（2026-10-04）

これは **INT独立PR #430専用／既存記録に対する追加資料**。出発G2 HEAD `69748673c80f421605f1c63607472903ac2ed68c`、G1独立各レーン未統合。既存G2/MAIN/G1の共有成果・採用リスト・別レーン予約は変更しない。以下は出版社の公開済み原著と一次公開査読の**source-native bounded examination**。MAINの構造分解・Grammar・再構築・H0/H1/H2・予備MAIN結果閲覧なし。正式バックアップ採用なし。

## 1. INT-B3（10.7554/eLife.57244）：ソース版・統合指標・査読公開の不利な再現性

刊行元eLifeの正式 **Version of Record 2021-03-16** を使用（accepted manuscript 2021-03-02をVORと取り違えない）。既存G2-D独立実取得 **35-page publisher VOR v2** raw SHA-256 `9e13535592ff1cf36c9eb4a9a1daae23cb6dfa8a916a40586a6cc5c651b80d35`、再取得の4バックアップ原本完全一致 CI `37196750620` と既存ページ索引を継承。出版社原著 https://elifesciences.org/articles/57244 、一次公式図 https://elifesciences.org/articles/57244/figures 、一次公開査読と著者応答 https://elifesciences.org/articles/57244/peer-reviews を別ソースとして突合。

**実際の方法と追加指標：** 6 PFC領域＋4 PPC領域のfMRI directed effective connectivityの基礎生成モデルは既発表spDCM（Friston 2014、Razi 2015/17）、SPM12/DCM12.5実装。spDCMはcross-spectral densityから**時間不変**結合を推定する。PPI（既存Friston 1997等）を別途使い、文脈制御要求による**時間変化**のconnectivity modulationを調べる。静的および動的な**integration indices**は文脈制御ネットワークについて**between-network−within-network**の方向付き差分を取り、他制御ネットワーク指標およびhead motionを残差化した論文固有の分析構成。2つの独立標本間で2-fold out-of-sample ridge regressionを行い、認知課題群の主成分と比較する。従って指標は研究固有の推定対象・説明量だが、**新しいspDCM/PPI生成アルゴリズムではない**。新しい独立の内生的cognitive-control computationが論文に導入されたと断定禁止。

**N_B3_001（査読必須負例）**：主解析の8 mm平滑化ではstatic＋dynamic integrationの複合で認知能力予測`r=0.32`。正式論文および公開査読上、4 mmへ削減するとstatic integrationと認知能力との相関が`r=-0.04`（旧`-0.22`から消失）、dynamicとの単独相関は`r=0.26`（旧`0.23`）程度で存続するものの、**両統合指数のjoint out-of-sample ability predictionは`r=0.03, p=0.44`、再現せず**（Fig8—figure supplement2）。「両統合指数は前処理非依存に認知能力を予測する」と書いてはならない。対してactivation指標は4 mmでも`r=0.31, p=0.04`、統合指数への追加は`r=0.32, p=0.03`、nested F(4,42)=3.05,`p=0.04`。この相違を隠して「完全再現」と呼ばない。

**N_B3_002（有利な存続も保持）**：TMS個人差の予測は主8 mm解析で`r=0.56, p=0.01`、4 mm感度解析でも維持。認知能力・activationを制御後のTMS予測`r=0.47,p=0.02`も報告され4 mm存続。上記N_B3_001を理由に**すべての結合結果/TMS結果が非再現**と誤分類禁止。

**N_B3_003（推論構造）**：PLOS/PNAS等のモデルとは異なり、fMRI上の正負のeffective connectivityの符号は細胞レベルの興奮・抑制を直接証明しない。未モデル化の領域CによるA→Bの媒介あり得る。公開査読自体もpositive=integrationの唯一解釈ではなく、biasing/modulationでも説明できる点を指摘。視覚的連結性の記述を**独立の新規情報統合計算式**として扱わない。

**N_B3_004（domain限定）**：TMSのdomain-general compositeは説明できたが、domain-specific composite`r=0.03,p>0.3`は説明できない。一般能力・全刺激領域に横断する同一高次統合原理まで外挿不可。

**暫定判定**：`SOURCE_NATIVE_B3_EXISTING_GENERATIVE_FAMILY_WITH_NEW_ANALYTIC_COMPOSITES_CONFIRMED`。出版社VORのoriginal modelとして統合network patternは実際に存在する。ただし**algorithmic central noveltyは未証明**、CTL-B1と同一DOIの重複予約未解決、eLife版の全補足全図pixel審査・全40＋G1系譜比較未終了。**HOLD・採用0**。

## 2. 既存選定INT-03（PNAS1998）とINT-06（PLOS2010）の中心系譜：名称だけで重複させない

INT-03：PNAS原著 DOI `10.1073/pnas.95.24.14529`、著者 Dehaene/Kerszberg/Changeux 1998、「A neuronal model of a global workspace in effortful cognitive tasks」。出版社の完全HTMLはG2既存ブラウザでfirst-party候補確認済み、ただし**正式PDF原本raw SHA未保存**。補助的全文対照は公的PMC `PMC24407`（出版社の公式資料と別物のため、単独で原著の完全文責に昇格させない）。モデル中核：長距離再帰接続を持つ分散workspace neuronによる複数の局所専門processorのアクセス調停；課題・報酬条件によるtop-down選択的動員・抑制。Stroop課題simulationのeffortful task activationを主例とする。

INT-06：PLOS正式公開原著 DOI `10.1371/journal.pcbi.1000765`、Zylberberg et al 2010、**DehaeneがINT-03と重複著者**で全く無関係な発明系譜とするのは不適切。G2で実取得済み正式PDF SHA `c276294fa7a111e5df98f35aa0da933af28d45a1e1347940a1b57753c0980706`（PLOS出版社原著本文 https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000765 ）。source-nativeの追加中核：感覚並列処理／刺激保持と分離して、課題選択task-settingのNMDA再帰電流でspiking-neuron routerをゲートし、ルータに流入する感覚統合が閾値到達後にmotor反応へ変換され、反応後feedback inhibitory resetで次課題を開放する**具体的実装**。二重課題PRPの短SOA下で感覚側の並列維持とrouter側の直列ボトルネックを同時に予測する。

**N_INT03_INT06_001**：共通の長距離相互接続・top-down制御＋Dehaene著者重複を認めた上で、1998年のeffortful Stroop workspaceと2010年のNMDA-controlled **task-specific routing, task order network, response inhibition, dual-task timing**には機構の明示的差分あり。「同じworkspace／routing語だから同一モデル」とも「2010年は完全に独立した大域的理論」とも認定しない。仮ラベル `SHARED_BROAD_WORKSPACE_ANCESTRY_DISTINCT_ROUTER_IMPLEMENTATION_CANDIDATE`（**global full model-family independence UNRESOLVED**）。

**N_INT03_INT06_002**：2010年原著は単純な各感覚／反応の小集団だけを実装。著者自ら無限に近いtask repertoireを有限神経集団に符号化する方法を検証していないと明記。PRPとattentional blinkのnetwork simulationは実際の霊長類の直接単細胞実証ではない。2010年原著Text S1の追加数学・supplement全数図とPNAS1998の全数学を揃えた独立照合は未完。並列作業のv3補助物取得は**完了CIと実原本SHAの確認後**だけ新たな取得証拠として繰り入れる。

## 3. INT-13（10.1371/journal.pcbi.1014796）正式出版状態の再確認

PLOS公式first-partyライブ本文 https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014796 を2026-10-04再確認。公開日2026-09-30、**publisher自身の`This is an uncorrected proof.`表記が現在も存続**。先行G2-D original PDF/HTML SHA一致は未校正版の同一性証拠であり「校正完了」ではない。既存RLWMとPADDL（joint choice+RT＋load-dependent threshold）との独創差分の暫定出典解釈は可能だが、**最終出版版の式や図の同一性を無断推定禁止**。INT-B4との比較も最終版未確認の限界を保つ。

## 検証状況と停止条件

既存G2 PR #419 HEAD `69748673c80f421605f1c63607472903ac2ed68c`；G1 PR #418 HEAD `38c5eb24c61b9e57371084a65fcbcb9fb9c62a4b`；G1-W2 PR #427 HEAD `10ed5122488bea2c94bc1e40213e381b591db367`を当時照合。G1-W2 eLife.39497代替は依然予約解放なしなのでINT-B2予約も不変。今回の追加は**新しい原著source-native有力反証の特定／系譜の明示的差分診断**であり、対象原著全数式・全正式補足・全再版の完全意味資格には昇格しない。INT-01原著未取得、INT-13最終版未検証、G1最終20とG2 40の独立系譜未凍結、正式バックアップ採用0、MAIN_NOT_AUTHORIZED。
