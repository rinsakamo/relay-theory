# Working Draft — Paper 1

> **Status:** Primary English working manuscript. Non-authoritative.
> **Scope:** Necessary structural and evidential-dependency conditions for operational individuation inferences.
> **Formal boundary:** The target domain and representation-to-target assignment are model inputs. Structural factorization does not itself supply scientific warrant.

# When May a Formal Difference Enter an Individuation Inference?
## Target Factorization, Restricted Tests, and a Unique Molecular Identifier Case

## Abstract

Formal differences between representations do not by themselves license target-level individuation. We separate an exact target-factorization condition from the scientific warrant required to accept it and connect representation-level observations to target-level outcomes through structurally admissible test families. A unique molecular identifier (UMI) case distinguishes software read IDs, latent molecular tags, and noisy observed tags. We distinguish structure-preserving re-encoding from assignment-changing perturbations in a counterfactual relevance audit. A Lean formalization checks structural dependencies and family-level separation. The framework audits individuation inferences relative to proposed representation-to-target assignments; it neither discovers those assignments nor supplies a complete theory of evidence or numerical identity.

## 1. Introduction

Formal representations routinely contain more distinctions than the target-level claims for which they are used. Two variables can have different names, two records can have different database identifiers, two sequencing reads can have different file-level identifiers, and two constructors can be formally unequal even when those differences do not track two distinct target-level individuals.

The problem is not that such representation-level structure is useless. It may be indispensable for computation, bookkeeping, locality, provenance, or model construction. The problem arises when a difference in that structure is used as a premise in an individuation inference.

This paper asks a deliberately narrow question:

> **When may a formal difference inside a representation enter an inference that treats represented targets as operationally distinct?**

The answer developed here has two layers that should not be conflated.

First, there is a **structural condition**. A representation-level feature must factor through the declared target assignment, or a representation-level observation must agree with a target-level response under the declared test. Without such factorization, the formal difference is only a difference in the representation.

Second, there is a **scientific-warrant condition**. Writing down a factorization does not make it true, reliable, or evidentially adequate. The experimental, causal, measurement, calibration, or semantic practice must independently justify treating that factorization as a good model of the target relation.

The formal artifact addresses only the first layer. It makes structural dependencies auditable. It does not manufacture the second.

This separation motivates what we call a practical **counterfactual relevance audit**. For an identifier-like feature, ask what kind of change is being considered. A consistent bijective renaming of labels should not change an inference that depends only on the structure those labels encode. By contrast, reassigning labels across representations can alter evidence if the assignment itself records a scientifically grounded relation. If the conclusion changes under an assignment perturbation, the argument must explain why that assignment is target-relevant rather than merely representational.

The paper develops this point using unique molecular identifiers (UMIs). A software read identifier and a molecular tag can both be represented as strings. Yet their evidential roles differ because one is bookkeeping metadata while the other can participate in an experimental chain linking downstream reads to pre-amplification template molecules. The UMI case also exposes an important limit of the exact formal model: observed UMI strings can contain errors, so the experimentally assigned tag and the observed read-level tag must be distinguished.

### 1.1 Contributions

The paper makes four limited contributions.

1. **Structural target factorization.** A representation-level feature is formally target-tracking only when it factors through the declared representation-to-target map. This is a structural admissibility condition, not an epistemic warrant.

2. **Test-family admissibility.** Representation-level observations and target-level responses are placed in one inference chain. A selected family can support target-level separation only when every separating test used in the inference has the declared target-response factorization.

3. **A counterfactual relevance audit.** The paper distinguishes structure-preserving re-encoding from evidence-changing reassignment and uses that distinction to diagnose when identifier assignments or encodings are doing hidden work.

4. **A machine-checked dependency analysis with a scientific case.** A small Lean formalization checks the structural claims, while the UMI case shows how latent target-linked tags, noisy observed tags, and representation-only identifiers come apart in practice.

The audit is designed to expose three recurrent failure modes. **Within-fiber leakage** occurs when a feature varies between representations assigned to the same target. **Unsupported observation bridging** occurs when a representation-level outcome is treated as a target response without an independently warranted factorization. **Regime overreach** occurs when separation under one selected test family is promoted to a stronger or unrestricted identity claim.

## 2. Formal Setting

### 2.1 Representations and targets

Let \(P\) be a set of representations and \(T\) a target domain. Let

\[
r:P\to T
\]

be a representation-to-target assignment. Distinct elements of \(P\) are not assumed to represent distinct elements of \(T\).

The assignment \(r\) is a modeling input. The paper does not infer \(r\) from raw observations and does not derive the ontology of \(T\). In applications where source assignment is uncertain, the framework audits a proposed assignment model rather than solving the source-assignment problem.

This makes the inferential role of the formalism asymmetric. It is not a procedure for discovering \(r\) from observed representation-level differences. Rather, conditional on a proposed \(r\), it audits whether a discriminator is compatible with that assignment without importing distinctions that vary within a single fiber of \(r\). Observing \(f(a)\neq f(b)\) therefore does not construct or validate the target assignment; the implication to \(r(a)\neq r(b)\) is licensed only within a model in which the relevant factorization has independent scientific warrant.

The exact formal core is restricted to one target value per representation. Many-to-many, distributed, and probabilistic correspondences are natural extensions, but they are outside the present claim.

### 2.2 Structural target factorization

Let a representation-level feature be

\[
f:P\to V
\]

and a target-level property be

\[
\phi:T\to V.
\]

We call the following a **target-factorization condition**

\[
F_r(f,\phi)
\quad\Longleftrightarrow\quad
\forall p\in P,\; f(p)=\phi(r(p)).
\]

If \(F_r(f,\phi)\) holds, then

\[
f(a)\neq f(b)
\quad\Longrightarrow\quad
r(a)\neq r(b).
\]

The proof is elementary: equal target assignments force equal values of every feature that factors through the target. The value of the condition is therefore not mathematical depth but dependency exposure.

A direct consequence is **fiber invariance**: if \(r(a)=r(b)\), then every feature satisfying \(F_r(f,\phi)\) must obey \(f(a)=f(b)\). In other words, a feature that varies within one fiber of the proposed target map cannot, under that same model, be treated as a property of the target. This is the operational anti-smuggling test used throughout the paper.

Crucially, \(F_r(f,\phi)\) is **not itself an evidential warrant**. It says what would have to be structurally true for \(f\) to track a target property under \(r\). Whether a scientific application is entitled to accept that model depends on evidence external to the formal identity.

Such warrant can come from different sources: calibration data linking observed values to target properties; knowledge of a causal production process connecting a feature to the target; a validated measurement or error model; an intervention protocol; or a semantic convention whose target reference is independently fixed. The framework does not rank these sources or derive them. It requires the relevant warrant to be stated rather than silently encoded in \(r\), \(\phi\), or the selected tests.

The warrant must also be **non-self-licensing**: it cannot consist solely in treating the very formal difference under dispute as if it already established the target distinction. A row identifier, barcode string, or constructor name does not become target evidence merely because a model has been parameterized so that different values denote different targets. The justificatory route must contain information that is independently grounded in the relevant scientific or semantic practice.

This distinction also blocks a trivialization. If \(r\) is chosen so finely that it encodes every representational distinction, many features can be made to factor through it. That does not establish that such an \(r\) is scientifically appropriate. The target assignment and its justification remain substantive inputs.

### 2.3 Test-specific observation factorization

The previous feature-level condition can be connected directly to tests.

Let \(Q\) be a class of tests, let

\[
\widehat O:Q\times P\to Y
\]

be the outcome actually read from the representation, and let

\[
O:Q\times T\to Y
\]

be the target-level response posited by the model.

For a particular test \(q\), define

\[
B_r(q)
\quad\Longleftrightarrow\quad
\forall p\in P,\;
\widehat O(q,p)=O(q,r(p)).
\]

This is a test-specific structural factorization. Under it,

\[
B_r(q)
\land
\widehat O(q,a)\neq \widehat O(q,b)
\quad\Longrightarrow\quad
r(a)\neq r(b).
\]

This yields a single inference chain rather than two disconnected modules:

\[
\text{representation-level observation}
\to
\text{target factorization}
\to
\text{target-level response}
\to
\text{operational separation}.
\]

Again, the equation does not justify itself. A scientific application must explain why the measurement or protocol makes \(B_r(q)\) a defensible approximation or idealization.

### 2.4 Selected test families

Let \(A\subseteq Q\) be a family of tests selected for an analysis. Define **structural family-level admissibility** by

\[
\operatorname{Adm}_r(A)
\quad\Longleftrightarrow\quad
\forall q\in A,\;B_r(q).
\]

Thus selection alone does no evidential work: every test actually used by the exact inference must satisfy the declared observation-to-target factorization. Scientific warrant for including such a test must be supplied independently and may not be self-licensed by the formal difference the test is being used to promote.

The family-wide requirement is deliberately stronger than validating only a separating witness after outcomes are known. It prevents an analysis from selecting a discriminator first and supplying structural admissibility only post hoc.

Define

\[
a\equiv_A b
\quad\Longleftrightarrow\quad
\forall q\in A,\;
\widehat O(q,a)=\widehat O(q,b),
\]

and

\[
a\mathrel{\#_A}b
\quad\Longleftrightarrow\quad
\exists q\in A:\;
\widehat O(q,a)\neq\widehat O(q,b).
\]

The factorization and restricted-test layers now yield the family-level implication

\[
\operatorname{Adm}_r(A)
\land
a\mathrel{\#_A}b
\quad\Longrightarrow\quad
r(a)\neq r(b).
\]

The separating witness \(q\in A\) is guaranteed by \(\operatorname{Adm}_r(A)\) to satisfy \(B_r(q)\), so its observed difference can be transferred to the target level. The Lean development checks the corresponding finite theorem.

If \(A_c\subseteq A_f\), indistinguishability under \(A_f\) implies indistinguishability under \(A_c\). The converse need not hold. This is a theorem about fixed exact semantics and set inclusion, not a claim that accumulating noisy evidence can never reverse a classification.

## 3. Scientific Case: UMI-Based Molecular Counting

### 3.1 Representation multiplicity is not molecule multiplicity

High-throughput sequencing supplies a concrete instance of the problem. Polymerase chain reaction (PCR) amplification can generate several downstream read records from one template molecule. Therefore

\[
100\ \text{read records}
\not\Rightarrow
100\ \text{source molecules}.
\]

A unique software identifier assigned to each read can distinguish all 100 records while providing no independent reason to infer 100 pre-amplification molecules.

Kivioja et al. (2012) introduced unique molecular identifiers to support absolute molecule counting by labeling molecules before amplification. Smith, Heger, and Sudbery (2017) show why the resulting strings still require error-aware analysis: UMI sequences can contain sequencing errors, and naive equality-based treatment can misidentify PCR duplicates.

### 3.2 The target is a tagged template, not a string

For the present case, the cleanest target domain is not a domain of abstract molecular identities read directly from barcodes. Let \(T\) contain **tagged template molecules after UMI assignment and before PCR amplification**.

Let

\[
u:T\to U
\]

denote the latent UMI assigned to a tagged template molecule. Downstream read records form \(P\), and \(r(p)\) denotes the tagged template from which read \(p\) descends.

If sequencing were error-free and if the observed UMI field on every read exactly reproduced the assigned molecular tag, then the observed tag feature \(\widehat u:P\to U\) would satisfy

\[
\widehat u(p)=u(r(p)).
\]

That is precisely a target-factorization condition.

Real data are more difficult. The observed read-level string need not equal the latent assigned tag. A sequencing error may alter one base; PCR or library effects may complicate the observation process; two distinct molecules may also receive the same UMI value by collision. Thus the real inferential chain is better pictured as

\[
\text{tagged template}
\to
\text{latent assigned UMI}
\to
\text{amplification}
\to
\text{noisy observed UMI on reads}.
\]

The exact formal factorization captures the no-error dependency skeleton. It does not replace the error model connecting the latent assigned tag to the observed read-level string.

### 3.3 A synthetic error-and-collision example

Consider three tagged templates:

- \(m_1\) has latent assigned UMI *ACGT* and produces three reads observed as *ACGT*, *ACGT*, and *ACGC*;
- \(m_2\) has latent assigned UMI *TGCA* and produces three reads observed as *TGCA*, *TGCA*, and *TGCA*;
- \(m_3\) also has latent assigned UMI *ACGT* and produces two reads observed as *ACGT* and *ACGT*.

There are eight read records but three tagged templates. The *ACGC* observation represents one sequencing error from the latent tag of \(m_1\), while \(m_1\) and \(m_3\) instantiate a UMI collision.

A naive rule that equates distinct observed UMI strings with distinct source molecules returns three groups: *ACGT*, *ACGC*, and *TGCA*. The numerical count therefore happens to equal the true number of tagged templates, but the partition is wrong in two opposite ways: the sequencing error splits \(m_1\), while the collision merges evidence from \(m_1\) and \(m_3\). Numerical agreement can therefore be accidental.

An error-aware model can treat *ACGC* as compatible with the *ACGT* tag, but UMI sequence alone cannot separate \(m_1\) from \(m_3\) once they collide. Additional genomic, transcript, library, or other experimentally warranted context may be required.

The example makes three layers explicit:

1. unique read IDs individuate eight records but overcount tagged templates;
2. latent assigned UMIs are protocol-generated target properties, but collisions make UMI equality insufficient for target identity;
3. observed UMI strings are noisy measurements of those latent tags, so raw string inequality can also over-separate one target.

Only the second layer satisfies the exact target factorization in the idealized model. The third requires an error model, and the first is representation-level bookkeeping unless some independent target link is supplied. The three candidate procedures also expose different audit outcomes: unique read IDs fail to factor through molecular source assignment; raw observed-string equality is target-linked but violates exact observation factorization under sequencing error and remains non-injective under collision; an error-aware inference is admissible only insofar as its measurement and error model is independently warranted.

This construction is diagnostic rather than a model of any particular current UMI pipeline, and it does not claim that contemporary tools simply count distinct raw strings. Its purpose is to place two documented problems---sequencing error and UMI collision---inside one transparent example where a correct scalar count can conceal a wrong source partition (Kivioja et al. 2012; Smith, Heger, and Sudbery 2017).

| Representation-level basis | Audit diagnosis | What further warrant is needed |
| --- | --- | --- |
| Unique read ID | Varies within one molecular-source fiber; cannot factor through source assignment. | An independent source link, absent from bookkeeping identity alone. |
| Raw observed UMI string | Sequencing error can split one target; collision makes equal tags compatible with different targets. | An error/collision model plus experimentally relevant context. |
| Error-aware UMI inference | May use target-relevant structure, but admissibility is model-relative rather than guaranteed by the barcode type. | Validated measurement/error assumptions and protocol/context support. |

### 3.4 What the framework diagnoses

The framework therefore does not say UMI difference means molecule difference. It says something narrower.

A read-level feature may enter a molecular individuation inference only through a justified model of how that feature was generated from the target. For UMIs, the experimental tagging protocol, genomic or transcript context, and error model supply the relevant scientific work. The string type itself supplies none.

This is also why the case is useful philosophically. Two fields can both be identifiers, both be strings, and both distinguish records, yet only one participates in a causal and measurement history designed to track pre-amplification templates.

## 4. Counterfactual Relevance Audit

The phrase relabeling invariance can hide two importantly different perturbations. The relevant notion of harmless change is not an arbitrary bijection in every application; it depends on which structure the inference actually uses.

### 4.1 Structure-preserving re-encoding

Let \(U\) be the value domain of an identifier-like field, and let \(\mathcal S\) denote the relations on \(U\) that the inference declares evidentially relevant. A re-encoding \(\pi:U\to U\) is **structure-preserving relative to \(\mathcal S\)** when it is bijective and preserves each declared relation. For a \(k\)-ary relation \(S\in\mathcal S\),

The choice of \(\mathcal S\) must itself be fixed and independently motivated before the counterfactual comparison. Otherwise an analyst could make an inconvenient transformation non-preserving merely by adding a relation that encodes the desired conclusion.

\[
S(u_1,\ldots,u_k)
\quad\Longleftrightarrow\quad
S(\pi(u_1),\ldots,\pi(u_k)).
\]

When an inference uses only equality classes, every bijection is a harmless renaming. When it uses sequence geometry, edit distance, neighborhood structure, order, or another relation on label values, an arbitrary bijection need not be harmless. In an error-aware UMI analysis, mapping strings to arbitrary numbers while destroying sequence distance is not a pure re-encoding of the evidential structure.

The appropriate invariance question is therefore whether the inference survives automorphisms of the representation-level structure it claims to use. If a conclusion changes under a transformation that preserves all declared evidential structure, the argument contains an unexplained representation dependence.

### 4.2 Assignment perturbation

A different operation reassigns values across representations while holding the independently specified target state fixed. This can alter which reads share a recorded tag or which records are grouped together without being a structure-preserving re-encoding of the same assignment.

Sensitivity to this operation is not automatically an error. It shows that the **assignment itself is evidentially active** and therefore needs justification.

For a software-generated read ID, using arbitrary ID assignment to infer source-molecule plurality would be illegitimate unless some additional target link were established.

For UMIs, by contrast, the recorded assignment is intended to preserve information about a physical tagging event. Randomly reassigning observed tags across reads destroys evidence about that event. The correct conclusion is therefore not that UMI-based inference should be invariant under arbitrary reassignment. It is that any legitimate sensitivity must be explained by the experimental provenance and error model.

The audit can thus be stated as two questions:

1. Is the inference invariant under every **structure-preserving re-encoding** of the representation-level relations it declares relevant?
2. If it is sensitive to an **assignment-changing perturbation**, what independently grounded scientific relation makes that assignment target-relevant?

This formulation avoids both errors: treating evidence-destroying reassignment as harmless renaming, and treating an arbitrary bijection as harmless when the inference actually uses more than equality.

## 5. Machine-Checked Dependency Analysis

The Lean formalization is intentionally small. Its role is to make the stated dependency structure machine-checkable.

The formal model contains three representations, a representation-to-target map, target-sensitive tests, coarse and fine test regimes, a representation-sensitive negative control, and semantically inert token metadata.

The feature-level factorization is defined over an arbitrary value domain. A representation-level feature can be paired with a target-level property only through the specified structural factorization. The formalization checks that two representations assigned to the same target receive the same value for every factorized feature, and that a difference in such a feature entails different target assignments. It also checks that a deliberately representation-sensitive test cannot satisfy target factorization when it separates two representations assigned to the same target, while a positive-control feature defined directly from the target assignment can.

The test layer is connected to the same structure. A formal observation-factorization condition states that a representation-level observed outcome agrees with the target-level response of its assigned target for each test. The corresponding target-linked observation function satisfies this condition, and a difference on any observed test outcome satisfying the factorization entails different target assignments. A family-level object then requires this factorization for every test accessible in a selected regime; if one such admissible test separates two representations, the formalization derives different target assignments. This is the finite counterpart of \(\operatorname{Adm}_r(A)\land a\mathrel{\#_A}b\Rightarrow r(a)\neq r(b)\).

The remaining results are negative controls and monotonicity checks. Re-encodings assigned to the same target preserve the target-linked observation profile. A richer selected test family can separate a pair left unresolved by a restricted family. Arbitrary reassignment of a token absent from target-sensitive semantics does not alter classification.

These proofs are elementary. The machine-checking claim is correspondingly modest: a reviewer can inspect whether a supposedly target-relevant discriminator actually enters through the declared target map and factorization, rather than through a hidden encoding choice, label, or metadata field.

## 6. Relation to Existing Work

### 6.1 Nguyen and target-directed representation

The closest conceptual comparison is Nguyen (2017). Nguyen argues that questions of scientific representation and theoretical equivalence should attend to how models are used to draw inferences about target systems, including whether models license the same claims about the same targets.

The present paper accepts rather than challenges that target-directed perspective. Its unit of analysis is different.

Nguyen's comparison is naturally read at the level of models, their representational use, and the claims they license about target systems. The present problem arises **inside an individuation inference** when a specific difference in the representing apparatus is recruited as a premise. Even when two representations are both used to reason about a declared target, it does not follow that every formal difference between them is evidence about that target.

Consider two database records known to concern the same person. Their distinct row IDs are genuine differences in the representational vehicles. A target-directed account can readily acknowledge that the records are used to make claims about the same person. The local question addressed here is different: may the inequality of those row IDs itself be used to support the claim that there are two people? The target-factorization test says no unless a scientifically or semantically justified target property explains why row-ID difference tracks person difference.

The same distinction matters in the UMI case. Both a software read ID and an observed UMI field occur inside representations used to make claims about source molecules. The fact that both belong to a target-directed representational practice does not determine whether each difference is evidentially relevant to molecular counting. That requires a more local account of the dependency from feature generation to target property.

The contribution is therefore not a rival theory of scientific representation, nor a new criterion of theoretical equivalence. It is a **feature-level dependency audit** for a particular inferential move within an already target-directed practice.

The converse limitation is equally important. Target factorization is not sufficient for representational adequacy. A formally factorized feature may arise from a bad target model, a mistaken reference assignment, or an unreliable measurement process. Nothing in the present framework settles those broader questions.

### 6.2 Inferential representation and experimental individuation

Suárez (2004) and Contessa (2007) already emphasize directionality, interpretation, and surrogate inference in scientific representation. The present framework does not claim that connecting a representation to a target is novel. It isolates one narrower dependency: what must be true before a **difference internal to the representational vehicle** can enter an individuation inference.

Practice-oriented work on individuation likewise constrains the claim. Bueno, Chen, and Fagan (2018), Waters (2018), and Love (2018) emphasize that counting, tracking, manipulation, and individuality depend on scientific purposes and practices. Chen (2018) distinguishes ontological and epistemological modes of experimental individuation and explicitly treats presentation as part of practice.

Accordingly, this paper does not claim that representation and individuation have only now been distinguished. Its contribution is a compact formal audit for a recurrent failure mode within such practices: allowing representation-level distinctions to do target-level individuating work without making the dependency explicit.

### 6.3 Technical neighbors

Representation independence in programming-language semantics constrains dependence on implementation details (Mitchell 1986). Observational and behavioral equivalence classify systems relative to specified interactions (Hennessy and Milner 1985; Rutten 2000). Work on identity and discernibility warns against identifying formal discernibility with unrestricted numerical identity (Ladyman, Linnebo, and Pettigrew 2012; Dieks and Versteegh 2008).

The present mathematics is substantially more modest than these mature frameworks. The distinctive use is methodological: combine target factorization, restricted tests, and counterfactual assignment analysis to audit individuation inferences.

Nor does failure to support individuation imply that a representational distinction is dispensable. Surplus structure can remain useful or even necessary for other representational tasks (Nguyen, Teh, and Wells 2020).

## 7. Outlook: Construct-Level Comparison

The UMI case motivates a broader methodological question, but this extension is prospective and is not a result established by the present formal model. A separate study can ask whether the same anti-smuggling discipline applies to theoretical constructs used to describe measured capacities.

Let \(\sigma(c)\) serve only as shorthand for an *operational structural signature*: the measurement roles, tests, criteria, temporal relations, resource conditions, and other dependencies retained after a construct label is suppressed and its associated claim is normalized. The signature is not assumed unique or complete, and its components must be fixed by the declared measurement question before construct labels or source identity and provenance are restored.

Under such a procedure, different construct names alone would provide no evidence of different measured capacities. A surviving signature difference would be candidate discriminating structure, not sufficient evidence of ontological or psychological independence; matching signatures would likewise not imply synonymy or explanatory interchangeability.

> **Nominal plurality is not evidential plurality. Preserve the discriminating structure that warrants a distinction, not merely the names of the distinguished things.**

Testing this proposal requires a separate corpus, normalization protocol, common measurement basis, and empirical analysis. The present paper contributes only the evidential discipline that such a comparison would have to satisfy.

## 8. Scope and Limitations

The framework deliberately leaves several problems open.

First, \(T\) and \(r\) are inputs. The theory does not derive target ontology or solve uncertain source assignment.

Second, exact target factorization is a structural idealization. Real measurements are noisy, probabilistic, and model-dependent. The UMI example makes this limitation explicit by separating latent assigned tags from observed tag strings. Accordingly, *necessary condition* in this paper means necessary within the declared exact deterministic model; it is not a claim that every noisy or probabilistic individuation procedure must satisfy the literal equality \(f(p)=\phi(r(p))\).

Third, structural factorization is not epistemic warrant. A badly chosen \(r\) can make irrelevant features appear target-factorized. Scientific justification for the target assignment, measurement model, and test relevance remains external to the Lean development.

Fourth, the formal core uses a function \(r:P\to T\). Many-to-many, distributed, and probabilistic representation-target relations are not treated.

Fifth, observation and intervention are not equated. Different test classes can induce different operational partitions.

Finally, operational separation is not metaphysical numerical identity, and synchronic discrimination does not establish diachronic persistence.

## 9. Formal Audit Summary

For the blind review copy, the machine-checked claims are grouped under neutral labels. The grouped map below states what each family checks and which declared dependency it uses.

| Results | Informal claim family | Declared dependency |
| --- | --- | --- |
| R1--R4 | Representation-only differences can coexist with one target assignment; target-linked observations are preserved for same-target representations. | Fixed representation-to-target map and exact target-response semantics. |
| R5--R7 | A richer selected test family can refine an operational partition left unresolved by a restricted family. | Fixed exact test semantics and test-family inclusion. |
| R8--R10 | A target-linked outcome difference can support a target-assignment difference in the positive control. | Deterministic target response under the declared test. |
| R11--R15 | Semantically inert identity-like tokens or decorative access metadata do not alter the tested classification. | Those fields are absent from the declared target-sensitive semantics. |
| R16--R19 | Generic feature factorization preserves equality within each fiber of the target map; a representation-sensitive negative control fails factorization. | Proposed representation-to-target map and explicit feature factorization. |
| R20--R22 | Representation-level observed outcomes can support target separation only under test-specific factorization; family-level separation is licensed only when every selected test is admissible. | Exact agreement between observed outcomes and target responses for each test used by the selected family. |

The number of small theorems is not itself a novelty claim. The collection is a machine-checkable record of the dependency structure. The complete set of neutral result labels is R1--R22.

## 10. Conclusion

A formal difference may enter an individuation inference only through a justified path from representation to target.

The formalism is therefore an audit of a proposed representation-to-target model, not a procedure for discovering target assignments from formal differences. The formal contribution separates two questions that are often compressed into one. **Structural target factorization** asks whether the feature or observed test outcome actually depends on the target assignment in the claimed way. **Scientific warrant** asks why that dependency model should be trusted in the application. The first can be machine-checked; the second cannot be obtained by declaration.

UMI-based molecular counting illustrates the distinction. Unique read IDs distinguish downstream records. Latent molecular tags can track tagged templates because of the pre-amplification protocol. Observed UMI strings are noisy measurements of those latent tags and require an error model. The fact that all three may appear as strings is irrelevant to their evidential role.

The practical lesson is therefore neither to ignore identifiers nor to trust target-linked identifiers merely because they appear target-linked. It is narrower:

> **When an individuation claim depends on a formal difference, expose the target factorization and the scientific reason for accepting it; then evaluate the claim relative to an explicitly specified observational or interventional regime.**

## References

Bueno, Otávio, Ruey-Lin Chen, and Melinda B. Fagan, eds. 2018. *Individuation, Process, and Scientific Practices*. Oxford University Press. DOI: 10.1093/oso/9780190636814.001.0001.

Chen, Ruey-Lin. 2018. "Experimental Individuation: Creation and Presentation." In *Individuation, Process, and Scientific Practices*, 192–213. Oxford University Press. DOI: 10.1093/oso/9780190636814.003.0009.

Contessa, Gabriele. 2007. "Scientific Representation, Interpretation, and Surrogative Reasoning." *Philosophy of Science* 74(1): 48–68. DOI: 10.1086/519478.

Dieks, Dennis, and Marijn A. M. Versteegh. 2008. "Identical Quantum Particles and Weak Discernibility." *Foundations of Physics* 38: 923–934. DOI: 10.1007/s10701-008-9243-z.

Hennessy, Matthew, and Robin Milner. 1985. "Algebraic Laws for Nondeterminism and Concurrency." *Journal of the ACM* 32(1): 137–161. DOI: 10.1145/2455.2460.

Kivioja, Teemu, Anna Vähärautio, Kasper Karlsson, Martin Bonke, Martin Enge, Sten Linnarsson, and Jussi Taipale. 2012. "Counting Absolute Numbers of Molecules Using Unique Molecular Identifiers." *Nature Methods* 9(1): 72–74. DOI: 10.1038/nmeth.1778.

Ladyman, James, Øystein Linnebo, and Richard Pettigrew. 2012. "Identity and Discernibility in Philosophy and Logic." *The Review of Symbolic Logic* 5(1): 162–186. DOI: 10.1017/S1755020311000281.

Love, Alan C. 2018. "Individuation, Individuality, and Experimental Practice in Developmental Biology." In *Individuation, Process, and Scientific Practices*, 165–191. Oxford University Press. DOI: 10.1093/oso/9780190636814.003.0008.

Mitchell, John C. 1986. "Representation Independence and Data Abstraction." In *Proceedings of the 13th ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages*, 263–276. Association for Computing Machinery. DOI: 10.1145/512644.512669.

Nguyen, James. 2017. "Scientific Representation and Theoretical Equivalence." *Philosophy of Science* 84(5): 982–995. DOI: 10.1086/694003.

Nguyen, James, Nicholas J. Teh, and Laura Wells. 2020. "Why Surplus Structure Is Not Superfluous." *The British Journal for the Philosophy of Science* 71(2): 665–695. DOI: 10.1093/bjps/axy026.

Rutten, Jan J. M. M. 2000. "Universal Coalgebra: A Theory of Systems." *Theoretical Computer Science* 249(1): 3–80. DOI: 10.1016/S0304-3975(00)00056-6.

Smith, Tom, Andreas Heger, and Ian Sudbery. 2017. "UMI-tools: Modeling Sequencing Errors in Unique Molecular Identifiers to Improve Quantification Accuracy." *Genome Research* 27(3): 491–499. DOI: 10.1101/gr.209601.116.

Suárez, Mauricio. 2004. "An Inferential Conception of Scientific Representation." *Philosophy of Science* 71(5): 767–779. DOI: 10.1086/421415.

Waters, C. Kenneth. 2018. "Ask Not 'What Is an Individual?'" In *Individuation, Process, and Scientific Practices*, 91–113. Oxford University Press. DOI: 10.1093/oso/9780190636814.003.0005.
