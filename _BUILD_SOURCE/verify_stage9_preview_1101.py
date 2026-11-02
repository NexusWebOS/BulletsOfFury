from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/stage9_amplify_1101';checks=[];errors=[]
def ck(n,ok,d=None):checks.append(dict(name=n,passed=bool(ok),data=d));print('PASS'if ok else'FAIL',n,flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8805/current/stage9-water-refit-1101.html',wait_until='networkidle');ck('Preview exposes19 current enemy clips',p.locator('nav button').count()==19)
 for button in p.locator('nav button').all():
  name=button.inner_text();button.click();p.wait_for_function('(()=>{const v=document.querySelector("video");return v.readyState>=2&&v.videoWidth>0&&!v.error})()',timeout=30000);p.evaluate('()=>{const v=document.querySelector("video");v.pause();v.currentTime=Math.min(5,v.duration*.4)}');p.wait_for_function('!document.querySelector("video").seeking');q=p.evaluate('()=>{const v=document.querySelector("video"),c=document.createElement("canvas");c.width=320;c.height=200;const g=c.getContext("2d");g.drawImage(v,0,0,320,200);const a=g.getImageData(0,0,320,200).data;let lit=0;for(let i=0;i<a.length;i+=4)if(a[i]+a[i+1]+a[i+2]>80)lit++;return {w:v.videoWidth,h:v.videoHeight,seconds:v.duration,lit,src:v.currentSrc};}');ck(name+' actual decoded seekable pixels',q['w']==1280 and q['h']==800 and q['lit']>10000,q)
 p.locator('nav button').filter(has_text='Current Breaker').click();p.wait_for_function('document.querySelector("video").readyState>=2');p.evaluate('()=>{const v=document.querySelector("video");v.pause();v.currentTime=9}');p.wait_for_function('!document.querySelector("video").seeking');p.evaluate('scrollTo(0,0)');p.screenshot(path=str(O/'preview-desktop.png'))
 p.set_viewport_size({'width':390,'height':844});p.evaluate('scrollTo(0,0)');p.screenshot(path=str(O/'preview-mobile.png'));q=p.evaluate('()=>({page:document.documentElement.scrollWidth,view:innerWidth})');ck('Mobile preview fits the viewport',q['page']<=q['view'],q)
 p.goto('http://127.0.0.1:8805/enemy-showcase-1031.html?revision=stage9-water-1101#enemy=stage9-cbreak',wait_until='networkidle');q=p.evaluate('async()=>{const x=await(await fetch("/enemy-showcase-1031/manifest.json")).json();return{cards:x.items.length,stage9:x.items.filter(q=>q.stage===9)};}');ck('Full guide uses19 distinct updated Stage9 clips and preserves154 total cards',q['cards']==154 and len(q['stage9'])==19,q)
 ck('No playback page or console errors',not errors,errors);b.close()
(O/'preview-checks.json').write_text(json.dumps(checks,indent=2));print('SUMMARY',sum(q['passed']for q in checks),'/',len(checks));sys.exit(0 if all(q['passed']for q in checks)else 1)
