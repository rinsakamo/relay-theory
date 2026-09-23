# Paper 2 structural-signature v1

Owner: #142. Parent coordination owner: #130.

This contract preserves the **dissection**, not only the terminal diagnosis, for a future Paper 2 per-claim decomposition. It is reproducibility infrastructure, not RelayTheory ontology and not an authorization to change the Paper 2 basis.

## Scope and authority boundary

A record is nested as:

```text
paper
  -> claim(s)
      -> ClaimIR record(s)
          -> decomposition attempt(s)
              -> basis instantiation
              -> relation topology
              -> temporal / P-Q-Pi-C / approximation structure
              -> bridge assumptions
              -> optional readable macros
              -> witness or localized residual
```

The embedded `claim_ir` is validated by the frozen #145 `paper2-claim-ir-v1` validator. Source-facing construct labels remain in provenance and are mechanically rejected if they leak into the decomposition-attempt analysis surface.

Current `main` does **not** define a frozen empirical Paper 2 basis version. Therefore v1's compatibility table admits only `paper2-synthetic-basis-v1` for deterministic fixtures. That identifier is a synthetic sentinel, not a scientific basis freeze. A real decomposition artifact remains rejected until an independently authorized basis version is frozen and deliberately added to the compatibility table.

## Structural identity

The canonical structural digest includes:

- ClaimIR structural content under the #147 rename/order convention;
- exact basis-coordinate expansion and coordinate provenance;
- typed relation graph, including ordered arguments, conditions, grounding, and temporal direction;
- temporal assumptions;
- P/Q/Pi/C state plus provenance/fixation when present;
- deterministic/stochastic/approximate settings and declared threshold/loss/etc.;
- bridge assumptions.

Readable macro labels, local attempt/relation IDs, analyzer identity, terminal outcome, and witness packaging are not part of the structural digest. They remain fully validated and replayable in the containing artifact. Ordered relation arguments remain semantic and are never sorted away. A relation marked unordered is canonicalized as a set of arguments. ClaimIR node/relation IDs are treated as presentation tokens under the #147 comparison convention, including when referenced by basis-coordinate provenance; their structural signatures, not their local names, enter the structural digest.

## Explicit absence semantics

Fields that may be scientifically absent use an explicit state object. The admissible non-present states are:

```text
explicitly_absent
not_required
not_measured
not_recoverable
unknown
unspecified
not_applicable
```

A present value is represented as:

```json
{"state":"present","value":...}
```

These states are distinct under serialization. JSON `null` is not accepted as an ambiguous replacement on those structural fields. This does not alter ClaimIR v1, whose provenance fields may retain their already-frozen null semantics.

## Anti-vacuity preservation

P, Q, Pi, and C use explicit control records. A present control must name its provenance and assert `fixed_before_target_analysis: true`. The accepted provenance kinds are source-declared, experimental-contract, pre-frozen-generic, or synthetic-fixture. This makes the #134/#136/#138 fixation boundary auditable rather than allowing a post-hoc control to look source-grounded merely because it was serialized.

The schema does not add a new scientific primitive for P/Q/Pi/C or for uncertainty. It only preserves the declared evaluation surface used by a decomposition.

## PASS / RESIDUAL discipline

`PASS` requires a witness record containing:

- generic witness-schema identity;
- theorem/schema references;
- instantiated formal obligation;
- verification status;
- checker/version/kernel/evidence provenance.

A `RESIDUAL` requires a versioned residual kind, failure layer, unmet obligation(s), details, and any witness attempts. A single opaque `RESIDUAL` label is invalid.

Derived macros are readability only. If a macro is present, it must expand to concrete coordinate IDs, relation IDs, and a witness schema ID; that witness schema ID must resolve to a witness actually recorded on the attempt outcome. A macro cannot replace the underlying structural expansion.

## Canonicalization and replay

`scripts/paper2_structural_signature_validate.py`, backed by the small contract/replay helper modules, provides:

- strict stdlib validation and cross-reference checks;
- version-tuple compatibility enforcement;
- source-label leakage rejection;
- deterministic canonical artifact serialization;
- canonical structural SHA-256 identity;
- replay output that re-emits basis expansion, relation graph, P/Q/Pi/C state, temporal and approximation structure, bridge assumptions, macro expansion, witness provenance, outcome, and residual localization.

The replay path is intentionally strong enough to inspect the decomposition without rereading source prose. It does not claim that the source-to-ClaimIR extraction was faithful; #147 owns that separate empirical question.

## Synthetic destructive fixtures

The self-test covers P1-P5 and N1-N7 from #142, including relation-sensitive same-coordinate pairs, distinct absence states, macro-only rejection, PASS-without-witness rejection, blinding leakage, localized residuals, malformed references, ambiguous null rejection, unsupported version rejection, presentation-invariant structural identity, and preservation of semantically ordered relation arguments.

No real paper, real ClaimIR agreement result, OpenAlex enumeration, corpus decomposition, basis coverage, or residual-rate estimate is produced by this contract.

Architecture consequence: **NONE**.
