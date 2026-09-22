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

Within the agency-local H-001 scope, #13 now classifies the generic dynamical machinery below the derived agency terms as **formal model/evaluation substrate rather than RelayTheory ontology primitives**.

This includes, when a chosen model requires them:

- configuration carriers / identifiers;
- transition or successor encodings;
- observation / equivalence probes;
- counterfactual or intervention response families;
- operational admissibility / validation contexts.

These components need not be mutually reconstructible. #22 formally shows that complete observational response can be identical while intervention response differs. Independent information relative to a smaller model is therefore retained when the claim needs it.

That information gap does not by itself promote a named primitive. #13's re-encoding test shows the named observational/counterfactual fields used by #22 are losslessly equivalent to a semantics-free response profile; the semantic roles are supplied by the surrounding model/evaluation context.

This scoped result does **not** classify intrinsic temporal orientation, physical causation in general, semantic grounding, epistemic justification, normative legitimacy, or ownership/title. Such stronger structure requires separate evidence; Time/cosmology reconstruction remains under #15.

## Formal dynamical and counterfactual substrate

RelayTheory may quantify over dynamical models without treating the representation vocabulary of those models as agency ontology.

A model may expose deterministic maps, nondeterministic successor sets, stochastic kernels, causal/interventional response families, validation rules, or equivalent encodings. What matters to a scoped RelayTheory claim is the invariant discriminating content preserved by the chosen semantics, not the noun used to store it.

The #22 countermodel establishes a real information gap:

```text
observational response
  -/-> 
counterfactual intervention response
```

The #13 re-encoding result establishes a separate representation fact:

```text
named observe / intervention fields
  <-> 
generic response profile
```

without information loss.

Therefore "formal substrate" does **not** mean "discard counterfactual information." It means that required lower-level information is carried explicitly by the model semantics rather than promoted merely because a current encoding names it State, Transition, Intervention, or Admissibility.

Evaluation parameters and model semantics can still be theory-essential for a particular theorem while remaining non-ontological in this scoped classification.

## Temporal reconstruction constraints

Time reconstruction remains separate from the agency-local substrate classification above.

Current scoped results distinguish at least:

```text
local Present
  -> focal event / evaluation index
     [#30]

global co-present slice
  -/-> causal/process order + focal event
     [#26 / #29]

strict temporal orientation
  -> requires independently represented asymmetry
     in the declared surface
     [#33]

local lineage totality
  -/-> ambient global totality
     [#45]
```

The finite #45 discriminator uses a three-event merge order:

```text
a -> c
b -> c

a || b
```

with selected local lineages `{a,c}` and `{b,c}`. Each lineage is total under the same ambient precedence relation and together they cover the event carrier, while the ambient relation remains non-total.

The same partial structure admits two injective scalar linearizations preserving every ambient precedence constraint:

```text
a < b < c
b < a < c
```

Their disagreement is not harmless if the serialization is substituted for temporal semantics. Relative to focal `a`, ambient `b` is `ELSEWHERE`; the two scalar serializations instead classify it as opposite `FUTURE` and `PAST` cases.

Therefore, within this finite deictic/order scope:

> **Local one-dimensionality and the existence of scalar serializations do not by themselves determine or require one intrinsic global total time.**

A scalar linearization may be a useful representation while still adding comparisons absent from the source partial structure.

This result does **not** establish that temporal precedence is a RelayTheory ontology primitive, that all physical Time is partially ordered, that incomparability means simultaneity, that spacetime admits no physically preferred foliation, or that relativity has been derived. Any stronger global temporal structure must supply independent discriminating information.

#66 adds a symmetry constraint on any such stronger structure. In the same three-event merge fixture, the source automorphism `a ↔ b`, `c ↦ c` preserves every ambient precedence fact. A universally quantified formal obstruction shows that no strict total order on the carrier can both remain invariant under that source automorphism and totalize the structurally exchangeable pair.

Two strict total extensions still exist and both preserve ambient precedence. Each necessarily breaks the source symmetry. Therefore, in this finite scope:

> **A preferred global total order cannot be reconstructed invariantly from a source structure that still treats the relevant incomparable events as symmetry-equivalent.**

This does not make symmetry-breaking itself a Time primitive. It states an information requirement: any preferred extension must contain, inherit, or derive additional structure that distinguishes the events it newly orders. That extra structure may come from a law, boundary condition, field, measurement convention, or another independently justified source; the present result does not choose among those possibilities.

#73 adds a separate metric-information constraint. Fix one complete strict chain:

```text
a < b < c
```

Two injective scalar clocks,

```text
0, 1, 2
0, 1, 3
```

both preserve and reflect exactly that same strict order. Their induced interval assignments are positive on all strict comparisons and additive along the finite chain, yet disagree on `b -> c` and `a -> c`.

Therefore, in this finite clock/interval surface:

> **Complete temporal ordering does not by itself determine metric-like duration.**

The formal reconstruction obstruction is exact: one deterministic recovery function given the identical source-order relation cannot return both extensionally different admissible duration assignments.

This does not promote a clock or metric to ontology merely because order is insufficient. It establishes only that any duration-like magnitude requires additional scale/spacing information not present in pure order. The result does not establish physical proper time, Lorentzian geometry, continuity, discreteness, relativity, or a universal temporal metric.

#81 adds a branching-continuation constraint. In a minimal three-event fork,

```text
root < left
root < right
left || right
```

the source admits an automorphism exchanging `left` and `right` while fixing `root` and preserving every ambient precedence fact.

A branch continuation is defined only as a selected subset that contains the root, is chain-like under ambient precedence, and contains at least one proper successor of the root. Both `{root,left}` and `{root,right}` satisfy that same criterion.

No valid continuation subset can remain invariant under the branch-exchange automorphism: invariance would force both incomparable branch events into the same selected subset, contradicting chainhood.

Therefore, in this finite branching surface:

> **Ambient branching order does not by itself select one intrinsic continuation lineage when the candidate branches remain symmetry-equivalent in the source structure.**

This is a lineage-selection result, not a personal-identity result. It does not determine which branch is “the same observer,” whether identity can split, or whether any physical process literally branches. Any distinguished continuation requires additional branch-discriminating information when the retained source structure leaves the alternatives symmetric.



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

The lower-level configuration / transition / intervention machinery is classified by #13 as formal model/evaluation substrate within the agency-local scope. The required information must remain explicit; only its promotion to a named ontology primitive is rejected.

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

“Self” is not treated here as one undifferentiated primitive question.

#5 established that a center / focal locus is required for Self-relative evaluation, while the center itself is an evaluation parameter rather than a Selfhood claim.

#43 sharpens the remaining operational question:

> H-001 does not currently require a locus to pass a prior `Eligible(Self)` / `isSelf` gate before Action-like, Perception-like, Cognition-like, or other focal response structure can be evaluated.

A finite raw-response model shows that an **operational agency-locus profile** can be derived directly from independently stated response sensitivities:

- exterior-to-internal sensitivity;
- internal source-to-intermediate sensitivity;
- intermediate-to-downstream sensitivity;
- internal-to-exterior sensitivity.

A fully responsive focal profile satisfies the declared operational bundle; an inert profile and a profile missing outward sensitivity fail for explicit structural reasons. A decorative `selfFlag` can toggle without changing that result.

This does **not** derive metaphysical Selfhood.

The operational agency-locus profile is intentionally weaker than:

- phenomenal selfhood;
- consciousness;
- personal identity;
- persistence across time or substrate replacement;
- organismic individuality / autopoiesis;
- internal de-se self-representation;
- body ownership;
- moral or legal personhood.

Those stronger notions require separate discriminating criteria if RelayTheory needs them.

Accordingly, prequalified Selfhood is not currently required for the operational H-001 scaffold, while stronger Selfhood remains unresolved rather than promoted or denied.

## Derived agency candidates

The following terms are useful descriptions but are **not currently primitive**.

### Perception

Within the scoped operational H-001 role tested by #37, Perception-like uptake is currently **derived rather than primitive**.

The retained lower-level account is:

> Counterfactual sensitivity of a target inside the supplied focal locus to a source outside that locus.

The finite #37 discriminator keeps the realized exterior/internal signature fixed while changing only the exterior-to-internal response family. The source-sensitive model is perception-like under the inward focal view; the replay/constant model is not.

Inwardness is evaluation-relative rather than an intrinsic edge type: the same source-sensitive response is inward under one supplied focal view and non-perception-like under an internal reindexing.

Operational uptake does not imply veridicality, semantic truth, or epistemic reliability. An inverted exterior-to-internal channel remains source-sensitive and inward while disagreeing with the exterior source on the realized value.

A decorative `perceptionFlag` can vary without changing the derived operational classification and therefore adds no independent information in this scope.

This result does **not** reduce phenomenal perception / qualia, conscious awareness, semantic aboutness or reference, perceptual objecthood, epistemic justification or reliability, modality-specific sensing, or every distinction between illusion and veridical perception. Those stronger meanings require separate justification if RelayTheory needs them.

### Cognition

Within the scoped operational H-001 role tested by #39, Cognition-like transformation is currently **derived rather than primitive**.

The retained lower-level account is:

> A source-sensitive transformation between states inside the supplied focal locus whose intermediate state changes at least one later scoped response family.

The finite #39 discriminator separates three models with the same realized source/intermediate/response signature:

- **active** — internal source sensitivity plus downstream response relevance;
- **replay** — downstream relevance without source-sensitive internal transformation;
- **inert** — source-sensitive internal transformation without downstream response relevance.

Only the active model satisfies the scoped Cognition-like predicate.

The later response may itself remain inside the focal locus, so operational Cognition-like classification does not require an exterior Action-like consequence.

Focal reindexing can remove the internal-to-internal classification, and a decorative `cognitionFlag` adds no independent information.

This functional role is deliberately broad. A thermostat, control circuit, or biochemical network may also instantiate the same structural pattern. Therefore the result does **not** identify this operational role with semantic thought, rational inference, logical validity, awareness / consciousness, phenomenal thought, deliberation, intentionality, intelligence, or long-horizon planning. Those stronger meanings require separate justification if RelayTheory needs them.

### Action

Within the scoped operational H-001 role tested by #35, Action-like attribution is currently **derived rather than primitive**.

The retained lower-level account is:

> Counterfactual sensitivity of a target outside the supplied focal locus to a source inside that locus.

The finite #35 discriminator keeps the realized outward signature fixed while changing only the source-to-target response family. The sensitive model is attributable under the outward focal view; the fixed-response model is not.

Outwardness is evaluation-relative rather than an intrinsic transition type: the same sensitive response is outward under one supplied focal view and non-outward under another.

Operational acceptance / authorization is not part of the attribution definition. It remains an explicit validation-context judgment, so attributable-but-unaccepted and attributable-and-accepted cases can coexist.

A decorative `actionFlag` can vary without changing the derived attribution result and therefore adds no independent information to this scoped operational classification.

This result does **not** reduce intention, reasons-responsiveness, conscious willing, moral or legal responsibility, normative authorship, or free will. Those stronger meanings require separate justification if RelayTheory needs them.

### Ownership

Ownership is currently treated as an overloaded family under decomposition rather than one accepted primitive.

The first scoped split is now earned by #46:

> **Causal/provenance authorship-like attribution and current revision authority are independently variable in the tested finite operational model class.**

The formal discriminator contains no Ownership/authorship/control classification field. It derives two judgments from independently interpretable lower-level response structure:

```text
generation-side attribution
  <- counterfactual sensitivity of generated state
     to an explicit source/intervention value

current revision privilege
  <- explicit acceptance of a fixed nontrivial
     successor proposal in the declared context
```

Four profiles hold the realized current state fixed while realizing all four Boolean combinations of those judgments. In particular:

- generation-sensitive but not revision-enabled;
- revision-enabled but not generation-sensitive.

A decorative high-level flag can vary without changing either result.

Therefore a monolithic Ownership account that requires causal authorship-like attribution and current control/revision authority to coincide is falsified for this scoped operational surface.

The previous shorthand `Authority + Grounding + Trace` remains insufficient for all senses of Ownership.

#58 now adds a second scoped decomposition result for **registry-mediated institutional title**.

The finite institutional surface contains only:

```text
initial assignment
transfer-admissibility rule
transfer proposal
```

and derives a current recognized claimant by applying the declared rule to the proposal. A scoped registry-title judgment is equality with that derived claimant; no primitive `owner`, `owns`, or `titleHolder` input is used.

Matched cases establish:

- the same #46 physical/control profile and same proposal can yield different registry-title outcomes under different institutional rules;
- current revision privilege can exist without registry title;
- registry title can exist without current revision privilege;
- a rejected transfer leaves the initial assignment unchanged;
- a decorative Ownership/title flag adds no information.

Therefore:

```text
physical causal/control structure alone
  -/->
registry-mediated institutional title
```

while, in this finite scope:

```text
registry-mediated title
  <-
explicit institutional initial assignment
+ transfer rule
+ transfer event
```

This is **not** a reduction of normativity to physics. The institutional base assignment and rule surface are explicit contextual inputs, and the result does not establish their legitimacy.

#61 adds a third scoped decomposition result for the physical/operational “possession” bundle.

The finite response surface contains no possession/custody/access classification input. It instead exposes two independent response families:

```text
carrier/location probe
  -> object location

claimant-associated request
  -> use outcome
```

The scoped operational judgments are:

```text
CustodyLike
  := object location is sensitive
     to the declared carrier/location probe

AccessLike
  := use outcome is sensitive
     to the declared claimant-associated request probe
```

Four matched profiles share the same realized carrier/object/request/use snapshot while realizing every Boolean combination:

```text
CustodyLike × AccessLike
=
00, 01, 10, 11
```

Additional matched controls establish:

- access-like use capability without #46 current revision privilege;
- #46 current revision privilege without access-like use capability;
- identical custody/access response structure with different #58 registry-title outcomes;
- the same registry-title result while custody/access roles differ;
- decorative possession-label deletion.

Therefore, in this finite operational scope:

```text
custody-like transport coupling
!=
access-like use capability
!=
current revision authority
!=
registry-mediated institutional title
```

This does not turn either role into legal possession. `CustodyLike` here is only transport/location coupling under the declared probe, and `AccessLike` is only use-outcome sensitivity under the declared request probe.

#51 adds a separate persistence result for the operational attribution senses already split by #46.

Its finite time-indexed witness establishes:

- revision privilege can transfer A -> B while the realized state and A's generation sensitivity remain fixed;
- current generation sensitivity can move A -> B across replacement while the realized Boolean value remains fixed;
- strict snapshot identity and an explicitly declared successor-lineage criterion can disagree on the same cross-snapshot pair;
- declared lineage continuity does not imply persistence of the earlier source's current generation-side attribution;
- a decorative continuity flag adds no information to these scoped judgments.

Therefore:

```text
current causal attribution
current revision privilege
cross-snapshot continuity
```

are not one timeless Ownership attribute in this finite operational surface. The first two are time/context-relative response judgments. Cross-snapshot continuity is evaluated relative to an explicitly supplied identity/lineage criterion.

This earns a scoped **persistence-criterion-relative** result. It does not select a metaphysically privileged identity criterion and does not reduce legal/normative title succession.

#71 adds a fourth scoped decomposition result for the residual focal-incorporation / “part of me” phrase.

It separates:

```text
analytic focal membership
```

from:

```text
bidirectional functional integration
```

The first is explicit evaluation structure inherited from #5: a candidate component is either inside or outside the supplied focal locus. It is not by itself a Selfhood or body-ownership judgment.

The second is reconstructed in the finite #71 model from two independently stated response families:

```text
focal-source probe
  -> candidate component response

candidate-component probe
  -> focal target response
```

with:

```text
FunctionallyIntegrated
  :=
outbound response sensitivity
AND
inbound response sensitivity
```

Four matched components share the same realized component/focal-target snapshot while realizing every combination:

```text
insideFocal × FunctionallyIntegrated
=
00, 01, 10, 11
```

Therefore analytic focal membership does not determine the tested functional-integration role, and the tested functional role does not determine analytic membership.

Additional controls establish:

- outbound-only coupling is insufficient for the declared bidirectional role;
- inbound-only coupling is insufficient;
- #61 custody-like transport coupling can exist without bidirectional functional integration;
- bidirectional functional integration can exist without #61 custody-like transport coupling;
- #61 access-like capability can exist without bidirectional functional integration;
- a decorative incorporation label adds no information.

Thus, in this finite operational scope:

```text
analytic focal membership
!=
bidirectional functional integration
!=
custody-like transport coupling
!=
access-like use capability
```

This scoped functional result does **not** establish phenomenal body ownership or identify every ordinary meaning of “part of me”.

Ownership therefore remains only **partially decomposed**. Still unresolved or outside these scoped results:

- phenomenal body ownership / body schema;
- biological or organismic individuality;
- arbitrary physical containment, exclusivity, or durable custody beyond the tested transport-coupling role;
- broader normative, social, legal, or economic legitimacy beyond the declared registry;
- consent;
- moral responsibility;
- copyright authorship;
- Selfhood or personal identity;
- normative/title persistence through arbitrary object replacement and broader identity questions.

Those meanings require separate criteria and owners if RelayTheory needs them.

### Skill

Within the scoped operational H-001 role tested by #41, Skill-like competence is currently **derived rather than primitive**.

The retained lower-level account is:

> A response mapping that satisfies an explicit task/evaluation criterion over a declared context class.

The finite #41 discriminator compares two mappings with the same observed training signature on the sole observed context:

```text
general(false) = false
replay(false)  = false
```

Under the explicit identity task over the full Boolean context class:

```text
success(c,r) iff r = c
```

the general mapping succeeds on both contexts while replay fails on the unvisited `true` context.

Therefore observed recurrence, training success, or realized trace compression does not establish the tested competence distinction.

Competence is task-relative: the same replay mapping becomes competent under a different explicit constant-false task criterion. It is also representation-invariant in this scope: extensionally equal response mappings have the same competence status under the same task criterion.

A decorative `skillFlag` can vary without changing competence and therefore adds no independent information.

Issue #47 tests the first residual hierarchical / reusable-decomposition pressure without introducing a Skill tree. Its finite matched pair has the same ordinary response mapping and the same ordinary #41 competence, but differs under one independently declared counterfactual probe. Thus ordinary extensional equality does **not** determine the full intervention-indexed response family.

In the tested case, however, the missing distinction is reconstructed directly by:

```text
Context × Probe -> Response
```

Pointwise-equal full profiles preserve the perturbation-sensitive classification, and a decorative `hierarchyFlag` does not alter it. The current scoped consequence is therefore **RECONSTRUCTIBLE UNDER INTERVENTION SURFACE**: perturbation sensitivity does not by itself establish an intrinsic hierarchical Skill object.

To earn independent decomposition structure, a stronger countermodel would need to preserve the entire declared intervention/recombination response family while still requiring a different operational classification for reasons not encoded by a hierarchy-equivalent label.

Issue #53 tests a separate compression/resource-pressure question using an explicit declared cost rather than a compression or crystallization primitive. Its finite models establish both directions of non-determination:

```text
same competence
  -/->
same explicit resource cost

same explicit resource cost
  -/->
same competence
```

Two candidates can implement the same competent response mapping while carrying different declared costs. Conversely, equal-cost general and replay policies differ in #41 identity-task competence. A resource-sensitive operational judgment is reconstructed directly as:

```text
task-relative competence
+
explicit cost <= declared budget
```

and a decorative `decorativeCrystallized` flag changes neither competence, budget qualification, nor the combined judgment.

The current scoped conclusion is therefore **COMPETENCE–RESOURCE ORTHOGONAL** for this explicit finite cost metric. This does not identify "compression" in general with one cost field, nor does it reduce learning-time crystallization. Current `PredictiveCapacity` and `LossyWorkload` results independently reinforce that representation sufficiency and lossy representation preference are relative to a declared response/workload surface.

Issue #64 tests exact deterministic robustness under an explicit variation coordinate. Its matched profiles agree on every nominal response and are both competent on the nominal identity-task surface, but differ on an admitted non-nominal variation. Nominal competence therefore does **not** determine exact robustness.

The additional result is stronger than a new robustness label. With:

```text
Profile : Context -> Variation -> Response
```

exact robustness is proved equivalent to ordinary competence after pairing the evaluation coordinates:

```text
ExpandedContext := Context × Variation

ExactRobust(success, profile)
  <->
Competent(liftedSuccess, asExpandedPolicy(profile))
```

Pointwise-equal full profiles preserve the result, and a decorative robustness flag adds no information. The scoped consequence is therefore **EXACT ROBUSTNESS DERIVED AS CONTEXT EXPANSION** for deterministic universal success over the declared variation class.

This result does not extend automatically to probabilistic success, expected loss, bounded degradation, adversarial risk, distribution shift, or other approximate/stochastic notions. Those require explicit measure / metric / threshold / distribution structure and separate testing.

Issue #74 tests the first bounded deterministic extension without introducing probability. Over the same two-variation #64 response surface, the exact profile has failure count 0 while the brittle profile has failure count 1. The brittle profile fails exact robustness and budget 0, but passes an explicit failure budget of 1.

Therefore exact robustness and bounded qualification are distinct:

```text
BudgetQualified(profile,budget)
  :=
FailureCount(profile) <= budget
```

The same profile can fail or pass solely when the declared budget changes, while the same budget can separate different profiles. Pointwise-equal full profiles preserve both failure count and qualification, and a decorative approximate-robustness label adds no information.

The scoped classification is **BOUNDED ROBUSTNESS RECONSTRUCTIBLE UNDER LOSS/THRESHOLD SURFACE** for this finite failure-count/budget evaluator. This does not generalize the count metric into a universal loss function and does not establish probabilistic or stochastic robustness.

Issue #78 adds an explicit finite variation-weight surface while reusing #74's binary failure loss. Two profiles have equal unweighted failure count but fail on opposite variation values. Under equal-total weight assignments `(2,1)` and `(1,2)`, the strict weighted-risk ranking reverses when only the declared weights are swapped.

Therefore unweighted bounded robustness does not determine distribution-weighted risk. In the tested finite scope, however, the missing distinction is reconstructed from:

```text
response profile
+ explicit pointwise binary loss
+ declared finite variation weights
+ threshold / comparison rule
```

Pointwise-equal full profiles preserve weighted failure under fixed weights, an explicit weighted budget reconstructs the finite qualification, and a decorative probabilistic-robustness label adds no information.

The scoped classification is **DISTRIBUTION-WEIGHTED ROBUSTNESS RECONSTRUCTIBLE UNDER MEASURE/LOSS SURFACE**. The equal-total integer weights may be normalized to finite distributions, but the formal result does not require general probability theory. It does not settle continuous measures, stochastic transition dynamics, Bayesian uncertainty/calibration, unknown distribution shift, adversarial optimization, or semantic error severity.

The #41/#47/#53 results do **not** reduce learning mechanism, sample efficiency, biological motor chunking, unique or intrinsic hierarchical composition, arbitrary cross-world transfer, expertise, automaticity, practice history, general compression/resource efficiency, human semantic know-how, Skill acquisition, or Skill crystallization dynamics. Those stronger meanings require separate justification if RelayTheory needs them.

Issue #60 now adds a distinct process-versus-state constraint relevant to #55. In its finite model, two experience-to-state maps produce the same actual retained state and the same current readout while differing under a counterfactual experience change. A #41-competent policy can also coexist with the experience-insensitive formation map. Therefore neither final retained structure nor operational competence determines an experience-sensitive formation process in this scope.

This does **not** promote formation history, provenance, learning, or Crystallization into ontology. It only blocks their silent identification with the current retained state. Any later Crystallization claim must earn whatever additional formation, provenance, stabilization, or future-closure information it requires rather than hiding it inside a retained-state label.

Issue #69 further prevents `Memory` from becoming a monolithic retained-state type by separating accurate reconstruction from local experience-sensitive formation. Each can occur without the other under the same finite carrier and explicit readout, while a positive control satisfies both. These remain derived operational judgments over formation/readout structure, not current ontology primitives. A later common-substrate account must preserve this distinction rather than hiding it in a Memory/Crystal label.

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
