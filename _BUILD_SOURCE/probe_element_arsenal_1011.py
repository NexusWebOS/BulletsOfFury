"""Native firing/collision matrix; stationary authored targets isolate each gun.

This is a protected weapon fixture, not a campaign clear or a balance benchmark.
Uses shoot.py, actual updatePlay, actual hits and the game context's drawImage.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/element_arsenal_1011/live';OUT.mkdir(parents=True,exist_ok=True)
checks=[];rows=[];errors=[]
def check(name,yes,data=None):
 checks.append(dict(name=name,passed=bool(yes),data=data));print(('PASS ' if yes else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page(viewport=dict(width=1100,height=950));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status}: {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=1,pilot='cole',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(1).ready}')
  p.evaluate('''()=>{
   window.ARSENAL_QA={hits:[],keys:new Set(),age:0,cd:0};const Q=ARSENAL_QA;
   const h=hitEnemy;hitEnemy=function(e,d){const before=e.hp,r=h.apply(this,arguments);if(before>e.hp)Q.hits.push({kind:_dmgBullet?.kind,el:damageProjectileElement(_dmgBullet),inf:_dmgBullet?._inf,seat:_dmgBullet?.seat,damage:before-e.hp});return r;};
   const get=XART.get;XART.get=function(k){Q.keys.add(k);return get.apply(this,arguments);};
   Q.equip=function(el,w,lv=3){run.weapon=w;run.wlevel=lv;run.wlevels=WEAPONS.map(()=>lv);run.wvars=WEAPONS.map(()=>null);run.forge={[w]:{elem:el,lv:1}};run.forgeForms={};run.infusion=null;forgeApply();
    if(w===5)run.wvars[5]=el==='fire'?'magmaorb':el+'orb';if(w===3&&el==='fire')run.wvars[3]='firewhip';yuriLightningOrbUnlocked=true;laserMistUnlocked=true;run._earnedUnlocks={lightningOrb:true,laserMist:true};};
   Q.reset=function(el,w,lv=3){ht27Stop();coopOn=false;diffKey='normal';run.mode='arcade';run.pilot='cole';run.stage=1;run.spaceMode=false;DIFF=difficultyForRun('arcade','normal');PILOTMOD={...PILOTS.find(q=>q.key==='cole')};run.lives=20;run.missileLevel=0;run.dkT=run.sonicT=0;run._chainHeat=run._chainOverheat=0;
    BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=special=thunderStorm=s6Opening=null;H3.ending=null;H3.release=false;AP10_X.intro=null;P2M.active=null;FS11.pending=null;FS11.boxes=[];
    boss=subBoss=null;bossActive=subBossActive=false;subBossDone=subBossTriggered=bossWarned=true;warnT=0;warnKind=null;stagePlan=[];aiQueue=[];spawnClock=9999;stageTimer=0;
    enemies=[];eBullets=[];pBullets=[];powerups=[];particles=[];pImpacts=[];efxBursts=[];fb10Clouds=[];voids=[];geysers=[];zoneCols=[];zaps=[];explosions=[];l5Rocks=[];l5RockT=99999;setState(GS.PLAY);player.reset();player.dead=player.out=false;player.invuln=40002;player.x=worldWidth()/2;player.y=VH*.8;camX=player.x-VW/2;player._orbCd=0;
    for(const k of Object.keys(Input.keys))Input.keys[k]=false;
    Q.equip(el,w,lv);if(w===8){run.pilot='yuri';PILOTMOD={...PILOTS.find(q=>q.key==='yuri')};}Q.hits=[];Q.keys.clear();Q.age=Q.cd=0;
    for(const dx of [-35,0,35]){spawnEnemy('scout',player.x+dx,player.y-120,{pattern:'straight'});const e=enemies.at(-1);e.hp=e.maxhp=10000;e._qaX=e.x;e._qaY=e.y;e.shoots=false;e._entry=0;}
   };
   Q.step=function(n,fire=true){for(let i=0;i<n;i++){Q.age+=1/60;Q.cd-=1/60;player.invuln=40002;
    for(const e of enemies){e.x=e._qaX;e.y=e._qaY;e.vx=e.vy=0;e.shoots=false;}
    if(fire&&Q.cd<=0){if(run.weapon===1&&run.infusion?.elem==='chrome')run._chromeSpreadRelease=1.6;pShoot();run._chromeSpreadRelease=0;Q.cd=Math.min(.3,_weaponCadence());}
    updatePlay(1/60);if(i%8===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}}
   };
  }''')
  elements=['fire','kinetic','lightning','water','ice','chrome','toxic','dark','wind']
  for el in elements:
   family=[]
   for w in range(9):
    p.evaluate('q=>ARSENAL_QA.reset(q.el,q.w)',dict(el=el,w=w))
    for batch in range(8):p.evaluate('ARSENAL_QA.step(15)');p.wait_for_timeout(5)
    q=p.evaluate('''()=>({hits:ARSENAL_QA.hits,keys:[...ARSENAL_QA.keys],state,draws:{...PA11.draws},bullets:pBullets.map(b=>({kind:b.kind,inf:b._inf,el:b._el,seat:b.seat,age:b._visualAge})),targets:enemies.map(e=>({hp:e.hp,burn:e._burn,poison:e._poison,soaked:e._soaked,frozen:e._frozen})),finite:[...pBullets,...enemies].every(b=>Number.isFinite(b.x+b.y))})''')
    q.update(element=el,slot=w);rows.append(q);family.append(q)
    if w in [0,4,5]:
     p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
     p.locator('#screen').screenshot(path=str(OUT/f'{el}-{w}.png'))
   check(el+': all nine weapons damage native targets',all(q['hits'] and q['finite'] for q in family),[dict(slot=q['slot'],hits=len(q['hits'])) for q in family])
   check(el+': successful direct hits retain their element',all(any(h.get('inf')==el and h.get('el')==el for h in q['hits']) for q in family))
   if el!='fire':check(el+': forged spray does not secretly burn targets',all(not e.get('burn',0) for e in family[4]['targets']))
  q=p.evaluate('''()=>{const Q=ARSENAL_QA;Q.reset('water',6);pShoot();const parents=pBullets.slice();Q.equip('fire',0);enemies=[];Q.step(32,false);return {parents:parents.map(b=>b._inf),children:pBullets.filter(b=>b._child).map(b=>({inf:b._inf,seat:b.seat,lv:b._infLv})),all:pBullets.map(b=>({kind:b.kind,inf:b._inf}))};}''')
  check('Switching mid-flight preserves both generations of water mist',q['children'] and all(b['inf']=='water' and b['seat']==1 for b in q['children']),q)
  q=p.evaluate('''()=>{const Q=ARSENAL_QA;Q.reset('fire',0);run.forge[2]={elem:'ice',lv:1};run.missileLevel=3;autoFireMissiles();const infused=pBullets.map(b=>b._inf);pBullets=[];delete run.forge[2];autoFireMissiles();return {infused,bare:pBullets.map(b=>b._inf)};}''')
  check('Automatic missiles use the missile recipe independently of the primary',q['infused']==['ice']*3 and q['bare']==[None]*3,q)
  q=p.evaluate('''()=>{const Q=ARSENAL_QA;Q.reset('water',3);pShoot();const b=pBullets.find(b=>b.kind==='beam');run.forge={};run.infusion=null;pShoot();return {inf:b?._inf,el:b?._el,damage:damageProjectileElement(b)};}''')
  check('Unforging a held laser clears its previous water identity',q.get('inf') is None and q.get('el')!='water' and q.get('damage')!='water',q)
  q=p.evaluate('''()=>{const Q=ARSENAL_QA;Q.reset('dark',3);run.pilot='maverick';run.forge={};run.infusion={elem:'dark',lv:1};run.wvars[3]='mavhoming';PILOTMOD={...PILOTS.find(q=>q.key==='maverick')};pShoot();return pBullets.map(b=>({kind:b.kind,lv:b.lv,dmg:b.dmg,inf:b._inf}));}''')
  check('Maverick homing lasers remain uninfused Level I at an upgraded laser slot',q and all(b['kind']=='mavlaser' and b['lv']==1 and b.get('inf') is None for b in q),q)
  for kind,w in [('beam',3),('flame',4)]:
   q=p.evaluate('''q=>{const Q=ARSENAL_QA;Q.reset('water',q.w);coopOn=true;run2.pilot='yuri';player2.reset();player2.dead=player2.out=false;player2.invuln=40002;player2.x=player.x+80;player2.y=player.y-30;pShoot();withSeat(2,()=>{Q.equip('toxic',q.w);pShoot();});Q.step(1,false);return pBullets.filter(b=>b.kind===q.kind).map(b=>({seat:b.seat,el:b._inf,x:b.x,owner:seatShip(b.seat).x}));}''',dict(w=w,kind=kind))
   check('Co-op '+kind+': separate element, entity and pilot anchor',len(q)==2 and {b['seat'] for b in q}=={1,2} and {b['el'] for b in q}=={'water','toxic'} and all(b['x']==b['owner'] for b in q),q)
  br.close()
finally:stop()
(OUT/'checks.json').write_text(json.dumps(dict(checks=checks,rows=rows,errors=errors),indent=2),encoding='utf-8')
print(json.dumps(dict(cases=len(rows),checks=len(checks),failed=[c['name'] for c in checks if not c['passed']],errors=errors)),flush=True)
sys.exit(1 if errors or any(not c['passed'] for c in checks) else 0)

