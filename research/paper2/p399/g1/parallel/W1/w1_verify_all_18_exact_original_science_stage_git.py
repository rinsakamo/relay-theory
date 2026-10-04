#!/usr/bin/env python3
"""Independently verify all 18 frozen W1 original science Git introductions and semantic-shape invariants.
No source reread is performed here. Does NOT substitute after E issuer reacquisition.
"""
import hashlib,json,pathlib,subprocess,sys
ROOT=pathlib.Path("research/paper2/p399/g1/parallel/W1")
F={
"P06":[("PRE_A","e9677b5a44e40996bf4dcc9c8a93f3ec98ac1d4d","P06_PRE_A_ORIGINAL_PUBLISHED_SOURCE_FREEZE_v1.json"),("A","13f46bfe82c9c06729904dcd7f6a583a1d9ae0de","P06_PASS_A_SOURCE_FIRST_FROZEN_v1.json"),("B","dd68116bc75f735182edf9faac1aa2bb47ff881e","P06_PASS_B_FULL_A_ORIGINAL_ADVERSARIAL_FROZEN_v1.json"),("C","ea0060dd6898314dfa04a9d4d1c637221705f987","P06_PASS_C_SOURCE_CLOSED_FROZEN_v1.json"),("D","f1bbb464315bf50b2075a1857501e37980f2c5e3","P06_PASS_D_ORIGINAL_STRUCTURE_UNCHANGED_GRAMMAR_v0_v1.json"),("E","2c57e8a4b09e0ec26e534d208058c475add89586","P06_PASS_E_SOURCE_RELATIVE_FIDELITY_FROZEN_v1.json")],
"P08":[("PRE_A","74b6310d8af50f5e126ee50e01d1cf59834be65b","P08_PRE_A_CORRECTED_PUBLISHED_MAIN_SOURCE_BOUNDED_v1.json"),("A","43db0f246ceeffbb5335e846bbd8bdd2185d516a","P08_PASS_A_CORRECTED_SOURCE_FIRST_FROZEN_v1.json"),("B","2efac266c981e3d0e79fdd2c4fa599f738384bbb","P08_PASS_B_FULL_CORRECTED_A_ADVERSARIAL_FROZEN_v1.json"),("C","db2e06d495273f7659e652cd4e1eeb99da636084","P08_PASS_C_FULL_CORRECTED_SOURCE_CLOSED_FROZEN_v1.json"),("D","1c84b7b44e529839d171b8660dfce04562932eb5","P08_PASS_D_CORRECTED_UNCHANGED_GRAMMAR_v0_FROZEN_v1.json"),("E","7eb5b2df6df90c186ae5140806752ac62d544f94","P08_PASS_E_CORRECTED_ORIGINAL_FIDELITY_FROZEN_v1.json")],
"P10":[("PRE_A","339c7d87e04903148322e51a959c58d2b906d33a","P10_PRE_A_MAIN_FUNDING_CORRECTION_SUPPLEMENTS_v1.json"),("A","f06a31987d9261e7a2c2682280c89136d7df4d5c","P10_PASS_A_ORIGINAL_SOURCE_FIRST_FROZEN_v1.json"),("B","43c1ad0bc898a136e239b7ea836293c0149da771","P10_PASS_B_FULL_ORIGINAL_A_SOURCE_ADVERSARIAL_FROZEN_v1.json"),("C","98e52fca82821d84f7fbf88cb264b62383023259","P10_PASS_C_SOURCE_CLOSED_FULL_A_NEGATIVE_FROZEN_v1.json"),("D","c3bcec6fca2b463e64ed314e052aec72a42e79d2","P10_PASS_D_FROZEN_UNCHANGED_GRAMMAR_v0_v1.json"),("E","dcfe66ff8c526ded46a262791d29c8bf6f1e35ee","P10_PASS_E_SOURCE_RELATIVE_FULL_MAIN_SUPPLEMENT_FIDELITY_FROZEN_v1.json")]
}
def cmd(*xs):return subprocess.check_output(["git",*xs],stderr=subprocess.DEVNULL).decode().strip()
report={"scope":"exact raw Git original stages BEFORE any qualification; NO fresh original publisher source check","all_stage_git_byte_and_ancestry":False,"per_paper":[]}
try:
 for name, stages in F.items():
    result={"paper":name,"stages":[]}
    docs={}
    last=None
    for key,commit,filename in stages:
      path=str(ROOT/name.lower()/filename)
      assert cmd("cat-file","-t",commit)=="commit"
      assert subprocess.run(["git","merge-base","--is-ancestor",commit,"HEAD"],capture_output=True).returncode==0
      if last:assert subprocess.run(["git","merge-base","--is-ancestor",last,commit],capture_output=True).returncode==0
      parent=cmd("rev-parse",commit+"^")
      assert subprocess.run(["git","cat-file","-e",parent+":"+path],capture_output=True).returncode!=0,"PREEXISTED_"+name+"_"+key
      blob=cmd("rev-parse",commit+":"+path)
      assert blob==cmd("rev-parse","HEAD:"+path),"MUTATED_"+name+"_"+key
      data=pathlib.Path(path).read_bytes()
      assert cmd("hash-object",path)==blob,"CURRENT_RAW_DRIFT_"+name+"_"+key
      docs[key]=json.loads(data)
      result["stages"].append({"stage":key,"first_git_commit":commit,"exact_original_blob":blob,"sha256":hashlib.sha256(data).hexdigest(),"immutable_pass":True})
      last=commit
    A,B,C,D,E=[docs[k] for k in ["A","B","C","D","E"]]
    if name=="P06":
      assert A==B["entire_exact_immutable_A_original_input"]==C["C1_original_full_A_reopened_before_patch"]
      claims={x["id"] for x in A["source_first_claims"]}
      neg={x["condition_id"] for x in C["C2_all_material_source_negative_conditions"]}
      targets=E["fidelity_targets"]
      cc={y for x in targets for y in x["covered_original_A_claim_ids"]}
      nn={y for x in targets for y in x["covered_C_condition_ids"]}
      assert len(claims)==28 and len(A["source_native_dependencies"])==40 and len(neg)==18
      assert len(D["source_claim_role_mapping"])==28 and len(D["all_original_source_dependencies"])==40
    elif name=="P08":
      assert A==B["exact_complete_immutable_A_reopened"]==C["full_frozen_original_A_reopened_BEFORE_any_corrections"]
      claims={x["id"] for x in A["source_first_claims"]}
      neg={x["id"] for x in C["C2_full_negative_register"]}
      targets=E["fidelity_groups"]
      cc={y for x in targets for y in x["covered_original_A_ids"]}
      nn={y for x in targets for y in x["covered_original_C_negative_ids"]}
      assert len(claims)==28 and len(A["source_native_original_dependencies"])==40 and len(neg)==17
      assert len(D["per_original_A_claim_v0_roles"])==28 and len(D["all_frozen_original_A_dependencies"])==40
    else:
      assert A==B["exact_entire_immutable_A_input"]==C["complete_original_frozen_A_reopened_before_any_patch"]
      claims={x["id"] for x in A["original_source_first_claims"]}
      neg={x["id"] for x in C["C2_original_full_unfavorable_conditions"]}
      targets=E["fidelity_targets"]
      cc={y for x in targets for y in x["all_original_A_claim_ids"]}
      nn={y for x in targets for y in x["material_original_C2_negative_ids"]}
      assert len(claims)==27 and len(A["original_native_dependencies"])==43 and len(neg)==18
      assert len(D["exact_source_claim_roles"])==27 and len(D["original_dependencies_roles"])==43
    assert claims<=cc and neg<=nn,"E_ORIGINAL_SOURCE_COVERAGE_INCOMPLETE_"+name
    result["immutability_and_exact_complete_A_in_B_C"]=True
    result["source_claims"]=len(claims);result["source_negatives"]=len(neg);result["original_E_coverage"]=True
    report["per_paper"].append(result)
 report["all_stage_git_byte_and_ancestry"]=True
 report["status"]="PASS_ALL_18_ORIGINAL_STAGE_INTRODUCTIONS_WITHOUT_FRESH_PUBLISHER_SOURCE"
except Exception as e:report.update({"status":"FAIL","error":repr(e)})
out=pathlib.Path("w1-git-original-history");out.mkdir(exist_ok=True)
(out/"exact_18_original_introduction_raw_sha.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({"status":report["status"],"per_paper":[{"paper":v["paper"],"stages":len(v["stages"])} for v in report["per_paper"]]}))
if not report["all_stage_git_byte_and_ancestry"]:sys.exit(1)
