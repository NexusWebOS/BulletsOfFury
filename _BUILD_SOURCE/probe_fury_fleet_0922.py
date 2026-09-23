import sys,json,base64
from pathlib import Path
sys.path.insert(0,str(Path('_BUILD_SOURCE').resolve()))
from shoot import GAME,serve,SETUP,STEP,TRAP_RAF
from playwright.sync_api import sync_playwright
O=Path('_shots/fury_fleet_0922');O.mkdir(exist_ok=True);errors=[];r={};port,stop=serve(GAME)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1280,'height':1000})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html');pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(TRAP_RAF)
  def ev(s,a=None):return pg.evaluate(s,a)
  def step(n):
   while n>0:
    v=ev(STEP,min(n,45));assert not v,v;n-=45;pg.wait_for_timeout(25)
  def cap(n,draw=True):
   if draw:step(1)
   (O/(n+'.png')).write_bytes(base64.b64decode(ev("()=>cv.toDataURL().split(',')[1]")))
  def setup(stage=6):
   assert ev(SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})['ok']
   ev("()=>{s6Opening=null;stagePlan=[];waveIdx=999;_adaptiveSpawnT=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];groundTargetingReset();aminiTriggered=true;subBossTriggered=true;subBossDone=true;_sc1=true;_sc2=true;player.x=worldWidth()/2;player.y=VH*.84;diffKey='furious';DIFF=DIFFS.furious;s6Wing=null;}")
  setup(1)
  ev("""()=>{window.fleetKeys=[];for(let v=0;v<4;v++)for(const [p,n] of [['bank',3],['roll',8],['pitch',8],['turn',8]])for(let f=0;f<n;f++)fleetKeys.push('furyjet_'+v+'_'+p+'_'+f);
  for(let v=0;v<2;v++)for(let f=0;f<3;f++)fleetKeys.push('furyboat_'+v+'_'+f);fleetKeys.forEach(k=>XART.rdy(k));}""")
  pg.wait_for_function('()=>fleetKeys.every(k=>XART.rdy(k))',timeout=45000)
  r['decoded']=ev('()=>fleetKeys.length')
  # Real renderer art review at a fixed scale: all attitudes, not CSS transforms.
  for pose in ['bank','roll','pitch','turn']:
   ev("""p=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#14232e';ctx.fillRect(0,0,cv.width,cv.height);ctx.imageSmoothingEnabled=false;
   for(let v=0;v<4;v++)for(let f=0;f<(p==='bank'?3:8);f++)ctx.drawImage(XART.get('furyjet_'+v+'_'+p+'_'+f),f*80,v*95,80,80);ctx.restore();}""",pose)
   cap('atlas_'+pose,False)
  ev("()=>{window.jets=['s1jetdelta','s1jetbomber','s1jetdelta_b','s1jetbomber_b'].map((k,i)=>spawnEnemy(k,camLeftX()+65+i*110,125,{route:'straight'}));window.boats=['s1boatgun','s1boatpatrol'].map((k,i)=>spawnEnemy(k,camLeftX()+145+i*155,255,{}));}")
  cap('stage1_fleet')
  ev("()=>jets.forEach((e,i)=>{e.x=camLeftX()+65+i*110;e.y=145;e._furyMove=null;});")
  r['evades']=ev("""()=>jets.map(e=>{e._furyEvadeCd=0;furyJetEvadeTick(e,.01,1);const first=e._furyMove.kind;furyJetEvadeTick(e,.6,0);const finished=!e._furyMove;e._furyEvadeCd=0;furyJetEvadeTick(e,.01,-1);return {first,finished,second:e._furyMove.kind,hp:e.hp};})""")
  for phase in [0,.25,.5,.75]:
   ev("(t)=>{for(const e of jets)e._furyMove={kind:'roll',t:t*.58,dur:.58};}",phase);cap('roll_'+str(phase))
  ev("()=>{for(const e of jets)e._furyMove={kind:'pitch',t:.29,dur:.58};for(const e of boats)e.hp=e.maxhp*.25;}")
  cap('loop_and_damaged_boats')
  # Count rotations in the actual new hull draw.
  r['hullRotations']=ev("""()=>{let n=0;const old=ctx.rotate;ctx.rotate=function(){n++;return old.apply(this,arguments)};try{jets.forEach(e=>furyFleetDraw(e));return n;}finally{ctx.rotate=old;}}""")
  r['directions']={}
  for direction in ['south','north','east','west']:
   setup()
   ev("d=>{window.jet=s6StrikeSpawn(d);window.origin={x:jet.x,y:jet.y};window.sites=[];}",direction)
   for i in range(7):
    step(18)
    ev("()=>{for(const q of groundTargetingFx)if(q._strikeMissile&&!sites.some(a=>a.q===q))sites.push({q,x:q.x,y:q.y});}")
    if i in [2,4,6]:cap(direction+'_'+str(i))
   step(180)
   r['directions'][direction]=ev("()=>({dx:jet.x-origin.x,dy:jet.y-origin.y,racks:jet._s6Strike.racks,exited:!!jet.dead,sites:sites.length,locked:sites.every(s=>!s.q.track&&s.q.x===s.x&&s.q.y===s.y),impacts:sites.filter(s=>s.q.impact).length})")
  r['difficulties']=ev("""()=>['easy','normal','hard','furious'].map(d=>{
   diffKey=d;groundTargetingReset();const e=s6StrikeSpawn('south');let seen=[];
   for(let i=0;i<160;i++){s6StrikeTick(e,1/60);groundTargetingTick(1/60);for(const q of groundTargetingFx)if(!seen.includes(q))seen.push(q);}
   return {difficulty:d,racks:e._s6Strike.racks,warn:seen[0].warn};
  })""")
  r['cap']=ev("""()=>{diffKey='furious';groundTargetingReset();for(let i=0;i<8;i++){
   const e=s6StrikeSpawn('south');e.y=100;e._s6Strike.cd=0;s6StrikeTick(e,.01);
  }return groundTargetingFx.filter(q=>q._strikeMissile).length;}""")
  r['damage']=ev("""()=>{groundTargetingReset();let hits=0;const old=playerHit;playerHit=()=>hits++;try{
   const q=groundTargetingSpawn({kind:'missile',x:player.x,y:player.y,track:false,lane:false,warn:1.25});
   groundTargetingTick(1);const before=hits;player.y-=70;groundTargetingTick(.35);const outside=hits;player.y=q.y;groundTargetingTick(.01);groundTargetingTick(.01);return {before,outside,inside:hits};
  }finally{playerHit=old;}}""")
  r['cancel']=ev("""()=>{const a={x:100,y:100,hp:10},q={owner:a,_strikeMissile:{launched:false},warn:1.25,t:.3};a.dead=true;s6StrikeMissileTick(q);
   const b={x:100,y:100,hp:10},p={owner:b,_strikeMissile:{launched:false},warn:1.25,t:.7};s6StrikeMissileTick(p);b.dead=true;s6StrikeMissileTick(p);
   return {before:!!q.dead,after:!p.dead&&p._strikeMissile.launched};}""")
  # Replay the actual authored wave callbacks and keep cardinal paths through the main loop.
  setup()
  r['plan']=ev("""()=>{let dirs=[];const old=s6StrikeSpawn;s6StrikeSpawn=d=>dirs.push(d);try{for(const w of buildStagePlan(6))if(String(w.fn).includes('s6StrikeSpawn'))w.fn();return dirs;}finally{s6StrikeSpawn=old;}}""")
  ev("()=>{stagePlan=buildStagePlan(6).filter(w=>w.t>=8&&w.t<=12);waveIdx=0;stageTimer=8;s6WingInit();window.strikesSeen=0;window.oldStrike=s6StrikeSpawn;s6StrikeSpawn=function(d){strikesSeen++;return oldStrike(d);};}")
  step(270);cap('native_stage6_wave')
  r['nativeWave']=ev("()=>{s6StrikeSpawn=oldStrike;return strikesSeen;}")
  ev(SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':True})
  r['stageReset']=ev("()=>groundTargetingFx.length")
  r['errors']=errors;br.close()
finally:stop()
(O/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
assert not errors,errors
assert r['decoded']==114 and r['hullRotations']==0
assert all(q['first']=='roll' and q['finished'] and q['second']=='pitch' for q in r['evades'])
for d,q in r['directions'].items():
 assert abs(q['dx'] if d in ['south','north'] else q['dy'])<.001,(d,q)
 assert q['racks']==3 and q['sites']>=2 and q['locked'] and q['exited'],(d,q)
assert [q['racks'] for q in r['difficulties']]==[1,1,2,3]
assert [q['warn'] for q in r['difficulties']]==[1.65,1.45,1.25,1.25]
assert r['cap']==5
assert r['damage']=={'before':0,'outside':0,'inside':1}
assert r['cancel']=={'before':True,'after':True}
assert r['plan']==['south','north','east','west','south','north','east']
assert r['nativeWave']>=1 and r['stageReset']==0
