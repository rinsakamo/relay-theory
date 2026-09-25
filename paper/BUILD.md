# Paper 1 — Build and Validation

> Working manuscript build note. This file is not theory authority.

## Source

- Primary manuscript: `paper/main.tex`
- Bibliography: `paper/references.bib`
- Primary prose draft: `paper/paper-1-draft-en.md`

## Current-source note — 2026-09-23

The manuscript was subsequently revised to promote the bibliographic-record motivating example, retain molecular counting as a cross-domain scientific stress test, and add an evidence-synthesis bridge. The historical build results below therefore do **not** validate the exact current source. Rebuild and visual inspection are required after this revision.

## Reproducible local build

A standard BibTeX installation can use `bibtex`. The validation environment used on 2026-09-22 exposed `bibtex8` instead, so the successful build sequence was:

```bash
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex8 main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Validation result — 2026-09-22

- PDF generated successfully.
- 10 pages.
- Bibliography resolved successfully with `plainnat`.
- Final LaTeX pass: no warnings.
- No overfull boxes.
- No underfull boxes.
- No undefined citations or references.
- Rendered all 9 pages and visually inspected the output.
- The long Lean theorem identifiers in the claim-to-artifact map wrap within the table after using `tabularx`, `xurl`, and `\path{...}`.

## Scope of this validation

This validates manuscript compilation and layout only. It does not validate:

- the scientific novelty claim beyond the separate `novelty-audit.md`;
- the truth of bibliographic content beyond the metadata audit;
- the Lean proofs, which are validated by the repository's formal CI;
- suitability for any specific venue template.

## Before submission

Rebuild after applying the target venue's class/style files and repeat visual inspection, because pagination and line breaking can change under venue-specific formatting.
