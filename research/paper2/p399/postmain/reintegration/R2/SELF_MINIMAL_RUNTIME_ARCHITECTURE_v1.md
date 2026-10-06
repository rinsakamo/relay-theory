# P399 post-MAIN — Minimal RelaySelf execution blueprint v1

## Status

This is a **post-MAIN engineering/theoretical blueprint** derived from the frozen MAIN40 reintegration in PR #465.

It does not modify the MAIN40 adjudication and does not claim that the proposed runtime is empirically superior.

Frozen upstream authority:

- M7 exact HEAD: `48b2cf3c627e030e7131af485206b0013d7e02f1`
- post-MAIN reintegration exact parent HEAD: `b60cd3fe4960e84e5ffb007f747ac43a6063c2c8`
- MAIN40: 40/40 A0
- component arm: 24/24 A0
- integrated arm: 16/16 A0
- reconstruction-added stateless adapters: 0
- reconstruction-added persistent/stateful coordinators: 0

## Design objective

Translate the reintegrated substrate into the smallest implementation shape that can be used by RelaySelf without adding a universal central executive.

The execution substrate is described by five interfaces:

1. state access
2. operator
3. criterion
4. port
5. scheduler

These are **execution interfaces, not five new semantic owners**.

RelaySelf's existing semantic ownership remains authoritative:

- Persistent Cognition owns durable cognition.
- Present Projection owns current transient projection.
- IntentCommitment owns Current Intent commitment state.
- SkillExecution owns one skill execution lifecycle.
- ActionLifecycle owns one primitive action lifecycle.
- Environment/world truth remains external.

## 1. State access — typed state fabric, not a generic mutable store

Do not introduce one universal dictionary-like State Store that becomes the owner of all cognition.

Instead expose a typed state-access fabric over existing owners.

Required scopes:

| Scope | Examples | Persistence |
| --- | --- | --- |
| durable | Memory, Belief, learned reusable structure, capability estimates | governed persistent |
| present | Situation Model, Attention State, Current Appraisal | transient/reprojectable |
| execution | Current Intent, SkillExecution, ActionLifecycle | lifecycle-owned |
| operator-local | planner frontier, accumulator, recurrent state, temporary hypothesis | source/mechanism-defined |
| external evidence | observations, consequences, attested body/world facts | external authority; not Self-owned truth |

Invariant:

```
state access interface != semantic ownership
```

A capability may read several scopes but may write only through the owner authorized for the target state.

## 2. Operator

An Operator is a typed transformation over declared inputs and outputs.

Minimal contract:

```
OperatorSpec:
  id
  reads
  writes
  preconditions
  deterministic_or_cognitive
  apply(...)
```

Examples:

- Bayesian belief update
- memory retrieval
- saliency/attention gate
- value update
- policy/action selection
- prediction rollout
- planning expansion
- learned skill transform
- feedback integration

An Operator must not keep hidden persistent state. If persistence matters, that state must be explicit in one of the state scopes above.

## 3. Criterion

A Criterion orients or filters alternatives without becoming another state owner.

Minimal contract:

```
CriterionSpec:
  id
  reads
  evaluate(candidate_or_state) -> score / ordering / admissibility
```

Examples:

- posterior probability
- expected value
- prediction error
- control error
- novelty
- relevance/priority
- threshold
- viability constraint

A Criterion may read source-defined persistent state, but cannot silently mutate it.

## 4. Port

A Port is an explicit typed boundary operation.

Two common directions:

```
P_in:
  Observation / evidence / reward / feedback / explicit write request
  -> Self-side processing

P_out:
  query / prediction / retrieval / expression / action proposal
  -> caller or external boundary
```

Important:

```
P_out action proposal != Action authorization != external execution
P_in observation != belief
```

RelayEngine is a cognition execution port, not a state owner.

Environment adapters are boundary ports, not World-truth owners inside RelaySelf.

## 5. Scheduler

The Scheduler provides ordering and due-work selection only.

It must not become a persistent coordinator.

Minimal responsibility:

```
available work
+ deadlines owned by source lifecycles
+ explicit event/projection triggers
+ enabled capability graph
-> ordered due operators
```

The Scheduler owns no hidden goals, beliefs, memory, intent, skill state, world model, or universal executive state.

Persistent scheduling facts, if ever required, must be owned by the lifecycle or semantic object that makes them meaningful.

This preserves the MAIN40 result:

```
coordination
=
typed dependency
+ temporal order
+ gating
+ feedback
```

without inferring a ninth cognitive module.

## Execution epoch

A minimal embodied epoch is:

```
1. ingest P_in observations/evidence
2. validate provenance/authority
3. update boundary-local evidence snapshot
4. reproject Present as required
5. compile enabled capabilities into due Operators
6. service due lifecycle deadlines
7. execute deterministic Operators first
8. evaluate Criteria
9. request RelayEngine cognition only for unresolved admitted work
10. produce P_out query/expression/action proposal
11. preserve Action authorization boundary
12. observe consequence through P_in
13. perform governed state update / optional Experience Integration
```

No LLM-per-tick loop is implied.

## Capability composition

A capability is a **composition descriptor**, not a new owner.

```
Capability =
required state scopes
+ Operators
+ Criteria
+ Ports
+ scheduling triggers
```

Enabling a capability activates its routes/operators. Disabling it does not delete durable state.

### Attention

```
present/boundary state
+ relevance/priority Criterion
+ gating/routing Operator
-> selected projection / downstream input
```

### Belief

```
durable or present belief state
+ evidence P_in
+ inference/update Operator
+ posterior Criterion
-> updated belief / query
```

### Concept

```
retained representation
+ composition/classification Operator
+ fit/predictive Criterion
-> reusable structured representation
```

### Control

```
Present + Current Intent + capability/body constraints
+ value/viability Criterion
+ control/selection Operator
-> Skill/Action path
```

### Learning

```
provenance-bearing feedback
+ learning Criterion/objective
+ governed update Operator
-> retained reusable structure
```

Learning remains OFF by default unless the target owner and update authority are explicit.

### Memory

```
governed write
+ retained Memory
+ retrieval Criterion
+ retrieval Operator
-> Present/cognition input
```

### Prediction

```
current/retained model state
+ rollout/inference Operator
+ expected-value/evidence Criterion
-> predicted trace / action valuation
```

### Skill

```
Current Intent
+ reusable Skill definition
+ execution-local state
+ feedback/control Operator
-> SkillExecution -> Action proposals
```

## Derived application capabilities

The following are useful RelaySelf application profiles but are not promoted to new Grammar primitives.

### Planning

```
prediction Operator
+ iterative T ordering
+ Criterion
+ temporary planner-local X
-> selected plan/action candidate
```

Planner frontier/search state is operator-local unless a concrete source requires persistence.

### Habit

```
retained cue/action or state/policy structure
+ direct selection Operator
+ Criterion
-> action/skill candidate
```

Habit is not allowed to bypass Action authorization or consequence monitoring.

### TALK

```
Present/Persistent projection
+ OPEN cognition Operator
+ expression Criterion/policy
+ expression P_out
-> transient outward expression
```

TALK output does not establish World truth, durable Memory, Current Intent, or Action authorization.

## ON/OFF semantics

Capability toggles control execution availability, not ontology.

```
OFF:
  operator routes unavailable
  state remains owned and preserved
  no implicit deletion or forgetting

ON:
  routes may be scheduled when preconditions/triggers hold
  all normal authority/provenance boundaries remain active
```

This allows agentization by composition rather than by changing one monolithic controller.

## Suggested profiles

### Observer

- Attention: ON
- Belief: ON
- Concept: ON
- Memory: optional
- Control/Skill: OFF
- TALK: optional

### Conversational Self

- Memory: ON
- Belief: ON
- Concept: ON
- TALK: ON
- Attention: ON
- Control/Skill: OFF unless external tools/actions are admitted

### Reactive embodied Self

- Attention: ON
- Memory: ON
- Control: ON
- Skill: ON
- Belief: minimal/ON
- Prediction/Planning: optional
- Learning/Habit: OFF initially

### Deliberative embodied Self

Reactive profile plus:

- Prediction: ON
- Planning: ON

### Adaptive embodied Self

Deliberative profile plus governed:

- Learning: ON
- Habit: ON

Adaptive mode requires independent validation of update authority and rollback/invalidation behavior.

## Mapping to current RelaySelf

The blueprint is deliberately compatible with the current bootstrap rather than replacing it.

| Blueprint concept | Current RelaySelf seam | Status |
| --- | --- | --- |
| durable state scope | `PersistentCognition` | implemented, bounded |
| Present scope | architectural Present Projection | partially implemented across experiment-local projections |
| execution state | `IntentCommitment`, `SkillExecution`, `ActionLifecycle` | implemented, bounded |
| cognition port | `RelayEngine` BOUNDED/THINK/OPEN | implemented, bounded |
| environment port | Mineflayer adapter / environment seams | implemented for qualified bounded slice |
| scheduling | `coordinate_decision_epoch` | minimal admitted epoch coordinator |
| Memory capability | `PersistentCognition.memories` + explicit retrieval consumers | partial |
| Skill capability | `SkillExecution` + experiment-local selection/control | partial |
| Control capability | Intent/Skill/Action contracts | partial |
| TALK | `RelayEngine.open` | execution seam implemented; general expression policy not owned |
| Belief | ontology exists; general executable owner absent | design gap |
| Concept | ontology/reusable representation not general executable owner | design gap |
| Prediction/Planning | experiment/model-specific only | design gap |
| Learning/Habit | experiment-local/compiled cognition work only | deliberately not general runtime owner |

## Minimal implementation sequence for RelaySelf

The next implementation should remain additive and evidence-driven.

### Slice S1 — declarative capability plan

Add immutable capability metadata only:

- capability id
- required state scopes
- operator ids
- criterion ids
- port ids
- dependencies
- enabled flag

No new semantic state owner and no execution behavior change.

### Slice S2 — operator/criterion contracts around existing concrete paths

Wrap already-existing concrete mechanisms first:

- Memory retrieval
- Current Intent / Skill selection seam
- Action proposal path
- RelayEngine OPEN/BOUNDED requests

Do not invent generic implementations for missing capabilities.

### Slice S3 — stateless epoch planner

Extend the admitted decision epoch coordinator so it can order due declared Operators while preserving:

- deadline-first Action supervision
- caller/source-owned state
- exactly-once admitted cognition calls
- no hidden scheduler persistence

### Slice S4 — existing-capability profiles

Qualify capability toggles for already-supported paths:

- MEM
- CTL
- SKL
- TALK

### Slice S5 — new cognitive mechanisms

Only then add concrete ATT / BLF / CNC / PRD mechanisms one at a time with independent tests.

LRN/HABIT remain later because durable self-modification carries stronger authority and invalidation requirements.

## Falsification / stop conditions

Reject this blueprint if implementation requires any of the following merely to make the architecture work:

- a hidden persistent central coordinator;
- a universal mutable state dictionary that bypasses semantic owners;
- a Scheduler-owned world model, goal, belief, or intent;
- opaque operator state not exposed to provenance/ownership;
- Action execution bypassing existing authorization;
- capability OFF deleting state;
- TALK output automatically becoming belief or memory;
- Learning writing durable state without owner-specific authority.

Such a requirement would be evidence that the post-MAIN minimal reintegration is insufficient for RelaySelf engineering and should be recorded rather than hidden.
