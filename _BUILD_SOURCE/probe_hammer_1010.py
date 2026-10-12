"""Native Chromium: real contact/damage, authored frames and timed Hammer clips."""
from pathlib import Path
import sys,json,base64,subprocess
from PIL import Image
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/hammer_1010';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[];videos=[]
def check(name,passed,data=None):
    checks.append({'name':name,'pass':bool(passed),'data':data})
    print(('PASS ' if passed else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status}: '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
  p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(650,450)
  p.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  p.evaluate('()=>hm10Warm()');p.wait_for_function('()=>hm10Ready()',polling=50)
  check('All 96 generated cells decode through native XART',p.evaluate('Object.values(HM10_ART).flat().length===96&&hm10Ready()'))
  def snap(name,gallery=False):
   if not gallery:p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);fb9HudSplit();}')
   q=base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]'))
   (OUT/(name+'.png')).write_bytes(q);shots.append(name+'.png')
  # Verify ordinary keyboard password entry as well as protected combat fixtures.
  p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;setState(GS.PASSWORD);drawPassword.typing=true;pwInput="";diffKey="furious";Input.clearTaps?.();}')
  p.keyboard.type('boss5');p.keyboard.press('Enter');p.evaluate('drawPassword(0)')
  check('BOSS5 keyboard entry retains normal difficulty selection',p.evaluate('state===GS.DIFF&&PENDING_STAGE===5&&ON5.pending?.role==="boss"'))
  p.evaluate('()=>{pilotIndex=PILOTS.findIndex(p=>p.key==="yuri");startRun(PENDING_STAGE);}')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(5).ready&&boss?._hammer?.hm10&&hm10Ready();}',polling=50)
  check('BOSS5 loads the regular live encounter with all new assets ready',p.evaluate('state===GS.PLAY&&run.stage===5&&bossActive&&!boss._hammerTime&&!!boss._hammer.hm10'))
  def setup(diff='furious'):
   p.evaluate('(diff)=>BAL7.setup({stage:5,kind:"chromehammer",pilot:"yuri",diff,fire:false,seconds:60})',diff)
   p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(5).ready;}',polling=50)
   p.evaluate('''()=>{BOFCinematicDirector.cancel();story=null;fb2Talk=fb2Intro=null;H3.ending=null;
    B._cin30Spoke=B._fb2IntroSeen=true;B.enter=B.dead=B._noHit=false;B.hp=B.maxhp=6000;
    const h=B._hammer;h.balance0922=h.gp4FailsafeSeen=h._fb2RageDone=h.intro1002=true;h.mode='hammer';
    h.phasePending=false;h.frRecovery=false;h.recovery=null;h.openingJump1003=false;
    h.frArmor={hp:3000,max:3000,t:0,active:true,activated:true,half:true,barrier:0,checkpoints:[.75,.5,.35,.15],rage:false};
    B.x=worldWidth()/2;B.y=180;hammerState(B,'hammer');camX=B.x-VW/2;
    player.dead=player.out=false;player.alive=true;player.invuln=999;player.x=B.x;player.y=PLAY.y+PLAY.h-60;
    player.roll=player.somer=player._spin=player._voidDeath=null;run.shield=0;shake=whiteBlast=0;
    enemies=[];eBullets=[];pBullets=[];powerups=[];l5Rocks=[];l5RockT=9999;HM10.events=[];}''')
  # Use the game's own canvas and drawImage with XART.get, never .src identity.
  original=p.evaluate('({w:cv.width,h:cv.height})')
  for name in ['shield_form','swing_right','swing_left','shield_wall','core','spike']:
   stats=p.evaluate('''(name)=>{cv.width=1280;cv.height=1280;ctx.setTransform(1,0,0,1,0,0);
    ctx.fillStyle='#101824';ctx.fillRect(0,0,cv.width,cv.height);const out=[];
    HM10_ART[name].forEach((a,i)=>{const col=i%4,row=i>>2,k=name==='spike'?.55:name==='core'?.65:.65;
     hm10Blit(name,i,col*320+160,row*320+(name==='spike'?285:name==='shield_wall'?160:142),k);
     const d=ctx.getImageData(col*320,row*320,320,320).data;let pixels=0;
     for(let j=0;j<d.length;j+=4)if(d[j+2]>d[j+0]+30||d[j+0]>80)pixels++;
     out.push({key:a.key,pixels,w:a.w,h:a.h});});return out;}''',name)
   snap('native-'+name,True)
   for q in stats:check(q['key']+' paints authored pixels on native canvas',q['pixels']>80 and q['w']%2==q['h']%2==0,q['pixels'])
  p.evaluate('(q)=>{cv.width=q.w;cv.height=q.h;ctx.setTransform(SS,0,0,SS,0,0);}',original)
  setup()
  # Real updatePlay body contact: same X/Y, different apparent depths.
  for state,t,expect in [('giant_warn',.4,False),('giant_dive',.10,False),('giant_dive',.26,False),('giant_dive',.30,True),('giant_sweep',.35,True)]:
   setup()
   q=p.evaluate('''({state,t})=>{const h=B._hammer;hammerState(B,state);h.t=t;B._noHit=false;
    B.y=200;h.giantFromX=h.tx=B.x;h.giantFromY=h.ty=B.y;
    player.x=B.x;player.y=B.y;player.invuln=0;run.shield=0;
    const scale=hammerDepthScale(B),targetable=bossHitTest(B.x,B.y);updatePlay(.000001);
    return{dead:player.dead,scale,targetable,state:h.state};}''',{'state':state,'t':t})
   check(f'{state} {t}s real body contact matches visible plane',q['dead']==expect,q)
   snap(f'depth-{state}-{str(t).replace(".","-" )}')
  for diff in ['easy','normal','hard','furious']:
   for kind in ['mg','laser','gmiss','retinaMissile']:
    setup(diff)
    q=p.evaluate('''(kind)=>{const h=B._hammer;hammerState(B,'giant_dive');h.t=.20;h.giantLeft=1;
     h.giantFromX=B.x;h.giantFromY=B.y;h.tx=B.x;h.ty=310;B._noHit=false;
     const shot={kind,x:B.x,y:B.y,vx:0,vy:-9,dmg:12,_hit:[]},a0=h.frArmor.hp;
     const reflected=hammerDiveReflect(B,shot);_dmgBullet=shot;_lastHitX=B.x;_lastHitY=B.y;B._hammerModuleHit=null;hitBoss(12);_dmgBullet=null;
     const committed=h.state==='giant_dive';for(let i=0;i<40&&h.state==='giant_dive';i++)hammerBossTick(B,1/60);
     return{reflected,vy:shot.vy,enemy:shot._enemyReflected||0,committed,landed:h.state==='giant_sweep',armorDamage:a0-h.frArmor.hp};}''',kind)
    check(diff+' '+kind+' damages armor and preserves orbital strike',not q['reflected'] and q['vy']==-9 and q['enemy']==0 and q['committed'] and q['landed'] and q['armorDamage']>0,q)
  setup('furious')
  q=p.evaluate('''()=>{const h=B._hammer,A=h.frArmor;A.barrier=6;h.recovery={status:'charging'};
   hammerState(B,'storm_raise');const head=hammerHeadPoint(B),y=B.y+85;
   const lane={kind:'mg',x:head.x,y,vx:0,vy:-9},body={kind:'mg',x:B.x+(head.x>B.x?-95:95),y,vx:0,vy:-9};
   pBullets=[lane,body];eBullets=[];fr27Reflect(B,A,1/60);
   return{lane:!lane.dead,body:!!body.dead,enemy:eBullets.length,flash:A.flash,hits:hm10Data(B).hits.length};}''')
  check('Chromium absorbs body fire without emitting hostile copies; hammer lane remains open',q['lane'] and q['body'] and q['enemy']==0 and q['flash']>0 and q['hits']==1,q)
  setup()
  q=p.evaluate('''()=>{const h=B._hammer;hammerState(B,'warn');h.t=.25;hammerTarget(B);h.hammerHP=1;
   B._hammerModuleHit='hammer';_dmgBullet={kind:'mg'};hitBoss(5);_dmgBullet=null;
   const deferred=h.hm10BreakPending&&h.state==='warn'&&!h.hammerDestroyed;
   for(let i=0;i<120&&h.state!=='hammer_exposed';i++)hammerBossTick(B,1/60);
   return{deferred,state:h.state,destroyed:h.hammerDestroyed,impact:h.leapFx>0};}''')
  check('Weapon depletion waits for the actual jump impact before breaking',q['deferred'] and q['state']=='hammer_exposed' and q['destroyed'] and q['impact'],q)
  setup()
  q=p.evaluate('''()=>{const h=B._hammer;h.gp4FailsafeSeen=false;h.frArmor.hp=0;B.hp=B.maxhp*.08;
   hammerState(B,'giant_dive');h.t=.20;h.giantFromX=h.tx=B.x;h.giantFromY=B.y;h.ty=310;h.giantLeft=1;
   hammerBossTick(B,.1);const deferred=h.state==='giant_dive'&&!h.gp4Emergency;
   for(let i=0;i<100&&!h.gp4Emergency;i++)hammerBossTick(B,1/60);
   const started=!!h.gp4Emergency;for(let i=0;i<185&&h.gp4Emergency;i++)hammerBossTick(B,1/60);
   return{deferred,started,ratio:B.hp/B.maxhp,state:h.state};}''')
  check('8% emergency reserve follows the committed impact and still restores 38%',q['deferred'] and q['started'] and abs(q['ratio']-.38)<.001,q)
  setup()
  q=p.evaluate('''()=>{const A=B._hammer.frArmor,Q=hm10Data(B);A.barrier=.02;Q.wallOn=true;Q.wallAge=1;
   const painted=[],old=hm10Blit;hm10Blit=function(name,f){painted.push({name,f});return old.apply(this,arguments);};
   try{hammerBossTick(B,.03);hammerBossDraw(B);return{broken:!Q.wallOn&&Q.wallBreak===0,painted};}finally{hm10Blit=old;}}''')
  check('Wall expiration renders the authored shatter without retaining an invisible shield',q['broken'] and any(v['name']=='shield_wall' and v['f']==12 for v in q['painted']),q)
  snap('chromium-wall-shatter')
  setup()
  q=p.evaluate('''()=>{const frames=[],old=hm10Blit;hm10Blit=function(name,f){if(name==='core')frames.push(f);return old.apply(this,arguments);};
   B.flash=.15;try{hammerBossDraw(B);hammerBossTick(B,.08);hammerBossDraw(B);return{frames,stillFlashing:B.flash>0};}finally{hm10Blit=old;}}''')
  check('Generated reactor advances independently while the body is hit flashing',q['stillFlashing'] and len(set(q['frames']))>1,q)
  snap('chromium-hit-core')
  for side in [-1,1]:
   setup()
   q=p.evaluate('''(side)=>{const h=B._hammer;h.mode='storm';h.stormWaves=[];hammerState(B,'storm_split');
    const C=h.bm9Counter={side,t:.8,tell:1.35,ox:B.x,oy:B.y,tx:B.x,ty:B.y},L=hm10CounterLane(B,C);
    return{width:L.width,contains:[7,8,9,10,11].every(f=>{const p=hm10CounterPoint(B,C,f);return s81003Distance(p.x,p.y,L)+19<=L.width/2+1e-8;})};}''',side)
   check('Side '+str(side)+' warning covers the complete generated hammer arc',q['contains'],q)
   snap('swing-warning-'+str(side))
  def clip(name,seconds,setup_js):
   setup();p.evaluate(setup_js);folder=OUT/name;folder.mkdir(exist_ok=True)
   for i in range(round(seconds*15)):
    p.evaluate('()=>{for(let n=0;n<4;n++)updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);fb9HudSplit();}')
    (folder/f'{i:04d}.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
    p.wait_for_timeout(5)
   ff=imageio_ffmpeg.get_ffmpeg_exe()
   subprocess.run([ff,'-v','error','-y','-framerate','15','-i',str(folder/'%04d.png'),'-c:v','libx264','-crf','19','-pix_fmt','yuv420p',str(OUT/(name+'.mp4'))],check=True)
   videos.append(name+'.mp4')
  clip('chromium-formation',3.65,'()=>{B._hammer.frArmor=null;fr27BeginArmor(B);}')
  for side in [1,-1]:
   clip('swing-'+('right' if side>0 else 'left'),2.8,'()=>{const h=B._hammer;h.mode="storm";h.stormWaves=[];h.stormHome={x:B.x,y:B.y};hammerState(B,"storm_split");h.bm9Counter={side:'+str(side)+',t:0,tell:1.35,ox:B.x,oy:B.y,tx:B.x,ty:B.y};}')
  clip('orbital-strike',5.4,'()=>{B._hammer.giantLeft=1;hammerState(B,"giant_idle");player.x=B.x+110;}')
  clip('chromium-spikes',1.55,'()=>{const h=B._hammer;h.mode="storm";h.stormWaves=[{x:B.x,y:hammerStormFloorY(),height:180,radius:9,t:0,split:0,delay:0,warm:0,active:2,riseRate:1}];h.stormHome={x:B.x,y:B.y};h.bm9CounterDone=true;hammerState(B,"storm_split");}')
  check('Runtime painted formation/core/left/right/wall/spike banks',p.evaluate('Object.keys(HM10_ART).every(k=>HM10.draws[k]>0)'),p.evaluate('HM10.draws'))
  check('No page, console or asset errors',not errors,errors)
  br.close()
finally:stop()
report={'checks':checks,'errors':errors,'screenshots':shots,'videos':videos,'pass':sum(c['pass'] for c in checks),'fail':sum(not c['pass'] for c in checks)}
(OUT/'report.json').write_text(json.dumps(report,indent=2))
html='<!doctype html><meta charset="utf-8"><title>Hammer 1010</title><style>body{background:#07101c;color:white;font:16px system-ui;max-width:1200px;margin:28px auto}img{max-width:100%;image-rendering:pixelated}video{width:48%;max-height:640px}a{color:#8fdcff}</style><h1>Hammer — committed strikes and authored Chromium</h1><p>96 generated frames; native engine capture. Use BOSS5 for the regular fight.</p>'
html+=''.join('<video controls loop src="'+v+'"></video>' for v in videos)
html+=''.join('<p>'+s+'</p><img src="'+s+'">' for s in shots if s.startswith('native-'))
(OUT/'review.html').write_text(html,encoding='utf-8')
print(json.dumps({'pass':report['pass'],'fail':report['fail'],'errors':errors},indent=2))
if report['fail']:raise SystemExit(1)
