# G4-B03 独立・全件系譜比較アクセラレータ v1

**状態: 監査用実行器 / 完全な科学的系譜資格ではない。MAIN NO-GO。**

### 入力と凍結

1. G2統合 #435 の親が保持する凍結済み G2 v5 WORKING 40 DOI 名簿（正式最終40ではない）。
2. G2 #419 の既存 780 + 800 **全列挙** v2 台帳。既存フラグ、原著引用検出、未判定の歴史を保持する。
3. G1 #433 の独立 v7 名簿20件。**コミット `c7317da41b15159864c014b8dc53449121c34a2c`、blob `7771759aa0fb8fd5e03f99a63b355c7503d095c2`** の実Git版から読み込み、旧G2台帳に写されたG1 DOI全件と突合する。
4. ORIGINAL_NATIVE_PROFILES_v1.json: **最初はゼロ件**。原著ソースと採用版を凍結・限定原著監査できた対象のみ追記する。未監査の推測や MAIN 結果は絶対に混入しない。

G2統合 #435 の新規原著監査・著者選択は科学的内容に応じて個別更新が必要。v5は**現状での実行入力スナップショット**であり、将来の最終名簿を宣言しない。#436等で原著版やモデルが変わった際は新しい入力版として実行し直す。

### 出力

- `PAIR_TRIAGE_MATRIX.json`: 全1580件、全件 `UNDERDETERMINED` が初期状態。旧原著引用/既存リスク/証拠付きプロファイルの共有演算子を**候補の優先順位**にのみ使用。
- `PRIORITIZED_REVIEW_QUEUE.json`: 正のリスク情報がある候補から、優先度0（厳密同一DOI）、1（記録済リスク）、2（引用または原著監査済構造候補）を選別。キューに**出ていない組も未審査**。
- `PAIR_TRIAGE_SUMMARY.json`: 40・20・780・800の照合、SHA256入力digest、リスク種別・件数、科学的グローバル独立判定 **0**、MAIN **未承認**。

入力の1組でも欠落/重複/名簿DOIズレがあれば **例外停止**。安全でない既定PASS、欠損を「非重複」に読み替える動作、引用の不在を独立性の証明とする動作はない。

### 完全実行

```bash
python research/paper2/p399/g4/genealogy_accelerator_v1/build_pair_matrix.py \
  --g2-manifest research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json \
  --g1-roster /tmp/G1_V7_PINNED_FROM_EXACT_GIT.json \
  --legacy-pairs research/paper2/p399/g2/MAIN40_G2_780_MAIN_AND_800_G1_FAMILY_RECONCILIATION_v2.json \
  --profiles research/paper2/p399/g4/genealogy_accelerator_v1/ORIGINAL_NATIVE_PROFILES_v1.json \
  --output /tmp/p399-g4-pair-triage-v1
```

公式CIは `git fetch` と `git show <固定G1コミット>:<固定ファイル>` で読み込み、想定Git blobまで検証する。GitHub Actionsに出力を保存する（変更できる名簿やMAIN科学結果は勝手にcommitしない）。

特定G2枠の差替え時は `--focus ATT-01` などで関係する59組だけ再表示可能。G1枠は関係する40組。**焦点実行では、まず元の全1580件の入力整合性を検証するが、部分出力を全件科学監査完了と称してはならない。**

### 証拠付きプロファイル追加（後続）

各要素は `id`、元の採用原著 `edition_sha256`、`original_source_evidence`（原著ページ/節/式と版を含む証拠参照）、`native_core_operators`（原著根拠付き、共有演算子に安定IDを付ける）、`direct_model_ancestors`（証明可能な直接祖先の DOI）を持つ。最初はゼロ件。完全原著の一括読解・原著モデルごとの一回の構造化で60プロファイルを漸進的に作る。

グラフ辺は **同一・直接継承・構成要素共有・抽象概念共通・機構相違**を別種として扱う。推移的に全てを同族に統合するUnion-Findは使わない。モデルの直接引用や共通祖先は中心機構の同一証明ではなく、数式上の違いも相互非導出性の完全証明ではない。

このv1は既存の限定原著系譜判断を最終判定に昇格させない。科学的最終判定は独立した原著読解とG4の署名付き合同監査に委ね、#399の著者MAIN明示GOは独立ゲートのまま維持する。
