"""Real Chromium coverage of all newly touched encounters and visual owners."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/audio_1010';OUT.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
def check(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name,flush=True)
 if not value:print(json.dumps(data),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1280,height=900));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(650,450)
  def frames(n):
   for i in range(0,n,30):
    err=p.evaluate(shoot.STEP,min(30,n-i))
    if err:errors.append(err);break
    p.wait_for_timeout(3)
  def scene(n,pilot='yuri'):
   p.evaluate(shoot.SETUP,dict(state='PLAY',stage=n,pilot=pilot,invuln=True))
   p.wait_for_function('n=>{stageLoadTick();return stageLoadInfo(n).ready}',arg=n,polling=50)
   p.evaluate("()=>{BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;H3.release=false;H3.ending=null;stagePlan=[];enemies=[];pBullets=[];eBullets=[];powerups=[];special=null;boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;player.invuln=1e9;}")
  def shot(name):
   p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);fb9HudSplit();}')
   p.screenshot(path=str(OUT/(name+'.png')))
  scene(2);p.evaluate("spawnBoss('infernoreaver')");frames(190);shot('furnace-chain')
  frames(420);shot('furnace-shield')
  q=p.evaluate('()=>({mode:boss._fz?.phase,draws:AP10_FIRE.draws,barrier:boss._mwBarrier})')
  check('Furnace forms before its 32-frame shield and uses authored animated chains',q['draws'].get('chain',0)>0 and q['draws'].get('fire_shield',0)>0,q)
  p.evaluate("()=>{boss._mwBarrier.active=false;boss._mwBarrier.breakT=.5;}");shot('furnace-shatter')
  scene(3);p.evaluate("spawnBoss(curStage.boss)");frames(200)
  p.evaluate("()=>{boss.enter=false;boss._l23Beam=null;er26Set(boss,'cannon-relay');}")
  frames(210);shot('ice-laser-live')
  q=p.evaluate('AP10_FX.draws');check('Actual icy laser and muzzles render from boss hardpoints',q.get('iceBeam',0)>0 and q.get('iceMuzzle',0)>0,q)
  scene(5,'cole');p.evaluate("()=>{run.spaceWeapon=1;run._spaceShadowCharge=FUSION30_FULL*1.75;run._spaceShadowHeld=true;}");shot('fusion-charge-live')
  p.evaluate("spaceShadowRelease(FUSION30_FULL*1.75)");frames(6);shot('fusion-release-live')
  q=p.evaluate('AP10_FX.draws');check('Space fusion charge and moving beam use new art',q.get('fusionCharge',0)>0 and q.get('fusionBeam',0)>0,q)
  p.evaluate("()=>{pBullets=[];for(const [i,k]of ['s5frigate','s5gravity','s5station'].entries())spawnEnemy(k,120+i*120,130,{});}")
  frames(720);shot('space-fleet-live')
  q=p.evaluate("()=>({events:AP10_FLEET.events.filter(q=>q.event==='space-attack'),moving:enemies.filter(e=>['s5frigate','s5gravity','s5station'].includes(e._s5space)).map(e=>({type:e._s5space,x:e.x,y:e.y,t:e._ap10Flight?.t})),bullets:eBullets.length})")
  check('Space frigate, gravity and station units move and actually fire',len({e['type'] for e in q['events']})>=3 and len(q['moving'])==3 and all((e.get('t') or 0)>1 for e in q['moving']),q)
  scene(6);p.evaluate("()=>{stageTimer=22;s6WingInit();s6WingTick(.02);}")
  q=p.evaluate("s6Wing.ships.length");check('Four allies arrive alongside the player early in Stage 6',q==4,q)
  p.evaluate("()=>{enemies=[];fb2Flights.length=0;fb2FlightPlan('south','red');fb2FlightPlan('south','green');spawnEnemy('s6dart',360,240,{});}");frames(140);shot('stealth-palettes-live')
  q=p.evaluate("enemies.filter(e=>e._ap10Palette).map(e=>({type:e.type,palette:e._ap10Palette,facing:e._sm10Facing}))")
  check('Red, green and blue stealth plates face south',set(e.get('palette') for e in q)=={'red','green','blue'} and all(e.get('facing')=='south' for e in q),q)
  p.evaluate("()=>{enemies=[];H3.release=true;fb2Talk=null;s6Opening=null;updatePlay(.016);}");check('Completed dialogue releases the fire latch immediately',p.evaluate('H3.release')==False)
  scene(6);p.evaluate("()=>{run._gp4StageX='left';spawnBoss('warhive');boss.enter=false;boss._whv.cy=boss.y=WHV_HOME_Y;boss._whv.st='open';boss._whv.can.cd=0;boss._whv.can.i=1;}")
  p.evaluate("whvCannonTick(boss,.01)");shot('stagex-cannon-warning')
  q=p.evaluate("()=>({seq:boss._whv.can.seq,hard:boss._whv.hard})");check('Normal Harrier cannons commit a warned volley',q['seq'] is not None and q['seq'].get('ap10Warm')==.7 and q['hard']==False,q)
  p.evaluate("()=>{const W=boss._whv;W.parts.L.dead=W.parts.R.dead=true;W.core=W.coreMax*.48;whvCarrierTick(boss,.016);}")
  q=p.evaluate("({mode:boss._whv.mode,core:boss._whv.core,max:boss._whv.coreMax})");check('Stage X does not die at half HP when fans are destroyed',q['mode']=='carrier' and q['core']>0 and q['core']<q['max'],q)
  p.evaluate("()=>{boss._whv.core=0;whvCarrierTick(boss,.016);}");check('Stage X ends its hull phase only at zero core HP',p.evaluate("boss._whv.mode")=='death')
  p.evaluate("delete run._gp4StageX")
  scene(8);p.evaluate("spawnBoss('vileexistence')");frames(30);p.evaluate("()=>{boss.x=240;boss.y=205;boss._r30.mode='takeover';boss._r30.t=1.5;}");shot('drone-consumption-live')
  check('Consumption plate actually draws during takeover',p.evaluate('AP10_C.draws.consumption||0')>0)
  for phase in [0,1]:
   p.evaluate("n=>{j3Encounter(boss,n);boss._r30.mode='fight';boss.enter=false;boss._r30.t=0;boss._r30.cd=.1;}",phase)
   frames(1100);shot('alien-phase-'+str(phase+1)+'-live')
   q=p.evaluate("n=>AP10_A.events.filter(q=>q.event==='projectile'&&q.phase===n).length",phase)
   check('Final encounter '+str(phase+1)+' produces sustained actual attacks',q>=20,q)
  scene(4);p.evaluate("()=>{run.mode='campaign';run.forgeElems={};run.forge={};run.forgeForms={};run.forgeCombos=30;run._earnedUnlocks={chaingun:true,laserMist:true,lightningOrb:true};forgeComboGrant('wind');}")
  outcomes=[]
  for w in range(9):
   q=p.evaluate("w=>{const result=forgeCombine(w,'wind'),selected=forgeSelect(w,'wind');run.weapon=w;run.wlevel=3;run.wlevels[w]=3;special=null;player._fuse=0;player._chgOn=false;run._spaceShadowCharge=0;pBullets=[];player._orbCd=0;pShoot();return{w,result,selected,form:run.forgeForms[w]?.wind,bullets:pBullets.map(b=>({kind:b.kind,elem:b._inf||b._el}))};}",w)
   frames(5);shot('wind-weapon-'+str(w));outcomes.append(q)
  check('All nine native Wind recipes craft and select',all(q['result']=='ok' and q['selected']=='ok' and q.get('form') for q in outcomes),outcomes)
  check('No page, console or asset errors',not errors,errors)
  br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
(OUT/'full-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
