"""Inspect only the replaced Current Breaker video through real Chromium."""
from pathlib import Path
import json, sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/current_flight_1101';checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print('PASS'if ok else'FAIL',name,flush=True)
report=json.loads((O/'video/report.json').read_text())['cuts'][0]
samples={view:next(q['seconds']-report['start'] for q in report['timeline'] if q.get('view')==view and (view!='front' or q['phase']=='transform')) for view in ['front','tilt','overhead']}
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8805/current/stage9-water-refit-1101.html#enemy=stage9-cbreak',wait_until='networkidle')
 ck('Nineteen Stage9 chapters remain',p.locator('nav button').count()==19)
 p.locator('nav button').filter(has_text='Current Breaker').click();p.wait_for_function('document.querySelector("video").readyState>=2')
 ck('Current chapter uses the new overhead film',p.evaluate('document.querySelector("video").currentSrc.endsWith("/current/stage9-cbreak-overhead-1101.mp4")'))
 for view,seconds in samples.items():
  p.evaluate('(t)=>{const v=document.querySelector("video");v.pause();v.currentTime=t}',seconds);p.wait_for_function('!document.querySelector("video").seeking');p.evaluate('scrollTo(0,0)')
  q=p.evaluate('()=>{const v=document.querySelector("video"),c=document.createElement("canvas");c.width=320;c.height=200;const g=c.getContext("2d");g.drawImage(v,0,0,320,200);const a=g.getImageData(0,0,320,200).data;let lit=0;for(let i=0;i<a.length;i+=4)if(a[i]+a[i+1]+a[i+2]>80)lit++;return {w:v.videoWidth,h:v.videoHeight,lit,time:v.currentTime,error:v.error}}')
  ck(view+' actual decoded seekable pixels',q['w']==1280 and q['h']==800 and q['lit']>10000 and not q['error'],q);p.screenshot(path=str(O/('playback-'+view+'.png')))
 p.set_viewport_size({'width':390,'height':844});p.evaluate('scrollTo(0,0)');p.screenshot(path=str(O/'playback-mobile.png'));q=p.evaluate('({page:document.documentElement.scrollWidth,view:innerWidth})');ck('Mobile preview fits',q['page']<=q['view'],q)
 p.goto('http://127.0.0.1:8805/enemy-showcase-1031.html#enemy=stage9-cbreak',wait_until='networkidle');q=p.evaluate('async()=>{const x=await(await fetch("/enemy-showcase-1031/manifest.json")).json();return {cards:x.items.length,current:x.items.find(q=>q.id==="stage9-cbreak")}}');ck('Full guide154 cards uses replaced film',q['cards']==154 and q['current']['video']=='/current/stage9-cbreak-overhead-1101.mp4',q)
 ck('No playback page or console errors',not errors,errors);b.close()
(O/'playback-checks.json').write_text(json.dumps(checks,indent=2));print('SUMMARY',sum(q['passed']for q in checks),'/',len(checks));sys.exit(0 if all(q['passed']for q in checks)else 1)
