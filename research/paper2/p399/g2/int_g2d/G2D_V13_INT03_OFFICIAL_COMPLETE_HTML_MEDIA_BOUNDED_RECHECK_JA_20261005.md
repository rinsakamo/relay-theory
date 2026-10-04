# G2-D v13 — INT03 PNAS出版社公式完全HTMLの技術一次媒体選択と停止条件（2026-10-05 JST）

**科学実験を実行しない出典・版ゲート専用のappend-only増分。** v11の実GitHub Actions 5つの旧PNAS配信URL全403＋Chromium403、v12の別Web reader閲覧記録、旧G2ロスター（すでにINT03公式HTML browser-only 1件としてカウント）を残す。旧#398/Grammar v0/PF/G1/G3/G4は不変。MAINの構造分解・再構築・H0/H1/H2やパイロット予備結果は閲覧／実行しない。

## 新しく確認した根拠と取得方式

- 対象：Dehaene, Kerszberg & Changeux, *A neuronal model of a global workspace in effortful cognitive tasks*, PNAS **1998-11-24, 95(24):14529–14534**, DOI **10.1073/pnas.95.24.14529**。
- **12秒以内に中断するローカル物理URL確認**：`curl --connect-timeout 5 --max-time 12` でPNAS DOI HTML/PDF双方が `Could not resolve host: www.pnas.org`、HTTP000/0バイト。これは今回のコンテナのDNS制限であり、PNAS自身のHTTP403が再発した証明ではない。旧v6/v11 GitHub Actions403とは別の失敗経路。
- **Webブラウザレイヤーで出版社自身の完全原著HTMLを今回再開**：`https://www.pnas.org/doi/10.1073/pnas.95.24.14529`。公式Research Article / Free access表示、同DOI・刊行日・巻号・頁に加え、`THEORETICAL PREMISES`、`COMPUTER SIMULATION`、`EMPIRICAL TESTS AND PREDICTIONS`、`CONCLUSIONS`、`REFERENCES`が実際に掲載され、abstractのみのレスポンスではない。表示版/ページを2026-10-05の現行公式ブラウザ閲覧に固定。原本HTML生バイトは取得していない。
- **元出版社ホストの図1、2、3画像をすべて個別に開いて画像表示を目視**。機械readabilityのみでなく、Fig1は分散workspace／5つのprocessor、Fig2はStroopネットワークと上位ゲーティング・報酬の原図と上下inset、Fig3は著者の200 trial**シミュレーション**のsearch/effort/routinizationとmodel-based putative brain imagesであることを可視確認。図3下段の脳画像の絵は新たな人間脳測定データとして**認定しない**。出版社画像URLは隣接のtyped JSONにすべて固定。
- 同HTMLモデル定義段落には inhibitory sigmoid、興奮単位の `S_EXC=sigmoid(Σ_asc Φ(Σ_desc))`、`Φ(0)=1` と興奮／抑制条件、reward-modulated Hebbian `Δw`、成功失敗依存のvigilance `ΔV`、短期結合係数 `Δw′` が実表示される。**Fig2下段のゲート原図はHTML本文の上位／下位項の区別と定性的に整合**する。数式全文の原刊PDF印刷ページとの画素同一性・原著量的再実装を主張しない。
- PNAS公式PDFとePDFの新しいWeb reader再試行は `/action/cookieAbsent` ページにリダイレクト。今回、正式PDFの生バイト、PDFファイル署名、ページのレンダリング原画およびSHAを取得した事実は**ない**。旧v12でPDF本文検索索引は一部見られたが原本物理取得の証拠ではない。無断第三者PDF・PMCを出版社原著の代用品へ昇格しない。

## 出版版・媒体の技術ゲート

#399で著者が明示した**PDF-first / 公式完全原著HTMLを同等な主一次資料候補にするルール**に従い、他の論文や付録を第二主媒体として混合せず、次の**INT03限定技術選択**を追加する：

1. 現時点で選ぶ単独原著主媒体は出版社自身の上記**公式1998論文・現在閲覧可能な完全HTML**。図1〜3は**このHTML内に掲載された同一出版物の構成素材**であり、別第二論文ではない。今後のAが行われるならこの媒体・刊行日・URL・3図・可視モデル主要段落・負例をPRE_Aに明記し、A→B→Cで原著版/媒体をすり替えない。
2. これは**browser-readable original scientific mediumの技術選択のみ**。出版社完全HTMLのバイト保存や正式PDFとの数式・図完全同一性、最終訂正／erratum/Crossmark網羅照合、全重要変種・不利条件科学監査を達成したとの証明ではない。将来公式原著PDFが得られ内容相違を見つけた場合、既存Aを無断変更せず版差を明示して停止・再審査する。
3. **既存G2ロスター分母36/40（そのうちINT03はすでにHTML browser access扱い）を増加させない**。新規出版社PDF raw SHA=0、MAIN科学的full qualificationの新規昇格0、INT03×INT06のglobal central lineage合格0、バックアップ採用0。

## 原著に明示された不利条件と境界

- 元著者はこのシミュレーションが部分的かつ不完全で**Stroop課題に限定**されると明記。汎用グローバル認知の新たな実証と解さない。
- 既存Dehaene/Changeuxモデル群（1989/1991/1993/1997）が1998論文の明示祖先である。INT06 2010 spiking routerの実装差とは区別するが、定義が異なることだけで最終中核系列独立を認定しない。
- 複数課題への初期結合汎化、海馬新奇検出、自己表象などは将来課題として述べられる。原著が実装済みと推定しない。
- Fig3に示す脳画像相関はあくまでputative図解。主な元図は200 trialモデルシミュレーションであり、新たな人間脳因果実験ではない。

**保留条件**：元PNAS正式PDFの生バイト取得/SHA、出版社版／訂正履歴の独立照合、印刷PDF全ページ画素照合、完全モデル数式・全不利条件の正式科学的確認、INT03×INT06およびG1×MAIN全中心数学系譜。別途明示的な承認なくMAIN分析を開始しない。

**限定結果：`PNAS_FIRSTPARTY_COMPLETE_HTML_BROWSER_MEDIA_SELECTED_ONLY`／`G2-D_PARTIAL`／`MAIN_NOT_AUTHORIZED`**。媒体選択は旧G2 v11 403実記録と両立し、原著物理PDFを取得したという新たな主張を生まない。

Typed source-and-stop ledger: `G2D_V13_INT03_PNAS_HTML_TECHNICAL_PRE_A_MEDIA_SCOPE_AND_STOP_GATES.json`。
