"""Full-window review boot, real keyboard and scene controls in Chromium."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/combat_revision_1017/review';O.mkdir(parents=True,exist_ok=True)
errors=[];checks=[]
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/combat_revision_1017/index.html');p.wait_for_function('ready&&!busy&&game.contentWindow.eval("bossActive&&!!boss?._hammer")')
  check('Review boots the actual Hammer with isolated saves',p.evaluate('game.contentWindow.__combatReviewStorage&&game.contentWindow.eval("run.stage===5&&SC12.active()&&run.spaceLevels[0]===5")'))
  game=p.frames[1];game.wait_for_function('boss._hammer.state!=="fr_activation"');game.locator('body').click(position=dict(x=850,y=600));p.keyboard.down('j');p.wait_for_timeout(350)
  row=game.evaluate('()=>({fire:Input.down("j"),rounds:pBullets.map(q=>q.kind),state,mode:run.mode})')
  check('Actual keyboard fire launches the installed space weapons',any(k in ['spaceLaser','spaceVolley'] for k in row['rounds']),row)
  p.keyboard.up('j');p.screenshot(path=str(O/'hammer.png'))
  for name,stage in [('guard',4),('fire',2),('ice',3),('camo',4),('small',1),('finish',5),('intro',7)]:
   p.select_option('#scene',name);p.wait_for_function('n=>!busy&&game.contentWindow.eval("run.stage")===n',arg=stage);p.wait_for_timeout(1500)
   row=game.evaluate('({stage:run.stage,state,ending:!!H3.ending?.hf17,enemies:enemies.length,scene:BOFCinematicDirector.current?.id,hud:SC12.active(),w:cv.width,h:cv.height})')
   ok=row['stage']==stage and (row['scene']=='stage7-approach' if name=='intro' else row['ending'] if name=='finish' else row['hud'])
   check(name+' scene renders in the actual native game',ok,row);p.screenshot(path=str(O/(name+'.png')))
  p.select_option('#scene','guard');p.wait_for_function('!busy&&game.contentWindow.eval("run.stage")===4');p.select_option('#difficulty','furious');p.wait_for_function('!busy&&game.contentWindow.eval("diffKey")=== "furious"')
  check('Difficulty control restarts the real Furious guard encounter',game.evaluate('bossActive&&sa14Storm(boss)&&diffKey==="furious"'))
  br.close()
finally:stop()
check('No page, console, draw or missing asset errors',not errors,errors)
result=dict(passed=sum(q['passed'] for q in checks),failed=[q for q in checks if not q['passed']],errors=errors,checks=checks)
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':result['passed'],'failed':len(result['failed']),'errors':errors}),flush=True)
if result['failed'] or errors:sys.exit(1)
