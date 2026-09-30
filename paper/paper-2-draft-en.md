# Working Draft — Paper 2

> **Status:** Primary English working manuscript v0. Non-authoritative.
> **Scope:** Concept-neutral decomposition and reconstruction of cognitive-capacity claims under partial observability and bounded information.
> **Evidence boundary:** Quantitative statements in this draft are drawn from frozen repository artifacts through Paper 2 Result v1. Related-work citation integration and venue formatting remain pending.
> **Reliability boundary:** The 60-claim reference corpus is source-grounded and full-text reviewed. Independent extractor agreement and deterministic model replay are not established.

# Toward a Concept-Neutral Measurement Basis for Cognitive Capacities

## Abstract

Scientific theories of cognition divide mental capacities into constructs such as memory, learning, skill, attention, prediction, control, belief, and concept. The labels are useful for communication, but label difference alone does not establish structural difference, and shared terminology does not guarantee a shared mechanism. We develop a concept-neutral method for comparing cognitive-capacity claims under partial observability and bounded information. A designed corpus of 60 claims—48 primary claims sampled across eight construct strata and 12 non-tuning challenge claims—was converted into source-grounded, machine-readable ClaimIR representations and fully reviewed against the corresponding source texts. We then projected claims into a frozen structural basis, compared whole-claim structures, diagnosed failure modes, reconstructed bounded reusable substructures, and reverse-projected the resulting structures into a compact system-role grammar.

The analysis deliberately preserves failed intermediate results. Whole-claim comparison produced 1,770 incomparable claim pairs and no equivalence or refinement relation. A post hoc diagnostic localized this failure primarily to an enriched comparison surface that blocked candidate pairs before topology was reached. We therefore replaced whole-claim identity as the unit of reuse with bounded subobject reconstruction under frozen forgetting rules. This yielded 213 lane-local candidate objects, 206 unique global Archetype/XLike objects, seven exact cross-lane equivalence components, 470 direct refinement edges, 2,894 strict subobject relations in transitive closure, and 99 cross-lane families. The bounded reconstruction covered 59 of 60 claims and passed eight destructive controls.

A subsequent reverse projection of all 60 claims supports a recurrent system-role grammar with roles for individuation or partition, configuration, realizability constraints, criterion-conditioned orientation, directional interface operations, typed transformation or dependence, temporal succession, and boundary-relative observation. Twenty-one claims were fully represented, 22 partially represented, and 17 retained residual structure. Adjudication of those residuals found no top-level role gap: 13 were primarily source-context parameters and four were primarily claim-language relation gaps. Strict-preservation comparisons show that a generic X/K/T dynamical view and a generous POMDP-like view recover substantial substructure but erase distinctions frozen in the corpus unless omitted roles are reintroduced.

The resulting proposal is intentionally narrower than a definition of cognition. It is a measurement-oriented system grammar recovered from a bounded reviewed corpus. It is not a complete scientific claim language, an ontology of nine substances, or a theorem of absolute mathematical minimality. The architecture further separates the cognitive system from World, cross-boundary coupling, experimental protocol, and the claim language used by scientists to describe them. This separation provides a reproducible basis for larger-scale validation without requiring construct labels to be treated as primitives.

## 1. Introduction

Cognitive science inherits a large vocabulary of capacities: memory, attention, learning, belief, skill, prediction, control, concepts, and many others. These labels organize literatures, experiments, textbooks, and institutions. They also create a methodological problem. A scientific field can accumulate names faster than it accumulates evidence that the named capacities are structurally distinct.

The converse problem is equally serious. Different labels may be attached to overlapping or closely related structures, while one familiar label may cover heterogeneous mechanisms, measurements, timescales, and experimental operations. Nominal identity and nominal difference are therefore both unreliable guides to structural individuation.

This paper asks whether cognitive-capacity claims can be compared on a common measurement surface without granting construct names privileged status. The target is not a dictionary of definitions and not a replacement taxonomy chosen in advance. The target is a procedure:

[
	ext{source claim}
ightarrow
	ext{label-suppressed structural representation}
ightarrow
	ext{comparison}
ightarrow
	ext{bounded reusable structure}
ightarrow
	ext{auditable grammar}.
]

The motivating setting is cognition under partial observability and bounded information. Scientific claims rarely expose an entire cognitive system. They provide restricted observations, interventions, behavioral outcomes, neural measurements, model variables, task manipulations, and relations among them. A common basis must therefore be able to compare partial structures without pretending that every paper reveals a complete mechanism.

Two commitments guide the analysis. First, no theoretical construct receives privileged treatment from authorship, venue prestige, citation count, disciplinary convention, or historical familiarity. Second, structural similarity is not semantic or ontological identity. The aim is to identify what distinctions are preserved when nominal and authority-bearing information is removed, not to declare that two named constructs are “really the same thing.”

The paper proceeds through a deliberately adversarial sequence. We first freeze the source and representation contracts, then test whole-claim comparison. When the whole-claim atlas collapses into universal incomparability, we preserve that negative result and diagnose it rather than relaxing the rules until a desired clustering appears. We then ask whether reusable structure survives at a bounded subobject level. Only after that reconstruction do we infer a compact role grammar and attack it with residual and comparator tests.

The central contribution is therefore methodological and empirical rather than theorem-theoretic: heterogeneous cognitive claims are decomposed under a shared contract, failed compression attempts are retained, surviving substructures are reconstructed, and the resulting grammar is tested against the frozen claims that generated it.

## 2. Problem and Inferential Scope

The basic inferential risk is simple:

[
	ext{different construct labels}

otRightarrow
	ext{different cognitive structures},
]

and

[
	ext{same construct label}

otRightarrow
	ext{same cognitive structure}.
]

A useful comparison system must therefore distinguish at least three levels.

First is the source-level scientific claim: what a paper actually states, models, manipulates, or measures. Second is a representation of that claim that removes information irrelevant to the structural comparison. Third is the target structural relation recovered across claims.

This paper treats the comparison as measurement-relative. A structural representation may preserve distinctions useful for one scientific question while forgetting distinctions important for another. Accordingly, an equivalence under the frozen projection is never promoted to full semantic equivalence, and a refinement relation is not treated as causal or ontological priority.

The analysis also separates a system grammar from a scientific claim language. A grammar may contain enough roles to describe a modeled cognitive system while remaining unable to directly express statements such as “these observations distinguish two latent explanations,” “the evidence does not entail a unique interpretation,” or “two outcomes differ under a specified comparison.” Those are statements about systems, evidence, and inference. Their absence from a system grammar is not automatically evidence for a missing cognitive primitive.

The same separation applies to experimental context. A condition used to construct a trial, define a comparison, or delimit an observation window is not automatically an intrinsic constraint of the cognitive system. This distinction becomes important in the residual analysis.

The strongest permitted conclusion is therefore bounded:

> A recurrent structural grammar can be recovered from the reviewed corpus under the declared representation and forgetting rules, and several weaker views demonstrably erase distinctions that the frozen analysis preserves.

The paper does not claim to define cognition exhaustively, discover a unique ontology, or prove that no alternative encoding can represent the same claims.

## 3. Retrieval and Designed Corpus

The broader retrieval program was built to prevent the final 60-claim surface from being selected in response to decomposition outcomes. The retrieval frame began from a mixed set of canonical works and broad text and anchor queries spanning cognitive science, neuroscience, artificial intelligence, information theory, embodied and dynamical approaches, and classical construct literatures. Citation count was used as a retrieval and ranking variable, not as evidence that a construct or claim was scientifically correct.

The final designed Paper 2 corpus contains 60 claims. Forty-eight primary claims are divided evenly across eight historical construct strata:

- Memory: 6
- Learning: 6
- Skill: 6
- Attention: 6
- Prediction: 6
- Control: 6
- Belief: 6
- Concept: 6

A separate 12-claim challenge set was frozen as a non-tuning surface. Its pressures include multi-timescale organization, stochastic or approximate structure, constitutive boundaries, compositional or systematic structure, embodied or world-coupled organization, normative or value criteria, hybrid labels, label-coordinate mismatch, multi-condition structure, same-inventory/different-topology pressure, strict-refinement pressure, and high structural heterogeneity.

The challenge set was not allowed to tune the frozen source selection, ClaimIR schema, working basis, or comparison semantics. This separation matters because a challenge corpus ceases to be a meaningful stress test if its failures are used to modify the representation until those same cases pass.

Each activated slot uses one primary claim per work. The primary and challenge surfaces together form the bounded empirical target of this paper. Population-scale validation is explicitly deferred to Paper 3.

## 4. Source-Grounded ClaimIR Construction

Each of the 60 designed claims was represented in ClaimIR v1, a source-grounded intermediate representation containing provenance, claim-level scope and modality, typed nodes, typed relations, source-span locators, and extraction metadata.

The primary extraction path used an interactive language model as a structured research assistant, but model output was not treated as ground truth. Every retained record had to remain auditable from the stable source identity and source-local evidence. The scientific object is therefore the reviewed ClaimIR record, not the hidden model response that first proposed it.

All 60 current ClaimIR files have manual_review_status = reviewed. The integrated manifest records:

[
48/48 	ext{primary}
+
12/12 	ext{challenge}
=
60/60 	ext{reviewed claims}.
]

Full-text review materially corrected many initial extractions. Typical corrections included narrowing population scope, separating experimental manipulation from endogenous response, restoring omitted intermediate states, distinguishing latent estimates from observed quantities, correcting temporal organization, and preserving source-explicit limitations. These corrections are a feature of the audit process rather than evidence that first-pass automated extraction was reliable.

The extraction-reliability result is correspondingly conservative. The structural comparator used to compare ClaimIR documents was validated, but historical local two-pass extraction calibrations produced zero valid ClaimIR records in both the v2 and v3 real calibration transactions. The valid A/B agreement denominator was therefore zero. Later interface defects were diagnosed and synthetically repaired, but no positive independent-extractor agreement result is claimed for the primary corpus.

The manuscript-level reliability boundary is:

[
	ext{source-grounded reviewed reference corpus}
=
	ext{established},
]

while

[
	ext{independent extractor agreement}
=
	ext{not established}.
]

This distinction is retained throughout the paper.

## 5. Concept-Neutral Structural Representation

ClaimIR preserves source-grounded scientific structure, but it is still too source-specific to serve directly as a common comparison object. The next layer therefore removes or suppresses information that should not decide structural similarity merely because it appears in a paper.

The frozen structural pipeline excludes author identity, institution, venue, citation count, historical construct labels, source-local node identifiers, and other presentation tokens from the comparison logic. It preserves typed claim structure, relation topology, temporal organization, intervention and probe information, criterion and constraint states, approximation structure, and declared bridge assumptions.

The intended transformation is:

[
	ext{scientific use}
ightarrow
	ext{typed structural claim}
ightarrow
	ext{label-independent comparison}.
]

This is not equivalent to eliminating semantics. The role vocabulary and relation types are semantically constrained by the source-grounded extraction contract. What is suppressed is the assumption that the historical name of a construct should itself determine whether two structures are identical or distinct.

The resulting representation is deliberately partial. It encodes the structure needed for the Paper 2 comparison task, not every scientifically meaningful fact in the source. This is why later residuals can be scientifically meaningful without implying that the structural basis has failed.

## 6. Frozen Working Basis B_P2

Before the designed-corpus outcomes were inspected, Paper 2 froze a working structural basis:

[
B_{P2} = {S,Pi,K,O,T,C,Q,P}.
]

The basis was treated as a measurement coordinate system rather than an ontology.

Its roles were initially interpreted as follows:

- S: state or structure carrier;
- (Pi): partition, subsystem, role, class, or individuation structure;
- K: typed dependence or transformation;
- O: observation, response, information, or outcome position;
- T: temporal placement, ordering, recurrence, persistence, history, or horizon structure;
- C: resource, capacity, realizability, or admissibility constraint where source evidence supports that reading;
- Q: criterion, objective, threshold, correctness, relevance, reference, or other orientation structure;
- P: experimentally or operationally relevant intervention/probe control.

The decomposition contract prevents lexical shortcuts. A source node called a “condition” is not automatically C. A variable called “reward” does not exhaust Q. A relation is not automatically K if its role is purely temporal. A partition need not be physical. An observation need not be terminal.

The basis was intentionally permissive enough to preserve heterogeneous claims but frozen tightly enough that failures could not be repaired post hoc by inventing claim-specific coordinates.

Later Grammar-v0 work reinterprets S as a generic configuration carrier X and splits P directionally into (P_{in}) and (P_{out}). That later compression is downstream of the frozen basis and does not retroactively alter the original decomposition records.

## 7. Phi and Whole-Claim Comparison

The frozen Phi projection was designed to compare complete claim structures after suppressing nominal and provenance information. It preserves claim type, modality, scope shape, typed node and relation topology, active basis coordinates, temporal presence states, control states, approximation mode, and the multiplicity and grounding of bridge assumptions.

Phi forgets authorship, institution, venue, citation count, construct label, source-local identifiers, free-text descriptions, literal temporal values, and other presentation-specific information.

The comparison semantics distinguish:

- EQUIVALENT: isomorphism under the frozen projected structure;
- REFINEMENT: an injective structure-preserving embedding with additional structure in the stronger object;
- FORGETTING: the omission witness associated with a verified refinement;
- INCOMPARABLE: neither object embeds into the other;
- MUTUAL_EMBEDDABILITY_NONISOMORPHIC: recorded separately rather than collapsed into equivalence.

For 60 claims there are

[
inom{60}{2}=1770
]

unordered pairs.

The global frozen whole-claim result was striking:

[
1770/1770 = 	ext{INCOMPARABLE}.
]

No whole-claim equivalence or refinement component survived the frozen comparison.

This negative result is central to the paper because it demonstrates why a concept-neutral coordinate system cannot be evaluated only by whether it produces visually satisfying clusters. A comparison rule can be formally precise and still be scientifically unhelpful if its conjunction of preserved fields makes every claim unique.

## 8. Whole-Claim Incomparability Diagnostic

The universal incomparability result triggered a diagnostic rather than a repair.

Across the 3,540 directed claim-pair comparisons, 3,518 failed at the scalar comparison stage, six reached node-count comparison, 16 reached node-label multiset comparison, and none reached topology or embedding. The dominant failure sources included modality, claim type, active-axis combinations, scope shape, approximation mode, probe state, and temporal-state fields.

The diagnostic therefore rejected a simple interpretation that “the eight basis roles themselves are necessarily too expressive.” Active-axis profiles showed substantial reuse: there were only 26 unique active-axis profiles across the 60 claims, and an active-axis-only comparison would have yielded many equal or subset-comparable pairs. Universal incomparability arose primarily from the enriched Phi/comparison surface before graph topology could be tested.

The frozen diagnostic classification was correspondingly severe but localized:

[
	ext{BASIS_TOO_EXPRESSIVE_OR_VACUOUS}
]

for the complete coordinate/comparison apparatus on the designed whole-claim surface, with the failure mechanism localized primarily to enriched pre-topology comparison constraints rather than to the eight-axis inventory alone.

No field was then deleted merely because deletion would produce attractive clusters. Instead, the next analysis changed the unit of reuse.

## 9. Archetype and Bounded XLike Reconstruction

Whole scientific claims often contain a shared mechanism plus source-specific scope, controls, temporal qualifiers, comparisons, and auxiliary structure. Requiring whole-claim isomorphism therefore asks a stronger question than whether reusable cognitive structure recurs.

Paper 2 next reconstructed bounded subobjects under a frozen basis-subobject forgetting operator. The operator permits restriction to retained typed substructure but forbids arbitrary rewiring or semantic relabeling. Candidate subobjects must remain recoverable from their source claims under the predeclared rules.

Lane-local reconstruction produced 213 candidate objects. Global deduplication yielded:

[
206 	ext{unique Archetype/XLike objects}.
]

Seven exact cross-lane equivalence components were recovered. The global refinement structure contained 470 direct refinement edges and 2,894 strict subobject relations in transitive closure.

The bounded XLike reconstruction retained:

[
99 	ext{cross-lane families},
]

and

[
107 	ext{lane-local-only families}.
]

There were 188 distinct support signatures. Fifty-nine of the 60 claims were covered by at least one surviving bounded object at this stage.

The reconstruction also passed eight destructive controls. These tested rejection of trivial cores, label deletion, permissive-forgetting pressure, richer competing cores, overlapping incomparable cores, cross-label recurrence, compatibility with whole-object incomparability, and presentation invariance. Notably, 1,304 whole-claim pairs shared at least one surviving Archetype even though all 1,770 whole-claim pairs were frozen as incomparable. This establishes that reusable substructure and whole-claim identity are different questions.

The bounded result therefore reverses the earlier null in a controlled way. Whole-claim compression failed, but bounded reusable structure survived without reopening the frozen claim representation or adding a post-outcome abstraction threshold.

## 10. Unified Cognitive Structural Grammar v0

The surviving Archetypes suggested that the original basis roles could be interpreted more compactly as roles in one reusable system grammar.

Grammar v0 uses:

[
{Pi, X, C, Q, P_{in}, P_{out}, K, T, ho/O}.
]

Here:

- (Pi) marks individuation, partition, boundary, role decomposition, classification, or recursive refinement;
- X is a generic configuration carrier;
- C specifies realizability or admissibility constraints;
- Q provides criterion-conditioned filtering or orientation;
- (P_{in}) is an interface operation directed into the modeled system boundary;
- (P_{out}) is a probe, query, or read operation exposing system-relative structure;
- K is typed transformation or dependence and need not be functional or deterministic;
- T supplies succession or temporal indexing and remains distinct from K;
- (ho/O) represents boundary-relative observation, trace, or projection and need not be terminal output.

A compact schematic form is:

[
X_{n+1}=K_{n;C,Q,P_{in}}(X_n),
]

with observation represented schematically as

[
O_n=ho_{Pi,C,P_{out},n}(X_n).
]

These expressions are mnemonic rather than commitments that every claim instantiates every role or that every K is a function.

The Lean formalization makes the non-functionality explicit by representing transition and observation relationally. It also makes an important temporal correction. Because configuration types may vary with time, persistence is not universally (K=I). Cross-time persistence requires an explicit carry or transport map

[
c_{t,t'}:X_tightarrow X_{t'}
]

with evidence that the relevant transition realizes that carry. Literal identity is licensed only when the time-indexed fibers have already been identified.

Grammar v0 is therefore a reusable role grammar, not nine ontological substances.

## 11. Sixty-Claim Reverse Projection

Grammar v0 was then tested by reverse-projecting the frozen structure of all 60 claims back into the new role vocabulary. The reverse projection did not reread source papers and did not alter ClaimIR, the original basis, Phi, structural adjudications, or bounded Archetype identities.

The claim-level results were:

[
	ext{FULL}=21,
qquad
	ext{PARTIAL}=22,
qquad
	ext{RESIDUAL}=17.
]

The role frequencies, counting a role once per claim when supported or partially supported, were:

| Role | Claims |
|---|---:|
| (Pi) | 15 |
| X | 53 |
| C | 13 |
| Q | 36 |
| (P_{in}) | 29 |
| (P_{out}) | 40 |
| K | 57 |
| T | 47 |
| (ho/O) | 56 |

Several conclusions follow directly from these counts.

First, X, K, T, and (ho/O) form a broad recurrent backbone, but the sparser roles cannot be dismissed as ornamental. Pi, C, Q, and the directional interface roles each have independent witnesses across multiple construct lanes.

Second, no claim requires all roles. The grammar is compositional: a claim instantiates the roles needed to preserve its structure.

Third, the distinction between K and T is empirically necessary. Temporal precedence cannot simply be encoded as transformation without losing frozen distinctions.

Fourth, interface direction matters. Twenty-six claims instantiate both (P_{in}) and (P_{out}) in the same claim, while other claims instantiate only one direction.

The residuals therefore become the crucial hostile test: if they recurrently require one additional system role, Grammar v0 is incomplete in a straightforward sense. If they fail for other reasons, the architecture must separate those reasons instead of adding a primitive by default.

## 12. Residual Adjudication

The 17 residual claims were classified under a frozen residual taxonomy:

- ROLE_GAP;
- RELATION_LANGUAGE_GAP;
- FORMAL_CARRIER_GAP;
- DERIVED_STRUCTURE_GAP;
- SOURCE_CONTEXT_PARAMETER;
- UNDERDETERMINED.

Only ROLE_GAP was permitted to count as prima facie evidence for a new top-level Grammar role.

The primary classification was:

[
13 	ext{SOURCE_CONTEXT_PARAMETER},
]

[
4 	ext{RELATION_LANGUAGE_GAP},
]

[
0 	ext{ROLE_GAP}.
]

Secondary pressures included six formal-carrier gaps, two derived-structure gaps, one underdetermined case, and one additional relation-language pressure.

The central result is therefore:

[
oxed{	ext{ROLE_GAP}=0}.
]

This does not prove that no future corpus can establish a missing role. It shows that the 17 failures in this frozen hostile test do not currently justify Grammar v1.

The four primary relation-language gaps concern structures such as observation-to-latent inference, condition-indexed dissociation, non-entailment, and other statements whose scientific meaning is not exhausted by the system transition/observation grammar. They motivate a richer claim language, not a new cognitive-system primitive.

The 13 source-context residuals required a second architectural analysis because the word “condition” had previously hidden several different kinds of structure.

## 13. Strict-Preservation Comparator Tests

Minimality was tested under a deliberately strict notion of direct preservation. A comparator preserves a frozen distinction only when it has an explicit role or operation capable of representing that distinction without hiding or retyping it inside a generic state or relation label.

This is not a theorem of absolute mathematical non-encodability. Any sufficiently flexible formalism can often simulate omitted distinctions by enriching its state space or labels. The question is whether the distinction survives as a first-class part of the comparison vocabulary.

The first comparator was a generic dynamical view:

[
G_{dyn}={X,K,T}.
]

Fifty-nine of 60 claims instantiate at least one Grammar-v0 role outside this vocabulary. The only claim whose instantiated role set is a subset of ({X,K,T}) still retains a source-context residual. Under strict direct preservation, therefore:

[
0/60
]

claims are fully preserved by the generic X/K/T view.

The second comparator was a generous POMDP-like view:

[
G_{pomdp}={X,P,K,ho/O,Q,T},
]

with Q already interpreted more broadly than standard scalar reward.

Even under that generous comparison:

[
26/60
]

claims require Pi or C,

[
26/60
]

instantiate both (P_{in}) and (P_{out}) within the same claim, and

[
44/60
]

are affected by at least one of missing Pi, missing C, or collapsed interface directionality.

The formal companion module makes these losses explicit as forgetful views. The X/K/T view existentially forgets the identity of the (P_{in}) operation. The POMDP-like view existentially forgets (P_{out}) query identity and omits Pi and C from its target signature.

The appropriate conclusion is not that generic dynamics or POMDPs “cannot represent cognition.” It is narrower:

> Weaker views exist, but their natural forgetful projections erase distinctions frozen in the reviewed corpus. Recovering those distinctions requires enrichments equivalent to reintroducing omitted structure.

## 14. Layered Claim, System, Context, and Formal Architecture

Residual analysis shows that one formal layer should not be forced to do every job.

Paper 2 therefore separates:

[
L_{sys}
eq L_{claim}
eq L_{ctx}
eq L_{formal}.
]

(L_{sys}) is the cognitive-system role grammar:

[
{Pi,X,C,Q,P_{in},P_{out},K,T,ho/O}.
]

(L_{claim}) contains scientific assertion semantics such as differs, distinguishes, non-equivalence, non-entailment, null effects, model rejection, qualified similarity, and observation-to-latent inference.

(L_{ctx}) contains source-defined contexts and parameters that condition the claim without automatically becoming intrinsic system roles.

(L_{formal}) contains concrete mathematical and machine-checkable realizations, including the current Lean carriers and comparator views.

The dependencies are asymmetric. Claim language can refer to system structure and condition on context. A formalization can realize the system grammar and optionally encode parts of the claim language. Context can parameterize a system without being retyped as C merely because the source calls it a condition.

This separation resolves an important ambiguity in the residuals. A failure to represent “the observation supports one latent interpretation over another” is not the same kind of failure as a missing state variable. Likewise, a task condition chosen by an experimenter is not necessarily an intrinsic realizability constraint.

Derived structures such as persistence, recurrence, history windows, future horizons, duration, and decay profiles remain overlays or derived structure when source evidence supports them. They are not promoted to primitives simply because a concrete formal carrier has not yet been supplied.

## 15. Cognitive System, World, Coupling, and Experiment Boundary

A further distinction emerged when the source-context residuals were reconsidered relative to the system boundary.

Grammar v0 describes the modeled cognitive system. It should not silently absorb the World or the experimental protocol.

The resulting architecture separates:

[
G_{cog},
qquad
W,
qquad
Gamma,
qquad
E_{exp},
qquad
R.
]

Here (G_{cog}) is Grammar v0, W is a World or environment carrier relative to the selected modeled-system boundary, (Gamma) is cross-boundary coupling, (E_{exp}) is the experimental protocol, and R is a realized finite run or history.

This yields three important non-identities:

[
K
eqGamma,
]

[
C
eq	ext{experimental condition},
]

and

[
P_{in/out}
eq	ext{experimental schedule}.
]

K is system transformation or dependence. (Gamma) describes coupling across an already selected system/World boundary. (P_{in}) and (P_{out}) are interface roles available at that boundary; an experiment may schedule particular interface operations without thereby becoming part of the cognitive mechanism.

The 13 source-context residual claims contain 27 explicit generic condition nodes. Architecture-relative placement yielded:

| Placement | Nodes |
|---|---:|
| EXPERIMENT_CONTEXT | 7 |
| WORLD_CONTEXT | 7 |
| RUN_BOUNDARY_OR_PREHISTORY | 4 |
| PARAMETER_ONLY | 5 |
| SYSTEM_INTRINSIC_CONSTRAINT_CANDIDATE | 2 |
| UNDERDETERMINED | 2 |

No node was newly promoted to C.

This analysis also clarifies initial conditions. The start time of a finite experiment need not be the origin of the cognitive system. It is better represented as a run cut:

[
cdotsightarrow X_{t-2}ightarrow X_{t-1}
ightarrow X_{t_0}ightarrow X_{t_1}ightarrowcdots
]

with (t_0) marking the experiment-relative observation start.

The intrinsic admissibility statement

[
C_{t_0}(x_{t_0})
]

says that the realized state is allowed at that cut. It does not explain why that state was realized. The realized state may depend on prior system history, prior World coupling, retained structure, and experimental preparation.

Thus:

[
	ext{intrinsic admissibility}

eq
	ext{realized cut state}

eq
	ext{experimental preparation}.
]

This prevents an initialization mechanism from being added to Grammar v0 merely because finite experiments require a defined starting surface.

## 16. Reliability, Limitations, and Related Positioning

### 16.1 Construct validity and cognitive ontologies

Paper 2 sits downstream of a long construct-validity problem rather than replacing it. Cronbach and Meehl (1955) made explicit that psychological constructs require networks of evidence rather than validation by name alone. Borsboom, Mellenbergh, and van Heerden (2004) sharpened one competing view by tying validity to the existence of an attribute and a causal relation from that attribute to measurement outcomes. The present analysis does not decide among general theories of validity. Its narrower role is to ask whether claims that are already in scientific use preserve the same or different structural distinctions when construct labels are denied evidential authority.

Cognitive-ontology projects are the closest field-level neighbors. The Cognitive Atlas explicitly represents mental concepts and their relations to experimental tasks (Poldrack et al. 2011), while the Cognitive Paradigm Ontology formalizes experimental paradigms in terms of structures such as stimuli, instructions, and responses (Turner and Laird 2012). Poldrack and Yarkoni (2016) frame the broader search for cognitive ontology as an informatics problem concerning mental structure.

Paper 2 shares the goal of making cognitive terminology inspectable, but the unit of analysis differs. It does not begin by declaring a concept ontology or a task ontology. It begins from source-grounded scientific claims, suppresses nominal and authority-bearing information, decomposes the claims into typed structure, and then asks which relations survive a frozen comparison and forgetting contract. Cognitive Atlas and CogPO are therefore complementary precedents rather than baselines that Paper 2 claims to replace.

### 16.2 Generic dynamics and partially observable decision systems

The X/K/T backbone has obvious precedent in dynamical approaches to cognition. van Gelder's dynamical hypothesis explicitly proposed that cognitive agents may be understood as dynamical systems (van Gelder 1998). Paper 2 therefore claims no novelty for representing cognition through state-like configurations, transformations, and time.

The strict-preservation result asks a different question: after heterogeneous source claims have already been frozen, which distinctions are lost if the comparison vocabulary is reduced to X/K/T? Under that test, 59 of 60 claims instantiate at least one additional Grammar-v0 role, and no claim is both fully preserved and exhausted by the generic dynamical vocabulary. This is a corpus-relative distinction-preservation result, not an argument against dynamical modeling.

Partially observable Markov decision processes provide a second important comparator. The canonical POMDP framework combines partially observable state, action, transition, observation, and criterion/reward structure for planning and acting under uncertainty (Kaelbling, Littman, and Cassandra 1998). This overlaps substantially with X, P, K, rho/O, Q, and T. Paper 2's POMDP-like comparator is intentionally generous: Q is allowed to be broader than scalar reward before comparison.

The residual difference is therefore not that POMDPs are mathematically incapable of representing cognitive systems. Arbitrary state augmentation can encode many distinctions. The narrower finding is that a natural POMDP-like projection does not directly preserve Pi, explicit C, the P_in/P_out distinction, generalized Q semantics, and some observation/inference orientations without adding structure equivalent to the distinctions that Grammar v0 keeps explicit.

### 16.3 Boundaries, Markov blankets, and system/World separation

Markov-blanket approaches provide a stronger boundary notion than Grammar-v0 Pi. In Friston's formulation, a Markov blanket separates internal and external states through conditional-independence structure (Friston 2013). Later work explicitly connected Markov blankets with autonomy and active inference (Kirchhoff et al. 2018).

Pi is deliberately weaker and more general. It can represent individuation, partition, role decomposition, classification, or a selected modeled-system boundary without asserting the conditional independencies required for a Markov blanket. A Markov blanket can therefore be represented as a possible specialization of boundary structure when its additional probabilistic conditions are established, but Pi must not be identified with a Markov blanket by default.

This distinction is also why the current architecture separates the cognitive system from World, cross-boundary coupling, and experiment. The boundary is relative to the modeled system; it does not make the environment disappear into system state, nor does an experimental manipulation automatically become an intrinsic cognitive transition.

### 16.4 Category-theoretic and compositional neighbors

Category theory has already been used to characterize structural relations in cognition. Phillips and Wilson (2010), for example, use categorical structure to explain cognitive systematicity in terms of relationships among cognitive processes. Paper 2 therefore does not claim that category-theoretic cognition or structural compositionality is new.

Likewise, categorical cybernetics and lens/optic formalisms provide prior mathematical machinery for bidirectional open systems. St Clere Smithe (2021) develops a categorical account of cybernetic systems using dynamical realizations of generalized open games and Bayesian lenses. These formalisms are especially relevant to the P_in/P_out and system-interface intuitions that appear in Grammar v0.

The relation is again one of possible realization rather than derivation. Paper 2 reconstructs a role inventory empirically from a frozen heterogeneous claim corpus and then asks which established mathematical formalisms can realize or forget those roles. It does not infer the role inventory from category theory, and it does not claim that the current Lean implementation is the unique categorical or mathematical realization.

### 16.5 Reliability and scope limitations

The strongest limitation concerns extraction reliability. The reference corpus is fully source-reviewed, but independent extraction agreement has not been established. The paper must therefore distinguish auditability from autonomous reproducibility.

A reader can inspect the retained source identities, source-local locators, reviewed ClaimIR records, frozen structural contracts, and deterministic downstream transformations. What the paper cannot claim is that a fresh model or human annotator will independently reproduce the same ClaimIR without adjudication.

The second limitation is corpus scale. Sixty designed claims are sufficient for a hostile bounded reconstruction but not for population-level coverage claims. The 1,000-work validation program is deliberately assigned to Paper 3 so that the Paper 2 basis and grammar cannot be tuned to the larger-scale outcomes.

The third limitation is representational relativity. Grammar-v0 roles are recovered under a particular decomposition contract. Their recurrence does not establish that they are the unique mathematical coordinates for cognition. The minimality result is strict-preservation minimality relative to frozen distinctions, not absolute minimality under arbitrary re-encoding.

The fourth limitation is the distinction between system grammar and scientific claim language. Residual assertion semantics remain scientifically meaningful. Paper 2 does not attempt to build a universal language for every epistemic, comparative, causal, or statistical statement appearing in cognitive science.

The fifth limitation is formal realization. The Lean development verifies explicit dependency structure and the absence of several illicit identifications, including the universal reduction of persistence to identity. It does not prove that the current Lean carrier is the unique or final mathematical semantics of Grammar v0.

A further philosophical interpretation is possible but not required for the scientific result. Treating construct names as hypotheses rather than essences is compatible with use-centered and family-resemblance approaches to scientific language. Paper 2 adds an empirical step: suppress the name, decompose the scientific use, measure the surviving structure, and restore provenance only after comparison. This retrospective framing must not be used as evidential authority for the reconstruction.

## 17. Conclusion and Paper-3 Handoff

Paper 2 began with a simple concern: cognitive-science terminology may overstate or obscure structural individuation. The solution was not to replace one vocabulary with another by stipulation, but to construct a sequence in which labels lose authority and surviving distinctions must be earned.

The sequence produced both negative and positive results.

At the whole-claim level, the frozen comparison failed completely: all 1,770 claim pairs were incomparable. Preserving that failure exposed an overly discriminating comparison surface.

At the bounded-subobject level, reusable structure reappeared: 206 unique Archetype/XLike objects, 99 cross-lane families, seven exact cross-lane equivalence components, and a large refinement preorder survived destructive controls.

At the system-role level, those structures compressed into a recurrent Grammar v0:

[
oxed{
{Pi,X,C,Q,P_{in},P_{out},K,T,ho/O}
}.
]

Reverse projection across all 60 claims produced 21 FULL, 22 PARTIAL, and 17 RESIDUAL cases. The residuals established no new top-level role gap. Instead they forced a separation among system structure, scientific claim language, context, formal realization, World, coupling, and experiment.

The resulting architecture is therefore not “The Cognition.” It is a bounded measurement basis and system grammar recovered from a reviewed corpus:

[
	ext{heterogeneous cognitive theories}
ightarrow
	ext{concept-neutral decomposition}
ightarrow
	ext{bounded reusable structure}
ightarrow
	ext{shared system grammar}.
]

The next test is scale and dynamics, not further post hoc compression of the same 60 claims. Paper 3 receives the frozen Paper 2 contracts and asks whether the structural coordinate system survives a much larger corpus, whether scalable extraction can reproduce the reference decisions, and how retained reusable structure behaves across time, learning, skill, habit, belief, and memory.

The methodological commitment remains unchanged:

> Construct names may guide retrieval and interpretation, but structural distinctions must survive without depending on the authority of the name itself.

**Working manuscript terminal:** PAPER2_WORKING_MANUSCRIPT_V0_INTEGRATED_FROM_FROZEN_RESULT_V1
