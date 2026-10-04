# G2-D v10 — 同一資格基準での選定INT-04↔INT-08刊行原著ペア照合と実験条件の例外（2026-10-04）

独立INT Draft PR #430だけに対する追加原著証拠。G2 parent HEAD `69748673c80f421605f1c63607472903ac2ed68c`、G1 working 20とG2 working 40の正規名簿・他レーン予約は無変更。MAIN本試験の構造分解、Grammar role付与、H0/H1/H2、忠実度検査、予備本試験科学結果は扱わない。

## INT-08の出版社正式原著の再取得（履歴ソースではなく今回物理実行）

選定INT-08 DOI `10.7554/eLife.74445`、Lu/Hasson/Norman、出版社eLife **正式Version of Record 2022-04-11**。公開eLife公式v3 PDF URL `https://cdn.elifesciences.org/articles/74445/elife-74445-v3.pdf`、刊行元 https://elifesciences.org/articles/74445v3 。元G2 v5から引継いだ正式原本SHA `89f8846ab34dbc5af0d4079423ff51e00c1873b6149c48217b547b1bdcb678da`。

[独立publisher firstparty再取得 CI 37206108178](https://github.com/rinsakamo/relay-theory/actions/runs/37206108178) SUCCESS：実際のeLife CDNから**HTTP200／PDF 4,476,771B／正式43頁／raw SHA原本と完全一致**。各リクエスト12秒timeout、失敗時のみ公式eLife Chromium記事18秒fallback（今回はraw PDF成功のため呼ばず）。PDF全43頁の抽出SHAおよびsource-native主機構用語・該当頁検索索引を出力artifactとして保存。今回の新規成果は実ソースを **V3正規公刊原著へSHA-locked独立再検証**したこと。文献自体の全図・全数式の人手意味資格を達成したとの昇格なし。

## 同じ出版社原著上で比較する実際の生成/制御中核

| 比較軸 | INT-04 Nature 2024正式主原著/正式補足 | INT-08 eLife 2022正式VOR |
|---|---|---|
| 主機構・依存対象 | MHNの一回記銘→ランダムreplay教師信号→offline皮質VAEのlatent schema learning、想起でgenerative decoderと海馬残差を結合 | LSTM-based neocortical situation modelで次状態予測、episodic snapshotを競合するLCA検索、neocortical EM-gateがLCAへの活性化を乗算制御 |
| 情報を選ぶ条件 | extended modeの入力再構成誤差が閾値より高い**個々の感覚要素**を海馬に残し、latent conceptual predictorで予測できる部分はschemaで補う | progressing episodeで**今検索する期待便益と誤検索リスク**によりゲート学習し、欠損した状態情報をepisodic recallで補う |
| 学習されたもの | replayによるVAE重み・潜在統計／schema再構成（既存MHN/teacher–student/VAE部品を統合） | episodic **retrieval policy**の学習、既存LSTM・Advantage Actor–Critic・LCAを組み合わせたnetwork |
| 時間と失敗条件 | replay訓練を介した段階的consolidation、閾値を上げれば残差容量は減るが再構成誤差増（Fig5） | オンライン推論でretrieval誤照合が次状態予測を損ねるため、必要性・確信度が低いと検索を抑制 |

**本ペアの限定的source-native中核演算区別は実証**：両者の主学習対象／選択作用とモデル出力は対応せず、単にhippocampus・neocortex・memory・predictionという名詞が同じで中央モデルまで同一だとは言えない。ただし**各々の元アルゴリズムの既成流用、共通memory-system祖先、他14 INT候補/40 MAIN/G1モデルとの家系衝突**は別の問題。単一ペアの判別を全G2 diversity admissionに拡張しない。

## 必須の原著不利な条件：INT08は全ての符号化を自由学習していない

INT08 eLife正式原著p6 *Experimental task modeling*：人間のrecent memory (RM)／distant memory (DM)／no memory (NM)条件を模擬した具体的シミュレーションのため、**各eventの最後にsnapshotを保存するencoding policyを実験者が手動固定**したと原著が明示。eLife original p3–p4ではLSTM、EM-gate、LCA競合が定義され、**learned retrieval**が本論文の中核。p12など後続実験はmid-eventに追加snapshotを入れるデメリットを別途調べ、selective end-of-event encodingが性能上有利との別結果。これを「全実験を通じてretrievalとencodingの両方をend-to-end自由学習」などと捏造しない。原著の著者要旨自体、学習したことは主としてretrievalの選択、符号化については手動構成を操作比較した有用性だと区別する。

**検出器失敗の履歴も保存**：元[CI 37206213517](https://github.com/rinsakamo/relay-theory/actions/runs/37206213517)でreal PDF raw SHAとp6原著native文字のbounded windowは正しい一方、先行v10bプログラムが「imposed (by hand) ... encoding policy」**連続literalの完全一致**を要求したため、PDF改行・括弧等により実在するpolicyを`false`と誤検出した。**原著PDFと公開された該当native windowを改竄せず**、後続v10cはPDFの改行を正規化し、`imposed／by hand／encoding policy`の近傍証拠を別途照合する。v10bの偽陰性を実験科学結果や論文未報告の証拠として扱わない。修正runの実際の結果を確認するまで`CORRECTED_MACHINE_WITNESS_PASS`と主張しない。

## 残す停止

- 選定INT04：先行v9によりVOR主7図＋正式supp3図／supp Eq1–3のsource-native視覚監査完了。ただし独立コード再現や全グローバル家系認定は未終了。
- 選定INT08：正式v3原著の同一raw SHA原本実再取得成功、43頁全テキスト索引、選択的検索ゲートと手動符号化条件のソース一次証拠を確認。ただし**43頁全Figure/Appendix／各重要数式の独立pixel審査は未完**。
- INT03：PNAS今回403/Cloudflare、過去G2のofficial HTML候補が今回そのまま取得成功だったとは偽記録しない。INT01 official Elsevier full原著未取得、INT13公式出版社表示still uncorrected proof。
- 正式バックアップ採用0、最終Global中心family独立認定0、G1/MAIN先行凍結未完、MAIN_NOT_AUTHORIZED、G2-D_PARTIAL。
