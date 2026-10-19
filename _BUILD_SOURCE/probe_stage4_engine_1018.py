"""Real Chromium: Warden gun pixels, player fire, tank hull clearance and roadside density."""
from pathlib import Path
import ast,json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage4_engine_1018/native';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof WC18!=="undefined"');p.evaluate(shoot.TRAP_RAF)
  p.evaluate("pilotIndex=PILOTS.findIndex(p=>p.key==='cole');run.pilot='cole';startRun(4)")
  p.evaluate('''()=>{window.wc18DrawKeys={};window.wc18DrawKey=null;const cell=mr27Cell,draw=ctx.drawImage;
   mr27Cell=function(s,c){const out=cell.apply(this,arguments);wc18DrawKey=s==='iron'&&c>=100?'wc18_gun_'+String(c-100).padStart(2,'0'):null;return out;};
   ctx.drawImage=function(){if(wc18DrawKey)wc18DrawKeys[wc18DrawKey]=(wc18DrawKeys[wc18DrawKey]||0)+1;return draw.apply(this,arguments);};
   window.nativePixels=fn=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const d=Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);ctx.restore();return d;};
   window.changedPixels=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(a[i+3]>100&&Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};
   window.trafficAudit=()=>{const es=enemies.filter(groundTrafficVehicle),pairs=[];for(let i=0;i<es.length;i++)for(let j=i+1;j<es.length;j++)if(groundTrafficTouch(es[i],es[j]))pairs.push([es[i]._traffic18,es[j]._traffic18]);
    return{count:es.length,pairs,visible:es.filter(e=>e.y>viewTopY()&&e.y<VH).map(e=>({x:e.x,y:e.y,legal:groundTrafficLegal(e,e.x,e.y),foot:groundTrafficFootprint(e)})),stats:{...GT18.stats}};};}''')
  def frames(n,extra=''):
   for i in range(0,n,12):
    err=p.evaluate(shoot.STEP,min(12,n-i))
    if err:errors.append(err)
    if extra:p.evaluate(extra)
    p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}');p.screenshot(path=str(O/(name+'.png')))
  def setup(diff='normal',mini=False,stage=4):
   p.keyboard.up('j');p.evaluate(SETUP,dict(stage=stage,pilot='cole',diff=diff,**(dict(kind='olivewarden',mini=True) if mini else {})))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&wc18Ready()&&bmfReady("game")}',polling=50)
   p.evaluate('''()=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=s6Opening=null;AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;warnT=0;warnKind=null;
    VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;stagePlan=[];subBossTriggered=aminiTriggered=true;stageEnding=0;bossDefeated=false;Input.keys={};Input.mouse.down=false;
    run.spaceMode=false;run.shield=0;run.sonicT=run.dkT=0;special=thunderStorm=null;chaingunUnlocked=false;run._earnedUnlocks={...(run._earnedUnlocks||{}),chaingun:false};weaponFormSelect(7,{kind:'primary1003b',id:'mg'});
    run.weapon=0;run.wlevel=run.wlevels[0]=0;run.wvars[0]=null;run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[0];player.fireCd=0;player.x=worldWidth()/2;player.y=VH-60;player.invuln=0;playerHit=()=>{};powerups=[];
    if(subBoss){subBoss._be=null;subBoss.enter=subBoss._noHit=false;subBoss._phaseInvuln=0;subBoss.x=worldWidth()/2;subBoss.y=subBoss._er26.home;subBoss._drawY=subBoss.y;mr27Init(subBoss);}
    camX=clamp(player.x-VW/2,0,worldWidth()-VW);SC12.refresh();__bofFit();}''');frames(1)
  for diff in ['normal','hard','furious']:
   setup(diff,True);frames(210)
   row=p.evaluate('''()=>({part:mr27Part(B,'gunC'),shape:mr27Shape(B,'gunC'),size:[VW,VH,worldWidth(),viewW()],ready:wc18Ready(),draws:wc18DrawKeys,keys:WC18_ART.frames.map(a=>({w:a.w,h:a.h,pivot:a.pivot}))})''')
   check(diff+' generated central gun is a live fifth modular part, drawn at regular FOV',row['part']['hp']>0 and len(row['draws'])>0 and row['size'][0:2]==[480,512] and row['ready'],row)
   if diff=='normal':snap('01-warden-central-turret')
   p.evaluate("()=>{er26Set(B,'sa14-mg');window.wcBefore=WC18.shots;window.fired18=[];const slug18=sa14Slug;sa14Slug=function(b,s){const n=eBullets.length,r=slug18.apply(this,arguments);for(const q of eBullets.slice(n))fired18.push({slot:s,x:q.x,y:q.y,proof:q._weaponProof,shootable:q._shootable,pose:wc18Pose(b),port:shipBossMount(b,s)});return r;};}") if diff=='normal' else p.evaluate("er26Set(B,'sa14-mg');window.wcBefore=WC18.shots;fired18=[]")
   frames(220)
   row=p.evaluate('''()=>({shots:WC18.shots-wcBefore,fired:fired18,draws:wc18DrawKeys,slots:new Set(fired18.map(q=>q.slot)).size,proof:fired18.every(q=>q.proof&&!q.shootable),errors:fired18.filter(q=>q.slot==='C'&&Math.hypot(q.x-q.port.x,q.y-q.port.y)>.01)})''')
   check(diff+' actual MG turn fires L/C/R from matching animated barrel sockets',row['shots']>0 and row['slots']==3 and row['proof'] and not row['errors'],row)
   p.evaluate('''()=>{window.legacyBullet=stage4WarfareShot(B,{x:worldWidth()/2,y:VH-175},Math.PI/2,0,'mg',{shootable:true,hp:2});legacyBullet.vx=legacyBullet.vy=0;
    legacyBullet._weaponProof=false;legacyBullet._shootable=true;legacyBullet.hp=8;s3kOrdnanceRules(legacyBullet);player.x=legacyBullet.x;player.y=legacyBullet.y+130;player.fireCd=0;eBullets=[legacyBullet];pBullets=[];}''')
   p.keyboard.down('j');frames(60);p.keyboard.up('j')
   row=p.evaluate('''()=>({dead:!!legacyBullet.dead,proof:legacyBullet._weaponProof,shootable:legacyBullet._shootable,intercept:enemyOrdnanceCanIntercept(legacyBullet),element:enemyOrdnanceElement(legacyBullet),shots:pBullets.length})''')
   check(diff+' actual J rounds pass the legacy miniboss bullet without destroying it',not row['dead'] and row['proof'] and not row['shootable'] and not row['intercept'] and row['element'] is None,row)
   p.evaluate('''()=>{window.rocket18=sa14Missiles(B,{x:player.x,y:player.y});window.counterRocket=eBullets.find(q=>q._sa14Missile&&!q.dead);counterRocket.x=player.x;counterRocket.y=player.y-90;counterRocket.vx=0;counterRocket.vy=counterRocket.spd=.3;counterRocket._s4Accel=0;eBullets=[counterRocket];pBullets=[];player.fireCd=0;}''')
   p.keyboard.down('j');frames(45);p.keyboard.up('j')
   row=p.evaluate('''()=>({dead:!!counterRocket.dead,hp:counterRocket.hp,proof:counterRocket._weaponProof,shootable:counterRocket._shootable,input:Input.down('j'),rounds:pBullets.map(q=>({kind:q.kind,x:q.x,y:q.y})),weapon:run.weapon,sonic:run.sonicT,dk:run.dkT,cooldown:player.fireCd,state,held:Input.keys.j})''')
   check(diff+' actual missiles retain native player-fire interception',row['dead'],row)
   p.evaluate('''()=>{eBullets=[];pBullets=[];er26Set(B,'recover');B._er26.dur=3;const g=mr27Part(B,'gunC');g.fireAge=99;g.rot=0;window.gunHP18=g.hp;const m=shipBossMount(B,'C');player.x=m.x-(wm26PlayerNose().x-player.x);player.y=m.y+90;player.fireCd=0;}''')
   p.keyboard.down('j');frames(60);p.keyboard.up('j')
   row=p.evaluate('''()=>({hp:mr27Part(B,'gunC').hp,before:gunHP18,dead:mr27Part(B,'gunC').dead,rounds:pBullets.map(q=>({kind:q.kind,x:q.x,y:q.y})),weapon:run.weapon,sonic:run.sonicT,dk:run.dkT,cooldown:player.fireCd,state,px:player.x,py:player.y,shape:mr27Shape(B,'gunC'),hull:B.hp,mode:B._er26.mode})''')
   check(diff+' native J gunfire damages the actual centre weapon',row['hp']<row['before'],row)
   row=p.evaluate('''()=>{eBullets=[];pBullets=[];const g=mr27Part(B,'gunC');g.fireAge=99;g.rot=0;g.age=0;B.flash=0;const a=nativePixels(()=>mr27Draw(B)),hp=g.hp,m=mr27Shape(B,'gunC');_dmgBullet={kind:'mg',x:m.x,y:m.y};hitSubBoss(1,m.x,m.y);_dmgBullet=null;const b=nativePixels(()=>mr27Draw(B));return{changed:changedPixels(a,b),flash:g.flash,loss:hp-g.hp};}''')
   check(diff+' real centre damage flashes authored gun pixels via markHit',row['changed']>20 and row['flash']>0 and row['loss']>0,row)
   frames(24);check(diff+' centre flash expires without palette suppression',p.evaluate('mr27Part(B,"gunC").flash<=0'))
   row=p.evaluate('''()=>{const g=mr27Part(B,'gunC'),target=retinaBossTargets(B).find(q=>q._pieceKey?.includes('gunC')||q.kind==='gunC'),m=mr27Shape(B,'gunC'),hp=g.hp;
    if(target)retinaMissileDamage(target,2,{kind:'gmiss'});return{target:!!target,loss:hp-g.hp,keys:retinaBossTargets(B).map(q=>({kind:q.kind,id:q._pieceKey}))};}''')
   check(diff+' manual Retina missile targets and damages the centre independently',row['target'] and row['loss']>0,row)
   p.evaluate('''()=>{const m=mr27Shape(B,'gunC');_dmgBullet={kind:'gmiss'};hitSubBoss(1e6,m.x,m.y);_dmgBullet=null;window.deadShots18=WC18.shots;er26Set(B,'sa14-mg');}''');frames(200)
   row=p.evaluate('''()=>({dead:mr27Part(B,'gunC').dead,can:mr27CanFire(B,'C'),newShots:WC18.shots-deadShots18,other:B._mr27.parts.filter(p=>p.id!=='gunC'&&!p.dead).length,breaks:B._mr27.breaks})''')
   check(diff+' destroyed centre stops firing while side guns and rockets remain',row['dead'] and not row['can'] and row['newShots']==0 and row['other']==4 and 'gunC' in row['breaks'],row)
   if diff=='normal':snap('02-centre-gun-destroyed')
  for diff in ['normal','hard','furious']:
   setup(diff);p.evaluate('''()=>{window.nativeTankShots=0;const s=eShootT;eShootT=function(){nativeTankShots++;return s.apply(this,arguments);};
    window.birthOverlaps=[];for(let i=0;i<12;i++){spawnEnemy('sandtank',worldWidth()/2,130,{shoots:true});if(trafficAudit().pairs.length)birthOverlaps.push(trafficAudit());}}''')
   row=p.evaluate('trafficAudit()');check(diff+' twelve simultaneous tank births reserve complete hulls immediately',not row['pairs'] and not p.evaluate('birthOverlaps.length'),row)
   p.evaluate('window.motionOverlaps=[];window.terrainFailures=[];window.shotStart=nativeTankShots')
   frames(1800,'''()=>{const a=trafficAudit();if(a.pairs.length)motionOverlaps.push(a);for(const e of a.visible)if(!e.legal)terrainFailures.push(e);}''')
   row=p.evaluate('''()=>({overlaps:motionOverlaps.length,terrain:terrainFailures.slice(0,3),shots:nativeTankShots-shotStart,audit:trafficAudit()})''')
   check(diff+' thirty seconds of driving and firing never stacks tank hulls',row['overlaps']==0 and row['shots']>0,row)
   check(diff+' queued highway tanks stay on drivable terrain when visible',not row['terrain'],row)
   if diff=='normal':
    snap('03-highway-tank-clearance')
    row=p.evaluate('''()=>{window.flashTank18=enemies.find(e=>groundTrafficVehicle(e)&&e.y>viewTopY()+60&&e.y<VH-60);const e=flashTank18;e.flash=0;const a=nativePixels(()=>drawEnemy(e)),hp=e.hp;_dmgBullet={kind:'mg',x:e.x,y:e.y};hitEnemy(e,1);_dmgBullet=null;const b=nativePixels(()=>drawEnemy(e));return{pixels:changedPixels(a,b),loss:hp-e.hp,flash:Math.max(e.flash||0,e._armor17.hullFlash,...e._armor17.parts.map(p=>p.flash||0))};}''')
    check('Spaced highway tanks still visibly flash their authored damaged pixels',row['pixels']>100 and row['loss']>0 and row['flash']>0,row)
    frames(20);check('Tank hit flashes expire through native movement',p.evaluate('flashTank18.flash<=0&&flashTank18._armor17.hullFlash<=0&&flashTank18._armor17.parts.every(p=>p.flash<=0)'))
  for stage in [1,3,7]:
   setup(stage=stage);row=p.evaluate('''()=>{for(let i=0;i<8;i++)spawnEnemy(run.stage===1?'s1tankheavy':'tank',worldWidth()/2,150,{shoots:true});return trafficAudit();}''')
   check('Stage '+str(stage)+' tank-class spawns obey the same engine clearance rule',not row['pairs'] and row['count']>0,row)
  pressures=[]
  for diff in ['normal','hard','furious']:
   setup(diff);p.evaluate('HM17.next=100');frames(2700)
   row=p.evaluate('''()=>({difficulty:diffKey,launched:HM17.events.filter(e=>e.event==='pad-spawn').length,events:HM17.events,scroll:LA1007.scroll,gap:hm17Config().gap,next:HM17.next})''');pressures.append(row)
   check(diff+' denser roadside nuclear pads alternate shoulders',row['launched']>=5 and len(set(q.get('side') for q in row['events'] if q['event']=='pad-spawn'))==2,row)
   if diff=='normal':snap('04-more-roadside-nuclear-missiles')
  check('Native roadside pressure rises Normal to Hard to Furious',pressures[0]['launched']<pressures[1]['launched']<=pressures[2]['launched'],pressures)
  br.close()
finally:stop()
check('No native page, console, draw or asset errors',not errors,errors)
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
