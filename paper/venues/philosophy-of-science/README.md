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

## Successful local build

Validated on 2026-09-22 with:

```bash
cp paper/references.bib paper/venues/philosophy-of-science/references.bib
cd paper/venues/philosophy-of-science

pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex8 main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Result after the layout fixes:

- PDF generated successfully;
- 18 review-format pages;
- final LaTeX pass has no overfull/underfull boxes and no undefined citations/references;
- all rendered pages were visually inspected;
- the long Lean theorem identifiers are line-breakable;
- the only non-LaTeX diagnostic in the validation environment is a `bibtex8` style warning for the editor-only Bueno–Chen–Fagan volume under `chicago.bst`; the rendered bibliography entry is correct.

A standard environment with ordinary `bibtex` can use it instead of `bibtex8`.

## Blind-review boundary

The review copy refers to a Lean development and theorem names because those are part of the evidential argument, but it intentionally does **not** identify the public repository or authorship.

Before actual submission, decide how the supplementary formal artifact should be supplied under the journal's anonymous-review policy. Do not insert a self-identifying repository link into the review manuscript before that decision.

## Remaining pre-submission decisions

- confirm that *Philosophy of Science* is the actual first target;
- decide whether and how to provide the anonymous Lean artifact;
- fill author metadata only in the non-blind submission fields / final accepted source as appropriate;
- do one final journal-portal check immediately before submission because submission requirements can change.

No journal submission has been made from this workspace.
