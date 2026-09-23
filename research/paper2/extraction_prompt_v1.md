You are normalizing one bounded scientific source passage into a concept-neutral claim structure.

Input:
- one JSON object matching `paper2-extraction-source-bundle-v1`
- an opaque `bundle_id`
- one or more source spans containing only the bounded source text

Output:
- exactly one JSON object matching `paper2-extraction-candidate-v1`
- no prose before or after the JSON

Rules:
1. Use only information supported by the supplied source spans.
2. Do not infer or mention author identity, institution, venue, citation status, paper title, registry metadata, or source prestige.
3. Do not use any external theory, basis, decomposition, residual, coverage result, or other extraction output.
4. Represent the narrowest single generalizable claim that best captures the passage's main stated contribution. Prefer explicit definitional, necessary/sufficient, counterfactual, comparative, predictive, constraint, or dependency claims over background context and illustrative examples.
5. Use the fixed ClaimIR vocabulary only for structural roles and relation kinds. Do not invent new schema fields.
6. Prefer operational descriptions over repeating named constructs when an equivalent source-grounded description is possible.
7. Every node and relation must cite one or more supplied `source_span_ids`.
8. Mark `grounding="explicit"` when the source directly states the element. Use `grounding="normalized"` only when the element is a conservative restatement needed to express the same source-supported relation.
9. Do not introduce a node, relation, modality, or scope restriction merely because it would make later decomposition easier.
10. If the source is genuinely underspecified, use the least committal allowed ClaimIR value (`other` where applicable) rather than inventing missing structure.
11. Preserve relation argument order unless the source itself states a symmetric relation.
12. The candidate must contain only: `schema_version`, `bundle_id`, and `claim_core`.

Return valid UTF-8 JSON only.
