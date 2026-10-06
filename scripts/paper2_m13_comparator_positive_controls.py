#!/usr/bin/env python3
from __future__ import annotations
import copy, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import paper2_phi_compare as phi

fixture=json.loads((ROOT/"research/paper2/structural_signature_v1.example.json").read_text(encoding="utf-8"))
fixture["contract_versions"]["basis"]=phi.WORKING_BASIS_VERSION
phi.validate_structural_signature(fixture)
base=phi.project_first(fixture)

renamed=phi._rename_presentation(fixture)
phi.validate_structural_signature(renamed)
pc1=phi.compare_phi(base,phi.project_first(renamed))
assert pc1["relation"]=="EQUIVALENT", pc1

meta=copy.deepcopy(fixture)
meta["paper"]["paper_id"]="example:paper:presentation-variant"
meta["paper"]["source_identity"]["stable_id"]="example:paper:presentation-variant"
ir=meta["paper"]["claims"][0]["claim_ir_records"][0]["claim_ir"]
ir["provenance"]["paper_id"]="example:paper:presentation-variant"
ir["provenance"]["authors"]=["Presentation Variant Author"]
ir["provenance"]["institutions"]=["Presentation Variant Institution"]
ir["provenance"]["venue"]="Presentation Variant Venue"
ir["provenance"]["citation_count"]=17
phi.validate_structural_signature(meta)
pc2=phi.compare_phi(base,phi.project_first(meta))
assert pc2["relation"]=="EQUIVALENT", pc2

refined=copy.deepcopy(fixture)
a=refined["paper"]["claims"][0]["claim_ir_records"][0]["decomposition_attempts"][0]
a["control_surface"]["resource_C"]={
    "state":"present",
    "value":{
        "identity":"fixture:resource:m13-fixed",
        "description":"predeclared M13 synthetic resource distinction",
        "provenance":{"kind":"synthetic_fixture","source_refs":["fixture:resource:m13-fixed"],"fixed_before_target_analysis":True},
    },
}
phi.validate_structural_signature(refined)
pc3=phi.compare_phi(base,phi.project_first(refined))
assert pc3["relation"]=="RIGHT_STRICT_REFINEMENT_OF_LEFT", pc3
w=pc3["forgetting_map_right_to_left"]
assert "C" in w["forgotten_axes"]
assert "resource_C" in w["forgotten_controls"]

expected=json.loads((ROOT/"research/paper2/p399/main/integration/M13/M13_COMPARATOR_POSITIVE_CONTROL_RESULTS_v1.json").read_text(encoding="utf-8"))
obs={"PC1":pc1["relation"],"PC2":pc2["relation"],"PC3":pc3["relation"]}
assert obs=={r["id"]:r["observed"] for r in expected["results"]}, (obs,expected)
print("M13_COMPARATOR_POSITIVE_CONTROLS_PASS")
