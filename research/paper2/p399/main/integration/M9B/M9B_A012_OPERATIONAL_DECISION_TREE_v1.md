# M9-B — Operational A0/A1/A2 decision tree

Decision variable: **the least reconstruction-added structure required for source-faithful reconstruction**.

```text
Eligible frozen source?
 ├─ no  -> SOURCE_INELIGIBLE
 └─ yes
    Sufficient evidence?
     ├─ no  -> UNDERDETERMINED
     └─ yes
        direct with Grammar v0 + source-defined mechanisms only?
         ├─ yes -> A0_FIDELITY
         └─ no
            reconstruction-added stateless adapter sufficient?
             ├─ yes -> A1_FIDELITY
             └─ no
                reconstruction-added persistent/stateful mechanism required?
                 ├─ yes -> A2_FIDELITY
                 └─ no
                    frozen non-lift established?
                     ├─ yes -> FAILURE_LOCALIZED
                     └─ no  -> UNDERDETERMINED
```

## Guardrails

- Source-defined memory, belief state, planner state, accumulators, gating, hierarchy, recurrence, and interfaces do **not** themselves imply A1/A2.
- A1 requires a reconstruction-added, stateless, fidelity-bearing bridge.
- A2 requires a reconstruction-added, persistent/stateful, load-bearing mechanism after A1 is insufficient.
- Complexity or failure alone is not A2.
- Source ambiguity remains UNDERDETERMINED rather than being completed by invention.
- M9-A demonstrates that A1 and A2 are reachable; this decision tree does not alter MAIN40's frozen outcomes.
