# Paper 2 Result v1 — deterministic reconciliation

Owner: #351

## Status

```
PAPER2_RESULT_V1_DETERMINISTICALLY_RECONCILED
```

This report reconciles already-frozen Paper-2 artifacts. It does not modify ClaimIR, B_P2, Phi, U_claim, F_R, structural adjudications, bounded Archetype identities, lane reverse projections, or Grammar v0.

## Source-review boundary

The primary reference corpus is:

```
48 / 48 primary claims reviewed
12 / 12 challenge claims reviewed
60 / 60 total reviewed
```

Manifest state:

```
ALL_60_DESIGNED_CLAIMIR_SOURCE_GROUNDED_REVIEWED
```

The extraction-reliability boundary remains intentionally narrower:

```
independent extractor agreement           = NOT ESTABLISHED
local automated production qualification = NOT ESTABLISHED
deterministic ChatGPT replay              = NOT CLAIMED
```

Terminal reliability classification:

```
EXTRACTION_UNDERDETERMINED_WITH_SOURCE_AUDITED_REFERENCE_CORPUS
```

## Grammar-v0 reverse projection

```
FULL     = 21
PARTIAL  = 22
RESIDUAL = 17
TOTAL    = 60
```

Role frequencies, counting a role once per claim when lane-local status is SUPPORTED or PARTIAL:

| Role | Claims |
|---|---:|
| Pi | 15 |
| X | 53 |
| C | 13 |
| Q | 36 |
| P_in | 29 |
| P_out | 40 |
| K | 57 |
| T | 47 |
| rho/O | 56 |

## Residual adjudication

Primary classes among the 17 residual claims:

```
SOURCE_CONTEXT_PARAMETER = 13
RELATION_LANGUAGE_GAP    = 4
ROLE_GAP                 = 0
```

Other classes occur only as secondary pressure in the frozen adjudication.

Therefore:

```
NO_TOP_LEVEL_ROLE_GAP_ESTABLISHED_IN_THE_17_RESIDUAL_CLAIMS
```

The residuals do not authorize Grammar v1.

## Source-context architecture placement

The 13 SOURCE_CONTEXT_PARAMETER residual claims contain 27 explicit generic condition nodes.

| Placement | Nodes |
|---|---:|
| EXPERIMENT_CONTEXT | 7 |
| WORLD_CONTEXT | 7 |
| RUN_BOUNDARY_OR_PREHISTORY | 4 |
| PARAMETER_ONLY | 5 |
| SYSTEM_INTRINSIC_CONSTRAINT_CANDIDATE | 2 |
| UNDERDETERMINED | 2 |
| **Total** | **27** |

No node is newly promoted to C or another Grammar-v0 role.

## Strict-preservation comparators

For:

```
G_dyn = {X,K,T}
```

59 / 60 claims instantiate at least one role beyond the target vocabulary and strict FULL direct preservation is 0 / 60.

For the generous POMDP-like comparator:

```
G_pomdp = {X,P,K,rho/O,Q,T}
```

the frozen loss witnesses are:

```
claims requiring Pi or C                         = 26
claims using both P_in and P_out                 = 26
union affected by missing Pi/C or collapsed P    = 44
```

These are strict direct-preservation results, not proofs of absolute mathematical non-encodability.

## Layered architecture

The final Paper-2 architecture keeps distinct:

```
L_sys
L_claim
L_ctx
L_formal
```

and additionally separates composition around the modeled cognitive system:

```
G_cog   cognitive-system grammar
W       World / environment carrier
Gamma   system–World coupling
E_exp   experimental protocol
R       realized finite run / history
```

World, coupling and experiment are not added to Grammar v0.

The experiment start is a finite run cut, not necessarily the origin of the cognitive system.

## Formal identity

`UnifiedCognitiveStructuralGrammar.lean` remains frozen at Git blob:

```
a688edb063c0ad43c25df15f497918817e8b74cd
```

The later comparator and system/World/experiment formal modules are companions rather than modifications of the Grammar record.

## Manuscript-safe core result

A bounded, source-reviewed 60-claim corpus supports a recurrent system-role grammar:

```
{Pi, X, C, Q, P_in, P_out, K, T, rho/O}
```

under strict frozen-distinction preservation.

The result does **not** establish:

- a complete scientific claim language;
- an ontology of nine cognitive substances;
- absolute mathematical minimality;
- independent extractor reliability;
- deterministic model replay;
- population-scale validation;
- a claim that all cognition instantiates all roles.

Residual pressure is localized primarily to claim-language semantics, source/world/experimental context, formal-carrier realization, and derived structure rather than to a missing top-level system role.

## Paper-3 boundary

The 1000-work validation, scalable extraction/replay, and large-scale retention/dynamics tests remain outside Paper 2.

## Terminal classification

```
PAPER2_RESULT_V1_DETERMINISTICALLY_RECONCILED
```
