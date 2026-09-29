# Paper 2 — Grammar v0 60-claim aggregate

Owner: #343  
Authority: #321, merged PR #322, and the ten merged lane PRs.

## Result

All 60 frozen claims were reverse-projected independently before aggregation.

| Verdict | Count |
|---|---:|
| FULL | 21 |
| PARTIAL | 22 |
| RESIDUAL | 17 |
| **Total** | **60** |

## Aggregate role frequency

A role is counted once per claim when its lane-local status is `SUPPORTED` or `PARTIAL`.

| Role | Claims |
|---|---:|
| Pi | 15 / 60 |
| X | 53 / 60 |
| C | 13 / 60 |
| Q | 36 / 60 |
| P_in | 29 / 60 |
| P_out | 40 / 60 |
| K | 57 / 60 |
| T | 47 / 60 |
| rho/O | 56 / 60 |

These are descriptive frequencies, not weights or importance scores.

## Aggregate interpretation

The independent lanes support a strong reusable core:

- K, rho/O, X and T recur across most of the corpus.
- Q and both interface directions recur across several independent cognitive lanes.
- Pi and C are sparse but independently necessary where frozen individuation or admissibility structure is present.

The same pass also rejects the stronger claim that Grammar v0 is already a lossless full claim language.

The 17 `RESIDUAL` claims, plus residual structure retained by some `PARTIAL` claims, cluster mainly into:

1. **SOURCE_CONTEXT_PARAMETER** — generic context/condition carriers that cannot be relabeled C merely because they are called conditions.
2. **RELATION_LANGUAGE_GAP** — differs/distinguishes/non-entailment, null effects, epistemic/model-inference relations, qualified similarity and model rejection.
3. **FORMAL_CARRIER_GAP** — the Lean carrier is narrower than some frozen Discussion-level K/rho/O/P topologies.
4. **DERIVED_STRUCTURE_GAP** — persistence, duration, recurrence or other structure may be derivable but lacks a frozen witness for the required derivation.
5. **UNDERDETERMINED** — a frozen claim retains an ambiguity not repaired by the grammar.

This aggregate pass does **not** establish a new top-level `ROLE_GAP`.

That matters: the current evidence does not yet say "add a ninth cognitive primitive." It says that the role grammar and a complete scientific claim language are different objects.

## Distinctions that survived hostile validation

The aggregate preserves the following separations:

- K != T
- P_in != P_out
- C != generic condition
- Q != scalar reward
- Pi != physical boundary
- O != terminal output
- K need not be a deterministic function
- persistence != literal K = I without explicit carry/transport

## Strong positive cases

BLF is 6/6 FULL. CNC is 5 FULL + 1 PARTIAL. Several individual claims in every major family directly instantiate substantial Grammar-v0 subobjects.

The failure pattern is therefore not "the grammar never fits." It is selective: the core role vocabulary compresses a large fraction of frozen cognitive structure, while additional scientific-claim semantics survive outside the role inventory.

## Next hostile tests

Do not repair Grammar v0 yet.

Compare:

```
G_dyn       = {X, K, T}
G_pomdp     = POMDP-like state/action/transition/observation/criterion grammar
G_full_v0   = {Pi, X, C, Q, P_in, P_out, K, T, rho/O}
```

The main question is whether the added roles in `G_full_v0` preserve frozen distinctions that the simpler comparators cannot recover without ad hoc additions.

After that, adjudicate residuals to determine whether any genuine `ROLE_GAP` remains.

## Terminal classification

```
GRAMMAR_V0_BROAD_ROLE_COVERAGE_WITH_NONLOSSLESS_CLAIM_LANGUAGE_RESIDUALS
```

Grammar v0 remains unchanged.
