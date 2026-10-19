"""Native regression for burst protection, elemental aircraft and the sewer intro."""
from pathlib import Path
import ast,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/combat_revision_1017/native';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
errors=[];checks=[];rows={}
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1920,height=1080));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof CR17!=="undefined"');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("()=>{run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');startRun(1);}")
  p.evaluate('''()=>{window.crArt={};const get=XART.get,draw=ctx.drawImage,seen=new WeakMap();
   XART.get=function(k){const im=get.apply(this,arguments);if(im)seen.set(im,k);return im;};
   ctx.drawImage=function(im,...a){const k=seen.get(im);if(k)crArt[k]=(crArt[k]||0)+1;return draw.call(this,im,...a);};
   window.crPixels=function(fn){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const d=ctx.getImageData(0,0,cv.width,cv.height).data;ctx.restore();return d;};
   window.crChanged=function(a,b){let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};
   window.rounds17=[];const emit=air17Emit;air17Emit=function(e){const n=eBullets.length,r=emit.apply(this,arguments);rounds17.push(...eBullets.slice(n));return r;};
   window.guardRounds=[];const warShot=stage4WarfareShot;stage4WarfareShot=function(){const q=warShot.apply(this,arguments);guardRounds.push(q);return q;};}''')
  def setup(stage,kind=None,diff='normal'):
   p.evaluate(SETUP,dict(stage=stage,kind=kind,diff=diff,pilot='cole'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}',polling=50)
   p.evaluate('''()=>{story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;
    VP12.next=CP12.next=EP13.next=99999;TARGET17.nextTank=HM17.next=99999;stagePlan=[];warnT=0;warnKind=null;subBossTriggered=true;aminiTriggered=true;player.invuln=999999;player.dead=player.out=false;run.shield=0;run.speed=0;run.spaceMode=false;l5Rocks=[];l5RockT=99999;crArt={};
    if(window.B){B._be=null;B._noHit=false;B.enter=false;B.x=worldWidth()/2;B.y=180;B._drawY=B.y;if(B._er26){B._er26.engaged=false;er26Tick(B,0);}}
    player.x=worldWidth()/2;player.y=VH-65;camX=clamp(player.x-VW/2,0,worldWidth()-VW);ctx.setTransform(SS,0,0,SS,0,0);SC12.refresh();__bofFit();}''')
  def frames(n):
   for i in range(0,n,12):
    p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(12,n-i));p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}')
   p.screenshot(path=str(O/(name+'.png')))
  # One regular laser trigger contains12 full-damage pulses; all pulses and the
  # passive rack must share the armor budget, including an Akimbo trigger.
  for diff in ['normal','hard','furious']:
   setup(5,'chromehammer',diff)
   row=p.evaluate('''()=>{B._cin30Spoke=B._fb2IntroSeen=true;B._hammer.intro1002=true;B._hammer.balance0922=true;B._hammer.gp4FailsafeSeen=true;B.hp=B.maxhp=6000;B._hammer.mode='hammer';hammerState(B,'hammer');fr27BeginArmor(B);const A=fr27Armor(B);A.activated=true;A.hp=A.max=1800;A.half=true;A.checkpoints=[.75,.5,.35,.15];A._fb2TwirlPreset=true;B._noHit=false;hammerState(B,'hammer');B._hammer.frAct=null;
    const before=A.hp;for(let i=0;i<48;i++){_dmgBullet={kind:i%2?'spaceLaser':'spaceVolley',x:B.x,y:B.y};B._hammerModuleHit=null;hammerBossDamage(B,100);}_dmgBullet=null;
    return{spent:before-A.hp,max:B.maxhp,limited:cr17Guard(B).limited,tokens:cr17Guard(B).tokens};}''')
   check(diff+' all laser pulses and rack missiles share one burst budget',0<row['spent']<=row['max']*.018+.01 and row['limited']>20,row)
   # A nuke can deplete armor but cannot skip the actual attack/recovery.
   row=p.evaluate('''()=>{const h=B._hammer,A=fr27Armor(B);A.hp=0;h.restorationSeen=h._fb2RageDone=true;_dmgBullet={kind:'mg',x:B.x,y:B.y};B._hammerModuleHit=null;const out=hammerBossDamage(B,1e7);B.hp-=out;_dmgBullet=null;return{hp:B.hp,floor:fb2HammerFloor(B),done:fb2HammerRageDone(B)};}''')
   check(diff+' huge damage cannot skip the required Hammer encounter',row['hp']>=row['floor'] and not row['done'],row)
   frames(400)
   check(diff+' merely starting restoration never releases the phase floor',p.evaluate('!fb2HammerRageDone(B)&&!cr17Guard(B).recoveryDone&&!B.dead'),p.evaluate('({state:B._hammer.state,guard:cr17Guard(B)})'))
   p.evaluate('''()=>{fr27Restore(B,.1,false,false);B._hammer.t=1.1;B._noHit=false;eBullets=[];pBullets=[];run.spaceMode=true;run.spaceLevels=[5,5,5];}''')
   for _ in range(6):
    p.evaluate('spaceVolleyLaunchRack(5)');frames(20)
   row=p.evaluate('({status:B._hammer.recovery.status,hits:hc17Counter(B)?.hits,done:cr17Guard(B).recoveryDone})')
   check(diff+' actual passive Volley rack cannot cancel a charge',row['status']=='charging' and row['hits']==0 and not row['done'],row)
   row=p.evaluate('''()=>{const C=hc17Counter(B);for(let i=0;i<C.required;i++){_dmgBullet={kind:'gmiss',x:B.x,y:B.y};B._hammerModuleHit='hammer';hammerBossDamage(B,25);} _dmgBullet=null;return{status:B._hammer.recovery.status,state:B._hammer.state,done:cr17Guard(B).recoveryDone,required:C.required,hits:C.hits};}''')
   check(diff+' deliberate multi-missile counter opens a real punish window',row['status']=='cancelled' and row['done'] and row['state']=='fr_stun' and row['hits']==row['required'],row)
   snap('hammer-'+diff+'-punish')
   frames(120)
   row=p.evaluate('''()=>{B._hammerModuleHit=null;_dmgBullet={kind:'mg',x:B.x,y:B.y};hitBoss(1e7);_dmgBullet=null;return{dead:B.dead,ending:!!H3.ending?.hf17};}''')
   check(diff+' boss can finish normally once attack and counter have played',row['dead'] and row['ending'],row)
  setup(5,'chromehammer')
  p.evaluate('''()=>{B._cin30Spoke=B._fb2IntroSeen=true;B._hammer.intro1002=B._hammer.balance0922=true;B.hp=B.maxhp*.5;B._hammer.mode='hammer';fr27BeginArmor(B);const A=fr27Armor(B);A.activated=true;A.hp=0;A.half=true;A.checkpoints=[.75,.5,.35,.15];B._noHit=false;fr27Restore(B,.1,false,false);window.chargeHp=B.hp;}''')
  frames(660)
  row=p.evaluate('({status:B._hammer.recovery?.status,done:cr17Guard(B).recoveryDone,hp:B.hp,before:chargeHp,dead:B.dead})')
  check('Letting the full charge finish also releases the safeguard without a missile',row['status']=='complete' and row['done'] and row['hp']>row['before'] and not row['dead'],row)
  # Full native draw, both sides of the damaged hull threshold.
  setup(4);p.wait_for_function('()=>!!air13Pose("s4interceptor","heading",Math.PI/2)')
  row=p.evaluate('''()=>{window.jet=spawnEnemy('s4interceptor',worldWidth()/2,200,{});jet.spin=.2;jet._air13Motion={kind:'heading',angle:Math.PI/2};const rows=[];
   for(const ratio of [1,.49,.2]){jet.hp=jet.maxhp*ratio;jet.flash=0;crArt={};crPixels(()=>drawEnemy(jet));rows.push({ratio,keys:Object.keys(crArt)});}return rows;}''')
  check('Camo hull keeps the same authored pose above and below half HP',all(any(k.startswith('air13_s4_s4interceptor_heading') for k in r['keys']) for r in row),row)
  row=p.evaluate('''()=>{jet.hp=jet.maxhp;jet.flash=0;const a=crPixels(()=>drawEnemy(jet)),hp=jet.hp;_lastHitX=jet.x;_lastHitY=jet.y;hitEnemy(jet,1);const b=crPixels(()=>drawEnemy(jet));return{pixels:crChanged(a,b),flash:jet.flash,damage:hp-jet.hp};}''')
  check('Real camo damage still produces visible native hit pixels',row['pixels']>30 and row['flash']>0 and row['damage']>0,row)
  frames(30);check('Camo hit flash expires and returns to its authored palette',p.evaluate('jet.flash<=0'));snap('camo-damage-palette')
  for diff in ['normal','hard','furious']:
   setup(4,'stormsovereign',diff)
   p.evaluate('''()=>{er26Set(B,'recover');B._er26.dur=999;B._s4war.shield.rearming=false;B._s4war.shield.active=false;stage4CoreTurretSpawnMissing(B,.5);window.guardRounds=[];}''')
   frames(30)
   row=p.evaluate('''()=>{const d=B._s4war.coreTurrets[0];return{entry:d._noHit,hit:!!stage4CoreTurretAt(B,d.x,d.y,0),shots:guardRounds.filter(q=>q._sg17JetShot).length};}''')
   check(diff+' lightning guards remain harmless and silent during depth entry',row['entry'] and not row['hit'] and row['shots']==0,row)
   frames(540)
   row=p.evaluate('''()=>({size:B._s4war.coreTurrets.map(d=>d.size),rounds:guardRounds.filter(q=>q._sg17JetShot&&!q._air17Missile).length,missiles:guardRounds.filter(q=>q._sg17JetShot&&q._air17Missile).map(q=>({homing:q.homing,shootable:q._shootable,proof:q._weaponProof,hp:q.hp})),art:crArt.ea11_lightning_missile||0})''')
   rows[diff+'-guards']=row
   check(diff+' smaller lightning guards sustain gun bursts and missile salvos',all(s==116 for s in row['size']) and row['rounds']>=8 and len(row['missiles'])>=2 and row['art']>0,row)
   check(diff+' lightning missiles are shootable and follow committed lanes',bool(row['missiles']) and all(not q['homing'] and q['shootable'] and not q['proof'] for q in row['missiles']),row)
   snap('lightning-guards-'+diff)
   row=p.evaluate('''()=>{const q=guardRounds.find(q=>q._sg17JetShot&&q._air17Missile);q.dead=false;q._intercepted=false;q.x=worldWidth()/2;q.y=350;q.vx=q.vy=0;q._s4Accel=0;q.hp=3;eBullets=[q];pBullets=[{kind:'mg',x:q.x,y:q.y,vx:0,vy:0,w:8,h:18,dmg:50,t:0}];const can=enemyOrdnanceCanIntercept(q);updatePlay(0);return{can,dead:q.dead,hp:q.hp};}''')
   check(diff+' actual machine-gun collision shoots down a lightning missile',row['can'] and row['dead'],row)
   row=p.evaluate('''()=>{const q=guardRounds.find(q=>q._sg17JetShot&&!q._air17Missile);q.dead=false;q.x=worldWidth()/2;q.y=350;q.vx=q.vy=0;eBullets=[q];pBullets=[{kind:'mg',x:q.x,y:q.y,vx:0,vy:0,w:8,h:18,dmg:50,t:0}];updatePlay(0);return{dead:q.dead,proof:q._weaponProof};}''')
   check(diff+' lightning gun rounds retain their bullet interception rules',not row['dead'] and row['proof'],row)
  aircraft=[]
  for stage,typ in [(2,'firejet1002'),(2,'ac10firejet'),(3,'s3interceptor'),(3,'ac10icejet'),(4,'s4rocket'),(4,'s4interceptor')]:
   setup(stage,diff='hard')
   p.evaluate('''type=>{window.jet=spawnEnemy(type,worldWidth()/2,150,{});if(!jet)throw Error('missing aircraft '+type);window.rounds17=[];}''',typ)
   frames(1)
   row=p.evaluate('''()=>{jet.flash=0;const a=crPixels(()=>drawEnemy(jet)),hp=jet.hp;_lastHitX=jet.x;_lastHitY=jet.y;hitEnemy(jet,1);const b=crPixels(()=>drawEnemy(jet));return{pixels:crChanged(a,b),flash:jet.flash,damage:hp-jet.hp};}''')
   check(typ+' real damage changes native sprite pixels',row['pixels']>20 and row['flash']>0 and row['damage']>0,row)
   frames(24);check(typ+' actual damage flash expires',p.evaluate('jet.flash<=0'))
   frames(540)
   row=p.evaluate('''()=>({type:jet.type,attacks:AIR17.events.filter(q=>['burst','missile'].includes(q.event)).length,tells:AIR17.events.filter(q=>q.event==='tell').length,rounds:rounds17.length,missiles:rounds17.filter(q=>q._air17Missile).length,art:Object.keys(crArt).filter(k=>k.startsWith('ea11_')),finite:rounds17.every(q=>Number.isFinite(q.x+q.y+q.vx+q.vy)),dead:jet.dead,cycles:jet._air17?.cycle})''');aircraft.append(dict(stage=stage,**row))
   check(str(stage)+' '+typ+' performs warned attacks with actual projectiles',row['tells']>0 and row['attacks']>0 and row['rounds']>0 and row['finite'],row)
   if stage in [2,3]:check(typ+' alternates elemental gunfire and shootable missiles',row['missiles']>0 and bool(row['art']),row)
   snap('stage'+str(stage)+'-'+typ)
  rows['aircraft']=aircraft
  for stage in [1,4]:
   counts=[]
   for diff in ['normal','hard','furious']:
    setup(stage,diff=diff)
    p.wait_for_function('()=>{const a=VP12_ART[run.stage];return XART.rdy(a.key)}')
    p.evaluate('''()=>{vp12Spawn('orbit');window.rounds17=[];}''');frames(420)
    row=p.evaluate('({shots:rounds17.length,attacks:AIR17.events.filter(q=>q.event==="release").length,tells:AIR17.events.filter(q=>q.event==="tell").length,roles:[...new Set(AIR17.events.filter(q=>q.event==="role").map(q=>q.role))],finite:rounds17.every(q=>Number.isFinite(q.x+q.y+q.vx+q.vy))})');counts.append(row['shots'])
    check('Stage'+str(stage)+' '+diff+' small jets have gunner and missile roles',row['shots']>0 and row['tells']>=row['attacks'] and len(row['roles'])==2 and row['finite'],row)
    snap('formation-stage'+str(stage)+'-'+diff)
   check('Stage'+str(stage)+' formations increase attack pressure Normal to Hard to Furious',counts[0]<counts[1]<counts[2],counts);rows['stage'+str(stage)+'-pressure']=counts
  setup(7)
  row=p.evaluate('''()=>{run.mode='campaign';run._sewerBriefed17=false;setState(GS.LAUNCH);drawLaunch(0);return{state,active:BOFCampaignStory.active,briefed:run._sewerBriefed17,starts:CR17.sewerStarts,beats:BOFCinematicDirector.current.beats.map(b=>b.bg)};}''')
  check('Direct campaign Stage7 entry restores the complete city/river/bridge/sewer approach',row['state']=='cutscene' and row['active'] and row['briefed'] and any('river_bridge' in b for b in row['beats']),row)
  p.wait_for_function('()=>BOFCinematicDirector.current.beats.every(b=>XART.rdy(b.bg))&&XART.rdy("ship_"+_pilotKey())')
  p.evaluate('''()=>{const s=BOFCinematicDirector.current;s.i=2;s.t=1.6;ctx.setTransform(SS,0,0,SS,0,0);BOFCinematicDirector.draw();SC12.refresh();__bofFit();}''');p.screenshot(path=str(O/'stage7-restored-approach.png'))
  check('Approach draws the selected actual aircraft in the native canvas',p.evaluate('(crArt["ship_"+_pilotKey()]||0)>0'))
  for pk in ['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']:
   p.evaluate('pk=>{run.pilot=pk;XART.rdy("ship_"+pk);}',pk);p.wait_for_function('()=>XART.rdy("ship_"+_pilotKey())')
   p.evaluate('BOFCinematicDirector.draw()');check(pk+' sewer approach uses its own actual ship',p.evaluate('(crArt["ship_"+_pilotKey()]||0)>0'))
  p.evaluate('''()=>{for(let i=0;i<6&&BOFCampaignStory.active;i++)BOFCinematicDirector.tick(9);}''')
  check('Approach completes into the actual Stage7 launch',p.evaluate('state===GS.LAUNCH&&!BOFCampaignStory.active'))
  row=p.evaluate('''()=>{const n=CR17.sewerStarts;setState(GS.LAUNCH);drawLaunch(0);return{starts:CR17.sewerStarts,n,state,briefed:run._sewerBriefed17};}''')
  check('Returning to launch does not replay the approach a second time',row['starts']==row['n'] and row['briefed'],row)
  setup(7);p.evaluate("()=>{run.mode='arcade';run._sewerBriefed17=false;setState(GS.LAUNCH);drawLaunch(0);}")
  check('Arcade keeps the native full-field Stage7 connector',p.evaluate('state===GS.LAUNCH&&!BOFCampaignStory.active'))
  br.close()
finally:stop()
check('No page, console, draw or asset errors',not errors,errors)
result=dict(passed=sum(q['passed'] for q in checks),failed=[q for q in checks if not q['passed']],errors=errors,checks=checks,measurements=rows)
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':result['passed'],'failed':len(result['failed']),'errors':errors}),flush=True)
if result['failed'] or errors:sys.exit(1)
