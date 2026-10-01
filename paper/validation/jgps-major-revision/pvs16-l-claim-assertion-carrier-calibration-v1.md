# PVS L_claim AssertionCarrier calibration v1

Status: `FROZEN_PVS_CALIBRATION`

This is **calibration**, not independent validation. The carrier schema was designed after observing the 14 PVS relations that required layered recovery.

## Carrier design

Frozen `ClaimIR v1 relation.arguments` remains the structural graph edge. `AssertionCarrier` adds typed `L_claim` information without rewriting that edge:

- 8 reusable predicate families;
- orthogonal qualifiers such as `EQUIVALENT`, `NEGATIVE`, `GREATER_THAN`, and `CONTRASTIVE_RATHER_THAN`;
- semantic roles for the frozen relation arguments;
- optional additional semantic references to existing ClaimIR nodes;
- optional assertion-level support provenance;
- bindings to already-existing `L_sys` and `L_ctx` placements.

## Calibration result

- observed non-strict PVS relations: 14
- carrier FULL: 14
- `ASSERTION_CARRIER_GAP`: 0
- added semantic references: 1
- relation-level support provenance cases: 1

Predicate-family counts:

- COMPARISON: 4
- DEPENDENCE: 3
- CHANGE: 2
- ASSOCIATION: 1
- DISSOCIATION: 1
- IMPLEMENTATION: 1
- EXPLANATION: 1
- OUTCOME_ASSERTION: 1

## Decisive carrier-pressure repair

`PVS-CNC-02.r2` keeps its frozen relation arguments exactly as `[category_type, feature_importance]`. The carrier adds `causal_position` as an `EXPLANANS` semantic reference because it is required by the frozen relation description. This repairs assertion-semantic precision without mutating the ClaimIR graph.

## Experimental provenance without invented P_in

`PVS-CNC-01.r3` records `EXPERIMENTAL_MANIPULATION_REPORTED` at the assertion level with `creates_p_in=false`. The source can support manipulation semantics even though the frozen ClaimIR relation contains no intervention node. No `P_in` is retrofitted.

## Boundary

14/14 closure is a calibration result only. It does not establish a complete, minimal, or uniquely correct scientific assertion language. Independent validation requires a newly frozen held-out assertion set selected after this schema freeze.

Terminal: `PVS14_ASSERTION_CARRIER_CALIBRATION_CLOSED_WITH_ONE_ADDITIVE_SEMANTIC_REFERENCE_AND_ZERO_CARRIER_GAPS`
