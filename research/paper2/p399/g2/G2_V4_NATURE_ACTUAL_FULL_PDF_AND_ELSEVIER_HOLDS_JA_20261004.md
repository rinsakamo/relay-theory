# RelayTheory Paper2 G2 v4 — Nature公式原本回収・Elsevier再照合（2026-10-04 JST）

**判定: G2_PARTIAL / MAIN_NOT_AUTHORIZED**。Issue #399・G4 #420に従い、先行v1/v2/v3・PF01–04・Grammar v0・#398・G1/G3所有物は改変しない。MAIN科学分解/再構築、anticipated H0/H1/H2評価、Grammar-roleマッピング、科学的忠実度試験を実施していない。

## 出版社所有の完全原本への新規実アクセス

1. **CNC-01**: Nature Human Behaviour出版社公式 `https://www.nature.com/articles/s41562-023-01719-1.pdf` を実際にブラウザで開き、全文PDF **15ページ**・巻号誌ページ・表紙DOI `10.1038/s41562-023-01719-1`・正規論文題名を照合。少なくとも出版PDF p7（0-index page7）を画像として独立表示・確認し、正式本文中の実験2–4方法・Adaptor grammar Algorithm 1を読めることを確認。PDFの**生バイトを本レーンへダウンロード保存・独立SHA記録したわけではない**。全15ページの重要数学・変種・負例・訂正の科学的監査や原著資格は未完了。
2. **INT-04**: Nature Human Behaviour出版社公式 `https://www.nature.com/articles/s41562-023-01799-z.pdf` をブラウザで開き、全文PDF **20ページ**、表紙DOI `10.1038/s41562-023-01799-z`、正規題名、刊行済み巻号誌ページを照合。加えて公式出版社 `https://www.nature.com/articles/s41562-023-01799-z` から本文Main/モデル説明にアクセス。出版PDF p3（0-index page3）を画像で確認し、図2のautoassociative + generative拡張モデルの可読性を確認。原著PDF生SHAは未取得、全variant/訂正・系譜照合未完了。
3. 以上は**出版社の刊行済み完全PDFに実アクセスできた**という限定的な実証。旧v3の「PDF raw SHA取得30件・PDF取得失敗後の公式完全HTML確認3件」と**重複しない2件**のため、一次原著のdistinct原媒体実アクセスを**33→35/40**へ増やす。raw PDF originalファイル独立SHA256は引き続き**30/40**。原著のscientific fully qualifiedは**0/40**であり、35とは同じ分母の別の状態を表す。

## 性質の異なるNature残り2件

- **LRN-01** `10.1038/s41467-025-58848-6`: Nature Communications出版社の検索索引はOA刊行済み原著であると表示。**しかしブラウザで原本直接URLを開くと出版社IdPへ強制遷移**。publisher PDF直URL・Springer direct PDF、Springer記事HTMLの代替試行も原著の完全性チェック未通過（後述クラウド実走）。検索索引から得た本文断片・第三者PMCや著者稿は、出版原著そのものを実取得した証拠としては使わない。アクセス未解決。
- **PRD-01** `10.1038/s41562-024-01930-8`: Nature出版社の原著ページを実表示したが、「subscription content preview」の明記があり、**完全HTMLの代替原著ではない**。正式出版社[Publisher Correction](https://www.nature.com/articles/s41562-024-01978-6) は、図2a/4aのtridentとplanetの初版確率表記 `p=0.33/0.67` を**正規訂正値 `p=0.69/0.31`**へ変更したと明記し、出版者の原著ページにも「updated」表示がある。原著更新版の図2a/4a実画像比較・本文全数学・モデル変種未完了。**訂正告知本文を原著完全版の代わりにしない**。

## Elsevier公式の二次経路実走

初回および別URL再取得でも失敗した ATT-03、BLF-01、INT-01 に対し追加で出版社所有の `ars.els-cdn.com`、`cell.com/action/showPdf`、`linkinghub.elsevier.com/retrieve/pii`、`sciencedirect.com` direct PDF をクラウドで実行。実行は[GitHub Actions 37185068452](https://github.com/rinsakamo/relay-theory/actions/runs/37185068452)、実行ログを実閲覧。試行は**PDF直URL HTTP400、Cell/ScienceDirect PDF HTTP403、linkinghub戻りHTMLが完全原著の肯定認証不能**に分類。対象3件の本当の出版者版PDF/完全HTMLは依然取得なし。BLF-01とINT-01は出版社の検索索引にOA表記があるが、HTTP403を可用な原著と誤認しない。

実行に用いたソースは `g2_second_official_source_rescue.py`、隔離Workflow `p399-g2-second-source-rescue.yml`。成功がゼロだった二次probeメタデータのrunner SHA-256 `e304b0c8625e926056c71065829d4e53dafc538fff9646e22d187e35c7ee54de`、実ジョブ111385180623。著者稿、PMCID記事、bioRxiv稿、出版社とは別のサイトを原著にする操作はしていない。

## 正確な未完了と外部同期

| 審査項目 | 現時点 | 保守的意味 |
|---|---:|---|
| 主候補の唯一DOI | 40/40 | 24 component + 16 integration 作業名簿変更なし |
| 出版社オリジナルPDFのactual raw byte SHA receipt | 30/40 | v3より追加バイトハッシュなし |
| 出版社公式完全PDFブラウザ新規可視原著 | 2件 | CNC-01 15pp、INT-04 20pp。生SHAはまだない |
| 別枠既存出版社完全HTML-only原著 | 3件 | ATT-01/MEM-01/INT-03（v2から維持） |
| 重複のないfirst-party original full mediaアクセス | **35/40** | raw PDF30 + HTML-only3 + browser PDF2 |
| 本当にアクセスが未解決 | **5/40** | LRN-01、PRD-01、ATT-03、BLF-01、INT-01 |
| 版/訂正/全数学/全モデル変種/負例の完全科学的原著採用 | **0/40** | アクセス実績から科学審査PASSを推論しない |
| 中央family独立性科学的承認 | **0/40** | 780+暫定800ペア未裁定 |
| 事前客観的バックアップ発動 | **0** | 欠落だけで恣意的差替え不可 |
| 最終合同科学凍結・MAIN着手権限 | **なし** | G4新規再監査および著者明示的承認が必要 |

G1他担当の独立スナップショットを2026-10-04 UTC 07頃HEAD `5ac0803dcb3d859ac396e83fd0806bd809472d03`で検証：P09も限定的科学的正式資格、先行PF01～04/P07と計**6/20**。未実施14件・最終20名簿未凍結。最終family照合は発行済みのG1最終名簿に対して別途行う。G3は独立責務、G4最新版の新規承認なし。全v4は**append-only**でv3マニフェストの40 DOI順・置換0を保存。

**次に必要:** LRN-01の出版社原本の手動アクセス・Nature直接媒体再評価、PRD-01購読許可または事前合法的に定義された原著媒体・図訂正後の実画像審査、Elsevier系3件の出版社現物取得・公式取得不能時の結果非依存バックアップ審査。さらにアクセス済み35件も全て数学/figure/variants/negative/source-native ancestryの個別監査が必要。成果に影響されるMAIN選択や早期科学的分類は禁止。
