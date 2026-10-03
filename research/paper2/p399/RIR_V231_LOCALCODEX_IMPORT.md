# #399 v2.3.1 — exact-byte import gate (cloud-first; LocalCodex optional)

**Author adopted v2.3.1 on 2026-10-04. Protocol already documented in this draft PR.** Importing the exact separately tested implementation remains PENDING until the original bytes are independently verified and committed. **The author’s local PC, WSL and LocalCodex are not required scientific or software admission gates**: an authorized cloud-only import is equally allowed. The author may use a local workflow for convenience.

This is compatible with [Paper 2 cloud-first 20+40 operations merged PR #402](https://github.com/rinsakamo/relay-theory/pull/402), which supplies a distinct generic *stage/receipt provenance* CI; it is **not** the exact v2.3.1 scientific C validator and does not qualify P399 science.

## Exact source bytes — mandatory, independent of transport

`P399_V231_TWO_SAFEGUARDS_ADOPTED_20261004.zip` SHA256
`02f00e721458e6a7c3d8ad0449166bebc33635f8dfcc8beb219f4038dac01c0d`.

The original ZIP contains the adopted protocol, C worker prompts, validator, tests, separate historical/derived regression fixture and report; no licensed full publisher source text or standalone supplements. Required member hashes:
- `validate_c_v231.py`: `508f4d5dd7e1fe7e79f7d95b668855352666a731ec08626b5178df426d5608b4`
- `test_validate_c_v231.py`: `e8326a99e182f81ce9f28440683e873bc40d4c5c0a966fa77ff1126712ed5ccc`
- `QP05_DERIVED_RETROSPECTIVE_V231_CHECK.json`: `101554a046449ef86dc387748698daa39e8230e9ce7b3828b9506e03a6638d38` (**retrospective** only)

**No accessible original archive bytes means NO SOFTWARE INTEGRATION**, even if its hashes and description are documented in Git. Never reconstruct an approximate source file from the PR summary and claim that the historical local tests apply.

## Either verified cloud transport OR optional verified local transport

1. Acquire the **actual archive bytes** through an authorized user-supplied ChatGPT upload, lawful access-controlled cloud staging accessible to the importer, or optional local copy. No system should silently search arbitrary private locations, put copyrighted originals on public GitHub, or claim inaccessible source bytes are verified.
2. Independently compute ZIP SHA256, validate ZIP CRC, verify member `SHA256SUMS`, check each exact script/test/fixture SHA above, and archive the input acquisition/provenance receipt. This byte check must occur **before** any trusted import.
3. Using GitHub connector or web UI from the cloud, or an optional local Git client, start from **this existing PR #401 branch** `protocol/p399-adopt-v23-source-closed-c-20261004`. Commit byte-for-byte validator/test files together under `research/paper2/p399/` and preserve original adopted text. If a cloud connector normalizes line endings or cannot preserve exact bytes, **fail closed** until an exact-byte method is available.
4. Add `.github/workflows/p399-v231-c-gate.yml` (Python 3.11, read-only permissions) running:
   - `python -m py_compile research/paper2/p399/validate_c_v231.py`
   - `python -m unittest discover -s research/paper2/p399 -p 'test_validate_c_v231.py' -v`
   - existing unchanged v2.3/v2.2.2 baseline regression tests against their exact historical fixtures where imported and available; never report a baseline that was not actually executed in CI.
5. Read remote files back and verify Git-tracked bytes/digests match the exact expected source hashes. Inspect actual GitHub Actions run and logs, including QP03 already-qualified-A overpatch blocker and QP04 **both** large-scalar requirement and continuing-instability limiter. Tests prove **structural bookkeeping only**, not higher scientific source-interpreting accuracy.

Until complete, record **PROTOCOL ADOPTED / SOURCE ZIP UNAVAILABLE TO CLOUD IMPORT OR IMPORT PENDING / GITHUB CI NOT RUN** as applicable, never `v2.3.1 SOFTWARE INTEGRATED`.

## Distinct scientific gates and source scope

#399 remains **publisher-designated original complete full HTML only**. Never replace it with #398's more permissive publisher/equivalent-copy source policy. Keep original old QP01–05 A/B/C and human decisions immutable; QP05 derived fixture is retrospective and cannot count as a new pilot. Four **NEW** independent predeclared, source/version/lineage-qualified, diverse v2.3.1 chains remain mandatory before any #399 MAIN use; current documented formal qualification **0/4**. #398 separately owns its MAIN40 roster, pretest20 and pre-unmask gates; passing cloud provenance CI in PR #402 cannot authorize either scientific MAIN track.
