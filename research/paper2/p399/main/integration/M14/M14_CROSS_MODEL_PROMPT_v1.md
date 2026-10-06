# M14 frozen cross-model source reconstruction prompt

You are independently reconstructing one source-grounded cognitive claim from an original scientific source.

## Inputs you may use

1. the original scientific source identified for this case;
2. this prompt;
3. `M14_CROSS_MODEL_REPLICATION_PROTOCOL_v1.json`;
4. `M14_CROSS_MODEL_BLANK_RECORD_v1.json`.

Do **not** use any retained ClaimIR, prior reconstruction, bounded-object membership, grammar verdict, capacity-case result, comparison answer, or prior model output.

## Task

Identify one focal cognitive claim that is explicit enough in the source to reconstruct structurally. Prefer a claim that states how a modeled cognitive system changes, preserves, selects, predicts, controls, learns, remembers, represents, or relates variables.

Return one record matching the blank schema.

For the focal claim:

- give a source locator sufficient for a later auditor to find the supporting passage;
- paraphrase the claim without importing terminology that is not supported by the source;
- record scope and modality;
- identify the entities or states needed by the claim;
- record typed relations or dependencies among them;
- record temporal commitments explicitly, including persistence, history dependence, ordering, delay, recurrence, or time indexing when source-supported;
- distinguish modeled cognitive-system structure from environmental coupling and experimental manipulation when the source makes the distinction relevant;
- do not invent missing structure to make the record look complete.

If the source does not support a stable reconstruction under these instructions, return `ABSTAIN` or `UNDERDETERMINED` and explain why.

## Independence rule

Complete and freeze your output before seeing any retained reference record or any other model's answer. Do not optimize for agreement with an expected answer.

## Output rule

Return only the completed JSON record. Do not add prose outside the JSON.
