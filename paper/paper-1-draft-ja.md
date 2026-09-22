# Working Draft — Paper 1

> **Status:** Working manuscript draft. This file is not repository theory authority and does not modify the terminal classification of #119–#122.  
> **Scope:** Paper 1 only — evidential conditions for operational individuation under restricted observation.  
> **Primary provenance:** #119, with formal/synthesis support from #120–#122 and current \`main\`.  
> **Draft language:** Japanese.  
> **Drafting principle:** A difference in representation is not, by itself, evidence of a difference in what is represented.  
> **Formal boundary:** The target domain and the representation-to-target map are explicit model inputs. This paper does not derive the ontology of the target domain from observation.

# 制限された観測下における個体化主張の証拠条件
## 表現の複数性と対象関連の識別可能性

## 要旨

形式モデルの中に複数の表現が存在しても、それだけで複数の個体が存在するとは言えない。

異なる変数、符号化、識別子、あるいは台集合の要素は、表現として異なっていても、同じ対象を指している可能性がある。したがって、表現の複数性そのものを、対象レベルの複数性の証拠として使用してはならない。

本論文では、利用可能な観測または介入が明示的に制限されている場合に、二つの表現を操作的に区別する主張を、どのような証拠が正当化するのかを検討する。

形式モデルでは、表現、表現から対象への参照写像、対象に適用されるテスト、およびテスト結果を分離する。ここで参照写像と対象領域は独立に与えられるモデル入力であり、本論文はそれらを観測から導出しない。この制約の下で、表現上の差が対象の差を示す証拠として暗黙に流入しないことを機械的に検査する。

Lean による有限形式化は、次の事実を確認する。第一に、異なる二つの表現が同じ対象を指し、対象に依存するすべてのテストで同じ結果を返す場合がある。第二に、制限されたテスト集合では区別できない二つの表現が、対象に関係する追加テストを導入すると区別可能になる場合がある。第三に、固定された正確な意味論の下では、テスト集合の包含関係が観測的不識別性の細分化関係を与える。第四に、テスト結果に影響しないメタデータは、そのテスト集合が支持する区別にも影響しない。

これらの結果から得られるのは、個体性一般の理論ではなく、個体化主張に対する証拠上の制約である。

**操作的な区別を主張するには、表現そのものの違いではなく、表現された対象に関係し、かつ明示されたテスト条件の下で実際に両者を区別する証拠が必要である。**

検討した形式的範囲では、対象領域、参照写像、利用可能なテスト、およびその結果が固定されれば、その証拠が支持する操作的な区別を決めるために、表現に付与された追加の同一性ラベルを参照する必要はない。

ただし、本論文は対象領域そのものの個体性を観測から導出しない。操作的識別可能性を形而上学的な数的非同一性と同一視しない。有限性が個体性を生み出すとも主張しない。

本論文の中心的な目的は、より限定されている。

**表現上の差と、対象について証拠として利用可能な差を分離する。**

## 1. はじめに

二つの表現があるというだけで、二つの個体があると言えるだろうか。

形式モデルでは、二つのものを作ること自体は簡単である。二つの変数を書き、二つの識別子を割り当て、二つの構成子や台集合要素を導入できる。

しかし、これらの操作によって直接示されるのは、形式表現が複数存在するということだけである。

**複数の表現は、複数の個体を意味しない。**

同じ対象が異なる名前を持つことはある。同じ状態が異なる方法で符号化されることもある。異なる内部表現が、指定された観測の下では同じ振る舞いを示す場合もある。

したがって、表現の違いと、表現された対象に関係する違いを分けなければならない。

本論文が扱う問いは次のものである。

**明示された証拠条件の下で、どのような差を個体化の証拠として使用してよいのか。**

この問いは、「観測から個体を生成できるか」という問いとは異なる。本論文では、対象領域と、表現がどの対象を指すかを指定する参照写像をモデル入力として与える。

したがって、本論文は target-level identity を無から導出するものではない。

検討するのは、その対象領域について区別を主張するときに、表現上の差を証拠として密輸せず、どの情報を利用してよいかという推論上の問題である。

中心原則は一文で表せる。

**表現が異なるというだけで、表現されたものが異なると推論してはならない。**

この原則は、単なる言葉上の注意ではない。

たとえば、形式化の冒頭で $x$ と $y$ を別の carrier element として導入し、後になって $x \neq y$ を「二個体が存在する」ことの証拠として用いるなら、結論がモデルの記法や carrier structure に埋め込まれている可能性がある。

本論文では、そのような推論を避ける。

まず複数の表現を置く。

次に、表現が指す対象に関係するテスト結果を調べる。

差が認められたテスト条件の下で検出されるなら、操作的な区別が支持される。

差が検出されないなら、表現が複数あるという事実だけから対象の複数性を結論しない。

この論文の貢献は、新しい観測等価性を定義することではない。

**どの形式的差異を個体化主張の証拠として利用してよいかを制約する inference discipline を、明示的な参照写像と機械検証可能な negative control によって与えること**が目的である。

## 2. 形式設定

### 2.1 表現と対象

$P$ を表現の集合とする。

$P$ の要素は、名前、式、符号化、記録、識別子など、対象を形式的に取り扱うためのものとする。

$P$ の異なる要素が異なる個体に対応するとは仮定しない。

$T$ を対象領域とし、

$$
r : P \rightarrow T
$$

を、各表現がどの対象状態または参照先に対応するかを指定する写像とする。

ここで重要な制約を明示しておく。

**$T$ と $r$ は本論文で導出される結論ではなく、モデルに与えられる意味論的入力である。**

したがって、以下の形式化は「対象領域に差が存在する理由」や「参照関係そのものがどのように確立されるか」を解決しない。

それが扱うのは、$T$ と $r$ が与えられた後に、どの表現上の差を対象レベルの区別を支持する証拠として利用してよいかという問題である。

### 2.2 テストと結果

$Q$ をテストの集合とする。

テストは、適用先に応じて観測、測定、問い合わせ、あるいは介入として解釈できる。ただし、本論文は観測と介入を同一視しない。以下の結果は、あらかじめ宣言された一つの test class の内部で成立する。

対象 $t$ にテスト $q$ を適用した結果を

$$
O(q,t)
$$

と書く。

ある分析で利用可能とするテスト集合を

$$
A \subseteq Q
$$

とする。

### 2.3 テスト集合に相対的な不識別性

二つの表現 $a,b$ が $A$ の下で区別できないことを

$$
a \equiv_A b
$$

と書き、

$$
a \equiv_A b
\quad\Longleftrightarrow\quad
\forall q\in A,\;
O(q,r(a))=O(q,r(b))
$$

と定義する。

逆に、

$$
a \mathrel{\#_A} b
$$

を

$$
a \mathrel{\#_A} b
\quad\Longleftrightarrow\quad
\exists q\in A:
O(q,r(a))\neq O(q,r(b))
$$

とする。

ここでの $\equiv_A$ は、対象の形而上学的同一性を定義するものではない。

それは、指定されたテスト集合が支持する操作的分類である。

**形式的不等号は、表現が異なることの証拠であって、それだけでは対象が異なることの証拠ではない。**

## 3. 表現の違いは対象の違いを含意しない

二つの異なる表現 $a$ と $b$ を考える。

符号化そのものを調べる手続きなら、両者を簡単に区別できるかもしれない。

しかし、その結果が直接示すのは、二つの符号化が異なるということだけである。

参照先が異なることまでは示されない。

現在の有限形式モデルには、まさにそのような negative control が含まれている。

二つの presentation constructor は形式的には異なり、presentation-sensitive な probe によって区別できる。

しかし両者は

$$
r(a)=r(b)
$$

に相当する同じ grounding result を持ち、対象に依存するすべての probe に対して同じ結果を返す。

したがって、

$$
a\neq b
$$

から

$$
r(a)\neq r(b)
$$

を推論することはできない。

**検出可能な差があることと、対象に関係する差があることは同じではない。**

この点は、個体化主張にとって重要である。

モデル構築上の都合で割り当てた識別子を、そのまま対象の複数性を支持する独立証拠として使うことはできない。

そうすると、表現を作るための選択が、表現された対象についての結論へ変換されてしまう。

したがって、本論文が採用する推論順序は

$$
\text{複数の表現}
\rightarrow
\text{対象に関係するテスト結果}
\rightarrow
\text{そのテスト条件が支持する操作的区別}
$$

である。

$$
\text{複数の表現}
\rightarrow
\text{複数の個体}
$$

ではない。

## 4. 区別可能性はテスト集合に依存する

二つのテスト集合 $A_c$ と $A_f$ が

$$
A_c\subseteq A_f
$$

を満たすとする。

このとき、固定された同じ結果意味論の下で、

$$
a\equiv_{A_f}b
\Longrightarrow
a\equiv_{A_c}b
$$

が成立する。

より多くのテストを使っても区別できないなら、より少ないテストでも区別できない。

逆は成立しない。

現在の有限モデルには、

$$
a\equiv_{A_c}b
$$

でありながら、

$$
a\mathrel{\#_{A_f}}b
$$

となる具体例がある。

つまり、制限されたテスト集合では見えなかった差が、追加の対象関連テストによって見えることがある。

この結果は、次のように限定して述べるべきである。

**固定された正確なテスト意味論の下では、テスト集合の拡張は induced equivalence relation を細分化しうる。**

これは、「現実世界で証拠を増やせば既存の判断が必ず保持される」という一般命題ではない。

ノイズ、測定誤差、統計的更新、測定による攪乱などを含む設定は、本論文の有限 exact model の外にある。

有限性についても同様である。

**有限性が個体を作るのではない。**

現在の一般的な包含定理そのものは、有限性を必要としない。有限性は、具体的な countermodel と proof audit を完全に検査可能にするための fixture の性質である。

したがって、本論文の依存関係は

$$
\text{宣言されたテスト集合}
\rightarrow
\text{検出可能な対象関連差}
\rightarrow
\text{その条件下で支持される操作的区別}
$$

である。

## 5. 機械検証された結果とその意味

現在の Lean artifact は \`GroundedPresentationDistinguishability.lean\` である。

この形式化の数学的内容は意図的に小さい。目的は新しい深い数学定理を提示することではなく、議論が presentation identity を個体化前提として使用していないことを機械的に監査できるようにすることである。

### 5.1 同じ参照先は同じ対象依存観測を与える

Lean theorem

\`sameGrounding_sameGroundedObservation\`

は、二つの presentation が同じ grounding result を持つなら、任意の grounded probe に対して同じ outcome を持つことを示す。

対応する profile-level theorem

\`sameGrounding_sameGroundedProfile\`

は、参照先を保存する re-encoding が対象依存の観測 profile を変えないことを示す。

これらは数学的には単純な結果である。

その役割は、

**encoding difference と target-sensitive evidence を formal surface 上で分離すること**

にある。

### 5.2 表現差があっても対象関連差はない場合がある

\`encodingProbe_separates_sameGrounding\`

は、二つの encoding が presentation-sensitive probe では区別される一方、同じ grounding result を持つことを確認する。

さらに

\`sameReferent_encodings_groundedlyIndistinguishable\`

は、その二つが richer finite test regime においても、すべての grounded probe について区別されないことを示す。

この negative control が、論文の最重要な anti-smuggling test である。

**表現差を検出できても、その差が参照先を通らないなら、対象レベルの区別の証拠にはならない。**

### 5.3 制限されたテスト集合では見えない差がある

\`coarse_indistinguishable\`

は、ある pair が coarse regime では区別できないことを示す。

\`fine_distinguishable\`

は、追加の grounded probe を含む fine regime では同じ pair が区別されることを示す。

したがって、不識別性はテスト集合に相対的である。

ただし、ここから「fine regime が対象の絶対的 identity を発見した」とは結論しない。

### 5.4 outcome difference から target-state difference を導く

\`groundedOutcomeDifference_impliesGroundDifference\`

は、grounded response difference があれば、対応する grounding results が異なることを導く。

具体例 \`derivedGroundDifference\` では、ground inequality を個体化 premise として最初から使用せず、response difference から導出している。

ただし、この theorem は target carrier 自体を導出するものではない。

**target domain と response semantics にすでに存在する識別構造を、presentation identity に頼らず検出している。**

これは本論文の重要な境界である。

### 5.5 テスト集合の包含による細分化

\`groundedIndist_of_access_inclusion\`

は、利用可能な probe family の包含関係に対して

$$
\text{fine-indistinguishable}
\Longrightarrow
\text{coarse-indistinguishable}
$$

を示す。

この結果は observational resolution の monotonic refinement を表現する。

ただし、固定された exact semantics に対する定理であり、ノイズや belief revision 一般についての主張ではない。

### 5.6 無関係なメタデータはテスト能力を変えない

\`decorativeInterfaceTag_irrelevant\`

は、実際の access profile が同じままなら decorative tag を変更しても probe accessibility が変化しないことを示す。

これは任意の hidden identity variable の一般的な除去定理ではない。

現在の形式化が示すのは、**定義された observational semantics に寄与しない metadata が、この具体的分類に寄与しない**という限定的な結果である。

## 6. 何が証拠として許されるのか

本論文の中心問題は、単なる distinguishability ではなく、**evidential admissibility** である。

少なくとも二つの問いを分ける必要がある。

第一に、

**検出された差は、表現についての差なのか、それとも表現された対象についての差なのか。**

第二に、

**その差を検出する test class は、現在の主張に対する証拠として明示的に採用されているか。**

たとえば、同じ人物を表す二つのデータベース行が異なる row ID を持っているとする。

row ID は二つの record を区別する。

しかし、その差だけでは二人の人物が存在するとは言えない。

この例で必要なのは、

$$
\text{record difference}
\neq
\text{person difference}
$$

という区別である。

一般化すると、次の原則になる。

**個体化の証拠は、個体化しようとしている対象の差を追跡しなければならない。**

ここで「追跡する」という関係を、本論文では参照写像と target-sensitive test semantics によって明示する。

ただし、その参照写像そのものが正しい理由は別問題である。

本論文は reference assignment の epistemology 全体を解決しない。

## 7. 既存研究との関係と新規性の範囲

観測可能な振る舞いによって系を比較する考え方は新しくない。

観測等価性、双模倣、行動等価性、representation independence などは、指定された観測や相互作用に対して異なる表現や系を同一視できる条件を長く研究してきた。

したがって、本論文は次のいずれも新規性として主張しない。

- observational equivalence そのもの
- test-relative equivalence そのもの
- representation independence そのもの
- equivalence classes や quotient の構成
- discernibility と numerical identity の区別そのもの

本論文が扱う問いは、これらより狭い。

**形式モデルが individuation claim を行うとき、どの difference をその claim の証拠として使ってよいのか。**

この問題に対して、本論文は三つの制約を組み合わせる。

第一に、representation multiplicity を target multiplicity の証拠として使用しない。

第二に、admissible evidence は明示された reference map を通じて target-relevant outcome に factorize しなければならない。

第三に、この制約が実際の formal proof で破られていないことを、presentation-sensitive negative control と Lean proof audit によって確認する。

したがって、本論文の新規性候補は新しい equivalence relation ではなく、

**individuation claim に対する presentation-safe evidential discipline**

にある。

この位置づけが既存研究によって完全に包含されるなら、本論文の独立性は弱くなる。

したがって最終稿では、representation independence、observational/behavioral equivalence、scientific individuation、discernibility と numerical identity の既存研究との比較を明示しなければならない。

## 8. 限界と反論への回答

### 8.1 「identity を target domain に移しただけではないか」

この反論は正しい部分を持つ。

本論文は target domain $T$ の構造を観測から導出しない。

また、reference map $r$ もモデル入力である。

したがって、本論文は primitive identity 一般を除去したとは主張しない。

主張はより限定的である。

**一度 target semantics と reference assignment が与えられた後、presentation identity を追加の証拠として使わなくても、その test regime が支持する operational distinction を決定できる。**

### 8.2 「これは observational equivalence の言い換えではないか」

equivalence relation 自体には新規性を主張しない。

本論文が扱うのは、observational difference を individuation evidence として利用する際の資格条件である。

特に、presentation-only difference を admissible evidence から排除する factorization constraint を明示し、それを formal negative control として監査する。

### 8.3 「なぜ operational distinction を individuation と呼ぶのか」

本論文では、equivalence class を metaphysical individual と同一視しない。

より正確には、

**指定された証拠条件がどの individuation claim を支持するか**

を扱う。

したがって、「individuality has been derived」ではなく、「an operational distinction is licensed under the declared evidential regime」と記述する。

### 8.4 「有限性は本質ではないのではないか」

その通りである。

一般的な access-inclusion theorem は有限性を必要としない。

有限性は、現在の countermodel と proof surface を完全に検査できることに意味がある。

したがって、本論文は finitude を individuation の原因として扱わない。

### 8.5 「観測と介入を混同していないか」

混同しない。

test class は分析ごとに宣言される。

observation-only equivalence と intervention-sensitive equivalence は別の test regimes として扱うべきであり、一方から他方を自動的に推論しない。

## 9. 未解決の最小形式課題

現在の formalization には、論文の中心 claim をさらに強く検査する余地が一つ残る。

現状では、unused identity token はそもそも formal model に導入されていない。

したがって、

> identity token を使わずに分類できる

ことと、

> identity token を追加し、それだけを変更しても分類結果が不変である

ことは厳密には異なる。

この差を埋めるための最小追加形式化は、presentation に decorative identity token を追加し、target semantics と admitted tests を固定したまま token のみを変更しても $\equiv_A$ が不変であることを示すことである。

期待される discriminator は次の形になる。

$$
\text{identity token changes}
\quad\land\quad
\text{target-relevant evidence fixed}
\quad\Longrightarrow\quad
\text{operational classification fixed}.
$$

一方で、

$$
\text{target-relevant outcome changes}
$$

なら classification が変わりうる。

この追加結果が得られれば、「identity を単にモデルから省略しただけではないか」という反論に対して、より直接的な formal answer を与えられる。

現時点では、この stronger invariance claim を機械検証済み結果としては扱わない。

## 10. 結論

形式的な複数性は簡単に作ることができる。

二つの名前を書ける。

二つの識別子を作れる。

二つの carrier elements を定義できる。

しかし、それだけでは対象について二つの個体が存在することは示されない。

本論文の第一の結論は単純である。

**複数の表現は、複数の個体を意味しない。**

第二の結論は、positive requirement を与える。

**操作的な区別を主張するには、表現された対象に関係し、明示された証拠条件の下で実際に両者を区別する情報が必要である。**

現在の Lean formalization は、この原則を小さな有限モデルで監査する。

異なる encoding が同じ target に対応しうる。

presentation-sensitive difference が target-sensitive difference を含意しない場合がある。

restricted test family では見えない差が、richer test family では見える場合がある。

無関係な metadata は、定義された observational semantics を変えない。

ただし、本論文は target ontology を観測から導出しない。

形而上学的 identity 一般を解決しない。

finite access が individuality を生成するとも主張しない。

したがって、中心的な主張は次のように限定される。

**対象領域、参照関係、および証拠条件が明示されたとき、表現上の差を独立した個体化証拠として使用せずに、その証拠条件が支持する操作的な区別を決定できる。**

より一般的な方法論的原則は、さらに短く表せる。

**表現の差を、証拠なしに対象の差へ変換してはならない。**
