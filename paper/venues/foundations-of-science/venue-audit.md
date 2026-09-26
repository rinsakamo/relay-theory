# Foundations of Science venue audit — Paper 1

Audit date: 2026-09-26. Owner: #206.

## Classification

**PRESERVE — light venue-specific reframing plus a small current-literature update.**

The current official FoS guidance supports the existing framework architecture: Standard Articles may combine broad cross-disciplinary problem setting with self-contained technical/formal exposition, and there is no a priori page limit.

Official sources:
- https://link.springer.com/journal/10699/aims-and-scope
- https://link.springer.com/journal/10699/submission-guidelines
- https://support.springernature.com/en/support/solutions/articles/6000258807-preprints

Verified current requirements:
- Standard Article is the appropriate type.
- Abstract 150–250 words.
- 4–6 keywords.
- Non-anonymous title-page author information, affiliation/location, active corresponding email, ORCID when available.
- Editable source files at submission; LaTeX accepted, Springer Nature template recommended rather than mandatory.
- Statements and Declarations including competing interests; funding disclosure retained.
- Data Availability Statement for original research; this conceptual/formal paper states that no datasets were generated or analysed.
- Generative-AI use documented in a suitable section.
- Supplementary material may include specialized source formats / ZIP and should be cited as an Online Resource.
- One-paragraph third-person vitae/biography requested.
- Reviewer suggestions are welcome but optional; identity/contact information must be verifiable if supplied.
- Current instructions do not tell authors to anonymize the FoS manuscript.
- Springer Nature generally permits preprints and does not treat them as prior publication.

## Current-literature refresh

Added only where each source supports a specific contrast:
- Rizza (2025): measurement theory inside scientific enquiry → formal structure does not supply scientific warrant.
- Gomes (2025): invariant representational schemes and counterfactuals → transformation-sensitive structural legitimacy.
- Runhardt (2025): categorization under convention/constraints → consensus or labels do not determine target-grounded legitimacy.
- Sartori (2026): current DEKI/artefactualism discussion → updates representation positioning while the present audit remains downstream.

## Historical distinction

The prior Philosophy of Science submission package remains intact under `paper/venues/philosophy-of-science/` and PR #123. The FoS package does not rewrite that submission history.

## Outstanding factual metadata

The active corresponding-author email required by FoS is not established in current repository or prior Paper 1 authority. It is intentionally not inferred.


## Fresh recent-article practice check — 2026-09-26

Recent FoS research practice remains compatible with this manuscript's architecture.

- Marek Sikora, “Evolution of the Ethos of Science: From the Representationalist to the Interventionist Approach to Science,” *Foundations of Science* 30 (2025): 811–827, DOI 10.1007/s10699-024-09969-6 — broad conceptual/methodological argument crossing philosophy and scientific practice.
- Fulvio Mazzocchi, “An Investigation Into the Notion of Complex Systems,” *Foundations of Science* (2025), DOI 10.1007/s10699-025-09975-2 — framework-building treatment of a cross-disciplinary foundational concept.
- M.Z. Naser, “Causality, Explanations, Machine Learning, and Engineering,” *Foundations of Science* 30 (2025): 945–970, DOI 10.1007/s10699-025-10006-3 — broad foundational synthesis spanning philosophy, ML, and engineering.
- Thijs M. K. Latten, Martin Sand, and Pieter E. Vermaas, “From Practice To Theory: Three Types of Influence of Quantum Technology on Quantum Mechanics and its Foundations,” *Foundations of Science* 31 (2026): 345–370, DOI 10.1007/s10699-025-10003-6 — explicit practice/theory cross-domain foundational analysis.

These are venue-fit comparators, not substantive premises of Paper 1, so they are not added to the manuscript bibliography merely to signal journal familiarity.

## Artifact inspection correction

The first exact-head CI artifact built cleanly, but its ESM ZIP accidentally included the local `.lake/build` products created by the validation build. This is a packaging defect, not a Lean/formal defect. The CI is revised to zip only the five source/provenance files and to fail if generated Lean build products leak into ESM_1.zip. A separate editable manuscript-source ZIP is also produced for FoS submission requirements.
