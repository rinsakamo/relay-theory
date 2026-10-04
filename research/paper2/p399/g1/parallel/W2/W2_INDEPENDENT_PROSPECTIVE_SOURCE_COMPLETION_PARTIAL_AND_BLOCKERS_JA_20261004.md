# G1-W2 独立原著科学処理・中間固定報告（2026-10-04 JST）

> **実測状態：W2_PARTIAL / P11・P12・P17 新規個別資格 0/3 / G1共通分母変更なし 9/20 / MAIN_NOT_AUTHORIZED。** 取得済み原著PDFは正式科学資格ではない。各論文PRE_Aに不足する原著証拠があるため、PRE_A/A/B/C/D/Eやafter-E資格の達成を偽装しない。W2単独で共同G1の全体分母・公刊多様性・モデル独立性は認定しない。

## 厳格な起点と隔離

Issue #399 / Draft PR #418 / G4 Draft PR #420 / G2参照 PR #419を確認し、共通G1の原著固定チャーター `G1_FOUR_PARALLEL_SCIENCE_LANES_FROZEN_COORDINATION_CHARTER_v1.json` が存在する完全一致の指定コミット `38c5eb24c61b9e57371084a65fcbcb9fb9c62a4b` から `paper2/p399-g1-w2-ctl-prd-diversity-20261004` を新規作成。W2専用ディレクトリと一意のW2 GitHub Actionsのみ書き込み。PF01–PF04、既資格P05/P07/P09/P13/P14、共有v1–v6台帳、Grammar v0、別の#398、G2/G3/G4、および他のWレーンの科学成果は未変更・未取得。

## 対象別の実際の結果

### P11 CTL — 取得と原著限定の機序確認

原著は Rac-Lubashevsky & Frank (2021), DOI `10.1371/journal.pcbi.1008971`、PLOS初刊24頁。過去の独立原著PDF受領記録と、新規CI [37191315123](https://github.com/rinsakamo/relay-theory/actions/runs/37191315123)・[37191407280](https://github.com/rinsakamo/relay-theory/actions/runs/37191407280)で **2,332,597 B / SHA256 `9291d8bca264a2216467e2254dede69dda71232708d94d10619f6d253458d022` 一致**。同時に出版社のS1〜S4原著図 TIFFおよびS1 Text DOCXの計5資料を物理再取得し、各原著生SHA・寸法・文書件数を記録。独立CIの画像描画で原著PDF p2/p5/p8/p11/p14/p17/p20、S1図、S3図の実画像を直接確認。原著全文HTMLは発行元PDFとはバイト同一を主張せず、本文表現と負例を並行照合した。

原著固有の構造はPBWM由来の選択的input/output/response gate、reference-back-2実験の3操作、独立EEGの時間的に部分重複するGLM指標、表現の条件付き復号、行動RT/誤答、別途フィットの階層DDM境界`a`・ドリフト`v`・非決定時間`t`。直接測定の行動・EEGとDDM推定パラメータを区別。原著は後尾RT量的フィット差、条件別ドリフト変動、EEG皮質基底核回路の直接局在不能、時間依存ドリフト/閾値モデル未試験を含む。先祖 PBWM/Frankと当該研究固有の新規実験を混同せず、G2 CTL-02/INT-12を中央系譜確定とは宣言しない。P17とのDDM用語共通だけで同一中央モデルとはしない。

**停止理由：** 原著Fig7とS4の独立ピクセル照合、取得はしたS1 Text全4,767文字の陰性所見精読、完全な補正史・直接先祖の厳密監査が未完。補充目的の新CI [37191492634](https://github.com/rinsakamo/relay-theory/actions/runs/37191492634) は発行元一律HTTP502、[37191592934](https://github.com/rinsakamo/relay-theory/actions/runs/37191592934) の先の正真正銘出版社転送URL直接再取得はHTTP403。旧成功CIを取り消さず新失敗も保全。**PRE_A源証拠不足／A〜E未実行／新規正式資格なし**。詳細・個別SHA：`p11/P11_ACTUAL_PUBLISHER_ORIGINAL_INTAKE_AND_PENDING_REVIEW_v1.json`、`p11/P11_ORIGINAL_SOURCE_REVIEW_AND_PRE_A_STOP_v1.json`。

### P12 CTL — 主論文の正しい別個扱い

Lieder et al. (2018), DOI `10.1371/journal.pcbi.1006043`、2018-04-25 PLOS正式原著27頁。CI [37191423786](https://github.com/rinsakamo/relay-theory/actions/runs/37191423786) で **2,864,504 B / SHA256 `17368c69624bc5e968ccd2f3cc5eeb349070801e3b240cbc50a66d770bae2370` 完全一致**。出版社原著PDFの式(5)〜(9)実画像と原著本文により、環境が与える報酬と規範EVC、学習されたLVOC近似・実際の行動反応を区別。特徴・制御強度・交互作用・遅延・制御コスト、ベイズ的近似重み学習と事後標本の制御信号選択を個別に確認。反例は特徴の線形加算近似が非線形報酬文脈で誤選択/過努力を予測する点、RWおよびWSLS比較の適用範囲、既存行動データの再分析と脳内実装の区別。

**重要な停止理由：** PLOS原著が明示する定義的S1数学原文（学習更新式1〜7）とS2 EVC/rational metareasoning統合数学の原資料未取得・未読。S3 neural implementationは仮説であり実証脳機構と混同禁止。[37191483782](https://github.com/rinsakamo/relay-theory/actions/runs/37191483782) の再試行で出版社HTTP502、仮想の別版GCSパスはHTTP403で、実際の補足原著とは認定しない。歴史的 `rev=1` の uncorrected proof 表示を正式原著版と混同しない。G2 CTL-01による当該DOI原著の引用リンクは直接源関係の存在であって同一中央モデルの証明ではない。PF02・他CTLとも完了した独立性審査ではない。**PLOS原著候補を維持、eLifeによる置換なし、PRE_A保留／A〜E未実行／新規資格なし**。詳細 `p12/P12_ORIGINAL_SOURCE_REVIEW_AND_PRE_A_STOP_v1.json`。

### eLife P12非PLOS代替（科学と調整を分離）

Jiang/Wagner/Egner, DOI `10.7554/eLife.39497`、出版社正式PDF v3/23頁、2018-10-19更新VoR。2018-08-16 accepted → 2018-09-06 VoR → 2018-10-19 updated VoRを出版社の版履歴で独立確認。原著v3 **1,480,961 B / SHA256 `c2adddf8d232d851d9decbb304fb02107686cf55a5dad4cbbfd8b0fd7ac7d64a`** は独立再取得 [37191423786](https://github.com/rinsakamo/relay-theory/actions/runs/37191423786)と [37191483782](https://github.com/rinsakamo/relay-theory/actions/runs/37191483782) で一致。専用原著図描画 [37191629215](https://github.com/rinsakamo/relay-theory/actions/runs/37191629215) で当該v3 PDF実画像p3/p5/p7/p10/p13/p16/p19を確認。ただし同CIのP11 S5別ステップはcontinue-on-errorのHTTP403であり、緑の総括CIをP11成功とは数えない。

eLife原著機序は内部の直近履歴予測 `P_int`、実験外部cueの `P_cue` を `P_joint=(1-beta)P_int+beta P_cue` で統合し、事前/事後予測切替要求と行動・fMRI多変量符号化を関連付けるモデル。実験上履歴は規範的予測に不要であること、単なるROI関連を独自の機構因果証明としないこと、task-set再構成と干渉低減を完全識別しないことなどの不利点を保持。P12の計算価値学習LVOCとは表面的CTL用語以外の数学的中心は異なる可能性が高いが、EVC共通先祖の詳細を含め中央系譜の最終独立性を認定しない。PF02等も未完結。

**科学判定：`BACKUP_UNRESOLVED_EVIDENCE`**。v3の公式補足・Fig supplement・訂正有無およびv2→v3更新箇所の原著版差分をまだ閉じていないため、潜在的非PLOS性だけで科学資格を認定しない。

**独立した調整判定：`BACKUP_BLOCKED_BY_CROSS_LANE_RESERVATION`**。同じ原著がG2 CTL-B2・INT-B2の二重予備登録にある。同じDOIをG1/G2で採用すれば同じ原著の厳密重複。現時点は双方とも予備であり実選定重複が発生したと偽らない。G1 eLife採用数0、出版社多様性の実績増加0、既存P12原著は維持。正式な科学源検証、全レーン調整とowner明示承認までいかなる置換もしない。詳細 `eLife/P12_ELIFE_39497_PROSPECTIVE_OUTCOME_BLIND_CONDITIONAL_ASSESSMENT_v1.json`。

### P17 PRD — 主論文の取得と候補機序

Turner et al. (2022), DOI `10.1371/journal.pcbi.1009738`、2022-01-13 PLOS正式原著16頁。CI [37191423786](https://github.com/rinsakamo/relay-theory/actions/runs/37191423786)で **1,551,349 B / SHA256 `e2d28aea56a31501db49aa791158f18771ae3054748d331df2ec26817f16f305` 完全一致**。原著図1/3およびモデル対照から、独自の初期感覚snapshot依存・試行間ドリフト変動を含む継続的蓄積モデルと代替変種を予備的に分離。実験観測4名、刺激13.33msフレーム、修正/誤修正を含む反転23.91%、初期応答正解66.95%・最終80.10%は原著報告値であり本研究で再実験や数値再現をした値ではない。最初のフレームの予測失敗やドリフト変動無効の代替モデルの原著の負例を保存。運動/反応観測トレースとモデル潜在蓄積変数を区別。P11の推定HDDMと同一中央モデルではあると断定しない。G2 PRD実在候補も元の参照関係のみ比較可能で完全独立は保留。

**停止理由：** 正式原著が明示するS1〜S6 PDF（混合モデル、個人別結果、モデル予測・フィット、競合早期証拠条件）の全文取得・解析が未了。取得時のPLOS HTTP502、非検証GCS 403を失敗として残す。正式なモデル変種と負例が別資料にあるため**PRE_Aを無条件凍結せず、A〜E未実行／新規資格なし**。詳細 `p17/P17_ORIGINAL_SOURCE_REVIEW_AND_PRE_A_STOP_v1.json`。

## 実測CIとstage chronology

| CI run | 実測状態 | その実際の意味 |
|---|---|---|
| 37191224175 / 37191278577 | FAILED | P11初回PDFテキスト断片アンカー過剰厳格・検証器改修の経緯を保全。科学源変更なし。 |
| 37191315123 / 37191407280 | SUCCESS | P11原著24pp・5点出版社サプリ実取得・一致、後者は一部原著図の実描画。A〜Eではない。 |
| 37191423786 | SUCCESS | P12/P17/eLife原著PDFの実SHA・ページ数再一致。正規表現の補足発見不備は別途修正。 |
| 37191483782 | FAILED | 改修補足発見再試行がPLOS HTTP502。eLife原著v3再照合自体は成功。 |
| 37191492634 | FAILED | P11追加決定図取得時PLOS原著・全補足でHTTP502。以前の原著実取得PASSを無効化しない。 |
| 37191592934 | FAILED | P11出版社転送署名のないGCS直URL HTTP403。新しく取得したという主張はしない。 |
| 37191629215 | SUCCESS（mixed step） | eLife v3原著追加実図描画に成功。P11 S5ステップ失敗はcontinue-on-errorで別途保全。P12/P17無署名GCS各HTTP403。 |

**W2正式科学stageコミット：PRE_A凍結0、A0、B0、C0、D0、E0、post-E科学源・履歴独立PASS0、正式個別資格0。** W2原著取得・スコープ付き予備機序調査と上記正直な停止レポートのGitコミットは正式ステージコミットとして流用しない。将来、未取得の必要原著・原図・版差・補正と原著由来の不利事実を証拠付きで閉じた場合にのみ、その論文のPRE_Aから論文別の6つの独立段階を新しく順番通り実施できる。

## 出版社多様性と統合ゲート

凍結共通G1の **9/20** は過去のPLOS初刊原著のみ。今回W2の新規個別資格潜在統合差分は **+0**。検討eLifeは異出版社の本物の原著v3を入手できたが、重複予約・科学源の未完全審査・author未承認のため資格取得数にも異出版社分母にも加算しない。G2個別採用科学ステージ・出力・Grammar/H0/H1/H2は未閲覧・未処理。

**G1_PARTIAL / MAIN_NOT_AUTHORIZED継続。** W1/3/4科学stageを先に見ること、共有v6台帳を更新すること、P12 eLifeの自動採用、G1全20件やG2最終独立性の宣言、共同MAINへの承認はすべて行わない。

## 次に必要な実証

P11は取得済み原著の不足図とS1 Text原著負例の実読・訂正系譜、P12は数学的必須S1/S2、P17はモデル比較原著S1〜S6、eLifeは公式v3補足・版差・訂正史とG2二重予約の独立owner解決。その後初めて各々の段階凍結、独立after-E発行元原著/コミット祖先CI、別個の限定資格審査を実施できる。
