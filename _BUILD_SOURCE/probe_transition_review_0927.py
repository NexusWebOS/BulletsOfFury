import json,http.server
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path(sh.GAME)/'_shots/furious_0927';port,stop=sh.serve(sh.GAME)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1360,'height':960});p.set_default_timeout(120000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate("()=>{diffKey='furious';DIFF=DIFFS.furious;run.mode='campaign';run.pilot='yuri';beginStage(7);setState(GS.PLAY);story=null;player.invuln=99999;spawnBoss(curStage.boss);bossActive=true;boss.enter=false;boss.x=worldWidth()/2;boss.y=160;s7mInit(boss);boss._s7mod.shield=0;boss._s7mod.core=0;for(const part of boss._s7mod.parts)part.hp=0;s7mSet(boss,'dead');}")
  for i in range(9):p.evaluate('()=>{for(let i=0;i<60;i++){updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}');p.wait_for_timeout(80)
  p.screenshot(path=str(out/'toxic-escape.png'))
  for i in range(7):p.evaluate('()=>{for(let i=0;i<60;i++){updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}');p.wait_for_timeout(50)
  p.screenshot(path=str(out/'toxic-portal.png'))
  for i in range(7):p.evaluate('()=>{for(let i=0;i<60;i++){if(state===GS.PLAY)updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}');p.wait_for_timeout(30)
  report={'exit':p.evaluate('()=>({state,finished:boss._s7warden.final.finished,entry:run._l78Entry,pending:campaign._l78Pending})')}
  p.evaluate('()=>beginStage(8)');p.wait_for_function("()=>XART.rdy('fr27_realm_terrain')&&XART.rdy('fr27_realm_fleet')&&XART.rdy('fr27_realm_boss')&&XART.rdy('fr27_realm_ordnance')")
  p.evaluate('()=>{for(let i=0;i<330;i++){ctx.setTransform(SS,0,0,SS,0,0);drawL78Entry(1/60);}}');p.wait_for_timeout(500);p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawL78Entry(.01);}');p.screenshot(path=str(out/'alien-arrival.png'))
  p.evaluate("()=>{for(let i=0;i<650;i++){if(state===GS.WARPENTRY){ctx.setTransform(SS,0,0,SS,0,0);drawL78Entry(1/60);}}spawnBoss(curStage.boss);bossActive=true;boss.enter=false;boss._symEntry=null;boss._be=null;boss._morphT=null;boss._vForm=0;boss.x=worldWidth()/2;boss.y=160;vile24Attack(boss);vile24Tick(boss,.65);ctx.setTransform(SS,0,0,SS,0,0);player.invuln=0;drawWorld(0);}");p.screenshot(path=str(out/'alien-boss.png'))
  report['arrivalY']=p.evaluate('()=>player.y')
  report['alien']=p.evaluate("()=>{vile24Tick(boss,.6);return {state,form:boss._vForm,pattern:boss._v24.pattern.type,projectiles:eBullets.filter(q=>q._frRealm!=null).length};}")
  report['errors']=errors;(out/'transition-probe.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));b.close()
finally:stop()
