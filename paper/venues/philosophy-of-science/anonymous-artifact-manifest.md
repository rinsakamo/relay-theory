# Anonymous formal artifact manifest

> Blind-review companion for the Paper 1 submission package.  
> This file intentionally contains no author name, project name, repository URL, issue/PR number, or public theorem identifier.

## Purpose

The manuscript uses Lean as a dependency audit rather than as a source of deep mathematical novelty. During blind review, machine-checked results are referred to by neutral labels `R1`--`R23`.

## Result labels

The executable anonymous supplement contains the exact theorem names below.

| Label | Anonymous theorem | Mechanized claim |
| --- | --- | --- |
| R1 | `encodedA_encodedB_sameGrounding` | Two encodings can have the same target assignment. |
| R2 | `encodingProbe_separates_sameGrounding` | A representation-sensitive discriminator can still separate those encodings. |
| R3 | `sameGrounding_sameGroundedObservation` | Equal target assignment preserves every target-sensitive observation. |
| R4 | `sameGrounding_sameGroundedProfile` | Equal target assignment preserves the full target-sensitive response profile. |
| R5 | `coarse_indistinguishable` | A restricted selected test family can leave a pair unresolved. |
| R6 | `fine_distinguishable` | A richer selected test family can separate the same pair. |
| R7 | `fine_indist_implies_coarse_indist` | Test-family inclusion induces the expected monotonicity. |
| R8 | `identityProbe_groundedDifference` | The positive-control target-sensitive observation difference is established. |
| R9 | `groundedOutcomeDifference_impliesGroundDifference` | A target-sensitive outcome difference entails a target-assignment difference. |
| R10 | `derivedGroundDifference` | The positive-control target difference is derived from the response difference. |
| R11 | `decorativeInterfaceTag_irrelevant` | Decorative interface metadata is semantically inert. |
| R12 | `tokenizedGroundedIndist_iff_base` | Adding identity-like token metadata preserves the base classification. |
| R13 | `identityToken_variation_preserves_groundedClassification` | Arbitrary reassignment of semantically inert tokens preserves classification. |
| R14 | `differentIdentityTokens_sameGroundedClassification` | Different token values do not create separation for same-target encodings. |
| R15 | `identityTokenCannotMask_groundedDifference` | Equal token values cannot mask a grounded difference already exposed by tests. |
| R16 | `groundFeature_hasGroundingBridge` | A positive-control target-derived feature satisfies target factorization. |
| R17 | `bridgedFeature_sameGrounding_sameValue` | A target-factorized feature is constant on equal-target fibers. |
| R18 | `bridgedFeatureDifference_impliesGroundDifference` | A target-factorized feature difference entails a target-assignment difference. |
| R19 | `encodingProbe_hasNoGroundingBridge` | A representation-sensitive discriminator that splits a fiber cannot factor through the target. |
| R20 | `observeGrounded_hasObservationFactorization` | The target-linked observation surface satisfies test-specific factorization. |
| R21 | `factorizedObservedDifference_impliesGroundDifference` | Test-specific observation factorization licenses target separation. |
| R22 | `familyFactorizedObservedDifference_impliesGroundDifference` | Family-level factorization licenses witnessed separation. |
| R23 | `fiberInvariant_differenceSound_descends_equivalent` | Fiber invariance, universal difference soundness, and quotient descent are equivalent relative to a fixed target assignment. |

## Formal scope

The mechanization assumes:

- an explicit representation type;
- an explicit target domain;
- a representation-to-target map;
- declared exact test semantics;
- declared test accessibility;
- a token carrier whose internal structure is not inspected by target-sensitive semantics;
- a generic structural target-factorization object for arbitrary feature-value carriers;
- a generic target-induced quotient, fiber-invariance condition, and universal difference-soundness condition over arbitrary representation, target, and feature-value types;
- a test-specific observation-factorization object connecting representation-level observed outcomes to target-level responses.
- a family-level admissibility condition requiring that factorization for every selected test used by the inference.

It does **not** derive target ontology, establish the representation-to-target assignment, manufacture epistemic warrant for a declared factorization, derive metaphysical numerical identity, select a uniquely correct test regime, model noisy/statistical inference, or infer interventional equivalence from observational equivalence.

## Validation boundary

The underlying formal development is checked without `sorry`, `admit`, `native_decide`, or project-local axioms. Repository CI builds both the non-blind formal core and the standalone anonymous supplement. It also rejects repository/author-identity leakage from the anonymous supplement before upload.

For anonymous peer review, the public development and public theorem identifiers are intentionally not linked from this manifest.

## Submission-package note

Attach the directory `anonymous-lean-supplement` as a separate supplementary file for review. It contains `Paper1Audit.lean`, `lean-toolchain`, `lakefile.lean`, `README.md`, and `RESULT_MAP.md`. The package is independently buildable with `lake build` and contains no public-repository metadata.
