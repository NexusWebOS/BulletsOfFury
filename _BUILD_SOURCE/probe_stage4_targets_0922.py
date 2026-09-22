import sys,json,base64
from pathlib import Path
sys.path.insert(0,str(Path('_BUILD_SOURCE').resolve()))
from shoot import GAME,serve,SETUP,STEP,TRAP_RAF
from playwright.sync_api import sync_playwright
O=Path('_shots/stage4_targets_0922');O.mkdir(exist_ok=True)
port,stop=serve(GAME);r={};errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  qa=br.new_context(storage_state={'cookies':[],'origins':[]},viewport={'width':1280,'height':1080})
  pg=qa.new_page();pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html');pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(TRAP_RAF)
  def ev(s,arg=None):return pg.evaluate(s,arg)
  def step(n):
   while n>0:
    z=ev(STEP,min(60,n));assert not z,z;n-=60;pg.wait_for_timeout(30)
  def cap(n): (O/(n+'.png')).write_bytes(base64.b64decode(ev('()=>cv.toDataURL().split(",")[1]')))
  ev(SETUP,{'state':'PLAY','stage':4,'pilot':'cole','invuln':True})
  setup='''(mini)=>{diffKey='hard';DIFF=DIFFS.hard;run.stage=4;curStage=STAGES[3];
    stagePlan=[];waveIdx=999;_adaptiveSpawnT=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];
    boss=null;bossActive=false;subBoss=null;subBossActive=false;player.dead=false;player.invuln=1e9;
    if(mini){spawnSubBoss('olivewarden');window.enc=subBoss;}else{spawnBoss('stormsovereign');window.enc=boss;}
    enc.enter=false;enc.x=worldWidth()/2;enc.y=enc._s4war.homeY;enc._drawY=enc.y;enc._noHit=false;
    if(mini){stage4MiniEscortEnsure(enc);for(const d of enc._s4war.drones){d.active=1;d.t=1;d.fireCd=999;}}
    else {enc.hp=enc.maxhp*.49;stage4CoreTurretSpawnMissing(enc,.5);for(const t of enc._s4war.coreTurrets){t.materialize=1;t.spawnT=1;t.state='windup';}}
    player.x=VW/2;player.y=VH*.82;}
  '''
  ev(setup,True);step(90)
  pg.wait_for_function("()=>XART.rdy('nsb_olivewarden_intact')&&XART.rdy('s4w_warden_gunner_0919')&&XART.rdy('s4w_warden_rocketeer_0919')")
  step(2);cap('miniboss_helpers')
  r['miniSize']=ev('()=>({w:subBoss.w,h:subBoss.h,helpers:subBoss._s4war.drones.map(d=>d.size)})')
  ev(setup,False);step(100);cap('warship_helpers')
  r['helperSize']=ev('()=>({size:S4H_SIZE,positions:boss._s4war.coreTurrets.map(t=>({x:t.x,y:t.y})),left:camLeftX(),right:camRightX()})')
  # Exercise actual weapon simulation at a helper outside the central hull.
  r['damage']=[]
  for mini in [True,False]:
   for kind in ['mg','spread','laser','missile','gmiss','beam','flame','orb']:
    ev(setup,mini)
    info=ev('''({mini,kind})=>{let d=mini?enc._s4war.drones[0]:enc._s4war.coreTurrets[0];window.victim=d;
      player.x=d.x;player.y=d.y+140;const q={kind,x:d.x,y:d.y+6,vx:0,vy:-6,w:12,h:18,dmg:12,life:2,t:0,lv:2,_hit:[],_ht:0,_bt:0,spin:0,frame:0,shardCd:99,shardN:4,_el:kind==='orb'?'ice':'fire'};
      if(kind==='missile'){q.spd=6;q.turn=0;}
      if(kind==='gmiss'){q.spd=6;q.tgt=retinaBossTargets(enc).find(t=>t.part===d);}
      if(kind==='beam'){q.w=18;q.top=-20;q.bot=player.y-14;}
      window.testShot=q;pBullets.push(q);return {mini,kind,target:!!q.tgt,valid:q.tgt?retinaTargetValid(q.tgt):null,before:d.hp+(d.shield||0)};}''',{'mini':mini,'kind':kind})
    step(80 if kind=='gmiss' else 2);info['after']=ev('()=>victim.hp+(victim.shield||0)');info['shot']=ev('()=>({x:testShot.x,y:testShot.y,dead:!!testShot.dead,target:!!testShot.tgt,vx:victim.x,vy:victim.y,materialize:victim.materialize})');r['damage'].append(info)
  # Place rounds below the boss so neither hull can consume the test weapon first.
  r['interception']=[]
  for mini in [False,True]:
   for kind in ['mg','beam','orb']:
    ev(setup,mini)
    ev('''(kind)=>{player.x=worldWidth()/2;player.y=VH*.86;window.round=stage4WarfareShot(enc,{x:player.x,y:player.y-85},Math.PI/2,1.5,'orb',{shootable:true,hp:3});
      pBullets.push({kind,x:round.x,y:round.y+8,vx:0,vy:-5,w:24,h:28,life:2,dmg:12,t:0,lv:2,spin:0,frame:0,shardCd:99,shardN:4,_hit:[],_ht:0,_el:'ice'});}''',kind)
    step(2);r['interception'].append(ev('''({mini,kind})=>({mini,kind,dead:!!round.dead,proof:!!round._weaponProof})''',{'mini':mini,'kind':kind}))
  ev(setup,False)
  r['mirrorProtected']=ev('''()=>{eBullets=[];let q=stage4WarfareShot(enc,{x:240,y:420},Math.PI/2,2,'spread',{});chromeMirror(240,420,40,1);return !q.dead;}''')
  ev('()=>stage4CoreEnrageStart(enc,enc._s4war.shield.nodes[0])');step(70);cap('enraged_helpers')
  # Follow a full Furious phase cycle, including the telegraphed ram and safe return.
  ev(setup,True);ev("()=>{diffKey='furious';DIFF=DIFFS.furious;player.x=VW*.5;player.y=VH*.88;}")
  r['cycle']=[]
  for i in range(30):
   step(60)
   r['cycle'].append(ev("()=>({mode:subBoss._s4war.mode,x:subBoss.x,y:subBoss.y,ram:subBoss._s4war.miniRamCount,left:camLeftX(),right:camRightX(),w:subBoss.w})"))
  cap('furious_cycle')
  r['errors']=errors;br.close()
finally:stop()
(O/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
assert not errors,errors
assert all(q['after']<q['before'] for q in r['damage']),r['damage']
assert all(not q['dead'] for q in r['interception'] if not q['mini']),r['interception']
assert all(q['dead'] for q in r['interception'] if q['mini']),r['interception']
assert r['mirrorProtected']


assert any(q['ram']>0 for q in r['cycle'])
assert all(q['x']-q['w']/2>=q['left']-4 and q['x']+q['w']/2<=q['right']+4 for q in r['cycle'] if q['mode'] not in ['hardRam','hardReturn'])
