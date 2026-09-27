# Toward a Structural Cartography of Scientific Claims
## A Protocol for Adversarial Basis Construction and Label-Independent Comparison

**Paper 0 — methodological working manuscript v0.1**

**Status:** claim-freezing draft for hostile prior-art review.  
**Novelty status:** unresolved.  
**Cross-domain validity:** not established.  
**Architecture consequence:** NONE.

---

## Abstract

Scientific literatures frequently use the same construct label for structurally different claims and different labels for structurally similar claims. This paper proposes a protocol for comparing such claims without treating inherited terminology as the primary analytical unit. The method first subjects candidate constructs and primitives to adversarial reduction, reconstruction, counterexample, and anti-trivialization tests. The discriminating structure that survives this forging stage is frozen as a working comparison basis rather than asserted as a final ontology. Source-grounded claims are then decomposed and mapped into richer structural objects that preserve dependency topology, temporal order, probes or interventions, criteria and their provenance, partitions, constraints, scope, and uncertainty where relevant. Comparisons distinguish structural equivalence, cross-label convergence, within-label fission, refinement, forgetting, incomparability, and residual structure. Basis semantics, mapping rules, and comparison criteria are frozen before target outcomes are inspected, and the resulting system is evaluated on held-out literature. The proposal is methodological rather than ontological: structural equivalence does not entail semantic or metaphysical identity, and a successful working basis is not claimed to be unique or complete. The present version fixes the protocol for hostile prior-art review; it does not yet claim methodological novelty or domain-general validity.

## 1. The Problem

Scientific concepts are often inherited as names before they are available as comparable structures. A literature may speak of memory, learning, skill, belief, resilience, capability, complexity, or other constructs as if the repeated label identified one stable object of comparison. Yet the same word can support different operational commitments across papers, while different words can encode materially similar dependencies, criteria, temporal relations, or intervention structures.

This creates two symmetric risks.

First, **nominal convergence can hide structural fission**. Two papers can use the same construct label while requiring different states, temporal horizons, success criteria, causal dependencies, partitions, or probes.

Second, **nominal plurality can hide structural convergence**. Two papers can use different construct labels while preserving the same discriminating structure under the comparison question at hand.

The methodological target of this paper is therefore not to decide what a construct “really is.” It is narrower:

> Given a scientific literature containing heterogeneous claims, how can those claims be compared without allowing inherited labels, prestige, or presentation conventions to determine the comparison outcome?

The proposal treats construct names as provenance to be restored after analysis rather than as privileged coordinates of the analysis itself.

## 2. Methodological Target

The candidate protocol has eight stages:

```text
existing theories / constructs
-> adversarial reduction and reconstruction
-> surviving discriminating structure
-> frozen working basis
-> source-grounded claim decomposition
-> label-independent structural mapping
-> structural atlas
-> held-out validation
```

For compactness:

```text
Forge -> Freeze -> Decompose -> Map -> Compare -> Atlas -> Validate
```

The protocol is intended to be repeatable across domains, but this paper does not assume that one fixed basis transfers across domains. A cognitive-science application may yield one working basis; medicine, organization studies, or another field may yield another. The candidate generality lies in the **procedure for producing and testing the basis**, not in a universal list of coordinates.

## 3. Adversarial Basis Forging

### 3.1 No a priori primitive list

The method does not begin by declaring that familiar construct names are fundamental dimensions. Nor does it begin by selecting an ontology because it is conventional, intuitive, or computationally convenient.

Instead, candidate structure is subjected to attempted destruction.

For a candidate distinction `x`, ask whether its discriminating content can be reconstructed from a smaller retained structure `R`. The relevant tests may include:

- deletion;
- explicit reconstruction;
- quotient or forgetting;
- reindexing or renaming;
- alternative decomposition;
- counterexample search;
- criterion perturbation;
- probe perturbation;
- partition perturbation;
- temporal decomposition;
- resource decomposition;
- anti-trivialization.

If two systems can agree on all retained structure while differing on a phenomenon the analysis must preserve, the deleted distinction carries independent information on the declared forging surface. If no such discriminator survives and the candidate can be reconstructed, the method does not retain a separate primitive merely because a literature names one.

### 3.2 Anti-trivialization

Reduction into generic vocabulary is not sufficient.

Replacing “Skill” with an arbitrary field named `skill_relation`, or replacing “Ownership” with `owns(a,b)`, does not expose lower-level structure. A successful reduction must preserve the required distinction through independently specified structure whose semantics do not merely restate the removed label.

A candidate dimension therefore survives only when its removal creates an information gap that cannot be reconstructed from the retained comparison surface.

### 3.3 Output of forging

The forging stage yields a **working basis**, not a final ontology.

Let a domain be `D`, its declared forging surface be `F_D`, and the resulting basis be `B_D`. The warranted claim is only:

> Relative to `F_D`, the coordinates in `B_D` survived the attempted reductions used to construct the current comparison system.

The protocol does not infer that `B_D` is unique, complete, metaphysically fundamental, or optimal for every scientific question.

## 4. Freezing the Working Basis

The working basis must be frozen before the target atlas is inspected.

Freezing should include, where applicable:

- basis dimensions and their semantics;
- admissible relation types;
- decomposition schema;
- mapping rules;
- equivalence criteria;
- refinement criteria;
- forgetting rules;
- incomparability rules;
- residual policy;
- null controls;
- source-selection and replacement rules;
- analysis metrics.

If later evidence requires revision, the revised system receives a new version. Results generated under the earlier frozen system remain results of that earlier system and are not silently recomputed as if the revision had been known in advance.

The methodological purpose is to separate **construction freedom** from **evaluation outcome**.

## 5. Source-Grounded Claim Decomposition

The primary unit of comparison is a source-grounded claim, not a construct label.

A decomposition should recover only structure supported by the source. Depending on domain and claim type, that may include:

- state or carrier structure;
- components, partitions, or candidate subsystems;
- dependency, coupling, transition, causal, constitutive, or correlational relations;
- observation or accessible-information structure;
- temporal ordering, persistence, history, or horizon;
- resource or capacity constraints;
- success, error, relevance, utility, viability, or other criteria;
- provenance of those criteria;
- probe, task, transformation, manipulation, or intervention families;
- stochastic or approximate structure;
- scope, quantification, and boundary conditions.

The decomposition must preserve source provenance. A reviewer must be able to trace each mapped component back to the source support that licensed it.

If the source is underspecified, the correct output can be **abstention** or **residual uncertainty**. The method must not manufacture a complete structure merely because the mapping system expects one.

## 6. Label-Independent Structural Mapping

Let `C_D` be the set of normalized, source-grounded claims in domain `D`. Let `S(B_D)` denote the admissible family of structured representations built over the frozen basis `B_D`.

The mapping stage introduces

$
\Phi_D : C_D \rightarrow S(B_D).
$

The object `Phi_D(c)` is not merely a binary inventory of basis coordinates. It may contain:

$
\Phi_D(c)
=
\text{coordinates}
+
\text{typed topology}
+
\text{temporal structure}
+
\text{probe structure}
+
\text{criteria and provenance}
+
\text{partition structure}
+
\text{scope and constraints}.
$

The exact representation may vary by implementation, but the comparison must preserve the structure that the declared scientific question treats as discriminating.

During mapping, the following information must not determine the answer:

- conventional construct label;
- author identity;
- institution;
- journal or venue prestige;
- citation count;
- theoretical fame;
- expected lineage;
- desired atlas cluster.

Those fields may be restored afterward for interpretation, provenance, and publication.

The operational control is simple:

> If the labels and authority metadata were hidden, would the same structural mapping still be produced?

If not, the mapping is contaminated by information outside its declared evidential surface.

## 7. Structural Relations

The atlas should distinguish different relations rather than collapse all similarity into one score.

### 7.1 Structural equivalence

Two claims are structurally equivalent under the frozen comparison semantics when the declared discriminating structure is preserved up to the permitted representation changes.

Write schematically:

$
c_1 \cong_{B_D} c_2.
$

This does not imply semantic identity, theoretical synonymy, metaphysical identity, causal equivalence, or practical interchangeability.

### 7.2 Cross-label convergence

If differently named constructs map to structurally equivalent claims, the atlas records cross-label convergence.

The warranted statement is not “the constructs are the same.” It is:

> Under the frozen comparison system, these source-grounded operational claims preserve the same declared discriminating structure.

### 7.3 Within-label fission

If claims carrying the same conventional label map to non-equivalent structures, the atlas records within-label fission.

This identifies a failure of the label to behave as one structurally homogeneous comparison class under the declared basis.

### 7.4 Refinement

A claim `c_2` strictly refines `c_1` when it preserves the structure represented by `c_1` while adding independently discriminating structure.

### 7.5 Forgetting

A forgetting operation deliberately removes specified structure. If forgetting `J` from `c_2` yields an object equivalent to `c_1`,

$
\operatorname{Forget}_{J}(\Phi_D(c_2))
\cong
\Phi_D(c_1).
$

then the atlas can state exactly which additional structure separates them.

### 7.6 Incomparability

Some claims may share components yet be neither equivalent nor ordered by a simple refinement relation. The method should record incomparability rather than force a ranking.

### 7.7 Residual

Define `Residual_{B_D}(c)` when a source-grounded claim cannot be represented under the frozen system without an unlicensed extension, claim-specific bespoke encoding, or loss of structure that the protocol requires preserving.

Residuals are scientific information about the boundary of the working system, not pipeline failures to be hidden.

## 8. Anti-Vacuity and Anti-Leakage Controls

A sufficiently expressive representation language can map anything if the analyst is free to add structure after seeing the desired conclusion. The protocol therefore requires explicit pressure against vacuity.

Useful controls include:

**Name deletion.** Remove labels, author identities, and authority metadata from the mapping input.

**Basis-inventory ablation.** Demonstrate that coordinate presence alone is not sufficient for equivalence when topology differs.

**Topology ablation.** Confirm that wiring, order, or dependency can distinguish claims with the same coordinate inventory.

**Criterion provenance.** Do not allow an arbitrary success or relevance criterion to be introduced solely to recover the desired classification.

**Probe provenance.** Do not extend a probe family after observing which probe creates the desired distinction unless the extension is independently justified and versioned.

**Partition provenance.** Do not introduce a convenient subsystem boundary after observing which partition produces the desired mapping.

**Mapping reuse.** Record whether one generic mapping rule applies across claims or whether each claim requires a bespoke encoding.

**Permutation or null controls.** Compare observed atlas structure against appropriate shuffled or target-permuted controls where the design permits.

**Explicit residuals.** Never treat forced fit as preferable to an honest residual.

A proposed common structural language fails if its apparent success depends on answer-bearing degrees of freedom.

## 9. Held-Out Validation

Construction and validation must be separated.

A method can appear coherent on the literature that helped create its basis. That does not establish generalization even within the same domain.

Held-out validation therefore asks whether the frozen system remains:

- mappable;
- non-vacuous;
- structurally discriminating;
- reproducible;
- resistant to label leakage;
- resistant to bespoke encoding pressure

on literature that did not determine the primary answer key.

Suitable validation surfaces may include:

- a predeclared challenge set;
- independently sampled papers;
- later publication periods;
- distinct theoretical lineages;
- distinct subdisciplines;
- eventually, distinct scientific domains.

Validation results must not silently tune the frozen primary system.

## 10. AI-Assisted Implementation

AI can substantially lower the cost of searching, segmenting, decomposing, comparing, and stress-testing large scientific literatures. That does not make the model a scientific authority.

Possible legitimate roles include:

- source discovery;
- candidate claim extraction;
- source segmentation;
- decomposition proposals;
- counterexample search;
- competing reconstruction generation;
- mapping candidate generation;
- consistency checks;
- large-corpus triage.

The epistemic authority remains with the source text, explicit provenance, frozen rules, reproducible transformations, formal or structural checks where available, human adjudication where required, and held-out validation.

Important AI-specific failure modes include:

- hallucinated sources;
- fabricated quotations;
- substituting secondary summaries for primary support;
- construct-label leakage;
- authority leakage;
- answer-bearing decomposition;
- hidden use of outcome information;
- overconfident completion of underspecified claims;
- spurious cross-domain analogy.

The method therefore does not claim that AI removes the need for domain expertise. A narrower hypothesis is that AI may reduce the cost of exposing and comparing conceptual structure before full domain mastery while leaving scientific justification source- and protocol-dependent.

## 11. Relationship to Domain Applications

The current RelayTheory cognitive-science program provides one implementation context, not the definition of the method.

Paper 2 asks whether heterogeneous cognitive claims can be represented in a fixed, non-vacuous common structural coordinate system and compared through preserved structure rather than name similarity.

Paper 3 is intended to test the frozen Paper 2 system at 1000-work scale without silently changing the answer key.

Paper 0 sits above those applications. It extracts the candidate invariant procedure:

$
\text{domain literature}
\rightarrow
\text{adversarial forging}
\rightarrow
B_D
\rightarrow
\text{claim decomposition}
\rightarrow
\Phi_D
\rightarrow
\text{atlas}
\rightarrow
\text{held-out validation}.
$

A future medical or management-science application would be expected to forge its own `B_D`. Reusing the cognitive basis by default would not demonstrate domain-generality of the method.

## 12. Falsification and Failure Conditions

The protocol should be rejected, reduced, or substantially revised if any of the following occurs.

1. A prior method already performs substantially the same end-to-end methodological work.
2. Adversarial basis forging reduces to a renamed familiar procedure without additional operational constraints.
3. Different analysts cannot reproduce basis construction within an acceptable declared tolerance.
4. Source-grounded decomposition is unstable even after scope and evidence rules are fixed.
5. Label deletion removes the apparent atlas structure.
6. The mapping language is so expressive that arbitrary claims can be made equivalent through bespoke encoding.
7. Residual policy is itself outcome-dependent.
8. Successful mapping requires repeated post-outcome tuning.
9. Held-out validation cannot be separated from method construction.
10. The method works only on the domain or sources that forged it.
11. Its only surviving novelty claim is that an existing idea has been made more precise.

These are not merely limitations. They are intended failure conditions for the methodological project.

## 13. Novelty Status and Prior-Art Audit Boundary

This v0.1 deliberately does **not** claim that the method is novel.

Its purpose is to freeze a sufficiently precise object for hostile comparison against prior work.

The required prior-art audit must ask a functional question rather than search only for similar terminology:

> Does any existing method, or a tightly integrated existing family of methods, already perform substantially the same work from adversarial basis construction through label-independent structural mapping and held-out validation?

The later audit should compare the strongest neighbors claim by claim and may terminate Paper 0 if the integration is already known.

Until that audit is complete, the correct novelty status is:

```text
UNDERDETERMINED
```

## 14. Research Program

If the protocol survives hostile prior-art review, the immediate research sequence is:

1. freeze the methodological core;
2. complete the bounded cognitive-science atlas under Paper 2;
3. validate the frozen cognitive system at scale under Paper 3;
4. test the same forging-and-mapping procedure in at least one independent domain;
5. revise the method only through explicit versioning.

The long-term hypothesis is that scientific literatures containing unstable construct vocabularies may be compared through domain-specific structural coordinate systems generated by one common adversarial procedure.

That hypothesis remains open.

## 15. Conclusion

This paper proposes a method for comparing scientific claims when inherited construct vocabularies are not reliable common coordinates.

The method does not begin by deciding what the domain’s concepts truly are. It attempts to break candidate distinctions, retains the discriminating structure that survives, freezes a working basis, decomposes source-grounded claims, maps them without using conventional labels as answers, and compares them through explicit structural relations before testing the frozen system on held-out literature.

The intended payoff is not a universal ontology. It is a reproducible discipline for asking a more modest question:

> Once names and authority are removed, what structure must remain for two scientific claims to count as the same, different, more specific, weaker, incomparable, or outside the current comparison language?

Whether this protocol is genuinely new is not decided here. That is the next test.
