# Paper 2 — JGPS Submission Package

Target journal: *Journal for General Philosophy of Science* (Springer Nature).

Prepared from the validated generic Paper-2 manuscript without changing any frozen research or formal artifact.

## Files

- `main.tex` — JGPS-facing manuscript.
- `title-page.tex` — separate title page and declarations.
- `references.bib` — standalone bibliography for Editorial Manager.
- `cover-letter.md` — submission cover letter.
- `submission-checklist.md` — journal-specific readiness checklist.

## Current JGPS requirements reflected here

- Full-length articles are around 10,000 words, with no strict upper limit.
- Abstract: 150–250 words.
- Keywords: 4–6.
- LaTeX is accepted for mathematical manuscripts.
- Editable sources must be supplied.
- Author/year citations are used.
- Statements and Declarations are required.
- Substantive LLM use is disclosed in Methods.
- JGPS uses Editorial Manager for online submission.

The Springer Nature LaTeX template is recommended by the publisher but is not stated as mandatory in the JGPS instructions. This package deliberately uses a flat, portable `article`-class source that compiles under `pdflatex` and packages all required editable files in one directory for Editorial Manager conversion.

## Build

```bash
cd paper/venues/jgps
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error title-page.tex
```

## Scientific authority

This venue package is presentation-only. Scientific authority remains with the frozen Paper-2 machine-readable artifacts and formal modules on `main`.

Terminal target:

```text
PAPER2_JGPS_SUBMISSION_PACKAGE_READY
```
