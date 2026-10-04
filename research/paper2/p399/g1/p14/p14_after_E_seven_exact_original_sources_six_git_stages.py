#!/usr/bin/env python3
"""P14 independent AFTER E original publisher seven-file scientific package.

Reacquire same official published primary PDF plus publisher S1–S6 originals,
all raw SHA/bytes/pages locked in PRE_A before first scientific A. Assert
selected page-specific textual bounded anchors and git-show exact frozen
PRE_A A B C D E raw bytes/strict Git ancestry and 39/56/19 original-source
coverage. This cannot establish blind scientific semantics or independently
execute author's fMRI model/data numeric analysis; pixels were separately
rendered/reviewed BEFORE PRE_A in earlier scoped actual CI.
"""
import urllib.request,io,hashlib,json,subprocess,pathlib,re
from pypdf import PdfReader
ROOT="research/paper2/p399/g1/p14/"
P=pathlib.Path(__file__).resolve().parent
doi="10.1371/journal.pcbi.1008969"
spec=[
 ("MAIN",None,"cca218ddff9764422316f99fe2cf8cf6a5519462a0b38ac25b45999080b79ec0",2551032,34,[(4,["sequence","repeat"]),(5,["associative","learning"]),(7,["presentation","recoding"]),(8,["Table 1","associative"]),(11,["interference","associative"]),(17,["hamming","item"]),(19,["mixture","recency"]),(20,["dirichlet","chunks"]),(21,["mapping","n-gram"]),(22,["optimal","chunk"]),(23,["Fig 8","evidence"]),(25,["noise","item"]) ]),
 ("S1",1,"f2e9bef0fd311132078f8de1e1ef261649c9d540ab93cba541c7d25534322385",368737,2,[(1,["item mixture","noise"]),(2,["Fig A","novel"])]),
 ("S2",2,"80ff7cca0501b3989fd8ba0867b4dea411f1243b5ca094cc2cecd1c34dd0575b",68383,2,[(1,["recency","primacy"])]),
 ("S3",3,"82f2a03519e5718428303158c27caf21b39937b9841a7581a40eb15901eb2be2",104835,3,[(1,["posterior","model evidence"]),(2,["model evidence","complexity"])]),
 ("S4",4,"044423d324d62b4231f056e704e41582c6bb1e1ab950d196c636322c10046f43",73915,1,[(1,["ABCD","BADC","ABDC"])]),
 ("S5",5,"3aee815baf0f50dcaf4e53f8a3563469ed3d2a89e73038b5e6429ac1aaca51c2",324995,2,[(1,["noise","response times"]),(2,["simulation","noise"])]),
 ("S6",6,"25eddff2e76155d34bd394f97644a6b438154095d72f369830aba239e4cda6d9",51221,1,[(1,["Individual sequences","four"])]),
]
proof={};anchors=0
for name,n,sha,size,pages,tests in spec:
 typ="printable" if n is None else "supplementary"
 pid=doi if n is None else f"{doi}.s{n:03d}"
 url=f"https://journals.plos.org/ploscompbiol/article/file?id={pid}&type={typ}"
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (RelayTheory P14 independent after-E exact issuer 7 original PDF source audit)"}),timeout=130) as f:data=f.read();issuer_url=f.geturl()
 assert data.startswith(b"%PDF") and len(data)==size and hashlib.sha256(data).hexdigest()==sha,"P14_PUBLISHED_ORIGINAL_CHANGED "+name
 reader=PdfReader(io.BytesIO(data),strict=False)
 assert len(reader.pages)==pages,"P14_ORIGINAL_PDF_PAGE_COUNT_CHANGED "+name
 print("P14_AFTER_E_REAL_ISSUER_ORIGINAL_BYTES_PASS",name,sha,size,pages,flush=True)
 checks=[]
 for pg,terms in tests:
  t=re.sub(r"\\s+"," ",reader.pages[pg-1].extract_text() or "").lower()
  found=[w for w in terms if w.lower() in t]
  ok=len(found)==len(terms)
  print("P14_AFTER_E_ORIGINAL_SOURCE_PAGE",name,pg,"PASS" if ok else "FAIL",found,flush=True)
  assert ok,"P14_BAD_TEST_ORIGINAL_ANCHOR "+name+" "+str(pg)
  anchors+=1;checks.append({"one_based_original_pdf_page":pg,"anchors":terms})
 proof[name]={"raw_publisher_sha256":sha,"bytes":size,"pages":pages,"url":issuer_url,"anchors":checks}
stages=[
 ("PRE_A","e52fc7ec6f7fd06f84454b0421a703aa926151cf","P14_PRE_A_PUBLISHED_MAIN_AND_ISSUER_S1_S6_SOURCE_FAMILY_FREEZE_v1.json"),
 ("A","e8375501c468f0897177692e64d9225571a28451","P14_PASS_A_SOURCE_FIRST_MAIN_S1_S6_v1.json"),
 ("B","423aada987c4cbe4b33762be09e2f29167e8031e","P14_PASS_B_RESULT_INFORMED_FULL_A_ALL_ORIGINALS_v1.json"),
 ("C","4d05a468affffb5f98845f487079754ee5ea4ca3","P14_PASS_C1_C2_ORIGINAL_SOURCE_CLOSED_v1.json"),
 ("D","71912c37c8109c8451d7a1cb9a93108456eb5266","P14_PASS_D_UNCHANGED_GRAMMAR_v0_39_56_v1.json"),
 ("E","0921922cfd74c59348a1038cbe7154209a202429","P14_PASS_E_ORIGINAL_MAIN_AND_S1_S6_FIDELITY_v1.json")
]
proof_git={};prev=None
for name,commit,filename in stages:
 actual=subprocess.check_output(["git","show",f"{commit}:{ROOT}{filename}"])
 assert actual==(P/filename).read_bytes(),"P14_FROZEN_SOURCE_SCIENCE_HISTORY_SILENT_MUTATION "+name
 if prev:subprocess.run(["git","merge-base","--is-ancestor",prev,commit],check=True)
 prev=commit
 sh=hashlib.sha256(actual).hexdigest()
 proof_git[name]={"original_stage_intro_git":commit,"original_raw_utf8_sha256":sh,"path":ROOT+filename}
 print("P14_AFTER_E_ORIGINAL_SCIENCE_STAGE_BYTES_PASS",name,sh,flush=True)
A=json.loads((P/stages[1][2]).read_text());B=json.loads((P/stages[2][2]).read_text())
C=json.loads((P/stages[3][2]).read_text());D=json.loads((P/stages[4][2]).read_text());E=json.loads((P/stages[5][2]).read_text())
assert A["count"]["claims"]==len(A["source_first_claims"])==39
assert A["count"]["edges"]==len(A["source_conditional_dependencies"])==56
assert B["complete_original_immutable_A_embedded_before_reviews"]==A
assert B["summary"]["old_A_nodes_reread"]==39 and B["summary"]["old_A_edges_reread"]==56
assert C["C1_original_FROZEN_complete_A_reopened_BEFORE_ANY_PATCH"]["complete_entire_original_A"]==A
assert C["count"]["unique_source_negative_conditions"]==19 and len(C["accepted_append_only_material_source_clarifications"])==3
assert len(D["full_source_claim_39_mapping"])==39 and len(D["original_56_source_dependencies"])==56
assert len(E["original_source_specific_fidelity_targets"])==9
assert E["full_source_claim_coverage"]==39 and E["full_original_A_source_dependency_coverage"]==56
assert E["all_C_material_source_negatives_unique_covered"]==19
assert E["source_edition"]["all34_main_pages_pixel_individually_read"] is False
assert E["E_does_not_automatically_grant_individual_qualification"]
assert E["no_MAIN_exposure"]
print("P14_AFTER_E_FULL_ORIGINAL_PROCEDURAL_PASS issuer7 exact sha raw files, bounded source anchors",anchors,"stage historic originals6/6 and 39/56/19 negative all covered, not blind human model validity",flush=True)
projection={"seven_actual_original_issuer_published_PDF_source_sha_bytes_pages":proof,"six_frozen_real_source_original_stage_git_sha":proof_git,"original_selected_page_text_anchors_count":anchors,"science_claims":39,"source_edges":56,"adverse":19,"semantic_blind_human_validation":False,"numeric_author_pipeline_replayed":False,"whole_G1_20_finished":False}
digest=hashlib.sha256(json.dumps(projection,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
print("P14_AFTER_E_ORIGINAL_MULTI_PDF_PROJECTION_SHA256",digest,flush=True)
pathlib.Path("g1-p14-poste").mkdir(exist_ok=True)
pathlib.Path("g1-p14-poste/source.json").write_text(json.dumps({"projection":projection,"sha256":digest,"stage_qualification_not_autogranted":True},indent=2)+"\n")
