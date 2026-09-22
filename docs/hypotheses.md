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

**Issue:** #1 — Test whether high-level agency concepts reduce to grounded interaction and change

### Claim

High-level concepts such as Skill, Action, Cognition, Perception, and Ownership may be derivable from lower-level source-anchored dependence / admissible transition structure rather than requiring independent primitive semantics.

Current candidate reductions include:

```text
Skill
  ↓
Action
  ↓
Effect
  ↓
grounded interaction / dependence / change
```

```text
Ownership
  ↓
causal authorship / control authority / incorporation / normative title
  ↓
candidate lower-level provenance / grounding / admissibility structure
```

```text
exterior → focal locus     perception-like
locus    ↔ locus           cognition-like
locus    → exterior        action-like
```

The focal locus is an evaluation/index parameter, not by itself a primitive Self claim.

### Null

High-level agency concepts require independent primitive semantics and cannot be recovered from lower-level grounded structure alone.

### Current constraint — realized-trace non-identifiability

Finite matched countermodels show that **realized trace alone is insufficient** for several target distinctions.

Two systems can have the same actually realized Interaction / Change / Grounding / Trace while differing under an unobserved intervention or context:

- the same outward change can be locus-dependent in one system and fixed/exogenous in another;
- the same internal update can be sensitive to an exterior variable in one system and constant/replayed in another;
- the same internal change can be coupled to prior internal state in one system and a constant overwrite in another;
- the same successful observed Skill-like training traces can come from a context-general mapping or a memorized/replayed mapping that fails in an unvisited context.

Therefore the following stronger subclaim is falsified:

> High-level agency semantics can be recovered from the actually realized interaction/change history alone.

H-001 remains open because the broader reduction may still survive if the missing distinctions are recoverable from lower-level **transition, dependence, counterfactual, admissibility, or contextual/task structure** without reintroducing the high-level concept under another name.

This constraint does **not** promote any such structure to primitive status.

### Current constraint — centered partition structure

Issue #5 established a scoped structural result:

- bare symmetric structure cannot in general select one unique Self;
- a global set of self-capable entities does not substitute for the current deictic center in multi-agent cases;
- genuinely Self-relative / de-se claims require an explicit center or locus of evaluation;
- that center can be represented as an evaluation parameter rather than a global primitive Self entity type;
- World-as-relative-exterior is derivable once ambient scope and focal locus are fixed;
- Boundary-as-crossing-interface is derivable once the locus and relevant relations are fixed.

Therefore Self, World, and Boundary are no longer treated as three independent flat primitive candidates in the current ontology.

This does **not** settle phenomenal selfhood, personal identity, or which organization warrants a Self-like derived classification.

### Current constraint — dynamical terms

Issue #6 established a model-class-constrained reduction:

- Change is derived as non-equivalence across ordered configurations once an explicit equivalence criterion is fixed;
- Trace is a realized path / evidence representation through richer transition structure;
- Interaction is derived as source-to-target sensitivity of admissible successor structure;
- the exact dependence operator is model-class relative across deterministic, nondeterministic, stochastic, and interventional models;
- observational transition structure alone may not identify causal direction under confounding.

Therefore Interaction, Change, and Trace are no longer treated as independent flat primitive candidates in the current ontology.

Issue #13 further classifies State / Configuration / Transition / Intervention-style machinery as formal model/evaluation substrate within the agency-local H-001 scope.

This classification is not based on assuming observational dynamics are sufficient. #22 provides a Level-B finite counterexample in which two models have the same complete observational signature but different intervention responses, and proves that no recovery function from the observational signature alone can reproduce both selected intervention responses.

The independent counterfactual information is therefore retained where required. The #13 re-encoding test separately shows that the named observational/counterfactual presentation is losslessly interconvertible with a generic response profile, so the information gap does not by itself earn a named ontology primitive.

This does **not** settle intrinsic temporal orientation, general physical causation, or cosmological Time.

### Current constraint — generic Relation

Issue #10 established that generic Relation belongs to the formal representation substrate rather than the current RelayTheory ontology.

Function, graph-relation, characteristic-map, adjacency, predicate, kernel, and equivalent encodings can preserve the same structural distinctions. The theoretically relevant content belongs to independently justified structures such as dependence, provenance, admissibility, ordering, or title — not to the generic noun Relation.

Therefore Relation is no longer treated as an independent flat primitive candidate.

This does **not** settle the ontology status of specific grounding / authority / dynamical structures, and it does not assert metaphysical anti-relationalism.

### Current constraint — Grounding and Authority

Issue #7 established a scoped `BOTH DERIVED BUT DISTINCT` result for the H-001 operational role.

- Grounding-like source anchoring is a derived judgment over explicit source identity, dependence, provenance/evidence structure, and a stated criterion.
- operational Authority is a derived context-relative judgment over explicit admissibility / acceptance behavior.
- the two remain orthogonal: unauthorized-but-grounding and authorized-but-inert cases are both coherent.

Therefore Grounding and Authority are no longer treated as independent flat primitive candidates **within this operational scope**.

This does **not** claim to reduce full semantic/reference grounding, epistemic justification, normative legitimacy, or ownership/title. Those stronger meanings must not be packed back into the operational terms.

### Current constraint — operational Action

Issue #35 establishes a scoped operational Action reduction.

A finite matched pair has the same realized source/exterior signature while differing only in counterfactual response of the exterior target to the internal source:

- source-sensitive response — changing the source changes the exterior response;
- fixed response — changing the source does not change the exterior response.

With the same outward focal view, the lower-level attribution predicate separates the pair without an Action flag.

Additional controls show:

- the same sensitive response becomes non-outward when the focal partition is reindexed;
- attribution remains fixed while explicit acceptance/admissibility changes;
- a decorative Action label can vary without changing the attribution result.

Therefore the tested operational H-001 Action role is reconstructed from **counterfactual source sensitivity + supplied focal partition**, with validation/admissibility kept separate.

This is not a reduction of intentional agency, reasons-responsiveness, conscious willing, moral/legal responsibility, normative authorship, or free will.

### Current constraint — operational Perception

Issue #37 establishes a scoped operational Perception reduction.

A finite matched pair has the same realized exterior/internal signature while differing only in counterfactual response of the internal target to the exterior source:

- source-sensitive response — changing the exterior source changes the internal response;
- replay/constant response — changing the exterior source does not change the internal response.

With the same inward focal view, the lower-level Perception-like predicate separates the pair without a Perception flag.

Additional controls show:

- the same source-sensitive response becomes non-perception-like when the focal partition is reindexed;
- an inverted but source-sensitive inward channel remains operationally perception-like, so veridicality / semantic truth / epistemic reliability are separate;
- a decorative Perception label can vary without changing the derived classification.

Therefore the tested operational H-001 Perception role is reconstructed from **counterfactual exterior-to-internal sensitivity + supplied focal partition**.

This is not a reduction of phenomenal perception, conscious awareness, semantic aboutness/reference, perceptual objecthood, epistemic justification/reliability, modality-specific sensing, or every illusion/veridical distinction.

### Current constraint — operational Cognition

Issue #39 establishes a scoped operational Cognition reduction.

Three finite models share the same realized source/intermediate/response signature while separating two lower-level conditions:

- **active** — the internal intermediate is counterfactually sensitive to the internal source and changes a later response;
- **replay** — the intermediate is not source-sensitive;
- **inert** — the intermediate is source-sensitive but does not change the later response.

Only the active model satisfies the lower-level Cognition-like predicate.

Additional controls show:

- the later response can remain inside the focal locus, so no exterior Action-like response is required;
- focal reindexing can remove the internal-to-internal classification;
- a decorative Cognition label can vary without changing the derived result.

Therefore the tested operational H-001 Cognition role is reconstructed from **internal source sensitivity + downstream response relevance + supplied focal partition**.

This is intentionally a broad functional class. Simple control circuitry may satisfy it. The result is not a reduction of semantic thought, rational inference, logical validity, awareness/consciousness, phenomenal thought, deliberation, intentionality, intelligence, or long-horizon planning.

### Current constraint — operational Skill

Issue #41 establishes a scoped operational Skill reduction in the task-relative competence sense.

Two policies have the same observed training signature on context `false`:

- **general** — returns the context itself;
- **replay** — always returns `false`.

Under the explicit identity task over the full Boolean context class, the general policy is competent while replay fails on the unvisited `true` context.

Additional controls show:

- observed training success does not identify competence over the declared context class;
- the same mapping can be competent under one explicit task criterion and not another;
- extensionally equal mappings preserve competence under the same task;
- a decorative Skill label can vary without changing the result.

Therefore the tested operational H-001 Skill role is reconstructed from **response mapping + declared context/task class + explicit evaluation criterion** rather than a primitive Skill object.

This is not a reduction of learning, sample efficiency, hierarchical composition, arbitrary cross-world transfer, expertise, automaticity, compression/resource efficiency, human know-how, Skill acquisition, or crystallization.

### Ownership constraint

Ownership is separately constrained because the term conflates at least:

- causal authorship / provenance;
- control or revision authority;
- focal-locus incorporation / membership;
- normative or social title.

Issue #46 now establishes the first scoped decomposition result.

A finite lower-level response model holds the realized current state fixed while independently varying:

```text
generation sensitivity
  = generated state changes under an explicit source/intervention value

revision privilege
  = a fixed nontrivial successor proposal is accepted
    in the declared revision context
```

All four Boolean combinations are realized, including:

- generation-sensitive without current revision privilege;
- current revision privilege without generation sensitivity.

The discriminator contains no primitive Ownership/authorship/control classification field, and toggling a decorative high-level flag changes neither derived judgment.

Therefore the local Grand Null that causal authorship-like attribution and current control/revision authority must be one obligatorily aligned relation fails in this finite operational scope.

This supports **partial decomposition**, not a reduction of Ownership as a whole.

Still unresolved and not packed into either lower-level judgment:

- focal incorporation / membership;
- possession / custody / access;
- normative, social, legal, or economic title;
- responsibility, consent, and institutional legitimacy;
- bodily ownership and Selfhood.

Primitive status for any surviving Ownership sense must be tested only after these remaining distinctions are separately specified.

### Discriminating evidence

Useful evidence must distinguish the reduction from the null.

Examples:

- paired cases with equivalent realized traces but different counterfactual transition/dependence structure;
- successful recovery of high-level distinctions without dedicated primitive flags;
- tests showing whether Self-like organization can be derived without a prior Self predicate;
- cross-world transfer where low-level interaction/change structure generalizes while domain-specific Skill semantics do not;
- formal countermodels showing that the proposed basis loses necessary distinctions;
- embodied experiments separating physical Body change, grounded focal state, internal transformation, and outward interaction.

### Falsification condition

The broad reduction is falsified or further constrained if a high-level distinction is required for prediction, control, explanation, or traceability and cannot be reconstructed from the candidate basis without silently reintroducing equivalent semantics under another name.

A realized-trace-only account is already falsified by finite countermodel.

A primitive-Self account regains force only if an intrinsic Self-relative distinction is required that cannot be represented by centered lower-level structure or independently grounded internal self-location without a Self-equivalent label.

### Evidence / links

- RelayTheory issue #1
- #1 formal countermodels: https://github.com/rinsakamo/relay-theory/issues/1#issuecomment-5761516750
- #5 terminal reconciliation: https://github.com/rinsakamo/relay-theory/issues/5#issuecomment-5762361501
- #6 terminal reconciliation: https://github.com/rinsakamo/relay-theory/issues/6#issuecomment-5762446402
- #10 terminal reconciliation: https://github.com/rinsakamo/relay-theory/issues/10#issuecomment-5762524282
- #7 terminal reconciliation: https://github.com/rinsakamo/relay-theory/issues/7#issuecomment-5762587015
- #13 dynamical-substrate owner: https://github.com/rinsakamo/relay-theory/issues/13
- #22 intervention information-gap formalization: https://github.com/rinsakamo/relay-theory/pull/22
- #35 operational Action reduction owner: https://github.com/rinsakamo/relay-theory/issues/35
- #36 operational Action finite formalization: https://github.com/rinsakamo/relay-theory/pull/36
- #37 operational Perception reduction owner: https://github.com/rinsakamo/relay-theory/issues/37
- #38 operational Perception finite formalization: https://github.com/rinsakamo/relay-theory/pull/38
- #39 operational Cognition reduction owner: https://github.com/rinsakamo/relay-theory/issues/39
- #40 operational Cognition finite formalization: https://github.com/rinsakamo/relay-theory/pull/40
- #41 operational Skill reduction owner: https://github.com/rinsakamo/relay-theory/issues/41
- #42 operational Skill finite formalization: https://github.com/rinsakamo/relay-theory/pull/42
- #46 Ownership authorship/control decomposition owner: https://github.com/rinsakamo/relay-theory/issues/46
- #49 Ownership authorship/control finite formalization: https://github.com/rinsakamo/relay-theory/pull/49
- Historical RelayLM `relay-theory` lane: provenance only
- RelaySelf experiments may be linked individually when their evidence is relevant

## Registry rule

Do not mark a hypothesis supported because its ontology is elegant.

A simpler theory wins only when it preserves or improves discriminating power against relevant alternatives.
