"""Decode review media and verify links, visible page and browser errors."""
import json,http.server
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
OUT=Path('_shots/director_0927');errors=[];report={}
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1280,'height':1000});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  root=f'http://127.0.0.1:{port}';p.goto(root+'/_shots/director_0927/review.html',wait_until='networkidle')
  report['media']=p.evaluate("""async()=>Promise.all([...document.querySelectorAll('video')].map(v=>new Promise(resolve=>{const done=()=>resolve({src:v.getAttribute('src'),duration:v.duration,width:v.videoWidth,height:v.videoHeight,error:v.error?.message||null});if(v.readyState>=1)done();else{v.onloadedmetadata=done;v.onerror=done;v.load();}})))""")
  report['posters']=[]
  for src in p.locator('video').evaluate_all('(a)=>a.map(e=>e.poster)'):
   report['posters'].append({'src':src.replace(root,''),'status':p.request.get(src).status})
  report['links']=[]
  for href in p.locator('a').evaluate_all('(a)=>a.map(e=>e.href)'):
   report['links'].append({'url':href.replace(root,''),'status':p.request.get(href).status})
  p.screenshot(path=str(OUT/'review-top.png'))
  report['errors']=errors;br.close()
finally:stop()
(OUT/'review-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
assert len(report['media'])==7 and all(v['width']>0 and v['duration']>=7 and not v['error'] for v in report['media'])
assert all(r['status']==200 for r in report['links']+report['posters'])
assert not errors,errors
