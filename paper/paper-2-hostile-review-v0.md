# Paper 2 — Hostile Review v0

> **Review target:** `paper/paper-2-draft-en.md` after #355 related-work integration.
> **Review mode:** adversarial manuscript review, not theory authority.
> **Allowed verdicts:** SURVIVES / PARTIAL / FAILS / UNDERDETERMINED.
> **Rule:** a favorable verdict requires support already frozen in the repository; this review does not repair research artifacts.

## Executive assessment

The manuscript contains a potentially publishable methodological and empirical contribution, but only under a narrow claim. The strongest version is not “a new formalism for cognition.” Most mathematical ingredients and neighboring system formalisms have substantial prior art. The defensible contribution is the **source-grounded, label-suppressed, predeclared structural-comparison pipeline plus the preserved failure/reconstruction sequence that yields a recurrent system-role grammar on a bounded corpus**.

The manuscript is strongest where it reports failures and limits explicitly. It is weakest where the title and grammar language can be read as broader than the 60-claim evidence supports.

Overall hostile classification:

```
PUBLISHABLE_DIRECTION_WITH_MAJOR_SCOPE_AND_METHOD_LIMITATIONS
```

No frozen scientific result is invalidated by this review, but several claims require stricter manuscript wording.

## 1. Novelty / prior-art collapse

**Attack.** Almost every component has clear predecessors: construct validity, cognitive ontologies, task ontologies, dynamical cognition, POMDPs, boundary formalisms, category-theoretic cognition, and bidirectional/open-system formalisms. If the contribution is merely “state + transition + observation + criterion + boundary,” the paper collapses into a relabeling exercise.

**Evidence.** The related-work set includes Cronbach & Meehl; Borsboom et al.; Cognitive Atlas; CogPO; Poldrack & Yarkoni; van Gelder; Kaelbling et al.; Friston/Kirchhoff; Phillips & Wilson; and St Clere Smithe. The repository also already treats generic formal components as prior art.

**Verdict: PARTIAL.**

**Why not FAILS.** The frozen result does not claim component-level mathematical novelty. The distinctive candidate contribution is the end-to-end empirical reconstruction:

[
	ext{heterogeneous source claims}
ightarrow
	ext{source-grounded ClaimIR}
ightarrow
	ext{frozen comparison}
ightarrow
	ext{preserved failure}
ightarrow
	ext{bounded subobject reconstruction}
ightarrow
	ext{hostile reverse projection}
ightarrow
	ext{residual/minimality audit}.
]

**Required manuscript defense.** State explicitly that novelty is **integration/protocol + empirical reconstruction**, not invention of the nine roles or of their mathematics. Historical firstness should remain unclaimed.

## 2. Corpus design and scale

**Attack.** Sixty claims cannot justify a general measurement basis for “cognitive capacities.” The corpus is designed rather than probability sampled, and the eight primary labels plus twelve challenge slots may encode the author's prior expectations.

**Verdict: PARTIAL.**

The design is defensible as a bounded hostile reconstruction because the 48+12 geometry and challenge pressures were frozen pre-outcome, the challenge set was non-tuning, and the paper does not report population prevalence. But the manuscript must not let “measurement basis for cognitive capacities” read as population-complete coverage.

The 1,000-work program is correctly deferred to Paper 3. Until that validation exists, all generality claims must remain corpus-relative.

## 3. Source-to-ClaimIR reliability

**Attack.** The main representation layer depends on a language-model-assisted extraction process. Historical independent local extraction calibrations produced zero valid ClaimIR, and no positive inter-rater or inter-model agreement result exists.

**Verdict: UNDERDETERMINED.**

This is the clearest empirical limitation. The current defense is auditability, not reproducibility: all 60 records were reviewed against source text and downstream transformations are deterministic. That establishes a curated reference corpus, not autonomous extraction reliability.

The manuscript correctly states this boundary. Any wording such as “reproducible extraction,” “reliable extractor,” or “validated automatic decomposition” would be unsupported.

## 4. Extraction/adjudication circularity

**Attack.** If the same project that seeks a common grammar also interprets source claims, reviews ClaimIR, adjudicates structure, and later reconstructs Archetypes, it may inadvertently normalize claims toward the desired grammar.

**Verdict: PARTIAL.**

The strongest defenses are procedural: construct labels and authority are excluded from structural comparison; ClaimIR source review is source-grounded; challenge claims are non-tuning; the original basis, Phi, structural adjudications, and Archetypes are frozen before Grammar-v0 reverse projection; reverse projection does not reread papers; residuals are preserved instead of repaired.

However, these controls do not equal independent human adjudication. The manuscript should describe this as **anti-circularity by frozen process separation**, not proof of absence of interpretive bias.

## 5. Whole-claim failure followed by Archetype success

**Attack.** The most dangerous appearance is post hoc rescue. The primary Phi atlas produced the maximally uninformative result: 1,770 of 1,770 pairs incomparable. The project then changed the unit of analysis until reusable structure appeared.

**Verdict: PARTIAL.**

This objection does not destroy the result because the manuscript preserves the failure, the diagnostic localizes why topology was never reached, and the bounded reconstruction uses an explicit forgetting operator with destructive controls. No result-dependent abstraction threshold was added, and presentation/label controls pass.

Still, bounded subobject reconstruction is **post-atlas reconstruction**. It should not be narrated as if it were the originally successful primary atlas. The paper must present the sequence as:

[
	ext{whole-claim comparison fails}
ightarrow
	ext{failure is diagnosed}
ightarrow
	ext{secondary bounded reconstruction is tested}.
]

This should be a feature of the argument, not hidden in chronology.

## 6. Basis expressivity and overfitting

**Attack.** A sufficiently expressive basis can make every source claim representable and later support almost any desired common substructure. Conversely, an over-specified Phi can make every whole claim incomparable. The project shows evidence of both risks.

**Verdict: PARTIAL.**

The universal whole-claim incomparability is direct evidence that expressivity/comparison design was a real problem. The later analysis partially answers the opposite concern through frozen forgetting semantics, non-triviality tests, competing-core pressure, cross-label recurrence, and no added post-outcome threshold.

Nevertheless, Paper 2 cannot establish that (B_{P2}) is optimally expressive. It establishes that a bounded reusable subobject structure survives a particular frozen basis and hostile controls.

## 7. Grammar-v0 role count and granularity

**Attack.** Why nine roles? Why split P into (P_{in}) and (P_{out}) but not split Q, C, O, or K further? Why reinterpret S as X? The role count may reflect modeling taste rather than empirical necessity.

**Verdict: PARTIAL.**

The strongest support is not the number nine itself. It is that each retained role has independent cross-lane witnesses, P directionality is jointly instantiated in 26 claims, K/T distinctions recur, residual adjudication produces ROLE_GAP=0, and simpler strict-preservation comparators lose frozen distinctions.

This supports **nontriviality of the current role inventory under the frozen distinction contract**, not uniqueness of granularity. The manuscript must say that alternative factorizations or equivalent role decompositions remain possible.

## 8. Comparator fairness

**Attack.** The generic-dynamics and POMDP-like competitors are defined under a “direct preservation” rule that favors explicit role-rich representations. A POMDP can augment its state; a dynamical system can encode interfaces or constraints inside state/transition structure. The comparator therefore proves only what it assumes.

**Verdict: SURVIVES, narrowly.**

The manuscript already states the correct narrow result: the tests are not non-encodability theorems. They ask which frozen distinctions remain first-class under natural forgetful projections. Formal companion maps make the forgetting explicit.

The comparator is fair only if described as a **strict distinction-preservation test**, not a capability ranking of mathematical formalisms.

## 9. System / World / experiment separation

**Attack.** “World” may merely be whatever is left outside the selected system boundary. If the boundary is chosen by the analyst, the architecture risks becoming tautological. Moreover, some embodied or extended-cognition theories dispute exactly where the cognitive boundary lies.

**Verdict: PARTIAL.**

The architecture is defensible because World is explicitly boundary-relative and is not promoted to a universal ontological primitive. Pi need not be physical, and Markov-blanket structure is treated only as a possible specialization. The experiment is also separated from the system rather than used to define cognition.

What remains underdetermined is **how a scientifically warranted system boundary is selected in each application**. Paper 2 supplies a representation architecture, not a universal boundary criterion.

## 10. Initial conditions, prehistory, and endogenous initialization

**Attack.** Treating experimental (t_0) as a run cut avoids a false system origin, but it also postpones the question of why the realized state (X_{t_0}) has the value it does. If initial-state selection matters to behavior, Grammar v0 may be incomplete.

**Verdict: UNDERDETERMINED.**

The current separation is logically clean:

[
C_{t_0}(x_{t_0})
]

constrains admissibility but does not select the realized state. Prehistory, retained structure, World coupling, and experimental preparation may all matter.

This is not evidence for a new Paper-2 primitive. It is an explicit downstream question about endogenous initialization/retention. The manuscript should keep it outside the current grammar and hand it to later dynamics/retention work.

## 11. Formalization overclaim

**Attack.** Lean formalization can create an impression that the scientific theory has been proved when only typed definitions and internal dependency theorems have been checked.

**Verdict: SURVIVES.**

The manuscript already limits the formal claim. Lean verifies the declared carrier structure, relational transition/observation, typed carry semantics, comparator maps, and associated dependency facts. It does not prove empirical adequacy, unique semantics, or cognitive truth.

This boundary must remain explicit in the abstract, methods, and discussion.

## 12. Rhetoric and title scope

**Attack.** “Toward a Concept-Neutral Measurement Basis for Cognitive Capacities” can be read as much broader than a 60-claim designed reconstruction. “Unified Cognitive Structural Grammar” can sound ontological or universal even with caveats.

**Verdict: PARTIAL.**

“Toward” helps, and the manuscript repeatedly states boundedness. Still, the abstract and conclusion should attach “bounded,” “reviewed corpus,” or equivalent qualifiers close to the strongest grammar claims.

The phrase “Unified Cognitive Structural Grammar v0” is acceptable as an internal model name only if the text consistently says that it is unified **over the frozen corpus**, not a demonstrated universal grammar of cognition.

## 13. Failure modes not yet tested

**Attack.** Several important hostile tests remain outside Paper 2: independent re-extraction, different annotators, larger-corpus prevalence, alternative basis construction, alternative forgetting operators, and prospective out-of-sample grammar recovery.

**Verdict: UNDERDETERMINED.**

These are real missing tests, not manuscript defects that can be repaired by prose. They should be listed as prospective validation rather than implied to have been solved.

## Final recommendation

The manuscript survives only in the following narrow form:

> Paper 2 presents a source-audited, concept-neutral structural reconstruction over a bounded designed corpus. Its main empirical contribution is that whole-claim comparison fails under a frozen rich projection, while bounded subobject reconstruction recovers cross-label reusable structure that compresses into a nontrivial recurrent system-role grammar. Residual and forgetful-map tests show that the grammar is useful under strict frozen-distinction preservation, without establishing a universal ontology, complete claim language, absolute minimality, or independent extraction reliability.

Recommended status:

```
MAJOR_REVISION_BEFORE_EXTERNAL_SUBMISSION
```

The major revision is primarily **scope/novelty/reliability framing**, not a demand to reopen frozen Paper-2 results.

## Required manuscript changes before hostile review v1

1. Add an explicit narrow novelty paragraph: integration/protocol + empirical reconstruction, not component mathematics.
2. Label Archetype recovery as a secondary/post-atlas reconstruction prompted by the preserved whole-claim failure.
3. State that the designed 60-claim corpus is not prevalence-representative.
4. State that Grammar-v0 role granularity is non-unique even though the current inventory is nontrivial under strict preservation.
5. State that system/World boundary selection is application-relative and not solved by Grammar v0.
6. Keep independent extraction reliability explicitly unresolved.
7. Keep comparator conclusions as first-class distinction-preservation results only.

No frozen research artifact should be changed to satisfy these manuscript requirements.
