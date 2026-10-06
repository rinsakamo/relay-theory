# P399 post-MAIN R5 — RelaySelf S4 qualification handoff

RelaySelf S4 is qualified on exact HEAD `5cc6b1b3cdcbafe3ccdc86d96d4de54e1cc8a302` in Draft PR #340.

The exact CI run `37404709146` passed:

```
repository-contracts  SUCCESS
pytest                SUCCESS
lint                  SUCCESS
mineflayer-adapter    SUCCESS
```

## Qualified bounded profiles

The following existing-mechanism profiles are now exercised end to end through the S3 stateless epoch-plan substrate:

```
MEM
CTL
CTL + SKL
TALK
MEM + CTL + SKL
MEM + TALK
```

No ATT / BLF / CNC / PRD / PLAN / LRN / HABIT mechanism is inferred or implemented by this qualification.

## Concrete seams

```
MEM
  -> PersistentCognition.retain_memory

CTL
  -> RelayEngine.__call__ on a bounded request

SKL
  -> SkillExecution.start
  -> ActionLifecycle.propose

TALK
  -> RelayEngine.open
```

These remain owner-local seams. S4 does not promote the composition layer into a new owner.

## Positive qualification

The executable tests demonstrate:

- governed Memory retention through the PersistentCognition owner;
- one bounded provider call for the CTL profile when THINK is disabled;
- one OPEN provider call for the TALK profile;
- Skill start preserves its actual Current Intent association;
- Action proposal preserves both Skill execution and Current Intent identity;
- MEM + TALK executes the owner transition before the final cognition step.

## Negative authority qualification

The important negative result is equally strong within this bounded implementation scope.

```
CTL + SKL
  -> ActionState.PROPOSED
  -> NOT AUTHORIZED
  -> NOT ISSUED
```

Capability composition therefore does not acquire Action authority merely because Skill and Control are enabled together.

Likewise TALK output remains transient and does not produce Action authority.

## Toggle isolation

The same MEM + TALK due-work surface was tested with one capability disabled at a time.

### MEM OFF / TALK ON

```
mem.retain           -> SUPPRESSED
talk.open_cognition  -> EXECUTED
existing Memory      -> PRESERVED
OPEN provider calls  -> 1
```

### MEM ON / TALK OFF

```
mem.retain           -> EXECUTED
talk.open_cognition  -> SUPPRESSED
provider calls       -> 0
```

This is direct executable evidence for the engineering interpretation:

> capability OFF changes route admission, not ontology or retained state.

It also shows that disabling one route does not globally disable the epoch.

## Current architecture status

The bounded implementation chain is now:

```
CapabilitySpec / CapabilityPlan
        ↓
Operator / Criterion descriptors
        ↓
source-owned due work
        ↓
explicit concrete bindings
        ↓
immutable EpochPlan
        ↓
deadline-first execution
        ↓
selective capability route effect
```

while still preserving:

```
no universal mutable State Store
no persistent Scheduler
no central executive state
no dynamic descriptor import
no generic hidden dispatch
no LLM-per-tick loop
```

## S5 boundary

S4 completes qualification of the already-existing MEM / CTL / SKL / TALK substrate.

The next slice may add one genuinely new cognitive mechanism at a time.

The conservative sequence remains:

```
ATT
-> BLF
-> CNC
-> PRD
-> PLAN
-> LRN
-> HABIT
```

ATT is the recommended first candidate because a bounded attention/gating mechanism can be introduced without immediately granting durable self-modification or action authority.

Any new capability must keep explicit state ownership and must distinguish a real cognitive orientation criterion from a mere contract guard.
