# System–World Coupled Recurrence: derived notation v0 (author-adopted; QP06 development)

**Architectural layer:** System–World Composition, NOT a ninth Grammar-v0 primitive. Based on #349 and author confirmation in the originating thread, tested here against QP06. Frozen Grammar v0, #398, the frozen original 60 science, and the #399 prospective v2.3.1 audit protocol remain unchanged.

## Types and temporal composition

Let X_n be the cognitive system state (which may include a belief), A_n retained output/control state where the source requires action dynamics, W_n the **World's actual state**, s_n the latest boundary sensory latch, and E_n the experiment protocol conditions (stimulus presentation schedule, vision mapping, observation horizon and external physical parameters). Here s_n is a retained interface value for making the overall update Markov; it is NOT asserted to be a ninth cognitive primitive or inherently a cognitive memory.

Use the typed *relational* composite (functions only when the source warrants determinism):

    mu_(n+1) ∈ K_mu(mu_n, s_n; q_n, C, dt)
    A_(n+1) ∈ K_A(A_n, mu_(n+1), s_n; C, dt)
    W_(n+1) ∈ D_W(W_n, Gamma_out(A_(n+1)); E_n, dt)
    s_(n+1) ∈ Gamma_in(W_(n+1); E_n)
    Z_n := (X_n, A_n, W_n, s_n)
    Z_(n+1) ∈ F_Gamma(Z_n; E_n)

This is an **explicit schedule for source-supported time-stepping**, not a universal physical micro-order. If the original source steps belief and action simultaneously, use a joint relation K_(mu,A), preserving causal dependencies rather than falsely imposing mu_(n+1) preceding action. Do NOT collapse independent World dynamics D_W into the system K, nor identify Gamma with either. T indexes succession; it is not itself K. Pi selects the modeling boundary. P_in/P_out remain system-relative, not synonymized with experimenter actions. Realized history R is an E-bounded cut through a potentially longer coupled sequence, not the origin of the cognitive system.

## Distinguishable derived motifs

- Open-loop: current system output does **not** causally change later observations through Gamma_out -> D_W -> Gamma_in; repeated observation or internal K alone is insufficient.
- Closed-loop: system output changes later World state and thereby later boundary input at the selected boundary and during the declared window.
- Adaptive feedback: closed-loop boundary observations influence a **retained** source-defined internal parameter/state that then alters later action or inference; do not infer learning from return flow alone.
- Recurrent internal K: state/feedback may recur wholly inside X without crossing the World. **Not** automatically feedback via Gamma.

Assess required edges by source-scoped ablations that distinguish (a) cutting Gamma_in return, (b) cutting the system-action effect at Gamma_out, (c) cutting an individual sensory-to-inference contribution, (d) cutting an individual sensory-to-action contribution, and (e) ablating retained adaptive state. These are separate counterfactuals and may be scientifically admissible to different extents depending on the original model.

## QP06 interpretation and caveat

Maselli, Lanillos & Pezzulo (2022), DOI 10.1371/journal.pcbi.1010095, [official original complete HTML](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010095), original 2.3–2.5 and Fig2–6, describe actual arm theta/velocity separately from internal state estimates through second-order generalized coordinates. Fig4 describes infer -> action -> actual physical dynamics -> new sensations. The target/desired attractor lives in the *internal generative model*, not the physical World. Results 3.1 demonstrate baseline reach possible with only proprioception-driven action; results 3.2 require visually informed *inference* but disable visually driven action for an uncontrollable rubber hand; results 3.3 add a virtual-hand gain and both visual/proprioceptive action contributions can oppose. The source's rasterized in-HTML exact equations have NOT been fully image-verified in this development run: all strict formula equality claims remain pending. The separate toy linear demonstrator is NOT a numerical replication of the nonlinear published model.

New derived notation is a **non-invasive architecture proposal/test result**; it does not prove new science, general minimality, universal loop necessity or any H0/H1/H2 conclusion. Do not call a post-selection known closed-loop example an independent prospective pilot.
