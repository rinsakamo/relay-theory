# PF04 isolated pilot — PRE_A final exception report (2026-10-04 JST)

**Verdict: PF04_PRE_A_SOURCE_MATH_UNDERDETERMINED_NOT_QUALIFIED.** The mandatory rule forbids A until every pre-A requirement passes. A/B/C/D/E **NOT STARTED**; no A0/A1/A2 or numerical-replication claim. This is **a source mathematical-specification blocker, not a demonstrated Grammar-v0 failure**.

## Source identity and primary edition lock

Dezfouli & Balleine, *Actions, Action Sequences and Habits: Evidence That Goal-Directed and Habitual Action Control Are Hierarchically Organized*, **PLOS Computational Biology 9(12): e1003364**, published 2013-12-05, DOI `10.1371/journal.pcbi.1003364`. Exact selected **publisher's complete original PDF**, never HTML fallback:
`https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1003364&type=printable`.

Actual original publisher PDF downloaded in two independent GitHub cloud executions: **377245 bytes; 14 pages; SHA-256 `bc84d4827df202cf5051cf10aa64cc09673b718af2acd31441a3712bcd376df9`**, 106265 pdftotext characters. The publisher PDF was rendered separately in the browser; equation glyphs (PDF printed pp. 12–13, eqs. 2–15), Table 1/Table 2 (p. 9), figures 1–8 (pp. 2–8) were visually examined. This is distinct access to the same canonical original URL, **not an independently demonstrated byte hash of the browser raster**. Rights-compliant actual PDF bytes were **not committed**; Git contains source URL, digests and stage receipts only.

Publisher article page offered no correction notice; cloud Crossref original-work record as retrieved 2026-10-04 showed empty `relation` and no `updated-by` or `update-to`; PubMed PMID 24339762 original XML showed zero `ErratumFor`, `ErratumIn` or `CorrectedandRepublishedIn` links. These are **bounded negative registered-correction observations**, not assurance that unregistered revision is impossible. Author-hosted reproduction of the published-layout article PDF, `https://adezfouli.github.io/materials/db-plosc-2013/db-plosc-2013.pdf`, visually repeats the same printed equation (10) and does not supply a correction. Do not substitute this mirror for frozen primary source.

## Exact-work and central-model genealogy

Checked the #399 10 unadmitted MAIN discovery seeds and separate PR #411 PF01–PF03, #398 official locked 40-comment roster `5941566993`, conditional #398 pilot20-comment roster `5942315852`, and **both** historical 60-work source manifests (designed Git blob `dd34e2048020124561477ba8fe53f1e4e1452bb7`; reviewed Git blob `597f487eef3e49aab440b24894cc5d25869b0d44` plus direct CH10 file). No exact 2013 article collision was identified within those checked lists. This is bounded roster screening, not universal literature novelty.

- **Direct hierarchical mechanism ancestor**: Dezfouli & Balleine (2012), *Habits, Action Sequences, and Reinforcement Learning*. The 2013 work adds new experimental design and model-family comparison; the idea of hierarchical action-sequence habits is not its independent new invention. The 2012 work did not collide with the checked reserved lists.
- **Flat comparator ancestor/exposure**: Daw, Niv & Dayan (2005), MB/MF control competition and arbitration, is explicitly #398 conditional pilot PD01 and historic Paper2 60 CH10. This is **shared comparator lineage**, not proof the focal 2013 hierarchical sequence mechanism duplicates it. Treat neither the 2013 flat comparator nor all reinforcement-learning vocabulary as novel.
- **Task/formal ancestors**: Daw et al. (2011) two-stage task and hybrid predecessor; Sutton–Precup–Singh options and hierarchical RL family. The original 2013 article itself discloses them. Similar procedural sequence-learning works in older corpus do not establish the same central computational model without dependency evidence.

## Mandatory qualification matrix

| Gate | Final status | Actual evidence |
|---|---|---|
| PREA01 identity/edition/date/corrections | PASS | publisher PDF/metadata, Crossref and PubMed bounded audit |
| PREA02 actual published PDF and visual audit | PASS | two cloud byte-identical runs; original PDF renders, p. 12–13 maths |
| PREA03 HTML fallback procedure | PASS (not invoked) | complete published PDF physically obtained |
| PREA04 exact single primary source/edition | PASS | publisher PDF SHA locked before any scientific A |
| PREA05 corpus and central-model lineage | PASS, caveated | checked specified rosters, 2012 direct ancestor and 2005 comparator overlap explicitly disclosed |
| PREA06 decisive original model-family definitions | **UNDERDETERMINED** | printed hierarchical **eq. (10) is not a normalized probability rule for general fitted parameter values**; original fitted-code interpretation unverified |
| PREA07 machine-readable immutable receipt | PASS | provisional PRE_A retained; append-only v2 records discovered blocker |

## Material original-source defect PF04-PREA-MATH-01

Original PDF **printed page 13, eq. (10)** gives the hierarchical first-stage choice probability, with option-dependent weighting `omega(a) = w` for a single action and `1-w` for a two-action sequence. The denominator explicitly sums over `a'` in the transition value `V^G(s,a')` and perseveration `kappa(s,a')`, but **prints `omega(a)` instead of `omega(a')`** in that denominator. This is present in the actual publisher PDF raster and visually unchanged in an author-hosted published-layout mirror; it is not just broken text extraction.

**Contradiction test**: the source model has six available first-stage options (two singleton, four sequences). As an illustrative *new algebraic probe, NOT an original experiment*, set beta=1, kappa=0, w=0.25, V^G(first singleton)=1, all five other values=0. The sum of the six as-printed alleged choice probabilities is **0.9254999009562278**, not 1. With the mathematically natural candidate edit of the denominator to `omega(a')`, the sum is 1. The exact published original fit-code behavior has **not** been verified, and neither a publisher correction nor an author confirmation was found in the accepted original. **Do not silently emend the original math**, then call it formally reconstructed or exactly replicated.

Related but separately scoped **PF04-PREA-VARIANTS-01**: original methods text says "eight simpler models" in addition to a general version, whereas the original Table 1 lists **eight actual compared variants per family** (a full combination and reduced combinations corresponding to three binary constraint toggles). The compared-set inventory can be grounded in original Table 1, but the inconsistent wording should remain disclosed.

## Immutable stage chronology and actually executed tests

1. Initial provisional original-source receipt `PRE_A.json` committed **before** decisive mathematical raster contradiction was recognized. Its PASS is **superseded before any scientific A**, never rewritten or hidden. SHA-256 `1ec2c0e10746abd974e1725fd8c696030acbf4dfe60f86b17202a833725b2514`.
2. Append-only corrected machine-readable `PRE_A_v2_source_math_blocker.json` committed separately, status **UNDERDETERMINED**. SHA-256 `7cf4e78e273bf415ca0b073323f3c881bc49edeae853fec5ed5f2b2f82c28bb4`.
3. Source-only GitHub cloud physical publisher PDF intake runs **37170144284** and **37170230487** both **SUCCESS**, with same canonical original PDF SHA, 377245 bytes and 14 pages. Second run queried source correction registries.
4. Independent PF04 **negative stop/provenance** CI run **37170498884 SUCCESS**. Validated both on-repo PRE_A versions' hashes, same source identity, seven final gate statuses, intentional `A/B/C/D/E=NOT_STARTED`, and independently recalculated the 0.9254999009562278 nonnormalization witness. This CI is **not** the original v2.3.1 scientific structural validator and no such imported/deployed claim is made.
5. All remaining A/B/C/D/E, complete reconstruction and source-grounded fidelity, model-family quantitative refitting and formal pilot approval are **NOT PERFORMED** by explicit source stop rule. Consequently no A0/A1/A2 per-family result exists.

## Exact exception route / restart policy

Resolve equation (10) against a **publisher/author correction or verified exact original model-fitting implementation**, demonstrating whether the actual first-stage denominator uses `omega(a')` and whether Table 1 correctly exhausts the modeled family variants. Retain current original PDF and its SHA unless source admission is separately reauthorized; add an append-only prospective `PRE_A_v3` with explicit evidence. Only after **all** mandatory gates PASS may source-first independent PF04 A start. Historical PRE_A v1/v2 remain immutable. No other pilot or MAIN work is authorized by this PR and the official pilot count is **unchanged**.
