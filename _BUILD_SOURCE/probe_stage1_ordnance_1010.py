"""Real Chromium: Furious Razorback missiles and Overlord sonic-wave counterplay.

Uses shoot.py's local server/manual clock and the existing balance fixture. These
protected, isolated attacks establish behavior/pixels, not a human balance clear.
"""
from pathlib import Path
import base64, http.server, json, sys
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
import shoot

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/stage1_ordnance_1010'
OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];details={}
def check(name,passed,data=None):
    checks.append({'name':name,'pass':bool(passed),'data':data})
    print(('PASS ' if passed else 'FAIL ')+name,flush=True)

http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--mute-audio','--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport={'width':1280,'height':1000});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append('page: '+str(e)))
  p.on('console',lambda m:errors.append('console: '+m.text[:700]) if m.type=='error' else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000)
  p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(60)
  p.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  def setup(kind='razorback',diff='furious'):
   p.evaluate('(c)=>BAL7.setup({stage:1,kind:c.kind,mini:c.kind==="razorback",pilot:"cole",diff:c.diff,fire:false})',{'kind':kind,'diff':diff})
   p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(1).ready;}',polling=50)
   p.evaluate('''()=>{BAL7.q=null;BOFCinematicDirector.cancel();story=null;fb2Talk=null;special=null;
    B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=140;B._drawY=140;
    if(B._rzb){const R=B._rzb;R.state='guns';R.trans=0;R.attack='missiles';R.at=0;R.a=R.turret=0;R.beat=-1;R.tgt={x:B.x,y:B.y};}
    player.x=B.x;player.y=VH-85;player.dead=player.out=false;player.alive=true;player.invuln=999;player.roll=player.somer=null;
    enemies=[];eBullets=[];pBullets=[];playerLocks=[];powerups=[];run.shield=0;shake=whiteBlast=0;}''')
  keys=['rzbf_razor_missile','rzbf_sonic_charge','rzbf_hull_base','rzbf_turret','rzb_sonic_wave','rzb_sonic_ring','nst1_upper']
  p.evaluate('(keys)=>keys.forEach(k=>XART.rdy(k))',keys)
  p.wait_for_function('(keys)=>keys.every(k=>XART.rdy(k))',arg=keys,polling=50)
  def draw(name):
   p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);fb9HudSplit();}')
   path=OUT/(name+'.png');path.write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
   return path
  def step(n):
   for start in range(0,n,8):
    err=p.evaluate(shoot.STEP,min(8,n-start));check('Manual native frame batch has no loop exception',err is None) if err else None
    p.wait_for_timeout(4)
  setup()
  # The real rack queues its original Retina, then launches from its real pod.
  q=p.evaluate('''()=>{razorbackCombat(B);const L=playerLocks[0];return{locks:playerLocks.length,launches:L?.launches.length};}''')
  check('Furious rack retains its warned fourteen-missile sequence',q=={'locks':1,'launches':14},q)
  step(70)
  q=p.evaluate('()=>({missiles:eBullets.filter(q=>q.kind==="rzbMissile").map(q=>({spd:q.spd,shootable:q._shootable,proof:q._weaponProof,lock:!!q._lockId}))})')
  details['rack']=q
  check('Actual Retina launch emits a faster shootable missile',bool(q['missiles']) and all(m['spd']>=4.2 and m['shootable'] and not m['proof'] for m in q['missiles']),q)
  draw('furious-rack-launch')
  for straight in (False,True):
   setup()
   before=p.evaluate('''(straight)=>{subBossActive=bossActive=false;eBullets=[];rzbMissile(B,{x:B.x,y:250},0,straight);
    window.Q=eBullets[0];return{x:Q.x,y:Q.y,speed:Math.hypot(Q.vx,Q.vy),old:rzbPxFrame(straight?230:160,B),ang:Q.ang};}''',straight)
   step(20)
   after=p.evaluate('()=>({y:Q.y,speed:Math.hypot(Q.vx,Q.vy),spd:Q.spd,ang:Q.ang,dead:!!Q.dead})')
   details['flurry' if straight else 'regular']={'before':before,'after':after}
   check(('Flurry' if straight else 'Rack')+' missile launch speed is increased',before['speed']>before['old']*1.4,before)
   check(('Flurry' if straight else 'Rack')+' missile moves faster in the native simulation',after['y']-before['y']>before['old']*20*1.4,after)
   check(('Flurry' if straight else 'Rack')+' missile preserves its launch lane',abs(after['ang']-before['ang'])<.001,after)
   check('Regular missile acceleration is restored' if not straight else 'Committed flurry retains its fixed speed',after['spd']>before['speed'] if not straight else after['spd']==before['speed'],after)
  for kind in ['mg','spread','missile','beam','sonic','orb']:
   setup()
   r=p.evaluate('''(kind)=>{subBossActive=bossActive=false;eBullets=[];rzbMissile(B,{x:B.x,y:300},0,false);window.Q=eBullets[0];
    pBullets=[{kind,x:Q.x,y:Q.y,vx:0,vy:0,w:kind==='beam'?16:10,h:20,dmg:10,lv:1,t:0,top:PLAY.y,bot:player.y,pierce:kind==='beam'||kind==='sonic',_hit:[],_ht:.1}];
    updatePlay(.00001);return{dead:!!Q.dead,present:eBullets.includes(Q),proof:Q._weaponProof,fx:explosions.length};}''',kind)
   check(kind+' really intercepts a Furious miniboss missile',r['dead'] and not r['present'],r)
  setup()
  p.evaluate('()=>{subBossActive=false;rzbMissile(B,{x:B.x,y:300},0,false);window.Q=eBullets[0];}')
  before=draw('missile-before-hit')
  p.evaluate('()=>{pBullets=[{kind:"mg",x:Q.x,y:Q.y,vx:0,vy:0,w:8,h:16,dmg:4,t:0}];updatePlay(.00001);}')
  after=draw('missile-intercept-explosion')
  im=ImageChops.difference(Image.open(before).convert('RGB'),Image.open(after).convert('RGB'))
  check('Interception visibly replaces the missile with an authored explosion',im.getbbox() is not None and p.evaluate('Q.dead&&explosions.length>0'))
  for vertical in (False,True):
   for kind in ['mg','spread','missile','beam','sonic','orb']:
    setup('damkeeper')
    r=p.evaluate('''({vertical,kind})=>{bossActive=subBossActive=false;eBullets=[];ovSonicWave(B,vertical);window.W=eBullets.slice();
     for(const q of W){q.y=300;pBullets.push({kind,x:q.x,y:q.y,vx:0,vy:0,w:kind==='beam'?20:10,h:20,dmg:50,lv:1,t:0,top:PLAY.y,bot:player.y,pierce:true,_hit:[],_ht:.1});}
     updatePlay(.00001);return{count:W.length,alive:W.every(q=>!q.dead&&eBullets.includes(q)&&q._weaponProof&&!q._shootable&&!enemyOrdnanceCanIntercept(q))};}''',{'vertical':vertical,'kind':kind})
    check(('Narrow' if vertical else 'Broad')+' boss sonic wave survives '+kind,r['count']==(3 if vertical else 1) and r['alive'],r)
  setup('damkeeper')
  p.evaluate('()=>{ovSonicStart(B);B._ovSonic.t=1.5;}')
  draw('overlord-sonic-warning')
  p.evaluate('()=>{bossActive=subBossActive=false;eBullets=[];ovSonicWave(B,false);window.Q=eBullets[0];Q.y=270;}')
  draw('overlord-sonic-wave')
  r=p.evaluate('''()=>{player.x=Q.x;player.y=Q.y;player.invuln=0;run.shield=0;pBullets=[];updatePlay(.00001);return{playerDead:player.dead,waveAlive:!Q.dead&&eBullets.includes(Q)};}''')
  check('Unshootable sonic wave still damages the pilot and continues traveling',r['playerDead'] and r['waveAlive'],r)
  setup('damkeeper')
  r=p.evaluate('''()=>{bossActive=subBossActive=false;eBullets=[];ovSonicWave(B,false);window.Q=eBullets[0];
   run.pilot='juggernaut';special={pilot:'juggernaut',t:2};wreckInit();wreckTick(0);
   Q.x=wreckBalls[0].x;Q.y=wreckBalls[0].y;const pellet={kind:'mg',x:Q.x,y:Q.y,w:6,h:12};eBullets.push(pellet);wreckTick(0);
   return{alive:!Q.dead,count:wreckBalls.length,pelletDead:!!pellet.dead};}''')
  check('Juggernaut wrecking balls cannot destroy the boss sonic wave',r['alive'] and r['count']>0,r)
  check('Wrecking balls still destroy ordinary gunfire at that same position',r['pelletDead'],r)
  check('Native Chromium has no page, console or asset errors',not errors,errors)
  br.close()
finally:stop()
result={'checks':checks,'errors':errors,'details':details,'limits':'Protected isolated attacks; not a human campaign-clear or fairness claim.'}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(f'{sum(q["pass"] for q in checks)} passed / {sum(not q["pass"] for q in checks)} failed',flush=True)
if any(not q['pass'] for q in checks):raise SystemExit(1)
