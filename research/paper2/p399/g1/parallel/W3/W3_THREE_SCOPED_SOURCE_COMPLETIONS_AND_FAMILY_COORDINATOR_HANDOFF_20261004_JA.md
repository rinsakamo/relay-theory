# RelayTheory Paper 2 — G1-W3 3本原著適格性完了・モデル系譜保留・調整担当への引継ぎ

日付: 2026-10-04 JST  
対象: #399 G1-W3、独立Draft PR #424  
共通固定起点: `38c5eb24c61b9e57371084a65fcbcb9fb9c62a4b`  
本資料は、以前の `W3_ACTUAL_COMPLETION_AND_SOURCE_BLOCKERS_20261004_JA.md`（当時の原著HTTP 502失敗、個別資格0/3）を**履歴として変更せず**、実再取得が成功した後の**追補**として記録する。

## 最新の判定

**W3指定のP15・P16・P18は3/3本とも、凍結した各PRE_A→A→B→C→D→Eの6科学段階と、それとは独立に後から実行した出版社原著実取得・正確なSHA・段階Git履歴のpost-E GitHub CIが完了。3本の原著範囲限定の個別科学的資格判定を別ファイルで発行。**

これは「各論文の出版版に支持された機構と逆風条件を原著範囲内で説明できる」という判定であり、他モデルとの全系譜独立、作者の実験コードの数値再現、盲検第三者による解釈一致、全20件のコーパス承認は含まない。G1共通の元の9/20件を勝手に12/20へ書き換えていない。

| 担当 | DOI | 別コミット科学段階 | 凍結したA主張/依存 | B反論/C否定/E忠実度 | 実際の独立post-E出版社原著監査 | 個別判定 |
| --- | --- | --- | --- | --- | --- | --- |
| P15 | `10.1371/journal.pcbi.1010589` | 6/6 | 26/32 | 14/16/12 | [37198525660](https://github.com/rinsakamo/relay-theory/actions/runs/37198525660) PASS、原著5点、artifact 11301736355 | 原著範囲限定PASS |
| P16 | `10.1371/journal.pcbi.1003648` | 6/6 | 29/35 | 12/13/12 | [37191737724 第2試行](https://github.com/rinsakamo/relay-theory/actions/runs/37191737724/attempts/2) PASS、正式原著、artifact 11301630951 | 原著範囲限定PASS |
| P18 | `10.1371/journal.pcbi.1008552` | 6/6 | 28/35 | 16/18/12 | [37198719136](https://github.com/rinsakamo/relay-theory/actions/runs/37198719136) PASS、原著4点、artifact 11301991827 | 原著範囲限定PASS |

追加の独立W3統合GitHub Actions [37198879082](https://github.com/rinsakamo/relay-theory/actions/runs/37198879082) PASS、artifact 11301946356: 18/18段階の実際の初回導入コミット、現在のバイト一致、厳密な前後関係、起点commit、W3固有の変更path、3本の原著post-E成功記録参照、7組の系譜判定がいずれも最終独立性未確定であることを確認。これは履歴・資料・機械的な範囲チェックであり、科学内容の独立した二重盲検実験ではない。最初の統合CI失敗 [37198847514](https://github.com/rinsakamo/relay-theory/actions/runs/37198847514) も保持。初回はP16の正常な過去receiptのキーが `result`、P15/P18の `conclusion` と異なることをソフト検証器が取り違えたためで、検証器を修正して別のCI実行でPASSした。凍結科学ファイルは変更していない。

## P15: 実際の元数式と正誤境界

以前のPLOS HTTP 502により欠損していた同一論文のS1 Appendix（原著5頁）、S1/S2 parameter Table（各1頁）を直接再取得した。加えてS1 EPS入力図（元458175バイト）を取得し、EPS署名・BoundingBox・Ghostscript画像化を確認。[出版原著一式の独立取得](https://github.com/rinsakamo/relay-theory/actions/runs/37197851068)、[原著本文・数式付録・表の独立再照合](https://github.com/rinsakamo/relay-theory/actions/runs/37198042557)、[EPS図の独立検証](https://github.com/rinsakamo/relay-theory/actions/runs/37198125975)。PRE_A資産の元SHAは `P15_PRE_A_original_complete_math_figures_frozen_v1.json` へ凍結した。

主な原著固有の核は、ECin直接入力時とDGを介した後続CA3状態を時間的に比較し、課題AB/ACの学習に結び付ける設計。ただしS1 Appendixにより実行されるLeabra/XCAL学習は**誤差成分と長期BCM型Hebbian成分を併用**し、別のHebbianのみの投射も残る。表S2に明記された非ゼロHebbian係数を論文題名からゼロ扱いしてはいけない。作者のモデル統計・外部人間行動比較は元論文で報告されたもので、W3が実験や作者hip-edlコードを完全再実行した事実はない。

限定資格: `P15_POST_E_INDEPENDENT_PUBLISHER_SCOPED_QUALIFICATION_v1.json`。凍結PRE_Aコミット `6e523ca5`、A `50268096`、B `25651804`、C `e64579b1`、D `e8bbe2eb`、E `1e49466b`（個別JSONに完全SHA・実証を記録）。

## P16: 保留していた実出版社原著post-E監査が成功

凍結済みPRE_A→Eの6個の元の科学コミットは再書込しなかった。先行する履歴だけの検証PASSを、新しい原著検証成功と混同していない。実際に過去に失敗した [37191737724](https://github.com/rinsakamo/relay-theory/actions/runs/37191737724) を正式に第2回再実行し、PLOS出版版10頁 **SHA256 `93428304dccfa6828e0f355d8b4c5875fb441fb939098519e78fbedf6405bdc5`** を取得、原著の限定ページ文字アンカー・画像化、凍結された6段階の全Git初回コミット、内部内容29/35・否定13・忠実度12を照合してPASS、receipt artifact 11301630951。

原著実装は予め設定した空間と文脈2パターンから固定Hebbian再帰重みを構築し、空間的なCA3の局所文脈アトラクタを活動ダイナミクスで検索。既存PF01の1次元ノイズ下の連続bumpと**実装された動的STP facilitation/depression**とは核の操作が異なる。ただし広い連続アトラクタ系の直接共通祖先候補の原著数学の比較はG4調整へ残る。原著Fig2本文参照のずれ、J=0比較の追加抑制I=0.8、重みJの安定性トレードオフ、リセット時のヒステリシス消失の条件は原著負例として維持する。

限定資格: `P16_POST_E_INDEPENDENT_REAL_SOURCE_SCOPED_QUALIFICATION_v1.json`。

## P18: 未校正稿の代用を拒否し、出版社最終出版版で検証

独立CIでPLOS正式出版原著28頁とUCL著者機関公開PDFのバイトSHAが両方、当初の出版社原著 `cb75481590c34686eeeb8635dcb8a381283bcbe3e7f8ed9f0ee246fa95e419d1` と一致。出版社同一論文のS5モデル回復TIFF（1084×641）、S6モデル検証TIFF（1028×1498）、原著S1パラメータPDFを取得し原画像署名・ピクセル解読とハッシュを検証した。[原著4点の独立post-E監査](https://github.com/rinsakamo/relay-theory/actions/runs/37198719136)、artifact 11301991827。

原著の核は、将来10バンディット選択期間の自己のmodel-free傾向を推定したmodel-based計画が、先行する環境の報酬設定を選ぶ実装である。同時に著者が試験した独立MF報酬設定学習、lazy MB encoder、選択履歴、一定バイアスを別々に保持。原著報告の入れ子モデル検定p<0.001は**著者が明記したモデル群内**での支持であって、脳内自己モデルの直接測定・未試験のあらゆるヒューリスティクスの排除ではない。パラメータ間トレードオフ修正後、MB係数関連p=0.06は強い証拠としない。原著被験者向けPPTXの完全逐語一致、実データを使う数値的な著者コード再実行は個別資格の対象外。

限定資格: `P18_POST_E_INDEPENDENT_PUBLISHER_SCOPED_QUALIFICATION_v1.json`。

## 系譜の科学判定: 個別原著資格3/3と、全体でのモデル独立性は別

旧`W3_SOURCE_SUPPORTED_CENTRAL_FAMILY_ADJUDICATION_MATRIX_v1.json`は古い当時のsource-HOLD記録として不変とし、出版社原著完成後の別ファイル `W3_SOURCE_COMPLETED_FAMILY_HANDOFF_MATRIX_v2.json` を追加した。

7組: P15対PF01、P15対PF03、P15対P14、P16対PF01、P18対PF04、P18対G2の**INT-15作業名義の公開書誌・原著要旨のみ**、W3内P15対P16。比較対象の保存済み原著機構と原著固有の演算子の違いを併記し、全組 `FAMILY_UNDERDETERMINED` とする。これは個別論文の出典検証不合格という意味ではなく、**G1/G2合同の全祖先グラフをまだ十分に照合していない**ため、全コーパスの独立モデル系統としての自動採用をしない措置。特にP16/PF01のStringer/Trappenberg/Rollsら連続アトラクタ前駆、P15のCLS/Leabraの直系、P18/PF04/INT15のDaw2005系を要審査とした。

また、**既存G1適格9編と新規W3の3編はいずれもPLOSが原出版元**である。UCL同一バイトの写しと同一誌の補足ファイルは出版社多様性の新規原著1本として数えられない。

## 責任分界・統合先への必要作業

- W3個別原著科学トランザクションとsource post-E独立監査は**3/3完了**。W3に残る全系譜の独立性問題は未解決のまま適正に引き渡す。W1/W2/W4の科学結果を先行閲覧してこの結論を作ったわけではない。
- 元のG1共通分母9/20、PF01–PF04の元の判定・限界、Grammar v0、#398旧コーパス、G2/G3/G4の専有資料は**書き換えていない**。調整担当が4作業レーンの出典・重複・出版社多様性を独立照合し、認められた科学論文を新しいappend-only統合ledgerへ追加する。3本すべてが採用可能なら科学的な**候補上限12/20**だが、この引継ぎ自体は正式なグローバル分母を更新しない。
- G2 INT15の最終的な所属系譜、PF系の直接祖先式・論文重複、全体の出版社多様性をG1統合担当とG4が審査する。完了後であっても独立G4合同監査と著者明示MAIN GOが必要。現時点**G1_PARTIAL / MAIN_NOT_AUTHORIZED**。
- ネットワーク取得は新規W3の実取得器で個別の18〜45秒タイムアウトと最大3回の再試行を設定し、無限待機させない。ブラウザ確認を要する場合はPLOS公式HTML/オリジナルPDF等を別経路で読むが、HTML閲覧を出版社原著PDFのバイト一致検証に読み替えない。以前のHTTP502失敗ログも保持する。

最終W3科学資料・監査コード・独立CI定義の書込場所: `research/paper2/p399/g1/parallel/W3/` と `.github/workflows/p399-g1-W3-*.yml` のみ。Draft PR #424は共通G1ブランチ宛のまま**未マージ**とし、MAINの分解・再構築やH0/H1/H2判定は一切実施していない。
