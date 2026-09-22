# Paper 1 — Hostile Review Notes

> Internal manuscript-audit note. Non-authoritative and not part of the paper.

## Current strongest claim

The manuscript should defend only the following conditional claim:

**Once a target domain, a representation-to-target map, a declared test class, and exact target-sensitive outcome semantics are fixed, representation-level multiplicity and semantically inert identity-like metadata provide no additional evidence for the operational distinctions supported by those tests.**

The paper must not claim that target ontology, metaphysical numerical identity, biological individuality, or a uniquely correct test regime has been derived.

## Major reviewer objections

### 1. "You moved identity into the target domain."

**Force:** Very high.

The model assumes a target carrier and reference map. It therefore does not eliminate identity structure.

**Current response:** Explicitly concede the point. The paper is about evidential admissibility after target semantics are fixed, not an ontology-from-observation reduction.

**Status:** Addressed in Abstract, Formal Setting, Objections, and Conclusion.

### 2. "The identity-token theorem is tautological."

**Force:** High.

The token is defined to be absent from target-sensitive semantics, so invariance is definitionally simple.

**Current response:** Present it as a negative control and dependency audit, not as deep mathematics. Its value is that the irrelevant field is explicitly represented and mechanically shown not to leak into classification.

**Status:** Addressed. Do not market the theorem itself as mathematical novelty.

### 3. "This is just observational equivalence / bisimulation / representation independence."

**Force:** Very high.

The underlying mathematical ideas are mature.

**Current response:** No novelty claim for the equivalence relation. The proposed contribution is the inference discipline governing when a formal distinction is admissible evidence for an individuation claim, plus machine-checkable anti-smuggling controls.

**Status:** Deepened on 2026-09-22. The novelty claim has been narrowed substantially after finding Suárez (2004), Contessa (2007), and especially Nguyen (2017). No novelty is now claimed for target-directed inference or for models licensing claims about targets. Remaining candidate novelty is individuation-specific evidential admissibility plus the mechanized anti-smuggling controls.

### 4. "Operational distinguishability is not individuality."

**Force:** Very high.

A test-relative equivalence class is not automatically a metaphysical individual.

**Current response:** The manuscript now speaks of when an individuation claim is evidentially supported, not of deriving individuality itself.

**Status:** Addressed. New title deliberately says "support an individuation claim."

### 5. "Target-sensitive is circular."

**Force:** Medium to high.

If target relevance is defined by the reference map, the central semantic work is outside the theorem.

**Current response:** Yes: target relevance is an explicit model assumption. The theorem tests downstream admissibility, not the epistemology of reference assignment.

**Status:** Addressed, but should be checked again during final edit.

### 6. "The positive theorem is only congruence/contraposition."

**Force:** Medium.

Outcome difference implying target difference is elementary because equal targets under a deterministic function must yield equal outputs.

**Current response:** Correct. Its role is not mathematical novelty; it verifies that the positive-control target inequality is derived from the declared discriminator rather than from presentation inequality.

**Status:** Addressed.

### 7. "Your test family is arbitrary. Why privilege it?"

**Force:** High.

The framework does not identify a uniquely correct observational or interventional regime.

**Current response:** No privileged regime is claimed. All conclusions are explicitly relative to a declared test class.

**Status:** Addressed. Avoid language suggesting absolute resolution.

### 8. "Observation and intervention are different."

**Force:** High.

Observation-only indistinguishability need not imply interventional indistinguishability.

**Current response:** The framework is parameterized by a test class and does not infer across classes.

**Status:** Addressed.

### 9. "The monotonic refinement claim fails under noise or model revision."

**Force:** Medium.

The theorem assumes exact fixed semantics and set inclusion.

**Current response:** Restrict the theorem explicitly to fixed exact semantics.

**Status:** Addressed.

### 10. "The finite model is toy-level."

**Force:** Medium.

The carrier is intentionally tiny and the proofs are elementary.

**Current response:** Treat the fixture as a fully auditable countermodel and proof-dependency audit, not as an empirical model or mathematically deep construction.

**Status:** Addressed.

## Remaining publication risks

1. **Novelty risk remains the main publication risk, but the first deeper pass is complete.** The closest identified prior art is Suárez (2004), Contessa (2007), Nguyen (2017), Chen (2018), and Nguyen, Teh, and Wells (2020). The manuscript must claim only the individuation-specific admissibility rule plus mechanized negative controls, not target-directed inference in general.
2. **Reference assignment remains exogenous.** This must stay visible throughout the manuscript.
3. **The word "individual" must remain carefully scoped.** Prefer "individuation claim," "operational distinction," and "separately resolved cases" over unrestricted individuality language.
4. **Mechanization must be sold as auditability, not theorem depth.**
5. **Application value is currently methodological.** A reviewer may ask for a non-toy worked example. Add one only if it clarifies the inference discipline without widening the ontology claim.
6. **The identity token is Boolean.** Generalizing token type would strengthen presentation but is not required for the current negative control.

## Optional strengthening before submission

A useful but nonessential Lean strengthening would parameterize the identity-like token by an arbitrary type rather than Bool. This would show that the invariance is structural rather than tied to the two-element token carrier.

Do this only if reviewers or final polishing make the Bool-specific presentation look distracting. It is not required for the current logical claim.

## Submission-readiness criterion

Paper 1 is ready for venue selection only when all of the following hold:

- English manuscript is the canonical working text.
- LaTeX compiles cleanly.
- Every mechanically attributed claim maps to an actual Lean theorem.
- Bibliography metadata is checked.
- Related Work survives a deeper novelty search.
- No sentence claims derivation of metaphysical identity or target ontology.
- Hostile review finds no unacknowledged use of presentation identity as evidence.
