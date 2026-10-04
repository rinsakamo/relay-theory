# G2-D v14：選定INT-02の出版社真正原著14/14頁・Fig1–8・印刷式(1)–(17)個別原典数学視認、出版前コード照合と不利な条件（2026-10-04 JST）

**独立作業・隔離**：Issue #399、G2親作業用HEAD `69748673c80f421605f1c63607472903ac2ed68c`、INT専用Draft PR #430。MAINのGrammar/構造分解・再構築・H0/H1/H2・予備結果・G1/他G2レーンの科学作業に立ち入らない。G2の正式40名簿、原著選定、バックアップ順位・予約は変えない。今回の`INT-02`は既存選定DOI `10.3390/e26060484`、`Entropy 26(6) 484`（2024-05-31正式刊行）、Aswin Paul / Takuya Isomura / Adeel Razi。

## 1. 既存G2凍結publisher originalとの新しい真の物理・目視照合

出版社web本体は直接ページ429、実行したfirstparty HTTPのMDPI記事HTML／標準pdf両経路403。**成功経路はMDPI発行元自身のmedia endpoint** `https://mdpi-res.com/d_attachment/entropy/entropy-26-00484/article_deploy/entropy-26-00484.pdf`、HTTP200で取得した正式出版社PDF **14頁、2,814,783 bytes、RAW SHA256 `a1e644c826bf1b356187bc556d5947eb23638f3f9bc6c61835d46850b4f1cc37`**。これは既存G2 v5記録SHAと完全一致。一次[実現場 v12 37209569351](https://github.com/rinsakamo/relay-theory/actions/runs/37209569351)でダイレクト各**12秒上限**、失敗時**Chromium18秒上限**のfail-closed切替を用意。MDPI media endpointが正確に同SHAで成功したため無用なbrowser再試行不要。出版社でないPMC、preprint、arXiv、mirrorは公刊原著へ昇格しない。

[実原本v13全ページ視認CI 37209720541](https://github.com/rinsakamo/relay-theory/actions/runs/37209720541)では、**独立5ジョブ5/5 SUCCESS**、各ジョブ出版社真正PDFを別々に実ダウンロードし、すべて同一旧G2 SHAを照合。全14頁をsource rawからPyMuPDFで画像化・レビューアが実際に視認：p1–3本文定義、p4数式、p5–7基礎3図と基準比較、p8–10混合追加数式とFig5–6、p11–12混合結果Fig7–8、p13–14ソフトウェア・資金・元論文ref。**主本文Fig1–8全8件および印刷主本文式(1)–(17)を原画素とNative全文アンカーで個別確認した**。全14頁の原文テキストSHAと各作業担当頁の画像レンダSHAを実metadata artifactに保存、生PDF・全原文はrepositoryに転載していない。

**元CIに残す非科学的偽陰性**：v13の図キャプション検出正規表現が`\\s*`と余分にエスケープされ、図1–8が空のページ候補となったが、PDF raw SHAと画素視認は成功。**初回偽陰性は保存、図の存在を削除しない。** [独立v13b修正原典再照合CI 37209913343](https://github.com/rinsakamo/relay-theory/actions/runs/37209913343)ではregexのみを修正し、図caption候補頁：Fig1=p4–5、Fig2=p5、Fig3=p6–7、Fig4=p7/p10(再言及)、Fig5=p8–9、Fig6=p10、Fig7=p11、Fig8=p12と**全8件目撃**。同runは元PDFの高解像度クロップp8式(8),(9)、p9式(10)–(13)、p10式(14)–(17)を独立再表示・読解した。見た目からの同一数学式確認とソースコードでの挙動を同一カテゴリーに混同しない。

## 2. 出版社主原著の実際の中核構造と先行アルゴリズムの境界

p2–4印刷式(1)–(7)はPOMDP生成モデルのstate/observation/action/transition parameter化、変分自由エネルギー、既成DPEFEでの`P_DPEFE(u|s)`（Eq4、expected free energyとaction precision）、既成CLでのlearned state-action mapping＋risk Γを更新（Eq5–7）。**これらの新規発明をこの論文へ帰属しない**。主原著ref13はPaulほか既刊のDPEFE、ref14はIsomura/Fristonほか既刊CLへ明示的に遡る。論文自身は2つの元方式を初出としてではなく**取り込む側**と説明する。

当該論文で提案された主な増分は、**事後state依存の混合重みβが2方式の行動確率のShannon entropy差を評価する更新**（印刷Eq8）と、DPEFE/CLの行動分布のβ重み付き乗法（印刷Eq9）、これをPOMDP/変分自由エネルギーの構成（Eq10）と特殊条件下の期待重み`β=sig(-H_DPEFE + H_CL)`（Eq16）、および混合log policy（Eq17）で関係づけること。**`β`は予測計画に割り当てる重み**。βの増減の基準はこのsourceでは**行動分布のエントロピー/相対的決定確信度**であり、ある時刻の計算量や取得済みトレーニングデータ量を測って直接最適配分する計算器ではない。「data–complexity tradeoffを衡量」という動機／simulation結果と、βがwall-clock/future observation acquisition costの厳密な最適制御則を証明したことを混同しない。

**数学的なsource-specific留保（矛盾断定ではない）**：

- **N_INT02_001：出版社印刷Eq9のnormalizer明示なし。** 原著高解像度画素でEq9は`P_MM(u|s)=P_CL(u|s)^(1-β(s)) · P_DPEFE(u|s)^β(s)`と表記し、行動`u`についての全和を1にする分配関数`Z(s)`は明示されていない。任意の非同一2分布でこの幾何プールの和が当然1になるわけではないため、**Eq9印刷の右辺をそのまま完全に正規化済み行動確率と認定してはならない**。元論文が`proportional`略記を意図したか不明、著者の意図を詐称して誤り断定しない。
- **N_INT02_002：刊行前著者公開コードに明示的normalizationあり**。論文本体p13 Software/Data Availability自身が公開するauthor-repository `https://github.com/aswinpaul/aimmppcl_2023` について、既に**2023-12-20T04:52Zに存在した**pre-publication commit `9922288952a4f999d0e272e6ab7416ba433b1923` をGitHub公式原履歴で確認。当時`main/MutatingGrid/CombinedModel_agent_full_mut.py` 原blob `e50c062847dd779e17077d6bda20ceb7dec92395` の**L148–149**では、`p=(1-bias)*log(p_d_1)+bias*log(p_d_2)`、続いて`p=softmax(p)`。したがって、この実装のsampling distributionは行動軸で**実際に正規化する**。**印刷Eq9省略≠実装で確率分布不正という結論**。このsource codeは出版社の原本そのものではなく、source-native問題を独立に解釈するauthor-released accompanying artifactであり、今回のPythonを新たに実機再走査/環境再現したわけではない。
- **N_INT02_003：printed Eq8とimplementation parameterizationの完全同一化禁止。** 版固定した同prepublication code **L143–146**ではstate belief重み付き`Beta[:] += qs[0]*(ent_1-ent_2)`、`Beta=np.clip(Beta,0,1)`、`bias=Beta·qs[0]`。原著のEq8は一般の正規化率αを記号導入しているが、当該実装のこのpathは**明示的な自由αではなく実質α=1**。出版本文が提案した一般式とこの一例のコードをparameter-by-parameter完全同値だとは断定しない。
- **N_INT02_004：Eq8とEq16の範囲**。著者の式(10)–(17)の説明は`Γ_t=0`、prior β=0.5等を明示したうえで、`|H_CL-H_DPEFE| ≪ 1`の範囲でEq8がEq16の近似となると限定。**一般すべてのenv/分布でEq8更新=Eq16の厳密同一公式**として原著を昇格しない。

## 3. 全主図における実際の比較と重要な不利証拠

- **Fig1・Fig2**：OpenAI GymのCartPole-v1についてpole ±12°/cart ±2.4を元課題、100 episode後の±6°/±1.2難化環境を区別。**CLが実際のこの即時reactive制御ではDPEFEなどのAIF方式より優位**。しかし後半性能向上は、難化による失敗増→フィードバック頻度増という代替説明を著者自身挙げる。**N_INT02_005：このsourceは強化学習方式全般に対するSOTA優位を主張せず**、Dyna-Qは定性的な対照用途と明記。
- **Fig3・Fig4A**：もう一つのoriginal環境は900状態maze、最適47stepに対しランダム探索は約9000step。長期戦略が必要なmazeでは**DPEFE predictive planningの初期学習がCLより速い**。ただし原著条件ではDPEFEはaction precision=1に固定され、性能の最適経路到達を保証せず、precisionを調整すれば比較が変わると著者が注記。**N_INT02_006：両方式の優劣は課題条件・精度パラメータ依存**。
- **Fig4B**：DPEFE/CL/他AIFアルゴリズムのcomputational-complexity曲線の縦軸は**対数**。CLに「計画探索の計算量」はないが、learned mapping更新全般に計算コストがないとは言えない。図の理論的complexity比較をGPU実測レイテンシや恒常的な実行費用ゼロと誤読しない。
- **Fig5・Fig6**：実図5のagent-environment loopではenvironment generative *process* と内部agent generative *model* を峻別、DPEFE/CLがともに行動分布を出しβで統合。Fig6はeasy→難しいmazeへのepisode300 mutation設定であり、刺激内容自体の実世界での自律発見ではない。
- **Fig7**：mixed agent N=5/25/50は易しいmazeを約10episodeで学ぶが、環境mutation後の学習はDPEFEとCLの**中間に位置する**。pure planningより**常に速い・優越するというデータではない**。より深いplanning horizonがどの比較でも常に改善するわけではない。**N_INT02_007：mixedの成功は本研究の限定したdata–complexity妥協**。
- **Fig8**：Γリスクとβ混合重みは環境mutationに反応、βは掲載3計画深度条件で**0.5を超えない**（初期β=0.5）。式の許容`β∈[0,1]`と試験条件での観測範囲は異なる。β低下が当該有限シミュレーションで経験依存学習側重み増と整合するが、人間脳の因果的切替や任意未知環境での最適メタ学習の証明ではない。
- **N_INT02_008**：Fig1–8はagentシミュレーション、独立したヒト神経/臨床実験ではない。論文のコード公開は有利な追試可能性だが、本レーンは**外部コードの全実機seed・数値の独立再現実施0**。数学/図の出版社original bounded source visual auditの前進を、source-reimplementation/実証再現済みと誤認しない。

## 4. 残存系譜・edition／MAINを先取りしない

当該モデルはpre-existing Paul et al. DPEFEおよびIsomura/Friston CLを明示的に結合しているため、INT02単体の**新規条件付きentropy-gated product-of-policies mechanism**を局所候補とし、既存planning/CL各方式そのものを独立発明と認定しない。INT04 replay/MHN→VAE・INT08 online episodic gateとは表層用語「hybrid」「planning」「memory」だけで同定せず、全モデル中核数理に基づく最終G1×MAIN各選定との比較はまだ実行なし。MDPI版History/Crossmarkの後続全補足/訂正が存在しないことを推測せず、現時点で**物理的元G2公刊PDFの同一版再現と公式論文刊行日のみ**確認。author-linked codeの完全科学再現と、全修正版履歴・全球系譜・他レーン正式版元対照は独立gate。

**新しく合理的に閉じる判定**：`SELECTED_INT02_2024_PUBLISHER_VOR_EXACT_ALL14P_MAIN_EQUATIONS1_TO17_MAIN_FIGURES1_TO8_BOUNDED_SOURCE_VISUAL_EXAMINED`。個別original source-native数学/主図の審査前進であり、出版版修正/外部公開コード実再現/全G1+MAIN global family/全選定INT scientific full freezeは未達。`G2-D_PARTIAL`、全MAIN40共有リスト変更0、INTバックアップ正式採用0、`MAIN_NOT_AUTHORIZED`。
