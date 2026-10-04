# QP cross-paper comparison — bounded exploratory result

Contract: e214a5c3ce5b2b30ee55ef83a193d896c07d2cdd. This is outcome-exposed retrospective research, not independent MAIN testing. Original QP A/B/C remain frozen.

## QP01 × QP03

Verdict: S1_PARTIAL. Both source models have prior represented state, incoming evidence, a source-specific influence modifier, and a successor represented state. QP01 uses fitted prior and likelihood coefficients in a sequential logit update; QP03 modulates hypothesis evidence by dynamically predicted hierarchical relevance. Their influence modifiers are *not* the same type. QP01 prior attenuation and long-run certainty effects and QP03 separate feature/exemplar/hypothesis states, within-level inhibition and between-level excitation must remain unmatched. X/K/T-only projection is a non-discriminating negative control.

## QP03 × QP04

Verdict: S1_PARTIAL. Both models condition which information has downstream influence. QP03's expected latent relevance modulates evidence during probabilistic inference. QP04's context signal and learned anti-correlated task-to-hidden weights gate activity via ReLU. Identifying inference with Oja/SGD weight learning would erase mechanism and temporal distinctions. QP04 EMA trial-history carryover also has no established QP03 equivalent. X/K/T-only projection is non-discriminating.

Both pairs: no S2 support and Grand Null not rejected. QP03 original model counts and w2/w3 naming unresolved; QP04 main Oja input mask uncertain. Deep-tree extension needs large context scaling and remains unstable even after such scaling unless the training scheme is conditionally changed.

Source: QP01 DOI 10.1371/journal.pcbi.1010796 (Fig2, Weighted Bayesian/Noisy-sampling Methods); QP03 DOI 10.1371/journal.pcbi.1004558 (Fig3–5 and Eqs6–12 prose); QP04 DOI 10.1371/journal.pcbi.1010808 (Fig3–5, Methods, Discussion). Only official full original HTML legible prose/captions checked. No exact source-image symbol audit or exact historical QP-A-ID maximal-common-subgraph proof was performed.
