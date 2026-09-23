# Anonymous formal artifact manifest

> Blind-review companion for the Paper 1 submission package.  
> This file intentionally contains no author name, project name, repository URL, issue/PR number, or public theorem identifier.

## Purpose

The manuscript uses Lean as a dependency audit rather than as a source of deep mathematical novelty. During blind review, machine-checked results are referred to by neutral labels `R1`--`R22`.

## Result labels

| Label | Mechanized claim |
| --- | --- |
| R1 | A representation-sensitive discriminator can separate two representations that have the same target reference. |
| R2 | Equal target reference preserves each target-sensitive observation. |
| R3 | Equal target reference preserves the complete target-sensitive observation profile. |
| R4 | Same-reference encodings remain indistinguishable under the admitted target-sensitive regime. |
| R5 | If one admitted test family is included in another, indistinguishability under the richer family implies indistinguishability under the poorer family. |
| R6 | A concrete pair is indistinguishable under the restricted test family. |
| R7 | The same pair is distinguishable under the richer test family. |
| R8 | A difference in a target-sensitive outcome entails a difference in the corresponding target values under the declared semantics. |
| R9 | The concrete positive-control target-sensitive response difference is established. |
| R10 | The corresponding positive-control target difference is derived from the response difference. |
| R11 | For any token carrier type, adding a semantically inert identity-like token leaves the base target-sensitive classification unchanged. |
| R12 | For any token carrier type, arbitrary reassignment of semantically inert identity-like tokens preserves the tested classification. |
| R13 | Different identity-like token values do not separate two same-reference encodings. |
| R14 | Assigning the same identity-like token cannot hide a target-sensitive difference already exposed by the admitted tests. |
| R15 | Decorative access metadata that does not change the admitted test profile does not change the tested classification. |
| R16 | For a feature with an explicit target factorization, equal target assignment forces equal feature values. |
| R17 | A difference in a target-factorized representation-level feature entails a difference in target assignment. |
| R18 | The deliberately representation-sensitive encoding discriminator cannot have a target factorization because it separates two representations assigned to the same target. |
| R19 | A positive-control feature defined directly from the target assignment satisfies target factorization. |
| R20 | The target-linked representation-level observation function satisfies test-specific observation factorization. |
| R21 | Under observation factorization, a difference in an observed test outcome entails a difference in target assignment. |
| R22 | If every test in a selected family satisfies the declared observation-to-target factorization, separation by that family entails different target assignments. |

## Formal scope

The mechanization assumes:

- an explicit representation type;
- an explicit target domain;
- a representation-to-target map;
- declared exact test semantics;
- declared test accessibility;
- a token carrier whose internal structure is not inspected by target-sensitive semantics;
- a generic structural target-factorization object for arbitrary feature-value carriers;
- a test-specific observation-factorization object connecting representation-level observed outcomes to target-level responses.
- a family-level admissibility condition requiring that factorization for every selected test used by the inference.

It does **not** derive target ontology, establish the representation-to-target assignment, manufacture epistemic warrant for a declared factorization, derive metaphysical numerical identity, select a uniquely correct test regime, model noisy/statistical inference, or infer interventional equivalence from observational equivalence.

## Validation boundary

The underlying formal development is checked without `sorry`, `admit`, `native_decide`, or project-local axioms. The repository validation also builds the Lean project, performs an independent kernel check, and audits theorem axioms against a pinned allow-list.

For anonymous peer review, the public development and public theorem identifiers are intentionally not linked from this manifest.

## Submission-package note

If the journal or editor requests executable anonymous source during review, export a scrubbed Lean source package whose public identifiers and repository metadata have been removed, and validate that exported package independently before submission. Do not point reviewers to the public repository during blind review.
