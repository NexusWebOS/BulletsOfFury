"""Real-time native Furious observe-then-clear waves, current layers, labelled GOD observer.
No enemy HP/phase/attack timer writes. Native scheduled, ambient and adaptive combat retained; only bosses/minibosses omitted.
"""
from pathlib import Path
import json,sys,base64,hashlib,re,subprocess,time,datetime,http.server,functools,threading,ctypes
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
R=Path(__file__).resolve().parents[2];W=Path(__file__).parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import TRAP_RAF,serve
from rough_riders_capture_base_1028 import CAPTURE
O=R/'_shots/waves_observe_1102';O.mkdir(parents=True,exist_ok=True);ff=imageio_ffmpeg.get_ffmpeg_exe()
stages=[(int(x.rstrip('r')),'right' if x.endswith('r') else 'left') for x in sys.argv[1:]] or [(2,'left'),(3,'left'),(4,'left'),(5,'left'),(6,'left'),(6,'right'),(7,'left'),(8,'left'),(9,'left'),(1,'left')]
paths=['index.html']+[m.split('?')[0] for m in re.findall(r'<script src="([^"]+)"',(R/'index.html').read_text(encoding='utf-8')) if (R/m.split('?')[0]).is_file()]
hashes={s:hashlib.sha256((R/s).read_bytes()).hexdigest() for s in paths};method=(W/'wave_observe_1102.js').read_bytes()
script=CAPTURE.replace('video/webm;codecs=vp9,opus','video/webm;codecs=vp8,opus').replace('videoBitsPerSecond:4500000','videoBitsPerSecond:8500000').replace('gain.gain.value=.5','gain.gain.value=.24');a=script.index(' function aim(elapsed){');z=script.index(' function render(){',a);script=script[:a]+' function aim(elapsed){}\n'+script[z:]
a=script.index(" diffKey='furious';debugUnlocked=true;");z=script.index(' return {entry,difficulty:',a);script=script[:a]+" const entry={stage:cfg.stage,role:'waves',kind:'regular'};setState(GS.PLAY);if(curStage.music)Audio.startMusic(curStage.music);\n"+script[z:]
script=script.replace("cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s'", "cfg.name+' / FURIOUS / GOD / '+WO16.phase+' / WAVE '+Math.min(WO16.expected,WO16.events.length)+'/'+WO16.expected+' / LIVE '+(WO16.lastInput?.visible||0)+' / SHOTS '+(WO16.lastInput?.bullets||0)+' / SIM '+WO16.clock.toFixed(1)+'s'")
# Persistent local HTTP connections and a generous accept queue prevent setup
# connection refusals during simultaneous UI/weapon bank preloads on Windows.
class FilmServer(http.server.ThreadingHTTPServer):
 request_queue_size=256
 daemon_threads=True
class FilmHandler(http.server.SimpleHTTPRequestHandler):
 protocol_version='HTTP/1.1'
 def log_message(self,*a):pass
 def handle(self):
  try:super().handle()
  except (ConnectionAbortedError,ConnectionResetError,BrokenPipeError):pass
httpd=FilmServer(('127.0.0.1',0),functools.partial(FilmHandler,directory=str(R)));port=httpd.server_address[1];stop=httpd.shutdown
ctypes.windll.kernel32.SetThreadExecutionState(0x80000001)
threading.Thread(target=httpd.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
  for stage,route in stages:
   label='stage-1-supplement-17';V=O/label;V.mkdir(exist_ok=True)
   completed=[]
   for receipt in O.glob(label+'*/verified.json'):
    v=json.loads(receipt.read_text(encoding='utf8'))
    if v.get('label')!=label or v.get('excluded'):continue
    prior=json.loads((receipt.parent/'report.json').read_text(encoding='utf8'))
    if prior.get('sourceHashes')==hashes and prior.get('methodSourceHash')==hashlib.sha256(method).hexdigest() and Path(v['movie']).is_file():completed.append(receipt)
   if completed:print('KEEP VERIFIED',label,flush=True);continue
   if any(V.iterdir()):V=O/(label+'-take-'+datetime.datetime.now().strftime('%H%M%S'));V.mkdir()
   errors=[];http=[];trace=[];(V/'wave-review-source.js').write_bytes(method)
   print('PREPARE',label,flush=True)
   b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows']);p=b.new_page(viewport={'width':1280,'height':800})
   p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r:http.append({'status':r.status,'url':r.url}) if r.status>=400 else None)
   p.on('requestfailed',lambda r:errors.append('REQUEST '+r.url+' '+str(r.failure)) if r.failure!='net::ERR_ABORTED' else None)
   p.route('**/assets/online-config.js',lambda route:route.fulfill(status=200,content_type='application/javascript',body='window.BOF_ONLINE_CONFIG={};'))
   p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&!!window.BOF_LAYERED_STAGES',timeout=180000);p.wait_for_load_state('networkidle',timeout=60000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
   p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.add_script_tag(path=str(W/'reference_wave_maps.js'));p.add_script_tag(path=str(V/'wave-review-source.js'))
   setup=p.evaluate('q=>{const r=WO16.start(q.stage,q.route);WO16.current=16;WO16.expected=17;waveIdx=16;return {...r,supplementWave:17}}',dict(stage=stage,route=route));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',timeout=180000)
   scenery=p.evaluate('()=>({active:ls112Live(),info:BOF_LAYERED_STAGES.info(),terrain:LS112_ART.levels[String(run.stage)]||null,material:LS112_ART.materials[LS112_ART.levels[String(run.stage)]?.material]||null,keys:ls112Keys(run.stage),allReady:ls112Keys(run.stage).every(k=>XART.rdy(k))})')
   assert stage==1 or scenery['active'] and scenery['allReady'],scenery
   assetHashes={a['path']:hashlib.sha256((R/a['path']).read_bytes()).hexdigest() for a in [scenery['terrain'],scenery['material']] if a and a.get('path')}
   p.evaluate('()=>{drawWorld(0);requestAnimationFrame=window.__bofRealRAF;window.__bofPendingRAF=null;}')
   with (V/'capture.webm').open('wb') as raw:
    p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)));p.evaluate(script,dict(name='Stage '+str(stage)+' / Regular waves',stage=stage,role='waves',kind='regular'))
    p.evaluate('''()=>{let previous=performance.now(),debt=0;window.waveFilmLive=true;
     function frame(now){if(!waveFilmLive)return;const gap=now-previous;debt+=Math.max(0,Math.min(.05,gap/1000));previous=now;let steps=0;const before=performance.now();
      stageLoadTick();while(debt+1e-9>=1/60&&steps<3&&state===GS.PLAY){WO16.input(1/60);stateT+=1/60;updatePlay(1/60);debt-=1/60;steps++;}
      const afterUpdate=performance.now();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;window.__bofFrames=(window.__bofFrames|0)+1;drawWorld(steps/60);WO16.frame(gap,afterUpdate-before,performance.now()-afterUpdate);
      requestAnimationFrame(frame);
     }requestAnimationFrame(frame);}''')
    beg=time.monotonic();nextShot=8;print('START',label,json.dumps(setup),flush=True)
    while True:
     p.wait_for_timeout(1000);q=p.evaluate('()=>({...WO16.snapshot(),wall:(performance.now()-captureStart)/1000,frames:__bofFrames,layers:BOF_LAYERED_STAGES.info()})');trace.append(q)
     if q['wall']>=nextShot:
      nextShot+=40
     if len(trace)%15==0:
      (V/'progress.json').write_text(json.dumps(q,indent=2));print('PROGRESS',label,round(q['wall']),q['events'],'/',q['expected'],q['input'],flush=True)
     if q['done'] or errors or http or q['state']!='play' or time.monotonic()-beg>1800:break
    detail=p.evaluate('()=>({events:WO16.events,attempts:WO16.attempts,units:WO16.units,clearWindows:WO16.clearWindows,earlyDamage:WO16.earlyDamage,firstFire:WO16.firstFire,waveMeta:WO16.waveMeta})')
    stats=p.evaluate('async()=>{waveFilmLive=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return{...captureStats,botErrors:reviewBot.errors};}')
   assert q['firstFire'] is None or q['firstFire']>=12
   report=dict(stage=stage,route=route,label=label,folder=str(V),setup=setup,result=q,trace=trace,**detail,stats=stats,errors=errors,httpErrors=http,sourceHashes=hashes,sceneryAssetHashes=assetHashes,scenery=scenery,policy={'visibleGrace':8,'eliteGrace':18,'initialQuiet':12,'normalCadence':False,'ambientAndAdaptive':False,'cleanup':'After demonstration, native player fire clears the current group before advancing','alliedFire':'held during observation; native during cleanup','pacing':'Explicit one-wave inspection with camera seeks to original native release locations'},method=__doc__,methodSourceHash=hashlib.sha256(method).hexdigest(),qaOverrides=['Optional online configuration disabled; gameplay/assets/audio unchanged'],captureCodec='VP8/Opus',recordedAt=datetime.datetime.now(datetime.timezone.utc).isoformat())
   (V/'report.json').write_text(json.dumps(report,indent=2));p.close();b.close()
   assert not errors and not http and q['done'] and not q['boss'] and not q['mini'],(label,q,errors,http)
   assert stage==1 or any(t['layers']['draws'].get('stage-'+str(stage),0)>0 for t in trace),'New terrain was not rendered'
   movie=V/('stage-'+str(stage)+'-waves.mp4');print('ENCODE',label,flush=True)
   subprocess.run([ff,'-y','-i',str(V/'capture.webm'),'-vf','fps=30','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(movie)],stdout=subprocess.DEVNULL,stderr=(V/'encode.log').open('w'),check=True)
   subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],capture_output=True,check=True)
   assert hashes=={s:hashlib.sha256((R/s).read_bytes()).hexdigest() for s in paths},'Production changed during recording'
   (V/'verified.json').write_text(json.dumps({'label':label,'folder':str(V),'movie':str(movie),'done':True,'sourceHashesMatch':True,'newTerrain':stage!=1,'chapters':len(detail['events'])},indent=2))
   print('DONE',label,round(q['wall'],2),'seconds',len(detail['events']),'chapters',flush=True)
finally:
 stop();ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
