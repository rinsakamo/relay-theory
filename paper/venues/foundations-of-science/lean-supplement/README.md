# Online Resource 1 — Lean dependency-verification supplement

Article: When May a Formal Difference Enter an Individuation Inference? Target Factorization, Restricted Tests, and Cross-Domain Audits
Journal: Foundations of Science
Author: Rintaro Sakamoto, MPH
Affiliation: Independent Scholar, Kitakyushu, Japan
ORCID: 0009-0002-0443-2508
Corresponding author email: rin.sakamoto.research@gmail.com

This archive formalizes only the dependency claims reported in the paper: representation-to-target assignment, fiber invariance, universal soundness of feature-difference inference, quotient descent, test-specific and family-level factorization, finite positive/negative controls, and semantically inert token metadata.

It does **not** establish empirical or semantic warrant for a target assignment, measurement model, test family, or scientific application.

Toolchain: Lean 4.33.1. External package dependencies: none.

Build:

```bash
elan toolchain install "$(cat lean-toolchain)"
lake build
```

See `RESULT_MAP.md` for the one-to-one R1–R23 mapping. Repository provenance: RelayTheory owner #206, branch `paper-1-foundations-of-science`.
