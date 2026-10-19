"""Exercise the production archive review and animation controls."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/dracodia_archive_1018/review';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/dracodia_archive_1018/index.html?scene=spiralLightning&difficulty=normal')
  p.wait_for_function('!document.querySelector("#replay").disabled');f=p.frames[1];f.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  check('review uses production assets, without a fixture injection',f.evaluate('D20_ART.fixture===false&&d20Keys().every(k=>!XART._src[k].startsWith(\"_shots/\"))'))
  check('campaign saves are isolated',f.evaluate('window.__archiveReviewStorage===true'))
  for scene in ['hover','armLasers','coreMissiles','spiralLightning','codeBombs','downloadLegion','bastion','camo','halberd','natural']:
   if p.input_value('#scene')!=scene:p.select_option('#scene',scene)
   else:p.click('#replay')
   p.wait_for_function('!document.querySelector("#replay").disabled')
   for i in range(24):
    f.evaluate('()=>{for(let i=0;i<12;i++){updatePlay(1/60);drawWorld(1/60);}}');p.wait_for_timeout(5)
    if scene=='downloadLegion' and i==14:p.screenshot(path=str(O/'materializing.png'))
   data=f.evaluate('({mode:boss._r30.mode,phase:j3State(boss).encounter,form:boss._r30.v18.form,type:boss._r30.v18.attack?.type,actors:enemies.filter(e=>e._d20&&!e.dead).map(e=>e._d20.kind),height:SC12.layout.field.h})')
   check(scene+' loads the actual controller and full playfield',data['mode']=='fight' and data['phase']==2 and data['form']==0 and data['height']>600,data)
   if scene in ['bastion','camo','halberd']:check(scene+' owns its intended archived hull',scene in data['actors'],data)
   f.evaluate('()=>{shake=0;SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(scene+'.png')))
   if scene in ['armLasers','coreMissiles','spiralLightning','codeBombs','downloadLegion']:
    for _ in range(60 if scene=='downloadLegion' else 40):f.evaluate('()=>{for(let i=0;i<12;i++){updatePlay(1/60);drawWorld(1/60);}}');p.wait_for_timeout(5)
    q=f.evaluate('({form:boss._r30.v18.form,types:D20.events.filter(e=>e.event==="main-release").map(e=>e.type)})')
    check(scene+' remains selected across complete attack cycles',q['form']==0 and len(q['types'])>=2 and set(q['types'])=={scene},q)
  p.select_option('#scene','armLasers');p.wait_for_function('!document.querySelector("#replay").disabled');p.click('#break')
  check('arm break button disables the main boss left arm',f.evaluate('boss.parts.find(p=>p.id==="left").destroyed'))
  p.select_option('#scene','camo');p.wait_for_function('!document.querySelector("#replay").disabled')
  for i in range(14):f.evaluate('()=>{for(let i=0;i<12;i++){updatePlay(1/60);drawWorld(1/60);}}');p.wait_for_timeout(5)
  p.click('#break');check('break button disables the actual left launcher',f.evaluate('enemies.some(e=>e._d20?.mini&&e._d20.parts.find(p=>p.id==="left").hp<=0)'))
  p.goto(f'http://127.0.0.1:{port}/docs/previews/dracodia_archive_1018/frames.html')
  p.wait_for_function('()=>active&&active.frames.every(a=>images.has(a.key))');p.click('#play')
  for bank in p.evaluate('Object.keys(banks)'):
   p.select_option('#bank',bank);p.wait_for_function('()=>active&&active.frames.every(a=>images.has(a.key))')
   p.focus('#frame');p.keyboard.press('Home');before=p.evaluate('canvas.toDataURL()');p.keyboard.press('End');after=p.evaluate('canvas.toDataURL()')
   q=p.evaluate('({n:active.frames.length,max:Number(slider.max),size:active.frames[0].w})')
   check(bank+' frame scrubber displays its complete shipping bank',16<=q['n']<=32 and q['max']==q['n']-1 and before!=after,q)
   p.keyboard.press('Home')
   for _ in range(q['n']//2):p.keyboard.press('ArrowRight')
   p.uncheck('#onion');before=p.evaluate('canvas.toDataURL()');p.check('#onion');after=p.evaluate('canvas.toDataURL()')
   check(bank+' onion changes actual rendered pixels',before!=after)
   p.screenshot(path=str(O/(bank+'-onion.png')))
  p.goto(f'http://127.0.0.1:{port}/docs/previews/stage8_pixellab_1018/index.html?scene=roar&difficulty=normal')
  p.wait_for_function('!document.querySelector("#replay").disabled');f=p.frames[1];f.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(30)
  for i in range(8):f.evaluate('()=>{for(let i=0;i<12;i++){updatePlay(1/60);drawWorld(1/60);}}');p.wait_for_timeout(5)
  check('existing Roar selector still selects the roar after the new attack book',f.evaluate('boss._r30.v18.acting==="colossus_roar"&&v18Rig(boss).every(v=>V19.draws[v.key]>0)'))
  p.screenshot(path=str(O/'existing-roar.png'))
  check('no page, console, draw or missing asset errors',not errors,errors);br.close()
finally:stop()
data=dict(fixture=False,production_wired=True,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'results.json').write_text(json.dumps(data,indent=2));print(json.dumps({k:data[k] for k in ['passed','failed','errors']}));sys.exit(bool(data['failed']))
