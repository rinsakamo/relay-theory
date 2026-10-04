#!/usr/bin/env python3
"""W3 P16 independent *history and structural inventory only* audit.
NO independent original publisher PDF acquisition or scientific qualification.
"""
import hashlib,json,pathlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
PREFIX="research/paper2/p399/g1/parallel/W3/"
stages=[
("PRE_A","P16_PRE_A_original_source_freeze_v1.json","09519d43dcf73ba0d18be443298528723b5cf8fa"),
("A","P16_A_source_native_v1.json","998dd41220b4365c2572cdcdd4e0ff7a460967ac"),
("B","P16_B_reaudit_complete_frozen_A_v1.json","8aa8bf28eda3e3dc42d8fae9a6518757e5fb36c9"),
("C","P16_C1C2_source_closed_v1.json","273193a55fe605c6d623efc05fcb8c81061c6462"),
("D","P16_D_unchanged_grammar_v0_v1.json","dcca60ef6b26227d3bb13de924a414dfa79a437f"),
("E","P16_E_original_source_fidelity_v1.json","b3f742422e12c07298b339d1e5067a7266781679")]
def git(*args):
    return subprocess.check_output(["git",*args])
records=[];objects={};prev=None
for name,file,commit in stages:
    path=PREFIX+file
    original=git("show",f"{commit}:{path}")
    current=(ROOT/file).read_bytes()
    assert original==current, f"immutable original scientific stage mutated: {name}"
    introduction=git("log","--diff-filter=A","--format=%H","HEAD","--",path).decode().splitlines()
    assert introduction==[commit],f"stage original introduction mismatch: {name}, {introduction}"
    assert subprocess.run(["git","merge-base","--is-ancestor",commit,"HEAD"],check=False).returncode==0
    if prev: assert subprocess.run(["git","merge-base","--is-ancestor",prev,commit],check=False).returncode==0
    prev=commit
    objects[name]=json.loads(original)
    records.append({"stage":name,"first_introduction_commit":commit,"raw_bytes":len(original),"raw_sha256":hashlib.sha256(original).hexdigest()})
A,B,C,D,E=(objects[k] for k in ["A","B","C","D","E"])
assert len(A["original_claims"])==29 and len(A["source_local_dependencies"])==35
assert set(B["review_all_A_claim_ids"])=={x["id"] for x in A["original_claims"]}
assert set(B["review_all_dependency_ids"])=={x["id"] for x in A["source_local_dependencies"]}
assert len(B["findings"])==12 and len(B["source_order_full_sweep"])==17
assert C["before_any_patch_reopen_complete_original_A"]["A_git_blob"]==records[1]["first_introduction_commit"] or C["before_any_patch_reopen_complete_original_A"]["A_git_blob"]
assert len(C["adjudications"])==12 and len(C["adjacent_negative_C2_unique"])==13 and len(C["append_only_source_supported_deltas"])==1
assert len(D["complete_A_roles"])==29 and len(D["all_source_dependencies_preserved"])==35
assert {x["claim_id"] for x in D["complete_A_roles"]}=={x["id"] for x in A["original_claims"]}
assert len(E["fidelity_targets"])==12 and len(E["all_original_C_unique_negatives"])==13
assert set(E["all_A_claim_ids"])==set(B["review_all_A_claim_ids"])
assert set(E["all_A_dependency_ids"])==set(B["review_all_dependency_ids"])
assert E["separate_scoped_qualification_status"]=="PENDING_REAL_AFTER_E_INDEPENDENT_GITHUB_ACTIONS"
# Illustrative integrity controls only: show forbidden mutation cannot be a byte-for-byte match.
assert hashlib.sha256((ROOT/stages[1][1]).read_bytes()+b"\n").hexdigest()!=records[1]["raw_sha256"]
assert records[0]["first_introduction_commit"]!=records[-1]["first_introduction_commit"]
assert len(A["original_claims"])-1!=29
assert len(C["adjacent_negative_C2_unique"])-1!=13
out={"result":"PASS_HISTORY_ONLY_NOT_AFTER_E_SOURCE_AUDIT","frozen_original_git_stage_records":records,
"counts":{"claims":29,"dependencies":35,"adverse":13,"E_targets":12,"stages":6},
"illustrative_mutation_guards":4,
"original_publisher_exact_after_E_reacquisition_success":False,
"scientific_qualification_issued":False,"MAIN_authorized":False}
print(json.dumps(out,indent=2,sort_keys=True),flush=True)
pathlib.Path("w3-p16-history-only").mkdir(exist_ok=True)
pathlib.Path("w3-p16-history-only/receipt.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
