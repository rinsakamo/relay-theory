#!/usr/bin/env python3
"""Independent G1 AFTER actual squash merges: exact old Git bytes, source scope,
original PR frozen stage chronology, previous v6 provenance and 190 pairs.
No MAIN scientific reconstruction, G2 study or independent human review.
"""
import ast, hashlib, itertools, json, os, pathlib, subprocess, sys, urllib.request
R=pathlib.Path(__file__).resolve().parents[1]
ROOT=R.parents[3]
BASE="38c5eb24c61b9e57371084a65fcbcb9fb9c62a4b"
PRE=R/"integration"
M=json.loads((PRE/"G1_FOUR_LANE_EXACT_PREMERGE_PROVENANCE_AND_CONDITIONAL_SCOPE_FREEZE_v1.json").read_text())
C=json.loads((PRE/"G1_POSTMERGE_INDEPENDENT_AUDIT_PREREGISTERED_CONTRACT_v1.json").read_text())
INTEGRATED=C["latest_actual_integrated_commit_at_audit_start"]
ORIGINAL_R="research/paper2/p399/g1/"
def cmd(*z,check=True):
 q=subprocess.run(["git",*map(str,z)],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if check and q.returncode:raise RuntimeError("GIT "+" ".join(z)+" "+q.stderr[-500:])
 return q.stdout.strip()
def isancestor(a,b):return subprocess.run(["git","merge-base","--is-ancestor",a,b],cwd=ROOT).returncode==0
def gitblob(commit,p):return cmd("rev-parse",commit+":"+p)
def fail(cond,m):
 if not cond:raise RuntimeError("FAIL_CLOSED_"+m)
fail(cmd("rev-parse",INTEGRATED)==INTEGRATED,"PINNED_INTEGRATED_HEAD_GONE")
fail(isancestor(INTEGRATED,"HEAD"),"NOT_POSTMERGE_AUDIT_BASE")
fail(isancestor(BASE,INTEGRATED),"ORIGINAL_CHARTER_START_MISSING")
assert M["file_change_count"]==171 and len(M["lanes"])==4
for item in C["expected_server_completed_merges"]:
 fail(isancestor(item["merge_commit_sha"],INTEGRATED),"ACTUAL_MERGE_MISSING_"+str(item["pr"]))
print("G1_AFTER_MERGE_FIVE_ACTUAL_GITHUB_COMMITS_IN_ANCESTRY_PASS",flush=True)
allfiles=set(); laneheads={}; stageproof={}; receiptproof={}
for lane in M["lanes"]:
 n=lane["lane"];h=lane["original_head_sha"];pr=lane["pr"]
 cmd("fetch","--no-tags","origin","refs/pull/"+str(pr)+"/head:refs/remotes/origin/g1-postmerge-pinned-"+str(pr))
 fail(cmd("rev-parse","refs/remotes/origin/g1-postmerge-pinned-"+str(pr))==h,"PINNED_ORIGINAL_PR_MOVED_"+n)
 fail(cmd("merge-base",BASE,h)==BASE,"ORIGINAL_PR_WRONG_BASE_"+n)
 files=lane["changed_filenames_exact_sorted"]
 for f in files:
  fail(f not in allfiles,"LANE_OVERLAP_"+f);allfiles.add(f)
  fail(f.startswith(ORIGINAL_R+"parallel/"+n+"/") or f.startswith(".github/workflows/p399-g1-"+n+"-"),"LANE_SCOPE_"+f)
  first=gitblob(h,f)
  fail(first==gitblob(INTEGRATED,f)==gitblob("HEAD",f),"SQUASH_CHANGED_ORIGINAL_GIT_BLOB_"+f)
 laneheads[n]=h
 print("G1_ACTUAL_POSTMERGE_ORIGINAL_BLOBS_IDENTICAL",n,len(files),flush=True)
fail(len(allfiles)==171,"TOTAL_171_SOURCE_FILES")
# Unchanged frozen historical v6 proof and every pre-existing original PF/G1 fingerprint.
z=subprocess.run([sys.executable,str(R/"g1_v6_actual_issuer_original_scoped_science_evidence_check.py")],cwd=ROOT,text=True,capture_output=True)
if z.returncode:print(z.stdout[-2000:],z.stderr[-1500:],flush=True)
fail(z.returncode==0 and "G1_V6_ALL_PASS" in z.stdout,"ORIGINAL_IMMUTABLE_V6_PROOF")
fail("f6d1fcaa83b07a1b4db67da083eecdd0238ec1f9c85b73265d3f3e78a2f78b05" in z.stdout,"ORIGINAL_V6_SHA_PROJECTION")
print("G1_ORIGINAL_HISTORIC_V6_REVALIDATED_9_OF_20_AND_P14_NEGATIVES_PASS",flush=True)
# Extract W3 exact six-stage authority WITHOUT relying on W3's verification code;
# parse its static preregistered STAGES literal independently.
source=(R/"parallel/W3/W3_three_scoped_science_handoff_independent_history_gate.py").read_text()
p=ast.parse(source)
W3=next(ast.literal_eval(x.value) for x in p.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="STAGES" for t in x.targets))
W4=json.loads((R/"parallel/W4/W4_FINAL_REAL_ORIGINAL_SCIENCE_AUDIT_REPORT_v1.json").read_text())
expected_run=C["each_paper_original_source_scoped_individual_postE_original_run"]
qual={}
for id,rel in C["expected_original_paper_qualification_paths"].items():
 path=ORIGINAL_R+rel
 doc=json.loads((ROOT/path).read_text())
 lane=next(x["lane"] for x in M["lanes"] if id in x["paper_ids"])
 original=laneheads[lane]
 fail(gitblob(original,path)==gitblob(INTEGRATED,path)==gitblob("HEAD",path),"QUALIFICATION_ORIGINAL_RAW_CHANGED_"+id)
 q_intro=cmd("log","--diff-filter=A","--format=%H",original,"--",path).splitlines()
 fail(len(q_intro)==1,"QUALIFICATION_ORIGINAL_COMMIT_NOT_SINGLE_"+id)
 if id in ("P06","P08"):stage=doc["original_frozen_stage_commits"]
 elif id=="P10":stage=doc["exact_separate_git_freeze_commit_ids"]
 elif id in ("P11","P12"):stage=doc["frozen_stages"]
 elif id=="P17":stage=doc["immutable_scientific_stage_original_intro_commits"]
 elif id in ("P15","P16","P18"):stage={a:c for a,f,c in W3[id]}
 elif id=="P19":stage=W4["immutable_qualifying_stage_commits"]["P19"]
 else:stage=W4["immutable_qualifying_stage_commits"]["P20"]
 order=list(stage)
 fail(len(order) in (6,7),"STAGE_COUNT_"+id)
 prev=BASE; items=[]
 for name in order:
  c=stage[name]
  fail(isancestor(prev,c),"STAGE_TRUE_SEQUENTIAL_ANCESTRY_"+id+"_"+name)
  fail(isancestor(c,original),"STAGE_GIT_ORIGINAL_PR_ANCESTRY_"+id+"_"+name)
  paths=cmd("diff-tree","--no-commit-id","--name-only","-r",c).splitlines()
  if id in ("P15","P16","P18"):
   sourcefile=next(f for k,f,s in W3[id] if k==name)
   checked=ORIGINAL_R+"parallel/W3/"+sourcefile
   fail(checked in paths,"ORIGINAL_W3_STAGE_NOT_INTRODUCED_"+id+"_"+name)
   fail(gitblob(c,checked)==gitblob(original,checked)==gitblob(INTEGRATED,checked),"W3_STAGE_RAW_ORIGINAL_MUTATED_"+id+"_"+name)
  else:
   pref=ORIGINAL_R+"parallel/"+lane+"/"+id.lower()+"/"
   candidates=[f for f in paths if f.startswith(pref) and (f.endswith(".json") or f.endswith(".md"))]
   fail(bool(candidates),"ORIGINAL_STAGE_NO_PAPER_FILE_"+id+"_"+name)
   found=0
   for f in candidates:
    if cmd("cat-file","-e",original+":"+f,check=False)=="":
     # only stage original files still present and identical count as frozen
     fail(gitblob(c,f)==gitblob(original,f)==gitblob(INTEGRATED,f),"ORIGINAL_STAGE_RAW_CHANGED_"+id+"_"+name+"_"+f)
     found+=1
   fail(found>0,"ORIGINAL_STAGE_ALL_FILES_MISSING_"+id+"_"+name)
  items.append({"stage":name,"original_introduction_commit":c,"files_identified":len(paths)})
  prev=c
 fail(isancestor(prev,q_intro[0]),"QUALIFICATION_PRIOR_TO_SCIENCE_E_"+id)
 if id=="P06":qualified=doc["formal_decision"].startswith("SOURCE_BOUNDED_")
 elif id=="P08":qualified="MANDATORY_COMPLETE_SUBSTANTIVE_CORRECTION" in doc["formal_decision"] and doc["mandatory_scientific_correction"]["doi"]=="10.1371/journal.pcbi.1005908"
 elif id=="P10":qualified=doc["qualification"]=="QUALIFIED_BOUNDED_ORIGINAL_SOURCE_STRUCTURAL_AND_PROCEDURAL_ONLY"
 elif id in ("P11","P12","P17"):qualified=doc["decision"]=="SOURCE_BOUNDED_INDIVIDUAL_QUALIFIED"
 elif id=="P15":qualified=doc["P15_individual_source_scientific_qualified"]
 elif id=="P16":qualified=doc["separate_scientific_candidate_qualified"] and not doc["diversity_or_family_qualified_for_aggregate_G1"]
 elif id=="P18":qualified=doc["P18_individual_scoped_scientific_source_qualified"]
 elif id=="P19":qualified=str(doc["outcome"]).upper().find("QUALIFIED")>=0
 else:qualified=doc["qualified_W4_delta_candidate"]==1 and "UNRESOLVED_ORIGINAL_STATISTICAL_NUMERIC_CONTRADICTION" in doc["decision"]
 fail(qualified,"EXACT_QUALIFICATION_SCOPE_"+id)
 qual[id]={"qualifying_scope":"SOURCE_BOUNDED_INDIVIDUAL_ONLY","original_git_qualification_blob":gitblob(original,path),"integrated_git_blob":gitblob(INTEGRATED,path),"original_qualification_commit":q_intro[0],"orig_stages":items,"historical_original_postE_real_issuer_ci":expected_run[id]}
 print("G1_ACTUAL_ORIGINAL_PREA_E_QUALIFICATION_CHRONOLOGY_PASS",id,len(items),flush=True)
fail(len(qual)==11 and sum(len(q["orig_stages"]) for q in qual.values())==67,"ALL_ELEVEN_STAGE_COUNT")
# Existing source-supported pair comparisons only; zero blanket DOI-based independence.
w3=json.loads((R/"parallel/W3/W3_SOURCE_COMPLETED_FAMILY_HANDOFF_MATRIX_v2.json").read_text())
w4=json.loads((R/"parallel/W4/W4_P19_PF03_P14_P20_G2_SKL_CENTRAL_FAMILY_COMPARISON_MATRIX_v1.json").read_text())
base=json.loads((R/"G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v6.json").read_text())
roster=["PF01","PF02","PF03","PF04","P05","P06","P07","P08","P09","P10","P11","P12","P13","P14","P15","P16","P17","P18","P19","P20"]
assert len(set(roster))==20
pairmap={frozenset([a,b]):{"pair":[a,b],"assessment":"NOT_YET_FULL_ORIGINAL_SOURCE_PAIR_ADJUDICATED","final_family_independence":False} for a,b in itertools.combinations(roster,2)}
for item in w3["rows"]:
 a=item["left"];b=item["right"]
 if a in roster and b in roster:
  pairmap[frozenset((a,b))] .update({"assessment":"UNDERDETERMINED_SOURCE_COMPARISON_W3" ,"source":"W3 final original-supported 7 pair handoff" ,"final_family_independence":False})
for item in w4["comparisons"]:
 a,b=item["pair"]
 if a in roster and b in roster:
  c=item["conclusion"];distinct="DISTINCT" in c
  pairmap[frozenset((a,b))] .update({"assessment":("SOURCE_SUPPORTED_IMPLEMENTED_CENTRAL_DISTINCT_W4" if distinct else "UNDERDETERMINED_SOURCE_COMPARISON_W4") ,"source":"W4 original exact math comparison v1" ,"final_family_independence":False})
distinct=[v for v in pairmap.values() if v["assessment"]=="SOURCE_SUPPORTED_IMPLEMENTED_CENTRAL_DISTINCT_W4"]
fail(len(pairmap)==190 and len(distinct)==2,"190_PAIR_OR_2_LIMITED_SOURCE_DISTINCT_COUNT")
fail(all(not v["final_family_independence"] for v in pairmap.values()),"FALSE_GLOBAL_FAMILY_CLEARANCE")
print("G1_190_OF_190_PAIR_ROWS_CREATED_SOURCE_SUPPORTED_TWO_BOUNDED_DISTINCT_ONLY",flush=True)
# Both live prior-publisher sources and full exact numerical replay are bounded historical receipts.
assert len(set(expected_run.values()))==11
# Independence: actual current Actions statuses, not just prior document assertions.
token=os.getenv("GITHUB_TOKEN")
fail(bool(token),"NO_GITHUB_TOKEN_FOR_INDEPENDENT_HISTORICAL_CI_VERIFICATION")
for pid,rid in expected_run.items():
 req=urllib.request.Request("https://api.github.com/repos/rinsakamo/relay-theory/actions/runs/"+str(rid),
  headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json","User-Agent":"G1-independent-postmerge-audit"})
 with urllib.request.urlopen(req,timeout=12) as stream:obj=json.load(stream)
 fail(obj["conclusion"]=="success" and obj["id"]==rid,"INDEPENDENT_HISTORICAL_ACTIONS_FAILED_"+pid)
 receiptproof[pid]={"run_id":rid,"real_github_server_current_run_conclusion":"success"}
 print("G1_INDEPENDENT_GITHUB_REAL_POSTE_ACTIONS_SUCCESS_CONFIRMED",pid,rid,flush=True)
# Four lane source proof has not converted same-publisher documents into extra papers.
fail(base["counts"]["cohort_current_source_scoped_formally_qualified"]==9,"DO_NOT_MUTATE_BASELINE")
fail(M["expected_integrated_original_primary_source_qualified_potential"]==20,"EXPECTED_SCOPED_COUNT")
fail(M["new_publication_diversity_success"]==0 and C["full_model_variant_certified_20"]==False,"NO_FALSE_DIVERSITY_FULL_SOURCE")
projection={"schema":"p399.g1.independent.actual.postmerge.integrity_and_scoped.decision.v1",
 "exact_original_merged_G1_tree":INTEGRATED,"exact_original_frozen_four_lane_heads":laneheads,
 "actual_transport_and_original_stage_commit_chains_rechecked":True,
 "all_171_integrated_lanes_exact_original_git_blobs_sha1":{p:gitblob(INTEGRATED,p) for p in sorted(allfiles)},
 "historic_v6_raw_proof_sha256":"f6d1fcaa83b07a1b4db67da083eecdd0238ec1f9c85b73265d3f3e78a2f78b05",
 "eleven_original_source_scoped_postE_individual_decision_proofs":qual,
 "independent_current_GitHub_original_postE_Actions_server_receipts":receiptproof,
 "all_190_intra_G1_pair_audit_matrix":list(pairmap.values()),
 "summary":{"historic_original_source_scoped":9,"new_exact_source_scoped_individual_decisions":11,
  "all_20_original_individual_scoped_science_present":True,
  "unconditional_new_bounded_nonP10":10,
  "P10_original_Eqs1_10_limited_individual_only":True,
  "P10_optional_full_SHT_Eqs11_13_scientific_reconstruction_qualified":False,
  "full_pilot20_scientific_admission":False,
  "all_190_native_family_independence_qualified":False,
  "source_supported_two_local_nonoverlap_not_whole_family_clearance":2,
  "G2_final_40_and_800_pairs_unverified":True,
  "qualified_issuer_original_nonPLOS":0,
  "full_publisher_diversity_gate":False,
  "new_G4_joint_audit":False,
  "author_MAIN_GO":False,
  "overall_G1_status":"PARTIAL_INDIVIDUAL_SOURCES_INTEGRATED_GLOBAL_HOLD"}}
s=json.dumps(projection,sort_keys=True,separators=(",",":"),ensure_ascii=False)
digest=hashlib.sha256(s.encode()).hexdigest()
out=pathlib.Path("g1-audit-postmerge");out.mkdir(exist_ok=True)
(out/"actual_original_postmerge_independent_projection.json").write_text(json.dumps({"sha256":digest,"projection":projection},indent=2,ensure_ascii=False)+"\n")
print("G1_POSTMERGE_INDEPENDENT_AUDIT_PROJECTION_SHA256",digest,flush=True)
print("G1_POSTMERGE_INDEPENDENT_BOUNDED_SOURCE_AUDIT_PASS_171_11_67_190_WITH_G1_HOLD_NO_MAIN",flush=True)
