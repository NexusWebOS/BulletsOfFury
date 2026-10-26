"""Native renderer and real component damage checks for Chronos commitment."""
from pathlib import Path
import ast,json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_flight_1025/probe';O.mkdir(parents=True,exist_ok=True)
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
  p.evaluate("armGun();boss._hammer.state='chaingun';")
  for t in [0,2,4.99,5.01]:
   q=p.evaluate("""t=>{const h=boss._hammer;h.c29GunTime=t;h.chainHP=1000;boss._hammerModuleHit='chaingun';hammerBossDamage(boss,100);return {hp:h.chainHP,flash:h.ch23GunFlash}}""",t)
   ck('Gun protection at '+str(t),q['hp']==1000 if t<5 else q['hp']<1000,q)
  p.evaluate('()=>{for(let i=0;i<15;i++){hammerBossTick(boss,1/60);boss.flash=Math.max(0,(boss.flash||0)-1/60);}}');shot('blue-gun')
  ck('Gun hit flash expires',p.evaluate('boss._hammer.ch23GunFlash===0'))
  p.evaluate("()=>{fresh();boss._hammer._hf22Red=true;boss._hammer._hf22Charge=null;boss._hammer.hb20Pickup=null;boss._hammer.c30={scale:1.08,cycle:1};c30Retreat(boss);}")
  for t in [.35,.7,1,1.55]:
   q=p.evaluate("""t=>{const R=boss._hammer.c30;R.t=t;c35DepthFlight(boss,R,.42);boss._drawY=boss.y;return {y:boss.y,scale:R.scale,top:viewTopY()}}""",t)
   shot('depth-'+str(t));ck('Depth flight '+str(t),q['scale']==(1.08 if t<.7 else .42),q)
  p.evaluate("()=>{const R=boss._hammer.c30;R.cycle=3;c30Retreat(boss);R.t=.7;c35DepthFlight(boss,R,1.08);}");ck('Return changes scale only offscreen',p.evaluate('boss.y<viewTopY()-200&&boss._hammer.c30.scale===1.08'))
  p.evaluate("()=>{fresh();boss._hammer.hb20Pickup=null;boss._hammer.state='hammer';}")
  p.evaluate("()=>{window.drawToolProof=()=>{drawWorld(0);c35Tool({x:340,y:350},0,0);};drawToolProof();}")
  p.screenshot(path=str(O/'thrown-hammer.png'))
  p.evaluate("()=>{fresh();boss._hammer._hf22Red=true;boss._hammer._hf22Charge=null;boss._hammer.hb20Pickup=null;boss._hammer.c30={scale:.42,cycle:2,phase:'beam',t:1.2,lock:{x:340,y:650}};boss.x=340;boss.y=160;}")
  frames=[]
  for t in [1.2,1.3]:
   p.evaluate('t=>boss._hammer.c30.t=t',t);shot('wave-end-'+str(t));frames.append(p.evaluate('C30.lastBeam.frame'))
  ck('Wave plays both authored terminal frames',frames==[6,7],frames)
  ck('No browser errors',not errors,errors);br.close()
finally:stop()
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
print(json.dumps(checks));assert all(c['passed'] for c in checks)
