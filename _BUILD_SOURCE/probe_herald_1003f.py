"""Native modular Herald, real stage scheduler, collision, live attacks and defeat."""
from pathlib import Path
import base64,json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/herald_1003f';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[]};errors=[]
def ck(v,name):
 report['checks'].append({'ok':bool(v),'name':name});print(('OK ' if v else 'FAIL ')+name,flush=True)
def frames(p,n):
 for i in range(0,n,12):p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(12,n-i));p.wait_for_timeout(8)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.add_init_script('(()=>{const draw=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(){if(window.hdKey&&typeof ctx!=="undefined"&&this===ctx)hdDraws.push(hdKey);return draw.apply(this,arguments);};})()')
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate(SETUP,{'stage':8,'diff':'furious'})
  p.evaluate('''()=>{window.hdKey=null;window.hdDraws=[];window.hdSounds={};const blit=hd1003Blit,ret=groundTargetReticleDraw,fov=l23FovDraw;
   hd1003Blit=function(p){hdKey='part-'+p.id;try{return blit.apply(this,arguments);}finally{hdKey=null;}};
   l23FovDraw=function(){hdKey='original-fov';try{return fov.apply(this,arguments);}finally{hdKey=null;}};
   groundTargetReticleDraw=function(){hdKey='original-retina';try{return ret.apply(this,arguments);}finally{hdKey=null;}};
   const sound=r30Sound;r30Sound=function(k){hdSounds[k]=(hdSounds[k]||0)+1;return sound.apply(this,arguments);};
  }''')
  p.wait_for_function('()=>XART.rdy(HD1003_ART.key)&&["hammer_reticle","bmfx_fov_red_tall",...Object.values(S81003_ART).map(a=>a.key)].every(k=>XART.rdy(k))',timeout=120000,polling=60)
  for diff in ['easy','normal','hard','furious']:
   p.evaluate(SETUP,{'stage':8,'diff':diff})
   # Approach the real half-stage gate; do not call spawnSubBoss for this check.
   p.evaluate('()=>{stageTimer=curStage.length*SUBBOSS[8].at-.03;mapScroll=SUBBOSS[8].afterScroll+1;window.hdSpawnCount=0;const spawn=spawnSubBoss;window.hdRestoreSpawn=spawn;spawnSubBoss=function(k){if(k==="heralddeath")hdSpawnCount++;return spawn.apply(this,arguments);};}')
   frames(p,370)
   q=p.evaluate('()=>({spawn:hdSpawnCount,mini:subBoss?._ship,active:subBossActive,entered:!subBoss?.enter,rig:subBoss?._hd1003?.parts.length,hp:subBoss?.hp,maxhp:subBoss?.maxhp,boss:!!boss,trigger:subBossTriggered,done:subBossDone})');report[diff]=q
   ck(q['spawn']==1 and q['mini']=='heralddeath' and q['active'] and q['entered'] and q['rig']==6 and not q['boss'],diff+' real halfway scheduler spawns exactly one modular Herald')
   p.evaluate('()=>{spawnSubBoss=hdRestoreSpawn;window.B=subBoss;window.hdHeldScroll=mapScroll;window.hdHeldTime=stageTimer;window.hdPeakShots=0;window.hdPeakBeams=0;}')
   captured=set()
   for j in range(130):
    frames(p,6)
    q=p.evaluate('()=>{hdPeakShots=Math.max(hdPeakShots,eBullets.filter(q=>q._heraldOwner1003===B).length);hdPeakBeams=Math.max(hdPeakBeams,S81003.beams.filter(q=>q.owner===B).length);return {mode:B._hd1003.mode,attack:B._hd1003.attack,age:B._hd1003.age};}')
    name=q.get('attack','')+'-'+q['mode']
    if diff=='furious' and name not in captured and q['mode'] in ['tell','fire'] and q['age']>.12:shot(p,name);captured.add(name)
   q=p.evaluate('()=>({history:B._hd1003.history,shots:hdPeakShots,beams:hdPeakBeams,scroll:mapScroll-hdHeldScroll,time:stageTimer-hdHeldTime,keys:[...new Set(hdDraws)]})');report[diff]['combat']=q
   ck(q['shots']>0 and ('skulls' in q['history']) and ('salvo' in q['history']) and (diff=='easy' or q['beams']>0),diff+' Herald releases skull volleys and its difficulty-appropriate attacks')
   # Stage 8's flying backdrop intentionally scrolls; the wave clock is held.
   ck(abs(q['time'])<.1,diff+' miniboss fight holds the stage wave clock')
  ck(p.evaluate('()=>HD1003_ART.key in XART._src&&["core","head","wingL","wingR","gunL","gunR"].every(id=>hdDraws.includes("part-"+id))'),'all six generated components actually draw on the game context')
  ck(p.evaluate('()=>hdDraws.includes("original-fov")&&hdDraws.includes("original-retina")'),'Herald uses original FOV and original Retina pixels')
  p.evaluate('''()=>{window.hdRealHit=playerHit;window.hdContactHits=0;playerHit=()=>{hdContactHits++;};
   B._hd1003.mode='rest';B._hd1003.age=-10;eBullets=[];S81003.beams=[];groundTargetingReset();powerups=[];enemies=[];
   window.hdGap=null;for(let y=B.y+35;y<B.y+100&&!hdGap;y+=5)for(let x=B.x-140;x<B.x+140;x+=5)if(!hd1003At(B,x,y)){hdGap={x,y};break;}
   player.x=hdGap.x;player.y=hdGap.y;player.invuln=0;player.rollT=0;player.saltT=0;
  }''');frames(p,1)
  ck(p.evaluate('()=>hdContactHits===0'),'empty space between modular parts does not damage the pilot')
  p.evaluate('()=>{const q=hd1003Center(B,hd1003Part(B,"core"));player.x=q.x;player.y=q.y;hdContactHits=0;}');frames(p,1)
  ck(p.evaluate('()=>hdContactHits>0'),'touching the visible core still damages the pilot')
  p.evaluate('()=>{playerHit=hdRealHit;player.x=worldWidth()/2;player.y=VH-110;player.invuln=1e9;}')
  p.evaluate('()=>{B._hd1003.mode="rest";B._hd1003.age=0;B._hd1003.clock=0;window.hdPoseBefore=hd1003Pose(B,hd1003Part(B,"wingL"));}');frames(p,24)
  ck(p.evaluate('()=>Math.abs(hd1003Pose(B,hd1003Part(B,"wingL")).a-hdPoseBefore.a)>.01'),'wing animates independently of the upright body')
  p.evaluate('()=>{window.hdGun=hd1003Part(B,"gunL");window.hdTarget=retinaBossTargets(B).find(q=>q._retinaId==="herald-gunL");window.hdHP=hdGun.hp;run.bombs=20;run.missileTier="standard";window.hdLaunched=useBomb(hdTarget);}')
  frames(p,150)
  ck(p.evaluate('()=>hdLaunched&&hdGun.hp<hdHP'),'an actual curved Retina missile damages the moving cannon')
  p.evaluate('()=>{const q=hd1003Center(B,hd1003Part(B,"gunR"));window.hdOtherGunHP=hd1003Part(B,"gunR").hp;pBullets.push({kind:"mg",x:q.x,y:q.y,vx:0,vy:0,w:5,h:12,dmg:10,t:0});}');frames(p,2)
  ck(p.evaluate('()=>hd1003Part(B,"gunR").hp<hdOtherGunHP'),'ordinary shots route into the cannon they visibly hit');shot(p,'cannon-hit')
  p.evaluate('()=>{retinaMissileDamage(hdTarget,hdGun.hp+1,{kind:"gmiss"});window.hdLost=hd1003Center(B,hdGun);B._hd1003.seq=0;hd1003Tell(B);hdDraws=[];}');shot(p,'cannon-broken')
  ck(p.evaluate('()=>hdGun.dead&&!retinaBossTargets(B).includes(hdTarget)&&!B._hd1003.lanes.some(q=>q.id==="gunL")'),'destroyed cannon detaches, loses its Retina lock and stops firing')
  p.evaluate('()=>{window.hdWing=hd1003Part(B,"wingL");window.hdWingTarget=retinaBossTargets(B).find(q=>q._retinaId==="herald-wingL");retinaMissileDamage(hdWingTarget,hdWing.hp+1,{kind:"gmiss"});B._hd1003.seq=1;hd1003Tell(B);}')
  ck(p.evaluate('()=>hdWing.dead&&B._hd1003.attack==="lances"&&B._hd1003.lanes.length===1&&B._hd1003.lanes[0].id==="wingR"'),'destroying a wing removes its beam emitter');shot(p,'wing-broken')
  # Head is a core weak point. Body remains killable even with live modules.
  p.evaluate('()=>{window.hdPreWeak=B.hp;const q=hd1003Center(B,hd1003Part(B,"head"));hitSubBoss(10,q.x,q.y);}')
  ck(p.evaluate('()=>Math.abs(hdPreWeak-B.hp-12)<.01'),'separate skull takes weak-point damage')
  p.evaluate('()=>{hitSubBoss(B.hp+1);window.hdBeforeDeathStage=stageTimer;}');frames(p,32);shot(p,'modular-destruction')
  ck(p.evaluate('()=>B.dead&&B._hd1003.deadBeats>0&&B._hd1003.debris.length>0'),'defeat ejects authored components with timed explosion beats')
  frames(p,105)
  ck(p.evaluate('()=>!subBoss&&subBossDone&&!subBossActive&&stageTimer>hdBeforeDeathStage'),'death resolves once and normal stage progression resumes')
  p.evaluate('()=>{stageTimer=curStage.length+.01;enemies=[];warnT=0;warnKind=null;BOFCinematicDirector.cancel();story=null;}');frames(p,200)
  ck(p.evaluate('()=>subBossDone&&!subBoss&&boss?.kind==="vileexistence"&&!!boss._r30.modular1003c'),'restored miniboss leads into the existing eight-form modular finale')
  report['sounds']=p.evaluate('()=>hdSounds');ck(report['sounds'].get('bossWeaponCharge',0)>0 and report['sounds'].get('combatModule0927',0)>0,'native charge and module-break audio cues fire')
  report['errors']=errors;ck(not errors,'no page or console errors')
  (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');br.close()
finally:stop()
print(json.dumps({'checks':len(report['checks']),'failed':[q['name'] for q in report['checks'] if not q['ok']],'errors':errors}))
if errors or any(not q['ok'] for q in report['checks']):raise SystemExit(1)
