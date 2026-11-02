"""Native Stage7 modular correction films; real mixer and movement input only.
No enemy HP/phase/attack-clock writes; invulnerable pilot is labelled.
"""
from pathlib import Path
import sys,json,base64,subprocess,hashlib,time
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
from rough_riders_capture_base_1028 import CAPTURE
W=R/'_shots/stage7_amplify_1101/video';W.mkdir(parents=True,exist_ok=True);ff=imageio_ffmpeg.get_ffmpeg_exe()
CASES=[('stage7-s7pipe','s7pipe','Modular Pipe Crawler / articulated pipe-side legs and twin toxic slugs',14),('stage7-s7tank','s7tank','Toxic Tank / dual machine-gun slug bursts, no Retina locks',12),('stage7-modturret','modturret','MG Ground Turret / paired toxic slugs from the actual mouths',12),('stage7-ll18brood','ll18brood','Brood Sentinel / aura shield, scythe claws and robot-fly maw',22),('stage7-modturret-2','modturret','Laser Ground Turret / toxic-green 1015 laser fire',12),('stage7-cp22relay','cp22relay','Heavy Sewer Relay / accelerating rotary fire and armed barrel rolls',19),('stage7-modturret-3','modturret','Sonic Ground Turret / toxic-green sonic waves',12),('stage7-cp22slime','cp22slime','Toxic Slime Jet / camouflaged hull and modular chainguns',17),('stage7-s7barge','s7barge','Toxic Barge / four articulated deck guns and hull-shaped shield',17),('stage7-s7missilejet','s7missilejet','Toxic Missile Jet / black-green hull, twin pods and Retina missiles',18),('stage7-brood-escort','s8crescent','Crescent Escort / distinct crescent fighter and toxic cannons',17)]
if len(sys.argv)>1:CASES=[c for c in CASES if c[0]in sys.argv[1:]]
files=['assets/game.js','assets/stage7_amplify_1101.js','assets/stage5_amplify_art_1101.js'];hashes={s:hashlib.sha256((R/s).read_bytes()).hexdigest()for s in files}
specs=json.loads((R/'_shots/enemy_flight_1031/before/stage7-specs.json').read_text());errors=[]
script=CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.26');i=script.index(' function aim(elapsed){');j=script.index(' function render(){',i)
script=script[:i]+r''' function aim(elapsed){
 Input.clearTaps();const K=Input.keys;for(const k of Object.keys(K))K[k]=false;
 const t=(performance.now()-caseStarted)/1000;K.a=t%5<1.65;K.d=t%5>2.3&&t%5<4.4;
 }'''+script[j:]
script=script.replace("cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s'","cfg.name+' / FURIOUS / NATIVE INPUTS / INVULNERABLE PILOT'")
i=script.index(" diffKey='furious';debugUnlocked=true;");j=script.index(' return {entry,difficulty:',i)
script=script[:i]+" const entry={stage:7,role:'enemy',kind:cfg.kind};window.reviewConfig=cfg;setState(GS.PLAY);if(curStage.music)Audio.startMusic(curStage.music);\n"+script[j:]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None)
 p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(30);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(7,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)&&Object.values(S711_ART.banks).every(B=>XART.rdy(B.key))}',timeout=180000)
 p.evaluate('()=>{const spawn=spawnEnemy;spawnEnemy=function(){if(!window.fixtureSpawn&&ai27Context!==window.E)return null;return spawn.apply(this,arguments);};}')
 cuts=[];partial=len(sys.argv)>1;previous=json.loads((W/'report.json').read_text())if partial and(W/'report.json').exists()else None;rawPath=W/('capture-'+str(int(time.time()))+'.webm'if partial else'capture.webm')
 with rawPath.open('wb')as raw:
  p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)))
  for idx,(cid,typ,title,limit)in enumerate(CASES):
   spec=next((s for s in specs if s['type']==typ and(s.get('opt',{}).get('_modWeapon')==({'stage7-modturret':'mg','stage7-modturret-2':'laser','stage7-modturret-3':'sonic'}.get(cid)) if typ=='modturret'else True)),dict(type=typ,pattern='s7toxic',map=1120,x=340,y=-150,opt={}))
   setup=p.evaluate('''s=>{window.fixtureSpawn=true;EA11.case(s);window.fixtureSpawn=false;bossWarned=false;thaw=story=fb2Talk=null;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;playerLocks=[];S711.events=[];S711.fx=[];if(E._s711?.model==='ground'){E._s711.anchor.y=levelSrcY()+140;E._modTurret.mapY=E._s711.anchor.y;E.y=140;}player.x=worldWidth()/2;player.y=VH-65;player.invuln=40002;DBGT.god=true;DBGT.speed=1;Input.mouse.active=false;run.weapon=0;run.wlevel=3;window.caseStarted=performance.now();
    drawWorld(0);return {hp:E.hp,maxhp:E.maxhp,type:E.type,x:E.x,y:E.y,model:E._s711?.model};}''',spec)
   if idx==0:
    p.evaluate('()=>{window.savedRAF=window.__bofPendingRAF;requestAnimationFrame=window.__bofRealRAF;window.__bofPendingRAF=null;}');p.evaluate(script,dict(name=title,kind=typ,stage=7,role='enemy'));p.evaluate('()=>{if(window.savedRAF)requestAnimationFrame(window.savedRAF);window.savedRAF=null;}')
   else:p.evaluate('q=>{reviewConfig.name=q[0];reviewConfig.kind=q[1]}',[title,typ])
   start=p.evaluate('(performance.now()-captureStart)/1000');timeline=[];deadAt=None;print('START',typ,'HP',setup['hp'],flush=True)
   while True:
    p.wait_for_timeout(350);q=p.evaluate('()=>({seconds:(performance.now()-captureStart)/1000,elapsed:(performance.now()-caseStarted)/1000,frames:__bofFrames,state,hp:E.hp,dead:E.dead,dying:E._dyingT,x:E.x,y:E.y,phase:E._s711?.phase,dir:E._s711Rendered?.dir,playerDead:player.dead,actors:enemies.filter(q=>!q.dead).map(q=>q.type),events:S711.events.length})');timeline.append(q)
    if(q['dead']or q.get('dying')is not None)and deadAt is None:deadAt=q['elapsed']
    if q['elapsed']>limit or deadAt is not None and q['elapsed']-deadAt>(2.0)or errors:break
   end=p.evaluate('(performance.now()-captureStart)/1000');details=p.evaluate('()=>({events:S711.events,peak:captureStats.peak,playing:{...captureStats.playing},god:DBGT.god,weapon:run.weapon,level:run.wlevel})')
   r=dict(id=cid,type=typ,title=title,setup=setup,start=start,end=end,timeline=timeline,details=details,errors=list(errors),sourceHashes=hashes,method=__doc__);cuts.append(r);(W/(cid+'.json')).write_text(json.dumps(r,indent=2));print('CUT',typ,round(end-start,2),'events',len(details['events']),'last HP',q['hp'],flush=True);assert not errors,errors
  stats=p.evaluate('async()=>{await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return {...captureStats,botErrors:reviewBot.errors};}')
 group=dict(cuts=cuts,stats=stats,errors=errors)
 if previous:
  current={c['id']:c for c in cuts};group['cuts']=[current.get(c['id'],c)for c in previous['cuts']];group['previousCaptureStats']=previous['stats']
 (W/'report.json').write_text(json.dumps(group,indent=2));p.close();b.close()
 for cut in cuts:
  out=W/(cut['id']+'.mp4');subprocess.run([ff,'-y','-ss',str(cut['start']),'-i',str(rawPath),'-t',str(cut['end']-cut['start']),'-vf','fps=30','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(out)],stdout=subprocess.DEVNULL,stderr=(W/'encode.log').open('w'),check=True);subprocess.run([ff,'-v','error','-i',str(out),'-f','null','-'],capture_output=True,check=True)
print('Completed',len(cuts),'native decoded correction films',flush=True)
assert hashes=={s:hashlib.sha256((R/s).read_bytes()).hexdigest()for s in files},'Production changed during recording'
