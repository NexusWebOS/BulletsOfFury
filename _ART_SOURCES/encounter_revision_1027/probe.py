from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
port,stop=serve(str(R));errors=[];console=[];assets=[];results={};checks={}
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:console.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:assets.append({'url':r.url,'status':r.status})if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  print('LOADED',errors,flush=True)
  def step(n):
   err=p.evaluate(STEP,n)
   if err:errors.append(err)
  def start(stage,kind,role='boss'):
   p.evaluate('n=>{run.stage=n;stageLoadBegin(n);}',stage);p.wait_for_function('n=>{stageLoadTick();return stageLoadReady(n);}',arg=stage,timeout=180000)
   p.evaluate('''e=>{diffKey='furious';DIFF=DIFFS.furious;debugUnlocked=true;debugStartFight(e,{pilot:'cole',record:false});DBGT.god=true;run.weapon=3;run.wlevel=5;run.bombs=40;if(e.role==='mini')spawnSubBoss(e.kind);else spawnBoss(e.kind);debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);if(e.role==='mini')subBossActive=true;else bossActive=true;}''',dict(stage=stage,kind=kind,role=role,name='Revision probe'))
   step(240)
  start(6,'warhive');step(300)
  results['harrier']=p.evaluate('''()=>({dims:{VH,viewW:viewW(),viewH:viewH()},stageTimer,opening:!!s6Opening,talk:!!fb2Talk,wing:{beats:s6Wing.beats,all:s6Wing.all,fake:!!s6Wing.fake,allies:s6Wing.ships.length},parts:boss._carrier17.parts.filter(p=>['gun','laser'].includes(p.kind)).map(p=>({id:p.id,angle:p.angle,bearing:p.er28Bearing,muzzle:roster17Muzzle(boss,p)}))})''');p.screenshot(path=str(W/'harrier-native.png'))
  checks['harrierNoTimedDialogue']=not results['harrier']['opening']and not results['harrier']['talk']and not results['harrier']['wing']['fake']
  start(6,'rebelsquad');step(120);results['rebels']=p.evaluate('''()=>({state,allies:s6Wing.ships.map(q=>({pilot:q.key,x:q.x,y:q.y,phase:q.phase})),pods:boss._rebels.ships.filter(q=>q.key==='rook').map(q=>({heading:q.rfHeading,socket:rr26Socket(q,1)}))})''');p.screenshot(path=str(W/'rebels-native.png'));checks['rebelAlliesPresent']=len(results['rebels']['allies'])>=4
  start(7,'dualscoopdredger','mini');p.evaluate("s7mSet(subBoss,'er28-guns')");step(150);results['dredger']=p.evaluate('''()=>({mode:subBoss._s7mod.mode,rounds:eBullets.filter(q=>q._er28Slug).length,shots:subBoss._s7mod.er28.round,guns:s7mPose(subBoss).filter(p=>p.id.startsWith('gun')).map(p=>({id:p.id,angle:p.a,at:s7mMuzzle(subBoss,p.id)}))})''');p.screenshot(path=str(W/'dredger-native.png'));checks['dredgerRapidBothGuns']=results['dredger']['shots']>=15 and len(results['dredger']['guns'])==2
  p.evaluate("s7mSet(subBoss,'er28-mortar')");step(85);results['mortars']=p.evaluate('''()=>SW28.mortars.map(m=>({x:m.q.x,y:m.q.y,origin:m.start,target:m.target,age:m.t,flight:m.flight}))''');checks['dorsalMortars']=len(results['mortars'])>=5;p.screenshot(path=str(W/'mortars-native.png'))
  start(7,'sludgeemperor');p.evaluate("s7mSet(boss,'chase')");step(90);results['warden']=p.evaluate('''()=>({x:boss.x,middle:worldWidth()/2,y:boss.y,mode:boss._s7mod.mode,canisters:boss._s7mod.er28Canisters,targets:s7mTargets(boss).map(q=>q._retinaId),rear:s7mPose(boss).filter(p=>p.id.startsWith('rear')).map(p=>({id:p.id,angle:p.a,cell:p.cell,world:s7mWorld(boss,p),target:p.target}))})''');p.screenshot(path=str(W/'warden-native.png'));checks['wardenMiddleLane']=abs(results['warden']['x']-results['warden']['middle'])<.01
  results['canisterGate']=p.evaluate('''()=>{const b=boss,M=b._s7mod,before=M.core;s7mHit(b,100,0,0,'core');const blocked=M.core===before;for(const q of M.parts)if(q.id.startsWith('front')||q.id.startsWith('rear')){q.hp=0;q.dead=true;}const targets=s7mTargets(b).map(q=>q._retinaId);for(const c of M.er28Canisters)s7mHit(b,c.hp+1,0,0,c.id);const afterCans=M.shield;s7mHit(b,100,0,0,'core');return{blocked,targets,afterCans,coreBefore:before,coreAfter:M.core,targetsAfter:s7mTargets(b).map(q=>q._retinaId)}}''');checks['coreBlockedUntilBothCans']=results['canisterGate']['blocked']and results['canisterGate']['afterCans']==0 and results['canisterGate']['coreAfter']<results['canisterGate']['coreBefore'];checks['canisterTargetsReplaceCore']='core'not in results['canisterGate']['targets']and all(k in results['canisterGate']['targets']for k in ['canL','canR'])and'core'in results['canisterGate']['targetsAfter']
  p.evaluate("s7mSet(boss,'er28-bounce')");step(104);p.screenshot(path=str(W/'warden-bounce-native.png'));step(150);results['bounce']=p.evaluate("ER28.events.filter(q=>q.event==='warden-bounce-impact')");checks['bounceImpactScatter']=len(results['bounce'])>=3
  start(8,'heralddeath','mini');step(100)
  for kind,count in [('storm',240),('nuke',240),('rage',119),('pentagram',330)]:
   p.evaluate('k=>hr28Start(subBoss,k)',kind);step(count);p.screenshot(path=str(W/f'herald-{kind}-native.png'));results['herald-'+kind]=p.evaluate('''()=>({mode:subBoss._hd1003.mode,attack:subBoss._hd1003.er28?.kind,events:HR28.events.slice(-12),rounds:eBullets.filter(q=>q._er28Herald&&!q.dead).map(q=>({kind:q._er28Herald,proof:enemyOrdnanceCanIntercept(q),hp:q.hp,bounces:q._er28Bounces})),parts:subBoss._hd1003.parts.map(p=>({id:p.id,pose:hd1003Pose(subBoss,p)}))})''')
  checks['heraldNuke85']=any(q['event']=='nuke-impact'for q in results['herald-nuke']['events']);checks['heraldLightningVolleys']=any(q['event']=='red-lightning-volley'for q in results['herald-rage']['events']);checks['heraldPentagramBounces']=any(q['event']=='pentagram-bounce'for q in results['herald-pentagram']['events']);checks['newOrdnanceUnshootable']=all(not q['proof']for key in results if key.startswith('herald-')for q in results[key]['rounds'])
  results['performance']=p.evaluate('''()=>({banks:Object.keys(ER28_ART).length,alphaFrames:ER28.alpha.size,events:ER28.events.length,heraldEvents:HR28.events.length})''')
  br.close()
finally:
 stop();checks['noRuntimeErrors']=not errors;checks['noDrawErrors']=not any('draw error'in s.lower()for s in console);checks['noAssetErrors']=not assets
 (W/'probe-results.json').write_text(json.dumps({'checks':checks,'results':results,'errors':errors,'console':console,'assets':assets},indent=2));print(json.dumps({'checks':checks,'errors':errors,'console':console[:8],'assets':assets[:5]}),flush=True)
