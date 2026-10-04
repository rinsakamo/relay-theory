#!/usr/bin/env python3
"""Scoped hash/media verifier for the user-provided INT-01 Blink MHT.
No copyrighted article/figure assets are output. This is NOT a scientific-semantic, edition or family test.
Run: python G2D_V15_VERIFY_USER_INT01_MHT_SOURCE_MEDIA.py --archive /private/path/to/source.mht
"""
import argparse,hashlib,json
from email import policy
from email.parser import BytesParser
from html.parser import HTMLParser
from pathlib import Path
MHT_SHA="32158948f6d1f4ffd7170393c30a5742ce7db1b0a871928f64bd176cf9ab3b64"
HTML_SHA="0c6c2670f715b06e3a9596cf848df9e08bb5b5168d5dd57113730d3d50b8fc52"
class Scope(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=set();self.headings=[];self.images=[];self._heading=None;self._chunks=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get("id"):self.ids.add(a["id"])
  if tag in ("h2","h3","h4"):
   if self._heading:self.flush()
   self._heading=tag;self._chunks=[]
  if tag=="img":self.images.append(a.get("src",""))
 def handle_data(self,data):
  if self._heading:self._chunks.append(data)
 def handle_endtag(self,tag):
  if tag==self._heading:self.flush()
 def flush(self):
  self.headings.append(" ".join("".join(self._chunks).split()));self._heading=None;self._chunks=[]
def verify(path):
 b=Path(path).read_bytes();r={"schema":"g2d.int01.user_mht_scoped_media_verify.v15","mht_sha256":hashlib.sha256(b).hexdigest(),"mht_bytes":len(b),"checks":{}}
 c=r["checks"];c["raw_uploaded_archive_sha"]=r["mht_sha256"]==MHT_SHA
 if not c["raw_uploaded_archive_sha"]:return r
 msg=BytesParser(policy=policy.default).parsebytes(b)
 htmls=[p.get_payload(decode=True) for p in msg.walk() if p.get_content_type()=="text/html" and "S0010027724002531" in (p.get("Content-Location") or "")]
 c["one_article_html_mime_part"]=len(htmls)==1
 if not c["one_article_html_mime_part"]:return r
 h=htmls[0];r["html_sha256"]=hashlib.sha256(h).hexdigest();r["html_bytes"]=len(h);c["html_part_sha"]=r["html_sha256"]==HTML_SHA
 c["doi_pii_identifiers"]=b"10.1016/j.cognition.2024.105967" in h and b"S0010027724002531" in h
 s=Scope();s.feed(h.decode("utf-8",errors="replace"))
 c["main_five_sections"]=all(any(k in t for t in s.headings) for k in ["1. Introduction","2. Methods","3. Results","4. Discussion","5. Conclusions"])
 c["appendix_A_and_B_embedded"]=all(any(k in t for t in s.headings) for k in ["Appendix A. Supplementary Methods","Appendix B. Supplementary Figures"])
 c["seven_main_eight_appendix_figure_ids"]=all(x in s.ids for x in ["fig"+str(i) for i in range(1,8)]+["figB."+str(i) for i in range(1,9)])
 c["both_algorithm_image_ids"]=all(x in s.ids for x in ("dfig1","dfig2"))
 images={p.get("Content-Location"):p.get_payload(decode=True) for p in msg.walk() if p.get("Content-Location") and p.get_content_type().startswith("image/")}
 local=[x for x in s.images if "S0010027724002531" in x]
 c["all_article_image_references_have_mime_parts"]=len(local)>=40 and all(x in images for x in local)
 jpg=[v for k,v in images.items() if "S0010027724002531" in k and k.lower().endswith(".jpg")]
 c["at_least_41_article_fig_and_inline_math_jpegs"]=len(jpg)>=41
 r["gates"]={"independent_elsevier_http_raw_verified":False,"publisher_pdf_raw_verified":False,"printed_likelihood_equation_semantically_reconciled":False,"complete_model_science_admitted":False,"global_family_independence_admitted":False,"main_authorized":False}
 c["reject_false_direct_acquisition"]=not r["gates"]["independent_elsevier_http_raw_verified"]
 c["reject_false_science_or_main_go"]=not any(r["gates"].values())
 return r
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--archive",required=True);args=ap.parse_args()
 r=verify(args.archive);r["passed"]=sum(r["checks"].values());r["total"]=len(r["checks"]);r["pass"]=bool(r["checks"]) and all(r["checks"].values())
 print(json.dumps(r,indent=2,ensure_ascii=False));raise SystemExit(0 if r["pass"] else 2)
