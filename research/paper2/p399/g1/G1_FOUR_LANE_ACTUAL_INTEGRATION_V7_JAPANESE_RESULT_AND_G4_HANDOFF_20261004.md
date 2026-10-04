# G1 4レーン統合後実監査：原著限定の20件証拠は揃ったが、G1全体正式採用は保留（2026-10-04）

**判定：`G1_SCIENCE_EVIDENCE_INTEGRATED_BUT_FINAL_QUALIFICATION_HOLD`、`G1_PARTIAL`、`MAIN_NOT_AUTHORIZED`。**

元の正式限定PF4＋新規P07/P09/P05/P13/P14＝**旧v6個別9/20**は歴史的凍結のまま。4独立レーンのPRE_A→E原著限定資料と別個個別資格の**追加11件**が共通G1に実際に取り込まれた。したがって**一次論文20/20の個別出典限定資格記録は存在する**。しかしこれは**20/20の全モデル変種・出版社多様性・中心ファミリー独立性についての最終科学的コーパス採用ではない**。

## 1．W3の正確な位置づけ

[PR #424](https://github.com/rinsakamo/relay-theory/pull/424)はP15・P16・P18の原著限定の個別資格**3/3完了**。P15原著＋数学S1 Appendix＋S1/S2パラメータ原資料と実画像、P16元10頁原著、P18原著＋S5/S6 TIFF＋S1表それぞれ、元6段階の科学記録を保持。E**後**に実原本照合成功：P15 [37198525660](https://github.com/rinsakamo/relay-theory/actions/runs/37198525660)、P16 [37191737724 attempt2](https://github.com/rinsakamo/relay-theory/actions/runs/37191737724/attempts/2)、P18 [37198719136](https://github.com/rinsakamo/relay-theory/actions/runs/37198719136)。W3 [統合個別CI37198879082](https://github.com/rinsakamo/relay-theory/actions/runs/37198879082)もPASS。一方でW3の直接原著比較**7組すべてが`FAMILY_UNDERDETERMINED`**。この2つの結論は矛盾しない。**個別論文の数学的原著限定再構成**と**20件全体における独立の中心メカニズム枠**は別の採用条件である。今回#424は原著資料・判定を共通ブランチへ輸送統合したが、W3の7組ファミリーをPASSに書き換えていない。

## 2．実際の4レーン輸送・歴史保護

凍結共通開始は `38c5eb24c61b9e57371084a65fcbcb9fb9c62a4b`。4PRの元の科学原本HEADはそれぞれW1 `da781352...`、W2 `10ed5122...`、W3 `8e21fbcc...`、W4 `ce42c13b...`。開始時に4PR **171個の変更ファイルが互いに0重複**かつすべて各W専用科学パス／GitHub Actionsに限ることを検証。

[元Git DAG完全保持non-FF一時的シミュレーション371?](https://github.com/rinsakamo/relay-theory/actions/runs/37206072952)は全171元ファイルGit blob SHAと旧v6証拠をPASS。しかし本番リポジトリは**merge commitをHTTP405禁止**したため、元の科学PRE_A→E導入コミットを「Squash後も歴史祖先」と虚偽表示しない。代わりに**W1〜W4の元Git原本HEADを4本の専用独立アーカイブ参照に先行固定**し、[別の実Square許可方式シミュレーション37206222355](https://github.com/rinsakamo/relay-theory/actions/runs/37206222355)で4アーカイブ原本と同一171個のblob、旧v6 SHA一致をPASSした後、GitHubの許可する**Squashで共通G1へ実輸送**：

- W1 #428: 共通Squash `00f01d6b`、37ファイル
- W2 #427: 共通Squash `46194e7c`、43ファイル
- W3 #424: 共通Squash `8abe16d2`、50ファイル
- W4 #425: 共通Squash `e577fdc2`、41ファイル

新[実統合ブランチ上171原本照合CI37206417445](https://github.com/rinsakamo/relay-theory/actions/runs/37206417445)は、本番共通G1で実際に各171ファイルblobと各元Git HEADを比較し**171/171原本バイト完全一致**、元科学段階4独立保存参照を保持、旧v6原本9件の歴史証拠再実行もPASS。証拠投影 SHA256: `8b536a5084efc76e6c5676b20e5e43d81e604239e32d13165b17c506d4c743e4`。[付加的v7否定対照CI37206521062](https://github.com/rinsakamo/relay-theory/actions/runs/37206521062)も成功。W3・P10・出版多様性・MAINについての虚偽昇格4件を4/4拒否した。

凍結科学stageの真の導入順はSquashコミットから復元したことに**しない**。各W元HEAD／アーカイブと個別E後元Git祖先監査が権威。元v6台帳と歴史旧失敗CI、元PF資格、Grammar v0と#398は書換えていない。

## 3．まだG1全体科学採用に使えない実ブロッカー

1. **P10：** W1が実際に凍結したのは原著基本モデルEqs1〜10の限定科学。元論文p18の**optional full SHT Eqs11〜13**の原著全変種まで資格化していない。単一論文コーパスの参加条件を「原著中の全中心変種」とするなら、追加の**新たなprospective補充科学A〜E＋元原本E後監査**を先行する必要がある。限定的核心モデルのみ採る別案は、科学的な事前基準と独立G4・著者判断が必要。今回自動的に「P10全変種PASS」とはしない。
2. **出版社多様性：** 源原著主一次論文の20件が**全てPLOS**。一論文の元補足PDFやEPS、異なる媒体サーバからの同一バイト取得は別出版社の独立一次論文にはならない。W2が調べたeLife.39497のv2/v3実本文差と必要公式補足原著の最終科学源は未解決、さらにG2 CTL-B2/INT-B2の二重予約。自動差替えなし、非PLOS科学的受入**0件**。
3. **全モデル中心系譜：** W3の7原著対比較はすべて未判定、W4 P19/P14及びP20/G2 SKL01/SKL03も未判定。異なるDOIや名称で全系譜の独立性を認定しない。PF元原著の範囲制約を保持する。
4. **原著の不利条件：** P08の実質訂正によるC3非最適／正しいC5とBayes filtering行動非識別、P20公式本文の `p=.944` と公式補足S1表の `p=.44`（両者とも非有意だが数値矛盾）、P11/P12/P17の限定、原著数値プログラム未独立再実行、独立盲検原著人間意味査読未実施を保持。
5. **他ゲート：** G2 #419はまだPARTIAL、G3 #417もPARTIAL。元G4 #420は当時の**MAIN_NO_GO**であり、今回の共通G1原著輸送後の**新たな独立科学採用・合同G4再監査は未実施**。author明示MAIN GOなし。

## 4．次の独立分担と停止線

科学的新規原著取得に戻るのではなく、**P10全変種のprospective補充か限定採用範囲のowner事前判断**、**非PLOS科学的候補のG2二重予約調停と正式原著必要補足版差確認**、**W3/W4/PF/G2との中心実装数式のcross-lane系譜比較**を分けて進める。調整側は [追補v7原著証拠と未採用条件](G1_FOUR_LANE_SOURCE_EVIDENCE_INTEGRATED_GLOBAL_ADMISSION_HOLDS_v7.json) を新しいG4監査入力として引き渡せるが、これを旧G4のGO決議と取り違えない。

**正確な表示：個別出典限定資格20件の証拠が共通G1に輸送済／正式G1全体適格性未認定／MAIN未承認。**
