# Hypotheses

This file is the lightweight registry of active RelayTheory hypotheses.

Detailed discussion and evidence should live in linked Issues, experiments, formal artifacts, or downstream repositories. This file records only the current research shape.

## Required fields

Each hypothesis should identify:

- **ID**
- **Claim**
- **Null**
- **Discriminating evidence**
- **Falsification condition**
- **Status**
- **Evidence / links**

Statuses should describe epistemic state, not implementation progress.

Suggested values:

- `PROPOSED`
- `UNDER_TEST`
- `PARTIALLY_SUPPORTED`
- `CONSTRAINED`
- `FALSIFIED`
- `UNDERDETERMINED`

## H-001 — High-level agency reduction

**Status:** `CONSTRAINED`

**Issue:** #1 — Test whether high-level agency concepts reduce to grounded Self–World interaction and change

### Claim

High-level concepts such as Skill, Action, Cognition, Perception, and Ownership may be derivable from grounded Self–World interaction/change structure rather than requiring independent primitive semantics.

Current candidate reductions include:

```text
Skill
  ↓
Action
  ↓
Effect
  ↓
Self–World interaction producing change
```

```text
Ownership
  ↓
Authority + Grounding + Trace
```

```text
World ↔ Self   perception-like / grounding interaction
Self  ↔ Self   cognition-like interaction
Self  ↔ World  outward / action-like interaction
```

### Null

High-level agency concepts require independent primitive semantics and cannot be recovered from grounded Self–World interaction and change alone.

### Current constraint

Finite matched countermodels show that **realized trace alone is insufficient** for several target distinctions.

Two systems can have the same actually realized Interaction / Change / Grounding / Trace while differing under an unobserved intervention or context:

- the same outward World change can be Self-dependent in one system and fixed/exogenous in another;
- the same Self update can be sensitive to a World variable in one system and constant/replayed in another;
- the same internal Self change can be coupled to prior internal state in one system and a constant overwrite in another;
- the same successful observed Skill-like training traces can come from a context-general mapping or a memorized/replayed mapping that fails in an unvisited context.

Therefore the following stronger subclaim is falsified:

> High-level agency semantics can be recovered from the actually realized interaction/change history alone.

H-001 remains open because the broader reduction may still survive if the missing distinctions are recoverable from lower-level **transition, dependence, counterfactual, admissibility, or contextual/task structure** without reintroducing the high-level concept under another name.

This constraint does **not** promote any such structure to primitive status.

Ownership is separately constrained because the term currently conflates causal authorship, control/revision authority, Self-boundary membership, and normative/social title. Primitive status should not be tested until those distinctions are separated.

### Discriminating evidence

Useful evidence must distinguish the reduction from the null.

Examples:

- paired cases with equivalent realized traces but different counterfactual transition/dependence structure;
- successful recovery of high-level distinctions without dedicated primitive flags;
- cross-world transfer where low-level interaction/change structure generalizes while domain-specific Skill semantics do not;
- formal countermodels showing that the proposed basis loses necessary distinctions;
- embodied experiments separating physical Body change, grounded Self state, internal Self transformation, and outward interaction.

### Falsification condition

The broad reduction is falsified or further constrained if a high-level distinction is required for prediction, control, explanation, or traceability and cannot be reconstructed from the candidate basis without silently reintroducing equivalent semantics under another name.

A realized-trace-only account is already falsified by finite countermodel.

### Evidence / links

- RelayTheory issue #1
- #1 formal countermodels: https://github.com/rinsakamo/relay-theory/issues/1#issuecomment-5761516750
- Historical RelayLM `relay-theory` lane: provenance only
- RelaySelf experiments may be linked individually when their evidence is relevant

## Registry rule

Do not mark a hypothesis supported because its ontology is elegant.

A simpler theory wins only when it preserves or improves discriminating power against relevant alternatives.
