# RelayTheory Paper 2 — G4 W9 最終報告

## 1. Authority / branch / PR

- Primary authority: Issue #399
- W9 branch: `paper2/p399-g4-w9-final-genealogy-integration-20261005`
- Draft PR: **#451 — G4 W9 — 60-profile final integration, 1,770-pair genealogy audit, and certification criterion**
- Frozen W7 base: `4325a9a4cba4da651e7cdf2617f7bc8b08c90f54`
- W8-S immutable input: `de35eba01d214a8dc42f9880371c264566965970`
- W8-A immutable input: `fceb4170930b35b54c40439efedb15e906452d09`
- W8-G immutable input: `f0f2ebba474ae89c433e0fac8ad18abc397f11d2`
- Genealogy Certification Criterion v1 freeze commit: `15e7541fc5e55ce9c5f1043b05a262e5f4978ac9`
- Criterion pre-result synthetic-test commit: `30307d04caf17392536a6d262131f405ba184c9b`
- scientific_main_authorized: **false**

W9 は preliminary MAIN outcomes、Grammar-v0 decomposition、H0/H1/H2 classification を参照していない。selected 60-paper roster の変更・backup activation も行っていない。

## 2. Immutable W8 intake

### W8-S
PR #448 / exact HEAD `de35eba...` / exact W7 base — **VALID**。
run 37267531226 は exact HEAD で SUCCESS。5/5 source blockers、9/9 official PLOS raw supplements、SHA256 freeze を確認し、source blocker/conflict は 0。

### W8-A
PR #450 / exact HEAD `fceb417...` / exact W7 base — **VALID**。
run 37267514277 は exact HEAD で SUCCESS。4 ancestry blockers、11 direct ancestry candidates、2 non-DOI bibliographic nodes を scope 内で確認した。

### W8-G
PR #449 / exact HEAD `f0f2eb...` / exact W7 base — **VALID_WITH_EXPLICIT_EXACT_HEAD_W9_REVALIDATION**。

指定 run 37267496395 自体は SUCCESS だが、実際の tested HEAD は `324b550dd78ce90f360f21e33262643507510efe` で、final `f0f2eb...` ではない。post-CI chain は source-attested graph relation label を `DIRECT_MODEL_ANCESTOR` に正規化した `82c4a056...` と completion metadata の final commit である。W9 はこの差を隠さず、final exact HEAD の 190-pair registry と 81-node/31-edge graph invariants を独立再検証した。pair promotion、new target、independence promotion はない。

## 3. Final 60-profile reconciliation

- W7 baseline: **51/60**
- W8-S source-resolved additions: **5**
- W8-A ancestry-resolved additions: **4**
- Final: **60/60 SOURCE-NATIVE PROFILE COMPLETE**
- Remaining profile blockers: **0**
- Partition: **G1=20 / G2=40**

P08 substantive correction、P10 funding-only correction、P18 final publication authority、P20 main-vs-S1 p-value conflict、PF04 author-approved Eq10 analytic exception、PRD-01 correction/manuscript bounded bundle、INT-01 author-selected softmax prepublication interpretation、INT-13 author-approved uncorrected publisher proofをそのまま保持し、silent normalization はしていない。

## 4. Non-DOI ancestry schema

Decision: **ACCEPT_WITH_DOCUMENTED_MODIFICATIONS**。

Identity-safe non-DOI node を **2件**採用した。

1. Liang, Jordan & Klein (2010), *Learning Programs: A Hierarchical Bayesian Approach*, ICML-10.
2. Christian Lebiere (1999), *Blending: An ACT-R Mechanism for Aggregate Retrievals*, Sixth Annual ACT-R Workshop.

`absence of DOI != absence of ancestry` を採用し、DOI は捏造しない。repository-local `rt-biblio-...` ID は外部 identifier ではない。

W8-G の `opaque:w8a:daw_niv_dayan_2005_mb_mf` は、凍結repository evidenceだけでは exact title / venue / locator を identity-safe に確定できないため、shared ancestry evidence を保持したまま unresolved opaque bibliographic node として残した。

## 5. Unified source-ancestry graph

- Nodes: **101**
- Edges: **52**
- Accepted non-DOI bibliographic nodes: **2**
- Remaining opaque/incomplete nodes: **1**
  - `opaque:w8a:daw_niv_dayan_2005_mb_mf`

Graph は source-attested relations のみを保持し、embedding/LLM similarity や用語類似による family edge、weak edge の自動 transitive closure を作っていない。

## 6. Exact 1,770-pair registry

- G1×G1 = **190/190**
- G2×G2 = **780/780**
- G2×G1 = **800/800**
- Total = **1,770/1,770**
- duplicates = **0**
- self-pairs = **0**
- canonical ordering = enforced

Final normalized categories:

| Category | Count |
|---|---:|
| DIRECT_OR_EXPLICIT_SHARED_MODEL_ANCESTRY | 2 |
| SHARED_CONSTITUENT_ONLY | 44 |
| BOUNDED_SOURCE_NATIVE_DIFFERENCE | 210 |
| UNDERDETERMINED | 1,514 |
| **Total** | **1,770** |

W8 affected W7 rowsは **495** 行。normalized category changes は **0**。

- BLF-02↔BLF-03: source gap は解消したが、citation/common vocabulary は direct/shared ancestry も bounded clearance も証明しないため **UNDERDETERMINED** を維持。
- INT-03↔INT-06: W8-A は direct edge を明示的に否定し broader SHARED_FRAMEWORK を残すため、normalized **SHARED_CONSTITUENT_ONLY** を維持。

## 7. Genealogy Certification Criterion v1

Criterion は final 1,770 registry 適用より前に commit `15e7541...` で凍結した。15-case synthetic stress test は real results を見ずに **15/15 PASS**。

Clearance には最低でも、両 profile の source completeness、genealogy-relevant edition/supplement/correction completeness、direct ancestry search、common ancestor search、shared constituent/model-family search、bounded bibliography/source coverage の positive attestation、unresolved ancestor 不在、residual uncertainty の明示を要求する。

以下は clearance evidence ではない。

- NO_DIRECT_EDGE
- NO_PATH_FOUND
- citation absence
- lexical similarity/dissimilarity
- shared/different authorship alone
- same experimental domain
- local operator difference
- BOUNDED_SOURCE_NATIVE_DIFFERENCE

Final certification states:

| Certification state | Count |
|---|---:|
| BLOCKED_BY_POSITIVE_ANCESTRY | 2 |
| BLOCKED_BY_SHARED_CONSTITUENT | 44 |
| BLOCKED_BY_UNRESOLVED_ANCESTRY | 1,724 |
| BOUNDED_GENEALOGY_CLEARANCE | **0** |

**0 clearance は科学的失敗ではない。** 全60 profile の ancestry exhaustiveness は `NOT_ATTESTED` のままであり、Criterion v1 が限定探索を universal independence に変換しないための fail-closed result である。

## 8. Adverse audit / destructive tests

- Pre-result criterion synthetic stress tests: **15/15 PASS**
- Global adverse audit: **15/15 PASS**
- Repository fail-closed test suite: **37 assertions**
  - user-required 28 invariants
  - exact W8-G final-head revalidation
  - 495 affected-pair cardinality
  - exact category counts
  - zero clearance
  - graph provenance / opaque-node invariants

GitHub Actions exact final-HEAD run ID は、その commit 自身には自己参照できないためこの report へ埋め込まない。Draft PR #451 の final check と completion response を exact run authority とする。

## 9. G4 closure

Decision: **G4_CLOSED_WITH_EXPLICIT_BOUNDED_LIMITATIONS**。

これは G4 genealogy audit / certification-design lane の closure であり、global genealogical independence の証明ではない。

Residual limitations:

- UNDERDETERMINED = **1,514**
- bounded genealogy clearance = **0**
- all 60 profiles: `ancestry_exhaustiveness=NOT_ATTESTED`
- unresolved opaque ancestry node = **1**

Global-independence interpretation boundary:

`NO_DIRECT_EDGE != NO_SHARED_ANCESTRY != BOUNDED_SOURCE_NATIVE_DIFFERENCE != GLOBAL_GENEALOGICAL_INDEPENDENCE`。

W9 は global independence を一件も promote しない。

## 10. MAIN

**scientific_main_authorized = false**

W9 は MAIN GO を発行しない。MAIN はユーザーの別途 explicit GO があるまで開始しない。
