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

## 6. Avoid semantic smuggling

A reduction fails if it deletes a concept by simply renaming it.

Example:

If primitive Action is removed but an `interaction_kind = self_action` flag is required everywhere to preserve the same distinction, the semantics have probably been reintroduced rather than reduced.

The same test applies to Skill, Ownership, Cognition, Emotion, and similar terms.

## 7. Test across boundaries

When possible, test claims in more than one substrate or world.

A useful primitive should not depend on Minecraft-native affordance names, a particular LLM API, or one implementation's data model unless the theory explicitly claims that scope.

## 8. Promotion rule

Promote a candidate primitive only when:

1. the distinction matters;
2. lower-level candidates cannot reconstruct it without semantic smuggling;
3. competing accounts have been tested;
4. evidence provenance is explicit;
5. the scope of the primitive is stated.

## 9. Revision rule

Theory may be changed by:

- **derive** — explain a term using lower-level structure;
- **split** — replace one overloaded term with several narrower distinctions;
- **merge** — unify terms shown to encode the same structure;
- **weaken** — narrow a claim to the evidence-supported scope;
- **delete** — remove a term that adds no discriminating content.

Backward compatibility with old terminology is not a theoretical requirement.

## 10. Exit classifications

Research Issues should prefer explicit outcomes such as:

- `REDUCTION_SURVIVES`
- `PARTIAL_REDUCTION`
- `GRAND_NULL_SURVIVES`
- `UNDERDETERMINED`

A null result is useful when it closes a possible reduction.

## Principle

**Breaking the ontology is progress only when the remaining account still explains the evidence.**
