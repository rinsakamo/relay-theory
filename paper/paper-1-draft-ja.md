# 作業稿 — Paper 1 日本語訳

> **位置づけ:** 英語原稿の読解・監査用日本語訳。投稿用の正本は英語版。
> **射程:** operational individuation inference に対する、必要な構造条件と evidential-dependency 条件。
> **形式的境界:** target domain と representation-to-target assignment はモデル入力である。structural factorization 自体は scientific warrant を与えない。

# 形式的な差は、いつ個体化推論に入ることができるのか？
## Target Factorization、Restricted Tests、そして Cross-Domain Audits

## 要旨

表現間に形式的な差があるという事実だけでは、target-level の individuation は正当化されない。exact deterministic な representation-to-target model の内部で、declared scope 全体にわたり universally sound な difference discriminator として用いる feature は fiber-invariant でなければならず、したがって target-induced quotient を介して descend しなければならない。その一方で scientific warrant は独立に必要である。さらに、representation-level observation を structurally admissible な test family を通じて target-level outcome に接続し、individuation-inference audit を定式化する。複数領域の事例で枠組みを例示し、機械検証された証明によって quotient descent と family-level separation を確認する。より一般的な methodological lesson は条件付きであり、formal distinction を target-level distinction に用いるには、declared target への warranted route が必要である。本枠組みはその assignment 自体を発見せず、unrestricted numerical identity も確立しない。

## 1. はじめに

形式的な representation は、それを用いて行う target-level の主張より多くの区別を含むことがある。異なる変数名、database record、file-level identifier、label、constructor は、形式的には区別できても、その差が distinct target-level individual を追跡しているとは限らない。

この問題は、身近な論文データベースを考えると直感的に分かる。一つの scholarly work が、OpenAlex、Crossref、PubMed などのサービス上で別々の bibliographic record として表現されることがある。\(P\) を bibliographic record の集合、\(T\) を宣言された scholarly work の target domain とし、

\[
r:P\to T
\]

を record-to-work assignment とする。二つの record \(A,B\in P\) について、\(\operatorname{ID}\) を service-qualified record identifier とする。このとき、

\[
\operatorname{ID}(A)\neq\operatorname{ID}(B)
\quad\not\Rightarrow\quad
r(A)\neq r(B).
\]

identifier が異なることは、record が異なることを確かに示す。しかし、それが scholarly target の差についての evidence になるのは、target model とその warrant がその関係を正当化するときだけである。これは entity resolution の問題を非常に分かりやすい形で表したものであり、record multiplicity は entity multiplicity を自動的には意味しない (Aleshin-Guendel and Steorts 2024)。

逆向きの近道も成立しない。unqualified identifier value が異なる namespace に局所的な値であったり、再利用・複製されたり、誤って付与されたりするなら、その unqualified value を \(\operatorname{rawID}\) と書く。このとき、

\[
\operatorname{rawID}(A)=\operatorname{rawID}(B)
\quad\not\Rightarrow\quad
r(A)=r(B).
\]

database が外部から付与した metadata も、自動的に target property になるわけではない。topic label、category、その他の externally assigned tag は、同じ work の record 間で異なることもあれば、異なる work の record 間で一致することもある。そのような field が target-level evidence になるには、declared target との関係が独立に正当化されなければならない。

この bibliographic example は target choice の重要性も示す。同じ preprint と journal publication を、ある counting question では一つの research work としてまとめ、別の question では異なる publication version として扱うことができる。したがって record multiplicity は work multiplicity を決定せず、publication-version multiplicity も research-work multiplicity を決定しない。identifier や label を解釈する前に、何を target として individuate するのかを宣言する必要がある。

二つの bibliographic record は形式的に異なっていても、それだけで二つの異なる論文を表すとは限らない。同様に、二つの theoretical label が異なっていても、それだけで二つの異なる measured capacity が存在することは確立されない。

問題は representation-level structure が無用だということではない。それは computation、bookkeeping、locality、provenance、search、model construction に不可欠かもしれない。問題が生じるのは、その structure 内の差が individuation inference の premise として使われるときである。

本稿は、意図的に狭い問いを扱う。

> **representation 内の formal difference は、どのような場合に、represented target を operationally distinct と扱う inference に入ることができるのか。**

本稿の答えには、混同すべきでない二つの層がある。

第一は **structural condition** である。representation-level feature は declared target assignment を介して factor しなければならない。あるいは representation-level observation が、declared test のもとで target-level response と一致しなければならない。そのような factorization がなければ、その formal difference は representation 内の差にとどまる。

第二は **scientific-warrant condition** である。factorization を書けること自体は、それが真であり、信頼でき、evidentially adequate であることを意味しない。experimental、causal、measurement、calibration、semantic practice が、その factorization を target relation の妥当な model として扱うことを独立に正当化しなければならない。

formal artifact が扱うのは第一の層だけである。それは structural dependency を監査可能にするが、第二の層を作り出すものではない。

この分離から、実践的な **counterfactual relevance audit** が導かれる。identifier-like feature について、どの種類の変更を考えているのかを問う。structure-preserving re-encoding は、inference が evidentially relevant と宣言した representation-level relation をすべて保存するなら、結論を変えるべきではない。一方、representation 間で value を再割当てすることは、その assignment 自体が scientifically grounded な relation を記録しているなら evidence を変えうる。assignment perturbation によって結論が変わるなら、その assignment がなぜ単なる representational difference ではなく target-relevant なのかを説明しなければならない。

bibliographic case だけなら、これは bookkeeping や data integration の話に見えるかもしれない。そこで Section 3 では molecular counting を cross-domain scientific stress test として用いる。その後、同じ区別を evidence synthesis に戻し、report、study、estimate、independent evidence unit を混同してはならないことを示す。流れは意図的である。直感的な record linkage から experimental measurement へ進み、最後に literature-scale inference へ戻る。

したがって novelty claim は狭い。本稿は target-directed representation、invariance、quotient mathematics、practice-relative individuation のいずれか単独を新規性として主張しない。貢献は、それらを一つの feature-level audit に統合し、quotient descent、test-specific transfer、independent scientific warrant、representation-preserving counterfactual check を individuation inference の中で分離することである。

したがって本稿の payoff は theorem-theoretic ではなく diagnostic である。この audit は既知の structural fact を local conservativity test として用いることで、individuation argument のどの段階で target assignment、observational bridge、independent warrant、permissible representational structure が導入されなければならないかを特定し、representational leakage と通常の evidential gap を区別する。

### 1.1 貢献

本稿の貢献は、限定的に四点である。

1. **structural admissibility の quotient characterization。** representation-level feature が target-level で structural に利用可能であるためには、proposed representation-to-target map の各 fiber 上で constant でなければならない。同値に、同じ target に assignment された representation を同一視する quotient へ descend しなければならない。

2. **test-family admissibility。** representation-level observation と target-level response を一つの inference chain に置く。selected family 内の全 test が declared target-response factorization を持つことを要求すれば、追加の witness-selection assumption なしに、その family による existential separation を license するための conservative sufficient condition が得られる。

3. **再利用可能な individuation-inference audit。** within-fiber leakage、observation-to-target bridge、independent warrant、structure-preserving re-encoding、assignment sensitivity、regime overreach を検査する protocol として structural condition をまとめる。

4. **machine-checked dependency analysis と cross-domain case。** 機械検証された証明により quotient descent と family-level separation を確認する。bibliographic record を motivating case、molecular counting を cross-domain scientific stress test、evidence synthesis を study-level / claim-level analysis へ拡張する事例として用いる。

## 2. 形式的設定

### 2.1 Representation と target

\(P\) を representation の集合、\(T\) を target domain とする。

\[
r:P\to T
\]

を representation-to-target assignment とする。\(P\) の異なる要素が \(T\) の異なる要素を表すとは仮定しない。

assignment \(r\) は modeling input である。本稿は raw observation から \(r\) を推定せず、\(T\) の ontology も導出しない。source assignment 自体が不確実な応用では、本枠組みは提案された assignment model を監査するのであって、source-assignment problem を解くものではない。

したがって、この formalism の inferential role は非対称である。これは observed representation-level difference から \(r\) を発見する procedure ではない。提案済みの \(r\) を条件として、discriminator が同じ fiber 内で変化する distinction を持ち込まずに、その assignment と両立するかを監査する。したがって \(f(a)\neq f(b)\) の observation 自体は target assignment を構成も検証もしない。\(r(a)\neq r(b)\) への implication が license されるのは、関連する factorization に独立した scientific warrant がある model の内部だけである。

exact formal core は、一つの representation に一つの target value を割り当てる場合に限定する。many-to-many、distributed、probabilistic correspondence は自然な拡張だが、本稿の主張の外に置く。

### 2.2 Structural target factorization と quotient descent

representation-level feature を

\[
f:P\to V
\]

target-level property を

\[
\phi:T\to V
\]

とする。次を **target-factorization condition** と呼ぶ。

\[
F_r(f,\phi)
\quad\Longleftrightarrow\quad
\forall p\in P,\; f(p)=\phi(r(p))
\]

\(F_r(f,\phi)\) が成立するなら、

\[
f(a)\neq f(b)
\quad\Longrightarrow\quad
r(a)\neq r(b)
\]

である。

同じ内容は、より一般的な structural characterization として書ける。

\[
a\sim_r b
\quad\Longleftrightarrow\quad
r(a)=r(b)
\]

とし、\(\pi_r:P\to P/{\sim_r}\) を、同じ target に割り当てられた representation を同一視する quotient map とする。\(f\) が **fiber-invariant** であるとは、

\[
r(a)=r(b)
\quad\Longrightarrow\quad
f(a)=f(b)
\]

が成立することをいう。さらに、proposed target assignment に相対した feature-difference inference の universal soundness を

\[
D_r(f)
\quad\Longleftrightarrow\quad
\forall a,b\in P,\;
f(a)\neq f(b)\Longrightarrow r(a)\neq r(b)
\]

と定義する。通常の classical logic のもとでは、これは fiber invariance の contraposition である。したがって structural core は三者同値として書ける。

\[
\begin{aligned}
&\forall a,b,\;r(a)=r(b)\Rightarrow f(a)=f(b) \\
\Longleftrightarrow\;&
\forall a,b,\;f(a)\neq f(b)\Rightarrow r(a)\neq r(b) \\
\Longleftrightarrow\;&
\exists\,\bar f:P/{\sim_r}\to V
\text{ such that }f=\bar f\circ\pi_r .
\end{aligned}
\]

つまり **fixed proposed target assignment を条件とすれば**、fiber invariance、feature-difference inference の universal soundness、target quotient への descent は同値である。これは、その assignment に相対して feature difference を universally sound な discriminator として使うための必要十分な structural criterion であって、assignment 自体を発見・正当化する procedure ではない。Lean development はこの三者同値を generic に検証する。

\(f=\phi\circ r\) なら、\(f\) は必ず \(P/{\sim_r}\) を介して descend する。逆に quotient descent が保持するのは、same-target difference を忘れた後にも残る representation-level information ちょうどそのものである。descended feature を \(T\) 全体上の property として解釈するには、\(r\) の represented image 外まで extension する追加 convention が必要だが、その off-range value は現在の inference には evidential work をしない。

したがって operational anti-smuggling rule は単純である。proposed target map の一つの fiber 内で変化する feature は target quotient を介して descend せず、その同じ model の下では target-level evidence として使えない。

ただし structural descent 自体は **evidential warrant ではない**。これは representation-level feature が proposed target assignment だけに依存するための構造条件を述べるだけである。科学的応用がその model を受け入れてよいかどうかは formal identity の外部の evidence に依存する。

その warrant は calibration data、causal production process、validated measurement / error model、intervention protocol、target reference が独立に固定された semantic convention などから得られうる。本枠組みはそれらを rank したり導出したりしない。関連する warrant を \(r\)、\(\phi\)、selected test の中に暗黙に埋め込まず、明示することを要求する。

さらに warrant は **non-self-licensing** でなければならない。問題となっている formal difference 自体を、すでに target distinction を成立させるものとして扱うことだけから warrant を得てはならない。row identifier、barcode string、constructor name は、異なる値を異なる target として parameterize しただけでは target evidence にならない。

\(r\) を representation-level difference をすべて encode するほど細かく選べば、多くの feature を descend / factorize させられる。しかし、それはその \(r\) が科学的に適切であることを示さない。target assignment とその justification は substantive input のままである。

### 2.3 Test-specific observation factorization

前節の feature-level condition は test に直接接続できる。

\(Q\) を test のクラスとし、

\[
\widehat O:Q\times P\to Y
\]

を representation から実際に読み取られる outcome、

\[
O:Q\times T\to Y
\]

を model が想定する target-level response とする。

特定の test \(q\) に対して、

\[
B_r(q)
\quad\Longleftrightarrow\quad
\forall p\in P,\;
\widehat O(q,p)=O(q,r(p))
\]

と定義する。

これは test-specific structural factorization である。この条件の下で、

\[
B_r(q)
\land
\widehat O(q,a)\neq \widehat O(q,b)
\quad\Longrightarrow\quad
r(a)\neq r(b)
\]

となる。

したがって、二つに分かれていた module ではなく、単一の inference chain が得られる。

\[
\text{representation-level observation}
\to
\text{target factorization}
\to
\text{target-level response}
\to
\text{operational separation}
\]

ここでも式は自分自身を正当化しない。scientific application は measurement や protocol がなぜ \(B_r(q)\) を妥当な approximation または idealization にするのかを説明しなければならない。

### 2.4 Selected test family

\(A\subseteq Q\) を analysis のために選択された test family とする。**structural family-level admissibility** を

\[
\operatorname{Adm}_r(A)
\quad\Longleftrightarrow\quad
\forall q\in A,\;B_r(q)
\]

と定義する。

selection 自体には evidential force はない。independently specified な特定の test \(q\) については test-specific theorem は \(B_r(q)\) だけを要求する。より強い \(\operatorname{Adm}_r(A)\) は、追加の witness-selection rule なしに「\(A\) のどれかが pair を分離した」と報告できる inference に用いる。

したがって family-wide requirement は every particular witnessed inference の necessary condition ではなく、conservative sufficient condition である。その methodological purpose は、post hoc licensing の一つの structural form、すなわち先に discriminator を探索し、selected witness に対してのみ admissibility を後から確立することを block する点にある。relevant test の scientific warrant は引き続き独立に与えられ、formal difference 自体によって self-license されてはならない。

ここでいう *test family* は structural な概念であって statistical multiplicity correction ではない。\(\operatorname{Adm}_r(A)\) は family-wise error、false-discovery rate、selective inference、researcher degrees of freedom を control しない。それらは test outcome や witness selection が stochastic / data-adaptive な場合に生じる別問題であり、present exact deterministic core は multiplicity correction を与えない。

\[
a\equiv_A b
\quad\Longleftrightarrow\quad
\forall q\in A,\;
\widehat O(q,a)=\widehat O(q,b)
\]

および

\[
a\mathrel{\#_A}b
\quad\Longleftrightarrow\quad
\exists q\in A:\;
\widehat O(q,a)\neq\widehat O(q,b)
\]

とする。このとき factorization と restricted-test layer は

\[
\operatorname{Adm}_r(A)
\land
a\mathrel{\#_A}b
\quad\Longrightarrow\quad
r(a)\neq r(b)
\]

を与える。separating witness \(q\in A\) は \(\operatorname{Adm}_r(A)\) により \(B_r(q)\) を満たすため、その observed difference を target level へ移せる。Lean development は対応する有限 theorem を検査する。

また \(A_c\subseteq A_f\) なら、\(A_f\) の下での indistinguishability は \(A_c\) の下での indistinguishability を含意する。逆は一般に成立しない。これは fixed exact semantics と set inclusion についての theorem であり、noisy evidence の蓄積が classification を反転させないという主張ではない。

### 2.5 Individuation-inference audit protocol

以上の条件は、再利用可能な audit protocol として用いることができる。これは individual を発見する automated decision procedure ではなく、proposed individuation inference が必要な dependency を明示しているかを段階的に検査するものである。

1. **Target model と scope を宣言する。** \(P\)、\(T\)、proposed assignment \(r\)、selected test family \(A\)、結論の強さを固定する。固定されていなければ audit は underdetermined である。
2. **Quotient descent を検査する。** candidate discriminator が \(r\) の各 fiber 上で一定かを問う。within-fiber difference は target-level use に対する structural failure である。
3. **Observation bridge を検査する。** pre-specified test \(q\) なら \(B_r(q)\) を確立する。analysis が \(A\) から arbitrary separating witness を選べるなら、より強い \(\operatorname{Adm}_r(A)\) を確立するか、independently fixed な witness-selection rule を与える。
4. **Independent warrant と representation structure を検査する。** \(r\)、factorization、selected family、inference が利用する representation-level relation / function / metric（以下 \(\mathcal S\) と表す）を受け入れる scientific reason を明示する。これらは non-self-licensing でなければならない。confirmatory use では discriminating comparison より前に固定し、adaptive に学習・選択するなら、その selection rule 自体を inference の一部として監査する。
5. **Counterfactual と scope を検査する。** structure-preserving re-encoding に対する invariance を調べる。assignment perturbation で結論が変わるなら、その sensitivity を evidentially relevant にする grounded relation を示す。最後に、結論を selected observational / interventional regime が支える範囲より強くしない。

audit の disposition は三つに整理できる。quotient / factorization condition の違反は **structural failure**。構造的には coherent でも independent warrant が足りなければ **scientifically underdetermined**。両層を通過した場合は **scoped pass** であり、declared target model と regime に相対して license されるだけで、unrestricted numerical identity を確立するわけではない。

## 3. Scientific Stress Test: Unique Molecular Identifier による分子カウント

### 3.1 多数の read が多数の source molecule を意味しない理由

**unique molecular identifier (UMI)** とは、amplification より前に導入される短い sequence tag であり、downstream observation がどの template molecule に由来するかについての情報を保持できるようにするためのものである。UMI は molecule が本来的に持つ identity ではない。protocol によって生成・付与される tag であり、その evidential value は assignment、propagation、observation、modeling の仕方に依存する。Kivioja et al. (2012) は、この種の tag を absolute molecule counting に利用できることを示した。

**polymerase chain reaction (PCR; ポリメラーゼ連鎖反応)** は、一つの template molecule から多数の copy を生成しうる amplification process である。それらの copy から複数の sequencing read record が生じうる。したがって、

\[
100\ \text{read records}
\not\Rightarrow
100\ \text{source molecules}.
\]

各 read に unique software identifier を付ければ100個の record はすべて区別できるが、それだけでは100個の pre-amplification molecule を推論する独立の理由にはならない。逆に UMI が等しいことも target identity の絶対的保証ではない。有限の tag space では、異なる template が同じ tag value を受け取る collision が起こりうるからである。

Smith, Heger, and Sudbery (2017) が示すように、observed UMI string には sequencing error も入りうるため、error-aware analysis が必要になる。したがってこの事例では、**record identity、protocol-generated tag identity、source-molecule identity** という三つの概念を明確に分離する必要がある。

### 3.2 Target は string ではなく tagged template である

この事例で最も明確な target domain は、barcode から直接読める抽象的な molecule identity の集合ではない。\(T\) を、**UMI assignment 後かつ PCR amplification 前の tagged template molecule** の集合とする。

\[
u:T\to U
\]

を tagged template molecule に割り当てられた latent UMI とする。downstream read record が \(P\) を構成し、\(r(p)\) は read \(p\) が由来する tagged template とする。

sequencing が error-free で、各 read 上の observed UMI field が assigned molecular tag を正確に再現するなら、observed tag feature \(\widehat u:P\to U\) は

\[
\widehat u(p)=u(r(p))
\]

を満たす。これは target-factorization condition にほかならない。

現実の data ではこの等式は保証されない。sequencing error は observed string の一塩基を変えることがあり、PCR や library effect が observation process を複雑化しうる。また、異なる template が collision により同じ UMI value を受け取ることもある。したがって実際の inferential chain は、

\[
\text{tagged template}
\to
\text{latent assigned UMI}
\to
\text{amplification}
\to
\text{noisy observed UMI on reads}
\]

と考える方が適切である。

exact formal factorization が表すのは no-error dependency skeleton であり、latent assigned tag と observed read-level string を結ぶ error model の代わりではない。

### 3.3 Error と collision を同時に含む synthetic example

三つの tagged template を考える。

- \(m_1\) の latent assigned UMI は *ACGT* で、observed UMI が *ACGT*, *ACGT*, *ACGC* の三つの read を生成する。
- \(m_2\) の latent assigned UMI は *TGCA* で、observed UMI が *TGCA*, *TGCA*, *TGCA* の三つの read を生成する。
- \(m_3\) も latent assigned UMI *ACGT* を持ち、observed UMI が *ACGT*, *ACGT* の二つの read を生成する。

read record は八つ、tagged template は三つである。*ACGC* は \(m_1\) の latent tag から生じた sequencing error を表し、\(m_1\) と \(m_3\) は UMI collision を表す。

異なる observed UMI string を異なる source molecule と同一視する naive rule は、*ACGT*, *ACGC*, *TGCA* の三 group を返す。そのため数だけ見れば tagged template の真の個数三と一致する。しかし partition は二方向に誤っている。sequencing error により \(m_1\) を分割し、collision により \(m_1\) と \(m_3\) の evidence を併合している。したがって numerical agreement は偶然に生じうる。

error-aware model は *ACGC* を *ACGT* tag と compatible に扱えるが、collision 後の \(m_1\) と \(m_3\) を UMI sequence だけで分離することはできない。追加の genomic / transcript / library context、あるいはその他の experimentally warranted information が必要になりうる。

この例では三つの層が明確になる。

1. unique read ID は八つの record を individuate するが、tagged template を overcount する。
2. latent assigned UMI は protocol によって生成された target property だが、collision のため UMI equality は target identity の十分条件ではない。
3. observed UMI string は latent tag の noisy measurement であり、raw string inequality は一つの target を過剰に分離しうる。

idealized model の exact target factorization を満たすのは第二層である。第三層には error model が必要であり、第一層は独立した target link が与えられない限り representation-level bookkeeping にすぎない。三つの candidate procedure は異なる audit outcome も示す。unique read ID は molecular source assignment を介して factorize しない。raw observed-string equality は target-linked ではあるが sequencing error の下で exact observation factorization を満たさず、collision の下では non-injective のままである。error-aware inference が admissible なのは、その measurement / error model が独立に warrant されている範囲に限られる。

この construction は diagnostic であり、特定の現在の UMI pipeline の model ではない。また contemporary tool が単純に distinct raw string を数えているという主張でもない。目的は、documented な二つの問題である sequencing error と UMI collision を、一見正しい scalar count が誤った source partition を隠しうる透明な例の中へ置くことである。

| Representation-level basis | Audit diagnosis | 必要な追加 warrant |
| --- | --- | --- |
| Unique read ID | 一つの molecular-source fiber 内で変化し、source assignment を介して factorize できない。 | bookkeeping identity とは独立した source link。 |
| Raw observed UMI string | sequencing error が一つの target を split し、collision により同じ tag が異なる target と両立する。 | error/collision model と experimentally relevant な context。 |
| Error-aware UMI inference | target-relevant structure を使いうるが、barcode type 自体で admissibility は保証されない。 | validated measurement/error assumption と protocol/context support。 |

### 3.4 本枠組みが診断するもの

本枠組みは「UMI difference は molecule difference である」とは言わない。より限定されたことを述べる。

read-level feature が molecular individuation inference に入るためには、その feature が target からどのように生成されたかを説明する justified model を経由しなければならない。UMI の場合、experimental tagging protocol、genomic または transcript context、error model が科学的な仕事を担う。string という型そのものには、その evidential force はない。

このため、この事例は哲学的にも有用である。二つの field がともに identifier であり、ともに string であり、ともに record を区別できたとしても、target を追跡するよう設計された causal and measurement history に参加するのはそのうち一方だけかもしれない。

同じ事例は audit disposition の違いも明示する。source-molecule fiber 内で変化する software read ID は structural test に失敗し、その差は target quotient を介して descend しない。sequencing noise の下にある raw observed UMI string は別の仕方で observation-to-target bridge に失敗しうる。すなわち observed string inequality が latent tag inequality を再現するとは限らない。tagging / error assumption が independent support を欠く error-aware UMI model は、formal に admissible でも scientifically underdetermined のままである。relevant protocol、error model、contextual assumption が独立に warrant されて初めて inference は scoped pass を得る。これらは declared target model に相対した inference の disposition であり、UMI technology 一般についての主張ではない。



## 4. Counterfactual Relevance Audit

“relabeling invariance” は、重要に異なる二種類の perturbation を隠しうる。無害な変更とは常に arbitrary bijection なのではなく、inference が実際にどの representation-level structure を利用しているかに依存する。

### 4.1 Structure-preserving re-encoding

\(U\) を identifier-like field の value domain、\(\mathcal S\) を inference が evidentially relevant と宣言した \(U\) 上の relation の集合とし、利用する function や metric も必要なら relational encoding として含める。re-encoding \(\pi:U\to U\) が \(\mathcal S\) に相対して **structure-preserving** であるとは、\(\pi\) が bijection であり、各 declared relation を保存することをいう。\(k\)-ary relation \(S\in\mathcal S\) について、

\[
S(u_1,\ldots,u_k)
\quad\Longleftrightarrow\quad
S(\pi(u_1),\ldots,\pi(u_k))
\]

が成立する。

\(\mathcal S\) の選択自体も独立に motivate されなければならない。confirmatory use では counterfactual comparison より前に固定し、adaptive に \(\mathcal S\) を学習するなら learning / selection rule を audited inference に含める。そうでなければ、望ましくない transformation を non-preserving にするためだけに、desired conclusion を encode する relation を後から追加できてしまう。

declared structure が豊かすぎて \(\operatorname{Aut}(U,\mathcal S)\) が trivial になる場合、invariance check は形式的には満たされても diagnostic leverage をほとんど持たないことがある。したがって independent-warrant requirement は、含めた relation だけでなく \(\mathcal S\) 自体の granularity にも適用される。

inference が equality class だけを利用するなら、任意の bijection は harmless renaming である。しかし sequence geometry、edit distance、neighborhood structure、order その他の relation を利用するなら、arbitrary bijection は無害とは限らない。error-aware UMI analysis で sequence distance を破壊しながら string を arbitrary number に写す変換は、evidential structure の pure re-encoding ではない。

したがって適切な invariance question は、inference が利用すると宣言した representation-level structure の automorphism に対して結論が保存されるか、である。より明示的には、\(X\) を inference が用いる完全な representation-level input、\(D(X)\) を target-level conclusion とする。declared representation structure の re-encoding のみを行う任意の \(\pi\in\operatorname{Aut}(U,\mathcal S)\) に対して、

\[
D(\pi\cdot X)=D(X)
\]

を要求する。output 自体にも transformed label が含まれる場合は対応する equivariance condition とする。宣言された evidential structure をすべて保存する変換で結論が変わるなら、説明されていない representation dependence がある。これは inference rule の audit criterion であり、assignment-changing perturbation まで harmless だという追加主張ではない。

### 4.2 Assignment perturbation

別の操作として、independently specified target state を固定したまま representation 間で value を再割当てすることがある。これは同じ assignment の structure-preserving re-encoding ではなく、どの read が tag を共有するか、どの record が group を共有するか自体を変えうる。

この操作への sensitivity は、それだけで誤りではない。むしろ **assignment 自体が evidentially active** であり、そのために正当化が必要であることを示す。

software-generated read ID について、追加の target link なしに arbitrary ID assignment から source-molecule plurality を推論することは正当化されない。

これに対して UMI の recorded assignment は、physical tagging event に関する情報を保存することを意図している。observed tag を read 間でランダムに再割当てすれば、その event に関する evidence を破壊する。したがって正しい結論は「UMI-based inference は arbitrary reassignment に不変であるべきだ」ではない。正当な sensitivity があるなら、それは experimental provenance と error model によって説明されなければならない。

audit は次の二問にまとめられる。

1. inference は、evidentially relevant と宣言した relation のすべての **structure-preserving re-encoding** に invariant か。
2. **assignment-changing perturbation** に sensitive なら、どの independently grounded scientific relation がその assignment を target-relevant にしているのか。

これにより、evidence-destroying reassignment を harmless renaming と扱う誤りと、equality より多くの structure を利用しているのに arbitrary bijection を harmless と扱う誤りの両方を避けられる。

## 5. Machine-Checked Dependency Analysis

Lean formalization は意図的に小さい。その役割は、記述された dependency structure を machine-checkable にすることである。

formal model には三つの representation、representation-to-target map、target-sensitive test、coarse / fine test regime、representation-sensitive negative control、semantically inert token metadata が含まれる。

feature-level analysis には generic three-way theorem が追加される。任意の representation type、target type、feature-value type について、fiber invariance と proposed target assignment に相対した feature-difference inference の universal soundness が同値であり、さらに両者がその map が誘導する quotient を介した descent と同値であることを formalization は証明する。従来の factorization result は、この anti-smuggling principle の target-specific instance として読める。同じ target に割り当てられた representation は target-factorized feature について同じ値を取り、representation-sensitive discriminator はこの条件に失敗する。

test layer も同じ構造に接続される。formal observation-factorization condition は、representation-level observed outcome が各 test について割り当てられた target の target-level response と一致することを表す。対応する target-linked observation function はこの条件を満たし、その factorization を満たす observed test outcome 上の差は異なる target assignment を含意する。さらに family-level object は selected regime で accessible なすべての test にこの factorization を要求し、その admissible family 内の一つの test が二つの representation を分離すれば、異なる target assignment が導かれる。これは \(\operatorname{Adm}_r(A)\land a\mathrel{\#_A}b\Rightarrow r(a)\neq r(b)\) の有限 counterpart である。

残りの result は negative control と monotonicity check である。同じ target に割り当てられた re-encoding は target-linked observation profile を保存する。より豊かな selected test family は、restricted family では unresolved だった pair を分離しうる。target-sensitive semantics に入っていない token の arbitrary reassignment は classification を変えない。

これらの proof は初等的である。machine-checking の主張もそれに応じて限定される。reviewer は、target-relevant とされる discriminator が hidden encoding choice、label、metadata field からではなく、宣言された target map と factorization を通して本当に入っているかを監査できる。

submission には anonymized supplementary Lean archive を添付する。これは paper-level result に対応する exact standalone source、pinned Lean toolchain、build configuration、build instructions、R1–R23 の one-to-one result map を含む。pinned Lean distribution 以外の external package dependency はなく、`lake build` で検証できる。review artifact から repository identity と non-blind provenance は除外し、review 後に non-anonymous archival reference へ置換できる。

## 6. 既存研究との関係

### 6.1 Nguyen と target-directed representation

最も近い概念的比較対象は Nguyen (2017) である。Nguyen は scientific representation と theoretical equivalence を論じる際、model が target system についてどのような inference を可能にするか、また model が同じ target について同じ claim を license するかに注意を向けるべきだと論じる。

本稿は、この target-directed perspective に異議を唱えるのではなく、それを受け入れる。ただし analysis の単位が異なる。

Nguyen の比較は、model、その representational use、target system について license される claim の水準で自然に理解できる。本稿の問題は、**individuation inference の内部**で、representing apparatus の特定の差が premise として使われるときに生じる。二つの representation が同じ target について reasoning するために使われていたとしても、その内部のすべての formal difference が target についての evidence になるわけではない。

同じ scholarly work を記述することが分かっている二つの bibliographic record が、それぞれ異なる service-local identifier を持つとする。その identifier inequality は representational vehicle の実在する差である。target-directed account は、両 record が同じ work について claim を行うために使われることを問題なく認められる。本稿の局所的な問いは別である。その identifier inequality 自体を、「二つの scholarly work がある」という claim の evidence として使ってよいのか。target-factorization test の答えは、その差が work-level difference を追跡する理由を与える scientifically / semantically justified target property がない限り、否である。

同じ区別は UMI workflow にも現れる。software read ID と observed UMI field は、どちらも source molecule について claim を行う representation の内部にある。しかし両者が target-directed representational practice に属しているという事実だけでは、各 feature difference が molecular counting に evidentially relevant かどうかは決まらない。feature generation から target property への、より局所的な dependency account が必要である。

したがって本稿の貢献は、scientific representation の rival theory でも theoretical equivalence の新しい criterion でもない。既に target-directed な practice の内部にある特定の inferential move に対する **feature-level dependency audit** である。

逆方向の限界も重要である。target factorization は representational adequacy の十分条件ではない。formally factorized feature であっても、bad target model、mistaken reference assignment、unreliable measurement process から生じうる。本枠組みはこれらの広い問題を決着させない。

### 6.2 DEKI と Contemporary Inferential Accounts

特に近い現代的比較対象は、Frigg and Nguyen (2020) が展開し Nguyen and Frigg (2022) が整理した DEKI account である。DEKI は scientific representation を denotation、exemplification、keying-up、imputation の組合せとして分析し、representational vehicle が exemplify する feature を key を介して target に impute される feature へ接続する。この構図は、本稿の基本的直観と整合する。すなわち、representing vehicle に存在する feature が自動的に target property になるわけではない。

本稿の audit は scientific representation の alternative general theory ではなく、DEKI が説明する「model がいかに represent するか」を置き換えるものでもない。問いはより狭く downstream である。proposed representation-to-target assignment と independently warranted な interpretive / scientific bridge を条件として、representation 内の *particular difference* を target plurality の discriminator として使ってよいかを問う。quotient descent は proposed assignment に対する conservativity を検査し、negative control は within-fiber leakage を露出し、selected-family admissibility は post-hoc witness selection を制約し、counterfactual audit は representational encoding への依存を検査する。DEKI の語彙で言えば、exemplified / keyed feature が存在することだけでは、その inequality が sound individuation discriminator かどうかは決まらない。

Suárez (2024) は representational force と inferential capacity を normative modeling practice 内の relational / context-dependent property として扱う contemporary inferential account を展開する。この立場は、本稿の structural factorization と scientific warrant の分離を補強する。本 formalism は、target assignment、key、measurement model、test を scientifically acceptable にする normative / empirical warrant 自体を導出しない。そうした commitment を **条件として**何が従うかを audit する。したがって貢献は complementary であり、already interpreted and warranted な representational practice 内の individuation inference に対する local conservativity test である。

### 6.3 Inferential representation と experimental individuation

Suárez (2004) と Contessa (2007) は、scientific representation における directionality、interpretation、surrogate inference を既に重視している。本稿は representation と target を結びつけること自体を新規性として主張しない。より狭く、**representational vehicle 内部の差**を individuation evidence として使う前に、何が明示されなければならないかを切り出す。

individuation の practice-oriented work も本稿の主張を制約する。Bueno, Chen, and Fagan (2018)、Waters (2018)、Love (2018) は、counting、tracking、manipulation、individuality が scientific purpose と practice に依存することを強調する。Chen (2018) は experimental individuation の ontological mode と epistemological mode を区別し、presentation を明示的に扱う。

したがって本稿は、presentation と individuation の区別自体が新しいとは主張しない。貢献は、そのような practice の内部で繰り返し起こりうる failure mode、すなわち presentation-level distinction が dependency を明示しないまま target-level individuating work をしてしまうことを監査する compact formal audit にある。

### 6.4 Technical neighbors

programming-language semantics における representation independence は implementation detail への依存を制約する (Mitchell 1986)。observational / behavioral equivalence は specified interaction に相対して system を分類する (Hennessy and Milner 1985; Rutten 2000)。identity and discernibility の研究は formal discernibility を unrestricted numerical identity と同一視することに警告する (Ladyman, Linnebo, and Pettigrew 2012; Dieks and Versteegh 2008)。

invariance 自体を新規な philosophical criterion として主張するわけではない。Liu (2015) は、epistemic representation が relevant representational convention に対して invariant であるべきだと明示的に論じている。本稿の quotient theorem も新しい数学や scientific representation 一般の新理論として提示するものではない。その役割は、proposed target assignment に相対した individuation inference において、same-target presentation を同一視した後にどの representation-level feature が残るかを特徴づけることにある。

特徴的なのはその methodological use、すなわち target-induced quotient descent、structurally admissible test family、independent scientific warrant、counterfactual assignment analysis を一つの auditable individuation protocol に統合する点にある。

また、individuation を支えない representational distinction が不要だということにもならない。surplus structure は別の representational task に有用または必要でありうる (Nguyen, Teh, and Wells 2020)。

## 7. Outlook: Evidence Synthesis と Construct-Level Comparison

### 7.1 Report、study、evidence unit

evidence synthesis は、同じ区別が重要になる第三の scale を与える。systematic review や meta-analysis では、bibliographic report がそのまま independent study や independent evidence unit であるとは限らない。一つの study から複数の report が生じることがあり、一つの report が複数の outcome、time point、subgroup analysis、effect estimate を含むこともある。見かけ上は異なる report が同じ underlying study に由来することもある。この report-to-study case は present functional model に直接収まり、複数の report が一つの study に map しうる。これに対して partially overlapping cohort は一般には単純な one-representation-to-one-target partition として表せず、present \(r:P\to T\) core の外側にある overlap、covariance、その他の dependence model を必要とする。representation multiplicity を independent evidence multiplicity と取り違えて duplicate inclusion を行えば、synthesis を歪めうる (Tramèr et al. 1997; von Elm et al. 2004)。

ここで必要な含意は限定的である。

\[
\text{report count}
\not\Rightarrow
\text{study count},
\qquad
\text{effect-estimate count}
\not\Rightarrow
\text{independent-evidence count}.
\]

これは両者が常に異なるという主張ではない。一つの level の multiplicity から別の level の multiplicity を自動的に推論することを否定しているだけである。

individuation の target は、synthesis question に応じて publication、study、cohort、comparison、outcome、independent evidence contribution のいずれにもなりうる。本枠組みは特定の meta-analytic model を規定しない。relevant relation が functional assignment で適切に表せる場合、たとえば report から underlying study への対応では、その assignment を宣言し、独立した methodological warrant を与えることを要求する。partial cohort overlap のようなより複雑な dependence structure は、present functional core に無理に押し込まず明示的に model すべきである。

### 7.2 Evidence unit から theoretical construct へ

bibliographic record、molecular measurement、evidence synthesis という流れは、さらに広い methodological question を動機づける。ただし、ここから先は prospective extension であり、present formal model が確立した結果ではない。別の corpus study では、paper を claim に分解し、claim を measured capacity に関する evidence として比較するときにも、同じ anti-smuggling discipline が適用できるかを検討できる。

\(\sigma(c)\) は、ここでは *operational structural signature* の shorthand としてのみ用いる。すなわち construct label を抑制し、関連 claim を normalize した後に残る measurement role、test、criterion、temporal relation、resource condition、その他の dependency である。この signature は unique とも complete とも仮定しない。また、その component は construct label や source identity / provenance を復元する前に、declared measurement question によって固定されなければならない。

この scale では、bibliographic identity、study/evidence identity、claim identity、capacity identity はそれぞれ異なる individuation relation であり、一つに潰してはならない。一つの paper が複数の operational claim を含むこともあり、複数の paper が materially the same operational structure に normalize される claim を表すこともありうる。したがって、

\[
\text{paper count}
\not\Rightarrow
\text{claim count},
\qquad
\text{claim-label count}
\not\Rightarrow
\text{capacity count}.
\]

ここでも矢印が否定しているのは automatic inference であり、すべての case で equality や inequality を主張しているわけではない。

このような procedure のもとでは、異なる construct name だけでは異なる measured capacity の evidence にならない。surviving signature difference は candidate discriminating structure であって、ontological または psychological independence の sufficient evidence ではない。逆に matching signature も synonymy や explanatory interchangeability を意味しない。

> **Nominal plurality is not evidential plurality. 区別されたものの名前ではなく、その区別を warrant する discriminating structure を保存せよ。**

この proposal の検証には、別の corpus、normalization protocol、common measurement basis、empirical analysis が必要である。本稿が提供するのは、そのような比較が満たすべき evidential discipline だけである。

## 8. 射程と限界

本枠組みはいくつかの問題を意図的に未解決のまま残す。

第一に、\(T\) と \(r\) は input である。本理論は target ontology を導出せず、不確実な source assignment を解決しない。

第二に、exact target factorization は structural idealization である。現実の measurement は noisy、probabilistic、model-dependent である。UMI の例では latent assigned tag と observed tag string を分離することで、この限界を明示している。したがって本稿でいう *necessary condition* は、宣言された exact deterministic model の内部での必要条件を意味する。すべての noisy / probabilistic individuation procedure が literal equality \(f(p)=\phi(r(p))\) を満たさなければならない、という主張ではない。

第三に、structural factorization は epistemic warrant ではない。不適切に選ばれた \(r\) によって、irrelevant feature まで target-factorized に見せることができる。target assignment、measurement model、test relevance の scientific justification は Lean development の外部に残る。

第四に、formal core は function \(r:P\to T\) を用いる。many-to-many、distributed、probabilistic representation-target relation は扱わない。

第五に、observation と intervention を同一視しない。異なる test class は異なる operational partition を誘導しうる。

最後に、operational separation は metaphysical numerical identity ではなく、synchronic discrimination だけでは diachronic persistence は確立されない。

## 9. Formal Audit Summary

blind review copy では machine-checked claim を neutral label にまとめる。以下の grouped map は、各 family が何を検査し、どの declared dependency を使うかを示す。

| Results | Informal claim family | Declared dependency |
| --- | --- | --- |
| R1--R4 | representation-only difference と同一 target assignment が両立しうること、same-target representation では target-linked observation が保存されること。 | fixed representation-to-target map と exact target-response semantics。 |
| R5--R7 | richer selected test family が restricted family で未分離の operational partition を refine できること。 | fixed exact test semantics と test-family inclusion。 |
| R8--R10 | positive control で target-linked outcome difference が target-assignment difference を支えうること。 | declared test の deterministic target response。 |
| R11--R15 | semantically inert identity-like token や decorative access metadata が tested classification を変えないこと。 | それらの field が declared target-sensitive semantics に含まれないこと。 |
| R16--R19 | generic feature factorization が target map の各 fiber 内で equality を保存し、representation-sensitive negative control が factorization に失敗すること。 | proposed representation-to-target map と explicit feature factorization。 |
| R20--R22 | test-specific factorization が witnessed target separation を license し、all-test family admissibility は追加の witness selection なしの existential family-level separation に対する sufficient condition であること。 | relevant test、または family-wide rule の下では selected test 全体について observed outcome と target response が exact に一致すること。 |
| R23 | fiber invariance が、arbitrary representation-to-target map が誘導する quotient を介した descent と同値であること。 | target-induced equivalence relation のみ。domain-specific な representation / target type を仮定しない。 |

小さな theorem が多数あること自体は novelty claim ではない。この collection は dependency structure の machine-checkable な記録である。neutral result label の完全な集合は R1--R23 である。

## 10. 結論

formal difference が individuation inference に入るためには、representation から target への justified path が必要である。

exact deterministic core は簡潔に述べられる。**declared functional representation-to-target model の内部で、declared scope 全体にわたり universally sound な difference discriminator として用いる representation-level feature は fiber-invariant でなければならず、したがって proposed target assignment が誘導する quotient を介して descend しなければならない。** within-fiber distinction は construction により捨てられる。selected test が separation を支持できるのは、その observation-to-target link が structurally admissible な場合に限られる。そして、どちらの condition も model を受け入れるための scientific warrant を作り出しはしない。より一般的な methodological lesson はこれより弱く、formal distinction を target-level distinction の支持に使うには、declared target への independently warranted route が必要だということである。

したがって individuation-inference audit は、target assignment や metaphysical individual を発見する procedure ではない。それは、explicitly declared target model と test regime に相対して、structural failure、scientific underdetermination、scoped pass を区別する reusable dependency check である。

三つの事例は異なる役割を持つ。bibliographic record は、record identity と work identity が同じではないという問題を直感的に示す。molecular counting は、同じ dependency problem が experimental measurement にも残ることを示し、read identity、tag identity、source-molecule identity を分離する必要を明らかにする。evidence synthesis は、この audit を広く適用可能な methodological setting へ戻し、report、study、estimate、independent evidence unit が一致しない場合を扱う。最後に construct-level outlook が、同じ discipline を paper から claim、さらに measured capacity へ prospective に延長する。

これらすべての case で、identifierhood、labelhood、multiplicity それ自体には evidential force はない。重要なのは、relevant difference が target quotient を survive し、target-level claim への independently warranted route を持つかどうかである。

> **individuation claim が formal difference に依存するなら、その difference が target quotient を survive することを要求し、observation-to-target bridge とその independent warrant を明示し、結論を declared test regime の内部に保て。**

## 参考文献

Aleshin-Guendel, Serge, and Rebecca C. Steorts. 2024. “Convergence Diagnostics for Entity Resolution.” *Annual Review of Statistics and Its Application* 11: 419–435. DOI: 10.1146/annurev-statistics-040522-114848.

Liu, Chuang. 2015. “Invariance and Scientific Representation.” *Frontiers of Philosophy in China* 10(4): 647–667. DOI: 10.3868/s030-004-015-0051-5.

Bueno, Otávio, Ruey-Lin Chen, and Melinda B. Fagan, eds. 2018. *Individuation, Process, and Scientific Practices*. Oxford University Press. DOI: 10.1093/oso/9780190636814.001.0001.

Chen, Ruey-Lin. 2018. "Experimental Individuation: Creation and Presentation." In *Individuation, Process, and Scientific Practices*, 192–213. Oxford University Press. DOI: 10.1093/oso/9780190636814.003.0009.

Contessa, Gabriele. 2007. "Scientific Representation, Interpretation, and Surrogative Reasoning." *Philosophy of Science* 74(1): 48–68. DOI: 10.1086/519478.

Dieks, Dennis, and Marijn A. M. Versteegh. 2008. "Identical Quantum Particles and Weak Discernibility." *Foundations of Physics* 38: 923–934. DOI: 10.1007/s10701-008-9243-z.

Hennessy, Matthew, and Robin Milner. 1985. "Algebraic Laws for Nondeterminism and Concurrency." *Journal of the ACM* 32(1): 137–161. DOI: 10.1145/2455.2460.

Kivioja, Teemu, Anna Vähärautio, Kasper Karlsson, Martin Bonke, Martin Enge, Sten Linnarsson, and Jussi Taipale. 2012. "Counting Absolute Numbers of Molecules Using Unique Molecular Identifiers." *Nature Methods* 9(1): 72–74. DOI: 10.1038/nmeth.1778.

Ladyman, James, Øystein Linnebo, and Richard Pettigrew. 2012. "Identity and Discernibility in Philosophy and Logic." *The Review of Symbolic Logic* 5(1): 162–186. DOI: 10.1017/S1755020311000281.

Love, Alan C. 2018. "Individuation, Individuality, and Experimental Practice in Developmental Biology." In *Individuation, Process, and Scientific Practices*, 165–191. Oxford University Press. DOI: 10.1093/oso/9780190636814.003.0008.

Mitchell, John C. 1986. "Representation Independence and Data Abstraction." In *Proceedings of the 13th ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages*, 263–276. Association for Computing Machinery. DOI: 10.1145/512644.512669.

Nguyen, James. 2017. "Scientific Representation and Theoretical Equivalence." *Philosophy of Science* 84(5): 982–995. DOI: 10.1086/694003.

Nguyen, James, Nicholas J. Teh, and Laura Wells. 2020. "Why Surplus Structure Is Not Superfluous." *The British Journal for the Philosophy of Science* 71(2): 665–695. DOI: 10.1093/bjps/axy026.

Rutten, Jan J. M. M. 2000. "Universal Coalgebra: A Theory of Systems." *Theoretical Computer Science* 249(1): 3–80. DOI: 10.1016/S0304-3975(00)00056-6.

Smith, Tom, Andreas Heger, and Ian Sudbery. 2017. "UMI-tools: Modeling Sequencing Errors in Unique Molecular Identifiers to Improve Quantification Accuracy." *Genome Research* 27(3): 491–499. DOI: 10.1101/gr.209601.116.

Suárez, Mauricio. 2004. "An Inferential Conception of Scientific Representation." *Philosophy of Science* 71(5): 767–779. DOI: 10.1086/421415.

Waters, C. Kenneth. 2018. "Ask Not 'What Is an Individual?'" In *Individuation, Process, and Scientific Practices*, 91–113. Oxford University Press. DOI: 10.1093/oso/9780190636814.003.0005.

Tramèr, Martin R., D. John M. Reynolds, R. Andrew Moore, and Henry J. McQuay. 1997. "Impact of Covert Duplicate Publication on Meta-analysis: A Case Study." *BMJ* 315(7109): 635–640. DOI: 10.1136/bmj.315.7109.635.

von Elm, Erik, Greta Poglia, Bernhard Walder, and Martin R. Tramèr. 2004. "Different Patterns of Duplicate Publication: An Analysis of Articles Used in Systematic Reviews." *JAMA* 291(8): 974–980. DOI: 10.1001/jama.291.8.974.

Frigg, Roman, and James Nguyen. 2020. *Modelling Nature: An Opinionated Introduction to Scientific Representation*. Cham: Springer. DOI: 10.1007/978-3-030-45153-0.

Nguyen, James, and Roman Frigg. 2022. *Scientific Representation*. Elements in the Philosophy of Science. Cambridge: Cambridge University Press. DOI: 10.1017/9781009003575.

Suárez, Mauricio. 2024. *Inference and Representation: A Study in Modeling Science*. Chicago: University of Chicago Press. DOI: 10.7208/chicago/9780226830032.001.0001.

