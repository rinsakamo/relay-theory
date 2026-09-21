# RelayTheory formal verification

This directory is the isolated Lean 4 formalization surface for the independent
`rinsakamo/relay-theory` repository.

It is validation infrastructure, not an ontology source.

Historical Lean modules from `rinsakamo/relay-lm:relay-theory` are provenance /
quarry material. They must be reviewed and re-forged against current
RelayTheory authority before being added here.

## Current gate

The repository Lean workflow:

1. checks out the exact transaction head;
2. installs the pinned Lean toolchain;
3. rejects banned proof shortcuts in project `.lean` source;
4. runs `lake build`;
5. independently kernel-checks the compiled `RelayTheory` module with
   `leanchecker`;
6. runs pinned `leanprover-community/axiom-audit`.

The current source gate rejects:

- `sorry`;
- `admit`;
- `native_decide`;
- project-local `axiom` declarations.

The axiom-audit allow-list is a technical ceiling, not a claim that use of every
allowed standard axiom is theoretically justified.

## Adding formal results

A formal result should enter this project only from a dedicated falsifiable
owner. Keep assumptions explicit, prefer countermodels and reconstruction tests,
and retain the scope of the theorem in any Level-C interpretation.

See [the forge protocol](../../.ai/forge-protocol.md).
