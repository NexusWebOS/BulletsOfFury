"""Verify the delivered Stage 8 review uses the full native game safely."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage8_pixellab_1018/review';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1700,height=1100));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/stage8_pixellab_1018/index.html?scene=conversion&difficulty=furious')
  p.wait_for_function('document.querySelector("#replay").disabled===false');f=p.frames[1];f.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  check('review storage is isolated from campaign saves',f.evaluate('window.__v18ReviewStorage===true'))
  check('review uses the real index and native Stage8 runtime',f.evaluate('typeof V18!=="undefined"&&typeof SC12!=="undefined"&&run.stage===8'))
  for scene,phase,form in [('phase1',0,0),('phase2',1,0),('colossus',2,0),('hammer',2,8),('helicopter',2,1),('harrier',2,6),('volcano',2,2)]:
   p.select_option('#scene',scene);p.wait_for_function('document.querySelector("#replay").disabled===false')
   f.wait_for_function('([phase,form])=>boss&&j3State(boss).encounter===phase&&boss._r30.v18.form===form&&boss._r30.mode==="fight"',arg=[phase,form]);f.evaluate('()=>{updatePlay(1/60);drawWorld(1/60);SC12.refresh();__bofFit();}')
   row=f.evaluate('({phase:j3State(boss).encounter,form:boss._r30.v18.form,parts:retinaBossTargets(boss).length,field:SC12.layout.field,canvas:{w:cv.width,h:cv.height},model:v18Model(boss)})')
   check(scene+' selector has native pixels, three locks and full playfield',row['parts']==3 and row['field']['h']>600,row)
   p.screenshot(path=str(O/(scene+'.png')))
  p.select_option('#scene','harrier');p.wait_for_function('document.querySelector("#replay").disabled===false');f.wait_for_function('boss?._r30?.v18?.form===6')
  p.click('#module');f.evaluate('()=>{updatePlay(1/60);drawWorld(1/60);}')
  check('review weapon-break control damages the real module',f.evaluate('boss.parts.find(p=>p.id==="left").destroyed&&retinaBossTargets(boss).length===2'))
  p.check('#onion');f.evaluate('()=>{updatePlay(1/60);drawWorld(1/60);}')
  check('onion control shows registered native animation samples',f.evaluate('window.v18Onion&&Object.keys(V18.draws).length>12'))
  p.screenshot(path=str(O/'harrier-onion-broken.png'))
  check('review has no page console drawing or asset errors',not errors,errors);br.close()
finally:stop()
data=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'results.json').write_text(json.dumps(data,indent=2));print(json.dumps(dict(passed=data['passed'],failed=data['failed'],errors=errors)));sys.exit(bool(data['failed']))
