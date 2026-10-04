#!/usr/bin/env python3
"""Physical original same-article publisher S1 EPS provenance and source-viz validation."""
import hashlib,os,pathlib,json,urllib.request,subprocess
u="https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1010589.s002&type=supplementary"
with urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"RelayTheory-W3-scoped-source-verification"}),timeout=40) as r:
 raw=r.read(15_000_001);final=r.url;ctype=r.headers.get("content-type")
rec={"source":u,"final_url":final,"content_type":ctype,"raw_bytes":len(raw),"raw_sha256":hashlib.sha256(raw).hexdigest(),
 "publisher_derived_original":True,"actual_provenance":"direct_PLOS_2022_same_article_S1_Fig","not_science_stage":True}
assert raw.startswith(b"%!PS"),("P15 S1 input source EPS magic invalid",raw[:16])
rec["eps_valid_signature"]=True
# Publisher source can contain actual EPS BoundingBox; require or report for original image completeness.
header=raw[:5000].decode("latin1","replace")
rec["has_eps_boundingbox"]="%%BoundingBox:" in header
rec["source_visual_rasterized"]=False
eps=pathlib.Path(os.environ.get("RUNNER_TEMP","/tmp"))/"w3_p15_s1_original.eps";eps.write_bytes(raw)
if subprocess.run(["bash","-lc","command -v gs"],capture_output=True).returncode==0:
 dst=eps.with_suffix(".png")
 proc=subprocess.run(["gs","-dSAFER","-dBATCH","-dNOPAUSE","-sDEVICE=png16m","-r80","-sOutputFile="+str(dst),str(eps)],capture_output=True,timeout=60)
 rec["source_visual_rasterized"]=proc.returncode==0 and dst.exists() and dst.stat().st_size>3000
 rec["image_bytes"]=dst.stat().st_size if dst.exists() else None
assert rec["has_eps_boundingbox"]
assert rec["source_visual_rasterized"],"EPS graphic semantic review gated on actual successful rasterisation"
out=pathlib.Path(os.environ.get("RUNNER_TEMP","/tmp"))/"W3_P15_original_S1_EPS_source_receipt.json"
out.write_text(json.dumps(rec,indent=2)+"\n")
print("ORIGINAL_P15_S1_EPS",json.dumps(rec),flush=True)
