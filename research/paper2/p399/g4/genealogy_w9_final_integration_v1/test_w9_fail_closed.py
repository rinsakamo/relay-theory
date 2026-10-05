#!/usr/bin/env python3
import hashlib, json, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent
def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))
def git_bytes(sha, path):
    return subprocess.check_output(["git", "show", f"{sha}:{path}"])
def git_json(sha, path):
    return json.loads(git_bytes(sha, path).decode("utf-8"))

INTAKE=load("W9_W8_IMMUTABLE_INTAKE_RECEIPT_v1.json")
PROF=load("W9_60_PROFILE_FINAL_RECONCILIATION_v1.json")
SCHEMA=load("W9_NON_DOI_ANCESTRY_SCHEMA_DECISION_v1.json")
GRAPH=load("W9_SOURCE_ANCESTRY_GRAPH_v1.json")
REG=load("W9_1770_PAIR_REGISTRY_v1.json")
READJ=load("W9_W8_AFFECTED_PAIR_READJUDICATIONS_v1.json")
CRIT=load("W9_GENEALOGY_CERTIFICATION_CRITERION_v1.json")
SYN=load("W9_CERTIFICATION_SYNTHETIC_PREFREEZE_TESTS_v1.json")
ADV=load("W9_CERTIFICATION_ADVERSE_TESTS_v1.json")
SUM=load("W9_FINAL_GENEALOGY_SUMMARY_v1.json")
CLOSE=load("W9_G4_CLOSURE_DECISION_v1.json")

W8S="de35eba01d214a8dc42f9880371c264566965970"
W8A="fceb4170930b35b54c40439efedb15e906452d09"
W8G="f0f2ebba474ae89c433e0fac8ad18abc397f11d2"
CRIT_COMMIT="15e7541fc5e55ce9c5f1043b05a262e5f4978ac9"
passed=[]

def ok(name, cond):
    if not cond:
        raise AssertionError(name)
    passed.append(name)

# 1-9 exact roster / enumeration invariants.
ids=[p["id"] for p in PROF["profiles"]]
ok("01_exact_60_selected_papers", PROF["final_profile_count"]==60 and len(ids)==60 and len(set(ids))==60)
ok("02_exact_20_g1_40_g2", PROF["partition"]=={"G1":20,"G2":40})
ok("03_exact_190_g1g1", REG["exact_counts"]["G1_G1"]==190 and sum(p["cohort"]=="G1_G1" for p in REG["pairs"])==190)
ok("04_exact_780_g2g2", REG["exact_counts"]["G2_G2"]==780 and sum(p["cohort"]=="G2_G2" for p in REG["pairs"])==780)
ok("05_exact_800_g2g1", REG["exact_counts"]["G2_G1"]==800 and sum(p["cohort"]=="G2_G1" for p in REG["pairs"])==800)
ok("06_exact_1770_total", REG["exact_counts"]["total"]==1770 and len(REG["pairs"])==1770)
ok("07_no_duplicate_pairs", len({p["pair_id"] for p in REG["pairs"]})==1770)
ok("08_no_self_pairs", all(p["a"]!=p["b"] for p in REG["pairs"]))
g1={x:i for i,x in enumerate(REG["roster"]["G1"])}
g2={x:i for i,x in enumerate(REG["roster"]["G2"])}
canonical=True
for p in REG["pairs"]:
    if p["cohort"]=="G1_G1":
        canonical &= g1[p["a"]]<g1[p["b"]]
    elif p["cohort"]=="G2_G2":
        canonical &= g2[p["a"]]<g2[p["b"]]
    elif p["cohort"]=="G2_G1":
        canonical &= p["a"] in g2 and p["b"] in g1
    else:
        canonical=False
ok("09_canonical_pair_ordering", bool(canonical))

# 10 exact immutable W8 HEADs are both recorded and resolvable Git objects.
lane={x["lane"]:x for x in INTAKE["lanes"]}
ok("10_exact_w8_immutable_heads",
   lane["W8-S"]["exact_head"]==W8S and lane["W8-A"]["exact_head"]==W8A and lane["W8-G"]["exact_head"]==W8G)
for sha in (W8S,W8A,W8G):
    subprocess.run(["git","cat-file","-e",sha+"^{commit}"],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

# 11 W8-S mandatory supplement hashes preserved and byte-identical at immutable W8-S HEAD.
receipts=PROF["w8s_official_supplement_receipts"]
ok("11_w8s_mandatory_supplement_hashes_preserved", len(receipts)==9 and all(r.get("sha256") for r in receipts))
for rec in receipts:
    raw=git_bytes(W8S, rec["raw_repository_path"])
    assert hashlib.sha256(raw).hexdigest()==rec["sha256"], rec["raw_repository_path"]

# 12-13 non-DOI safety.
ok("12_w8a_no_fabricated_doi",
   all(n.get("doi") is None and not n["local_node_id"].lower().startswith("doi:") for n in SCHEMA["accepted_nodes"]))
required=("title","authors","year","venue","publishing_authority","descendant_citation_locus","local_node_id")
ok("13_valid_non_doi_identity_required",
   len(SCHEMA["accepted_nodes"])==2 and all(all(n.get(k) for k in required) for n in SCHEMA["accepted_nodes"]))

# 14 independently read final W8-G exact head and verify 190 integrity.
w8g_pairs=git_json(W8G,"research/paper2/p399/g4/genealogy_w8g_g1_190_graph_v1/W8G_G1_190_PAIR_REGISTRY_v1.json")
w8g_graph=git_json(W8G,"research/paper2/p399/g4/genealogy_w8g_g1_190_graph_v1/W8G_SOURCE_ANCESTRY_GRAPH_v1.json")
w8g_counts={}
for p in w8g_pairs["pairs"]:
    c=p["normalized_scientific_category"]; w8g_counts[c]=w8g_counts.get(c,0)+1
ok("14_w8g_g1_190_integrity",
   len(w8g_pairs["pairs"])==190 and len(w8g_graph["nodes"])==81 and len(w8g_graph["edges"])==31 and
   w8g_counts=={"UNDERDETERMINED":180,"BOUNDED_SOURCE_NATIVE_DIFFERENCE":6,"SHARED_CONSTITUENT_ONLY":3,"DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY":1})

# 15-25 fail-closed certification requirements.
pairs=REG["pairs"]
ok("15_direct_ancestry_cannot_become_independence",
   all(p["certification_state"]=="BLOCKED_BY_POSITIVE_ANCESTRY" for p in pairs if p["normalized_scientific_category"]=="DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY"))
ok("16_shared_constituent_cannot_become_independence",
   all(p["certification_state"]=="BLOCKED_BY_SHARED_CONSTITUENT" for p in pairs if p["normalized_scientific_category"]=="SHARED_CONSTITUENT_ONLY"))
ok("17_no_graph_path_cannot_become_independence",
   "NO_PATH_FOUND never implies independence" in CRIT["criterion_core"]["non_evidence_rules"] and SUM["certification"]["bounded_genealogy_clearance"]==0)
ok("18_bounded_difference_cannot_auto_become_independence",
   all(p["certification_state"]!="BOUNDED_GENEALOGY_CLEARANCE" for p in pairs if p["normalized_scientific_category"]=="BOUNDED_SOURCE_NATIVE_DIFFERENCE"))
missing=next(t for t in SYN["tests"] if t["id"]=="missing_supplement")
ok("19_incomplete_source_cannot_receive_clearance", missing["observed"]=="BLOCKED_BY_INCOMPLETE_SOURCE")
unresolved=next(t for t in SYN["tests"] if t["id"]=="local_operator_difference_with_unresolved_higher_ancestry")
ok("20_unresolved_ancestry_cannot_receive_clearance", unresolved["observed"]=="BLOCKED_BY_UNRESOLVED_ANCESTRY")
correction=next(t for t in SYN["tests"] if t["id"]=="correction_changes_decisive_science")
ok("21_correction_edition_mismatch_blocks_affected_certification", correction["observed"]=="BLOCKED_BY_EDITION_CONFLICT")
positive=next(t for t in SYN["tests"] if t["id"]=="same_ancestor_but_different_descendant_operator")
ok("22_positive_shared_ancestry_overrides_clearance", positive["observed"]=="BLOCKED_BY_POSITIVE_ANCESTRY")
ok("23_criterion_result_deterministic", SYN["all_pass"] and SYN["pass_count"]==SYN["total"]==15)
ok("24_criterion_applied_only_after_freeze",
   CRIT["freeze"]["frozen_before_final_1770_application"] and REG["authority"]["criterion_freeze_commit"]==CRIT_COMMIT)
ok("25_no_global_independence_from_lexical_model_label_heuristics",
   all(not p["global_independence_certified"] for p in pairs) and REG["certification_state_counts"].get("BOUNDED_GENEALOGY_CLEARANCE",0)==0)

# 26-28 isolation / MAIN NO-GO.
ok("26_main_authorization_remains_false",
   not INTAKE["scientific_main_authorized"] and not PROF["scientific_main_authorized"] and not GRAPH["scientific_main_authorized"] and not REG["scientific_main_authorized"] and not CLOSE["scientific_main_authorized"])
ok("27_no_grammar_h0_h1_h2_dependency", SUM["dependencies"]["grammar_v0"]==[] and SUM["dependencies"]["h0_h1_h2"]==[])
ok("28_no_preliminary_main_artifact_dependency", SUM["dependencies"]["preliminary_main_artifacts"]==[])

# Additional destructive/adverse integrity.
ok("29_exact_495_w8_affected_rows", READJ["affected_w7_pair_count"]==495 and READJ["category_changes"]==0)
ok("30_exact_final_category_counts",
   REG["normalized_pair_category_counts"]=={"UNDERDETERMINED":1514,"BOUNDED_SOURCE_NATIVE_DIFFERENCE":210,"SHARED_CONSTITUENT_ONLY":44,"DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY":2})
ok("31_zero_bounded_genealogy_clearance", REG["certification_state_counts"].get("BOUNDED_GENEALOGY_CLEARANCE",0)==0)
ok("32_global_adverse_all_pass", ADV["global_adverse_audit"]["all_pass"] and ADV["global_adverse_audit"]["pass_count"]==ADV["global_adverse_audit"]["total"])
ok("33_g4_bounded_closure", CLOSE["layers"]["D_g4_scientific_closure"]=="G4_CLOSED_WITH_EXPLICIT_BOUNDED_LIMITATIONS")
ok("34_graph_counts_self_consistent", GRAPH["node_count"]==len(GRAPH["nodes"]) and GRAPH["edge_count"]==len(GRAPH["edges"]))
ok("35_graph_edges_have_exact_git_provenance",
   all(e.get("exact_evidence_source",{}).get("repository_git_blob_sha1") and e.get("exact_evidence_source",{}).get("source_repository_ref") for e in GRAPH["edges"]))
ok("36_only_one_opaque_graph_node", GRAPH["unresolved_node_ids"]==["opaque:w8a:daw_niv_dayan_2005_mb_mf"])
ok("37_w8g_ci_caveat_not_hidden",
   lane["W8-G"]["reported_ci"]["exact_head_ci_match"] is False and lane["W8-G"]["exact_head_w9_revalidation"]["status"]=="PASS")

print(f"W9 fail-closed destructive/synthetic tests PASS: {len(passed)}/{len(passed)}")
