# 48-primary-only ablation v1

Status: **VALIDATION EXTENSION RESULT**

This is a challenge-set dependence / induction-set sensitivity test, **not**
held-out validation. The historical 12 challenge claims were excluded before
the primary-only global Archetype reconstruction.

## Primary-only structural reconstruction

- frozen lane-local candidates: 187
- unique global Archetypes: 181
- exact cross-lane equivalence components: 6
- transitive strict-subobject relations: 2595
- direct refinement edges: 410
- cross-lane objects by refinement closure: 81
- bounded survivors after same-support maximality: 181
- cross-lane bounded survivors: 81
- supported primary claims: 47/48
- unsupported primary claim IDs: CNC03

## Frozen Grammar mapping support after challenge exclusion

- `Pi`: 9/48
- `X`: 43/48
- `C`: 11/48
- `Q`: 29/48
- `P_in`: 26/48
- `P_out`: 38/48
- `K`: 45/48
- `T`: 38/48
- `rho/O`: 45/48

- claims instantiating both `P_in` and `P_out`: 25/48
- verdicts: FULL=18, PARTIAL=16, RESIDUAL=14
- all nine roles retain at least one primary-claim witness: true

## Interpretation

Cross-lane recurrence survives challenge exclusion: **true**.

All nine already-frozen Grammar roles retain primary-claim support: **true**.

This does **not** establish independent Grammar discovery or turn the 48
primary claims into an independent induction surface. Grammar v0 remains a
data-constrained refinement/factorization of the declared basis. This result
only tests whether the historical challenge set is necessary for the observed
cross-lane recurrence and for role support under the frozen mapping.

Prospective validation remains required.

Terminal:

`PRIMARY_ONLY_ABLATION_PRESERVES_CROSS_LANE_RECURRENCE_AND_FROZEN_GRAMMAR_ROLE_SUPPORT`
