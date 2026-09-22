# Philosophy of Science — Paper 1 submission checklist

> Working checklist. No submission has occurred.

## Manuscript identity

- [x] Submission type planned as **Article**.
- [x] Title fixed for the current review copy.
- [x] Author field omitted from the blind manuscript.
- [x] No public repository URL, project name, issue/PR number, or author identifier in the review manuscript.
- [x] Public Lean theorem identifiers replaced by neutral labels `R1`--`R15`.
- [x] Anonymous artifact manifest prepared.
- [ ] If executable Lean source is supplied during review, export a scrubbed anonymous package and validate it independently before upload.

## Journal format

- [x] Abstract <=100 words (current review abstract: 88 words).
- [x] Article length comfortably below the current Article word limit.
- [x] 12pt review text.
- [x] Double-spaced body.
- [x] Ragged-right review copy.
- [x] Chicago author-date bibliography style selected.
- [x] Bibliography source includes full `https://doi.org/...` URLs for all 13 current references with DOIs; exact PDF rebuild still required to verify the rendered output.
- [x] Rebuild the **exact current anonymized review source**: Paper 1 Review CI run #4 / exact head `c46dab5a3355e74af3f61711bc5e0a7dc1fcccde` generated an 18-page PDF and passed the blind-source and final LaTeX audits.
- [x] Manually visually inspect all 18 pages of the exact CI artifact PDF: rendered at 160 dpi on 2026-09-22; no clipping, overlap, broken glyphs, missing sections, or reference-layout defects found.

## Claims and novelty

- [x] Target domain and representation-to-target mapping are explicit semantic inputs.
- [x] No claim that metaphysical numerical identity is derived.
- [x] No claim that finite access creates individuality.
- [x] No novelty claim for observational equivalence, bisimulation, representation independence, target-directed scientific representation, discernibility theory, or practice-relative individuation.
- [x] Remaining novelty claim restricted to individuation-specific evidential admissibility plus mechanized anti-smuggling controls.
- [x] Closest prior art discussed explicitly.
- [x] The identity-token result is described as a negative control / dependency audit rather than deep mathematics.

## Formal artifact

- [x] Mechanized claims mapped to review labels `R1`--`R15`.
- [x] Public development has exact-head and merge-head Lean validation on its formal branch history.
- [x] No `sorry`, `admit`, `native_decide`, or project-local axioms in the validated formal surface.
- [x] Anonymous manifest states the formal scope and limitations.
- [x] Initial artifact policy decided: submit the anonymous manifest only; prepare executable scrubbed Lean source if requested by the editor/reviewers or required by the live portal.

## AI-use transparency

- [x] Anonymous manuscript disclosure included in `Acknowledgements`.
- [x] Tool named as OpenAI ChatGPT / GPT-5.6 Sol.
- [x] Access date stated.
- [x] Uses described: drafting, restructuring, translation, literature-search query formulation, editorial revision.
- [x] Author responsibility and independent verification stated.
- [x] Matching disclosure included in the non-blind cover-letter draft.

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

**Current state:** exact-source blind review CI and page-by-page visual inspection are complete, and the initial artifact policy is fixed. Remaining pre-upload gates are the live-portal instruction re-check, submission metadata, and confirmation that the manuscript is not under review elsewhere.
