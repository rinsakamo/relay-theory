# M29 — Finite pair-law derivation and representation-specific support

**Parent authority:** M28 Draft PR #490, exact HEAD `fb689ce586be1cf1d2d9b87a75eb385c2674ffda`.  
**Branch:** `paper2/p399-main-m29-finite-pair-law-20261008`.  
**Scope:** strictly philosophical/formal refinement. No source corpus recoding, rerun, reassignment of identity kinds, or human reliability claims.

## Main result

An exactly specified conditional pair law on `F={0,1}^3` with `C(c,x,y)=c` and maps `phi_x(f)=x`, `phi_y(f)=y`. Both maps have C-crossing fibers. Under one fixed pair distribution:

| Event | P(E given same C) | P(E given different C) | LR |
|---|---:|---:|---:|
| Equal x signatures | 4/5 | 1/5 | 4 |
| Equal y signatures | 1/2 | 1/2 | 1 |
| Bounded motif overlap (x OR y) | 9/10 | 3/5 | 3/2 |
| Unlabelled map choice, weight x = 1/2 | 13/20 | 7/20 | 13/7 |

The conditional law explicitly stipulates which response feature covaries with mechanistic identity. It is *not* inferred from Daw et al. (2011), whose DOI 10.1016/j.neuron.2011.02.027 motivates the scientific plausibility of mixed model-based and model-free choice influences only. No actual scientific capacity-identity defeater is inferred.

## Critical correction to the earlier philosophical reading

Two distinct reasons for revising a support statement must not be conflated. First, two specified preservation maps generate different evidential events under the same fine-state law; hence their valid likelihood ratios can differ. **This is not undercutting of the correctly attributed LR 4 for phi_x.** Second, when provenance of *which event* the report contains is missing and the argument attributes the x-specific LR 4 to the unlabelled match, the unsupported attribution is undercut. In the latter case a reporting-map mixture has a separately justified weight w; the BF becomes (1/2+3w/10)/(1/2-3w/10). The existence of a competing map alone does not change LR 4.

## Bounded event bridge

Typed motifs `M(f)={m^x_x,m^y_y}` generate pair event `E_x OR E_y`, with derived LR 3/2. It is nontransitive, so it does not define signature-equivalence fibers; the audit examines event preimages on the product space `F x F`.

## Qualification gates

Run exhaustive `scripts/paper2_m29_finite_pair_law_audit.py` plus all inherited M28/M27 scientific and manuscript guards. Strictly compile article and supplement; refuse unresolved final citations, undefined control sequences, and overfull boxes. No CI pass claim before the run finishes.

## Remaining philosophical limits

- Probabilities follow exactly from a **stipulated generative model**, not empirical cognitive science.
- Independence of the reporter-map indicator from H is an express condition, not a universal property.
- Which C (functional, mechanistic, etc.) is justified is not decided by the construction.
- A model-agnostic positivity claim is invalid; a calibrated map-specific one may be valid.
- The comparison demonstrates operational representation-induced event specificity, not an independent probabilistic theory of confirmation.
- Complete final manuscript and M29 artifact URLs still require archival pinning at deposition; M27/M28 fixed citations do not replace that.

**Do not modify** the frozen 1770/1770, 206, 99, 143, 63/99, 21/22/17, 0/17 or human-coding reliability status.
