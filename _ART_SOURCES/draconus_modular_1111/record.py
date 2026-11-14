from pathlib import Path
import sys,json,time,base64,subprocess,shutil,re,hashlib,socket,os,threading
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Draconus-rotor-and-full-stages';O.mkdir(exist_ok=True);stage=int(sys.argv[1]);assert 5<=stage<=8
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve
sys.stdout.reconfigure(encoding='utf-8');ff=imageio_ffmpeg.get_ffmpeg_exe();probe=shutil.which('ffprobe');V=O/('stage-'+str(stage));V.mkdir(exist_ok=True);errors=[];console=[];requests=[];timeline=[]
paths=['index.html']+[m.split('?')[0]for m in re.findall(r'<script src="([^"]+)"',(R/'index.html').read_text(encoding='utf-8'))if(R/m.split('?')[0]).is_file()];hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest()for p in paths}
report=dict(stage=stage,difficulty='furious',pilot='cole',assistance='Recording-only player-hit protection and keyboard review pilot; tier5 initial review loadout,40 initial missiles. Native stage entry, waves, enemy health, phases and defeat; no enemy health/phase/clock/clear writes.',completed=False,reason='preparing',sourceHashes=hashes)
raw=V/'capture-native.mp4';movie=O/('stage-'+str(stage)+'-furious.mp4');assert not raw.exists()and not movie.exists(),'Keep previous captures; choose a fresh output before retrying.'
assert shutil.disk_usage(O).free>300_000_000,'Insufficient free space for a full-stage recording.'
port,stop=serve(str(R));cfg=dict(stage=stage)
sock=socket.socket();sock.bind(('127.0.0.1',0));debugport=sock.getsockname()[1];sock.close();report['diagnostics']=dict(pid=os.getpid(),debugport=debugport)
heartbeat=[time.monotonic()];finished=threading.Event()
def watchdog():
 while not finished.wait(5):
  if time.monotonic()-heartbeat[0]>100:
   (V/'watchdog.json').write_text(json.dumps(dict(reason='Recorder RPC timeout',pid=os.getpid(),seconds=time.monotonic()-heartbeat[0])))
   subprocess.run(['taskkill','/PID',str(os.getpid()),'/T','/F'],capture_output=True);return
threading.Thread(target=watchdog,daemon=True).start()
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows','--disk-cache-size=16777216','--media-cache-size=16777216','--js-flags=--expose-gc',f'--remote-debugging-port={debugport}']);context=br.new_context(viewport={'width':1280,'height':800});context.add_init_script((W/'record-audio-init.js').read_text());context.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p=context.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('crash',lambda _:errors.append('Native browser page crashed'));p.on('console',lambda m:console.append(m.text)if m.type=='error'or'draw error'in m.text or'update error'in m.text else None);p.on('requestfailed',lambda r:requests.append(dict(url=r.url,failure=r.failure)))
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate('s=>{run.stage=s;stageLoadBegin(s)}',stage);p.wait_for_function('s=>{stageLoadTick();return stageLoadReady(s)}',arg=stage,timeout=180000)
  if stage==8:p.wait_for_function('()=>{stageLoadTick();return v18Warm()&&dgm1111Warm()}',timeout=180000)
  heartbeat[0]=time.monotonic();p.add_script_tag(path=str(W/'record-input.js'))
  with raw.open('wb')as stream:
   def chunk(data):stream.write(base64.b64decode(data));stream.flush()
   p.expose_function('saveCaptureChunk',chunk);steering_start=time.time();report['setup']=p.evaluate((W/'record-capture.js').read_text(),cfg);report['reason']='recording';print('START',stage,json.dumps(report['setup']),flush=True);(V/'report.json').write_text(json.dumps(report,indent=2));last_print=-100;next_shot=10;endpoint=None;beg=time.monotonic();last_progress=beg;previous_native=-1
   while True:
    p.wait_for_timeout(950);q=p.evaluate('film1111Snapshot()');heartbeat[0]=time.monotonic();q['diskFree']=shutil.disk_usage(O).free;timeline.append(q);(V/'live.json').write_text(json.dumps(q,indent=2))
    if q['nativeFrames']!=previous_native:last_progress=time.monotonic();previous_native=q['nativeFrames']
    if q['wall']-last_print>=20:print('PROGRESS',stage,json.dumps({k:q.get(k)for k in ['wall','state','stageTimer','waves','expected','kind','hp','mode','phase','form','audioPeak','gunPhases','diskFree']}),flush=True);last_print=q['wall'];p.evaluate('()=>{if(window.gc)window.gc()}')
    if q['wall']>=next_shot:
     data=p.evaluate("reviewCapture.toDataURL('image/png').split(',')[1]");(V/f'frame-{int(q["wall"]):04}.png').write_bytes(base64.b64decode(data));next_shot+=60
    # Live steering may adjust inputs only. Never use it for native state/HP.
    adjust=W/f'input-adjust-stage{stage}.js'
    if adjust.exists()and adjust.stat().st_mtime>steering_start and adjust.stat().st_mtime!=getattr(chunk,'adjusted',None):p.evaluate(adjust.read_text(encoding='utf-8'));chunk.adjusted=adjust.stat().st_mtime
    if q['defeated']and q['stage']!=stage:report.update(completed=True,reason='native stage handoff');break
    done=q['defeated']and not q['bossActive']and q['state']in ['stageclear','victory','stagesel','forge','powers','unlocks','supplies','loadout']and not q['director']
    if done and endpoint is None:endpoint=q['wall']
    if endpoint is not None and q['wall']-endpoint>=7:report.update(completed=True,reason='native stage completion');break
    if q['state']in ['continue','gameover']:report['reason']='recording pilot died';break
    if errors or q['botErrors']or any('draw error'in e or'update error'in e for e in console):report['reason']='runtime error';break
    if time.monotonic()-last_progress>45:report['reason']='native renderer stalled';break
    if shutil.disk_usage(O).free<130_000_000:report['reason']='recording space limit';break
    if q['wall']>1800:report['reason']='review run time limit';break
   report['capture']=p.evaluate("""async()=>{FILM1111.enabled=false;for(const k of Object.keys(Input.keys))Input.keys[k]=false;if(reviewRecorder.state!=='inactive')await new Promise(resolve=>{reviewRecorder.onstop=resolve;reviewRecorder.stop()});await capturePending;captureLive=false;return{...captureStats,events:FILM1111.events,waves:FILM1111.waves,spawned:FILM1111.spawned,maxEnemies:FILM1111.maxEnemies,maxRounds:FILM1111.maxRounds,gunPhases:[...FILM1111.gunFrames],final:film1111Snapshot()};}""");p.screenshot(path=str(V/'final-screen.png'));report['nativeJSUnchanged']=hashes=={path:hashlib.sha256((R/path).read_bytes()).hexdigest()for path in paths};br.close()
finally:
 finished.set();stop();report.update(errors=errors,consoleErrors=console,failedRequests=requests,timeline=timeline);(V/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if report.get('setup',{}).get('mimeType','').startswith('video/mp4'):
 assert raw.resolve().parent==V.resolve()and movie.resolve().parent==O.resolve();raw.rename(movie);report['encoding']='Native MP4, without transcoding. Actual audio/video codecs verified below.'
else:
 args=[ff,'-y','-v','warning','-i',str(raw),'-threads','2','-vf','fps=30','-c:v','libx264','-preset','veryfast','-crf','23','-c:a','aac','-b:a','128k','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)]
 with(V/'encode.log').open('w')as log:subprocess.run(args,stdout=subprocess.DEVNULL,stderr=log,check=True)
if probe:
 data=json.loads(subprocess.check_output([probe,'-v','error','-show_streams','-show_format','-of','json',str(movie)]));report['media']=data;assert any(s['codec_type']=='video'for s in data['streams'])and any(s['codec_type']=='audio'for s in data['streams'])
subprocess.run([ff,'-v','error','-threads','2','-i',str(movie),'-f','null','-'],capture_output=True,check=True);report['decoded']=True;report['bytes']=movie.stat().st_size
if raw.exists():
 assert raw.resolve().parent==V.resolve()and raw.name=='capture-native.mp4';raw.unlink()
(V/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('FINISHED',stage,report['reason'],str(movie),flush=True)
assert report['completed']and report.get('nativeJSUnchanged')and not errors and not report['capture']['tapErrors']and report['capture']['peak']>.001,report['reason']
