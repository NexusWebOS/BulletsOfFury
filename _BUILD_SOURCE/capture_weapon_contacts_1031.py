"""Short audible native-collision fixture, not a campaign fight. The authored
high-HP target is pinned for legible contacts; native weapons/damage/draw run live."""
from pathlib import Path
import sys,json,base64,time,subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
from rough_riders_capture_base_1028 import CAPTURE
W=R/'_shots/weapon_contacts_1031';W.mkdir(exist_ok=True)
port,stop=serve(str(R));errors=[]
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof WC1031!=="undefined"',timeout=180000);p.mouse.click(3,3)
  p.evaluate("()=>{run.stage=1;stageLoadBegin(1)}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&Object.values(WC1031_ART).every(a=>XART.rdy(a.key))}',timeout=180000)
  # Reuse only the shared audio tap/real canvas capture, replacing the fight bot.
  script=CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.32')
  a=script.index(' function aim(elapsed){');b=script.index(' function render(){',a)
  script=script[:a]+r''' function aim(elapsed){
   const phase=Math.min(5,Math.floor(elapsed/4.5)),time=elapsed-phase*4.5;
   if(window.fxPhase!==phase){fxPhase=phase;pBullets.length=0;pImpacts.length=0;efxBursts.length=0;fb10Clouds=[];
    WC1031.gates=new WeakMap();run.pilot=phase>=3?'maverick':'cole';run.weapon=phase===1?3:phase===2?5:0;run.wlevel=phase===0?1:2;run.infusion=null;run.forge={};run.wvars={3:'laserbeam',5:'iceorb'};window.nextShot=0;}
   if(window.T&&!T.dead){T.x=targetHome.x;T.y=targetHome.y;T.vx=T.vy=0;}
   for(const k of ['a','d','w','s','j','c'])Input.keys[k]=false;
   player.x=targetHome.x;player.y=VH-70;player.invuln=1e9;
   if(time>=nextShot){nextShot=time+(phase===5?8:phase===2?1.2:.85);
    if(phase<3)pShoot();
    else if(phase===3)maverickLaserVolley(2,2,2);
    else releaseHelix(phase===4?.45:1);
   }
   const names=['MACHINE GUN / metal puff + bullet marks','LASER / contact flare + cooling singe','ICE ORB / elemental splash + residue','MAVERICK LASERS / matching energy contact','HELIX LANCE / green energy contact','HELIX BALL / purple-blue release + native volley'];
   cfg.name=names[phase];
 }''' + script[b:]
  script=script.replace("cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s'","cfg.name+' / NATIVE COLLISION FIXTURE / '+elapsed.toFixed(1)+'s'")
  a=script.index(" diffKey='furious';debugUnlocked=true;");b=script.index(' return {entry,difficulty:',a)
  script=script[:a]+r''' debugUnlocked=true;diffKey='furious';
   debugStartFight(debugFightFor(1,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(1,'boss').kind);debugFight.spawned=true;
   boss=null;bossActive=false;subBoss=null;subBossActive=false;debugFight=null;run.mode='campaign';warnT=0;DBGT.god=true;BOFCinematicDirector.cancel();setState(GS.PLAY);
   enemies.length=0;eBullets.length=0;pBullets.length=0;player.x=worldWidth()/2;player.y=VH-70;
   window.T=spawnEnemy('s1tankheavy',player.x,player.y-190,{});
   Object.assign(T,{hp:1e7,maxhp:1e7,pattern:'__dummy',shoots:false,fk:null,vx:0,vy:0,_noSep:true,t:0});T._esh=null;
   window.targetHome={x:T.x,y:T.y};window.fxPhase=-1;
   const entry={stage:1,role:'fixture',kind:'weapon contacts'};
   Audio.startMusic('stage1');
''' + script[b:]
  with (W/'contacts-native.webm').open('wb')as raw:
   p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)))
   p.evaluate(script,dict(name='WEAPON CONTACTS',stage=1,role='fixture',kind='weapon contacts'))
   events=[]
   while p.evaluate('(performance.now()-captureStart)/1000')<27:
    p.wait_for_timeout(450);q=p.evaluate('({at:(performance.now()-captureStart)/1000,phase:fxPhase,hp:T.hp,frames:__bofFrames,fx:WC1031.events.slice(-3),draws:{...WC1031.draws}})');events.append(q)
    if q['at']>2 and not (W/('phase-'+str(q['phase'])+'.png')).exists():p.screenshot(path=str(W/('phase-'+str(q['phase'])+'.png')))
    if errors:break
   report=p.evaluate("async()=>{for(const k of ['j','c'])Input.keys[k]=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return{...captureStats,draws:WC1031.draws,events:WC1031.events,hp:T.hp};}")
   report.update(errors=errors,method='Native weapon launch functions, real RAF/updatePlay/drawImage/shared mixer. One pinned high-HP authored target for contact readability; not a campaign fight or balance run.',timeline=events)
   (W/'capture-report.json').write_text(json.dumps(report,indent=2));print('RECORDED',report['frames'],'errors',errors,flush=True)
  br.close()
finally:stop()
ff=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff,'-y','-i',str(W/'contacts-native.webm'),'-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(W/'weapon-contacts-1031.mp4')],stdout=subprocess.DEVNULL,stderr=(W/'ffmpeg.log').open('w'),check=True)
subprocess.run([ff,'-i',str(W/'weapon-contacts-1031.mp4'),'-af','volumedetect','-f','null','-'],stdout=subprocess.DEVNULL,stderr=(W/'audio-decode.txt').open('w'),check=True)
