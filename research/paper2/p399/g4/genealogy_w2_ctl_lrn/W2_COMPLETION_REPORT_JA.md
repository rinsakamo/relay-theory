# RelayTheory Paper 2 — G4 Genealogy W2 CTL/LRN 完了報告

## 実行境界

- Primary authority: Issue #399
- Parent genealogy accelerator: Draft PR #438
- Exact W2 starting HEAD: `ae044a8f475fb0dc9140a91e360e1ff26a0b5e3a`
- Independent branch: `paper2/p399-g4-w2-ctl-lrn-native-20261005`
- 対象: CTL-01 / CTL-02 / CTL-03 / LRN-01 / LRN-02 / LRN-03 の6本のみ
- `research/paper2/p399/g4/genealogy_accelerator_v1/ORIGINAL_NATIVE_PROFILES_v1.json`: **未変更**
- shared pair-matrix code / shared CI: **未変更**
- MAIN scientific authorization: **false / NO-GO**

最終HEADは自己参照commitを避けるため本文中には固定せず、Draft PR metadata と完了時報告をauthorityとする。

## 6論文ステータス

| slot | DOI | status | 採用版 | source-supported direct model ancestry |
|---|---|---|---|---|
| CTL-01 | 10.1371/journal.pcbi.1012228 | PROFILE_FRAGMENT_READY | PLOS final Version of Record | 10.1016/j.jmp.2020.102472 |
| CTL-02 | 10.7554/eLife.12029 | PROFILE_FRAGMENT_READY | eLife v3 Version of Record | 10.1037/a0037015 |
| CTL-03 | 10.7554/eLife.28040 | PROFILE_FRAGMENT_READY | eLife v2 Version of Record | 10.7554/eLife.12112 |
| LRN-01 | 10.1038/s41467-025-58848-6 | PROFILE_FRAGMENT_READY | Nature Communications Version of Record | source-supported DOI ancestorを追加せず |
| LRN-02 | 10.1371/journal.pcbi.1007963 | PROFILE_FRAGMENT_READY | PLOS final Version of Record | 10.1038/nn1954; 10.3389/fnhum.2014.00825 |
| LRN-03 | 10.7554/eLife.21492 | PROFILE_FRAGMENT_READY | eLife v2 Version of Record | 10.1093/jigpal/jzp049 |

**Ready 6/6、SOURCE_BLOCKED 0/6、SCIENTIFIC_ANCESTRY_UNDERDETERMINED 0/6。**

全6 profileで `global_family_independence_certified=false`、`ancestry_exhaustiveness="NOT_ATTESTED"`、`main_scientific_authorization=false` を保持した。

## 使用したrepository evidence

W2はrepo-firstで監査した。主要な固定元は次の通り。

- G2 v5 working roster: `research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json`, Git blob `b97b67a34ad9c2858745dfa6aa60444520eaab13`
- G2 actual source receipts: `research/paper2/p399/g2/MAIN40_G2_ACTUAL_SOURCE_RECEIPTS_AND_DECISIONS_v2.json`, Git blob `ac3ffa59fcdc078550df587bc972632b7ca5ff7f`
- G2 legacy 780+800 family register: `research/paper2/p399/g2/MAIN40_G2_780_MAIN_AND_800_G1_FAMILY_RECONCILIATION_v2.json`, Git blob `2ffc0e2056e1185d99f5f8f3cc4e24814a6ec286`
- LRN-01 dual publisher acquisition: `research/paper2/p399/g2/MAIN40_G2_LRN01_FIRST_PARTY_DUAL_PHYSICAL_ACQUISITION_v5.json`, Git blob `cf4914465563d62644a6f7d94d2db631c6ccc635`
- Existing 26-profile accelerator ledger: `research/paper2/p399/g4/genealogy_accelerator_v1/ORIGINAL_NATIVE_PROFILES_v1.json`, Git blob `903f8db6e1569ed27507cf47e668f7599a08cd98`

Main article raw SHA256は6本すべて既存G2 receiptから保持した。LRN-01はpublisher PDFの独立二重取得run 37185492865 / 37185593074も維持した。

## source-native科学所見

### CTL

**CTL-01** は、context-specific Bayesian planningをchoice+RTへ拡張するBCCである。論文固有に凍結した中心は、context-conditioned policy posterior、adaptive policy prior、independent MCMC policy sampler、precision/entropy stoppingによるRTである。DDMはS2 Appendixで関係を検討する comparator であり、MCMC samplerをDDM機構へ同一化しない。base BCCは前研究からの直接継承として DOI `10.1016/j.jmp.2020.102472` を保持した。

**CTL-02** は neural / Bayesian / algorithmic の三レベルを分離した。paper-specific centerは、TAN pause/uncertainty feedback、OpAL opponent actor weight decay、Beta-belief uncertaintyによるflexibility制御である。OpALそのものは新規発明とせず、明示的祖先 DOI `10.1037/a0037015` を保持した。神経相関・回路モデルを、直接実証された生物学的controllerへ昇格させていない。

**CTL-03** は、cTBS/control-demandという実験操作、fitted DCM、行動/fMRI evidenceを分離した。2016 DCM DOI `10.7554/eLife.12112` を直接祖先として保持する。現サンプルでは913 DCMの探索から単一一意解ではなく19候補が残り、過去サンプルでの追加adjudicationを使っている。未検査modulationの可能性、以前のtrait relation非再現、予測外SFS効果によるmodel revisionを adverse evidence として残した。

### LRN

**LRN-01** は generic policy-gradient RLをpaper-specific noveltyへ数えず、reward objectiveから `lambda I(S;Z)` を差し引くefficient-coding objective、latent encoder/decoder policy、両者のgradient updateを中心として凍結した。task schedule、experimenter-defined feature embedding、RLPG/CPG等のcomparatorsをrepresentation-learning operatorから分離した。source-supportedな直接祖先DOIは無理に追加していない。

**LRN-02** は、VKFのstate mean/variance update、volatility error-correction、binary moment-matching、latent-space learning rateを中心として凍結した。Behrens DOI `10.1038/nn1954` とHGF DOI `10.3389/fnhum.2014.00825` は本文がconceptual derivationを明示するためpositive ancestryとして保持した。latent-space learning rateとobservation-space implied learning rateを同一視しない。

**LRN-03** は、decision RNNのrecurrent policy gradient、value RNNのreward baseline、reward-based weight updateを中心として凍結した。REINFORCE/recurrent-policy-gradient自体は継承constituentであり、Wierstra DOI `10.1093/jigpal/jzp049` をmethod ancestryとして保持した。value networkは学習を安定化するが学習後task executionには不要なので、task controllerそのものへ昇格させていない。

## edition / supplement / correction bundle

CTL-01のPLOS S1/S2 Appendix、LRN-01のNature Supplementary Information、LRN-02のPLOS S1/S2 Appendixは、中心数理を支える**required same-article bundle**としてprofileから消せないよう固定した。

既存G2 receiptにはこれらsupplement単体のraw SHA256が別途凍結されていない。このため3件をnonblocking provenance gapとして明示した。これは「補足未取得」や「補足不存在」という判定ではない。公式identity/linkと役割は保持され、main Version of Recordのraw SHAは全6本で固定済みである。

別correction/corrigendumは今回のbounded publisher reviewでは同定していないが、これを網羅的な「訂正なし」証明へ昇格させていない。

## bounded pair adjudication

`W2_BOUNDED_PAIR_ADJUDICATIONS_v1.json` に **37件**を記録した。

- W2内部6本の全15組
- CTL priority: P11 / P12 / P17
- LRN priority: P13 / P14 / P15 / P19
- source-supported additional positive-priority: CTL-01 × INT-01、LRN-03 × INT-08

内訳は `BOUNDED_SOURCE_NATIVE_DIFFERENCE=27`、`SHARED_CONSTITUENT_ONLY=10`。  
`DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY=0`、`UNDERDETERMINED=0` は「残余pairがclear」という意味ではない。

特に CTL-01 × P12 は旧G2 ledgerが「CTL-01原著がP12を引用」と記録するが、旧ledger自身がcitation onlyとしているため、direct ancestryには昇格させなかった。

各pairで `main_promotion_allowed=false`、`global_independence_inferred=false` を固定した。bounded differenceはglobal independenceではない。

## source gaps / genealogy limits

Blocking source gap: **0**。

Nonblocking gapは9件。

1. CTL-01 required supplement raw SHA未凍結
2. LRN-01 required supplement raw SHA未凍結
3. LRN-02 required supplement raw SHA未凍結
4. 6本それぞれの ancestry exhaustiveness 非証明

従って全6本はprofile fragmentとしてREADYだが、**global family independenceは6本とも未認定**であり、系譜探索の網羅性も認定していない。

## fail-closed test contract

`test_w2_fail_closed.py` は少なくとも次を破壊的に守る。

- exact six DOI identities
- duplicate paper禁止
- CTL/LRN以外のW2 profile混入禁止
- operator IDの `<slot>:<operator-name>` prefix
- Git provenance path + 40-hex blob/ref
- global independence true禁止
- MAIN authorization true禁止
- ancestry exhaustiveness promotion禁止
- required supplement bundle消失禁止
- blocking source gapがあるpaperのREADY禁止
- pair judgment vocabulary固定
- pairからMAIN/global independenceへのpromote禁止
- W2内部15 pairの欠落禁止
- shared profile fileをW2 outputとして扱わない

テストは最終W2 HEAD上で実行し、その結果はDraft PR metadataと完了時報告に記録する。

## 明示的 MAIN NO-GO

**MAIN NO-GO。**

W2はsource-native profile fragmentとbounded pair evidenceだけを生成した。preliminary MAIN structural outcomes、Grammar-v0 decomposition/reconstruction、H0/H1/H2、Paper 2最終科学結論を閲覧・実行していない。G1 decisions、backup、MAIN40 roster、shared #438 profile ledger、shared pair-matrix code、shared CIも変更していない。
