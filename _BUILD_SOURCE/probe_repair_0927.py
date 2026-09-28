"""Native Chromium checks for held locks, scrolling and the actual Stage 6 sequence."""
import ast,base64,http.server,json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(sh.GAME)
OUT=Path(sh.GAME)/'_shots/repair_0927';OUT.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(str(ROOT));errors=[];report={}
RESET="""stage=>{diffKey='furious';DIFF=DIFFS[diffKey];run.mode='arcade';run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');run.stage=stage;beginStage(stage);setState(GS.PLAY);player.reset();player.invuln=99999;story=null;stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=false;stageTimer=0;run.bombs=30;run.retinaScan=true;retinaScanClear();retina.target=null;retina.phase=null;player.x=worldWidth()/2;player.y=VH*.8;for(const k of Object.keys(Input.keys))Input.keys[k]=false;}"""
def shot(p,name):
 p.evaluate('()=>{const inv=player.invuln;player.invuln=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);if(run.stage===6)s6WingChoiceDraw();player.invuln=inv;}')
 (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport={'width':1100,'height':1200});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  report['locks']=[]
  for stage in range(1,10):
   p.evaluate(RESET,stage)
   report['locks'].append(p.evaluate("""()=>{
    const a=spawnEnemy('s6dart',player.x+90,180,{}),closer=spawnEnemy('s6dart',player.x,270,{});
    retina.target=a;retina.phase='locked';retina.lockT=5;retina.holdCd=0;retina.x=a.x;retina.y=a.y;
    Input.keys.c=true;Input.keys.k=true;const start=run.bombs;
    for(let f=0;f<180;f++){retinaScanInput(1/60);retinaScanTick(1/60);updateRetina(1/60);}
    const selected=retina.target===a,spent=start-run.bombs,targets=pBullets.filter(q=>q.target||q._target).map(q=>q.target||q._target);
    retinaScanDirection(0,-1);const scan=player._retinaScan;
    for(let f=0;f<420;f++){retinaScanTick(1/60);retinaScanHeldFire();}
    return{stage:run.stage,selected,spent,marks:scan.marks.length,retained:scan.marks.some(m=>m.target===a),ammo:run.bombs};
   }"""))
  p.evaluate(RESET,6)
  p.wait_for_function("()=>XART.rdy('ship_yuri')")
  report['carrier']=p.evaluate("""()=>{s6OpeningInit();s6Opening.phase='flyover';s6Opening.t=2.05;s6OpeningTick(1/60);const j=s6Opening.carrierJets[0],y=j.y;s6OpeningTick(.1);return{launched:s6Opening.carrierLaunchN,deltaY:j.y-y,sizeStart:28,sizeEnd:61};}""")
  p.wait_for_function("()=>['whv_open','whv_closed','whv_fan','whv_ace'].every(k=>XART.rdy(k))");shot(p,'carrier-north')
  p.evaluate("()=>{s6Opening=null;s6WingInit();s6Wing.all=true;s6Wing.beats=2;stageTimer=70;subBossDone=true;s6Wing.postMiniT=4;s6WingTick(1/60);}")
  p.wait_for_function("()=>['warn_escape_arrow_0916',...REBEL_SHIPS.map(k=>'rr_ship_'+k)].every(k=>XART.rdy(k))")
  p.evaluate('()=>{s6Wing.fake.t=2.9;}');shot(p,'split-flyover')
  report['route']=p.evaluate("""()=>{s6Wing.fake.t=5.99;s6WingTick(.02);const choice=s6Wing.choice,spawned=bossActive;s6Wing.choiceT=29.99;s6WingTick(.02);return{choice,spawned,route:s6Wing.route,fakeDone:s6Wing.fakeDone};}""")
  p.evaluate("()=>{s6Wing.route=null;s6Wing.choiceT=4;}");shot(p,'route-arrows')
  p.evaluate(RESET,6);p.evaluate("()=>{s6Opening=null;s6Wing=null;for(const [i,t]of ['s6dart','s6bomber','s6lancer'].entries())spawnEnemy(t,camLeftX()+100+i*150,220,{});}")
  p.wait_for_function("()=>['s6atk_storm_dart_0','s6atk_four_engine_bomber_0','s6atk_cloud_lancer_0'].every(k=>XART.rdy(k))");shot(p,'new-fleet')
  p.evaluate(RESET,4);p.wait_for_function('()=>XART.rdy(stageMasterKey(_levelCfg()))')
  report['scroll']=p.evaluate("""()=>{mapScroll=1000;_bossHold=0;const x=player.x,y=player.y,z=viewZoom(),c=camX;spawnEnemy('s6dart',player.x,190,{});const e=enemies[0];killEnemy(e);drawWorld(1/60);const first={x:player.x-x,y:player.y-y,zoom:viewZoom()-z,scroll:mapScroll-1000};_bossHold=1;mapScroll=1500;drawWorld(1/60);return{kill:first,releaseDelta:mapScroll-1500};}""");shot(p,'stage4-scroll')
  report['hammer']=[]
  for diff in ['normal','hard','furious']:
   p.evaluate(RESET,5)
   report['hammer'].append(p.evaluate("""d=>{diffKey=d;DIFF=DIFFS[d];spawnBoss('chromehammer');boss._noHit=false;boss.enter=false;boss.y=VH*.34;const h=boss._hammer;hammerState(boss,'hammer');hammerBossTick(boss,1/60);const hp=boss.maxhp;boss.hp=hp*.45;h.ballSeen=true;hammerBossTick(boss,1/60);const whirlwind=h.whirlSeen&&h.state==='whirl_warn';h.arsenalStep=1;h.mode='chaingun';hammerArsenalNext(boss);const start=boss.hp;for(let i=0;i<480;i++)hammerBossTick(boss,1/60);return{diff:d,hp,whirlwind,restoration:h.restorationSeen,healed:boss.hp-start,status:h.recovery?.status};}""",diff))
  p.wait_for_function("()=>XART.rdy('arch_storm_charge_0926')");shot(p,'hammer-restoration')
  report['whirlCounter']=p.evaluate("""()=>{const h=boss._hammer;h.mode='hammer';hammerWhirlStart(boss);hammerState(boss,'whirlwind');boss._noHit=false;_dmgBullet=null;for(let i=0;i<10;i++){h.whirlHitCd=0;boss._hammerModuleHit=null;hammerBossDamage(boss,10);}const bodySafe=h.state==='whirlwind';for(let i=0;i<8;i++){h.whirlHitCd=0;boss._hammerModuleHit='hammer';hammerBossDamage(boss,1);}return{bodySafe,hammerStagger:h.state==='hammer_stun'};}""")
  report['music']=p.evaluate('()=>({mini2:BOFA.music.mini2,mini3:BOFA.music.mini3})')
  report['audio']=p.evaluate("""async()=>{const a=new AudioContext(),out=[];try{for(const key of ['mini2','mini3']){const response=await fetch(BOFA.music[key]);const decoded=await a.decodeAudioData(await response.arrayBuffer());out.push({key,seconds:decoded.duration,channels:decoded.numberOfChannels});}}finally{await a.close();}return out;}""")
  p.evaluate(RESET,1)
  report['emptyAmmo']=p.evaluate("""()=>{const target=spawnEnemy('s6dart',player.x,180,{});retinaScanAdd(target);Input.keys.c=Input.keys.k=true;for(let i=0;i<30;i++)retinaScanTick(1/60);run.bombs=0;let sounds=0;const hit=Audio.SFX.hit;Audio.SFX.hit=()=>sounds++;try{for(let i=0;i<180;i++){retinaScanTick(1/60);retinaScanHeldFire();}}finally{Audio.SFX.hit=hit;}return{sounds,targetRetained:player._retinaScan.marks.some(m=>m.target===target)};}""")
  report['errors']=errors;(OUT/('release-probe.json' if len(sys.argv)>1 else 'probe.json')).write_text(json.dumps(report,indent=2),encoding='utf-8');b.close()
finally:stop()
print(json.dumps(report,indent=2))
assert not errors,errors
assert all(r['selected'] and r['spent']>=3 and r['retained'] for r in report['locks'])
assert report['carrier']['deltaY']<0
assert report['route']['choice'] and not report['route']['spawned'] and report['route']['route']
assert report['scroll']['kill']['x']==report['scroll']['kill']['y']==report['scroll']['kill']['zoom']==0
assert 0<report['scroll']['releaseDelta']<.1
assert all(r['whirlwind'] and r['healed']>0 and r['status']=='complete' for r in report['hammer'])
assert report['whirlCounter']['bodySafe'] and report['whirlCounter']['hammerStagger']
assert all(r['seconds']>30 for r in report['audio'])
assert 1<=report['emptyAmmo']['sounds']<=10 and report['emptyAmmo']['targetRetained']
