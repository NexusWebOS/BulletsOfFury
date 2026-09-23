"""Real Chromium probe of the Stage 9 pilot-POV intercept and hand poses."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import base64, io, json, sys, http.server
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
from shoot import GAME,SETUP,STEP,TRAP_RAF,serve
OUT=ROOT/'_shots/cockpit_pov_0923';OUT.mkdir(exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=serve(GAME);errors=[];results={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1500,'height':1000})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>window.__bofFrames>4')
  pg.evaluate(TRAP_RAF)
  setup=pg.evaluate(SETUP,{'state':'PLAY','stage':9,'pilot':'axel','invuln':True})
  assert setup['ok'],setup
  pg.evaluate("()=>{run.pilot='axel';setState(GS.INTRO);proceedIntro();}")
  pg.wait_for_function('()=>cockpitEncounterReady()',timeout=45000)
  assert pg.evaluate('()=>PILOTS.every(p=>{const c=cockpitHandTint(p.key);return !!c&&c.width===2172&&c.height===724;})')
  def capture(name):
   pg.evaluate(STEP,1)
   data=base64.b64decode(pg.evaluate("document.getElementById('screen').toDataURL('image/png').split(',')[1]"))
   (OUT/(name+'.png')).write_bytes(data)
   im=Image.open(io.BytesIO(data))
   results[name]={'size':im.size,'state':pg.evaluate('()=>state'),
                  'pilot':pg.evaluate('()=>cockpitEncounter&&cockpitEncounter.pilot'),
                  'hand':pg.evaluate('()=>cockpitEncounter&&cockpitEncounter.handFrame')}
  pg.evaluate(STEP,175)
  assert pg.evaluate('()=>cockpitEncounter.enemies.length')>=1
  e0=pg.evaluate('()=>{let e=cockpitEncounter.enemies[0];return cockpitEnemyProject(e,cutsceneViewWidth(),VH).size}')
  capture('male_neutral')
  pg.evaluate("()=>{Input.keys['arrowleft']=true;}")
  pg.evaluate(STEP,8);capture('male_left')
  assert pg.evaluate('()=>cockpitEncounter.handFrame')==1
  pg.evaluate("()=>{Input.keys['arrowleft']=false;Input.keys['arrowright']=true;}")
  pg.evaluate(STEP,8);capture('male_right')
  assert pg.evaluate('()=>cockpitEncounter.handFrame')==2
  pg.evaluate("()=>{Input.keys['arrowright']=false;Input.mouse.down=true;}")
  capture('male_fire')
  assert pg.evaluate('()=>cockpitEncounter.handFrame')==3
  pg.evaluate("()=>{Input.mouse.down=false;let c=cockpitEncounter;c.enemies=[{seq:98,x:0,y:0,z:5,age:0,hp:1,key:'ns9x_horizon_0'}];let p=cockpitEnemyProject(c.enemies[0],cutsceneViewWidth(),VH);c.aimX=p.x;c.aimY=p.y;c.fireCd=0;Input.mouse.down=true;}")
  pg.evaluate(STEP,1)
  assert pg.evaluate('()=>cockpitEncounter.kills')>=1
  pg.evaluate("()=>{Input.mouse.down=false;let c=cockpitEncounter;Input.injectTap('pad_b1');c.enemies=[{seq:99,x:0,y:0,z:1.21,age:0,hp:1,key:'ns9x_horizon_0'}];}")
  hull=pg.evaluate('()=>cockpitEncounter.hull')
  pg.evaluate(STEP,2)
  assert pg.evaluate('()=>cockpitEncounter.hull')==hull
  pg.evaluate("()=>{Input.mouse.down=false;cockpitEncounter.pilot='falva';}")
  capture('female_neutral')
  pg.evaluate("()=>{Input.mouse.down=true;}")
  capture('female_fire')
  pg.evaluate("()=>{Input.mouse.down=false;cockpitEncounter.t=25.5;cockpitEncounter.enemies=[];}")
  pg.evaluate(STEP,1)
  assert pg.evaluate('()=>state')==pg.evaluate('()=>GS.LAUNCH')
  capture('stage9_launch')
  pg.evaluate(STEP,100)
  capture('stage9_launch_later')
  assert not errors,errors
  results['perspective_size_early']=e0
  results['errors']=errors
  (OUT/'results.json').write_text(json.dumps(results,indent=2))
  print('PASS: cockpit frames, male/female pilot swaps, fire, perspective and Stage 9 transition; no browser errors')
  br.close()
finally:stop()
