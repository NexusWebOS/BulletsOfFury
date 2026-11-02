"""Decode, seek and inspect every replaced Stage9 palette film in Chromium."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage9_palettes_1101';publication=json.loads((O/'publication.json').read_text());checks=[];errors=[]
def ck(n,ok,d=None):checks.append(dict(name=n,passed=bool(ok),data=d));print('PASS'if ok else'FAIL',n,flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8805/current/stage9-water-refit-1101.html',wait_until='networkidle');ck('All19 Stage9 chapters remain',p.locator('nav button').count()==19)
 for c in publication['clips']:
  p.locator('nav button[data-id="'+c['id']+'"]').click();p.wait_for_function('document.querySelector("video").readyState>=2');p.evaluate('t=>{const v=document.querySelector("video");v.pause();v.currentTime=t}',c['posterAt']);p.wait_for_function('!document.querySelector("video").seeking');p.evaluate('scrollTo(0,0)')
  q=p.evaluate('()=>{const v=document.querySelector("video"),c=document.createElement("canvas");c.width=320;c.height=200;const g=c.getContext("2d");g.drawImage(v,0,0,320,200);const a=g.getImageData(0,0,320,200).data;let lit=0;for(let i=0;i<a.length;i+=4)if(a[i]+a[i+1]+a[i+2]>80)lit++;return{w:v.videoWidth,h:v.videoHeight,seconds:v.duration,lit,src:v.currentSrc,error:v.error}}');ck(c['model']+' replaced film decodes real seekable pixels',q['w']==1280 and q['h']==800 and q['lit']>10000 and not q['error']and q['src'].endswith(c['id']+'-palette-1101.mp4'),q);p.screenshot(path=str(O/(c['model']+'-playback.png')))
 p.set_viewport_size({'width':390,'height':844});p.evaluate('scrollTo(0,0)');p.screenshot(path=str(O/'preview-mobile.png'));q=p.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth})');ck('Mobile preview fits viewport',q['scroll']<=q['width'],q)
 p.goto('http://127.0.0.1:8805/enemy-showcase-1031.html#enemy=stage9-s9interceptor',wait_until='networkidle');q=p.evaluate('async()=>{const x=await(await fetch("/enemy-showcase-1031/manifest.json")).json();return{cards:x.items.length,recolored:x.items.filter(q=>q.palette).length,current:x.items.find(q=>q.id==="stage9-cbreak").video};}');ck('Guide154 cards includes ten palettes and retains overhead Current clip',q['cards']==154 and q['recolored']==10 and q['current'].endswith('overhead-1101.mp4'),q)
 ck('No page or console errors',not errors,errors);b.close()
(O/'playback-checks.json').write_text(json.dumps(checks,indent=2));print('SUMMARY',sum(q['passed']for q in checks),'/',len(checks));sys.exit(0 if all(q['passed']for q in checks)else 1)
