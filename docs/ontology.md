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

## Formal representation substrate

### Relation notation

Generic Relation is not currently treated as RelayTheory ontology.

Relational notation, functions, predicates, graphs, matrices, kernels, tuple sets, and equivalent structural encodings are formal presentation choices when translations preserve the distinctions used by the theory.

Specific structures — for example dependence, provenance, admissibility, temporal ordering, or normative title — must earn their semantics independently. They are not licensed merely by being named relation types.

This classification follows #10 and does not assert metaphysical anti-relationalism.

## Current primitive frontier

No member of the original flat bootstrap candidate set currently survives **unchanged** as an independent primitive within the operational H-001 scope.

This is not a claim that RelayTheory has proved a primitive-free ontology.

The unresolved frontier has moved downward into questions such as:

- configuration identity and equivalence;
- transition / admissibility structure;
- intervention / causal structure;
- source / provenance representation;
- rule / validation context.

Issue #13 owns the dynamical / admissibility ontology-vs-formal-substrate question.

Stronger semantic or normative notions must receive separate justification if H-001 later requires them.

## Derived source and validation terms

### Grounding-like source anchoring

The operational role previously called Grounding is not currently treated as an independent primitive.

A source-anchoring judgment must expose:

- target;
- source;
- scope / time;
- explicit dependence and/or provenance evidence;
- any additional evidential criterion required by the claim.

Different grounding-like claims can therefore diverge. Historical provenance, current source sensitivity, and epistemic reliability are not interchangeable.

Full semantic/reference grounding — aboutness, meaning, truth conditions, intentional reference — is not claimed reduced by this operational result and must not be hidden inside source anchoring.

### Authority-like operational admissibility

Operational Authority is not currently treated as an independent primitive.

It is derived relative to an explicit rule / validation context and a scoped proposal class from the system's admissibility / acceptance behavior.

Authority is therefore not an intrinsic property of a source: the same source and physical dynamics can have different operational authority under different validation contexts.

Operational acceptance is not the same as legal, moral, social, institutional, or other normative legitimacy. Normative ownership/title likewise remains distinct.

The two derived notions remain orthogonal: a source may causally/provenance-anchor a state without being admissible, and may be admissible without producing the current state.

## Derived dynamical terms

### Interaction

Interaction-like coupling is not currently treated as an independent primitive.

Under an explicit dynamical / intervention model class, it is derived as source-to-target sensitivity of admissible successor structure.

Examples:

- deterministic model — successor-value sensitivity;
- nondeterministic model — successor-set sensitivity;
- stochastic model — successor-distribution sensitivity;
- causal / interventional model — sensitivity under admissible intervention or mechanism replacement.

The exact dependence operator is model-class relative. Observational transition structure may be insufficient to identify causal direction.

### Change

Change is not currently treated as an independent primitive.

Given ordered configurations and an explicitly justified equivalence criterion, descriptive Change is derived as non-equivalence:

```text
Change_Q(x,y)
  := not (x ≡_Q y)
```

The unresolved theoretical burden belongs to configuration identity, ordering, and the equivalence / observation criterion rather than to a separate Change object.

### Trace

Trace is not currently treated as independent system ontology.

A realized trace is a path / record through an explicit transition or admissibility structure, optionally carrying separately justified provenance / grounding annotations.

This distinction matters because #1 showed that a realized path is insufficient to identify several agency distinctions that depend on unrealized alternatives.

The lower-level status of configuration / transition / intervention structure is owned by #13 and is not settled by this reduction.

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

> Exterior-to-locus source-sensitive / source-anchored dependence that modifies locus-accessible state.

A realized update alone is insufficient. The reduction must distinguish a channel that is sensitive to exterior state from replay / injection that happens to produce the same observed update.

### Cognition

Candidate reduction:

> Locus-internal dependence / interaction that transforms locus-accessible relations, representations, or choice structure.

This definition is provisional. Mere internal physical change is insufficient if it lacks the relevant causal / relational role.

### Action

Candidate reduction:

> A locus-to-exterior transition whose relevant outward contribution is counterfactually attributable to the locus and admissible under the explicit validation context.

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
Body → focal locus              embodied / interoceptive source anchoring
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
