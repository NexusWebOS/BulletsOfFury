import sys,json,base64
from pathlib import Path
sys.path.insert(0,str(Path('_BUILD_SOURCE').resolve()))
from shoot import GAME,serve,SETUP,STEP,TRAP_RAF
from playwright.sync_api import sync_playwright
O=Path('_shots/overlord_sonic_0922');O.mkdir(exist_ok=True)
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
  def cap(n):
   (O/(n+'.png')).write_bytes(base64.b64decode(ev('()=>cv.toDataURL().split(",")[1]')))
  ev(SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':True})
  r['damage']=ev('''()=>{let a=[];for(const pk of ['cole','axel']){run.pilot=pk;for(const p of [.2,.5,1]){pBullets=[];sonicRelease(p);a.push({pk,p,damage:pBullets[0].dmg,boss:pBullets[0]._bossDmg});}}run.pilot='cole';return a;}''')
  ev('''()=>{diffKey='furious';spawnBoss('damkeeper');boss.enter=false;boss._ovIntro=null;boss._noHit=false;boss._ovAirborne=false;
    stagePlan=[];waveIdx=999;_adaptiveSpawnT=999;spawnClock=9999;player.invuln=1e9;player.x=VW*.5;player.y=VH*.77;
    window.waveLog=[];window.volleyLog=[];window.beepLog=[];
    const wave=ovSonicWave;ovSonicWave=function(b,v){waveLog.push({vertical:v,a:b._ovSonic.angle,t:b._ovSonic.t});return wave(b,v);};
    const volley=ovSonicMissileVolley;ovSonicMissileVolley=function(b,i){volleyLog.push({i,x:b.x,y:b.y,state:b._ovState});return volley(b,i);};
    const beep=Audio.SFX.retinaLockBeep;Audio.SFX.retinaLockBeep=function(){if(boss._ovSonic?.phase==='missileTell')beepLog.push(boss._ovSonic.t);return beep?.();};}''')
  step(2)
  # Reentry is the native handoff after the rain sweeps; do not call the new combo directly.
  ev('''()=>{boss._ovState='reentry';boss._re={t:4,from:-1};boss.x=VW*.5;boss.y=VH*.23;boss._pivot=0;playerLocks=[];eBullets=[];}''')
  step(2);r['handoff']=ev('()=>boss._ovSonic?.phase')
  step(22);cap('tell_green');step(45);cap('tell_yellow');step(40);cap('tell_red')
  step(25);cap('wave_horizontal');step(40);cap('wave_vertical');step(40);cap('wave_horizontal_last')
  step(75);cap('missile_tell')
  step(240);cap('moving_missile_volleys')
  r['waves']=ev('()=>waveLog');r['volleys']=ev('()=>volleyLog');r['beeps']=ev('()=>beepLog')
  r['missiles']=ev('()=>eBullets.filter(b=>b._ovSonicMissile).map(b=>({shootable:b._shootable,lock:b._lockId,homing:b.homing}))')
  # Keep one just-launched missile on screen to exercise the native interception path.
  ev('''()=>{eBullets=[];pBullets=[];ovSonicMissileVolley(boss,7);window.targetMissile=eBullets[0];
    targetMissile.x=player.x;targetMissile.y=player.y-95;targetMissile.vx=0;targetMissile.vy=2.3;
    pBullets.push({kind:'mg',lv:1,x:targetMissile.x,y:targetMissile.y+10,vx:0,vy:-8,w:8,h:16,dmg:3});}''')
  step(2);r['intercepted']=ev('()=>targetMissile.dead===true')
  r['collision']=ev('''()=>{const q={x:240,y:240,ang:Math.PI/2,_waveW:190,_waveH:46};return {
    center:ovSonicWaveHit(q,{x:240,y:240},9,10),edgeSafe:!ovSonicWaveHit(q,{x:360,y:240},9,10),
    cornerSafe:!ovSonicWaveHit(q,{x:322,y:267},9,10)};}''')
  # Same base/critical plates side by side, using the real XART and game canvas.
  ev('''()=>{for(const k of ['ovbody_intact','ovbody_critical'])XART.rdy(k);}''');pg.wait_for_timeout(400)
  ev('''()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#10151c';ctx.fillRect(0,0,cv.width,cv.height);
    for(let i=0;i<2;i++){let k=i?'ovbody_critical':'ovbody_intact',im=XART.get(k);ctx.drawImage(im,30,40+i*340,300,300);ctx.drawImage(ovFuryPlate(k),400,40+i*340,300,300);}ctx.restore();}''');cap('palette_comparison')
  r['nonFurious']=ev('''()=>{diffKey='hard';boss._ovSonic=null;boss._ovState='reentry';boss._re={t:4.01,from:-1};updateOverlordX(boss,.02);return {state:boss._ovState,sonic:!!boss._ovSonic};}''')
  # Let the native enraged rain-sweep sequence reach the new combo without forcing its endpoint.
  ev('''()=>{diffKey='furious';boss.hp=boss.maxhp*.45;boss._ovState='fight';boss._ovSonic=null;boss._ovChargeCd=.01;
    boss._ovPassUsed=false;boss._ovPassSeq=null;boss._ovFurySingleRam=false;boss._rageStarted=false;
    boss.x=VW/2;boss.y=VH*.22;boss._pivot=0;eBullets=[];pBullets=[];playerLocks=[];player.invuln=1e9;
    window.rainCalls=0;const rain=ovPassRain;ovPassRain=function(){rainCalls++;return rain.apply(this,arguments);};}''')
  for i in range(45):
   step(60)
   if ev('()=>!!boss._ovSonic'):break
  r['naturalSweep']=ev('()=>({rain:rainCalls,combo:!!boss._ovSonic,state:boss._ovState})');cap('natural_sweep_combo')
  # Native roll and somersault must protect against the actual hostile pressure-front collision.
  r['evasion']={}
  for mode in ['roll','somer','none']:
   ev('''(mode)=>{boss._ovSonic=null;boss._ovState='fight';boss._ovChargeCd=100;boss.fireCd=100;
     enemies=[];eBullets=[];pBullets=[];playerLocks=[];player.dead=false;player.alive=true;player.x=VW*.5;player.y=VH*.78;
     player.invuln=0;player.roll=null;player.somer=null;player._rollCool=0;player._somerCool=0;run.shield=0;
     XART.rdy('ship_cole_so0');window.hitBefore=run.lives;
     if(mode==='roll')startRoll(1);else if(mode==='somer')startSomersault();
     eBullets.push({kind:'ovSonic',_ovSonicWave:true,x:player.x,y:player.y-7.8,vx:0,vy:7.8,w:190,h:46,_waveW:190,_waveH:46,ang:Math.PI/2,t:0});}''',mode)
   pg.wait_for_timeout(80)
   if mode=='somer':ev('()=>startSomersault()')
   step(2);r['evasion'][mode]=ev('()=>({dead:player.dead,invuln:player.invuln,roll:!!player.roll,somer:!!player.somer})')
  r['errors']=errors;br.close()
finally:stop()
(O/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
assert not errors,errors
assert [q['damage'] for q in r['damage'] if q['pk']=='cole']==[q['damage']*1.5 for q in r['damage'] if q['pk']=='axel']
assert r['handoff']=='waveTell'
assert [q['vertical'] for q in r['waves']]==[False,True,False]
assert len(r['volleys'])==3 and len({round(q['x']) for q in r['volleys']})>1
assert len(r['beeps'])==6,r['beeps']
assert r['intercepted'] and all(r['collision'].values())
assert r['nonFurious']=={'state':'fight','sonic':False}
assert r['naturalSweep']['rain']>0 and r['naturalSweep']['combo']
assert not r['evasion']['roll']['dead'] and r['evasion']['roll']['roll']
assert not r['evasion']['somer']['dead'] and r['evasion']['somer']['somer']
assert r['evasion']['none']['dead']
