#!/usr/bin/env python3
"""G1 v7 ledger independent deterministic consistency and false-promotion guards.
Checks committed data against immutable original v6, pinned postmerge contract,
and the original W3/W4 scientific comparison reports. Does NOT issue global GO.
"""
import copy,hashlib,itertools,json,pathlib,subprocess
G=pathlib.Path(__file__).resolve().parents[1]
L=json.loads((G/"G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v7.json").read_text())
P=json.loads((G/"integration/G1_INDEPENDENT_POSTMERGE_ORIGINAL_SOURCE_NATIVE_190_PAIR_AUDIT_MATRIX_v7.json").read_text())
V=json.loads((G/"G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v6.json").read_text())
C=json.loads((G/"integration/G1_POSTMERGE_INDEPENDENT_AUDIT_PREREGISTERED_CONTRACT_v1.json").read_text())
S=json.loads((G/"parallel/W3/W3_SOURCE_COMPLETED_FAMILY_HANDOFF_MATRIX_v2.json").read_text())
T=json.loads((G/"parallel/W4/W4_P19_PF03_P14_P20_G2_SKL_CENTRAL_FAMILY_COMPARISON_MATRIX_v1.json").read_text())
def require(t,m):
 if not t:raise RuntimeError("G1_V7_REJECT_"+m)
def pair(a,b):return tuple(sorted((a,b)))
old=V["original_four"]+V["additional"];dois={x["id"]:x["doi"] for x in old}
source_sha={x["id"]:x.get("original_pdf_sha256") or x.get("publisher_pdf",{}).get("raw_sha256") for x in old}
base_old=set(["PF01","PF02","PF03","PF04","P05","P07","P09","P13","P14"])
new={"P06","P08","P10","P11","P12","P17","P15","P16","P18","P19","P20"}
expected={pair(x["left"],x["right"]):"SOURCE_REVIEW_UNDERDETERMINED" for x in S["rows"] if x["left"] in dois and x["right"] in dois}
for x in T["comparisons"]:
 a,b=x["pair"]
 if a in dois and b in dois:
  q=pair(a,b);require(q not in expected,"ORIGINAL_W3_W4_COMPARISON_CONFLICT")
  expected[q]="BOUNDED_IMPLEMENTED_CORE_DISTINCT_NOT_UNIVERSAL_FAMILY_CLEARED" if x["conclusion"]=="CENTRAL_FAMILY_DISTINCT_SOURCE_SUPPORTED" else "SOURCE_REVIEW_UNDERDETERMINED"
assert len(expected)==9
def validate(l,p):
 c=l["qualification_counts"];u=p["universe"];v=l["roster_snapshot"]
 require(l["base_original_v6_raw_Git_blob"]=="e8a051f3506d7368197896f5b1b78615eae81701","ORIGINAL_V6_RAW_GIT_SHA")
 require(l["original_actual_shared_four_lane_after_merge_git_HEAD"]==C["latest_actual_integrated_commit_at_audit_start"],"WRONG_ACTUAL_MERGED_HEAD")
 require(len(v)==20 and len({x["id"] for x in v})==20 and len({x["doi"] for x in v})==20,"TWENTY_UNIQUE_PUBLISHER_WORKS")
 require(set(x["id"] for x in v)==set(dois),"EXACT_ORIGINAL_V6_PILOT_ROSTER")
 for item in v:
  id=item["id"]
  require(item["doi"]==dois[id] and item["original_publisher_main_raw_sha256"]==source_sha[id],"PINNED_ORIGINAL_PUBLISHER_SHA_OR_DOI_"+id)
  require(item["published_primary_issuer"]=="PLOS Computational Biology","UNJUSTIFIED_NEW_PUBLISHER_"+id)
  require(item["scope_individual_qualified_record_or_baseline_authority"]==("HISTORIC_INDEPENDENT_SOURCE_SCOPED_BASELINE_V6" if id in base_old else "NEW_FOUR_LANE_ORIGINAL_SOURCE_SCOPED_DECISION_INTEGRATED_V7"),"ORIGINAL_V6_TO_V7_PROSPECTIVE_STATUS_"+id)
  require(item["global_family_independent_approved"] is False,"FALSE_GLOBAL_NATIVE_FAMILY_"+id)
 p10=next(x for x in v if x["id"]=="P10")
 require("SHT_EQUATIONS_11_13_NOT_SCIENTIFICALLY_RECONSTRUCTED" in p10["scientific_scope_exception"],"P10_FULL_VARIANT_FALSIFIED")
 require(c["prior_unmodified_source_scoped_individual_receipts"]==9 and c["new_scope_qualified_fourlane_individual_decisions"]==11 and c["all_20_have_original_scoped_qualification_record"]==20,"SOURCE_SCOPE_COUNTS_NOT_BOTH")
 require(sum(c["new_"+x] for x in ("W1","W2","W3","W4"))==11 and [c["new_"+x] for x in ("W1","W2","W3","W4")]==[3,3,3,2],"FOUR_LANE_SCOPE_COUNTS")
 require(c["new_candidate_original_stages_introduced_immutable"]==67 and c["original_identical_integrated_lane_file_blobs"]==171 and c["independent_afterE_original_CI_current_success_rechecked"]==11,"ACTUAL_INDEPENDENT_CI_COUNTS")
 require(c["all_20_paper_full_all_original_variants_complete_asserted"] is False and c["P10_full_SHT_Eqs11_13_qualified"] is False,"FALSE_P10_OR_FULL_MODEL")
 require(c["actual_qualified_primary_original_publisher_PLOS"]==20 and c["actual_qualified_primary_original_non_PLOS"]==0 and c["full_original_publisher_diversity_gate"] is False,"FALSE_PUBLISHER_DIVERSITY")
 require(l["publication_diversity_hold"]["automatic_replacement_or_G2_reservation_released"] is False,"UNAUTHORIZED_ELIFE_DOUBLE_RESERVED_REPLACEMENT")
 require(len(p["pair_rows"])==190 and len({pair(*x["ids"]) for x in p["pair_rows"]})==190,"ALL_190_DISTINCT_PAIR_ROWS")
 require(len(list(itertools.combinations(dois,2)))==190 and set(pair(*x["ids"]) for x in p["pair_rows"])==set(pair(a,b) for a,b in itertools.combinations(dois,2)),"PAIR_UNIVERSE_MATCH_EXACT_20")
 counts={"BOUNDED_IMPLEMENTED_CORE_DISTINCT_NOT_UNIVERSAL_FAMILY_CLEARED":0,"SOURCE_REVIEW_UNDERDETERMINED":0,"NOT_YET_FULL_SOURCE_NATIVE_ORIGINAL_PAIR_AUDITED":0}
 for x in p["pair_rows"]:
  q=pair(*x["ids"]);expected_result=expected.get(q,"NOT_YET_FULL_SOURCE_NATIVE_ORIGINAL_PAIR_AUDITED")
  require(x["assessment"]==expected_result and x["final_global_independent_family_accepted"] is False,"UNSUPPORTED_NATIVE_FAMILY_PROMOTION_"+str(q))
  counts[x["assessment"]]+=1
 require(counts=={"BOUNDED_IMPLEMENTED_CORE_DISTINCT_NOT_UNIVERSAL_FAMILY_CLEARED":2,"SOURCE_REVIEW_UNDERDETERMINED":7,"NOT_YET_FULL_SOURCE_NATIVE_ORIGINAL_PAIR_AUDITED":181},"PAIR_CLASS_DENOMINATORS")
 require([u["bounded_original_implemented_core_nonoverlap_supported"],u["bounded_original_comparison_underdetermined"],u["not_full_original_ancestry_audited"],u["final_model_family_independent_accepted"]]==[2,7,181,0],"NATIVE_PAIR_SUMMARY")
 require(u["G1_x_G2_final_native_pairs_completed"]==0 and c["cross_G1_x_final_G2_pair_source_cleared"]==0,"UNAUTHORIZED_G2_FAMILY_CLEARANCE")
 require(l["global_scientific_qualifications_exhaustive_final"] is False and l["MAIN_authorized"] is False and l["G1_global_status"]=="G1_PARTIAL","UNAUTHORIZED_MAIN_OR_FINAL_G1")
 return counts
counts=validate(L,P)
# Destructive proof of fail-closed against eight distinct false promotions.
for name,fn in [
 ("SILENT_FULL_P10",lambda l,p:l["qualification_counts"].__setitem__("P10_full_SHT_Eqs11_13_qualified",True)),
 ("NEW_NON_PLOS_WITHOUT_SCIENCE",lambda l,p:l["qualification_counts"].__setitem__("actual_qualified_primary_original_non_PLOS",1)),
 ("FALSE_ONE_PAIR_CLEARED",lambda l,p:p["pair_rows"][0].__setitem__("final_global_independent_family_accepted",True)),
 ("FALSE_G2_800_CLEARANCE",lambda l,p:l["qualification_counts"].__setitem__("cross_G1_x_final_G2_pair_source_cleared",800)),
 ("FALSE_AUTHOR_MAIN_GO",lambda l,p:l.__setitem__("MAIN_authorized",True)),
 ("FALSE_V6_ORIGINAL_SHA",lambda l,p:l["roster_snapshot"][0].__setitem__("original_publisher_main_raw_sha256","0"*64)),
 ("FALSE_QUALIFICATION_ROSTER",lambda l,p:l["roster_snapshot"][0].__setitem__("doi",l["roster_snapshot"][1]["doi"])),
 ("FALSE_UNAUDITED_PAIR_DISTINCT",lambda l,p:p["pair_rows"][0].__setitem__("assessment","BOUNDED_IMPLEMENTED_CORE_DISTINCT_NOT_UNIVERSAL_FAMILY_CLEARED"))]:
 l=copy.deepcopy(L);p=copy.deepcopy(P);fn(l,p)
 try:validate(l,p)
 except RuntimeError:print("G1_V7_DESTRUCTIVE_FALSE_PROMOTION_REJECTED",name,flush=True)
 else:raise RuntimeError("FALSE_PROMOTION_ACCEPTED "+name)
print("G1_V7_EIGHT_OF_EIGHT_DESTRUCTIVE_FALSE_PROMOTIONS_REJECTED",flush=True)
projection={"ledger_actual_raw_sha256":hashlib.sha256((G/"G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v7.json").read_bytes()).hexdigest(),"pair_matrix_raw_sha256":hashlib.sha256((G/"integration/G1_INDEPENDENT_POSTMERGE_ORIGINAL_SOURCE_NATIVE_190_PAIR_AUDIT_MATRIX_v7.json").read_bytes()).hexdigest(),"earlier_actual_after_merges_original_171_67_11_proof":"c7e5198729e5fdfddffc2c034dd7760b9f1486cb9af8473302263fdf15d42ea6","previous_v6_raw_git_blob":"e8a051f3506d7368197896f5b1b78615eae81701","source_scoped_individual_papers":20,"full_original_variant_clearance":False,"native_pair_categories":counts,"publisher_diversity_pass":False,"MAIN":False}
out=pathlib.Path("g1-audit-v7");out.mkdir(exist_ok=True)
projection_sha=hashlib.sha256(json.dumps(projection,sort_keys=True,separators=(",",":")).encode()).hexdigest()
(out/"validated_v7_scoped_original_provenance.json").write_text(json.dumps({"projection":projection,"projection_sha256":projection_sha},indent=2)+"\n")
print("G1_V7_INDEPENDENT_LEDGER_AND_NATIVE_190_PAIR_CONTENT_SHA256",projection_sha,flush=True)
print("G1_V7_INDEPENDENT_LEDGER_20_SCOPED_NOT_FINAL_MAIN_NO_GO_PASS",flush=True)
