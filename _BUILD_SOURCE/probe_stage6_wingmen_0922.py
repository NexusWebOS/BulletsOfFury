import sys,json,base64,math
from pathlib import Path
sys.path.insert(0,str(Path('_BUILD_SOURCE').resolve()))
from shoot import GAME,serve,SETUP,STEP,TRAP_RAF
from playwright.sync_api import sync_playwright
O=Path('_shots/wing_0922');O.mkdir(exist_ok=True)
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
  def cap(name):
   step(1);(O/(name+'.png')).write_bytes(base64.b64decode(ev("()=>cv.toDataURL().split(',')[1]")))
  def setup():
   ev(SETUP,{'state':'PLAY','stage':6,'pilot':'cole','invuln':True})
   ev('()=>{s6Opening=null;enemies=[];eBullets=[];pBullets=[];powerups=[];groundTargetingReset();stageTimer=0;stagePlan=[];waveIdx=999;_adaptiveSpawnT=999;spawnClock=9999;aminiTriggered=true;_sc1=true;_sc2=true;player.x=worldWidth()/2;player.y=VH*.84;s6WingInit();s6Wing.beats=2;}')
  setup()
  r['independence']=ev('''()=>{
    const runAt=x=>{player.x=x;let q={key:'axel',x:camLeftX()+85,y:180,slot:0,t:4,phase:'fight',hp:3,fcd:0};let W={ships:[q],choice:false};
      for(let i=0;i<120;i++){q.t+=1/60;s6WingNavigate(q,W,1/60);}return {x:q.x,y:q.y};};
    return [runAt(camLeftX()+30),runAt(camRightX()-30)];
  }''')
  ev('()=>{s6WingLaunch(8,true);s6Wing.all=true;stageTimer=53;subBossDone=true;}')
  step(350)
  ev('()=>{s6Wing.line=null;player.invuln=0;}');cap('independent_squadron')
  r['squadron']=ev('()=>s6Wing.ships.map(q=>({key:q.key,x:q.x,y:q.y,phase:q.phase,hp:q.hp}))')
  r['drawHeights']=ev('''()=>{const calls=[],orig=ctx.drawImage;ctx.drawImage=function(){if(arguments.length===5)calls.push(arguments[4]);return orig.apply(this,arguments);};try{s6WingDraw();}finally{ctx.drawImage=orig;}return calls;}''')
  # A real friendly projectile must damage a live enemy, not only exist in the array.
  setup();ev('''()=>{s6Wing.ships=[{key:'axel',x:player.x,y:300,slot:0,t:5,hp:3,phase:'fight',fcd:0}];spawnEnemy('s6thunder',player.x,135,{});window.victim=enemies[0];victim.hp=200;victim.pattern='none';victim.vy=0;}''')
  step(70);r['nativeDamage']=ev('()=>({hp:victim.hp,bullets:pBullets.filter(b=>b.ally).map(b=>({kind:b.kind,w:b.w,h:b.h})),ship:s6Wing.ships[0].phase})');cap('support_fire')
  r['dodge']=ev('''()=>{let q=s6Wing.ships[0];q.x=camLeftX()+130;q.y=280;q.dodgeCd=0;q.dodgeT=0;q.target=null;enemies=[];eBullets=[{x:q.x,y:q.y-90,vx:0,vy:6,w:8,h:12}];s6WingNavigate(q,s6Wing,1/60);return {dodge:q.dodgeT,mode:q.dodgeMode,dx:q.evadeX-q.x};}''')
  cap('authored_evasion')
  # Side runs: native shared reticles, immutable landing sites, racks and visible falling bombs.
  r['bombers']={}
  for difficulty in ['easy','normal','hard','furious']:
   setup();ev('(d)=>{diffKey=d;spawnEnemy("s6bomber",camLeftX()-90,VH*.23,{_jetManeuver:"bomb"});window.bomber=enemies[0];window.sites=[];}',difficulty)
   for i in range(5):
    step(30)
    if difficulty=='furious':cap('bomb_run_'+str(i))
    ev('()=>{for(const q of groundTargetingFx)if(q._jetBomb&&!sites.some(a=>a.q===q))sites.push({q,x:q.x,y:q.y});}')
   r['bombers'][difficulty]=ev('()=>({racks:bomber._jetManeuver.racks,sites:sites.map(s=>({x:s.x,y:s.y,dx:s.q.x-s.x,dy:s.q.y-s.y,warn:s.q.warn,track:s.q.track,impact:s.q.impact}))})')
  # Ground strike damage respects the warning interval and normal dodge invulnerability.
  r['warningDamage']=ev('''()=>{enemies=[];eBullets=[];groundTargetingReset();let n=0;const old=playerHit;playerHit=()=>n++;
    try{let q=groundTargetingSpawn({x:player.x,y:player.y,warn:1.25,active:.5,track:false,lane:false});groundTargetingTick(1);let before=n;groundTargetingTick(.34);return {before,after:n};}finally{playerHit=old;}}''')
  # Exercise the real late-stage wave plan with the full squad and normal input.
  setup();ev('''()=>{diffKey='furious';stagePlan=buildStagePlan(6).filter(w=>w.t>=52);waveIdx=0;stageTimer=52;
    subBossDone=true;subBossTriggered=true;s6WingLaunch(8,true);s6Wing.all=true;run.weapon=0;run.wlevel=3;player.invuln=1e9;}''')
  pg.keyboard.down('j')
  for i in range(20):
   if i%4==0:pg.keyboard.down('ArrowLeft' if i%8==0 else 'ArrowRight')
   if i%4==2:pg.keyboard.up('ArrowLeft');pg.keyboard.up('ArrowRight')
   step(60)
   if i in [4,9,14]:cap('furious_action_'+str(i))
   if ev('()=>s6Wing.choice&&!s6Wing.route'):break
  pg.keyboard.up('j');pg.keyboard.up('ArrowLeft');pg.keyboard.up('ArrowRight')
  r['battle']=ev('()=>({choice:s6Wing.choice,ships:s6Wing.ships.map(q=>({key:q.key,hp:q.hp,phase:q.phase})),enemies:enemies.length})')
  cap('route_choice');pg.keyboard.down('ArrowLeft');step(2);pg.keyboard.up('ArrowLeft');step(2)
  r['route']=ev('()=>s6Wing.route')
  # Render the reused source art at inspection scale using the game's own canvas.
  ev("()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#10151c';ctx.fillRect(0,0,cv.width,cv.height);let im=XART.get('lz_bomb');ctx.drawImage(im,80,80,im.width*2,im.height*2);ctx.restore();}")
  (O/'bomb_source.png').write_bytes(base64.b64decode(ev("()=>cv.toDataURL().split(',')[1]")))
  r['errors']=errors;br.close()
finally:stop()
(O/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
assert not errors,errors
assert math.dist(list(r['independence'][0].values()),list(r['independence'][1].values()))<.01
assert len(r['squadron'])==8 and all(q['phase']=='fight' for q in r['squadron'])
assert r['drawHeights'].count(60)==8  # Ship draws; supply icons have their own sizes.
assert r['nativeDamage']['hp']<200
assert r['dodge']['dodge']>0
for d,n in [('easy',1),('normal',1),('hard',2),('furious',3)]:
 assert r['bombers'][d]['racks']==n,(d,r['bombers'][d])
 assert all(not q['track'] and q['dx']==0 and q['dy']==0 for q in r['bombers'][d]['sites'])
assert r['warningDamage']=={'before':0,'after':1}
assert r['battle']['choice'] and r['route']=='left'

