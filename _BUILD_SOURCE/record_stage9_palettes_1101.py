"""Native Stage9 modular correction films; real mixer and movement input only.
No enemy HP/phase/attack-clock writes; invulnerable pilot is labelled.
"""
from pathlib import Path
import sys,json,base64,subprocess,hashlib,time
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
from rough_riders_capture_base_1028 import CAPTURE
W=R/'_shots/stage9_palettes_1101/video';W.mkdir(parents=True,exist_ok=True);ff=imageio_ffmpeg.get_ffmpeg_exe()
from stage9_cases_1101 import CASES
palettes=json.loads((R/"_BUILD_SOURCE/stage9_amplify_1101/palettes.json").read_text())["models"]
CASES=[c for c in CASES if c[2]in palettes]
CASES=[(cid,t,title,secs,model,role)for cid,t,model,role,title,secs in CASES]
CASES.sort(key=lambda q:q[4]!='current')
if len(sys.argv)>1:CASES=[c for c in CASES if c[0]in sys.argv[1:]]
files=['assets/game.js','assets/stage9_amplify_1101.js','assets/stage9_amplify_art_1101.js','assets/current_flight_1101.js','_BUILD_SOURCE/stage9_amplify_1101/palettes.json'];hashes={s:hashlib.sha256((R/s).read_bytes()).hexdigest()for s in files}
specs=[];errors=[]
script=CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.26');i=script.index(' function aim(elapsed){');j=script.index(' function render(){',i)
script=script[:i]+r''' function aim(elapsed){
 Input.clearTaps();const K=Input.keys;for(const k of Object.keys(K))K[k]=false;
 const t=(performance.now()-caseStarted)/1000;K.a=t%5<1.65;K.d=t%5>2.3&&t%5<4.4;
 }'''+script[j:]
script=script.replace("cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s'","cfg.name+' / FURIOUS / NATIVE INPUTS / INVULNERABLE PILOT'")
i=script.index(" diffKey='furious';debugUnlocked=true;");j=script.index(' return {entry,difficulty:',i)
script=script[:i]+" const entry={stage:9,role:'enemy',kind:cfg.kind};window.reviewConfig=cfg;setState(GS.PLAY);if(curStage.music)Audio.startMusic(curStage.music);\n"+script[j:]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None)
 p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(30);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(9,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(9)&&s911Keys().every(k=>XART.rdy(k))}',timeout=180000)
 p.evaluate('()=>{const spawn=spawnEnemy;spawnEnemy=function(){if(!window.fixtureSpawn)return null;return spawn.apply(this,arguments);};}')
 cuts=[];partial=len(sys.argv)>1;previous=json.loads((W/'report.json').read_text())if partial and(W/'report.json').exists()else None;rawPath=W/('capture-'+str(int(time.time()))+'.webm'if partial else'capture.webm')
 with rawPath.open('wb')as raw:
  p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)))
  for idx,(cid,typ,title,limit,model,role)in enumerate(CASES):
   spec=dict(type=typ,pattern='s9refit',map=1120,x=-80 if model=='comet'else 340,y=110 if model=='comet'else -180,opt={'_s9Role':role,'_side':1})
   setup=p.evaluate('''s=>{window.fixtureSpawn=true;EA11.case(s);window.fixtureSpawn=false;bossWarned=false;thaw=story=fb2Talk=null;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;playerLocks=[];S911.events=[];S911.fx=[];S911.hazards.clear();S911.splashes=[];S911.heavy=null;player.x=worldWidth()/2;player.y=VH-65;player.invuln=40002;DBGT.god=true;DBGT.speed=1;Input.mouse.active=false;run.weapon=0;run.wlevel=3;window.caseStarted=performance.now();
    drawWorld(0);return {hp:E.hp,maxhp:E.maxhp,type:E.type,x:E.x,y:E.y,model:E._s911?.model};}''',spec)
   if idx==0:
    p.evaluate('()=>{window.savedRAF=window.__bofPendingRAF;requestAnimationFrame=window.__bofRealRAF;window.__bofPendingRAF=null;}');p.evaluate(script,dict(name=title,kind=typ,stage=9,role='enemy'));p.evaluate('()=>{if(window.savedRAF)requestAnimationFrame(window.savedRAF);window.savedRAF=null;}')
   else:p.evaluate('q=>{reviewConfig.name=q[0];reviewConfig.kind=q[1]}',[title,typ])
   start=p.evaluate('(performance.now()-captureStart)/1000');timeline=[];deadAt=None;print('START',typ,'HP',setup['hp'],flush=True)
   while True:
    p.wait_for_timeout(350);q=p.evaluate('()=>({seconds:(performance.now()-captureStart)/1000,elapsed:(performance.now()-caseStarted)/1000,frames:__bofFrames,state,hp:E.hp,dead:E.dead,dying:E._dyingT,x:E.x,y:E.y,phase:E._s911?.phase,view:E._s911Rendered?.view,dir:E._s911Rendered?.dir,playerDead:player.dead,actors:enemies.filter(q=>!q.dead).map(q=>q.type),events:S911.events.length})');timeline.append(q)
    if(q['dead']or q.get('dying')is not None)and deadAt is None:deadAt=q['elapsed']
    if q['elapsed']>limit or deadAt is not None and q['elapsed']-deadAt>(2.0)or errors:break
   end=p.evaluate('(performance.now()-captureStart)/1000');details=p.evaluate('()=>({events:S911.events,peak:captureStats.peak,playing:{...captureStats.playing},god:DBGT.god,weapon:run.weapon,level:run.wlevel})')
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
