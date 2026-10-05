#!/usr/bin/env python3
"""P399 G4 W8-G: G1 190-pair audit + source-ancestry graph accelerator.

Source-scoped and fail-closed. Graph signals are triage only and never certify
global genealogical independence.
"""
from __future__ import annotations

import itertools
import json
import re
import subprocess
from collections import Counter, deque
from pathlib import Path

W7_HEAD = "4325a9a4cba4da651e7cdf2617f7bc8b08c90f54"
G1_REF = "c7317da41b15159864c014b8dc53449121c34a2c"
BRANCH = "paper2/p399-g4-w8g-g1-190-genealogy-graph-20261005"
PR_NUMBER = 449
ROOT = Path("research/paper2/p399/g4/genealogy_w8g_g1_190_graph_v1")
PROFILES_PATH = Path("research/paper2/p399/g4/genealogy_accelerator_v1/ORIGINAL_NATIVE_PROFILES_v1.json")
RECON_PATH = Path("research/paper2/p399/g4/genealogy_w7_integration_v1/W7_60_PROFILE_RECONCILIATION_v1.json")
G1_ROSTER_PATH = Path("research/paper2/p399/g1/G1_PILOT20_SCIENTIFIC_ADMISSION_AND_DENOMINATORS_v7.json")
G2_ROSTER_PATH = Path("research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json")
ALLOWED = {
    "DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY",
    "SHARED_CONSTITUENT_ONLY",
    "BOUNDED_SOURCE_NATIVE_DIFFERENCE",
    "UNDERDETERMINED",
}
HEX40 = re.compile(r"^[0-9a-f]{40}$")
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.I)

class W8GError(RuntimeError):
    pass

def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def git_json(ref: str, path: Path):
    return json.loads(git("show", f"{ref}:{path.as_posix()}"))

def git_blob(ref: str, path: str | Path) -> str:
    value = git("rev-parse", f"{ref}:{Path(path).as_posix()}")
    if not HEX40.match(value):
        raise W8GError(f"bad blob for {ref}:{path}")
    return value

def dump(name: str, obj) -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def normdoi(value: str) -> str:
    if not isinstance(value, str):
        raise W8GError("missing DOI")
    x = value.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if x.startswith(prefix):
            x = x[len(prefix):]
    if not DOI_RE.match(x):
        raise W8GError(f"bad DOI: {value}")
    return x

def canonical_pair(a: str, b: str, order: dict[str, int]) -> tuple[str, str]:
    if a == b:
        raise W8GError("self pair")
    if a not in order or b not in order:
        raise W8GError("missing profile/paper in canonicalization")
    return (a, b) if order[a] < order[b] else (b, a)

def enumerate_pairs(ids: list[str]) -> list[tuple[str, str]]:
    if len(ids) != len(set(ids)):
        raise W8GError("duplicate roster IDs")
    rows = list(itertools.combinations(ids, 2))
    if any(a == b for a, b in rows):
        raise W8GError("self pair generated")
    if len(set(rows)) != len(rows):
        raise W8GError("duplicate pair generated")
    return rows

def profile_prov(profile: dict, locus: str) -> list[dict]:
    out = []
    for e in profile.get("original_source_evidence") or []:
        out.append({
            "repository_path": e["repository_path"],
            "repository_git_blob_sha1": e["repository_git_blob_sha1"],
            "source_repository_ref": e["source_repository_ref"],
            "source_locus": locus,
            "edition_sha256": profile.get("edition_sha256"),
        })
    return out

def exact_source(profile: dict, locus: str) -> dict:
    e = (profile.get("original_source_evidence") or [None])[0]
    if not e:
        raise W8GError(f"missing source evidence for {profile['id']}")
    return {
        "repository_path": e["repository_path"],
        "repository_git_blob_sha1": e["repository_git_blob_sha1"],
        "source_repository_ref": e["source_repository_ref"],
        "source_locus": locus,
        "edition_sha256": profile.get("edition_sha256"),
    }

def validate_provenance(items: list[dict], profiles: dict[str, dict]) -> None:
    if not items:
        raise W8GError("empty provenance")
    for p in items:
        if not HEX40.match(str(p.get("repository_git_blob_sha1", ""))):
            raise W8GError("bad provenance blob")
        if not HEX40.match(str(p.get("source_repository_ref", ""))):
            raise W8GError("bad provenance ref")
        if git_blob(p["source_repository_ref"], p["repository_path"]) != p["repository_git_blob_sha1"]:
            raise W8GError("provenance blob drift")
        owner = p.get("profile_id")
        if owner and p.get("edition_sha256") != profiles[owner].get("edition_sha256"):
            raise W8GError("source edition mismatch")

def pair_rules(profiles: dict[str, dict], order: dict[str, int]) -> dict[tuple[str, str], dict]:
    def src(pid: str, locus: str) -> dict:
        x = exact_source(profiles[pid], locus)
        x["profile_id"] = pid
        return x
    raw = [
        ("P18", "PF04", "DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY",
         "Both frozen sources explicitly name Daw–Niv–Dayan 2005 as MB/MF ancestry; non-DOI identity is retained as an opaque W8-A-owned node.",
         [src("P18", "source_only_provisional_family_ancestry[0,2]"),
          src("PF04", "formal_review_checks[1].evidence; lineage_science.parent_flat_Daw_2005_overlap_historical_corpus")]),
        ("P11", "P17", "SHARED_CONSTITUENT_ONLY",
         "Both frozen sources explicitly identify diffusion/DDM machinery while also stating that the central updates are not identical.",
         [src("P11", "ancestry_graph[5] PROVISIONAL_DIFFUSION_FAMILY_SHARED"),
          src("P17", "direct_original_ancestry[3] BROAD_DDM_MODEL_SIMILARITY_NOT_CENTRAL_IDENTITY")]),
        ("P15", "P16", "SHARED_CONSTITUENT_ONLY",
         "Both sources contain hippocampal CA3 recurrent/Hebbian constituent machinery, with different learning and remapping operators.",
         [src("P15", "pinned_sources[1]; family_comparison_risk"),
          src("P16", "original_mathematical_ancestor_registry[2]; original Methods Eq1/Eq2")]),
        ("PF01", "P16", "SHARED_CONSTITUENT_ONLY",
         "P16 explicitly flags PF01 as a mandatory attractor-family comparator and states that same attractor class overlap remains unresolved.",
         [src("PF01", "formal qualification source-defined ring attractor/STP center"),
          src("P16", "original_mathematical_ancestor_registry[3]; pre_A_adverse_register[11]")]),
        ("P05", "P06", "BOUNDED_SOURCE_NATIVE_DIFFERENCE",
         "P06 explicitly distinguishes its V1 maximum-response race relation from P05 IVSN/IOR visual-search machinery; this is local only.",
         [src("P05", "new_central_native_model"),
          src("P06", "family_pre_a.already_qualified_P05")]),
        ("P07", "P08", "BOUNDED_SOURCE_NATIVE_DIFFERENCE",
         "Both ledgers explicitly contrast opponent-recursive game inference with temporal HMM/window inference while leaving wider ancestry open.",
         [src("P07", "central_model.P08"),
          src("P08", "source_model_family.P07")]),
        ("P09", "P10", "BOUNDED_SOURCE_NATIVE_DIFFERENCE",
         "The frozen sources distinguish insect KC/PCT learning from human latent-hypothesis/value learning, without global family clearance.",
         [src("P09", "source_native_cross_family_scope.pending_P10"),
          src("P10", "family_provisional.qualified_P09")]),
        ("P11", "P12", "BOUNDED_SOURCE_NATIVE_DIFFERENCE",
         "Both sources explicitly distinguish fitted PBWM gate-demand HDDM from Bayesian LVOC/metareasoning control-policy optimization.",
         [src("P11", "ancestry_graph[4]"),
          src("P12", "direct_original_ancestry_graph[4]")]),
        ("P15", "PF01", "BOUNDED_SOURCE_NATIVE_DIFFERENCE",
         "P15 explicitly contrasts PF01 STP ring-bump machinery with its mixed XCAL-trained hippocampal CA3 learning system.",
         [src("P15", "family_comparison_risk[0]"),
          src("PF01", "formal qualification source-defined ring attractor/STP center")]),
        ("PF01", "PF04", "BOUNDED_SOURCE_NATIVE_DIFFERENCE",
         "PF04 explicitly records a distinct source target relative to PF01 while refusing any inherited-component independence claim.",
         [src("PF01", "formal qualification source-defined ring attractor/STP center"),
          src("PF04", "lineage_science.diversity_relative_to_PF01")]),
    ]
    out = {}
    for a, b, cat, reason, prov in raw:
        key = canonical_pair(a, b, order)
        if key in out:
            raise W8GError("duplicate scientific rule")
        if cat not in ALLOWED:
            raise W8GError("bad scientific category")
        validate_provenance(prov, profiles)
        out[key] = {"category": cat, "reason": reason, "provenance": prov}
    return out

def build_registry(g1_ids: list[str], g1_dois: dict[str, str], profiles: dict[str, dict], rules: dict, order: dict) -> list[dict]:
    if any(i not in profiles for i in g1_ids):
        raise W8GError("missing G1 profile: fail closed")
    rows = []
    for ordinal, (a, b) in enumerate(enumerate_pairs(g1_ids), 1):
        key = canonical_pair(a, b, order)
        rule = rules.get(key)
        cat = rule["category"] if rule else "UNDERDETERMINED"
        prov = rule["provenance"] if rule else (
            profile_prov(profiles[a], "frozen source-native profile; no positive pair ancestry inference")
            + profile_prov(profiles[b], "frozen source-native profile; no positive pair ancestry inference")
        )
        validate_provenance(prov, profiles)
        rows.append({
            "pair_id": f"G1G1::{a}::{b}",
            "ordinal": ordinal,
            "a": a,
            "b": b,
            "doi_a": g1_dois[a],
            "doi_b": g1_dois[b],
            "normalized_scientific_category": cat,
            "scientific_reason": rule["reason"] if rule else "No source-attested direct/shared ancestry or source-scoped pair distinction sufficient for promotion; citation/path absence is not evidence of independence.",
            "provenance": prov,
            "ancestry_exhaustiveness": "NOT_ATTESTED",
            "global_independence_certified": False,
            "main_authorized": False,
        })
    if len(rows) != 190 or len({r["pair_id"] for r in rows}) != 190:
        raise W8GError("G1 190 enumeration drift")
    return rows

def build_graph(all_roster: dict[str, str], profiles: dict[str, dict], unresolved: dict[str, str], rules: dict, order: dict):
    profile_blob = git_blob(W7_HEAD, PROFILES_PATH)
    nodes = []
    for pid, doi in sorted(all_roster.items()):
        nodes.append({
            "node_id": f"paper:{pid}",
            "node_class": "SELECTED_PAPER",
            "paper_id": pid,
            "doi": doi,
            "profile_status": "PROFILE_SOURCE_LEDGER_COMPLETE" if pid in profiles else unresolved.get(pid, "INCOMPLETE"),
            "incomplete": pid not in profiles,
        })
    ancestor_dois = sorted({normdoi(d) for p in profiles.values() for d in (p.get("direct_model_ancestors") or [])})
    selected_dois = set(all_roster.values())
    for doi in ancestor_dois:
        if doi not in selected_dois:
            nodes.append({
                "node_id": f"doi:{doi}",
                "node_class": "ATTESTED_ANCESTOR_WORK",
                "doi": doi,
                "incomplete": False,
            })
    opaque_id = "opaque:w8a:daw_niv_dayan_2005_mb_mf"
    nodes.append({
        "node_id": opaque_id,
        "node_class": "OPAQUE_EXTERNAL_ANCESTOR_PLACEHOLDER",
        "display_label": "Daw Niv Dayan 2005 broad MB/MF comparative precursor",
        "identity_status": "OPAQUE_PENDING_W8A",
        "doi": None,
        "incomplete": True,
        "non_doi_extension": {
            "schema_owner": "W8-A",
            "final_schema": "UNSET",
            "w8g_policy": "fail-closed placeholder only; no DOI or canonical identifier invented",
        },
    })
    node_ids = {n["node_id"] for n in nodes}
    edges = []
    def add_edge(source, target, relation, prov, directed=True, status="SOURCE_ATTESTED"):
        if source not in node_ids or target not in node_ids:
            raise W8GError("edge endpoint missing")
        validate_provenance(prov, profiles)
        eid = f"E::{relation}::{source}::{target}"
        edges.append({
            "edge_id": eid,
            "source": source,
            "target": target,
            "relation_type": relation,
            "directed": directed,
            "status": status,
            "attested": True,
            "provenance": prov,
            "global_independence_implication": False,
        })
    for pid, p in sorted(profiles.items()):
        for anc in sorted(normdoi(x) for x in (p.get("direct_model_ancestors") or [])):
            target = f"paper:{next((q for q, d in all_roster.items() if d == anc), '')}" if anc in selected_dois else f"doi:{anc}"
            if target == "paper:":
                raise W8GError("selected ancestor resolution failure")
            add_edge(
                f"paper:{pid}", target, "DIRECT_ADAPTATION",
                [{
                    "repository_path": PROFILES_PATH.as_posix(),
                    "repository_git_blob_sha1": profile_blob,
                    "source_repository_ref": W7_HEAD,
                    "source_locus": f"profiles[{pid}].direct_model_ancestors::{anc}",
                    "edition_sha256": p.get("edition_sha256"),
                    "profile_id": pid,
                }],
            )
    direct_key = canonical_pair("P18", "PF04", order)
    direct_prov = rules[direct_key]["provenance"]
    add_edge("paper:P18", opaque_id, "EXPLICIT_SHARED_ANCESTOR", direct_prov, True, "OPAQUE_IDENTITY_PENDING_W8A")
    add_edge("paper:PF04", opaque_id, "EXPLICIT_SHARED_ANCESTOR", direct_prov, True, "OPAQUE_IDENTITY_PENDING_W8A")
    for (a, b), rule in sorted(rules.items()):
        if rule["category"] == "SHARED_CONSTITUENT_ONLY":
            add_edge(f"paper:{a}", f"paper:{b}", "SHARED_CONSTITUENT", rule["provenance"], False)
        elif rule["category"] == "BOUNDED_SOURCE_NATIVE_DIFFERENCE":
            add_edge(f"paper:{a}", f"paper:{b}", "BOUNDED_OPERATOR_DIFFERENCE", rule["provenance"], False)
    ids = [e["edge_id"] for e in edges]
    if len(ids) != len(set(ids)):
        raise W8GError("duplicate graph edge")
    return {
        "schema": "relaytheory.p399.g4.w8g.source_ancestry_graph_v1",
        "base_w7_head": W7_HEAD,
        "graph_semantics": "source-attested relations only; topology is triage and cannot certify independence",
        "non_doi_extension_owner": "W8-A",
        "nodes": sorted(nodes, key=lambda n: n["node_id"]),
        "edges": sorted(edges, key=lambda e: e["edge_id"]),
        "incomplete_node_ids": sorted(n["node_id"] for n in nodes if n.get("incomplete")),
        "global_independence_certified": False,
        "main_authorized": False,
    }

def adjacency(graph: dict, ancestry_only=True):
    rels = {"DIRECT_ADAPTATION", "DIRECT_EXTENSION", "DIRECT_IMPLEMENTATION_DESCENT", "EXPLICIT_SHARED_ANCESTOR"}
    out = {}
    for n in graph["nodes"]:
        out[n["node_id"]] = []
    for e in graph["edges"]:
        if ancestry_only and e["relation_type"] not in rels:
            continue
        out[e["source"]].append(e["target"])
        if not e["directed"]:
            out[e["target"]].append(e["source"])
    return out

def reachable(start: str, graph: dict) -> set[str]:
    adj = adjacency(graph, True)
    seen = set()
    q = deque(adj.get(start, []))
    while q:
        x = q.popleft()
        if x in seen:
            continue
        seen.add(x)
        q.extend(adj.get(x, []))
    return seen

def has_undirected_relation(a: str, b: str, relation: str, graph: dict) -> bool:
    aa, bb = f"paper:{a}", f"paper:{b}"
    for e in graph["edges"]:
        if e["relation_type"] != relation:
            continue
        if {e["source"], e["target"]} == {aa, bb}:
            return True
    return False

def derive_signals(registry: list[dict], graph: dict) -> dict:
    rows = []
    for r in registry:
        a, b = r["a"], r["b"]
        na, nb = f"paper:{a}", f"paper:{b}"
        ra, rb = reachable(na, graph), reachable(nb, graph)
        direct = nb in ra or na in rb
        common = sorted((ra & rb) - {na, nb})
        shared = has_undirected_relation(a, b, "SHARED_CONSTITUENT", graph)
        diff = has_undirected_relation(a, b, "BOUNDED_OPERATOR_DIFFERENCE", graph)
        signals = []
        if direct:
            signals.append("DIRECT_ANCESTRY_PATH")
        if common:
            signals.append("COMMON_EXPLICIT_ANCESTOR")
        if shared:
            signals.append("SAME_EXPLICIT_CONSTITUENT")
        if diff:
            signals.append("DIFFERENT_LOCAL_OPERATOR")
        if not signals:
            signals.append("NO_PATH_FOUND")
        score = 100 if direct or common else 80 if shared else 40 if diff else 10
        rows.append({
            "pair_id": r["pair_id"],
            "a": a,
            "b": b,
            "signals": signals,
            "common_ancestor_nodes": common,
            "priority_score": score,
            "scientific_category_snapshot": r["normalized_scientific_category"],
            "triage_only": True,
            "independence_judgment": False,
        })
    rows.sort(key=lambda x: (-x["priority_score"], x["pair_id"]))
    return {
        "schema": "relaytheory.p399.g4.w8g.graph_review_signals_v1",
        "warning": "TRIAGE_ONLY: NO_PATH_FOUND is never INDEPENDENT; DIFFERENT_LOCAL_OPERATOR is never GLOBAL_INDEPENDENT.",
        "count": len(rows),
        "signals": rows,
        "global_independence_certified": False,
        "main_authorized": False,
    }

def validate_graph_edges(graph: dict) -> None:
    node_ids = {n["node_id"] for n in graph["nodes"]}
    edge_ids = set()
    for e in graph["edges"]:
        if e["edge_id"] in edge_ids:
            raise W8GError("duplicate edge")
        edge_ids.add(e["edge_id"])
        if e["source"] not in node_ids or e["target"] not in node_ids:
            raise W8GError("fabricated edge endpoint")
        if e.get("attested") is not True or not e.get("provenance"):
            raise W8GError("fabricated ancestry edge rejected")
        if e.get("global_independence_implication") is not False:
            raise W8GError("graph cannot imply independence")

def build_w9_plan(g1_ids: list[str], g2_ids: list[str]) -> dict:
    g1g1 = len(enumerate_pairs(g1_ids))
    g2g2 = len(enumerate_pairs(g2_ids))
    g2g1 = len(g2_ids) * len(g1_ids)
    total = g1g1 + g2g2 + g2g1
    if (g1g1, g2g2, g2g1, total) != (190, 780, 800, 1770):
        raise W8GError("1770 enumeration drift")
    return {
        "schema": "relaytheory.p399.g4.w8g.w9_1770_enumeration_plan_v1",
        "g1_g1": g1g1,
        "g2_g2": g2g2,
        "g2_g1": g2g1,
        "total": total,
        "canonicalization": "frozen roster order within each cohort; unordered self-free pairs",
        "graph_use": "priority triage only; every scientific judgment must retain source provenance",
        "no_path_policy": "NO_PATH_FOUND => review remains unresolved, never independent",
        "w8a_import": "replace/resolve opaque non-DOI placeholders only through deterministic W8-A/W9 import; W8-G schema is not final",
        "global_independence_certified": False,
        "main_authorized": False,
    }

def main():
    if git("merge-base", "HEAD", W7_HEAD) != W7_HEAD:
        raise W8GError("branch is not descended from exact frozen W7 HEAD")
    g1_doc = git_json(G1_REF, G1_ROSTER_PATH)
    g1 = g1_doc["roster_snapshot"]
    g2 = load(G2_ROSTER_PATH)["selected_working_roster"]
    g1_ids = [x["id"] for x in g1]
    g2_ids = [x["slot"] for x in g2]
    if len(g1_ids) != 20 or len(g2_ids) != 40:
        raise W8GError("roster denominator drift")
    g1_dois = {x["id"]: normdoi(x["doi"]) for x in g1}
    g2_dois = {x["slot"]: normdoi(x["doi"]) for x in g2}
    all_roster = {**g1_dois, **g2_dois}
    if len(all_roster) != 60:
        raise W8GError("selected roster collision")

    profile_doc = load(PROFILES_PATH)
    profiles = {p["id"]: p for p in profile_doc["profiles"]}
    if len(profiles) != 51:
        raise W8GError("W7 profile count drift")
    if any(p.get("global_family_independence_certified") is not False for p in profiles.values()):
        raise W8GError("preexisting independence promotion")
    if any(i not in profiles for i in g1_ids):
        raise W8GError("G1 20 not complete")

    recon = load(RECON_PATH)
    unresolved = {}
    for x in recon["blocked"]:
        unresolved[x["id"]] = x["status"]
    for x in recon["scientific_ancestry_underdetermined"]:
        unresolved[x["id"]] = x["status"]
    if len(unresolved) != 9:
        raise W8GError("W7 unresolved count drift")

    order = {x: i for i, x in enumerate(g1_ids)}
    rules = pair_rules(profiles, order)
    registry = build_registry(g1_ids, g1_dois, profiles, rules, order)
    counts = Counter(r["normalized_scientific_category"] for r in registry)
    direct_shared = counts["DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY"] + counts["SHARED_CONSTITUENT_ONLY"]
    summary = {
        "schema": "relaytheory.p399.g4.w8g.g1_190_summary_v1",
        "exact_pair_count": len(registry),
        "category_counts": dict(sorted(counts.items())),
        "positive_risk_count": direct_shared,
        "direct_or_shared_risk_count": direct_shared,
        "underdetermined_count": counts["UNDERDETERMINED"],
        "global_independence_count": 0,
        "main_authorized": False,
    }

    graph = build_graph(all_roster, profiles, unresolved, rules, order)
    validate_graph_edges(graph)
    signals = derive_signals(registry, graph)
    plan = build_w9_plan(g1_ids, g2_ids)

    registry_doc = {
        "schema": "relaytheory.p399.g4.w8g.g1_190_pair_registry_v1",
        "base_w7_head": W7_HEAD,
        "pair_count": 190,
        "normalized_categories": sorted(ALLOWED),
        "pairs": registry,
        "global_independence_certified": False,
        "main_authorized": False,
    }
    dump("W8G_G1_190_PAIR_REGISTRY_v1.json", registry_doc)
    dump("W8G_G1_190_SUMMARY_v1.json", summary)
    dump("W8G_SOURCE_ANCESTRY_GRAPH_v1.json", graph)
    dump("W8G_GRAPH_DERIVED_REVIEW_SIGNALS_v1.json", signals)
    dump("W8G_W9_1770_ENUMERATION_PLAN_v1.json", plan)

    report = f"""# W8-G 完了報告

- Branch: {BRANCH}
- Draft PR: #{PR_NUMBER if PR_NUMBER else "TBD"}
- frozen W7 base: {W7_HEAD}
- G1×G1: **{len(registry)}/190**
- categories: {json.dumps(dict(sorted(counts.items())), ensure_ascii=False)}
- direct/shared-risk: **{direct_shared}**
- UNDERDETERMINED: **{counts["UNDERDETERMINED"]}**
- graph nodes: **{len(graph["nodes"])}**
- graph edges: **{len(graph["edges"])}**
- incomplete/unresolved graph nodes: **{len(graph["incomplete_node_ids"])}**
- global independence promoted: **0**
- MAIN authorization: **false**

## 科学的境界

W8-G は G1 20件の既存 source qualification を変更しない。P08 の substantive scientific correction、P10 の funding-only correction、P18 final publication authority、P20 main-vs-S1 p-value conflict、PF04 author analytic Eq10 exception を保持する。

Graph は source-attested edge だけを使う triage accelerator であり、NO_PATH_FOUND は独立性を意味しない。DIFFERENT_LOCAL_OPERATOR も global independence を意味しない。非 DOI ancestor は W8-A の最終 schema を先取りせず opaque fail-closed placeholder のまま保持する。

## W9 handoff

W9 は本190行を G1×G1 科学監査入力として取り込み、W7 の780 G2×G2 + 800 G2×G1 と合わせて 1,770 組を再列挙すること。Graph signal は priority ordering にだけ使い、各 pair の科学判定は source provenance を再検証すること。W8-S/W8-A の解決結果は W9 で deterministic import し、W8-G の unresolved/opaque 状態を上書きする場合は provenance と edition identity を保持すること。
"""
    (ROOT / "W8G_COMPLETION_REPORT_JA.md").write_text(report, encoding="utf-8")
    print(json.dumps({
        "pairs": len(registry),
        "categories": dict(sorted(counts.items())),
        "direct_shared_risk": direct_shared,
        "underdetermined": counts["UNDERDETERMINED"],
        "graph_nodes": len(graph["nodes"]),
        "graph_edges": len(graph["edges"]),
        "incomplete_nodes": len(graph["incomplete_node_ids"]),
        "global_independent": 0,
        "main_authorized": False,
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
