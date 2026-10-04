# PRD-C 独立監査・実行ログ／正常系・異常系履歴（追記資料）
2026-10-04 JST。元HEAD = 69748673c80f421605f1c63607472903ac2ed68c、元branch = paper2/p399-g2-outcome-blind-main40-working-20261004、独立branch = paper2/p399-g2-prd-c-independent-20261004。作業開始時に#399・Draft #419/#420/#418、G2 v4/v6/v7/v8a、backup_priority v1、G1 v6の実ブランチ・原資料・旧raw receiptを照合。旧v1～v8証拠を書き換えず、PRD子dirとPRD専用workflowsのみ追記。元MAIN40と#398、Grammar v0、PF01–04の公式科学判断・他lane成果物に無変更。

## 出版社原本の実物受領 — 出版社PDF原本のSHA
* PRD01 10.1038/s41562-024-01930-8：出版社正式本文/訂正済完全原著の新規物理取得0（正式訂正2024-08-08の記事テキストのみ再照合。訂正通知を原著と数えず）。
* B1 10.1371/journal.pcbi.1010740：旧v6既存 32頁／3,306,881B／SHA 9c17c00fba0985f6f66b8520c6fc971ae5a2c6d3e1bac266d9fba2739c9792fe。新独立原本再取得 37191084857、37191127360、37191344471で全一致。正式PDF p0題名・DOI画像+重要原著モデル/数式/負例画像を肉眼確認。公式同論文HTML本文DOI一致。前回pypdf連続DOI検出失敗の実観測を偽陰性と確定したが、歴史的な失敗受領は削除しない。
* B2 10.1371/journal.pcbi.1009557：旧v7既存 39頁／2,306,402B／SHA 7b6e4192bfe1b60d794d197e14822997b77d22e437db89850fc4cddcb79482db。新独立原本再取得 37191260135、37191344563で全一致。正式PDF p0 DOI/題名画像＋源重要数学/図の選定画像を肉眼確認。前回pypdf先頭DOI偽陰性記録はそのまま保持。
* 比較選定主候補PRD02（既存G2受領）12頁／815,804B／SHA 0e812158b939a8eb78cbe84cbbf731058a67b9c79fb612ad5722dea65043fc2f、PRD03（既存G2受領）20頁／2,141,209B／SHA d12dfd455fbbd43a5580a0a349f0dd9b9439a0f914eabc026a90f3ae0b80452a。旧実取得記録を引用し、再取得を行わない。PRD02/03の全原著数式/全系譜の新しい完全科学admissionは主張しない。

## 正常系／失敗を区別したCI
* B1専用publisher page-source success: https://github.com/rinsakamo/relay-theory/actions/runs/37191084857 （表紙）、https://github.com/rinsakamo/relay-theory/actions/runs/37191127360 （主モデル式Table2/fig等）、https://github.com/rinsakamo/relay-theory/actions/runs/37191344471 （Fig6–13の重要ページ追加）。初回以降の再実行は必要な「未視覚検査の決定的数学/図」という正当な追加目的あり。取得時原著ハッシュ不変。
* B2条件付きpublisher page-source success: https://github.com/rinsakamo/relay-theory/actions/runs/37191260135 （同一原本/先頭頁）、https://github.com/rinsakamo/relay-theory/actions/runs/37191344563 （Eq1/5–10/15–17、Fig4/6の選定原本画像）。source証拠の機械的PASSは完全科学認証や二重予約の解放を意味しない。
* B1追加control Eq(1)–(3)を含む可能性のあるp0=9の追加視覚検査 https://github.com/rinsakamo/relay-theory/actions/runs/37191486794 はattempt 1/2の双方が、HTTPS公式出版社側 HTTP 502 Bad Gatewayで原本取得前に停止。レーンコードの改変による偽PASS処理も、過去の成功runの上書きも行わない。追加p0=9ピクセル検証は未証明のまま別項目HOLD。ただし旧成功runで本体の原著Table1のposterior式とp0 12–15主要計算は実ピクセル監査済み。公式PLOS完全HTMLのEq(1)–(3)説明は補助的source-nativeテキスト参照。無意味な第3同一リトライをせず停止。
* 確定原著元byteをプロジェクト公開gitへ再配布せず、対応するGitHub Actionsは原著raw SHA/サイズ/頁数、抽出ページSHA/ページラベルと選択original-pageピクセルのログ（短期Artifactsおよび実workflow log）を残す。raw original SHAは先行G2不変JSONとこのPRD-C判定JSONに二重記録。
* 機械可読PRD-C JSON と独立検査scriptで、元40 slots unique、元PRD-01/02/03 exact DOI、最初のrank 1 B1/rank2 B2、偽の訂正全文認証・不利結果削除・DOI SHA偽装・黙示バックアップ発動・G1最終凍結捏造・MAIN GO捏造を拒否。初回実テスト https://github.com/rinsakamo/relay-theory/actions/runs/37191445749 は11/11破壊的陰性PASS。チェックの可読性改善後の独立本実行 https://github.com/rinsakamo/relay-theory/actions/runs/37191655342 も同様にPASS。これらは科学適格性や意味レベルの独立人間査読を検査するものではない。

## 凍結していないもの
Nature訂正版フル原著・比較図、B1スタンドアロンS5/S6全実画像、B2全39頁および全Method数式・陰性の網羅、PRD02/03本体全数学と祖先、G1最終20系譜、全PRD中央family、元MAIN40最終科学名簿/合同プロトコル。原著モデルの限定技術的存在YESと、主枠の予測系譜要件適格性・MAIN採用YESとは別。G2統合担当へHOLDを提出、修正後の原著アクセス・事前基準判断を待つ。
