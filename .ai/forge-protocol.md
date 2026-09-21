# RelayTheory forge protocol

This document is the repository-local operational authority for research transactions in RelayTheory.

Its purpose is not to decide which theory is true. Its purpose is to constrain **how claims are forged, attacked, validated, scoped, merged, and reconciled** so that implementation convenience, historical vocabulary, proof artifacts, and attractive explanations do not silently become ontology.

The current `main` branch and current repository authority always take precedence over this document's historical copies, prompts, issue text, remembered conclusions, prior SHAs, and downstream implementations.

## 1. Forge by attempted destruction

RelayTheory is forged by attempted destruction, not accumulated by addition.

Before adding a concept, primitive, field, relation, witness, decomposition, root, coordinate, or layer, first ask whether the same discriminating content can be recovered from smaller existing structure.

Prefer, in this order when applicable:

1. deletion;
2. reduction;
3. equivalence / reconstruction;
4. quotient or forgetting tests;
5. explicit counterexample search;
6. only then additional independent structure.

"Useful", "intuitive", "human-readable", "easy to implement", or "already present in RelayLM / RelaySelf" are not evidence of primitive status.

## 2. Grand Null first

Every material theory transaction must state a falsifiable Grand Null or competing account.

The Grand Null should be deliberately strong enough to fail.

For a proposed new structure, the default pressure is:

> The proposed structure is redundant; the currently retained structure already determines every distinction in scope.

For a proposed reduction, the default pressure is:

> The deleted structure carries independent discriminating information that the reduced account cannot reconstruct.

Do not weaken the null merely to make a theorem easy to prove.

## 3. Independent-information test

A candidate distinction is not independent merely because it appears as a separate field or name.

Before retaining it, test whether forgetting, reindexing, quotienting, normalizing, or reconstructing it preserves all currently claimed observables / relations within the declared scope.

Typical questions:

- Can the field be derived from the others?
- Can two presentations differ in the field while remaining intrinsically equivalent?
- Can the field be removed and reconstructed after normalization?
- Does a finite countermodel show two systems with the same reduced structure but different required behavior?
- Is the apparent distinction only unreachable / unused representation garbage?

Ontology growth requires a demonstrated information gap, not a naming gap.

## 4. Presentation is not intrinsic structure

A label, root, coordinate, decomposition, witness, representative, field, or serialization choice is not intrinsic merely because a current definition exposes it.

When possible, explicitly distinguish:

```text
presentation structure
  vs
intrinsic invariant
```

Test whether the claimed result survives:

- renaming;
- reindexing;
- change of representative;
- reachable-carrier restriction;
- quotienting irrelevant coordinates;
- equivalent encodings.

Do not promote presentation-level structure into ontology without a discriminator.

## 5. Reject structural trivialization

Reduction into a generic noun such as Relation, State, Transition, Graph, Constraint, or Process is not automatically a substantive reduction.

A lower-level account fails the anti-trivialization test if it preserves the deleted concept only through an arbitrary label such as `owns(a,b)`, `action_transition`, or another name carrying equivalent semantics.

For a specifically structural claim, require the derived distinction to survive semantics-free renaming / isomorphism except for asymmetries that are independently grounded or explicitly designated.

Any distinguished subsystem, observer, root, index, boundary, or perspective parameter must state which role it has:

- analysis-relative coordinate;
- independently grounded source;
- derived closure / invariant;
- explicitly postulated primitive.

Do not hide semantic privilege inside a generic relation.

## 6. Owner discipline

Before creating a new research owner:

1. fetch fresh `main`;
2. read current repository authority;
3. inspect open Issues and PRs;
4. search for duplicate or overlapping owners;
5. identify the smallest unresolved question.

One research question should have one current owner whenever practical.

A historical issue can be provenance without being execution authority.

If a current owner already exists, continue or reconcile it instead of creating a parallel theory lane.

## 7. Claim hierarchy

RelayTheory distinguishes claim strength.

### Level A — definition / interface / conjecture

Examples:

- a newly introduced relation;
- a candidate primitive;
- an experimental interface;
- a Grand Null;
- an unvalidated formal statement.

Level A is not evidence that the structure is necessary or intrinsic.

### Level B — earned result

A result becomes Level B only when it satisfies the **current repository-declared validation gate appropriate to the claim**.

For formal Lean results, this includes the current formal CI gate and both exact-head and merge-head validation when the transaction protocol requires them.

For empirical results, the owning Issue must state the experimental qualification and evidence requirements.

Passing CI proves only what the checked theorem / experiment establishes.

### Level C — scoped interpretation

A Level-C statement interprets Level-B evidence within an explicit scope.

It must preserve all assumptions and boundaries of the underlying result.

### Architecture consequence

**NONE unless independently earned.**

A formal or empirical theory result does not authorize RelayLM, RelaySelf, or other implementation changes merely because an architectural analogy is attractive.

## 8. Proof-shape failure is not a counterexample

Distinguish at least:

```text
proof-shape failure
scientific / mathematical counterexample
interface mismatch
tooling failure
underdetermination
```

Failure to prove a theorem in Lean does not show the theorem is false.

A counterexample requires an explicit model / witness satisfying the retained assumptions while falsifying the target conclusion.

A CI failure is not theoretical evidence unless the failure itself exposes a specified semantic contradiction.

## 9. Anti-overclaim boundary

Every material owner should state what its result does **not** establish.

In particular, do not automatically generalize a scoped result across changes such as:

- finite -> infinite / unbounded;
- deterministic -> stochastic;
- exact -> approximate / noisy;
- sequential -> tensor / monoidal / concurrent;
- fixed-probe -> adaptive / policy-dependent;
- extensional -> resource-sensitive;
- causal capability -> governance / authorization;
- abstract semantics -> embodied / physical systems.

Each extension needs an explicit bridge theorem, experiment, or new falsification owner.

Absence of a counterexample is not proof of ontology.

## 10. Implementation-independent boundary

RelayLM, RelaySelf, World adapters, benchmarks, and other systems may provide:

- evidence;
- counterexamples;
- implementation probes;
- formalization targets.

They do not define RelayTheory ontology.

Historical `rinsakamo/relay-lm:relay-theory` material is a research quarry / provenance source. It must be re-evaluated against current RelayTheory authority before migration.

Do not reverse-import implementation names as primitives.

## 11. Formalization discipline

Lean formalization is a validation instrument, not an ontology generator.

Formal transactions should prefer the smallest theorem surface that discriminates the competing claims.

Project formal source must not use, unless repository authority is explicitly changed in a dedicated transaction:

- `sorry`;
- `admit`;
- `native_decide`;
- project-local `axiom` declarations.

Also avoid:

- unnecessary `Classical.choice`;
- arbitrary canonical representatives introduced only to force a construction;
- hidden semantic assumptions packaged into helper structures;
- new quotient layers when native extensional equality is sufficient.

The CI axiom allow-list is an upper technical boundary, not evidence that every allowed axiom is theoretically justified.

## 12. Fresh-authority transaction protocol

Consequential mutation must be preceded by fresh authority.

A normal research transaction is:

1. fresh `main`, authority docs, open Issues, open PRs, and active ruleset;
2. duplicate-owner search;
3. create or identify the dedicated Issue;
4. create a research branch from the observed current `main`;
5. make the smallest change that tests the question;
6. open a draft PR;
7. run exact-head validation;
8. after all required exact-head gates are GREEN, fetch fresh authority;
9. mark the PR ready;
10. fetch fresh authority again immediately before merge;
11. squash merge using the expected PR head;
12. validate the actual merge-head on `main`;
13. post terminal reconciliation to the owning Issue;
14. fetch fresh Issue authority;
15. close with an explicit outcome when closure is earned;
16. if a parent / frontier owner exists, reverse-import the result there after fresh authority.

Do not silently substitute an old SHA, old CI run, or prompt snapshot for a fresh authority read.

## 13. Exact-head and merge-head validation

For validated transactions, distinguish:

```text
exact-head
  the exact proposed transaction head

merge-head
  the actual commit that became current main
```

A passing exact-head does not by itself certify the merged state.

When the repository declares both gates mandatory for a claim class, Level B is not earned until both have passed.

## 14. Terminal reconciliation

A completed owner should record:

- current merge-head / relevant evidence identity;
- final classification;
- what was defined;
- what was proved or falsified;
- whether the result was a counterexample or only proof/interface pressure;
- the exact scope;
- explicit anti-overclaim boundaries;
- architecture consequence;
- remaining frontier.

Terminal reconciliation is part of the theory record, not administrative decoration.

## 15. Preferred classifications

Owners may define specialized outcomes, but prefer explicit terminal classes such as:

- `REDUCTION_SURVIVES`;
- `PARTIAL_REDUCTION`;
- `GRAND_NULL_SURVIVES`;
- `COUNTEREXAMPLE`;
- `RECONSTRUCTIBLE`;
- `INDEPENDENT_STRUCTURE`;
- `RECONSTRUCTIBLE_UNDER_EXTRA_PROPERTY`;
- `UNDERDETERMINED`;
- `INTERFACE_PRESSURE`.

The name matters less than making the discriminating evidence explicit.

## 16. Reference literature registry

External scientific literature materially used by RelayTheory research must be registered in the permanent [Reference Literature Registry](https://github.com/rinsakamo/relay-theory/issues/23).

The registry is provenance infrastructure, not theory authority.

When a paper, preprint, book chapter, standard, technical report, or comparable external scientific source materially informs a research transaction:

1. search the registry for an existing entry using DOI, arXiv ID, exact title, or canonical URL;
2. if absent, add a registry entry before terminal reconciliation;
3. record stable bibliographic identity and exact version/date when relevant;
4. link the related RelayTheory Issue, hypothesis, formalization, or PR;
5. state the source's role, such as background, supporting evidence, counterexample source, competing account, formalization inspiration, or implementation/experiment precedent;
6. state the exact scoped claim or question for which the source is relevant;
7. record important assumptions, limitations, population/domain, and whether the source was read in full, partially inspected, or only discovered;
8. link the research Issue / PR back to the registry entry rather than maintaining an isolated ad hoc bibliography.

Do not duplicate an existing source entry merely because a new research owner uses it. Add the new relation / relevance to the existing registry entry.

Do not treat:

- a citation as repository authority;
- an abstract alone as equivalent to full-paper evidence;
- a secondary summary as equivalent to the primary source;
- a paper's terminology as automatic RelayTheory ontology;
- an external source as authorization to generalize beyond its studied population, assumptions, or domain.

The registry stores bibliographic metadata, stable links, and scoped relevance notes. Do not reproduce copyrighted full text there.

A transaction that materially relies on external scientific literature is not fully reconciled until the corresponding registry provenance is present.

## 17. Repository principle

> **Break the ontology before growing it. Preserve only distinctions that survive declared probes, counterexamples, formalization, and scope boundaries.**

The forge protocol itself is revisable. Changes to it require a repository-authority transaction and must not be smuggled in as ordinary theory edits.
