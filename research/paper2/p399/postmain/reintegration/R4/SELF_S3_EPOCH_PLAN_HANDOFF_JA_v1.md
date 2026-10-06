# P399 post-MAIN R4 — RelaySelf S3 handoff

RelaySelf S3 is implemented and validated on exact HEAD `303dbc7f6fb6e7ea8edb3ce60636079b909ac048` in Draft PR #339.

This is the first implementation slice in which capability ON/OFF selection changes admitted runtime work.

The implemented shape is:

```
CapabilityPlan
+ CapabilityDescriptorSet
+ source/caller-owned due work
+ explicit concrete bindings
        ↓
immutable EpochPlan
        ↓
coordinate_planned_epoch
        ↓
existing coordinate_decision_epoch
```

No persistent Scheduler or central executive was introduced.

## ON/OFF semantics now executable

For an already-declared capability:

```
MEM ON
+ due mem.retain
+ exact explicit binding
-> scheduled and executed

MEM OFF
+ same due mem.retain
-> recorded as suppressed
-> not executed
```

The OFF transition changes route availability only. It does not delete Memory or mutate any other semantic owner.

## Ordering and cognition constraints

The existing Action supervision rule remains first:

```
due Action supervision
    BEFORE
planned inner capability work
```

Within the plan:

- caller/source due order is preserved;
- the outer coordination operator cannot be scheduled recursively;
- at most one cognition call is admitted per epoch;
- cognition must be the final inner step;
- cognition requires an explicit `CognitionInvocation(request, runner)`;
- a deterministic owner-transition binding must return `None` and cannot smuggle a cognition request.

Descriptor `implementation_ref` strings remain audit-only and are never auto-imported as executable bindings.

## Evidence

RelaySelf CI run `37400393408` on the exact S3 HEAD passed:

```
repository-contracts  SUCCESS
pytest                SUCCESS
lint                  SUCCESS
mineflayer-adapter    SUCCESS
```

The S3 test surface also exercises:

- capability-OFF suppression;
- exact binding matching;
- unknown-operator rejection;
- nested-coordination rejection;
- multi-cognition rejection;
- cognition-last ordering;
- deadline-first Action supervision;
- explicit existing Memory owner transition;
- exactly-once cognition runner invocation;
- prevention of cognition smuggling through deterministic work.

## Interpretation

The post-MAIN reintegration can now be expressed in RelaySelf as an actual compositional execution mechanism without introducing another persistent executive state.

The strongest engineering statement is:

> A bounded set of already-existing RelaySelf mechanisms can be enabled, disabled, ordered, and executed through stateless composition metadata plus explicit owner-local bindings.

This remains an engineering handoff, not a new MAIN scientific claim.

## S4 boundary

S4 should qualify concrete already-supported profiles rather than add new cognitive mechanisms.

Priority profiles:

```
MEM
CTL
CTL + SKL
TALK
MEM + CTL + SKL
MEM + TALK
```

The key test is no longer merely that the planner compiles. It is that toggling one capability changes only its admitted route while preserving ownership, Action authority, consequence semantics, and bounded cognition-call behavior.
