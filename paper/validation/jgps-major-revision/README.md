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

5. `pvs16-claimir-candidates-v1/` + candidate manifest/source authority
   - 16 source-grounded candidates frozen as **unreviewed**;
   - candidate/schema/admission CI passes;
   - no Grammar mapping has begun.
6. `pvs16-source-consistency-audit-v1.{md,json}`
   - assistant source cross-check: 16/16 PASS for material consistency;
   - this is not human or independent adjudication.
7. `pvs16-author-review-packet-v1.{md,json}`
   - exact candidate SHA-256 values frozen;
   - human decision fields remain null;
   - Grammar mapping remains unauthorized.

## Next authorized operation

A human author/reviewer must complete the PVS-16 source/ClaimIR review transaction
against the frozen author-review packet. Candidates may be ACCEPTED, REVISED, or
REJECTED; any revision must preserve provenance and be re-hashed before the
reviewed PVS surface is frozen.

Only after the reviewed PVS ClaimIR surface is frozen may prospective Grammar
reverse projection begin.

No manuscript rewrite should pre-empt those results.
