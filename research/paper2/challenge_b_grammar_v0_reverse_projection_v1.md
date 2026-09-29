# Challenge B reverse projection into Unified Cognitive Structural Grammar v0

Owner: #336  
Authority: #321, merged PR #322  
Frozen Challenge-B Archetype reconstruction: commit `bcd8c6d34c306a9149fcdc89cc973eae9513c71b`  
Base `main`: `78cd63cd6ec2898f3b4783b6db394c73c0551ff4`

## Scope

Processed exactly:

- `CH02.C1`
- `CH04.C1`
- `CH06.C1`
- `CH08.C1`
- `CH10.C1`
- `CH12.C1`

CH01/03/05/07/09/11 and every non-CH lane were not processed. No paper was reread. ClaimIR, B_P2, Phi, U_claim, F_R, structural adjudications, bounded Archetype identities, and Grammar v0 were not modified.

The exact per-role evidence, frozen input hashes, relation mappings, Archetype IDs, derived candidates, and residuals are recorded in:

`research/paper2/challenge_b_grammar_v0_reverse_projection_v1.json`

## Per-claim result

| Claim | Verdict | Instantiated Grammar-v0 roles |
|---|---|---|
| CH02.C1 | PARTIAL | X, Q, K, rho/O (partial) |
| CH04.C1 | FULL | Pi, X, K, rho/O |
| CH06.C1 | PARTIAL | X, Q, P_in, K, T, rho/O (partial) |
| CH08.C1 | PARTIAL | Pi, X, K, T, rho/O |
| CH10.C1 | RESIDUAL | X, Q, K, T, rho/O (partial) |
| CH12.C1 | PARTIAL | Pi, X, C, Q, P_in (partial), K, T, rho/O |

## Coverage

```text
CH-B coverage = 6 / 6

FULL     = 1
PARTIAL  = 4
RESIDUAL = 1
```

Role frequency counts SUPPORTED or PARTIAL instantiation:

```text
Pi     = 3 / 6
X      = 6 / 6
C      = 1 / 6
Q      = 4 / 6
P_in   = 2 / 6
P_out  = 0 / 6
K      = 6 / 6
T      = 4 / 6
rho/O  = 6 / 6
```

## Main findings

All six claims instantiate X and K. O carriers also occur in all six, but O-carrier membership is not treated as proof of a directed or functional `rho : X -> O`. CH02, CH06, and CH10 therefore retain only partial rho/O support.

The three frozen partition cases map cleanly to non-physical Pi only where the structural adjudication explicitly retained `partition_Pi`:

- CH04: role and nested-role decomposition;
- CH08: processing-stage and information-type decomposition;
- CH12: specialized subsystem decomposition.

Q remains non-scalar. Across CH-B it covers Bayesian criterion satisfaction, objective/value-cost/prior orientation, uncertainty-based comparison, and cycle-specific control-value selection.

C is needed only by CH12, where `limited_interface_states` is explicitly frozen under `resource_C` and constrains exposed interface contents. Generic `condition` nodes are not promoted into C.

P directionality is sparse. CH06 has explicit intervention/write support from `world_directed_action`. CH12 has partial P_in support because `interface_update_or_request` is structurally a write/request but is frozen as an O outcome rather than as a separate operation carrier. No CH-B claim requires P_out.

## Recurrent frozen substructures

The Challenge-B Archetype report contains 12 maximal candidates, all with `edge_count = 0`. They therefore support recurrent role bundles but do not independently license K or rho edges.

Notable recurrent candidates include:

- `A-ab04d718522b`: O/Q/S across CH02, CH06, CH10, CH12;
- `A-d47d66c86623`: O/S/T across CH06, CH08, CH10, CH12;
- `A-1ed75dd53a7a`: O/Pi/S across CH04, CH08, CH12;
- `A-00e50f4529f6`: O/Q/S/T across CH06, CH10, CH12.

## Residuals and pressure

### CH02

The frozen old-`probe_P` control includes `linear_population_transform`, but the ClaimIR explicitly describes it as internal computation rather than intervention and supplies no read/query direction. The computation maps cleanly to K, but not to Grammar-v0 P_in/P_out. Its principal encoding relations run O -> X, so no directed rho is invented.

### CH06

`world_directed_action` supports P_in. The same frozen old-P control also includes `internal_state_optimization`, which has no independently frozen interface direction; it is retained as K pressure rather than forced into P. Sensory O is boundary-coupled, but no explicit P_out/rho read operation is frozen.

### CH08

Frozen persistence is retained, but there is no explicit typed carry map or K witness identifying successive maintained configurations. Persistence is therefore only a candidate derived feature over T, never a blanket `K = I`.

### CH10

CH10 is the decisive bounded counterexample to full direct/lossless expressibility under unchanged Grammar v0.

Two required frozen nodes remain outside the grammar-role inventory:

```text
current_state     -> basis.cnd1
candidate_action  -> basis.cnd2
```

`resource_C` is `not_required`, so neither node can be repaired into C. They remain required inputs to r3/r7.

CH10 also preserves its already-frozen structural-adjudication residual: the single approximation-mode contract cannot simultaneously retain approximate internal valuation computation and stochastic final action sampling. Grammar v0 does not repair that separate claim-language loss.

Persistence is present but again lacks an explicit typed carry witness.

### CH12

CH12 is the strongest direct interface case: Pi + C + rho/O is explicitly supported by subsystem partitioning, limited interface states, and constrained exposure. Its `current_interface_pattern -> selected_mapping -> interface_update_or_request` ordering remains T, separate from K.

The source-acknowledged `direct_bypass_pathway` remains a topology pressure point. The frozen relation distinguishes it from the serial route but does not specify subsystem endpoints, so no extra Pi-indexed bypass K edge is inferred.

## Compression / derived-feature candidates

Supported or plausible compressions on the frozen surface:

- frozen S -> X across all six claims;
- nested-role, processing-stage, information-type, and subsystem decompositions -> Pi where `partition_Pi` is frozen present;
- heterogeneous criterion forms -> generalized Q;
- history-window, future-horizon, recurrence, and explicit order -> T refinements;
- CH12 limited interface exposure -> Pi + C + rho/O specialization;
- some old-P internal computations -> K rather than Grammar-v0 interface P, without rewriting frozen provenance.

Persistence -> typed carry across T remains unearned in CH-B because no explicit carry map is frozen.

## Counterexample assessment

```text
YES_BOUNDED_COUNTEREXAMPLE_TO_FULL_DIRECT_EXPRESSIBILITY
```

Decisive claim: `CH10.C1`.

This does not invalidate the frozen B_P2 mapping, does not imply that the Grammar-v0 role vocabulary is useless, and does not authorize a grammar change in this lane.

Terminal classification:

```text
CHALLENGE_B_GRAMMAR_V0_PARTIAL_COVERAGE_WITH_CH10_DIRECT_EXPRESSIBILITY_COUNTEREXAMPLE
```

Architecture consequence: **NONE**.

Stop after Challenge B.
