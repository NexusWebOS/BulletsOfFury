"""Verify the exact review page plays/seeks with decoded audio and current pixels."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from shoot import serve
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_aura_gun_1025';errors=[];port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/chronos_frames_1025/index.html');p.wait_for_function('fight.readyState>=1&&Object.keys(images).length===9',timeout=60000)
  p.evaluate("""async()=>{window.reviewPeak=0;const c=new AudioContext();await c.resume();const n=c.createMediaElementSource(fight),a=c.createAnalyser();n.connect(a);a.connect(c.destination);window.reviewTimer=setInterval(()=>{const d=new Float32Array(a.fftSize);a.getFloatTimeDomainData(d);for(const v of d)reviewPeak=Math.max(reviewPeak,Math.abs(v));},10)}""")
  p.get_by_role('button',name='Play with sound',exact=True).click();p.wait_for_function('!fight.paused&&fight.currentTime>1',timeout=60000)
  p.get_by_role('button',name='Spin-up and firing',exact=True).click();p.wait_for_function('fight.currentTime>5.4&&fight.currentTime<9',timeout=60000);p.wait_for_timeout(800);p.screenshot(path=str(O/'review-page.png'))
  p.get_by_role('button',name='Pause frames',exact=True).click();before=p.locator('#regular').evaluate('(c)=>c.toDataURL()');p.get_by_role('button',name='Next pose',exact=True).click();p.wait_for_timeout(80);after=p.locator('#regular').evaluate('(c)=>c.toDataURL()');p.locator('.pair').screenshot(path=str(O/'review-three-forms.png'))
  p.get_by_role('button',name='Aura during two-handed spin',exact=True).click();p.wait_for_function('fight.currentTime>28&&fight.currentTime<33',timeout=60000);p.wait_for_timeout(500);p.screenshot(path=str(O/'review-rage.png'))
  result=p.evaluate('()=>({duration:fight.duration,playing:!fight.paused,muted:fight.muted,peak:reviewPeak,bodyFrames:art.banks.body.length,barrelFrames:art.banks.barrel.length})');result.update(errors=errors,frameStepChangesPixels=before!=after);result['passed']=result['duration']>=46 and result['playing'] and not result['muted'] and result['peak']>.01 and not errors and before!=after
  (O/'review-validation.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result),flush=True);b.close()
finally:stop()
raise SystemExit(0 if result['passed'] else 1)
