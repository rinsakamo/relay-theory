# RelayTheory Paper 2 — G4 W8-A 完了報告

## Authority / isolation

- Primary authority: Issue #399
- W7 integration authority: Draft PR #447
- Frozen W7 HEAD: `4325a9a4cba4da651e7cdf2617f7bc8b08c90f54`
- W8-A branch: `paper2/p399-g4-w8a-ancestry-resolution-20261005`
- W8-A は W7 の 51/60 profile registry と 1,580-pair matrix を直接書き換えない。
- W8-S の5件の supplement 取得、G1 internal 190-pair audit、Grammar-v0、H0/H1/H2、MAIN outcome は扱っていない。
- global independence は一件も promote せず、MAIN scientific authorization は false のまま。

## 科学判定

| Paper | W8-A status | Direct ancestry | Non-DOI |
|---|---|---|---|
| CNC-01 | ANCESTRY_RESOLVED_NON_DOI_NODE_REQUIRED | Liang / Jordan / Klein 2010 ICML への DIRECT_ADAPTATION | 必要 |
| MEM-01 | ANCESTRY_RESOLVED_NON_DOI_NODE_REQUIRED | ACT-R declarative-memory の限定された source-defined mechanism lineage | Lebiere 1999 workshop node が必要 |
| INT-03 | ANCESTRY_RESOLVED_DIRECT_EDGE | 1989 / 1991 / 1993 / 1997 Dehaene–Changeux models への明示的 DIRECT_EXTENSION | 不要 |
| INT-06 | ANCESTRY_RESOLVED_DIRECT_EDGE | Brunel–Wang 2001 local recurrent module と Lo–Wang 2006 threshold circuit への DIRECT_IMPLEMENTATION_DESCENT | central direct edge には不要 |

4件の profile-level `SCIENTIFIC_ANCESTRY_UNDERDETERMINED` は、W8-A の限定範囲では 0 件になった。ただしこれは W9 未統合の proposal であり、W7 registry の status/count は不変である。

## CNC-01

Nature Human Behaviour の本文は Liang et al. 2010 の algorithm を明示的に adapt すると述べ、cache/share/reuse を行う combinatory-logic / adaptor-grammar program-learning machinery を process-level conceptual bootstrapping に転用している。CNC-01 側の新規部分は、固定 primitive set ではなく、利用価値に応じて更新される latent concept library と bounded search を導入した点である。

Liang / Jordan / Klein の predecessor は official ICML 2010 paper #568、pp.639–646 と DBLP key `conf/icml/LiangJK10` で一意に同定でき、DBLP は DOI を持たない record としている。したがって DOI 不在を ancestry 不在に読み替えるのは科学的に不適切で、non-DOI bibliographic node が必要である。Liang 論文がさらに用いる combinatory logic / nonparametric Bayesian antecedents は constituent history として認識するが、CNC-01 からそれらへの transitive direct edge は追加しない。

## MEM-01

MEM-01 は独立に新しい memory architecture を発明する paper ではなく、ACT-R declarative-memory system の計算機構を神経生物学へ写像する統合である。bounded genealogy として次を固定した。

- Anderson 2007: ACT-R declarative-memory algorithmic implementation の architecture-level source。
- Anderson & Schooler 1991: equation 3 の base-level / power-law trace accumulation。
- Pavlik & Anderson 2005: equations 4–5 の activation-dependent trace-specific decay。
- Lebiere 1999: equation 8 の blending / aggregate retrieval。
- Anderson, Reder & Lebiere 1996 は partial matching / source activation の source-backed constituent だが、MEM-01 が equation 7 の唯一の起源として明示していないため `SHARED_CONSTITUENT` に留める。
- Anderson et al. 2004 は `SHARED_FRAMEWORK`。

ACT-R 全史の再構築は行わない。non-DOI book node は今回の bounded central-operator resolution には不要だが、blending が Lebiere 1999 Sixth Annual ACT-R Workshop contribution に明示的に帰属するため、non-DOI proceedings node は必要である。

## INT-03

1998 PNAS 本文は、その minimal scheme が delayed response、card sorting、number processing、planning の4つの former model attempts を **extends** すると明記し、それらに共通する effortful-task architecture を Stroop / global-workspace model に一般化している。従って著者重複ではなく descendant 自身の relation statement を根拠に direct extension を認定できる。

exact predecessors は以下である。

1. Dehaene & Changeux 1989 — DOI `10.1162/jocn.1989.1.3.244`
2. Dehaene & Changeux 1991 — DOI `10.1093/cercor/1.1.62`
3. Dehaene & Changeux 1993 — DOI `10.1162/jocn.1993.5.4.390`
4. Dehaene & Changeux 1997 — DOI `10.1073/pnas.94.24.13293`

reward-modulated Hebbian rule は 1989 predecessor に、reward-conditioned short-term stability は 1989/1991/1997 predecessors に source-located linkage がある。これ以上の transitive chain は自動生成しない。

## INT-06

PLOS 本文自身が、この model は既存要素を利用する一方、novel aspect はそれらを global functional architecture に統合することだと境界を引いている。このため引用文献をすべて direct ancestor にすることはしない。

source-explicit direct implementation descent は2本に限定した。

- Brunel & Wang 2001 — DOI `10.1023/A:1011204814320`: local sensory/router recurrent module と、INT-06 が「same」とする local synaptic efficacies。
- Lo & Wang 2006 — DOI `10.1038/nn1722`: response-selection threshold / cortico-basal-ganglia motor gating circuit。INT-06 は response execution / motor commands をこの predecessor に従って model/simulate すると明示する。

Wang 2002 は `SHARED_CONSTITUENT`、Dehaene–Sergent–Changeux 2003 は `SHARED_CONSTITUENT`、Dehaene–Changeux 1997 の termination signal は「similar」とされるため `SHARED_CONSTITUENT` とした。

**INT-03 → INT-06 の direct edge は作らない。** 両者には broader workspace/recurrent lineage があるが、INT-06 は INT-03 の exact model を直接継承したとは source-explicit に述べず、central operator も task-set-controlled NMDA router + threshold circuit で異なる。したがって両者の relation は `SHARED_FRAMEWORK` に限定する。

## Schema extension

`DOI_WORK` と `NON_DOI_BIBLIOGRAPHIC_WORK` の2 node type を提案する。non-DOI node は exact title / authors / year / venue / locator / proceedings authority / stable locator / descendant citation locus を要求し、title-only node は reject する。repository-local ID は `rt-biblio-` prefix と normalized bibliographic identity の hash suffix を用い、外部 identifier として扱わない。

今回必要な non-DOI node は2件だけである。

1. `rt-biblio-liang-jordan-klein-2010-learning-programs-fb673590fbc7`
2. `rt-biblio-lebiere-1999-actr-blending-b876f955be9a`

この extension は「DOI が無いから ancestry を見えなくする」ことと「実在しない DOI を作る」ことの両方を避けるため科学的に必要である。

## W9 integration implications

W9 はこの branch の JSON を独立検証したうえで、4 profile の ancestry status と node/edge delta を取り込める。W8-A は W7 shared matrix を silent rewrite していないため、W9 は profile registry と pair matrix の整合性を改めて reconcile する必要がある。特に shared-framework / shared-constituent edge を global independence の positive evidence に反転してはならない。

W8-A が解いたのは **4 ancestry blockers のみ**。W7 の5 `SOURCE_BLOCKED` は W8-S の管轄であり、この branch では0件解決した。W7 pair matrix に残る broader `UNDERDETERMINED` rows も未処理である。

## Safety state

- direct ancestry edges resolved: **11**
- non-DOI nodes required: **2**
- remaining profile-level ancestry blockers among these four: **0**
- W7 profile count rewritten: **no**
- W7 1,580-pair matrix rewritten: **no**
- global independent count promoted: **no**
- MAIN authorization: **false**
