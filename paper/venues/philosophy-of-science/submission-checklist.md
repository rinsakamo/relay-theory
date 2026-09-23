# Philosophy of Science — Paper 1 submission checklist

> Working checklist. No submission has occurred.

## Manuscript identity

- [x] Submission type planned as **Article**.
- [x] Title fixed for the current review copy.
- [x] Author field omitted from the blind manuscript.
- [x] No public repository URL, project name, issue/PR number, or author identifier in the review manuscript.
- [x] Public Lean theorem identifiers replaced by neutral labels `R1`--`R23`.
- [x] Anonymous artifact manifest prepared.
- [ ] If executable Lean source is supplied during review, export a scrubbed anonymous package and validate it independently before upload.

## Journal format

- [x] Abstract <=100 words (current review abstract: 99 words).
- [x] Article length comfortably below the current Article word limit.
- [x] 12pt review text.
- [x] Double-spaced body.
- [x] Ragged-right review copy.
- [x] Initial anonymous source follows the explicit initial-submission sequence: title → abstract → main text, with no forced page break between abstract and Introduction.
- [x] Submission-facing section/subsection titles use headline capitalization.
- [x] Venue-source tables use full-size 12pt text (no `\\small` overrides).
- [x] Reference page ranges are normalized to Chicago-style abbreviated inclusive numbers where applicable.
- [x] Chicago author-date bibliography style selected.
- [x] Anonymous review manuscript ends with **References**; acknowledgements are omitted for blind review.
- [x] Accepted-manuscript back-matter order is fixed as **References → Acknowledgements → Declarations → Funding Statement**; factual Declarations/Funding text remains author-supplied.
- [x] Bibliography source contains 22 references; all 22 include DOI fields and full `https://doi.org/...` URLs.
- [x] Rebuild the **exact current anonymized review source** after DOI completion: Paper 1 Review CI run #11 / exact head `1ee8022a7fc740ec8e11c27b7e59aa489373ddbb` generated an 18-page PDF and passed all blind-source, bibliography, and final LaTeX audits.
- [x] Manually visually inspect all 18 pages of the DOI-complete exact CI artifact PDF: run #11 artifact ID `10702765379`, rendered at 140 dpi on 2026-09-23; no clipping, overlap, broken glyphs, missing sections, or reference-layout defects found. This validation is historical after the later cross-domain narrative revision.
- [x] Exact final anonymous review source validated at manuscript head `36abe07d3041171465907bb6288d09209f512fa7`: Paper 1 Review CI run `35858767105` PASS; exact PDF artifact `10749180124`; 34 pages; abstract 99 words; blind-source audit PASS; anonymous-Acknowledgements omission PASS; AI-disclosure-footnote PASS; final LaTeX warning/layout audit PASS.
- [x] Manually visually inspect all 34 pages of exact artifact `10749180124` at 160 dpi on 2026-09-23: no clipping, overlap, broken glyphs, malformed tables, missing sections, or reference-layout defects found.

## Claims and novelty

- [x] Target domain and representation-to-target mapping are explicit semantic inputs.
- [x] No claim that metaphysical numerical identity is derived.
- [x] No claim that finite access creates individuality.
- [x] No novelty claim for observational equivalence, bisimulation, representation independence, target-directed scientific representation, discernibility theory, or practice-relative individuation.
- [x] Remaining novelty claim restricted to individuation-specific evidential admissibility plus mechanized anti-smuggling controls.
- [x] Closest prior art discussed explicitly.
- [x] The identity-token result is described as a negative control / dependency audit rather than deep mathematics.

## Formal artifact

- [x] Mechanized claims mapped to review labels `R1`--`R23`.
- [x] Public development has exact-head and merge-head Lean validation on its formal branch history.
- [x] No `sorry`, `admit`, `native_decide`, or project-local axioms in the validated formal surface.
- [x] Anonymous manifest states the formal scope and limitations.
- [x] Reviewer-facing formal artifact policy updated after external review: submit the anonymous standalone Lean supplement together with its R1–R23 map; keep non-blind repository provenance out of the review package.

## AI-use transparency

- [x] Anonymous manuscript AI disclosure moved to a non-identifying footnote; the anonymous review source contains no Acknowledgements section.
- [x] Tool named as OpenAI ChatGPT / GPT-5.6 Sol.
- [x] Access date stated.
- [x] Uses described: drafting, restructuring, translation, literature-search query formulation, editorial revision.
- [x] Author responsibility and independent verification stated.
- [x] Matching disclosure included in the non-blind cover-letter draft.
- [x] Cover-letter title and manuscript summary synchronized to the current Cross-Domain Audits version.

## Submission-system checks

- [ ] Supply the author's truthful **Funding Statement** for the typeset manuscript; do not infer or invent this.
- [ ] Supply the author's truthful **Declarations / competing-interests statement**; do not infer or invent this.
- [ ] Supply non-blind author metadata: full author name, affiliation, contact details, and ORCID if desired.

- [x] Re-opened the live Philosophy of Science author instructions and publishing-ethics pages on 2026-09-23; current Article limit is 9,000 words inclusive of abstract/footnotes/in-text citations/figures/tables/print appendices, with references excluded.
- [ ] Confirm manuscript is not under review elsewhere.
- [ ] Confirm all submission metadata.
- [ ] Add author / affiliation only in the non-blind submission fields as required.
- [ ] Decide whether any public preprint/repository disclosure is required at submission.
- [ ] Ensure every reviewer-facing supplementary file is anonymous.
- [ ] Upload final PDF and any source files requested by Editorial Manager.
- [ ] View and approve the PDF built by Editorial Manager before final submission; the journal will not forward the manuscript until this approval.
- [ ] Do not upload the public repository link as blind-review material.

## Decision gate

**Current state:** the manuscript was changed after the last validated artifact to incorporate the three final minor edits requested in re-review: stronger AI disclosure wording, explicit diagnostic/local-conservativity novelty framing, and narrower wording for structural post-hoc licensing. The previous PDF/visual validation is therefore historical only. Fresh exact-head Lean / English / Japanese CI, anonymous supplement build, PDF generation, and visual inspection are required before submission.

## External-review closure — 2026-09-23

- [x] Central theorem stated as fiber invariance ⇔ universal difference soundness ⇔ quotient descent, conditional on fixed proposed target assignment.
- [x] Direct DEKI comparison added: Frigg & Nguyen (2020); Nguyen & Frigg (2022).
- [x] Suárez (2024) contemporary inferential account directly compared.
- [x] Anonymous standalone Lean supplement added with pinned Lean 4.33.1, no external package dependencies, build instructions, and R1–R23 map.
- [x] CI audits supplement for identity leakage and banned proof shortcuts, builds it, and uploads it as a separate anonymous artifact.
- [x] Structural family admissibility explicitly distinguished from statistical multiple-testing correction.
- [x] Counterfactual re-encoding audit sharpened with a decision-rule automorphism criterion.
- [x] Exact revised anonymous PDF rebuilt on validation head `4a20763ce382dc4be3e8e497507690e7fae82565`: English Review CI `35873770536` PASS; artifact `10757245747`; same validated manuscript source; 37-page revision visually inspected at 160 dpi with no layout defects.
- [x] Exact anonymous Lean supplement validated and uploaded by Lean CI `35873770567`; artifact `10756480648`; pinned Lean 4.33.1; standalone `lake build` PASS.


## Re-review minor-edit closure — 2026-09-24

- [x] AI disclosure wording strengthened while remaining in the anonymous footnote.
- [x] Introduction explicitly states the diagnostic, local-conservativity payoff.
- [x] Section 2.4 narrows the post-hoc-selection language to one structural form of licensing.
- [ ] Rebuild and validate exact current head after these edits.
- [ ] Visually inspect every page of the resulting anonymous PDF.
