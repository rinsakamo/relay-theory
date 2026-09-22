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
- LaTeX compiles cleanly. **PASS (2026-09-22):** `pdflatex -> bibtex8 -> pdflatex -> pdflatex`, 10 pages, bibliography resolved, no LaTeX warnings, overfull boxes, underfull boxes, or undefined citations in the final pass.
- Every mechanically attributed claim maps to an actual Lean theorem.
- Bibliography metadata is checked. **PASS for the current bibliography:** titles/authors/venues/pages/DOIs were cross-checked against ACM, Cambridge, Springer, Oxford Academic, ScienceDirect/authoritative institutional records, and BJPS metadata during the 2026-09-22 audit.
- Related Work survives a deeper novelty search. **PASS WITH NARROWED CLAIM:** closest prior art materially reduced the novelty surface; the remaining claim is the individuation-specific admissibility rule plus mechanized anti-smuggling controls.
- No sentence claims derivation of metaphysical identity or target ontology. **PASS in the current English/LaTeX draft.**
- Hostile review finds no unacknowledged use of presentation identity as evidence. **PASS for the current theorem-to-prose mapping; final venue-specific review still required.**


## Compiled-manuscript hostile review — 2026-09-22

The compiled 10-page manuscript was reviewed after the target-relativity worked example was added.

### Result

No new correctness blocker was found.

The strongest previously ambiguous point—what counts as `target-relevant`—is now made explicitly claim-relative. The duplicate-record example shows that the same row identifier can legitimately individuate records while failing, by itself, to individuate the persons represented by those records. The manuscript therefore does not classify labels or identifiers as intrinsically meaningless.

The current positive rule is also scoped to a **declared evidential regime**, avoiding an unrestricted claim that one universal test family determines individuality.

### Residual publication risks

1. **Incremental-novelty risk remains real.** Nguyen (2017) already places licensed claims about shared targets at the center of representation/equivalence. Chen (2018) already treats experimental individuation and presentation. The paper must continue to sell the conjunction of individuation-specific admissibility and mechanized anti-smuggling controls, not any broad representational thesis.
2. **The formal mathematics is intentionally elementary.** The paper is stronger as a formal-methodological / philosophy-of-science note than as a mathematics or theoretical-CS theorem paper.
3. **Reference assignment remains exogenous.** This is now explicit rather than hidden.
4. **The worked example is illustrative, not empirical evidence.** It improves clarity but does not broaden the theorem.
5. **Venue fit now matters more than another theoretical extension.** Further ontology or additional test regimes would likely weaken Paper 1 by widening scope.

### Current judgment

The manuscript is ready to move from theory development to **venue selection and venue-specific editorial adaptation**.

It is not yet marked publication-final because author metadata, venue template, abstract/word limits, repository/archive statement, and any venue-specific artifact requirements remain unset.


## Venue-specific blind-review audit — 2026-09-22

The Philosophy of Science adaptation now removes public Lean theorem identifiers from the reviewer-facing manuscript and replaces them with neutral labels `R1`--`R15`. The claim-to-artifact map remains readable, while direct linkage to the public development is withheld from blind review.

The manuscript also includes a non-identifying Acknowledgements section disclosing generative-AI assistance, consistent with current Cambridge publishing-ethics guidance.

### Remaining blocker

The **final anonymized review source still needs one last compile/render pass** after these venue-specific edits. Earlier review-format and venue-neutral versions compiled cleanly, but publication-final status should not be claimed until the exact anonymized source currently in the branch has been rebuilt and visually inspected.


## Exact anonymized review-copy validation — 2026-09-22

The current Philosophy of Science blind source has now passed an exact-head GitHub Actions build.

- exact head: `c46dab5a3355e74af3f61711bc5e0a7dc1fcccde`
- workflow: `Paper 1 Review CI`
- run: `#4 / 35742256009`
- job: `review-copy`
- result: **SUCCESS**
- output: **18-page PDF**

Validated gates:

- exact PR-head checkout;
- blind-source identifier audit;
- abstract <=100 words;
- neutral result labels `R1`--`R15`;
- LaTeX + standard BibTeX build;
- no final LaTeX warnings, overfull/underfull boxes, or undefined citations/references under the CI audit;
- PDF smoke checks for title, Acknowledgements, and result labels.

### Artifact policy

For initial blind review, use the anonymous artifact manifest rather than an executable copy of the public Lean development. Export a scrubbed executable package only if requested by the editor/reviewers or required by the live submission portal.

### Remaining manual gate

The exact final PDF still requires a human visual page-by-page inspection immediately before upload. This is an editorial presentation check, not a theoretical or compilation blocker.


## Exact CI artifact visual inspection — 2026-09-22

The PDF uploaded directly by the successful Paper 1 Review CI run was downloaded from GitHub Actions and inspected rather than reconstructed from a separate local source.

- workflow run: `#6 / 35742873397`
- exact head: `8a521862be76f0526422bf343f7fa2d036b26ac3`
- artifact ID: `10699848683`
- artifact: `paper-1-philosophy-of-science-review-pdf`
- PDF pages: `18`
- PDF SHA-256: `1662175011fe0f1760ab19499cde1f4cf1a86ae47ad6b0cc3e9cd22bd1061da2`

The artifact was rendered to PNG at 160 dpi and all 18 pages were inspected. No clipped text, overlaps, black squares, broken glyphs, missing section text, or reference-page layout defects were found. The R1--R15 claim-to-artifact map, Acknowledgements / AI disclosure, and both reference pages render cleanly.

This closes the manuscript build/layout gate for the current Philosophy of Science review copy. Any later textual change to the blind manuscript must rerun the same CI and visual-review cycle.
