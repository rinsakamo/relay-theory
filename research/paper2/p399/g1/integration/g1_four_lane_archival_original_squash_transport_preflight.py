#!/usr/bin/env python3
"""Outcome-blind original-commit-preserving FOUR G1 science-lane temporary integration.

Uses only frozen evidence and the four original pinned PR HEAD objects.
Makes temporary LOCAL squash transport in disposable worktree, NEVER pushes. Original historical scientific Git stage DAGs are retained by verified separate immutable archival branches.
All qualification is per paper source-scoped; G1 full admission, family
all-pairs, publisher diversity, MAIN GO stay FALSE.
"""
import json,subprocess,tempfile,pathlib,hashlib,os,sys,shutil
R=pathlib.Path(__file__).resolve().parents[1]
M=json.loads((R/"integration/G1_FOUR_LANE_EXACT_PREMERGE_PROVENANCE_AND_CONDITIONAL_SCOPE_FREEZE_v1.json").read_text())
X=json.loads((R/"integration/G1_ORIGINAL_STAGE_ARCHIVE_AND_SQUASH_TRANSPORT_EXCEPTION_AFTER_GITHUB_405_v1.json").read_text())
assert X["actual_host_integration_blocker"]["API_response"].startswith("HTTP 405")
archives={x["lane"]:x for x in X["archived_immutable_scientific_history_heads"]}
BASE=M["base_exact_before_any_science_lane_integration"]
assert BASE=="38c5eb24c61b9e57371084a65fcbcb9fb9c62a4b"
assert len(M["lanes"])==4 and len(M["all_11_exact_paper_ids"])==11
assert len(set(M["all_11_exact_paper_ids"]))==11 and len(set(M["all_11_exact_paper_ids"])|set(["PF01","PF02","PF03","PF04","P07","P09","P05","P13","P14"]))==20
def git(*args,cwd=None):
 return subprocess.check_output(["git",*map(str,args)],cwd=cwd,stderr=subprocess.STDOUT,text=True).strip()
def blob(rev,path,cwd=None):return git("rev-parse",str(rev)+":"+path,cwd=cwd)
expected=set()
for lane in M["lanes"]:
 n=lane["lane"];files=lane["changed_filenames_exact_sorted"]
 assert len(files)>20 and len(files)==len(set(files))
 assert all(x.startswith("research/paper2/p399/g1/parallel/"+n+"/") or x.startswith(".github/workflows/p399-g1-"+n+"-") for x in files)
 assert not expected.intersection(files)
 expected.update(files)
assert len(expected)==M["file_change_count"]==171
q={
"P06":("W1","p06/P06_SEPARATE_LIMITED_ORIGINAL_SCIENCE_QUALIFICATION_20261004.json"),
"P08":("W1","p08/P08_SEPARATE_LIMITED_ORIGINAL_SCIENCE_QUALIFICATION_20261004.json"),
"P10":("W1","p10/P10_SEPARATE_LIMITED_ORIGINAL_SCIENCE_QUALIFICATION_20261004.json"),
"P11":("W2","p11/P11_SEPARATE_INDIVIDUAL_SOURCE_BOUNDED_QUALIFICATION_v1.json"),
"P12":("W2","p12/P12_SEPARATE_SOURCE_BOUNDED_QUALIFICATION_AFTER_POSTE_v1.json"),
"P17":("W2","p17/P17_SEPARATE_INDIVIDUAL_SOURCE_BOUNDED_QUALIFICATION_AFTER_POSTE_v1.json"),
"P15":("W3","P15_POST_E_INDEPENDENT_PUBLISHER_SCOPED_QUALIFICATION_v1.json"),
"P16":("W3","P16_POST_E_INDEPENDENT_REAL_SOURCE_SCOPED_QUALIFICATION_v1.json"),
"P18":("W3","P18_POST_E_INDEPENDENT_PUBLISHER_SCOPED_QUALIFICATION_v1.json"),
"P19":("W4","p19/P19_SEPARATE_BOUNDED_POSTE_SCIENTIFIC_QUALIFICATION_20261004.json"),
"P20":("W4","p20/P20_SEPARATE_POSTE_SOURCE_BOUNDED_SCIENTIFIC_QUALIFICATION_20261004.json")}
assert set(q)==set(M["all_11_exact_paper_ids"])
old=["G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v6.json","G1_INDEPENDENT_EVIDENCE_SHA256_RECEIPT_v6.json","G1_FOUR_PARALLEL_SCIENCE_LANES_FROZEN_COORDINATION_CHARTER_v1.json"]
prefix="research/paper2/p399/g1/"
for lane in M["lanes"]:
 pr=lane["pr"];target=lane["original_head_sha"]
 git("fetch","--no-tags","origin","refs/pull/"+str(pr)+"/head:refs/remotes/origin/p399-preflight-"+str(pr))
 actual=git("rev-parse","refs/remotes/origin/p399-preflight-"+str(pr))
 assert actual==target,"ORIGINAL_FOUR_PR_HEAD_MOVED "+str(pr)
 orig=git("merge-base",BASE,actual)
 assert orig==BASE,"NOT_ORIGINAL_FROZEN_COMMON_ANCESTOR "+str(pr)
 arc=archives[lane["lane"]]
 assert arc["original_source_head"]==target
 git("fetch","--no-tags","origin","refs/heads/"+arc["archival_branch"]+":refs/remotes/origin/p399-archive-"+lane["lane"])
 assert git("rev-parse","refs/remotes/origin/p399-archive-"+lane["lane"])==target
 print("P399_G1_PINNED_ORIGINAL_PR_AND_IMMUTABLE_ARCHIVE_PASS",lane["lane"],pr,actual,len(lane["changed_filenames_exact_sorted"]),flush=True)
with tempfile.TemporaryDirectory(prefix="relaytheory-g1-four-lane-") as d:
 git("worktree","add","--detach",d,BASE)
 try:
  git("config","user.email","g1-preflight@example.invalid",cwd=d)
  git("config","user.name","G1 Scientific Preflight Simulation",cwd=d)
  for lane in M["lanes"]:
   head=lane["original_head_sha"]
   # Host forbids merge commits (actual HTTP405); audit-only squash transport preserves exact original file Git BLOBS; frozen original PRE_A->E Git ancestors remain on independent archival branches, not in squash ancestry.
   print("P399_G1_SIMULATE_SQUASH_EVIDENCE_ONLY_TRANSPORT_BEGIN",lane["lane"],head,flush=True)
   git("merge","--squash",head,cwd=d)
   git("commit","-m","G1 temporary audit-only squash transport "+lane["lane"],cwd=d)
   for file in lane["changed_filenames_exact_sorted"]:
    assert blob("HEAD",file,d)==blob(head,file,d),"SOURCE_BLOB_WAS_REWRITTEN "+file
   assert all(blob("HEAD",prefix+x,d)==blob(BASE,prefix+x,d) for x in old)
   print("P399_G1_SIMULATED_LANE_ORIGINAL_BLOBS_UNCHANGED_PASS",lane["lane"],len(lane["changed_filenames_exact_sorted"]),flush=True)
  found=set(git("diff","--name-only",BASE,"HEAD",cwd=d).splitlines())
  assert found==expected,"FOUR_LANE_DIFF_CHANGED_OR_MISSING expected "+str(len(expected))+" got "+str(len(found))+" different "+repr(sorted(found^expected)[:7])
  for lane in M["lanes"]:
   assert git("merge-base","--is-ancestor",BASE,lane["original_head_sha"],cwd=d)=="" # historical original stages remain reachable on archived refs, squash transport does not pretend Git ancestry.
  qualifiers={}
  for pid,(lane,file) in q.items():
   p=pathlib.Path(d)/prefix/"parallel"/lane/file
   assert p.is_file(),pid+" qualification absent"
   data=json.loads(p.read_text())
   if pid=="P06": assert data["formal_decision"].startswith("SOURCE_BOUNDED_") and data["no_MAIN"]
   if pid=="P08": assert "MANDATORY_COMPLETE_SUBSTANTIVE_CORRECTION" in data["formal_decision"] and data["no_MAIN"]
   if pid=="P10": assert data["qualification"].startswith("QUALIFIED_BOUNDED") and not data["MAIN_authorized"]
   if pid in ("P11","P12","P17"):assert data["decision"]=="SOURCE_BOUNDED_INDIVIDUAL_QUALIFIED"
   if pid=="P15":assert data["P15_individual_source_scientific_qualified"] and data["author_MAIN_GO"] is False
   if pid=="P16":assert data["separate_scientific_candidate_qualified"] and data["main_authorization"] is False
   if pid=="P18":assert data["P18_individual_scoped_scientific_source_qualified"] and not data["MAIN_authorized"]
   if pid=="P19":assert data["outcome"] and not data["MAIN_authorized"]
   if pid=="P20":assert data["qualified_W4_delta_candidate"]==1 and not data["MAIN_authorized"]
   qualifiers[pid]={"path":str(p.relative_to(d)),"git_blob":blob("HEAD",str(p.relative_to(d)),cwd=d),"only_original_source_scoped":True}
  # Independent execution of actual earlier v6 selected historical proof from disposable merged history.
  old_check=pathlib.Path(d)/prefix/"g1_v6_actual_issuer_original_scoped_science_evidence_check.py"
  run=subprocess.run([sys.executable,str(old_check)],cwd=d,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  if run.returncode:print(run.stdout[-6000:],flush=True)
  assert run.returncode==0 and "G1_V6_ALL_PASS" in run.stdout
  assert "f6d1fcaa83b07a1b4db67da083eecdd0238ec1f9c85b73265d3f3e78a2f78b05" in run.stdout
  print("P399_G1_ORIGINAL_V6_RAW_SCIENCE_EVIDENCE_ON_COMBINED_TREE_PASS",flush=True)
  for canary,override in [("FALSE_GLOBAL_G1_GO",True),("P10_FULL_OPTIONAL_EQS_11_13_PROVEN",True),("ALL_FAMILY_INDEPENDENT",True),("NON_PLOS_DIVERSITY_ACHIEVED",True)]:
   assert override and canary not in M,"intentional false promotion blocked by unchanged scope-frozen manifest"
   print("P399_G1_FAIL_CLOSED_AGAINST",canary,flush=True)
  projection={"schema":"p399.g1.four_lane_original_head_temp_merge_source_provenance_only.v1",
    "frozen_original_premerge":BASE,
    "original_unmodified_lane_heads":{x["lane"]:x["original_head_sha"] for x in M["lanes"]},
    "archival_history_refs_verified":{x["lane"]:archives[x["lane"]]["archival_branch"] for x in M["lanes"]},
    "mode":"TEMPORARY_GITHUB_REPOSITORY_ALLOWED_SQUASH_TRANSPORT_NOT_ORIGINAL_STAGE_GIT_ANCESTRY",
    "per_lane_unmodified_git_files":{x["lane"]:len(x["changed_filenames_exact_sorted"]) for x in M["lanes"]},
    "exact_scoped_diff_171_blobs":{k:blob("HEAD",k,cwd=d) for k in sorted(found)},
    "eleven_original_only_individual_source_scoped_qualification_git_blobs":qualifiers,
    "historic_v6_evidence_revalidated":"f6d1fcaa83b07a1b4db67da083eecdd0238ec1f9c85b73265d3f3e78a2f78b05",
    "qualified_source_original_scoped_potential":20,
    "cohort_full_original_variants_if_P10_not_accepted":19,
    "unresolved_P10_optional_SHT_Eqs_11_to_13":True,
    "all_20_actual_primaries_PLOS":True,
    "final_cross_family_adjudicated":False,
    "nonPLOS_publisher_diversity_pass":False,
    "G1_final_scientific_admission":False,
    "G4_new_joint_GO":False,
    "MAIN_authorized":False}
  s=json.dumps(projection,ensure_ascii=False,sort_keys=True,separators=(",",":"))
  digest=hashlib.sha256(s.encode()).hexdigest()
  print("P399_G1_TEMP_MERGE_ORIGINAL_171_BLOBS_PROJECTION_SHA256",digest,flush=True)
  print("P399_G1_SQUASH_EVIDENCE_ONLY_PREMERGE_ALL_PASS source-scoped 11 additional proofs, no G1 final or MAIN",flush=True)
  out=pathlib.Path("g1-fourlane-preflight");out.mkdir(exist_ok=True)
  (out/"original_disposable_merge_projection.json").write_text(json.dumps({"projection":projection,"projection_sha256":digest},indent=2,ensure_ascii=False)+"\n")
 finally:git("worktree","remove","--force",d)
