# #399 QP01 — Grammar v0 reconstruction / fidelity developmental run (2026-10-04 JST)

**Classification:** RETROSPECTIVE_DEVELOPMENT / SCOPED_WEIGHTED_CORE_SUPPORTED / EXACT_NUMERICAL_AND_ORIGINAL_A_ALIGNMENT_UNDERDETERMINED / FORMAL_NEW_PILOT_0_OF_4 / MAIN_NOT_AUTHORIZED.

This new D/E development report does not overwrite historical QP01 A/B/C, PR #400 lineage authority, prospective v2.3.1 (PR #401), original Grammar v0, or frozen #398. Prior QP01 outcomes were visible to the analyst. It is neither blinded nor a prospectively qualified new pilot.

## Reference authority
- Original full publisher HTML: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010796 (Ashinoff et al., 2022).
- Historic scoped A/B/C receipt: https://github.com/rinsakamo/relay-theory/issues/399#issuecomment-5967000829
  - A SHA256 `646d2c5693fae6126400999ab63215763988fd2591e1afb0bcf200f971e07305` (16 initial items, 11 edges)
  - B SHA256 `de56d78fe5fafb9911451150933d9e96e7dea34c70e2dffdb1a57dc212b961ab`
  - C SHA256 `e268ba17349106adb6a328d721835438be5c4da005fb1a70a19c1cddef190200` (A17/E12 additions and E05 scope qualifier as author accepted)
- Original full A/B/C *JSON* bytes were not available via this GitHub reading surface; exact per-ID exhaustive D/E replay is **not verified**. Historic metadata/digests plus original public source were used for an explicitly separate source-scoped D/E artifact.
- Author-ratified source regime: publisher original full HTML only. Unembedded standalone supplements outside the source universe; their unseen formulas/variant details are not certified. Some in-HTML math remains image-rendered and has not been freshly independently checked symbol-for-symbol.

## Explicit source-level reconstruction
The source-visible weighted Bayesian focal recursive model has logit internal belief `x_d`, signed bead log-likelihood-ratio `e_d(l)`, prior weight `w1`, and **bead-ratio-condition indexed fixed model parameter** `w2(l)`. Each draw:
```
x_d = w1*x_(d-1) + w2(l)*e_d(l)
x_n = w1^n*x_0 + w2(l)*SUM(i=1..n) w1^(n-i)*e_i(l)
delta_d = (w1-1)*x_(d-1) + w2(l)*e_d(l)
```
For `0 <= w1 < 1`, older evidence decays geometrically; the model jointly predicts recency and prior-dependent belief updates. For **fixed concordant evidence and parameters only**, `x_limit = w2*e/(1-w1)` gives reduced reachable confidence ceiling. This preserves the old C A17/E12 scope and does not universalize the ceiling. Fig 2's comparator `w1=1` retains its caption-specified likelihood weight; do not secretly substitute `w2=1` during like-for-like ablation. `w2(l)` is a **condition-indexed fitted parameter**, not online `K` learning (old C E05 qualifier).

The nested noisy-sampling account distinguishes noisy prior and likelihood logit representations, their respective encoding-noise variances `sigma^2_prior` / `sigma^2_l(l)`, and separate assumed underlying-logit variances `omega^2_prior` / `omega^2_l(l)`. Source-math/author-accepted historical mapping supports `gamma=omega^2/(omega^2+sigma^2)` and an additional approximation correction `rho_source`, yielding effective relative weights `gamma/rho_source`. **Exact image-embedded integral/nonlinear correction is not newly independently reproduced**, so the noisy account is assessed as structural/topological reconstruction with an exact-math gap. `rho_source` is not Grammar observation `rho_grammar`.

## Grammar-v0 reconstruction
- `Pi`: separate cognitive belief system vs World and researcher model-comparison space; no invented neural modules.
- `X`: internal log-odds beliefs; the noisy account refines represented prior/likelihood and posterior uncertainty.
- `C`: internal representation noise/cost-of-precision assumptions and model admissibility. Study exclusion and fit bounds are `L_ctx`, **not intrinsic C**.
- `Q`: theory-level precision/resource versus prediction-inaccuracy criterion; not a proven subject reward component.
- `K`: actual weighted belief update and noisy conditional inference, distinct from World coupling `Gamma`.
- `T`: draw-index succession 0→8 and nine reports; not assumed wall-clock continuous time.
- `P / rho_grammar / O`: input interface and belief-to-reported-probability readout. Experimenter stimulus ordering stays outside participant `K`.
- `World / Gamma / E_exp`: true hidden-box process, presented beads and experimental manipulation. RMSE/BIC estimation/selection are *analyst-side in context/claim layers*, not participant cognition.

Topology: `World evidence --Gamma_in--> represented evidence`; `(X_prior, represented evidence, constraints) --K--> X_post` along `T`; `X_post --rho_grammar/P_out--> O_report`. The paper contains nested competing/explanatory models, not an empirically source-established controller coordinating separate cognitive components.

## Faithfulness ledger
14 explicit source-critical distinctions assessed in the exact local manifest:
- Scoped supported F01–F06: experimental boundary/temporal order, exact visible weighted recursion, condition-indexed weight, age-discount, the dual dynamics with a conditional bounded confidence ceiling, comparator-preserving weights.
- Scoped supported topology/context F07–F08 and F10–F12: separate encoding/underlying variances, functional normative premise, analyst-side fit parameter split, late *recovery simulation* noise confined to reports (not internal state).
- **PARTIAL F09**: source-derived `gamma/rho_source` topology is grounded, but exact embedded formula independently unchecked.
- **SCOPE_LIMIT F13–F14**: full ten fitting-variant parameter grids and the fully specified external volatility competitor cannot be claimed from readable HTML alone; no external supplement inspected or certified.

**Verdict:** `SOURCE_SCOPED_WEIGHTED_FORMAL_CORE_RECONSTRUCTED`; `NOISY_ACCOUNT_TOPOLOGY_RECONSTRUCTED_EXACT_NUMERICAL_FIDELITY_UNDETERMINED`; `FULL_MODEL_VARIANTS_NOT_CLAIMED`. A single numerical all-model fidelity percentage would be misleading. No independent fit-to-participant-data replication was performed.

## Executed mathematical destructive probes
A locally runnable Python stdlib fixture tested 12/12 PASS: closed-form versus eight-step recursion, recency under ordered reversal, removal of asymmetry on `w1=1` ablation, prior-consistent/inconsistent conditional update differences, fixed-evidence confidence limit and ablation, condition-indexed `w2` not learned in-loop, evidence-erasure when `w2=0`, recovery-only late-report-noise not propagating to beliefs, noise-dependent Gaussian shrinkage `gamma`, and logistic readout order. For **illustrative not participant-fitted** Fig-2 parameter choice `w1=.88, w2(60:40)=.51`, matching five-positive/three-negative mirror sequences gave front logit 0.005703 versus back 0.524155; on `w1=1` with `w2=.51`, both 0.413574. These verify encoded consequences only, not original code/data empirical replication.

Content-addressed full chat-local development ZIP `QP01_GRAMMAR_RECONSTRUCTION_DEV_20261004.zip`, SHA256 `bde26d1ea60dea10074d01b914c501174f859840331491c5a3875284b119af47`, contains the detailed 14-distinction Japanese/English scope-aware report, machine-readable manifest, exact executed Python probe script, and per-member SHA256SUMS. The full ZIP is **not imported into this branch and should not be presented as a Git-tracked executable**. A follow-up exact-byte review/import is needed if repository CI is desired.

## Scientific and coordination boundary
The focal BLF component model needs **no fabricated extra coordinator** in this scoped direct typed reconstruction. This is *not* a corpus-level H0 victory: A1/A2 cross-component and H1/H2 classifications are **NOT APPLICABLE / NOT EARNED** for this single component study. A reduced `{X,K,T}` notation can rewrite the arithmetic, but deleting typed `C` loses the original variance-source distinction, deleting `rho/O` erases report-only vs inferential noise, and merging `Gamma` with `K` conflates external input with cognitive update; these are local typed-erasure witnesses, **not universal minimality proofs**.

**Open precise gates:** exact original A/B/C JSON replay; re-inspect decisive in-HTML image equations for exact nonlinear noisy math; external variants not certified; independent data-fitting if requested; source-qualified *four new, diverse prospective* v2.3.1 A/B/C papers and independent MAIN freeze. **QP01 remains retrospective, 0/4 formal scientific pilot, MAIN NO-GO.**
