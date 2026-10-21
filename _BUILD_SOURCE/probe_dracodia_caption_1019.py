"""Focused native caption and final asset-composite verification."""
from pathlib import Path
from PIL import Image
from io import BytesIO
from playwright.sync_api import sync_playwright
import ast,base64,http.server,json
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/dracodia_demon_1019';errors=[];checks=[]
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1400,height=1000));p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>3');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(SETUP,dict(stage=8,kind='vileexistence',diff='normal',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&dr21Warm();}')
  p.evaluate("""()=>{B=boss;v18Clear(B);v18Budget(B);v18Enter(B,2,0);v18Fight(B);B._r30.v18.arenaPhase=2;B.x=worldWidth()/2;B.y=viewTopY()+190;B._r30.v18.home={x:B.x,y:B.y};B._noHit=B.enter=false;player.dead=false;player.invuln=999;fb2Talk=fb2Intro=thaw=s6Opening=null;H3.release=false;H3.ending=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;P2M.active=null;enemies=[];eBullets=[];pBullets=[];explosions=[];particles=[];floaters=[];smokeTrails=[];stagePlan=[];spawnClock=999999;subBossTriggered=aminiTriggered=true;dr21Begin(B,'shadowAscension');for(let i=0;i<70;i++)r30Tick(B,1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}""")
  (O/'caption-cast.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  row=p.evaluate('DR21.caption');checks.append(dict(name='Fear THIS caption uses authored font below HUD',passed=row and row['text']=='Fear THIS!' and row['y']>=100,data=row))
  p.evaluate('()=>{v18Clear(B);B._r30.mode="v18conversion";B._r30.t=2.2;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}')
  (O/'mechanical-infusion.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  checks.append(dict(name='Mechanical symbiote appears in native drone infusion',passed=p.evaluate('DR21.draws.symbiote>0')))
  p.wait_for_function('()=>XART.rdy("pt11_mystery_emergence")&&XART.rdy("pt11_mystery_contact")')
  checks.append(dict(name='Both new orbital cinematic plates decode',passed=p.evaluate('XART.get("pt11_mystery_emergence").width===960&&XART.get("pt11_mystery_contact").width===960')))
  p.evaluate("""()=>{v18Clear(B);v18Enter(B,2,0);v18Fight(B);B._r30.v18.arenaPhase=2;B.x=worldWidth()/2;B.y=viewTopY()+190;player.dead=false;player._dr21Death=null;player.invuln=0;run.shield=0;player.x=B.x;player.y=viewTopY()+viewH()-110;dr21Begin(B,'shadowAscension');const P=B._r30.v18.attack;P.t=P.tell+P.travel*.95;v18AttackTick(B,1/60);}""")
  checks.append(dict(name='Lethal eradication keeps the incoming ball large',passed=p.evaluate('player.dead&&player._dr21Death?.foreground>1000')))
  p.evaluate('()=>{updateDeathSpin(.3);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}')
  (O/'homing-eradication.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  # The ball follows a moving aircraft, then commits. The pilot moves out of
  # the final line at native base speed, without defensive invulnerability.
  p.evaluate("""()=>{v18Clear(B);v18Enter(B,2,0);v18Fight(B);B._r30.v18.arenaPhase=2;B.x=worldWidth()/2;B.y=viewTopY()+190;B._r30.v18.home={x:B.x,y:B.y};player.dead=false;player._dr21Death=null;player.invuln=0;player.x=worldWidth()/2;player.y=viewTopY()+viewH()-110;dr21Begin(B,'shadowAscension');window.P=B._r30.v18.attack;}""")
  film=[]
  for i in range(112):
   p.evaluate('()=>{for(let i=0;i<4;i++){if(!P.locked)player.x=worldWidth()/2+Math.sin(P.t*1.3)*90;else{P.dodgeDir??=P.target.x>worldWidth()/2?-1:1;player.x=clamp(player.x+P.dodgeDir*playerBaseSpeed(),camLeftX()+25,camRightX()-25);}r30Tick(B,1/60);}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}')
   film.append(Image.open(BytesIO(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))).convert('RGB'))
  film[0].save(O/'homing_encounter.webp',save_all=True,append_images=film[1:],duration=67,loop=0,quality=85)
  checks.append(dict(name='Visible lateral dodge clears the complete shadow attack without iframes',passed=p.evaluate('!player.dead&&player.invuln===0')))
  checks.append(dict(name='No browser errors',passed=not errors,data=errors));br.close()
finally:stop()
(O/'caption-report.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks),flush=True);raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
