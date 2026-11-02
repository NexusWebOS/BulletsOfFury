"""Run the actual shipped ZIPs through Chromium without duplicating the runtime."""
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json,mimetypes,threading,urllib.parse,zipfile,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/github_upload_1102';plan=json.loads((O/'plan.json').read_text());archives=[zipfile.ZipFile(x['path'])for x in plan['packages']];files={};miss=[];errors=[];checks=[]
for z in archives:
 for n in z.namelist():files[n.split('/',1)[1]]=(z,n)
lower={k.lower():k for k in files}
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  name=urllib.parse.unquote(urllib.parse.urlparse(self.path).path).lstrip('/')or'index.html';name=lower.get(name.lower(),name)
  if name not in files:miss.append(name);self.send_error(404);return
  z,key=files[name];data=z.read(key);self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(name)[0]or'application/octet-stream');self.send_header('Content-Length',str(len(data)));self.end_headers()
  try:self.wfile.write(data)
  except(ConnectionResetError,ConnectionAbortedError,BrokenPipeError):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.goto('http://127.0.0.1:'+str(server.server_port),wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.screenshot(path=str(O/'packaged-bootstrap.png'));checks.append(dict(name='Packaged runtime boots in Chromium',passed=True))
  p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  for stage in [1,6,9]:
   p.evaluate("s=>{EA11.setup(s,'furious');stagePlan=[];waveIdx=999;debugUnlocked=true;DBGT.god=true;if(s===6)spawnSubBoss('razorwake');}",stage);p.wait_for_function('s=>{stageLoadTick();return stageLoadReady(s)&&(s!==6||fb112Ready());}',arg=stage,timeout=180000);p.wait_for_timeout(1800);p.screenshot(path=str(O/f'packaged-stage{stage}.png'));checks.append(dict(name='Packaged Stage'+str(stage)+' art and runtime render',passed=not errors));print('STAGE',stage,'errors',len(errors),'missing',len(miss),flush=True)
  audio=p.evaluate('''async()=>{Audio.stopMusic();Audio.resume();const c=Snd._audioCtx();await c.resume();const a=c.createAnalyser();a.fftSize=2048;BOF_AUDIO_QUALITY_1102.tap().connect(a);Snd.prepare('enemyMachineGunHeavy');await new Promise(r=>setTimeout(r,350));Snd.play('enemyMachineGunHeavy');let peak=0;for(let i=0;i<20;i++){await new Promise(r=>setTimeout(r,25));const f=new Float32Array(2048);a.getFloatTimeDomainData(f);for(const v of f)peak=Math.max(peak,Math.abs(v));}return{peak,errors:AQ112.errors};}''');checks.append(dict(name='Packaged combat cue is audibly decoded through the mixer',passed=audio['peak']>.00001 and not audio['errors'],data=audio));b.close()
finally:
 server.shutdown()
 for z in archives:z.close()
miss=[x for x in miss if x!='favicon.ico'];checks.append(dict(name='No missing package resources or game errors',passed=not miss and not errors));out=dict(files=len(files),checks=checks,missing=miss,errors=errors);(O/'package-playback.json').write_text(json.dumps(out,indent=2));print('SUMMARY',sum(c['passed']for c in checks),'/',len(checks));sys.exit(0 if all(c['passed']for c in checks)else 1)
