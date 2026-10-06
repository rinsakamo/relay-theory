# M14 replay comparison report

## Status

Comparison was opened only after the Astra/Medium and GPT-6.1 Sol/Medium replay packages had been frozen. Both packages contain the same frozen comparison-rules object with SHA256 `eb54f84a6b4d38ea645f7d93db8b950a960776b90a6d2f2302e3dfc3e9f247b1`.

The comparison uses only the four predeclared case classes:

- `EXACT_OR_NORMALIZED_RECOVERY`
- `COMPATIBLE_ALTERNATIVE_DECOMPOSITION`
- `SUBSTANTIVE_DISAGREEMENT`
- `ABSTENTION_OR_UNDERDETERMINED`

No new fifth outcome class was introduced.

## Frozen replay inputs

Astra/Medium replay:

- package SHA256: `3b7911f2288c6a1f9ee4ab6cd033cc6eaba5c10fedf5b002170562b6ca531d04`
- original receipt SHA256: `c148424f3cc12ce0911a6e1ad02793fbb35b12857b9b4c37c1c9715f0dc5f435`
- original execution: 9 COMPLETE / 1 ABSTAIN / 0 contaminated
- postfreeze UI evidence supports the product-level label GPT-6 Astra / Medium
- exact backend snapshot and routing remain unverified

GPT-6.1 Sol/Medium replay:

- package SHA256: `b09ed20aa54c302843e069d10f9ad925ad1bf0f43b8832d96085df6bcf52dd73`
- receipt SHA256: `68446ebab712cc7b648524c528661195a18929914d7f4c903c3cffe19f2579d1`
- original execution: 10 COMPLETE / 0 ABSTAIN / 0 contaminated
- product-level label: GPT-6.1 Sol / Medium
- exact backend snapshot and routing remain unverified

## Frozen-class results

| Case | Retained slot | Astra/Medium | GPT-6.1 Sol/Medium |
|---|---|---|---|
| XM01 | ATT03 | SUBSTANTIVE | SUBSTANTIVE |
| XM02 | BLF04 | SUBSTANTIVE | SUBSTANTIVE |
| XM03 | CNC01 | ABSTENTION | SUBSTANTIVE |
| XM04 | CTL01 | SUBSTANTIVE | SUBSTANTIVE |
| XM05 | LRN03 | SUBSTANTIVE | COMPATIBLE |
| XM06 | MEM02 | COMPATIBLE | COMPATIBLE |
| XM07 | PRD05 | SUBSTANTIVE | COMPATIBLE |
| XM08 | SKL06 | SUBSTANTIVE | SUBSTANTIVE |
| XM09 | CH03 | SUBSTANTIVE | SUBSTANTIVE |
| XM10 | CH12 | SUBSTANTIVE | SUBSTANTIVE |

Aggregate:

- Astra/Medium: 0 exact, 1 compatible, 8 substantive, 1 abstention.
- GPT-6.1 Sol/Medium: 0 exact, 3 compatible, 7 substantive, 0 abstention.

These are **not** reported as a single reliability or recovery score.

## Main finding: focal-claim selection is a confound

The largest comparison effect is upstream of fine structural decomposition. The frozen v1 prompt instructed the replay model to identify *one focal cognitive claim* from each source but did not provide a claim anchor from the retained extraction. As a result, a source can support a valid replay record while the replay selects a different claim than the retained ClaimIR.

Examples:

- BLF04: both replays selected the think-aloud/process-orientation claim; the retained record centers the validity × believability factorial acceptance effect.
- CTL01: both replays selected delayed/noisy state estimation via a forward model; the retained record centers minimal intervention and selective correction.
- CH03: Astra selected the room/friend embedded-cognition example, while Sol selected the developmental historical-integrity argument; the retained record centers the general system-boundary criterion.

This matters because `SUBSTANTIVE_DISAGREEMENT` is the correct frozen class whenever the focal claim or an identity-relevant role/relation/boundary differs. It does **not** imply that the replay's independently selected claim is false.

## Post hoc descriptive check

This check is explicitly not a predeclared score.

Among the 9 cases completed by both replay configurations, the two replay records selected the same broad focal region in 8/9 cases. Eight cases used byte-identical source files in both replays (XM02 and XM04–XM10); within that stricter subset, the replay configurations selected the same focal region in 7/8 cases. XM09 is the exception.

Thus the high retained-vs-replay substantive count should not be interpreted as simple model instability. Much of it reflects a mismatch between an unanchored source-level replay task and a retained reference that had already fixed one particular claim.

## Scientific consequence

The replay succeeds as a public audit of procedure execution and reveals a specification defect in the validation target: **claim selection and claim decomposition were not isolated**. A future decomposition-reliability replay should freeze a source-grounded claim anchor (for example a locator plus a minimally identifying proposition) while withholding the retained structural decomposition. That would test reconstruction of the same claim rather than joint claim selection plus reconstruction.

The current results remain valid for the protocol actually frozen. They must not be rescored under a post hoc anchored protocol.

Independent human validation remains unperformed.

**Procedural auditability is established; inter-rater reliability remains unmeasured.**
