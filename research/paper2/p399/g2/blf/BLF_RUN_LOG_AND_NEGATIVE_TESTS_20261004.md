# G2-B BLF 独立実行・異常系ログ（2026-10-04 JST）

## Git evidence chronology（実際にこのレーンで作成）

- 開始G2ブランチ実HEAD: `69748673c80f421605f1c63607472903ac2ed68c`。この1点から新規独立 `paper2/p399-g2-blf-source-family-qualification-20261004` を作成。
- BLF専用の判定記録: `5dff2cd965e85441fa5a5939c5595315b24ea9ed`。
- BLF限定日本語科学資料/原出版社比較: `e32c59321ea71e3c98ba63d91c0b523ae3f7bbe5`。
- BLF-only fail-closed Pythonテスト: `45b913513b5c328cbd7287be1019731bec6a0615`。
- 公開Gitの実コミット済みファイルを`GitHub fetch_file`で個別に再読した後、独立したUTF-8 SHA-256実装を既知標準ベクトル2つ（空列と `abc`）で先に検証し、JSON・レポート・テストのSHAとGit blobを記録した `BLF_INDEPENDENT_RAW_SHA256_READBACK_RECEIPT_v1.json` コミット: `27abb420775d47322451304949083413a9451ba4`。証拠はそのJSONに保存。

## このレーンの実際の独立検証

1. **Git上の実ファイル再読実行**: Pythonソース・BLF判定JSON・報告Markdownの3/3ファイルに対して生UTF-8バイト長/SHA-256/Git blobを確認し、個別受領を記録。SHA-256独立実装の空列およびabc標準ベクトル **2/2 PASS**。
2. **別実のJSONメタデータ安全ガード**: 実際にGit上から再読した判定JSONを入力として正常系 **1/1 PASS**。偽PMC≡出版社版、出版社取得済み捏造、PDF生SHA改変、全19ページピクセル確認捏造、全文数式画素資格捏造、全体family認可捏造、G1全件凍結捏造、B2条件起動捏造、B2重複配分許容、著者GO捏造、中央family全40認可捏造、MAIN実行捏造、12モデルを13と偽る **13/13 異常系拒否 PASS**。この別実ガードはGitファイルの実データで動作したが、コミットしたPython実行と同一ではない。
3. `blf_evidence_fail_closed.py` はPython標準ライブラリだけで実checkoutのJSONを検査する**追加12種類の破壊的回帰テスト**。この記録時点で本PythonスクリプトのGitHub Actions実行は未実施。専用CIが別途実行できた場合は赤/緑のrun IDと科学的制限を追記し、独立JS検証と混同しない。

## 原著アクセス／旧証拠の正確な範囲

- BLF-01: 先行Elsevier正規API HTTP200だがcoredata 1,949 Bのみ、ScienceDirect/Cell正式全文経路は403。今回公開ScienceDirect原著のブラウザ参照も完全本文不可。旧失敗経路の自動再実行数を成功数に換算しない。
- BLF-01 Europe PMCの先行アーカイブXMLはDOI/PII一致／物理生ハッシュあり。正式出版社刊行版バイト一致は未証明。
- BLF-B1: 先行出版社PLOS原本物理受領 run [37186367137](https://github.com/rinsakamo/relay-theory/actions/runs/37186367137)／19p、生SHA `869c8b1a535fcb4a922d677bc0c26ca8959930a7f62208c4bf74701899aa8870`。今回は出版者完全HTML・訂正告知の原著内容を照合、同じPDFの不必要な再ダウンロードはしていない。
- BLF-B2: 未起動の第二候補。以前の専用firstparty媒体取得 [37188410375](https://github.com/rinsakamo/relay-theory/actions/runs/37188410375)／39pは再取得も科学実行もしない。

## 合格基準の制限

このレーンの生SHAテストが証明するのはGitコミット済みローカル**記録のバイト整合性**。既存source runnerの先行受領が証明するのは当時の元PDFの物理取得。どちらも今回の元B1 PDF全19ページのピクセル式/図監査、元出版社補足全検査、全版訂正不存在、BLF-02/G1全体での確定独立性を証明しない。科学的最終判定はHOLD、代替採用0、MAIN NO-GO。

## 追記: 提出後の厳密なPython実CI実測（同日）

上の「記録時点で未実施」という時系列記述は保存する。続いて同一のコミット済みPython検証器が実際にGitHub Actionsで走った。[BLF専用push実行 37191252008](https://github.com/rinsakamo/relay-theory/actions/runs/37191252008) はブランチHEAD `02432849d50042992200ade1c7ae92d4c64ca2ba` に対して**SUCCESS**。ジョブ `blf-pre-a-source-receipts` 内の `Exact newly authored raw UTF-8 SHA256 readback`、`Original-candidate false-promotion rejection only`、`Preserve bounded qualification marker` の全3つの実検証ステップをGitHub Actions job APIでそれぞれ明示的に `conclusion=success` と独立確認。前者は元Gitにある新生成3原資料の実バイトと受領SHA、後者はPythonユニット正常系1および破壊的12系、末尾は元40/0代替/NO_MAIN保護を検査する。**独立JS別実13種類＋実Python12種類を混同して合算しない**。実CI成功は元出版社PDF画素、版訂正完全性および全族独立の科学資格を意味しない。ログ追記コミット後の新HEADは再実CIで別途確認する。
