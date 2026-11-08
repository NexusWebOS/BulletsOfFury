from pathlib import Path
import subprocess,time,json,urllib.request,ctypes,hashlib
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');ROOT=W/'qa/Installed BOF';EXE=ROOT/'Bullets of Fury.exe';Q=W/('qa/game-'+str(int(time.time())));Q.mkdir(exist_ok=True);PROFILE=W/'qa/game-profile';PORT=48973;checks=[];errors=[];missing=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,str(d)[:160]if d is not None else'',flush=True)
def logs():
 f=Q/'desktop.jsonl';return [json.loads(l)for l in f.read_text().splitlines()]if f.exists()else[]
def launch(direct=False):
 args=[str(EXE),'--qa-dir',str(Q),'--profile',str(PROFILE),'--debug-port',str(PORT)]
 if direct:args.append('--game')
 proc=subprocess.Popen(args,cwd=ROOT)
 if not direct:
  until=time.monotonic()+40
  while time.monotonic()<until:
   if any(r['name']=='doors-open'for r in logs()):break
   if proc.poll()is not None:raise RuntimeError('Launcher exited early: '+str(logs()))
   time.sleep(.2)
  h=ctypes.windll.user32.FindWindowW(None,'Bullets of Fury - Fury HQ');assert h
  ctypes.windll.user32.PostMessageW(h,0x100,0x0D,0);ctypes.windll.user32.PostMessageW(h,0x101,0x0D,0)
 until=time.monotonic()+65
 while time.monotonic()<until:
  try:
   with urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json/version',timeout=1)as f:json.load(f)
   return proc
  except Exception:
   if proc.poll()is not None:raise RuntimeError('Game window exited early: '+str(logs()))
   time.sleep(.3)
 raise RuntimeError('Native WebView2 debug endpoint did not open: '+str(logs()))
proc=None
try:
 with sync_playwright()as pw:
  proc=launch();b=pw.chromium.connect_over_cdp(f'http://127.0.0.1:{PORT}');context=b.contexts[0];p=context.pages[0];p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda f:missing.append(f.url)if f.status>=400 and'bof.coleforge.local'in f.url else None)
  p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.screenshot(path=str(Q/'fullscreen-title.png'))
  ck('Installed EXE launches the real local game in its own WebView2 window',p.url.startswith('https://bof.coleforge.local/index.html')and p.evaluate('()=>!!document.querySelector("canvas")'))
  row=[r for r in logs()if r['name']=='game-navigation'][-1]['data'];ck('Game starts fullscreen and occupies the screen',row['fullscreen']and row['bounds']==row['screen'],row)
  ck('Normal startup has no recording bot or GOD mode',p.evaluate('()=>!DBGT.god&&typeof reviewBot===\'undefined\''))
  p.keyboard.press('F11');p.wait_for_timeout(400);ck('F11 changes the actual native window to windowed mode',any(r['name']=='fullscreen'and not r['data']['enabled']for r in logs()))
  p.keyboard.press('Alt+Enter');p.wait_for_timeout(400);ck('Alt+Enter restores the native fullscreen window',[r for r in logs()if r['name']=='fullscreen'][-1]['data']['enabled'])
  p.evaluate("()=>localStorage.setItem('bof_desktop_save_probe','kept')")
  ck('Desktop build preserves the requested default mouse controls',p.evaluate("()=>keybind.retina.includes('mouse2')&&keybind.bomb.includes(' ')&&keybind.multilock.includes('mouse3')"))
  p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  p.evaluate("()=>{EA11.setup(1,'furious');stagePlan=[];waveIdx=0;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;debugUnlocked=true;DBGT.god=true;run.bombs=40;player.invuln=0;spawnSubBoss('razorback');}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',timeout=180000,polling=100)
  # Bring the real native window to the foreground before measuring its game loop.
  hwnd=ctypes.windll.user32.FindWindowW(None,'Bullets of Fury');ctypes.windll.user32.SetForegroundWindow(hwnd)
  # Record the cold compositor, then test the warmed loop without reducing quality.
  a=p.evaluate('window.__bofFrames');start=time.monotonic();p.wait_for_timeout(5000);fps=(p.evaluate('window.__bofFrames')-a)/(time.monotonic()-start);ck('Cold native fullscreen combat loop is measured at original SS2 quality',fps>15,{'fps':round(fps,2)})
  p.wait_for_timeout(5000);a=p.evaluate('window.__bofFrames');start=time.monotonic();p.wait_for_timeout(6000);fps=(p.evaluate('window.__bofFrames')-a)/(time.monotonic()-start);ck('Warmed native fullscreen combat is measured at original SS2 quality',fps>15,{'fps':round(fps,2),'comparison':'see paired-performance.json; not a 60 FPS claim'})
  p.screenshot(path=str(Q/'fullscreen-combat.png'));p.evaluate('''()=>{window.oldRAF1106=requestAnimationFrame;requestAnimationFrame=()=>0;cancelAnimationFrame(window.raf);window.fixture1106=()=>{Input.cancelMouseRetina();EA11.setup(1,'furious');stagePlan=[];waveIdx=0;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;debugUnlocked=true;DBGT.god=true;run.bombs=40;player.invuln=0;spawnSubBoss('razorback');};fixture1106();}''')
  # Stop the captured RAF chain at the following browser task, using the same
  # deterministic trap as the production game's existing verification helper.
  from sys import path as syspath
  syspath.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
  p.evaluate(TRAP_RAF)
  def step(n):p.evaluate('(n)=>{for(let i=0;i<n;i++)updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}',n)
  def reset():
   p.evaluate('fixture1106');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',polling=100);step(220)
   for _ in range(25):
    if p.evaluate('()=>_lockTargets().length>=2'):break
    step(30);p.wait_for_timeout(25)
  reset();rect=p.evaluate('()=>{const r=cv.getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height}}');x=rect['x']+rect['width']*.5;y=rect['y']+rect['height']*.75;p.mouse.move(x,y)
  p.mouse.down(button='right');step(40);ck('Native app right click Retina locks without firing missiles',p.evaluate('()=>retina.phase===\'locked\'&&!!retina.target&&run.bombs===40'));p.mouse.up(button='right');p.keyboard.press('Space');step(3);ck('Native app Space launches the real missile',p.evaluate('run.bombs')==39)
  reset();cdp=context.new_cdp_session(p);cdp.send('Input.dispatchMouseEvent',dict(type='mousePressed',x=x,y=y,button='back',buttons=8,clickCount=1));step(110);ck('Native app Mouse4 scans multiple real targets',p.evaluate('()=>retinaScanHeld()&&player._retinaScan.marks.length>=2'));p.keyboard.press('Space');step(100);ck('Native app Space releases the marked-target missile volley',p.evaluate('run.bombs')<39);cdp.send('Input.dispatchMouseEvent',dict(type='mouseReleased',x=x,y=y,button='back',buttons=0,clickCount=1))
  reset();p.mouse.click(x,y,button='right',delay=35);p.wait_for_timeout(50);p.mouse.down(button='right');step(110);ck('Native app double right tap and hold enters Multi-Retina',p.evaluate('()=>Input.mouseMultiRetina&&player._retinaScan.marks.length>=2'));p.mouse.up(button='right');step(1);ck('Native app releases the hold cleanly',p.evaluate('()=>!Input.mouseMultiRetina&&!retinaScanHeld()'))
  for stage in [2,5,6,7,8,9]:
   p.evaluate("s=>{EA11.setup(s,'furious');stagePlan=[];waveIdx=0;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;DBGT.god=true;}",stage);p.wait_for_function('s=>{stageLoadTick();return stageLoadReady(s)}',arg=stage,timeout=180000,polling=100);step(2);ck('Installed native Stage '+str(stage)+' loads and renders',not errors and not missing)
  ck('No missing installed local assets or page errors',not missing and not errors,dict(missing=missing,errors=errors))
  p.evaluate('()=>window.close()');time.sleep(1.8);ck('The game Exit action returns to the graphical launcher',any(r['name']=='game-closed'for r in logs())and proc.poll()is None)
  h=ctypes.windll.user32.FindWindowW(None,'Bullets of Fury - Fury HQ');ck('Launcher is visible again after closing game',bool(h)and ctypes.windll.user32.IsWindowVisible(h));ctypes.windll.user32.PostMessageW(h,0x10,0,0);proc.wait(timeout=20);b.close();proc=None
  proc=launch(True);b=pw.chromium.connect_over_cdp(f'http://127.0.0.1:{PORT}');p=b.contexts[0].pages[0];p.wait_for_function('window.__bofFrames>5',timeout=180000);ck('Native game save and controls persist across EXE restarts',p.evaluate("()=>localStorage.getItem('bof_desktop_save_probe')==='kept'&&keybind.bomb.includes(' ')&&keybind.retina.includes('mouse2')"));p.evaluate('()=>window.close()');proc.wait(timeout=20);proc=None;b.close()
finally:
 if proc and proc.poll()is None:proc.terminate();proc.wait(timeout=15)
 (W/'qa/desktop-checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,missing=missing),indent=2))
print('DESKTOP_CHECKS',sum(c['passed']for c in checks),'/',len(checks),flush=True);raise SystemExit(0 if all(c['passed']for c in checks)else 1)
