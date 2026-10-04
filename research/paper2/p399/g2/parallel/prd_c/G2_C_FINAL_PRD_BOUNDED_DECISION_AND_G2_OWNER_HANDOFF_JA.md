# G2-C PRD独立レーン：最終限定判定とG2統合者への引渡し
2026-10-04 JST。Primary #399、G2起点 Draft #419 exact HEAD 69748673c80f421605f1c63607472903ac2ed68c、G4 #420、参考G1 #418。専用branch paper2/p399-g2-prd-c-independent-20261004、専用dir research/paper2/p399/g2/parallel/prd_c/（第2順位物理source pixel scriptだけ並行子dir parallel/prd_b2_conditional/）。PRのtargetは作業開始G2 branch、他4レーンに触れない。

## 8条件別の原著限定監査
| 条件 | 元PRD-01 | rank1 PRD-B1 | 条件付きrank2 PRD-B2 |
| --- | --- | --- | --- |
| (1) 出版社完全原著の物理取得 | HOLD: Nature購読preview | PASS: PLOS raw 32頁3,306,881B exact SHA | PASS: PLOS raw 39頁2,306,402B exact SHA |
| (2) 刊行版/訂正 | Nature正式訂正通知のみPASS; corrected full source HOLD | 同一刊行原著DOI/表紙PASS。全Crossmark履歴未網羅 | 同一刊行原著DOI/表紙PASS。全Crossmark履歴未網羅 |
| (3) 全重要数式/図/variant/負例 | 原著フル未取得HOLD | 中心主文3variant・Eq4–13・Figures6–13選定原ページ＋負例レビューPASS限定。別p0 9追加ピクセルHTTP502、S5/S6独立ピクセルはHOLD | 解析主式と条件付き主要原ページ選択検証PASS限定。全Method/全39頁の網羅審査HOLD |
| (4) 独自明示数理モデル | Natureプレビュー以上はUNDERDETERMINED | YES: 認知行動上の運動成績confidence posterior+期待効用数学（原著限定） | YES: 理論的感覚posterior変動→神経共変動解析数学（原著限定） |
| (5) 元PRD-01のpredeclared prediction席適格 | HOLD original | HOLD: adaptive forward/backward prediction≠pre/post motor confidence自動同一 | HOLD: neural posterior covariance≠適応的双方向予測自動同一 |
| (6) PRD-02/03の中央family独立 | 原著数学欠でHOLD | 元演算は暫定差、共有Bayesian/期待効用祖先・全式/全源の比較HOLD | 元演算は暫定差、既存neural Bayes祖先・全源比較HOLD |
| (7) G1最終20のfamily独立 | HOLD（G1 9/20） | HOLD（同） | HOLD（同） |
| (8) 重複・予約 | 元PRD01席保持 | rank1登録のみ／未採用 | rank2、BLF-B2/LRN-B2と同一DOI、共有・順序調停HOLD、未採用 |

## 分母（独立した計数対象を混ぜない）
1. 当レーンで今回source raw物理再取得済み・過去の不変SHA照合済みのスタンドバイ出版社完全原著：**2 distinct PDF（B1＋B2）**。本命PRD-01の出版社完全原著：**0件**。出版社訂正通知は別の1通知、原著数に足さない。
2. G2の他の既存SOURCE取得履歴を尊重するPRD-02/PRD-03正式PLOS原著：**以前の受領2件**、本レーンで理由なき再ダウンロードは0。
3. 原著中心数理モデルの限定的な存在を肯定できたスタンドバイ：**2候補**（B1とB2。ただしB2は条件付きで原著全式監査未完）。本命PRD-01は本文数学未読なので論じない。
4. 元PRD-01に代わる、事前PRD基準・3つ独立中央family・G1全体の全条件を科学的に通したバックアップ：**0候補**。正式採用・40名簿変更：**0件**。
5. 元40の他39の科学資格や全MAINのGOにこの限定監査から加算する論拠なし。G4旧MAIN_NO_GO継続。

## 決定事項を所有者へ上げる
* 著者/機関（許可された経路のみ）: Nature改訂済完全正式出版社原本を確認できるか。取得できればFigure2a/4aピクセルの出版版本体対照、全数学/モデル変種/負例の網羅的原文再審査を新receiptとして実行。単独訂正通知、第三者稿、第三者転載を出版社正式原著に格上げしない。
* G2統合担当/著者: 本来のPRD predictionサンプリング事前定義がB1のmotor performance confidenceを予測第三familyとして許容する既存客観条項を示すこと。現在の候補結果を根拠にレーンを再定義してはならない。許容できなければrank1を理由付き保留/棄却し、必要な場合に限りrank2を予約・系譜含め審査する。候補がなくても都合のよい新候補を後付けしない。
* G2統合担当: PRD02/03の全出版社原著数学/全family ancestorレビュー、最新主MAIN40間とPILOT20との中央family、B2のBLF/LRN予約状態を全レーン共同整合。観察時G1は9/20で全20凍結待ち。仮の0 exact DOI一致は全family独立PASSではない。
* G4独立監査 → #399著者の明示GOと別の初回MAIN承認なしに科学的MAINを走らせない。最新PRD専用Draft PRのmergeもMAIN GOとは無関係。

## 監査パケット案内
- PRD01_PUBLISHER_CORRECTION_AND_BLOCKED_ORIGINAL_JA.md
- PRD_B1_ORIGINAL_MATH_VARIANTS_NEGATIVES_PIXEL_SCIENCE_JA.md
- PRD_B1_PREDICTION_VS_CONFIDENCE_ELIGIBILITY_OWNER_HOLD_JA.md
- PRD_B2_CONDITIONAL_ORIGINAL_SHARED_BACKUP_PREA_JA.md
- PRD02_PRD03_G1_SOURCE_NATIVE_GENEALOGY_BOUNDED_JA.md
- PRD_C_INDEPENDENT_RECEIPTS_RUNLOG_AND_FAULT_CHRONOLOGY_JA.md
- PRD_C_BOUNDED_VERDICTS_AND_OWNER_ESCALATIONS_v1.json（機械限定判定）
- prd_c_source_pixel_probe.py、並行子dir b2_conditional_pixel_probe.py、prd_c_safeguard_check.py、専用GitHub workflows（main/prior他lane無影響）。

特にサイエンス分母は、取得の成功・source-native数学の限定的存在・PRD席全条件科学資格・正式置換を別のカウンタとして維持する。
