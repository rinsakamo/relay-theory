# M15 frozen claim-anchored source-reconstruction prompt

You are reconstructing one **pre-specified scientific claim** from an original source.

This is a decomposition-reproducibility task. The focal claim has already been fixed for you so that claim selection is not part of the measurement.

## Inputs you may use

1. the original scientific source for this case;
2. the corresponding row in `M15_CLAIM_ANCHORS_v1.json`;
3. this prompt;
4. `M15_CLAIM_ANCHORED_BLANK_RECORD_v1.json`.

Do **not** use retained RelayTheory ClaimIR, retained structural adjudication, M14 replay outputs, M14 comparison results, another M15 model's output, or any repository answer artifact.

## Target rule

Use the supplied `anchor_proposition` as the focal claim.

Do not replace it with another interesting, nearby, broader, or narrower claim from the paper.

The anchor identifies **which scientific claim** to reconstruct. It is not a structural answer key.

Every node, relation, temporal commitment, criterion, probe, and boundary you record must still be supported by the original source.

## Reconstruction task

For the anchored claim:

- read the cited source region and enough surrounding material to understand the claim;
- conservatively paraphrase the anchored claim;
- record its scope and modality;
- identify only source-supported entities, states, variables, criteria, probes, or other required components;
- record only source-supported typed dependencies or relations;
- explicitly record source-supported temporal structure such as ordering, persistence, recurrence, delay, history dependence, or time indexing;
- distinguish cognitive-system structure, environmental coupling, and experimental manipulation when relevant;
- do not insert missing structure simply to make the record complete.

If adequate full text cannot be obtained, return `ABSTAIN`.

If the supplied anchored claim cannot be stably decomposed from the available source without unsupported extrapolation, return `UNDERDETERMINED`.

Do not switch to another focal claim instead.

## Blindness rule

Before this run is frozen, do not inspect or use:

- retained structured answers;
- prior M14 v1 replay outputs;
- M14 comparison results;
- another M15 replay output;
- manuscript passages reporting replay outcomes.

Complete and freeze all ten cases for this model configuration before any retained-answer comparison.

## Output

Return only one completed JSON record matching `M15_CLAIM_ANCHORED_BLANK_RECORD_v1.json`.

The first completed scientific JSON output must be preserved as RAW before any serialization normalization.
