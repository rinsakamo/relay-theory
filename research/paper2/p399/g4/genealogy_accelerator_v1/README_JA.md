# G4-B03 独立・全件系譜比較アクセラレータ v1

**状態: 監査用実行器 / 完全な科学的系譜資格ではない。MAIN NO-GO。**

### 入力と凍結

1. G2統合 #435 の親が保持する凍結済み G2 v5 WORKING 40 DOI 名簿（正式最終40ではない）。
2. G2 #419 の既存 780 + 800 **全列挙** v2 台帳。既存フラグ、原著引用検出、未判定の歴史を保持する。
3. G1 #433 の独立 v7 名簿20件。**コミット `c7317da41b15159864c014b8dc53449121c34a2c`、blob `7771759aa0fb8fd5e03f99a63b355c7503d095c2`** の実Git版から読み込み、旧G2台帳に写されたG1 DOI全件と突合する。
4. G2-D v20のINT-01対35件の限定source-native比較。索引付き根拠がある組のみ再利用し、最終独立認定には昇格しない。Git blob `886bed52531abec3457f3b9976f39236b8899007` を検証する。
5. G2-D v10dのINT-04対INT-08独立限定原著比較（正式v3/eLife原著とNature main+supp）。正式な広域同族認定は未実行。
6. ORIGINAL_NATIVE_PROFILES_v1.json: **既存の限定科学監査から26/60件投入済み（G1の20/20件すべて、G2のATT-03, BLF-01, PRD-01, INT-01, INT-04, INT-08）**。25個の厳密な原著監査Git blobを元のG1/G2分岐コミットに照合し、主原著raw SHAと重要な正式訂正/同一論文補足資料をチェック。26件の取り込みは新たな原著全体の独立科学審査ではない。以降の34件（現在すべてG2）は独立の台帳ルール更新と原著証拠が必要。

G2統合 #435 の新規原著監査・著者選択は科学的内容に応じて個別更新が必要。v5は**現状での実行入力スナップショット**であり、将来の最終名簿を宣言しない。#436等で原著版やモデルが変わった際は新しい入力版として実行し直す。

### 出力

- `PAIR_TRIAGE_MATRIX.json`: 全1580件、科学的な広域独立性は全件 `UNDERDETERMINED` のまま。旧原著引用/既存リスク/既存原著限定比較/証拠付きプロファイルの共有演算子を**候補の優先順位**にのみ使用。
- `PRIORITIZED_REVIEW_QUEUE.json`: 正のリスク情報がある候補から、優先度0（厳密同一DOI）、1（記録済リスク）、2（引用または原著監査済構造候補）、3（既存限定source-native比較だがG4再判定が必要）を選別。キューに**出ていない組も未審査**。
- `REMAINING_PROFILE_EVIDENCE_QUEUE.json`: 60件の候補名簿から既登録26件を除く**残り34件**について、既存リスクまたは限定原著比較が関連する組の数に基づき、科学結果非依存の原著調査順に整理。リスク0は独立ではない。
- `PROFILE_GIT_PROVENANCE_RECEIPT.json`: G2の後続ユーザー提供原著監査ブランチを含む厳密な元Git blob照合記録。原著PDF/MHTの新規再取得は行っていない。
- `PAIR_TRIAGE_SUMMARY.json`: 40・20・780・800の照合、SHA256入力digest、リスク種別・件数、科学的グローバル独立判定 **0**、MAIN **未承認**。

入力の1組でも欠落/重複/名簿DOIズレがあれば **例外停止**。安全でない既定PASS、欠損を「非重複」に読み替える動作、引用の不在を独立性の証明とする動作はない。

### 完全実行

```bash
python research/paper2/p399/g4/genealogy_accelerator_v1/build_pair_matrix.py \
  --g2-manifest research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json \
  --g1-roster /tmp/G1_V7_PINNED_FROM_EXACT_GIT.json \
  --legacy-pairs research/paper2/p399/g2/MAIN40_G2_780_MAIN_AND_800_G1_FAMILY_RECONCILIATION_v2.json \
  --profiles research/paper2/p399/g4/genealogy_accelerator_v1/ORIGINAL_NATIVE_PROFILES_v1.json \
  --source-native-v20 research/paper2/p399/g2/int_g2d/G2D_V20_INT01_THREE_ADDITIONAL_PAIRS_INT09_OFFICIAL_FIG9_CORRIGENDUM_AND_35_QUEUE.json \
  --source-native-int04-int08 research/paper2/p399/g2/int_g2d/G2D_V10D_CORRECTED_PAIR_SOURCE_NATIVE_MACHINE_GATES.json \
  --output /tmp/p399-g4-pair-triage-v1
```

公式CIは `git fetch` と `git show <固定G1コミット>:<固定ファイル>` で読み込み、想定Git blobまで検証する。GitHub Actionsに出力を保存する（変更できる名簿やMAIN科学結果は勝手にcommitしない）。

特定G2枠の差替え時は `--focus ATT-01` などで関係する59組だけ再表示可能。G1枠は関係する40組。**焦点実行では、まず元の全1580件の入力整合性を検証するが、部分出力を全件科学監査完了と称してはならない。**

### 証拠付きプロファイル追加（後続）

各要素は `id`、元の採用原著 `edition_sha256`、`original_source_evidence`（原著ページ/節/式と版を含む証拠参照）、`native_core_operators`（原著根拠付き、共有演算子に安定IDを付ける）、`direct_model_ancestors`（証明可能な直接祖先の DOI）を持つ。最初はゼロ件。完全原著の一括読解・原著モデルごとの一回の構造化で60プロファイルを漸進的に作る。現在の10件は原著監査台帳の中核限定情報を再利用した最小初期型であり、原著全体を新しく再読了したとの主張は禁止。オペレータIDは紙面固有（例 `P05:clipped-finite-spatial-ior`）とし、同名を理由に自動で同族グラフ統合しない。直接祖先はDOIを用いて照合する。

グラフ辺は **同一・直接継承・構成要素共有・抽象概念共通・機構相違**を別種として扱う。推移的に全てを同族に統合するUnion-Findは使わない。モデルの直接引用や共通祖先は中心機構の同一証明ではなく、数式上の違いも相互非導出性の完全証明ではない。

このv1は既存の限定原著系譜判断を最終判定に昇格させない。科学的最終判定は独立した原著読解とG4の署名付き合同監査に委ね、#399の著者MAIN明示GOは独立ゲートのまま維持する。

### 実測と重要な残務（2026-10-05）

- [10件・10既存限定比較版 GitHub Actions 37252337405](https://github.com/rinsakamo/relay-theory/actions/runs/37252337405) **SUCCESS**：17/17 合成・破壊的テスト、8個の別個source-ledger Git blobと10件のDOI/主原著SHA/補足・訂正、一貫した780+800全件を検査。優先組は旧リスク23＋旧引用2＋新規限定比較9＝34、残り1546件も未判定、科学的グローバル独立PASS 0。
- 元の 2009 Neuron review・2025 iScience original・2024 Nature author manuscript/訂正はユーザー取得媒体のSHAを既存監査台帳から照合したもの。元PDFをこのレーンのCIで新規取得・独立画像監査したものではない。INT01も私的原著MHTで、出版社サイトからの独立取得証明ではない。
- 追加50件の原著数学/直接モデル祖先/正式出版社版の有効な証拠が揃うまではプロファイルを作らず、源泉欠落を機構相違と捏造しない。G4-B03科学判定と著者明示的GOは別責務。

### 26/60 source-ledger profiles and 13 bounded original-native pairs — 最新証拠

- G1 PILOT20の **20/20件は限定原著プロファイル入力完了**。PF01–PF04はそれぞれ独立で正式に凍結された Git commit で直接照合。G1内190組の相互独立・20件の全体最終資格は**未判定**。G2残り34件はSOURCE_SCIENCE_AVAILABILITY_UNDETERMINEDであり、論文を読了した/新規原著科学資格したと捏造しない。
- G2-Dの限定原著比較 13 組を採用前の source-scoped witness として再利用。内訳：INT01起点 source-indexed v20=9、INT04–INT08 v10d=1、INT15–G1 P18 と INT16–G1 P09 v15b=2、INT01–INT14 v16b=1。ある組は前からリスク分類があるので追加優先キューの増分と混同しない。
- **[26件/13組の実CI run 37253211172](https://github.com/rinsakamo/relay-theory/actions/runs/37253211172) SUCCESS**。19/19 test、25 distinct Git source-ledger blobs、実 780+800=1,580 full reconciliation PASS。優先キュー35組＝既存risk23＋引用2＋追加限定比較のみ10、残る1,545組も未判定。全1,580組の独立資格PASS 0、科学的MAIN GOなし。
- 対象モデル間の直接系譜DOIがソース台帳で明示された時だけ候補として機械検出。別論文間の演算子同一性は、名前・機能語から同族を断定せず、独立原著で数式・直接祖先・同一変種の追加審査を行う。現行元監査資料だけでは独立性の完全な数理証明は生成できない。
