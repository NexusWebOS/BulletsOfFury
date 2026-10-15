"""Record the isolated native preview and smoke-test its review controls."""
from pathlib import Path
import sys,json,base64,io,subprocess
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/siege_tanks_1010';errors=[];checks=[]
def check(name,ok):
 checks.append({'name':name,'pass':bool(ok)});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT));encoder=None
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1320,'height':1120});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/siege_tanks_1010/index.html');f=p.frames[1];f.wait_for_function('window.PT10&&PT10.ready()',polling=50)
  f.evaluate(shoot.TRAP_RAF);f.wait_for_timeout(60);p.locator('#auto').uncheck();p.locator('#pause').click()
  if '--still' in sys.argv:
   p.locator('#pause').click();f.evaluate('()=>{PT10.restore();ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   p.wait_for_timeout(250);p.screenshot(path=str(OUT/'preview-desktop.png'));br.close();print('Captured native preview with synchronized review controls',flush=True);sys.exit(0)
  check('Pause control stops preview time',f.evaluate('()=>{const t=PT10.t;PT10.tick(.1);return PT10.paused&&PT10.t===t;}'))
  p.locator('#pause').click();p.locator('#view').select_option('damage');p.locator('#part').select_option('weapon')
  check('Damage gallery chooses the independent weapon plate',f.evaluate('PT10.mode==="damage"&&PT10.part==="weapon"'))
  p.locator('#view').select_option('combat')
  for unit in ['sonic','devastator','deviator']:
   p.locator('[data-unit="'+unit+'"]').click();f.wait_for_function('PT10.ready()',polling=50)
   f.evaluate('()=>{PT10.mode="combat";PT10.auto=false;PT10.paused=false;PT10.t=0;PT10.restore();}');p.locator('#charged' if unit=='sonic' else '#fire').click()
   check(unit+' fire control starts native attack',f.evaluate('!!PT10.attack'))
   for i in range(96):
    if i==64:
     p.locator('#destroy').click()
     check(unit+' delayed breakup retains waiting pieces visibly at their mounts',f.evaluate('PT10.debris.filter(d=>d.t<0).length===7&&PT10.debris.every(d=>!Number.isFinite(d.alpha))'))
     f.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
     (OUT/(unit+'-breakup-onset.png')).write_bytes(base64.b64decode(f.evaluate('cv.toDataURL().split(",")[1]')))
    data=f.evaluate('()=>{PT10.tick(1/16);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return cv.toDataURL().split(",")[1];}')
    im=np.array(Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB'))
    if encoder is None:
     h,w=im.shape[:2];encoder=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r','16','-i','-','-an','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p',str(OUT/'siege-tank-demo.mp4')],stdin=subprocess.PIPE,creationflags=0x08000000 if sys.platform=='win32' else 0)
    encoder.stdin.write(im.tobytes())
    if i%8==7:f.wait_for_timeout(5)
   p.locator('#reset').click();check(unit+' rebuild restores all eight modules',f.evaluate('Object.values(PT10.parts).every(p=>!p.gone)&&PT10.debris.length===0'))
  p.locator('[data-unit="sonic"]').click();f.wait_for_function('PT10.ready()',polling=50);f.evaluate('()=>{PT10.mode="combat";PT10.auto=false;PT10.restore();ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
  p.wait_for_timeout(250);p.screenshot(path=str(OUT/'preview-desktop.png'));br.close()
 if encoder:encoder.stdin.close();check('18-second native animation proof encodes successfully',encoder.wait()==0)
finally:stop()
check('Review controls produce no page or console errors',not errors)
(OUT/'demo-smoke.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2)+'\n')
if errors or any(not q['pass'] for q in checks):sys.exit(1)
