# G2-D v5：選定INT06の正式PLOS付録8/8物理取得と元実験の致命的な混同防止（2026-10-04）

本記録は既存v1–v4bを上書きしない **append-only** 科学ソース監査追補。独立PR #430、起点G2 HEAD `69748673c80f421605f1c63607472903ac2ed68c`。他G2レーン・G1名簿・MAIN40の変更なし、MAIN科学分解/構造再構築/Grammar role/H0/1/2/予備結果閲覧/MAIN許可は実行せず、バックアップ正式採用0。

## 1. 実行された出版社原著・正式補足の取得

[独立物理CI run 37198751884](https://github.com/rinsakamo/relay-theory/actions/runs/37198751884) **SUCCESS**、script HEAD `15bcd7bf1f460dd7dd06d7397852af6f1c6e6621`。PLOS公式各DOI `https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1000765.s00N&type=supplementary` から実際にHTTP取得し、配信先を**PLOS自体のHTTPSから発行された署名付き`plos-corpus-prod/10.1371/journal.pcbi.1000765/<source-version>/pcbi.1000765.s00N.tif`、PLOS特有のサービス主体に完全限定**。全ファイルPillowで本物のTIFFと画像形式・画素寸法を検証。外部mirror、一般Googleバケット、出版社リンク以外からの任意バイナリを偽承認しない。実行resultは原本RAW SHAと非著作権metadataのみ保存し、original TIFF生バイナリはrepoに再配布しない。

| DOI補足 | 出版社原図の内容 | raw bytes | 実原本SHA-256 | verified pixel dimensions |
|---|---|---:|---|---|
| `...1000765.s001` | Fig S1 コロラリーディスチャージ除去での応答固執 | 611,584 | `7923010b6449f00ff37807358af1a2ae46927dbeed142821a7225cec3b494bdb` | 1899×896 |
| `...1000765.s002` | Fig S2 順序決定回路を取り除いてもPRP曲線が存在 | 74,554 | `d01181c75eb525c713935ffe6aad1229e0c0307af20398d2af2c7088159b411c` | 1707×702 |
| `...1000765.s003` | Fig S3 ルータのAMPA/NMDA/GABA入力推移 | 334,249 | `6f102a9de2ecd3aae3c8de0fbe3fa9ca947a65002156d7252cddeb427c108524` | 1689×1200 |
| `...1000765.s004` | Fig S4 感覚・ルータ・task-settingのスペクトログラム | 514,139 | `5b6be0840536fd9e21c0082e1dae0393258a32bcac942411b127285d0b5fa3ad` | 1897×635 |
| `...1000765.s005` | Fig S5 感覚・ルータ細胞のspike-density coherence | 350,389 | `498c5cdfefb764ad8d3eb11d378d12a3179d3dcd7ceecdf6a606580703f5bc66` | 1572×1451 |
| `...1000765.s006` | Fig S6 組合せ式router：独立複数刺激に対応する新しい符号化例 | 363,605 | `e3e2247e2676d97bedfe7cc83da3ab8b081e81a93dc26434516d771fc0d39049` | 1730×1087 |

正式main PDFは既存取得+別[run 37198446072](https://github.com/rinsakamo/relay-theory/actions/runs/37198446072)で23頁 raw SHA `c276294fa7a111e5df98f35aa0da933af28d45a1e1347940a1b57753c0980706` **exact一致**。同runでは残余の正式補足`...s007` Supporting Notes DOC（22,016B / `ceec10ca95ae7bd2207d95c1ddb45098f2dc9741697c3608497dc2efd9b33bb5`）と`...s008` ANOVA Table DOC（31,744B / `0813b44b5770f03b833a0623da876a76dde6e2ee5cd8dcbaf5ec8257fa04b504`）をSHA固定。別[real source-native DOC抽出 CI 37198626050](https://github.com/rinsakamo/relay-theory/actions/runs/37198626050)で**同一原本SHAの再取得後のantiword文字抽出**とS1 PDF全11頁のnative readout 3/3 PASS。この組合せで、INT06選定原著main+publisher DOI補足S001–S008の**9媒体（原著本文1＋補足8）全物理取得は成立**。図の実際の画素の全解釈/校正歴まで完了したわけではない。

## 2. 重要なsource-native機構の限定と不利な条件

2010 original publisher HTML全文 `https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000765`のMethodsと付録caption、真正原DOC S7に限定：
- **N_INT06_V5_001 order-network ≠ seriality generator**：Task-order networkはT1先行順序を強制する便利な外部層であって、本質的処理ボトルネックの唯一の実装ではない。公式Figure S2と原DOC S7 paragraph Bはorder network全体を除去しても典型的PRP曲線が現れると明示。INT03と共有するglobal selective workspace思想との対照では、INT06の増分は**task-setting/routerの競合・局所抑制、スパイクベースの感覚蓄積、独立手続構造**へ限定する。
- **N_INT06_V5_002 nonmodeled router capacities**：原DOC S7 paragraph Aでは検証外router神経群を明示的に実装せず、non-specific router backgroundへまとめている。主本文の21,000neuron/46,634,400synapse/84population simulationは実装規模を示すが、恣意的に大きい課題空間を現状の有限回路が処理できる独立実証ではない。
- **N_INT06_V5_003 experimental mismatch**：原DOC S7 paragraph Cは短SOA下でより難しい条件の方が**速く**積算される逆説的予測を報告、対応する人間PRP実験の同様報告を知らないと明示。word-superiority effectをPRPでの直接実証の代用品として扱わない。
- **N_INT06_V5_004 Table S1 null cells and flattened DOC**：原DOC S8は全RT1/RT2、task/SOA/interactionが有意とは報告しない。RT1のNotation2 `p=0.1`、Distance2 `p=0.72`等の不利な非有意主効果を残す。ただしantiword抽出はTableの2段階見出し・セル順を崩す可能性があるので、**全数値とF統計・p値の厳密対応はraw DOC実画面の視覚照合までHOLD**。矛盾した可能性のあるセルを見つけても出版物の不正や欠陥だと無断断言しない。
- **N_INT06_V5_005 supplemental image-specific restraints**：Fig S3の時点比較は50模擬trialから追加filterで37のみ、Fig S4 spectrogramは100模擬からRT2>800msを除いて83のみ。Fig S5は200模擬trial、SOA=0条件。これらのサンプル条件・選択と生物学的fMRI/単細胞実測を混同しない。Fig S6のcombinatorial alternativeは元大規模モデルの無限拡張の完全学習則ではなく小規模回路の構成例であり、細胞の全combinatorial coverageを実証しない。

**今回真に閉じたgate**：`SELECTED_INT06_ALL_NINE_PUBLISHER_ORIGINAL_MEDIA_PHYSICALLY_OBTAINED_SHA_LOCKED`。さらに図ごとの正式captionを原著ソースに照合した`FIG_S1_TO_S6_SOURCE_NATIVE_CAPTION_CLASSIFICATION`。ただし人間の原画素読解と全補足・main画像内の数式完全監査、独立の意味再現、INT03との全モデル同値/非同値の最終数学的立証、全G1×MAIN40の家系判定は未完。**INT06_SOURCE_MEDIA_9_9/SCIENTIFIC_FULL_HOLD**、モデル家系独立合格0、MAIN開始不可。

## 3. グローバル停止条件と既存レーンの保全

B4公式S1 11頁A–Gの文字情報/負例、B3 35頁eLife出版社VORと縮小smoothing失敗、INT03 1998 PNAS正式PDF raw欠如、B1 INT12の直接CRP継承、B2 G1 P12代替予約、INT01 Elsevier正式原著未取得、INT13正式最終校正版未公開/未確認の状態は元v1–v4bと同じ。今回の物理サプリ取得の成功を正式原著全数学SCIENCE QUALIFIEDやバックアップ有効化に転換しない。版凍結・全G1系譜とG4合同科学GO・作者明示GOなしにMAINを実行しない。
