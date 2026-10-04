#!/usr/bin/env python3
"""W1 targeted source reacquisition ONLY. No scientific qualification is implied."""
import hashlib, json, os, pathlib, re, sys, time
from urllib.request import Request, urlopen
from pypdf import PdfReader
from io import BytesIO
OUT = pathlib.Path("w1-source-probe")
OUT.mkdir(exist_ok=True)
ROOT = "https://journals.plos.org/ploscompbiol/article/file?id="
ROWS = [
 ("P06","10.1371/journal.pcbi.1004375","printable","50a8e9fb16bbb00eab02a934a629fe43a7142456206df7b6e5331d33c561da15",39,"main"),
 ("P08","10.1371/journal.pcbi.1005418","printable","58ab19b12c6bf637329645f67889d11914a701e511744a784091d52958f1cd08",20,"main"),
 ("P08-CORRECTION","10.1371/journal.pcbi.1005908","printable",None,3,"correction"),
 ("P08-S1","10.1371/journal.pcbi.1005418.s001","supplementary",None,None,"official_docx"),
 ("P10","10.1371/journal.pcbi.1010699","printable","36839ae5557a296d73903089523328d75b5e0300fc3e6fca3be18d53a2c9c5d4",22,"main"),
 ("P10-CORRECTION","10.1371/journal.pcbi.1010775","printable",None,1,"correction"),
 ("P10-S1TEXT","10.1371/journal.pcbi.1010699.s005","supplementary",None,None,"essential_math"),
 ("P10-S4FIG","10.1371/journal.pcbi.1010699.s004","supplementary",None,None,"model_alternatives"),
]
anchors = {
"P06":{0:["Saliency","Zhaoping"],5:["reaction","salien"],6:[],7:[],8:[],9:[],10:["salien"],11:[],12:[],13:[],14:[],15:[],16:[],17:[],18:[],19:[],20:[],21:[],22:[],23:[],24:[],25:[],26:[]},
"P08":{0:["FitzGerald","Sequential inference"],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[]},
"P08-CORRECTION":{0:[],1:["filtering","optimal"],2:[]},
"P10":{4:[],5:[],6:[],7:[],8:[],9:["Fig","Model"],10:[],11:[],12:[],13:[],14:["Feature","reinforcement"],15:["Bayesian","hypothesis"],16:["hypothesis","switch"],17:[],18:[]},
"P10-CORRECTION":{0:["Funding","supported"]},
"P10-S1TEXT":{0:["hypothesis"],1:[]},
"P10-S4FIG":{0:[]},
}
rows=[]
ok=True
for name,doi,kind,expected,pages,scope in ROWS:
    url=ROOT+doi+"&type="+kind
    rec={"name":name,"doi":doi,"url":url,"scope":scope,"success":False}
    for attempt in range(1,4):
        try:
            data=urlopen(Request(url,headers={"User-Agent":"RelayTheory-W1-original-science-source-qualification/1.0"}),timeout=50).read()
            if kind=="printable" or name in ["P10-S1TEXT","P10-S4FIG"]:
                if not data.startswith(b"%PDF"): raise ValueError("NOT_PDF")
                reader=PdfReader(BytesIO(data))
                n=len(reader.pages)
                rec["pages"]=n
                if pages is not None and n!=pages:raise ValueError("PAGE_MISMATCH")
                hits=[]
                for idx,need in anchors.get(name,{}).items():
                    if idx>=n: raise ValueError("ANCHOR_PAGE_OUT_OF_RANGE")
                    t=reader.pages[idx].extract_text() or ""
                    found=[str(z) for z in need if re.search(re.escape(z),t,re.I)]
                    hits.append({"page_1based":idx+1,"required":need,"found":found,"text_extract_chars":len(t)})
                rec["bounded_text_probes"]=hits
            elif name=="P08-S1":
                if not data.startswith(b"PK"): raise ValueError("NOT_DOCX")
            rec.update({"raw_sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"success":True})
            if expected and rec["raw_sha256"]!=expected:raise ValueError("ORIGINAL_SHA_MISMATCH")
            if kind=="printable" or name in ["P10-S1TEXT","P10-S4FIG"]:
                try:
                    import fitz
                    doc=fitz.open(stream=data,filetype="pdf")
                    for idx in anchors.get(name,{}):
                        page=doc[idx]
                        pix=page.get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False)
                        pix.save(str(OUT/(name+"-page"+str(idx+1)+".png")))
                    rec["rendered_bounded_pages"]=[v+1 for v in anchors.get(name,{})]
                except Exception as e: rec["render_problem"]=str(e)
            break
        except Exception as e:
            rec["last_error"]=repr(e)
            if attempt<3:time.sleep(attempt*2)
    print(json.dumps(rec,ensure_ascii=False),flush=True)
    rows.append(rec)
    if not rec["success"]:ok=False
report={"schema":"relaytheory.g1.W1.real_publisher_source_targeted_probe.v1","scientific_qualification":False,"proof_scope":"actual runner byte SHA/page/targeted rendered pages; zero human equation semantic certification","sources":rows,"all_acquired":ok}
(OUT/"source.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
sys.exit(0 if ok else 2)
