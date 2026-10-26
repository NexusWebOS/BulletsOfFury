from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_contract_1025';port,stop=serve(str(R));errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text+' '+str(m.location)) if m.type=='error' else None)
  p.on('response',lambda r:print('HTTP '+str(r.status)+' '+r.url,flush=True) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/chronos_contract_1025/index.html');p.wait_for_function("document.querySelector('#fight').readyState>=1&&document.querySelector('#counter').readyState>=1",timeout=60000)
  p.evaluate("""async()=>{window.reviewPeak=0;const c=window.reviewAudio=new AudioContext();await c.resume();const n=c.createMediaElementSource(fight),a=c.createAnalyser();n.connect(a);a.connect(c.destination);window.reviewTimer=setInterval(()=>{const d=new Float32Array(a.fftSize);a.getFloatTimeDomainData(d);for(const v of d)reviewPeak=Math.max(reviewPeak,Math.abs(v));},10);}""")
  p.get_by_role('button',name='Play with sound',exact=True).click();p.wait_for_function('!fight.paused&&fight.currentTime>.5',timeout=60000);p.get_by_role('button',name='Beginning dialogue',exact=True).click();p.wait_for_function('fight.currentTime>7&&fight.currentTime<12',timeout=60000);p.wait_for_timeout(300)
  p.screenshot(path=str(O/'review-page.png'));r=p.evaluate('()=>({times,seekable:Array.from({length:fight.seekable.length},(_,i)=>[fight.seekable.start(i),fight.seekable.end(i)]),duration:fight.duration,counterDuration:counter.duration,playing:!fight.paused,muted:fight.muted,time:fight.currentTime,peak:reviewPeak})');r['errors']=errors;r['passed']=r['duration']>=149 and r['counterDuration']>=17 and r['playing'] and not r['muted'] and r['peak']>.01 and not errors
  (O/'review-page-validation.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf8');print(json.dumps(r),flush=True);b.close()
finally:stop()
raise SystemExit(0 if r['passed'] else 1)
