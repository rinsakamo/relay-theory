# Response to Reviewer — Major Revision

We thank the reviewer for identifying a genuine ambiguity in the earlier presentation: the prospective 40-paper result was reported more strongly than the manuscript had demonstrated the discriminability and auditability of the A0/A1/A2 procedure. We have revised the paper accordingly. The central empirical result remains unchanged: in the pre-specified 40-paper prospective corpus, all 40 papers were adjudicated A0, with no reconstruction-added stateless adapter and no reconstruction-added persistent/stateful coordinator. The revision changes the evidential framing, exposes the paper-level decision trail, and adds a separate post hoc discriminability stress test.

## 1. A0/A1/A2 discriminability

We now define A0/A1/A2 by the minimal faithful reconstruction level in a nested reconstruction hierarchy: direct reconstruction, reconstruction with added stateless mediation, and reconstruction with added persistent/stateful mediation. This makes the distinction depend on the least reconstruction-added structure required for fidelity to the source model, not on source-model complexity.

We also added a matched six-case calibration with Dynamic and POMDP-like families. Each family contains an A0, A1, and A2 case. The A1 case has a direct typed-port mismatch repaired by a stateless adapter. The A2 case requires history dependence: no current-input-only stateless map can satisfy the pre-specified contract, while a one-bit persistent bridge can. These results are formalized and kernel-checked in Lean.

This calibration is explicitly post hoc. It does not re-adjudicate the prospective 40-paper corpus and is not presented as part of the prospective chronology.

## 2. Paper-level evidence for all 40 prospective cases

We added a complete 40-paper audit table derived from the integrated prospective analysis. Each row exposes the exact paper/DOI, summary of coordination or state specified by the source model, reconstruction-added stateless/stateful counts, unresolved evidence, genealogy annotation, exact analysis-stream version, paper-level outcome artifact, and source-first evidence ledger.

The purpose is not to create a second adjudication. It is to make the original adjudication externally inspectable.

## 3. Prospective chronology

We added a repository pre-specification chronology with exact commits and timestamps. It distinguishes the adopted source-closed method reference, genealogy criterion, bounded genealogy audit, explicit prospective-study authorization, six analysis-stream outcomes, integration, manuscript preparation, and the later review-response work.

The chronology preserves historical states rather than retroactively relabeling them. An earlier roster remains historically designated as a working/outcome-blind artifact; later prospective authorization fixed that exact roster as the no-substitution denominator. Exact commit identifiers and timestamps are provided in the supplementary provenance ledger rather than repeated in the manuscript.

## 4. Independent human re-adjudication

We agree with the reviewer that independent human re-adjudication was not established.

Independent human re-adjudication was not performed in the present single-author study. We now state this directly and do not treat LLM-assisted checking, separate model sessions, deterministic CI, Lean formal verification, synthetic calibration, genealogy analysis, or source-identity separation as substitutes for an independent human coder.

Accordingly, the manuscript now describes the result as establishing **procedural auditability rather than inter-rater reliability**. We provide the complete audit surface so that an external researcher can perform an independent re-adjudication without relying on the aggregate labels reported here.

## 5. Genealogy and independence

We have narrowed the language throughout. Exact DOI non-overlap is described only as source-identity separation. The 40 papers are not treated as 40 independent replications. Genealogy uncertainty remains explicit, and we make no binomial, effective-N, or population-frequency inference from the 40/40 result.

The prospective study is now described as a **single-adjudicator, source-identity-separated prospective compatibility test under a pre-specified reconstruction contract**.

## 6. Structural role grammar, Dynamic models, and POMDP-like models

We clarified that the reason for not adopting the POMDP-like view as the comparison basis is not lack of generic encoding power. The issue is direct distinction preservation.

The pre-existing comparators show that the strict Dynamic view and the POMDP-like view forget distinctions that the source corpus had held fixed as first-class. The new post hoc stress test additionally formalizes the transition-backbone forgetting chain from the structural role grammar through the POMDP-like view to the Dynamic view.

We therefore do not claim that POMDPs cannot encode the tested cognitive models. We claim only that the tested POMDP-like projection is too forgetful for the equivalence relation examined in this paper.

## 7. Circularity and conceptual leakage

We have made the chronology and inferential layers explicit:

1. the original 60-claim recovery and comparator analysis;
2. the pre-outcome prospective specification;
3. the 40-paper compatibility test;
4. the later post hoc discriminability stress test.

No prospective paper is re-adjudicated in response to the later calibration. This controls formal outcome leakage. We agree that a single-adjudicator design cannot eliminate every form of conceptual leakage, and we retain that as a limitation rather than claiming otherwise.

## 8. Philosophical contribution

The Discussion now states three implications explicitly.

First, construct individuation is not inherited from vocabulary: labels are not treated as evidential authority for structural identity. Second, the 1770/1770 whole-claim incomparability result is interpreted as an informative negative compression result at that granularity, not as evidence of global incommensurability or meaningless constructs. Third, successful reconstruction with the structural role grammar is representation-relative: it supports the utility of the pre-specified comparison basis under the declared preservation contract, not metaphysical realism, a universal ontology, or absolute minimality.

## 9. Claim strength and terminology

We replaced stronger validation language with:

> uniform descriptive compatibility with direct composition under a pre-specified reconstruction contract faithful to each source model

and consistently distinguish prospective compatibility from independent validation. The post hoc matched calibration is reported separately.

We also removed repository-internal shorthand from the manuscript wherever it was not needed for scientific meaning. Terms such as internal milestone names, CI terminal strings, and implementation-specific type labels are retained only in the supplementary provenance materials.

## 10. Manuscript and artifact authority

We removed the statement that the manuscript is “non-authoritative.” The revised text states that the manuscript is the object submitted for scholarly review, while versioned machine-readable artifacts and formal modules provide auditable provenance for its empirical and formal claims.

## Remaining limitations

The revision does not claim to eliminate all limitations. In particular:

- independent human re-adjudication was not performed;
- inter-rater reliability is unmeasured;
- global genealogical independence is not certified;
- the 40-paper roster is purposive rather than a probability sample;
- POMDP non-encodability is not claimed;
- the structural role grammar is not claimed to be a universal or absolutely minimal cognitive ontology;
- the 40/40 result remains corpus-relative.

We believe these revisions answer the reviewer's central concern by separating what has now been demonstrated—formal discriminability, paper-level auditability, chronology, and bounded representation-relative comparison—from what remains explicitly unestablished.
