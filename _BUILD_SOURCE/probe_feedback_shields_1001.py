"""Native Furnace/miniboss shield hits through the shared elemental gate."""
from pathlib import Path
import json,base64,http.server
import shoot as sh
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/feedback_1001';OUT.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
port,stop=sh.serve(str(ROOT));errors=[];report=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1100,'height':1000})
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate("()=>{run.mode='arcade';run.pilot='cole';diffKey='normal';DIFF=DIFFS.normal;beginStage(2);setState(GS.PLAY);player.reset();story=null;stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];player.invuln=9999;spawnBoss('infernoreaver');bossActive=true;}")
  for i in range(90):
   r=p.evaluate(sh.STEP,30);assert r is None,r
   p.wait_for_timeout(40)
   if p.evaluate("()=>boss?._fz?.phase==='arms'&&!boss._fz.trans"):break
  assert p.evaluate("()=>boss?._fz?.phase==='arms'"),'Furnace never reached arms phase'
  for i in range(12):p.evaluate(sh.STEP,4);p.wait_for_timeout(60)
  for role in ['boss','miniboss']:
   if role=='miniboss':
    p.evaluate("()=>{boss=null;bossActive=false;spawnSubBoss__inner('magmaward');subBossActive=true;subBoss.enter=false;subBoss._be=null;subBoss._noHit=false;subBoss.x=worldWidth()/2;subBoss.y=170;subBoss._drawY=170;subBoss._er26.mode='recover';window.B=subBoss;}")
    for i in range(8):p.evaluate("()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}");p.wait_for_timeout(80)
   else:p.evaluate('()=>window.B=boss')
   p.evaluate("()=>{floaters=[];B._elemCritNext=0;if(B._mwBarrier){B._mwBarrier.active=true;B._mwBarrier.hp=200;}_lastHitX=B.x;_lastHitY=B.y;_dmgBullet={kind:'iceorb',_el:'ice'};}")
   r=p.evaluate("""role=>{const pool=B._mwBarrier||B,before=pool.hp;if(role==='boss')hitBoss(20);else hitSubBoss(20,B.x,B.y);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return {role,before,after:pool.hp,color:hitFlashColor(B),labels:floaters.filter(f=>f.elementCrit).length,phase:B._fz?.phase};}""",role)
   report.append(r);(OUT/(role+'_ice_shield.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL()').split(',')[1]))
  b.close()
finally:stop()
(OUT/'shields.json').write_text(json.dumps({'cases':report,'errors':errors},indent=2),encoding='utf-8')
print(json.dumps({'cases':report,'errors':errors},indent=2))
assert not errors
assert all(r['before']-r['after']==30 and r['labels']==1 and r['color']=='#83d9ff' for r in report)
