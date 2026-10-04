# #399 QP06 — Feedback coupled-recurrence development test (2026-10-04)

**DEVELOPMENT ONLY; source-scoped structural evaluation, not a prospective qualified scientific pilot.**

**Source:** Maselli, Lanillos & Pezzulo (2022), *Active inference unifies intentional and conflict-resolution imperatives of motor control*, DOI `10.1371/journal.pcbi.1010095`, [canonical original PLOS complete HTML](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010095).

QP06 was chosen AFTER the author adopted a coupled feedback-recurrence notation; this is a purpose-selected feasibility/development case, not a preselected blind test. Bounded #398 issue/DOI/code-phrase search exposed no exact-work match but no complete ancestry/exposure clearance was performed. v2.3.1 source-first immutable A→B→source-closed C was **not run** for this new work; do not fabricate or imply frozen QP06 A/B/C. Detached standalone supplements are outside the author-approved official-full-HTML-only science universe. Embedded in-page original math/figure images were not independently pixel/glyph verified; exact equations are **not fully transcribed/certified**.

## Source-described mechanism mapped without a new Grammar primitive

- `X`: internal belief about arm position/velocity/acceleration (estimated generalized state up to 2nd order), its desired internal attractor, and source-defined retained action state when appropriate. Separate World `W` contains **actual** arm position/velocity, plus environment-side virtual-arm state when required.
- `K_mu` uses sensory *and* internal expected-dynamics prediction errors; `K_A` is based on proprioceptive and visual sensory-error contributions, with distinct source-defined gains. Neither action nor physical damping is a new basic cognitive role.
- Typed `Gamma_out` delivers action to World physical dynamics `D_W`; typed `Gamma_in` returns subsequent proprioceptive and visual feedback as a boundary input. Do not identify world-to-system Gamma with system-internal K. Experiment `E_exp` chooses target onset, noise and sensory mapping. `T` indexes the integration steps. The complete relationship can be written as `Z_(n+1) in F_Gamma(Z_n; E_n)` on composite state `Z=(X,A,W,s)` **without modifying Grammar v0**. See the companion derived-notation document in this PR.
- Fig4 (source section 2.5) explicitly gives belief update, action update, World physical state update, next sensory observation. The source recognizes differing physical and free-energy-gradient timescales requiring calibration; a single untyped K erases a real causal distinction.
- Main Results 3.1: reaching can also be accomplished using **only proprioception-driven action**. Results 3.2: the uncontrollable rubber hand remains visually available for **perceptual inference**, while the **vision-driven action path is disabled** (`k_A,v=0`). Results 3.3: controllable virtual arm with gain `1.3` gives action-dependent sensory conflict and possible opposing visual/proprioceptive action effects; the text states removing the visual-action contribution changes the resulting conflict handling. Never claim visual-action input is universally required across all three conditions, nor add a missing external goal to scenario 2.
- These observations are about different coupling topologies/edge activation and do not establish a separate persistent H2 coordinator. Closed-loop action–perception is also NOT equivalent to parameter learning; this original case chiefly tests recurrent action–sensory coupling.

## Bounded fidelity and local destructive demonstration

An **illustrative reduced linear** one-degree-of-freedom state-transition toy was written in standard-library Python, intentionally **not** the published nonlinear damped arm, full VFE derivatives, second-order belief update, Gaussian sensor-noise process, or original empirical/numerical simulation. Its 30 local tests PASS (**29 dynamics/typing/destructive and one scope/self-disclosure test**). The toy uses 6 s, dt=.02, target angle=.7; the published model uses 20 s and dt=.01 s. These toy numbers are **not** source data, published result values or evidence that Fig7/8/9 have been quantitatively reproduced.

Toy six-second terminal angular positions: closed loop `0.699996`; new-sensation return severed `10.967040`; no physical action `0`; virtual gain1.3 full `0.608699`; virtual gain1.3 visual-to-action off `0.777808`. These examples demonstrate that the derived notation can encode causally distinct feedback ablations. Whether the original complete equations produce matching quantitative contrasts remains untested.

**26-entry source-locator fidelity ledger:**
- 18 source-scoped mechanism/topology distinctions **SUPPORTED** at text/caption granularity;
- 2 strict inline mathematical formula confirmations **PARTIAL**;
- 3 original full numerical simulation/figure reproduction checks **PARTIAL/NOT_RUN**;
- 1 Fig4 exact raster equation-line interpretation **UNDERDETERMINED** pending actual visual glyph inspection;
- 1 human-data external validation **NOT_EVALUATED**;
- 1 formal prospective pilot qualification **NOT_ESTABLISHED**.

Full detailed Japanese report, 26-row JSON+CSV ledger, toy source, 30-test run receipt, numerical receipt and exact hashes reside ONLY in the separately supplied originating-chat ZIP `QP06_GRAMMAR_FEEDBACK_RECONSTRUCTION_DEV_20261004.zip`, independently verified ZIP SHA256 `aaaa302f75bcbd111a86340482a2999e9a88133b94532eb489ad26be98b0e688`, 8 archive members, CRC and 7 member digests PASS. This GitHub PR stores **metadata only**, not full original source text, embedded copyrighted figures, local ZIP, executable or GitHub CI runs.

**Disposition:** `DERIVED_FEEDBACK_NOTATION_STRUCTURAL_APPLICATION_PASS / COMPLETE_SOURCE_EXACT_FIDELITY_UNDETERMINED / NEW_QUALIFIED_PILOT_0_OF_4 / MAIN_NOT_AUTHORIZED`. No new Grammar primitive or proof of minimality, H0/H1/H2, or measured improvement is asserted. Historical QP01–05 development, all frozen earlier science, PR #401 prospective validator handoff and #349/#351 architecture remain unchanged.
