#!/usr/bin/env python3
"""W1 critical previously uncovered mathematically decisive ORIGINAL publisher PDF pages.
Publisher HTTP failures remain explicit BLOCKERS and preserve prior success SHA receipts.
"""
import hashlib,json,pathlib,time,urllib.request
from io import BytesIO
from pypdf import PdfReader
import fitz
D=pathlib.Path('w1-decisive-original-pages');D.mkdir(exist_ok=True)
S=[
('P06','10.1371/journal.pcbi.1004375','50a8e9fb16bbb00eab02a934a629fe43a7142456206df7b6e5331d33c561da15',39,[28,29,30,31,32,33,34,35]),
('P08','10.1371/journal.pcbi.1005418','58ab19b12c6bf637329645f67889d11914a701e511744a784091d52958f1cd08',20,[13,14,15,16,17,18]),
('P10','10.1371/journal.pcbi.1010699','36839ae5557a296d73903089523328d75b5e0300fc3e6fca3be18d53a2c9c5d4',22,[17,18,19,20,21])
]
result=[]
for name,doi,sha,pages,render in S:
    url='https://journals.plos.org/ploscompbiol/article/file?id='+doi+'&type=printable'
    row={'name':name,'url':url,'success':False,'source_status':'TARGETED_ADDITIONAL_ORIGINAL_VISUAL_SCIENCE_NOT_THE_POSTE_AUDIT','http_attempts':[]}
    for attempt in range(1,5):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'RelayTheory-W1-original-science-source-qualification/1.0'})
            data=urllib.request.urlopen(req,timeout=80).read()
            if not data.startswith(b'%PDF'):raise ValueError('NOT_PDF')
            h=hashlib.sha256(data).hexdigest()
            r=PdfReader(BytesIO(data))
            if h!=sha or len(r.pages)!=pages:raise ValueError('ORIGINAL_RAW_HASH_OR_PAGES_CHANGED')
            doc=fitz.open(stream=data,filetype='pdf')
            row.update({'success':True,'raw_sha256':h,'bytes':len(data),'pages':pages,'rendered_pages':[]})
            for i in render:
                pix=doc[i].get_pixmap(matrix=fitz.Matrix(1.55,1.55),alpha=False)
                pix.save(str(D/(name+'-page'+str(i+1)+'.png')))
                row['rendered_pages'].append(i+1)
            break
        except Exception as exc:
            row['http_attempts'].append({'n':attempt,'exception':repr(exc)})
            if attempt<4:time.sleep(4*attempt)
    result.append(row)
    print(json.dumps(row),flush=True)
(D/'real_targeted_pages_metadata.json').write_text(json.dumps(result,indent=2)+'\n')
assert all(x['success'] for x in result), 'BOUNDED_RENDER_MISSING_OR_HTTP_SOURCE_BLOCKER'

# Post-E targeted publisher source recovery attempt; previous 502 executions preserved unchanged.
