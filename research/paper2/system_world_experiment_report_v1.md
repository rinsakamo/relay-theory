# Paper 2 — Cognitive system / World / experiment separation

Owner: #349

## 1. Boundary correction

The current Paper-2 architecture is refined to:

    G_cog   cognitive-system grammar
    W       World / environment carrier
    Gamma   system–World coupling
    E_exp   experimental protocol
    R       realized finite run / history

Grammar v0 remains:

    G_cog = {Pi, X, C, Q, P_in, P_out, K, T, rho/O}

World, coupling and experiment are not added to Grammar v0.

## 2. Interface meaning

`P_in` and `P_out` are system-relative interface roles. They do not say who schedules the operation.

    P_in  = operation directed into the modeled system boundary
    P_out = query/read operation exposing a system-relative trace

An experiment may select particular P operations through a coupling/protocol, but:

    experimental action != P_in role
    measurement schedule != P_out role
    K != Gamma
    C != experimental condition

K is retained system transformation/dependence. Gamma is cross-boundary coupling.

## 3. Experiment start is a run cut

The experiment-relative start time `t0` is not assumed to be the cognitive system's absolute origin.

    ... -> X_{t-2} -> X_{t-1} -> X_{t0} -> X_{t1} -> ...

At the observation cut:

    C_{t0}(x_{t0})

states that the realized system state is intrinsically admissible. It does not state why that particular `x_{t0}` was realized.

That may depend on:
- earlier system history;
- earlier World coupling;
- retained/endogenous structure;
- experimental preparation.

Thus:

    intrinsic admissibility != realized cut state != experimental preparation

This removes the need to force an initialization primitive into Grammar v0 at this stage.

## 4. SOURCE_CONTEXT_PARAMETER split

The 13 residual claims contain 27 explicit generic condition nodes.

| Class | Nodes |
|---|---:|
| EXPERIMENT_CONTEXT | 7 |
| WORLD_CONTEXT | 7 |
| RUN_BOUNDARY_OR_PREHISTORY | 4 |
| PARAMETER_ONLY | 5 |
| SYSTEM_INTRINSIC_CONSTRAINT_CANDIDATE | 2 |
| UNDERDETERMINED | 2 |
| **Total** | **27** |

No node is newly promoted to C, X, P, Q or another Grammar-v0 role.

The old SOURCE_CONTEXT_PARAMETER bucket was therefore not one missing primitive. It mixed several different relations to the modeled system boundary.

## 5. Formal companion

A non-invasive Lean companion adds:

- `WorldCoupling G`
- `RunCut G`
- `RunCut.HasSystemPrehistory`
- `ExperimentProtocol G WC`
- `ExperimentStart G WC`

The original `Grammar` record is unchanged.

`RunCut` requires only an experiment-relative start state satisfying existing `stateAdmissible`. It does not assert that the cut is the system's origin.

## 6. Initialization / SOUL consequence

Paper 2 does not currently require a universal initialization role.

A downstream system may require an endogenous prior or selection law over admissible run-cut states. That can be tested separately.

RelaySelf/SOUL is therefore a possible downstream test case for endogenous initialization / retained prehistory, not evidence used to derive the Paper-2 grammar.

## Terminal classification

    COGNITIVE_SYSTEM_WORLD_COUPLING_AND_EXPERIMENT_SEPARATED_WITH_RUN_CUT_SEMANTICS

Grammar v0 remains unchanged.
