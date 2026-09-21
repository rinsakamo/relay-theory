# RelayTheory repository authority

This directory defines repository-local operational authority for RelayTheory.

RelayTheory is a research repository. Its authority model exists to prevent implementation convenience, historical terminology, and handoff prose from silently becoming theory.

## Authority classes

RelayTheory distinguishes five classes:

- **theory** — current definitions, derivations, and constraints accepted by repository authority;
- **hypothesis** — falsifiable claims under investigation;
- **evidence** — observations, formal results, experiments, counterexamples, or measurements;
- **implementation** — mechanisms used to test or instantiate hypotheses; implementation structure is not theory by default;
- **history** — prior states, branches, prompts, issues, and superseded documents that do not override current authority.

## Precedence

Current repository authority takes precedence over:

- handoff prompts;
- historical branches;
- old issue text;
- remembered conclusions;
- assumptions inherited from RelayLM or RelaySelf;
- terminology retained only for implementation compatibility.

Historical material may remain valuable evidence or provenance. It is not automatically current theory.

## Cross-repository boundary

RelayLM and RelaySelf are downstream implementations and experimental subjects.

They may:

- produce evidence;
- expose counterexamples;
- motivate hypotheses;
- test formal or architectural claims.

They do not define RelayTheory ontology.

The historical `rinsakamo/relay-lm:relay-theory` lane is a research source and migration quarry, not an authority root for this repository.

## Primitive discipline

No concept is primitive merely because it is familiar or useful.

A candidate primitive must remain provisional until competing reductions have been tested. A term should be weakened, split, derived, or deleted when a smaller account preserves the required distinctions.

High-level terms such as Skill, Action, Cognition, Perception, Emotion, and Ownership must not be treated as primitives unless evidence requires independent semantics.

## Forge protocol

Research transactions are governed by [`.ai/forge-protocol.md`](forge-protocol.md).

The forge protocol defines Grand Null discipline, independent-information tests, structural anti-trivialization, duplicate-owner checks, claim levels, formal validation boundaries, anti-overclaim rules, fresh-authority gates, and terminal reconciliation. `docs/method.md` explains the research method; the forge protocol is the operational transaction authority.

## Repository workflow

Use Issues for falsifiable questions and research transactions.

Use pull requests for changes to current theory or repository authority.

A merged document records the current repository position. It does not make an empirical claim true by decree; empirical claims remain constrained by their evidence and falsification conditions.

When theory changes, prefer updating the canonical surface rather than preserving duplicate live definitions.
