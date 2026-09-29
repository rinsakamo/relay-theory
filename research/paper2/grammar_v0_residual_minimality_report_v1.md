# Paper 2 — Residual adjudication and Grammar v0 minimality test

Owner: #345

## 1. Residual adjudication

All 17 aggregate `RESIDUAL` claims were re-adjudicated without rereading papers or changing any frozen lane result.

Primary classification:

| Class | Claims |
|---|---:|
| SOURCE_CONTEXT_PARAMETER | 13 |
| RELATION_LANGUAGE_GAP | 4 |
| ROLE_GAP | **0** |

Secondary pressures include formal-carrier mismatch (6 claims), derived-structure underidentification (2), and one underdetermined approximation contract.

**Result: no top-level role gap is established by the 17 residual claims.**

The dominant residual is not "missing cognition primitive." It is that a structural role grammar is not identical to a full scientific claim language.

## 2. G_dyn hostile comparator

Define:

```
G_dyn = {X, K, T}
```

Under strict frozen-distinction preservation:

- 59/60 claims instantiate at least one role beyond G_dyn.
- Only CH01.C1 has an instantiated role set contained in {X,K,T}.
- CH01.C1 is itself RESIDUAL because its phase-condition identities survive beyond T.

Therefore:

```
strict FULL direct preservation by G_dyn = 0 / 60
```

This does not mean an arbitrary dynamical formalism cannot encode the claims. It means it cannot do so **while preserving the frozen distinctions directly** without hiding Pi/C/Q/P/rho structure inside X or K.

## 3. POMDP-like hostile comparator

Use the generous comparator:

```
G_pomdp = {X, P, K, rho/O, Q, T}
```

even before restricting Q to scalar reward.

Observed pressure:

- 26/60 claims require explicit Pi or C.
- 26/60 claims instantiate both P_in and P_out in the same claim.
- 44/60 claims are hit by at least one of:
  - missing Pi,
  - missing C,
  - collapsing P_in/P_out into one P.
- Q occurs in 36/60 claims and includes non-scalar predicates, thresholds, reference-relative classifications, relevance filters, correctness and uncertainty criteria.
- LRN and CH-B expose O/rho directionality beyond a single state-generated outward observation model.

Thus the POMDP-like comparator captures much of the backbone, but loses frozen distinctions unless it is enriched in ways that substantially reconstruct Grammar-v0 roles.

## 4. Role ablation result

Every Grammar-v0 role has independent cross-lane frozen support.

| Role | Claims | Lanes |
|---|---:|---:|
| Pi | 15 | 9 |
| X | 53 | 10 |
| C | 13 | 9 |
| Q | 36 | 10 |
| P_in | 29 | 9 |
| P_out | 40 | 9 |
| K | 57 | 10 |
| T | 47 | 10 |
| rho/O | 56 | 10 |

These frequencies are not importance scores. Their use here is only to show that no role is a one-paper or one-lane artifact.

The frozen evidence also supplies role-specific witnesses that block simple collapse:
- Pi: nested/functional/classificatory individuation;
- C: admissibility distinct from criterion and generic condition;
- Q: criterion orientation distinct from dynamics;
- P_in/P_out: intervention versus query direction;
- K/T: transformation/dependence versus succession/order;
- rho/O: trace/readout distinct from X and P.

## 5. Main conclusion

The current evidence supports:

```
Grammar v0 role inventory
  = non-trivial under strict frozen-distinction preservation

Grammar v0
  != complete scientific claim language

17 residuals
  != evidence for a ninth top-level cognitive role
```

This is the useful split.

The next manuscript architecture should distinguish:

1. **system grammar** — Pi, X, C, Q, P_in, P_out, K, T, rho/O;
2. **claim/assertion layer** — comparison, non-entailment, null-effect, epistemic/model-inference and related semantics;
3. **context/index layer** — source-defined experimental/context parameters;
4. **formal carrier layer** — concrete Lean signatures and their generalizations.

No Grammar-v1 repair is authorized by this test.

## Terminal classification

```
GRAMMAR_V0_ROLE_INVENTORY_NONTRIVIAL_UNDER_STRICT_PRESERVATION_WITH_NO_NEW_ROLE_GAP
```
