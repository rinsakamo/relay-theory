# Ontology

RelayTheory does not begin from a fixed ontology.

This document tracks the **smallest currently useful candidate basis**, the formal parameters used to evaluate it, and the high-level concepts that may be derivable from it. Every entry is provisional.

## Rule

A name is not a primitive because it is intuitive, implementation-friendly, or common in cognitive language.

Prefer a smaller structural account when it preserves the distinctions required by evidence.

A reduction into a generic Relation / State / Transition label is not sufficient if the deleted semantics are merely stored under a new name.

## Evaluation parameters

The following are part of the current formal scaffold, not current ontology primitives.

### Focal locus / center

Self-relative analysis is evaluated relative to an explicit focal locus (L) inside an ambient scope (U).

The focal locus is an **index / evaluation parameter**. Choosing (L) does not by itself assert that (L) is a Self.

This distinction is required by #5:

- bare symmetric structure cannot in general select one unique Self;
- multi-agent cases require different Self-relative evaluations over the same underlying structure;
- genuinely de-se / indexical claims require a center;
- the center can be represented without a global primitive Self entity type.

Whether a focal locus exhibits **Self-like organization** remains a derived-classification question under #1.

### Ambient scope

(U) denotes the domain currently under analysis.

Its selection is scope-relative formal machinery. RelayTheory does not currently treat “the universe under analysis” as an additional agency primitive.

## Candidate primitives

The following remain research candidates, not settled fundamentals.

### Relation

A structured dependency or connection among states or entities.

This candidate is under direct pressure in #10: generic Relation may belong to the formal substrate rather than the ontology.

Relations must not carry arbitrary high-level semantic labels merely to preserve a rejected primitive.

### Interaction

A coupling or dependence through which components participate in possible transitions.

Interaction is intentionally lower-level than Action.

It is under active reduction in #6, including whether interaction-like structure can be derived from counterfactual dependence under explicit model classes.

### Change

A difference between relevant configurations, states, or relations across an ordering / transition.

Change is intentionally descriptive before it is agentive.

It is under active reduction in #6 because a sufficiently explicit transition account may make Change derivable.

### Grounding

The traceable connection between a representation / relation and the state, observation, body interface, memory, or other source that constrains it.

Grounding is descriptive and must not be identified with Authority merely because both connect sources to state.

Its primitive status is under active reduction in #7.

### Authority

The rule or constraint determining which source may establish, revise, validate, or accept a state or relation.

Authority is not synonymous with grounding, causal authorship, control, or ownership.

Its primitive status is under active reduction in #7.

### Trace

Provenance sufficient to connect realized changes, grounding sources, authority transitions, and intermediate interactions.

Trace is under strong pressure in #6 because realized traces can be represented as paths through richer transition structure and are insufficient by themselves to identify several agency distinctions.

## Conditionally derived structural terms

### World

For ambient scope (U) and focal locus (L):

```text
World(U,L) := U \ L
```

World-as-Self-relative exterior therefore carries no independent partition information once the scope and center are fixed.

If future evidence requires additional World semantics beyond relative exterior, that additional content must be stated separately.

### Boundary

For a relevant relation (R), Boundary is provisionally the cut crossing the focal locus and its exterior:

```text
Boundary_R(U,L)
  := R-crossings between L and U\L
```

Boundary-as-interface is therefore conditionally derived.

Privileged grounding, embodiment, authority, ownership, or other semantics must not be hidden inside Boundary; each must be tested independently.

### Self-like organization

“Self” is no longer treated here as one undifferentiated primitive question.

The current structural result from #5 is:

- a center / locus is required for Self-relative evaluation;
- the center is an evaluation parameter, not by itself a Selfhood claim;
- no prior `Eligible(Self)` predicate has been shown necessary;
- which organization warrants a Self-like description remains unresolved.

A future Self-like classification must therefore be derived from independently testable lower-level organization or survive as a narrower primitive only after those reductions fail.

## Derived agency candidates

The following terms are useful descriptions but are **not currently primitive**.

### Perception

Candidate reduction:

> Exterior-to-locus grounded dependence / interaction that modifies locus-accessible state.

A realized update alone is insufficient. The reduction must distinguish a channel that is sensitive to exterior state from replay / injection that happens to produce the same observed update.

### Cognition

Candidate reduction:

> Locus-internal dependence / interaction that transforms locus-accessible relations, representations, or choice structure.

This definition is provisional. Mere internal physical change is insufficient if it lacks the relevant causal / relational role.

### Action

Candidate reduction:

> A locus-to-exterior interaction/change whose relevant outward contribution is attributable, authorized, and traceable to the focal locus.

A realized outward change alone is insufficient. Action-like attribution may require counterfactual dependence on internal selection rather than a primitive Action flag.

### Ownership

Candidate reduction:

> A family of attributions currently under decomposition, including causal authorship, control/revision authority, focal-locus incorporation, and normative/social title.

The previous shorthand `Authority + Grounding + Trace` is not sufficient for all senses of Ownership.

Ownership remains unresolved until those distinctions are separated and tested.

### Skill

Candidate reduction:

> A recurrent, reusable, compressed interaction/change pattern or competence over a relevant context class.

Observed recurrence and compression alone are insufficient if a memorized replay and a transferable mapping share the same realized training traces.

### Emotion-like structure

Candidate reduction:

> A recurrent pattern that changes which relations or future interactions remain actionable, often under viability/value constraints.

Whether this requires an independent primitive is unresolved.

## Body

Body is deliberately not equated with the focal cognitive locus.

A useful current hypothesis is:

```text
Exterior / environment ↔ Body   physical interaction
Body → focal locus              embodied / interoceptive grounding
focal locus ↔ focal locus       cognition-like interaction
focal locus → Body → exterior   embodied outward interaction
```

Under this account, metabolism, damage, hunger, temperature, and movement may remain Body-side physical processes unless and until they participate in grounding into the focal locus.

The exact Body / locus partition is itself hypothesis-dependent and must not be frozen by this diagram.

## Promotion and deletion

A candidate may be promoted only when a narrower derivation fails to preserve required distinctions.

A candidate should be:

- **derived** when a lower-level account preserves the needed semantics;
- **split** when one term hides multiple mechanisms;
- **merged** when distinctions collapse under discriminating tests;
- **weakened** when evidence supports only a subset of its claim;
- **deleted** when it adds no discriminating structure.

Formal evaluation parameters should not be promoted to ontology merely because the theory needs coordinates from which to state a relative claim.

Ontology growth is not a success metric.
