#!/usr/bin/env python3
"""First-party INT13 edition witness: 12s direct, Chromium 18s when proof/blocked; metadata only."""
import asyncio,hashlib,io,json,re,os,urllib.request,urllib.error,datetime
from urllib.parse import urlparse
from pypdf import PdfReader
from playwright.async_api import async_playwright
doi='10.1371/journal.pcbi.1014796'
article='https://journals.plos.org/ploscompbiol/article?id='+doi
pdf='https://journals.plos.org/ploscompbiol/article/file?id='+doi+'&type=printable'
old={'html':{'sha':'057e12d6c60605f3f5344b3411e6038397c3f823e09274c4929da9af1afaaca0','bytes':356026},'pdf':{'sha':'5f313f8690f377faaea6b9a3610013c71b880af86634c97dbd4a5344bede9258','bytes':2581474,'pages':31}}
rows=[]
def audit(kind,raw,url,status,mode):
 d={'medium':kind,'method':mode,'status':status,'final_url':url,'firstparty_final_host':urlparse(url).hostname=='journals.plos.org','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
 d['matches_old_uncorrected_sha']=d['sha256']==old[kind]['sha']
 if kind=='html':
  s=raw.decode('utf8','replace');plain=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',s))
  d['proof_banner']=bool(re.search('this is an uncorrected proof',plain,re.I))
  d['doi_and_title']=doi in s and 'Modeling decision dynamics disentangles working memory' in plain
  d['full_sections']=all(re.search(x,s,re.I) for x in ('abstract','introduction','results','methods'))
  d['verified_complete_firstparty_original']=d['firstparty_final_host'] and status==200 and len(raw)>50000 and d['doi_and_title'] and bool(d['full_sections'])
 else:
  d['pdf_signature']=raw.startswith(b'%PDF-')
  if d['pdf_signature']:
   try:
    p=PdfReader(io.BytesIO(raw));d['pages']=len(p.pages);t=' '.join((p.pages[i].extract_text() or '') for i in range(min(len(p.pages),2))).lower()
    d['title_tokens']={w:w in t for w in ('decision','dynamics','memory','learning')}
    d['verified_complete_firstparty_original']=d['firstparty_final_host'] and status==200 and d['pages']>=10 and sum(d['title_tokens'].values())>=3
   except Exception as e:d['pdf_error']=str(e)[:140]
 return d
def direct(kind,url):
 x={'method':'DIRECT_FIRSTPARTY_12S','requested':url}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Accept':'application/pdf,text/html,*/*'})
  with urllib.request.urlopen(req,timeout=12) as r:raw=r.read(12000001);x.update(audit(kind,raw,r.url,r.status,'actual_firstparty_raw_response'))
 except Exception as e:x['error']=type(e).__name__+':'+str(e)[:180]
 rows.append(x);print('INT13_DIRECT',json.dumps(x,sort_keys=True),flush=True)
 return x
async def browser():
 x={'method':'CHROMIUM_AFTER_DIRECT_CHECK','nav_timeout_ms':18000,'requested':article}
 try:
  async with async_playwright() as p:
   b=await p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
   page=await b.new_page(user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36')
   response=await page.goto(article,wait_until='domcontentloaded',timeout=18000)
   dom=(await page.content()).encode('utf8')
   x.update(audit('html',dom,page.url,response.status if response else None,'browser_DOM_NOT_original_raw_html'))
   visible=await page.locator('body').inner_text(timeout=4000)
   x['visible_proof_banner']=bool(re.search('this is an uncorrected proof',visible,re.I))
   try:
    links=await page.locator('a[href*="type=printable"]').evaluate_all('(links)=>links.map(a=>a.href)')
    links=[u for u in links if urlparse(u).hostname=='journals.plos.org']
    x['publisher_printable_links']=links[:2]
    if links:
     resp=await page.request.get(links[0],timeout=12000)
     v=audit('pdf',await resp.body(),resp.url,resp.status,'chromium_context_actual_firstparty_pdf')
     rows.append(v);print('INT13_BROWSER_PDF',json.dumps(v,sort_keys=True),flush=True)
   except Exception as e:x['browser_pdf_error']=type(e).__name__+':'+str(e)[:140]
   await b.close()
 except Exception as e:x['error']=type(e).__name__+':'+str(e)[:180]
 rows.append(x);print('INT13_BROWSER_HTML',json.dumps(x,sort_keys=True),flush=True)
async def main():
 h=direct('html',article);p=direct('pdf',pdf)
 if h.get('proof_banner') or not h.get('verified_complete_firstparty_original') or not p.get('verified_complete_firstparty_original'):await browser()
 result={'schema':'p399_int13_edition_independent_witness.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'doi':doi,'baseline_original_uncorrected':old,'direct_timeout_seconds':12,'browser_timeout_milliseconds':18000,'attempts':rows,'final_version_scientifically_verified':False,'proof_final_equivalence_verified':False,'source_gate':'HOLD_FINAL_VOR','global_family_gate':'UNDETERMINED','main_authorized':False}
 os.makedirs('int13-edition-witness',exist_ok=True)
 with open('int13-edition-witness/receipts.json','w') as f:json.dump(result,f,indent=2,ensure_ascii=False)
 print('INT13_FINAL',json.dumps({'gate':result['source_gate'],'attempts':len(rows)}),flush=True)
if __name__=='__main__':asyncio.run(main())
