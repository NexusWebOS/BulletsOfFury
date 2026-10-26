from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve
import json,base64
R=Path(__file__).resolve().parents[1];port,stop=serve(str(R));checks=[];errors=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('!!window.BOF_STORYBOARD',timeout=180000);p.mouse.click(2,2);p.evaluate('()=>{campaignIntroStart(()=>{});campaignIntroWarm();}');p.wait_for_function('campaignIntroReady()',timeout=180000)
 def ck(n,v):checks.append({'name':n,'passed':bool(v)})
 for shot,t in [('arrival',6),('takeover',.1),('takeover',7.9),('downlink',4)]:
  r=p.evaluate("([shot,t])=>{const b=IP21.beats.find(b=>b.replay===shot);campaignIntro.t=b.at+t;ip21Visual(b,campaignIntro,t,cutsceneViewWidth(),VH);return OT24.last;}",[shot,t]);ck(shot+' advances absorption/beam phase at '+str(t),(r.get('fluidAlpha')==1 if shot=='arrival' else r.get('lockedHull',False) and r.get('alpha')==1 if shot=='takeover' else r.get('laser',False)))
  if shot=='arrival':ck('Reuses native circular Stage 8 purple void portal',r['portal']=='black_void')
  if shot=='downlink':
   import math
   dx=r['to'][0]-r['from'][0];dy=r['to'][1]-r['from'][1];cross=dx*math.cos(r['angle'])+dy*math.sin(r['angle']);ck('Angled emitter points along Earth transmission lane',abs(cross)<1e-6 and dy>0 and abs(r['angle'])>.2)
 audio=p.evaluate("""async()=>{Snd.resume();Snd.play('crackle');const pool=Snd.pools.crackle,el=pool.slots.find(v=>v&&v.el).el;const ac=new AudioContext();const buf=await ac.decodeAudioData(await(await fetch(el.src)).arrayBuffer());let peak=0;for(const v of buf.getChannelData(0))peak=Math.max(peak,Math.abs(v));await new Promise(r=>setTimeout(r,100));const played=pool.slots.some(v=>v?.el?.currentTime>0&&!v.el.error);await ac.close();return peak>0&&played;}""");ck('Transmission cue decodes and plays in shared mixer',audio);ck('No page/console errors',not errors);b.close()
stop();(R/'_shots/intro_order_1024/attachment-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf8');print(json.dumps(checks,indent=2));raise SystemExit(0 if all(c['passed']for c in checks)else 1)
