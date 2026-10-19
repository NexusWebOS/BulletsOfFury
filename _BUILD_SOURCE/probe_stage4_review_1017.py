"""Verify the Stage 4 replay page with the actual game, input and full side HUD."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage4_panic_1017/review';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/stage4_panic_1017/index.html');p.wait_for_function('ready&&!busy&&game.contentWindow.eval("subBossActive&&!!subBoss?._wing17")')
  g=p.frames[1]
  native_size=g.evaluate('({w:cv.width,h:cv.height,view:viewW(),play:PLAY.h})');scene_sizes=[]
  check('Review starts the native Furious Warden with isolated saves',g.evaluate('window.__stage4ReviewStorage&&run.stage===4&&run.mode==="campaign"&&diffKey==="furious"&&SC12.active()&&subBoss._wing17.slots.length===6'))
  g.locator('body').click(position=dict(x=850,y=600));p.keyboard.down('j');p.wait_for_timeout(300)
  row=g.evaluate('({fire:Input.down("j"),rounds:pBullets.length,active:subBossActive,hud:SC12.active()})')
  check('Actual keyboard fire works in the review fight',row['fire'] and row['rounds']>0 and row['active'] and row['hud'],row);p.keyboard.up('j')
  g.wait_for_function('P4_17.events.some(e=>e.event==="wing-spiral"&&e.jets===6)',timeout=20000)
  check('The review automatically launches the complete six-jet spiral',g.evaluate('P4_17.events.some(e=>e.event==="wing-spiral"&&e.jets===6)'))
  p.screenshot(path=str(O/'warden-automatic-spiral.png'))
  for scene in ['panic','pursuit','row']:
   p.select_option('#scene',scene);p.wait_for_function('!busy&&game.contentWindow.eval("bossActive&&sa14Storm(boss)")');p.wait_for_timeout(450)
   row=g.evaluate('({phase:boss._p4Final?.phase,mode:boss._er26.mode,hp:boss.hp,max:boss.maxhp,hud:SC12.active(),scale:boss._sa14.scale,angle:boss._sa14.angle,isolated:window.__stage4ReviewStorage,size:{w:cv.width,h:cv.height,view:viewW(),play:PLAY.h}})');scene_sizes.append(row['size'])
   check(scene+' opens the actual encounter and regular side HUD',row['hud'] and row['isolated'] and (row['mode']=='sa14-storm' if scene=='row' else row.get('phase')=='rear' if scene=='pursuit' else row.get('phase') in ['panic','ram']),row)
   if scene=='pursuit':
    row=g.evaluate('''()=>{const b=boss,p=mr27Shape(b,'core');b._s4ShieldHit=b._s4CoreHit=null;_lastHitX=p.x;_lastHitY=p.y;_dmgBullet={kind:'mg',x:p.x,y:p.y};const hp=b.hp;hitBoss(b.maxhp*.015);_dmgBullet=null;return{loss:hp-b.hp,anger:b._p4Final.anger};}''')
    check('Review shots provoke the installed pursuit retaliation',row['loss']>0 and row['anger']>0,row)
   p.screenshot(path=str(O/(scene+'.png')))
  p.select_option('#difficulty','normal');p.wait_for_function("!busy&&game.contentWindow.eval('diffKey')==='normal'");p.select_option('#scene','warden');p.wait_for_function('!busy&&game.contentWindow.eval("subBossActive&&sa14Mini(subBoss)")')
  check('Difficulty selector restores the native two-jet Normal roster',g.evaluate('subBoss._wing17.slots.length===2&&SC12.active()'))
  g.wait_for_function('enemies.some(e=>e._wing17&&!e.dead&&!e._noHit)')
  row=g.evaluate('''()=>{const e=enemies.find(e=>e._wing17&&!e.dead&&!e._noHit);e.hp=0;updatePlay(1/60);return{dying:e._dyingT,dead:e.dead,hp:e.hp};}''')
  check('Owned flight still enters native death when HP reaches zero',row.get('dead') or row.get('dying') is not None,row)
  check('Regular FOV remains the same across all review scenes',all(s==native_size for s in scene_sizes) and p.locator('#game').bounding_box()['width']==1920,dict(native=native_size,scenes=scene_sizes))
  br.close()
finally:stop()
check('No review page, console, draw or asset errors',not errors,errors)
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
