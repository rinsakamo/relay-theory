# RelayTheory Paper2 G2 v6: 残り4件の出版社・アーカイブ版判別と事前第1バックアップの原本確認

**2026-10-04 JST。正式判定：G2_PARTIAL / MAIN_NOT_AUTHORIZED。** #399／#420・PDF優先→出版社指定完全原著HTMLの同格fallbackを維持し、従来v1–v5・40 DOI候補・#398旧研究・PF01–04・Grammar v0・G1/G3結果には一切手を加えない。本レーンではMAIN科学的分解／再構築／Grammar role mapping／H評価／source-reference packet形成は行っていない。

## A. 残り4件：出版社200と全文200を厳密に区別

実クラウド[版判別/アーカイブ照合 v6, run 37186252465](https://github.com/rinsakamo/relay-theory/actions/runs/37186252465)・[公式Elsevier API本文有無追加実行 37186297530](https://github.com/rinsakamo/relay-theory/actions/runs/37186297530) は、**BLF-01 / INT-01 / ATT-03**の DOI/PII 対応を公式 Elsevier API `https://api.elsevier.com/content/article/pii/...` の **HTTP200公式XML coredata**で認証した。ただし実応答は1,949/2,057/1,904 bytesの書誌＋リンク・メタデータのみで、原著のモデル数式・節・図を含む完全本文は返っていない。HTTP200を出版社全文取得の成功と数えない。Cell/ScienceDirect正式PDF/HTMLは引き続き403、Elsevier静的候補URLは400。4件の追加原著完全媒体の取得成功は**0**。

- **BLF-01** `10.1016/j.isci.2025.112844`：Europe PMCの一次医療アーカイブ **PMC12221758** の実際のXML（513,990 bytes、raw SHA256 `68369c258b53098c934f6f3c8c2c29d1c16c8236df50e61040fd55b3b6b76c52`）で刊行版DOIおよび正規PII `S2589-0042(25)01105-8` を原文のarticle-id metadataに確認。出版社ScienceDirect検索表示にも**OA/Creative Commons**、PMC掲載本文にもCC BYが表示される。これは公開アーカイブの正しい論文同一性の有用な二次証拠だが、**原出版社刊行原著PDFの生バイト・完全HTMLと版同一という証拠ではない**。公式原著未取得の状態を維持。
- **INT-01** `10.1016/j.cognition.2024.105967`：Elsevier公式API正規PII `S0010027724002531`；公開の **PMC12052257** は **Author manuscript** と明示するので、正式出版原著の代用にしない。PMC Europe経由XMLは本次HTTP500、公式Elsevierの完全原著は未取得。
- **ATT-03** `10.1016/j.neuron.2009.01.002`：公式API正規PII `S0896627309000038`。出版社 `Neuron` は掲載区分を**Review**としている一方、この論文本文自体は明確な正規化数理モデルの提示を主張する。「Review」だけで科学モデルを自動棄却／採用しない。事前ルールによる original modelling eligibility と ATT02/他familyとの原文比較が必要。公開 **PMC2752446** は **Author manuscript**、原著として不採用。
- **PRD-01** `10.1038/s41562-024-01930-8`：Nature原著の本体は **subscription preview only**。公式PDF別経路が返すHTMLを本体として扱わない。[2024-08-08正式出版社訂正](https://www.nature.com/articles/s41562-024-01978-6) はFig2a/4aの trident / planet の確率を初版 `0.33 / 0.67` から正規 `0.69 / 0.31` に修正。訂正通知は数式・全図版・全文を保証しないため、**正式訂正後の原著一次媒体入手待ち**。

## B. 作業40件のさらに別の正式版問題

**INT-13** `10.1371/journal.pcbi.1014796` を出版社[公式全文](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014796)で再実読みした結果、現在も `This is an uncorrected proof.` と明記（取得HTML raw SHA256 `057e12d6c60605f3f5344b3411e6038397c3f823e09274c4929da9af1afaaca0`）。出版日表示が2026-09-30でも、最終校正版として昇格させない。INT-B1は既存INT12直接後続、INT-B2はG1予約、INT-B3は他レーン兼用なので、目的に無関係な都合による候補飛ばしは禁止。

## C. 合理的代替の事前準備：候補は **0件起動**

元の冻结 `MAIN40_G2_OBJECTIVE_BACKUPS_v1.json` の**第1順位**3件のみを、40 DOIに完全重複しないことを照合した上で**新規実取得**。[Publisher-only PLOS physical first standby run 37186367137](https://github.com/rinsakamo/relay-theory/actions/runs/37186367137) は各PLOS公式原著PDF署名＋ページ数＋実raw SHAを保存した（著作物本体は公開Gitへ保管せず）。

| 元の未取得slot → 第1 standby | 出版社正式原著PDF実取得 | 制約 |
|---|---|---|
| ATT-03 → **ATT-B1** `10.1371/journal.pcbi.1011283` | 20 pages／1,760,491 bytes／SHA `8c190f4d6e981061e4ccd67f4797b83ccdeb8f1d47d8368fdafe137f1ef44209`。公式PDF p0のDOI/原題を独立表示・視認、元の`pypdf`連続文字列ではDOI false-negative。 | ATT-01とも selection-history、本人の旧CoRLEGOの発展を直接主張。元40/G1 family区別と全math/fig/variants未確認。**未採用**。 |
| BLF-01 → **BLF-B1** `10.1371/journal.pcbi.1003810` | 19 pages／3,419,858 bytes／SHA `869c8b1a535fcb4a922d677bc0c26ca8959930a7f62208c4bf74701899aa8870`。PDF p0–1正規DOI抽出PASS。 | PLOS[公式2014訂正](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003952)は第2著者の所属欠落のみを追加し、**数式／図修正は訂正告知に記載なし**。ただしBLF-02等の階層Bayesian/HGF系と中央系譜独立性未裁定。**未採用**。 |
| PRD-01 → **PRD-B1** `10.1371/journal.pcbi.1010740` | 32 pages／3,306,881 bytes／SHA `9c17c00fba0985f6f66b8520c6fc971ae5a2c6d3e1bac266d9fba2739c9792fe`。出版社公式HTMLのDOIは確定だが `pypdf` first2 DOI直結文字列はfalse/未解決。 | sensorimotor confidenceにおけるprospective/retrospective cueモデルが、元PRD-01のforward/backward **prediction** という原著中心メカニズムの適格代替かは未確認。公式PDF全図/全数式/全訂正のsource-first監査も未了。**未採用**。 |

上述3件は**predeclared discovery-source-receipt only**。例えばBLF-B1の訂正がモデル数式に影響しないことは、原著全モデル科学的資格・全訂正absence・BLF系譜独立性を意味しない。MAIN40 DOIの置換、INT系バックアップ飛越、G1予約の使用は実行していない。代替の科学的source-nativeモデル・正規刊行版・family比較を全て終え、#399規則とG4・著者承認を得るまでは原枠名簿を変更しない。

## D. 機械可読な判定と実行分母

版付き元原著/補助候補の識別子・取得成否・PDF SHA/ページ/訂正/未解決独立性は `MAIN40_G2_V6_OFFICIAL_SOURCE_VERSUS_ARCHIVE_AND_STANDBY_RECEIPTS.json` に保存。目的非依存追記イベント `MAIN40_G2_OBJECTIVE_EVENT_DELTA_v6.json`。旧v5作業用main manifest raw SHA `06df3a52c09f8146571ceb0f18add3d3e0673716ffefb807a7fafea2465b3c5b` は今回**変更なし**。

- 提案・変更禁止の MAIN40：**40/40 unique DOI** (24+16)
- 原MAIN一次媒体の実アクセス：**36/40**（PDF raw SHA取得31 + publisher full PDFブラウザのみ2 + complete publisher HTMLのみ3）
- 第1備候補のpublisher original PDF raw SHAの実取得：**3件（MAIN原著取得数とは完全に別分母）**
- 元4件first-party正式原著媒体アクセス：**依然0/4**、BLF01のEurope PMC原著metadata=原出版社資格ではない
- 元40件の重要数学／図／全variant／負例／原著訂正を科学的完全qualified：**0/40**
- 元40件の中央source-native family最終admitted：**0/40**
- 第一順位備候補の全source-family科学的qualified：**0/3**；実起動：**0**
- 最終joint freeze、G3正式source packet、初回MAIN author GO：**なし**

**G2_PARTIAL**。残る先行課題は、4件のpublisher original editionの正規アクセス／客観的予備候補科学的採用、PRD訂正済み媒体、INT13 PLOS最終版、および計40件の原著math/figure/variant/negative原文・家系完全監査、G1最終20名簿との公正な照合。科学的な結果・予想結果に基づいてどの論文を取り替えるか選ぶことは禁止。
