#!/usr/bin/env python3
"""W4 P19 post-E independent original-source and immutable Git-introduction verifier.
No blinded semantic rater or original-model numeric reproduction.
Publisher 502 exception remains explicitly visible even if archival originals match.
"""
import hashlib, io, json, subprocess
from pathlib import Path
from urllib.request import urlopen,Request
from pypdf import PdfReader
from PIL import Image
BASE="research/paper2/p399/g1/parallel/W4/p19/"
STAGES=[
("PRE_A_v2","56c49136f3b80f5e70497569997f0f47fe91f7f4","P19_PRE_A_v2_COMPLETE_ISSUER_DEPOSIT_ORIGINAL_SOURCE_FREEZE.json"),
("A_v2","2a391e4d226d0c3ca4eb17b23c66ff72017205c8","P19_A_v2_FULL_ORIGINAL_MAIN_S1_S8_SOURCE_FIRST.json"),
("B_v2","61a4640cd492f2db3c8741f47d8649652a9a70aa","P19_B_v2_FULL_SOURCE_CHALLENGE.json"),
("C_v2","0eb078d796834828b116dd2f25b16aefb66b026a","P19_C_v2_COMPLETE_SOURCE_CLOSED_ADJUDICATION.json"),
("D_v2","0d870d761a25af46302560639058e3461853dc83","P19_D_v2_FULL_SOURCE_40_62_UNCHANGED_GRAMMAR.json"),
("E_v2","e968ef253e4103bbf3fcbcd8d151ce246f62952f","P19_E_v2_COMPLETE_ORIGINAL_SOURCE_FIDELITY.json")]
SHA={"s001":"c45ab7072bfcbbe91e8e77c83091293cd43d3dc133c94dfb74be89f7de729ab4",
"s002":"a82c34c729e533566c516ad95f08c9403be86dc837874aec85b00e338c958596",
"s003":"483045895785a85097a6602a5cc250119629dae129c8dc3846851d4668293794",
"s004":"e247c7daa7503796d13fd8f539b067a2cee5918a1c4e3a0e7e52f584044a91eb",
"s005":"2fd6809a7f3a963bd73f7ebc875f80a1de8e4c1ed5ff4f6abb1cf62b1043ffe3",
"s006":"c4e8edc3a0caadafb02a1c58a88258674d77ae1f3ea0bb29a9b14076870192fd",
"s007":"1165fb5904735d21d294747bbcb7c66ba73bf94f99bbf55cdfc5550f63343ed8",
"s008":"a3c65317bebf22d0b37ac86612f90ca90d9a46813ad270b7c29422e8cc2ac937"}
MAIN="4ee1e89bb1d0bc0961c86185cee7bb851a25033c2f8f71270212fd6b313deee4"
out=Path("g1-w4-p19-postE");out.mkdir(exist_ok=True);record={"stage":"P19_POST_E","checks":[],"failures":[],"direct_live_publisher_extras_sha":"UNVERIFIED_SIX_ADDITIONAL_ISSUER_HTTP_502"}
def chk(name,ok,details):
    item={"name":name,"pass":bool(ok),"details":details};record["checks"].append(item)
    if not ok:record["failures"].append(item)
    print(json.dumps(item,sort_keys=True),flush=True)
def sha(x):return hashlib.sha256(x).hexdigest()
def git(*args):return subprocess.check_output(["git",*args])
try:
    parent="38c5eb24c61b9e57371084a65fcbcb9fb9c62a4b"
    for stage,commit,name in STAGES:
        path=BASE+name
        intro=git("show",commit+":"+path)
        current=Path(path).read_bytes()
        ancestors=git("merge-base","--is-ancestor",parent,commit)==b""
        chk("historical_original_exact_bytes_"+stage,intro==current and ancestors,{"introduction_commit":commit,"git_sha256":sha(intro),"head_sha256":sha(current)})
        parent=commit
    for before,after in zip(STAGES,STAGES[1:]):
        import subprocess as sp
        check=sp.run(["git","merge-base","--is-ancestor",before[1],after[1]],capture_output=True)
        chk("stage_ancestry_"+before[0]+"_"+after[0],check.returncode==0,{"ancestor":before[1],"descendant":after[1]})
except Exception as e:chk("git_verification_exception",False,repr(e))
original="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1009866&type=printable"
try:
    d=urlopen(Request(original,headers={"User-Agent":"RelayTheory-W4-independent-postE/1"}),timeout=80).read()
    p=PdfReader(io.BytesIO(d))
    chk("original_current_issuer_main_SHA_bytes_pages",sha(d)==MAIN and len(d)==2080943 and len(p.pages)==28,{"sha":sha(d),"bytes":len(d),"pages":len(p.pages)})
    textmap={6:["Dirichlet process"],8:["hierarchical"],16:["interference"]}
    for page,terms in textmap.items():
        t=" ".join((p.pages[page-1].extract_text() or "").split()).lower()
        for term in terms:chk("original_main_text_source_anchor_"+str(page)+"_"+term,term.lower() in t,{"p":page,"anchor":term})
except Exception as e:chk("original_current_issuer_main_unavailable",False,repr(e))
root="https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9744313/"
try:
    import xml.etree.ElementTree as ET
    jats=urlopen(root+"fullTextXML",timeout=70).read()
    tree=ET.fromstring(jats)
    ids=[x.text for x in tree.findall(".//article-id") if x.attrib.get("pub-id-type")=="doi"]
    chk("independent_issuer_deposited_article_DOI_jats", "10.1371/journal.pcbi.1009866" in ids,{"DOIs":ids,"sha":sha(jats)})
    blob=urlopen(root+"supplementaryFiles",timeout=105).read()
    import zipfile
    z=zipfile.ZipFile(io.BytesIO(blob))
    for key,expect in SHA.items():
        name="pcbi.1009866."+key+(".pdf" if key in ("s001","s002","s007","s008") else ".tiff")
        try:
            data=z.read(name)
            fields={"name":name,"sha":sha(data),"bytes":len(data)}
            valid=sha(data)==expect
            if name.endswith(".pdf"):
                pdf=PdfReader(io.BytesIO(data));fields["pages"]=len(pdf.pages)
                if key=="s001":
                    expected=["S1.A Algorithm","S1.B Algorithm","S1.C Algorithm"]
                    for i,text in enumerate(expected):
                        ok=text in " ".join(pdf.pages[i].extract_text().split())
                        chk("S1_actual_original_algorithm_page_"+str(i+1),ok,{"page":i+1,"anchor":text})
                if key=="s007":
                    joined=" ".join(p.extract_text() or "" for p in pdf.pages)
                    chk("S1_table_real_prior_source",("1.25" in joined and "error RT" in joined and "all RT" in joined and "forgetful" in joined),{"page":1,"tokens_check":"truncated original prior"})
            else:
                img=Image.open(io.BytesIO(data));fields["dimensions"]=list(img.size);fields["format"]=img.format
                valid=valid and img.format=="TIFF"
            chk("independent_doi_archival_original_sha_"+key,valid,fields)
        except Exception as e:chk("archival_original_missing_"+key,False,repr(e))
except Exception as e:chk("archive_original_bundle_unavailable",False,repr(e))
# Firstparty S1/S2 independently reacquire, marked non-promotable when issuer remains down.
for key in ("s001","s002"):
    url="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1009866."+key+"&type=supplementary"
    try:
        raw=urlopen(Request(url,headers={"User-Agent":"RelayTheory-W4-independent-postE/1"}),timeout=50).read()
        chk("postE_direct_issuer_against_archival_original_"+key,sha(raw)==SHA[key],{"sha":sha(raw),"bytes":len(raw)})
    except Exception as e:
        chk("postE_direct_issuer_unavailable_"+key,False,repr(e))
record["all_strict_checks_pass"]=not record["failures"]
(out/"P19_POSTE_REAL_SOURCE_AND_GIT_RECEIPT.json").write_text(json.dumps(record,sort_keys=True,ensure_ascii=False,indent=2)+"\n")
print("W4_P19_POST_E_ERRORS",len(record["failures"]),flush=True)
if record["failures"]:raise SystemExit(1)
