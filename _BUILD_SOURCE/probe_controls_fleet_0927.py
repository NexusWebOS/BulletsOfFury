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
  report=p.evaluate("""()=>{diffKey='furious';DIFF=DIFFS.furious;run.mode='arcade';run.pilot='yuri';beginStage(1);setState(GS.PLAY);story=null;stagePlan=[];enemies=[];run.bombs=30;player.invuln=9999;for(const k in Input.keys)Input.keys[k]=false;for(let i=0;i<4;i++)spawnEnemy('s1jet',230+i*55,120+i*20,{});Input.keys.c=true;cycleLock();const chosen=retina.target;for(let i=0;i<100;i++){updateRetina(1/60);retinaScanInput(1/60);retinaScanTick(1/60);}const single={marks:player._retinaScan?.marks.length||0,target:!!retina.target,same:retina.target===chosen};Input.keys.c=false;Input.keys.y=true;for(let i=0;i<100;i++){retinaScanInput(1/60);retinaScanTick(1/60);}const multi={marks:player._retinaScan?.marks.length,locked:player._retinaScan?.marks.filter(m=>m.phase==='locked').length};Input.keys.y=false;const ammo=run.bombs;retinaScanFire();for(let i=0;i<120;i++)retinaScanTick(1/60);const volley={spent:ammo-run.bombs,missiles:pBullets.length};return{single,multi,volley};}""")
  p.evaluate("()=>{diffKey='furious';DIFF=DIFFS.furious;beginStage(8);setState(GS.PLAY);run._l78Entry=0;l78entry=null;story=null;player.invuln=0;enemies=[];for(const [i,k]of ['s8scout','s8manta','s8needlejet','s8gunship'].entries())spawnEnemy(k,180+i*105,120+(i%2)*85,{});for(const e of enemies)s8MegaTick(e,.01);for(const name of ['realm_fleet','realm_ordnance','rebel_pitch'])XART.rdy('fr27_'+name);}")
  p.wait_for_function("()=>XART.rdy('fr27_realm_fleet')&&XART.rdy('fr27_realm_ordnance')&&XART.rdy('fr27_rebel_pitch')")
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}');p.screenshot(path=str(out/'alien-fleet.png'))
  p.evaluate("()=>{beginStage(6);setState(GS.PLAY);story=null;s6Opening=null;s6Wing.route='right';spawnBoss('rebelsquad');bossActive=true;rebelSquadTick(boss,30);s6Wing.line=null;for(const q of boss._rebels.ships){q.y=q.homeY;q.x=q.homeX;}const q=boss._rebels.ships[0];boss._rebels.hit=0;boss._rebels.frHit='left';rebelSquadDamage(boss,q.max*.2);boss._rebels.ships[1].frCloak=1;boss._rebels.ships[2].evadeT=.22;boss._rebels.ships[2].frSomersault=true;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}");p.wait_for_timeout(500);p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}');p.screenshot(path=str(out/'rebel-modules.png'))
  report['errors']=errors;(out/'controls-fleet-probe.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));b.close()
finally:stop()
