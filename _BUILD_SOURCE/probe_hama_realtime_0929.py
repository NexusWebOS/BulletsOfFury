"""Real-time HAMA playback with no clock override; record the actual canvas."""
from pathlib import Path
import sys,json,time,base64,http.server
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path(sh.GAME)/'_shots/hama_frames_0929';out.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[];samples=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
  pg=br.new_page(viewport={'width':1000,'height':1100})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000)
  pg.wait_for_function('() => (window.__bofFrames|0)>4',timeout=120000)
  pg.evaluate("""() => {diffKey='normal';DIFF=DIFFS.normal;debugFight=null;coopOn=false;setState(GS.PASSWORD);pwInput='HAMA';submitPassword();
   pilotIndex=PILOTS.findIndex(p=>p.key==='maverick');startRun(PENDING_STAGE);player.invuln=99999;
   window.__rtLog={modes:{},states:{},launched:0,caught:0};
   const tick=ht27Tick;ht27Tick=function(b,dt){const H=b._hammerTime&&b._hammerTime.hama,was=H&&!!H.flyHammer;
    const r=tick.apply(this,arguments),d=b._hammerTime,L=window.__rtLog;
    if(d){L.modes[d.mode]=(L.modes[d.mode]||0)+1;L.states[b._hammer.state]=(L.states[b._hammer.state]||0)+1;
     if(H&&!was&&H.flyHammer)L.launched++;if(H&&was&&!H.flyHammer)L.caught++;}return r;};
  }""")
  pg.wait_for_function('() => boss._hammerTime.musicStarted && !Snd.music.hama.paused',timeout=120000)
  start=pg.evaluate("""() => {const m=Snd.music.hama,canvas=document.getElementById('screen'),stream=canvas.captureStream(30);
   let audioTracks=0;if(m.captureStream){const sound=m.captureStream();for(const a of sound.getAudioTracks()){stream.addTrack(a);audioTracks++;}}
   window.__rtChunks=[];window.__rtRecorder=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:3500000});
   window.__rtRecorder.ondataavailable=e=>{if(e.data.size)window.__rtChunks.push(e.data);};window.__rtRecorder.start(500);
   return {audioTracks,media:m.currentTime,frames:window.__bofFrames};}""")
  print('Recording actual gameplay, unmodified media clock:',start,flush=True)
  deadline=time.monotonic()+36
  while time.monotonic()<deadline:
   pg.wait_for_timeout(500)
   samples.append(pg.evaluate("""() => ({media:Snd.music.hama.currentTime,game:boss._hammerTime.clock,
    paused:Snd.music.hama.paused,frames:window.__bofFrames,state,mode:boss._hammerTime.mode})"""))
  encoded=pg.evaluate("""async () => {const r=window.__rtRecorder;await new Promise(resolve=>{r.onstop=resolve;r.stop();});
   const blob=new Blob(window.__rtChunks,{type:'video/webm'});return await new Promise(resolve=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(blob);});}""")
  (out/'hama_realtime_0929.webm').write_bytes(base64.b64decode(encoded.split(',',1)[1]))
  report=pg.evaluate('() => window.__rtLog');report.update(start=start,end=samples[-1],samples=samples,errors=errors)
  report['maxClockDrift']=max(abs(s['media']-s['game']) for s in samples)
  report['framesAdvanced']=samples[-1]['frames']-start['frames']
  (out/'realtime.json').write_text(json.dumps(report,indent=2))
  print(json.dumps({k:v for k,v in report.items() if k!='samples'},indent=2),flush=True)
  assert not errors,errors
  assert report['maxClockDrift']<.08 and samples[-1]['media']-start['media']>35
  assert report['launched']>=1 and report['caught']>=1 and report['modes'].get('attack',0)>20
  assert report['framesAdvanced']>900
  pg.evaluate('() => setState(GS.TITLE)')
  assert pg.evaluate('() => !ht27Active && Snd.cur!==Snd.music.hama')
  br.close();print('REAL-TIME HAMA OK; music, toss/catch, combat, cleanup and canvas recording passed.',flush=True)
finally:stop()
