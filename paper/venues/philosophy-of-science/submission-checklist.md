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
- [x] Abstract followed by a page break, matching the journal's non-template accepted-manuscript structure guidance.
- [x] Submission-facing section/subsection titles use headline capitalization.
- [x] Venue-source tables use full-size 12pt text (no `\\small` overrides).
- [x] Reference page ranges are normalized to Chicago-style abbreviated inclusive numbers where applicable.
- [x] Chicago author-date bibliography style selected.
- [x] Anonymous review manuscript ends with **References**; acknowledgements are omitted for blind review.
- [x] Accepted-manuscript back-matter order is fixed as **References → Acknowledgements → Declarations → Funding Statement**; factual Declarations/Funding text remains author-supplied.
- [x] Bibliography source includes full `https://doi.org/...` URLs for all 13 current references with DOIs; run #11 rebuilt the exact review PDF and the rendered references were visually verified.
- [x] Rebuild the **exact current anonymized review source** after DOI completion: Paper 1 Review CI run #11 / exact head `1ee8022a7fc740ec8e11c27b7e59aa489373ddbb` generated an 18-page PDF and passed all blind-source, bibliography, and final LaTeX audits.
- [x] Manually visually inspect all 18 pages of the DOI-complete exact CI artifact PDF: run #11 artifact ID `10702765379`, rendered at 140 dpi on 2026-09-23; no clipping, overlap, broken glyphs, missing sections, or reference-layout defects found. This validation is historical after the later cross-domain narrative revision.
- [ ] Rebuild and visually inspect the exact current anonymized review source after the final Philosophy of Science compliance edit (AI footnote + cover-letter synchronization).

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
- [x] Initial artifact policy decided: submit the anonymous manifest only; prepare executable scrubbed Lean source if requested by the editor/reviewers or required by the live portal.

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

- [x] Re-opened the live Philosophy of Science author instructions on 2026-09-22; current Article limit is 9,000 words inclusive of abstract/footnotes/in-text citations/figures/tables/print appendices, with references excluded.
- [ ] Confirm manuscript is not under review elsewhere.
- [ ] Confirm all submission metadata.
- [ ] Add author / affiliation only in the non-blind submission fields as required.
- [ ] Decide whether any public preprint/repository disclosure is required at submission.
- [ ] Ensure every reviewer-facing supplementary file is anonymous.
- [ ] Upload final PDF and any source files requested by Editorial Manager.
- [ ] View and approve the PDF built by Editorial Manager before final submission; the journal will not forward the manuscript until this approval.
- [ ] Do not upload the public repository link as blind-review material.

## Decision gate

**Current state:** the anonymous review source is structurally aligned with the current Philosophy of Science instructions: 99-word abstract, anonymous author field, no Acknowledgements section, AI disclosure in a non-identifying footnote, and References as the final review-manuscript section. The exact post-edit source still requires fresh CI/PDF validation. Author-supplied Funding/Declarations, non-blind metadata, publication/concurrent-review eligibility, and final Editorial Manager PDF approval remain required.
