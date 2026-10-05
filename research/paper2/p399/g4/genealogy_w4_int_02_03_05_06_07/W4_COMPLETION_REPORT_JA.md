# RelayTheory Paper 2 — G4 Genealogy W4 Completion Report

## Scope and isolation

W4 was branched exactly from Draft PR #438 head `ae044a8f475fb0dc9140a91e360e1ff26a0b5e3a` onto `paper2/p399-g4-w4-int02-03-05-06-07-native-20261005`. This lane profiles only INT-02, INT-03, INT-05, INT-06 and INT-07. INT-01/04/08 are comparison targets only; INT-09–16 and all non-INT lanes were not profiled here.

The shared 26-profile manifest `research/paper2/p399/g4/genealogy_accelerator_v1/ORIGINAL_NATIVE_PROFILES_v1.json` was not edited and remains pinned at Git blob `903f8db6e1569ed27507cf47e668f7599a08cd98`. Shared pair-matrix generation/CI was not modified. Preliminary MAIN results, Grammar-v0 reconstruction, H0/H1/H2 classification and MAIN scientific conclusions were not inspected or performed. MAIN authorization remains **false**.

## Five-paper status

| Slot | DOI | Completion | Adopted source | Source-native center |
|---|---|---|---|---|
| INT-02 | 10.3390/e26060484 | PROFILE_FRAGMENT_READY | MDPI/Entropy VoR PDF, SHA256 `a1e644…cc37` | entropy-difference beta update + CL/DPEFE geometric policy pooling |
| INT-03 | 10.1073/pnas.95.24.14529 | SCIENTIFIC_ANCESTRY_UNDERDETERMINED | official PNAS complete HTML; raw PDF/HTML hash unavailable | recurrent workspace gating + reward-modulated Hebbian update + vigilance/gain |
| INT-05 | 10.1371/journal.pcbi.1004110 | PROFILE_FRAGMENT_READY | PLOS PDF SHA256 `6a0445…bb95` + first-party HTML crosscheck | drift-diffusion evidence + action focus + position-feedback commitment |
| INT-06 | 10.1371/journal.pcbi.1000765 | SCIENTIFIC_ANCESTRY_UNDERDETERMINED | PLOS main + 8 official supplements; main SHA256 `c27629…0706` | task-set/NMDA spiking router + threshold gate + inhibitory reset + sensory buffer |
| INT-07 | 10.1371/journal.pcbi.1003383 | SOURCE_BLOCKED | PLOS main SHA256 `a22b6e…6698` + first-party HTML; Text S1–S4 raw media not frozen | transition/observation model + EKF filter + RTS/gamma smoother + input inference |

Counts: **READY 2 / SOURCE_BLOCKED 1 / SCIENTIFIC_ANCESTRY_UNDERDETERMINED 2**.

## Provenance and edition boundaries

INT-02 reuses G2-D v14 blob `956d3626ea527b1977d17a5710094bc7dd327b14`; historical author code remains a separate non-edition artifact. INT-03 reuses G2-D v13 blob `bc28569f6a79ea4adef00ceb4f02361f57646272` and deliberately leaves browser-only source hashing unresolved rather than inventing bytes.

INT-05 and INT-07 reuse source gate blob `c2a46cdceea3e9aba89b94a6c4f9347f85f32047` for exact publisher-main identities, with current first-party PLOS HTML used only for semantic recovery. INT-05's external code ZIP is not a VoR substitute. INT-07's Text S1–S4 are explicitly model-defining but not raw-frozen, so it fails closed.

INT-06 reuses v5 blob `db2f91eb09eb373d57e9b417dbf5a9af8cd70363`, preserving all eight supplement SHA256s and the source-local adverse findings.

## Pairwise findings

All ten W4-internal pairs were reviewed. Nine are new **BOUNDED_SOURCE_NATIVE_DIFFERENCE** findings. INT-03×INT-06 reuses prior G2-D blob `7dc2cd214d61312e60e8bb03ff1bf654aaf0f288` and is **SHARED_CONSTITUENT_ONLY**: broad recurrent/global-workspace ancestry is supported, but the task-set/NMDA router is not the exact same central mathematical model. Neither bounded difference nor router difference implies global family independence.

Each W4 paper was also reviewed against all 20 existing G1 profiles and the six existing G2 profiles ATT-03, BLF-01, PRD-01, INT-01, INT-04 and INT-08. The resulting 130 cross-profile rows remain **UNDERDETERMINED** absent pair-specific source witnesses; generic words such as workspace, recurrent, Bayesian, state-space, gating, planning, control or attention never auto-promote identity or independence.

Reused bounded pair count: **1**. Newly added bounded pair count: **9**. Global family independence certified: **0**.

## Remaining blockers and authorization

Material blockers are INT-03's DOI-level predecessor genealogy/edition reconciliation, INT-06's exact workspace/router genealogy relative to INT-03, and INT-07's four required official Text S1–S4 raw media/SHA. All are explicit; none are silently resolved.

`test_w4_fail_closed.py` enforces exact identities, provenance, hash retention, local operator IDs, no global independence, no ancestry-exhaustiveness promotion, no broad-workspace auto-promotion, no bounded-difference-to-independence promotion, shared-manifest immutability, W4-only path isolation and MAIN authorization=false.

Draft PR metadata and final HEAD/CI are reported at lane completion after the PR is opened.
