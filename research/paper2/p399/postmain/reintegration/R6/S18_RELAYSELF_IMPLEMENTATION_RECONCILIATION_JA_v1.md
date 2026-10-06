# RelaySelf S18 implementation reconciliation against Paper2 post-MAIN

## Status

This document is a **post-MAIN theory-to-implementation reconciliation**.

It does not modify the frozen MAIN40 adjudication, does not add scientific
corpus evidence, does not redesign RelaySelf, and does not start Paper3.

Theory base for this layer:

- RelayTheory R5 exact HEAD:
  `826ad01fd2caa8a6a783a1670b4255888f262c0d`
- parent branch:
  `paper2/p399-postmain-self-s4-handoff-20261006`

RelaySelf implementation subject:

- repository: `rinsakamo/relay-self`
- S18 Draft PR: #354
- exact S18 HEAD:
  `b5eb5d3416a9c303b855250adea4323e7611f350`
- exact S18 base:
  `64868337510a960c140e96d5d3d20949ad53fb8e`
- `docs/postmain-architecture.json` SHA256:
  `762e575572c2ccb70cf073006b7e18d9617fd3939d0f9f72665d41901958eec9`
- `docs/postmain-architecture.md` SHA256:
  `33218278d69d16764db890ff4e1dde2c5eaee39213873e7438c47fbe12d56fbb`
- S18 freeze receipt: PR #354 comment `6026139132`

Frozen S18 terminal interpretation:

```
S18_FROZEN_AS_SINGLE_TRANSACTION_COGNITIVE_ACTION_LEARNING_ARCHITECTURE_WITH_EXPLICIT_OWNERSHIP_AND_AUTHORITY_BOUNDARIES
```

## Theory authorities inspected

This reconciliation was written from current repository artifacts rather than
from memory.

1. **M7 / PR #459**, exact HEAD
   `48b2cf3c627e030e7131af485206b0013d7e02f1`
   - `research/paper2/p399/main/integration/M7/M7_MAIN_RESULT_JA.md`
   - `M7_RECURRING_INTERFACE_ARCHETYPES_v1.json`
   - `M7_A1_INTERFACE_ADVERSE_AUDIT_v1.json`
   - `M7_A2_STATEFUL_MECHANISM_ADVERSE_AUDIT_v1.json`
2. **M9A / PR #461**, exact HEAD
   `1938a09e119860dc3d4325b86b1ce5b8bab62fd5`
   - `research/paper2/p399/main/integration/M9A/M9A_CATEGORICAL_LIFT_FOUNDATION_v1.md`
3. **R1 / PR #465**, exact HEAD
   `b60cd3fe4960e84e5ffb007f747ac43a6063c2c8`
   - `POSTMAIN_REINTEGRATED_ARCHITECTURE_v1.json`
   - `POSTMAIN_REINTEGRATION_RESULT_JA_v1.md`
4. **R2 / PR #466**, exact HEAD
   `4ae4833c103f1cbeb6617be681dab4e183c69aa0`
   - `SELF_MINIMAL_RUNTIME_ARCHITECTURE_v1.md`
   - `SELF_RELAYSELF_MAPPING_v1.json`
5. **R3 / PR #467**, exact HEAD
   `31da772f19dfb447fd5cb9f6b092967e436e334f`
6. **R4 / PR #468**, exact HEAD
   `ac5303dfb98f88de2307405b9550e9ba9663faec`
7. **R5 / PR #470**, exact HEAD
   `826ad01fd2caa8a6a783a1670b4255888f262c0d`
8. **M11 / PR #472**, exact HEAD
   `e6b01717129b5f924e489dd8b89d3ee647d252a1`
   - used only for the current interpretation boundary that MAIN40 40/40 A0
     does not by itself validate the exact role inventory under an
     encoding-permissive baseline.

The exact frozen MAIN40 scientific result is unchanged:

```
MAIN40 = 40
component = 24/24 A0
integrated = 16/16 A0
A0 = 40
A1 = 0
A2 = 0
reconstruction-added stateless adapter = 0
reconstruction-added persistent/stateful coordinator = 0
```

No row below modifies that result.

## Executive reconciliation

No material contradiction was found between the S18 single-transaction
architecture and the current post-MAIN structural architecture.

The strongest bounded conclusion is:

> RelaySelf S1-S18 provides a concrete implementation correspondence for the
> post-MAIN common typed execution substrate, owner-local retained structure,
> typed transformation graph, stateless sequencing, and absence of a required
> persistent central coordinator in this bounded architecture.

The important qualification is that the correspondence contains substantial
**implementation-specific refinement**. In particular, RelaySelf adds an
explicit authority ladder and named integration surfaces needed for safe
software execution. Those additions are not retroactive Paper2 empirical
findings.

## Primary reconciliation table

| Paper2 / post-MAIN structural claim | RelaySelf concrete implementation | Status | Evidence | Interpretation | Limitation |
| --- | --- | --- | --- | --- | --- |
| Common typed execution substrate across heterogeneous capacities | CapabilitySpec/DescriptorSet, typed mechanism outputs, owner state surfaces and EpochPlan form one shared execution fabric | DIRECTLY_INSTANTIATED | R1 #465; R2 #466; S18 #354 | Concrete implementation correspondence for the common-substrate picture | One implementation is not universal validation |
| Typed state access is not semantic ownership | state_scopes expose surfaces while PersistentCognition, IntentCommitment, Skill/Action owners, LearningPreferenceState and HabitRepertoire retain authority | DIRECTLY_INSTANTIATED | R2 state-access invariant; S18 owner matrix | Access metadata and owner authority remain separate | RelaySelf scopes are not one-to-one Grammar-v0 classes |
| Typed transformation/operator interface | OperatorDescriptor distinguishes READ_ONLY / COORDINATION / OWNER_TRANSITION and forbids hidden persistent operator state | DIRECTLY_INSTANTIATED | R2 Operator; S18 descriptor regression | Concrete K-like execution interface without hidden interpreter | Python interface is not the theory role itself |
| Criterion/orientation separate from ownership | COGNITIVE_ORIENTATION and CONTRACT_GUARD are distinct; criteria never mutate state | INSTANTIATED_WITH_REFINEMENT | R2 Criterion; S18 criterion-kind freeze | Preserves criterion separation and adds authority-oriented refinement | Contract-guard category was not measured by MAIN |
| Typed ports and boundary-relative observation | RelayEngine plus Mineflayer I/O; command, WorldConsequence, Action outcome and feedback remain distinct | INSTANTIATED_WITH_REFINEMENT | R1 P/rho-O; R2 Port; S18 WORLD_EXEC/ACTION_OUTCOME | Abstract interface becomes a stricter execution chain | Mineflayer protocol is target-local |
| Stateless temporal ordering | immutable EpochPlan; caller/source owns due cause and exact binding | DIRECTLY_INSTANTIATED | R1 T; R4 #468; S18 scheduler audit | One bounded transaction needs no persistent cognitive scheduler | Multi-epoch scheduling unqualified |
| Optional retained persistent substructure without universal coordinator | owner-local PersistentCognition, LearningPreferenceState, HabitRepertoire and lifecycle owners | INSTANTIATED_WITH_REFINEMENT | R1 optional retained X; M9A; S18 owners | Retention is distributed rather than flattened into SelfState | Owner boundaries are engineering choices |
| Capacity as substrate + retained structure + transformation graph | ATT -> BLF -> CNC -> {PRD -> PLAN, HABIT} | DIRECTLY_INSTANTIATED | R1 synthesis; S18 canonical graph | Concrete correspondence for the post-MAIN compositional formula | Not a theorem of capacity identity |
| Capability composition rather than one-domain-one-module | capabilities compose scopes/operators/criteria/dependencies; integration IDs are not faculties | DIRECTLY_INSTANTIATED | R2 capability composition; S18 taxonomy | Mechanism composition replaces an eight-box architecture | Software capability labels remain conveniences |
| No demonstrated need for universal persistent coordinator | single transaction completes through retained adaptation without persistent central executive | DIRECTLY_INSTANTIATED | M7 integrated 16/16 A0; R1; S18 central-executive audit | Bounded implementation existence result | Not a universal impossibility theorem |
| Sequencing need not become persistent cognition | EpochPlan stateless; ActionSupervisor remains only a typed Action lifecycle/deadline owner | DIRECTLY_INSTANTIATED | R2 Scheduler; R4; S18 | Lifecycle supervision and cognition scheduling remain distinct | Future pacing may require additional runtime structure |
| Cognitive mechanisms distinct from execution/authority integration | ATT/BLF/CNC/PRD/PLAN/LRN/HABIT vs ROUTE/ADMISSION/EXEC_BIND/WORLD_EXEC/ACTION_OUTCOME/FEEDBACK | INSTANTIATED_WITH_REFINEMENT | R1 motifs; S18 capability classes | Sharpens the theory-side distinction in software | Exact taxonomy is not a Paper2 empirical result |
| Exact authority ladder | selection != admission != commitment != binding != proposal != authorization != issue != physical execution != outcome != feedback != retained update | IMPLEMENTATION_SPECIFIC_ADDITION | S18 authority invariants; coarser R2 proposal/authorization separation | Strong semantic refinement discovered in construction | Do not attribute the full ladder to MAIN40 |
| Explicit integration metadata | ROUTE/ADMISSION/EXEC_BIND/WORLD_EXEC/ACTION_OUTCOME/FEEDBACK | IMPLEMENTATION_SPECIFIC_ADDITION | M9A A-state semantics; S18 metadata | A1-style in engineering shape, not MAIN A1 evidence | MAIN remains 40/0/0 |
| System/World separation | ISSUED + exact binding -> Mineflayer command -> WorldConsequence -> existing Action owner | INSTANTIATED_WITH_REFINEMENT | R1 rho/O; R2 observation != belief; S15/S16 frozen in S18 | Adds explicit identity and authority joins to the prior boundary | Concrete protocol is target-specific |
| Stateless transformation vs retained structure | ATT/BLF/CNC/PRD/PLAN stateless; HABIT reads retained repertoire; LRN proposal and retained commit separated | INSTANTIATED_WITH_REFINEMENT | R1 retained X/K distinction; S18 | Concrete examples for retained reusable structure in stateless graph | Paper3 theory not yet performed |
| Forbidden implicit edges | 17 negative edges freeze prohibited ownership/authority shortcuts | IMPLEMENTATION_SPECIFIC_ADDITION | S18 forbidden_implicit_edges; R2 stop conditions | Makes abstract separations executable and auditable | Most are not direct corpus measurements |
| Zero provider/model calls in canonical structured transaction | deterministic trace reaches LearningPreferenceState 4/rev1 with 0 calls | IMPLEMENTATION_SPECIFIC_ADDITION | S18 trace | Demonstrates one model-free structured path | RelaySelf as a whole is not model-free |
| General Present Projection owner | present surface is used, but S18 adds no universal Present owner | NOT_YET_INSTANTIATED | R2 marked Present partial; S18 owners | No contradiction; Present is non-load-bearing here | Broader Present runtime remains outside scope |
| Genuine embodied field execution | live field not run | NOT_TESTED | S18 receipt | No field validation claim | blocker: genuine Minecraft endpoint unavailable |
| Continuous autonomous reentry | learning ends at STOP; no LRN -> ATT edge | NOT_YET_INSTANTIATED | S18 autonomous_reentry | One transaction only | Multi-epoch runtime remains future work |
| Advanced multi-step/learned runtime | multi-step rollout, learned arbitration/admission, habit acquisition, broader belief/concept learning remain unqualified | NOT_YET_INSTANTIATED | S18 known limitations | Current correspondence remains bounded | No silent completion of missing mechanisms |

Counts:

- DIRECTLY_INSTANTIATED = **8**
- INSTANTIATED_WITH_REFINEMENT = **6**
- IMPLEMENTATION_SPECIFIC_ADDITION = **4**
- NOT_YET_INSTANTIATED = **3**
- NOT_TESTED = **1**
- APPARENT_TENSION = **0**

## 1. Common execution substrate

R1 described a common substrate in Grammar-v0 terms and R2 translated it to
five execution-interface families:

1. state access;
2. operator;
3. criterion;
4. port;
5. scheduler.

S18 does not map every Grammar-v0 role one-to-one onto a Python class. It does
something more conservative: it instantiates a software fabric that preserves
the corresponding distinctions.

### State access

`CapabilitySpec.state_scopes` describes what a capability may access. It does
not establish ownership.

This distinction is directly preserved in S18.

### Operator

Operators are explicit typed transformations with declared effects.
S18 additionally freezes absence of hidden persistent operator state.

### Criterion

R2's criterion separation survives, but S18 adds a useful engineering
refinement:

```
COGNITIVE_ORIENTATION
!=
CONTRACT_GUARD
```

That refinement should not be projected backward into MAIN40.

### Port

The R2 P_in/P_out idea becomes concrete in RelayEngine and Mineflayer-facing
interfaces. S18 further separates physical command construction, external
consequence, Action closure and learning interpretation.

### Scheduler

EpochPlan is immutable and stateless. It does not own goals, beliefs, intent,
world state or a hidden trigger loop.

Therefore the five-interface blueprint is **directly instantiated as an
execution substrate**, with criterion/port semantics refined by the concrete
implementation.

## 2. Retained structure

Paper2/M9A explicitly distinguishes source-defined persistent structure from a
reconstruction-added persistent coordinator.

S18 exhibits the same structural distinction in engineered form:

- `PersistentCognition` retains Identity / Memory / appraisal dispositions;
- `IntentCommitment` retains current Intent/history;
- `SkillExecution` retains lifecycle lineage;
- `ActionLifecycle` and `ActionSupervisor` retain Action lifecycle,
  deadlines and outcome closure;
- `LearningPreferenceState` retains owner-local learned preference;
- `HabitRepertoire` retains owner-local habit rules.

None of these objects becomes a universal cross-domain SelfState.

Thus:

```
retained semantic/lifecycle state
!=
persistent universal coordinator
```

This is a strong implementation correspondence, not a claim that these exact
owners are theory primitives.

## 3. Transformation graph

The cognitive part of S18 is:

```
ATT -> BLF -> CNC
             +-> PRD -> PLAN --+
             |                 |
             +-----> HABIT ----+
```

This concretely fits the R1 post-MAIN expression:

```
cognitive capacity
≈ common execution substrate
+ retained structure
+ typed transformation graph
```

The symbol here remains an implementation correspondence, not a theorem or
identity claim.

## 4. Canonical correspondence graph

Legend:

- `--cog-->` cognitive transformation/orientation
- `==retained==>` retained-structure read/update
- `--int-->` integration interface
- `--guard-->` authority contract/guard
- `--owner-->` semantic/lifecycle owner transition
- `--env-->` environment boundary
- `-X->` forbidden automatic edge

```text
ATT --cog--> BLF --cog--> CNC
                         | \
                         |  +--cog--> HABIT <==retained== HabitRepertoire
                         |
                         +--cog--> PRD --cog--> PLAN
                                      PLAN + HABIT
                                           |
                                         --int-->
                                           ROUTE
                                             |
                                         --guard-->
                                         ADMISSION
                                             |
                                         --guard-->
                                         EXEC_BIND
                                           /   \
                                   --owner-->  --owner-->
                                  SkillExec   ActionLifecycle
                                                   |
                                              authorization
                                                   |
                                            ActionSupervisor
                                                   |
                                                ISSUED
                                                   |
                                                --env-->
                                              WORLD_EXEC
                                                   |
                                            WorldConsequence
                                                   |
                                                --int-->
                                           ACTION_OUTCOME
                                                   |
                                             --owner--> ActionSupervisor terminal
                                                   |
                                                --int-->
                                                FEEDBACK
                                                   |
                                                --cog-->
                                                  LRN
                                                   |
                         explicit LearningUpdateAuthority
                                                   |
                                            ==retained==>
                                      LearningPreferenceState
                                                   |
                                                  STOP

LearningPreferenceState -X-> automatic next ATT / next epoch
```

This graph deliberately keeps cognitive mechanism, retained structure,
integration interface, authority transition, and environment boundary
different.

## 5. Coordinator question

The bounded conclusion is:

> The RelaySelf S1-S18 implementation demonstrates that the frozen
> single-transaction cognitive-action-learning architecture can be constructed
> without introducing a persistent central executive or a persistent cognitive
> scheduler.

The required bound follows immediately:

> This is an implementation existence result for the present architecture, not
> a universal impossibility result for centralized coordination.

This is consistent with M7/R1. It is not an independent re-test of the
scientific corpus.

## 6. A0 / A1 / A2 reconciliation

M9A defines:

- A0: source-defined mechanisms plus frozen Grammar/substrate are sufficient;
- A1: fidelity additionally requires reconstruction-added stateless typed
  interface / sequencing / translation;
- A2: fidelity additionally requires a reconstruction-added persistent
  coordination mechanism.

Therefore the MAIN40 result remains exactly:

```
A0 = 40
A1 = 0
A2 = 0
integrated = 16/16 A0
```

RelaySelf asks a different engineering question.

```
MAIN A0:
Do the scientific mechanisms require an added load-bearing
coordination mechanism under the frozen reconstruction?

RelaySelf integration metadata:
What explicit software interfaces are useful for safely implementing
ownership, authority, sequencing and environment I/O?
```

ROUTE, ADMISSION, EXEC_BIND, WORLD_EXEC, ACTION_OUTCOME and FEEDBACK are
**A1-style in implementation shape** because they are largely typed/stateless
interface or authority structure.

They are **not MAIN A1 cases**.

No scientific paper is reclassified by their existence.

## 7. Authority as implementation refinement

Paper2/post-MAIN already motivated:

- typed interfaces;
- source/world boundary;
- explicit state access;
- stateless sequencing;
- separation of proposal from external execution.

S18 makes that much stronger:

```
selection
!= admission
!= commitment
!= binding
!= proposal
!= authorization
!= issue
!= physical execution
!= Action outcome
!= LearningFeedback
!= retained update
```

The exact ladder should be recorded as an
`IMPLEMENTATION_SPECIFIC_ADDITION`.

It is scientifically valuable precisely because implementation exposed a
semantic distinction that Paper2 did not directly measure.

## 8. System / World boundary

The concrete path is:

```
ISSUED Action
+ exact ExecutionBindingResult
-> Mineflayer command
-> WorldConsequence
-> ACTION_OUTCOME interpretation
-> existing ActionSupervisor terminal owner
```

Two critical inequalities remain explicit:

```
Action authority != physical action semantics
WorldConsequence != Belief != LearningFeedback
```

This strongly corresponds to the R1/R2 P/rho-O and external-evidence
separation, while adding target-local exact identity joins.

## 9. Stateless vs retained mechanisms

S18 provides the following concrete partition:

```
ATT   stateless
BLF   stateless
CNC   stateless
PRD   stateless
PLAN  stateless

HABIT = retained HabitRepertoire + stateless selection
LRN   = stateless/pure proposal + explicit authority + retained commit
```

This is a particularly clean implementation correspondence for the Paper2
distinction between executable transformation and retained reusable structure.

## 10. Negative-edge correspondence

S18 freezes 17 implicit-edge prohibitions.

### Directly implied by the post-MAIN structural separation

The strongest direct cases are:

- CNC -> World truth;
- WorldConsequence -> Memory;
- WorldConsequence -> Belief.

These follow from the post-MAIN insistence that boundary-relative observation
and external evidence are not silently identical to internal retained state or
representation.

### Engineering refinements

The following are best treated as software-semantic refinements:

- ATT -> belief mutation;
- BLF -> Memory write;
- PRD -> plan commitment;
- PLAN -> Current Intent;
- PLAN -> Action proposal;
- HABIT -> Action execution;
- HABIT -> LearningFeedback;
- ROUTE -> Intent mutation;
- ADMISSION -> Skill start;
- EXEC_BIND -> authorization;
- WORLD_EXEC -> LearningFeedback;
- ACTION_OUTCOME -> LearningFeedback without explicit FEEDBACK criterion;
- FEEDBACK -> retained update without LRN authority.

They make the abstract structural separation executable, but Paper2 did not
empirically establish these exact prohibitions.

### Future runtime question

```
LRN -> automatic next epoch
```

is deliberately absent in S18. Whether a future multi-epoch architecture
requires additional pacing/reentry structure is a future runtime question, not
a Paper2 result.

## 11. Retained adaptation and Paper3 handoff

This reconciliation does **not** start Paper3.

It records only bounded implementation-generated hypotheses:

1. retention can be owner-local rather than globally centralized;
2. read/reuse can be separated from governed update authority;
3. provenance and authority can be explicit parts of retained-state
   transitions;
4. retained structures can participate in a largely stateless transformation
   graph without becoming a universal coordinator.

These are design observations/hypotheses for future Paper3 work, not Paper3
results.

## 12. Provider/model boundary

The canonical S18 structured deterministic transaction reaches retained
adaptation with:

```
provider/model calls = 0
```

This does **not** show that RelaySelf as a whole is model-free.

TALK / RelayEngine and future model-assisted mechanisms remain available.

## 13. Live-field limitation

Frozen exactly:

```
LIVE_FIELD_STATUS = BLOCKED_NOT_RUN
BLOCKER = genuine Minecraft endpoint unavailable
```

The evidence class is:

```
DETERMINISTIC_TEST_APPARATUS_TRACE
```

Therefore this reconciliation uses the phrase:

> deterministic implementation-apparatus qualification

and does not claim:

- genuine embodied execution;
- genuine Minecraft learning loop;
- empirical field validation.

## 14. Autonomy limitation

Frozen exactly:

```
AUTONOMOUS_REENTRY = NOT_IMPLEMENTED
CONTINUOUS_MULTI_EPOCH_OPERATION = NOT_QUALIFIED
```

The demonstrated architecture is:

```
one bounded transaction
```

not:

```
continuous autonomous cognition
```

Future work must keep these questions separate:

```
single-transaction architecture
vs
multi-epoch runtime architecture
```

## 15. Final reconciliation

No `APPARENT_TENSION` is recorded in this R6 comparison.

The S18 implementation:

- directly instantiates the common typed execution substrate in bounded
  software form;
- refines retained structure into explicit owner-local state;
- realizes a typed transformation graph across cognitive mechanisms;
- adds explicit integration and authority layers without turning them into
  cognitive faculties;
- completes one cognitive-action-learning transaction without a persistent
  central executive or persistent cognitive scheduler;
- preserves a strict System/World and outcome/feedback/update separation.

The strongest licensed terminal interpretation is therefore:

```
POSTMAIN_SELF_S18_RECONCILED_WITH_PAPER2_STRUCTURAL_ARCHITECTURE_WITH_IMPLEMENTATION_SPECIFIC_AUTHORITY_REFINEMENTS
```

This is a reconciliation result, not a new MAIN result.
