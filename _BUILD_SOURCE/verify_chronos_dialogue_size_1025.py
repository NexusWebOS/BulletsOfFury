"""Native renderer and real component damage checks for Chronos commitment."""
from pathlib import Path
import ast,json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_dialogue_size_1025/probe';O.mkdir(parents=True,exist_ok=True)
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
  p.evaluate("()=>{ui20Radio=()=>({who:'DECKER - HQ',text:'Its core is spiking! Snap out of it - get your hands back on the stick, NOW!',age:1,duration:5});XART.rdy(commPortrait('decker','talk'));XART.rdy(commPortrait('decker','idle'));}")
  p.wait_for_function("XART.rdy(commPortrait('decker','talk'))&&XART.rdy(commPortrait('decker','idle'))")
  p.evaluate('drawWorld(0)');p.wait_for_timeout(2500);shot('decker-portrait')
  q=p.evaluate('UI20.dialogue');ck('Decker resolves actual portrait',bool(q.get('portrait')),q);ck('Decker name normalized',q.get('who')=='DECKER',q.get('color'));ck('Decker uses compact fixed height',q['h']==94);ck('Decker text fits aperture',q['layout']['height']<=q['text']['h'])
  p.evaluate("()=>{ui20Radio=()=>({who:'???',text:'.........',age:1,duration:5});XART.rdy('fb1002_hammer_portrait');}")
  p.wait_for_function("XART.rdy('fb1002_hammer_portrait')")
  shot('chronos-portrait');q=p.evaluate('UI20.dialogue');ck('Unknown Chronos opening uses authored portrait',q.get('portrait')=='fb1002_hammer_portrait',q)
  ck('Chronos uses same fixed height',q['h']==94);ck('No browser errors',not errors,errors);br.close()
finally:stop()
print(json.dumps(checks));assert all(c['passed'] for c in checks)
