"""Exercise the exact delivered preview and every revised boss selector."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage8_swipes_1018/review';O.mkdir(parents=True,exist_ok=True)
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
  check('review isolates campaign saves',f.evaluate('window.__v18ReviewStorage===true'))
  check('review loads the updated real native game',f.evaluate('typeof V19!=="undefined"&&run.stage===8'))
  for scene,phase,form,count in [('phase1',0,0,3),('phase2',1,0,3),('colossus',2,0,3),('hammer',2,8,2),('helicopter',2,1,3),('harrier',2,6,6),('volcano',2,2,2),('roar',2,0,3),('speech',2,0,0),('volcanohead',2,2,1),('death',2,0,0),('swipes',0,0,3),('ghostswipes',1,0,3),('scythes',2,0,3),('volcanoswipes',2,2,2)]:
   p.select_option('#scene',scene);p.wait_for_function('document.querySelector("#replay").disabled===false')
   f.wait_for_function('([phase,form])=>boss&&j3State(boss).encounter===phase&&boss._r30.v18.form===form',arg=[phase,form]);f.evaluate('()=>{updatePlay(1/60);drawWorld(1/60);SC12.refresh();__bofFit();}')
   row=f.evaluate('({phase:j3State(boss).encounter,form:boss._r30.v18.form,parts:retinaBossTargets(boss).length,protected:boss._noHit,field:SC12.layout.field,mode:boss._r30.mode})')
   check(scene+' uses actual identity and full native playfield',(row['parts']==count or scene=='hammer' and row['parts']==0 and row['protected']) and row['field']['h']>600,row);p.screenshot(path=str(O/(scene+'.png')))
   if scene in ['swipes','ghostswipes','scythes','volcanoswipes']:
    p.check('#onion')
    for i in range(7):f.evaluate('()=>{for(let i=0;i<12;i++){updatePlay(1/60);drawWorld(1/60);}}');p.wait_for_timeout(5)
    check(scene+' preview starts and onions actual shoulder sweeps',f.evaluate('window.v18Onion&&!!boss._r30.v18.swipe&&v18Rig(boss).some(v=>v.p.id!=="core"&&Math.abs(v.rot)>.1)'))
    p.screenshot(path=str(O/(scene+'-onion.png')));p.uncheck('#onion')
  p.select_option('#scene','harrier');p.wait_for_function('document.querySelector("#replay").disabled===false');f.wait_for_function('boss?._r30?.v18?.form===6')
  p.click('#module');f.evaluate('()=>{updatePlay(1/60);drawWorld(1/60);}')
  check('break control destroys the real Harrier fan',f.evaluate('boss.parts.find(p=>p.id==="fanL").destroyed&&retinaBossTargets(boss).length===5'))
  p.select_option('#scene','hammer');p.wait_for_function('document.querySelector("#replay").disabled===false');p.check('#onion');f.evaluate('()=>{updatePlay(1/60);drawWorld(1/60);}')
  check('Hammer onion shows actual two-arm poses',f.evaluate('window.v18Onion&&boss.parts.length===2'))
  p.screenshot(path=str(O/'hammer-onion.png'));check('review has no page console drawing or asset errors',not errors,errors);br.close()
finally:stop()
data=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'results.json').write_text(json.dumps(data,indent=2));print(json.dumps({k:data[k] for k in ['passed','failed','errors']}));sys.exit(bool(data['failed']))
