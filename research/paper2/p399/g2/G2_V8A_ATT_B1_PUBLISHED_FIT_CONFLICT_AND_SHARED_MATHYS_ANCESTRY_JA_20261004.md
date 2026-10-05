# G2 v8a 追加原著内ソース衝突（元v8固定データを変更しない）

ATT-B1のPLOS正式原著 `10.1371/journal.pcbi.1011283` には、SH-CoR 5モデルの優劣に関して**元本文の文章と同じ結果節の適合誤差の大小とが一見整合しない**という新たな不利情報がある。元v8で登録した7件の不利条件は一切変更せず、`N_ATT_B1_008` として追記。

出版社原著の結果節では平均誤差がM3a（同時facilitation/inhibition）**0.86 ±0.05**、M3b（facilitation先行）**0.99 ±0.03**、M3c（inhibition先行）**0.64 ±0.01**。本文はM3cの最低誤差を最良とする一方、同じ節の記述にM3bのsimulation resultがM3aより良いという文章がある。**評価値の大きさだけではM3bがM3aより劣る**ため、この文章が異なる定性目的（軌跡の一部）を意味するのか、出版原稿の文章問題なのかは**未解決**。本文を研究者判断で黙って改変したり、予想Paper2の再構成結果に都合がよい優劣だけを選んではいけない。

判定 `HOLD_UNDERDETERMINED`：正式20頁PDFの元Fig4Bをピクセルで開き、同一raw版S3の誤差式S16–S19を可視的に照合し、著者が「better simulation results」で指した対象が合計誤差なのか定性軌跡なのかを確認するまで、M3b対M3aの相対優劣の強い断定を科学資格対象外とする。M3c最良という**出典に記載された限定的記録**と、一般的な神経機構の真理という主張も区別する。これはMAIN構造分解やH分類ではなく、未採用備候補の出版者内部ソースの矛盾監査である。

加えてBLF-B1（Diaconescu 2014）と現BLF-02（Meyniel 2019）の両正式PLOS原著の参考文献から、**Mathys et al. 2011を双方が実際に引用**する点を確かめた。BLF-B1はMathysのHGF連続変動を適用し、BLF-02は元原著で共有突然change pointを構成するから、同論文への共通引用は厳密な同型モデルの証明ではないが、中央familyの全く独立した祖先と認定できない警告として維持する。個別source-nativeの異なるモデル式・direct inheritanceか共通backgroundかは今後の比較で決める。

初回v8台帳CIの2回のFAILED（新しいテスト自体がロール名・JSON field階層を誤認）を成功として書き換えず、ソースデータを変えずにテスト条件を修正し、最終 [v8独立raw sidecar＋9 destructive checks](https://github.com/rinsakamo/relay-theory/actions/runs/37189519695) **PASS**。正式ATT main/S3物理再取得 [37189209061](https://github.com/rinsakamo/relay-theory/actions/runs/37189209061) もPASS。以上はソフトウェア/ソース媒体の証拠であり科学的M3a/M3b優劣の解消ではない。

**G2選定40 DOI／源資料取得36／元原著raw31は不変。ATT-B1のsole-primary＋mandatory S3はPRE_A資料構成技術固定済み、正式科学資格0、備候補稼働0、G2_PARTIAL、MAIN_NOT_AUTHORIZED。**
