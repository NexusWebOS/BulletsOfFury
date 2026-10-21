"""Real Chromium: Stage4 lightning must survive actual player projectile collisions."""
from pathlib import Path
import ast,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1]; O=R/'_shots/storm_proof_1021'; O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1528,height=900));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&ASSETS.ready');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='yuri');run.pilot='yuri';startRun(4)")
  for diff in ['normal','hard','furious']:
   p.evaluate(SETUP,dict(stage=4,kind='stormsovereign',diff=diff,pilot='yuri'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(4)&&bmfReady("game")}')
   p.evaluate('''()=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=s6Opening=null;AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;
    VP12.next=CP12.next=EP13.next=HM17.next=TARGET17.nextTank=999999;stagePlan=[];warnT=0;warnKind=null;subBossTriggered=aminiTriggered=true;
    B._be=null;B.enter=false;B._noHit=false;B._phaseInvuln=0;B.x=worldWidth()/2;B.y=B._drawY=160;er26Tick(B,0);er26Set(B,'recover');B._er26.dur=999;
    player.x=worldWidth()/2;player.y=VH-50;player.invuln=1e9;run.shield=0;run.spaceMode=false;Input.keys={};camX=clamp(player.x-VW/2,0,worldWidth()-VW);SC12.refresh();__bofFit();}''')
   for role in ['orb','lightning','lightningmg','spread']:
    for weapon in ['mg','beam','gmiss','iceorb','flame']:
     row=p.evaluate('''({role,weapon})=>{eBullets=[];pBullets=[];enemies=[];
      window.Q=stage4WarfareShot(B,{x:player.x,y:VH-160},Math.PI/2,0,role,{shootable:true,hp:1});Q.vx=Q.vy=0;
      // Emulate stale family adapters attempting to restore interception flags.
      Q._weaponProof=false;Q._shootable=true;s3kOrdnanceRules(Q);
      pBullets=[{kind:weapon,x:Q.x,y:Q.y,w:60,h:60,vx:0,vy:0,dmg:999,t:0,life:2,top:PLAY.y,bot:VH,pierce:true,_hit:[],_ht:1,r:30}];
      for(let i=0;i<3;i++)updatePlay(1/60);
      return{dead:!!Q.dead,alive:eBullets.includes(Q),proof:Q._weaponProof,shootable:Q._shootable,intercept:enemyOrdnanceCanIntercept(Q),defense:enemyDefensiveProof(Q),impact:!!Q._fbImpact1002,kind:Q.kind};}''',dict(role=role,weapon=weapon))
     ck(diff+' '+role+' survives '+weapon+' collision',row['alive'] and not row['dead'] and row['proof'] and not row['shootable'] and not row['intercept'] and not row['impact'],row)
   # Actual helper missile release, which used a different interception policy.
   for weapon in ['mg','beam','gmiss','iceorb','flame']:
    row=p.evaluate('''weapon=>{eBullets=[];pBullets=[];B._s4war.shield.active=B._s4war.shield.rearming=false;stage4CoreTurretSpawnMissing(B,.5);const d=B._s4war.coreTurrets.find(d=>!d.dead);window.D=d;
    d.active=true;d.spawnT=10;d._sg17={age:10,move:'orbit',moveT:0,nextRaid:999,raid:0,bombs:0,announced:true,phase:'fire',t:0,shot:0,round:0,cycle:2,missile:true,aim:{x:player.x,y:player.y},angle:Math.PI/2};
    sg17Wing(B,d,1/60);window.Q=eBullets.find(q=>q._sg17JetShot&&q._air17Missile);if(!Q)return{missing:true};
    Q.x=player.x;Q.y=VH-160;Q.vx=Q.vy=Q.spd=0;Q._s4Accel=0;pBullets=[{kind:weapon,x:Q.x,y:Q.y,w:60,h:60,vx:0,vy:0,dmg:99,t:0,life:2,top:PLAY.y,bot:VH,pierce:true,_hit:[],_ht:1,r:30}];
    updatePlay(1/60);return{dead:!!Q.dead,alive:eBullets.includes(Q),intercept:enemyOrdnanceCanIntercept(Q),proof:Q._weaponProof,shootable:Q._shootable,ballArt:s4ac13Electric(Q)};}''',weapon)
    ck(diff+' actual helper lightning missile survives '+weapon,not row.get('missing') and row['alive'] and not row['dead'] and row['proof'] and not row['intercept'] and not row['shootable'] and not row['ballArt'],row)
   row=p.evaluate('''()=>{eBullets=[];pBullets=[];window.control=eShootT(player.x,VH-160,Math.PI/2,0,'emissile',{w:20,h:24,silent:true});control.hp=1;control._shootable=true;control._weaponProof=false;control.spd=0;
    pBullets=[{kind:'mg',x:control.x,y:control.y,w:30,h:30,vx:0,vy:0,dmg:9,t:0}];updatePlay(1/60);return{dead:!!control.dead,intercept:enemyOrdnanceCanIntercept(control)};}''')
   ck(diff+' physical missile control is still intercepted by the same gun collision',row['dead'] and row['intercept'],row)
   # Native full-row emitter and native renderer, rather than invented visual fixtures.
   p.evaluate('''()=>{eBullets=[];pBullets=[];p4EmitBalls(B,p4BallLanes(B));for(const q of eBullets)q.t=.28;er26Warm();}''')
   p.wait_for_function('()=>XART.rdy("s4w_lightning_ball_5")')
   p.evaluate('''()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}''');p.screenshot(path=str(O/(diff+'-lightning.png')))
   ck(diff+' native row remains protected',p.evaluate('eBullets.length>=7&&eBullets.every(q=>q._weaponProof&&!enemyOrdnanceCanIntercept(q))'))
  br.close()
finally:stop()
ck('No page, console, draw or asset errors',not errors,errors)
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/('baseline.json' if '--baseline' in sys.argv else 'report.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['passed','failed','errors']}),flush=True);sys.exit(bool(report['failed']))
