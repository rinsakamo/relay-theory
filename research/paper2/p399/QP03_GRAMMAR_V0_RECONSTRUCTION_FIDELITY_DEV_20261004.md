# Issue #399 QP03 — retrospective Grammar-v0 reconstruction / fidelity (2026-10-04)

**Scope: developmental D/E only, not one of the 4 prospectively qualified new pilots.** This document summarizes a separate source-scoped reconstruction of Marković, Gläscher, Bossaerts, O'Doherty & Kiebel (2015), “Modeling the Evolution of Beliefs Using an Attentional Focus Mechanism,” DOI 10.1371/journal.pcbi.1004558.

- Canonical primary source: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004558 . The same-article PMC HTML transcript was used only to render already present mathematical content into legible characters: https://pmc.ncbi.nlm.nih.gov/articles/PMC4619749/ . Do not treat unseen stand-alone supplements as audited, or treat the auxiliary transcript as certification that exact publisher embedded math/figure pixels were independently visually checked.
- Historic frozen original A: **17 items, 12 edges**, SHA256 `8900c52c8ce96947b1e8f43ffe146035aa99deaedc211ee0496911b4bcb54e84`. B SHA256 `5e829ab35695343a03856bc7b4f6340f2f887048b4acd47eb3965863f9a10e23`. C SHA256 `72958c88495d3eecd82cb2745ed00aaece8080c2b43e22ce52950807dcd5d9f4`. Existing A_v2 delta SHA256 `6fce9cf94cf584c5e528e8b9ace61a45a59b738ab16e804223c0f15e93486795`. The original full 17+12 JSON records were **not available during this separate D/E run**; an exact all-ID comparison is NOT claimed and no earlier artifact is edited.

## Source-defined direct integration: candidate A0 topology, not proven full-fidelity A0
- `Pi/X`: six exemplar/rule hypotheses, six exemplar relevance states and three feature relevance states in the full perceptual model; matching exemplar-to-feature partition.
- `K/T/C`: independent internal noise, nonlinear competitive attention dynamics with within-level inhibition and between-level matched excitation, predicted state mean/covariance; ordered information-dependent update. Original connection matrix `W` ≠ RelayTheory World `W`.
- `Gamma` imports external trial evidence. Eq(9) explicitly uses *predicted relevance times likelihood*, a load-bearing attention-to-inference dependency. Eq(11) drives mean belief update with covariance-weighted categorical prediction error. Feature-level direct innovation is zero but covariance/structured coupling can transmit influence. The paper's parameter `γ` is **not** boundary `Gamma`.
- `Q/P_out/rho/O` produces a three-feature response with risk attitude and permitted fixed versus uncertainty-dependent variability. OTO inversion and CMA-ES/Laplace/model-family selection stay in researcher-side `E_exp/L_ctx/L_formal`, not an invented participant coordinator.

## Six distinct perceptual structures and variant restrictions
- `w1`: both levels inhibited, linked by matched cross-level excitation.
- Equation/Structured-model designation: `w2` has `κ_e=0`; `w3` has `κ_f=0`. **Original List-of-models prose reverses their apparent level labels**. Preserve the conflict and do not silently fix names. Historic original C already appends A18 for this source conflict.
- `d`: both lateral inhibitions removed, **matched cross-level excitation retained**.
- `rw`, `rd`: feature level removed; the first retains exemplar inhibition, the second removes it.
- Bayesian belief uncertainty updates are distinct from the fixed-uncertainty non-Bayesian competitor, with reduced-model covariance exact scope left explicitly qualified.
- Eligibility rule yields `4 full Bayesian × 2 responses + 2 reduced Bayesian × 1 + 6 nonBayesian × 1 + 1 baseline = 17`, but the article's literal neighboring list states `12 + 6 + 1 = 19`; both source assertions remain visible. Response-model text uses `θ3` for the full noise parameter, neighboring list uses `θ2`; use semantically full/reduced response typing until source adjudication.
- Condition-specific behavioral claims must also be retained: Bayesian and full hierarchical model families supported in both conditions; structured model reaches the paper's threshold only in no-switch; full response evidence in switch is inconclusive.

## Developmental fidelity receipt
The separately archived 29-item scoped audit ledger has:
- 17 `SUPPORTED_SCOPED`
- 4 `PARTIAL_ORIGINAL_VISUAL`
- 3 `PARTIAL_FULL_DYNAMIC`
- 4 `UNDERDETERMINED_SOURCE_CONFLICT`
- 1 `BLOCKED_INPUT_NOT_AVAILABLE` (exact old full A/B/C record reconciliation).

Standard-library *developmental* algebraic/topology/destructive tests **26/26 PASS**: source-described Eq(4)/(5)/(9)/(11) fragments with supplied predicted state and covariance, six variant-topology tests, predicted-prior ablation, crosslevel-coupling edge ablation, permitted model pairing, preservation of the known published contradictions. **NOT** the original Eq(6–12) full 9D nonlinear neural simulation, original 17-model fitting or independent subject-data replication. Structural tests of manually entered formulas cannot certify full source fidelity.

Local detailed Japanese report, per-row JSON, executable tests, SHA256SUMS and raw execution receipt are delivered in originating-chat `QP03_GRAMMAR_RECONSTRUCTION_DEV_20261004.zip` (SHA256 `6e0d64ba9d4adfa867c1f0c62d4ded47095178b39017c1d60af33c3a73fda0f8`). This PR intentionally stores only safe summary metadata; the local ZIP/code is **not Git-tracked or CI validated**.

**Scientific label:** `SOURCE_SCOPED_TOPOLOGICAL_RECONSTRUCTION_SUCCESS`; `A0_TOPOLOGY_CANDIDATE_ONLY`; `FULL_ORIGINAL_DYNAMIC_FIDELITY_UNDERDETERMINED`. The source itself already fuses WTA and Bayesian inference, so no new coordinator or extra primitive is needed *to represent its stated integration topology*, not a general H0 proof. Historical exposure: NO prospective validation credit; **qualified new pilot 0/4 and MAIN NOT AUTHORIZED**. Unchanged 60-ClaimIR, Grammar v0, QP03 A/B/C, PR #401 source-audit adoption and previous QP01/02 reconstruction PRs. Refs #399 #321.
