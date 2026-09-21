# Research method

RelayTheory is reductionist in method, not reductionist by decree.

The repository deliberately attempts to remove high-level concepts, but a concept remains independent when evidence requires it.

## 1. Start from a discriminating question

Research Issues should ask what observation would differ between competing accounts.

Bad:

> Can we make a nicer definition of Skill?

Better:

> Is there any required distinction captured by primitive Skill semantics that cannot be recovered from recurrent grounded interaction/change structure?

## 2. State the null

Every material reduction should have an explicit null or competing explanation.

The default Grand Null is:

> High-level cognitive / agency concepts require independent primitive semantics and cannot be recovered from grounded Self–World interaction and change alone.

Individual Issues should narrow this to something testable.

## 3. Prefer falsification over confirmation

Search for cases where the proposed reduction should fail.

Useful probes include:

- matched counterexamples;
- adversarial traces;
- cross-world transfer;
- ablations;
- formal countermodels;
- ambiguity tests;
- cases where provenance, authority, and grounding disagree;
- Body/Self separation cases;
- internally identical vs externally distinct histories.

A demonstration that one implementation works is not enough to establish theory.

## 4. Separate theory, evidence, and implementation

Implementation structure does not automatically become ontology.

A RelaySelf class named `Skill`, a RelayLM field named `ownership`, or a Minecraft API named `attack` is implementation vocabulary until evidence shows the corresponding semantics must be primitive.

Likewise, an implementation may use high-level shortcuts for efficiency while the theory treats them as derived macros.

## 5. Require provenance

A theoretical claim should identify where its support comes from:

- repository derivation;
- formal proof / counterexample;
- local experiment;
- RelaySelf evidence;
- RelayLM evidence;
- external scientific source;
- historical research material.

Historical prompts and old branch states are provenance, not current authority.

### External scientific literature

External scientific papers and comparable sources that materially support a RelayTheory research transaction must be registered in the permanent [Reference Literature Registry](https://github.com/rinsakamo/relay-theory/issues/23).

Research Issues / PRs should link to the relevant registry entry instead of maintaining isolated ad hoc bibliographies.

The registry should capture stable bibliographic identity, exact version/date where relevant, the related RelayTheory owner, the source's role, scoped relevance, important limitations, and read status. Deduplicate by DOI, arXiv ID, exact title, or canonical URL.

Registration records provenance, not authority. A cited paper does not automatically establish RelayTheory ontology or justify generalization beyond the source's scope. Abstract-only inspection and secondary summaries must not be presented as equivalent to full primary-source evidence.

## 6. Avoid semantic smuggling

A reduction fails if it deletes a concept by simply renaming it.

Example:

If primitive Action is removed but an `interaction_kind = self_action` flag is required everywhere to preserve the same distinction, the semantics have probably been reintroduced rather than reduced.

The same test applies to Skill, Ownership, Cognition, Emotion, and similar terms.

## 7. Reject relational trivialization

Reducing a concept to a generic noun such as Relation, State, Transition, Graph, or Constraint is not enough by itself.

A reduction is vacuous if the lower-level structure is allowed to carry an arbitrary label equivalent to the deleted concept, for example:

- `owns(a, b)`;
- `perceives(a, b)`;
- `action_transition`;
- `skill_relation`.

When a claim is specifically **structural**, require a stronger test:

> The derived distinction should be recoverable from the lower-level structure under semantics-free renaming / isomorphism, except for asymmetries that are independently grounded or explicitly designated.

If two low-level models are structurally isomorphic but the proposed derived concept classifies them differently only because names or labels changed, the reduction is incomplete.

This test does not prohibit indexical or perspective-relative parameters. It requires their role to be explicit.

For example, a distinguished subsystem parameter may be:

- an analysis-relative index;
- an independently grounded evidence source;
- a derived closure;
- or a genuine primitive designation.

The theory must say which, rather than hiding the distinction inside a generic relation label.

## 8. Test across boundaries

When possible, test claims in more than one substrate or world.

A useful primitive should not depend on Minecraft-native affordance names, a particular LLM API, or one implementation's data model unless the theory explicitly claims that scope.

## 9. Promotion rule

Promote a candidate primitive only when:

1. the distinction matters;
2. lower-level candidates cannot reconstruct it without semantic smuggling;
3. competing accounts have been tested;
4. evidence provenance is explicit;
5. the scope of the primitive is stated.

## 10. Revision rule

Theory may be changed by:

- **derive** — explain a term using lower-level structure;
- **split** — replace one overloaded term with several narrower distinctions;
- **merge** — unify terms shown to encode the same structure;
- **weaken** — narrow a claim to the evidence-supported scope;
- **delete** — remove a term that adds no discriminating content.

Backward compatibility with old terminology is not a theoretical requirement.

## 11. Exit classifications

Research Issues should prefer explicit outcomes such as:

- `REDUCTION_SURVIVES`
- `PARTIAL_REDUCTION`
- `GRAND_NULL_SURVIVES`
- `UNDERDETERMINED`

A null result is useful when it closes a possible reduction.

## 12. Operational forge protocol

The conceptual method in this document is executed under the repository-local [forge protocol](../.ai/forge-protocol.md).

The forge protocol adds transaction requirements such as Grand Null first, independent-information tests, duplicate-owner search, fresh-authority gates, claim levels, exact-head / merge-head validation for applicable claims, proof-shape versus counterexample separation, explicit anti-overclaim boundaries, and terminal reconciliation.

These operational constraints do not make a theory true. They prevent the repository from promoting claims beyond their evidence.

## Principle

**Breaking the ontology is progress only when the remaining account still explains the evidence.**
