# Paper 2 — JGPS Major Revision Validation Extension v1

Status: **FROZEN PRE-ANALYSIS PROTOCOL**

Authority issue: #365  
Base scientific/manuscript authority: `4adf9b105af818115bfb13b6ea4d8e7cfbf4e0d9`

Terminal target for this protocol-freeze stage:

`PAPER2_JGPS_VALIDATION_EXTENSION_V1_FROZEN`

## Purpose

This validation extension addresses the two strongest surviving objections from the fresh JGPS Major Revision review:

1. Grammar v0 may substantially inherit the structure already present in the frozen comparison basis `B_P2`.
2. The historical 60-claim reverse projection is a same-corpus adequacy result rather than independent out-of-sample validation.

The extension does **not** reopen the frozen Paper-2 core.

## Frozen boundary

The following remain immutable:

- reviewed ClaimIR;
- `B_P2`;
- `Phi`, `U_claim`, `F_R`;
- whole-claim adjudications;
- bounded Archetype/XLike identities;
- cross-lane family identities;
- frozen Grammar-v0 reverse projections;
- residual adjudications;
- comparator outputs;
- System / World / coupling / experiment formal distinctions;
- deterministic Paper-2 Result-v1 authority.

New outputs must be additive and explicitly tagged as validation-extension artifacts.

## A. Basis-to-Grammar provenance audit

Audit:

[
B_{P2}=\{S,\Pi,K,O,T,C,Q,P\}
]

against:

[
G_{cog}=\{\Pi,X,C,Q,P_{in},P_{out},K,T,\rho/O\}.
]

Allowed provenance labels:

- `INHERITED`
- `RENAMED_OR_REINTERPRETED`
- `DATA_CONSTRAINED_SPLIT`
- `NEW_TOP_LEVEL_ROLE`

The audit must identify exact frozen evidence for every non-`INHERITED` label.

The default interpretation under test is:

> Grammar v0 is a data-constrained refinement / factorization of the frozen comparison basis, not an independently discovered primitive inventory.

## B. 48-primary-only ablation reconstruction

Exclude the historical 12 challenge claims and rerun only the post-atlas reconstruction / grammar-induction logic on the 48 primary claims.

This analysis is a **challenge-set dependence / induction-set sensitivity test**.

It is **not** a held-out validation test because the historical challenge claims were already visible during the research process.

Required outputs:

- primary-only reusable structures relevant to Grammar formation;
- primary-only role inventory/support;
- any role that disappears, merges, splits, or weakens;
- explicit comparison with frozen 60-claim Grammar v0;
- preservation of all differences without rewriting frozen artifacts.

## C. Prospective validation set: PVS-16

Target:

[
16 = 8\text{ lanes}\times2\text{ new claims}.
]

Lanes:

1. Memory
2. Learning
3. Skill
4. Attention
5. Prediction
6. Control
7. Belief
8. Concept

For each lane, admit the first two previously unused eligible claims/sources under the **pre-existing frozen retrieval/sampling order**.

Admission must not depend on expected Grammar-v0 fit.

Exclude:

- original 60 claims;
- duplicate claims;
- sources or claims previously used to tune the frozen representation, comparison, reconstruction, grammar, residual taxonomy, or comparator semantics;
- candidates failing already-frozen eligibility rules.

If the repository does not provide enough frozen ordering evidence to select the next claims mechanically, stop with:

`PROSPECTIVE_SELECTION_UNDERDETERMINED`

and do not invent a new rule after candidate inspection.

### Admission lock

Before any Grammar mapping, freeze a manifest with:

- validation claim ID;
- lane;
- stable source identity;
- DOI or stable locator;
- pre-existing selection rank/provenance;
- eligibility basis;
- explicit pre-mapping status.

Hash that manifest. The manifest hash becomes PVS admission authority.

After admission, no Grammar role, residual class, comparator semantics, or admitted ClaimIR may be tuned to improve fit.

Primary prospective outputs:

- FULL / PARTIAL / RESIDUAL;
- supported roles;
- residual class;
- `ROLE_GAP` count.

All failures are retained.

## D. Independent human re-adjudication

Prepare, but do not self-certify, a blinded packet covering roughly 20–30% of the 60-claim corpus.

Include FULL, PARTIAL, and RESIDUAL cases and oversample residual cases where feasible.

Requested judgments:

- principal ClaimIR typing;
- bounded-substructure / Archetype identity judgment;
- FULL / PARTIAL / RESIDUAL;
- residual primary class.

Independence is established only when a second human completes the packet.

## Manuscript constraints already implied by the protocol

Until stronger evidence exists:

- do not present Grammar v0 as independently discovered primitives;
- use “data-constrained refinement/factorization of a declared structural comparison basis” where appropriate;
- never relabel the historical 12 challenge claims as held out;
- describe dynamical/POMDP-like comparisons as natural coarse-projection loss audits;
- mark System/World/Coupling/Experiment as downstream architectural interpretation.

## Required execution order

1. protocol freeze;
2. provenance audit;
3. 48-primary-only ablation;
4. prospective-selection resolvability check;
5. PVS manifest + hash freeze;
6. prospective reverse projection;
7. blinded human packet;
8. manuscript revision.

No manuscript rewrite may pre-empt the validation results.
