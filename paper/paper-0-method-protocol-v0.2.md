# Structural Cartography of Scientific Claims
## An Integration Protocol for Adversarial Basis Construction, Blinded Structural Comparison, and Held-Out Validation

**Paper 0 — methodological preprint v0.2**

**Status:** preprint-ready integration-method manuscript.  
**Novelty classification:** `PAPER0_INTEGRATION_NOVELTY_ONLY`.  
**Cross-domain validity:** not established.  
**Architecture consequence:** NONE.

---

## Abstract

Scientific literatures often reuse the same construct label for operationally different claims and use different labels for claims that may preserve similar dependency, temporal, intervention, or criterion structure. Existing methods already address many parts of this problem: Carnapian explication sharpens concepts; counterexample-guided abstraction refinement iterates between abstraction and counterexample; multiverse analysis and preregistration expose or constrain analyst degrees of freedom; structure-mapping and ontology matching compare relational structure across heterogeneous descriptions; systematic review practices preserve source provenance; and formal methods provide mature notions of refinement and forgetting. This paper does not claim novelty for those components.

The contribution proposed here is an integration protocol for claim-level comparison under unstable terminology. The protocol couples five constraints in a fixed order: (1) adversarial construction of a bounded working basis by deletion, reconstruction, counterexample, and anti-trivialization tests; (2) pre-outcome freezing of the representational and comparison contract; (3) source-grounded decomposition and mapping that are blinded to answer-bearing construct labels and authority metadata while retaining the semantic content needed to interpret the source claim; (4) comparison through explicit equivalence, refinement, incomparability, and residual semantics under bounded expressivity; and (5) held-out checks of mapping coverage, reproducibility, label leakage, discrimination, and bespoke-encoding pressure. The method treats residuals and abstentions as informative boundaries rather than as failures to be hidden.

The paper's novelty claim is intentionally narrow. It does not assert a uniquely correct ontology, semantics-free interpretation, demonstrated cross-domain validity, superiority to existing methods, or historical firstness. The defended claim is that the coupled end-to-end protocol provides a falsifiable comparison contract for testing whether scientific claims can be compared structurally without allowing inherited labels or post-outcome analyst freedom to determine the result. A synthetic worked example illustrates the protocol without importing empirical outcomes from downstream applications.

## 1. Problem and Scope

Scientific comparison is often organized around inherited names. A literature may speak of *memory*, *learning*, *skill*, *resilience*, *capability*, *complexity*, or another construct as if a repeated label denoted one stable object of comparison. Yet two uses of the same label can differ in state variables, causal dependencies, temporal horizons, success criteria, intervention families, partitions, or resource assumptions. Conversely, differently named claims can preserve much of the same operational structure.

Two symmetric errors follow.

First, **nominal convergence can conceal structural fission**: a repeated label can group claims whose operational commitments differ in ways relevant to the scientific question.

Second, **nominal plurality can conceal structural convergence**: different labels can obscure claims that preserve the same declared discriminating structure.

The methodological question is therefore narrower than the metaphysical question of what a construct “really is”:

> Given a scientific literature containing heterogeneous claims, how can source-grounded claims be compared while preventing inherited construct labels, authority metadata, and post-outcome analytical flexibility from determining the comparison?

This paper proposes a protocol for that task. It is an integration contribution, not a claim that its component techniques are new.

The intended object of comparison is a **source-grounded scientific claim**. A construct name remains useful as provenance and as an object of later interpretation, but it is not permitted to assign a structural representation by itself.

## 2. Novelty Boundary

### 2.1 What is established prior art

The following ideas are treated here as inherited methodology rather than Paper 0 novelty.

**Conceptual explication.** Carnap's method of explication replaces an unclear or inexact concept with a clearer and more exact one under explicit desiderata. Paper 0 therefore does not claim novelty for the general idea of replacing inherited conceptual vocabulary with a more precise working representation (Carnap 1950).

**Counterexample-guided abstraction and refinement.** CEGAR iterates between an abstraction, counterexample analysis, and refinement of the abstraction. The adversarial posture of attempting to break a reduced representation, and then refining when a discriminating counterexample survives, is therefore not new (Clarke et al. 2003).

**Analyst-choice and robustness analysis.** Multiverse analysis exposes results across many reasonable analytical choices rather than allowing one discretionary path to remain hidden (Steegen et al. 2016). More generally, preregistration and Registered Reports separate design commitments from observed outcomes (Chambers and Tzavella 2022). Paper 0 borrows this family of controls rather than claiming to invent pre-outcome constraint.

**Relational structure mapping.** Structure-Mapping Theory explicitly gives priority to relations over object attributes and defines mappings by structural properties rather than domain-specific content (Gentner 1983). Formal Concept Analysis mathematically represents concept hierarchies from object-attribute relations (Ganter and Wille 1999). Ontology matching finds correspondences such as equivalence, subsumption, and disjointness across heterogeneous ontologies (Euzenat and Shvaiko 2013). Paper 0 therefore does not claim that relational or cross-vocabulary mapping is new.

**Evidence provenance and structured review.** Systematic-review methodology already requires explicit scope, source selection, data collection, and traceable evidence handling. Paper 0 adopts that discipline for claim decomposition rather than presenting source traceability as a new method.

**Measurement invariance.** Psychometrics provides formal ways to ask whether measurement structure is invariant across groups or populations (Meredith 1993). Paper 0 differs in object and workflow, but it does not claim novelty for the general idea of formally testing preserved structure across heterogeneous instances.

**Refinement and forgetting.** Refinement calculi and knowledge-representation research provide established formal notions of refinement and of forgetting or variable elimination while preserving specified structure (Morgan and Vickers 1990; Wang, Sattar, and Su 2005). Paper 0 borrows these terms for protocol-specific comparison relations.

**Severe or hostile testing.** The philosophical idea that a claim should face tests capable of exposing error is not novel to this protocol (Mayo 1996).

**Science mapping and literature-based discovery.** Bibliometric science mapping and literature-based discovery already organize or connect scientific literatures at scale (Cobo et al. 2011; Cestnik et al. 2025). Paper 0's use of the word *atlas* is not a novelty claim.

### 2.2 What is combined

Paper 0 combines those inherited elements into a single claim-comparison contract with a required temporal order:

```text
candidate distinctions
-> adversarial reduction / reconstruction / counterexample testing
-> surviving discriminating structure
-> frozen working comparison contract
-> source-grounded decomposition
-> construct-label / authority-blinded structural mapping
-> explicit structural relations and residuals
-> held-out validation
```

The ordering is essential. Construction freedom is exercised before target outcomes are inspected. Mapping operates inside a frozen schema. Unsupported structure becomes abstention or residual rather than a claim-specific extension. Held-out literature tests the frozen system rather than silently rewriting it.

### 2.3 What the paper claims

The substantive claim is limited to the following integration:

> A bounded protocol can make claim-level structural comparison auditable by coupling adversarial basis construction, pre-outcome freezing, source-grounded and label/authority-blinded mapping, explicit relation semantics, residual handling, and held-out tests of non-vacuity and stability.

The present prior-art audit did not identify a single near-neighbor that was shown to enforce this whole contract as one method. That observation supports an integration contribution only. It does not establish historical firstness.

### 2.4 What the paper does not claim

Paper 0 does **not** claim:

- that explication, counterexample-guided refinement, preregistration, structure mapping, ontology matching, evidence provenance, measurement invariance, refinement, forgetting, or held-out testing are new;
- that the working basis is unique, complete, optimal, or metaphysically fundamental;
- that construct labels can or should be removed from the original source text in a way that makes interpretation semantics-free;
- that structural equivalence entails semantic identity, theoretical synonymy, causal equivalence, metaphysical identity, or practical interchangeability;
- that freezing eliminates all researcher degrees of freedom;
- that a successful held-out test establishes truth or ontology completeness;
- that the protocol has demonstrated domain-general validity;
- that AI is a scientific authority or a source of methodological novelty;
- that the protocol has been shown superior to its strongest component methods;
- that no earlier integrated method exists.

The last point remains a live falsification condition.

## 3. Functional Relation to the Strongest Near-Neighbors

The relevant prior art is not best understood as a list of vaguely related literatures. The important comparison is functional: which part of the target workflow does each method already perform, and which coupling problem remains unresolved?

### 3.1 Explication versus adversarial basis construction

Carnapian explication and related conceptual-engineering traditions already license replacing an imprecise concept by a more exact one for specified purposes. That directly undermines any claim that Paper 0 newly discovers the strategy of reconstructing inherited concepts.

The narrower role of adversarial basis construction is different. It does not begin by asking only which replacement concept would be clearer or more useful. It asks whether a candidate distinction carries independent discriminating information relative to a declared comparison surface. The distinction is retained only if deletion or quotienting produces an information gap that cannot be reconstructed from the retained structure under the declared tests. This is closer in operational shape to abstraction/refinement than to explication alone.

### 3.2 CEGAR versus literature-level forging

CEGAR is the strongest near-neighbor for the attack-and-refine loop. It constructs an abstraction, checks it, analyzes counterexamples, and refines the abstraction when the counterexample is spurious or exposes insufficient abstraction (Clarke et al. 2003). Paper 0 therefore treats counterexample-guided refinement as borrowed.

The remaining difference is the object and epistemic contract. CEGAR is designed for formal models with a property to be verified. Paper 0 addresses heterogeneous source claims whose representation is itself under construction, whose source support can be incomplete, and whose conventional labels can leak the intended answer. The protocol therefore adds source provenance, label/authority blinding, abstention, residual semantics, and a freeze between construction and atlas evaluation. These are integration constraints, not a new abstraction-refinement algorithm.

### 3.3 Structure mapping, FCA, and ontology matching versus claim-level comparison

Gentner's structure-mapping framework shows that mapping can be governed by relational organization rather than by surface attributes. Ontology matching provides mature machinery for finding correspondences among heterogeneous knowledge structures, including equivalence and subsumption. FCA derives concept lattices from formal object-attribute contexts.

Paper 0 does not compete with these methods as a general matching formalism. Instead, it specifies the conditions under which a scientific claim is admitted to the matching problem: the claim must be source-grounded, represented under a frozen schema, insulated from answer-bearing construct and authority metadata, and rejected into abstention or residual when the source does not license the required structure. The protocol's primary target is not ontology integration but the auditability of comparisons among scientific claims.

### 3.4 Multiverse analysis, preregistration, and Registered Reports versus freeze discipline

Multiverse analysis reveals how conclusions depend on reasonable analytical choices. Preregistration and Registered Reports move key commitments before outcome inspection. Paper 0 imports both lessons.

Its freeze stage should therefore be understood modestly. It does not make analyst judgment disappear. It makes the judgment surface explicit and versioned. The protocol requires the analyst to declare the basis semantics, decomposition schema, admissible relation types, comparison criteria, residual policy, source-replacement rules, and validation metrics before target atlas outcomes are inspected. If those commitments later change, the system receives a new version rather than retroactively treating the revision as if it had governed the original analysis.

### 3.5 Measurement invariance versus structural claim equivalence

Measurement-invariance analysis asks whether measurement relations are preserved across populations or groups under a specified latent-variable model (Meredith 1993). It is therefore a genuine structural-comparison predecessor.

Paper 0's problem is less statistically specific and more representationally prior. Heterogeneous source claims may not share a measurement instrument, construct name, latent-variable model, or even a common operational vocabulary. The protocol therefore places source-grounded decomposition and representational qualification before any equivalence relation is evaluated. Where measurement invariance is available and appropriate, it can be one domain-specific probe inside the wider protocol rather than something Paper 0 replaces.

### 3.6 Systematic review, science mapping, and LBD versus structural atlas construction

Systematic review supplies disciplined evidence acquisition and traceability. Science mapping supplies bibliometric maps of conceptual, intellectual, and social structure. LBD supplies methods for discovering associations across literatures and increasingly emphasizes reproducible pipelines. These methods are therefore direct predecessors for provenance, large-scale literature processing, and reproducibility.

The proposed atlas differs in unit of analysis. Its nodes are not papers, citations, keywords, or automatically induced topics by default. They are source-grounded claims transformed under a frozen comparison contract. The atlas records declared structural relations among those transformed claims and separately records representational residuals. Whether that distinction is useful in practice is an empirical question for downstream applications, not something established by definition.

## 4. Protocol Contract

### 4.1 Objects and surfaces

For a domain or bounded literature `D`, define:

- `C_D`: the eligible source-grounded claims;
- `F_D`: the declared **forging surface**, i.e., the phenomena and discriminators the basis-construction stage is required to preserve;
- `K_D`: the construction literature used to propose, attack, and freeze the working comparison system;
- `V_D`: the held-out validation literature, disjoint from the outcome-determining construction surface under the declared split;
- `B_D^v`: a versioned working basis;
- `R_D^v`: the versioned representational and comparison rules associated with `B_D^v`;
- `S(B_D^v, R_D^v)`: the admissible representation family under the frozen version.

The version identifier is part of every reported result.

The protocol is not committed to one universal basis across domains. Even within a single domain, different scientific questions may justify different forging surfaces and therefore different working bases.

### 4.2 Step 1 — declare the comparison question and forging surface

Before candidate coordinates are evaluated, the analyst must state what distinctions the comparison is required to preserve.

A forging surface should include, as applicable:

- target claim class;
- admissible source types;
- phenomena whose distinction matters to the comparison;
- admissible probes or interventions;
- temporal and resource scope;
- allowed approximation or stochastic tolerance;
- explicit out-of-scope distinctions.

Without a declared forging surface, “independence” of a candidate coordinate is undefined: a distinction can be redundant for one question and essential for another.

### 4.3 Step 2 — build a candidate ledger

Candidate structure must be recorded before it is accepted or rejected. Each ledger item should include:

```text
candidate_id
provenance
candidate semantics
why it might be discriminating
known reductions
known counterexamples
allowed reconstruction operations
current status
```

Candidate provenance can include theory, prior literature, formal decomposition, empirical practice, or analyst proposal. Provenance does not grant primitive status.

The ledger makes the initial choice surface visible. It does not make candidate generation objective.

### 4.4 Step 3 — adversarially forge the basis

For candidate distinction `x` relative to retained structure `R`, attempt to destroy the need for `x`.

The default attack family is:

1. **deletion:** remove `x`;
2. **reconstruction:** attempt to recover the relevant content of `x` from `R`;
3. **quotient / forgetting:** identify whether `x` is only a presentation distinction that can be collapsed without losing required discrimination;
4. **reindexing / renaming:** test whether the distinction survives a change of names or representatives;
5. **alternative decomposition:** test whether the same discrimination is available under a smaller decomposition;
6. **counterexample search:** seek a pair agreeing on `R` but differing on a required phenomenon;
7. **criterion perturbation:** test dependence on the evaluation criterion;
8. **probe perturbation:** test dependence on the selected intervention or observation family;
9. **partition perturbation:** test dependence on a chosen subsystem boundary;
10. **temporal / resource decomposition:** test whether an apparent primitive is recoverable from time or resource structure;
11. **anti-trivialization:** reject reductions that merely rename the deleted concept inside a generic relation.

A candidate survives only if the retained structure fails to reconstruct a required distinction and the failure can be witnessed on the declared forging surface.

The survival claim is therefore local:

> Relative to `F_D` and the declared attack family, the current representation requires an independently discriminating distinction corresponding to `x`.

This does not establish uniqueness, completeness, or metaphysical fundamentality.

### 4.5 Reconstruction and counterexample witnesses

A reduction decision should be auditable through one of two witness types.

**Reconstruction witness.** A reproducible transformation from retained structure `R` to the information previously carried by candidate `x`, sufficient for every declared discriminator in scope.

**Independence witness.** A pair of admissible cases `a,b` such that:

```text
R(a) = R(b)
```

under the retained representation, while the declared comparison surface requires them to remain distinct.

If neither witness can be produced, the correct status is `UNDERDETERMINED`, not automatic retention.

### 4.6 Stopping and basis-freeze point

Forging cannot be required to continue until “all possible attacks” have been tried. A finite stopping rule is therefore required.

A basis version may be frozen when:

1. the candidate ledger has no unresolved candidate required by the declared comparison question;
2. every retained coordinate has a recorded survival rationale or independence witness;
3. every deleted coordinate has a recorded reconstruction or out-of-scope rationale;
4. the declared attack family has been applied or explicitly marked inapplicable;
5. known analyst choice points have been enumerated;
6. the representation schema and relation inventory are specified;
7. no target-atlas outcome has been used to decide the freeze.

The freeze point is procedural, not ontological. Later counterexamples may justify `v+1`, but they do not retroactively rewrite results obtained under version `v`.

### 4.7 Step 4 — freeze the comparison contract

The frozen contract `R_D^v` should include, at minimum:

- basis dimensions and semantics;
- decomposition schema;
- admissible typed relation vocabulary;
- allowed representation changes;
- structural-equivalence criterion;
- refinement criterion;
- forgetting operations;
- incomparability rule;
- residual taxonomy;
- abstention rule;
- source selection and replacement rule;
- masking / blinding rule;
- analyst decision ledger;
- generic mapping rules;
- anti-vacuity controls;
- null or permutation controls where appropriate;
- held-out split and validation metrics;
- amendment and versioning rule.

A frozen contract reduces answer-bearing freedom. It does not eliminate judgment.

### 4.8 Step 5 — source-grounded claim decomposition

The comparison unit is a claim whose mapped components are traceable to source support.

Depending on the domain and claim type, decomposition may include:

- state or carrier structure;
- components, partitions, or candidate subsystems;
- dependency, transition, causal, constitutive, or correlational relations;
- observation or accessible-information structure;
- temporal order, duration, persistence, or horizon;
- resource or capacity constraints;
- criteria such as success, error, relevance, utility, or viability;
- provenance of those criteria;
- probe, task, transformation, manipulation, or intervention families;
- stochastic, approximate, or uncertainty structure;
- scope, quantification, and boundary conditions.

Every mapped component should have a source anchor or an explicit transformation rule from anchored source content.

When the source is insufficient, the allowed outcomes are:

- **abstention:** the source does not license a required decomposition decision;
- **bounded uncertainty:** multiple mappings remain licensed by the source and contract;
- **representational residual:** the source licenses structure that the frozen representation cannot preserve.

The analyst must not manufacture a complete representation merely because the schema has a field for it.

### 4.9 Step 6 — construct-label and authority blinding

The phrase **label-independent** is too strong if interpreted as semantics-free reading. Scientific claims cannot generally be understood while deleting all lexical and conceptual content.

The intended control is narrower:

> Mapping should be blinded to answer-bearing construct labels and authority metadata, while preserving the ordinary semantic content required to understand the claim.

Fields forbidden from determining the mapping may include:

- conventional construct label when it directly identifies the target comparison class;
- author identity;
- institution;
- venue prestige;
- citation count;
- expected theoretical lineage;
- sampling stratum if it leaks the desired relation;
- desired atlas cluster or comparison outcome.

The source content needed to understand states, dependencies, time, interventions, criteria, and scope is retained.

A practical test is:

> After answer-bearing labels and authority metadata are masked, can an analyst using only source-grounded content and the frozen contract reproduce the same mapping within the declared tolerance?

If not, the result is label- or authority-dependent.

### 4.10 Step 7 — map into a bounded structural representation

Define a partial mapping

```text
Phi_D^v : C_D -> S(B_D^v, R_D^v) ∪ {ABSTAIN, RESIDUAL}.
```

A representation can include:

```text
basis coordinates
+ typed dependency topology
+ temporal structure
+ probe / intervention structure
+ criteria and criterion provenance
+ partition structure
+ scope / quantification / constraints
+ approximation / uncertainty annotations
```

The schema must be bounded before target outcomes are inspected. Claim-specific new relation types or fields are forbidden inside the primary frozen analysis.

If a claim requires structure outside the schema, the primary result is a residual. A future schema version may incorporate the new structure, but the new version must not replace the original result in the primary evaluation.

## 5. Structural Relations

### 5.1 Equivalence

Two claims `c1` and `c2` are structurally equivalent under version `v` only when their mapped structures are equivalent under the explicitly permitted representation changes:

```text
Phi_D^v(c1) ≅_v Phi_D^v(c2).
```

The permitted transformations must be frozen. They can include semantics-free reindexing, graph isomorphism, or other domain-appropriate equivalences, but they cannot be invented after seeing a desired pair.

Equivalence under the protocol does not imply semantic identity of the full source texts.

### 5.2 Cross-label convergence and within-label fission

After labels are restored for interpretation:

- **cross-label convergence** occurs when differently named claims are structurally equivalent under the frozen contract;
- **within-label fission** occurs when claims carrying the same conventional label are non-equivalent under that contract.

These are descriptive results about a comparison system. They do not establish that the historical constructs are “really the same” or “really different.”

### 5.3 Strict refinement

`c2` strictly refines `c1` when `c2` preserves the structure represented by `c1` while adding independently discriminating structure under the frozen contract.

A strict-refinement report should identify the added structure and provide a forgetting witness.

### 5.4 Forgetting

For an allowed forgetting operation `Forget_J`, if

```text
Forget_J(Phi_D^v(c2)) ≅_v Phi_D^v(c1),
```

then the protocol may report that `c2` reduces to `c1` after forgetting the declared structure `J`.

The operation is not a newly invented logical forgetting operator. It is a protocol-level use of an inherited formal idea.

### 5.5 Incomparability

Two claims can overlap without being equivalent and without either being a refinement of the other. The protocol records `INCOMPARABLE` rather than forcing all pairs into an ordered similarity scale.

### 5.6 Residual semantics

A **representational residual** is not merely “whatever differs.” It occurs when a source-grounded claim cannot be represented under the frozen contract without one of the following:

1. adding an unlicensed coordinate or relation type;
2. adding a claim-specific encoding rule;
3. discarding source-grounded structure that the contract requires preserving;
4. violating a scope or provenance constraint.

Residuals should be typed, for example:

```text
OUT_OF_SCHEMA_STRUCTURE
UNLICENSED_RELATION_TYPE
UNLICENSED_PARTITION
PROBE_FAMILY_OUT_OF_SCOPE
CRITERION_PROVENANCE_UNREPRESENTABLE
TEMPORAL_STRUCTURE_UNREPRESENTABLE
RESOURCE_STRUCTURE_UNREPRESENTABLE
```

Residuals must be distinguished from:

- source inaccessibility;
- eligibility exclusion;
- extraction failure;
- decomposition abstention;
- ordinary non-equivalence;
- statistical uncertainty.

The residual rate is therefore a diagnostic of representational pressure, not a direct measure of scientific importance.

## 6. Anti-Vacuity and Anti-Leakage Controls

A sufficiently expressive structural language can make almost any pair look equivalent or different if the analyst may add fields, relation types, partitions, or probes after inspecting the desired conclusion. The protocol therefore requires explicit pressure against answer-bearing flexibility.

### 6.1 Bounded schema

The primary representation language is frozen before atlas outcomes. New fields or relation types trigger residuals or a new method version, not an in-place repair.

### 6.2 Name and authority deletion

Answer-bearing construct labels, authors, institutions, venues, citation counts, and expected lineage are removed from the mapping input where feasible.

### 6.3 Basis-inventory ablation

Claims with the same set of coordinates but different topology must remain distinguishable when topology is part of the declared comparison surface. This prevents an eight-bit or bag-of-features representation from masquerading as a structural mapping.

### 6.4 Topology ablation

The analyst should test whether removing topology, temporal order, or dependency type collapses distinctions the protocol was designed to preserve.

### 6.5 Provenance constraints

Criteria, probes, partitions, and scope restrictions cannot be introduced solely because they create a preferred classification. Each must be source-grounded or independently specified by the frozen contract.

### 6.6 Generic-rule reuse

For each mapping, record whether the result was produced by a previously declared generic rule or required a bespoke exception. A high bespoke-encoding rate is evidence against the protocol's non-vacuity.

### 6.7 Negative and null controls

Where meaningful, use target permutations, shuffled labels, synthetic same-inventory/different-topology pairs, and deliberately incompatible claims to test whether the system detects structure rather than merely accommodating input.

### 6.8 Explicit abstention and residuals

Forced fit is not preferable to failure. A protocol that reports more residuals can be more informative than one that achieves nominally perfect coverage by expanding the schema after every difficult case.

## 7. Analyst Degrees of Freedom and Reproducibility

The method does not promise objectivity by eliminating analysts. It instead requires that consequential judgment be visible.

A reproducible implementation should retain a **decision ledger** containing:

```text
decision_id
stage
available options
selected option
rationale
source or rule authority
whether the choice was frozen pre-outcome
whether an alternative was tested
version introduced
```

At minimum, the ledger should cover:

- candidate-coordinate generation;
- scope decisions;
- decomposition rules;
- ambiguity handling;
- masking rules;
- admissible relation types;
- equivalence tolerances;
- residual assignments;
- source replacements;
- post-freeze amendments.

### 7.1 Analyst replication

When feasible, a second analyst should independently execute a subset of forging or mapping decisions under the same frozen contract. The objective is not perfect agreement. It is to identify which outputs are reproducible consequences of the contract and which remain underdetermined by it.

Disagreement should be classified rather than averaged away, for example:

```text
SOURCE_AMBIGUITY
SCHEMA_AMBIGUITY
RULE_AMBIGUITY
ANALYST_ERROR
GENUINE_UNDERDETERMINATION
```

### 7.2 Versioned amendment rule

After freezing, an amendment is allowed only if:

1. the triggering evidence is recorded;
2. the new rule is assigned a new version;
3. the original primary result remains preserved;
4. the new version is evaluated prospectively on a newly protected surface where possible.

This is the main mechanism by which the protocol separates learning from retrospective answer repair.

## 8. Held-Out Validation

Held-out validation tests the **frozen comparison system**, not the truth of the scientific claims being mapped.

Let `V_D` be a literature surface that did not determine the primary basis, representation schema, or comparison rules. The validation asks whether the frozen system remains:

- **mappable:** eligible claims can be represented without systematic failure;
- **reproducible:** repeated mappings agree within the declared tolerance;
- **non-vacuous:** mapping does not depend on pervasive bespoke exceptions;
- **discriminating:** predeclared structural differences are preserved;
- **leakage-resistant:** masking answer-bearing labels and authority metadata does not destroy the mapping;
- **residual-honest:** out-of-schema structure is exposed rather than repaired in place.

Useful validation metrics include:

```text
eligible-claim coverage
abstention rate
representational residual rate
bespoke-rule rate
generic-rule reuse rate
analyst agreement / disagreement taxonomy
label-mask sensitivity
topology-ablation sensitivity
null / permutation contrast
```

A successful held-out test does **not** establish:

- that the basis is uniquely correct;
- that the mapped claims are true;
- that structural equivalence entails semantic identity;
- that the method generalizes to another domain;
- that future literature will not expose a missing coordinate.

A failure can be scientifically informative because it localizes the pressure: source ambiguity, schema weakness, excessive expressivity, label leakage, or genuine basis-extension demand.

## 9. Synthetic Worked Example

This example is deliberately artificial. It demonstrates the protocol mechanics without importing an empirical result from a downstream scientific application.

Suppose a bounded literature contains three claims, shown here after answer-bearing construct names and author metadata have been masked.

**Claim A.** After exposure to input `u`, system state `s` changes to `s'`. After a delay `Δt`, a probe `p` is applied. Success is defined by criterion `q`: the probe-dependent output must exceed threshold `θ` relative to a pre-exposure baseline.

**Claim B.** A differently named literature states that input `u*` induces an internal state transition. After the same declared horizon class, a retrieval-like intervention `p*` tests whether an output meets an independently specified success criterion with the same dependency and temporal pattern.

**Claim C.** A third claim has the same structure as A but additionally requires that the post-exposure state remain recoverable under a bounded resource budget `r <= R`, and the source treats that budget as part of the phenomenon rather than as an incidental implementation limit.

Assume the frozen basis contains:

```text
S  state/carrier
K  transition/dependency
T  temporal structure
P  probe/intervention
Q  criterion + provenance
C  resource constraint
```

and the frozen representation preserves typed edges and temporal order.

A and B may map to isomorphic structures after semantics-free reindexing of local identifiers. If so, the protocol can report **structural equivalence under version v**, even if the historical construct labels differ. It cannot report semantic identity of the full theories.

C contains all structure represented in A plus a source-grounded resource constraint `C`. If forgetting `C` from the representation of C yields an object equivalent to A, the protocol can report **strict refinement with forgetting witness C**.

Now introduce **Claim D**, whose source makes a recurrent two-way causal loop between system and environment essential, while the frozen representation permits only acyclic dependency edges. The primary analysis must not add a recurrent-edge type for D alone. D receives a typed representational residual such as `UNLICENSED_RELATION_TYPE`. The residual can motivate a future version, but it cannot rewrite the original frozen result.

This toy example illustrates four features at once:

1. construct names do not assign mappings;
2. ordinary source semantics remain available for decomposition;
3. refinement requires an explicit forgetting witness;
4. difficult claims can remain residual rather than forcing schema expansion.

## 10. Evaluation and Falsification

The protocol is a method proposal. Its strongest claims remain open until tested.

The method should be rejected, reduced, or materially revised if any of the following occurs.

1. **Integrated prior-art collapse.** A prior method is shown to enforce substantially the same end-to-end contract.
2. **Forging collapse.** Adversarial basis construction adds no operational constraint beyond familiar explication or abstraction/refinement.
3. **Candidate-instability collapse.** Reasonable analysts produce incompatible bases even after the forging surface and candidate rules are fixed, with no stable explanation of the divergence.
4. **Decomposition instability.** Source-grounded claims cannot be mapped reproducibly under a fixed schema.
5. **Label dependence.** Masking answer-bearing labels or authority metadata destroys the apparent atlas structure.
6. **Expressivity collapse.** Arbitrary claims can be made equivalent or non-equivalent through generic but unconstrained representational choices.
7. **Bespoke-encoding collapse.** Successful coverage depends on frequent claim-specific exceptions.
8. **Residual instability.** Residual assignment depends on knowing the desired downstream result.
9. **Post-outcome repair.** The system requires repeated retuning after atlas outcomes are inspected.
10. **Held-out collapse.** The frozen system fails on untouched literature even within the construction domain.
11. **Portability collapse.** A future independent-domain application cannot reconstruct an analogous workflow without reintroducing domain labels as primitive coordinates.

The current manuscript does not report an empirical victory over these failure conditions.

## 11. AI-Assisted Implementation

AI can reduce the cost of literature search, segmentation, decomposition proposal, counterexample generation, mapping proposal, and consistency checking. None of those uses makes the model an epistemic authority.

A model-assisted implementation should preserve the same constraints as a manual one:

- every scientific assertion must remain source-grounded;
- generated citations or quotations must be verified;
- decomposition must be auditable against source anchors;
- answer-bearing construct and authority metadata must be masked where required;
- the model may not silently expand the frozen schema;
- uncertainty must not be converted into confident completion;
- outputs must remain reproducible enough to inspect and challenge.

AI is therefore an implementation option, not part of the novelty claim.

## 12. Relationship to Downstream Applications

Paper 0 is a methodology paper. It does not own the scientific results of any domain application.

A downstream construction paper may use the protocol to forge and freeze a domain-specific working basis and produce a bounded structural atlas. A later validation paper may then test that frozen system at larger scale.

The methodological separation is:

```text
Paper 0
  protocol / integration contract

Paper 2
  domain-specific coordinate-system construction
  + bounded designed atlas

Paper 3
  frozen-system large-scale validation
```

Paper 0 may cite already-frozen methodological artifacts from a downstream application as provenance for implementability, but it must not use unpublished atlas outcomes to tune the method.

A future independent-domain replication would be required before any strong cross-domain claim becomes defensible.

## 13. Limitations

The protocol has several limitations even if it functions as intended.

First, **candidate generation remains theory-laden**. A decision ledger exposes but does not eliminate the fact that analysts choose which distinctions to test.

Second, **source interpretation remains semantic**. Construct-label masking cannot make scientific reading syntax-only. The protocol blocks answer-bearing labels and authority cues, not the ordinary meaning required to understand a claim.

Third, **equivalence is representation-relative**. Two claims can be equivalent under one frozen comparison contract and non-equivalent under another legitimate contract aimed at a different question.

Fourth, **bounded expressivity creates residuals by design**. A low residual rate is not automatically better than a high one.

Fifth, **held-out validation is local**. It tests one frozen system on one protected surface; it does not prove domain-generality.

Sixth, **integration novelty is vulnerable to later prior-art discovery**. Because each component has substantial precedent, a sufficiently close integrated predecessor could collapse the paper's remaining novelty claim.

These are not side notes. They define the scope of the method.

## 14. Status Decision

The hostile prior-art review supports the following classification:

```text
PAPER0_INTEGRATION_NOVELTY_ONLY
```

The reason is asymmetric.

The audit provides strong evidence that the protocol's components are individually established: conceptual explication, abstraction/refinement, robustness analysis, structure mapping, ontology matching, evidence provenance, pre-outcome freezing, invariance testing, formal refinement/forgetting, and severe testing all have substantial prior art.

At the same time, the reviewed near-neighbors do not by themselves establish a complete collapse of the ordered integration contract defended here. That remaining claim is therefore best stated as a protocol integration contribution, not as method-component novelty.

The status should be downgraded to `PAPER0_PRIOR_ART_COLLAPSE` if a prior framework is found that already enforces substantially the same sequence of basis attack, freeze, source-grounded blinded mapping, bounded relation semantics, residual handling, and held-out validation for scientific-claim comparison.

## 15. Conclusion

When scientific construct vocabularies are unstable, comparison cannot safely assume that names are already the right coordinates. But replacing names with structure is not itself a new idea. Neither are counterexample-guided refinement, preregistration, structure mapping, ontology matching, evidence provenance, refinement, forgetting, or held-out testing.

The narrower proposal is to bind these established ideas into one auditable comparison contract. Candidate distinctions are attacked before being retained. The working representation is frozen before target outcomes. Claims are decomposed from sources rather than from construct stereotypes. Answer-bearing labels and authority cues are masked while source semantics are preserved. Structural relations are defined under bounded expressivity. Unsupported structure becomes abstention or residual instead of a bespoke extension. Held-out literature then tests the frozen system rather than silently rewriting it.

The resulting question is deliberately modest:

> Under one explicitly versioned comparison contract, which source-grounded claims preserve the same declared structure, which add or lose structure, which remain incomparable, and which fall outside the current representation?

Whether this integration is scientifically useful is not settled by the protocol's definition. It must be earned by reproducible domain applications, hostile comparison with prior methods, and held-out failure tests.

---

## References

Carnap, R. (1950). *Logical Foundations of Probability*. University of Chicago Press.

Cestnik, B., Kastrin, A., Koloski, B., & Lavrač, N. (2025). Make literature-based discovery great again through reproducible pipelines. *Advances in Intelligent Data Analysis XXIII*, 261-273. https://doi.org/10.1007/978-3-031-91398-3_20

Chambers, C. D., & Tzavella, L. (2022). The past, present and future of Registered Reports. *Nature Human Behaviour, 6*, 29-42. https://doi.org/10.1038/s41562-021-01193-7

Clarke, E. M., Grumberg, O., Jha, S., Lu, Y., & Veith, H. (2003). Counterexample-guided abstraction refinement for symbolic model checking. *Journal of the ACM, 50*(5), 752-794. https://doi.org/10.1145/876638.876643

Cobo, M. J., López-Herrera, A. G., Herrera-Viedma, E., & Herrera, F. (2011). Science mapping software tools: Review, analysis, and cooperative study among tools. *Journal of the American Society for Information Science and Technology, 62*(7), 1382-1402. https://doi.org/10.1002/asi.21525

Euzenat, J., & Shvaiko, P. (2013). *Ontology Matching* (2nd ed.). Springer. https://doi.org/10.1007/978-3-642-38721-0

Ganter, B., & Wille, R. (1999). *Formal Concept Analysis: Mathematical Foundations*. Springer. https://doi.org/10.1007/978-3-642-59830-2

Gentner, D. (1983). Structure-mapping: A theoretical framework for analogy. *Cognitive Science, 7*(2), 155-170. https://doi.org/10.1207/s15516709cog0702_3

Higgins, J. P. T., Thomas, J., Chandler, J., Cumpston, M., Li, T., Page, M. J., & Welch, V. A. (Eds.). (2024). *Cochrane Handbook for Systematic Reviews of Interventions* (Version 6.5). Cochrane.

Mayo, D. G. (1996). *Error and the Growth of Experimental Knowledge*. University of Chicago Press.

Meredith, W. (1993). Measurement invariance, factor analysis and factorial invariance. *Psychometrika, 58*(4), 525-543. https://doi.org/10.1007/BF02294825

Morgan, C., & Vickers, T. (1990). Types and invariants in the refinement calculus. *Science of Computer Programming, 14*(2-3), 281-304. https://doi.org/10.1016/0167-6423(90)90024-8

Steegen, S., Tuerlinckx, F., Gelman, A., & Vanpaemel, W. (2016). Increasing transparency through a multiverse analysis. *Perspectives on Psychological Science, 11*(5), 702-712. https://doi.org/10.1177/1745691616658637

Wang, K., Sattar, A., & Su, K. (2005). A theory of forgetting in logic programming. *Proceedings of the Twentieth National Conference on Artificial Intelligence (AAAI-05)*, 682-687.