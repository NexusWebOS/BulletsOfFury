"""Native Stage 3/4 combat and Yuri progression fixtures; not human clear evidence."""
from pathlib import Path
import ast,json,sys,traceback
from playwright.sync_api import sync_playwright
import shoot

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/stage34_assault_1014';OUT.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((ROOT/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];scenes=[]
def check(ok,name,data=None):
 checks.append({'passed':bool(ok),'name':name,'data':data})
 print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)

port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio','--autoplay-policy=no-user-gesture-required'])
  page=browser.new_page(viewport={'width':1440,'height':1000});page.set_default_timeout(120000)
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  page.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  page.goto(f'http://127.0.0.1:{port}/index.html');page.wait_for_function('window.__bofFrames>4&&typeof SA14!=="undefined"')
  page.evaluate(shoot.TRAP_RAF);page.wait_for_timeout(40)
  def frames(n,expression='updatePlay(1/60);'):
   for start in range(0,n,24):
    page.evaluate('(n)=>{for(let j=0;j<n;j++){'+expression+'}}',min(24,n-start));page.wait_for_timeout(8)
  def setup(stage,kind=None,diff='normal',mini=False,pilot='cole'):
   page.evaluate(SETUP,dict(stage=stage,kind=kind,diff=diff,mini=mini,pilot=pilot))
   page.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&XART.rdy(SC12_ART.key)&&bmfReady("game")}',polling=50)
   if kind:
    page.evaluate('()=>{B._er26.engaged=false;B._phaseInvuln=0;B.flash=0;er26Tick(B,0);stage4ShieldSyncNodes(B);}')
    page.wait_for_function('()=>{drawWorld(0);return !B._mr27||(B._ship==="frostcruiser"?pt11Ready("ice_parts"):XART.rdy("mr27_"+B._mr27.skin));}')
   page.evaluate('()=>{SA14.events=[];Input.keys={};story=fb2Talk=null;BOFCinematicDirector.cancel();player.invuln=1e9;run.weapon=0;run.wlevel=1;run.wlevels=run.wlevels||WEAPONS.map(()=>0);run.wvars=run.wvars||WEAPONS.map(()=>null);run.wlevels[0]=1;run.wvars[0]=null;}')
  def snap(name):
   page.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();window.__bofFit();}')
   page.screenshot(path=str(OUT/(name+'.png')));scenes.append(name)

  # A real earned Stage-4 reward must survive the Stage-5/6 deployment path.
  setup(4,pilot='yuri')
  page.evaluate('()=>{run._earnedUnlocks={};run._thunderStormUnlocked=false;yuriLightningOrbGrantStage4();beginStage(5);setState(GS.PLAY);story=null;BOFCinematicDirector.cancel();stagePlan=[];spawnClock=9999;waveIdx=999;player.reset();player.invuln=1e9;}')
  page.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)}')
  check(page.evaluate('run._thunderStormUnlocked&&run._chainLightningLevel>=2&&run._earnedUnlocks.lightningOrb'),'Yuri retains earned Storm and chain tier across actual Stage 4 -> 5 entry')
  check(page.evaluate('ph8Values().name.startsWith("THUNDER STORM")'),'Stage-5 HUD identifies the Storm upgrade')
  page.evaluate('startSpecial()')
  fire_key=page.evaluate('keybindFor(1).fire.find(k=>!k.startsWith("pad_")&&!k.startsWith("mouse"))')
  page.keyboard.down(fire_key)
  print('Yuri activation '+json.dumps(page.evaluate('({active:specialActive("yuri"),special,state,space:run.spaceMode,charging:chargePilotActive(),keys:keybindFor(1).fire})')),flush=True)
  frames(72)
  print('Yuri held '+json.dumps(page.evaluate('({active:specialActive("yuri"),t:special?.t,charge:special?._yCharge,held:player._tapHeld,fire:Input.hold(1,"fire"),timer:stageTimer,scene:h3Locked(),entry:run._s5Entry,story:!!story,cinematic:BOFCinematicDirector.live})')),flush=True)
  page.keyboard.up(fire_key);frames(2)
  check(page.evaluate('!!thunderStorm&&thunderStorm.power>.5'),'Actual held fire/release invokes Storm in Stage 5')
  snap('yuri-stage5-storm')
  page.evaluate('beginStage(6)');check(page.evaluate('run._thunderStormUnlocked'),'Earned Storm also survives Stage 6 entry')
  page.evaluate('()=>{run.pilot="yuri";run._earnedUnlocks={};beginStage(1);}');check(page.evaluate('!run._thunderStormUnlocked'),'An unearned fresh run does not inherit account or previous-run Storm')
  setup(4,pilot='cole');page.evaluate('()=>{coopOn=true;run2.pilot="yuri";run2._earnedUnlocks={};yuriLightningOrbGrantStage4();beginStage(5);}')
  check(page.evaluate('run2._thunderStormUnlocked&&run2._chainLightningLevel>=2&&!run._thunderStormUnlocked'),'Co-op Yuri retains his reward without granting Cole the ability')
  page.evaluate('coopOn=false')

  for difficulty in ['easy','normal','hard','furious']:
   setup(3,'frostcruiser',difficulty,True)
   before=page.evaluate('({kind:B.kind,name:B.name,hp:B.maxhp,w:B.w,h:B.h})')
   frames(360)
   q=page.evaluate('({same:B.kind,form:B._er26.form,nuclear:!!B._s3Nuclear,strike:!!S3_THERMO_STRIKE.mini,atomic:atomBooms.length,skin:B._mr27.skin})')
   check(q['form']=='ice' and not q['nuclear'] and not q['strike'],difficulty+' Frost miniboss remains ice without nuclear transformation',q)
   check(q['same']==before['kind'] and page.evaluate('B.maxhp')==before['hp'],difficulty+' ice miniboss retains its actor and authored modular health')
   if difficulty=='furious':snap('frost-miniboss-furious')
   setup(3,'cryospear',difficulty)
   page.evaluate('()=>{er26Set(B,"sa14-mg");}')
   frames(210)
   slugs=page.evaluate('eBullets.filter(q=>q._sa14Slug).map(q=>({kind:q.kind,proof:q._weaponProof,source:q._er26Source}))')
   emitted=page.evaluate('B._er26.shots')
   check(emitted>=8 and all(q['kind']=='mg' and q['proof'] for q in slugs),difficulty+' Rime turrets release rapid non-interceptable machine slugs',{'emitted':emitted,'remaining':len(slugs)})
   check(page.evaluate('!B._l23Beam&&!eBullets.some(q=>q._beam||q.kind==="beam")'),difficulty+' Rime boss does not launch a laser')
   page.evaluate('()=>{eBullets=[];er26Set(B,"sa14-rockets");}')
   frames(int(page.evaluate('B._er26.warm*60'))+25)
   missiles=page.evaluate('eBullets.filter(q=>q._sa14Missile).map(q=>({shootable:q._shootable,proof:q._weaponProof,kind:q.kind}))')
   check(len(missiles)>0 and all(q['shootable'] and not q['proof'] for q in missiles),difficulty+' Rime missile volleys use shootable missile ordnance',len(missiles))
   page.evaluate('()=>{eBullets=[];SA14.events=[];er26Set(B,"sa14-ice");}')
   frames(85)
   if difficulty=='normal':snap('rime-ice-charge')
   frames(195)
   ice=page.evaluate('SA14.events.filter(q=>q.event==="ice-volley")')
   check(len(ice)==4 and all(len(q['angles'])<7+page.evaluate('vp12Tier()')*2 for q in ice),difficulty+' charged ice salvos keep a real two-lane opening',ice)
   check(len(ice)>1 and all(ice[i]['x']>ice[i-1]['x'] for i in range(1,len(ice))),difficulty+' Rime shifts right between ice volleys',[q['x'] for q in ice])
   if difficulty=='normal':snap('rime-moving-ice-salvos')

  setup(4,'stormsovereign')
  page.evaluate('()=>{player.x=B.x+55;player.y=VH-85;er26Set(B,"sa14-drive");}')
  before=page.evaluate('({x:B.x,y:B.y,nodes:B._s4war.shield.nodes.map(n=>({x:n.x,y:n.y}))})')
  frames(60)
  check(page.evaluate('shake>1&&BOF_CHIP_PASS.stats.gd_tankEngineLoop>0'),'Sovereign windup produces shake and the approved engine cue')
  snap('sovereign-charge-warning')
  frames(40)
  q=page.evaluate('({x:B.x,y:B.y,nodes:B._s4war.shield.nodes.map(n=>({x:n.x,y:n.y})),targets:retinaBossTargets(B).filter(t=>t.part).map(t=>({x:t.x,y:t.y}))})')
  delta=(q['x']-before['x'],q['y']-before['y'])
  check(abs(delta[1])>10 and all(abs(q['nodes'][i]['x']-before['nodes'][i]['x']-delta[0])<.01 and abs(q['nodes'][i]['y']-before['nodes'][i]['y']-delta[1])<.01 for i in range(4)),
   'All four generator graphics/targets translate with the charging hull',q)
  check(page.evaluate('B._s4war.shield.nodes.every(n=>bossHitTest(n.x,n.y)&&B._s4ShieldHit===n)'), 'Native point damage still addresses every moving generator')
  snap('sovereign-moving-cores')

  setup(4,'stormsovereign')
  page.evaluate('()=>{player.y=PLAY.y+PLAY.h*.34;B._sa14.lockCd=0;}');frames(62)
  check(page.evaluate('B._er26.mode==="sa14-lock"&&SA14.events.filter(q=>q.event==="lock-beep").length>=5'),'Crossing mid-screen starts orbiting Retina and repeated lock beeps')
  snap('sovereign-retina-tracking')
  page.evaluate('player.y=VH-90');frames(2)
  check(page.evaluate('B._er26.mode==="recover"&&!eBullets.some(q=>q._sa14Missile)&&SA14.events.some(q=>q.event==="lock-cancel")'),'Retreating south before lock cancels the missile trap')
  page.evaluate('()=>{player.y=PLAY.y+PLAY.h*.32;B._sa14.lockCd=0;}');frames(118)
  check(page.evaluate('SA14.events.some(q=>q.event==="retina-lock")&&eBullets.some(q=>q._sa14Missile)'), 'Remaining north commits the lock and releases the missile volley')
  page.evaluate('player.y=VH-90');snap('sovereign-locked-missiles')
  page.evaluate('''()=>{player.x=camRightX()-70;window.testMissile=eBullets.find(q=>q._sa14Missile&&!q.dead);testMissile.x=camLeftX()+70;testMissile.y=VH-65;testMissile.vx=testMissile.vy=0;
   pBullets=[{kind:'mg',x:testMissile.x,y:testMissile.y,vx:0,vy:0,w:8,h:12,dmg:5,t:0}];}''');frames(1)
  check(page.evaluate('testMissile.dead'), 'A real player MG bullet intercepts a locked volley missile')

  setup(4,'stormsovereign')
  page.evaluate('()=>{er26Set(B,"sa14-storm");B._er26.t=B._er26.warm*.88;er26Tick(B,0);}')
  snap('sovereign-lightning-charge')
  frames(30)
  check(page.evaluate('eBullets.filter(q=>q._sa14Electric).every(q=>q._weaponProof&&!q._shootable&&!enemyOrdnanceCanIntercept(q))&&eBullets.some(q=>q._sa14Electric)'), 'Electrical volleys remain unshootable through the shared ordnance policy')
  page.evaluate('''()=>{player.x=camRightX()-70;window.testElectric=eBullets.find(q=>q._sa14Electric&&!q.dead);testElectric.x=camLeftX()+70;testElectric.y=VH-65;testElectric.vx=testElectric.vy=0;
   pBullets=[{kind:'mg',x:testElectric.x,y:testElectric.y,vx:0,vy:0,w:8,h:12,dmg:999,t:0}];}''');frames(1)
  check(page.evaluate('!testElectric.dead'), 'Actual ordinary MG fire cannot erase a lightning ball')

  setup(4,'stormsovereign')
  page.evaluate('()=>{er26Set(B,"sa14-overflight");player.y=VH-85;}');frames(200)
  q=page.evaluate('({depth:B._sa14.depth,scale:B._sa14.scale,angle:B._sa14.angle,safe:B._noHit,air:B._s4Airborne})')
  check(q['depth'] and q['scale']>1.6 and q['safe'] and q['air'], 'South exit returns north above the player at a visibly enlarged safe depth',q)
  snap('sovereign-overhead-return')
  page.evaluate('()=>{player.x=B.x;player.y=B.y;player.invuln=0;window.beforeLives=run.lives;window.beforeShield=run.shield;}');frames(1)
  check(page.evaluate('!player.dead&&run.lives===beforeLives&&run.shield===beforeShield'), 'Passing beneath the overhead hull cannot kill or damage the player')
  page.evaluate('()=>{player.invuln=1e9;player.y=VH-90;}');frames(120)
  q=page.evaluate('({angle:B._sa14.angle,depth:B._sa14.depth,y:B.y,balls:eBullets.filter(q=>q._sa14Electric).length})')
  check(not q['depth'] and abs(q['angle']-3.141592653589793)<.001 and q['balls']>0,'Boss reaches the player plane flying vertically north and drops rear lightning balls',q)
  snap('sovereign-northbound-chase')
  y=q['y'];frames(36);check(page.evaluate('B.y')<y,'The chase hull keeps travelling north')

  setup(4,'olivewarden',mini=True)
  frames(210)
  check(page.evaluate('enemies.some(e=>e._sa14Escort)&&eBullets.some(q=>q._sa14Slug)'), 'Warden is a rapid machine gunner with genuine south-origin helpers')
  escort=page.evaluate('enemies.filter(e=>e._sa14Escort).map(e=>({y:e.y,scale:e._sa14Escort.scale,hp:e.hp}))')
  check(len(escort)>0 and any(q['scale']>1 for q in escort), 'Helper entry scales down from an enlarged south fly-in',escort)
  snap('warden-south-helpers')
  frames(125)
  check(page.evaluate('eBullets.some(q=>q._sa14EscortShot)&&enemies.some(e=>e._sa14Escort?.shots>0)'), 'Twisting helpers fire real MG projectiles after reaching the combat plane')
  check(page.evaluate('!B._l23Beam&&!eBullets.some(q=>q._beam||q.kind==="beam")'), 'Warden does not fall back to a core laser')
  page.evaluate('()=>{er26Set(B,"sa14-rockets");}');frames(110)
  check(page.evaluate('eBullets.some(q=>q._sa14Missile)'), 'Warden also releases missile-box volleys')
  page.evaluate('()=>{for(const e of enemies)if(e._sa14Escort)e.flash=.2;}');snap('warden-hit-preserves-palette')
  check(page.evaluate('enemies.filter(e=>e._sa14Escort).every(e=>e._air13RenderedKey===AM13_ART.flight_variant_4.heading.key)'), 'Helpers use the authored camo pose bank through native drawImage')

  for kind in ['bowling','crisscross','peel-bomb']:
   setup(4);page.evaluate('k=>{enemies=[];VP12.groups=[];VP12.serial=0;vp12Spawn(k);}',kind)
   check(page.evaluate('VP12.groups.length===1'),kind+' formation spawns through the normal family/health pipeline')
   frames(160);snap('formation-'+kind)
   check(page.evaluate('SA14.events.length>=0&&enemies.filter(e=>e._vp12).every(e=>Number.isFinite(e.x)&&Number.isFinite(e.y)&&!!e._air13RenderedKey)'),kind+' route has finite positions and actual authored aircraft frames')
   if kind=='peel-bomb':check(page.evaluate('VP12.events.some(q=>q.type==="peel-bomb"&&q.event==="bomb-drop")'),'Individual peel-offs release actual falling bombs')

  browser.close()
except Exception as exc:
 errors.append(str(exc));print(traceback.format_exc(),flush=True)
finally:
 stop()
 report={'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'checks':checks,'errors':errors,'scenes':scenes,
  'scope':'Controlled native combat, progression and render fixtures; synthetic haptics capability, not full human campaign or hardware play.'}
 (OUT/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 (ROOT/'docs/qa/stage34_assault_1014.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps({'passed':report['passed'],'failed':report['failed'],'errors':errors}),flush=True)
if report['failed'] or errors:sys.exit(1)
