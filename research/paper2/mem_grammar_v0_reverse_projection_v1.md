# MEM-only reverse projection to Unified Cognitive Structural Grammar v0

Owner: #324  
Authority: #321, merged PR #322, frozen MEM pilot #295  
Base main: `78cd63cd6ec2898f3b4783b6db394c73c0551ff4`

Only MEM01–MEM06 were processed. No papers were reread and no frozen ClaimIR, B_P2, Phi, U_claim, F_R, structural adjudication, Archetype identity, or Grammar-v0 artifact was changed.

## Coverage

| Claim | Verdict | Instantiated roles | Main pressure |
|---|---|---|---|
| MEM01.C1 | PARTIAL | Pi, X, K, T | Discussion-level P-free K fits, but the merged Lean transition field is Pin-indexed. |
| MEM02.C1 | FULL | X, C, P_out, rho/O | Direct C-conditioned probe/readout fit. |
| MEM03.C1 | PARTIAL | Q, P_in, P_out, K, T, rho/O | Frozen P_in x T -> O interaction and P_out -> O readout have no frozen X carrier. |
| MEM04.C1 | PARTIAL | Pi, X, K, T | Pi is itself a dependence/conjunction endpoint; PR #322 only supplies Config -> Part. |
| MEM05.C1 | RESIDUAL | X, P_in, K, T, rho/O | Required acquisition/retrieval condition nodes have identities beyond T; O has no frozen P_out. |
| MEM06.C1 | RESIDUAL | Q, P_out, K, T, rho/O | foil_similarity_condition has no justified v0 role; O-to-O lower-bound topology remains. |

Counts: **FULL 1 / PARTIAL 3 / RESIDUAL 2**.

Role frequency (SUPPORTED or PARTIAL): Pi 2, X 4, C 1, Q 2, P_in 2, P_out 3, K 5, T 5, rho/O 4.

## Lane result

The eight-role vocabulary remains useful, and no role is globally unused by MEM. But strict reverse projection does **not** achieve full topology-preserving coverage.

The clearest bounded counterexample is MEM06: `foil_similarity_condition` is a required frozen condition node, but it is not licensed as C, Q, T, or P. Folding it into `paired_recognition_probe` would erase a frozen node distinction. MEM05 independently retains `initial_acquisition` and `later_retrieval` as required condition nodes whose identities are not exhausted by bare temporal indices.

There is also a formal-signature mismatch between the broad Discussion-level K/rho roles and the merged Lean carrier. Frozen MEM relations include P-free K, Pi-to-X dependence, P_in x T -> O dependence, O-to-O inference, O without P_out, and P_out/O without X. These are recorded as pressure, not repaired.

## Required MEM distinctions

P_in/P_out, C/Q, Pi/X, and T/K all remain independently required. MEM06 additionally requires multiple O nodes to stay distinct. K cannot be narrowed to a deterministic function.

## Compression findings

The P split is supported. Some generic conditions can compress when the frozen topology licenses it: MEM02 qualifying-limit conditions map to C, while MEM03 retention interval maps to T. That does not license a blanket condition->C or condition->T rewrite.

The persistence compression is **not** established in MEM. MEM01/MEM03/MEM05/MEM06 have frozen persistence metadata, but none supplies a clean frozen Config-to-Config carry witness. No `K = I` or identity-like carry was inferred.

## Counterexample status

**Yes, for full direct-expressibility of Grammar v0 as frozen.** MEM05 and MEM06 leave genuine role/topology residuals. This is not a rejection of the eight-role vocabulary; it is a failure of complete, bridge-free reverse projection under the current role/signature set.

The machine-readable artifact contains exact frozen evidence references for every supported mapping and all residuals.
