# M16 LRN03 source-correction sensitivity

## Correction

M15 identified one source-grounded retained-reference conflict in LRN03.C1. The frozen retained record treated total initial activity time as matched across the focal protocols without restricting that statement to Experiment 1.

The successor correction keeps the frozen parent artifacts unchanged and narrows the condition:

- Experiment 1: exact total learning time remains matched (30 min versus 30 min).
- Experiment 2: the source schedule is 25 min for the open-book relational-diagram protocol and 24 min for the closed-book reconstruction protocol; exact matching is therefore not asserted for Experiment 2.

No retrieval-practice outcome, probe, scoring, text-structure, or temporal-ordering claim is changed.

## Deterministic sensitivity result

The corrected ClaimIR changes five semantic/provenance paths and therefore changes the canonical semantic structural digest:

- original: `c1e7ae83b83f0e27b9659930c3f9e0e1f16d5d33712f8796a9639697153c0fa5`
- corrected: `03007848ee3a156febd441d5214667636027936d8818b46e495d48f2820c61aa`

However, the frozen Phi projection is exactly identical:

`2ff9cc0fd4981c8c91f4e813c7d43c0691c76a915e9bb128594dfd53e4e84ecb`

for both original and corrected LRN03.

This means the correction is real at the source-faithfulness/semantic-provenance layer but lies below the structural granularity used by the Paper 2 Phi comparator.

## Whole-claim comparator

The full 60-claim surface was replayed with corrected LRN03:

- claims: 60
- pairwise comparisons: 1,770
- relation counts: 1,770 INCOMPARABLE
- LRN03-involving pairs directly affected in principle: 59
- changed pairwise relations: **0**

Thus the frozen whole-claim result remains `1770/1770 INCOMPARABLE`.

## Bounded reconstruction

Because corrected LRN03 Phi is exactly equal to frozen LRN03 Phi, every deterministic Phi-derived bounded-subobject input is unchanged.

- bounded XLike objects: 206
- cross-stratum families: 99
- LRN03 memberships: 28
- membership changes: 0

## Grammar v0 reverse projection

The C role remains source-grounded but is now scoped correctly:

- exact matched-time C: Experiment 1 only
- Experiment 2: 25-versus-24-minute qualification, not exact matching

LRN03 remains:

- verdict: FULL
- roles: `{C,Q,P_in,P_out,T,rho/O}`

Aggregate reverse projection therefore remains:

`21 FULL / 22 PARTIAL / 17 RESIDUAL`

with `0/17` residuals requiring a new top-level role.

## MAIN and validation consequences

No headline Paper 2 structural result changes:

- whole claims: 1770/1770 INCOMPARABLE
- bounded objects: 206
- cross-stratum families: 99
- reverse projection: 21 FULL / 22 PARTIAL / 17 RESIDUAL
- new top-level role among residuals: 0/17
- prospective MAIN40: 40/40 A0

MAIN40 is a separate prospective denominator and is not modified by this designed-corpus source correction.

The frozen M15 replay result is also not post-hoc rescored. It remains 9/10 compatible for Astra and 9/10 compatible for Sol under the rules frozen before the correction. M16 instead records the corrected source authority for successor analyses.

## Interpretation

M16 demonstrates a useful separation between source fidelity and structural comparison. A source-level statement can require correction while leaving the comparison object unchanged because the corrected distinction is finer than the comparator's frozen granularity. This does not make the source error irrelevant; it shows exactly where its effect terminates.

Terminal:

`M16_LRN03_CORRECTION_STRUCTURALLY_INVARIANT`

**Procedural auditability is established; inter-rater reliability remains unmeasured.**
