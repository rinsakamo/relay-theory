# P399 post-MAIN 再統合結果 v1

## 結論

exact frozen MAIN40 の 40 本の Grammar-v0 reconstruction を横断して再統合すると、8つの認知領域を8個の固定モジュールとして置く必要はない。

最小の共通像は次のとおり。

```
外部/課題
   │
   ▼
 P_in  ── write / evidence / reward / feedback
   │
   ▼
 X_t   ── current configuration
   │      └─ optional retained source-defined structure
   │         belief / memory / weights / values / maps / cache / recurrent state ...
   ▼
 K     ── typed transform / inference / update / retrieval / prediction / learning
   │
   ▼
 Q     ── source-defined criterion / orientation
   │
   ▼
 P_out ── action / choice / prediction / retrieval / probe
   │
   ▼
 rho/O ── boundary-relative trace

T orders the steps.
Pi and C define typed individuation and admissibility.
```

この substrate 上で、source-defined feedback、routing、planning、hierarchy、replay、accumulation、plasticity などを必要なモデルだけが持つ。

## 1. 中央 coordinator は再統合から要求されなかった

M7 の確定結果は component 24/24 A0、integrated 16/16 A0、合計 40/40 A0 であり、reconstruction-added stateless adapter も persistent/stateful coordinator も 0 だった。

したがって今回の再統合では、integrated models を説明するためだけの ninth module / central executive / persistent orchestration state を追加しない。

これは「中央 coordinator が存在しない」という普遍的主張ではない。exact MAIN40 の source scope 内で、それを**追加しないと再構成できない事例が出なかった**という意味に限定する。

## 2. 能力名より下にある反復構造

40本を横断すると、source-defined mechanisms は主に次の反復構造として読める。

- retention: belief、memory trace、weight、value、map、cache、recurrent/workspace state、eligibility/tag などを X 内に保持する。
- update/inference: Bayesian update、prediction error、belief propagation、recurrent transition、plasticity、actor/critic update などを K として実行する。
- selection/control: Q で候補を向け、K/P で softmax、threshold、policy、priority、motor command 等へ落とす。
- prediction/planning: K を T に沿って内部反復し、Q で評価してから P_out に出す。
- routing/gating: attention、task-set routing、feedback gate、neuromodulatory gate、hierarchy-conditioned search 等を source-defined Q/K/P composition として持つ。
- feedback/learning: P_in から reward/error/outcome を受け、K が retained X を更新する。

これらは新しい universal primitives として追加したものではなく、凍結済み Grammar roles と source-defined mechanisms の再配置である。

## 3. 8領域は合成として表せる

### Attention

候補の分割 Pi/C
+ priority/saliency X
+ orientation Q
+ modulation/normalization/routing K
+ readout P

### Belief

retained posterior X
+ evidence update K
+ posterior criterion Q
+ recursive T
+ report/action query P

### Concept

structured reusable representation X
+ typed composition/reconstruction K
+ predictive/fit criterion Q
+ readout P

### Control

state/value/context X
+ control criterion Q
+ policy/control transformation K
+ action P
+ feedback T

### Learning

retained parameter/representation X
+ reward/error/objective Q
+ update K
+ train-to-test T
+ feedback/readout P

### Memory

retained trace X
+ write P_in
+ retention/retrieval K
+ encode-delay-retrieve T
+ read P_out

### Prediction

learned model/belief/predictive representation X
+ transition/inference/value K
+ expected-value/evidence Q
+ prediction/planning T
+ prediction/action query P

### Skill

retained maps/weights/cache X
+ forward/inverse/control K
+ task/error/reinforcement Q
+ action P
+ outcome-feedback-update T

## 4. 統合モデル16本が示すこと

INT-01..16 では、belief、memory、value、planning、routing、accumulation、hierarchy、feedback、plasticity などが複数同時に現れる。

それでも M7 では 16/16 A0 であり、共通の追加 stateful coordinator は必要にならなかった。

そのため今回の再統合では、

```
cognitive capacity
    =
common execution substrate
    +
source-defined retained structure
    +
source-defined transformation graph
```

という表現を採用する。

能力間 coordination も独立した第9能力としてではなく、

```
typed dependency
+ temporal order
+ gating
+ feedback
```

の組合せとしてまず表現できる。

## 5. Self へ落とす場合の最小実装像

実装上は「Memory module」「Belief module」「Skill module」を最初から固定して作るより、

1. typed state store
2. transform/update operators
3. criterion/evaluation operators
4. input/output ports
5. stateless temporal scheduler

を核にし、persistent state は各 mechanism が必要な分だけ持つ方が MAIN40 の分解結果に近い。

例:

```
Belief = retained state + Bayesian update + query
Memory = retained state + write/read + retrieval transform
Skill  = retained state + learned transform + action
Habit  = retained state + direct selection/action path
Plan   = internal transform rollout + criterion + selection
Attention = criterion-conditioned gating/routing
```

この形なら、能力の on/off は「固定モジュールの有無」ではなく、どの retained structure と operator graph を有効にするかとして扱える。

## 6. 今回の再統合で最も重要な観察

新コーパスから得られた像は「8能力 = 8箱」ではない。

むしろ、

> **同じ小さな execution substrate の上に、保持される構造と変換グラフの違いとして各認知能力が現れる。**

そして integrated 16本でも、この substrate を越える universal persistent coordinator は要求されなかった。

これは RelaySelf を、中央 executive を先に設計する方式ではなく、source-defined mechanism の組合せから構成する方向を支持する探索的結果である。

## 限界

これは post-MAIN exploratory reintegration であり、MAIN の事前登録済み判定ではない。

したがって universal cognitive architecture、脳実装の普遍性、系譜独立性、人口母集団上の頻度、RelaySelf の性能優位は主張しない。
