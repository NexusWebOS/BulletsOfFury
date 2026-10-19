"""Native Stage4 visual/combat/audio verification. No campaign-completion claim."""
from pathlib import Path
import ast,json,sys,http.server,hashlib
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/storm_assault_1018/native';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];rows={};http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1600,height=900));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof ST18!=="undefined"');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(35)
  p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(4)")
  p.evaluate('''()=>{window.stShots=[];window.stFovs=[];window.stBombs=[];window.stHistory=[];
   const shot=stage4WarfareShot;stage4WarfareShot=function(){const q=shot.apply(this,arguments);stShots.push(q);return q;};
   const bomb=groundTargetingSpawn;groundTargetingSpawn=function(){const q=bomb.apply(this,arguments);stBombs.push(q);return q;};
   const fov=combatWarningDraw;combatWarningDraw=function(b,q){if(b===window.B)stFovs.push({...q});return fov.apply(this,arguments);};
   window.stPixels=function(fn){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};
   window.stChanged=function(a,b){let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>18)n++;return n;};}''')
  def setup(diff='hard'):
   p.evaluate(SETUP,dict(stage=4,kind='stormsovereign',mini=False,diff=diff,pilot='cole'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(4)&&bmfReady("game")&&bmfReady("dialogue")}',polling=50)
   p.evaluate('''()=>{story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;Input.keys.j=Input.keys.k=Input.keys.y=false;
    VP12.next=CP12.next=EP13.next=HM17.next=TARGET17.nextTank=99999;stagePlan=[];warnT=0;warnKind=null;subBossTriggered=aminiTriggered=true;
    player.invuln=999999;player.dead=player.out=false;run.shield=0;run.speed=0;run.spaceMode=false;powerups=[];
    ST18.events=[];ST18.audio=[];B._be=null;B._noHit=false;B._phaseInvuln=0;B.enter=false;B.x=worldWidth()/2;B.y=B._drawY=180;B._er26.engaged=false;er26Tick(B,0);
    player.x=worldWidth()/2;player.y=VH-65;camX=clamp(player.x-VW/2,0,worldWidth()-VW);
    stShots=[];stFovs=[];stBombs=[];stHistory=[];P4_17.events=[];ctx.setTransform(SS,0,0,SS,0,0);SC12.refresh();__bofFit();}''')
  def frames(n,extra=''):
   for i in range(0,n,12):
    p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);'+extra+'drawWorld(1/60);debugRecFrame();}}',min(12,n-i));p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(name+'.png')))
  setup();frames(2)
  row=p.evaluate('''()=>{const a=B._s4war.shield.nodes.map(n=>n.spin);window.nodeBefore=B._s4war.shield.nodes.map(n=>({x:n.x,y:n.y}));return{said:ST18.events.filter(e=>e.event==='radio'),active:B._s4war.shield.active,spins:a};}''')
  check('Shield engagement explains four generators and multi-Retina',any(e['id']=='generators' and 'MULTI-RETINA' in e['text'] for e in row['said']),row)
  p.evaluate('''()=>{window.casingDraws=[];window.captureCasing=mr27Blit;mr27Blit=function(s,c,q){if(s==='storm'&&c===5)casingDraws.push({...q});return captureCasing.apply(this,arguments);};}''')
  frames(18)
  row=p.evaluate('''()=>{const nodes=B._s4war.shield.nodes,at=casingDraws.slice(-4);const im=stPixels(()=>mr27Draw(B));return{draws:at,pixels:im.filter((v,i)=>i%4!==3&&v>30).length,spins:nodes.map(n=>n.spin)};}''')
  check('All four outer generator plates rotate in the actual renderer',len(row['draws'])==4 and all(abs(q.get('rot',0))>.01 for q in row['draws']),row)
  snap('shield-generators-radio')
  row=p.evaluate('''()=>{const nodes=retinaBossTargets(B).filter(t=>t.kind==='electrical node');retinaScanClear();for(const t of nodes.slice(0,4))retinaScanAdd(t);return{nodes:nodes.length,marks:retinaScanState().marks.length,cap:RETINA_SCAN_CAP};}''')
  frames(35)
  row.update(p.evaluate('''()=>({locked:retinaScanState().marks.filter(m=>m.phase==='locked').length,alive:retinaScanState().marks.every(m=>retinaTargetValid(m.target))})'''))
  check('Real multi-Retina acquires all four spinning generator targets',row['nodes']==4 and row['marks']==4 and row['locked']==4 and row['alive'],row)
  snap('multi-retina-four-generators')
  row=p.evaluate('''()=>{run.bombs=12;const n=pBullets.length;retinaScanFire();for(let i=0;i<60;i++)retinaScanTick(1/60);return{used:12-run.bombs,missiles:pBullets.slice(n).filter(q=>q.kind==='gmiss'||q.target).length};}''')
  check('Multi-Retina launches actual missile salvo at the generators',row['used']>=4 and row['missiles']>=4,row)
  # A helper deployment preserves actors and HP; all entry shots remain disabled.
  for diff in ['normal','hard','furious']:
   setup(diff);p.evaluate('''()=>{B._s4war.shield.active=B._s4war.shield.rearming=false;B.hp=B.maxhp*.48;B._s4war.shieldThresholdIndex=2;stage4CoreTurretSpawnMissing(B,.5);er26Set(B,'sa14-mg');window.stWing=B._s4war.coreTurrets.slice();window.stWingHp=stWing.map(d=>d.hp);window.stTrack=[];}''')
   frames(87,'stTrack.push(stWing.map(d=>({x:d.x,y:d.y,scale:d._sg17Scale,safe:d._noHit,mat:d.materialize,move:d._sg17.move,phase:d._sg17.phase})));')
   row=p.evaluate('''()=>({rows:stTrack,shots:stShots.filter(q=>q._sg17JetShot).length,targets:retinaBossTargets(B).filter(q=>(q.part||q._part)?._sg17).length,said:ST18.events.filter(q=>q.event==='radio')})''')
   check(diff+' helpers visibly enter from south scaled above the combat plane',all(q['y']>500 and q['scale']>2 for q in row['rows'][0]) and all(q['safe'] and q['mat']==0 for frame in row['rows'] for q in frame),{'first':row['rows'][0],'last':row['rows'][-1]})
   check(diff+' south entry has no gun shots or Retina targets',row['shots']==0 and row['targets']==0,row['shots'])
   check(diff+' radio detects the incoming lightning wing',any(q['id'].startswith('helpers-') for q in row['said']))
   if diff=='hard':snap('south-entry-harmless-depth')
   frames(140)
   row=p.evaluate('''()=>({on:stWing.every(d=>!d._noHit&&d.materialize===1),same:stWing.every((d,i)=>d===B._s4war.coreTurrets[i]&&d.hp===stWingHp[i]),targets:retinaBossTargets(B).filter(q=>(q.part||q._part)?._sg17).length,moves:stWing.map(d=>d._sg17.move)})''')
   check(diff+' same helpers become shootable after landing on the combat plane',row['on'] and row['same'] and row['targets']>=2,row)
   frames(1080,'stTrack.push(stWing.map(d=>({x:d.x,y:d.y,move:d._sg17.move})));')
   row=p.evaluate('''()=>({shots:stShots.filter(q=>q._sg17JetShot).length,missiles:stShots.filter(q=>q._sg17JetShot&&q._air17Missile).length,bullets:stShots.filter(q=>q._sg17JetShot&&!q._air17Missile).length,bombs:stBombs.filter(q=>q._st18Bomb).map(q=>({x:q.x,y:q.y,track:q.track,warn:q.warn,from:q._jetBomb})),cross:ST18.events.filter(q=>q.event==='helper-cross'),orbit:ST18.events.filter(q=>q.event==='helper-orbit'),draws:{...ST18.draws},same:stWing.every((d,i)=>d===B._s4war.coreTurrets[i]&&d.hp===stWingHp[i])})''')
   check(diff+' helpers orbit, scatter, cross and rejoin without respawning',len(row['cross'])>=2 and len(row['orbit'])>=2 and row['same'],row)
   check(diff+' wing independently fires lightning bullets and counterable missiles',row['bullets']>=12 and row['missiles']>=4,row['shots'])
   if diff=='hard':
    continuity=p.evaluate('''()=>{const oldDepth=B._sa14.depth,oldRearm=B._s4war.shield.rearming,n=stShots.length;try{B._sa14.depth=true;B._s4war.shield.rearming=true;for(const d of stWing){d._sg17.phase='fire';d._sg17.t=0;d._sg17.shot=0;d._sg17.round=0;d._sg17.angle=Math.PI/2;}sa14CoreTick(B,1/60);return{shots:stShots.length-n};}finally{B._sa14.depth=oldDepth;B._s4war.shield.rearming=oldRearm;}}''')
    check('On-plane helpers keep firing during the hull overhead/rearm state',continuity['shots']>=2,continuity)
   check(diff+' crossing wing drops fixed lightning bombs with a full warning',len(row['bombs'])>=4 and all(not q['track'] and q['warn']>=1.3 for q in row['bombs']) and row['draws']['bomb']>0 and row['draws']['impact']>0,row['bombs'])
   if diff=='hard':
    row=p.evaluate('''()=>{const d=stWing[0],g=mr27HelperState(d);d.flash=g.flash=0;const a=stPixels(()=>mr27HelperDraw(B,d)),hp=d.hp;B._s4CoreHit=d;_lastHitX=d.x;_lastHitY=d.y;_dmgBullet={kind:'mg',x:d.x,y:d.y};hitBoss(1);_dmgBullet=null;const c=stPixels(()=>mr27HelperDraw(B,d));return{pixels:stChanged(a,c),flash:d.flash,gunFlash:g.flash,hp:hp-d.hp,deflect:d.deflectFlash};}''')
    check('Updated helper hit/deflect feedback changes actual authored pixels',row['pixels']>30 and max(row['flash'],row['gunFlash'],row['deflect'])>0,row)
    frames(30);check('Helper flash expires',p.evaluate('stWing[0].flash<=0&&mr27HelperState(stWing[0]).flash<=0'))
    p.evaluate('''()=>{const d=stWing[0];d._sg17.move='cross';d._sg17.moveT=.65;d._sg17.from={x:camLeftX()+60,y:PLAY.y+110};d._sg17.to={x:camRightX()-60,y:VH-160};d._sg17.bombs=0;}''');frames(5);snap('lightning-crossing-bomb-retinas');frames(92);snap('lightning-bomb-impact')
   rows[diff+'-wing']=row
  # Check committed bomb geometry with a real ground-target damage clock.
  setup();p.evaluate('''()=>{B._s4war.shield.active=B._s4war.shield.rearming=false;window.testBomb=st18Bomb(B,{x:camLeftX()+80,y:PLAY.y+160,side:-1},0);window.bombX=testBomb.x;window.bombY=testBomb.y;player.x=camRightX()-40;player.y=VH-40;}''');frames(45)
  row=p.evaluate('''()=>({fixed:testBomb.x===bombX&&testBomb.y===bombY,impact:testBomb.impact,t:testBomb.t,warn:testBomb.warn})''');check('Lightning bomb site stays fixed after the pilot dodges',row['fixed'] and not row['impact'],row)
  row=p.evaluate('''()=>{const saved=playerHit;let hits=0;try{playerHit=()=>hits++;player.x=testBomb.x;player.y=testBomb.y;testBomb.t=testBomb.warn-.05;groundTargetingTick(.025);const before=hits;groundTargetingTick(.13);return{before,hits,impact:testBomb.impact};}finally{playerHit=saved;}}''')
  check('Lightning bomb cannot hurt before its warning ends and hits at impact',row['before']==0 and row['hits']==1 and row['impact'],row)
  p.evaluate('''()=>{testBomb.t=testBomb.warn+.24;testBomb.impact=true;}''');snap('generated-lightning-impact')
  for diff in ['normal','hard','furious']:
   setup(diff)
   p.evaluate('''()=>{B._s4war.shield.active=B._s4war.shield.rearming=false;B._s4war.shieldThresholdIndex=2;B.hp=B.maxhp*.26;const q=mr27Shape(B,'core');B._s4ShieldHit=B._s4CoreHit=null;_lastHitX=q.x;_lastHitY=q.y;_dmgBullet={kind:'mg',x:q.x,y:q.y};hitBoss(B.maxhp*.02);_dmgBullet=null;}''')
   frames(50,'stHistory.push({phase:B._p4Final?.phase,glow:B._sa14.glow,y:B.y,scale:B._sa14.scale,safe:B._noHit,road:B._p4Final?.roadSpeed});')
   row=p.evaluate('''()=>({phase:B._p4Final.phase,glow:B._sa14.glow,shake,road:B._p4Final.roadSpeed,radio:B._st18.radio,draws:ST18.draws.glow})''')
   check(diff+' quarter-HP handoff lights the whole hull and announces the ram',row['phase']=='panic' and row['glow']>.7 and row['shake']>2 and row['road']>600 and row['radio']['id']=='overload' and row['draws']>0,row)
   if diff=='hard':snap('overload-whole-hull-lightning')
   frames(round((p.evaluate('p4FinalCfg().tell')+.82+.15)*60)-50,'stHistory.push({phase:B._p4Final?.phase,glow:B._sa14.glow,y:B.y,scale:B._sa14.scale,safe:B._noHit,road:B._p4Final?.roadSpeed});')
   row=p.evaluate('''()=>({ram:stHistory.filter(q=>q.phase==='ram'),maxY:Math.max(...stHistory.map(q=>q.y)),speed:Math.max(...stHistory.map(q=>q.road||0)),hp:B.hp,unchanged:B._p4Final.attacks.length})''')
   check(diff+' committed south ram visibly accelerates the road',len(row['ram'])>35 and row['maxY']>700 and row['speed']>1000,{'ramFrames':len(row['ram']),'maxY':row['maxY'],'speed':row['speed']})
   frames(43,'stHistory.push({phase:B._p4Final?.phase,scale:B._sa14.scale,safe:B._noHit});')
   row=p.evaluate('''()=>({phase:B._p4Final.phase,depth:B._sa14.depth,scale:B._sa14.scale,safe:B._noHit,contact:target17BossContact(B,B.x,B.y),north:B._sa14.angle===Math.PI})''')
   check(diff+' enlarged return flies overhead northward without body damage',row['phase']=='overhead' and row['depth'] and row['safe'] and row['scale']>1.5 and not row['contact'] and row['north'],row)
   if diff=='hard':snap('overhead-return-scaled')
   frames(220)
   row=p.evaluate('''()=>({phase:B._p4Final.phase,speed:B._p4Final.roadSpeed,north:B._sa14.angle===Math.PI,shots:stShots.filter(q=>q._p4FinalShot).length,proof:stShots.filter(q=>q._p4FinalShot).every(q=>q._weaponProof&&!q._shootable),warnings:P4_17.events.filter(q=>q.event==='final-warning').length,said:ST18.events.filter(q=>q.event==='radio'),audio:ST18.audio.map(q=>q.key)})''')
   check(diff+' chase remains fast, north-facing, with warned unshootable lightning',row['phase']=='rear' and row['speed']>950 and row['north'] and row['shots']>=7 and row['proof'] and row['warnings']>=2,row)
   check(diff+' lightning, rev and attack cues cover the whole transition',all(k in row['audio'] for k in ['geyserLightning','chargeDash','bossCannon','enemyLightningChaingun']),row['audio'])
   if diff=='hard':snap('northbound-chase-radio-fov')
   rows[diff+'-phase']=row
  # Speaker routing is actual seat state, including both co-op orderings.
  row=p.evaluate('''()=>{const old={pilot:run.pilot,pilot2:run2.pilot,coop:coopOn};try{coopOn=false;run.pilot='cole';const cole=st18Speaker();run.pilot='decker';const decker=st18Speaker();coopOn=true;run2.pilot='cole';const both=st18Speaker();run.pilot='cole';run2.pilot='decker';const reverse=st18Speaker();return{cole,decker,both,reverse};}finally{run.pilot=old.pilot;run2.pilot=old.pilot2;coopOn=old.coop;}}''')
  check('Decker or Cole briefs the pilot; Axel briefs their co-op pair',row==dict(cole='decker',decker='cole',both='axel',reverse='axel'),row)
  # Ask actual media elements to play, then yield for decoding: not a cue-count
  # substitute for verifying the approved MP3s were loaded and could start.
  p.evaluate('''()=>{for(const k of ['geyserLightning','enemyLightningChaingun','chargeDash','missileLaunch','bombDrop','element_lightning_hit'])Snd.play(k);const v=BOF_CHIP_PASS.sound(B._sa14.engine,'gd_tankEngineLoop',{loop:true,gain:3.8});}''');p.wait_for_timeout(1000)
  row=p.evaluate('''()=>({loaded:['geyserLightning','enemyLightningChaingun','chargeDash','missileLaunch','bombDrop','element_lightning_hit'].map(k=>({key:k,slots:Snd.pools[k].slots.filter(Boolean).map(v=>({ready:v.el.readyState,duration:v.el.duration,used:v.used,paused:v.el.paused}))})),owned:[...BOF_CHIP_PASS.owned.values()].filter(v=>v.key==='gd_tankEngineLoop').map(v=>({ready:v.el.readyState,started:v.started,paused:v.el.paused,volume:v.el.volume,rate:v.el.playbackRate})),failures:BOF_CHIP_PASS.failures})''')
  check('Approved lightning/attack MP3 voices decode in native Chromium',all(any(v['ready']>=2 and v['duration']>0 for v in q['slots']) for q in row['loaded']) and not row['failures'],row)
  check('Revving loop actually starts and has audible mix gain',bool(row['owned']) and any(v['started'] and not v['paused'] and v['volume']>0 for v in row['owned']),row['owned'])
  p.evaluate('''()=>{B.dead=true;updatePlay(1/60);}''')
  check('Boss death stops its owned engine loop and clears comms',p.evaluate('!BOF_CHIP_PASS.owned.has(B._sa14.engine)&&!B._st18.radio'))
  check('No native page, console, draw or asset errors',not errors,errors[:20]);br.close()
finally:stop()
report=dict(checks=checks,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),errors=errors,rows=rows,sourceSha256=hashlib.sha256((R/'assets/storm_assault_1018.js').read_bytes()).hexdigest())
(O/'report.json').write_text(json.dumps(report,indent=2));print(f"{report['passed']} passed / {report['failed']} failed",flush=True)
sys.exit(1 if report['failed'] else 0)
