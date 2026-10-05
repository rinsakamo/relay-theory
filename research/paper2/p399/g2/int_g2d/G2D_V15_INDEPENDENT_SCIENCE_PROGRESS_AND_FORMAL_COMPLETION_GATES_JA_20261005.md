# G2-D v15 — INT原著の独立科学監査増分と正式資格化の残留停止条件（2026-10-05 JST）

**厳密な現在判定：G2D_BOUNDED_PROGRESS / GLOBAL_HOLD、MAIN_NOT_AUTHORIZED。** 旧版が誤りであったという歴史の改竄はしない。G2-D Draft PR #430だけに科学証拠と停止台帳をappend-only追記する。主G2の40件名簿、他G2/G1/G3/G4、Grammar v0、#398、予備MAIN成果は未変更・未閲覧であり、正式バックアップの発動ゼロ。

## 1. INT-01：ユーザーから提供された元出版社ScienceDirect MHTを実際に再監査

- 学術対象：Li & Collins, *Cognition* **254（2025）105967**、DOI **10.1016/j.cognition.2024.105967**。公式出版社公開検索面 [ScienceDirect原著](https://www.sciencedirect.com/science/article/pii/S0010027724002531) と PubMed刊行元情報（PMID 39368350）で論題・DOI/PII・巻号・著者が一致。出版社への本実行環境での新しい直接raw HTML成功やraw PDF成功とは**言わない**。
- 実提供MHT 5,754,741B、SHA256 `32158948f6d1f4ffd7170393c30a5742ce7db1b0a871928f64bd176cf9ab3b64`。MIME内唯一の当該原稿本文HTML 1,250,747B、SHA256 `0c6c2670f715b06e3a9596cf848df9e08bb5b5168d5dd57113730d3d50b8fc52`。独立再読取で従前v14記録と原本同一、Chrome/Blink出版社スナップショットである。新しい原著HTTPレスポンスSHAや出版社PDF署名と混同しない。著作権保護原著MHT/画像/PDFは公Gitへ保存しない。
- 本文５章（Introduction/Methods/Results/Discussion/Conclusions）、本文内に完全な**Appendix A Supplementary Methods / Appendix B Supplementary Figures**、Fig1–7とFigB.1–B.8計**15図**、本文**Algorithm1, Algorithm2の印刷版ビジュアル**、**表2**を確認。該当HTMLで実参照されている**47件の記事特有の画像SRCが全てMHTのMIME内に存在**、元図JPEG15・本文内数式／記号JPEG26、計41個のJPEGを形式デコード。15図すべてのアーカイブ画像を独立にcontact sheetへ整列し原画像として目視確認、**ただし各パネルの高解像ピクセル完全数学意味査読ではない**。Algorithm1/2の版面は著者公開の**出版社組版を持つ19頁PDF**の印刷ページで実視覚確認（別ドメイン由来なので別の第一者出版社HTTP原本とはしない）。MHT図の原本SHAを含む著作物そのものはリポジトリへ配布しない。
- 後続A/Bが正確に同一MHTを再利用できるよう、**入力原MHT SHAと本文部分SHAを両方fail-closed検査する独立ローカル検証器**をこのPRに追加。今回使用した実ファイルに対応した検査は**12/12 PASS**、先頭1byte変更した別ファイルは**exit2で正しく拒否**。これは媒体と内容の可視構造・保全テストで、式の正しさ・訂正不存在・独立新数理・全Source scienceを証明しない。GitHub側には原著本体はないためGitHub CIで**MHT実ファイルの再取得・実際の検証器によるクラウドでの完全再現PASSとは言わない**。

### 出版社原著内の中核機構・既存系譜

- **Algorithm1, Methods 2.3.1**：既存Xia & Collins 2021オプション階層モデルを明示拡張し、タスクセット表現＋文脈別CRP先験、行動softmax＋ノイズ、ベイズ更新で再利用を制御。Xia原モデルへの**直接継承**であり、階層・CRP・softmax自体をすべて本論文が発明したと数えない。本文ではstage2選択の解析に集中し、stage1方策モデルは当該実装対象から省いている。
- **Algorithm2, Methods 2.3.2**：圧縮方策2種＋階層方策1種のモデル選択確率をベイズ的に更新し、softmaxで重み付けした決定方策を用いる。固定`beta_meta=5`、忘却`gamma`等の当該原著の境界を保存。圧縮を単に1つの固定混合則と同一視しない。
- **Methods 2.3.3, Fig5/Fig6**：同一複雑性の前向き／後ろ向き2モデルは、方策チャンクの文脈としてステージ1／2どちらを使用するかが主な差分で、V3の再合成、V1↔V2の混合条件で差異を調べる。
- **比較INT-12** [Franklin & Frank 2018原著](https://doi.org/10.1371/journal.pcbi.1006116)：reward／transitionの**別々／共同クラスタリング**と環境統計依存の裁定を中心とする。一方INT01は**状態に関する方策チャンク・圧縮階層間meta-learning・時間の逆向き文脈化**が中心。同じCRP系一般祖先というだけで数理同型・直接派生とせず、現時点では **`DISTINCT_NATIVE_OPERATORS_PROVISIONAL`**。Xia/Collins 2021との直接先行関係やINT全体・G1全体との本格数学比較は**未認定**。

### 独立に回収した重要な負例・原本内境界

- **Fig7**：同じV1／V2の反復では前向きと後ろ向きの尤度差は有意でなく、両モデルとも学習向上を再現。**FigB.2**：mid群ではV3を含む一部条件だけ後ろ向き優位であり、V3-V1やV1-V2/V2-V1を一律優位としない。
- **FigB.6B**：beta等は回復比較的良好でもeta等のパラメータ識別力は弱い。**FigB.8**：ベイズ更新を除去し固定先験にしたモデルの不利な比較を確認、単なる3方策混合で本文のmeta-learning効果と同一視しない。
- **FigB.7/本文§3.2.1**：圧縮方策単独の適合には性能上限。**Discussion**：主にオンライン募集されたバークレー所属学生群という標本バイアス可能性を著者自ら指摘。神経活動の因果実装、無制限な人一般性は原著の主張外。
- **新たな原著／公開著者コード間の模型上重要な記述差**：出版社完全HTML **§2.3.4**の例示印刷尤度は`-log Σ_i Pr(TS_i|c;t) · TS_i(s,a;t)`と表示される。著者公開の出版社組版PDF p6にも同じ表記を視覚確認。ところが同原著のAlgorithm1はTSを行動価値としてsoftmaxで確率に変換し、著者公開 [modeling.py](https://github.com/jl3676/learning_hierarchy/blob/main/modeling.py) Blob SHA `97104ec77c324654883cd96518d93e6304edb875` の`abstraction_model_nllh`では**タスクセットごとのsoftmax条件付き行動選択確率をCRPのPTSで周辺化して`log pchoice_2`を蓄積し負値を返す**。これは印字`TS_i`の意味・モデル数理忠実性の**重要な文面／コード照合課題**。現行mainコードと刊行当時のexact code commitもまだ照合しておらず、出版社の正式誤植訂正を確認したわけではない。研究者が勝手に式を書き換えて資格化せず、**印刷式を文字どおり唯一の量的モデルとする主張と、厳密な量的同一性資格をHOLD**。中核の**構造的モデル種類と限定的先行系譜の理解**はこの問題とは分離できる。

**INT01限定判定**：`PUBLISHER_FULL_HTML_PRIVATE_CAPTURE_EXACT_HASH_VERIFIED`＋`SOURCE_NATIVE_CORE_OPERATORS_AND_NEGATIVES_BOUNDED_REVIEWED`。ただし`FORMAL_FULL_SOURCE_SCIENCE_HOLD_PRINTED_LIKELIHOOD_AND_EDITION`。データの分析再実行・著者codeの数値再現実験は実施していない。

## 2. INT-13：著者の新しい参照版採用権限をG2-Dの判断に読み込む

[独立PR #434](https://github.com/rinsakamo/relay-theory/pull/434)の後続**著者明示指示「未校正稿を正式採用とする」**により、選択済みINT13の**PLOS公式31頁未校正稿PDF SHA `5f313f8690f377faaea6b9a3610013c71b880af86634c97dbd4a5344bede9258`**を、この研究における正規凍結参照版として限定的に採用。独立実出版社raw再取得、HTML SHA `057e12d6c60605f3f5344b3411e6038397c3f823e09274c4929da9af1afaaca0`は別物として保持。元出版社は依然uncorrected proofであり、公式最終校正版・proof→final同一性を**断言しない**。これまでの`HOLD_FINAL_VOR`は研究用版選定の停止理由から解除。ただし全数式、図、負例、Collins/Frank RLWM全系譜の資格は**一切自動合格しない**。PR434の限定判断と旧PR430の歴史的v1を同一視しない。

## 3. 他の対象・正式バックアップ・G1との境界

- **INT03**：PNAS出版社完全HTML＋Fig1–3をブラウザ可視、v13で唯一の技術媒体候補として選択。しかし物理PDF原本SHA・訂正史・INT06との最終数学家系は未完。
- **INT04**：Nature公式公刊主PDF20p・科学補足9p・reporting summary2pの3媒体を独立同一SHAで再取得、主Fig1–7・補足Fig1–3＋補足式1–3は独立の限定画像レビュー済み。INT08とのoffline schema学習対online retrieval学習の局所演算相違は根拠あるがglobal家系資格ではない。
- **INT06**：PLOS元主原著＋8公式補足=9/9 raw媒体完備、task-order network除去でもPRPが残る等の不利な原著条件を保存。全図数式・INT03との最終独立数学家系は未完。
- **他選定11件**（02/05/07/08/09/10/11/12/14/15/16）は旧G2のreal raw publisher PDF入手を継承するものが多いが、各原著の重要数式・全図・全変種・負例・訂正と内部同士の独立数学家系を全件QUALIFIEDとする**新証拠なし**。INT08に実publisher VORペアINT04比較、INT12に今回INT01および既存B1比較の**部分新証拠**あり。
- **第一順位バックアップB1**はINT12直接系譜ゆえINT12存続中BLOCKED。**B2**はG1 P12代替として予約中かつCTL-B2共有。**B3**はCTL-B1共有でspDCM/PPI既成中核・重要4mm再解析不再現が残る。**B4**は主／補足の高品質限定監査はあるがRLWM直接系譜と`n_s=K`分岐が原著上未定義。**採用0**。
- **G1独立PR #418最新版**は20/20個別証拠レコードを統合済みで**最終グローバルコホート未承認**。P10本SHT拡張、20/20 PLOS中心の出版源多様性、複数W3家系／INT系衝突、eLife.39497二重予約等が残り、**800件DOI無一致は800中心系譜クリアの証明ではない**。

## 4. G2-D独立正式資格までの残務（MAIN分析は行わない）

1. **source custody/edition**：今回の非公開実MHTを後続A/B双方がexact SHAで再開できる状態で保管し、INT01訂正・版レジストリと印字尤度式／著者コード版の違いを解決。INT03は公式HTML前提で出版訂正史・数式図を固定。INT13は新しい著者承認**凍結未校正稿**の元数学・図・負例を確実に審査する。
2. **残り選定全件のsource-science**：既に取得した11件PDFの無差別再DLなしで原著本体の数式／図／変種／負例／正式訂正を個別でsource-native審査。INT04/06など既存十分な媒体と限定監査は再使用して重複実験予算を節約する。
3. **統合モデル中心家系**：内部16件間、G1最新個別20件、他G2レーンの共有論文予約の科学的衝突を各ペアの**中心演算と直接継承証拠**で判断。モデル系譜未解決はUNDERDETERMINED、同名・同概念・同DOI欠如では合格しない。
4. **独立G2-Dの閉鎖後は別の全体gate**：G2共通統合・最新G1最終名簿/G3測定正式資料・G4新合同独立監査と著者#399明示的GOが必要。これらをG2-D原著の個別技術監査の開始阻害としない。

**今回正式な科学的全面資格昇格ゼロ／中心系譜の全体合格ゼロ／バックアップ発動ゼロ／MAIN_NOT_AUTHORIZED。** ただしINT01出版社完全HTMLの明確な研究利用可用性、15図・2algorithm・2表の現存範囲、未記録の印刷式／コード差、INT12との限定差分、INT13著者版選定を**新しい実証済み証拠として追加**する。対応機械台帳：`G2D_V15_INDEPENDENT_INT01_MHT_SCIENTIFIC_BOUNDARY_AND_G2D_CURRENT_GATES.json`。
