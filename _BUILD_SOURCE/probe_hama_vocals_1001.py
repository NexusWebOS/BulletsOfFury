"""Real Chromium, real mixed audio clock. The player is invulnerable for this review."""
from pathlib import Path
import sys,json,base64,time,http.server,io,re
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/hama_hooks_1001';O.mkdir(parents=True,exist_ok=True)
class AudioRangeHandler(http.server.SimpleHTTPRequestHandler):
 # SimpleHTTPRequestHandler ignores Range and Chromium can reset MP3 seeks to
 # zero. Exercise real media seeking with ordinary HTTP byte-range support.
 def log_message(self,*args):pass
 def end_headers(self):self.send_header('Accept-Ranges','bytes');super().end_headers()
 def send_head(self):
  p=Path(self.translate_path(self.path));r=self.headers.get('Range','');m=re.fullmatch(r'bytes=(\d+)-(\d*)',r)
  if m and p.is_file():
   size=p.stat().st_size;a=int(m[1]);b=min(size-1,int(m[2]) if m[2] else size-1)
   if a>=size:self.send_error(416);return None
   with p.open('rb') as f:f.seek(a);data=f.read(b-a+1)
   self.send_response(206);self.send_header('Content-Type',self.guess_type(str(p)));self.send_header('Content-Length',str(len(data)));self.send_header('Content-Range',f'bytes {a}-{b}/{size}');self.end_headers();return io.BytesIO(data)
  return super().send_head()
http.server.SimpleHTTPRequestHandler=AudioRangeHandler
port,stop=sh.serve(str(R));errors=[];out={'checks':[],'samples':[]}
def check(v,name):out['checks'].append({'ok':bool(v),'name':name});print(('OK ' if v else 'FAIL ')+name,flush=True)
def shot(p,name):
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1080,'height':950})
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.mouse.click(500,400)
  p.evaluate("()=>{diffKey='normal';DIFF=DIFFS.normal;debugFight=null;coopOn=false;setState(GS.PASSWORD);pwInput='HAMA';submitPassword();pilotIndex=PILOTS.findIndex(p=>p.key==='maverick');startRun(PENDING_STAGE);player.invuln=99999;window.slams=[];const sl=hamaSlam;hamaSlam=function(b,d,w){slams.push({t:d.clock,word:w});return sl.apply(this,arguments);};}")
  p.wait_for_function('()=>boss?._hammerTime.musicStarted&&!ht27Song().paused&&ht27Song().readyState>=3&&ht27Song().volume>0',timeout=120000)
  check(p.evaluate("()=>ht27Song().src.includes('hama_mike_robot_mix_1001_v3.mp3')&&ht27Song().readyState>=3&&ht27Song().volume>0&&!ht27Song().muted"),'new recording is decoded and playing through HAMA music')
  # Capture this element's real audio, not a separately muxed replacement.
  capture=p.evaluate("""async()=>{const m=ht27Song(),sound=m.captureStream(),stream=cv.captureStream(30);for(const t of sound.getAudioTracks())stream.addTrack(t);const C=new AudioContext();await C.resume();const src=C.createMediaStreamSource(sound),an=C.createAnalyser();src.connect(an);an.fftSize=2048;window.voiceMeter={C,an};window.chunks=[];window.rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:1800000});rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};rec.start(500);return {tracks:stream.getAudioTracks().length,clock:m.currentTime};}""")
  out['capture']=capture;check(capture['tracks']==1,'recording captures the single real mixed audio stream')
  deadline=time.monotonic()+44
  while time.monotonic()<deadline:
   p.wait_for_timeout(400)
   row=p.evaluate("""()=>{const a=new Float32Array(voiceMeter.an.fftSize);voiceMeter.an.getFloatTimeDomainData(a);return {media:ht27Song().currentTime,game:boss._hammerTime.clock,lines:boss._hammerTime.hama.lines.map(l=>l.text),rms:Math.sqrt(a.reduce((s,x)=>s+x*x,0)/a.length),paused:ht27Song().paused};}""");out['samples'].append(row)
   if 15<row['media']<15.6:shot(p,'lead-in-game')
   if 33<row['media']<33.6:shot(p,'crew-in-game')
  data=p.evaluate("""async()=>{await new Promise(resolve=>{rec.onstop=resolve;rec.stop();});const b=new Blob(chunks,{type:'video/webm'});return await new Promise(resolve=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(b);});}""")
  (O/'hama-vocal-gameplay.webm').write_bytes(base64.b64decode(data.split(',')[1]));p.evaluate('()=>voiceMeter.C.close()')
  drift=sorted(abs(r['media']-r['game']) for r in out['samples']);out['clockDrift']={'max':max(drift),'p95':drift[int(len(drift)*.95)]}
  check(out['clockDrift']['p95']<.05 and out['clockDrift']['max']<.25,'fight follows the single media clock (frame-lag samples recorded)')
  check(any(r['rms']>.03 for r in out['samples'] if 15<r['media']<30),'instrumental section keeps playing with removed verses')
  check(all(not r['lines'] for r in out['samples'] if 12<r['media']<30),'removed verses leave the singing captions clear')
  check(any(any('CANT TOUCH' in s for s in r['lines']) for r in out['samples']),'background hook is captioned in game')
  p.evaluate("()=>setState('paused')");p.wait_for_timeout(150);t=p.evaluate('()=>ht27Song().currentTime');p.wait_for_timeout(250)
  check(p.evaluate('t=>state===\'paused\'&&ht27Song().paused&&Math.abs(ht27Song().currentTime-t)<.02',t),'pause stops the whole vocal/music mix')
  p.evaluate('()=>setState(GS.PLAY)');p.wait_for_timeout(300);check(p.evaluate('t=>!ht27Song().paused&&ht27Song().currentTime>t',t),'resume continues from the same position')
  # Actual seek then a real second through both slam syllables.
  p.evaluate("()=>{const d=boss._hammerTime;d.hama.stopFlags={};d.mode='dance';d.t=0;d.duration=5;d.locked=false;boss._hammer.frRecovery=false;hammerState(boss,'hammer');ht27Song().currentTime=60.8;}");p.wait_for_timeout(2100)
  out['slamState']=p.evaluate('()=>({slams,clock:ht27Song().currentTime,game:boss._hammerTime.clock,mode:boss._hammerTime.mode,state:boss._hammer.state,protected:ht27CombatSequence(boss)})')
  check(p.evaluate("()=>slams.some(q=>q.word==='HAMMER'&&Math.abs(q.t-61.8)<.08)&&slams.some(q=>q.word==='TIME!'&&Math.abs(q.t-(61.8+HAMA_P))<.08)"),'instrumental choreography retains both physical slam cues');shot(p,'slam-in-game')
  p.evaluate("()=>{const d=boss._hammerTime;d.mode='dance';d.t=0;d.duration=5;d.locked=false;boss._hammer.frRecovery=false;hammerState(boss,'hammer');ht27Song().currentTime=102.1;}");p.wait_for_timeout(500);shot(p,'breakdown-in-game')
  check(p.evaluate("()=>boss._hammerTime.hama.lines.some(l=>l.text.includes('OH'))&&HAMA_VOCALS_1001.captions.every(l=>['CANT TOUCH THIS','OH! OH-OH!'].includes(l.text))"),'only hook and recorded OH chant captions remain')
  p.evaluate('()=>{ht27Song().currentTime=179.7;}');p.wait_for_timeout(1100)
  check(p.evaluate('()=>ht27Song().currentTime<3&&!ht27Song().paused&&boss._hammerTime.clock<3'),'track loops without a second voice player drifting')
  p.evaluate('()=>setState(GS.TITLE)');p.wait_for_timeout(100)
  check(p.evaluate('()=>!ht27Active&&Snd.music.hama.paused&&Snd.cur!==Snd.music.hama'),'exit stops the vocal mix')
  p.evaluate("()=>{setState(GS.PASSWORD);pwInput='HAMMER';submitPassword();startRun(PENDING_STAGE);}");p.wait_for_function('()=>boss?._hammerTime.musicStarted',timeout=120000)
  check(p.evaluate("()=>ht27SongName()==='hammerTime'&&!ht27Song().src.includes('hama_mike_robot')"),'HAMMER retains its separate remix');p.evaluate('()=>setState(GS.TITLE)')
  check(not errors,'no page or console errors');br.close()
finally:
 stop();out['errors']=errors;(O/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
sys.exit(0 if out['checks'] and all(q['ok'] for q in out['checks']) and not errors else 1)
