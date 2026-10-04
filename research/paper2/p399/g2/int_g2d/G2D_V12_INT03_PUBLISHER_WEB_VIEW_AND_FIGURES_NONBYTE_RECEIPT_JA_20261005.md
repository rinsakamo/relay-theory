# G2-D v12 — INT-03 PNAS公式HTML・公式図のブラウザ再確認（非バイト証拠、2026-10-05 JST）

独立G2-D Draft PR #430 の append-only 補充。対象 DOI `10.1073/pnas.95.24.14529`、Dehaene, Kerszberg & Changeux, *A neuronal model of a global workspace in effortful cognitive tasks*, PNAS 95(24):14529–14534 (1998)。旧G2原稿・元v11の物理取得失敗・凍結MAIN40、他レーン/旧#398、Grammar v0は変更しない。

## 今回の実際の取得経路を分けて記録

1. **時間制限付きローカル直接アクセス：失敗**。`curl -L --connect-timeout 5 --max-time 12` とブラウザUAで出版社公式の `/doi/pdf/`、`/doi/epdf/`、`/doi/` 3 URLを個別試行。全て `HTTP 000`、生本文0B。実行環境の `www.pnas.org` DNS解決失敗（うちepdfは約5秒）なので**PNASサーバー403を新規再現したとはいえない**。このローカル実行は原著物理取得失敗であり、科学的原著の欠如や出版社全域アクセス不能の証拠ではない。
2. **ブラウザ型Web閲覧：出版社ホスト公式HTML全文を可視**。`https://www.pnas.org/doi/10.1073/pnas.95.24.14529` が PNAS の `Research Article / Free access`、著者・1998-11-24・95(24):14529–14534・同DOIを表示。単なるabstractでなく `THEORETICAL PREMISES`、`COMPUTER SIMULATION`、モデルの `Network Architecture and Dynamics`、`Implementation of the Stroop Tasks`、`Simulation Results`、`EMPIRICAL TESTS AND PREDICTIONS`、`CONCLUSIONS` および文献表までブラウザのコンテンツ表現上で閲覧。HTMLの模型更新式・reward/vigilance・反証的境界も掲載されている。
3. **同じ出版社のFigure 1–3の実画像リンクを個別開き、表示を確認**。単にcaptionを検索したものではない：
   - Fig 1 `https://www.pnas.org/cms/10.1073/pnas.95.24.14529/asset/28836ce4-a0d9-49cc-95fe-2e4e165f294d/assets/graphic/pq2483639001.jpeg`：評価、長期記憶、注意、知覚・運動とglobal workspace、下段のfrontal/sensory説明。
   - Fig 2 `https://www.pnas.org/cms/10.1073/pnas.95.24.14529/asset/0f524c94-9440-4cb5-b720-e61d9ea69afe/assets/graphic/pq2483639002.jpeg`：reward/vigilance・workspace・processor/inputs と gating の元図・式表示。
   - Fig 3 `https://www.pnas.org/cms/10.1073/pnas.95.24.14529/asset/438335a8-dd9d-42f4-82ec-b435322ac6fa/assets/graphic/pq2483639003.jpeg`：Stroop 200 trialのモデル時系列・search、effortful execution、routinization。
4. **公式PDFはWeb閲覧レイヤーで本文索引のみ部分的に確認**。`https://www.pnas.org/doi/pdf/10.1073/pnas.95.24.14529` にブラウザのPDF読取が `application/pdf / 6 pages` を表示し、初頁のDOIに相当する誌名/原題/著者/巻頁、原著本文とモデル章のtextが取得表示された。しかし同じPDFのページ画像screenshotでは出版社の `/action/cookieAbsent` にリダイレクト。**元PDF生バイト、PDF署名、raw SHA256、全ページ画素は取得／検証していない**。ブラウザの収集済み・キャッシュ済み表示である可能性と、独立ライブHTTP本文取得の差を残す。PNGスクリーンショットの成功と誤称しない。

## 判定と次の必要条件

今回の新しい肯定的事実は **出版社ホスト上のHTML全文のブラウザ表示と、公式ホストのFig1–3原画像表示** の再確認。このセッションでも出版元PDFの独立raw-file取得・再取得同SHA・公刊版pdf画像の全ページ審査は **未達**。先行v6/v11 GitHub Actions物理403／Chromium Cloudflare403という別実行経路の陰性記録を消さないし、このWeb readerの肯定結果をその陰性実行の虚偽否定にも使わない。

#399のPDF-first/完全出版社HTML fallbackによれば、実際に完全公式HTMLと全模型決定的重要図を閲覧可能な場合、**将来のPRE_Aで版/媒体・URL/観察日・全ソース範囲を明示固定してHTMLを主一次媒体とする可能性**はある。ただし本v12はWeb表示証拠だけで、原著版・訂正履歴・式/図全数や全変種・負例・INT03×INT06の全中核数学系譜を独立最終判定していない。現在の選定G2 ledger、原本バイト・出版版の正式原著source admission、G1/MAIN数学系譜独立、backup activationやMAIN資格を**一切昇格しない**。

限定状態：`PUBLISHER_HOSTED_FULL_HTML_AND_FIG1_TO_FIG3_WEB_VIEW_OBSERVED`、`PUBLISHER_PDF_INDEXED_TEXT_ONLY_NO_RAW_SHA`、`INDEPENDENT_PUBLISHER_RAW_VOR_ACQUISITION_HOLD`、`G2-D_PARTIAL`、`MAIN_NOT_AUTHORIZED`。
