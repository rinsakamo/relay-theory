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

**Status:** `PARTIALLY_SUPPORTED`

**Terminal issue classification:** `PARTIAL REDUCTION`

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

The broader H-001 program therefore tests recovery from lower-level **transition, dependence, counterfactual, admissibility, and contextual/task structure** rather than realized history alone.

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

Issue #47 then tests a residual claim: whether hierarchical / reusable decomposition adds operational information beyond that extensional competence surface.

A finite paired profile has the same ordinary context-to-response mapping and the same ordinary identity-task competence in both systems, while a separately declared counterfactual probe produces different responses. Therefore ordinary extensional equality does not determine intervention-indexed response.

The tested difference is nevertheless fully represented by an explicit `Context × Probe -> Response` family. Pointwise-equal full profiles preserve the derived perturbation-sensitive distinction, and a decorative hierarchy label can vary without changing it.

Current scoped classification:

```text
RECONSTRUCTIBLE UNDER INTERVENTION SURFACE
```

This does not establish that intrinsic or uniquely privileged hierarchical decomposition exists. A stronger independence result would require two systems with the same full declared intervention/recombination response family but a remaining operational distinction that is not carried by a hierarchy-equivalent label.

Issue #53 then separates the first explicit resource-sensitive axis from #41 competence.

Using an explicit finite cost field, the paired cases establish:

- the same competent response mapping can have different declared costs;
- equal declared costs can coexist with different #41 identity-task competence;
- a combined resource-sensitive judgment is reconstructed as competence plus `cost <= declared budget`;
- a decorative crystallization flag does not alter competence, budget qualification, or the combined result.

Current scoped classification:

```text
COMPETENCE–RESOURCE ORTHOGONAL
```

This classification is only about the tested explicit cost metric. It does not identify compression in general with that metric or reduce learning-time crystallization. Current `PredictiveCapacity` and `LossyWorkload` results separately show that exact representation sufficiency is response-surface-relative and lossy representation preference can reverse when declared future-query weights change.

Issue #64 then tests whether exact deterministic robustness adds a new Skill-like distinction beyond #41 competence. Two profiles share the same nominal mapping and nominal identity-task competence while differing under a separately declared variation. Thus nominal competence does not determine robustness over a larger evaluation surface.

However the exact robustness predicate is mechanically equivalent to the same competence schema over an enlarged product context:

```text
Context × Variation
```

with the ordinary success criterion lifted to ignore the variation coordinate except through the response. Pointwise-equal full profiles preserve the result and a decorative robustness label adds no information.

Current scoped classification:

```text
EXACT ROBUSTNESS DERIVED AS CONTEXT EXPANSION
```

This applies only to deterministic universal success over the declared variation class. Probabilistic, approximate, graded, adversarial, and distributional robustness remain unresolved and may require additional explicit evaluation structure.

Issue #74 then tests a deterministic bounded-failure surface. Reusing the #64 profiles, the exact profile has zero failures and the brittle profile has one failure over the declared two-variation evaluation. The brittle profile is not exactly robust, fails budget 0, and passes budget 1.

Thus approximate qualification is threshold-relative and is reconstructed in this finite instance from:

```text
response profile
+ explicit failure aggregation
+ explicit budget
```

Pointwise-equal profiles preserve the aggregation and qualification, and a decorative approximate-robustness flag changes nothing.

Current scoped classification:

```text
BOUNDED ROBUSTNESS RECONSTRUCTIBLE UNDER LOSS/THRESHOLD SURFACE
```

This classification is only for the explicit finite failure-count/budget evaluator. Probability distributions, expected loss, stochastic dynamics, adversarial optimization, continuous perturbation metrics, and semantic error severity remain unresolved.

The #41/#47/#53 results are not a reduction of learning, sample efficiency, biological motor chunking, unique or intrinsic hierarchical composition, arbitrary cross-world transfer, expertise, automaticity, general compression/resource efficiency, human know-how, Skill acquisition, or crystallization dynamics.

### Current constraint — formation process vs final retained state

Issue #60 tests the first process-versus-structure boundary needed by #55.

A finite pair uses only an explicit experience-to-retained-state map. The two maps have the same actual final retained state and the same current identity readout, but one is counterfactually sensitive to experience while the other is constant across the experience coordinate. Therefore:

```text
same current retained state / readout
  -/->
same experience-dependent formation structure
```

The same transaction combines the experience-insensitive formation map with #41's already-proved competent `generalPolicy`. Thus, in this finite product model:

```text
operational Skill-like competence
  -/->
experience-sensitive retained-state formation
```

This constrains the #55 Crystallization hypothesis: process semantics cannot be recovered from the final retained state alone unless the required formation/provenance information is explicitly represented. It does not establish that such information is an ontology primitive, nor that a common retained substrate exists across Memory / Skill / Concept / Habit / Belief.

### Current constraint — prequalified Selfhood

Issue #43 tests whether operational H-001 needs a prior Self-like eligibility predicate for the supplied focal locus.

A finite raw-response profile contains no Self / Action / Perception / Cognition classification fields. The derived operational agency-locus predicate is expressed directly as a conjunction of:

- exterior-to-internal sensitivity;
- internal source-to-intermediate sensitivity;
- intermediate-to-downstream sensitivity;
- internal-to-exterior sensitivity.

The fully responsive profile satisfies the declared bundle. Inert and partial profiles fail because specific lower-level response structure is absent. A decorative Self label can vary without changing the result.

Therefore current operational H-001 does **not** require a prequalified `Eligible(Self)` gate before evaluating the focal response structure.

This is **not** a derivation of phenomenal or person-level Selfhood. The resulting agency-locus profile is deliberately a weaker operational summary. Consciousness, personal identity, persistence, organismic individuality, autopoiesis, internal de-se representation, body ownership, and personhood remain outside this result.

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

Issue #58 then tests one narrower normative/institutional surface: registry-mediated title.

Its finite witness keeps the #46 physical/control profile and the transfer proposal fixed while varying only an explicit institutional transfer-admissibility rule. The current recognized claimant changes with that rule surface.

The same transaction also realizes:

- current revision privilege without registry title;
- registry title without current revision privilege;
- rejected transfer without title change;
- decorative Ownership/title label deletion.

Therefore physical causal/control structure is insufficient to determine this title sense.

However, after an explicit institutional initial assignment, transfer rule, and proposal are supplied, the finite current recognized claimant is reconstructed without an additional Ownership/title primitive.

This yields the scoped constraint:

```text
physical reduction fails for registry title

but

registry title is reconstructible
relative to an explicit institutional rule surface
```

The institutional initial assignment and rule are **inputs**. #58 does not derive them from physics and does not establish institutional, legal, or moral legitimacy.

Issue #61 then tests a narrower physical/operational possession split.

Four finite profiles hold the realized carrier/object/request/use snapshot fixed while independently varying:

```text
custody-like transport coupling
  = object-location sensitivity
    to a declared carrier/location probe

access-like use capability
  = use-outcome sensitivity
    to a declared claimant-associated request probe
```

All four `CustodyLike × AccessLike` combinations are realized.

The same transaction also separates:

- access-like capability from #46 current revision privilege in both directions;
- custody/access structure from #58 registry title;
- the derived roles from a decorative possession label.

Therefore one obligatorily aligned possession variable is too coarse for these tested operational roles.

This result does not define legal possession or arbitrary physical custody. It only establishes that the tested transport-coupling, use-capability, revision-authority, and registry-title roles carry independently variable information.

Issue #51 then tests persistence of the already-separated operational attribution senses through transfer/replacement.

Its finite time-indexed witness shows:

- revision privilege can transfer A -> B while the realized state and A's generation sensitivity remain fixed;
- current generation sensitivity can transfer A -> B across replacement while the realized Boolean value remains fixed;
- strict snapshot identity and an explicitly declared successor-lineage criterion can disagree on the same cross-snapshot pair;
- declared lineage continuity does not imply persistence of the earlier source's current generation-side attribution;
- a decorative continuity flag adds no information.

Therefore, for this scoped operational surface:

```text
current causal attribution
current revision privilege
cross-snapshot continuity
```

must not be collapsed into one timeless Ownership attribute.

The first two are time/context-relative lower-level judgments. The third is criterion-relative to an explicitly supplied identity/lineage standard. This supports **PERSISTENCE_CRITERION_RELATIVE / RECONSTRUCTIBLE_UNDER_IDENTITY_CRITERION** for the tested attribution surface, not a metaphysical identity theory and not a reduction of normative title succession.

Issue #71 then tests the residual focal-incorporation / “part of me” phrase.

The finite witness separates analytic membership in the supplied focal locus from a declared bidirectional functional-integration role.

Four matched candidate components share the same realized component/focal-target snapshot while realizing all four:

```text
insideFocal × FunctionallyIntegrated
=
00, 01, 10, 11
```

where the functional role is reconstructed directly from:

```text
focal-source -> component sensitivity
AND
component -> focal-target sensitivity
```

One-way outbound-only and inbound-only controls fail the declared bidirectional role.

Cross-checks against #61 also establish that custody-like transport coupling and access-like use capability do not force bidirectional functional integration, while bidirectional functional integration need not carry the tested custody-like transport role.

Therefore the tested residual incorporation phrase splits:

```text
analytic focal membership
!=
bidirectional functional integration
```

and the latter is reconstructible from the explicit response surface in this finite scope without an incorporation bit.

This does not reduce phenomenal body ownership, body schema, biological individuality, personal identity, or persistence through replacement.

Still unresolved or outside these scoped Ownership results:

- phenomenal body ownership / body schema;
- biological or organismic individuality;
- arbitrary physical containment / exclusivity / durable custody beyond the tested role;
- broader normative, social, legal, or economic legitimacy;
- responsibility and consent;
- copyright authorship;
- Selfhood / personal identity;
- normative/title persistence through arbitrary replacement and broader identity questions.

Primitive status for any surviving Ownership sense must be tested only after these remaining distinctions are separately specified.

### Terminal synthesis — PARTIAL REDUCTION

Issue #1 has reached its stated exit condition.

The accumulated finite/formal results support the following scoped conclusions:

- operational Action-like attribution is reconstructed from counterfactual source sensitivity plus the supplied focal partition;
- operational Perception-like uptake is reconstructed from exterior-to-internal sensitivity plus the supplied focal partition;
- operational Cognition-like function is reconstructed from internal source sensitivity plus downstream response relevance;
- task-relative Skill-like competence is reconstructed from response mapping plus declared context/task/evaluation surface, with later robustness/resource refinements likewise represented by explicit evaluation structure;
- current operational H-001 does not require a prequalified Selfhood gate;
- the original flat Self / World / Boundary / Relation / Interaction / Change / Grounding / Authority / Trace candidate set does not survive unchanged as an independent primitive set in the tested agency-local scope.

At the same time, stronger reduction claims fail or remain outside the result:

- realized interaction/change history alone is insufficient;
- observational response alone does not in general determine intervention response;
- monolithic Ownership does not survive: authorship-like attribution, revision authority, custody-like coupling, access-like capability, registry-mediated title, cross-snapshot continuity, analytic focal membership, and bidirectional functional integration carry independently variable information;
- registry-mediated title is **not** determined by physical causal/control structure alone and is reconstructed only relative to an explicit institutional rule surface;
- phenomenal Selfhood/body ownership, biological individuality, broader normative legitimacy, responsibility/consent, and other stronger meanings remain separate research questions.

Therefore the broad issue-level outcome is:

```text
PARTIAL REDUCTION

operational agency categories
  -> substantially reconstructible from lower-level explicit structure

but

grounded physical interaction/change alone
  -/->
all higher-level normative / phenomenal / identity semantics
```

This closes the broad H-001 Issue without claiming a primitive-free theory. Narrower residual questions continue in their own Issues and may further constrain or extend these results.

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
- #47 hierarchical Skill decomposition residual owner: https://github.com/rinsakamo/relay-theory/issues/47
- #50 intervention-indexed Skill decomposition formalization: https://github.com/rinsakamo/relay-theory/pull/50
- #53 Skill competence/resource orthogonality owner: https://github.com/rinsakamo/relay-theory/issues/53
- #54 Skill competence/resource finite formalization: https://github.com/rinsakamo/relay-theory/pull/54
- #43 Self-like qualification / operational agency-locus owner: https://github.com/rinsakamo/relay-theory/issues/43
- #44 operational agency-locus finite formalization: https://github.com/rinsakamo/relay-theory/pull/44
- #46 Ownership authorship/control decomposition owner: https://github.com/rinsakamo/relay-theory/issues/46
- #49 Ownership authorship/control finite formalization: https://github.com/rinsakamo/relay-theory/pull/49
- #58 registry-mediated Ownership title owner: https://github.com/rinsakamo/relay-theory/issues/58
- #59 registry-mediated title finite formalization: https://github.com/rinsakamo/relay-theory/pull/59
- #61 possession custody/access decomposition owner: https://github.com/rinsakamo/relay-theory/issues/61
- #63 custody/access finite formalization: https://github.com/rinsakamo/relay-theory/pull/63
- #71 focal membership/integration decomposition owner: https://github.com/rinsakamo/relay-theory/issues/71
- #72 focal membership/integration finite formalization: https://github.com/rinsakamo/relay-theory/pull/72
- Historical RelayLM `relay-theory` lane: provenance only
- RelaySelf experiments may be linked individually when their evidence is relevant

## Registry rule

Do not mark a hypothesis supported because its ontology is elegant.

A simpler theory wins only when it preserves or improves discriminating power against relevant alternatives.
