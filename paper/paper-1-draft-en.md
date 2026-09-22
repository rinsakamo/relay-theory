# Working Draft — Paper 1

> **Status:** Primary English working manuscript. Non-authoritative.
> **Scope:** Evidential conditions for operational individuation claims under restricted tests.
> **Repository provenance:** #119–#122, formal strengthening #124/#125, and the current formal artifact on main.
> **Formal boundary:** The target domain and representation-to-target map are explicit model inputs. This paper does not derive target ontology or metaphysical numerical identity from observation.

# When Does a Formal Difference Support an Individuation Claim?
## Representation, Target Relevance, and Restricted Tests

## Abstract

A formal model can contain multiple representations without representing multiple individuals. Distinct variables, encodings, identifiers, or carrier elements may differ as representations while referring to the same target. Representational multiplicity therefore does not, by itself, provide evidence for target-level plurality.

This paper asks a narrower question than the metaphysics of numerical identity: **under explicitly declared observational or interventional conditions, what kinds of difference may legitimately support an operational individuation claim?** We separate four components that formal reasoning can otherwise conflate: representations, a representation-to-target map, an admitted family of tests, and the resulting target-sensitive outcomes. The target domain and reference map are treated as model inputs rather than conclusions.

A small Lean development serves as a mechanically checked audit of this separation. It verifies that two distinct encodings may be representation-distinguishable while referring to the same target and remaining indistinguishable under all admitted target-sensitive tests; that a pair unresolved by a restricted test family may become distinguishable under a richer one; that test-family inclusion monotonically refines the induced indistinguishability relation under fixed exact semantics; and that decorative metadata does not alter access. An additional identity-token negative control makes the strongest anti-smuggling claim explicit: arbitrary reassignment of a semantically inert identity-like token leaves the tested operational classification unchanged, while such a token cannot mask a target-sensitive difference already exposed by the admitted tests.

The contribution is not a new theory of observational equivalence, nor a derivation of metaphysical identity. It is an inference discipline for individuation claims: **a formal difference is not admissible evidence of target-level distinctness merely because it distinguishes representations; it must be connected to the represented target through the declared evidential semantics.**

## 1. Introduction

A formal model can contain two representations without thereby representing two individuals.

The point is elementary, but formal arguments can violate it in subtle ways. A model may introduce two variables, two constructors, two identifiers, two records, or two carrier elements and subsequently appeal to their formal inequality as evidence that two target-level individuals exist. In that pattern, representational multiplicity risks doing the ontological work that the argument was supposed to justify.

The problem is evidential: **when is a difference between representations a legitimate reason to claim a difference in what they represent?**

This question sits near several mature research traditions. Scientific-representation accounts already treat representation as directional and inferential: models are used to draw warranted inferences about target systems (Suárez 2004; Contessa 2007), and Nguyen (2017) explicitly analyzes model and theoretical equivalence in terms of whether models license the same claims about the same targets. Programming-language semantics studies representation independence (Mitchell 1986). Process semantics and coalgebra study observational or behavioral equivalence relative to specified interactions (Hennessy and Milner 1985; Rutten 2000). Philosophical work on identity and discernibility factorizes questions about the adequacy of a descriptive language from mathematical discernibility within that language (Ladyman, Linnebo, and Pettigrew 2012). Practice-oriented philosophy of science studies individuation through experimental and epistemic practices (Bueno, Chen, and Fagan 2018; Waters 2018; Love 2018; Chen 2018).

This paper does not replace those frameworks. Its target is narrower: the evidential transition from a formal difference to an individuation claim.

The central rule is:

> **Do not infer a difference in what is represented merely from a difference in representation.**

Its positive counterpart is:

> **Within a declared evidential regime, a claim of operational distinctness requires a difference that is relevant to the represented target and detectable by the admitted tests.**

The target domain is not reconstructed from observation, and the reference map is not derived from the tests. The result therefore does not eliminate identity from the target domain. Instead, it constrains what may count as evidence for an individuation claim once the semantic target of that claim has been fixed.

### 1.1 Contributions

The paper makes three deliberately limited contributions.

1. **Representation-safe individuation discipline.** It separates representational multiplicity from target-relevant evidence and makes explicit that formal inequality, constructor choice, list position, identifiers, and similar representation features are not automatically admissible individuation evidence.

2. **Test-relative refinement without metaphysical overclaim.** It characterizes operational indistinguishability relative to a declared test family and verifies the expected refinement law under test-family inclusion, while rejecting the inference from test-relative distinguishability to unrestricted numerical identity.

3. **Mechanized anti-smuggling controls.** A Lean development checks concrete negative and positive controls, including an explicit identity-like token whose arbitrary reassignment leaves the target-sensitive classification unchanged when the target-relevant semantics are fixed.

The mathematical content is intentionally small. The role of mechanization is not to turn elementary facts into deep theorems. It is to make the dependency structure auditable.

## 2. Formal Setting

Let \(P\) be a set of representations. Elements of \(P\) may be names, terms, encodings, records, identifiers, or other formal handles. Distinct elements of \(P\) are not assumed to represent distinct individuals.

Let \(T\) be a target domain and let

\[
r : P \to T
\]

be a representation-to-target map.

The role of \(r\) is semantic: it states what each representation is taken to represent in the model. This paper does not derive \(T\) or \(r\) from the tests below. Consequently, it does not claim to derive target-level identity from observation.

Let \(Q\) be a class of tests. Depending on the application, a test may be an observation, measurement, query, or intervention. The framework does not identify these notions; a concrete analysis must declare which test class it is using.

For \(q \in Q\) and \(t \in T\), let

\[
O(q,t)
\]

denote the outcome of applying test \(q\) to target \(t\). Let \(A \subseteq Q\) be the family admitted by a particular analysis.

Define

\[
a \equiv_A b
\quad\Longleftrightarrow\quad
\forall q \in A,\;
O(q,r(a)) = O(q,r(b)).
\]

Correspondingly,

\[
a \mathrel{\#_A} b
\quad\Longleftrightarrow\quad
\exists q \in A:
O(q,r(a)) \neq O(q,r(b)).
\]

The induced relation is operational and test-relative. It is not a definition of metaphysical numerical identity.

**Formal inequality is evidence of representational difference; it is not, by itself, evidence of target-level individuality. Which differences are target-relevant depends on the target of the claim.**

## 3. Representational Multiplicity Is Insufficient

Suppose \(a,b \in P\) are formally distinct.

A representation-sensitive procedure may separate them immediately by inspecting a constructor, row identifier, address, token, or encoding convention. That establishes a difference between the representations. It does not establish a difference between their targets.

The Lean model contains a direct negative control. The constructors encodedA and encodedB are distinct. A deliberately representation-sensitive function separates them, yet both map to the same target value.

The theorem *encodingProbe_separates_sameGrounding* checks exactly this conjunction: representation-sensitive separation together with equal reference.

The theorem *sameGrounding_sameGroundedObservation* proves that equal reference forces equal outcome for every target-sensitive probe in the model. Its profile-level counterpart, *sameGrounding_sameGroundedProfile*, shows that a reference-preserving re-encoding preserves the complete target-sensitive response profile.

The concrete theorem *sameReferent_encodings_groundedlyIndistinguishable* establishes that encodedA and encodedB remain indistinguishable under the richer target-sensitive regime even though the representation-sensitive control separates them.

The invalid inference is

\[
a \neq b
\quad\Longrightarrow\quad
r(a) \neq r(b).
\]

The disciplined order is instead

\[
\text{multiple representations}
\rightarrow
\text{target-sensitive tests}
\rightarrow
\text{supported operational distinction, if any}.
\]

This is not a new equivalence theory. It is a restriction on what may be used as evidence when moving from formal structure to an individuation claim.

### 3.1 Scientific case: molecular individuation with unique molecular identifiers

High-throughput sequencing provides a concrete scientific case in which representational multiplicity and target multiplicity come apart. Sequencing workflows commonly amplify DNA or RNA molecules before detection. Consequently, several sequencing reads can descend from one pre-amplification molecule. Counting read records is therefore not, by itself, the same task as counting original molecules.

Unique molecular identifiers (UMIs) were introduced to address precisely this problem. Kivioja et al. (2012) used molecular identifiers to distinguish individual DNA or RNA molecules before amplification and thereby support absolute molecule counting. In the terminology of the present framework, a natural target domain is the set of pre-amplification molecules, while the observed representations are downstream sequencing reads. Different read records, file identifiers, or sequencing coordinates can distinguish representations without establishing that the reads originated from different target molecules.

In the notation of Section 2, the application can be idealized as follows:

- \(P\): downstream sequencing-read records;
- \(T\): pre-amplification source molecules;
- \(r(p)\): the source molecule from which read \(p\) descends;
- \(Q\): source-relevant measurements or queries admitted by the analysis, including experimentally introduced molecular tags and alignment context;
- \(A\subseteq Q\): the subset actually used by a particular deduplication or counting procedure;
- \(O(q,t)\): the outcome associated with source molecule \(t\) under query \(q\).

The mapping is deliberately idealized. In an actual UMI workflow, the source assignment \(r\) is not read directly from token equality: it is inferred through the experimental protocol together with sequencing, alignment, and error assumptions. The exact formal framework therefore audits which declared differences may support the individuation inference; it does not replace the statistical or experimental work required to establish the source assignment.

A UMI has a different evidential status from an arbitrary read identifier. The important difference is not that one string is called an identifier and another is not. A UMI is introduced by the experimental protocol at the molecular stage, before PCR amplification. Copies descended from the same tagged molecule can therefore inherit information that is experimentally linked to that source molecule. The identifier participates in the measurement process that connects a downstream read to the target of the counting claim.

This does not make the UMI an infallible identity oracle. Smith, Heger, and Sudbery (2017) emphasize that UMI sequences themselves are subject to sequencing error and show that naive treatment of UMI values can misidentify PCR duplicates. Their UMI-tools method uses the structure of observed UMI sequences to correct such errors and improve molecular quantification. Thus even an experimentally introduced molecular identifier must be interpreted within a declared error model and analysis procedure.

The lesson is not that UMIs are intrinsically real identifiers while read IDs are merely conventional. The same formal kind of feature—a token attached to a representation—can have different evidential roles depending on how it is connected to the target of the claim.

> **The evidential status of an identifier depends not on identifierhood itself, but on the declared experimental and semantic link between that identifier and the target being individuated.**

This case also gives the identity-token negative control below a positive scientific contrast. If a token is excluded from target-relevant semantics, arbitrary reassignment should not change the tested classification. If experimental practice supplies a target-relevant link, as UMI protocols are designed to do for pre-amplification molecules, the token may legitimately contribute to an individuation inference. Errors in that link then belong in the evidential model rather than being hidden by the label identifier.

## 4. Distinguishability Relative to a Test Family

Let \(A_c\) and \(A_f\) satisfy

\[
A_c \subseteq A_f.
\]

Under fixed exact outcome semantics,

\[
a \equiv_{A_f} b
\Longrightarrow
a \equiv_{A_c} b.
\]

The Lean theorem *groundedIndist_of_access_inclusion* proves this inclusion property, and *fine_indist_implies_coarse_indist* instantiates it for the two declared interfaces.

The converse need not hold. The fixture provides a pair satisfying

\[
a \equiv_{A_c} b
\]

while

\[
a \mathrel{\#_{A_f}} b.
\]

The corresponding theorems are *coarse_indistinguishable* and *fine_distinguishable*.

The interpretation is deliberately limited:

> **Under fixed exact semantics, enlarging the admitted test family can refine the induced indistinguishability relation.**

This is not the empirical claim that more evidence can never overturn an earlier judgment. Noise, statistical updating, model revision, and measurement disturbance are outside the exact semantics considered here.

Finiteness is likewise not proposed as the source of individuality. It makes the countermodel and its evidential surface completely inspectable; the refinement theorem itself does not depend on a thesis that finite access creates individuals.

## 5. From Outcome Difference to Target Difference

The positive side of the framework must show how an admitted target-sensitive difference can support an operational distinction without simply assuming the desired target inequality as a premise.

The theorem *groundedOutcomeDifference_impliesGroundDifference* establishes

\[
O(q,r(a)) \neq O(q,r(b))
\Longrightarrow
r(a) \neq r(b)
\]

for the target-sensitive response function used in the formalization.

The concrete theorem *identityProbe_groundedDifference* supplies the outcome difference for encodedA and encodedC, and *derivedGroundDifference* derives their target inequality from that discriminator.

This does not create the target carrier or its semantics. The target domain is already a model input. The result is narrower:

> **Within the declared target semantics, the positive-control target difference is derived from an admitted response difference rather than imported from representation identity.**

## 6. Explicit Identity-Token Invariance

A natural objection remains:

> Perhaps the model appears to avoid primitive identity only because no identity-like field was represented explicitly.

The formal model therefore adds a tokenized representation containing the original presentation together with an explicit identity-like token drawn from an arbitrary carrier type.

The token is deliberately absent from the representation-to-target map, probe accessibility, and target-sensitive response semantics. This is a controlled negative test. If the token is irrelevant to the declared evidential surface, changing it should not change the induced classification.

The theorem *tokenizedGroundedIndist_iff_base* shows that, for fixed underlying presentations, tokenized indistinguishability is equivalent to the original target-sensitive indistinguishability.

The central theorem, *identityToken_variation_preserves_groundedClassification*, proves that arbitrary reassignment of the identity-like tokens on either side leaves the tested classification unchanged:

The theorem is polymorphic in the token carrier: the result does not depend on the token being Boolean, numeric, textual, or otherwise structured.

\[
\text{identity-like token changes}
\land
\text{target-relevant semantics fixed}
\Longrightarrow
\text{operational classification fixed}.
\]

The concrete negative control *differentIdentityTokens_sameGroundedClassification* uses different token values on two encodings with the same reference and proves that they remain target-sensitively indistinguishable.

The positive contrast *identityTokenCannotMask_groundedDifference* shows that assigning the same token to two presentations cannot hide a target-sensitive difference already exposed by the admitted test family.

The core invariance proof is definitionally simple because the token is intentionally absent from the target-sensitive semantics. That simplicity is a feature of the negative control, not a claim of mathematical depth. Its purpose is to turn the prose statement "the identity label is not doing hidden work" into an executable dependency check.

## 7. Mechanization as an Anti-Smuggling Audit

The formal results are elementary enough to prove on paper. The reason to use Lean is methodological.

A prose argument can state that representation identity is not being used while a hidden identifier, constructor distinction, or data-structure choice enters a later definition. A mechanized artifact exposes the actual dependency graph.

In the present development, a reviewer can inspect that:

- the representation-sensitive probe is isolated as a negative control;
- target-sensitive observation factors through the explicit reference map;
- coarse and fine regimes differ in admitted target-sensitive probes rather than in labels;
- decorative interface metadata does not alter access;
- the explicit identity-like token does not occur in the target-sensitive classification semantics;
- the positive target difference is derived from a target-sensitive outcome difference rather than constructor inequality.

The CI rejects sorry, admit, native_decide, and project-local axiom declarations, builds the Lean project, independently kernel-checks compiled modules, and audits theorem axioms against a pinned allow-list.

The mechanization claim is therefore narrow:

> **The artifact makes it mechanically checkable that inadmissible representation-level distinctions do not do hidden work in the tested individuation argument.**

## 8. Relation to Existing Work

### 8.1 Scientific representation and target-directed inference

The closest prior work is not observational equivalence itself but the inferential literature on scientific representation.

Suárez (2004) characterizes scientific representation in terms of directionality toward a target and the capacity to support surrogate inference. Contessa (2007) develops an interpretational account in which a user interprets a representational vehicle in terms of a target so that valid surrogative inferences can be drawn. These accounts already establish that representation is not exhausted by formal resemblance between a vehicle and its target.

Nguyen (2017) is especially close to the present paper. He connects scientific representation with model and theoretical equivalence and proposes that equivalence should depend on how models are used to draw inferences about target systems—specifically, whether they license the same claims about the same targets.

Accordingly, this paper does **not** claim novelty for target-directed inference, for the idea that representations license claims about targets, or for separating representational vehicles from target systems.

The narrower question here is individuation-specific:

> **When a formal difference is offered as evidence for an individuation claim, has the difference entered through the declared target-relevant semantics, or only through the representation apparatus?**

The Lean artifact operationalizes that question with explicit negative controls. This is the principal remaining distinction from the scientific-representation literature.

### 8.2 Representation independence

Mitchell (1986) studies representation independence for abstract data types: clients should depend on behavior exposed through the abstraction boundary rather than on implementation representation.

The present paper adopts a related caution but applies it to a different inference target. The question is not whether two implementations are contextually interchangeable for clients. It is whether a formal difference may count as evidence that represented targets are operationally distinct.

### 8.3 Observational and behavioral equivalence

Observational equivalence and bisimulation already provide mature accounts of when systems should count as behaviorally equivalent relative to specified observations or interactions. Hennessy and Milner (1985) develop observational congruence for concurrent programs, while Rutten (2000) develops a broad coalgebraic theory of systems and bisimulation.

The relation \(\equiv_A\) used here is mathematically modest by comparison. No new general equivalence theory is claimed.

The difference is inferential: when an observed difference is used to support an individuation claim, a difference visible only in the representation layer is not automatically admissible evidence of target-level distinctness.

### 8.4 Identity and discernibility

Ladyman, Linnebo, and Pettigrew (2012) show that identity-and-discernibility questions can be factorized into the adequacy of a formal language and mathematical discernibility within that language. Their analysis is an important constraint on the present paper: discernibility relations alone should not be advertised as solving numerical identity.

The present framework is compatible with that separation and narrower in ambition. It does not offer a new taxonomy of logical discernibility. It asks which formal differences may be used as evidence for a declared target-level individuation claim.

Work on weak discernibility in philosophy of physics likewise illustrates why discernibility and unrestricted numerical identity should not be conflated (Dieks and Versteegh 2008).

### 8.5 Individuation in scientific practice

Practice-oriented work shifts attention from the abstract question "What is an individual?" toward how scientists count, track, manipulate, and distinguish entities in inquiry. Bueno, Chen, and Fagan (2018) develop this program across multiple sciences. Waters (2018) asks how and for what purposes scientists individuate, while Love (2018) emphasizes problem-relative individuation in developmental biology.

Chen (2018) is particularly relevant because it distinguishes ontological and epistemological modes of experimental individuation, describing the latter in terms of the presentation of individuals in experimental practice. The present use of *representation* is more formal and should not be conflated with Chen's experimental notion of presentation, but the comparison reinforces the need to separate what an experiment or formalism presents from stronger claims about what individuals exist.

The present paper's contribution, if any, is narrower: when an individuation practice is represented by an explicit formal test regime, the representation apparatus itself must not supply unacknowledged evidence for target-level plurality.

### 8.6 Redundant and surplus representational structure

The argument should also not be read as saying that representation-level or redundant structure is useless. Nguyen, Teh, and Wells (2020) show, in the context of gauge theory, that structure regarded as surplus in one sense may still be essential for representing a sufficiently rich collection of physically relevant local fields.

That result blocks an overly strong reading of the present negative controls. The claim here is only evidential:

> **A representation-only difference does not by itself support the tested target-level individuation claim.**

It does not follow that every such difference should be deleted from the formalism, or that representational redundancy can never have explanatory, computational, or representational value.

### 8.7 Novelty boundary

The paper does not claim novelty for:

- target-directed scientific representation or surrogative inference;
- observational equivalence, bisimulation, or behavioral equivalence;
- representation independence;
- test-relative classification;
- the distinction between discernibility and numerical identity;
- practice-relative or experimental individuation;
- the existence or possible usefulness of surplus representational structure.

The strongest defensible novelty claim is therefore conjunctive and methodological:

> **an individuation-specific admissibility rule that separates representation-only differences from target-relevant discriminators, together with a machine-checked dependency audit containing explicit negative controls for representation-sensitive probes and semantically inert identity-like tokens.**

This is a narrower claim than earlier versions of the manuscript. If prior work is shown to formulate this same package explicitly, the novelty claim should be weakened further.

## 9. Objections and Scope

### 9.1 The identity problem has merely been moved into the target domain

Partly correct. The paper assumes a target domain \(T\) and a reference map \(r\). It therefore does not derive target ontology or eliminate identity structure from the target domain.

The claim is conditional:

> **Once target semantics and reference assignment are fixed, representation identity need not be used as additional evidence to determine the operational distinctions supported by the declared test regime.**

### 9.2 The identity-token theorem is trivial

Mathematically, the central invariance is definitional. That is exactly why it functions as a negative control. The theorem does not show that every identity-relevant variable is decorative. It shows that a field that does not enter target-relevant semantics cannot independently alter the tested classification.

### 9.3 Operational distinguishability is not individuality

Agreed. The paper does not identify an equivalence class with a metaphysical individual. It studies when an operational individuation claim is evidentially licensed within a declared formal setting.

### 9.4 Observation and intervention are not equivalent

Agreed. The framework is parameterized by a declared test class. Observation-only and intervention-sensitive families may induce different relations, and no theorem licenses an inference from one to the other.

### 9.5 The refinement theorem ignores uncertainty

Correct. The monotonic refinement result assumes fixed exact semantics and literal inclusion of test families. Probabilistic observation, noise, decision thresholds, and model revision require additional structure.

## 10. Claim-to-Artifact Map

| Manuscript claim | Lean theorem |
| --- | --- |
| Equal reference preserves each target-sensitive observation | sameGrounding_sameGroundedObservation |
| Equal reference preserves the full target-sensitive profile | sameGrounding_sameGroundedProfile |
| Representation-sensitive metadata can separate same-reference encodings | encodingProbe_separates_sameGrounding |
| Same-reference encodings remain target-sensitively indistinguishable | sameReferent_encodings_groundedlyIndistinguishable |
| Restricted tests may fail to separate a pair | coarse_indistinguishable |
| A richer admitted test family may separate that pair | fine_distinguishable |
| Target-sensitive outcome difference entails target difference | groundedOutcomeDifference_impliesGroundDifference |
| Positive-control target difference is derived from the outcome difference | derivedGroundDifference |
| Test-family inclusion preserves fine-to-coarse indistinguishability | groundedIndist_of_access_inclusion |
| Decorative access metadata is irrelevant | decorativeInterfaceTag_irrelevant |
| Tokenized and base classifications coincide | tokenizedGroundedIndist_iff_base |
| Arbitrary identity-token reassignment preserves classification | identityToken_variation_preserves_groundedClassification |
| Different identity tokens do not separate same-reference encodings | differentIdentityTokens_sameGroundedClassification |
| Same identity token cannot hide a target-sensitive difference | identityTokenCannotMask_groundedDifference |

Every mechanically attributed prose claim should map to a theorem in this table, and the prose interpretation should not be stronger than the theorem surface.

## 11. Discussion

The framework distinguishes three levels that formal arguments can collapse.

First are representation facts: two terms, records, constructors, tokens, or positions differ.

Second are target-semantic facts: the model specifies how those representations relate to a target domain and how tests act on that domain.

Third are licensed evidential claims: given the declared semantics and admitted tests, some differences may support an operational distinction and others may not.

The error targeted by this paper occurs when a first-level fact is promoted directly to a third-level conclusion without an explicit second-level link.

The identity-token control sharpens this point. Adding a field named "identity" contributes nothing to the tested classification when that field has no role in the declared target semantics. Conversely, a target-sensitive response difference can matter even when two representations carry the same decorative token.

This suggests a simple audit question for formal models:

> **If the representation-level identifier were arbitrarily reassigned while all target-relevant semantics were held fixed, would the individuation conclusion change?**

If the answer is yes, the argument should explain why the identifier itself is target-relevant evidence rather than an implementation convenience.

## 12. Conclusion

Multiple representations do not imply multiple individuals.

The paper's positive rule is:

> **A claim of operational distinctness requires target-relevant evidence that actually distinguishes the cases under the declared test conditions.**

The formal model separates representation, target reference, admitted tests, and outcomes. Its negative controls show that representation-sensitive differences can exist without target-sensitive separation. Its refinement result shows how a richer test family can reveal a distinction hidden under a poorer one. Its positive control derives a target difference from an admitted target-sensitive outcome difference rather than constructor inequality. Its identity-token invariance result makes explicit that a semantically inert identity-like field contributes no independent information to the tested classification.

None of these results derives metaphysical numerical identity. None shows that finite access creates individuals. None establishes a universally privileged test family.

The narrower conclusion is enough:

> **Differences in representation should count as evidence of differences in what is represented only when an explicit target-relevant evidential link justifies that inference.**

## References

Bueno, Otávio, Ruey-Lin Chen, and Melinda B. Fagan, eds. 2018. *Individuation, Process, and Scientific Practices*. Oxford University Press. DOI: 10.1093/oso/9780190636814.001.0001.

Dieks, Dennis, and Marijn A. M. Versteegh. 2008. "Identical Quantum Particles and Weak Discernibility." *Foundations of Physics* 38: 923–934. DOI: 10.1007/s10701-008-9243-z.

Hennessy, Matthew, and Robin Milner. 1985. "Algebraic Laws for Nondeterminism and Concurrency." *Journal of the ACM* 32(1): 137–161. DOI: 10.1145/2455.2460.

Ladyman, James, Øystein Linnebo, and Richard Pettigrew. 2012. "Identity and Discernibility in Philosophy and Logic." *The Review of Symbolic Logic* 5(1): 162–186. DOI: 10.1017/S1755020311000281.

Love, Alan C. 2018. "Individuation, Individuality, and Experimental Practice in Developmental Biology." In *Individuation, Process, and Scientific Practices*, 165–191. Oxford University Press. DOI: 10.1093/oso/9780190636814.003.0008.

Mitchell, John C. 1986. "Representation Independence and Data Abstraction." In *Proceedings of the 13th ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages*, 263–276. Association for Computing Machinery. DOI: 10.1145/512644.512669.

Rutten, Jan J. M. M. 2000. "Universal Coalgebra: A Theory of Systems." *Theoretical Computer Science* 249(1): 3–80. DOI: 10.1016/S0304-3975(00)00056-6.

Waters, C. Kenneth. 2018. "Ask Not 'What Is an Individual?'" In *Individuation, Process, and Scientific Practices*, 91–113. Oxford University Press. DOI: 10.1093/oso/9780190636814.003.0005.

Kivioja, Teemu, Anna Vähärautio, Kasper Karlsson, Martin Bonke, Martin Enge, Sten Linnarsson, and Jussi Taipale. 2012. "Counting Absolute Numbers of Molecules Using Unique Molecular Identifiers." *Nature Methods* 9(1): 72–74. DOI: 10.1038/nmeth.1778.

Smith, Tom, Andreas Heger, and Ian Sudbery. 2017. "UMI-tools: Modeling Sequencing Errors in Unique Molecular Identifiers to Improve Quantification Accuracy." *Genome Research* 27(3): 491–499. DOI: 10.1101/gr.209601.116.
