# PRD-C：PRD-B1の「Prediction vs Confidence」事前選定適格性 — 判定とG2担当への照会
Authority: #399原研究目的・レーンラベル、G2先行凍結ranked backup v1、#419 v6/v7、#420 G4。2026-10-04。原著を採用するための事後的なレーン基準書換えは禁止。

## 明示的に別の二つの科学的問い
**Q1 独自の明示的機構/数理モデルは存在するか: YES（原著本体の限定的実証）**。Fassold et al (2023) DOI 10.1371/journal.pcbi.1010740は、運動前motor prior、運動後proprioception、設定ノイズを区別し、posterior endpointを介して期待得点を最大化する連続confidence-size決定を定義。出版社PDF p0 11 Table2の3候補、p0 12 Eq4、p0 14 Eq5–9、p0 15 Eq10–13が中心定義である。3候補の差はpriorの有無と現在観測の有無という内部演算差である。文言のみの『prospective/retrospective』ではない。先行ベイズ感覚統合・期待効用に由来する数学を全て独自発明したという意味でのYESではない。

**Q2 元PRD-01の代わりの事前PRD第三中心系譜として許されるか: HOLD / 原著からは自動導出不能**。元席はSharp & Eldar (2024)の適応的forward/backward predictionで、Nature正式出版訂正済み全文未取得。B1自身は「リーチを終えた後、成功確信度としてどの円サイズを設定するか」というメタ判断で、原本に試行間forward/backward sequence-prediction更新を主モデルとして提示していない。背景として過去のmotor varianceを用いることと順方向・逆方向予測の機構を同一視しない。完全Nature原本未取得なのでB1と元席の全式非同一性・全系譜独立性も推論しない。

#399はPRDをpredictionとして抽出する8レーンのsampling labelとし、ラベルを自然な不変モジュールと仮定しない。一方、各レーン3つの中央独立familyを事前に選ぶ規則、元席PRD01の基準は適応的forward/backward predictionである。『全ベイズ推論をpredictionと呼べる』という広義化を今回B1の結果を見た後に採用すると選定基準を事後変更してしまう。#399だけから広義confidenceによる第3予測系譜の自動許容を立証できない。G2統合担当・著者には事前解釈の既存客観的条項を提示して判断してもらう。新しい基準を承認する場合は既存の独立検証集合としてではなく、明示的protocolバージョン・G4再監査と結果非依存性を別途審査する。

## 不利結果と比較対象を含む境界
原著n16のbest fitはIdeal5／Retro1／Pro10で、55/60のsyntheticモデル回復、極端なproprioceptionノイズでIdeal4回復失敗、候補外の未知モデルは排除できない。完全な動的prediction学習モデルという主張は原著支持なし。
既存PRD02は報酬系列における構造依存関係の仮説モデルとBellman選択、PRD03は既知タスク内の潜在状態HMM証拠履歴統合。B1とは原本に記述された入力・数式の作用が暫定的に異なるが、Bayesian prior/inference/expectationという共通の技術原祖がある。全文の祖先引用と全MAIN/G1科学採用完了前に中央独立familyを最終PASSにはしない。

## 代替順位の扱い
元Nature出版社出版原著のアクセス障害自体はバックアップ科学審査へ進む客観条件。B1の形式モデルQ1はsource-scope限定YES、PRD席Q2はHOLD。従ってB1を昇格させない。B1が事前条項によって客観的に適格と認められない場合に限り、rank 2のB2を**条件付き審査**する。ただしB2は感覚神経posterior covariabilityで、予測席問題を自動解決せずBLF/LRNと共有。正式な置換イベントはG2統合担当とG4、著者の別権限まで0件。判定不能ならPRD01席は未充足／保留、初回MAINは実施不可。
