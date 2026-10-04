# PRD-C：PRD-02 / PRD-03およびG1とのsource-native中心モデル系譜・未決一覧
2026-10-04 JST。MAIN科学のGrammar分解、H比較、既存の予備MAIN結果の閲覧は一切しない。系譜の暫定比較は正式出版社本文に現れる研究対象の演算・採用済み先行手法に限り、全体独立性を先行認定しない。

## 確認した同一出版者原著
PRD-02 Acuña & Schrater (2010), *Structure Learning in Human Sequential Decision-Making*, DOI 10.1371/journal.pcbi.1001003、出版社 https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1001003 。元G2選定原著PDF取得 receipt 12頁／815,804B／SHA 0e812158b939a8eb78cbe84cbbf731058a67b9c79fb612ad5722dea65043fc2f を尊重し、取得を再実行しない。本文公式HTMLに明記された主モデルは、複数アームの報酬確率間に依存構造があるか（独立、結合、ほかの候補構造）という仮説のベイズ証拠更新と、この構造信念を報酬価値と選択に反映させる計算。固定した独立/結合構造モデルとモデルフリーQ-learning+softmaxを対照。単なる刺激sequence予測ではなく、報酬構造を推定しつつ探索・選択する作用。原文は結合状態の行動を説明するが、独立条件には説明不足の残留を報告している。Bellman/確率更新の正確な全式ピクセル・全先行引用・全negativeは本PRD-Cの既存旧G2 receiptとは別に最終科学admissionが必要。

PRD-03 Ahilan et al (2019), *Learning to use past evidence in a sophisticated world model*, DOI 10.1371/journal.pcbi.1007093、出版社 https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007093 。元G2選定原著PDF取得 receipt 20頁／2,141,209B／SHA d12dfd455fbbd43a5580a0a349f0dd9b9439a0f914eabc026a90f3ae0b80452a。出版社公式本文に主モデルの隠れた課題試行状態に関するHMM/遷移行列、frequency/price観測likelihood、過去証拠の不完全保持・forgettingを利用したオンライン状態推論が記載される。行動実験と推定の不一致は別々に残す：短反応分布の近似は6人中5人、frequency/price/durationのすべてを完全説明したのではない。著者が表すHMMの状態・履歴信念は、PRD02の報酬依存「構造そのもの」を仮説として学ぶモデルと厳密に同一とは証拠上認められない。しかし双方がBayesian familyを共有し、祖先引用と他MAINとの交差が全完了するまで中央family独立はHOLD。

## 事前第1・第2候補の演算との暫定源対照
| 原著 | 公式原著から読み取れる中心演算 | 共通祖先・未証明項 |
| --- | --- | --- |
| 元PRD-01 Nature Sharp & Eldar | 公開抄録／原題に適応的なforward/backward prediction、正式訂正された基準確率。完全な出版社原著数式なし。 | B1/B2と元原著との厳密数学的非同一性・直接祖先を判定できない。 |
| PRD-02 PLOS Acuña & Schrater | 報酬生成構造に関するベイズ仮説＋意思決定。 | 一般Bayesian model selection / RL/optimal controlと祖先共通。 |
| PRD-03 PLOS Ahilan et al | 課題状態HMM posteriorの時間更新、過去証拠forgetting。 | 一般Bayesian filtering/HMMと祖先共通。 |
| PRD-B1 PLOS Fassold et al | 既知ターゲット付近のmotor Gaussian prior × 試行固有proprioceptive posterior、期待得点最大のconfidence circle。p0 11–15で原著数式・3変種視認。 | 一般ベイズ感覚統合・期待効用の祖先が既存。PRD02の構造学習でもPRD03のHMM-state filteringでもない作用だが、familyを確定せず、何よりPRD prediction席への適格性HOLD。 |
| PRD-B2 PLOS Lange & Haefner | 感覚posterior分布コードの信念変動微分→学習タスク依存の神経共変動という解析的予測。 | Bayesian coding/sampling祖先が既存。神経posteriorのsignatureは順/逆方向sequence predictionではない。BLF/LRN共有予約有り。 |

本表の「演算差」は「完全に独立の第三系譜」を意味しない。モデルの新規部分と、既存神経表現・prior・ベイズ更新・行動選択を継承した部分を混同しない。全モデルの親論文引用DOIの完全集合の確定と数学的中心メカニズムの統合審査は、G2統合者が全PRD対象と関連統合レーンを一貫して比較すべき課題としてHOLDする。

## G1との限定交差
読み取ったG1 Draft #418科学分母は旧PF01–04 + P05/P07/P09/P13/P14 = 9/20個別限定QUALIFIED、新規11件は未実施。G1のPRD P17 DOI 10.1371/journal.pcbi.1009738 は初期観測固定の感覚情報に基づくchange-of-mind accumulator、P18 DOI 10.1371/journal.pcbi.1008552 は将来のmodel-free行動傾向を内包するreflective model-based plannerで、両方とも原著を取得済みでも科学PRE_A→E未了。直接「予測」という語が似ることによる一律重複/独立判定はしない。追加P13はBayesianカテゴリrun-length学習、P14は観測系列のngram/chunk code compressionで、PRD-02の構造学習という広い語と重なるが対象内の実更新・祖先を最終比較するまで保留。旧PF01–04の資格範囲・数値例外も維持。

G1全20科学的名簿の資格・最終代替が未凍結であることから、任意のB1/B2・PRD02/03対G1全組み合わせの中央独立PASSは**HOLD**（正確な全体照合は20×40=800ペアであり、PRD-onlyの20×3の個別対比もこの未決条件に含まれる）。現時点のexact DOI重複0はcentral family独立の証明ではない。BLF/LRNとのB2共有候補の正式予約同期もG2統合者が行う。PRD席採用0、MAIN不許可。
