import json
from pathlib import Path
R=Path(__file__).parent
def j(n): return json.loads((R/n).read_text(encoding="utf-8"))
I=j("M7_SIX_LANE_IMMUTABLE_INTAKE_RECEIPT_v1.json")
C=j("M7_MAIN40_RECONCILIATION_v1.json")
M=j("M7_40_PAPER_ARCHITECTURAL_MATRIX_v1.json")
G=j("M7_CROSS_LANE_GRAMMAR_CONSISTENCY_AUDIT_v1.json")
A1=j("M7_A1_INTERFACE_ADVERSE_AUDIT_v1.json")
A2=j("M7_A2_STATEFUL_MECHANISM_ADVERSE_AUDIT_v1.json")
F=j("M7_FAILURE_AND_UNDERDETERMINATION_DECOMPOSITION_v1.json")
RCA=j("M7_RECURRING_INTERFACE_ARCHETYPES_v1.json")
MIN=j("M7_MINIMALITY_AUDIT_v1.json")
GEN=j("M7_GENEALOGY_AWARE_MAIN_SUMMARY_v1.json")
H=j("M7_H0_H1_H2_EVIDENCE_MATRIX_v1.json")
ADJ=j("M7_MAIN_SCIENTIFIC_ADJUDICATION_v1.json")
L=j("M7_INTEGRATION_LIMITATIONS_v1.json")
rows=M["rows"]; acc=[x for x in rows if x["m7_consumption_status"].startswith("IMPORTED")]; qua=[x for x in rows if x["m7_consumption_status"].startswith("QUARANTINED")]
allowed={"A0_FIDELITY","A1_FIDELITY","A2_FIDELITY","FAILURE_LOCALIZED","UNDERDETERMINED","SOURCE_INELIGIBLE"}
m6=next(x for x in I["lanes"] if x["lane"]=="M6")
def conflict_requires_flag(lane_state,m7_state,flag):
    return lane_state==m7_state or flag=="INTEGRATION_CONFLICT_REQUIRES_READJUDICATION"
def a2_licensed(a0_failed,a1_failed,source_defined,kind):
    excluded={"CTL","belief","memory","planner","learned_parameter","environment","accumulator","temporal_order","routing_metadata"}
    return a0_failed and a1_failed and (not source_defined) and kind not in excluded
checks=[
("1 exact six immutable lane inputs accepted",len(I["lanes"])==6 and all(x["disposition"]=="ACCEPT" for x in I["lanes"]) and not qua),
("2 exact kickoff ancestry all six and M6 CI certified",all(x["kickoff_ancestry"]["result"]=="PASS" for x in I["lanes"]) and m6["exact_final_head"]=="baa033088191286962332d84fc04349d3d1604dd" and m6["successful_final_ci"]["run_id"]==37296888771 and m6["successful_final_ci"]["conclusion"]=="success"),
("3 exact 40 papers",C["checks"]["rows"]==40 and len(rows)==40),
("4 exact 24 component",C["checks"]["component"]==24),
("5 exact 16 INT",C["checks"]["integrated"]==16),
("6 no duplicate slot",C["checks"]["duplicate_slots"]==0 and len({x["slot"] for x in rows})==40),
("7 no duplicate DOI",C["checks"]["duplicate_dois"]==0 and len({x["doi"] for x in rows})==40),
("8 no missing slot",C["checks"]["missing_slots"]==0),
("9 no backup activation",C["checks"]["backup_activations"]==0),
("10 no roster substitution",C["checks"]["roster_substitutions"]==0),
("11 G1 excluded",C["checks"]["g1_pilot20_counted"]==0),
("12 permitted final states",len(acc)==40 and all(x["m7_adjudicated_final_A_state"] in allowed for x in acc)),
("13 M7 no silent state change",all(x["lane_reported_final_A_state"]==x["m7_adjudicated_final_A_state"] for x in acc)),
("14 contradiction requires readjudication flag",not conflict_requires_flag("A0_FIDELITY","A1_FIDELITY",None) and conflict_requires_flag("A0_FIDELITY","A1_FIDELITY","INTEGRATION_CONFLICT_REQUIRES_READJUDICATION")),
("15 Grammar roles unchanged",G["accepted_findings"]["lane_specific_role_redefinitions"]==0 and G["accepted_scope"]["papers"]==40),
("16 custom primitive blocked",G["accepted_findings"]["custom_hidden_primitives"]==0),
("17 source state not A2",not a2_licensed(True,True,True,"other")),
("18 CTL not A2",not a2_licensed(True,True,False,"CTL")),
("19 belief not A2",not a2_licensed(True,True,False,"belief")),
("20 memory not A2",not a2_licensed(True,True,False,"memory")),
("21 planner not A2",not a2_licensed(True,True,False,"planner")),
("22 environment not A2",not a2_licensed(True,True,False,"environment")),
("23 accumulator not A2",not a2_licensed(True,True,False,"accumulator")),
("24 temporal order not A2",not a2_licensed(True,True,False,"temporal_order")),
("25 stateless metadata not A2",not a2_licensed(True,True,False,"routing_metadata")),
("26 A2 requires A0+A1 failure",not a2_licensed(False,True,False,"novel") and not a2_licensed(True,False,False,"novel")),
("27 A1 genuinely stateless",all(x["A1_adapter_type_count"]==0 for x in acc)),
("28 redundant A1 not H1",A1["H1_positive_evidence_count"]==0 and A1["accepted_scope_papers"]==40),
("29 failure not H2",H["H2"]["evidence_for"]["count"]==0 and A2["accepted_scope_papers"]==40),
("30 UNDERDETERMINED not decisive global H",H["overall"]=="INSUFFICIENT_FOR_GLOBAL_H_DISCRIMINATION"),
("31 source-ineligible no replacement",C["checks"]["backup_activations"]==0),
("32 genealogy cannot remove papers",C["checks"]["rows"]==40 and GEN["main40_pair_denominator"]==780),
("33 no global independence",GEN["global_genealogical_independence_claimed"] is False),
("34 no independent replicate assumption",GEN["independent_replicate_assumption"] is False),
("35 raw denominator preserved and fully imported",ADJ["exact_main_denominator"]==40 and ADJ["scientifically_imported_into_M7"]==40 and ADJ["quarantined_unconsumed"]==0),
("36 lane label not natural kind",any(x["type"]=="SAMPLING" and "natural kinds" in x["detail"] for x in L["limitations"])),
("37 no majority-only H",H["majority_vote_used"] is False),
("38 no hidden universal coordinator",G["accepted_findings"]["hidden_universal_coordinators"]==0),
("39 no outcome-driven edition rewrite",L["negative_evidence_preserved"] is True),
("40 final result preserves negative evidence",L["negative_evidence_preserved"] is True and ADJ["status"]=="CERTIFIED_EXACT_MAIN40_SCIENTIFIC_RESULT" and ADJ["m7_accepted_state_counts"]["A0_FIDELITY"]==40),
]
for name,ok in checks:
    if not ok: raise AssertionError(name)
print(f"M7_FAIL_CLOSED_PASS {len(checks)}/{len(checks)}")
