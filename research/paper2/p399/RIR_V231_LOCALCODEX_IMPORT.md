# #399 v2.3.1 — exact-code LocalCodex import gate

**Author adopted v2.3.1 on 2026-10-04. Protocol already documented in this branch; software import remains PENDING until byte-exact code is committed and tested.** Do not substitute an untested rewrite for the tested local artifact.

## Input archive

`P399_V231_TWO_SAFEGUARDS_ADOPTED_20261004.zip` SHA256 `02f00e721458e6a7c3d8ad0449166bebc33635f8dfcc8beb219f4038dac01c0d`.

ZIP contains the adopted protocol, C worker prompts, validator, tests, local development regression fixture and report; no publisher source full text or separate supplements. Verify archive CRC and `SHA256SUMS` before import. Exact code hashes:

- `validate_c_v231.py`: `508f4d5dd7e1fe7e79f7d95b668855352666a731ec08626b5178df426d5608b4`
- `test_validate_c_v231.py`: `e8326a99e182f81ce9f28440683e873bc40d4c5c0a966fa77ff1126712ed5ccc`
- `QP05_DERIVED_RETROSPECTIVE_V231_CHECK.json`: `101554a046449ef86dc387748698daa39e8230e9ce7b3828b9506e03a6638d38` (**retrospective** only).

## Owner transaction

1. Starting from **this existing PR #401 branch** `protocol/p399-adopt-v23-source-closed-c-20261004`, commit **exact-byte copies** of validator and tests together in `research/paper2/p399/`. Do not rewrite the committed author-adopted protocol, frozen #398 or any original QP01–05 A/B/C.
2. Add `.github/workflows/p399-v231-c-gate.yml` that runs `python -m unittest discover -s research/paper2/p399 -p 'test_validate_c_v231.py' -v` and `python -m py_compile research/paper2/p399/validate_c_v231.py` using Python 3.11; use `permissions: {contents: read}`. No downloads of source text/supplements.
3. Independently verify **committed** file hashes match above. Run real repository code tests (41/41 expected) and unchanged v2.3 baseline 28/28 plus unchanged v2.2.2 baseline 35/35 in isolated fixtures (104/104 expected); do not misstate synthetic structural tests as scientific semantic fidelity.
4. Test known QP03 B02 overpatch avoidance: original A10 already limits covariance to full model, so no fabricated reduced-form patch. Test QP04 B02 limiter coverage: the in-HTML discussion has **both** very-large-scalar requirement **and instability even after scaling**, each must be source-located and ledger-accounted when present in the evidence inventory. The validator cannot discover a source clause never entered into the inventory.
5. Read back remote code, confirm status checks, preserve actual hash genealogy. Only then report `v2.3.1 SOFTWARE INTEGRATED` and consider readying/merging PR #401. The code may be reviewed separately, but do not leave an unverified CI workflow on main.

**Adopted scientific method, still missing executable import** is distinct from scientific qualification. Former QP03/04/05 examples are development data, new 4-diverse PILOT qualification remains **0/4**, MAIN **NOT AUTHORIZED**.