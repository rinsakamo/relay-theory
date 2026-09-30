# PVS-16 prospective Grammar-v0 mapping v1

Status: `FROZEN_PROSPECTIVE_MAPPING`

Input: human-reviewed PVS-16 ClaimIR under unchanged Grammar v0. Evidence Profile v1 is **not joined in this artifact** and E0–E3 is not used to set mapping verdicts.

## Aggregate mapping

- FULL: 7
- PARTIAL: 4
- RESIDUAL: 5
- relation PRESERVED: 38
- relation PARTIAL: 5
- relation UNMAPPED: 9
- ROLE_GAP claims: 0

## Claim verdicts

| Claim | Verdict | Roles | Primary residual |
|---|---|---|---|
| PVS-MEM-01 | RESIDUAL | P_out, T, rho/O | SOURCE_CONTEXT_PARAMETER |
| PVS-MEM-02 | PARTIAL | Pi, K, T, rho/O | — |
| PVS-LRN-01 | RESIDUAL | X, K, T, rho/O | SOURCE_CONTEXT_PARAMETER |
| PVS-LRN-02 | PARTIAL | X, P_in, K, T, rho/O | — |
| PVS-SKL-01 | FULL | X, K, T, rho/O | — |
| PVS-SKL-02 | FULL | X, K, T | — |
| PVS-ATT-01 | FULL | X, Q, K, rho/O | — |
| PVS-ATT-02 | RESIDUAL | X, P_in, K, T, rho/O | SOURCE_CONTEXT_PARAMETER |
| PVS-PRD-01 | RESIDUAL | X, K, T, rho/O | SOURCE_CONTEXT_PARAMETER |
| PVS-PRD-02 | PARTIAL | X, K, rho/O | — |
| PVS-CTL-01 | FULL | X, Q, K, T, rho/O | — |
| PVS-CTL-02 | FULL | Q, P_in, K, T, rho/O | — |
| PVS-BLF-01 | FULL | X, K, T, rho/O | — |
| PVS-BLF-02 | FULL | X, K, T, rho/O | — |
| PVS-CNC-01 | PARTIAL | X, Q, K, T, rho/O | — |
| PVS-CNC-02 | RESIDUAL | X, P_in, K, rho/O | RELATION_LANGUAGE_GAP |

## Role frequency

- Pi: 1/16
- X: 13/16
- C: 0/16
- Q: 4/16
- P_in: 4/16
- P_out: 1/16
- K: 15/16
- T: 13/16
- rho/O: 15/16

## Interpretation

The five RESIDUAL claims do not establish a missing top-level cognitive role. Their decisive failures are source-context carriers or scientific relation/assertion semantics. This artifact therefore does not authorize Grammar-v1 repair.

Evidence-stratified interpretation is deliberately deferred to a separate post-freeze join.
