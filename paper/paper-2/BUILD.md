# Paper 2 — Generic Manuscript Build

> Submission-style working manuscript v1. This directory is not theory authority.

## Source

- Manuscript: `paper/paper-2/main.tex`
- Shared bibliography: `paper/references.bib`
- Prose working draft: `paper/paper-2-draft-en.md`
- Frozen result summary: `research/paper2/paper2_result_v1.json`

## Local build

```bash
cd paper/paper-2
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The manuscript uses the shared bibliography through:

```tex
\bibliography{../references}
```

## Validation contract

The dedicated GitHub Actions workflow must:

- check out the exact PR head;
- compile with BibTeX;
- fail on undefined citations/references;
- fail on LaTeX/package warnings after the final pass;
- fail on overfull boxes;
- verify that the PDF contains the title, author, core failure result, and ROLE_GAP result;
- upload the PDF and editable source package.

## Scientific boundary

Successful PDF compilation validates manuscript plumbing only.

Scientific authority remains with the frozen research and formal artifacts, especially:

- `research/paper2/paper2_result_v1.json`
- `research/paper2/claim_ir_reliability_boundary_v1.json`
- `research/paper2/grammar_v0_reverse_projection_aggregate_v1.json`
- `research/paper2/grammar_v0_residual_adjudication_v1.json`
- `research/paper2/grammar_v0_minimality_comparator_v1.json`
- `research/paper2/source_context_architecture_placement_v1.json`
- `research/paper2/system_world_experiment_architecture_v1.json`

Manuscript edits must not silently alter those results.

Terminal target:

```text
PAPER2_LATEX_MANUSCRIPT_V1_BUILD_VALIDATED
```
