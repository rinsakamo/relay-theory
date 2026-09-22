# Philosophy of Science review-copy workspace

> Working submission adaptation for Paper 1. This directory is not repository theory authority and does not imply that submission has occurred.

## Intended article type

**Article**.

The manuscript is an independent contribution rather than a focused response to a recent published paper, so it is being adapted as an Article rather than a Discussion Note.

## Review-copy status

Current review source:

- `paper/venues/philosophy-of-science/main.tex`

Shared bibliography:

- `paper/references.bib`

The venue-neutral manuscript remains:

- `paper/main.tex`

The venue-specific copy is deliberately separate so formatting changes do not alter the canonical working text.

## Current checks

- anonymous author field;
- no author name, repository name, GitHub URL, issue/PR number, or project name in the review-copy source;
- 12pt text;
- double-spaced body;
- ragged-right review text;
- review margins adapted to the journal guidance used in the 2026-09-22 venue audit;
- abstract: **88 words**, below the current 100-word limit;
- article body: roughly **2,600 words**, well below the current Article word limit;
- Chicago author-date bibliography style;
- title/abstract separated from the main text for readable review pagination.

## Previous successful local build

Validated on 2026-09-22 with:

```bash
cp paper/references.bib paper/venues/philosophy-of-science/references.bib
cd paper/venues/philosophy-of-science

pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex8 main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Result for the review-format source before the final R1--R15 / Acknowledgements anonymization pass:

- PDF generated successfully;
- 18 review-format pages;
- final LaTeX pass has no overfull/underfull boxes and no undefined citations/references;
- all rendered pages were visually inspected;
- public theorem identifiers are removed from the blind review copy and replaced by neutral labels R1--R15;
- the only non-LaTeX diagnostic in the validation environment is a `bibtex8` style warning for the editor-only Bueno–Chen–Fagan volume under `chicago.bst`; the rendered bibliography entry is correct.

A standard environment with ordinary `bibtex` can use it instead of `bibtex8`.

## Blind-review boundary

The review copy refers to the Lean development only through neutral result labels R1--R15. Public theorem identifiers, repository names, repository URLs, issue/PR numbers, and author metadata are excluded from the blind manuscript.

An anonymous artifact manifest is maintained in this venue workspace. Do not insert the public repository URL or public theorem identifiers into materials sent for blind review.

## Remaining pre-submission decisions

- confirm that *Philosophy of Science* is the actual first target;
- decide whether and how to provide the anonymous Lean artifact;
- fill author metadata only in the non-blind submission fields / final accepted source as appropriate;
- do one final journal-portal check immediately before submission because submission requirements can change.

No journal submission has been made from this workspace.


## AI-tool disclosure

The current Cambridge publishing-ethics policy requires disclosure when generative AI is used to generate manuscript text. The blind review copy therefore includes an anonymous AI Tool Disclosure naming OpenAI ChatGPT / GPT-5.6 Sol, the access date, and the purposes for which it was used, while stating that the author independently verified the manuscript and remains responsible for the content.

This disclosure is intentionally non-identifying.


## Final rebuild status

**Exact-source CI: PASS.**

The current anonymized review source was validated at exact PR head `c46dab5a3355e74af3f61711bc5e0a7dc1fcccde` by **Paper 1 Review CI**, run #4 (`35742256009`).

The job passed:

- exact-head checkout verification;
- blind-source identifier audit;
- abstract-length check;
- presence of all anonymous result labels `R1`--`R15`;
- full LaTeX + BibTeX build;
- 18-page PDF generation;
- final LaTeX warning / citation / layout audit;
- PDF text smoke checks for title, Acknowledgements, and formal result labels.

The exact CI artifact from run #6 was downloaded and rendered at 160 dpi. All 18 pages were inspected page-by-page on 2026-09-22. No clipping, overlap, black/broken glyphs, missing sections, or reference-layout defects were observed.

Artifact details:

- run: `#6 / 35742873397`
- head: `8a521862be76f0526422bf343f7fa2d036b26ac3`
- artifact ID: `10699848683`
- artifact name: `paper-1-philosophy-of-science-review-pdf`
- PDF pages: `18`
- PDF SHA-256 after artifact extraction: `1662175011fe0f1760ab19499cde1f4cf1a86ae47ad6b0cc3e9cd22bd1061da2`


## Initial artifact policy

For the initial blind submission, the planned reviewer-facing formal supplement is the **anonymous artifact manifest**, not an executable copy of the public Lean source.

Rationale:

- the current journal guidance does not require supplementary executable material at initial submission;
- the public source is searchable and could weaken anonymous review;
- the manuscript's formal claims are already represented by neutral labels `R1`--`R15`;
- a scrubbed executable Lean package can be exported and independently revalidated if an editor or reviewer requests it.

If the live submission portal explicitly requires executable supplementary source, revisit this decision before upload.
