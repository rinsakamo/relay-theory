# RelayTheory

**RelayTheory** is an implementation-independent research project for reducing cognitive and agent-like systems to smaller relational primitives.

Its central question is not merely how to implement concepts such as cognition, action, skill, memory, emotion, or ownership, but:

> **Which of those concepts actually need to exist as primitives?**

RelayTheory studies whether apparently high-level structures can instead be derived from grounded interaction among **Self**, **World**, their **Boundary**, and observable **Change**.

## Current research direction

The current direction is intentionally provisional. Concepts such as:

- Skill
- Action
- Perception
- Cognition
- Ownership
- Emotion-like structure

may not require independent primitive semantics.

A current candidate basis includes:

```text
Self
World
Boundary
Relation
Interaction
Change
Grounding
Authority
Trace
```

These are **candidate primitives**, not a frozen ontology.

A motivating reduction is:

```text
Skill
  ↓
Action
  ↓
Effect
  ↓
Self–World interaction producing change
```

Likewise, ownership may be derivable from grounded and authorized provenance rather than stored as an independent primitive:

```text
Ownership
  ↓
Authority + Grounding + Trace
```

And familiar cognitive categories may describe interaction topology rather than separate fundamental mechanisms:

```text
World ↔ Self   perception-like / grounding interaction
Self  ↔ Self   cognition-like interaction
Self  ↔ World  outward / action-like interaction
```

None of these reductions are accepted merely because they are simpler. They must survive falsification.

## Research rule

RelayTheory prefers **reduction over premature ontology**.

A concept should not be promoted to a primitive merely because it is intuitive, useful in human language, or convenient to implement.

The goal is not to eliminate useful high-level language. The goal is to determine whether that language describes fundamental structure or recurring structure.

## Grand Null

A useful default null hypothesis is:

> High-level concepts such as Skill, Action, Cognition, Perception, Emotion, and Ownership require independent primitive semantics and cannot be recovered from grounded Self–World interaction and change alone.

Individual hypotheses should define narrower nulls and explicit discriminating evidence.

## Relationship to Relay projects

RelayTheory is independent of any particular implementation.

```text
              RelayTheory
                  |
          hypotheses / constraints
             /            \
            v              v
       RelaySelf         RelayLM
       embodied          cognitive
       experiments       runtime
```

RelaySelf and RelayLM may provide experiments, counterexamples, implementation probes, and formalization targets. Neither repository defines RelayTheory's ontology.

Historical material in the former `relay-theory` lane of `rinsakamo/relay-lm` is research provenance, not current authority for this repository.

## Repository authority

The current `main` branch of this repository is the repository-local authority for RelayTheory.

Old prompts, handoff text, branches, issues, experiments, and external implementations are evidence or history. They do not override current repository authority.

See:

- [Ontology](docs/ontology.md)
- [Hypotheses](docs/hypotheses.md)
- [Research method](docs/method.md)
- [Repository authority](.ai/README.md)

## Status

RelayTheory is experimental.

Definitions are expected to be deleted, merged, renamed, or reduced when a smaller explanation survives available evidence.

**Breaking the ontology is progress.**
