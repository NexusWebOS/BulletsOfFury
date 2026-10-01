from pathlib import Path
import sys,json,base64,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/realm_0930';O.mkdir(exist_ok=True,parents=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot as sh
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
SETUP="""()=>{ht27Stop();debugFight=null;coopOn=false;diffKey='furious';DIFF=DIFFS.furious;run.pilot='yuri';run.mode='campaign';beginStage(8);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;special=null;thunderStorm=null;s6Opening=null;s6Wing=null;stagePlan=[];spawnClock=9999;waveIdx=999;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;player.x=worldWidth()/2;player.y=VH-110;player.invuln=999;spawnBoss('vileexistence');bossActive=true;r30Warm();return {hp:boss.hp,S:boss._r30};}"""
port,stop=sh.serve(str(R));errors=[];rows=[]
def check(v,n):
 rows.append({'ok':bool(v),'name':n});print(('OK ' if v else 'FAIL ')+n,flush=True)
def shot(p,n):
 p.evaluate('()=>drawWorld(0)');(O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1000,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>3',timeout=120000);p.evaluate(sh.TRAP_RAF)
  print(p.evaluate(SETUP),flush=True)
  p.wait_for_function("()=>Object.keys(REALM30_ART).every(k=>XART.rdy('r30_'+k))&&XART.rdy('enc30_entry')",timeout=120000)
  for t in [1,3,5]:p.evaluate('t=>boss._r30.t=t',t);shot(p,'takeover_'+str(t))
  p.evaluate('()=>{for(let i=0;i<100;i++)updateBoss(1/60);}');check(p.evaluate('()=>boss._r30.mode==="fight"'),'intro reaches fight')
  for form in range(3):
   p.evaluate('n=>{r30Form(boss,n);boss._r30.mode="fight";boss.enter=false;}',form)
   for attack in range([6,6,11][form]):
    p.evaluate('i=>{boss._r30.seq=i;boss._r30.attack=null;r30Attack(boss);updateBoss(.01);}',attack);shot(p,f'form{form}_attack{attack}_tell')
    p.evaluate('()=>{for(let i=0;i<75;i++)updateBoss(1/60);}');shot(p,f'form{form}_attack{attack}_active')
    p.evaluate('()=>{for(let i=0;i<400;i++)updateBoss(1/60);eBullets=[];enemies=[];}')
   check(p.evaluate('()=>Number.isFinite(boss.hp)&&boss.hp>0'),f'form {form} cycles without invalid HP')
  p.evaluate('()=>{r30Form(boss,0);boss._r30.mode="fight";boss.enter=false;r30Wall(boss,"datawall");}')
  check(p.evaluate('()=>{const e=enemies.find(e=>e._r30Wall);const hp=e.hp;hitEnemy(e,5);return e.hp===hp-5&&e.flash>0;}'),'wall takes damage and flashes')
  check(p.evaluate('()=>{const e=enemies.find(e=>e._r30Wall);hitEnemy(e,99999);return e.dead;}'),'wall destroyed opens gap')
  p.evaluate('()=>{for(const e of enemies)e.dead=true;enemies=[];}')
  for form in range(3):
   p.evaluate('n=>{r30Form(boss,n);boss._r30.mode="fight";boss.enter=false;boss._lastPart=boss.parts[0];modularHit(boss.maxhp+1);}',form)
   check(p.evaluate('()=>!bossDefeated&&!bossHealthVisible(boss)'),f'form {form} death hides bar without ending fight')
   for frames,label in [(50,'fall'),(140,'quiet'),(110,'reform'),(130,'reveal')]:
    p.evaluate('n=>{for(let i=0;i<n;i++)updateBoss(1/60);}',frames);shot(p,f'break{form}_{label}')
  p.evaluate('()=>{for(let i=0;i<600&&!boss._r30.rewarded;i++)updateBoss(1/60);}')
  check(p.evaluate('()=>run._realmReturned&&boss._r30.rewarded'),'portal reunion rewards only at completion')
  check(not errors,'no native browser errors')
  print('ERRORS',errors[:12],flush=True);b.close()
finally:
 stop();(O/'verification.json').write_text(json.dumps({'checks':rows,'errors':errors},indent=2))
sys.exit(0 if rows and all(v['ok'] for v in rows) and not errors else 1)
