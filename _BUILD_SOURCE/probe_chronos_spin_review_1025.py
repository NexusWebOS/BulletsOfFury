"""Real Chromium playback, decoded audio and frame stepping for the spin review."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_original_1025';errors=[];port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/chronos_frames_1025/two-handed-spin.html');p.wait_for_function("fight.readyState>=1&&Object.keys(images).length===3&&art.originalSpin.frames===8",timeout=60000)
  p.evaluate("""async()=>{window.reviewPeak=0;const c=window.reviewAudio=new AudioContext();await c.resume();const n=c.createMediaElementSource(fight),a=c.createAnalyser();n.connect(a);a.connect(c.destination);window.reviewTimer=setInterval(()=>{const d=new Float32Array(a.fftSize);a.getFloatTimeDomainData(d);for(const v of d)reviewPeak=Math.max(reviewPeak,Math.abs(v));},10)}""")
  p.get_by_role('button',name='Play with sound',exact=True).click();p.wait_for_function('!fight.paused&&fight.currentTime>1',timeout=60000)
  p.get_by_role('button',name='Chromium',exact=True).click();p.wait_for_function('fight.currentTime>7.3&&fight.currentTime<12',timeout=60000);p.wait_for_timeout(700);p.screenshot(path=str(O/'review-page.png'))
  p.get_by_role('button',name='Pause frames',exact=True).click();a=p.locator('#regular').evaluate('(c)=>c.toDataURL()');f=p.locator('#frame').inner_text();p.get_by_role('button',name='Next frame',exact=True).click();z=p.locator('#regular').evaluate('(c)=>c.toDataURL()');g=p.locator('#frame').inner_text();p.locator('.pair').screenshot(path=str(O/'review-three-forms.png'))
  result=p.evaluate('()=>({duration:fight.duration,playing:!fight.paused,muted:fight.muted,peak:reviewPeak,frames:art.originalSpin.frames,source:art.originalSpin.sourceKey})');result.update(errors=errors,frameStepChangesPixels=a!=z,frameBefore=f,frameAfter=g);result['passed']=result['duration']>=19 and result['playing'] and not result['muted'] and result['peak']>.01 and not errors and a!=z
  (O/'review-validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps(result),flush=True);b.close()
finally:stop()
raise SystemExit(0 if result['passed'] else 1)
