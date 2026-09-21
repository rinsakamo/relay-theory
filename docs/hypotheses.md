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

**Status:** `UNDER_TEST`

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

### Discriminating evidence

Useful evidence must distinguish the reduction from the null.

Examples:

- paired cases with equivalent low-level traces but necessarily different Action / Ownership / Cognition semantics;
- successful recovery of high-level distinctions without dedicated primitive flags;
- cross-world transfer where low-level interaction/change structure generalizes while domain-specific Skill semantics do not;
- formal countermodels showing that the proposed basis loses necessary distinctions;
- embodied experiments separating physical Body change, grounded Self state, internal Self transformation, and outward interaction.

### Falsification condition

The broad reduction is falsified or constrained if a high-level distinction is required for prediction, control, explanation, or traceability and cannot be reconstructed from the candidate basis without silently reintroducing equivalent semantics under another name.

### Evidence / links

- RelayTheory issue #1
- Historical RelayLM `relay-theory` lane: provenance only
- RelaySelf experiments may be linked individually when their evidence is relevant

## Registry rule

Do not mark a hypothesis supported because its ontology is elegant.

A simpler theory wins only when it preserves or improves discriminating power against relevant alternatives.
