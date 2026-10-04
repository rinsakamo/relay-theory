# PF01 source-frozen chronological provenance under squash-only main

**2026-10-04 JST — post-qualification repository integration control; not a new scientific A/B/C edit.**

Repository `rinsakamo/relay-theory` currently allows **squash merge only**, not merge commits or rebase merges. Squashing the 39+ chronological PF01 branch commits into one main commit would otherwise leave the original separate before-next-stage lock commits unreachable if GitHub automatically deletes the merged PR branch. File-level SHA sidecars remain valid, but they alone do not prove the actual original temporal freeze.

**Retention action performed before merge:** created dedicated long-lived provenance branch
`audit/p399-pf01-chronology-20261004`, pinned at immutable commit
`21ca1cbae4d27bb22e54cfe7816fbd11a6588cf7`.

This branch retains the full original PR chain, including the previously recorded original PRE_A failure, requalified PRE_A receipt, each original A/B/C/D/E stage artifact and separate SHA sidecar commits, post-E source review, and formal scoped-qualification decision. Do **not** move, squash, delete or force-push this audit branch. Do not treat the audit branch's existence as independent scientific confirmation. It preserves the original Git chronology for review.

Preexisting sampled chronological pin commits in earliest-to-latest order:
- PRE_A: `4203bedf35cd7d5f1d414f2f997b97731fdbe40a`
- A: `2cf93d7c7564a5156dadefb639b9c3fdf52ae207`
- B: `1850085fc913ec9f536a15f66a10f028a51f13fd`
- C: `9db4c66fdc8032981dd7890a590c1bfb356bdc54`
- D: `262fdde0febe8076e979b20885a816b2eb6709c7`

To check after the approved squash merge on main, full-history clone or GitHub Actions checkout with `fetch-depth: 0` and run:

```bash
git fetch origin '+refs/heads/audit/p399-pf01-chronology-20261004:refs/remotes/origin/audit/p399-pf01-chronology-20261004'
test "$(git rev-parse refs/remotes/origin/audit/p399-pf01-chronology-20261004)" = 21ca1cbae4d27bb22e54cfe7816fbd11a6588cf7
git merge-base --is-ancestor 4203bedf35cd7d5f1d414f2f997b97731fdbe40a 2cf93d7c7564a5156dadefb639b9c3fdf52ae207
git merge-base --is-ancestor 2cf93d7c7564a5156dadefb639b9c3fdf52ae207 1850085fc913ec9f536a15f66a10f028a51f13fd
git merge-base --is-ancestor 1850085fc913ec9f536a15f66a10f028a51f13fd 9db4c66fdc8032981dd7890a590c1bfb356bdc54
git merge-base --is-ancestor 9db4c66fdc8032981dd7890a590c1bfb356bdc54 262fdde0febe8076e979b20885a816b2eb6709c7
```

Scoped CI adjustment: `pf01-fidelity-tests.yml` additionally verifies that the remote audit ref still equals the exact expected hash, and the two PF01 workflows additionally run on `main` only when relevant PF01 files/workflows change. No original source copyrighted PDF was added to the repository; the source-first PLOS original PDF is re-fetched at CI runtime and checked against the frozen exact SHA. Any future audit-ref disappearance/movement is a provenance **STOP**, not a reason to weaken tests or relabel the stage history.

**Scientific decision remains bounded** exactly as in `PF01_FORMAL_SCIENTIFIC_QUALIFICATION_DECISION_20261004.json`; PF01 qualifies as one procedural/source-structural pilot (1/4 as then recorded), not independent numerical replication or general intermodule H0/H1/H2 discrimination. Remaining PFs in independent threads and #399 MAIN gate are unaffected.
