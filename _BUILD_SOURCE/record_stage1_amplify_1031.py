"""Five native isolated enemy sorties with audible shared-mixer output.
Legal terrain and one authored enemy selected before recording. Enemy HP, clocks,
route/attack states and projectiles are never written during footage. Observer is
invulnerable and uses normal movement/fire input. Not a campaign balance run.
"""
from pathlib import Path
import sys,json,ast,time,base64,subprocess,http.server,hashlib
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,TRAP_RAF
from rough_riders_capture_base_1028 import CAPTURE
W=R/'_shots/stage1_amplify_1031/video';W.mkdir(parents=True,exist_ok=True);http.server.ThreadingHTTPServer.request_queue_size=256
tree=ast.parse((R/'_BUILD_SOURCE/probe_stage1_amplify_1031.py').read_text());SETUP=next(ast.literal_eval(a.value)for a in tree.body if isinstance(a,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='SETUP'for t in a.targets))
cases=[('s1boatgun','Gunboat / straight machine-gun fire'),('s1corvette','River Corvette / physical barrel flashes'),('s1jetdelta','Delta Fighter / turning gun pass and animated thrusters'),('s1jetbomber','Strike Bomber / visible continuous bombing run'),('s1tankheavy','Heavy Jungle Tank / twin-tube locked missile salvo'),('s1jetdelta_pair','Delta Fighter / authored paired flyby')]
if len(sys.argv)>1:cases=[x for x in cases if x[0]in sys.argv[1:]]
port,stop=serve(str(R));ff=imageio_ffmpeg.get_ffmpeg_exe();files=['assets/game.js','assets/stage1_amplify_1031.js','assets/stage1_amplify_art_1031.js'];hashes={x:hashlib.sha256((R/x).read_bytes()).hexdigest()for x in files}
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);reports=[]
  for kind,title in cases:
   folder=W/kind;folder.mkdir(exist_ok=True);errors=[];p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof S1A!=="undefined"',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(50)
   p.evaluate("()=>{debugStartFight(debugFightFor(1,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(1,'boss').kind);warnT=0;DBGT.god=true;BOFCinematicDirector.cancel();setState(GS.PLAY);s1mWarm();stageLoadBegin(1)}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&Object.values(S1A_ART).every(a=>XART.rdy(a.key))}',timeout=180000)
   setup=p.evaluate(SETUP,['s1jetdelta'if kind=='s1jetdelta_pair'else kind,'furious']);
   if kind=='s1jetdelta_pair':setup=p.evaluate("()=>{enemies=[];fb9SwoopPair();window.E=enemies[0];return{type:'s1jetdelta',pair:true,hp:E.hp,x:E.x,y:E.y};}")
   p.evaluate('drawWorld(0)');p.wait_for_timeout(100)
   p.evaluate("()=>{debugUnlocked=true;DBGT.god=true;DBGT.speed=1;DBGT.frozen=false;player.invuln=0;Input.pollGamepad=()=>{};for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.clearTaps();Input.mouse.down=false;Input.mouse.active=false;}")
   # Reuse just the native canvas compositor/shared mixer tap, with an input-only
   # observer and no boss spawn/reset after the enemy fixture has been prepared.
   script=CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.26')
   a=script.index(' function aim(elapsed){');z=script.index(' function render(){',a)
   script=script[:a]+r''' function aim(elapsed){
    if(!window.E)return;Input.clearTaps();const K=Input.keys;for(const k of Object.keys(K))K[k]=false;
    const tx=clamp(E.x,camLeftX()+35,camRightX()-35);K.a=player.x>tx+7;K.d=player.x<tx-7;
    // Show the actual attack first, then ordinary fire can hit/kill the actor.
    K.j=elapsed>6.5&&elapsed%1.1<.17&&E.y<player.y-65&&!E.dead;
   }''' + script[z:]
   script=script.replace("cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s'","cfg.name+' / FURIOUS / ISOLATED NATIVE SORTIE / INVULNERABLE OBSERVER / '+elapsed.toFixed(1)+'s'")
   a=script.index(" diffKey='furious';debugUnlocked=true;");z=script.index(' return {entry,difficulty:',a)
   script=script[:a]+" const entry={stage:1,role:'enemy',kind:cfg.kind};window.reviewConfig=cfg;Input.clearTaps();setState(GS.PLAY);Audio.startMusic('stage1');\n"+script[z:]
   timeline=[]
   with (folder/'capture.webm').open('wb')as raw:
    p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)))
    p.evaluate('()=>{window.__s1aGameRAF=window.__bofPendingRAF;window.requestAnimationFrame=window.__bofRealRAF;window.__bofPendingRAF=null;}')
    p.evaluate(script,dict(name=title,kind=kind,stage=1,role='enemy'))
    # Resume exactly one previously parked game RAF chain.
    p.evaluate("()=>{if(window.__s1aGameRAF)requestAnimationFrame(window.__s1aGameRAF);window.__s1aGameRAF=null;}")
    print('START',kind,setup,flush=True);saved=set();deadAt=None
    while True:
     p.wait_for_timeout(300);q=p.evaluate("()=>({seconds:(performance.now()-captureStart)/1000,state,frames:__bofFrames,hp:E.hp,dead:!!E.dead,dying:E._dyingT,x:E.x,y:E.y,angle:s1aPlaneHead(E),heading:E._air13Frame,phase:E._s1aFlight?.phase,shots:S1A.events.filter(q=>q.event==='shot').length,bombs:S1A.events.filter(q=>q.event==='bomb-drop').length,pairs:S1A.events.filter(q=>q.event==='tank-dual').length,actors:enemies.filter(e=>!e.dead).map(e=>e.type),playerDead:player.dead,inputs:Object.entries(Input.keys).filter(([k,v])=>v).map(([k])=>k),god:DBGT.god,fx:S1A.fx.length,draws:{...S1A.draws}})");timeline.append(q)
     for name,condition in [('release',(q['shots']>0 or q['bombs']>0 or q['pairs']>0)),('turn',kind=='s1jetdelta'and q.get('heading',0)not in [0,None]),('late',kind=='s1jetbomber'and q['y']>350),('overview',q['seconds']>4)]:
      if condition and name not in saved:
       p.screenshot(path=str(folder/(name+'.png')));saved.add(name)
     if q['dead']or q.get('dying')is not None:
      if deadAt is None:deadAt=q['seconds']
     if deadAt is not None and q['seconds']-deadAt>1.5 or q['seconds']>16 or errors:break
    stats=p.evaluate("async()=>{for(const k of ['a','d','w','s','j','c'])Input.keys[k]=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return{...captureStats,botErrors:reviewBot.errors,events:S1A.events,draws:S1A.draws};}")
    report=dict(type=kind,title=title,setup=setup,method=__doc__,errors=errors,timeline=timeline,stats=stats,sourceHashes=hashes);(folder/'report.json').write_text(json.dumps(report,indent=2));reports.append(report)
   p.close()
   subprocess.run([ff,'-y','-i',str(folder/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(folder/'preview.mp4')],stdout=subprocess.DEVNULL,stderr=(folder/'encode.log').open('w'),check=True)
   subprocess.run([ff,'-i',str(folder/'preview.mp4'),'-af','volumedetect','-f','null','-'],stdout=subprocess.DEVNULL,stderr=(folder/'audio-decode.txt').open('w'),check=True);print('DONE',kind,'seconds',timeline[-1]['seconds'],'shots',timeline[-1]['shots'],'bombs',timeline[-1]['bombs'],'pairs',timeline[-1]['pairs'],'errors',errors,flush=True)
  (W/'reports.json').write_text(json.dumps(reports,indent=2));b.close()
finally:stop()
assert hashes=={x:hashlib.sha256((R/x).read_bytes()).hexdigest()for x in files},'Source changed while recording'
