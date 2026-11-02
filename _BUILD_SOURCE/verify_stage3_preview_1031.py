"""Real Chromium gallery/guide playback, decoded audio and stable roster links."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/stage3_amplify_1031';errors=[];checks=[]
def ck(n,v,d=None):checks.append({'name':n,'passed':bool(v),'data':d});print('PASS'if v else'FAIL',n,flush=True)
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':980});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto('http://127.0.0.1:8805/enemy-showcase-1031.html?revision=stage3-amplify-1031#enemy=stage3-cryoeye',wait_until='networkidle',timeout=120000);p.wait_for_function('data?.items?.length===164&&v.readyState>=2')
  ck('Enemy guide selects the current four-laser Cryoeye',p.evaluate('selected.id==="stage3-cryoeye"&&v.currentSrc.includes("stage3-cryoeye-1031.mp4")'))
  old=json.loads((R/'_shots/stage2_amplify_1031/guide-manifest-current.json').read_text());live=p.evaluate('data.items')
  ck('All current non-Stage3 guide films remain intact',all(next(x for x in live if x['id']==q['id'])['video']==q['video']for q in old['items']if q['stage']!=3))
  ck('All13 Stage3 cards point to current ice movies',p.evaluate('data.items.filter(e=>e.stage===3).length===13&&data.items.filter(e=>e.stage===3).every(e=>e.video.startsWith("/current/stage3-"))'))
  p.evaluate('v.currentTime=5');p.wait_for_function('!v.seeking&&v.readyState>=2');before=p.evaluate('v.currentTime');p.evaluate('v.play()');p.wait_for_timeout(650);q=p.evaluate('({time:v.currentTime,audio:v.webkitAudioDecodedByteCount,paused:v.paused,error:v.error?.message})');ck('Guide video seeks and decodes native sound',q['time']>before+.2 and q['audio']>0,q);p.evaluate('v.pause()');p.screenshot(path=str(W/'guide-current.png'))
  p.goto('http://127.0.0.1:8805/current/stage3-amplify-1031.html',wait_until='networkidle');ck('Focused page supplies all8 current films',p.locator('video').count()==8)
  for i in range(8):
   p.evaluate('i=>{const v=document.querySelectorAll("video")[i];v.preload="auto";v.load();}',i)
   p.wait_for_function('i=>document.querySelectorAll("video")[i].readyState>=2',arg=i,timeout=30000)
   p.evaluate('i=>{const v=document.querySelectorAll("video")[i];v.currentTime=Math.min(5,v.duration*.5);}',i);p.wait_for_function('i=>!document.querySelectorAll("video")[i].seeking',arg=i)
   before=p.evaluate('i=>document.querySelectorAll("video")[i].currentTime',i);p.evaluate('i=>document.querySelectorAll("video")[i].play()',i);p.wait_for_timeout(360)
   q=p.evaluate('i=>{const v=document.querySelectorAll("video")[i];v.pause();return{title:v.previousElementSibling.textContent,time:v.currentTime,audio:v.webkitAudioDecodedByteCount,w:v.videoWidth,h:v.videoHeight,error:v.error?.message}}',i)
   ck(q['title']+' plays/seeks with decoded sound',q['time']>before+.15 and q['audio']>0 and q['w']==1280 and q['h']==800 and not q['error'],q)
   p.evaluate('i=>{const v=document.querySelectorAll("video")[i];v.preload="none";v.load();}',i)
  p.screenshot(path=str(W/'focused-page.png'));ck('No preview page, console or asset errors',not errors,errors);b.close()
finally:(W/'guide-checks.json').write_text(json.dumps(checks,indent=2))
assert all(q['passed']for q in checks)
