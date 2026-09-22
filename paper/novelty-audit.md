# Paper 1 — Novelty Audit

> Internal working note. Non-authoritative.  
> Search pass: 2026-09-22.  
> Purpose: record the closest prior art found and the remaining defensible novelty surface. This is a targeted search, not a proof of absence.

## Result

The deeper search materially narrows the manuscript's novelty claim.

The following ideas are clearly prior art and must **not** be claimed as new:

1. **Scientific representation is target-directed and inferential.**  
   Suárez (2004) explicitly characterizes scientific representation through directionality and inferential capacity.

2. **Representations can be interpreted in terms of targets so as to license surrogative inferences.**  
   Contessa (2007) develops this as an interpretational account.

3. **Model/theory comparison can turn on which claims models license about the same target systems.**  
   Nguyen (2017) is the closest result found in this pass and substantially overlaps the manuscript's representation-to-target evidential framing.

4. **Individuation is practice-relative and can have an epistemological/presentational mode.**  
   Bueno, Chen, and Fagan (2018), Waters (2018), Love (2018), and especially Chen (2018) cover this terrain.

5. **Representationally redundant or surplus structure need not be dispensable.**  
   Nguyen, Teh, and Wells (2020) blocks any inference from "not target-individuating evidence" to "useless structure."

6. **Observational equivalence, bisimulation, representation independence, and discernibility are mature prior frameworks.**

## Closest prior art

### Nguyen 2017 — Scientific Representation and Theoretical Equivalence

This is the most important novelty constraint.

Nguyen argues that attention to how models are used to draw inferences about target systems supports a notion of theoretical equivalence based on whether models license the same claims about the same targets.

This means Paper 1 cannot claim novelty for:

```text
representation
-> target-directed inference
-> licensed claims about target
```

The remaining distinction is that Paper 1 applies an explicit admissibility question specifically to **individuation claims** and tests representation-only discriminators with a machine-checked negative-control artifact.

### Chen 2018 — Experimental Individuation: Creation and Presentation

Chen distinguishes ontological and epistemological modes of experimental individuation and discusses the presentation of individuals in experimental practice.

Paper 1 should therefore avoid suggesting that the separation between presentation and individuation is itself novel.

Its narrower formal question is whether a difference that exists only in the representation apparatus is admissible evidence for target-level plurality under a declared semantics.

### Nguyen, Teh, and Wells 2020 — Why Surplus Structure Is Not Superfluous

This work is important as a limiting comparison.

Paper 1's negative result is **not eliminativist**. A representation-only distinction can fail to count as evidence for the tested target-level individuation claim while still being useful or necessary for representation, computation, locality, or other theoretical purposes.

## Remaining candidate novelty

The strongest defensible contribution after this search is conjunctive:

```text
individuation-specific evidential admissibility
+
explicit representation/target/test factorization
+
representation-sensitive negative control
+
explicit identity-like-token invariance control
+
machine-checkable dependency audit
```

No exact prior formulation of that complete package was located in this targeted pass.

That sentence is **not** a proof of novelty. A venue-specific literature review could still uncover a closer predecessor.

## Consequence for manuscript language

Use:

> a representation-safe evidential discipline for formal individuation claims

Avoid:

> a new theory of representation

> a new theory of observational equivalence

> a derivation of individuality from distinguishability

> target-directed inference is our contribution

> representation-only or surplus structure is dispensable

## Current publication assessment

The paper remains potentially publishable as a narrow formal-methodological note if the contribution is presented as:

1. a precise individuation-specific inference rule;
2. a set of explicit counterexamples/negative controls preventing presentation identity from doing hidden work;
3. a Lean artifact that audits those dependencies.

The novelty case is substantially weaker if the mechanization is removed; without it, much of the conceptual content lies very close to existing work on scientific representation, equivalence, and practice-relative individuation.
