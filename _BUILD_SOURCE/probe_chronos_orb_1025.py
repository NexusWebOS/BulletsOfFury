"""Native renderer and real component damage checks for Chronos commitment."""
from pathlib import Path
import ast,json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_orb_1025/probe';O.mkdir(parents=True,exist_ok=True)
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
  p.evaluate("XART.get('c41_wave')")
  p.wait_for_function("XART.rdy('c41_wave')")
  out=O.parent/'frames';out.mkdir(exist_ok=True)
  p.wait_for_function("Array.from({length:8},(_,i)=>XART.rdy('c42_bolt_'+i)).every(Boolean)")
  p.evaluate("()=>{fresh();boss.x=240;boss.y=160;boss.flash=0;boss._hammer.hb20Pickup=null;boss._hammer._hf22Red=true;c30Start(boss);boss._hammer.c30={phase:'gather',t:0,scale:1,cycle:0,hit:new Set(),lock:{x:240,y:620}};}")
  for i in range(126):
   q=p.evaluate("i=>{const t=i/30,R=boss._hammer.c30;R.phase=t<1.7?'gather':t<2.06?'thrust':t<3.41?'beam':'recover';R.t=t<1.7?t:t<2.06?t-1.7:t<3.41?t-2.06:t-3.41;efxClock+=1/30;drawWorld(0);return {orb:C42.lastOrb,line:c30Line(boss),storm:C33.lastDraw};}",i)
   p.screenshot(path=str(out/f'{i:03d}.png'))
   if i==45:ck('Orb red before blast',q['orb']['charge']==1)
   if i==80:ck('Beam originates at orb',abs(q['orb']['y']-q['line']['from']['y'])<.01 and q['storm']['pixellab'])
  ck('24 smooth sustain frames',p.evaluate("new Set(Array.from({length:24},(_,i)=>c41Frame(.16+(i+.5)/24,3))).size===24"))
  ck('No browser errors',not errors,errors);br.close()
finally:stop()
import subprocess,imageio_ffmpeg
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-framerate','30','-i',str(out/'%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(O.parent/'orb-charge-blast.mp4')],check=True)
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));assert all(c['passed'] for c in checks)
