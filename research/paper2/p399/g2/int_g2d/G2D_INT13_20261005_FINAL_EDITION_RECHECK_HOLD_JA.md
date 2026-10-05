# G2-D INT-13 publisher final edition — 2026-10-05 bounded independent recheck

**Decision: HOLD_FINAL_VOR; no scientific or family admission; MAIN_NOT_AUTHORIZED.** This record is appended on a separate branch based on G2-D PR #430 exact start `fff4641feeab6d29a3ede55be3989d713a9b2e79`; it does not edit any original baseline receipts, selected DOI roster, alternatives, Grammar v0, G1/G3/G4 or #398.

## Reason for check

INT-13 is Bera et al. 2026, PLOS Computational Biology, DOI [10.1371/journal.pcbi.1014796](https://doi.org/10.1371/journal.pcbi.1014796), publisher-designated publication date 2026-09-30. As recorded in G2-D, previously acquired publisher HTML (356,026 B; SHA256 `057e12d6c60605f3f5344b3411e6038397c3f823e09274c4929da9af1afaaca0`) visibly said "This is an uncorrected proof"; prior printable PDF was 31 pages, 2,581,474 B, SHA256 `5f313f8690f377faaea6b9a3610013c71b880af86634c97dbd4a5344bede9258`. A publication date and DOI alone do not resolve a proof-versus-final-edition gate.

## Executed publisher and browser verification

1. The separate local 5s-resolution-bounded direct probe could not resolve journals.plos.org or crossmark.crossref.org because the container had no functioning external DNS. That failure is an **environment failure**, not a PLOS failure or negative edition evidence.
2. Independently opened the current publisher article in the built-in web browser (2026-10-05 JST). The official complete article still states **"This is an uncorrected proof."** Publisher article: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014796 .
3. Isolated first-party GitHub Actions on 2026-10-04 15:05 UTC / 2026-10-05 00:05 JST, [run 37211673439](https://github.com/rinsakamo/relay-theory/actions/runs/37211673439), **completed success**. The probe enforces **12-second** direct HTTP per original and an **18-second** Playwright Chromium navigation timeout when the page is proof or direct media fail. Physical responses were:
   - official publisher full HTML, actual raw HTTP 200, **356,026 bytes; SHA256 `057e12d6c60605f3f5344b3411e6038397c3f823e09274c4929da9af1afaaca0`**, original title/DOI/major sections present, **explicit uncorrected proof banner**; matches old G2-D raw HTML bytes exactly;
   - official publisher printable PDF, actual raw HTTP 200, valid PDF, **31 pages; 2,581,474 bytes; SHA256 `5f313f8690f377faaea6b9a3610013c71b880af86634c97dbd4a5344bede9258`**; matches the prior G2-D uncorrected-associated PDF raw bytes **exactly**;
   - Chromium independently opened publisher article, visible body **still contains the uncorrected-proof notice**, followed the publisher-owned page PDF link and physically re-fetched the **same printable PDF raw SHA**.
4. Chromium's rendered DOM serialized to **963,304 bytes** with a different DOM-specific checksum. That is **not** a changed publisher full HTML raw file, proof of a final edition, nor contradictory evidence; the separate direct official publisher raw HTML hash exactly matches baseline.

Actual cloud source run is a provenance witness, **not a new corrected edition** or proof-to-final equivalence. Its receipt artifact is ephemeral (14 days); source metadata and exact full SHA are preserved in this branch's append-only JSON. Copyrighted full PDF bytes are not committed.

## Decision boundary and next legitimate trigger

INT-13 remains `HOLD_FINAL_VOR`; **there is no qualified corrected final original in this verification**. A later genuine publisher update requires new bounded acquisition of publisher-designated corrected full original (PDF first or full official HTML per current scope), comparison of new raw content with this proof baseline including material model-defining equations, figures, variants, and correction notices, and separately independent central-family decisions. A banner disappearing, DOI/date or Crossref metadata alone must not auto-qualify the new edition. No backup activation, no outcome inspection, no MAIN mapping, no global family promotion. PR #430 source and unresolved INT13/B4 ancestry boundaries remain unchanged.

Machine-readable exact record: `G2D_INT13_20261005_TIMED_FIRSTPARTY_AND_CHROMIUM_APPEND_ONLY_RECEIPT_v1.json`. Executable first-party probe: `int13_edition_firstparty_probe.py`. Dedicated GitHub Actions workflow: `p399-g2d-int13-firstparty-edition-witness.yml`. Draft handoff PR #434.
