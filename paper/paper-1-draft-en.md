# Working Draft — Paper 1

> **Status:** Primary English working manuscript. Non-authoritative.
> **Scope:** Evidential conditions for operational individuation under restricted tests.
> **Repository provenance:** #119–#122, formal strengthening #124/#125, and the current formal artifact on main.
> **Formal boundary:** The target domain and representation-to-target map are explicit model inputs. This paper does not derive target ontology or metaphysical numerical identity from observation.

# Evidential Conditions for Operational Individuation
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

This question sits near several mature research traditions. Programming-language semantics has long studied representation independence: clients of an abstract data type should depend on exposed behavior rather than on a particular internal representation (Mitchell 1986). Process semantics and coalgebra study observational or behavioral equivalence relative to specified interactions (Hennessy and Milner 1985; Rutten 2000). Philosophical work on identity and discernibility separates logical discernibility from broader questions about identity and explicitly factorizes the adequacy of a descriptive language from mathematical discernibility within that language (Ladyman, Linnebo, and Pettigrew 2012). Practice-oriented philosophy of science likewise emphasizes how individuation depends on concrete experimental and epistemic practices rather than on a single context-free metaphysical criterion (Bueno, Chen, and Fagan 2018; Waters 2018; Love 2018).

This paper does not replace those frameworks. Its target is narrower: the evidential transition from a formal difference to an individuation claim.

The central rule is:

> **Do not infer a difference in what is represented merely from a difference in representation.**

Its positive counterpart is:

> **A claim of operational distinctness requires a difference that is relevant to the represented target and detectable by the admitted tests.**

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

**Formal inequality is evidence of representational difference; it is not, by itself, evidence of target-level individuality.**

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

The formal model therefore adds a tokenized representation containing the original presentation together with an explicit Boolean identity-like token.

The token is deliberately absent from the representation-to-target map, probe accessibility, and target-sensitive response semantics. This is a controlled negative test. If the token is irrelevant to the declared evidential surface, changing it should not change the induced classification.

The theorem *tokenizedGroundedIndist_iff_base* shows that, for fixed underlying presentations, tokenized indistinguishability is equivalent to the original target-sensitive indistinguishability.

The central theorem, *identityToken_variation_preserves_groundedClassification*, proves that arbitrary reassignment of the identity-like tokens on either side leaves the tested classification unchanged:

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

### 8.1 Representation independence

Mitchell (1986) studies representation independence for abstract data types: clients should depend on behavior exposed through the abstraction boundary rather than on implementation representation.

The present paper adopts a related caution but applies it to a different inference target. The question is not whether two implementations are contextually interchangeable for clients. It is whether a formal difference may count as evidence that represented targets are operationally distinct.

The novelty claim is therefore not representation independence itself. It is the use of explicit representation/target/test factorization as an evidential admissibility condition for individuation claims.

### 8.2 Observational and behavioral equivalence

Observational equivalence and bisimulation already provide mature accounts of when systems should count as behaviorally equivalent relative to specified observations or interactions. Hennessy and Milner (1985) develop observational congruence for concurrent programs, while Rutten (2000) develops a broad coalgebraic theory of systems and bisimulation.

The relation \(\equiv_A\) used here is mathematically modest by comparison. No new general equivalence theory is claimed.

The difference is inferential: when an observed difference is used to support an individuation claim, a difference visible only in the representation layer is not automatically admissible evidence of target-level distinctness.

### 8.3 Identity and discernibility

Ladyman, Linnebo, and Pettigrew (2012) show that identity-and-discernibility questions can be factorized into the adequacy of a formal language and mathematical discernibility within that language. Their analysis is an important constraint on the present paper: discernibility relations alone should not be advertised as solving numerical identity.

The present framework is compatible with that separation and narrower in ambition. It does not offer a new taxonomy of logical discernibility. It makes a specific evidential distinction between properties of the representation and target-relevant differences exposed by declared tests.

Work on weak discernibility in philosophy of physics likewise illustrates why discernibility and unrestricted numerical identity should not be conflated (Dieks and Versteegh 2008).

### 8.4 Individuation in scientific practice

Practice-oriented work shifts attention from the abstract question "What is an individual?" toward how scientists count, track, manipulate, and distinguish entities in inquiry. Bueno, Chen, and Fagan (2018) develop this program across multiple sciences. Waters (2018) asks how and for what purposes scientists individuate, while Love (2018) emphasizes problem-relative individuation in developmental biology.

The present paper shares the idea that individuation can depend on explicitly specified epistemic or experimental practices. Its contribution is narrower and formal: when a practice is represented by a declared test family, the model must still distinguish differences generated by the representation apparatus from differences linked to the target of the individuation claim.

### 8.5 Novelty boundary

The paper does not claim novelty for observational equivalence, bisimulation, representation independence, test-relative classification, the distinction between discernibility and numerical identity, or practice-relative individuation.

The proposed contribution lies in their intersection:

> **a representation-safe evidential discipline for formal individuation arguments, together with mechanized negative controls showing that representation-only differences and semantically inert identity-like tokens cannot supply hidden evidence for the tested target-sensitive classification.**

If prior work is shown to entail this complete package as an explicit individuation methodology, the novelty claim should be weakened.

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
