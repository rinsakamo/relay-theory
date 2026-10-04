# G2-D v8：公式Nature INT04正式原著＋科学補足＋報告書31ページ独立再照合とFig1/2限定原図視認（2026-10-04）

**authority:** Issue #399、G2 frozen HEAD `69748673c80f421605f1c63607472903ac2ed68c`、INT独立Draft PR #430。既存v7歴史およびすべての403/200 challenge/初回ブラウザ成功は保持。本記録は既存原著v7の**独立再取得＋一部原著画像を実際に読んだ科学限定delta**。MAIN Grammar/構造再構築/H0-H1-H2/予備MAIN結果へのアクセスなし。

## 真の実行結果

[独立GHA run 37200273167](https://github.com/rinsakamo/relay-theory/actions/runs/37200273167) `SUCCESS`：各正式媒体はNature記事自身に実在するリンクからのみ取得。Chromium初期論文ページ18秒のtimeout、各媒体取得12秒のtimeout。ブラウザ起点の同一クライアントsessionで再取得し、上流v7の**生バイト数・SHA-256と完全一致**したため3/3証明。

| 公式原著媒体 | PAGES | バイト数 | RAW SHA-256 |
|---|---:|---:|---|
| 正式Version of Record main PDF `s41562-023-01799-z.pdf` | 20 | 2,666,492 | `b78a62b28775ec55610aeeca2252bc43b1ba782486c083a5065a3419ed3cde31` |
| 公式科学補足 `41562_2023_1799_MOESM1_ESM.pdf` | 9 | 2,912,573 | `6f9baebc2f95492b4ce275c64ed0cb640105cd480d401b78dee09c5abbb03612` |
| 公式Reporting Summary `41562_2023_1799_MOESM2_ESM.pdf` | 2 | 47,812 | `a9b713fbc8d39e24534ecaceb9c6deb53f13d36b0ec21843130bb69f67ad93bf` |

3媒体の合計31 PDFページを真正原本からすべてNative PDF text extractionし、各ページ抽出UTF-8 SHA・指定用語のページ候補索引を実行結果JSONアーティファクトに保存した（PDFの元バイナリや本文全文はrepositoryに再配布しない）。これはソース物理証明と**検索位置の記録**であり、抽出テキストのみで全数式の画像・全図の意味を監査したと主張しない。

**今回実際に初めて原著画像をモデルに表示し視認した箇所**：上記20頁正式 main PDFのzero-based p2（印刷p528、正式Fig1全パネルa–g）とp3（印刷p529、正式Fig2全パネルa–d）。本物のSource SHAが一致したPDFをrunner内PyMuPDFで直接renderしたpage JPEGを一時的GHA実行ログからモデル内部閲覧、原著に対する図画素確認を実施。図画素の実際の回路矢印とsource captionを突合した。残り本文Fig3以降と9頁の付録全図は**まだ画像画素を網羅視認していない**。当初web内PDFスクリーンショットはNature認証転送で2回失敗した（履歴保全）ためGitHub上の正規firstparty raw-source renderで代替した。「スクリーンショット未遂」と「成功したactual SHA-locked原PDF render」を混同しない。

## 限定的に視認済みの科学構造

- **Fig1 basic**：赤の海馬側のautoassociative MHNはfeature/memory units間を結合して**one-shot encoding**、青のgenerative cortical networkはreplayされた教師パターンから潜在変数を学ぶ（encoder/decoder）。Fig1c/dはShapes3D 10,000件のMHN-replay例およびVAEによるpartial image reconstruction。Fig1e–gはconsolidated episodic memory/imagery/semantic memoryで**生成可能な経験像と概念的潜在表現の出力先**を分ける。これらはFigureの図示であり人間脳回路の因果実測ではない。
- **Fig2 extended**：Fig2aは海馬側に**生成モデルで予測される概念情報と、予測困難な新規sensory residual**の両方を関連付ける拡張。Fig2bは新規動物を森林スキーマへ合成する例、Fig2c/dは概念情報＋想定外感覚を一時的に分割して保存し、recombined retrievalする。**この拡張でのprediction-error選択的な記憶符号化**とbasic Fig1教師リプレイを区別。Fig2aはentorhinal/pFC/alTLの複数生成ネットワーク候補を表現するが、実際の各回路神経録音や神経接続の因果実証ではない。

## 原著source-nativeの否定条件

- **N_INT04_V8_001:** Fig1ページ原著印字本文自体で、basic autoassociative memoryについて**decay、deletion、capacity constraintsをsimulationしていない**と明示。論文の「有限海馬容量の合理的使用」という理論的動機を、容量制約ありのシミュレーション実証と混同しない。
- **N_INT04_V8_002:** basic modelのevent-level prediction errorに基づき予測困難なイベントだけ海馬保存という構成は、原著本文の限定で**basicの当該選択をsimulationで明示実装していない**。実際のextended Fig2の予測誤差に基づく概念・感覚分解の図示／例と別。basic全実験にerror-based selective sparse memoryが搭載済みという誤認を禁止。
- **N_INT04_V8_003:** MHN・teacher–student・VAE/空間認知モデル各構成は先行研究の明示的継承であり、このsourceの統合アーキテクチャ差分を個々の初出と取り違えない。
- **N_INT04_V8_004:** 図1c/dの10,000 source Shapes3Dパターンに関するsimulation例は任意外部経験・臨床人間神経系への一般化を証明しない。

## INT08との限定対照と留保

INT08 正式eLife VOR（DOI `10.7554/eLife.74445`）の最重要操作はLSTM/A2C学習が**次状態予測に役立つ時点を選んでepisodic encode/retrieveする可変ゲート**とLCA既成競争的検索。**INT04 Fig1/2のreplay→VAE latent schema学習・error-selective hippocampal trace補完**とは、source-native実際の主要演算が異なる。両者は共通海馬/新皮質仮説、先行ニューラル部品の再利用、予測・一般化用途を共有。元のsource-native局所分類は `DISTINCT_OPERATIONAL_TARGET_AND_UPDATE_PATHWAY_BOUNDED`、**数学的完全同値判定・全Figure数学の比較・他選定INT13/G1/MAIN系譜とのグローバル独立合格ではない**。

## 現状と不変条件

INT04の正式刊行主原著20p＋公式科学補足9p＋Reporting2pは同一媒体を2回の独立runnerで exact raw SHA確認、31pの各text索引とFig1/Fig2目視追加。公刊改訂監査は2026-10-04 Crossmark「Document is current」を参照し、未記録の第三者更新全不存在は断言しない。選定INT04の**physical source completenessはPASS**、全数式・残図・科学内容・グローバル中心モデル系譜のフル資格は**HOLD**。INT03 PNAS 403＋Cloudflare制限のため、初回G2 browser候補の再取得に新規成功なし。INT01 Elsevier完全原著・INT13 PLOS最終版は未解決。元のB1条件BLOCKED、B2 G1予約、B3/B4 HOLDも不変。**G2-D_PARTIAL、formal backup adopted=0、MAIN_NOT_AUTHORIZED**。
