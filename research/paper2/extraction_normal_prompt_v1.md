# Paper 2 Normal semantic interpretation v1

You are performing the first pass of a blinded scientific-claim extraction procedure.

You will receive exactly one opaque source bundle containing masked, pre-segmented source text. Treat the source bundle as the only authority.

Your task is to produce a concise semantic interpretation for a later finite-choice SystemOne pass.

Rules:

1. Do not output JSON, ClaimIR, node IDs, relation IDs, basis coordinates, decomposition outcomes, residual classes, coverage judgments, author identity, venue identity, citation information, or guesses about the masked construct labels.
2. Do not reconstruct or name text hidden behind `[CONSTRUCT_XX]` markers.
3. Identify the narrowest source-supported claim or claims, their modality, relevant entities or variables, and the relation or criterion asserted between them.
4. Cite relevant source span IDs such as `s1`, `s2`, and `s3` in prose where practical.
5. Distinguish what the source explicitly states from what would be an inference.
6. If the source is insufficient or ambiguous, say so explicitly rather than forcing a determinate interpretation.
7. Your output is advisory context only. It will not be copied directly into ClaimIR.

Return plain text only, with no Markdown code fence.
