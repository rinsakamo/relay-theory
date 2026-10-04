# PF01 prospective pilot: source qualification stopped at PRE_A (2026-10-04 JST)

**Disposition:** `FAIL_CLOSED_PRE_A / SCIENTIFIC_A_NOT_STARTED / NOT_QUALIFIED`. This PR records only PF01. It changes no Grammar, frozen corpus, other pilot branches or MAIN authorization. Primary method authority: [#399](https://github.com/rinsakamo/relay-theory/issues/399), [#411](https://github.com/rinsakamo/relay-theory/pull/411) (candidate registration), [#401](https://github.com/rinsakamo/relay-theory/pull/401) (author-adopted v2.3.1 contract; exact source code not yet Git/CI deployed).

## Immutable chronology and provenance

1. **Identity/edition:** Alexander Seeholzer, Moritz Deger, Wulfram Gerstner; *PLOS Computational Biology* 15(4):e1006928, published 2019-04-19, DOI [10.1371/journal.pcbi.1006928](https://doi.org/10.1371/journal.pcbi.1006928). Official [full original HTML](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006928) physically opened in this session; original publisher printable-PDF link exists and searchable PDF excerpts exist. No specific material published correction was found on the inspected original article page or in a targeted title/DOI search; an exhaustive correction-record audit was *not* completed. Publication identity is verified; complete correction history remains a PRE_A pending field.
2. **Actual PDF access:** Publisher printable original-PDF raw bytes could not be downloaded; no truthful PDF size or raw SHA256 can be reported. An [EPFL author-institution PDF](https://lcnwww.epfl.ch/gerstner/PUBLICATIONS/Seeholzer19.pdf) opened in the web reader as a **48-page PLOS published-layout PDF** and its searchable text was accessible, but its raw bytes could not be acquired; the required rendered PDF screenshots for zero-based pages 0, 3, 5, 18 each timed out. Searchable PDF text or a PDF link does not count as a source-byte receipt or verified mathematical rendering. The institution-hosted published layout is an *additional access lead*, not silently adopted as a byte-verified publisher original.
3. **HTML fallback audit:** Publisher-designated full original HTML has visible Abstract, Author summary, Introduction, Results, Discussion, Materials and methods, in-page Figs 1-7, Table 1, Supporting information listings, Acknowledgments and References. Candidate source inventory recognizes the noisy rate-based ring model; STP facilitation/depression; a one-dimensional stochastic bump-center reduction; spiking LIF simulation; heterogeneity variants; delayed mutual-information and distractor analyses. **No PASS A source-first decomposition or mapping was performed.** Critical equations are raster images within the official HTML rather than recovered mathematical glyphs in the available page text. In particular, exact visual inspection of source-critical Eq (3)-(10), analytical projection equations and spiking/STP equations (27), (29)-(35), as well as necessary figure-panel pixels, was not achieved. We attempted the secondary published-layout PDF visual path; screenshot retrieval timed out. The official HTML is thus a *provisional fallback candidate*, not a frozen qualified primary original.
4. **Lineage:** Candidate PR #411 recorded bounded literal exact-work negative comparisons against #399 MAIN/PF preregistration, #398 MAIN40/PILOT20 and both historical 60-work rosters; this transaction rechecked the retrieved #398 issue comments and found no exact Seeholzer/Deger/Gerstner/DOI match. This inherits a *bounded* prior manifest audit, not a fresh independently re-read full pair of historical manifests. The original article explicitly traces its model through Compte et al. 2000 [11] for a spiking working-memory network, Itskov et al. 2011 [38] for facilitation/drift, Burak & Fiete 2012 [39] and Kilpatrick & Ermentrout 2012 [40] for noise-driven bump dynamics, Kilpatrick 2018 [45] for facilitation-only interference, Tsodyks et al. 1998 [49] for dynamic synapses, and same-author Seeholzer et al. 2017 [97] for continuous-attractor reduction. The reserved MEM MAIN Stocco/ACT-R seed and PF02's rule/decision composition are *not* established as central-mechanism duplicates merely by shared labels or attractor ancestry. Source-by-source exhaustive near-lineage comparison remains incomplete. This is **not** a claimed demonstration of total lineage independence.
5. **PRE_A decision:** `BLOCKED` due to decisive in-page original notation/figure pixels not directly verified. Additional not-yet-closed fields: complete correction history and complete central-ancestry comparison. Do not invent the uninspected equation glyphs from OCR, search snippets, paraphrases or related mathematical literature. The original PDF raw bytes and SHA256 are unverified. The one-primary-source freeze has **not** been executed.

## Source-specific risks recorded without treating them as A findings

The official article's Results/Discussion text identifies source-bounded approximation near a stationary network state, a large-N/low-heterogeneity perturbative reduction, a white-Gaussian approximation to spiking variability, retuning of bump shapes across plasticity parameters, low-rate instability when depression vanishes under the chosen network configuration, and finite circular-domain saturation rather than indefinitely linear diffusion. These are PRE_A *reading and negative-case audit targets only*, **not** certified A nodes, B objections or C decisions.

## Mandatory scientific gates: not executed

| Stage | State | Reason |
|---|---|---|
| PRE_A | BLOCKED, frozen receipt | math/figure visual checks and remaining edition/lineage checks are incomplete |
| A | NOT_STARTED, no scientific artifact or A hash | prohibited while PRE_A is blocked |
| B | NOT_STARTED, no B coverage ledger/hash | cannot receive nonexistent immutable A |
| C | NOT_STARTED, no C1/C2 ledger/delta/hash | cannot adjudicate nonexistent B; no fabricated closure |
| D | NOT_STARTED | no corrected source-supported A+C reconstruction |
| E | NOT_STARTED | no valid structural fidelity test; scientific fidelity **UNDERDETERMINED**, not FAILED evidence |

`A0/A1/A2` coordination discrimination: **NOT_ASSESSED**. **Do not** infer H2 from recurrent neural dynamics or equate these with system-to-World coupled recurrence.

## Receipt and actual execution

- Machine-readable frozen `PF01_PRE_A_RECEIPT_20261004.json` has companion SHA-256 sidecar `PF01_PRE_A_RECEIPT_20261004.sha256`. Receipt commit preceded the sidecar/report. Source PDF bytes are **not** in this repository.
- The new PRE_A receipt's JS SHA-256 implementation was checked against the standard `abc` vector, stage/gate fail-closed invariants were checked in the Github-write transaction, and the committed file was fetched back by its exact branch/path and compared **byte-for-byte in UTF-8 string representation** against the intended receipt; calculated SHA matched the pinned digest. These are **metadata integrity checks only**.
- The exact original v2.3.1 structural validator from #401 **was not executed** and is not represented as GitHub CI-deployed. No original numerical replication, computational fidelity probe or empirical verification was run. Generic GitHub PR provenance CI should be reported only if its run is actually observed.

## Re-entry conditions

Obtain the original published-PDF raw bytes and verify SHA-256, size, page count and decisive rendered pages **or** directly inspect all decisive original in-page mathematical/figure pixels on the publisher's complete original HTML. Complete publisher correction audit and source-local central-model lineage review, and then make a **new, timestamped, append-only PRE_A requalification receipt**. Only on an actual passing receipt may a single medium and edition be frozen and PASS A begun. Do not rewrite the original failed PRE_A receipt or retrospectively claim prospective A completion.

**Official new diverse pilot count remains 0/4. MAIN remains unauthorized.**
