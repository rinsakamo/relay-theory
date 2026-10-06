# M12 Independent Human Re-adjudication Packet

**Status: protocol and materials only — no independent human result has been obtained.**

This packet supports two bounded validation questions.

1. **Independent downstream re-adjudication:** can a competent human who did not create the original judgment recover the same structural adjudications from the frozen source-grounded inputs?
2. **Metadata-masked sensitivity:** do downstream claim judgments remain stable when original slot, DOI, authors, venue, stratum, and historical construct labels are removed?

The second question is **not conceptual blindness**. Scientific content can itself reveal a construct. Metadata masking therefore tests lexical/metadata leakage in downstream adjudication, not whether the original human source coding was conceptually independent of construct identity.

## Blind-coding rule

During coding, do not inspect original reverse-projection files, bounded-family membership artifacts, MAIN40 architectural outcome artifacts, M9B answer tables, or any M12 reference-key files. Because the project repository is public, blindness is procedural rather than cryptographic.

## Claim module

For each HCxx case:

- select supported roles from `Pi;X;C;Q;P_in;P_out;K;T;rho/O`;
- choose `FULL`, `PARTIAL`, or `RESIDUAL`;
- adjudicate supplied candidate bounded objects A/B as `SUPPORTED`, `NOT_SUPPORTED`, or `UNDERDETERMINED`;
- record reasons/ambiguities.

## Prospective module

For each HPxx source-first packet, choose:

- `A0`, `A1`, `A2`, `UNDERDETERMINED`, or `FAILURE`;
- whether reconstruction-added load-bearing stateless mediation is required;
- whether reconstruction-added load-bearing persistent/stateful structure is required.

Do not inspect the corresponding `ARCHITECTURAL_OUTCOME` while coding.

## Reporting

The scoring script is permitted only after independent responses exist. It reports exact categorical agreement, Cohen's kappa when defined, role-wise precision/recall/F1, candidate-membership agreement, and a disagreement ledger.

No agreement statistic is a result of M12 until an actual independent human response file is supplied.


## Strict coder export

For actual coder distribution, do **not** distribute the repository case files directly. Generate the stricter blind surface with:

`python scripts/paper2_m12_export_strict_blind_packet.py --out <output-dir>`

The strict export additionally removes original normalized node-role labels, relation-kind labels, source identity locators, and explicit prospective DOI/slot/path/lane metadata. Candidate bounded objects remain visible because judging those supplied candidates is one of the coding tasks.

The strict export still does not establish conceptual blindness: scientific descriptions can themselves reveal domain identity. It also does not convert downstream re-adjudication into independent source extraction.
