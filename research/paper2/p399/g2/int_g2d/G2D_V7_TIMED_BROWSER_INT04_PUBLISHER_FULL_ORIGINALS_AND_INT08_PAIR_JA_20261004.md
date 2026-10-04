# G2-D v7：時間制限付き直接取得→Chromium原著取得結果、INT04真正VOR+正式補足、選定INT08との限定系譜（2026-10-04）

本追補は [Issue #399](https://github.com/rinsakamo/relay-theory/issues/399) と既存G2 frozen HEAD `69748673c80f421605f1c63607472903ac2ed68c` に対するINT独立Draft PR #430のみの成果。既存G2/MAIN40/G1 roster・他G2レーン・#398不変更。MAIN分解/Grammar再構築/H0/H1/H2/本番の予備結果閲覧なし。採用バックアップゼロ。

## 0. リトライと科学的資格の峻別

指定された方法を**実際に実行**。初回のpublisher direct HTTPリクエストに**1本12秒**、不成功ならGitHub Actions内部の**headless Chromiumのナビゲーション1本18秒**を設定。データは出版社一次ドメインだけを信用する。予期しない別ホストへの転送、書誌だけ／チャレンジページ／Author Manuscript／第三者mirrorをfirstparty VORへ昇格しない。失敗経路を消さない。

[実CI v6 run 37199967871](https://github.com/rinsakamo/relay-theory/actions/runs/37199967871) **SUCCESS=取得試行が完走**（論文双方の原著成功という意味ではない）：
- **INT03 PNAS DOI `10.1073/pnas.95.24.14529`**：出版社PDF正規+downloadクエリ双方403、出版社FULL HTMLもHTTP403、ChromiumではCloudflare challenge +403、可視本文0。既存G2時点の過去に観測した公式HTML browser候補を否定するのではなく、**今回新規のPNAS FULL原著raw取得/独立再現0**。PMCは二次資料として参照可能だが、未取得のPNAS出版社オリジナルへ偽昇格しない。
- **INT04 Nature DOI `10.1038/s41562-023-01799-z`**：直接 Nature PDF、Springer PDF、Nature HTML各HTTP200でも内容すべて**3,038Bの同一アクセス制限文書** SHA `32ed63159c77e21ee19ca1b9aa3213ccf0218eb59539560b132a8e68ef0e18ea`。**HTTP200は正式版取得とは限らない**。Chromium切替後は出版社Nature official HTML実際に117,153可視文字、DOM 738,528B、原著 DOI・全タイトル・Intro/Methods/Results/Discussion/References等、publisher URLへの再解決が成功。初回v6におけるDOM SHA `b626bedbb3d03b51bbd06bfc36b37b0b9ebec2340772e6cf766352e2fd1ead01`、ブラウザ描画DOMをPDF raw SHAへすり替えない。

[実CI v7 run 37200081279](https://github.com/rinsakamo/relay-theory/actions/runs/37200081279) でNature出版社の取得済みDOM内に**実在したリンク**だけを追跡。独立publisher Chromiumナビゲーション→ブラウザsessionの第一者linked mediaを**各12秒で厳格取得**、原本文献タイトルによるPDF identity、本文初頁で判定。Natureの記事レコードは出版社正式VOR **2024年1月19日公開**（March 2024 issue）。Crossref [Crossmark firstparty-registered record](https://crossmark.crossref.org/dialog/?doi=10.1038%2Fs41562-023-01799-z)は2026-10-04閲覧時 **Document is current** と表示、登録上の更新なし（これは全世界の訂正不存在の証明ではない）。

| INT04 firstparty正規媒体 | 原典/独立URL | 生バイト数 | 新規出版社RAW SHA-256 /頁 |
|---|---|---:|---|
| **正式刊行主原著** | `https://www.nature.com/articles/s41562-023-01799-z.pdf`（刊行元HTMLリンクと完全一致） | 2,666,492 | `b78a62b28775ec55610aeeca2252bc43b1ba782486c083a5065a3419ed3cde31`、20頁 |
| **正式科学補足** | `https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41562-023-01799-z/MediaObjects/41562_2023_1799_MOESM1_ESM.pdf`（出版社自身の実リンク） | 2,912,573 | `6f9baebc2f95492b4ce275c64ed0cb640105cd480d401b78dee09c5abbb03612`、9頁 |
| **出版社 Reporting Summary** | 同一 official `.../41562_2023_1799_MOESM2_ESM.pdf` | 47,812 | `a9b713fbc8d39e24534ecaceb9c6deb53f13d36b0ec21843130bb69f67ad93bf`、2頁 |

刊行元 HTML **HTTP original response** 719,927B raw SHA `71796e6b9ccc1bc5721384fa9095d957f90377792dfcc7a1daf5a36f444bae3f` と full live DOM/visible text の別ハッシュも保存した。Nature direct HTTPのアクセス制限文書を科学資料から除外、Chrome本物の完全HTMLはsource parityに適合。**INT04原本科学参照媒体主PDF20p＋正式科学補足9pが新たに物理SOURCE-COMPLETE**、別報告Summary2pも原本取得。特に初回G2の「publisher browser PDFのみ、raw SHA無し」は**今回の実取得でINT04については克服**された（他39候補・G2共通台帳の未承認変更は行わず、INT独立deltaとして記録）。

## 1. INT04 と INT08、source-native中核の限定比較

選定INT04正式本文が記述する主要構成は**既存Modern Hopfield Network (MHN)による海馬側一回記銘 → 既存teacher–student learning/hippocampal replayで生成モデル（VAE）を段階的に訓練 → cortical latent schemaで再構成／想像・意味抽出 → schemaで予測しきれない詳細のみ海馬trace補完**。MHN、VAE、teacher-studentの計算法はそれぞれ既知であり、本論文が「MHNやVAEを世界で初めて発明した」と主張してはならない。貢献候補は**反復replayによるこの複合システムの学習・固定化と記憶構築の説明**。

対照として選定INT08正式eLife DOI `10.7554/eLife.74445` の刊行版v3（2022-04-11）と出版社公式Figure1説明／Methodsをsource-native確認。元G2凍結INT08 publisher主原著RAW SHA `89f8846ab34dbc5af0d4079423ff51e00c1873b6149c48217b547b1bdcb678da` は継承（今回は不要な物理再取得を行わない）。INT08の主構成は**LSTM/RNN recurrent neocortex＋Advantage Actor Critic (A2C)学習＋海馬相当episodic store、既成leaky competing accumulator (LCA)検索にneocortexが学習する可変episodic memory gateを掛け、次状態予測のためにいつ符号化・検索するかを制御**。LCA自体はUsher/McClelland 2001等既成数理。

**両原著の違いは単語・分野名ではなく、原典source-native演算**：(i) INT04はリプレイによりgenerative latent weightsを更新し、記憶の時間的固定化・schemaに合う/合わない特徴の再構築が対象、(ii) INT08は進行するepisodeのオンライン次状態予測の際episodic retrievalを**ゲートで制御**し、A2C最適化とLCA競合でアクセス判断を行う。いずれも海馬/新皮質、記憶/一般化、予測という上位理論祖先を共有。モデル部品の再利用は双方にあるが**同一の中心更新・制御演算であるとする直接原著証拠はこの2原著範囲では検出されない**。限定判断は`DISTINCT_OPERATIONAL_TARGET_AND_UPDATE_PATHWAY_AT_SOURCE_TEXT_LEVEL`。全原著/補足math/figure対照および全G1/MAIN40中心家系同定はまだ`HOLD`：現段階の限定対照から全般の正式独立認定はしない。

## 2. 追加科学的負例・未解決

- INT04主原著自身がMHN/teacher–student/VAEと空間認知先行研究を直接継承すると説明しているため「全構成要素の完全独立初出」認定は禁止。
- INT04は構造的モデルのsimulationであり、海馬/entorhinal/mPFC/anterolateral temporal cortexの各神経回路の因果操作によるモデル独立検証そのものではない。reconstruction/schema distortion、hippocampal lossの予測を本人の全記憶事象で生物学的に立証とは扱わない。
- 新規主原著20pと科学付録9pの**全数学式の画像画素目視・全図semantic・全負例記録**は別検査、ソース取得成功3/3やraw SHAだけで`SCIENCE_FULL_QUALIFIED`へ昇格させない。今回web PDF視覚スクリーンショットは出版社IDP制限で失敗したので、画像を検証したという未遂の昇格禁止。
- INT03の今回の取得不成功も別のG2旧接続で観測した全文HTMLを偽りだったと断言する材料ではない。新しい独立監査では`PNAS_REACQUISITION_FAILED_403_CHALLENGE`を明示。

**現時点：INT04原著・重要公式付録物理原本が正式取得成功、選定INT04×INT08の限定原文演算差は確認、原稿の全文source-native science完全審査と全G1/MAINモデル系譜独立認定は依然未完。G2-D PARTIAL／正式バックアップ採用0／MAIN_NOT_AUTHORIZED。**
