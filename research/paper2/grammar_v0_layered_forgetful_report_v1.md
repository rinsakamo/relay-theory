# Paper 2 — Layered architecture and comparator forgetful maps

Owner: #347

## Layer split

The post-hostile-validation architecture is:

```
L_sys    system grammar
L_claim  scientific assertion semantics
L_ctx    source / experimental context parameters
L_formal concrete mathematical realization
```

with:

```
L_sys = {Pi, X, C, Q, P_in, P_out, K, T, rho/O}
```

This split preserves the result of #345: **ROLE_GAP = 0** among the 17 RESIDUAL claims.

The residuals do not currently justify Grammar v1. They instead show that a system grammar is not identical to a complete scientific claim language.

## Formal forgetful views

A new non-invasive Lean module defines two views without changing `Grammar`.

### Dynamical view

```
F_dyn : G_full_v0 -> {X,K,T}
```

The target K relation is the existential image of the source transition:

```
K_dyn(x,x')  iff  exists p_in, K_full(x,p_in,x')
```

Therefore P-in identity is deliberately forgotten, together with Pi, C, Q, P-out and O/rho.

This makes the empirical minimality statement precise: G_dyn is a coarse view, not an equivalent presentation.

### POMDP-like view

The second view keeps:

```
State = X
Action = P_in
transition = K
observation carrier = O
criterion preorder = Q
succession = T
```

but defines observation after existentially forgetting which P-out query generated the trace:

```
observe_pomdp(x,o)  iff  exists p_out, observe_full(x,p_out,o)
```

Pi and C are absent from the target signature.

The formal comparator deliberately retains generalized preorder Q. Restricting further to scalar reward would be an additional specialization and would lose further frozen Q distinctions.

## Frozen witness counts

| Distinction | Claims |
|---|---:|
| Pi | 15 |
| C | 13 |
| Q | 36 |
| P_in | 29 |
| P_out | 40 |
| P_in and P_out both required in one claim | 26 |
| rho/O | 56 |

For G_dyn, 59/60 claims instantiate at least one role outside {X,K,T}; the only role-subset case, CH01.C1, is itself RESIDUAL.

For the POMDP-like comparison, 26/60 require Pi or C, and 26/60 require both P directions. The union of claims hit by missing Pi, missing C, or loss of a first-class P-direction split is 44/60.

## Manuscript interpretation

The safe result is:

> Grammar v0 is a recurrent system-role grammar, while scientific claim semantics, source-defined contextual parameters, and concrete formal carriers occupy distinct layers.

and:

> Generic dynamical and POMDP-like views recover substantial substructure, but their natural forgetful projections erase frozen distinctions. Recovering those distinctions requires enrichments equivalent to reintroducing omitted Grammar-v0 structure.

Do not strengthen this to an absolute mathematical minimality claim. Arbitrary re-encodings into a weaker formalism are not ruled out; they simply cease to preserve the frozen distinctions directly.

## Formal status

`UnifiedCognitiveStructuralGrammar.Grammar` is unchanged.

New formal companion:
- `RelayTheory/GrammarComparatorViews.lean`
- `Grammar.toDynView`
- `Grammar.toPomdpLikeView`
- kernel-visible iff witnesses for the existential forgetting steps.

## Terminal classification

```
SYSTEM_GRAMMAR_LAYER_FROZEN_WITH_FORMAL_FORGETFUL_COMPARATORS
```
