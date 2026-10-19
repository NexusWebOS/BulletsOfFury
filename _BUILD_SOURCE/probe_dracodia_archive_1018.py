"""Native archive combat probe. --fixture tests only local source-art logic."""
from pathlib import Path
import ast,json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];fixture='--fixture' in sys.argv;O=R/'_shots/dracodia_archive_1018'/('fixture' if fixture else 'native');O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];rows=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
def math_ceil_half(n):return (n+1)//2
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof V19!=="undefined"');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  if fixture:
   p.add_script_tag(url=f'http://127.0.0.1:{port}/_shots/dracodia_archive_1018/fixture_art.js')
   p.evaluate('''()=>{const copy=b=>({...b,frames:b.frames.map(a=>({...a,w:b.w,h:b.h,pivot:b.pivot}))});D20_ART.fx={bomb_charge:copy(ST18_ART.bomb),bomb_burst:copy(ST18_ART.impact),lightning_loop:copy(ST18_ART.impact),storm_loop:{fps:10,frames:PXV17_ART.code}};}''')
   p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/dracodia_archive_1018.js')
  p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(8)")
  p.evaluate('''()=>{window.archiveHits=[];window.arcNativeHit=playerHit;window.arcTrackHits=function(reason){archiveHits.push(reason);};playerHit=arcTrackHits;window.arcPixels=fn=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const a=ctx.getImageData(0,0,cv.width,cv.height).data;ctx.restore();return a;};window.arcDiff=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};window.keepD20Finish=d20Finish;d20Finish=function(b){keepD20Finish(b);b._r30.cd=999;};}''')
  def frames(n):
   for i in range(0,n,12):p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(12,n-i));p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(name+'.png')))
  def setup(diff='normal',phase=2,form=0):
   p.evaluate(SETUP,dict(stage=8,diff=diff,kind='vileexistence',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&d20Warm()&&bmfReady("game")}')
   p.evaluate('''([phase,form])=>{s6Opening=null;story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;stagePlan=[];warnT=0;warnKind=null;subBossDone=subBossTriggered=aminiTriggered=true;
    enemies=[];powerups=[];eBullets=[];pBullets=[];D20.sparks=[];D20.blasts=[];D20.events=[];archiveHits=[];playerHit=arcTrackHits;v18Budget(B);v18Enter(B,phase,form);B._r30.v18.arenaPhase=phase;v18Fight(B);B._r30.cd=999;
    player.x=worldWidth()/2;player.y=VH-70;player.invuln=0;player.dead=player.out=false;run.shield=0;run.spaceMode=false;bossWarned=true;for(const k of ['j','k','y','a','d','w','s'])Input.keys[k]=false;SC12.refresh();__bofFit();}''',[phase,form])
  for diff in ['normal','hard','furious']:
   setup(diff);p.evaluate('d20Start(B,"spiralLightning")');frames(48)
   check(diff+' lightning gives a real warning before contact',p.evaluate('D20.sparks.length===0&&!archiveHits.includes("spiraling code lightning")'))
   frames(120);snap(diff+'-spiral')
   q=p.evaluate('''()=>({count:D20.sparks.length,angles:D20.sparks.map(q=>Math.atan2(q.y-q.origin.y,q.x-q.origin.x)),release:D20.events.find(e=>e.event==='main-release'),pools:V18.forms.slice()})''');rows.append(dict(diff=diff,spiral=q))
   check(diff+' lightning actually spirals out from the core',q['count']>=8 and len(set(round(a,1) for a in q['angles']))>=5,q)
   check(diff+' retains exactly the five approved form pools',q['pools']==[0,8,1,6,2])
   p.evaluate('''()=>{window.arcQ=D20.sparks[0];window.arcT={...arcQ.origin};player.x=camLeftX()+20;player.y=viewTopY()+80;}''');frames(12)
   check(diff+' spiral trajectory never homes after release',p.evaluate('arcQ.origin.x===arcT.x&&arcQ.origin.y===arcT.y'))
   setup(diff);p.evaluate('d20Start(B,"codeBombs")');frames(190);snap(diff+'-bombs')
   check(diff+' retreats to the background before the bomb volley',p.evaluate('B._r30.v18.archiveDepth<.7&&B._noHit'))
   depth=p.evaluate('''()=>{const hp=B.hp;B._lastPart=B.parts[0];hitBoss(10);const rig=v18Rig(B);return{damage:hp-B.hp,depth:B._r30.v18.archiveDepth,scales:rig.map(v=>v.k),plane:target17BossContact(B,player.x,player.y)};}''')
   check(diff+' background body cannot hit or take plane damage',depth['damage']==0 and not depth['plane'] and max(depth['scales'])==min(depth['scales']),depth)
   bomb=p.evaluate('''()=>{window.testBomb=enemies.find(e=>e._d20?.kind==='bomb'&&!e.dead);if(!testBomb)return null;const hp=testBomb.hp,target={...testBomb._d20.target};_dmgBullet={x:testBomb.x,y:testBomb.y};hitEnemy(testBomb,999);_dmgBullet=null;return{hp,dead:testBomb.dead||testBomb._dyingT!=null,intercept:D20.events.some(e=>e.event==='code-bomb-intercepted'),target};}''')
   check(diff+' code bombs can be shot down',bool(bomb and bomb['dead'] and bomb['intercept']),bomb)
   frames(430);check(diff+' surviving bombs detonate at their committed target',p.evaluate('D20.events.some(e=>e.event==="code-detonation")'))
   check(diff+' boss returns to full scale and becomes damageable',p.evaluate('B._r30.v18.archiveDepth===1&&!B._noHit&&!B._r30.v18.attack'))
   setup(diff);p.evaluate('d20Start(B,"downloadLegion")');frames(150)
   check(diff+' downloads are harmless while assembling',p.evaluate('enemies.filter(e=>e._d20).length>0&&enemies.filter(e=>e._d20).every(e=>e._noHit&&e._d20.phase==="download")'))
   frames(240);snap(diff+'-archive')
   army=p.evaluate('''()=>enemies.filter(e=>e._d20&&!e.dead).map(e=>({id:e._d20.id,kind:e._d20.kind,hp:e.maxhp,source:e._d20.sourceHP,mini:e._d20.mini,phase:e._d20.phase,noHit:e._noHit,parts:e._d20.parts.map(p=>p.id),locks:_lockTargets().filter(q=>q._retinaOwner===e).length}))''');rows.append(dict(diff=diff,army=army))
   check(diff+' former bosses spawn at half their source HP',any(e['mini'] for e in army) and all(e['hp']==math_ceil_half(e['source']) for e in army if e['mini']),army)
   check(diff+' each downloaded hull exposes all three Retina modules',all(e['locks']==3 for e in army),army)
   check(diff+' formation respects the total actor cap',len(army)=={'normal':1,'hard':2,'furious':3}[diff],army)
   check(diff+' all summons become active and fire from real mounts',p.evaluate('enemies.filter(e=>e._d20&&!e.dead).every(e=>!e._noHit)&&D20.events.some(e=>e.event==="archive-shot")'))
   # Independent weapon pool, actual native damaged pixels and expiry.
   damage=p.evaluate('''()=>{window.archiveE=enemies.find(e=>e._d20?.mini&&!e.dead);const A=archiveE._d20,part=A.parts.find(p=>p.id==='left'),a=arcPixels(()=>d20EnemyDraw(archiveE)),hp=part.hp;window.archiveLock=_lockTargets().find(t=>t._retinaOwner===archiveE&&t.kind==='left');retinaMissileDamage(archiveLock,1,{kind:'missile',x:archiveLock.x,y:archiveLock.y});return{hp:hp-part.hp,pixels:arcDiff(a,arcPixels(()=>d20EnemyDraw(archiveE))),flash:part.flash,owner:archiveE.flash};}''')
   check(diff+' native Retina damage flashes the actual independent module pixels',damage['hp']>0 and damage['pixels']>20 and damage['flash']>0 and damage['owner']>0,damage)
   frames(18);check(diff+' summon flash expires',p.evaluate('archiveE.flash<=0&&archiveE._d20.parts.every(p=>p.flash<=0)'))
   p.evaluate("archiveE._d20.direct='left';hitEnemy(archiveE,archiveE._d20.parts.find(p=>p.id==='left').hp+.1);D20.events=[]");frames(360)
   check(diff+' destroyed launcher stops its own shots',p.evaluate('archiveE._d20.parts.find(p=>p.id==="left").hp<=0&&!retinaTargetValid(archiveLock)&&!D20.events.some(e=>e.event==="archive-shot"&&e.id===archiveE._d20.id&&e.port==="left")'))
   p.evaluate('d20Start(B,"downloadLegion")');frames(200)
   check(diff+' repeated downloads never exceed the live formation cap',p.evaluate('enemies.filter(e=>e._d20&&e._d20.kind!=="bomb"&&!e.dead&&e._dyingT==null&&e._d20.phase!=="erase").length<=1+d20Rank()'))
   p.evaluate('v18Clear(B)');frames(55)
   check(diff+' phase cleanup removes summons, shots and hazards',p.evaluate('!enemies.some(e=>e._d20&&!e.dead)&&!eBullets.some(q=>q._d20Owner===B)&&!D20.sparks.length&&!D20.blasts.length'))
  setup();p.evaluate('d20Finish=keepD20Finish;B._r30.cd=0;for(const i of V18.forms)if(i!==0)j3State(B).hp[i]=0;');frames(2880)
  kinds=p.evaluate('D20.events.filter(e=>e.event==="main-release").map(e=>e.type)')
  check('natural main-form controller uses all three new attacks',all(x in kinds for x in ['downloadLegion','spiralLightning','codeBombs']),kinds)
  for kind in ['bastion','camo','halberd']:
   setup();p.evaluate('(kind)=>{window.actor=d20Enemy(kind,worldWidth()/2,viewTopY()+viewH()*.32,B,true)}',kind);frames(390)
   check(kind+' archived weapon assemblies actually attack',p.evaluate('D20.events.some(e=>e.event==="archive-shot"&&e.kind===actor._d20.kind)'))
   snap(kind+'-modules')
   p.evaluate('''()=>{window.archiveHpBefore=actor.hp;B._r30.v18.home.x=B.x=camLeftX()-800;player.x=actor.x;run.weapon=0;run.wlevels[0]=run.wlevel=0;run.wvars[0]=null;run.forge={};run.forgeForms={};run.infusion=null;chaingunUnlocked=false;run._earnedUnlocks.chaingun=false;player.fireT=0;Input.keys.j=true;}''');frames(180);p.evaluate('Input.keys.j=false')
   check(kind+' takes actual centered machine-gun damage',p.evaluate('actor.hp<archiveHpBefore||actor.dead||actor._dyingT!=null'))
  # The real player damage path still owns protection and deaths.
  setup();p.evaluate('''()=>{window.archiveDeaths=stageStats.deaths;d20Bomb(B,{x:player.x,y:player.y});playerHit=arcNativeHit;}''');frames(120)
  check('code bomb arrival is harmless until its warned detonation',p.evaluate('stageStats.deaths===archiveDeaths&&!player.dead'))
  frames(90)
  check('a surviving code bomb actually damages an unprotected native player',p.evaluate('stageStats.deaths>archiveDeaths'))
  setup();p.evaluate('''()=>{window.archiveDeaths=stageStats.deaths;const e=d20Bomb(B,{x:player.x,y:player.y});e._d20.phase='arming';e._d20.t=e._d20.warm-.05;e.x=player.x;e.y=player.y;player.invuln=100;playerHit=arcNativeHit;}''');frames(30)
  check('code bombs respect the native dodge invulnerability path',p.evaluate('stageStats.deaths===archiveDeaths&&!player.dead'))
  setup();p.evaluate('d20Start(B,"spiralLightning")');frames(168)
  p.evaluate('''()=>{window.archiveDeaths=stageStats.deaths;const q=D20.sparks[0],t=q.t+1/60,r=28+t*q.speed,a=q.angle+t*q.spin;player.x=q.origin.x+Math.cos(a)*r;player.y=q.origin.y+Math.sin(a)*r;player.invuln=0;playerHit=arcNativeHit;}''');frames(1)
  check('visible spiral bolts actually damage the native player',p.evaluate('stageStats.deaths>archiveDeaths'))
  setup();p.evaluate('''()=>{window.actor=d20Enemy('camo',worldWidth()/2,viewTopY()+viewH()*.32,B,true);}''');frames(390)
  p.evaluate('''()=>{for(const id of ['left','right']){actor._d20.direct=id;hitEnemy(actor,actor._d20.parts.find(p=>p.id===id).hp+.1);}D20.events=[];}''');frames(280)
  check('destroying both Camo batteries silences their weapons',p.evaluate('!D20.events.some(e=>e.event==="archive-shot"&&e.id===actor._d20.id)&&actor._d20.parts[0].hp>0'))
  p.evaluate('''()=>{window.deadHullLocks=_lockTargets().filter(t=>t._retinaOwner===actor);actor._d20.direct='core';hitEnemy(actor,actor._d20.parts[0].hp+1);}''')
  check('destroyed hulls retire every cached Retina target immediately',p.evaluate('!_lockTargets().some(t=>t._retinaOwner===actor)&&deadHullLocks.every(t=>t.dead&&!retinaTargetValid(t))'))
  check('no page, console, drawing or asset errors',not errors,errors[:25]);br.close()
finally:stop()
data=dict(fixture=fixture,art_approval_pending=fixture,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,rows=rows,errors=errors)
(O/'results.json').write_text(json.dumps(data,indent=2));print(json.dumps({k:data[k] for k in ['fixture','passed','failed','errors']}));sys.exit(bool(data['failed']))
