"""Native stationary-core charge, highway pressure and encounter weapon-lock regression."""
from pathlib import Path
import ast,json,sys,hashlib,traceback,argparse,http.server
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path);args=ap.parse_args()
O=R/'_shots/targeting_1017'/('candidate-verification' if args.candidate else '');O.mkdir(parents=True,exist_ok=True)
overrides={}
if args.candidate:
 for f in args.candidate.rglob('*'):
  if f.is_file():overrides['/'+f.relative_to(args.candidate).as_posix()]=f.read_bytes()
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[]
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
# Whole-stage loose art/audio banks create a large first-use request burst.
# Keep the real static server's accept queue from refusing an unrelated sample.
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=browser.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.on('requestfailed',lambda r:errors.append(str(r.failure)+' '+r.url) if r.failure and 'ERR_ABORTED' not in r.failure else None)
  if overrides:
   def candidate_route(route,request):
    path=urlparse(request.url).path
    if path in overrides:route.fulfill(body=overrides[path],content_type='text/html' if path.endswith('.html') else 'application/javascript')
    else:route.continue_()
   for path in overrides:p.route('**'+path+'*',candidate_route)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof target17Tick==="function"');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.targetArt={};const draw=ctx.drawImage;ctx.drawImage=function(im){const t=im?._so21||PXG.tags.get(im);if(t?.key&&/^(rp21_pulse_|pt11_sonic_pulse_|l23fx_inferno_mg_|bfx_cryo_[pm]_|retm_|retmb_|nsw_)/.test(t.key))targetArt[t.key]=(targetArt[t.key]||0)+1;return draw.apply(this,arguments)};
   window.targetBeeps=0;const s=Audio.SFX.lockon;Audio.SFX.lockon=function(){targetBeeps++;return s?.apply(this,arguments)};}''')
  def setup(stage,kind=None,mini=False,diff='hard'):
   p.evaluate(SETUP,dict(stage=stage,kind=kind,mini=mini,pilot='cole',diff=diff))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}')
   p.evaluate('''()=>{story=fb2Talk=null;BOFCinematicDirector.cancel();VP12.next=CP12.next=EP13.next=9999;stagePlan=[];warnT=0;warnKind=null;aminiTriggered=true;_sc1=_sc2=_mc1=_mc2=true;Input.keys={};player.invuln=1e9;run.shield=0;powerups=[];targetArt={};targetBeeps=0;TARGET17.events=[];
    if(window.B){B._noHit=false;B._jcGhost=false;B._phaseInvuln=0;if(B._er26){B._er26.engaged=false;er26Tick(B,0);}}}''')
  def frames(n):
   for i in range(0,n,30):p.evaluate('n=>{for(let i=0;i<n;i++){story=fb2Talk=null;BOFCinematicDirector.cancel();updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60)}}',min(30,n-i));p.wait_for_timeout(4)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();window.__bofFit()}');p.screenshot(path=str(O/(name+'.png')))
  for diff in ['normal','hard','furious']:
   setup(4,'stormsovereign',diff=diff)
   data=p.evaluate('''()=>{stage4ShieldSyncNodes(B);const H=B._s4war.shield,before=H.nodes.map(n=>({x:n.x,y:n.y}));window.stationTest={before,start:{x:B.x,y:B.y},lengths:[]};
    er26Set(B,'sa14-drive');B._er26._sa14.aim={x:B.x+70,y:VH-95};return{nodes:before,start:stationTest.start};}''')
   p.evaluate('()=>{for(let i=0;i<24;i++){B._er26.t=B._er26.warm+i/60;sa14Attack(B,1/60);stage4ShieldSyncNodes(B);stationTest.lengths.push(Math.hypot(B.x-B._s4war.shield.nodes[0].x,B.y-B._s4war.shield.nodes[0].y));}}')
   charge=p.evaluate('''()=>({moved:Math.hypot(B.x-stationTest.start.x,B.y-stationTest.start.y),fixed:B._s4war.shield.nodes.every((n,i)=>Math.hypot(n.x-stationTest.before[i].x,n.y-stationTest.before[i].y)<.001),extended:Math.max(...stationTest.lengths)-Math.min(...stationTest.lengths),contacts:B._s4war.shield.nodes.map(n=>target17BossContact(B,n.x,n.y)),shootable:B._s4war.shield.nodes.map(n=>{B._noHit=false;return bossHitTest(n.x,n.y)&&B._s4ShieldHit===n;})})''')
   check(diff+' charge moves the hull and leaves every generator at its station',charge['moved']>80 and charge['fixed'],charge)
   check(diff+' lightning tether extends and generators remain shootable',charge['extended']>25 and all(charge['shootable']),charge)
   check(diff+' detached cores do not cause hull contact damage',not any(charge['contacts']),charge)
   if diff=='hard':snap('sovereign-charging-cores-stay-behind')
   safe=p.evaluate('''()=>{const h=B._s4war.shield.nodes[0];player.reset();player.invuln=0;run.shield=0;player.x=h.x;player.y=h.y+6;eBullets=[];enemies=[];pBullets=[];updatePlay(0);return{dead:player.dead};}''')
   check(diff+' native player survives at the detached generator',not safe['dead'],safe)
   control=p.evaluate('''()=>{const hit=target17BossContact,n=B._s4war.shield.nodes[0];player.reset();player.invuln=0;run.shield=0;run.lives=3;player.x=n.x;player.y=n.y+6;
    try{target17BossContact=(b,x,y)=>bossHitTest(x,y);updatePlay(0);return player.dead;}finally{target17BossContact=hit;}}''')
   check(diff+' legacy contact control reproduces the generator death',control)
   hull=p.evaluate('''()=>{player.reset();player.invuln=0;run.shield=0;run.lives=3;player.x=B.x;player.y=B.y+6;updatePlay(0);return player.dead;}''')
   check(diff+' the physical charging hull still causes contact damage',hull)
  for diff in ['normal','hard','furious']:
   setup(4,diff=diff)
   p.evaluate('()=>{subBossTriggered=subBossDone=true;TARGET17.nextTank=0;stageTimer=3;stagePlan=[];}')
   frames(2400)
   road=p.evaluate('()=>({count:TARGET17.tanks,spawns:TARGET17.events.filter(e=>e.type==="highway-tank"),visible:enemies.filter(e=>e._target17Tank&&!e.dead).map(e=>({x:e.x,y:e.y,mod:e._modTank})),paved:TARGET17.events.filter(e=>e.type==="highway-tank").every(q=>tankDrivable(q.x,q.sourceY,false)&&tankDrivable(q.x-23,q.sourceY,false)&&tankDrivable(q.x+23,q.sourceY,false)),scroll:LA1007.scroll,mini:subBossActive})')
   if diff=='normal':check('Normal retains its existing highway density',road['count']==0,road)
   else:
    check(diff+' sustains extra highway tanks',road['count']>=(7 if diff=='hard' else 10),road)
    check(diff+' tank spawns use the scrolling paved central highway',road['paved'] and road['scroll']>400 and not road['mini'] and all(680*.30<=q['x']<=680*.70 for q in road['spawns']),road)
    check(diff+' reinforcement art uses native modular desert tanks',any(q['mod']==4 for q in road['visible']),road)
    snap('highway-'+diff+'-reinforcements')
  for stage,kind,element in [(1,'razorback','sonic'),(2,'magmaward','fire'),(3,'frostcruiser','ice')]:
   for diff in ['normal','hard','furious']:
    setup(stage,kind,True,diff);frames(660)
    row=p.evaluate('''()=>({events:TARGET17.events.filter(e=>e.type==='weapon-shot'),locked:TARGET17.events.filter(e=>e.type==='target-locked'),beeps:targetBeeps,art:Object.keys(targetArt),shots:eBullets.filter(q=>q._target17Owner===B).map(q=>({port:q._target17Port,kind:q.kind,art:q._target17Art,element:enemyOrdnanceElement(q),shootable:q._shootable,proof:q._weaponProof,mg:q.mg}))})''')
    check(str(stage)+' '+diff+' tracks, beeps and releases from its weapon mounts',len(row['events'])>0 and len(row['locked'])>0 and row['beeps']>3,row)
    prefix={'sonic':'rp21_pulse_','fire':'l23fx_inferno_mg_','ice':'bfx_cryo_p_'}[element]
    check(str(stage)+' '+diff+' native renderer draws authored '+element+' projectile frames',any(k.startswith(prefix) for k in row['art']) and any(k.startswith('retm_') for k in row['art']) and any(k.startswith('retmb_') for k in row['art']),row['art'])
    if stage in [2,3]:check(str(stage)+' '+diff+' gun bullets retain native interception rules',any(q.get('mg') for q in row['shots']) and all(not q.get('shootable') and q.get('proof') for q in row['shots'] if q.get('mg')),row['shots'][:6])
    if stage==3:check(diff+' ice miniboss fires gun bullets and rack missiles',any(not q['rocket'] for q in row['events']) and any(q['rocket'] for q in row['events']),row['events'][:6])
    if diff=='hard':snap(element+'-tracking-and-projectiles')
  # Destroyed emitters must stop their own targeting channel; surviving mounts remain.
  for stage,kind,part in [(2,'magmaward','gunL'),(3,'frostcruiser','gunL')]:
   setup(stage,kind,True);frames(180)
   p.evaluate('''part=>{if(B._av3Reaver){const p=av3Part(B,part);p.hp=0;p.dead=true;}else{const p=mr27Part(B,part);p.hp=0;p.dead=true;}TARGET17.events=[];}''',part)
   frames(420)
   ports=p.evaluate('TARGET17.events.filter(e=>e.type==="weapon-shot").map(e=>e.port)')
   check(kind+' never fires its destroyed left turret but keeps the right active','L' not in ports and 'R' in ports,ports)
  for stage,kind,mini in [(7,'dualscoopdredger',True),(7,'sludgeemperor',False),(8,'heralddeath',True),(8,'vileexistence',False),(9,'voidhorizon',True),(9,'tidalfusion',False)]:
   setup(stage,kind,mini);frames(1200)
   late=p.evaluate('()=>({ports:target17Ports(B,target17Kind(B)).map(q=>q.id),events:TARGET17.events.filter(e=>e.type==="weapon-shot"),beeps:targetBeeps})')
   check(kind+' uses tracking locks and releases from live existing weapons',len(late['events'])>=2 and late['beeps']>3,late)
   if stage in [7,8,9]:snap(kind+'-targeting')
  # A final red lock stays put; only the Stage-1 sonic projectile gets a short,
  # explicit guidance grant. Verify through the real update/missile interception path.
  setup(1,'razorback',True,'normal');frames(180)
  lock=p.evaluate('''()=>{const T=B._target17;T.phase='recover';T.cool=0;target17Tick(B,0);
   T.t=T.warm-.45;player.x=camLeftX()+viewW()*.7;target17Tick(B,.02);const tracked={...T.aim};
   T.t=T.warm-.39;player.x=camLeftX()+viewW()*.2;target17Tick(B,.02);const held={...T.aim};
   T.t=T.warm;target17Tick(B,.02);window.sonicProbe=eBullets.findLast(q=>q._target17Art==='sonic');T.phase='recover';T.cool=999;
   eBullets=[sonicProbe];pBullets=[];sonicProbe.x=camLeftX()+viewW()/2;sonicProbe.y=260;sonicProbe.vx=0;sonicProbe.vy=sonicProbe.spd;
   player.x=camLeftX()+viewW()*.88;player.y=VH-80;return{tracked,held,start:Math.atan2(sonicProbe.vy,sonicProbe.vx)};}''')
  check('Final warning commits its aim before launch',lock['tracked']==lock['held'],lock)
  frames(30);guided=p.evaluate('Math.atan2(sonicProbe.vy,sonicProbe.vx)')
  check('Sonic missile visibly turns during its bounded homing window',abs(guided-lock['start'])>.1,dict(lock=lock,angle=guided))
  frames(57)
  committed=p.evaluate('()=>{player.x=camLeftX()+viewW()*.1;return{a:Math.atan2(sonicProbe.vy,sonicProbe.vx),age:sonicProbe._target17Guide.t};}')
  frames(12)
  final=p.evaluate('({a:Math.atan2(sonicProbe.vy,sonicProbe.vx),alive:!sonicProbe.dead,homing:sonicProbe.homing})')
  check('Sonic guidance expires and cannot reacquire after a dodge',committed['age']>=1.35 and abs(final['a']-committed['a'])<.00001 and final['alive'] and not final['homing'],dict(committed=committed,final=final))
  p.evaluate('''()=>{sonicProbe.x=camLeftX()+viewW()/2;sonicProbe.y=PLAY.y+300;window.sonicTrailsBefore=sonicTrail.length;
   pBullets=[{kind:'mg',x:sonicProbe.x,y:sonicProbe.y,vx:0,vy:0,w:8,h:12,dmg:4,t:0}];}''')
  frames(1)
  interception=p.evaluate('()=>({dead:sonicProbe.dead,impact:sonicProbe._fbImpact1002,trail:sonicTrail.length>sonicTrailsBefore})')
  check('Ordinary gunfire intercepts the sonic missile with sonic impact feedback',interception['dead'] and interception['impact'] and interception['trail'],interception)
  snap('sonic-shot-down')
  # Each copied finale form must use its current moving rig, not the previous
  # form's sockets. Transformation gates and destroyed emitters stay authoritative.
  setup(8,'vileexistence');frames(180)
  for form in range(1,8):
   p.evaluate('n=>{r30Form(B,n);B._r30.mode="fight";TARGET17.events=[];delete B._target17;}',form)
   frames(420)
   row=p.evaluate('()=>({id:f1003bDef(B).id,shots:TARGET17.events.filter(q=>q.type==="weapon-shot").length,ports:target17Ports(B,"dark").map(q=>q.id)})')
   if row['id']=='knight':check('Finale knight retains its native melee targeting',row['shots']==0 and not row['ports'],row)
   else:check('Finale '+row['id']+' targets from the current modular rig',row['shots']>0 and len(row['ports'])>0,row)
  p.evaluate('()=>{B._r30.mode="morph";TARGET17.events=[];}');frames(30)
  check('Finale transformation cancels the extra targeting channel',p.evaluate('TARGET17.events.every(q=>q.type!=="weapon-shot")&&B._target17.phase==="recover"'))
  setup(9,'tidalsovereign');frames(600)
  tidal=p.evaluate('()=>({kind:target17Kind(B),ports:target17Ports(B,target17Kind(B)).map(q=>({id:q.id,...q.pos()})),shots:TARGET17.events.filter(e=>e.type==="weapon-shot")})')
  check('Merged Tidal Sovereign uses its authored water-cannon tips',tidal['kind']=='water' and len(tidal['ports'])==2 and len(tidal['shots'])>0,tidal)
  snap('merged-tidal-targeting')
  # Real damage must still change actual authored pixels and its flash must expire.
  def feedback(stage,kind,mini=True):
   setup(stage,kind,mini);frames(180)
   for i in range(25):
    if p.evaluate('retinaBossTargets(B).some(q=>!q.dead)'):break
    frames(30)
   row=p.evaluate('''()=>{const ts=retinaBossTargets(B).filter(q=>!q.dead),t=ts.find(q=>/gun|turret|left|sentinel|ward|module/i.test(q._retinaId||q.part?.id||q.kind||q.name||''))||ts[0];
    if(!t)return{missing:true,mode:B._rzb?.state,pair:B._rzbPair?.actors.map(b=>({state:b._rzb.state,trans:b._rzb.trans,dead:b.dead,enter:b.enter}))};window.flashProbe={target:t};
    function image(){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);if(B===subBoss)drawSubBoss();else drawBoss();ctx.restore();return ctx.getImageData(0,0,cv.width,cv.height).data;}
    const a=image(),hp=t.hp;const routed=retinaMissileDamage(t,1,{kind:'gmiss',x:t.x,y:t.y});const c=image();let pixels=0;
    for(let i=0;i<a.length;i+=4)if(a[i]!==c[i]||a[i+1]!==c[i+1]||a[i+2]!==c[i+2])pixels++;
    window.readTargetFlash=function(){const bs=B._rzbPair?.actors||[B];return Math.max(0,...bs.flatMap(b=>b._rzb?Object.values(b._rzb.flash):[b.flash||0,...(b._mr27?.parts||[]).map(p=>p.flash||0),...(b._av3Reaver?.parts||[]).map(p=>p.flash||0),...(b._s7mod?.parts||[]).map(p=>p.flash||0),...(b._hd1003?.parts||[]).map(p=>p.flash||0),...(b.parts||[]).map(p=>p.flash||0),b._s9rift?.core?.flash||0,b._s9fusion?.left?.flash||0,b._s9fusion?.right?.flash||0]));};
    return{routed,pixels,hpLost:hp-t.hp,flash:readTargetFlash(),target:t._retinaId||t.kind||t.name};}''')
   check(kind+' native damage still flashes its authored pixels',row.get('routed') and row.get('pixels',0)>10 and row.get('hpLost',0)>0 and row.get('flash',0)>0,row)
   frames(60)
   check(kind+' damage flash expires normally',not row.get('missing') and p.evaluate('readTargetFlash()<=0'))
  for stage,kind,mini in [(1,'razorback',True),(2,'magmaward',True),(3,'frostcruiser',True),(7,'dualscoopdredger',True),(7,'sludgeemperor',False),(8,'heralddeath',True),(8,'vileexistence',False),(9,'voidhorizon',True),(9,'tidalfusion',False),(9,'tidalsovereign',False)]:feedback(stage,kind,mini)
  setup(4);p.evaluate('()=>{subBossTriggered=subBossDone=true;window.roadFlash=spawnEnemy("sandtank",worldWidth()/2,300,{shoots:true});roadFlash._target17Tank=true;}');frames(2)
  row=p.evaluate('''()=>{function im(){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);drawEnemy(roadFlash);ctx.restore();return ctx.getImageData(0,0,cv.width,cv.height).data;}
   const a=im(),hp=roadFlash.hp;hitEnemy(roadFlash,1);const c=im();let pixels=0;for(let i=0;i<a.length;i+=4)if(a[i]!==c[i]||a[i+1]!==c[i+1]||a[i+2]!==c[i+2])pixels++;return{hpLost:hp-roadFlash.hp,flash:roadFlash.flash,pixels};}''')
  check('Additional highway tank visibly flashes on real damage',row['hpLost']>0 and row['flash']>0 and row['pixels']>10,row);frames(30)
  check('Highway tank flash expires normally',p.evaluate('roadFlash.flash<=0'))
  check('No page, console or missing-asset errors',not errors,errors);browser.close()
except Exception as e:errors.append(str(e));print(traceback.format_exc(),flush=True)
finally:
 stop();report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors,
  runtime_sha256={f:hashlib.sha256(overrides.get('/'+f,(R/f).read_bytes())).hexdigest() for f in ['index.html','assets/game.js','assets/targeting_1017.js']},scope='Native controlled encounter, highway and unshielded-contact fixtures, actual art and sound calls. Not a full human campaign clear.')
 (O/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='checks'}),flush=True)
if errors or report['failed']:sys.exit(1)
