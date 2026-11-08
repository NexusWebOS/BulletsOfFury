from pathlib import Path
import json,hashlib,zipfile,os,subprocess,time,re,urllib.request,urllib.parse,sys
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');receipt=json.loads((W/'package.json').read_text());Z=Path(receipt['path']);E=W/'Clean Extracted Tester Copy';E.mkdir(exist_ok=True);checks=[];errors=[];missing=[];external=[]
def ck(n,v,data=None):checks.append(dict(name=n,passed=bool(v),data=data));print('PASS'if v else'FAIL',n,str(data)[:250]if data is not None else'',flush=True)
with zipfile.ZipFile(Z)as z:
 prefix=receipt['prefix'];manifest=json.loads(z.read(prefix+'FILE-MANIFEST.json'));expected={row['path']:row for row in manifest['files']};verified=0
 for i,info in enumerate(z.infolist()):
  target=(E/info.filename).resolve();assert target.is_relative_to(E.resolve());target.parent.mkdir(parents=True,exist_ok=True);h=hashlib.sha256()
  with z.open(info)as src,target.open('wb')as dst:
   for chunk in iter(lambda:src.read(1024*1024),b''):h.update(chunk);dst.write(chunk)
  rel=info.filename[len(prefix):]
  if rel in expected:assert h.hexdigest()==expected[rel]['sha256']and target.stat().st_size==expected[rel]['bytes'];verified+=1
  if i%2000==0:print('VERIFY_EXTRACT',i,'/',len(z.infolist()),flush=True)
root=E/prefix.rstrip('/');ck('All ZIP entries extract with valid CRC and all payload SHA256 hashes match',verified==len(expected),{'verified':verified,'entries':len(expected)+1})
ck('Package includes all current game assets and extensions',len([n for n in expected if n.startswith('assets/')])==18674 and len([n for n in expected if n.startswith('extensions/')])==91)
ck('Latest boss owners and the exact requested core controls are packaged',all((root/n).is_file()for n in ['assets/razorwake_tempest_1105.js','assets/thunderhead_reactor_1105.js','assets/sumpjaw_tandem_1105.js'])and hashlib.sha256((root/'assets/game.js').read_bytes()).hexdigest()==receipt['build']['gameJsSha256'])
ps=Path(os.environ['SystemRoot'])/'System32/WindowsPowerShell/v1.0/powershell.exe';env={**os.environ,'PATH':str(Path(os.environ['SystemRoot'])/'System32')+';'+str(ps.parent)};process=None;log=None
def launch(port):
 global process,log
 log=(W/f'package-server-{port}.log').open('w',encoding='utf8');process=subprocess.Popen([str(ps),'-NoLogo','-NoProfile','-ExecutionPolicy','Bypass','-File',str(root/'PLAY_LOCAL.ps1'),'-NoBrowser','-Port',str(port),'-DurationSeconds','1800'],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
 deadline=time.monotonic()+60;path=Path(log.name)
 while time.monotonic()<deadline:
  s=path.read_text(encoding='utf8',errors='replace');m=re.search(r'BULLETS OF FURY READY: (http://127\.0\.0\.1:\d+/index\.html)',s)
  if m:return m[1]
  if process.poll()is not None:raise RuntimeError(s)
  time.sleep(.2)
 raise RuntimeError('Local Windows launcher did not become ready: '+s)
def stop():
 global process,log
 if process and process.poll()is None:process.terminate();process.wait(timeout=20)
 if log:log.close()
url=launch(0);port=urllib.parse.urlparse(url).port;ck('Extracted Windows launcher runs without Python or Node on PATH',True,{'url':url,'path':env['PATH']})
try:
 with urllib.request.urlopen(urllib.request.Request(url.replace('/index.html','/assets/game/shared/audio/sounds/goodluck.mp3'),headers={'Range':'bytes=0-255'}),timeout=10)as f:ck('Standalone server supports real audio byte ranges',f.status==206 and len(f.read())==256)
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda f:missing.append(f.url)if f.status>=400 and urllib.parse.urlparse(f.url).hostname=='127.0.0.1'else None)
  p.on('console',lambda m:errors.append(m.text[:500])if(m.type=='error'or'draw error'in m.text.lower())and not('net::ERR_FAILED'in m.text and external)else None)
  def route(q):
   if urllib.parse.urlparse(q.request.url).hostname in ['127.0.0.1','localhost']:q.continue_()
   else:external.append(q.request.url);q.abort()
  p.route('**/*',route);p.goto(url+'?quality=high',wait_until='load',timeout=240000);p.wait_for_function('window.__bofFrames>5',timeout=60000);p.mouse.click(3,3);p.screenshot(path=str(W/'packaged-start.png'));ck('Clean extracted game boots offline with normal player vulnerability',p.evaluate('()=>!DBGT.god&&typeof reviewBot===\'undefined\'')and not errors)
  p.evaluate("()=>{localStorage.setItem('bof_package_save_probe','persisted');setState(GS.TITLE);}");p.keyboard.press('Space');p.wait_for_timeout(300);ck('Space remains a working menu Confirm control',p.evaluate('()=>state!==GS.TITLE'))
  p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  for stage in range(1,10):
   p.evaluate("s=>{EA11.setup(s,'furious');stagePlan=[];waveIdx=0;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;debugUnlocked=true;DBGT.god=true;}",stage)
   p.wait_for_function('s=>{stageLoadTick();return stageLoadReady(s)}',arg=stage,timeout=240000);p.wait_for_timeout(300);p.screenshot(path=str(W/f'packaged-stage{stage}.png'));ck('Extracted Stage '+str(stage)+' loads and renders',not errors and not missing)
  p.evaluate("()=>{EA11.setup(7,'furious');spawnSubBoss('dualscoopdredger');}");p.wait_for_function('()=>{stageLoadTick();return sj98Ready()&&stageLoadReady(7)}',timeout=180000);ck('Current Sumpjaw pair and mouth/core atlas decode from the ZIP',p.evaluate('()=>!!subBoss._sj120&&subBoss.maxhp===14000&&SJ120.keys.every(k=>XART.rdy(k))'))
  p.evaluate("()=>{EA11.setup(6,'furious');spawnSubBoss('razorwake');}");p.wait_for_function('()=>{stageLoadTick();return fb112Ready()&&stageLoadReady(6)}',timeout=240000);ck('Current Razorwake and Thunderhead assets/masks decode from the ZIP',p.evaluate('()=>!!subBoss._rw118&&!!TC119.bits&&!!RW118.bits&&TC119.keys.every(k=>XART.rdy(k))'))
  p.evaluate("()=>{Audio.stopMusic();Audio.resume();}");audio=p.evaluate('''async()=>{const c=Snd._audioCtx();await c.resume();const a=c.createAnalyser();a.fftSize=2048;BOF_AUDIO_QUALITY_1102.tap().connect(a);Snd.prepare('enemyMachineGunHeavy');await new Promise(r=>setTimeout(r,500));Snd.play('enemyMachineGunHeavy');let peak=0;for(let i=0;i<20;i++){await new Promise(r=>setTimeout(r,25));const f=new Float32Array(2048);a.getFloatTimeDomainData(f);for(const v of f)peak=Math.max(peak,Math.abs(v));}return{peak,errors:AQ112.errors};}''');ck('Packaged shared mixer plays decoded combat sound',audio['peak']>.00001 and not audio['errors'],audio)
  stop();new_url=launch(port);p.goto(new_url,wait_until='load',timeout=240000);p.wait_for_function('window.__bofFrames>5');ck('Same-origin launcher restart preserves saves and control preferences',new_url==url and p.evaluate('()=>localStorage.getItem(\'bof_package_save_probe\')===\'persisted\'&&keybind.bomb.includes(\' \')&&keybind.retina.includes(\'mouse2\')'))
  ck('No missing packaged resources or JavaScript errors',not missing and not errors,{'missing':missing,'errors':errors});b.close()
finally:stop()
(W/'package-checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,missing=missing,blockedExternalRequests=external,extractedRoot=str(root),archive=receipt['path']),indent=2));print('PACKAGE_CHECKS',sum(c['passed']for c in checks),'/',len(checks));raise SystemExit(0 if all(c['passed']for c in checks)else 1)
