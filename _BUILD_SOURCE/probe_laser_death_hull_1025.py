from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/laser_death_hull_1025';O.mkdir(parents=True,exist_ok=True)
port,stop=serve(str(R));errors=[];checks={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});run.spaceMode=true;run.gravityShipReady=true;gravityMode=GRAVITY_SHIP_ACTIVE;}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&furyShipReady()}',timeout=180000)
  p.evaluate("()=>{BOFCinematicDirector.cancel();fb2Intro=fb2Talk=null;HT23.speech.length=0;debugFight.spawned=true;boss=null;bossActive=false;warnT=0;enemies=[];eBullets=[];DBGT.god=false;run.shield=0;run.lives=5;player.dead=false;player.out=false;player.invuln=0;player.x=PLAY.x+PLAY.w*.5;player.y=PLAY.y+PLAY.h*.6;window.deathArt=[];const get=XART.get.bind(XART);XART.get=function(k){deathArt.push(k);return get(k)};hammerLaser(player.x,player.y,Math.PI/2,.01,true);}")
  p.evaluate(STEP,5)
  checks['native_laser_kills']=p.evaluate("player.dead&&player._dr21Death?.kind===\"laser\"")
  checks['captured_current_hull']=p.evaluate("!!player._dr21Death?.image&&deathArt.some(k=>k==='fury_base'||k.startsWith('sm10_fury'))")
  for i in range(15):
   p.evaluate(STEP,7);p.screenshot(path=str(O/f'frame-{i:02}.png'))
  checks['current_fury_pixels_drawn']=p.evaluate("deathArt.some(k=>k==='fury_base'||k.startsWith('sm10_fury'))")
  checks['no_legacy_eradication']=p.evaluate("!deathArt.includes('arch_pilot_eradication')&&!player._hammerEvap&&!player._eradicated")
  checks['laser_sequence_completed']=p.evaluate('!!player._dr21Death?.ended')
  checks['no_browser_errors']=not errors
  (O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors,keys=p.evaluate("[...new Set(deathArt.filter(k=>k.includes('fury')||k.includes('eradication')))]")),indent=2))
  br.close()
finally:stop()
print(json.dumps(checks));assert all(checks.values())

