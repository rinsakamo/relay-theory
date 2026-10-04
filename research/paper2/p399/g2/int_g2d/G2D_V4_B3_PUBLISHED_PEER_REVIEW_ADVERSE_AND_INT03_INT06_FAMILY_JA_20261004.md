# G2-D v4：eLife INT-B3最終原著＋公開査読の反証監査、および選定INT03×INT06の直接系譜スクリーニング
Date: 2026-10-04 JST

**権限と境界**：G2 Issue #399、凍結G2 HEAD `69748673c80f421605f1c63607472903ac2ed68c`、INT独立Draft PR #430。既存凍結INT01–16 DOI、補欠順位B1>B2>B3>B4、G1 P12予約、Grammar v0を変更しない。他G2レーン／共有MAIN40／G1／G3／G4ファイルへ書き込まない。MAIN論文の科学的構造分解、再構築、H0/H1/H2、preview結果の閲覧なし。本書は**出版社原著＋正式公開査読に依拠する限定原著科学増分**であり、新しい正式バックアップ採用・全原著認定ではない。

## 1. INT-B3 eLife 57244：旧分析が新処理条件で崩れる公開査読根拠

原著：Derek Evan Nee (2021), *Integrative frontal-parietal dynamics supporting cognitive control*, DOI `10.7554/eLife.57244`。**正式VOR 2021-03-16**、正式出版PDF v2 raw SHA `9e13535592ff1cf36c9eb4a9a1daae23cb6dfa8a916a40586a6cc5c651b80d35` / 35pp、前段独立実取得済み。

**原著VOR**：https://elifesciences.org/articles/57244 ; 正式独立資料**公開editor decision＋author response**：https://elifesciences.org/articles/57244/peer-reviews ; **著者オリジナル図＋正式補図**：https://elifesciences.org/articles/57244/figures 。

### 実際に元論文が用いた学習/神経モデルは何か

- **spectral DCMは既存**：SPM12 / DCM12.5、Friston (2014), Razi (2015, 2017)に基づくBOLD cross-spectral densityの生成モデル逆推定。研究対象は**前頭6＋頭頂4領域**。先行Nee & D'Esposito 2016/2017では前頭6領域をclassic time-series DCMで分析済み。新しいモデル本体は論文自身が実装したspDCMではなく、**既存モデルを別領域集合で再推定**する研究設計。
- **dynamic PPIも先行分析変種**：Friston 1997およびCole 2013を明示し、task-contrast×source-region time-seriesを対象領域信号に回帰する線形モデル。新規の介入可能なRL/WM/制御変換規則ではない。
- **本論文独自の実証・二次指標**：source/target別静的effective connectivity、課題依存PPI変調、**between-network minus within-network integration index**、他ネットワークindexとhead motionを回帰で除去した残差指標、cross-sample ridge predictionを使って中央領域の横断的役割を調べる。これは有意義な**network application/contrast construction**であって、そのまま**新規の独立した力学的生成モデル**とは判定できない。静的接続＋PPIを独自の新しい一体的微分方程式や状態推定アルゴリズムへすり替えない。
- **二系列のreliability差**：原著はcontext-independent effective connectivity r=0.86、temporal-control PPI r=0.32、contextual-control PPI r=0.78と報告する一方、sensory-motor control PPIおよびcontextual-control × stimulus-domain PPIはサンプル間の再現性不十分で後続推論から除外した。表示の有向相互作用に一部**uncorrected p<.05**の可視化もあるため、全ての線をfamily-wiseで実証された個別接続として昇格禁止。
- **新しい中心的否定的証拠 N_B3_V4_001**：当初8mm volumetric smoothingでstatic + dynamic integrationから認知能力をcross-validated ridge予測（r=0.32）。公開査読者の過剰な空間平滑化指摘で**4mmへ再解析**したところ、static integrationとの関係はr=-0.04へ消失し、**統合指標2つの認知能力予測はr=0.03, p=0.44で不再現**。対して活性化ベース指標はr=0.31,p=0.04で予測継続。4mmでは動的統合と能力の正の単独相関は残ったが、**統合予測の交差検証成功を最終VORの一般ロバスト知見として語れない**。この不利条件は受理済み最終原著とeditor-replyの両方に記録済み。抽象の「integrative dynamics predict higher cognitive ability」は4mm反証で必ず限定解釈。
- **N_B3_V4_002**：静的spDCMはtime-invariant有向接続、PPIはcondition-dependent変調の関連であり、細胞単位の興奮/抑制の直接証明や未観測領域を除いた因果同定でない。抑制的解釈はlatent-state inferenceに依存。
- **N_B3_V4_003**：前回指摘したshared-DOI G2 CTL-B1と予約解放手続が未解決。新モデル独立性の証拠にも選定権限にもならない。

**源流に関する結論**：本文・査読が直接証明するのは**旧DCM＋PPIを再配置し、ネットワーク間統合を定量化した新規分析・新しい検証仮説**。既存Friston/Razi/Coleのモデルと区別される新しい独立の中心**generative cognitive integration algorithm**は本原著から未確認。学術的価値を否定するのでなく、G2の「一意の中心モデル系譜」条件へ「network-scoped secondary index」を無根拠昇格させない。現時点**INT-B3 SOURCE_LOCAL_NEW_GENERATIVE_FAMILY_NOT_DEMONSTRATED／FORMAL_RESERVED_HOLD**を維持。G2 CTL-B1担当との優先権調停・全MAIN科学選定なしにB3を独断採用・最終不適格認定しない。

## 2. 選定INT03（1998）×INT06（2010）：共有概念と独立実装の境界

- **INT03：1998 PNAS正式出版原著** DOI `10.1073/pnas.95.24.14529`, Dehaene/Kerszberg/Changeux。元論文の有用な出版一致NLM全文アーカイブ https://pmc.ncbi.nlm.nih.gov/articles/PMC24407/ は1998 PNAS掲載版（独立出版社書誌にも一致）。ただし現在のPNAS自社ページ https://www.pnas.org/doi/10.1073/pnas.95.24.14529 はブラウザcookie/challengeで単独再実取得不可。**NLM正式アーカイブや大学PDFを凍結G2で記録されたPNAS出版社完全HTMLのraw原著媒体に無断置換せず、今回INT03の物理新取得を主張しない**。原著の理論二空間：分散specialized parallel processors＋long-range globally connected workspace、指令下でtop-downに処理を選択/抑制、vigilance/報酬の影響、主実験はStroop。原著の最小モデルではexc/inhibユニット、sigmoid型gateなどを用いる。
- **INT06：2010 PLOS出版社VOR** DOI `10.1371/journal.pcbi.1000765`, Zylberberg/Fernández Slezak/Roelfsema/Dehaene/Sigman。全文 https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000765 。**2010の新しい中心設計**は約20,000個のspiking neuron/約46M synapseへ規模を拡張し、task-settingの相互抑制で1つのrouterを選択、sensory→motorのtask conditional routing、局所sensory bufferのNMDA維持、response-triggered inhibitory resetでresponse perseverationを防ぎ、PRP/attentional-blinkのSOA-RT分布/神経予測を再現する。**具体的タスクとメカニズムの新規実装はINT03のStroop/minimal workspaceと同一とは断定できない**。
- **INT06自身が明示した継承**：既存のsensory perceptual attractor、蓄積閾値（Wang/Basal ganglia Lo & Wang 2006）、既存task-rule top-down control、sensory-to-motor routing (Fusi 2007, Salinas 2004, Deco/Rolls、SAIM)等の複合**integration of existing constructs**という自己説明。2010文献一覧に著者が重複するだけで**1998年INT03の全数理をそのまま直接コピーした証拠とはならない**。1997年Dehaene/Changeuxや2003年Dehaene/Sergent/Changeux、および2009年の同著者sensory-buffer等、**中間系譜を独立に開示**。2010の新しいserial resource bottleneck条件・スパイキング実装を全て旧1998に還元するのも誤り。
- **INT06原著の不利な限界 N_INT06_V4_001**：主実験は**刺激2・反応2**と2つの感覚モダリティを固定し、routerの刺激×反応の各組合せに個別の神経集団を割り当てた。任意多数のmappingでは**combinatorial explosion**が生じるため、本文自身が別途**combinatorial/distributed router仮案を正式Fig S6に留める**。abstractの“arbitrarily large possible tasks”は現在の元モデルで任意規模を達成したことの証明ではない。
- **N_INT06_V4_002**：PRP/AB再現はtask-setting競争抑制と局所bufferの対課題機構から生じる**この限定設計のsimulation**であり、ヒト／サルのrouter実神経回路局在や同時記録による因果機構実証ではない。
- **N_INT06_V4_003**：外部公開公式PLOSではSupporting Fig S1–S6, Text S1 (DOC, `...s007`), Table S1 (DOC, `...s008`)を別媒体として配布。独立run [37198446072](https://github.com/rinsakamo/relay-theory/actions/runs/37198446072) で**元2010主PDF 23pp 3,127,883B、SHA c276294fa7a111e5df98f35aa0da933af28d45a1e1347940a1b57753c0980706、Text S1 DOC 22,016B SHA ceec10ca95ae7bd2207d95c1ddb45098f2dc9741697c3608497dc2efd9b33bb5、Table S1 DOC 31,744B SHA 0813b44b5770f03b833a0623da876a76dde6e2ee5cd8dcbaf5ec8257fa04b504**を出版社公式ゲートから取得し署名付きPLOSデリゲート保管URLを実照合。Fig S1–S6自体の画像独立pixel意味審査やDOC表数値全セル監査はまだ未実行。
- **2010正式Fig S2重要な比較**：task-order setting networkを除去しても、response orderをSOAに応じ自発化した条件で**なおPRP曲線が出る**。従って「order-setting自体が必須ボトルネック」という簡略化は元実験に反する。task-setting inhibition / router bottleneck と外側のtask-order unitを分けて扱う。**S1除外負例にも同じ反応固着解除を含む**。

**INT03×INT06の限定系譜判定**：`SHARED_HIGH_LEVEL_GLOBAL_WORKSPACE_CONCEPT; DISTINCT_SCIENTIFIC_TASK_AND_SPIKING_IMPLEMENTATION; DIRECT_SAME_CENTRAL_MATH_NOT_SHOWN; FULL_CENTRAL_INDEPENDENCE_UNDERDETERMINED`。異なる計算実装・対象実験がある点を積極的に認めるが、共有概念＋中間モデルに基づく「family重複」審査は**独立主モデル凍結と分離**。両者を「完全に同一だから片方を除外」も「タスクが違うので独立」とも短絡しない。

## 3. B4 S1公式補足およびINT06 DOCの物理科学段階

別の独立source-native readout [GitHub Actions G2-D v4](https://github.com/rinsakamo/relay-theory/actions/workflows/p399-g2d-v4-int06-b4-native-supplement.yml) が上記INT06公式DOCの元SHAと、B4正式PLOS補足 DOI `10.1371/journal.pcbi.1012872.s001` **11pp/1,627,464B SHA `64f1e1f18bb51909e89b22112929125914ccff75c2ffd1c91ace4851ae091e88`**を実照合し、publisher-delegated公式保管URLを確認。B4 S1 Fig A–G は実際に存在し、Fig C parameter recovery, D model recovery, E choice-kernel robustness, F exploratory testing, G exclusionsを掲載（**テキスト検出・本文と別媒体**）。付録の画像と表の全画素・全セルを独立に目視したものではない。主本文全数式図のv2a限定レビューを付録の全面適格性へ勝手に拡張しない。

**停止**：原著源流レビューと公式媒体取得・限定補助負例という進歩はあるが、共有G1/MAIN40の全数理独立性、全訂正版、INT01正式出版社本文、INT13最終非proofは未完。backup採用0、全MAIN科学監査0、MAIN承認なし。旧v1/v2/v2aと実行結果の不利な失敗履歴は改変禁止。
