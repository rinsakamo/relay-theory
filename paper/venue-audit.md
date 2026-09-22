# Paper 1 — Venue Audit

> Working venue-selection note. Non-authoritative.  
> Audit date: 2026-09-22.

## Manuscript profile

Current venue-neutral manuscript:

- approximately 2,600 words by `texcount` before references;
- 10 pages in the current compact working layout;
- no figures;
- one theorem-to-artifact table;
- formal-methodological philosophy of science;
- Lean mechanization is an audit artifact rather than the source of mathematical novelty.

## Primary candidate — Philosophy of Science

### Fit

Strong topical fit.

The paper directly engages scientific representation, model-to-target inference, evidential admissibility, individuation, and formal methodology. Several of its closest references are already central philosophy-of-science literature, including Nguyen (2017) in `Philosophy of Science`.

### Current submission constraints checked

As of the 2026-09-22 audit:

- Articles: maximum 9,000 words, excluding references.
- Discussion Notes: normally maximum 4,000 words, but are intended as focused commentary on a recent article/result and are not the natural category for the current independent manuscript.
- Abstract: maximum 100 words for Articles and Discussion Notes.
- Anonymous review required.
- Initial submission can be PDF, Word, TeX, or LaTeX.
- The journal explicitly supports LaTeX submissions.
- Accepted-manuscript house style is Chicago author-date.
- The journal allows self-archiving of a preprint under its stated publishing policy.

### Required adaptation

The current manuscript easily fits the Article word limit, but its abstract must be reduced to 100 words.

For a `Philosophy of Science` submission branch:

1. keep submission type as **Article**, not Discussion Note;
2. reduce abstract to <=100 words;
3. use 12pt, double spacing, journal margin settings, and ragged-right text for the review copy;
4. preserve anonymous author metadata;
5. switch bibliography style to the journal's Chicago requirements or template;
6. keep the Lean artifact/repository statement anonymized or separated as required by blind-review policy;
7. replace public theorem identifiers with neutral review labels;
8. include a non-identifying acknowledgement of generative-AI assistance, because current Cambridge publishing-ethics guidance requires disclosure when AI is used to generate manuscript text.

### Risk

The main risk is not length or format. It is novelty threshold.

Because target-directed inference and claims licensed about target systems are already explicit in the literature, acceptance would depend on the narrower contribution being judged sufficiently substantive: individuation-specific evidential admissibility plus mechanized anti-smuggling controls.

## Secondary candidate — European Journal for Philosophy of Science

### Fit

Very strong conceptual fit.

Recent EJPS publications include papers categorized as `General Philosophy of Science` and `Philosophy of Science in Practice`, both close to the manuscript's methodological orientation.

### Relative advantage

The manuscript's combination of formal analysis, scientific representation, and practice-sensitive individuation sits naturally within EJPS's current publication profile.

### Remaining audit need

Before converting the manuscript to an EJPS-specific submission package, re-check the current Springer submission instructions and any article-length/style limits directly from the active submission portal.

## Secondary candidate — British Journal for the Philosophy of Science

### Fit

Strong conceptual fit, especially for representation, equivalence, and formal philosophy of science.

### Current submission constraints checked

As of the audit:

- strict 24-page limit excluding title, abstract, and references but including footnotes/appendices;
- abstract <=300 words;
- Times New Roman, 12pt, 1.5 spacing, 1-inch margins for new submissions;
- triple-masked review;
- TeX submissions must include the associated PDF.

The manuscript is comfortably below the length ceiling.

### Risk

The novelty bar is very high, and the current result is explicitly methodological with elementary mathematics. This makes BJPS plausible but ambitious.

## Secondary candidate — Journal for General Philosophy of Science

### Fit

Good fit for the manuscript's methodology-of-science emphasis.

Recent JGPS publications cover representation, epistemic principles, detection, models, and general philosophy of science. This venue may fit the manuscript's methodological contribution without encouraging an inflated mathematical novelty claim.

### Remaining audit need

Confirm the current Springer author instructions and any article-type/length constraints before adaptation.

## Broad fallback — Synthese / Erkenntnis / Foundations of Science

All are plausible broad philosophy venues, but they provide a less specific topical home than the dedicated philosophy-of-science journals above.

They are best treated as later alternatives rather than the first adaptation target.

## Current order for adaptation

The present working order is:

1. **Philosophy of Science** — strongest direct topical conversation, but highest immediate novelty pressure.
2. **European Journal for Philosophy of Science** — very strong scope fit and likely natural home for the methodological framing.
3. **Journal for General Philosophy of Science** — strong general-methodology fit.
4. **British Journal for the Philosophy of Science** — excellent fit but ambitious novelty threshold.
5. **Synthese / Erkenntnis / Foundations of Science** — broad fallbacks.

This ordering is a manuscript-development heuristic, not a claim about acceptance probability.

## Next adaptation step

Do not overwrite the venue-neutral `paper/main.tex`.

Create a separate venue-specific branch/file only after selecting the first submission target. For `Philosophy of Science`, the first concrete edits are:

- 100-word abstract;
- review formatting;
- Chicago-style bibliography;
- anonymous artifact/repository wording.

The underlying theoretical claim should not be broadened to fit a venue.


### AI-tool disclosure and blind artifact labels

The current Philosophy of Science review copy uses neutral mechanized-result labels `R1`--`R15` rather than the public theorem identifiers. This reduces direct searchability into the public formal-development repository during anonymous review.

The current Cambridge publishing-ethics policy requires disclosure when an AI tool has been used to generate manuscript text. The review copy therefore contains an anonymous `Acknowledgements` section identifying OpenAI ChatGPT / GPT-5.6 Sol, the access date, and the manuscript-development tasks for which it was used. The matching non-blind cover-letter draft carries the same disclosure.

This disclosure is compatible with blind review because it does not contain author, affiliation, repository, or project identifiers.
