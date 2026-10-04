# G3 独立レーン handoff v1.0.0 — PRE-FREEZE
**判定: G3_PARTIAL / MAIN_NOT_AUTHORIZED**。対象: #399 の新規 MAIN40 (24 component + 16 integration)。#398旧ロスターは移管しない。main base `3be3267858c0b735ef7da74a876868191664a6e1`。専用 Draft PR #417; PR #416 は READ-ONLY G1/G2 作業台帳、#401 は別の exact-byte validator 未取込案件。

## G3 単独で完了した部分
- 原著定義を出発点にした Reference Object と、別管理する Analyst Packet を区別。original primary は実取得可能な完全文献 PDF 優先、取得・読解できなければ出版社が完全原著とする全文 HTML。命題を成立させる式・図・時間順・否定結果・変種は隠蔽の犠牲にしない。
- 元の source-native R を先に凍結、Grammar 役割に関する別 Role Bridge は **R後・D前** に凍結。元のRが先にGrammar基底から構成されることを禁止。
- 分母は source-native の原著凍結資料と突き合わせる。スコア入力だけで分母を減らした見せかけ FULL をブロック。モデル変種ごとのノード、辺、役割、時間、制約/否定、境界、機構的区別と除外数値を**別々に**記録。構造的FULL≠数値的再現。
- A0 → A1 → A2 は同一ソース課題・予算で比較。source-native の型インタフェース対照がなければ H1、履歴依存対照がなければ H2 は `NON_DISCRIMINATING`。A2失敗だけでは H2にならず、原著由来の既存状態や制御機構を網羅的に検討する。
- 出典で保証されない「独立R2」を拒否。採用 v2.3.1 の A→B→C、C1重複防止と C2局所否定列挙、人間の例外審査は変更しない。#401の原validatorを移植したと偽称しない。
- 7種類の破壊変異＋G_dyn固定弱比較を事前登録。非識別な対照や無効対照は感度の成功数に入れない。ラベル開封前の複数 maximal common images 保持を規則化。

## 実際のテスト
[GitHub Actions 成功 37179072375](https://github.com/rinsakamo/relay-theory/actions/runs/37179072375)、テスト対象 commit `3eaf0b4c8c7089cf7c2ab7e665fbc615eb57c88c`: **69 / 69 Python合成・既知PF限界の手続き互換テスト PASS**。うちPFは公開済・結果既知の補助フィクスチャであり、独立の研究精度検証ではない。実行ソース `evaluate_g3.py` raw SHA256 `eb9153a9a5471424a6cfe940d2fa1f12eb647d53fc85573f624e472c7111ea98`。全バージョン化 JSON/MD の raw SHA256 は `G3_EXECUTION_RECEIPT_v1.json` に格納。本ファイルとreceiptは**記録の追記**であり、参照したテスト対象コミットのコード・スキーマ・フィクスチャを変更しない。

PF01–04の資格書を正式参照で照合。資格は各々、原著を使った手続き/構造の限定合格のみ。PF01の元論文の2数値矛盾、PF02のStemme直接祖先とp33数値、PF03の原著にない厳密ゲートscalar、PF04の**PRE-Aで承認された研究者版 Eq10 omega(a')** と原典数値未検証は、今回の試験でも昇格していない。特定の本物の構造的意味の妥当性、外部独立査定者の能力差、H2の因果的不可約性は測定していない。

## 決定的な未解決条件
1. **G1:** PILOT20全体のmodel-family/出版社/媒体多様性と校正の正式審査。PR #416 は4正式PF+16 discovery-onlyで未合格。
2. **G2:** MAIN40全候補、原著本文の現物版/訂正/実際の可読式、モデル変種、親系統とPILOT衝突、順序固定バックアップの outcome-blind freeze。PR #416の10 seed+30空欄は未合格。
3. **実務的G3/R-P:** G2に実在する最終ソースへ、実査定者の参照・curatorの完全性監査・認識漏洩記録を実施し、合法なソース証拠が実際に保存されること。設計だけで実際に「二者独立」と称さない。
4. **共同承認:** G1/G2のロスターとG3測定/パケット/ラベル非開封比較の規則を共同著者が正式に承認し、#399で明示的な MAIN GO を記録。未完了の間は `PRE_FREEZE/MAIN_NO_GO`。

**独立G3設計・合成テストは完了、共同プロトコル最終凍結は未達。** 既存のPF本論文決定、Grammar v0、旧60主張と凍結comparator、過去の#398結果、未処理MAIN原著には変更を加えていない。
