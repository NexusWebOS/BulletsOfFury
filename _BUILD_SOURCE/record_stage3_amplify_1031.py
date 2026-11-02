"""Native Stage2 isolated sorties, real mixer, movement-only observer.
Enemy health, clocks, projectiles and attack modes are not written in footage.
Carrier owns its child squadron. God observer uses normal left/right input.
"""
from pathlib import Path
import sys,json,ast,base64,subprocess,http.server,hashlib
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,TRAP_RAF
from rough_riders_capture_base_1028 import CAPTURE
source=ast.parse((R/'_BUILD_SOURCE/probe_stage3_amplify_1031.py').read_text())
SETUP=next(ast.literal_eval(n.value)for n in source.body if isinstance(n,ast.Assign)and any(getattr(t,'id','')=='SETUP'for t in n.targets))
CASES=[('sharddart','Shard Dart / larger upright banking fighter',10),('s3interceptor','Interceptor / actual turning and twin gun mouths',15),('ac10icejet','Ice Interceptor / turning flight and clear twin ice bullets',15),('glaciercarrier','Glacier Carrier / paired ice bullets',13),('cryoeye','Cryoeye / four cardinal level2 ice lasers',16),('s3mine','Ice Mine Bomber / mine deployment and boost escape',12),('modturret-laser','Island Laser Turret / registered ice barrel',13),('modturret-sonic','Island Sonic Turret / blue pressure waves',13)]
if len(sys.argv)>1:CASES=[q for q in CASES if q[0]in sys.argv[1:]]
W=R/'_shots/stage3_amplify_1031/video';W.mkdir(parents=True,exist_ok=True)
files=['assets/game.js','assets/stage3_amplify_1031.js','assets/stage2_amplify_art_1031.js'];hashes={x:hashlib.sha256((R/x).read_bytes()).hexdigest()for x in files}
http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R));ff=imageio_ffmpeg.get_ffmpeg_exe()
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding'])
  for kind,title,duration in CASES:
   folder=W/kind;folder.mkdir(exist_ok=True);errors=[];p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof I31!=="undefined"',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(40)
   p.evaluate("()=>{debugStartFight(debugFightFor(3,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(3,'boss').kind);warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);stageLoadBegin(3)}")
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(3)&&Object.values(I31_ART.banks).every(a=>XART.rdy(a.key))}',timeout=180000)
   fixture=SETUP
   if kind.startswith('i31elite_'):fixture=fixture.replace("{_modWeapon:","{_i31Role:'"+kind.split('_')[-1]+"',_modWeapon:")
   setup=p.evaluate(fixture,[kind,'furious']);p.evaluate('drawWorld(0)');p.wait_for_timeout(50)
   p.evaluate("()=>{player.invuln=0;Input.mouse.active=false;}")
   script=CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.26')
   a=script.index(' function aim(elapsed){');z=script.index(' function render(){',a)
   script=script[:a]+r''' function aim(elapsed){
    Input.clearTaps();const K=Input.keys;for(const k of Object.keys(K))K[k]=false;
    K.a=elapsed%5<2.1;K.d=elapsed%5>2.8&&elapsed%5<4.8;
   }'''+script[z:]
   script=script.replace("cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s'","cfg.name+' / FURIOUS / NATIVE SORTIE / INVULNERABLE OBSERVER / '+elapsed.toFixed(1)+'s'")
   a=script.index(" diffKey='furious';debugUnlocked=true;");z=script.index(' return {entry,difficulty:',a)
   script=script[:a]+" const entry={stage:3,role:'enemy',kind:cfg.kind};window.reviewConfig=cfg;Input.clearTaps();setState(GS.PLAY);if(curStage.music)Audio.startMusic(curStage.music);\n"+script[z:]
   timeline=[]
   with (folder/'capture.webm').open('wb')as raw:
    p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)))
    p.evaluate('()=>{window.__i31SavedRAF=window.__bofPendingRAF;requestAnimationFrame=window.__bofRealRAF;window.__bofPendingRAF=null;}')
    p.evaluate(script,dict(name=title,kind=kind,stage=3,role='enemy'))
    p.evaluate('()=>{if(window.__i31SavedRAF)requestAnimationFrame(window.__i31SavedRAF);window.__i31SavedRAF=null;}')
    print('START',kind,setup,flush=True);seen=set();deadAt=None
    while True:
     p.wait_for_timeout(300);q=p.evaluate("()=>({seconds:(performance.now()-captureStart)/1000,frames:__bofFrames,state,hp:E.hp,dead:!!E.dead,dying:E._dyingT,x:E.x,y:E.y,phase:E._i31?.phase||E._i31Ground?.phase,key:E._i31Rendered?.key,pose:E._i31Rendered?.frame,shots:I31.events.filter(q=>['shot','cross-lasers'].includes(q.event)).length,actors:enemies.filter(e=>!e.dead).map(e=>e.type),playerDead:player.dead,god:DBGT.god})");timeline.append(q)
     if q.get('phase')not in seen and q['seconds']>1:
      p.screenshot(path=str(folder/(str(q.get('phase'))+'.png')));seen.add(q.get('phase'))
     if q['dead']or q.get('dying')is not None:
      if deadAt is None:deadAt=q['seconds']
     if q['seconds']>duration or deadAt is not None and q['seconds']-deadAt>1.4 or errors:break
    stats=p.evaluate("async()=>{for(const k of Object.keys(Input.keys))Input.keys[k]=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return{...captureStats,botErrors:reviewBot.errors,events:I31.events};}")
    (folder/'report.json').write_text(json.dumps(dict(type=kind,title=title,setup=setup,method=__doc__,timeline=timeline,stats=stats,errors=errors,sourceHashes=hashes),indent=2))
   p.close();assert not errors,errors[:2]
   subprocess.run([ff,'-y','-i',str(folder/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(folder/'preview.mp4')],stdout=subprocess.DEVNULL,stderr=(folder/'encode.log').open('w'),check=True)
   subprocess.run([ff,'-v','error','-i',str(folder/'preview.mp4'),'-f','null','-'],capture_output=True,check=True)
   print('DONE',kind,round(timeline[-1]['seconds'],2),'attacks',timeline[-1]['shots'],'audio',list(stats['playing']),flush=True)
  b.close()
finally:stop()
assert hashes=={x:hashlib.sha256((R/x).read_bytes()).hexdigest()for x in files},'Production source changed while recording'
