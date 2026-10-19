"""Native Chromium: Fortress reactor, enlarged modular carrier and live allies."""
from pathlib import Path
import ast,json,sys,http.server,hashlib
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/harrier_wing_1018/native';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];rows={};http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=900));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof S6R18!=="undefined"');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(35)
  p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(6)")
  p.evaluate('''()=>{window.s6Pixels=fn=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const a=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return a;};
   window.s6Changed=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};
   window.s6Art=[];const art=weaponFeedbackArt;weaponFeedbackArt=function(key,x,y){const r=art.apply(this,arguments);if(r)s6Art.push({key,x,y});return r;};
   window.s6Jets=[];const launch=whvLaunchJet;whvLaunchJet=function(b){const n=b._whv.jets.length,r=launch.apply(this,arguments);if(b._whv.jets.length>n)s6Jets.push(b._whv.jets.at(-1));return r;};
   window.s6HiveShots=[];window.s6HiveOwner=null;const hive=hivewingTick,shot=eShootT;
   hivewingTick=function(e){const old=s6HiveOwner;s6HiveOwner=e;try{return hive.apply(this,arguments);}finally{s6HiveOwner=old;}};
   eShootT=function(){const q=shot.apply(this,arguments);if(s6HiveOwner)s6HiveShots.push({owner:s6HiveOwner,kind:q.kind});return q;};}''')
  p.evaluate('''()=>{window.s6AllyDamage=[];const damage=warhiveDamage;warhiveDamage=function(b){const shot=_dmgBullet,hp=b.hp,out=damage.apply(this,arguments);if((shot?.ally||shot?._wingKey)&&hp>b.hp)s6AllyDamage.push({pilot:shot._wingKey,mini:!!b._cargo17Mini,damage:hp-b.hp});return out;};}''')
  def frames(n,extra=''):
   for i in range(0,n,12):
    p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);'+extra+'drawWorld(1/60);debugRecFrame();}}',min(12,n-i));p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(name+'.png')))
  def setup(mini=True,diff='normal'):
   p.evaluate(SETUP,dict(stage=6,kind='siegefortress17' if mini else 'warhive',mini=mini,diff=diff,pilot='cole'))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&bmfReady("game")&&bmfReady("dialogue")}',polling=50)
   p.evaluate('''()=>{s6Opening=null;story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;stagePlan=[];warnT=0;warnKind=null;
    VP12.next=CP12.next=EP13.next=SEWER17.next=999999;B._be=null;B.enter=false;B._phaseInvuln=0;player.x=worldWidth()/2;player.y=VH-65;player.invuln=0;playerHit=()=>{};run.shield=0;run.spaceMode=false;
    s6WingInit();s6Wing.beats=99;s6Wing.all=true;s6Wing.fakeDone=true;s6Wing.route='left';subBossTriggered=aminiTriggered=true;
    for(const k of ['j','k','y','a','d','w','s'])Input.keys[k]=false;S6R18.events=[];s6Art=[];s6Jets=[];s6HiveShots=[];__bofFit();}''')
   frames(210)
  def mg(frames_count,which):
   p.evaluate('''()=>{window.mgPreviousSpecial={sonic:run.sonicT,dk:run.dkT};run.sonicT=run.dkT=0;special=thunderStorm=null;weaponFormSelect(7,{kind:'primary1003b',id:'mg'});chaingunUnlocked=false;run._earnedUnlocks={...(run._earnedUnlocks||{}),chaingun:false};run.weapon=0;run.wvars[0]=null;run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[0];run.wlevels[0]=run.wlevel=0;powerups=[];player.fireCd=0;Input.keys.j=true;player._mgMuzT=0;retinaScanClear();retina.target=null;retina.phase=null;}''')
   # Isolate module routing from the carrier's separately verified escort
   # squadron: an elite jet in the stream can legitimately absorb these rounds.
   frames(frames_count,'powerups=[];enemies=[];'+which);p.evaluate('Input.keys.j=false')
  for diff in ['normal','hard','furious']:
   setup(True,diff)
   row=p.evaluate('''()=>({kind:B.kind,gunCount:B._cargo13.guns.length,line:s6Wing.line,t:s6Wing.line?.t,held:!!S6Q13.held,radio:S6R18.draws.radio,paused:!!story,mode:B._cargo13.mode})''')
   check(diff+' miniboss combat captions draw and age without parking the wing',not row['held'] and row['t']>.5 and row['radio']>0 and not row['paused'] and 'SIX' in row['line']['full'],row)
   if diff=='normal':snap('mini-live-dialogue')
   p.evaluate('window.targetGun=B._cargo13.guns[0];window.gunHP=targetGun.hp')
   mg(65,"{const m=sc13Mount(B,targetGun.id);player.x=m.x;player.y=m.y+155;}")
   check(diff+' actual J machine gun damages a miniboss battery',p.evaluate('targetGun.hp<gunHP'),p.evaluate('({hp:targetGun.hp,before:gunHP})'))
   row=p.evaluate('''()=>{const g=B._cargo13.guns[1],m=sc13Mount(B,g.id);g.fl=g.flash=0;const a=s6Pixels(()=>warhiveDraw(B)),hp=g.hp;
    B._cargo13.directId=g.id;_dmgBullet={kind:'mg',x:m.x,y:m.y};hitSubBoss(1);_dmgBullet=null;const c=s6Pixels(()=>warhiveDraw(B));return{pixels:s6Changed(a,c),flash:g.flash,fl:g.fl,damage:hp-g.hp};}''')
   check(diff+' battery damage visibly flashes native pixels through markHit',row['pixels']>10 and row['flash']>0 and row['damage']>0,row)
   frames(25);check(diff+' battery flash expires normally',p.evaluate('B._cargo13.guns[1].flash<=0&&B._cargo13.guns[1].fl<=0'))
   row=p.evaluate('''()=>{const C=B._cargo13,core=C.core;for(const g of C.guns.slice(0,5)){C.directId=g.id;hitSubBoss(1e6);}C.directId='core';hitSubBoss(1e6);return{core:C.core,expected:core,closed:!sc13Open(B),targets:retinaBossTargets(B).map(t=>t.kind)};}''')
   check(diff+' reactor remains protected with one of six batteries alive',row['closed'] and row['core']==row['expected'] and 'reactor' not in row['targets'],row)
   p.evaluate('''()=>{B._cargo13.directId=5;hitSubBoss(1e6);window.coreBefore=B._cargo13.core;}''');frames(24)
   row=p.evaluate('''()=>{B._cargo13.directId='core';hitSubBoss(1e6);return{open:B._s6r18.open,protected:B._cargo13.core===coreBefore,retina:retinaBossTargets(B).map(t=>t.kind)};}''')
   check(diff+' reactor hatch visibly opens before it accepts core damage',0<row['open']<1 and row['protected'] and 'reactor' not in row['retina'],row)
   if diff=='normal':snap('mini-hatch-opening')
   frames(38)
   row=p.evaluate('''()=>({open:sc13Open(B),progress:B._s6r18.open,targets:retinaBossTargets(B).map(t=>t.kind),line:s6Wing.line,draws:{...S6R18.draws},core:sc13Core(B)})''')
   check(diff+' full opening exposes an animated energy core and Retina target',row['open'] and 'reactor' in row['targets'] and row['draws']['reactor']>0 and 'EXPOSED' in row['line']['full'],row)
   if diff=='normal':snap('mini-energy-core-exposed')
   p.evaluate('window.coreHP=B._cargo13.core');mg(60,"{const m=sc13Core(B);player.x=m.x;player.y=m.y+160;}")
   check(diff+' actual J machine gun damages the exposed energy core',p.evaluate('B._cargo13.core<coreHP'),p.evaluate('({hp:B._cargo13.core,before:coreHP})'))
   row=p.evaluate('''()=>{const t=retinaBossTargets(B).find(q=>q.kind==='reactor'),hp=B._cargo13.core;const hit=retinaMissileDamage(t,3,{kind:'gmiss',x:t.x,y:t.y});return{hit,damage:hp-B._cargo13.core};}''')
   check(diff+' normal Retina missile damage reaches the miniboss core',row['hit'] and row['damage']>0,row)
   p.evaluate('''()=>{B._cargo13.directId='core';hitSubBoss(1e6);}''');frames(185)
   check(diff+' miniboss defeat advances the stage without awarding boss clear',p.evaluate('subBossDone&&!subBossActive&&!bossDefeated&&!subBoss'))
  for diff in ['normal','hard','furious']:
   setup(False,diff);frames(180)
   row=p.evaluate('''()=>{const b=B,C=b._carrier17,targets=retinaBossTargets(b);return{scale:C.hullScale,width:b.w,height:b.h,view:viewW(),zoom:viewZoom(),parts:C.parts.length,pool:b.hp,expected:C.parts.reduce((n,p)=>n+p.hp,0),core:'reactor' in C,targets:targets.map(t=>t.kind),aligned:C.parts.every(p=>{const m=roster17Mount(b,p),t=targets.find(t=>t.name==='harrier '+p.id||t._retinaId?.endsWith(p.id));return roster17At(b,m.x,m.y)===p.id&&targets.some(t=>Math.abs(t.x-m.x)<.01&&Math.abs(t.y-m.y)<.01&&Math.abs(t.w-p.w*C.hullScale)<.01);})};}''')
   check(diff+' carrier is 45 percent larger with a module-only health budget and unchanged FOV',row['scale']==1.45 and row['width']>660 and row['height']>370 and row['view']==480 and row['zoom']==1 and row['pool']==row['expected'] and not row['core'] and 'reactor' not in row['targets'],row)
   check(diff+' all eight enlarged modules share hit and Retina geometry',row['aligned'] and row['parts']==8,row)
   row=p.evaluate('''()=>({phase:B._carrier17.phase,bay:B._s6r18.bay,open:B._whv.doorOpen,jets:s6Jets.length,live:s6Jets.filter(e=>!e.dead).length,art:s6Jets.map(e=>e.type),events:S6R18.events.filter(q=>q.event==='jet-launch')})''')
   check(diff+' physical bay opens and launches real elite fighter actors',row['jets']>=4 and all(q=='xelite_hivewing' for q in row['art']) and len(row['events'])>=4,row)
   if diff=='normal':snap('harrier-bay-launched-jets')
   p.evaluate('window.bayPoses=new Set();window.flightPhases=new Set();window.jetAttackStart=s6Jets.map(e=>e._eb11?.attacks||0)')
   frames(1200,"bayPoses.add(Math.round(B._s6r18.bay.open*10));flightPhases.add(B._carrier17.phase);")
   row=p.evaluate('''()=>({poses:[...bayPoses],phases:[...flightPhases],cap:B._whv.jetN,alive:whvJetsAlive(B._whv),jets:s6Jets.length,shots:s6HiveShots.length,moving:s6Jets.some(e=>Math.abs(e.x-B.x)>70||e.y>B.y+80)})''')
   check(diff+' bay closes and carrier retains its south departure and scaled return',len(row['poses'])>=5 and 'leave' in row['phases'] and 'flyover' in row['phases'],row)
   check(diff+' deployed fighter actors move and remain bounded by the wing cap',row['moving'] and row['alive']<=row['cap'],row)
   check(diff+' launched elite fighters independently fire native attacks',row['shots']>=4,row['shots'])
   frames(180)
   # Return to a stable fight for the component geometry and damage checks.
   p.evaluate('''()=>{const C=B._carrier17;C.phase='fight';C.depth=false;C.scale=1;C.t=0;C.flight=999;B._noHit=false;B.x=worldWidth()/2;B.y=roster17Home(B);roster17Sync(B);window.fanL=C.parts.find(q=>q.id==='L');window.fanR=C.parts.find(q=>q.id==='R');}''')
   row=p.evaluate('''()=>{const C=B._carrier17,p=fanL,m=roster17Mount(B,p);p.flash=p.fl=0;const a=s6Pixels(()=>warhiveDraw(B)),hp=p.hp;C.direct=p.id;_dmgBullet={kind:'mg',x:m.x,y:m.y};hitBoss(1);_dmgBullet=null;const c=s6Pixels(()=>warhiveDraw(B));return{pixels:s6Changed(a,c),flash:p.flash,damage:hp-p.hp};}''')
   check(diff+' intact fan visibly flashes on actual damage',row['pixels']>20 and row['flash']>0 and row['damage']>0,row)
   p.evaluate('''()=>{B._carrier17.phase='leave';B._carrier17.t=0;}''');frames(25)
   check(diff+' real part hit flash expires during the south departure',p.evaluate('fanL.flash<=0&&fanL.fl<=0'))
   p.evaluate('''()=>{const C=B._carrier17;C.phase='fight';C.depth=false;C.scale=1;C.t=0;C.flight=999;B._noHit=false;B.y=roster17Home(B);roster17Sync(B);}''')
   p.evaluate('''()=>{B._carrier17.direct='L';warhiveDamage(B,1e6);window.fanHP=fanR.hp;window.driftSamples=[];}''');frames(75,"driftSamples.push({x:B._s6r18.drift.x,v:B._s6r18.drift.v,xNow:B.x,base:camLeftX()+viewW()/2+Math.sin(B._carrier17.age*.36)*8});")
   row=p.evaluate('''()=>({dead:fanL.dead,other:fanR.hp===fanHP,smoke:S6R18.draws.smoke,burst:S6R18.draws.burst,drift:Math.max(...driftSamples.map(q=>Math.abs(q.xNow-q.base))),velocity:Math.max(...driftSamples.map(q=>Math.abs(q.v)))})''')
   check(diff+' broken fan smokes, repeatedly explodes and causes bounded momentum',row['dead'] and row['other'] and row['smoke']>0 and row['burst']>0 and 1<row['drift']<15 and row['velocity']>1,row)
   if diff=='normal':snap('harrier-fan-anchored-smoke-bursts')
   row=p.evaluate('''()=>{const b=B,C=b._carrier17,W=b._whv;function fx(){s6Art=[];s6r18FanDraw(b,C);return s6Art.filter(q=>/^nsd_chim_|^nxp_upward_/.test(q.key));}const a=fx();b.x+=64;b.y+=27;roster17Sync(b);const c=fx();const result={count:a.length,attached:a.every((q,i)=>c[i]&&Math.abs(c[i].x-q.x-64)<.01&&Math.abs(c[i].y-q.y-27)<.01)};b.x-=64;b.y-=27;roster17Sync(b);return result;}''')
   check(diff+' fire and smoke follow the actual fan after hull translation',row['count']>=4 and row['attached'],row)
   row=p.evaluate('''()=>{const C=B._carrier17;for(const p of C.parts.filter(p=>p.kind==='laser')){C.direct=p.id;warhiveDamage(B,1e6);}return{parts:C.parts.filter(p=>!p.dead).map(p=>p.id),targets:retinaBossTargets(B).map(t=>t.kind),opening:B._s6r18.opening,core:'reactor' in C};}''')
   check(diff+' destroying the lasers leaves only real fan and rack targets, no core',not row['core'] and not row['opening'] and 'reactor' not in row['targets'] and len(row['parts'])==3,row)
   p.evaluate('''()=>{const C=B._carrier17;for(const p of C.parts.filter(p=>!p.dead&&p.id!=='rackR')){C.direct=p.id;warhiveDamage(B,1e6);}window.lastPart=C.parts.find(p=>!p.dead);window.lastHP=lastPart.hp;enemies=[];B._whv.jets=[];powerups=[];window.coreDraws=S6R18.draws.reactor;}''')
   mg(65,"{const m=roster17Mount(B,lastPart);player.x=m.x;player.y=m.y+155;}")
   row=p.evaluate('''()=>({damage:lastHP-lastPart.hp,alive:!!B._carrier17&&lastPart.hp>0,pool:B.hp,expected:lastPart.hp,weapon:run.weapon,previousSpecial:mgPreviousSpecial})''')
   check(diff+' actual J machine gun damages the last enlarged module without an extra core pool',row['weapon']==0 and row['damage']>0 and row['alive'] and row['pool']==row['expected'],row)
   row=p.evaluate('''()=>{B._carrier17.direct=lastPart.id;warhiveDamage(B,1e6);return{same:B===boss,dead:B.dead,stageClear:bossDefeated,fall:!!B._s6CarrierFall,mode:B._whv.mode,hp:B.hp,coreDraws:S6R18.draws.reactor-coreDraws,opening:B._s6r18.opening};}''')
   check(diff+' final module immediately starts carrier breakup without a core or early stage clear',row['same'] and not row['dead'] and not row['stageClear'] and row['fall'] and row['mode']=='death' and row['hp']>0 and not row['opening'] and row['coreDraws']==0,row)
   if diff=='normal':snap('carrier-breakup-no-core')
   frames(147)
   check(diff+' destroyed-module hit flashes also expire during carrier breakup',p.evaluate('B._s6CarrierFall.parts.every(p=>p.flash<=0&&p.fl<=0)'))
   row=p.evaluate('''()=>{const A=B._whv.ace,W=B._whv,u=clamp(A.t/.7,0,1),k=lerp(.48,1,u*u*(3-2*u));return{age:A.t,width:184*k,bay:WHV_DOOR.w*WHV_S*roster17HullScale(B),x:A.x,expectedX:whvPartPos(B,'door').x};}''')
   check(diff+' blue jet begins within the enlarged hangar before approaching the combat plane',row['age']<.15 and row['width']<=row['bay'] and row['x']==row['expectedX'],row)
   if diff=='normal':snap('blue-jet-emerging-from-bay')
   frames(23);row=p.evaluate('''()=>({ace:!!B._whv.ace,name:B.name,stageClear:bossDefeated,mode:B._whv.mode,hp:B.hp,max:B.maxhp,size:[B.w,B.h],pool:B._whv.aceMax,dead:B.dead})''')
   check(diff+' original giant blue Nightwing emerges from the falling carrier',row['ace'] and row['name']=='NIGHTWING ACE' and not row['stageClear'] and row['hp']==row['max'] and row['size'][0]>=140 and not row['dead'],row)
   if diff=='normal':snap('giant-blue-ace-emerges')
   frames(130);check(diff+' ace takes over the same live boss encounter',p.evaluate('B===boss&&B._whv.mode==="ace"&&!B.dead&&!bossDefeated'))
   if diff=='normal':snap('giant-blue-ace-fight')
   row=p.evaluate('''()=>{const b=B,A=b._whv.ace;A.roll=A.somer=A.dash=A.desp=null;A.st='fight';b.flash=0;const a=s6Pixels(()=>whvDrawAce(b)),hp=b.hp;_dmgBullet={kind:'mg',x:A.x,y:A.y};_lastHitX=A.x;_lastHitY=A.y;hitBoss(1);_dmgBullet=null;const c=s6Pixels(()=>whvDrawAce(b));return{damage:hp-b.hp,flash:b.flash,pixels:s6Changed(a,c)};}''')
   check(diff+' giant ace retains real damage and native hit feedback',row['damage']>0 and row['flash']>0 and row['pixels']>30,row)
   frames(25);check(diff+' ace flash expires normally',p.evaluate('B.flash<=0'))
   p.evaluate('''()=>{const A=B._whv.ace;A.roll=A.somer=A.dash=A.desp=null;A.st='fight';_dmgBullet={kind:'mg',x:A.x,y:A.y};_lastHitX=A.x;_lastHitY=A.y;hitBoss(1e8);_dmgBullet=null;}''')
   check(diff+' only the ace defeat awards the native Stage6 boss clear',p.evaluate('B.dead&&bossDefeated&&!bossActive'))
   rows[diff]=row
  for diff in ['normal','hard','furious']:
   for mini in [True,False]:
    setup(mini,diff)
    p.evaluate('''mini=>{s6AllyDamage=[];s6WingLaunch(mini?2:8,!mini);window.wingOriginal=s6Wing.ships.slice();for(const q of wingOriginal){q.phase='fight';q.t=24.8;q.x=camLeftX()+90+q.slot*39;q.y=VH-65;q.fcd=0;q.missileCd=0;q.specialCd=8;}if(!mini)subBossDone=true;window.wingRounds=new Set();}''',mini)
    p.wait_for_function('()=>s6Wing.ships.length>0&&s6Wing.ships.every(q=>XART.rdy("ship_"+q.key))',polling=50)
    frames(240,"for(const q of pBullets)if(q.ally||q._wingKey)wingRounds.add(q);")
    row=p.evaluate('''()=>{const a=s6Pixels(()=>{}),c=s6Pixels(()=>s6WingDraw());return{count:s6Wing.ships.length,expected:wingOriginal.length,same:wingOriginal.every(q=>s6Wing.ships.includes(q)&&q.phase==='fight'&&q.hp>0&&q.t>25),rounds:wingRounds.size,damages:s6AllyDamage.length,damage:s6AllyDamage.reduce((n,q)=>n+q.damage,0),held:BOF_STAGE6_SEQUENCE.snapshot().held,targets:wingOriginal.map(q=>q.target?.name||q.target?.kind),phases:wingOriginal.map(q=>q.phase),pixels:s6Changed(a,c)};}''')
    label=diff+(' Fortress' if mini else ' Harrier')
    check(label+' allies retain the same living actors through combat and the old 25-second departure',row['same'] and row['count']==row['expected'] and not row['held'],row)
    check(label+' allies visibly draw, fire live rounds and damage real modules',row['rounds']>0 and row['damages']>0 and row['damage']>0 and row['pixels']>300,row)
    if diff=='normal':snap('fortress-live-allies' if mini else 'harrier-live-allies')
    if not mini:
     p.evaluate('''()=>{const C=B._carrier17;for(const part of C.parts.filter(q=>!q.dead)){C.direct=part.id;warhiveDamage(B,1e6);}}''');frames(280)
     row=p.evaluate('''()=>({same:wingOriginal.every(q=>s6Wing.ships.includes(q)&&q.phase==='fight'&&q.hp>0),ace:B._whv.mode==='ace',count:s6Wing.ships.length,expected:wingOriginal.length})''')
     check(diff+' allied wing persists through carrier breakup into the blue-ace fight',row['same'] and row['ace'] and row['count']==row['expected'],row)
  check('No native page, console, draw or missing-asset errors',not errors,errors[:20]);br.close()
finally:stop()
report=dict(checks=checks,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),errors=errors,rows=rows,sourceSha256=hashlib.sha256((R/'assets/stage6_reactor_1018.js').read_bytes()).hexdigest())
(O/'report.json').write_text(json.dumps(report,indent=2));print(f"{report['passed']} passed / {report['failed']} failed",flush=True)
sys.exit(1 if report['failed'] else 0)
