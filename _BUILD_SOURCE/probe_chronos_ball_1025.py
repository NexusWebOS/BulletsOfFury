"""Native renderer and real component damage checks for Chronos commitment."""
from pathlib import Path
import ast,json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_ball_1025/probe';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 if not ok:print(json.dumps(data),flush=True)
src=ast.parse((R/'_BUILD_SOURCE/audit_chronos_aura_gun_1025.py').read_text(encoding='utf8'))
seed=next(n.args[0].value for n in ast.walk(src) if isinstance(n,ast.Call) and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str) and 'window.seedGun=' in n.args[0].value)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function("window.__bofFrames>5&&typeof C35!=='undefined'&&typeof c32Warm==='function'",timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;c32Warm();c30Warm();c29Warm();bi24Warm();ht23Warm();c25Warm();c26Warm();c27Warm();ch23Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return [stageLoadReady(5),c32Warm(),c30Warm(),c29Warm(),bi24Warm(),ht23Warm(),ch23Warm(),c25Warm(),c26Warm(),c27Warm()].every(Boolean)}',timeout=180000);p.evaluate(seed)
  p.evaluate("()=>{window.fresh=()=>{seedGun();boss._hammer.c30=null;boss._hammer.c29Break=null;boss._hammer.c29GunTime=0;boss._hammer.c27RagePending=false;};window.armGun=()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.hb20PickupDone=h.hammerDestroyed=true;h.mode='chaingun';h.chainHP=h.chainMax=1000;h.chainDestroyed=false;hammerChainStart(boss);boss.x=340;boss.y=220;};}")
  def shot(name):
   p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
  p.evaluate("()=>{fresh();boss._hammer.hb20Pickup=null;boss.x=340;boss.y=250;boss.flash=0;}")
  keys=[];out=O.parent/'frames';out.mkdir(exist_ok=True)
  for i in range(120):
   q=p.evaluate("i=>{const h=boss._hammer;h.state=i<60?'curl':'uncurl';h.t=(i<60?i/59*HAMMER_BALL_WARN:(i-60)/59*1.65);const q=ha21Blue(boss);drawWorld(0);return {key:q.a.key,k:q.k};}",i);keys.append(q);p.screenshot(path=str(out/f'{i:03d}.png'))
  ck('Eleven distinct authored fold poses',len(set(q['key'] for q in keys))==11)
  ck('Fixed proportional scale',all(q['k']==1.75 for q in keys))
  ck('Reverse animation returns to original pose',keys[0]==keys[-1])
  ck('No browser errors',not errors,errors);br.close()
finally:stop()
import subprocess,imageio_ffmpeg
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-framerate','30','-i',str(out/'%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(O.parent/'ball-fold.mp4')],check=True)
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));assert all(c['passed'] for c in checks)
