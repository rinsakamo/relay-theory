# Anonymous Lean supplement — Paper 1

This archive is the anonymous machine-checkable supplement for the manuscript.

## Scope

The source formalizes only the dependency claims reported in the paper:
representation-to-target assignment, fiber invariance, universal soundness of
feature-difference inference, quotient descent, test-specific and family-level
factorization, finite positive/negative controls, and semantically inert token
metadata.

It does **not** establish empirical warrant for a target assignment, measurement
model, test family, or scientific application.

## Toolchain

- Lean: 4.33.1
- External package dependencies: none
- Build system: Lake bundled with the pinned Lean distribution

## Build

```bash
elan toolchain install "$(cat lean-toolchain)"
lake build
```

A successful build compiles `Paper1Audit.lean`.

## Anonymous result map

See `RESULT_MAP.md` for the one-to-one mapping from manuscript labels
`R1`–`R23` to theorem names in `Paper1Audit.lean`.

Repository identity, author identity, and non-blind provenance are intentionally
omitted from this review artifact. A non-anonymous archival citation can replace
this supplement after review.
