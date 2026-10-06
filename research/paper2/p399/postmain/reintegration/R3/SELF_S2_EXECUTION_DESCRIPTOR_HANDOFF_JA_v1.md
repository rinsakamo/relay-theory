# P399 post-MAIN R3 — RelaySelf S2 handoff

RelaySelf S2 is now implemented and validated on exact HEAD `40b83d9012dc1bcc8e1dc2c74664a7d0e0ffb172` in Draft PR #338.

S2 maps the already-existing MEM / CTL / SKL / TALK runtime seams into non-executing `OperatorDescriptor` / `CriterionDescriptor` metadata. The descriptors contain no callable bindings and perform no dispatch.

The current mapped seams are:

```
MEM  -> PersistentCognition.retain_memory

CTL  -> coordinate_decision_epoch
     -> RelayEngine.__call__

SKL  -> SkillExecution.start
     -> ActionLifecycle.propose

TALK -> RelayEngine.open
```

All current S2 criteria are explicitly classified as **contract guards**, not as newly invented cognitive-orientation objectives. This is important: the research-level Q role is not backfilled into RelaySelf merely because the post-MAIN architecture contains a Criterion interface.

The exact S2 CI run `37399855964` passed repository contracts, pytest, and lint.

No new semantic owner, generic mutable State Store, hidden persistent operator state, dispatcher, or persistent Scheduler was added.

## Consequence for S3

S3 may now compile enabled capability metadata into an ordered epoch plan, but must remain stateless.

The admissible shape is:

```
CapabilityPlan
+ explicit DescriptorSet
+ caller-supplied concrete bindings
+ source-owned deadlines / triggers
-> immutable ordered EpochPlan
```

The plan may order work. It must not acquire cognition or state merely by existing.

In particular:

```
implementation_ref string != executable binding
EpochPlan             != Scheduler state owner
order                  != semantic authority
```

Action supervision remains deadline-first, and model cognition remains an explicitly admitted call rather than a tick-level loop.
