# M9-D — JGPS reviewer-facing terminology audit

This pass changes terminology and presentation only. Scientific counts, classifications, source roster, formal results, and limitation boundaries are unchanged.

## Principle

Reviewer-facing prose now uses ordinary philosophy-of-science / cognitive-science language. Repository-internal milestone names, machine status codes, CI terminal strings, implementation type names, and provenance hashes are kept out of the manuscript unless they carry scientific meaning. Exact repository identifiers remain available in the supplementary provenance materials.

## Main replacements

| Internal / engineering-facing term | Reviewer-facing term |
|---|---|
| Archetype/XLike | reusable structural subobject |
| ClaimIR | structured claim record |
| MAIN40, M7, W9, G2, M9-* | prospective 40-paper corpus; integration/genealogy audit; post hoc stress test |
| ROLE_GAP and machine residual codes | ordinary-language residual classes |
| Grammar v0 | structural role grammar |
| lane / lane-local | analysis stream / within-stratum |
| fail-closed | conservative decision/integration rule |
| hostile / destructive controls | adversarial tests / negative and ablation controls |
| frozen | pre-specified, fixed, or versioned according to context |
| source-native / source-faithful | specified by / faithful to the source model |
| least-lift | minimal faithful reconstruction level |
| H0/H1/H2 | direct composition / stateless mediation / persistent coordination |
| system/World | system--environment |
| CI status strings and hashes | supplementary provenance ledger |

## Scientific invariants

- whole-claim comparison: 1770/1770 incomparable
- reusable structural subobjects: 206
- cross-stratum families: 99
- reverse projection: 21 full / 22 partial / 17 residual
- residual claims requiring an additional top-level role: 0
- prospective corpus: A0=40 / A1=0 / A2=0
- component arm: 24/24 A0
- integrated arm: 16/16 A0
- independent human re-adjudication: not performed
- genealogical independence: not claimed
