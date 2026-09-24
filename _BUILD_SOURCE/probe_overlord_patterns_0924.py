"""Overlord sequence contracts plus authored-art captures in real Chromium."""
import sys, json, base64
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from shoot import GAME, serve, SETUP, STEP, TRAP_RAF
from playwright.sync_api import sync_playwright

OUT=Path(GAME)/'_shots/overlord_patterns_0924'
OUT.mkdir(parents=True,exist_ok=True)
port,stop=serve(GAME)
report={};errors=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  page=browser.new_page(viewport={'width':1280,'height':1080})
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/index.html')
  page.wait_for_function('()=>(window.__bofFrames|0)>4')
  page.evaluate(TRAP_RAF)
  ev=page.evaluate
  def step(n):
   while n>0:
    batch=min(n,30);assert not ev(STEP,batch);n-=batch;page.wait_for_timeout(20)
  def capture(name):
   (OUT/(name+'.png')).write_bytes(base64.b64decode(ev('()=>cv.toDataURL().split(",")[1]')))
  ev(SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':True})
  ev('''()=>{stagePlan=[];waveIdx=999;_adaptiveSpawnT=999;spawnClock=9999;player.invuln=1e9;
    window.resetOV=function(d){diffKey=d;DIFF=DIFFS[d];spawnBoss('damkeeper');boss.enter=false;boss._ovIntro=null;
      boss._noHit=false;boss._ovAirborne=false;boss.x=VW/2;boss.y=VH*.22;boss._pivot=0;
      enemies=[];eBullets=[];pBullets=[];playerLocks=[];powerups=[];player.x=VW/2;player.y=VH*.8;
      updateOverlordX(boss,1/60);return boss;};resetOV('normal');
    for(const k of ['ovbody_intact','ovrotor_00','rzb_sonic_wave','mlaunch_3',
      'bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall',
      'bmfx_alert_green_danger','bmfx_alert_yellow_danger','bmfx_alert_red_danger'])XART.rdy(k);
  }''')
  page.wait_for_function("()=>['ovbody_intact','rzb_sonic_wave','mlaunch_3','bmfx_fov_red_tall'].every(k=>XART.rdy(k))")
  report['contracts']=ev('''()=>{
    const result=[];const mg=ovTwinMG,rocket=ovRocketSide,wave=ovSonicWave;
    try{for(const d of ['normal','hard','furious']){
      const b=resetOV(d),row={difficulty:d},tune=ovAttackTune();let shots=[],rockets=[],fans=[];
      ovTwinMG=function(b,sweep){const before=eBullets.length;mg(b,sweep);if(sweep){
        const m=ovFacingMount(b,-10,54),q=eBullets[before];shots.push({pass:b._ovSweep.pass,x:b.x,a:b._pivot,anchor:Math.hypot(q.x-m.x,q.y-m.y)});}};
      ovRocketSide=function(b,side,fan){rockets.push({side,t:b._ovVolley?.t});rocket(b,side,fan);};
      ovSonicWave=function(b,v){const n=eBullets.length;wave(b,v);fans.push({fan:v,count:eBullets.length-n,south:eBullets.slice(n).every(q=>q._south&&q.vy>0)});};
      ovStartSweep(b);let n=0;while(b._ovState==='gunSweep'&&n++<1200){updateOverlordX(b,1/60);eBullets=[];}
      row.sweep={passes:new Set(shots.map(q=>q.pass)).size,shots:shots.length,anchored:shots.every(q=>q.anchor<.001),
        bank:Math.max(...shots.map(q=>Math.abs(q.a)))*180/Math.PI,charge:b._ovState==='chargeTell',bounded:n<1200};
      b._chargeTell=null;ovSonicStart(b);n=0;
      while(b._ovState==='sonicCombo'&&n++<1000){updateOverlordX(b,1/60);eBullets=[];}
      row.sonic={fans,salvoHandoff:b._ovState==='missileLock'};n=0;
      while(b._ovState==='missileLock'&&n++<1000){updateOverlordX(b,1/60);eBullets=[];}
      row.missiles={left:rockets.filter(q=>q.side<0).length,right:rockets.filter(q=>q.side>0).length,
        staggered:rockets.every((q,i)=>!i||q.t>rockets[i-1].t),rushHandoff:b._ovState==='zoneRush'};
      let legs=[],locks=[],last=-1,phase='',start=0,clock=0,committed=true;n=0;
      while(b._ovState==='zoneRush'&&n++<4000){
        const r=b._ovRush;clock+=1/60;player.x=clock%1<.5?30:VW-30;
        if(r.phase!==phase){if(phase==='lock')locks.push(clock-start);phase=r.phase;start=clock;}
        if(r.phase==='charge'){if(last!==r.leg){last=r.leg;legs.push({leg:r.leg,dir:r.dir,lane:r.lane});}committed=committed&&Math.abs(b.x-r.lane)<.001;}
        updateOverlordX(b,1/60);
      }
      row.rush={legs,locks,committed,restored:b._ovState==='fight'&&Math.abs(b.y-VH*.22)<.01&&b._pivot===0,bounded:n<4000};
      result.push(row);
    }}finally{ovTwinMG=mg;ovRocketSide=rocket;ovSonicWave=wave;}return result;
  }''')
  # Real native update/render: enter through ordinary opening MG rather than calling sweep.
  ev("()=>{resetOV('furious');window.statesOV=[];}")
  for i in range(90):
   step(30)
   state_now=ev('()=>boss._ovState')
   if state_now not in report.setdefault('nativeStates',[]):report['nativeStates'].append(state_now)
   if state_now=='gunSweep' and 'sweepCaptured' not in report:
    capture('furious_sweep');report['sweepCaptured']=True
   if state_now=='zoneRush':break
  ev("()=>{resetOV('furious');ovStartSweep(boss);boss._ovSweep.phase='travel';boss._ovSweep.side=1;boss.x=VW*.4;boss._pivot=-25*Math.PI/180;}")
  step(12);capture('sweep_anchored')
  ev("()=>{eBullets=[];boss._ovSweep=null;ovSonicStart(boss);boss._ovSonic.phase='waves';boss._ovSonic.sent=1;boss._ovSonic.t=.64;}")
  step(18);capture('south_three_wave_fan')
  ev("()=>{eBullets=[];ovStartMissileLock(boss);}")
  step(66);capture('missile_warning_pods')
  step(38);capture('staggered_missiles')
  ev("()=>{eBullets=[];boss._ovVolley=null;ovStartRush(boss);boss.y=-boss.h;ovRushLeg(boss);}")
  step(15);capture('rush_all_zones')
  step(26);capture('rush_committed_zone')
  step(34);capture('rush_charge')
  # All four authored lane plates remain visible during selection; no FOV during a missile tell.
  report['warningRoutes']=ev('''()=>{let lanes=0,cones=0,alerts=0;
    const fov=l23FovDraw,alert=l23WarnSymbolDraw;
    l23FovDraw=function(){cones++;return fov.apply(this,arguments);};
    l23WarnSymbolDraw=function(){const shown=alert.apply(this,arguments);if(shown)alerts++;return shown;};
    try{resetOV('furious');ovStartMissileLock(boss);boss._ovVolley.t=1.1;drawBossSprite(boss);
      const missile={cones,alerts};cones=0;alerts=0;
      boss._ovVolley=null;ovStartRush(boss);ovRushLeg(boss);boss._ovRush.t=.22;boss._ovRush.active=2;
      ovRushWarningDraw(boss,false);lanes=cones;
      boss._ovRush.phase='lock';boss._ovRush.t=.03;ovRushWarningDraw(boss,true);
      return {missile,lanes,lockAlert:alerts>0};
    }finally{l23FovDraw=fov;l23WarnSymbolDraw=alert;}}''')
  report['evasion']={}
  ev("()=>{XART.rdy('ship_cole_so0');}");page.wait_for_timeout(100)
  for mode in ['roll','somer','clear','none']:
   ev('''mode=>{resetOV('furious');player.dead=false;player.alive=true;player.invuln=0;player.roll=null;player.somer=null;
     player._rollCool=0;player._somerCool=0;run.shield=0;run.lives=5;special=null;
     ovStartRush(boss);ovRushLeg(boss);const r=boss._ovRush;r.phase='charge';r.dir=1;r.lane=player.x;
     r.t=((player.y+boss.h)/(VH+boss.h*2))*r.tune.travel-1/60;
     boss.x=r.lane;boss.y=player.y-30;
     if(mode==='clear')player.x=r.lane+120;
     if(mode==='roll')startRoll(1);if(mode==='somer')startSomersault();}''',mode)
   step(2)
   report['evasion'][mode]=ev('()=>({dead:!!player.dead,lives:run.lives,invuln:player.invuln})')
  report['errors']=errors
  browser.close()
finally:stop()
(OUT/'report.json').write_text(json.dumps(report,indent=2))
for row in report['contracts']:
 d=row['difficulty'];s=row['sweep'];m=row['missiles'];r=row['rush']
 assert s['passes']==(3 if d=='furious' else 1) and s['anchored'] and s['bounded'] and s['charge'],row
 assert 24<s['bank']<26,row
 assert row['sonic']['salvoHandoff'] and all(f['south'] and f['count']==(3 if f['fan'] else 1) for f in row['sonic']['fans']),row
 assert m['left']==m['right']=={'normal':2,'hard':4,'furious':8}[d] and m['staggered'] and m['rushHandoff'],row
 assert len(r['legs'])==(12 if d=='furious' else 4) and all(q['dir']==(1 if i%2==0 else -1) for i,q in enumerate(r['legs'])),row
 assert r['committed'] and r['restored'] and r['bounded'] and all(t>=.33 for t in r['locks']),row
assert all(s in report['nativeStates'] for s in ['gunSweep','chargeTell','chargeOff','reentry','sonicCombo','missileLock','zoneRush']),report['nativeStates']
assert report['warningRoutes']=={'missile':{'cones':0,'alerts':1},'lanes':4,'lockAlert':True},report['warningRoutes']
assert all(not report['evasion'][m]['dead'] and report['evasion'][m]['lives']==5 for m in ['roll','somer','clear']),report['evasion']
assert report['evasion']['none']['dead'] or report['evasion']['none']['lives']<5,report['evasion']
assert not errors,errors
print('PASS: all three difficulties, native sequence, anchors, 2/4/8-per-side missiles, south-facing fans, and 4/4/12 committed rush legs. No browser errors.')
