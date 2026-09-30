# JGPS Major Revision validation extension

Authority: #365

This directory contains additive validation work produced after the fresh JGPS
Major Revision review. It does not replace or rewrite frozen Paper-2 authority.

## Current state

Completed and frozen:

1. `validation-extension-v1.{md,json}`
   - pre-analysis protocol;
   - historical challenge set explicitly not treated as held out.
2. `basis-to-grammar-provenance-v1.{md,json}`
   - Grammar v0 classified as a data-constrained refinement/factorization of
     `B_P2`;
   - no independently discovered new top-level primitive is claimed.
3. `primary-only-ablation-v1.{md,json}`
   - Challenge A/B excluded before global Archetype reconstruction;
   - 181 unique primary-only global Archetypes;
   - 81 cross-lane bounded survivors;
   - 47/48 primary claims covered;
   - all nine frozen Grammar roles retain primary-claim support;
   - this remains a sensitivity analysis, not held-out validation.
4. `pvs16-admission-v1.{md,json,sha256}`
   - 16 claims admitted from the frozen pre-Grammar candidate ledger;
   - selection is deterministic from validator-bound ledger order;
   - admission hash frozen before ClaimIR creation or Grammar mapping.

## PVS-16 admission digest

`0a4454887189730cf4b13d12061f4cab93fb8e4d8f0ec089a08f77bc088dc123`

## Next authorized operation

Create source-grounded ClaimIR for the 16 admitted PVS claims under the existing
frozen ClaimIR schema and source-review rules, without changing Grammar v0,
residual taxonomy, or comparator semantics.

Only after those records are reviewed and frozen may prospective Grammar
reverse projection begin.

No manuscript rewrite should pre-empt those results.
