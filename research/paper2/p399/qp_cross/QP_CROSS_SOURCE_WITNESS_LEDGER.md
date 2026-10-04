# QP pair evidence ledger and source-bound structural losses

**Status:** exploratory retrospective sidecar for #399; not a blinded independent reconstruction. Method contract committed at `e214a5c3ce5b2b30ee55ef83a193d896c07d2cdd` **before pair verdict file** `QP_CROSS_RESULT_SHORT.md`, but the author and assistant had previously seen QP development summaries and some original text. New ledger IDs below **are not** original A IDs.

## Primary source witness table

| Sidecar ID | Paper | Graph relation or bound | Exact accessible original HTML locator |
| --- | --- | --- | --- |
| 01-E1 | QP01 Ashinoff et al. 2022 | prior logit and bead-draw likelihood logit weighted separately -> current posterior; prior from previous posterior, time indexed by draw | [PLOS original full HTML](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010796), Computational modeling, *Weighted Bayesian belief-updating model and variants* |
| 01-E2 | QP01 | fitted prior underweight predicts recency plus prior-dependent update and reduced **attainable upper certainty**; omega2 scales evidence separately; these should not be fused | same source, original Fig 2C–E captions, Results and computational modeling |
| 01-E3 | QP01 | distinct noisy-sampling *functional account* links noisy representation of prior/likelihood to effective weights; do not treat it as a measured online relevance gate | same source, Computational modeling, *Noisy-sampling model* |
| 03-E1 | QP03 Marković et al. 2015 | prior beliefs + experimenter observations + predicted relevance enter next represented belief; predicted relevance attenuates evidence for low-relevance hypotheses | [PLOS original full HTML](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004558), *Bayesian inference*, text after Eqs 10–12 |
| 03-E2 | QP03 | separate hypothesis, exemplar-pair and feature representations; within-level WTA inhibition and between-level excitation govern relevance dynamics | same source, *Hierarchical generative model* Fig 4, Eqs 5–7 prose and *Structured models* Fig 5 |
| 03-E3 | QP03 | represented belief -> separate response mapping; analyst-side OTO Bayesian model evidence is **not** the modeled participant's cognitive update | same source, *Observing the Observer framework* Fig 3 |
| 04-E1 | QP04 Flesch et al. 2023 | task cue history -> EMA-modulated signal, prior-trial persistence governed by alpha | [PLOS original full HTML](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010808), *Sluggishness* Methods and original Fig 3 |
| 04-E2 | QP04 | task cue plus task-to-hidden anticorrelated weights -> selective ReLU activation suppresses irrelevant hidden units | same source, original Figs 4–5 and *Anti-correlated task weights via Hebbian learning* |
| 04-E3 | QP04 | alternating Oja/Hebbian association updates and SGD train task network parameters, distinct learning operations/time regimes | same source, *Continual Learning with Hebbian updates and SGD*, Methods |
| 04-E4 | QP04 | deeper-tree context not leading variance unless very large context scalar; training unstable **even then**; task-only known-context updates used as conditional extension | same source, Discussion paragraph beginning *We focussed on a simple context-dependent decision-making problem* |

## Pair 01 × 03: candidate common image vs necessary losses

Bounded common image `M13`: `represented prior + source-facing evidence + typed influence modifier -> next represented belief`, with `next belief -> following prior` where explicitly documented. Witness `01-E1` against `03-E1`. **Typed mismatch:** `QP01.omega2` is a subject/condition model coefficient, whereas `QP03.predicted_relevance` is an evolving internal inferred representation; mapping them requires forgetting their origin and state dynamics and therefore **cannot be a faithful mechanism equivalence**. `01-E2` and `03-E2` remain retained *unmatched* discriminatory witnesses; do not manufacture a shared WTA, hierarchy, noise rule or long-run certainty bound. Verdict `S1_PARTIAL` under explicitly weakened graph only.

Weak negative `M13-XKT`: discard influence-modifier provenance and type; both become X→K→X with T, so agreement is compatible with the `G_dyn={X,K,T}` Grand Null. The richer common image is **not** an all-source discriminating maximal common subgraph because of the typed mismatch above.

## Pair 03 × 04: candidate common image vs necessary losses

Bounded common image `M34`: `information relevance/context mediates selective influence of incoming information on downstream represented state/activity`. Witness `03-E1/03-E2` against `04-E1/04-E2`. This is a candidate **functional relation-pattern** within Q/K; *not* a transfer of the actual control algorithm. The essential mismatch: QP03 inferentially evolves latent hierarchical relevance using noise, inhibition and excitation, while QP04 receives externally cued context, retains a trial-level EMA, and learns synaptic task-to-hidden weights through Oja interleaved with task learning via SGD (`04-E3`). ReLU hidden-unit selection is not Bayesian posterior weighting. Current evidence does not supply a source-defined mechanism-preserving bridge; `S1_PARTIAL`, **no S2**.

Weak negative `M34-XKT`: after removing relevance/context semantics, both are merely internal state transformations over time; this cannot reject Grand Null.

## Source exclusions and scientifically mandatory limitations

1. QP03's published 17-model claim conflicts with the literally enumerated 12+6+1 reading; the w2/w3 source descriptions also conflict on level labeling. Neither may be arbitrarily repaired. Exact embedded mathematical glyphs and standalone supplements are unverified in this sidecar.
2. QP04's Methods/Discussion distinctions do not certify one exact full-model Oja **input mask** for every claimed variant. `04-E4` is a *conditional deep-tree extension*, not automatic main-model equivalence. Keep its **two** adverse clauses individually.
3. No claim of independent blinded rater, formal pairwise exact A-ID alignment, machine-verified source truth, empirical frequency of shared structure, new Grammar primitive or general H0/H1/H2 inference. The historical QP source-scoped first passes remain frozen and these observations must not enter an unmasked MAIN analyst packet.
