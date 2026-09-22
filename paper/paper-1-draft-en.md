# Working Draft — Paper 1

> **Status:** Primary English working manuscript. Non-authoritative.
> **Scope:** Necessary evidential conditions for operational individuation claims under declared target semantics and restricted tests.
> **Formal boundary:** The target domain and representation-to-target map are model inputs. The paper audits proposed evidential links; it does not derive target ontology, latent source assignment, or metaphysical numerical identity.

# When Is a Formal Difference Admissible Evidence for an Individuation Claim?
## Representation, Evidential Bridges, and Restricted Tests

## Abstract

A formal difference between representations is not by itself evidence that represented targets are distinct. We formulate an individuation-specific admissibility framework separating representation features, target reference, evidential bridges, and admitted tests. A representation-level feature may contribute only when an independently justified experimental, causal, measurement, or semantic bridge connects it to the target; declaration alone does not supply warrant. A UMI sequencing case contrasts arbitrary read identifiers with experimentally grounded molecular tags. A small Lean artifact audits bridge dependence, relabeling invariance, and test-relative refinement. The framework states necessary, not sufficient, conditions for operational individuation claims.

## 1. Introduction

A formal model can contain two different representations without thereby providing evidence for two different target-level individuals. Variables, constructors, row identifiers, memory addresses, labels, and carrier elements can differ because of how a model is encoded rather than because the represented world contains two individuals.

The problem addressed here is therefore not a general metaphysics of identity. It is an evidential question:

> **When may a difference inside a representation be used as evidence for an operational individuation claim about the represented target?**

The negative answer is straightforward but easy to violate: representation-level inequality alone is insufficient. The positive answer requires more structure. A representation-level feature can contribute to an individuation inference only when a defensible evidential bridge connects that feature to the target of the claim, and the resulting target-relevant difference is detectable under the tests admitted by the analysis.

The condition is **necessary, not sufficient**. A target-linked feature can still be unreliable, confounded, noisy, or badly calibrated. The framework therefore does not turn target relevance into complete epistemic warrant. It asks a prior dependency question: has the argument shown why this formal difference is evidence about the target at all?

This yields a practical audit:

> **If a representation-level identifier were arbitrarily reassigned while all independently justified target-relevant relations were held fixed, should the individuation conclusion change?**

If the answer is yes, the argument owes an account of the evidential bridge from that identifier to the target. If no such bridge can be supplied, the identifier is doing representational rather than target-level work.

This question is adjacent to established work on scientific representation, theoretical equivalence, representation independence, observational equivalence, discernibility, and experimental individuation. The closest conceptual comparison is Nguyen's target-directed account of scientific representation and theoretical equivalence: models can be compared by the claims they license about the same targets. The present paper asks a narrower downstream question: when a **difference in the representation itself** is offered as evidence for an individuation claim, what must connect that difference to the target before the inference is admissible?

### 1.1 Contributions

The paper makes three limited contributions.

1. **An explicit evidential-bridge condition.** It separates representation-level features from target-level properties and makes the bridge between them an explicit dependency. Declaring a bridge exposes the dependency; scientific justification for that bridge must come from the relevant experimental, causal, measurement, or semantic practice.

2. **A relabeling-invariance diagnostic with a scientific case.** The counterfactual reassignment test detects when identifiers or labels are doing hidden individuating work. A UMI sequencing case shows why two syntactically similar identifiers can differ epistemically: ordinary read identifiers distinguish records, whereas pre-amplification molecular tags can acquire target relevance through the experimental protocol.

3. **A mechanized dependency audit.** A small Lean development checks the bridge logic, test-family refinement, and negative controls for representation-sensitive and semantically inert identity-like features. The mathematics is intentionally elementary; the purpose is to make dependency claims executable rather than to claim a new general equivalence theory.

## 2. Formal Setting

### 2.1 Representations and targets

Let \(P\) be a set of representations and \(T\) a target domain. Let

\[
r:P\to T
\]

be a representation-to-target map. Distinct elements of \(P\) are not assumed to represent distinct elements of \(T\).

The map \(r\) is a semantic/modeling input. This paper does not infer \(r\) from observations. In applications where source assignment is itself uncertain, the framework audits a proposed assignment model rather than solving the source-assignment problem.

The formal core is restricted to one target value per representation. Many-to-many and probabilistic correspondence relations are natural extensions, but they are not required for the present dependency claim.

### 2.2 Representation features and evidential bridges

Let a representation-level feature be a function

\[
f:P\to V
\]

and let a target-level property be

\[
\phi:T\to V.
\]

For the exact setting used here, say that \(f\) has a **target bridge** to \(\phi\) when

\[
W(f,\phi)
\quad\Longleftrightarrow\quad
\forall p\in P,\; f(p)=\phi(r(p)).
\]

This factorization matters because it distinguishes two claims that are otherwise easy to conflate:

\[
f(a)\neq f(b)
\]

is only a representation-level difference, whereas

\[
W(f,\phi)\land f(a)\neq f(b)
\]

supports the target-level conclusion

\[
r(a)\neq r(b).
\]

The proof is elementary: if \(r(a)=r(b)\), then \(\phi(r(a))=\phi(r(b))\), and the bridge forces \(f(a)=f(b)\).

The important point is not the mathematics but the dependency. **Declaration does not create epistemic warrant.** In a scientific application, accepting \(W(f,\phi)\) requires an independent reason grounded in the relevant experiment, causal chain, measurement procedure, calibration, or semantics. The formal bridge records the claimed connection so that the argument can be audited.

### 2.3 Admitted tests

Let \(Q\) be a class of target-sensitive tests. Depending on the application, a test may be an observation, measurement, query, or intervention; the framework does not identify these classes.

For \(q\in Q\) and \(t\in T\), let \(O(q,t)\) be the outcome of test \(q\) on target \(t\). Let \(A\subseteq Q\) be the family admitted by a particular analysis. “Admitted” does not mean “declared at will”: the analysis must independently justify why those tests bear on the target and claim at issue.

Define

\[
a\equiv_A b
\quad\Longleftrightarrow\quad
\forall q\in A,\;O(q,r(a))=O(q,r(b)),
\]

and

\[
a\mathrel{\#_A}b
\quad\Longleftrightarrow\quad
\exists q\in A:\;O(q,r(a))\neq O(q,r(b)).
\]

These relations are operational and test-relative. They are not definitions of metaphysical numerical identity.

## 3. Scientific Case: UMI-Based Molecular Counting

High-throughput sequencing gives a direct example of the inference problem. PCR amplification can produce many downstream reads from one pre-amplification DNA or RNA molecule. A hypothetical data set containing 100 read records therefore does not, merely by containing 100 records, support the conclusion that 100 source molecules were present.

Kivioja et al. (2012) introduced unique molecular identifiers (UMIs) to support molecule counting by attaching molecular tags before amplification. Smith, Heger, and Sudbery (2017) later showed why the tags still require error-aware analysis: UMI sequences can themselves contain sequencing errors, and naive use of token equality can misidentify PCR duplicates.

The case contrasts two formally similar features.

An ordinary software read identifier is assigned to a read record for data handling. Its inequality distinguishes two representations:

\[
f_{\mathrm{readID}}(a)\neq f_{\mathrm{readID}}(b).
\]

That difference alone supplies no bridge to source-molecule plurality.

A pre-amplification UMI is different because the experimental procedure is designed to connect the tag to a source molecule before the representational multiplicity created by PCR arises. In the idealized formal model, the protocol supplies the candidate bridge between an observed tag feature and a target-level molecular property.

The idealization can be mapped as follows: \(P\) is the set of downstream read records; \(T\) is the set of pre-amplification source molecules; \(r(p)\) is the source molecule of read \(p\); and admitted tests include the experimentally introduced tag together with the alignment and contextual information used by the analysis.

Crucially, actual investigators do not directly observe \(r\). Source assignment is inferred through the protocol, alignment, barcode statistics, and error assumptions. The framework therefore does **not** reconstruct molecular deduplication from raw data. It audits a proposed source-assignment and evidential model: which observed differences have an independently defensible route to the source molecules, and which differences merely distinguish downstream records?

The UMI case also prevents an overly simple conclusion. Target relevance is not infallibility. Barcode collisions, sequencing errors, and other failure modes mean that “same UMI” and “different UMI” cannot be treated as unrestricted numerical-identity rules. Experimental provenance makes the tag evidentially relevant; the error model determines how strongly particular tag observations support a molecular-counting inference.

## 4. Test-Relative Distinguishability

Let \(A_c\subseteq A_f\). Under fixed exact outcome semantics,

\[
a\equiv_{A_f} b
\Longrightarrow
a\equiv_{A_c} b.
\]

The converse need not hold. A pair may be unresolved under a restricted family and distinguished after an additional target-sensitive test is admitted.

The interpretation is deliberately narrow:

> **Under fixed exact semantics, enlarging a justified test family can refine the induced operational classification.**

This is not a theorem that more empirical evidence can never reverse a judgment. Noise, statistical updating, changing models, and measurement disturbance are outside the exact semantics used by the formal fixture.

## 5. Mechanized Dependency Audit

The Lean artifact is a dependency audit, not a claim of deep mathematical novelty.

The finite model contains three presentations, an explicit grounding map into a referent carrier, a representation-sensitive negative-control probe, two target-sensitive probes, coarse and fine access regimes, and an arbitrary identity-like token carrier.

The new bridge layer makes the central dependency explicit. A presentation-level Boolean feature may be paired with a target-level Boolean property only through a bridge that factors the feature through the grounding map. The artifact checks four bridge facts: equal grounding forces equality of a bridged feature; a difference in a bridged feature entails a grounding difference; the deliberately representation-sensitive encoding probe admits no such bridge because it separates two same-grounding presentations; and a positive-control feature that directly tracks grounding does admit one.

The older negative controls remain useful but secondary. Same-reference re-encodings have the same target-sensitive profile. A restricted test family can fail to separate a pair that a richer family separates. Arbitrary reassignment of a semantically inert identity-like token leaves the tested classification unchanged for any token carrier type.

These results are intentionally simple. Their role is to expose hidden dependencies. If the model claims that an identifier is irrelevant, the formal definitions make it possible to check whether that identifier actually enters the target map, bridge, test accessibility, or outcome semantics.

## 6. Relation to Existing Work

### 6.1 Scientific representation and theoretical equivalence

Suárez (2004) and Contessa (2007) already treat scientific representation as target-directed and inferential. Nguyen (2017) is the closest comparison for the present argument: he connects scientific representation with model and theoretical equivalence by asking whether models license the same claims about the same target systems.

The present paper does not claim novelty for target-directed inference or same-target claim licensing. Its narrower question begins when a **formal difference inside a representation** is itself offered as evidence for target plurality. Two models may be used to license claims about the same target while still differing in numerous representation-level features. The issue here is whether any such feature is admissible in an individuation inference. The bridge condition isolates that dependency: the feature must have a justified route to a target-level property rather than merely be formally discriminating.

### 6.2 Individuation in scientific practice

Practice-oriented work asks how scientists count, track, separate, manipulate, and present entities in concrete experimental settings (Bueno, Chen, and Fagan 2018; Waters 2018; Love 2018). Chen (2018) distinguishes ontological and epistemological modes of experimental individuation and explicitly treats presentation as part of individuation practice.

The present framework does not claim that the distinction between presentation and individuation is new. It supplies a narrower formal audit for one recurrent inferential risk: when a representational device is used in an individuation practice, what justifies treating differences in that device as evidence about the target?

### 6.3 Technical neighbors

Representation independence (Mitchell 1986) constrains dependence on implementation details; observational and behavioral equivalence (Hennessy and Milner 1985; Rutten 2000) classify systems relative to specified interactions; and work on identity and discernibility cautions against equating formal discernibility with unrestricted numerical identity (Ladyman, Linnebo, and Pettigrew 2012; Dieks and Versteegh 2008).

The present relation is mathematically modest by comparison. Its contribution is methodological and individuation-specific: **representation-level discrimination is not admissible target-level evidence unless the dependency is exposed and justified.**

Nor does the negative result imply that representation-only or surplus structure is useless. Such structure may be indispensable for other representational, computational, or local purposes (Nguyen, Teh, and Wells 2020).

## 7. Scope and Limitations

The framework deliberately leaves several problems open.

First, \(T\) and \(r\) are inputs. The paper does not derive the target ontology or solve uncertain source assignment. In the UMI case, the actual read-to-molecule relation is latent and must be inferred by scientific methods outside the exact formal core.

Second, the bridge condition is exact and deterministic. Real scientific warrants can be probabilistic, error-prone, and model-dependent. The exact bridge should therefore be read as a dependency skeleton, not a complete theory of evidence.

Third, target relevance and test discrimination are necessary but not sufficient for epistemic warrant. Reliability, calibration, confounding, background assumptions, and statistical decision rules can still defeat an individuation inference.

Fourth, the formal core uses a function \(r:P\to T\). Many-to-many, distributed, and probabilistic representation-target relations are outside the current scope.

Fifth, observation and intervention are not equated. Different test classes can induce different operational partitions, and no result licenses an inference from observational equivalence to interventional equivalence.

Finally, operational distinguishability is not metaphysical numerical identity, and synchronic discrimination does not by itself establish diachronic persistence.

## 8. Relabeling Invariance as a Practical Audit

The framework can be used without reproducing the entire formalism.

For any identifier-like feature used in an individuation argument, ask two questions. First, would arbitrary reassignment of that feature alter the conclusion if the independently justified target relations were held fixed? Second, if it would, what experimental, causal, measurement, or semantic bridge explains why?

This separates two failure modes.

A **representation-only discriminator** changes the encoding or bookkeeping while leaving the target-relevant model fixed. Such a feature cannot acquire evidential force merely from formal inequality.

A **bridged discriminator** participates in a justified process connecting the representation to the target. Its values may therefore contribute evidence, but only subject to the reliability and error assumptions of that bridge.

The UMI case instantiates the distinction. Read IDs fail the molecular relabeling audit; pre-amplification UMIs are designed to survive it because changing the tag while holding the actual tagging history fixed would change the recorded evidence about that history. The force comes from the experimental provenance, not from identifierhood.

## 9. Formal Audit Summary

The public development contains a broader set of elementary checks than the argument needs in the main text. For anonymous review, the claims are grouped under neutral labels.

R1--R4 cover the separation between representation-sensitive discrimination and same-reference target-sensitive invariance. R5--R7 cover test-family inclusion and the coarse/fine witness. R8--R10 cover target-sensitive outcome differences and the positive-control target distinction. R11--R15 cover token and access-metadata invariance. R16--R19 cover the new bridge layer: same-grounding preservation for bridged features, bridge-licensed inference from feature difference to grounding difference, failure of a bridge for the representation-only encoding probe, and existence of a bridge for a positive-control ground-tracking feature.

The claim is not that nineteen elementary results constitute a new mathematical theory. The collection is an executable audit surface: it records which assumptions each individuation step actually depends on.

## 10. Conclusion

A formal difference is not admissible evidence for an individuation claim merely because it distinguishes two representations.

The missing step is an evidential bridge. A representation-level feature may contribute to target-level individuation only when an independently justified experimental, causal, measurement, or semantic relation connects that feature to the target. A difference must then survive the relevant admitted tests. These are necessary conditions, not a complete epistemology of individuation.

UMI-based molecular counting shows why the distinction matters. A read identifier and a molecular barcode can have the same formal type while playing very different evidential roles. The difference is explained by provenance and error-aware measurement practice, not by the syntax of an identifier.

The formal contribution is correspondingly modest: make the bridge explicit, make relabeling invariance testable, and make hidden dependence on representation-level identity mechanically auditable.

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
