"""Native renderer and real component damage checks for Chronos commitment."""
from pathlib import Path
import ast,json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_chromium_1025/probe';O.mkdir(parents=True,exist_ok=True)
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
  p.evaluate("()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.state='fr_activation';boss.x=340;boss.y=300;boss.flash=0;boss._lastPart=null;}")
  for t in [.65,1.2,1.8,2.4,2.9]:
   p.evaluate('t=>boss._hammer.t=t',t);shot('activation-'+str(t))
  q=p.evaluate("""()=>{const a=c29Row('hold',8,'regular'),z=c29Row('hold',8,'chrome'),read=k=>{const im=XART.get(k),c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);return g.getImageData(0,0,c.width,c.height).data;};const src=read(a.key),dst=read(z.key);let alpha=true,blue=true;const counts=[];for(const step of [0,6,12,18,24]){const d=read(c38Plate(a,z,step));let changed=0;for(let i=0;i<d.length;i+=4){alpha=alpha&&d[i+3]===src[i+3];if(src[i+2]>src[i]*1.3&&src[i+2]>src[i+1]*1.1)blue=blue&&d[i]===src[i]&&d[i+1]===src[i+1]&&d[i+2]===src[i+2];if(d[i]!==src[i]||d[i+1]!==src[i+1]||d[i+2]!==src[i+2])changed++;}counts.push(changed);}return {counts,alpha,blue};}""")
  ck('Progressive authored-pixel replacement',all(a<b for a,b in zip(q['counts'],q['counts'][1:])),q)
  ck('Alpha silhouette unchanged',q['alpha']);ck('Blue energy unchanged',q['blue'])
  p.evaluate("()=>{boss._hammer.state='hammer';const A=fr27Armor(boss);A.hp=1000;A.activated=true;}");shot('plated-idle')
  ck('Persistent armor selects chrome bank',p.evaluate("ha21Blue(boss).a.key.includes('armor')"))
  ck('No browser errors',not errors,errors)
  # Short native-rendered transformation review, not a replacement full-fight recording.
  out=O.parent/'frames';out.mkdir(exist_ok=True)
  for i in range(100):
   p.evaluate("t=>{boss._hammer.state='fr_activation';boss._hammer.t=t;drawWorld(0)}",i/30)
   p.screenshot(path=str(out/f'{i:03d}.png'))
  br.close()
finally:stop()
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
import subprocess,imageio_ffmpeg
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-framerate','30','-i',str(out/'%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(O.parent/'chromium-transformation.mp4')],check=True)
assert all(c['passed'] for c in checks)
