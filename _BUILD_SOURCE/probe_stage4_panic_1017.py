"""Native Chromium verification of the Warden spiral and Sovereign final pursuit."""
from pathlib import Path
import ast,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage4_panic_1017/native';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];rows={}
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof P4_17!=="undefined"');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');startRun(4);}")
  p.evaluate('''()=>{window.p4Art={};window.p4Shots=[];window.p4Bombs=[];window.p4Fields=[];const get=XART.get,draw=ctx.drawImage,seen=new WeakMap();
   XART.get=function(k){const im=get.apply(this,arguments);if(im)seen.set(im,k);return im;};
   ctx.drawImage=function(im,...a){const k=seen.get(im);if(k)p4Art[k]=(p4Art[k]||0)+1;return draw.call(this,im,...a);};
   const shot=stage4WarfareShot;stage4WarfareShot=function(){const q=shot.apply(this,arguments);p4Shots.push(q);return q;};
   const bomb=groundTargetingSpawn;groundTargetingSpawn=function(){const q=bomb.apply(this,arguments);p4Bombs.push(q);return q;};
   const fov=combatWarningDraw;combatWarningDraw=function(owner,o){if(owner===window.B)p4Fields.push({...o});return fov.apply(this,arguments);};
   window.p4Markers=0;const reticle=groundTargetReticleDraw;groundTargetReticleDraw=function(){const r=reticle.apply(this,arguments);if(r)p4Markers++;return r;};
   window.p4Pixels=function(fn){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const d=ctx.getImageData(0,0,cv.width,cv.height).data;ctx.restore();return d;};
   window.p4Changed=function(a,b){let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};}''')
  def setup(kind='stormsovereign',diff='hard',stage=4):
   p.evaluate(SETUP,dict(stage=stage,kind=kind,mini=kind=='olivewarden',diff=diff,pilot='cole'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}',polling=50)
   p.evaluate('''()=>{story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;
    VP12.next=CP12.next=EP13.next=99999;TARGET17.nextTank=HM17.next=99999;stagePlan=[];warnT=0;warnKind=null;subBossTriggered=true;aminiTriggered=true;player.invuln=999999;player.dead=player.out=false;run.shield=0;run.speed=0;run.spaceMode=false;powerups=[];
    B._be=null;B._noHit=false;B._phaseInvuln=0;B.enter=false;B.x=worldWidth()/2;B.y=B._drawY=180;B._er26.engaged=false;er26Tick(B,0);
    player.x=worldWidth()/2;player.y=VH-65;camX=clamp(player.x-VW/2,0,worldWidth()-VW);p4Art={};p4Shots=[];p4Bombs=[];p4Fields=[];p4Markers=0;P4_17.events=[];ctx.setTransform(SS,0,0,SS,0,0);SC12.refresh();__bofFit();}''')
  def frames(n,extra=''):
   for i in range(0,n,12):
    p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);'+extra+'drawWorld(1/60);}}',min(12,n-i));p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(name+'.png')))
  for diff,want in [('easy',1),('normal',2),('hard',4),('furious',6),('insanity',6)]:
   setup('olivewarden',diff);frames(420)
   row=p.evaluate('''()=>({live:B._wing17.slots.filter(s=>s.e&&!s.e.dead).length,enter:B._wing17.slots.some(s=>s.e?._wing17.t<WING17_ENTRY),shots:B._er26.shots,keys:Object.keys(p4Art).filter(k=>k.startsWith('air13_'))})''')
   check(diff+' Warden roster reaches live orbit',row['live']==want and not row['enter'] and bool(row['keys']),row)
   p.evaluate('''()=>{window.wingActors=B._wing17.slots.map(s=>s.e);window.wingHP=wingActors.map(e=>e.hp);window.wardenShots=B._er26.shots;window.wingPos=wingActors.map(e=>({x:e.x,y:e.y}));window.wingAngles=wingActors.map(()=>new Set());B._wing17.p4Next=0;}''')
   frames(40,'wingActors.forEach((e,i)=>wingAngles[i].add(e._air13Frame));')
   row=p.evaluate('''()=>({spiral:wingActors.every(e=>e._wing17.phase==='spiral'),moving:wingActors.every((e,i)=>Math.hypot(e.x-wingPos[i].x,e.y-wingPos[i].y)>30),bombs:p4Bombs.filter(q=>q._p4Bomb).length,bombingJets:new Set(p4Bombs.filter(q=>q._p4Bomb).map(q=>q.owner)).size,bombArt:p4Art.lz_bomb||0,reticle:p4Markers,jets:wingActors.map(e=>({hp:e.hp,dead:e.dead,phase:e._wing17.phase}))})''')
   check(diff+' all living jets spiral out together without culling',row['spiral'] and row['moving'] and all(not j['dead'] for j in row['jets']),row)
   check(diff+' every surviving jet drops authored bombs with committed warning markers',row['bombs']>=want and row['bombingJets']==want and row['bombArt']>0 and bool(row['reticle']),row)
   if diff=='furious':snap('warden-six-jet-spiral-bombs')
   p.evaluate('''()=>{window.bombSites=p4Bombs.filter(q=>q._p4Bomb).map(q=>({q,x:q.x,y:q.y}));player.x=camLeftX()+36;player.y=VH-36;}''')
   frames(105,'wingActors.forEach((e,i)=>wingAngles[i].add(e._air13Frame));')
   row=p.evaluate('''()=>({away:wingActors.every(e=>e._wing17.phase==='away'),off:wingActors.every(e=>e.x<camLeftX()-40||e.x>camRightX()+40||e.y<PLAY.y-40||e.y>VH+40),alive:wingActors.every(e=>!e.dead&&enemies.includes(e)),fixed:bombSites.every(s=>!s.q.track&&s.q.x===s.x&&s.q.y===s.y),poses:wingAngles.map(s=>s.size)})''')
   check(diff+' survivors leave the field alive with actual turning frames',row['away'] and row['off'] and row['alive'] and min(row['poses'])>=8,row)
   check(diff+' bomb targets never follow the dodge',row['fixed'],row)
   frames(40)
   row=p.evaluate('''()=>({enter:wingActors.every(e=>e._wing17.phase==='enter'),safe:wingActors.every(e=>e._noHit),same:wingActors.every((e,i)=>B._wing17.slots[i].e===e&&e.hp===wingHP[i]),shots:B._er26.shots-wardenShots})''')
   check(diff+' same actors and HP return through the harmless depth entry',row['enter'] and row['safe'] and row['same'],row)
   check(diff+' Warden continues his independent attacks during the raid',row['shots']>0,row)
   if diff=='furious':
    row=p.evaluate('''()=>{const tick=wing17JetTick,hit=playerHit,save={x:player.x,y:player.y,invuln:player.invuln};let hits=0;
     try{playerHit=()=>hits++;player.invuln=0;eBullets=[];groundTargetingReset();wing17JetTick=function(e,dt){const r=tick.apply(this,arguments);if(e===wingActors[0]){player.x=e.x;player.y=e.y;}return r;};
      for(let i=0;i<6;i++)updatePlay(1/60);return{hits,safe:wingActors[0]._noHit,phase:wingActors[0]._wing17.phase,alive:!player.dead&&!player.out};
     }finally{wing17JetTick=tick;playerHit=hit;Object.assign(player,save);}}''')
    check('Native body collisions do not kill the player during a jet depth return',row['hits']==0 and row['safe'] and row['phase']=='enter' and row['alive'],row)
   if diff=='furious':snap('warden-six-jet-safe-return')
   frames(100)
   check(diff+' returned jets resume orbit and combat contact',p.evaluate('wingActors.every(e=>!e._noHit&&!e._wing17.p4Raid&&e._wing17.t>=WING17_ENTRY)'),p.evaluate('wingActors.map(e=>({phase:e._wing17.phase,t:e._wing17.t}))'))
   if diff=='hard':
    row=p.evaluate('''()=>{const e=wingActors[0];e.flash=0;const a=p4Pixels(()=>drawEnemy(e)),hp=e.hp;_dmgBullet=null;hitEnemy(e,1);const c=p4Pixels(()=>drawEnemy(e));return{pixels:p4Changed(a,c),flash:e.flash,damage:hp-e.hp};}''')
    check('Warden jet real damage changes native pixels',row['pixels']>20 and row['flash']>0 and row['damage']>0,row)
    frames(25);check('Warden jet native hit flash expires',p.evaluate('wingActors[0].flash<=0'))
   if diff=='furious':
    p.evaluate('''()=>{const e=wingActors[0];e.hp=1;hitEnemy(e,99999);if(e._dyingT==null&&!e.dead)hitEnemy(e,99999);window.killedWing=e;B._wing17.p4Next=0;window.deathClock=0;}''')
    frames(2)
    check('Destroyed jet is excluded from the next coordinated raid',p.evaluate('(killedWing.dead||killedWing._dyingT!=null)&&!killedWing._wing17.p4Raid&&P4_17.events.filter(e=>e.event==="wing-spiral").at(-1).jets===5'),p.evaluate('({dead:killedWing.dead,dying:killedWing._dyingT,hp:killedWing.hp,raid:P4_17.events.filter(e=>e.event==="wing-spiral").at(-1)})'))
    frames(270);check('Destroyed jet is not resurrected during return',p.evaluate('killedWing.dead&&B._wing17.slots[0].e===null'))
    frames(70);check('Destroyed slot spawns a distinct replacement after five seconds',p.evaluate('B._wing17.slots[0].e&&B._wing17.slots[0].e!==killedWing&&B._wing17.slots[0].e._noHit'))
  for diff in ['easy','normal','hard','furious']:
   setup(diff=diff)
   row=p.evaluate('''()=>{er26Set(B,'sa14-storm');B._er26.t=B._er26.warm*.7;const lanes=sg17Fan(B);p4Fields=[];er26Draw(B);p4Shots=[];sa14Balls(B,false);return{count:lanes.length,want:7+p4Rank()*2,centre:lanes.some(l=>Math.abs(l.angle-Math.PI/2)<.0001&&Math.abs(l.x-B.x)<.001),match:p4Shots.every((q,i)=>Math.abs(q.x-lanes[i].x)<.01&&Math.abs(q.y-lanes[i].y)<.01&&Math.abs(Math.atan2(q.vy,q.vx)-lanes[i].angle)<.001),proof:p4Shots.every(q=>!enemyOrdnanceCanIntercept(q)&&q._weaponProof&&!q._shootable),fov:p4Fields.filter(q=>q.ey-q.y>500).length};}''')
   check(diff+' forward lightning is a complete row including the centre',row['count']==row['want'] and row['centre'],row)
   check(diff+' full FOV warnings match every unshootable ball',row['match'] and row['proof'] and row['fov']>=row['count'],row)
   p.evaluate('''()=>{eBullets=[];sa14FanWarning(B,.7);}''')
   if diff=='hard':snap('sovereign-full-row-warning')
   row=p.evaluate('''()=>{er26Set(B,'sa14-overflight');B._er26.t=4.8;sa14Overflight(B,1/60);p4Fields=[];mr27Draw(B);return{warnings:B._er26.warnings.length,warm:B._er26._sa14.p4BallWarm,fields:p4Fields.filter(q=>q.fieldOnly&&q.ey-q.y>VH*.7).length};}''')
   check(diff+' regular overflight feeds the native hull renderer real FOV lanes',row['warnings']==7+2*['easy','normal','hard','furious'].index(diff) and row['fields']>=row['warnings'] and row['warm']>=.9,row)
   # Follow the native quarter-HP damage/rearm handoff, not a forced final mode.
   row=p.evaluate('''()=>{B._s4war.shield.active=B._s4war.shield.rearming=false;B._s4war.shieldThresholdIndex=2;B.hp=B.maxhp*.26;B._s4ShieldHit=B._s4CoreHit=null;const core=mr27Shape(B,'core');_lastHitX=core.x;_lastHitY=core.y;_dmgBullet={kind:'mg',x:core.x,y:core.y};hitBoss(B.maxhp*.02);_dmgBullet=null;return{hp:B.hp,max:B.maxhp,phase:B._p4Final?.phase,mode:B._er26.mode};}''')
   check(diff+' actual core damage triggers the final-quarter panic',row.get('phase')=='panic' and row['mode']=='sa14-final' and row['hp']<=row['max']*.2501,row)
   row=p.evaluate('''()=>{const hp=B.hp,d=er26DamageClamp(B,1e9);return{floor:hp-d,min:B.maxhp*.04};}''')
   check(diff+' burst damage cannot cancel the committed ram',abs(row['floor']-row['min'])<.01,row)
   p.evaluate('''()=>{window.panicAim=B._p4Final.aim.x;player.x=camLeftX()+85;window.historyP4=[];}''')
   frames(55)
   if diff=='hard':snap('sovereign-panic-ram-warning')
   frames(round((p.evaluate('p4FinalCfg().tell')+.82+.13)*60)-55,'historyP4.push({phase:B._p4Final?.phase,y:B.y,angle:B._sa14.angle,safe:B._noHit});')
   row=p.evaluate('''()=>({ram:historyP4.filter(q=>q.phase==='ram').length,furthest:Math.max(...historyP4.map(q=>q.y)),releases:P4_17.events.filter(q=>q.event==='final-ram').length,phase:B._p4Final.phase})''')
   check(diff+' panic performs one actual southbound ram',row['ram']>20 and row['furthest']>600 and row['releases']==1,row)
   frames(70,'historyP4.push({phase:B._p4Final?.phase,y:B.y,angle:B._sa14.angle,safe:B._noHit});')
   row=p.evaluate('''()=>({phase:B._p4Final.phase,depth:B._sa14.depth,scale:B._sa14.scale,north:B._sa14.angle===Math.PI,overhead:historyP4.filter(q=>q.phase==='overhead'),noShots:p4Shots.filter(q=>q._p4FinalShot).length===0})''')
   check(diff+' enlarged northbound return stays harmless above the combat plane',row['phase']=='overhead' and row['depth'] and row['north'] and row['scale']>1 and row['noShots'] and all(q['safe'] for q in row['overhead']),row)
   if diff=='hard':snap('sovereign-northbound-overhead-return')
   if diff=='hard':
    row=p.evaluate('''()=>{const tick=er26WarTick,hit=playerHit,save={x:player.x,y:player.y,invuln:player.invuln};let hits=0;
     try{playerHit=()=>hits++;player.invuln=0;eBullets=[];groundTargetingReset();er26WarTick=function(b,dt){const r=tick.apply(this,arguments);if(b===B){player.x=b.x;player.y=b.y;}return r;};
      for(let i=0;i<6;i++)updatePlay(1/60);return{hits,safe:B._noHit,depth:B._sa14.depth,contact:target17BossContact(B,B.x,B.y),alive:!player.dead&&!player.out};
     }finally{er26WarTick=tick;playerHit=hit;Object.assign(player,save);}}''')
    check('Native body collisions ignore the enlarged overhead boss',row['hits']==0 and row['safe'] and row['depth'] and not row['contact'] and row['alive'],row)
   frames(180)
   row=p.evaluate('''()=>({phase:B._p4Final.phase,angle:B._sa14.angle,safe:B._noHit,depth:B._sa14.depth,hp:B.hp,shots:p4Shots.filter(q=>q._p4FinalShot).length,warnings:P4_17.events.filter(q=>q.event==='final-warning').length})''')
   check(diff+' pursuit stays north-facing and releases warned rear lightning',row['phase']=='rear' and abs(row['angle']-3.141592653589793)<.001 and not row['safe'] and not row['depth'] and row['shots']>0 and row['warnings']>0,row)
   row=p.evaluate('''()=>{const core=mr27Shape(B,'core');B.flash=0;B._sa14.glow=0;const a=p4Pixels(()=>mr27Draw(B)),hp=B.hp;B._s4ShieldHit=B._s4CoreHit=null;_lastHitX=core.x;_lastHitY=core.y;_dmgBullet={kind:'mg',x:core.x,y:core.y};hitBoss(B.maxhp*.012);_dmgBullet=null;const c=p4Pixels(()=>mr27Draw(B));return{loss:hp-B.hp,base:B.maxhp*.012,mult:p4FinalCfg().mult,anger:B._p4Final.anger,flash:B.flash,pixels:p4Changed(a,c)};}''')
   check(diff+' exposed hull loses HP quickly and real damage angers it',row['loss']>row['base']*1.7 and row['anger']>0 and row['flash']>0,row)
   check(diff+' actual northbound hull hit changes native pixels',row['pixels']>50,row)
   frames(45)
   row=p.evaluate('''()=>({angerWarnings:P4_17.events.filter(q=>q.event==='final-warning'&&q.kind==='anger').length,early:p4Shots.filter(q=>q._p4Retaliation).length,flash:B.flash,pending:B._p4Final.attacks.filter(q=>q.kind==='anger').length})''')
   check(diff+' retaliation has a real warning window before releasing',row['angerWarnings']>0 and row['early']==0 and row['pending']<=2,row)
   check(diff+' northbound hull flash expires',row['flash']<=0,row)
   if diff=='hard':snap('sovereign-retaliation-fov')
   frames(105)
   row=p.evaluate('''()=>({shots:p4Shots.filter(q=>q._p4Retaliation).length,proof:p4Shots.filter(q=>q._p4FinalShot).every(q=>q._weaponProof&&!q._shootable),hp:B.hp,damage:B._p4Final.damage})''')
   check(diff+' damage retaliation releases authored lightning after its warning',row['shots']>=2 and row['proof'] and row['damage']>0,row)
   frames(1440)
   row=p.evaluate('''()=>({phase:B._p4Final.phase,mode:B._er26.mode,angle:B._sa14.angle,scale:B._sa14.scale,y:B.y,depth:B._sa14.depth,playerAlive:!player.dead&&!player.out,nodes:B._s4war.shield.nodes.filter(n=>!n.dead).length,hp:B.hp,events:P4_17.events.filter(q=>q.event==='final-release')})''')
   check(diff+' after thirty seconds pursuit never resets or turns around',row['phase']=='rear' and row['mode']=='sa14-final' and abs(row['angle']-3.141592653589793)<.001 and row['scale']==1 and not row['depth'] and row['nodes']==0 and row['playerAlive'],row)
   check(diff+' every final lightning release had its own warning',all(q['warned']>=.85 for q in row['events']) and len(row['events'])>10,row)
   if diff=='hard':snap('sovereign-long-northbound-pursuit')
   row=p.evaluate('''()=>{for(let i=0;i<8&&!B.dead;i++){B._s4ShieldHit=B._s4CoreHit=null;const core=mr27Shape(B,'core');_lastHitX=core.x;_lastHitY=core.y;_dmgBullet={kind:'gmiss',x:core.x,y:core.y};hitBoss(1e9);}_dmgBullet=null;const n=p4Shots.length;updatePlay(1/60);return{dead:B.dead,hp:B.hp,more:p4Shots.length-n};}''')
   check(diff+' exposed pursuit finishes through native boss death',row['dead'] and row['hp']<=0 and row['more']==0,row)
   rows[diff+'-pursuit']=row
  setup('cryospear','hard',3)
  row=p.evaluate('''()=>{er26Set(B,'sa14-ice');eBullets=[];sa14Balls(B,true);return{count:eBullets.length,want:7+vp12Tier()*2-2,final:!!B._p4Final};}''')
  check('Stage 3 retains its authored moving ice gap',row['count']==row['want'] and not row['final'],row)
  check('No native page, console, draw or asset errors',not errors,errors[:12]);br.close()
finally:stop()
report=dict(checks=checks,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),errors=errors,rows=rows)
(O/'report.json').write_text(json.dumps(report,indent=2));print(f"{report['passed']} passed / {report['failed']} failed",flush=True)
sys.exit(1 if report['failed'] else 0)
