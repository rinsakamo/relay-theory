# M11 hostile review — discriminative baselines and philosophical reframing

Status: FINAL_INTERNAL_HOSTILE_REVIEW  
Authority: Issue #399  
M10 parent: `095c6f41bc7ca6a08bf423137bbf3b8f7bc068e5`

## Review question

Does the revised manuscript now establish a non-trivial philosophical proposition, while keeping the scientific meaning of the 40/40 A0 prospective result, representation sensitivity, and single-adjudicator boundary explicit?

## 1. Philosophical target

**Disposition: substantially resolved.**

The manuscript no longer treats "labels can mislead" as the principal conclusion. Its explicit thesis is:

> Construct-based individuation is evidentially incomplete unless the comparison representation, preservation criterion, and granularity are independently stated; neither terminology nor successful reconstruction licenses representation-independent identity.

The analyzed objects are now explicitly scientific claims about capacities. The inferential bridge is stated as claim-level structural comparison -> evidential constraint on capacity comparison -> capacity individuation. The paper therefore does not pretend to individuate capacities directly.

The opponent is an inference form rather than a straw-man attribution to one cited author: terminology or successful reconstruction within one representation is insufficient by itself for representation-independent capacity identity.

## 2. Prospective 40/40 A0 discriminative validity

**Disposition: reviewer concern confirmed, then correctly delimited.**

A literal encoding-permissive weak-basis baseline was added after hostile self-review. Under the original A-state semantics, source-defined mechanisms remain admissible and representation-only recoding is not a reconstruction-added mechanism.

Result:

- full basis: 40/40 A0;
- dynamic backbone: 40/40 A0;
- POMDP-like view: 40/40 A0;
- minus Pi: 40/40 A0;
- minus C: 40/40 A0;
- minus P: 40/40 A0;
- minus T: 40/40 A0.

Therefore the prospective A0 result **does not discriminate the exact role inventory**. This is the key negative result required by the reviewer objection.

A separate direct-preservation closure control yields the complementary result:

- full basis: 40 A0 / 0 A1;
- each weaker arm: 0 A0 / 40 A1.

This does not rescue grammar selection through composition. It establishes only that the working basis keeps declared distinctions first-class while weaker views require stateless re-exposure under the stricter preservation objective.

The revised manuscript now assigns the two results correctly:

- prospective A0 -> no reconstruction-added coordinator was required;
- direct-preservation comparator -> reason to prefer the working basis for the declared distinction-preservation purpose.

This separation is philosophically stronger than treating 40/40 A0 as grammar validation.

Residual limitation: the encoding-permissive mapping is constructive and deterministic on already adjudicated structures rather than a fresh independent source adjudication. This is appropriate to the question but should not be described as an independent replication.

## 3. Representation sensitivity

**Disposition: substantially improved.**

TAIF is retained only as a non-uniqueness control. Because it is invertible, preservation of higher-order results is not presented as strong robustness evidence.

The new CPCG rival is deliberately lossy and non-injective:

- 206 original bounded objects -> 143 CPCG signatures;
- 37 collision groups;
- 63/99 original cross-stratum families collide;
- 62 cross-stratum CPCG signatures remain;
- 58/60 claims retain support from at least one cross-stratum CPCG signature;
- ATT01-BLF01 cross-label reuse survives.

This shows that the exact object/family inventory is representation-sensitive while a substantial higher-order reuse pattern survives one genuinely lossy alternative.

Residual limitation: only one non-invertible rival has been tested. No representation-neutral robustness claim is licensed.

## 4. Label symmetry

**Disposition: resolved.**

The manuscript now has both directions:

- different labels / shared bounded structure: ATT01 x BLF01;
- same label / different bounded structure: MEM04 x CNC05, shared historical label "semantic memory".

MEM04 and CNC05 have zero overlap in their frozen bounded-archetype sets and zero overlap after CPCG projection. This supplies a concrete counterexample to inferring preserved structural identity from label identity.

The MEM04-CNC05 pair was selected after candidate exploration and is correctly marked as an expository witness, not a predeclared prevalence test.

## 5. Claim/capacity level

**Disposition: resolved.**

Title, abstract, introduction, discussion, and conclusion now identify the direct target as cognitive-capacity **claims** and the philosophical contribution as a pre-individuation evidential constraint.

The manuscript no longer relies on "construct-label-neutral"; it uses "construct-label-suppressed at the comparison stage" and explicitly denies theory- or representation-neutrality.

## 6. JGPS-style argumentative foreground

**Disposition: materially improved.**

The main text now foregrounds:

1. philosophical problem;
2. evidential-burden thesis;
3. claim/capacity bridge;
4. failure/recovery results;
5. representation baselines;
6. philosophical consequences.

Exact commit chronology, stage ancestry, detailed comparator contracts, CI role, and repository provenance are moved to a separate Supplementary Methods document. The main text retains enough method to evaluate the inference without reading the repository as an argument.

"Paper 2" and reviewer-facing milestone names are removed from the manuscript.

## 7. Single-adjudicator reliability

**Disposition: unresolved by design and correctly exposed.**

Independent human re-adjudication was NOT PERFORMED.

The manuscript retains the exact boundary:

> Procedural auditability is established; inter-rater reliability remains unmeasured.

LLM assistance, deterministic CI, formal verification, synthetic A-state reachability, real-source perturbation controls, direct-preservation controls, CPCG sensitivity, and encoding-permissive baselines are not substitutes for an independent human coder.

This remains the largest external-validation weakness.

## 8. Remaining inferential boundaries

The revised paper still must not claim:

- population or prevalence estimates;
- global genealogical independence;
- a universal or unique cognitive ontology;
- representation-neutral identity;
- absolute minimality;
- generic non-encodability of dynamical or POMDP formalisms;
- that 40/40 A0 validates the exact grammar;
- that CPCG exhausts plausible rival representations;
- independent extraction or inter-rater reliability.

## Final hostile-review disposition

**M11 target: SATISFIED WITH EXPLICIT BOUNDED LIMITATIONS.**

The largest reviewer objection changed the paper rather than merely being rebutted: encoding-permissive weak bases also achieve 40/40 A0, so prospective composition is no longer used as evidence for the exact role inventory. That negative result strengthens the central philosophical thesis that successful reconstruction is representation-relative and cannot by itself license representation-independent individuation.

The principal remaining vulnerability is empirical-adjudicative rather than conceptual: there is still no independent human second coding of a stratified subset. A broader set of genuinely lossy rivals would also strengthen the sensitivity case. Neither limitation should be obscured by further internal automation.
