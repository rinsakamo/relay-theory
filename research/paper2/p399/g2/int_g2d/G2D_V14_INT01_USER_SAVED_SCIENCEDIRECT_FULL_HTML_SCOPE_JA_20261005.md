# G2-D v14 — INT-01 ユーザー提供ScienceDirect MHT原著全文媒体の実体監査（2026-10-05 JST）

**結果**：過去のElsevier通常HTTP/Chromium403で「研究セッション内で正式版の完全本文にアクセスできない」というINT01の実務上のアクセス障害は、ユーザーが通常ブラウザから保存したMHTによって**本セッション内で実質解消**。しかし、そのMHTは独立HTTP取得したElsevier raw HTML/公式PDFではなく、保存ファイルの真正性・将来全ステージでの原本管理・版と訂正履歴・原著数式／図の科学的意味・中核モデル系譜は別審査である。原著の正式「全面科学資格」には昇格しない。#399の「PDF優先／出版社公式完全HTML代替」はHTML媒体を許すため、PDF取得そのものをMAIN分析の絶対必要条件に新設しない。

## アップロード原本の実解析

- 添付MHTは `From: <Saved by Blink>`、`Snapshot-Content-Location: https://www.sciencedirect.com/science/article/pii/S0010027724002531?via%3Dihub`、`Date: Sun, 04 Oct 2026 15:16:04 GMT`。**5,754,741バイト**、**SHA256 `32158948f6d1f4ffd7170393c30a5742ce7db1b0a871928f64bd176cf9ab3b64`**。これは**ユーザーが提供したアーカイブそのもの**のhashでありElsevierサーバーの生HTTPレスポンスhashではない。
- 独立にMIME解析した元ページHTML本体 **1,250,747バイト**／そのHTMLパートSHA256 **`0c6c2670f715b06e3a9596cf848df9e08bb5b5168d5dd57113730d3d50b8fc52`**。`citation_doi` は `10.1016/j.cognition.2024.105967`、canonicalは出版社の対応PIIページ。出版社の別系統の公開検索インデックスにある正式全文ページと**DOI/PII/論題/著者/巻254／2025年1月／本文冒頭・データ公開説明**が整合するが、インデックスとの完全バイト一致・過去の改変不存在の証明ではない。
- スナップショットに本文**Introduction、Methods、Results、Discussion、Conclusions**、そのまま掲載の**Appendix A Supplementary Methods、Appendix B Supplementary Figures、Data and code、References**が存在。2.3 Models下の hierarchical model / meta-learning model / temporally forward and backward representations / fitting and model comparison の節も実在。**著者原稿ではなく、少なくとも出版社刊行版の完全HTMLを保存した構造・本文の強い証拠**。
- 出版社HTML内の掲載キャプションは **本文Fig1–7＋Appendix Fig B.1–B.8＝図15点、表2点**。PDF以外の数式・記号インライン画像 **26点** と図の高解像JPEG **15点**、計**41点すべてMHTに封入されPillowで形式正常にデコード**。本文が参照する同論文原図／式の `img src` **47件すべて対応MIME資産あり**（重複小画像とlargeを含む）。これは資産存在／形式審査であり**全数式の正確な下付きや各図の科学的な全パネル意味の人間査読ではない**。
- フルHTML内のSupplementary MethodsとSupplementary Figuresは本文と**同一ページに含まれている**。独立外部ファイルの有無、正式訂正履歴、出版ページ外のモデル定義要件は最終PRE_Aで再確認する。MHTの付随する別フレームがchrome-errorでも主本文HTML本体・article 47画像の全資産存在と混同しない。
- 実解析の構造的整合テスト **10/10 PASS**：原本／HTMLの長さ、公式URL形式、正規DOI、主要5節／掲載付録、画像src全保存、15本の原図＋26本の式記号JPEG、15原図＋表2キャプション、全41 JPEGデコード。**真正性の第三者公証や独立原著科学資格を証明する10件ではない**。

## 出典・研究手続上の限定判定

今回新たに成立するのは **`INT01_PUBLISHER_FULL_HTML_CONTENT_AVAILABLE_IN_THIS_SESSION_FROM_USER_SNAPSHOT`**。公式PDFの同一原本raw byte取得、独立Elsevier HTTP200取得は新規0のまま。旧G2-Dで実行したHTTP403・公式API書誌限定・Chromium403の失敗履歴を削除しない。ただし、もはや「出版社の完全本文をこのセッションで実際に読めない」とは扱わない。PMC著者原稿を出版社正式版と取り違えない。

技術的PRE_A候補の主一次媒体を**ユーザー保存のScienceDirect公式完全HTMLスナップショット**とする方向は#399規則と整合。再現可能なA→B→C実行前には、著作権条件に従って**この実MHTを管理された原著入力として継続利用できる形で保持**し、URL/本文パート原SHA/掲載図群・表示日・版／訂正履歴を原著スコープに明示する。現時点のチャット添付は直接GitHub資産ではないので本公共Gitリポジトリには著作物本文・MHT本体をコミットせず、SHAと監査結果のみ追加。

**正式原著科学的全面資格・G1/MAIN中核モデル全体独立・backup発動は0増分。G2-D_PARTIAL、MAIN_NOT_AUTHORIZED不変。** 対応機械台帳：`G2D_V14_INT01_USER_PUBLISHER_MHT_FULL_HTML_MEDIA_RECEIPT_20261005.json`。
