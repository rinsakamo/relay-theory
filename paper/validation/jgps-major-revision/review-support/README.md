# JGPS review-support checkpoint v1

Authority: #365

This checkpoint supports two fresh-review requests without changing frozen Paper-2 results.

## Independent re-adjudication packet

- population: 60 historical claims
- sample: 18 claims (30%)
- fixed quota policy: 5 historical FULL, 5 historical PARTIAL, 8 historical RESIDUAL
- residual cases are deliberately oversampled
- packet IDs are anonymized as `IR01`–`IR18`
- original Grammar verdicts and residual classes are not included in the adjudicator packet
- all adjudicator response fields are null at generation time
- selection is deterministic from fixed seed `JGPS365-INDEPENDENT-READJUDICATION-V1`

The separate selection receipt exists only for later scoring. It must not be supplied to the independent adjudicator before the response is locked. Because the repository already contains the historical results, procedural independence also requires the adjudicator not to inspect those files.

Packet SHA-256:

`733bc47819f5f634c2441ca5251d7793f41c5522f02e7047dc55c0efb9853beb`

## Supplementary source/claim table

The generator produces exactly 60 rows from the frozen source manifest and reviewed ClaimIR, with:

- slot / stratum
- DOI or stable identity
- canonical locator
- title / year
- claim ID
- source access class
- claim type / modality
- source-grounded claim summary
- source-span count

The table is descriptive and intentionally omits Grammar-v0 verdicts.

CSV SHA-256:

`fbcb52e82a9dfb984d9858d599c7653d72358e8a27eedeab0971163a9bd53213`

Markdown SHA-256:

`92aa858660a1ce809c6a245f6f58142323dc0fcd0233440e9fd02bd64f7a0e1a`

## Boundary

This checkpoint does not satisfy the PVS-16 human author-review gate and does not authorize prospective Grammar mapping.

Terminal:

`PAPER2_JGPS_REVIEW_SUPPORT_V1_FROZEN`

## Worked-example candidates

Deterministic selection from frozen artifacts produced:

- different labels / shared exact structure: `ATT02` × `BLF04`, exact Archetype `A-3b814de4da04`;
- same label / different structure: `CNC01` × `LRN06`, sharing construct labels `categorization` and `similarity`, with zero shared bounded Archetypes;
- residual case: `MEM06.C1`, primary `SOURCE_CONTEXT_PARAMETER`, secondary `RELATION_LANGUAGE_GAP` + `FORMAL_CARRIER_GAP`, `ROLE_GAP=false`.

Worked-example selection SHA-256:

`a37f77d786cc7231f3a7814973e269bed08f3659ff67813dc58ff3fe96267af9`

These selections are candidates for exposition only; they do not create new scientific adjudications.

Worked-example evidence JSON SHA-256:

`817fda3c08b032f5b21257862e2f9639a393beccefc6a98fa78e348ddbe99445`

Worked-example evidence Markdown SHA-256:

`eec75ef0eb7da1f391b36ae93d1c307f02cb6691422c59529ba114a9a6db38f8`
