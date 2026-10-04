# G2-D v19–v20 総合継続監査 — INT01系譜 3→12/35 と INT09 正式図訂正の発見（2026-10-05 JST）

**本件はMAINのGrammar分解・H0/H1/H2・予備結果閲覧ではなく、#399が要求する原著側の科学的適格性／中心系譜トリアージ。** 凍結済みG2 working40の全slot・DOI、G1 working20、既存全source SHA・全バックアップ順位は不変。INT01は著者指示どおりsoftmax→潜在タスクセット周辺化→探索ノイズ→必要な3方策混合→NLLを研究モデルとして採用済み。

## A. 進捗分母を厳密に固定

旧v18bのINT01外部比較母集団 **35組**＝G2選定INTの他15＋G1現行個別20。旧v18bで原著に即した限定比較3組（INT12・INT14・G1 P12）、**global family最終合格は0**。

- **v19：出版社原著・既存正式原本監査を用いた6組**を追加：G1 PF04、G1 P18、G2 INT04、G2 INT08、G2 INT13、G2 INT15。
- **v20：さらにPLOS独立完全原著から3組**：G2 INT05、G2 INT07、G2 INT09。
- 現在**12/35で「中心演算の限定的な相違」が原著から説明可能**、残り**23組は未実施**。12/35は統計的独立／数理同型不存在／完全な中核家系最終合格ではなく、そのような資格は**0**。正確な35件全DOIを維持したappend-only更新台帳を保存。出版社閲覧ページ以外の既存G2-D個別VOR・G1の原本取得/段階監査はすでにあるものを再利用し、再DLを成功数に二重計上しない。

## B. 単語一致による同一モデル誤認が特に危険な比較

1. **G1 PF04（Dezfouli et al. 2013）**：PLOS原著の階層習慣モデルは、goal-directed systemが2行動のsequence-optionを起動し、その後**open-loop的に**続行・中断する仮説と第2段階RTを主要根拠とする。15人・各270trialを使い、原著自身が並列flat controllerや系列の価値更新方式を一義的排除できないと明記。INT01は潜在task-setの文脈別事後分布・2圧縮＋完全階層の経験依存meta方策と前後stage文脈による新課題合成。階層RL・softmax・optionという広い共通要素は保持し、**習慣系列実行をINT01の新しい同一中心演算とはしない**。全歴史的数理祖先排除ではない。[PF04 PLOS正式原著](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003364)
2. **G2 INT07（Penny et al. 2013）**：同じ「forward/backward」でも、PLOS元論文では**潜在状態空間のGaussian/LL forward filterとbackward inference**による空間ナビゲーション・経路/運動計画であり、INT01の**stage1/2をcontext/stateのどちらに置くかでtask-set転移を説明**する前後方向と数学対象が異なる。Penny原著はオンラインモデル計算であってepisodic recall自体のモデルではなく、local linearizationで多峰性分布が近似できない限界を明示。**語彙一致「前向き・後ろ向き」≠中心同型**。ただしBayesian temporal inference一般の先行数学は双方で利用し得る。[INT07 PLOS正式原著](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003383)
3. **G2 INT13（Bera et al. 2026）**：著者承認の公刊**未校正稿**を本研究の凍結原稿として尊重。中心は既存RLWM方策にRT/choiceのLBAとcollapsed/set-size依存proactive decision boundを組み合わせるモデル。INT01のtask-set階層圧縮meta-choice（研究用softmax尤度）は**RT蓄積過程を推定しない**。既成softmax・WM/RL構成要素が共通でも新しい一体演算は同一と認定しない。INT13の全図式・変種・正規研究版の科学審査は別途必要。[INT13 PLOS第一者完全本文](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014796)
4. **G2 INT08（Lu et al. 2022）**：オンラインのepisodic retrieval LCA（活性化する記憶の競争）、記憶符号化・検索gate、neocortical LSTM/A2Cで未来状態を予測。INT01のBayesian圧縮task-set選択はLSTM hidden state/episodic memoryの検索・符号化gateではない。INT08既存LSTM/A2C/LCAはその論文の独立な全構成発明として扱わず、手動符号化条件の負例も旧v10d保存。eLife公式刊行版v3の第一者本文／図、既存正式43頁PDF SHA実取得監査を使用。[INT08 eLife原著v3](https://elifesciences.org/articles/74445v3)
5. **G2 INT04（Spens & Burgess 2024）**：Nature公式主原著＋補足によるMHN即時保存→海馬replay→VAE学生のschema生成、predictable conceptualとunpredictable sensory residueへの分離。INT01にはreplayによる感覚schema生成はなく、方策の行動選択と転移を扱う。既存MHN/VAE/teacher-studentという部品を著者の単独新規発明としては数えない。前G2-D v9の出版社同一主20頁+補足9頁を再利用。[INT04 Nature原著](https://www.nature.com/articles/s41562-023-01799-z)
6. **G1 P18（Moran et al. 2021）**：モデルベースplannerが自身の将来model-free傾向に合わせて**次の報酬環境を設計**する内省的計画。INT01の課題中latent task-set抽象・3方策meta選択・転移は、自己の未来MF方策の影響を予期した環境報酬設計と違う。P18が神経self-modelを実観測したことにはならない。[G1 P18 PLOS元原著](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008552)
7. **G2 INT15（Lei & Solway 2022）**：MB/MF間のaction/value conflictと非線形DDM的な意思決定cautionを比較。INT01はtask-setの生成・再利用とmeta-policyの選択学習が中心で、DDMのtrial内競争を推定しない。INT15自著はbetween/within system value conflictの高相関を別原著の負例として明示。[INT15 PLOS元原著](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010047)
8. **G2 INT05（Lepora & Pezzulo 2015）**：運動そのもののtrajectory・kinematicsが進行中のperceptual decisionへfeedbackし、action preparation/commitmentで結果が変わる具身的選択。INT01の試行間task-set階層の抽象化やsoftmax choiceには実運動trajectoryを通した認知への逆feedbackはない。モデル対象が異なる。[INT05 PLOS元原著](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004110)
9. **G2 INT09（Yeo, Franklin, Wolpert 2016）**：state-dependent sensory noiseによりmotor optimal feedbackのみでは足りず、将来の可視性を確保するfeedforward sensorimotor policyが現れる。INT01は4択2段階のlatent policy重み学習であり、15cm移動・方向依存視認性の連続制御とは中核演算が違う。[INT09 PLOS元原著](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005190)

上記の【限定的に異なる中心演算】は**モデル全系譜における独立発明の証明ではない**。元INT01自身の直接ancestorはXia/Collins21（旧v18確定）である。コード同一性・原著ソースの存在と、既成algorithm componentsの再利用可否は別問題。

## C. 重要な他論文の訂正 — INT09は元出版社だけでは不完全

**新しく科学適格性への必須ソースを見つけた**。INT09のPLOS第一者元原著（2016-12-14）には、**出版社編集部の2017-02-03正式訂正**が明示リンクされている。[正式Correction DOI 10.1371/journal.pcbi.1005370](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005370)は**Fig9のlegendだけ**を訂正する。旧文言では(C)(D)は(A)(B)と同じ「model mean only」と読めるが、正式訂正の図パネル対応は**(B)(D)が(A)(C)と同じmodel mean-only**である。訂正本文はモデル式やプロットraw値の改変は記載しないが、訂正文のスコープを越えて「全モデル数値が完全不変」とは証明しない。

**重要なsource-native実再確認**：2026-10-05に改めて開いた元の第一者PLOS原著ページでも、**誤った元のFig9凡例はそのまま表示**されている。したがって現行原著URLへのリンクだけでは不適切で、**原著＋正式2017図9訂正をセットで研究用の正しい出典媒体束として扱う**。旧G2の選定DOIや以前取得のofficial PDF raw SHAは変更せず、訂正版の内容をソース・資格に追加。図9全高解像画素の意味審査やINT09全数式・全変種・全Figure科学適格性は**まだ未完**。この単独訂正が論文の訂正史全件だと独断しない。v20a新しい訂正専用append-only台帳あり。

## D. INT01の75%原著問題／出版社版確認で今回新たに確認した範囲

同一private MHTのraw/HTMLの両SHAを再読取し、原出版社Discussionには正確に「majority ... (75% of all participants including top and mid performers)」と残存する一方、原著Fig3B/Appendixの`best 591 + mid 254 + random 181 = 1026`が**845/1026=82.359%**であることを再確認。**元データの原著記述不一致は確証されたが理由は未確定**。結論全体の数学的モデル優越や選択推定値が数値誤りだと推定せず、当該一般化比率の科学主張に限った保留を維持。

出版社元MHT本文は17個の`_lrg.jpg`高解像公式URLをリンクするが、高解像版0点封入。内蔵標準画質の元Fig7+補足Fig8+印刷Algorithm2=17原画像は旧v18で全点媒体SHA・目視審査済み。今回元公式高解像の例`gr5_lrg.jpg`・`gr7_lrg.jpg`を別Web readerで試みたが開けず、ローカルは`--connect-timeout 4 --max-time 10`で出版社画像CDN・Crossref両方DNS解決に失敗（HTTP000）。**ローカルDNS失敗は出版社がHTTP403を返した証拠ではない**。元MHTに訂正への直接Crossmark/corrigendum/erratumリンクは0だったが、訂正が存在しないとの完全な版史証明ではない。研究用のsoftmax決定は最新著者指示として不変。

## E. 今回の手続判定・次の資格条件

- **今回完了**：9件の新しい原著に即したINT01の「限定的中心演算差分」審査。計**12/35**の限定比較／**23**未実施。別途INT09の**正式2017 Fig9訂正原著の本文と原著上の旧表示の両方**を直接検証し、必要な原著媒体束の構成を決定。
- **まだ未完**：35件の全数学・全引用系譜の厳密な独立比較、INT01の私有MHTを後続独立審査員が継続取得できる管理入力として保持する条件、公式高解像全図／第三者出版社訂正全件検証、INT01「75%」記述の意味、G1最新コホートの全体正式入場、G2-D他15原著の全式図変種負例、INT09 Fig9全画素と補足、必要なG3/G4合同gate。
- **停止判定**：新規選定原著の「無条件全モデル科学合格」**0件**、グローバル中心系譜最終クリア**0組**、正式バックアップ採用**0件**、**G2-D PARTIAL / MAIN_NOT_AUTHORIZED**。本レーンの仕事を進めるために他レーンを待つ必要はないが、全体GOには別の統合が必要。

今回のversioned機械台帳：`G2D_V19_INT01_SIX_ORIGINAL_NATIVE_PAIRS_AND_EXACT_35_JUDGMENT_LEDGER.json`、`G2D_V20_INT01_THREE_ADDITIONAL_PAIRS_INT09_OFFICIAL_FIG9_CORRIGENDUM_AND_35_QUEUE.json`、`G2D_V20A_INT09_FIRSTPARTY_CORRECTION_IN_ORIGINAL_PAGE_PERSISTENT_20261005.json`。
