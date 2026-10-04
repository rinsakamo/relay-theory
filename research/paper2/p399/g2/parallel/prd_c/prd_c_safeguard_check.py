#!/usr/bin/env python3
"""PRD-C machine-record integrity and destructive false-promotion tests, no science."""
import copy,json
from pathlib import Path
d=Path(__file__).resolve().parent
v=json.loads((d/"PRD_C_BOUNDED_VERDICTS_AND_OWNER_ESCALATIONS_v1.json").read_text())
g2=d.parents[1]
m=json.loads((g2/"MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json").read_text())
b=json.loads((g2/"MAIN40_G2_OBJECTIVE_BACKUPS_v1.json").read_text())
def check(x):
 assert x["source_only"] and x["main_result_inspected"] is False and x["manifest_changed"] is False
 assert x["baseline_sha"]=="69748673c80f421605f1c63607472903ac2ed68c"
 assert x["main_authorized"] is False and x["backup_activated"] is False
 assert x["PRD01"]["correction_notice_not_full_original"] and not x["PRD01"]["publisher_corrected_complete_original_obtained"]
 assert x["PRD01"]["correction_final"]=={"trident":.69,"planet":.31}
 assert x["B1"]["sha256"]=="9c17c00fba0985f6f66b8520c6fc971ae5a2c6d3e1bac266d9fba2739c9792fe"
 assert x["B1"]["prediсtion_slot_fit"] if False else x["B1"]["prediction_slot_fit"].startswith("HOLD_")
 assert x["B1"]["model_recovery_success"]==55 and x["B1"]["source_negative_extreme_proprioceptive_noise_ideal_misidentified"]==4
 assert not x["B1"]["activated"] and x["B1"]["central_family_independence"]=="HOLD"
 assert x["B2"]["sha256"]=="7b6e4192bfe1b60d794d197e14822997b77d22e437db89850fc4cddcb79482db"
 assert x["B2"]["prediction_slot_fit"].startswith("HOLD_") and x["B2"]["cross_lane_double_adoption_forbidden"]
 assert not x["B2"]["activated"]
 assert not x["G1"]["final_roster_frozen"]
 assert x["denominators"]["original_science_eligible_as_PRD01_slot"]==0
 assert x["denominators"]["standby_scientifically_qualified_as_independent_PRD_family"]==0
def main():
 check(v)
 rows=next(x for x in m.values() if isinstance(x,list) and len(x)==40 and any(z.get("slot")=="PRD-01" for z in x))
 assert len({x["doi"] for x in rows})==40
 for key,doi in (("PRD-01","10.1038/s41562-024-01930-8"),("PRD-02","10.1371/journal.pcbi.1001003"),("PRD-03","10.1371/journal.pcbi.1007093")):
  z=next(x for x in rows if x["slot"]==key)
  assert z["doi"]==doi and z["source_eligible"] is False and z["backup_activation_state"]=="NOT_ACTIVATED_PROSPECTIVE_ONLY"
 bk=next(x for x in b.values() if isinstance(x,list) and any(y.get("id")=="PRD-B1" for y in x))
 assert [(x["id"],x["doi"]) for x in bk if x["id"] in ["PRD-B1","PRD-B2"]]==[("PRD-B1","10.1371/journal.pcbi.1010740"),("PRD-B2","10.1371/journal.pcbi.1009557")]
 mutations=[
 ("correction-as-entire-source",lambda z:z["PRD01"].update(publisher_corrected_complete_original_obtained=True)),
 ("wrong-corrected-figure",lambda z:z["PRD01"]["correction_final"].update(trident=.33)),
 ("fabricated-B1-hash",lambda z:z["B1"].update(sha256="0"*64)),
 ("B1-auto-eligible",lambda z:z["B1"].update(prediction_slot_fit="ACCEPT")),
 ("erased-source-model-negative",lambda z:z["B1"].update(model_recovery_success=60)),
 ("B1-silent-activation",lambda z:z["B1"].update(activated=True)),
 ("B2-auto-eligible",lambda z:z["B2"].update(prediction_slot_fit="ACCEPT")),
 ("shared-B2-double-activation",lambda z:z["B2"].update(cross_lane_double_adoption_forbidden=False)),
 ("B2-silent-activation",lambda z:z["B2"].update(activated=True)),
 ("fabricated-frozen-G1",lambda z:z["G1"].update(final_roster_frozen=True)),
 ("fabricated-MAIN-GO",lambda z:z.update(main_authorized=True))
 ]
 for name,fn in mutations:
  t=copy.deepcopy(v);fn(t)
  try:check(t)
  except AssertionError: print("EXPECTED_REJECTION",name)
  else:raise AssertionError("false promotion accepted: "+name)
 print("PASS: exact 40 identities, ranked B1-B2 unchanged, 11/11 destructive false-promotion tests rejected")
if __name__=="__main__": main()
