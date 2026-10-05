# Response to Reviewer — Major Revision

We thank the reviewer for identifying a genuine ambiguity in the earlier presentation: the prospective 40-paper result was reported more strongly than the manuscript had demonstrated the discriminability and auditability of the A0/A1/A2 procedure. We have revised the paper accordingly. The central empirical result remains unchanged: in the exact frozen MAIN40, all 40 papers were adjudicated A0, with no reconstruction-added stateless adapter and no reconstruction-added persistent/stateful coordinator. The revision changes the evidential framing, exposes the paper-level decision trail, and adds a separate post-hoc falsifiability calibration.

## 1. A0/A1/A2 discriminability and falsifiability

We now define A0/A1/A2 as least faithful-lift classes in a nested reconstruction hierarchy: direct reconstruction, reconstruction with added stateless mediation, and reconstruction with added persistent/stateful mediation. This makes the distinction depend on the least reconstruction-added structure required for source fidelity, not on source-model complexity.

We also added a matched six-case calibration with Dynamic and POMDP-like families. Each family contains an A0, A1, and A2 case. The A1 case has a direct typed-port mismatch repaired by a stateless adapter. The A2 case requires history dependence: no current-input-only stateless map can satisfy the frozen contract, while a one-bit persistent bridge can. These results are formalized and kernel-checked in Lean.

This calibration is explicitly post hoc. It does not re-adjudicate MAIN40 and is not presented as part of the prospective freeze.

## 2. Paper-level evidence for all 40 MAIN cases

We added a complete 40-paper audit table derived from the frozen M7 matrix. Each row exposes the exact paper/DOI, source-defined coordination/state summary, reconstruction-added stateless/stateful counts, unresolved evidence, genealogy annotation, lane PR and exact HEAD, the paper-level architectural-outcome artifact, and the sibling source-first source-loci ledger.

The purpose is not to create a second adjudication. It is to make the original adjudication externally inspectable.

## 3. Prospective chronology

We added a repository freeze chronology with exact commits and timestamps. It distinguishes the adopted source-closed method reference, genealogy criterion freeze, W9 closure, explicit MAIN kickoff, six lane outcomes, M7 integration, M8 manuscript integration, and the later M9 review-response work.

The chronology also preserves historical states rather than retroactively relabeling them. The 2026-10-04 v5 roster remains historically a working/outcome-blind artifact; the later explicit MAIN GO freezes that exact blob as the no-substitution MAIN denominator.

## 4. Independent human re-adjudication

We agree with the reviewer that independent human re-adjudication was not established.

Independent human re-adjudication was not performed. It was not performed in the present single-author study. We now state this directly and do not treat LLM-assisted checking, separate model sessions, deterministic CI, Lean formal verification, synthetic calibration, genealogy analysis, or source-identity separation as substitutes for an independent human coder.

Accordingly, the manuscript now describes the result as establishing **procedural auditability rather than inter-rater reliability**. We provide the complete audit surface so that an external researcher can perform an independent re-adjudication without relying on the aggregate labels reported here.

## 5. Genealogy and independence

We have narrowed the language throughout. Exact DOI non-overlap is described only as source-identity separation. The 40 papers are not treated as 40 independent replications. W9 genealogy uncertainty remains explicit, and we make no binomial, effective-N, or population-frequency inference from the 40/40 result.

The prospective study is now described as a **single-adjudicator, source-identity-separated prospective compatibility test under a frozen reconstruction contract**.

## 6. Grammar v0, Dynamic models, and POMDP-like models

We clarified that the reason for not adopting the POMDP-like view as the comparison basis is not lack of generic encoding power. The issue is direct distinction preservation.

The pre-existing comparators show that the strict Dynamic view and the POMDP-like view forget distinctions that the source corpus had frozen as first-class. M9-A additionally formalizes the transition-backbone forgetting chain from Grammar v0 through the POMDP-like view to the Dynamic view.

We therefore do not claim that POMDPs cannot encode the tested cognitive models. We claim only that the tested POMDP-like projection is too forgetful for the equivalence relation examined in this paper.

## 7. Circularity and conceptual leakage

We have made the chronology and inferential layers explicit:

1. the original 60-claim recovery and comparator analysis;
2. the pre-outcome MAIN freeze;
3. the 40-paper compatibility test;
4. the later post-hoc M9 falsifiability calibration.

No MAIN40 paper is re-adjudicated in response to the M9 calibration. This controls formal outcome leakage. We agree that a single-adjudicator design cannot eliminate every form of conceptual leakage, and we retain that as a limitation rather than claiming otherwise.

## 8. Philosophical contribution

The Discussion now states three implications explicitly.

First, construct individuation is not inherited from vocabulary: labels are not treated as evidential authority for structural identity. Second, the 1770/1770 whole-claim incomparability result is interpreted as an informative negative compression result at that granularity, not as evidence of global incommensurability or meaningless constructs. Third, successful Grammar-v0 reconstruction is representation-relative: it supports the utility of the frozen comparison basis under the declared preservation contract, not metaphysical realism, a universal ontology, or absolute minimality.

## 9. Claim strength and terminology

We replaced stronger validation language with:

> uniform descriptive compatibility with direct composition under the frozen source-faithful reconstruction contract

and consistently distinguish prospective compatibility from independent validation. The post-hoc matched calibration is reported separately.

## 10. Manuscript and artifact authority

We removed the statement that the manuscript is “non-authoritative.” The revised text states that the manuscript is the object submitted for scholarly review, while the frozen machine-readable artifacts and formal modules provide auditable provenance for its empirical and formal claims.

## Remaining limitations

The revision does not claim to eliminate all limitations. In particular:

- independent human re-adjudication was not performed;
- inter-rater reliability is unmeasured;
- global genealogical independence is not certified;
- the MAIN40 roster is purposive rather than a probability sample;
- POMDP non-encodability is not claimed;
- Grammar v0 is not claimed to be a universal or absolutely minimal cognitive ontology;
- the 40/40 result remains corpus-relative.

We believe these revisions answer the reviewer's central concern by separating what has now been demonstrated—formal discriminability, paper-level auditability, chronology, and bounded representation-relative comparison—from what remains explicitly unestablished.
