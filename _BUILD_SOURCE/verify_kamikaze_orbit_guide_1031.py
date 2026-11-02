"""Actual Chromium guide selection, seeking and decoded audio for both films."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/kamikaze_orbit_1031';checks=[];errors=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,flush=True)
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':980});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto('http://127.0.0.1:8805/enemy-showcase-1031.html?revision=kamikaze-orbit-1031#enemy=stage1-s1jetdelta-b-2',wait_until='networkidle',timeout=120000);p.wait_for_function('data?.items?.length===163&&v.readyState>=2')
  ck('Guide selects the new earth-camo kamikaze',p.evaluate('selected.id==="stage1-s1jetdelta-b-2"&&v.currentSrc.includes("kamikaze-orbit-1031.mp4")&&selected.title.includes("Earth Camo")'))
  old=json.loads((R/'_shots/stage1_followup_1031/guide-manifest-current.json').read_text());live=p.evaluate('data.items');ck('Other162 guide cards retain their current films',all(next(a for a in live if a['id']==o['id'])['video']==o['video']for o in old['items']if o['id']!='stage1-s1jetdelta-b-2'))
  p.evaluate('()=>{v.currentTime=v.duration*.5;}');p.wait_for_function('!v.seeking&&v.readyState>=2');before=p.evaluate('v.currentTime');p.evaluate('v.play()');p.wait_for_timeout(450);after=p.evaluate('v.currentTime');ck('Guide kamikaze seeks and plays with decoded native sound',after>before+.2 and p.evaluate('v.webkitAudioDecodedByteCount>0'));p.evaluate('v.pause()');p.screenshot(path=str(W/'guide-current.png'))
  p.goto('http://127.0.0.1:8805/current/kamikaze-orbit-1031.html',wait_until='networkidle');ck('Focused page provides single and three-plane clips',p.locator('video').count()==2)
  for i in range(2):
   p.wait_for_function('i=>document.querySelectorAll("video")[i].readyState>=2',arg=i)
   p.evaluate('i=>{document.querySelectorAll("video")[i].currentTime=5;}',i);p.wait_for_function('i=>!document.querySelectorAll("video")[i].seeking',arg=i);p.evaluate('i=>document.querySelectorAll("video")[i].play()',i);p.wait_for_timeout(450)
   q=p.evaluate('i=>{const v=document.querySelectorAll("video")[i];v.pause();return{time:v.currentTime,audio:v.webkitAudioDecodedByteCount,width:v.videoWidth,height:v.videoHeight,error:v.error?.message};}',i);ck(('Single'if i==0 else'Wave')+' video seeks,plays and decodes audio',q['time']>5.2 and q['audio']>0 and q['width']==1280 and q['height']==800 and not q['error'],q)
  p.screenshot(path=str(W/'focused-page.png'));ck('No page/console/asset errors',not errors,errors);b.close()
finally:(W/'guide-checks.json').write_text(json.dumps(checks,indent=2))
print('RESULT',sum(q['passed']for q in checks),'/',len(checks));assert all(q['passed']for q in checks)
