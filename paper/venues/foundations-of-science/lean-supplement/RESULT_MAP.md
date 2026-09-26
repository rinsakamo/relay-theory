# Online Resource 1 — R1–R23 result map

Article: When May a Formal Difference Enter an Individuation Inference? Target Factorization, Restricted Tests, and Cross-Domain Audits
Journal: Foundations of Science
Author: Rintaro Sakamoto, MPH
Affiliation: Independent Scholar, Kitakyushu, Japan
ORCID: 0009-0002-0443-2508
Corresponding author email: rin.sakamoto.research@gmail.com

| Label | Theorem in `Paper1Audit.lean` | Role |
|---|---|---|
| R1 | `encodedA_encodedB_sameGrounding` | Same-target positive control for two encodings |
| R2 | `encodingProbe_separates_sameGrounding` | Presentation-sensitive negative control |
| R3 | `sameGrounding_sameGroundedObservation` | Same target implies same grounded observation |
| R4 | `sameGrounding_sameGroundedProfile` | Same target implies same grounded response profile |
| R5 | `coarse_indistinguishable` | Restricted family leaves a pair unresolved |
| R6 | `fine_distinguishable` | Richer family separates that pair |
| R7 | `fine_indist_implies_coarse_indist` | Test-family inclusion monotonicity |
| R8 | `identityProbe_groundedDifference` | Positive-control observed difference |
| R9 | `groundedOutcomeDifference_impliesGroundDifference` | Test outcome difference transfers to target difference |
| R10 | `derivedGroundDifference` | Positive-control target difference is derived |
| R11 | `decorativeInterfaceTag_irrelevant` | Decorative interface metadata is inert |
| R12 | `tokenizedGroundedIndist_iff_base` | Inert token metadata preserves classification |
| R13 | `identityToken_variation_preserves_groundedClassification` | Arbitrary inert-token reassignment is harmless |
| R14 | `differentIdentityTokens_sameGroundedClassification` | Different tokens do not create target separation |
| R15 | `identityTokenCannotMask_groundedDifference` | Same token cannot mask a grounded difference |
| R16 | `groundFeature_hasGroundingBridge` | Positive-control feature factorization exists |
| R17 | `bridgedFeature_sameGrounding_sameValue` | Factorized feature is fiber-invariant |
| R18 | `bridgedFeatureDifference_impliesGroundDifference` | Factorized feature difference entails target difference |
| R19 | `encodingProbe_hasNoGroundingBridge` | Presentation-sensitive discriminator fails factorization |
| R20 | `observeGrounded_hasObservationFactorization` | Positive-control observation bridge exists |
| R21 | `factorizedObservedDifference_impliesGroundDifference` | Test-specific factorization licenses separation |
| R22 | `familyFactorizedObservedDifference_impliesGroundDifference` | Family-level admissibility licenses witnessed separation |
| R23 | `fiberInvariant_differenceSound_descends_equivalent` | Fiber invariance ⇔ universal difference soundness ⇔ quotient descent |

The theorem names are descriptive implementation names inside this anonymous
artifact. The manuscript uses only the neutral R-labels.
