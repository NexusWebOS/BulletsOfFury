"""Native renderer and real component damage checks for Chronos commitment."""
from pathlib import Path
import ast,json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_readability_1025/probe';O.mkdir(parents=True,exist_ok=True)
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
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function("window.__bofFrames>5&&typeof C34!=='undefined'&&typeof c32Warm==='function'",timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;c32Warm();c30Warm();c29Warm();bi24Warm();ht23Warm();c25Warm();c26Warm();c27Warm();ch23Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return [stageLoadReady(5),c32Warm(),c30Warm(),c29Warm(),bi24Warm(),ht23Warm(),ch23Warm(),c25Warm(),c26Warm(),c27Warm()].every(Boolean)}',timeout=180000);p.evaluate(seed)
  p.evaluate("()=>{window.fresh=()=>{seedGun();boss._hammer.c30=null;boss._hammer.c29Break=null;boss._hammer.c29GunTime=0;boss._hammer.c27RagePending=false;};window.armGun=()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.hb20PickupDone=h.hammerDestroyed=true;h.mode='chaingun';h.chainHP=h.chainMax=1000;h.chainDestroyed=false;hammerChainStart(boss);boss.x=340;boss.y=220;};}")
  def shot(name):
   p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
  p.evaluate("()=>{fresh();boss._hammer.hb20Pickup=null;boss._hammer.state='hammer';boss._hammer.frArmor.hp=8415;boss._hammer.frArmor.activated=true;BOFCinematicDirector.play('ht23-announcement-proof',[{who:'CHRONOS',text:'Chromium Armor, Activated!'}],()=>{},true);}")
  p.wait_for_timeout(500);shot('dialogue');ck('Dialogue uses a visible authored window',p.evaluate('C34.radio?.who==="CHRONOS"&&UI20.dialogue?.w>300'))
  before=p.evaluate('_stage5SpaceScroll');p.evaluate(STEP,20);ck('Dialogue leaves background scrolling',p.evaluate('_stage5SpaceScroll')>before)
  p.evaluate("()=>{BOFCinematicDirector.cancel();const h=boss._hammer;h.hb20Pickup=null;h.state='fr_activation';h.t=1.4;}");shot('chrome-charge')
  p.evaluate("()=>{const h=boss._hammer;h.state='whirlwind';h.c26SpinClock=3;}");shot('chrome-spin');ck('Spin selects chromium plate',p.evaluate("ha21Blue(boss)?.a.bank==='spin_chrome'"))
  p.evaluate("()=>{const h=boss._hammer;h.state='c27_depth_combo';h.c27Combo=hj22Pair(boss,'blue',{x:340,y:480});h.c27Combo.scale=1.25;h.c27Combo.clock=.9;c27ComboTick(boss,h.c27Combo);}");shot('side-fov');ck('Depth combo restores swing warning renderer',p.evaluate('C34.warnings>0'))
  p.evaluate("()=>{boss._hammer.c27Combo=null;eBullets=[];c27MissileRing(boss,0);}");shot('laser-ring');ck('Slam launches chromium lasers and no missiles',p.evaluate("eBullets.length===16&&eBullets.every(q=>q._hammerLaser&&q._c34Chromium&&q.kind==='eglaser')"))
  ck('No browser errors',not errors,errors);br.close()
finally:stop()
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
print(json.dumps(checks));assert all(c['passed'] for c in checks)
