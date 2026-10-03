# #399 QP02 — retrospective Grammar-v0 D/E reconstruction and fidelity audit (2026-10-04)

**DEVELOPMENT ONLY**: this work is a source-scoped post-A/B/C reconstruction of Ryom et al. (2021), DOI `10.1371/journal.pcbi.1008809`; it is NOT a prospectively qualified new pilot, independent assessor result, runnable full Potts simulation or alteration of frozen source science.

## Source and historic authority
- Original publisher-designated full article: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008809 .
- Legible published-article mathematical rendering, checked solely to transcribe corresponding original-article formulas (not external supplementary model content): https://pmc.ncbi.nlm.nih.gov/articles/PMC8476040/ .
- Existing frozen A=22 items, 14 edges (SHA `219ffe0c087479f34c5667387f367c277c3364c8d41c0dc9673930933dc100de`), B (SHA `8daf7f6255397230c08b5f9fb597582e2dc934d291ddba77ad425f2153f98841`), C (SHA `b4219cc756de05896d1361feb44dd0bb105e02de77692a3344822ef47b20d4ce`), and original C append-only A_v2 (SHA `a0bbbf1cadbf8349dc8c1df80c62a9dfb293b4f5ebf51d93092606f8ad7793a7`) were not changed.
- Original JSON for the 22+14 initial records was **NOT directly available in this session**. This report uses source and prior recorded counts/dispositions; do not claim exact per-ID replay.
- Preserve accepted historic C `A23/E15` addition: Model2's selected-state adaptive threshold reduction screens refractory effect and independently alters spontaneous latching length, not only interference. Historical B02 external-supplement gate is superseded under author-ratified v2.2.2 original-full-HTML-only scope; numerical unshown supplement claims remain uncertified.

## Frozen Grammar roles, no modifications
- `Pi`: distinguish network unit, state, pattern, connection and selected set of L patterns. This necessary partition separates the four short-term boost variants.
- `X`: **common** distributed long-term Potts network configurations reused for short-term function; no invented standalone STM module.
- `K/T`: Hebbian-fixed existing tensors, transient selective boosts, state adaptation, dual-timescale inhibition, and intrinsic spontaneous state succession. Continuous neural time, latch count and experimental presentation timing stay typed apart.
- `C`: sparsity/network resource overlap, refractory effects and permissible inhibition/latching regimes. The source's Eq18–21 `L_c` is **a heuristic resource occupancy crossing**, not measured subject capacity.
- `Q`: selected-set orientation at most; do NOT convert external researcher `Delta M_corr` into intrinsic reward/utility.
- `P/rho/O`: stimulus and cue crossing World/system boundary; Eq9 pattern overlap and recalled-item readout. Experimenter stopping and measured cursor response belong to `E_exp/L_ctx`, not a detailed source-specified motor mechanism.
- Article symbol `gamma_A` balances fast/slow inhibition; it is **not** RelayTheory `Gamma` world–system coupling.

## Four distinct source-model operations
1. **Model1:** selected-participant UNIT-specific `w` feedback boost; original Eq10.
2. **Model2:** selected UNIT-STATE-specific `theta` decrease; Eq11, plus the independent refractory/latching-length consequence `A23/E15`.
3. **Model3a:** selected COMMON-PATTERN autoassociative synapses; Eq12.
4. **Model3b:** selected ANY-PAIR synapses, including distinct-pattern heteroassociations; Eq13. Never collapse 3a into 3b.

Source formula substructure: Eq9 normalized overlap; Eq10–13 four masks; Eq14–17 occupation `M1=1-(1-a)^L`, `M2=1-(1-a/S)^L`, `M3a=1-(1-a^2/S^2)^L`, `M3b=(1-(1-a/S)^L)^2`, and the heuristic crossing Eq18–21. For a=.25,S=7, published rounded crossings ~3.5 / 27.5 / 783.5 / 43.5 (M1/M2/M3a/M3b), NOT the model's plotted task capacity.

**Serial extension**: source-defined Model2 plus **ordered, weak** heteroassociative instruction Eq24 biases pre-existing spontaneous latching. This is not Model3b's all-pair strengthening. Excessive ordering strength harms latching quality; the published model cannot capture the human repetition benefit for AA/ABA, an explicit limitation.

**Source-internal unresolved conflict**: Fig2C caption reports M2/M3b peaks and M3a continuing growth, one body sentence attributes a drop to M2/M3a; later critical-resource discussion gives M3a far higher heuristic threshold. Do not correct this by guessing. Exact plotted variant ranks remain `UNDERDETERMINED` until original in-page figure inspection/adjudication. `SRC01` was flagged before historical A; not a new B success.

## Fidelity result and limits
- Source-described architecture, all four **distinct topology/mask types**, and Model2 C amendment are represented using unchanged Grammar v0.
- For composing original LTM, STM boosts, and ordered serial extension, **A0 at source-level topology is a candidate**: no source-mandated new stateful coordinator or extraneous stateless adapter is needed *to express this graph*. This is **not** a verified full-dynamic `A0_FIDELITY`, not universal H0 and not a claim that new coordination mechanisms never exist.
- Source-scoped full article has 20 explicitly logged developmental fidelity distinctions. Exact complete network simulation, full original Eq1–31 integration, Fig2/Fig8 numeric curves, original parameters from standalone external supplements and human data replication were **NOT** run. Figure conflict and raw historic JSON absence remain explicit.
- Developmental Python-standard-library synthetic probes: **19/19 PASS** on Eq9 source-overlap readout; Eq10–13 grain-specific masks; Eq14–21 probability/heuristic threshold; error-vs-repeat stopping; serial ordered relations; Gamma/gamma_A separation. These are logic tests of entered equations and topology, **NOT** model-behaviour validation or a scientific 19/19 fidelity score.

Full detailed Japanese-source-mapped report/20-row machine manifest/test code/run receipt exist as the exact chat ZIP `QP02_GRAMMAR_RECONSTRUCTION_DEV_20261004.zip`, SHA256 `bd06bef017780da67df024dc3c8aa952de07bb59c97aed7caadd334f7a89f0a1`. This PR intentionally commits only a metadata summary; does NOT claim the local ZIP or executable are tracked or GitHub CI-tested.

**Current study gate stays `0/4 qualified NEW pilots`, `MAIN NOT AUTHORIZED`.** Refs #399 #321, PR #401 and separately scoped prior QP01 D/E PR #403.
