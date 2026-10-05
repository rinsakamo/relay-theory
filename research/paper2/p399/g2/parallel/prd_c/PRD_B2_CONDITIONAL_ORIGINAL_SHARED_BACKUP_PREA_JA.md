# PRD-C / PRD-B2：条件付き第二順位原著の予備的source-native審査
2026-10-04 JST。第一順位B1の元PRD-01に対する「prediction vs confidence」適合HOLDという客観的障害があるため、登録済み第二順位を**条件付きで科学的予備審査**する。ただしB1の正式不適格判定・B2発動・MAIN名簿変更は実施しない。

原著: Lange & Haefner (2022), *Task-induced neural covariability as a signature of approximate Bayesian learning and inference*, DOI 10.1371/journal.pcbi.1009557、正式PLOS 2022-03-08、https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009557 。正式PDF https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1009557&type=printable 。

## 正式原著の物理受領と視覚監査範囲
前G2 v7の原本（39頁、2,306,402 bytes、生SHA-256 7b6e4192bfe1b60d794d197e14822997b77d22e437db89850fc4cddcb79482db）を独立Github Actions 37191260135、37191344563で再物理取得・raw hash/page/byte完全一致検証。公式完全HTMLの同一DOI/原題確認済み。元v7 pypdf先頭DOI連続文字列不検出をp0画像のDOI目視で解消。原著PDF本体は公Gitにアップロードしていない。

著作元PDF画像として検査した0-indexページは0,4,8,9,11,12,15,18,23（紙面の1,5,9,10,12,13,16,19,24頁）。PDF p0 4はposteriorをコード化する平均発火率と観測sの微分 Eq(1)、p0 8はカテゴリー信念微分の近似 Eq(5)、Fisher的方向とDifferential covariance Eq(6)–(7)、p0 9は共分散Eq(8)とchoice probability Eq(9)。p0 11はモデルに対応するFig4のlikelihood・prior・covariability、p0 12は学習依存のpriorノイズ濾過 Eq(10)、p0 15はFig6内部信念のニューラル推定simulation、p0 23はMethods Eq(15)–(17)を実画像で確認。原著39ページ全頁とMethods全式のピクセル審査を終えたという主張はしない。

## 中心機構・モデル変種・不利条件
原著は、観測Eに対する内部変数xのposterior p_b(x|E)を神経分布コードRで表すという前提の下、課題別の学習されたprior・可変beliefが、感覚神経の微分方向の共変動/選択相関にどう現れるかの解析的予測を導く。独自の数理的予測があるという源限定判定はYES。一方で原著は既存Bayesian inferenceと既存のdistributional/sampling codeを基底として使い、ヒトが順方向・逆方向sequence predictionを適応更新する中心機構を構築・フィットした論文ではない。

作者自身の主要な条件は、仮説課題の内部カテゴリ統計が十分学習された「self-consistent prior」であること、カテゴリ刺激差が小さい/識別threshold近傍、連続微分近似と特定の神経表現の仮定。信念由来変動とlikelihood自身の変動・内因性ノイズは区別し、Fig4では観測Eが一定でもlikelihood形状が変動し得る場合の効果を比較。Fig6のsynthetic-neural simulationは新規ヒト神経実験の直接実測ではない。原文は神経相関の増大が必ずしも課題情報の劣化を意味しないと議論するが、近似・実装独立性や心理物理の限定を超えた証明と取り違えない。

必要な全原著Methods頁・追加独立資料の網羅的科学認証、全負例/全派生モデル数学の完全再監査、全main40・G1原著との前駆family確定は未完。もしPRD席への正式採用検討に進む場合は、その時点で残頁と訂正版、原文Methods式系・source negativesの全件締めと第三者原著監査が必要。

## 候補順位と共有DOIの衝突を解消しない
PRD-B2（このDOI）は同時に既存BLF-B2/LRN-B2として登録済み。初期G2 v8aに発動済みは0、順位1 B1を飛び越える根拠なし。G2のcanonical manifest順と他並行レーンの時点・予約を中央integratorが判定し、同じ1論文を2枠に二重採用させない。さらにB2のposterior neural covariabilityは「予測」という語から元の適応的forward/backward prediction系列に自動合格しない。Q1=限定YES、Q2=HOLD_OWNERSHIP_AND_PREDICTION_CRITERION、全体family=HOLD。新PRD採用0件。
