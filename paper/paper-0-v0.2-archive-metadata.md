# Paper 0 v0.2 — Zenodo / PhilSci-Archive Metadata Packet

**Purpose:** deposit-preparation metadata only. **Do not publish, reserve/mint a DOI, or submit to PhilSci-Archive without explicit author approval.**

## Canonical manuscript identity

- **Title:** Structural Cartography of Scientific Claims: An Integration Protocol for Adversarial Basis Construction, Blinded Structural Comparison, and Held-Out Validation
- **Version:** v0.2
- **Resource class:** methodological preprint / philosophy of science
- **Language:** English
- **Manuscript file:** `Paper0_v0.2_preprint.pdf`
- **Source file:** `paper-0-method-protocol-v0.2.md`
- **Repository:** `rinsakamo/relay-theory`
- **Repository revision vehicle:** PR #245
- **Novelty classification:** `PAPER0_INTEGRATION_NOVELTY_ONLY`

## Author fields that must be confirmed before any public deposit

- **Creator / publication name:** `[CONFIRM AUTHOR PUBLICATION NAME]`
- **Email:** `[CONFIRM PUBLIC DEPOSIT EMAIL]`
- **ORCID:** `[CONFIRM ORCID]`
- **Affiliation:** `[CONFIRM; use “Independent researcher” only if that is the author's intended public affiliation]`
- **License:** `[CONFIRM; do not inherit the repository's Apache-2.0 software license automatically for the manuscript]`

## Abstract

Scientific literatures often reuse the same construct label for operationally different claims and use different labels for claims that may preserve similar dependency, temporal, intervention, or criterion structure. Existing methods already address many parts of this problem: Carnapian explication sharpens concepts; counterexample-guided abstraction refinement iterates between abstraction and counterexample; multiverse analysis and preregistration expose or constrain analyst degrees of freedom; structure-mapping and ontology matching compare relational structure across heterogeneous descriptions; systematic review practices preserve source provenance; and formal methods provide mature notions of refinement and forgetting. This paper does not claim novelty for those components.

The contribution proposed here is an integration protocol for claim-level comparison under unstable terminology. The protocol couples five constraints in a fixed order: (1) adversarial construction of a bounded working basis by deletion, reconstruction, counterexample, and anti-trivialization tests; (2) pre-outcome freezing of the representational and comparison contract; (3) source-grounded decomposition and mapping that are blinded to answer-bearing construct labels and authority metadata while retaining the semantic content needed to interpret the source claim; (4) comparison through explicit equivalence, refinement, incomparability, and residual semantics under bounded expressivity; and (5) held-out checks of mapping coverage, reproducibility, label leakage, discrimination, and bespoke-encoding pressure. The method treats residuals and abstentions as informative boundaries rather than as failures to be hidden.

The paper's novelty claim is intentionally narrow. It does not assert a uniquely correct ontology, semantics-free interpretation, demonstrated cross-domain validity, superiority to existing methods, or historical firstness. The defended claim is that the coupled end-to-end protocol provides a falsifiable comparison contract for testing whether scientific claims can be compared structurally without allowing inherited labels or post-outcome analyst freedom to determine the result. A synthetic worked example illustrates the protocol without importing empirical outcomes from downstream applications.

## Suggested keywords

- philosophy of science
- scientific methodology
- theory comparison
- conceptual cartography
- structural comparison
- scientific constructs
- structural equivalence
- reproducibility
- preregistration
- ontology matching

## Zenodo draft metadata

- **Resource type:** Publication -> Preprint
- **Title:** Structural Cartography of Scientific Claims: An Integration Protocol for Adversarial Basis Construction, Blinded Structural Comparison, and Held-Out Validation
- **Creators:** `[CONFIRM CREATOR RECORD(S), ORCID, AFFILIATION]`
- **Description / Abstract:** use the abstract above verbatim
- **Publication date:** `2026-09-27` is the defensible candidate if the public GitHub PR #245 is treated as the first public availability of v0.2; confirm before deposit
- **Language:** English
- **Version:** v0.2
- **Keywords / subjects:** use the suggested keywords above
- **License:** `[CONFIRM]`
- **Access right:** Public, unless the author explicitly chooses otherwise
- **Related identifier:** GitHub repository / PR #245 may be added as project/source provenance; select the relation in Zenodo only after checking the exact UI wording
- **DOI:** none currently. Do **not** click “Get a DOI now!” or publish until explicit approval. If a DOI is reserved before final PDF upload, regenerate the PDF only if the author wants the DOI printed inside the document.
- **Notes (optional):** “Version 0.2. Methodological integration proposal. No Paper 2 atlas outcome or Paper 3 large-scale validation result is reported in this preprint.”

### Zenodo sequencing note

Zenodo requires publication date, resource type, title, and creators among its basic metadata. A draft can be saved and previewed before publication. A DOI can be reserved in a draft, but the DOI is registered when the record is published. The intended project sequence remains: final v0.2 review -> Zenodo archival record / DOI -> PhilSci-Archive.

## PhilSci-Archive draft metadata

- **Item Type:** Preprint
- **Title:** Structural Cartography of Scientific Claims: An Integration Protocol for Adversarial Basis Construction, Blinded Structural Comparison, and Held-Out Validation
- **Creators:** `[CONFIRM AUTHOR PUBLICATION NAME, EMAIL, ORCID]`
- **Abstract:** use the abstract above verbatim
- **Keywords:** philosophy of science; scientific methodology; theory comparison; conceptual cartography; structural comparison; scientific constructs; structural equivalence; reproducibility; preregistration; ontology matching
- **Primary subject:** `General Issues > Structure of Theories`
- **Additional subjects:** add only if the author wants broader indexing; do not pad the taxonomy
- **Date:** 2026-09-27 as candidate v0.2 public-release date; confirm at deposit time
- **Text file:** `Paper0_v0.2_preprint.pdf`
- **Content/version field:** use `Submitted Version` if that option accurately describes the deposited preprint; otherwise use the archive's neutral/unspecified option rather than claiming an accepted version
- **License:** `[CONFIRM]`
- **DOI or Unique Handle:** `[INSERT ZENODO DOI AFTER ZENODO PUBLICATION]`
- **Official URL:** `[INSERT ZENODO RECORD URL AFTER PUBLICATION]` (repository URL may be added as secondary provenance if appropriate)
- **Additional Information (optional):** “Paper 0 v0.2. Integration-method contribution; component methods are explicitly treated as prior art. Downstream Paper 2/Paper 3 scientific outcomes are outside this manuscript.”

### PhilSci sequencing note

PhilSci-Archive records expose Item Type, creator identity (including email/ORCID where supplied), keywords, subject taxonomy, date, DOI/unique handle, and uploaded-text version information. `General Issues > Structure of Theories` is a well-established subject category and is also used by closely related conceptual-cartography / theory-structure deposits.

## Deposit-time checksum block

Populate/check these against the exact file actually uploaded:

- `paper-0-method-protocol-v0.2.md` SHA-256: `8646819e148b5199de7d64e9599ce27de0602d6f04179d975e6667f54a8fd5b0`
- `paper-0-v0.2-adjudication.md` SHA-256: `f6e6c9eea57d200d523e4dfb17fc1bda2537f1f3769f15c8ce96733ddf0ef0e3`
- `Paper0_v0.2_preprint.pdf` SHA-256: `5f1e5260d566d92421d54a1b81801695a6412ba2290bcfb537f62ddc331d3841`

If the PDF is regenerated after DOI reservation, license selection, author-name correction, or metadata insertion, recompute all affected checksums before publication.