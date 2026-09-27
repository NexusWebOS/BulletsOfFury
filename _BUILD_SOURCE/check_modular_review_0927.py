"""Check the review's real media, links, browser errors and ending routing."""
import base64,http.server,json
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/modular_roster_0927')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1280,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  root=f'http://127.0.0.1:{port}'
  p.goto(root+'/_shots/modular_roster_0927/review.html',wait_until='networkidle')
  report['media']=p.evaluate('''async()=>{const videos=[...document.querySelectorAll('video')];return await Promise.all(videos.map(v=>new Promise(resolve=>{const done=()=>resolve({src:v.getAttribute('src'),duration:v.duration,width:v.videoWidth,height:v.videoHeight,error:v.error?.message||null});if(v.readyState>=1)done();else{v.onloadedmetadata=done;v.onerror=done;v.load();}})));}''')
  p.evaluate("()=>document.querySelectorAll('details').forEach(d=>d.open=true)")
  p.evaluate("()=>document.querySelectorAll('img').forEach(i=>i.loading='eager')")
  p.wait_for_function("()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0)")
  report['images']=p.evaluate("()=>[...document.images].map(i=>({src:i.getAttribute('src'),width:i.naturalWidth}))")
  report['links']=[]
  for href in p.locator('a').evaluate_all('(a)=>a.map(e=>e.href)'):
   res=p.request.get(href);report['links'].append({'url':href.replace(root,''),'status':res.status})
  p.screenshot(path=str(OUT/'review-page.png'),full_page=True)
  p.goto(root+'/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  report['ending']=[]
  for true in [False,True]:
   report['ending'].append(p.evaluate('''flag=>{run.mode='campaign';run.pilot='cole';drawVictory._ready=true;drawVictory._trueEnding=flag;drawVictory._t=VICTORY_DISH_AT+.02;drawVictory._sfx={};drawVictory(1/60);return {trueEnding:flag,time:drawVictory._t,atResultCard:drawVictory._t>=VICTORY_CARD_AT};}''',true))
  report['errors']=errors;br.close()
finally:stop()
(OUT/'review-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
assert len(report['media'])==6 and all(v['width']>0 and v['duration']>20 and not v['error'] for v in report['media'])
assert all(l['status']==200 for l in report['links'])
assert report['ending'][0]['atResultCard'] and not report['ending'][1]['atResultCard']
assert not errors,errors
print(json.dumps(report,indent=2))
