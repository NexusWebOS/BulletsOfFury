from pathlib import Path
import subprocess,time,json,ctypes
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;ROOT=W/'qa/Installed BOF';Q=W/('qa/restart-'+str(int(time.time())));Q.mkdir(exist_ok=True);PROFILE=W/'qa/game-profile';checks=[];port=48976
def ck(n,v):checks.append(dict(name=n,passed=bool(v)));print('PASS'if v else'FAIL',n,flush=True)
def log():return [json.loads(x)for x in(Q/'desktop.jsonl').read_text().splitlines()]if(Q/'desktop.jsonl').exists()else[]
def start(direct,pw):
 args=[str(ROOT/'Bullets of Fury.exe'),'--qa-dir',str(Q),'--profile',str(PROFILE),'--debug-port',str(port)]+(['--game']if direct else[]);before=len(log());p=subprocess.Popen(args)
 if not direct:
  until=time.monotonic()+30
  while not any(r['name']=='doors-open'for r in log()[before:]):
   if time.monotonic()>until:raise RuntimeError('Launcher not ready')
   time.sleep(.1)
  h=ctypes.windll.user32.FindWindowW(None,'Bullets of Fury - Fury HQ');assert h;ctypes.windll.user32.PostMessageW(h,0x100,13,0);ctypes.windll.user32.PostMessageW(h,0x101,13,0)
 until=time.monotonic()+60
 while True:
  try:b=pw.chromium.connect_over_cdp(f'http://127.0.0.1:{port}');break
  except:
   if time.monotonic()>until:raise
   time.sleep(.2)
 page=b.contexts[0].pages[0];page.wait_for_function('window.__bofFrames>5',timeout=180000);return p,b,page
p=None
try:
 with sync_playwright()as pw:
  p,b,page=start(False,pw);ck('Native desktop save and controls survive restarting the EXE',page.evaluate("()=>localStorage.getItem('bof_desktop_save_probe')==='kept'&&keybind.bomb.includes(' ')&&keybind.retina.includes('mouse2')"));page.evaluate('()=>window.close()');time.sleep(1.8);h=ctypes.windll.user32.FindWindowW(None,'Bullets of Fury - Fury HQ');ck('The real game Exit action returns to the graphical launcher',any(r['name']=='game-closed'for r in log())and p.poll()is None and h and ctypes.windll.user32.IsWindowVisible(h));ctypes.windll.user32.PostMessageW(h,0x10,0,0);p.wait(timeout=20);p=None
  try:b.close()
  except:pass
  p,b,page=start(True,pw);ck('Direct fullscreen EXE restart also preserves the same save origin',page.evaluate("()=>localStorage.getItem('bof_desktop_save_probe')==='kept'&&location.hostname==='bof.coleforge.local'&&!DBGT.god"));page.evaluate('()=>window.close()');p.wait(timeout=20);ck('Closing the standalone game exits its process cleanly',p.returncode==0);p=None
  try:b.close()
  except:pass
finally:
 if p and p.poll()is None:p.terminate();p.wait(timeout=15)
(W/'qa/restart-checks.json').write_text(json.dumps(dict(checks=checks),indent=2));raise SystemExit(0 if all(x['passed']for x in checks)else 1)
