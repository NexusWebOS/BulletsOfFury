"""Live native enemy/weapon/item cue ownership. Audio is muted only in this
accelerated route probe; every unique sample has a separate audible-output test.
"""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/furious_encounters_1102/audio';O.mkdir(exist_ok=True)
report=dict(enemies=[],weapons=[],items=[],missiles=[],missing=[],errors=[],encounters=[])
def save():(O/'live-routes.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.set_default_timeout(180000);p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['errors'].append(m.text[:700])if m.type=='error'or'draw error'in m.text else None)
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load');p.wait_for_function('window.__bofFrames>5');p.mouse.click(4,4);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
 p.evaluate('''()=>{window.routeCalls=[];window.routeMissing=new Set();const old=Snd.play;Snd.play=function(name){routeCalls.push(name);if(!Snd.pools[name])routeMissing.add(name);return old.apply(this,arguments);};window.routeFunctions=[];for(const[k,f]of Object.entries(Audio.SFX))if(typeof f==='function')Audio.SFX[k]=function(){routeFunctions.push(k);return f.apply(this,arguments);};Snd.vol.master=0;window.routeReset=()=>{routeCalls=[];routeFunctions=[];window.routeShots=0;window.routeSeen=new WeakSet();};window.routeTick=()=>{for(let j=0;j<30;j++){updatePlay(1/60);for(const r of eBullets)if(!routeSeen.has(r)){routeSeen.add(r);routeShots++;}}};window.routeResult=()=>({shots:routeShots,cues:[...new Set(routeCalls)],functions:[...new Set(routeFunctions)]});}''')
 for stage in range(1,10):
  p.evaluate('s=>{EA11.setup(s,"furious");debugUnlocked=true;DBGT.god=true;Snd.vol.master=0;Audio.stopMusic();}',stage);specs=p.evaluate('EA11.collect()');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}')
  for spec in specs:
   if spec['type']in['cloudcarrierbridge','cloudcarrierbay']:continue
   p.evaluate('s=>{EA11.case(s);stagePlan=[];CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;routeReset();}',spec)
   for i in range(24 if spec['type']!='cbreak'else 100):
    p.evaluate('()=>{routeTick();if(routeShots<2){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}}');p.wait_for_timeout(2)
   row=p.evaluate('routeResult()');row.update(stage=stage,type=spec['type'],pattern=spec['pattern']);report['enemies'].append(row);save()
  print('STAGE',stage,len(specs),'cases; fired-but-silent',sum(r['shots']>0 and not r['cues']and not r['functions']for r in report['enemies']),flush=True)
  p.screenshot(path=str(O/f'stage{stage}-routes.png'))
 # All nine pilots, nine physical weapon choices and the three native space
 # weapons are exercised. Locked/non-firing combinations remain labelled.
 pilots=p.evaluate('PILOTS.map(p=>p.key)')
 for pilot in pilots:
  for stage in [1,5]:
   p.evaluate('q=>{EA11.setup(q.stage,"furious");pilotIndex=PILOTS.findIndex(p=>p.key===q.pilot);run.pilot=q.pilot;PILOTMOD={...PILOTS[pilotIndex]};stagePlan=[];debugUnlocked=true;DBGT.god=true;run._earnedUnlocks={lightningOrb:true,chaingun:true,laserMist:true};run.bombs=40;Snd.vol.master=0;Audio.stopMusic();}',dict(stage=stage,pilot=pilot))
   for weapon in range(9 if stage==1 else 3):
    q=p.evaluate('''w=>{pBullets=[];run.weapon=w;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);run.spaceWeapon=w;run.spaceLevels=[5,5,5];special=null;player._fuse=0;player._orbCd=0;player.fireCd=0;routeReset();const n=pBullets.length;pShoot();for(let i=0;i<100;i++)updatePlay(1/60);return{...routeResult(),rounds:pBullets.length-n,types:[...new Set(pBullets.map(p=>p.kind))]};}''',weapon);q.update(pilot=pilot,stage=stage,weapon=weapon);report['weapons'].append(q);save()
   q=p.evaluate('''()=>{routeReset();pBullets=[];player._fuse=0;run.bombs=40;useBomb(null);for(let i=0;i<30;i++)updatePlay(1/60);return{...routeResult(),types:[...new Set(pBullets.map(p=>p.kind))]};}''');q.update(pilot=pilot,stage=stage);report['missiles'].append(q);save()
 # Native pickup application owns these sounds, including space accessories.
 p.evaluate('()=>{EA11.setup(1,"furious");stagePlan=[];Snd.vol.master=0;Audio.stopMusic();}')
 for kind in ['speed','shield','life','missilepack','retinascan','weapon','special','sonicbox','lzmgbox','spacehelper','spaceakimbo','spacemine','scrate','mcrate','capsule']:
  try:q=p.evaluate('''kind=>{routeReset();applyPowerup({kind,x:player.x,y:player.y,wtype:0,wvar:0});return routeResult();}''',kind)
  except Exception as e:q=dict(error=str(e))
  q['kind']=kind;report['items'].append(q);save()
 report['missing']=p.evaluate('[...routeMissing]');report['routingErrors']=p.evaluate('AQ112.errors');b.close()
report['suspectEnemies']=[r for r in report['enemies']if r['shots']>0 and not r['cues']and not r['functions']]
report['suspectWeapons']=[r for r in report['weapons']if r['types']and not r['cues']and not r['functions']]
save();print('DONE',len(report['enemies']),'enemy cases;',len(report['weapons']),'weapon/pilot cases;',len(report['items']),'items; missing',report['missing'],'suspects',len(report['suspectEnemies']),len(report['suspectWeapons']),'errors',len(report['errors']),flush=True)
