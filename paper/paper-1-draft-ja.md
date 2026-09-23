# 作業稿 — Paper 1 日本語訳

> **位置づけ:** 英語原稿の読解・監査用日本語訳。投稿用の正本は英語版。
> **射程:** operational individuation inference に対する、必要な構造条件と evidential-dependency 条件。
> **形式的境界:** target domain と representation-to-target assignment はモデル入力である。structural factorization 自体は scientific warrant を与えない。

# 形式的な差は、いつ個体化推論に入ることができるのか？
## Target Factorization、Restricted Tests、そして Unique Molecular Identifier (UMI) の事例

## 要旨

表現間の形式的な差は、それだけでは target-level individuation を正当化しない。本稿は、structural target-factorization condition と、それを受け入れるために必要な scientific warrant を分離し、test-specific factorization を通じて representation-level observation と target-level test outcome を接続する。unique molecular identifier (UMI) の事例では、software read ID、latent molecular tag、noisy observed tag を区別する。また、本稿で counterfactual relevance audit と呼ぶ分析において、無害な全単射的 renaming と assignment-changing perturbation を区別する。Lean による小規模な machine-checked formalization により、構造依存関係と test-relative refinement を検査する。本枠組みが与えるのは individuation inference の必要条件であり、証拠一般や numerical identity の完全な理論ではない。

## 1. はじめに

形式的表現には、それが支える target-level claim よりも多くの区別が含まれることがある。二つの変数は異なる名前を持ち、二つの record は異なる database identifier を持ち、二つの sequencing read は異なる file-level identifier を持ち、二つの constructor は形式的に不等でありうる。しかし、その差が二つの異なる target-level individual を追跡しているとは限らない。

問題は、そのような representation-level structure が無用だということではない。それは computation、bookkeeping、locality、provenance、model construction に不可欠な場合がある。問題は、その構造上の差が individuation inference の前提として使われるときに生じる。

本稿が問うのは、意図的に狭い次の問いである。

> **表現内部の形式的な差は、いつ、表現対象を operationally distinct と扱う推論に入ることができるのか？**

ここでの答えには、混同すべきでない二つの層がある。

第一は **structural condition** である。representation-level feature は、宣言された target assignment を介して factorize しなければならない。あるいは representation-level observation が、宣言された test の下で target-level response と一致しなければならない。そのような factorization がなければ、形式的な差は表現上の差にとどまる。

第二は **scientific-warrant condition** である。factorization を式として書いたことは、それが真であり、信頼でき、証拠として十分であることを意味しない。experiment、causal process、measurement、calibration、semantic practice が、その factorization を target relation の妥当なモデルとして扱うことを独立に正当化しなければならない。

formal artifact が扱うのは第一層だけである。構造依存関係を監査可能にするが、第二層を作り出すものではない。

この分離から、本稿で **counterfactual relevance audit** と呼ぶ実用的な分析が得られる。identifier-like feature について、まずどの種類の変更を考えているのかを問う。label を一貫して全単射的に rename しただけなら、label が符号化している構造だけに依存する推論は変わるべきではない。一方、representation 間で label assignment を入れ替える操作は、その assignment 自体が科学的に ground された関係を記録しているなら、証拠を変化させうる。assignment perturbation によって結論が変わるなら、その assignment が単なる representational detail ではなく target-relevant である理由を説明しなければならない。

本稿では unique molecular identifier (UMI) を用いてこの点を示す。software read identifier と molecular tag は、どちらも string として表現できる。しかし evidential role は異なる。一方は bookkeeping metadata であり、他方は downstream read と pre-amplification template molecule を結ぶ実験的生成過程に参加しうる。UMI の事例は exact formal model の限界も示す。observed UMI string には error が入りうるため、experimentally assigned tag と observed read-level tag を区別しなければならない。

### 1.1 貢献

本稿の貢献は四つに限定される。

1. **Structural target factorization.** representation-level feature が target を形式的に追跡していると言えるのは、その feature が宣言された representation-to-target map を介して factorize するときだけである。これは structural admissibility condition であり、epistemic warrant ではない。

2. **Test-specific observation factorization.** representation-level observation と target-level response を一つの inference chain に置く。observed outcome の差が target-level separation を支えられるのは、その observation が当該 test の target response に構造的に結びついているときだけである。

3. **Counterfactual relevance audit.** pure renaming と evidence-changing reassignment を区別し、identifier assignment が隠れた individuating work をしている場合を診断する。

4. **Scientific case を伴う machine-checked dependency analysis.** 小規模な Lean formalization により structural claim を検査し、UMI の事例により latent target-linked tag、noisy observed tag、representation-only identifier が実践上どう異なるかを示す。

## 2. 形式的設定

### 2.1 Representation と target

\(P\) を representation の集合、\(T\) を target domain とする。

\[
r:P\to T
\]

を representation-to-target assignment とする。\(P\) の異なる要素が \(T\) の異なる要素を表すとは仮定しない。

assignment \(r\) は modeling input である。本稿は raw observation から \(r\) を推定せず、\(T\) の ontology も導出しない。source assignment 自体が不確実な応用では、本枠組みは提案された assignment model を監査するのであって、source-assignment problem を解くものではない。

exact formal core は、一つの representation に一つの target value を割り当てる場合に限定する。many-to-many、distributed、probabilistic correspondence は自然な拡張だが、本稿の主張の外に置く。

### 2.2 Structural target factorization

representation-level feature を

\[
f:P\to V
\]

target-level property を

\[
\phi:T\to V
\]

とする。本稿では、次を **target-factorization condition** と呼ぶ。

\[
F_r(f,\phi)
\quad\Longleftrightarrow\quad
\forall p\in P,\; f(p)=\phi(r(p))
\]

と定義する。

\(F_r(f,\phi)\) が成立するなら、

\[
f(a)\neq f(b)
\quad\Longrightarrow\quad
r(a)\neq r(b)
\]

である。

証明は初等的である。target assignment が等しければ、target を介して factorize するすべての feature は同じ値を取る。したがって、この条件の価値は数学的な深さではなく、dependency を露出させる点にある。

重要なのは、\(F_r(f,\phi)\) 自体は **evidential warrant ではない**ということである。これは \(f\) が \(r\) の下で target property を追跡するために、構造的に何が真でなければならないかを述べるだけである。科学的応用がそのモデルを受け入れてよいかどうかは、formal identity の外部にある evidence に依存する。

この区別は trivialization も防ぐ。\(r\) を representation-level difference をすべて encode するほど細かく選べば、多くの feature を \(r\) を介して factorize させることができる。しかし、それはその \(r\) が科学的に適切だという証拠にはならない。target assignment とその正当化は substantive input のままである。

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

\(A\subseteq Q\) を、ある analysis のために選択された test family とする。exact framework では、選択には target claim との relevance と、representation-level observation と target-level response の間の独立に正当化可能な structural link の両方が必要である。

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

と定義する。

\(A_c\subseteq A_f\) なら、\(A_f\) の下での indistinguishability は \(A_c\) の下での indistinguishability を含意する。逆は一般には成立しない。

これは fixed exact semantics と set inclusion に関する定理である。noisy evidence が増えたとき classification が決して反転しない、という定理ではない。

## 3. 科学的事例: UMI による分子カウント

### 3.1 Representation multiplicity は molecule multiplicity ではない

high-throughput sequencing では、一つの template molecule から polymerase chain reaction (PCR) amplification により複数の downstream read record が生成されうる。したがって、

\[
100\ \text{read records}
\not\Rightarrow
100\ \text{source molecules}
\]

である。

各 read に一意な software identifier を付ければ100個の record をすべて区別できる。しかし、それだけでは100個の pre-amplification molecule を推論する独立の理由にはならない。

Kivioja et al. (2012) は amplification 前に molecule を label する unique molecular identifier を用い、absolute molecule counting を行う方法を導入した。Smith, Heger, and Sudbery (2017) は、得られた UMI string にも error-aware analysis が必要な理由を示した。UMI sequence 自体に sequencing error が入りうるため、token equality を素朴に扱うと PCR duplicate を誤って識別しうる。

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

### 3.3 最小の synthetic example

二つの tagged template を考える。

- \(m_1\) の latent assigned UMI は *ACGT* で、observed UMI が *ACGT*, *ACGT*, *ACGC* の三つの read を生成する。
- \(m_2\) の latent assigned UMI は *TGCA* で、observed UMI が *TGCA*, *TGCA*, *TGCA* の三つの read を生成する。

この synthetic example には六つの read record があるが、tagged template は二つしかない。*ACGC* は \(m_1\) の latent tag から生じた一つの sequencing error を表す。

異なる observed UMI string を異なる source molecule と同一視する naive rule は、\(m_1\) を二つの apparent group に分割し、三つの group を返しうる。error-aware procedure なら、*ACGC* を *ACGT* source と整合的な evidence として扱える。逆に UMI collision があれば、tag identity を十分条件として扱うことで、異なる template 由来の evidence を一つに併合してしまう可能性がある。

この例では三つの層が明確になる。

1. unique read ID は六つの record を individuate する。
2. latent assigned UMI は protocol によって tagged template に与えられた property である。
3. observed UMI string はその latent tag の noisy measurement である。

idealized model の exact target factorization を満たすのは第二層である。第三層には error model が必要である。第一層は、独立した target link が与えられない限り representation-level bookkeeping にすぎない。

### 3.4 本枠組みが診断するもの

本枠組みは「UMI difference は molecule difference である」とは言わない。より限定されたことを述べる。

read-level feature が molecular individuation inference に入るためには、その feature が target からどのように生成されたかを説明する justified model を経由しなければならない。UMI の場合、experimental tagging protocol、genomic または transcript context、error model が科学的な仕事を担う。string という型そのものには、その evidential force はない。

このため、この事例は哲学的にも有用である。二つの field がともに identifier であり、ともに string であり、ともに record を区別できたとしても、target を追跡するよう設計された causal and measurement history に参加するのはそのうち一方だけかもしれない。

## 4. Counterfactual Relevance Audit

“relabeling invariance” という表現は、重要に異なる二種類の perturbation を隠しうる。

### 4.1 Pure renaming

全単射 \(\pi:U\to U\) をすべての label value に一貫して適用するとする。*ACGT* を *17* に、*TGCA* を *42* に変え、すべての occurrence を整合的に置換する。

この変換は equality / inequality structure を保存する。label value による grouping だけに依存する推論は、この変更に対して invariant であるべきである。label の表記や encoding だけを変えたことで結論が変わるなら、その推論には説明を要する representation dependence がある。

### 4.2 Assignment perturbation

これとは別に、independently specified target state を固定したまま representation 間で label value を再割当てする操作がある。この操作は、どの read が同じ recorded tag を共有するか、どの record が同じ group に入るかを変えうる。

この操作への sensitivity は、それだけで誤りではない。むしろ **assignment 自体が evidentially active** であり、そのために正当化が必要であることを示す。

software-generated read ID について、追加の target link なしに arbitrary ID assignment から source-molecule plurality を推論することは正当化されない。

これに対して UMI の recorded assignment は、physical tagging event に関する情報を保存することを意図している。observed tag を read 間でランダムに再割当てすれば、その event に関する evidence を破壊する。したがって正しい結論は「UMI-based inference は arbitrary reassignment に不変であるべきだ」ではない。正当な sensitivity があるなら、それは experimental provenance と error model によって説明されなければならない、ということである。

audit は次の二問にまとめられる。

1. inference は **representation-preserving renaming** に invariant か。
2. **assignment-changing perturbation** に sensitive なら、どの scientific relation がその assignment を target-relevant にしているのか。

これにより、無害な renaming と evidence destruction を同じ counterfactual として扱うことを避けられる。

## 5. Machine-Checked Dependency Analysis

Lean formalization は意図的に小さい。その役割は、記述された dependency structure を machine-checkable にすることである。

formal model には三つの representation、representation-to-target map、target-sensitive test、coarse / fine test regime、representation-sensitive negative control、semantically inert token metadata が含まれる。

feature-level factorization は任意の value domain に対して定義される。representation-level feature は、指定された structural factorization を通じてのみ target-level property と対応づけられる。formalization は、同じ target に割り当てられた二つの representation が、factorized feature について同じ値を取ること、およびそのような feature の値が異なれば target assignment も異なることを検査する。また、同じ target に割り当てられた二つの representation を分離するような representation-sensitive test は target factorization を満たせない一方、target assignment から直接定義された positive-control feature は満たせることも検査する。

test layer も同じ構造に接続される。observation-factorization object は presentation-level observed outcome が各 probe について grounded referent の target-level response と一致することを表す。built-in grounded observation surface はこの条件を満たし、structurally factorized observed probe の差は grounding difference を含意する。

残りの result は negative control と monotonicity check である。same-reference re-encoding は grounded observation profile を保存する。より豊かな admitted test family は、restricted family では unresolved だった pair を分離しうる。target-sensitive semantics に入っていない token の arbitrary reassignment は classification を変えない。

これらの proof は初等的である。mechanization の主張もそれに応じて限定される。reviewer は、target-relevant とされる discriminator が hidden constructor、label、metadata field からではなく、宣言された target map と factorization を通して本当に入っているかを監査できる。

## 6. 既存研究との関係

### 6.1 Nguyen と target-directed representation

最も近い概念的比較対象は Nguyen (2017) である。Nguyen は scientific representation と theoretical equivalence を論じる際、model が target system についてどのような inference を可能にするか、また model が同じ target について同じ claim を license するかに注意を向けるべきだと論じる。

本稿は、この target-directed perspective に異議を唱えるのではなく、それを受け入れる。ただし analysis の単位が異なる。

Nguyen の比較は、model、その representational use、target system について license される claim の水準で自然に理解できる。本稿の問題は、**individuation inference の内部**で、representing apparatus の特定の差が premise として使われるときに生じる。二つの representation が同じ target について reasoning するために使われていたとしても、その内部のすべての formal difference が target についての evidence になるわけではない。

同じ一人の person に関する二つの database record が、それぞれ異なる row ID を持つとする。その row-ID inequality は representational vehicle の実在する差である。target-directed account は、両 record が同じ person について claim を行うために使われることを問題なく認められる。本稿の局所的な問いは別である。その row-ID inequality 自体を、「二人の person がいる」という claim の evidence として使ってよいのか。target-factorization test の答えは、その差が person difference を追跡する理由を与える scientifically / semantically justified target property がない限り、否である。

同じ区別は UMI workflow にも現れる。software read ID と observed UMI field は、どちらも source molecule について claim を行う representation の内部にある。しかし両者が target-directed representational practice に属しているという事実だけでは、各 feature difference が molecular counting に evidentially relevant かどうかは決まらない。feature generation から target property への、より局所的な dependency account が必要である。

したがって本稿の貢献は、scientific representation の rival theory でも theoretical equivalence の新しい criterion でもない。既に target-directed な practice の内部にある特定の inferential move に対する **feature-level dependency audit** である。

逆方向の限界も重要である。target factorization は representational adequacy の十分条件ではない。formally factorized feature であっても、bad target model、mistaken reference assignment、unreliable measurement process から生じうる。本枠組みはこれらの広い問題を決着させない。

### 6.2 Inferential representation と experimental individuation

Suárez (2004) と Contessa (2007) は、scientific representation における directionality、interpretation、surrogate inference を既に重視している。本稿は representation と target を結びつけること自体を新規性として主張しない。より狭く、**representational vehicle 内部の差**を individuation evidence として使う前に、何が明示されなければならないかを切り出す。

individuation の practice-oriented work も本稿の主張を制約する。Bueno, Chen, and Fagan (2018)、Waters (2018)、Love (2018) は、counting、tracking、manipulation、individuality が scientific purpose と practice に依存することを強調する。Chen (2018) は experimental individuation の ontological mode と epistemological mode を区別し、presentation を明示的に扱う。

したがって本稿は、presentation と individuation の区別自体が新しいとは主張しない。貢献は、そのような practice の内部で繰り返し起こりうる failure mode、すなわち presentation-level distinction が dependency を明示しないまま target-level individuating work をしてしまうことを監査する compact formal audit にある。

### 6.3 Technical neighbors

programming-language semantics における representation independence は implementation detail への依存を制約する (Mitchell 1986)。observational / behavioral equivalence は specified interaction に相対して system を分類する (Hennessy and Milner 1985; Rutten 2000)。identity and discernibility の研究は formal discernibility を unrestricted numerical identity と同一視することに警告する (Ladyman, Linnebo, and Pettigrew 2012; Dieks and Versteegh 2008)。

本稿の数学は、これらの成熟した framework よりはるかに控えめである。特徴的なのはその methodological use、すなわち target factorization、restricted test、counterfactual assignment analysis を組み合わせて individuation inference を監査する点にある。

また、individuation を支えない representational distinction が不要だということにもならない。surplus structure は別の representational task に有用または必要でありうる (Nguyen, Teh, and Wells 2020)。

## 7. より広い含意: Identifier から Theoretical Construct へ

UMI の事例から、より一般的な methodological consequence が得られる。identifier の evidential force は、それが identifier であることから生じるのではない。identifier assignment と target の間にある、独立に warrant された関係から生じる。

同じ規律は、object identification より一段高い methodological level、すなわち measured capacity を記述する theoretical construct にも適用できる。異なる construct label は、それ自体が representational vocabulary 上の差である。その nominal plurality は、それだけでは measured capacity の plurality を成立させない。

\(C\) を theoretical construct label の集合とし、\(\sigma(c)\) を、construct \(c\) に結びついた claim について label suppression と normalization を行った後に残る 本稿で operational structural signature と呼ぶ構造的シグネチャ とする。この signature には、claim を再構成するために必要な measurement role、test、criterion、temporal relation、resource condition、その他の dependency が含まれうる。

この signature は一意であるとも完全であるとも仮定しない。その構成要素は、construct label や source authority を復元する前に、宣言された measurement question によって固定されなければならない。そうしなければ、好ましい distinction を保存または消去するように比較手続きを事後的に調整できてしまう。

方法論的ポイントは非対称である。

\[
c_1\neq c_2
\quad\not\Rightarrow\quad
\text{distinct measured capacities}
\]

一方、

\[
\sigma(c_1)\neq\sigma(c_2)
\]

は、capacity distinction をさらに検討する根拠となりうる candidate discriminating structure を構成する。しかし、この第二の差も ontological / psychological independence の十分条件ではない。上述した target choice、measurement warrant、selected test の要件を引き続き満たさなければならない。

逆に、異なる名前を持つ二つの construct が common measurement basis の下で同じ normalized structural signature を与えるなら、名前の差そのものは capacity plurality の追加 evidence を与えない。これは historical construct が synonymous、explanatorily interchangeable、あるいは useless であるという意味ではない。意味するのは、その label がそれ自体では specified measurement framework 上の independent status を獲得していない、ということだけである。

得られる原則は次である。

> **Nominal plurality is not evidential plurality. 区別されたものの名前だけではなく、その区別を warrant する discriminating structure を保存せよ。**

この帰結は cognitive science その他の construct-rich field に対する別の research question を示唆する。analysis の間は authority と construct label を伏せ、operational claim を common measurement basis 上へ normalize し、残存する discriminating structure を比較することができる。本稿は、その procedure の下でどの named cognitive capacity が distinct のまま残るかを答えない。また、いかなる common basis の completeness も仮定しない。本稿が与えるのは、そのような比較に必要な evidential discipline である。

## 8. 射程と限界

本枠組みはいくつかの問題を意図的に未解決のまま残す。

第一に、\(T\) と \(r\) は input である。本理論は target ontology を導出せず、不確実な source assignment を解決しない。

第二に、exact target factorization は structural idealization である。現実の measurement は noisy、probabilistic、model-dependent である。UMI の例では latent assigned tag と observed tag string を分離することで、この限界を明示している。

第三に、structural factorization は epistemic warrant ではない。不適切に選ばれた \(r\) によって、irrelevant feature まで target-factorized に見せることができる。target assignment、measurement model、test relevance の scientific justification は Lean development の外部に残る。

第四に、formal core は function \(r:P\to T\) を用いる。many-to-many、distributed、probabilistic representation-target relation は扱わない。

第五に、observation と intervention を同一視しない。異なる test class は異なる operational partition を誘導しうる。

最後に、operational separation は metaphysical numerical identity ではなく、synchronic discrimination だけでは diachronic persistence は確立されない。

## 9. Formal Audit Summary

blind review copy では mechanized claim を neutral label にまとめる。R1--R15 は元の presentation/target、test-family、semantically inert-token control を扱う。R16--R19 は generic target factorization とその positive / negative control を扱う。R20 は grounded observation surface に対する test-specific observation factorization を確立し、R21 はその factorization の下で observed difference が grounding difference を含意することを検査する。

小さな theorem が多数あること自体は novelty claim ではない。この collection は dependency structure の machine-checkable な記録である。

## 10. 結論

形式的な差が individuation inference に入るためには、representation から target への justified path を経由しなければならない。

formal contribution は、しばしば一つに圧縮される二つの問いを分離する。**Structural target factorization** は、feature または observed test outcome が主張された仕方で target assignment に実際に依存しているかを問う。**Scientific warrant** は、その dependency model を application でなぜ信頼してよいのかを問う。前者は mechanically audit できるが、後者は宣言だけでは得られない。

UMI-based molecular counting はこの区別を示す。unique read ID は downstream record を区別する。latent molecular tag は pre-amplification protocol によって tagged template を追跡しうる。observed UMI string はその latent tag の noisy measurement であり、error model を必要とする。三者がすべて string として現れうるということは、その evidential role には関係しない。

したがって実践的な教訓は、identifier を無視せよということでも、target-linked に見える identifier をそれだけで信頼せよということでもない。より限定された次の原則である。

> **individuation claim が形式的な差に依存するなら、その target factorization と、それを受け入れる科学的理由を明示せよ。そのうえで、明示的に admit された observational / interventional regime に相対して claim を評価せよ。**

## 参考文献

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
