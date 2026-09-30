# Basis-to-Grammar Provenance Audit v1

Status: **VALIDATION EXTENSION RESULT — ADDITIVE ONLY**

Authority:
- validation protocol: #365
- frozen basis: `research/paper2/working_basis_v1.json`
- Grammar-v0 discussion authority: #321
- frozen reverse-projection aggregate: `research/paper2/grammar_v0_reverse_projection_aggregate_v1.json`
- frozen comparator support counts: `research/paper2/grammar_v0_minimality_comparator_v1.json`
- reconciled result: `research/paper2/paper2_result_v1.json`

No frozen Paper-2 artifact is modified by this audit.

## Result

The fresh JGPS objection is **substantively correct**: Grammar v0 is not an independently discovered nine-primitive inventory.

The frozen provenance is better described as:

> **a data-constrained refinement / factorization of the declared comparison basis (B_{P2})**.

The role inventory contains no role classified as `NEW_TOP_LEVEL_ROLE`.

| Grammar-v0 role | Frozen basis source | Provenance class | Frozen support relevant to the classification |
|---|---|---|---|
| (Pi) | (Pi) | INHERITED | Same explicit partition/subsystem coordinate; 15/60 claims support the Grammar role. |
| (X) | (S) | RENAMED_OR_REINTERPRETED | #321 explicitly treats frozen (S) as a generic configuration/carrier (X); 53/60 claims support (X). |
| (C) | (C) | INHERITED | Same explicit constraint coordinate; 13/60 claims support (C). |
| (Q) | (Q) | INHERITED | Same explicit criterion/evaluation coordinate, generalized in Discussion semantics; 36/60 claims support (Q). |
| (P_{in}) | (P) | DATA_CONSTRAINED_SPLIT | Frozen (P) already covered probes/interventions/transformations but not an explicit directional factorization. Reverse projection supports (P_{in}) in 29 claims. |
| (P_{out}) | (P) | DATA_CONSTRAINED_SPLIT | Same frozen (P) parent; reverse projection supports (P_{out}) in 40 claims. |
| (K) | (K) | INHERITED | Same explicit transition/coupling/dependency coordinate; 57/60 claims support (K). |
| (T) | (T) | INHERITED | Same explicit temporal coordinate; 47/60 claims support (T). |
| (ho/O) | (O) | RENAMED_OR_REINTERPRETED | Frozen (O) is observation/access; #321 adds the weaker Discussion-level interpretation of boundary-relative projection/trace; 56/60 claims support the role. |

## Directional (P) split

The only top-level factorization that increases the number of named roles relative to the eight-coordinate basis is:

[
P ightarrow (P_{in},P_{out}).
]

This split is not licensed merely by notation. The frozen aggregate reports:

- (P_{in}): 29 claims / 9 lanes;
- (P_{out}): 40 claims / 9 lanes;
- 26 claims instantiate **both** directions.

The last count is preserved in `paper2_result_v1.json` under the POMDP-like strict-preservation summary.

This supports the claim that the directional distinction is nontrivial **within the frozen representation and corpus**.

It does **not** establish that the split was discovered independently of the Grammar proposal, because the directional Grammar mapping was itself introduced after the bounded reconstruction. The correct evidential claim is therefore:

> Once the directional split was proposed, frozen claim structure supported preserving it in a substantial subset of the corpus, including 26 claims requiring both directions under the frozen mapping.

## (Sightarrow X) and (Oightarrowho/O)

These are not new empirical roles.

- (Sightarrow X) is a deliberate carrier-level reinterpretation intended to avoid treating the basis symbol (S) as a substantive state ontology.
- (Oightarrowho/O) is a Discussion-level relational interpretation of the frozen observation/access coordinate.

Both remain representation choices constrained by the frozen claim structures.

## Consequence for the manuscript

Avoid:

> “the data independently recover nine primitive cognitive roles.”

Prefer:

> “Within the declared structural representation, the bounded reconstruction supports a reusable factorization of the frozen comparison basis. Most roles inherit basis coordinates directly; (S) and (O) receive carrier/trace reinterpretations, while the frozen corpus supports a directional refinement of (P) into (P_{in}) and (P_{out}).”

Also preserve:

- no theory-neutrality claim;
- no ontology-neutrality claim;
- no representation-neutrality claim;
- no demarcation criterion for cognition;
- no independent primitive-discovery claim.

## Terminal classification

`GRAMMAR_V0_IS_DATA_CONSTRAINED_BASIS_REFINEMENT_NOT_INDEPENDENT_PRIMITIVE_DISCOVERY`
