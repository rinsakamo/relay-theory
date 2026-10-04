# RelayTheory Paper 2 G1-W2 — 独立科学処理の追補最終報告（2026-10-04 JST）

**W2個別原著の限定的資格：3/3（P11、P12、P17）。共通G1既存分母は9/20のまま変更なし。将来のG1調整統合候補のみ +3。異出版社の正式採用：0。G1_PARTIAL / MAIN_NOT_AUTHORIZED。**

この報告は旧 `W2_INDEPENDENT_PROSPECTIVE_SOURCE_COMPLETION_PARTIAL_AND_BLOCKERS_JA_20261004.md` を削除・書換えせず、当時の真の未完了履歴を継承する追加完了記録である。Issue #399、PR #418/#419/#420、凍結済四分割チャーターに従い、唯一の指定コミット `38c5eb24c61b9e57371084a65fcbcb9fb9c62a4b` から作ったW2専用分岐だけを変更。W1/W3/W4暫定科学結果、MAIN解体・再構築・Grammar結果・H0/H1/H2は閲覧・実行せず、Grammar v0も変更していない。

## 1. 三件の原著別独立科学資格

| 対象 | 凍結された出版社刊行原著 | 必須出版社発行サプリ | 個別資格／独立post-E |
|---|---|---|---|
| P11 CTL | PLOS 24pp、2,332,597B、SHA `9291d8bca264a2216467e2254dede69dda71232708d94d10619f6d253458d022` | 原著TIFF図4件＋DOCX原著S1 Text 1件。5件とも生SHA凍結値一致 | 個別QUALIFIED、当初after-E [37192572210](https://github.com/rinsakamo/relay-theory/actions/runs/37192572210)、追加独立原著6点＋6段階元Gitバイト [37195855150](https://github.com/rinsakamo/relay-theory/actions/runs/37195855150) ともPASS |
| P12 CTL | PLOS 27pp、2,864,504B、SHA `17368c69624bc5e968ccd2f3cc5eeb349070801e3b240cbc50a66d770bae2370` | S1原著ベイズLVC式、S2 EVC/VOC統合式、S3仮説dACC神経モデル。3件DOCX全原著生SHA一致 | 個別QUALIFIED、当初after-E [37192799989](https://github.com/rinsakamo/relay-theory/actions/runs/37192799989)、追加独立原著4点＋6段階元Gitバイト [37195816485](https://github.com/rinsakamo/relay-theory/actions/runs/37195816485) ともPASS |
| P17 PRD | PLOS 16pp、1,551,349B、SHA `e2d28aea56a31501db49aa791158f18771ae3054748d331df2ec26817f16f305` | 発行元正式S1–S6原著PDF全6点。すべて生SHAおよび原著頁数2/3/2/1/1/1照合 | 新たにE別コミット `129d00795aebd859f889a407f1cc4288d993ef61`、別個の限定的QUALIFIEDコミット `479ed26c4104539d3aa8eca74eec5777064cb0c3`。独立原著7点＋原著実ページ1/6/13＋六段階元Gitバイト [37195752076](https://github.com/rinsakamo/relay-theory/actions/runs/37195752076) PASS |

P11／P12の6つの元科学stage introduction commitは各個別資格JSONに記録され、今回新CIはoriginal `git show` bytesと現在のstage raw bytesの一致、各stage一回限りの導入と厳密祖先順を照合。P17は以下がすべて独立コミットで元Git byte一致：PRE_A `68370cf8` → A `7bc50b07` → B `750a7395` → C `ba83e6a9` → D `77f1a434` → E `129d0079`。**各Eそのものは資格を発行していない**。Eの後の別CI実施・合格を前提として、別コミットで限定的資格を発行した。

### 原著固有の実際の機序・不利な証拠

**P11（Rac-Lubashevsky & Frank 2021）**：先行Frank/PBWMの選択的input/output/motor gateという理論的継承と、本研究の独立switch操作、観測RT・error・頭皮EEGの時間経過、推定値である階層DDMの閾値a・ドリフトv・非決定時間tを切り分けた。原著S1 Textの条件別RT／errorの非有意結果、S2/S3密度・尾部fit不足、S4ドリフト変動（aだけではない）を保持。頭皮EEGだけで生体PFC/BGゲーティング回路の因果局在を実証したとは認定しない。G2 CTL-02/INT-12との中心モデル同一／独立は未決。

**P12（Lieder et al. 2018）**：原著数学S1/S2を含め規範EVC・有界計算価値VOC・ベイズ学習されたLVOC近似とその制御候補選択を区別。Worldで与えられる外的実験reward、モデル予測値・posterior sample、人間の実測選択は異なる。線形特徴近似が非線形環境に失敗する原著条件、RW/WSLS等の代替、原著S3のdACC/SARSAはあくまで神経実装仮説という制約を保持。直接先祖Shenhav等EVCと以前のLieder rational metareasoning、G2 CTL-01によるP12 DOI引用は開示、最終中心モデル独立判定は保留。eLifeで元PLOS配分を消去せず、元P12自身の完全別科学取引を終了した。

**P17（Turner et al. 2022）**：Resulaj 2009原著の初回選択＋継続統合＋反対change boundを親機構として明記。本論文固有の最初の感覚frameに直接依存して線形減衰する外的なtrial drift、独立の内的trial drift、瞬間的な刺激雑音・内部雑音を元の出版PDF p13原式・p6 Fig3とS1–S6に照らし、凍結28元A主張・37元関係・8件C1/C2修正・8件PRE_A不利条件の完全対応と原著忠実度11項目をEに記録。独立原著post-Eでは元のp1題名、p6 Fig3の実在モデル変種、p13数学 `externalVar`/`firstFrame`、S1–S6各原著頁と生SHAを改めて確認。完全モデルの予測に対し同分布でも初期刺激との結合を切った変種は **逆符号**、trial driftなしは **初期効果なし**。実測データではむしろ初期frameを除く後続情報と200–400msの情報が強いこと、被験者わずか4名、予測可能な刺激開始、稀な誤正答反転・稀な平均逆証拠の制約を保持。100,000試行は**モデルシミュレーション**、脳内latent DVは**未実測**であり、ボタン応答そのものではない。P11とのDDM語彙一致による中央モデル同一視も、他G2 PRDとの完全独立認定もしない。

**資格範囲**：上記3件すべて、発行元原著を用いた構造／手続に限定。物理ソース＋履歴のCI PASSは人手ブラインド意味査読や原論文のtrial-level統計・数値モデル再推定に代わらない。完全な外部訂正索引不存在は保証できず、科学的実質訂正が新発見されれば再審査。祖先共有の開示は自動的な二重計数確定でも中央モデルの独立証明でもない。

## 2. eLife代替：科学と予約の独立した結論

事前登録済み `10.7554/eLife.39497` はeLife正式更新VoR v3（2018-10-19）、23頁、1,480,961B、発行元原著生SHA `c2adddf8d232d851d9decbb304fb02107686cf55a5dad4cbbfd8b0fd7ac7d64a` が実取得一致。最初のVoR v2も別個に取得（SHA `69f4746dd13ba8c04cce0af2277e0d6558a6c60eb8ef523b60900d91bad1c954`）。**v2とv3は生バイトだけでなく抽出全文も実際に異なる**。実際の各更新箇所・決定図のピクセル・v3に対応する全公式個別補足の科学的意味は十分閉じていない。v1 accepted manuscriptの正式ZIP取得成功をv3正式発行版の補足充足と偽らない。HTTP404のv3補足ZIP一括URLは個別図補足の不存在証明ではない。

本体のcue由来予測と過去履歴由来予測の混合と、P12 LVOCの価値学習は、原著自身の数学上、直接の同型と確定する理由は見つからない一方、EVCの引用祖先および周辺関連モデルの最終完全比較は未了。原著の履歴予測が課題外部の正答予測には不要な場合、全脳比較補正後の不検出条件、fMRI符号化の因果機序非同定も保持。

- 科学判定：`BACKUP_UNRESOLVED_EVIDENCE`
- 調整判定：`BACKUP_BLOCKED_BY_CROSS_LANE_RESERVATION`（G2 CTL-B2およびINT-B2同一DOIの二重予約）
- 原P12 PLOSは残存、eLife採用0、予約開放0、異出版社の実現多様性増加0。

出版社が異なるという一点では現行選択基準を変更しない。今後eLifeを正式採用するには原著v3の更新差分・必要公式補足・直接先祖源の完全源資格、G2予約衝突の調整、およびowner明示承認が別々に必要である。

## 3. 検証器の失敗履歴と救済の厳密な境界

- 発行元PDFの過去取得と新規source CIに実際の成功がある一方、以前の出版社HTTP502および期限・署名のないGCS直URLのHTTP403も消さず保持した。
- 新規独立ソースCI [37195358986](https://github.com/rinsakamo/relay-theory/actions/runs/37195358986) のFAILはTIFF magic-string記述の誤り。**原著mainおよび全5補足の生SHAは一致していた**。科学stageを変更せず検証器だけを修正し [37195469643](https://github.com/rinsakamo/relay-theory/actions/runs/37195469643) PASS。
- 新規after-E CI [37195498002](https://github.com/rinsakamo/relay-theory/actions/runs/37195498002) のFAILはC1/C2凍結JSONのファイル名を`PASS_C_`に過剰限定した検証器の誤り。原著6点の実取得＋生SHAは当該失敗runでも成功。科学stage未変更で名前照合だけ修正して [37195628740](https://github.com/rinsakamo/relay-theory/actions/runs/37195628740) PASS、その後独立元Git raw-byte照合とP17決定原著頁チェックを追加した最終CI 3本も全PASSした。
- メタデータだけの共通G1 greenを原著意味査読のPASSには転用しない。新規資格は各原著固有のstage／別post-E成功／別資格コミットでのみ数える。

## 4. 出版社多様性・クロスレーン・次の権限

凍結共通G1既存9件もW2追加3件も、**現時点で正式個別資格を得た原著はPLOSに限定**されている。eLifeは非PLOS原著を実取得したが**採用には至らず、科学的・調整上の代替候補のまま**。現時点の客観的な異出版社diversity達成は0。W2単独の計3件を共通G1の9/20へ直接足した新たな公式12/20とは宣言しない。

次段階はG1コーディネータが4つの独立Wレーンの凍結資格と原著元祖系譜を競合に注意して順次統合し、事前要件を満たした場合にのみ共有の新v7以降証拠台帳へ反映すること。G2のfinal 40とモデル関係・eLife予約をその担当者が確定後、G3独立計測とG4新規合同監査を経て、ownerの明示MAIN GOまでは **G1_PARTIAL / MAIN_NOT_AUTHORIZED** とする。

機械可読完全追補：`W2_FINAL_BOUNDED_THREE_SOURCE_QUALIFICATIONS_AND_CONDITIONAL_PUBLISHER_ALTERNATIVE_v1.json`。旧PARTIAL報告は真正の時点履歴として変更していない。
