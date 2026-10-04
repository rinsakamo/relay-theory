# Paper2 G2 v5 — LRN-01 Nature出版社原著の実取得と残り4件（2026-10-04 JST）

**判定: G2_PARTIAL / MAIN_NOT_AUTHORIZED**。#399およびDraft G4 #420を尊重する。G2 Draft PR #419の専用ブランチのみを更新。従来のv1/v2/v3/v4、#398旧コーパス、PF01–04、Grammar v0、G1/G3は改変していない。MAIN科学分解/再構築、H0/H1/H2、先行MAIN結果閲覧は実行していない。

## LRN-01 実出版社刊行原著を二つの実行で取得

Nature Communications `10.1038/s41467-025-58848-6`（Fang & Sims 2025; 2025-04-29正式刊行）の**出版社第一者原著**を、Python一般HTTPクライアント/通常検索のpublisher IdPリダイレクト失敗と分離し、専用隔離GitHub Actionsの本物のChromiumブラウザから実アクセスできた。

- 初回 [actual firstparty Chromium 37185492865](https://github.com/rinsakamo/relay-theory/actions/runs/37185492865) で、出版社Nature公式20ページpublished PDF **59,865,461 raw bytes / SHA-256 `638c40d95b03e9ed076949c1c17f469bed4e1c3c9959ca8a84dc65c8a0744718`** を物理取得し、PDF署名、DOI、原題長語5件を抽出元の原著p0～p1と照合。独立して出版社原著完全HTML raw response **589,806 bytes / SHA-256 `615b87a820b1d499df54cad3afdaad3d2771a9fbaf536f29982b31e64336c883`**、ブラウザ表示本文116,965文字、Introduction/Methods/Results/Discussion/Referencesの全5節存在を検査。PDFや本文の著作物はGitに公開せずメタデータだけをartifact/ログへ残した。
- [第二のactual publisher physical reacquisition 37185593074](https://github.com/rinsakamo/relay-theory/actions/runs/37185593074) で20ページ/59,865,461 raw bytes/**上記PDF SHAが完全一致**した。原著HTMLは同じ589,806 bytes/116,965文字でもHTTP response SHAが `7adb63a533ef39da71a7a67be28d45aa469265d56426bbc117a7364bbb763ec0` に変化したため、HTML byte-equivalentとは主張しない。ページ全科学モデル数学・図・全variant/negative・訂正は未審査。
- **重要なCI履歴保全:** 第二回原本データ自体は完全一致したが、当初のtest scriptは`pypdf`で折返しが混じるタイトルをPDF textの完全単語文字列検索で認定しようとしたため、事実に反する`title_found=false`を出し、**workflow全体はFAIL**。原本PDFの同一SHA・DOI実一致・独立HTML原題表示の組合せを客観的な正式判定条件とするようscriptをコミット `0f958bf523db7916f3ea838fc13123db2933e04b` で改め、真正な2回目以降のPASSを別途受領するまで初回の失敗CIを成功とは表示しない。この検証器問題は物理原著取得の事実を取り消さないが、合格CIの事前宣言は許さない。

新規のLRN01原著について、モデル審査時の**索引のみ**としてpublished原著自身の標準強化学習`RLPG`、cascade `CPG`、効率符号化を含む `ECPG`、2つのgeneralization実験と対照・負例を追う。索引は source-native 情報であり、Paper2 Grammarによる再構築や新科学的採用ではない。出版社の全訂正履歴、本論文全モデル数学・図・変種・対象外記述の全面監査は今後行う。

## 残り4件のfirst-party gate

| Slot | DOI | 出版社の実状と決定 |
|---|---|---|
| PRD-01 | `10.1038/s41562-024-01930-8` | Natureは購読制限付きAbstract/previewにとどまる。Publisher Correction `10.1038/s41562-024-01978-6`はFig2a/4a trident:planet初版`0.33/0.67`→正規訂正`0.69/0.31`と明示。訂正通知を原著の完全数学図版に置換しない。正規訂正後の刊行PDF/完全HTMLアクセスが必須。 |
| ATT-03 | `10.1016/j.neuron.2009.01.002` | Neuron/Elsevier第一者PDF/fulltextではHTTP403、他公式CDNは400。出版社正式掲載種別は**Review**だが、本文が独自の正式計算モデルを提示する可能性と、本レーンのoriginal-modelling-paper採択基準は別途source-native要審査。PMC `PMC2752446`は明示的**Author manuscript**、刊行済original PDFの代用は禁止。 |
| BLF-01 | `10.1016/j.isci.2025.112844` | Elsevier第一者のCell/ScienceDirect PDF/fulltextはHTTP403、CDNは400。公式登録のOA/CC表記は確認したが原著刊行PDFバイトは未取得。PMC `PMC12221758`には公開刊行記事テキストがあるが、出版社ファイルとのversion-of-record物理同一性/第一者publisher provenanceは未証明；**本文索引・二次照合以外として採用しない**。 |
| INT-01 | `10.1016/j.cognition.2024.105967` | 出版社公式CognitionはOA/full-lengthと掲載するが本レーン実取得はHTTP403。PMC `PMC12052257`は本文に明示された**Author manuscript**であり刊行版と区別し、原著primary扱いを禁止。G1とのCollins/Frankなど中央系譜は独立source comparison未解決。 |

上記公式のHTTP障害は作品不存在を意味しない。目的とルールに合わないからといって、これらを都合よくunilateral backupへ差し替えない。正式に出版社公開の完全原著へアクセスするか、候補確定前の客観的除外・代替優先順位・レーン配分審査を別建てで行う。

## 実際の分母（重複しない）

| 分母 | v4 | v5 |
|---|---:|---:|
| MAIN 事前提案40個の固有DOI | 40 | 40、不変 |
| 物理raw SHAがあるoriginal出版社PDF | 30 | **31**（LRN01追加、二回SHA一致） |
| 出版社PDF実閲覧のみ、生SHAなし | 2 | 2（CNC01/INT04） |
| 出版社原著完全HTMLのみ実閲覧 | 3 | 3（ATT01/MEM01/INT03） |
| 重複排除済original媒体first-party実アクセス | 35 | **36** |
| first-party原著取得未解決 | 5 | **4** |
| 版/全数学/全図/全変種/負例/訂正を科学的完全採用 | 0 | **0** |
| 厳密central-family科学的独立合格 | 0 | **0** |
| 事前客観backupの実発動 | 0 | 0 |
| G2/G3最終科学名簿凍結・MAIN承認 | なし | **なし** |

G1独立PR #418の観測HEAD `9d45aa277aa148d3f8c1a3b5bf5adf38166e7fc4`では、PF4＋P05＋P07＋P09のsource-scoped限定資格で**7/20**。ただし最終科学20名簿・中央系譜とのG2跨ぎ判定は未凍結、G1外部更新後は再照合必須。G2によるG1/PF科学を一切変更しない。

新たに `MAIN40_G2_LRN01_FIRST_PARTY_DUAL_PHYSICAL_ACQUISITION_v5.json` と `MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json`、今後のv5追加objective events、raw evidence SHA台帳、fail-closedテストをappend-onlyで保管。**G2_PARTIAL・MAIN_NO_GO 維持。**

## 追記：独立再取得の正式な修正版テストPASS

過度に厳密なPDF文字列連結条件だけを修正した公式ワークフロー [37185663924](https://github.com/rinsakamo/relay-theory/actions/runs/37185663924) は **PASS**。初回・非該当の厳格テストFALSE-negative回・修正後PASS回の**3つの実際の出版社原著PDF**のSHAはすべて `638c40d95b03e9ed076949c1c17f469bed4e1c3c9959ca8a84dc65c8a0744718`、59,865,461bytes、20pages完全一致。PDFの行分割で`efficient`だけ文中連結一致しない一方、原著HTMLに完全題名が実表示され、正規DOIと二重原著生SHAが一致することを検査。修正後HTMLはdynamic raw response 589,798bytesでSHA `7bdf30b55aecc0a677d1c3ed42e27d240a174cf1e6b659f0e1fdea06a7f5d0c2`、表示完全本文116,965文字・5節は維持。旧FAILED runを偽ってPASSと改記しない。科学的全本文審査PASSを意味しない。
